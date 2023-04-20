from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import activate, get_language
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    RedirectView,
    TemplateView,
    UpdateView,
)
from django.views.generic.detail import SingleObjectMixin

from beyondtheadmin.clients.models import Client
from beyondtheadmin.users.models import User

from ..forms import BaseInvoiceForm, EmailForm, InvoiceEditForm, InvoiceStatusForm
from ..models import Invoice
from ..tasks import send_invoice_email


class InvoiceSingletonMixin(SingleObjectMixin):
    def get_object(self, queryset=None) -> Invoice:
        return super().get_object(queryset=queryset)  # type: ignore


class UserInvoiceMixin(InvoiceSingletonMixin):
    def get_queryset(self):
        # noinspection PyUnresolvedReferences
        user: User = self.request.user
        return Invoice.objects.filter(Q(company__users=user) | Q(created_by=user)).distinct()


class InvoiceCancelView(LoginRequiredMixin, UserInvoiceMixin, UpdateView):
    model = Invoice
    template_name = "invoices/confirm_cancel.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.canceled,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class CreateOrUpdateDraftInvoiceView(LoginRequiredMixin, View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        # Check if there's an existing draft invoice for the current user
        draft_invoice, created = Invoice.objects.get_or_create(
            created_by=request.user, status=Invoice.STATUS.draft
        )
        # Redirect to the update view for the draft invoice
        return redirect("invoices:update", pk=draft_invoice.pk, permanent=False)


class InvoiceAppView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "invoices_app/index.html"

    def get_queryset(self):
        return Invoice.objects.filter(status=Invoice.STATUS.draft)

    def get(self, request, *args, **kwargs):
        # noinspection PyTypeChecker
        invoice: Invoice = self.get_object()
        if not invoice.check_rights(request.user):
            # If the object owner is not the current user, redirect to a custom URL or render a custom template
            return self.handle_no_permission()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["invoice_id"] = self.kwargs["pk"]
        context["invoice"] = self.get_object()
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = "invoices/create.html"
    form_class = BaseInvoiceForm

    def get_form_kwargs(self):
        user: User = self.request.user
        kwargs = super().get_form_kwargs()
        kwargs["companies"] = user.companies.all()
        kwargs["clients"] = Client.objects.filter(company__in=kwargs["companies"])
        return kwargs

    def get_success_url(self):
        # noinspection PyUnresolvedReferences
        return self.object.get_edit_url()


class InvoiceDuplicateView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = "pk"

    def get_redirect_url(self, *args, **kwargs):
        try:
            source = Invoice.objects.filter(
                Q(company__users=self.request.user) | Q(created_by=self.request.user)  # type: ignore
            ).get(pk=kwargs["pk"])
        except Invoice.DoesNotExist:
            raise Http404()
        duplicata = source.duplicate()
        return duplicata.get_edit_url()


class InvoiceListView(LoginRequiredMixin, TemplateView):
    template_name = "invoices/list.html"


class InvoiceMarkPaidView(LoginRequiredMixin, UserInvoiceMixin, UpdateView):
    model = Invoice
    template_name = "invoices/confirm_paid.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.paid,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceSendMailView(LoginRequiredMixin, UserInvoiceMixin, FormView):
    """
    GET: Form with mail text and invoice as PDF
    POST: send
    """

    model = Invoice
    form_class = EmailForm
    template_name = "invoices/send.html"

    def form_valid(self, form):
        invoice: Invoice = self.get_object()
        send_invoice_email.delay(
            invoice.pk, form.cleaned_data["subject"], form.cleaned_data["message"]
        )
        messages.success(self.request, self.get_success_message())
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        # noinspection PyAttributeOutsideInit
        self.object = self.get_object()
        if not self.object.is_ready:
            messages.error(self.request, self.get_failure_message())
            return HttpResponseRedirect(self.object.get_absolute_url())
        if not self.object.code:
            self.object.save(generate_code=True)
        return super().get(request, *args, **kwargs)

    def get_failure_message(self):
        return _("Your invoice could not be sent, administrators have been warned.")

    def get_initial(self):
        invoice: Invoice = self.get_object()
        current_lang = get_language()
        activate(invoice.client.language)
        initial = super().get_initial()
        initial["subject"] = render_to_string("invoices/mail_subject.txt", {"invoice": invoice})
        initial["message"] = render_to_string("invoices/mail_message.txt", {"invoice": invoice})
        activate(current_lang)
        return initial

    def get_success_message(self):
        return _("Your invoice has been sent to %(email)s") % {
            "email": self.get_object().client.contact_email
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceSendReminderEmailView(InvoiceSendMailView):
    template_name = "invoices/send-reminder.html"

    def get_initial(self):
        invoice: Invoice = self.get_object()
        current_lang = get_language()
        activate(invoice.client.language)
        initial = super().get_initial()
        initial["subject"] = render_to_string(
            "invoices/reminder_subject.txt", {"invoice": invoice}
        )
        initial["message"] = render_to_string(
            "invoices/reminder_message.txt", {"invoice": invoice}
        )
        activate(current_lang)
        return initial

    def get_failure_message(self):
        return _("Your reminder could not be sent, administrators have been warned.")

    def get_success_message(self):
        return _("Your reminder has been sent to %(email)s") % {
            "email": self.get_object().client.contact_email
        }


class InvoiceSnailMailUpdateView(LoginRequiredMixin, UserInvoiceMixin, UpdateView):
    model = Invoice
    template_name = "invoices/confirm_print.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.sent,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceUpdateView(LoginRequiredMixin, UserInvoiceMixin, UpdateView):
    form_class = InvoiceEditForm
    model = Invoice
    template_name = "invoices/update.html"

    def get_form_kwargs(self):
        user: User = self.request.user
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["companies"] = user.companies.all()
        kwargs["clients"] = Client.objects.filter(company__in=kwargs["companies"])
        return kwargs

    # noinspection PyUnresolvedReferences
    def get_initial(self):
        initial = {}
        if not self.object.due_date:
            initial["due_date"] = (now() + timedelta(days=self.object.client.payment_delay_days),)
        if self.object.vat_rate is None:
            initial["vat_rate"] = self.object.client.vat_rate
        return initial
