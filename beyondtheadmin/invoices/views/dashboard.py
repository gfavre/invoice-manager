from datetime import timedelta

from django.utils.timezone import now
from django.views.generic import CreateView, ListView, UpdateView

from ..models import Invoice
from ..forms import BaseInvoiceForm, InvoiceEditForm


class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'invoices/create.html'
    form_class = BaseInvoiceForm

    def get_success_url(self):
        return self.object.get_edit_url()


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/list.html'


class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/update.html'
    form_class = InvoiceEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self) :
        return {
            'due_date': now() + timedelta(days=self.object.client.payment_delay_days),
            'vat_rate': self.object.client.vat_rate
        }
