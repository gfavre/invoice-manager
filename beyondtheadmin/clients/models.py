from decimal import Decimal

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from model_utils import Choices

from beyondtheadmin.utils.model_utils import UUIDModel


class Client(UUIDModel):
    TYPES = Choices(("company", _("Company")), ("person", _("Person")))
    client_type = models.CharField(
        _("Client type"), choices=TYPES, default=TYPES.company, max_length=10
    )

    company_name = models.CharField(_("Name"), max_length=255, blank=True)

    contact_first_name = models.CharField(_("Contact first name"), max_length=255, blank=True)
    contact_last_name = models.CharField(_("Contact last name"), max_length=255, blank=True)
    contact_email = models.EmailField(_("Contact email"), blank=True)

    address = models.TextField(_("Address"), blank=True)
    zip_code = models.CharField(_("Postal code"), max_length=10, blank=True)
    city = models.CharField(_("City"), max_length=255, blank=True)
    country = CountryField(_("Country"), blank=True, null=True, default="CH")

    language = models.CharField(
        _("Language"),
        max_length=2,
        choices=(
            ("en", "English"),
            ("de", "Deutsch"),
            ("fr", "Français"),
            ("it", "Italiano"),
        ),
        default="fr",
    )
    currency = models.CharField(
        _("Currency"),
        max_length=3,
        choices=(("CHF", "CHF"), ("EUR", "Euro")),
        default="CHF",
    )
    payment_delay_days = models.IntegerField(
        _("Payment delay"), help_text=_("Default delay in days to due date"), default=30
    )
    vat_rate = models.DecimalField(
        _("VAT rate"),
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.077"),
        blank=True,
    )
    default_hourly_rate = models.DecimalField(
        _("Default hourly rate"), max_digits=5, decimal_places=2, default="0.00"
    )

    email_template = models.TextField(
        verbose_name=_("Email Template"),
        help_text=_(
            "Default text for invoices sent by mail. Use double curly braces {{ and }} as delimiters for variables."
        ),
        blank=True,
    )

    slug = models.CharField(
        _("Slug"), help_text=_("Used to generate invoice code"), max_length=15, blank=True
    )
    invoice_current_count = models.IntegerField(
        _("Current count of invoices"),
        help_text=_("Used to generate invoice code"),
        default=0,
    )
    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        related_name="clients",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("company_name", "contact_last_name", "country")

    @property
    def api_url(self):
        return reverse_lazy("api:client-detail", kwargs={"pk": self.pk})

    @property
    def name(self):
        if self.is_company:
            return self.company_name
        return self.contact_fullname

    @property
    def contact_fullname(self):
        if self.contact_last_name:
            return "{} {}".format(self.contact_first_name, self.contact_last_name)
        return self.contact_first_name

    @property
    def full_contact_email(self):
        if self.contact_fullname:
            return "{} <{}>".format(self.contact_fullname, self.contact_email)

    @property
    def is_company(self):
        return self.client_type == self.TYPES.company

    @property
    def is_person(self):
        return self.client_type == self.TYPES.person

    @property
    def last_invoice_date(self):
        last_invoice = self.invoices.order_by("displayed_date").last()
        if last_invoice:
            return last_invoice.displayed_date
        return None

    def get_absolute_url(self):
        return reverse_lazy("clients:update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("clients:delete", kwargs={"pk": self.pk})

    def get_update_url(self):
        return self.get_absolute_url()

    def __str__(self):
        return (
            self.client_type == self.TYPES.company and self.company_name or self.contact_fullname
        )
