# Generated by Django 3.1.7 on 2021-08-17 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0006_companyclient"),
        ("clients", "0012_remove_client_company"),
        ("users", "0003_user_companies"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="clients",
            field=models.ManyToManyField(
                related_name="users", to="clients.Client", verbose_name="Clients"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="companies",
            field=models.ManyToManyField(
                related_name="users", to="companies.Company", verbose_name="Companies"
            ),
        ),
    ]
