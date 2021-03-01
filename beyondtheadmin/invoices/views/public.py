# -*- coding: utf-8 -*-
import io

from django.utils.translation import activate
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.http import FileResponse, Http404

from ..models import Invoice


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/detail.html'

    def get(self, request, *args, **kwargs):
        # noinspection PyAttributeOutsideInit
        self.object = self.get_object()
        # noinspection PyUnresolvedReferences
        activate(self.object.client.language)
        if self.request.GET.get('pdf', ''):
            return self.pdf()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def pdf(self):
        """output: filelike object"""
        from django.http import HttpResponseRedirect
        # noinspection PyUnresolvedReferences
        return HttpResponseRedirect(self.object.latest_pdf_url)


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
                        filename='qrbill.svg'.format(invoice.code))
