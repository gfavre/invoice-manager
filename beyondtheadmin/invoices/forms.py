# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Invoice


class BaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('company', 'client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))


class InvoiceEditForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('company', 'client', 'due_date', 'displayed_date', 'title', 'description',
                  'period_start', 'period_end', 'vat_rate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))
