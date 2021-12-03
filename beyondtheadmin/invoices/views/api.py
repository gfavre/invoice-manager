# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from beyondtheadmin.companies.models import Company

from ..models import Invoice, InvoiceLine
from ..serializers import (InvoiceLineSerializer, InvoiceListSerializer,
                           InvoiceSerializer)


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


class CompanyInvoiceListView(APIView):
    serializer_class = InvoiceListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, company_pk=None):
        company_obj = get_object_or_404(Company, pk=company_pk, users=request.user)
        invoices_qs = Invoice.objects.filter(company=company_obj).select_related('client')
        context = {'request': request}
        return Response(InvoiceListSerializer(invoices_qs, many=True, context=context).data)


class InvoiceLineViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceLineSerializer

    def get_queryset(self):
        if 'invoice_pk' not in self.kwargs:
            raise Http404()
        return InvoiceLine.objects.filter(invoice_id=self.kwargs['invoice_pk'])

    def perform_create(self, serializer):
        serializer.save(invoice_id=self.kwargs['invoice_pk'])
