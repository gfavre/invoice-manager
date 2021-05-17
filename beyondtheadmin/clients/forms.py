# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Fieldset, ButtonHolder, Row, Submit

from .models import Client


class ClientForm(ModelForm):

    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _("Company"),
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
                css_class='border-left-primary shadow'

            ),
            Fieldset(
                _("Contact Person"),
                Row(
                    Column('contact_first_name'),
                    Column('contact_last_name'),
                ),
                'contact_email',
                css_class='border-left-info shadow'
            ),
            Fieldset(
                _("Invoices"),
                Row(
                    Column('currency'),
                    Column('vat_rate'),
                    Column('default_hourly_rate'),
                ),
                'language',
                'payment_delay_days',
                Row(
                    Column('slug'),
                    Column('invoice_current_count'),
                ),
                css_class='border-left-success shadow'

            ),
            ButtonHolder(
                Submit('submit', _("Save"), css_class='button white')
            )
        )

