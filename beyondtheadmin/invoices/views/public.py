# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.utils.translation import activate
from django.views.generic import DetailView

import requests

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
        # noinspection PyUnresolvedReferences
        url = self.request.build_absolute_uri(self.object.get_absolute_url())
        phantomjs_conf = {
            'renderType': 'pdf',
            'omitBackground': False,
            "renderSettings": {
                'emulateMedia': 'print',
                'pdfOptions': {
                    'format': 'A4',
                    'landscape': False,
                    'preferCSSPageSize': True,
                }
            }
        }
        if settings.DEBUG:
            context = self.get_context_data(object=self.object)
            page = render_to_string(self.template_name, context=context, request=self.request)
            phantomjs_conf['content'] = page
        else:
            phantomjs_conf['url'] = url
        pdf = requests.post(settings.PHANTOMJSCLOUD_API_URL, json.dumps(phantomjs_conf))
        if not pdf.status_code == 200:
            raise HttpResponseServerError(pdf.text)
        response = HttpResponse(pdf.content, content_type="application/pdf")
        # noinspection PyUnresolvedReferences
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % self.object.code
        return response
