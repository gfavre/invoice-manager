# -*- coding: utf-8 -*-
from decimal import Decimal

from crispy_forms.bootstrap import InlineCheckboxes, InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (ButtonHolder, Column, Fieldset, HTML, Layout, Row, Submit)
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from beyondtheadmin.companies.models import Company
from .models import Client


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"), max_length=255, required=False)
    last_name = forms.CharField(label=_("Last name"), max_length=255, required=False)
    person_address = forms.CharField(label=_("Address"), required=False,
                                     widget=forms.Textarea(attrs={'rows': 2}))
    person_country = CountryField(default='CH').formfield(label=_("Country"))
    person_zipcode = forms.CharField(label=_("Postal code"), max_length=10, required=False)
    person_city = forms.CharField(label=_("City"), max_length=255, required=False)
    person_email = forms.EmailField(label=_("Email"), max_length=255, required=False)
    companies = forms.ModelMultipleChoiceField(
        label=_("Client for"),
        queryset=Company.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Media:
        js = (
            'js/bootstrap-autocomplete.min.js',
            'js/clients.js',
        )

    class Meta:
        model = Client
        fields = ('client_type', 'company_name', 'contact_first_name', 'contact_last_name',
                  'address', 'zip_code', 'city', 'country', 'language', 'currency', 'payment_delay_days',
                  'vat_rate', 'default_hourly_rate', 'contact_email', 'slug', 'invoice_current_count',
                  'companies', 'email_template',
                  'first_name', 'last_name', 'person_address', 'person_country', 'person_zipcode')
        widgets = {
            'client_type': forms.RadioSelect,
            'address': forms.Textarea(attrs={'rows': 2}),
            'company_name': forms.TextInput(
                attrs={'data-url': reverse_lazy("api:companies-autocomplete")}
            ),
        }

    def clean_vat_rate(self):
        vat_rate = self.cleaned_data.get("vat_rate")
        if vat_rate is None:
            vat_rate = Decimal('0.0')
        return vat_rate

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_type'].choices = (
            ('company', mark_safe('<i class="bi bi-journal"></i> ' + _("Company"))),
            ('person', mark_safe('<i class="bi bi-person-fill"></i> ' + _("Person"))),
        )
        companies_qs = Company.objects.filter(users=user)
        companies_visible = True
        self.fields['companies'].queryset = companies_qs
        if companies_qs.count() == 1:
            self.fields['companies'].initial = companies_qs
            self.fields['companies'].widget = forms.HiddenInput()
            companies_visible = False
        self.helper = FormHelper()
        self.helper.include_media = False
        self.helper.layout = Layout(

            InlineCheckboxes('companies'),
            companies_visible and HTML('<hr>') or HTML(),
            InlineRadios('client_type'),
            Fieldset(
                _("About client"),
                Row(
                    Column('first_name'),
                    Column('last_name'),
                ),
                'person_address',
                Row(
                    Column(
                        'person_country',
                        css_class='col-md-4'
                    ),
                    Column(
                        'person_zipcode',
                        css_class='col-md-2'
                    ),
                    Column(
                        'person_city'
                    )
                ),
                'person_email',
                css_class='border-left-info shadow d-none',
                id='person_infos'
            ),

            Fieldset(
                _("Company"),
                'company_name',
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
                HTML('<hr>'),
                Row(
                    Column('contact_first_name'),
                    Column('contact_last_name'),
                ),
                'contact_email',
                id='company_infos',
                css_class='border-left-primary shadow'
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
