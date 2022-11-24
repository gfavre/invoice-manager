# Generated by Django 3.1.7 on 2021-08-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0012_remove_client_company"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={"ordering": ("company_name", "contact_last_name", "country")},
        ),
        migrations.RemoveField(
            model_name="client",
            name="name",
        ),
        migrations.AddField(
            model_name="client",
            name="client_type",
            field=models.CharField(
                choices=[("company", "Company"), ("person", "Person")],
                default="company",
                max_length=10,
                verbose_name="Client type",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="company_name",
            field=models.CharField(blank=True, max_length=255, verbose_name="Name"),
        ),
    ]
