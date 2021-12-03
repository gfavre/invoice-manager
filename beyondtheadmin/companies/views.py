from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # noinspection PyAttributeOutsideInit
        self.object = form.save()
        self.object.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'companies/confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/detail.html'

    def get_queryset(self):
        return super(CompanyDetailView, self).get_queryset().filter(users=self.request.user)\
                                                            .prefetch_related('invoices')


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/update.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(users=self.request.user)
