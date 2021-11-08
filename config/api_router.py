from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from beyondtheadmin.users.api.views import UserViewSet
import beyondtheadmin.invoices.views.api as invoices_views
from beyondtheadmin.dashboard.views import ProfitView, OpenInvoicesView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register('invoices', invoices_views.InvoiceViewSet)
invoices_router = routers.NestedSimpleRouter(router, r'invoices', lookup='invoice')
invoices_router.register(r'lines', invoices_views.InvoiceLineViewSet,
                         basename='invoices-lines')

app_name = "api"
urlpatterns = [
    path('', include(router.urls)),
    path('', include(invoices_router.urls)),
    path('earnings/<uuid:company_pk>/', ProfitView.as_view(), name='earnings-per-company'),
    path('open-invoices/<str:company_pk>', OpenInvoicesView.as_view(), name='open-invoices-per-company'),
    path('open-invoices', OpenInvoicesView.as_view(), name='open-invoices'),
    path('invoices/<str:company_pk>', invoices_views.CompanyInvoiceListView.as_view(), name='company-invoices'),

]

