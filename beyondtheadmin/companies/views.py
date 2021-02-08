from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from .forms import CompanyForm
from .models import Company


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/create.html'
    success_url = reverse_lazy('dashboard')


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'companies/confirm_delete.html'
    success_url = reverse_lazy('dashboard')


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/update.html'
    success_url = reverse_lazy('dashboard')
