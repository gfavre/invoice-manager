from django.db import models
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField, BICField
from phonenumber_field.modelfields import PhoneNumberField

from beyondtheadmin.utils.model_utils import UUIDModel


class Company(UUIDModel):
    name = models.CharField(_("Company name"), max_length=255)
    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

    phone = PhoneNumberField(_("Phone number"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Web site"), blank=True)
    vat_id = models.CharField(_("VAT ID"), blank=True, max_length=20)

    bank = models.TextField(_("Bank"), blank=True)
    bic = BICField(_("BIC"), blank=True)
    iban = IBANField(_("IBAN"), blank=True)

    logo = models.ImageField(_("Logo"), blank=True, null=True)
    contrast_color = ColorField(_("Contrast color"), default="#3B4451")

    signature_text = models.CharField(_("Signature as text"), max_length=100, blank=True)
    signature_image = models.ImageField(_("Signature as image"), null=True, blank=True)

    class Meta:
        ordering = ('name', 'created')
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

    @property
    def has_signature(self):
        return bool(self.signature_text or self.signature_image)
