import io

from django.http import FileResponse, Http404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView


from .models import Invoice


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/list.html'


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/detail.html'


def qrbill(request, *args, **kwargs):
    try:
        invoice = Invoice.objects.get(pk=kwargs.get('pk'))
    except Invoice.DoesNotExist:
        raise Http404(_("Invoice does not exist"))
    if not invoice.qr_bill:
        raise Http404(_("Invoice has no QR Bill"))
    buffer = io.BytesIO(invoice.qr_bill.encode('utf-8'))
    return FileResponse(buffer, content_type='image/svg+xml',
                        as_attachment=True,
                        filename='{}.svg'.format(invoice.code))
