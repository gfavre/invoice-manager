from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from beyondtheadmin.utils.models import UUIDModel


class Client(UUIDModel):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=10)
    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

