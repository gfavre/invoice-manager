from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, TemplateView

from beyondtheadmin.dashboard.permissions import HasCompanyMixin

from ..models import Client


class ClientAppView(LoginRequiredMixin, HasCompanyMixin, TemplateView):
    template_name = "clients_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "pk" in self.kwargs:
            context["client_id"] = self.kwargs["pk"]
            context["client"] = get_object_or_404(
                Client, pk=self.kwargs["pk"], company__users=self.request.user
            )
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
