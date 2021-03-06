import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import IntegerField, Sum, Func
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView

from beyondtheadmin.companies.models import Company
from beyondtheadmin.companies.forms import CompanyForm
from beyondtheadmin.invoices.models import Invoice


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['company_form'] = CompanyForm()

        context['invoices'] = Invoice.objects.order_by('-due_date')[:5]
        return context


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = IntegerField()


class OpenedInvoicesView(APIView):
    def get(self, request, format=None):
        current_date = now()
        waiting_invoices = Invoice.sent.filter(due_date__gte=current_date).aggregate(total=Sum('total')).get('total', 0) or 0
        overdue_invoices = Invoice.sent.filter(due_date__lte=current_date).aggregate(total=Sum('total')).get('total', 0) or 0
        return Response({
            'total': waiting_invoices + overdue_invoices,
            'waiting': waiting_invoices,
            'overdue': overdue_invoices,
        })


class ProfitView(APIView):
    def get(self, request, format=None):
        year = self.request.query_params.get('year', '')
        try:
            year = int(year)
        except ValueError:
            year = None
        if year is None:
            year = now().year
        invoices = Invoice.objects.filter(displayed_date__year=year)\
                                  .annotate(month=Month('displayed_date'))\
                                  .values('month')\
                                  .annotate(monthly_total=Sum('total'))\
                                  .order_by('month')
        months = dict(invoices.values_list('month', 'monthly_total'))
        months_list = []
        labels = [datetime.date(1900, i, 1).strftime('%B') for i in range(1, 13)]
        datasets = [
            {
                'label': _("Earnings"),
                'data': [months.get(i, 0) for i in range(1, 13)]
            }
        ]
        for i in range(1, 13):
            months_list.append((datetime.date(1900, i, 1).strftime('%B'), months.get(i, 0)))
        total = sum([invoice.get('monthly_total') for invoice in invoices])
        return Response({
            'total': total,
            'monthly_sums': {'labels': labels, 'datasets': datasets}
        })
