from decimal import Decimal, ROUND_UP
from io import StringIO

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
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
    company = models.ForeignKey('companies.Company', on_delete=models.PROTECT, related_name='invoices', null=True)
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='invoices')
    code = models.CharField(max_length=13, editable=False)
    due_date = models.DateField(null=False, blank=False)
    displayed_date = models.DateField(blank=True, null=True)
    vat_rate = models.DecimalField(max_digits=6, decimal_places=4, default=0.065, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=True, editable=False)

    title = models.CharField(max_length=100, blank=True)
    description = RichTextField(blank=True)
    period_start = models.DateField(blank=True, null=True)
    period_end = models.DateField(blank=True, null=True)

    qr_bill = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.code

    @property
    def subtotal(self):
        acc = Decimal('0.0')
        for line in self.lines.all():
            acc += line.total
        return acc

    def get_absolute_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.pk})

    def get_api_url(self):
        return reverse('api:invoice-detail', kwargs={'pk': self.pk})

    def get_cancel_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.pk})

    def get_duplicate_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('invoices:detail', kwargs={'pk': self.pk})

    def get_qrbill_url(self):
        return reverse('invoices:qrbill', kwargs={'pk': self.pk})

    def get_vat(self):
        return (self.subtotal * self.vat_rate).quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_total(self):
        return self.subtotal + self.get_vat()

    def get_code(self):
        return '{}-{}'.format(self.client.slug, Invoice.objects.filter(client=self.client).count() + 1)

    def get_qrbill(self):
        qr_bill = QRBill(
            account='CH56 0900 0000 2546 2510 8 ',
            debtor={
                'name': self.client.name,
                'pcode': self.client.zip_code, 'city': self.client.city,
                'country': self.client.country.code,
            },
            extra_infos=self.code,
            creditor={
                'name': 'Beyond the Wall', 'street': 'Route de Châtel 19',
                'pcode': '1272', 'city': 'Genolier',
                'country': 'CH',
            },
            language='fr',
            due_date=self.due_date.strftime('%Y-%m-%d'),
            amount=self.get_total(),
        )
        qr_bill.title_font_info = {'font_size': '10pt', 'font_family': 'Helvetica Neue', 'font_weight': 'bold'}
        qr_bill.font_info = {'font_size': '7pt', 'font_family': 'Helvetica Neue', 'font-weight': 300}
        qr_bill.head_font_info = {'font_size': 8, 'font_family': 'Helvetica Neue', 'font_weight': 'bold'}
        qr_bill.proc_font_info = {'font_size': 7, 'font_family': 'Helvetica'}
        return qr_bill

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.get_code()
        if not self.displayed_date:
            self.displayed_date = self.created
        self.total = self.get_total()
        try:
            qr_bill = self.get_qrbill()
            qr_io = StringIO()
            qr_bill.as_svg(qr_io)
            self.qr_bill = qr_io.getvalue()
        except ValueError:
            pass
        super().save(*args, **kwargs)


class InvoiceLine(UUIDModel):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='lines')

    description = models.TextField()
    note = models.TextField(blank=True)

    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Choices(
        ('h', _("Hour")),
        ('nb', _("Number"))
    ))
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def total(self):
        return (self.price_per_unit * self.quantity).quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_api_url(self, request=None):
        from rest_framework.reverse import reverse

        return reverse('api:invoices-lines-detail', kwargs={'pk': self.pk, 'invoice_pk': self.invoice.pk},
                       request=request)
