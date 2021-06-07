# Generated by Django 3.1.7 on 2021-06-07 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0013_auto_20210426_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, editable=False, max_digits=7, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
