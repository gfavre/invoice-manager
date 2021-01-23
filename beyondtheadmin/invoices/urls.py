from django.urls import path

from .views import (
    InvoiceListView, InvoiceDetailView, qrbill
)

app_name = "invoices"
urlpatterns = [
    path("", view=InvoiceListView.as_view(), name="list"),
    path("<uuid:pk>/", view=InvoiceDetailView.as_view(), name="detail"),
    path("<uuid:pk>/qrbill", view=qrbill, name="qrbill"),
]
