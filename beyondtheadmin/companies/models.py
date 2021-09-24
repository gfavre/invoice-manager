from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from django_countries.fields import CountryField
from localflavor.generic.models import IBANField, BICField
from model_utils.models import TimeStampedModel
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

    name_for_bank = models.CharField(_("Bank account name"), max_length=255, blank=True)
    bank = models.TextField(_("Bank"), blank=True)
    bic = BICField(_("BIC"), blank=True)
    iban = IBANField(_("IBAN"), blank=True)

    logo = models.ImageField(_("Logo"), blank=True, null=True)
    contrast_color = ColorField(_("Contrast color"), default="#3B4451")

    signature_text = models.CharField(_("Signature as text"), max_length=100, blank=True)
    signature_image = models.ImageField(_("Signature as image"), null=True, blank=True)
    email_signature = models.TextField(_("Email signature"), blank=True)
    from_email = models.CharField(_("From email"), max_length=255,
                                   default='{} <{}>'.format(settings.ADMINS[0][0], settings.ADMINS[0][1]))
    bcc_email = models.EmailField(_("Copy of invoices"),
                                  help_text=_("Email address that will receive every sent invoice in bcc"),
                                  blank=True)
    thanks = models.TextField(
        _("Thanks"), blank=True,
        help_text=_("Thanks at bottom of invoice. If set, this will be on every invoice, regardless of language"))

    class Meta:
        ordering = ('name', 'created')
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

    @property
    def bank_account_name(self):
        return self.name_for_bank or self.name

    @property
    def delete_url(self):
        return reverse('companies:delete', kwargs={'pk': self.pk})

    @property
    def edit_url(self):
        return reverse('companies:update', kwargs={'pk': self.pk})

    @property
    def has_signature(self):
        return bool(self.signature_text or self.signature_image)

    def get_absolute_url(self):
        return self.edit_url


class CompanyClient(TimeStampedModel):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients')
    invoice_current_count = models.IntegerField(_("Current count of invoices"),
                                                help_text=_("Used to generate invoice code"),
                                                default=0)

    def __str__(self):
        return f'{self.client} - {self.company}'
