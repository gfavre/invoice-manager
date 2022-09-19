# -*- coding: utf-8 -*-
from decimal import Decimal

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Column, Div, Layout, Row, Submit

from .models import Invoice


class BaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('company', 'client')

    def __init__(self, *args, **kwargs):
        companies = kwargs.pop('companies', None)
        clients = kwargs.pop('clients', None)
        super().__init__(*args, **kwargs)
        if companies:
            self.fields['company'].queryset = companies
        if clients:
            self.fields['client'].queryset = clients
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))


class InvoiceEditForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ('company', 'client', 'displayed_date', 'due_date', 'title', 'description',
                  'period_start', 'period_end', 'vat_rate')

    def clean_vat_rate(self):
        vat_rate = self.cleaned_data.get("vat_rate")
        if vat_rate is None:
            vat_rate = Decimal('0.0')
        return vat_rate

    def __init__(self, *args, request=None, **kwargs):
        companies = kwargs.pop('companies', None)
        clients = kwargs.pop('clients', None)
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = None
        self.fields['client'].empty_label = None

        date_picker_options = {
            "format": "DD.MM.YYYY",  # moment date-time format
            "locale": settings.LANGUAGE_CODE,
        }
        if request:
            date_picker_options['locale'] = request.LANGUAGE_CODE
        if companies:
            self.fields['company'].queryset = companies
        if clients:
            self.fields['client'].queryset = clients
        self.fields['due_date'].widget = DatePickerInput(options=date_picker_options)
        self.fields['displayed_date'].widget = DatePickerInput(options=date_picker_options)
        self.fields['period_start'].widget = DatePickerInput(options=date_picker_options)
        self.fields['period_end'].widget = DatePickerInput(options=date_picker_options)

        self.helper = FormHelper()
        self.helper.include_media = False
        self.helper.layout = Layout(
            Row(
                Column('company', css_class='form-group col-md-6 mb-0'),
                Column('client', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('displayed_date', css_class='form-group col-md-6 mb-0'),
                Column('due_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'title',
            'description',
            Row(
                Column('period_start', css_class='form-group col-md-6 mb-0'),
                Column('period_end', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'vat_rate',
            Div(
                Div(
                    HTML('<h5 class="text-xs font-weight-bold text-info text-uppercase mb-4">{}</h5>'.format(
                        _("Lines"))
                    ),
                    Div(css_class='lines'),
                    Div(
                        Button('add', _("Add line"), css_class='btn btn-info'),
                        css_id='add-line', css_class='pt-2'
                    ),
                    css_class='card-body'
                ),
                css_class='card border-left-info shadow mb-3'
            ),
            Div(
                Submit('save', _("Save")),
            )
        )


class InvoiceStatusForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('status',)
        widgets = {'status': forms.HiddenInput}

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.include_media = False
        self.helper.layout = Layout(
            'status',
            Div(
                Submit('save', _("Save")),
            )
        )


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False

        self.helper.layout = Layout(
            'subject',
            'message',
            Div(
                Submit('save', _("Send")),
            ),
        )
