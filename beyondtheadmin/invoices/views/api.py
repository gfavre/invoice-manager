# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Invoice, InvoiceLine
from ..serializers import InvoiceSerializer, InvoiceListSerializer, InvoiceLineSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.select_related('client', 'company')

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return self.serializer_class


class InvoiceLineViewSet(viewsets.ModelViewSet):
    queryset = InvoiceLine.objects.all()
    serializer_class = InvoiceLineSerializer
