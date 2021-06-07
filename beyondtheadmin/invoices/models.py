from decimal import Decimal, ROUND_UP
from io import StringIO

from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from ckeditor.fields import RichTextField
from dateutil.relativedelta import relativedelta
from model_utils.models import StatusModel
from model_utils import Choices
from qrbill.bill import QRBill

from beyondtheadmin.utils.model_utils import UUIDModel


class Invoice(UUIDModel, StatusModel):
    STATUS = Choices(
        ('draft', _("Draft")),
        ('sent', _("Sent")),
        ('paid', _("Paid")),
        ('canceled', _("canceled")),
    )
    company = models.ForeignKey('companies.Company', on_delete=models.PROTECT, related_name='invoices',
                                null=True,  blank=False, verbose_name=_("Company"))
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='invoices', null=False,
                               verbose_name=_("Client"))
    code = models.CharField(_("Code"), max_length=30, blank=True)
    due_date = models.DateField(_("Due date"), null=True, blank=False)
    displayed_date = models.DateField(_("Displayed date"), blank=True, null=True)
    vat_rate = models.DecimalField(_("VAT rate"), max_digits=6, decimal_places=4, default=Decimal('0.077'), blank=True)
    total = models.DecimalField(_("Total"), max_digits=7, decimal_places=2, default=0.0, blank=True, editable=False)

    title = models.CharField(_("Title"), max_length=100, blank=True)
    description = RichTextField(_("Description"), blank=True)
    period_start = models.DateField(_("Start of invoice period"), blank=True, null=True)
    period_end = models.DateField(_("End of invoice period"), blank=True, null=True)

    version = models.PositiveIntegerField(_("Version"), default=1, editable=False)

    pdf = models.FileField(_("PDF"), null=True, upload_to='invoices/', editable=False)
    pdf_version = models.PositiveIntegerField(_("Version of PDF"), null=True, editable=False)

    qr_bill = models.TextField(_("QR Bill"), blank=True, null=True)

    class Meta:
        ordering = ('displayed_date',)

    def __str__(self):
        return self.code

    @property
    def is_draft(self):
        return self.status == self.STATUS.draft

    @property
    def is_sent(self):
        return self.status == self.STATUS.sent

    @property
    def latest_pdf_url(self):
        if self.pdf_version != self.version:
            self.generate_pdf()
        return self.pdf.url

    @property
    def subtotal(self):
        acc = Decimal('0.0')
        for line in self.lines.all():
            acc += line.total
        return acc

    def add_pdf(self, content):
        self.pdf.save('{}.pdf'.format(self.code), ContentFile(content), save=False)
        self.pdf_version = self.version
        self.save(update_version=False)

    def duplicate(self):
        previous_pk = self.pk
        self.pk = None
        self.code = ''
        self.displayed_date = now().date()
        if self.period_start:
            self.period_start = self.period_start + relativedelta(months=1)
        if self.period_end:
            self.period_end = self.period_end + relativedelta(months=1)
        self.status = Invoice.STATUS.draft
        self.version = 1
        self.pdf = None
        self.pdf_version = None
        self.qr_bill = None
        self.save()
        assert(previous_pk != self.pk)
        for line in InvoiceLine.objects.filter(invoice_id=previous_pk):
            line.pk = None
            line.invoice = self
            line.save()
        return self

    def generate_pdf(self):
        from .pdf import generate_pdf
        pdf = generate_pdf(self)
        if pdf:
            self.add_pdf(pdf)

    def get_absolute_url(self):
        return reverse('invoice-print', kwargs={'pk': self.pk})

    def get_api_url(self):
        return reverse('api:invoice-detail', kwargs={'pk': self.pk})

    def get_cancel_url(self):
        return reverse('invoices:cancel', kwargs={'pk': self.pk})

    def get_duplicate_url(self):
        return reverse('invoices:duplicate', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('invoices:update', kwargs={'pk': self.pk})

    def get_set_paid_url(self):
        return reverse('invoices:mark_paid', kwargs={'pk': self.pk})

    def get_send_url(self):
        return reverse('invoices:send', kwargs={'pk': self.pk})

    def get_qrbill_url(self):
        return reverse('qrbill', kwargs={'pk': self.pk})

    def get_snail_mail_url(self):
        return reverse('invoices:mark_sent', kwargs={'pk': self.pk})

    def get_vat(self):
        return (self.subtotal * self.vat_rate).quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_total(self):
        return self.subtotal + self.get_vat()

    def get_code(self):
        return '{}-{}'.format(self.client.slug, self.client.invoice_current_count + 1)

    def get_qrbill(self):
        if not self.due_date:
            raise ValueError
        qr_bill = QRBill(
            account=self.company.iban,
            debtor={
                'name': self.client.name,
                'pcode': self.client.zip_code, 'city': self.client.city,
                'country': self.client.country.code,
            },
            extra_infos=self.code,
            creditor={
                'name': self.company.name, 'street': self.company.address,
                'pcode': self.company.zip_code, 'city': self.company.city,
                'country': self.company.country.code,
            },
            language=self.client.language,
            due_date=self.due_date.strftime('%Y-%m-%d'),
            amount=self.get_total(),
        )
        qr_bill.title_font_info = {'font_size': '11pt', 'font_weight': '500'}
        qr_bill.font_info = {'font_size': '8pt', 'font-weight': '300'}
        qr_bill.head_font_info = {'font_size': '7.5pt', 'font_weight': '500'}
        qr_bill.proc_font_info = {'font_size': '7.5pt'}
        return qr_bill

    def save(self, update_version=True, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
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
                qr_bill.as_svg(qr_io)
                self.qr_bill = qr_io.getvalue()
            except ValueError:
                pass
        super().save(*args, **kwargs)

    def set_sent(self):
        self.status = self.STATUS.sent
        self.save(update_fields=["status"])


class InvoiceLine(UUIDModel):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='lines')

    description = models.TextField()
    note = models.TextField(blank=True)

    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Choices(
        ('h', _("Hour")),
        ('nb', _("Number"))
    ))
    price_per_unit = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('created', )

    @property
    def is_hours(self):
        return self.unit == 'h'

    @property
    def total(self):
        return (self.price_per_unit * self.quantity).quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_api_url(self, request=None):
        from rest_framework.reverse import reverse

        return reverse('api:invoices-lines-detail', kwargs={'pk': self.pk, 'invoice_pk': self.invoice.pk},
                       request=request)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.save()
