# Generated by Django 3.1.7 on 2021-02-25 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0011_auto_20210225_0507"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="pdf",
            field=models.FileField(
                editable=False, null=True, upload_to="invoices/", verbose_name="PDF"
            ),
        ),
    ]
