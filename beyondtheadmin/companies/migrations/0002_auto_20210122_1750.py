# Generated by Django 3.0.11 on 2021-01-22 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="company",
            options={
                "ordering": ("name", "created"),
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
            },
        ),
    ]
