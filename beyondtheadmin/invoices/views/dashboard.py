from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import CreateView, ListView, UpdateView, RedirectView

from ..models import Invoice
from ..forms import BaseInvoiceForm, InvoiceEditForm, InvoiceStatusForm


class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'invoices/create.html'
    form_class = BaseInvoiceForm

    def get_success_url(self):
        # noinspection PyUnresolvedReferences
        return self.object.get_edit_url()


class InvoiceListView(ListView):
    #model = Invoice
    template_name = 'invoices/list.html'
    queryset = Invoice.objects.exclude(status=Invoice.STATUS.canceled)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/update.html'
    form_class = InvoiceEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        # noinspection PyUnresolvedReferences
        return {
            'due_date': now() + timedelta(days=self.object.client.payment_delay_days),
            'vat_rate': self.object.client.vat_rate
        }


class InvoiceCancelView(UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_cancel.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.canceled,
        }

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceMarkPaidView(UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_paid.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.paid,
        }

    def get_success_url(self):
        return reverse('invoices:list')


class InvoiceSnailMailUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/confirm_print.html'
    form_class = InvoiceStatusForm

    def get_initial(self):
        return {
            'status': Invoice.STATUS.sent,
        }

    def get_success_url(self):
        return reverse('invoices:list')



class InvoiceDuplicateView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'pk'

    def get_redirect_url(self, *args, **kwargs):
        source = get_object_or_404(Invoice, pk=kwargs['pk'])
        duplicata = source.duplicate()
        return duplicata.get_edit_url()
