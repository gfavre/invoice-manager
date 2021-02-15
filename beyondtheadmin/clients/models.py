from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from beyondtheadmin.utils.model_utils import UUIDModel


class Client(UUIDModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=10)
    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

    language = models.CharField(max_length=2,
                                choices=(('en', 'English'), ('de', 'Deutsch'), ('fr', 'Français'), ('it', 'Italiano')),
                                default='fr')
    currency = models.CharField(max_length=3, choices=(('CHF', 'CHF'), ('EUR', 'Euro')), default='CHF')

    contact_name = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '#'
