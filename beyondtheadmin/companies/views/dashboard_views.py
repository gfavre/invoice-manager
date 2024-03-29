from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView

from ..forms import CompanyForm
from ..models import Company


class CompanyAppView(LoginRequiredMixin, TemplateView):
    template_name = "companies_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "pk" in self.kwargs:
            context["company_id"] = self.kwargs["pk"]
            context["company"] = get_object_or_404(
                Company, pk=self.kwargs["pk"], users=self.request.user
            )
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/create.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # noinspection PyAttributeOutsideInit
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = "companies/confirm_delete.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object: Company = self.get_object()
        success_url = self.get_success_url()
        self.object.set_deleted()
        return HttpResponseRedirect(success_url)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = "companies/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user).prefetch_related("invoices")


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/update.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)
