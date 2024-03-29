from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.translation import activate, get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, FormView, RedirectView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from beyondtheadmin.clients.models import Client
from beyondtheadmin.companies.models import Company
from beyondtheadmin.dashboard.permissions import HasCompanyMixin
from beyondtheadmin.users.models import User

from ..forms import EmailForm, InvoiceStatusForm
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


class InvoiceCancelView(LoginRequiredMixin, HasCompanyMixin, UserInvoiceMixin, UpdateView):
    model = Invoice
    template_name = "invoices/confirm_cancel.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.canceled,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceCreateView(LoginRequiredMixin, HasCompanyMixin, TemplateView):
    model = Invoice
    template_name = "invoices_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["company"] = None
        # noinspection PyUnresolvedReferences
        companies = self.request.user.companies.all()
        company = Company.objects.filter(pk=self.request.GET.get("company", None)).first()
        if company:
            if company not in companies:
                raise PermissionDenied(
                    _("You are not allowed to create invoices for this company.")
                )
            context["company"] = company.pk

        context["client"] = None
        client = Client.objects.filter(pk=self.request.GET.get("client", None)).first()
        if client:
            if client.company not in companies:
                raise PermissionDenied(
                    _("You are not allowed to create invoices for this client.")
                )
            context["client"] = client.pk
            # That way we remain coherent. Client > Company
            context["company"] = client.company.pk
        return context


class InvoiceDuplicateView(LoginRequiredMixin, HasCompanyMixin, RedirectView):
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


class InvoiceListView(LoginRequiredMixin, HasCompanyMixin, TemplateView):
    template_name = "invoices/list.html"


class InvoiceMarkPaidView(LoginRequiredMixin, HasCompanyMixin, UserInvoiceMixin, UpdateView):
    model = Invoice
    template_name = "invoices/confirm_paid.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.paid,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceSendMailView(LoginRequiredMixin, HasCompanyMixin, UserInvoiceMixin, FormView):
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
            invoice.pk, form.cleaned_data["subject"], form.cleaned_data["message"] + "\n\n"
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


class InvoiceSnailMailUpdateView(
    LoginRequiredMixin, HasCompanyMixin, UserInvoiceMixin, UpdateView
):
    model = Invoice
    template_name = "invoices/confirm_print.html"
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            "status": Invoice.STATUS.sent,
        }

    def get_success_url(self):
        return self.get_object().company.detail_url


class InvoiceUpdateView(LoginRequiredMixin, HasCompanyMixin, DetailView):
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
