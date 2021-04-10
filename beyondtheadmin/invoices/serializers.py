# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from rest_framework import serializers

from beyondtheadmin.clients.serializers import ClientSerializer
from .models import InvoiceLine, Invoice


class InvoiceLineSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceLine
        fields = ('id', 'description', 'note', 'quantity', 'unit', 'price_per_unit', 'total', 'url')
        extra_kwargs = {
            'quantity': {'coerce_to_string': False},
            'price_per_unit': {'coerce_to_string': False}

        }

    def get_url(self, obj):
        request = self.context['request']
        return obj.get_api_url(request)


class InvoiceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:invoice-detail',
        lookup_field='pk'
    )
    lines = InvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'code', 'company', 'client', 'due_date', 'displayed_date',
                  'vat_rate',
                  'title', 'description', 'period_start', 'period_end',
                  'url', 'total', 'lines')

    def get_url(self, obj):
        return obj.get_api_url()


class InvoiceListSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:invoice-detail',
        lookup_field='pk'
    )
    actions = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('id', 'status', 'code', 'company', 'client', 'due_date', 'displayed_date',
                  'vat_rate',
                  'title', 'description', 'period_start', 'period_end',
                  'url', 'total', 'actions')

    def get_url(self, obj):
        return obj.get_api_url()

    def get_actions(self, obj):
        actions = [
            {
                'url': obj.get_absolute_url(),
                'label': _("View"),
                'icon_class': 'bi-file-earmark-text'
            },
            {
                'url': obj.get_duplicate_url(),
                'label': _("Duplicate"),
                'icon_class': 'bi-files'
            },
        ]
        if obj.is_draft:
            actions += [
                {
                    'url': obj.get_edit_url(),
                    'label': _("Edit"),
                    'icon_class': 'bi-pencil'
                },
                {
                    'url': obj.get_send_url(),
                    'label': _("Send"),
                    'icon_class': 'bi-box-arrow-right'
                },
                {
                    'url': obj.get_cancel_url(),
                    'label': _("Cancel"),
                    'icon_class': 'bi-trash'
                },

            ]
        if obj.is_sent:
            actions += [
                {
                    'url': obj.get_set_paid_url(),
                    'label': _("Payment received"),
                    'icon_class': 'bi-credit-card'
                },
            ]
        return actions

    def get_status(self, obj):
        return {
            'label': obj.get_status_display(),
            'value': obj.status
        }
