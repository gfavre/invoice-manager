from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import activate, get_language
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (CreateView, FormView, RedirectView,
                                  TemplateView, UpdateView)
from django.views.generic.detail import SingleObjectMixin

from anymail.exceptions import AnymailError

from ..forms import (BaseInvoiceForm, EmailForm, InvoiceEditForm,
                     InvoiceStatusForm)
from ..models import Invoice


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = 'invoices/create.html'
    form_class = BaseInvoiceForm

    def get_success_url(self):
        # noinspection PyUnresolvedReferences
        return self.object.get_edit_url()


class InvoiceListView(LoginRequiredMixin, TemplateView):
    template_name = 'invoices/list.html'


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    form_class = InvoiceEditForm
    model = Invoice
    template_name = 'invoices/update.html'

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # noinspection PyUnresolvedReferences
    def get_initial(self):
        initial = {}
        if not self.object.due_date:
            initial['due_date'] = now() + timedelta(days=self.object.client.payment_delay_days),
        if self.object.vat_rate is None:
            initial['vat_rate'] = self.object.client.vat_rate
        return initial


class InvoiceCancelView(LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_cancel.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.canceled,
        }

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceMarkPaidView(LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_paid.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.paid,
        }

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceSnailMailUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_print.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.sent,
        }

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceDuplicateView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pk'

    def get_redirect_url(self, *args, **kwargs):
        source = get_object_or_404(Invoice, pk=kwargs['pk'], company__users=self.request.user)
        duplicata = source.duplicate()
        return duplicata.get_edit_url()


class InvoiceSendMailView(SingleObjectMixin, LoginRequiredMixin, FormView):
    """
    GET: Form with mail text and invoice as PDF
    POST: send
    """
    model = Invoice
    form_class = EmailForm
    template_name = 'invoices/send.html'

    def form_valid(self, form):
        invoice: Invoice = self.get_object()
        bcc = []
        if invoice.company.bcc_email:
            bcc.append(invoice.company.bcc_email)
        reply_to = []
        if not invoice.company.override_default_from_email:
            reply_to.append(invoice.company.from_email)
        email = EmailMessage(
            subject=form.cleaned_data.get('subject'),
            body=form.cleaned_data.get('message'),
            from_email=invoice.company.invoice_from_email,
            to=[invoice.client.full_contact_email],
            reply_to=reply_to,
            bcc=bcc
        )
        if not invoice.pdf or invoice.pdf_version != invoice.version:
            invoice.generate_pdf()

        email.attach_file(invoice.pdf.path, 'application/pdf')
        try:
            email.send()
            invoice.set_sent()
            messages.info(
                self.request,
                message=_("Your invoice has been sent to %(email)s") % {'email': invoice.client.contact_email})
        except AnymailError as e:
            messages.info(
                self.request,
                message=_("Your invoice could not be sent, administrators have been warned."))
            raise
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        # noinspection PyAttributeOutsideInit
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        invoice: Invoice = self.get_object()
        current_lang = get_language()
        activate(invoice.client.language)
        initial = super().get_initial()
        initial['subject'] = render_to_string('invoices/mail_subject.txt', {'invoice': invoice})
        initial['message'] = render_to_string('invoices/mail_message.txt', {'invoice': invoice})
        activate(current_lang)
        return initial

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceReminderEmail(InvoiceSendMailView):
    def get_initial(self):
        invoice: Invoice = self.get_object()
        current_lang = get_language()
        activate(invoice.client.language)
        initial = super().get_initial()
        initial['subject'] = render_to_string('invoices/reminder_mail_subject.txt', {'invoice': invoice})
        initial['message'] = render_to_string('invoices/reminder_mail_message.txt', {'invoice': invoice})
        activate(current_lang)
        return initial
