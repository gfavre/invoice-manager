# Generated by Django 3.0.11 on 2021-01-21 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='vat_rate',
            field=models.DecimalField(decimal_places=4, default=0.065, max_digits=6),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='code',
            field=models.CharField(editable=False, max_length=13),
        ),
    ]
