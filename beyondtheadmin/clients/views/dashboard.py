from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from ..forms import ClientForm
from ..models import Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:list")
    template_name = "clients/create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ClientAppView(LoginRequiredMixin, TemplateView):
    template_name = "clients_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "pk" in self.kwargs:
            context["client_id"] = self.kwargs["pk"]
            context["client"] = get_object_or_404(
                Client, pk=self.kwargs["pk"], company__users=self.request.user
            )
        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("clients:list")
    template_name = "clients/confirm_delete.html"

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/list.html"

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("clients:list")
    template_name = "clients/update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return Client.objects.filter(company__users=self.request.user)
