# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import viewsets

from ..models import Invoice, InvoiceLine
from ..serializers import InvoiceSerializer, InvoiceListSerializer, InvoiceLineSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user)\
                              .exclude(status=Invoice.STATUS.canceled)\
                              .select_related('client', 'company')

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return self.serializer_class


class InvoiceLineViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceLineSerializer

    def get_queryset(self):
        if 'invoice_pk' not in self.kwargs:
            raise Http404()
        return InvoiceLine.objects.filter(company__users=self.request.user,
                                          invoice_id=self.kwargs['invoice_pk'])

    def perform_create(self, serializer):
        serializer.save(invoice_id=self.kwargs['invoice_pk'])
