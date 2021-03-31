from django.urls import path

from .views import (
    InvoiceCreateView, InvoiceDuplicateView, InvoiceListView, InvoiceUpdateView
)

app_name = "invoices"
urlpatterns = [
    path("", view=InvoiceListView.as_view(), name="list"),
    path("new/", view=InvoiceCreateView.as_view(), name="create"),
    path("<uuid:pk>/duplicate", view=InvoiceDuplicateView.as_view(), name="duplicate"),
    path("<uuid:pk>/send", view=InvoiceUpdateView.as_view(), name="send"),

    path("<uuid:pk>/update", view=InvoiceUpdateView.as_view(), name="update"),
]
