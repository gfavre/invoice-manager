from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from beyondtheadmin.utils.model_utils import UUIDModel


class Client(UUIDModel):
    name = models.CharField(_("Name"), max_length=255)
    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

    language = models.CharField(_("Language"), max_length=2,
                                choices=(('en', 'English'), ('de', 'Deutsch'), ('fr', 'Français'), ('it', 'Italiano')),
                                default='fr')
    currency = models.CharField(_("Currency"), max_length=3, choices=(('CHF', 'CHF'), ('EUR', 'Euro')), default='CHF')
    payment_delay_days = models.IntegerField(_("Payment delay"), help_text=_("Default delay in days to due date"), default=30)
    vat_rate = models.DecimalField(_("VAT rate"), max_digits=6, decimal_places=4, default=Decimal('0.077'), blank=True)
    default_hourly_rate = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')

    contact_name = models.CharField(_("Contact name"), max_length=255, blank=True)
    contact_email = models.EmailField(_("Contact email"), blank=True)

    slug = models.CharField(_("Slug"), max_length=10)
    invoice_current_count = models.IntegerField(_("Current count of invoices"),
                                                help_text=_("Used to generate invoice code"),
                                                default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '#'
