# Generated by Django 3.0.11 on 2021-02-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_invoice_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, editable=False, max_digits=6),
        ),
    ]
