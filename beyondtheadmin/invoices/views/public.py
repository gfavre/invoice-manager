# -*- coding: utf-8 -*-
from django.utils.translation import activate
from django.views.generic import DetailView

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

