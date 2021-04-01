# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Submit, Row, Column, Div, Button

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

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        date_picker_options = {
            "format": "DD.MM.YYYY",  # moment date-time format
            "locale": settings.LANGUAGE_CODE,
        }
        if request:
            date_picker_options['locale'] = request.LANGUAGE_CODE
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
                Column('due_date', css_class='form-group col-md-6 mb-0'),
                Column('displayed_date', css_class='form-group col-md-6 mb-0'),
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
                    HTML('<h5 class="text-xs font-weight-bold text-info text-uppercase mb-4">{}</h5>'.format(_("Lines"))),
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
