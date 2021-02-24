from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from beyondtheadmin.companies.models import Company
from beyondtheadmin.companies.forms import CompanyForm
from beyondtheadmin.invoices.models import Invoice


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['company_form'] = CompanyForm()

        context['invoices'] = Invoice.objects.all()
        return context