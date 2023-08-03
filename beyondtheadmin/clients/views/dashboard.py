import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView

from beyondtheadmin.dashboard.permissions import HasCompanyMixin
from beyondtheadmin.invoices.models import Invoice

from ..models import Client


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


class ClientAppView(LoginRequiredMixin, HasCompanyMixin, TemplateView):
    template_name = "clients_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "pk" in self.kwargs:
            context["client_id"] = self.kwargs["pk"]
            context["client"] = get_object_or_404(
                Client, pk=self.kwargs["pk"], company__users=self.request.user
            )
        invoice_param = self.request.GET.get("invoice", None)
        if invoice_param:
            context["redirect_to_invoice"] = 1
            if is_valid_uuid(invoice_param):
                try:
                    invoice = Invoice.objects.get(pk=invoice_param)
                    if not invoice.check_rights(self.request.user):
                        raise Invoice.DoesNotExist()
                    success_url = invoice.get_edit_url()
                except Invoice.DoesNotExist:
                    success_url = reverse_lazy("invoices:create")
            else:
                success_url = reverse_lazy("invoices:create")
        else:
            context["redirect_to_invoice"] = 0
            success_url = reverse_lazy("clients:list")
        context["success_url"] = success_url
        return context


class ClientDeleteView(LoginRequiredMixin, HasCompanyMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:list")
    template_name = "clients/confirm_delete.html"

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)


class ClientListView(LoginRequiredMixin, HasCompanyMixin, ListView):
    model = Client
    template_name = "clients/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_multiple_companies"] = self.request.user.companies.count() > 1
        return context

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)
