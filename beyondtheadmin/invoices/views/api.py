# -*- coding: utf-8 -*-
from django.db.models import Count
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import gettext_lazy as _
from django.utils.timezone import now

from rest_framework import generics, permissions, viewsets

from beyondtheadmin.api.filters import DatatablesFilterAndPanesBackend
from beyondtheadmin.clients.models import Client
from beyondtheadmin.companies.models import Company

from ..models import Invoice, InvoiceLine, InvoicePDF
from ..serializers import (InvoiceLineSerializer, InvoiceListSerializer,
                           InvoicePDFSerializer,
                           InvoiceSerializer)
from ..pdf import build_content_for_pdf
from ..tasks import generate_pdf


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(company__users=self.request.user) \
            .exclude(status=Invoice.STATUS.canceled) \
            .select_related('client', 'company')

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return self.serializer_class


class CompanyInvoiceListView(generics.ListAPIView):
    filter_backends = (DatatablesFilterAndPanesBackend,)
    serializer_class = InvoiceListSerializer
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        """Meta class for viewset."""
        datatables_extra_json = ('get_search_panes',)

    def get_queryset(self):
        company_obj = get_object_or_404(Company, pk=self.kwargs.get('company_pk'), users=self.request.user)
        return Invoice.objects.filter(company=company_obj).select_related('client')

    def get_search_panes(self):
        clients = Client.objects.filter(companies__company=self.kwargs.get('company_pk')).annotate(
            invoice_count=Count('invoices')
        )
        invoices = self.get_queryset()
        invoice_status = invoices.values('status').annotate(total=Count('status')).order_by('total')
        current_date = now()
        waiting_invoices_qs = invoices.filter(due_date__gte=current_date, status=Invoice.STATUS.sent)
        overdue_invoices_qs = invoices.filter(due_date__lt=current_date, status=Invoice.STATUS.sent)

        return 'searchPanes', {
            "options": {

                "client": [
                    {'label': client.name,
                     'value': client.id,
                     'count': client.invoice_count,
                     'total': client.invoice_count}
                    for client in clients
                ],

                "status": [
                    {'label': Invoice.STATUS[i_status.get('status')],
                     'value': i_status.get('status'),
                     'count': i_status.get('total'),
                     'total': i_status.get('total')
                     } for i_status in invoice_status
                ],

                "overdue": [
                    {
                        'label': _("Waiting"),
                        'value': 'waiting',
                        'count': waiting_invoices_qs.count(),
                        'total': waiting_invoices_qs.count()
                    },
                    {
                        'label': _("Overdue"),
                        'value': 'overdue',
                        'count': overdue_invoices_qs.count(),
                        'total': overdue_invoices_qs.count()
                    },
                ]
            }
        }


class InvoiceLineViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceLineSerializer

    def get_queryset(self):
        if 'invoice_pk' not in self.kwargs:
            raise Http404()
        return InvoiceLine.objects.filter(invoice_id=self.kwargs['invoice_pk'])

    def perform_create(self, serializer):
        serializer.save(invoice_id=self.kwargs['invoice_pk'])


class InvoicePDFViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoicePDFSerializer
    lookup_field = 'version'

    def get_queryset(self):
        if 'invoice_pk' not in self.kwargs:
            raise Http404()
        return InvoicePDF.objects.filter(invoice_id=self.kwargs['invoice_pk'])

    def get_object(self):
        try:
            version = int(self.kwargs['version'])
            return self.get_queryset().get(version=version)
        except InvoicePDF.DoesNotExist:
            invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
            if invoice.version != version:
                raise Http404()
            invoice_pdf = InvoicePDF.objects.create(invoice=invoice, version=version)
            content = build_content_for_pdf(invoice)
            transaction.on_commit(
                lambda: generate_pdf.delay(invoice_id=str(invoice.id), version=version, content=content)
            )
            return invoice_pdf
        except ValueError:
            raise Http404()



