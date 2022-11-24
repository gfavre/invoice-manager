# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from colorfield.widgets import ColorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (ButtonHolder, Column, Field, Fieldset, Layout, Row, HTML,
                                 Submit)

from .models import Company


class CompanyForm(forms.ModelForm):

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/vue/dist/vue.js',
            'js/companies-form.js',
            'js/bootstrap-autocomplete.min.js',
            'js/companies-autocomplete.js',
        )


    class Meta:
        model = Company
        fields = '__all__'

        widgets = {
            'contrast_color': ColorWidget(),
            'address': forms.Textarea(attrs={'rows': 2}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.layout = Layout(
            Fieldset(
                _("Contact"),
                'name',
                'address',
                Row(
                    Column(
                        'country',
                        css_class='col-md-4'
                    ),
                    Column(
                        'zip_code',
                        css_class='col-md-2'
                    ),
                    Column(
                        'city'
                    )
                ),
                'phone',
                'additional_phone',
                'email',
                'website',
                css_class='border-left-info shadow'

            ),
            Fieldset(
                _("Business"),
                'vat_id',
                Row(
                    Column(
                        Field('iban',
                              **{"v-model": "iban",
                                 ":class": "classIbanValid"}),
                        css_class='col-md-6'
                    ),
                    Column(
                        'name_for_bank',
                        css_class='col-md-6'
                    ),
                ),
                Row(
                    Column(
                        Field('bank', v_model='bank', rows=3),
                        css_class='col-9'
                    ),
                    Column(
                        Field('bic', v_model='swift'),
                        css_class='col'
                    ),
                ),
                css_class='border-left-warning shadow'
            ),
            Fieldset(
                _("Invoices"),
                'logo',
                'contrast_color',
                'invoice_note',
                'signature_text',
                'signature_image',
                'email_signature',
                'from_email',
                'bcc_email',
                'thanks',
                css_class='border-left-primary shadow'

            ),
            ButtonHolder(
                Submit('submit', _("Save"), css_class='button white')
            )
        )
