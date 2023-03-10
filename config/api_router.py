from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

import beyondtheadmin.invoices.views.api as invoices_views
from beyondtheadmin.api.views import csrf_token
from beyondtheadmin.clients.views.api import ClientViewSet
from beyondtheadmin.companies.views.api_views import (
    CompaniesViewSet,
    CompanyDetailView,
    CompanySearchView,
    IBANSearchView,
)
from beyondtheadmin.dashboard.views import OpenInvoicesView, ProfitView
from beyondtheadmin.users.api.views import UserViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("clients", ClientViewSet)
router.register("companies", CompaniesViewSet)

router.register("invoices", invoices_views.InvoiceViewSet)
invoices_router = routers.NestedSimpleRouter(router, r"invoices", lookup="invoice")
invoices_router.register(r"lines", invoices_views.InvoiceLineViewSet, basename="invoices-lines")
invoices_router.register(r"pdf", invoices_views.InvoicePDFViewSet, basename="invoices-pdf")


app_name = "api"
urlpatterns = [
    path("csrf-token/", csrf_token, name="csrf-token"),
    path("", include(router.urls)),
    path("", include(invoices_router.urls)),
    path("companies-search/", CompanySearchView.as_view(), name="companies-autocomplete"),
    path("iban/", IBANSearchView.as_view(), name="iban-lookup"),
    path("company-detail/", CompanyDetailView.as_view(), name="company-detail"),
    path("earnings/<uuid:company_pk>/", ProfitView.as_view(), name="earnings-per-company"),
    path(
        "open-invoices/<str:company_pk>",
        OpenInvoicesView.as_view(),
        name="open-invoices-per-company",
    ),
    path("open-invoices", OpenInvoicesView.as_view(), name="open-invoices"),
    path(
        "invoices/<str:company_pk>",
        invoices_views.CompanyInvoiceListView.as_view(),
        name="company-invoices",
    ),
]
