# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from colorfield.widgets import ColorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (ButtonHolder, Column, Fieldset, Layout, Row,
                                 Submit)

from .models import Company


class CompanyForm(forms.ModelForm):

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
                'name_for_bank',
                Row(
                    Column(
                        'bank',
                        css_class='col-9'
                    ),
                    Column(
                        'bic',
                        css_class='col'
                    ),
                ),
                'iban',
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
