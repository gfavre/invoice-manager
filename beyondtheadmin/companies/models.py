from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField
from django_countries.fields import CountryField
from localflavor.generic.models import BICField, IBANField
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
    override_default_from_email = models.BooleanField(_("Override default from email"), default=False)
    from_email = models.CharField(
        _("From email"), max_length=255, default='{} <{}>'.format(settings.ADMINS[0][0], settings.ADMINS[0][1])
    )
    bcc_email = models.EmailField(
        _("Copy of invoices"), help_text=_("Email address that will receive every sent invoice in bcc"),
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
    def all_invoices_api_url(self):
        return reverse('api:company-invoices', kwargs={'company_pk': self.pk})

    @property
    def bank_account_name(self):
        return self.name_for_bank or self.name

    @property
    def delete_url(self):
        return reverse('companies:delete', kwargs={'pk': self.pk})

    @property
    def earnings_api_url(self):
        return reverse('api:earnings-per-company', kwargs={'company_pk': self.pk})

    @property
    def detail_url(self):
        return reverse('companies:detail', kwargs={'pk': self.pk})

    @property
    def edit_url(self):
        return reverse('companies:update', kwargs={'pk': self.pk})

    @property
    def has_signature(self):
        return bool(self.signature_text or self.signature_image)

    @property
    def invoice_from_email(self):
        if self.override_default_from_email:
            return self.from_email
        return f'{self.name} <{settings.DEFAULT_INVOICE_FROM_EMAIL}>'

    @property
    def open_invoices_api_url(self):
        return reverse('api:open-invoices-per-company', kwargs={'company_pk': self.pk})

    @property
    def single_line_address(self):
        output = []
        if self.address:
            output.append(self.address)
        if self.zip_code:
            output.append(f'{self.zip_code} {self.city}')
        if self.country:
            output.append(self.country.name)
        return ', '.join(output)

    def open_invoices(self):
        from beyondtheadmin.invoices.models import Invoice
        return Invoice.visible.filter(company=self).select_related('client')

    def latest_open_invoices(self):
        return self.open_invoices().order_by('-due_date')[:5]

    def get_absolute_url(self):
        return self.detail_url


class CompanyClient(TimeStampedModel):
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients')
    invoice_current_count = models.IntegerField(_("Current count of invoices"),
                                                help_text=_("Used to generate invoice code"),
                                                default=0)

    def __str__(self):
        return f'{self.client} - {self.company}'

    class Meta:
        ordering = ('company', 'client')
        unique_together = ('client', 'company')
        verbose_name = _("Company client")
        verbose_name_plural = _("Company clients")
