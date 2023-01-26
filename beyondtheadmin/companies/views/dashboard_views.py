from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from ..forms import (
    CompanyCreateWizardBankDataForm,
    CompanyCreateWizardBaseDataForm,
    CompanyCreateWizardConfigureInvoicesForm,
    CompanyForm,
)
from ..models import Company


class CompanyWizardView(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    success_url = reverse_lazy("dashboard")
    template_name = "companies/wizard.html"
    forms_classes = [
        CompanyCreateWizardBaseDataForm,
        CompanyCreateWizardBankDataForm,
        CompanyCreateWizardConfigureInvoicesForm,
    ]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"].setdefault("from_email", self.request.user.email_from)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        context["form_base"] = CompanyCreateWizardBaseDataForm(**form_kwargs)
        context["form_bank"] = CompanyCreateWizardBankDataForm(**form_kwargs)
        context["form_invoices"] = CompanyCreateWizardConfigureInvoicesForm(**form_kwargs)
        return context

    def forms_valid(self, form):
        forms_valid = True
        for subform in form:
            if not subform.is_valid():
                forms_valid = False
        if forms_valid:
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # noinspection PyAttributeOutsideInit
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


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


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = "companies/detail.html"

    def get_queryset(self):
        return (
            super(CompanyDetailView, self)
            .get_queryset()
            .filter(users=self.request.user)
            .prefetch_related("invoices")
        )


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/update.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)
