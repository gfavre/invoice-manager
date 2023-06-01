from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django_countries.fields import CountryField
from localflavor.generic.models import BICField, IBANField
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from beyondtheadmin.utils.model_utils import UUIDModel


STATUS = Choices(
    ("active", _("Active")),
    ("inactive", _("Inactive")),
)


class ActiveCompanyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=STATUS.active)


class Company(UUIDModel):
    name = models.CharField(_("Company name"), max_length=255)
    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

    phone = PhoneNumberField(_("Phone number"), blank=True)
    additional_phone = PhoneNumberField(_("Additional phone number"), blank=True)

    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Web site"), blank=True)
    enable_vat = models.BooleanField(_("Enable VAT"), default=True)
    vat_id = models.CharField(_("VAT ID"), blank=True, max_length=20)
    vat_rate = models.DecimalField(
        _("VAT rate"),
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.077"),
        blank=True,
    )

    name_for_bank = models.CharField(_("Bank account's owner name"), max_length=255, blank=True)
    bank = models.TextField(_("Bank"), blank=True)
    bic = BICField(_("BIC"), blank=True)
    iban = IBANField(_("IBAN"), blank=True)

    logo = models.ImageField(_("Logo"), blank=True, null=True)
    contrast_color = ColorField(_("Contrast color"), default="#3B4451")

    signature_text = models.CharField(_("Signature as text"), max_length=100, blank=True)
    signature_image = models.ImageField(_("Signature as image"), null=True, blank=True)
    email_signature = models.TextField(_("Email signature"), blank=True)
    invoice_note = RichTextField(
        _("Notes"),
        blank=True,
        help_text=_("Displayed between banking details and signature"),
    )

    override_default_from_email = models.BooleanField(
        _("Override default from email"), default=False
    )
    from_email = models.CharField(
        _("From email"),
        max_length=255,
        default=f"{settings.ADMINS[0][0]} <{settings.ADMINS[0][1]}>",
        blank=True,
    )
    bcc_email = models.EmailField(
        _("Copy of invoices"),
        help_text=_("Email address that will receive every sent invoice in bcc"),
        blank=True,
    )
    thanks = models.TextField(
        _("Thanks"),
        blank=True,
        help_text=_(
            "Thanks at bottom of invoice. If set, this will be on every invoice, regardless of language"
        ),
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS,
        default=STATUS.active,
    )
    objects = ActiveCompanyManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ("name", "created")
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

    @property
    def api_url(self):
        return reverse("api:company-detail", kwargs={"pk": self.pk})

    @property
    def all_invoices_api_url(self):
        return reverse("api:company-invoices", kwargs={"company_pk": self.pk})

    @property
    def bank_account_name(self):
        return self.name_for_bank or self.name

    @property
    def delete_url(self):
        return reverse("companies:delete", kwargs={"pk": self.pk})

    @property
    def earnings_api_url(self):
        return reverse("api:earnings-per-company", kwargs={"company_pk": self.pk})

    @property
    def detail_url(self):
        return reverse("companies:detail", kwargs={"pk": self.pk})

    @property
    def edit_url(self):
        return reverse("companies:update", kwargs={"pk": self.pk})

    @property
    def has_signature(self):
        return bool(self.signature_text or self.signature_image)

    @property
    def invoice_from_email(self):
        if self.override_default_from_email:
            return self.from_email
        return f"{self.name} <{settings.DEFAULT_INVOICE_FROM_EMAIL}>"

    @property
    def open_invoices_api_url(self):
        return reverse("api:open-invoices-per-company", kwargs={"company_pk": self.pk})

    @property
    def single_line_address(self):
        output = []
        if self.address:
            output.append(self.address)
        if self.zip_code:
            output.append(f"{self.zip_code} {self.city}")
        if self.country:
            output.append(self.country.name)
        return ", ".join(output)

    def set_deleted(self):
        self.status = STATUS.inactive
        self.save()

    def open_invoices(self):
        from beyondtheadmin.invoices.models import Invoice

        return Invoice.visible.filter(company=self).select_related("client")

    def latest_open_invoices(self):
        return self.open_invoices().order_by("-due_date")[:5]

    def get_absolute_url(self):
        return self.detail_url


class Bank(TimeStampedModel):
    name = models.CharField(_("Bank name"), max_length=255)
    code = models.IntegerField(_("Code"), null=True)
    swift = models.CharField(_("BIC/Swift"), blank=True, max_length=11)

    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True)

    class Meta:
        ordering = ("name", "created")
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

    def __str__(self):
        return self.name
