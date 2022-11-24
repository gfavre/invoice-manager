from django.urls import path

from . import views


app_name = "invoices"
urlpatterns = [
    path("new/", view=views.InvoiceCreateView.as_view(), name="create"),
    path("<uuid:pk>/cancel", view=views.InvoiceCancelView.as_view(), name="cancel"),
    path("<uuid:pk>/duplicate", view=views.InvoiceDuplicateView.as_view(), name="duplicate"),
    path(
        "<uuid:pk>/send-reminder",
        view=views.InvoiceSendReminderEmailView.as_view(),
        name="reminder",
    ),
    path("<uuid:pk>/send", view=views.InvoiceSendMailView.as_view(), name="send"),
    path("<uuid:pk>/mark-as-paid", view=views.InvoiceMarkPaidView.as_view(), name="mark_paid"),
    path(
        "<uuid:pk>/mark-as-sent", view=views.InvoiceSnailMailUpdateView.as_view(), name="mark_sent"
    ),
    path("<uuid:pk>/update", view=views.InvoiceUpdateView.as_view(), name="update"),
    path("", view=views.InvoiceListView.as_view(), name="list"),
]
