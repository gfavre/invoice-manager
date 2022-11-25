from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Func, IntegerField, Sum
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.views import APIView

from beyondtheadmin.companies.forms import CompanyForm
from beyondtheadmin.companies.models import Company
from beyondtheadmin.invoices.models import Invoice


def dashboard(request):
    if hasattr(request.user, "companies"):
        nb_companies = request.user.companies.count()
    else:
        nb_companies = 0
    if nb_companies > 1:
        return DashboardView.as_view()(request)
    elif nb_companies == 1:
        from beyondtheadmin.companies.views import CompanyDetailView

        company = request.user.companies.first()
        return CompanyDetailView.as_view()(request, pk=company.pk)
    else:
        from beyondtheadmin.companies.views import CompanyCreateView

        # FIXME: wizard
        return CompanyCreateView.as_view()(request)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(users=self.request.user)
        context["company_form"] = CompanyForm()

        return context


class Month(Func):
    function = "EXTRACT"
    template = "%(function)s(MONTH from %(expressions)s)"
    output_field = IntegerField()


class OpenInvoicesView(APIView):
    def get(self, request, company_pk=None, format=None):
        current_date = now()
        waiting_invoices_qs = Invoice.sent.filter(due_date__gte=current_date)
        overdue_invoices_qs = Invoice.sent.filter(due_date__lt=current_date)
        try:
            company_obj = Company.objects.get(pk=company_pk, users=request.user)
            waiting_invoices_qs = waiting_invoices_qs.filter(company=company_obj)
            overdue_invoices_qs = overdue_invoices_qs.filter(company=company_obj)
        except (Company.DoesNotExist, ValueError):
            waiting_invoices_qs = waiting_invoices_qs.filter(company__users=self.request.user)
            overdue_invoices_qs = overdue_invoices_qs.filter(company__users=self.request.user)
        waiting_invoices = waiting_invoices_qs.aggregate(total=Sum("total")).get("total", 0) or 0
        overdue_invoices = overdue_invoices_qs.aggregate(total=Sum("total")).get("total", 0) or 0
        return Response(
            {
                "total": waiting_invoices + overdue_invoices,
                "waiting": waiting_invoices,
                "overdue": overdue_invoices,
            }
        )


class ProfitView(APIView):
    def get(self, request, company_pk, format=None):
        company_obj = get_object_or_404(Company.objects.filter(users=request.user), pk=company_pk)
        year = self.request.query_params.get("year", "")
        try:
            year = int(year)
        except ValueError:
            year = None
        if year is None:
            year = now().year
        invoices = (
            Invoice.visible.filter(company=company_obj, displayed_date__year=year)
            .annotate(month=Month("displayed_date"))
            .values("month")
            .annotate(monthly_total=Sum("total"))
            .order_by("month")
        )
        months = dict(invoices.values_list("month", "monthly_total"))
        datasets = [{"label": _("Earnings"), "data": [months.get(i, 0) for i in range(1, 13)]}]
        labels = [
            _("January"),
            _("February"),
            _("March"),
            _("April"),
            _("May"),
            _("June"),
            _("July"),
            _("August"),
            _("September"),
            _("October"),
            _("November"),
            _("December"),
        ]

        total = sum([invoice.get("monthly_total") for invoice in invoices])
        return Response({"total": total, "monthly_sums": {"labels": labels, "datasets": datasets}})
