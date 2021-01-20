from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import StatusModel
from model_utils import Choices
from beyondtheadmin.utils.models import UUIDModel


class Invoice(UUIDModel, StatusModel):
    STATUS = Choices(
        ('draft', _("Draft"))
        ('sent', _("Sent"))
        ('paid', _("Paid"))
        ('canceled', _("canceled"))
    )
    client = models.ForeignKey('beyondtheadmin.clients.Client', on_delete=models.PROTECT, related_name='invoices')
    code = models.CharField(blank=False, max_length=13)
    expiration = models.DateField(null=False, blank=False)
    displayed_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '{}-{}'.format(self.client.slug,
                                       self.objects.filter(client=self.client).count() + 1)
        super().save(*args, **kwargs)


class InvoiceLine(UUIDModel):
    description = models.TextField()
    note = models.TextField(blank=True)

    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(choices=Choices(
        ('h', _("Hour")),
        ('nb', _("Number"))
    ))
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def total(self):
        return self.price_per_unit * self.quantity
