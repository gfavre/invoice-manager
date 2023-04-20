import datetime
from decimal import ROUND_UP, Decimal
from io import StringIO

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from dateutil.relativedelta import relativedelta
from model_utils import Choices
from model_utils.models import StatusModel
from qrbill.bill import QRBill

from beyondtheadmin.utils.model_utils import UUIDModel


class OpenInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__in=(Invoice.STATUS.sent, Invoice.STATUS.paid))


class Invoice(UUIDModel, StatusModel):
    STATUS = Choices(
        ("draft", _("Draft")),
        ("sent", _("Sent")),
        ("paid", _("Paid")),
        ("canceled", _("canceled")),
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
        verbose_name=_("Company"),
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="invoices",
        null=True,
        blank=True,
        verbose_name=_("Client"),
    )
    code = models.CharField(_("Code"), max_length=30, blank=True)
    due_date = models.DateField(_("Due date"), null=True, blank=True)
    displayed_date = models.DateField(_("Displayed date"), blank=True, null=True)
    vat_rate = models.DecimalField(
        _("VAT rate"),
        max_digits=6,
        decimal_places=4,
        default=Decimal("0.077"),
        blank=True,
    )
    total = models.DecimalField(
        _("Total"),
        max_digits=7,
        decimal_places=2,
        default=0.0,
        blank=True,
        editable=False,
    )

    title = models.CharField(_("Title"), max_length=100, blank=True)
    description = RichTextField(_("Description"), blank=True)
    period_start = models.DateField(_("Start of invoice period"), blank=True, null=True)
    period_end = models.DateField(_("End of invoice period"), blank=True, null=True)

    version = models.PositiveIntegerField(_("Version"), default=1, editable=False)

    qr_bill = models.TextField(_("QR Bill"), blank=True, null=True)
    sent_date = models.DateTimeField(_("Sent date"), blank=True, null=True)
    last_reminder_date = models.DateTimeField(_("Last reminder date"), blank=True, null=True)

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="invoices_created",
        null=True,
        blank=True,
        verbose_name=_("Created by"),
    )

    objects = models.Manager()
    visible = OpenInvoiceManager()

    class Meta:
        ordering = ("-due_date",)

    def __str__(self):
        return self.code

    @property
    def displayed_datetime(self):
        if self.due_date:
            return datetime.datetime(
                self.displayed_date.year,
                self.displayed_date.month,
                self.displayed_date.day,
            )
        return None

    @property
    def due_datetime(self):
        if self.due_date:
            return datetime.datetime(self.due_date.year, self.due_date.month, self.due_date.day)
        return None

    @property
    def is_draft(self):
        return self.status == self.STATUS.draft

    @property
    def is_sent(self):
        return self.status == self.STATUS.sent

    @property
    def is_paid(self):
        return self.status == self.STATUS.paid

    @property
    def is_ready(self):
        conditions = [
            self.displayed_date is not None,
            self.due_date is not None,
            self.company is not None,
            self.client is not None,
            self.title != "",
            self.period_start is None or self.period_end is not None,
            self.period_end is None or self.period_start is not None,
        ]
        return all(conditions) and self.lines.exists()

    @property
    def is_overdue(self):
        return self.status == self.STATUS.sent and self.due_date < now().date()

    @property
    def latest_pdf(self):
        try:
            return self.pdfs.get(version=self.version).pdf
        except InvoicePDF.DoesNotExist:
            return None

    @property
    def subtotal(self):
        acc = Decimal("0.0")
        for line in self.lines.all():
            acc += line.total
        return acc

    def add_pdf(self, content, version):
        invoice_pdf, created = InvoicePDF.objects.get_or_create(invoice=self, version=version)
        invoice_pdf.pdf.save("{}.pdf".format(self.code), ContentFile(content), save=False)
        invoice_pdf.status = InvoicePDF.STATUS.ready
        invoice_pdf.save()

    def duplicate(self):
        previous_pk = self.pk
        self.pk = None
        self.code = ""
        self.displayed_date = now().date()
        self.due_date = self.displayed_date + relativedelta(days=self.client.payment_delay_days)
        if self.period_start:
            self.period_start = self.period_start + relativedelta(months=1)
        if self.period_end:
            self.period_end = self.period_end + relativedelta(months=1)
        self.status = Invoice.STATUS.draft
        self.version = 1
        self.pdf = None
        self.pdf_version = None
        self.qr_bill = None
        self.save(generate_code=False)
        assert previous_pk != self.pk
        for line in InvoiceLine.objects.filter(invoice_id=previous_pk):
            line.pk = None
            line.invoice = self
            line.save()
        return self

    def get_absolute_url(self):
        return reverse("invoice-print", kwargs={"pk": self.pk})

    def get_api_url(self):
        return reverse("api:invoice-detail", kwargs={"pk": self.pk})

    def get_api_lines_url(self):
        return reverse("api:invoices-lines-list", kwargs={"invoice_pk": self.pk})

    def get_cancel_url(self):
        return reverse("invoices:cancel", kwargs={"pk": self.pk})

    def get_code(self):
        return "{}-{}".format(self.client.slug, self.client.invoice_current_count + 1)

    def get_duplicate_url(self):
        return reverse("invoices:duplicate", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("invoices:update", kwargs={"pk": self.pk})

    def generate_latest_pdf(self):
        from .pdf import build_content_for_pdf, generate_pdf

        content = build_content_for_pdf(self)
        generated_pdf = generate_pdf(content)
        self.add_pdf(generated_pdf, self.version)

    def get_pdf_generation_url(self):
        return reverse(
            "api:invoices-pdf-detail",
            kwargs={"invoice_pk": self.pk, "version": self.version},
        )

    def get_qrbill(self):
        if not (self.due_date and self.company and self.client):
            raise ValueError
        qr_bill = QRBill(
            account=self.company.iban,
            debtor={
                "name": self.client.name,
                "pcode": self.client.zip_code,
                "city": self.client.city,
                "country": self.client.country.code,
            },
            extra_infos=self.code,
            creditor={
                "name": self.company.bank_account_name,
                "street": self.company.address,
                "pcode": self.company.zip_code,
                "city": self.company.city,
                "country": self.company.country.code,
            },
            language=self.client.language,
            due_date=self.due_date.strftime("%Y-%m-%d"),
            amount=self.get_total(),
        )

        return qr_bill

    def get_qrbill_url(self):
        return reverse("qrbill", kwargs={"pk": self.pk})

    def get_reminder_url(self):
        return reverse("invoices:reminder", kwargs={"pk": self.pk})

    def get_set_paid_url(self):
        return reverse("invoices:mark_paid", kwargs={"pk": self.pk})

    def get_send_url(self):
        return reverse("invoices:send", kwargs={"pk": self.pk})

    def get_snail_mail_url(self):
        return reverse("invoices:mark_sent", kwargs={"pk": self.pk})

    def get_total(self):
        return self.subtotal + self.get_vat()

    def get_vat(self):
        return (self.subtotal * self.vat_rate).quantize(Decimal(".01"), rounding=ROUND_UP)

    def check_rights(self, user):
        if not self.company:
            return self.created_by == user
        return self.company in user.companies.all()

    def save(self, update_version=True, generate_code=False, *args, **kwargs):
        if not self.code and generate_code:
            self.code = self.get_code()
            self.client.invoice_current_count += 1
            self.client.save()
        if not self.displayed_date:
            self.displayed_date = self.created
        if update_version:
            self.total = self.get_total()
            self.version += 1
            try:
                qr_bill = self.get_qrbill()
                qr_io = StringIO()
                qr_bill.as_svg(qr_io, full_page=False)
                self.qr_bill = qr_io.getvalue()
            except ValueError:
                pass
        super().save(*args, **kwargs)

    def set_canceled(self):
        self.status = self.STATUS.canceled
        self.save(update_fields=["status"])

    def set_draft(self):
        self.status = self.STATUS.draft
        self.save(update_fields=["status"])

    def set_paid(self):
        self.status = self.STATUS.paid
        self.save(update_fields=["status"])

    def set_sent(self):
        self.status = self.STATUS.sent
        self.sent_date = now()
        self.save(update_fields=["status", "sent_date"])

    @staticmethod
    def get_overdue_query_params(values):
        if values and values[0] == "overdue":
            return {"status": Invoice.STATUS.sent, "due_date__lt": now().date()}
        else:
            return {"status": Invoice.STATUS.sent, "due_date__gt": now().date()}


class InvoicePDF(UUIDModel, StatusModel):
    STATUS = Choices(("generating", _("Generating")), ("ready", _("Ready")), ("error", _("Error")))
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="pdfs")
    pdf = models.FileField(_("PDF"), null=True, upload_to="invoices/", editable=False)
    version = models.PositiveIntegerField(_("Version of PDF"), null=True, editable=False)

    class Meta:
        unique_together = ("invoice", "version")


class InvoiceLine(UUIDModel):
    invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE, related_name="lines")

    description = models.TextField()
    note = models.TextField(blank=True)

    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Choices(("h", _("Hour")), ("nb", _("Number"))))
    price_per_unit = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ("created",)

    @property
    def is_hours(self):
        return self.unit == "h"

    @property
    def total(self):
        return (self.price_per_unit * self.quantity).quantize(Decimal(".01"), rounding=ROUND_UP)

    def get_api_url(self, request=None):
        from rest_framework.reverse import reverse

        return reverse(
            "api:invoices-lines-detail",
            kwargs={"pk": self.pk, "invoice_pk": self.invoice.pk},
            request=request,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.save(generate_code=False)
