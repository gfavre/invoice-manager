from django.urls import path

from .views import (
    InvoiceCreateView, InvoiceDuplicateView, InvoiceListView,
    InvoiceCancelView, InvoiceMarkPaidView, InvoiceSendMailView,
    InvoiceSnailMailUpdateView, InvoiceUpdateView
)

app_name = "invoices"
urlpatterns = [
    path("new/", view=InvoiceCreateView.as_view(), name="create"),

    path("<uuid:pk>/cancel", view=InvoiceCancelView.as_view(), name="cancel"),
    path("<uuid:pk>/duplicate", view=InvoiceDuplicateView.as_view(), name="duplicate"),
    path("<uuid:pk>/send", view=InvoiceSendMailView.as_view(), name="send"),
    path("<uuid:pk>/mark-as-paid", view=InvoiceMarkPaidView.as_view(), name="mark_paid"),
    path("<uuid:pk>/mark-as-sent", view=InvoiceSnailMailUpdateView.as_view(), name="mark_sent"),
    path("<uuid:pk>/update", view=InvoiceUpdateView.as_view(), name="update"),
    path("", view=InvoiceListView.as_view(), name="list"),

]
