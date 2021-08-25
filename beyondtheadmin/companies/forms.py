# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from colorfield.widgets import ColorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Fieldset, ButtonHolder, Row, Submit

from .models import Company


class CompanyForm(ModelForm):

    class Meta:
        model = Company
        fields = '__all__'

        widgets = {
            'contrast_color': ColorWidget(),
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
                'signature_text',
                'signature_image',
                'email_signature',
                'from_email',
                'bcc_email',
                'thanks',
                css_class='border-left-primary shadow'

            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

