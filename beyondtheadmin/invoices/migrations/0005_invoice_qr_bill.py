# Generated by Django 3.0.11 on 2021-01-21 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20210121_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='qr_bill',
            field=models.TextField(blank=True, null=True),
        ),
    ]
