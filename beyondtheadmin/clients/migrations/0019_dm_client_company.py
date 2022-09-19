# Generated by Django 3.2.12 on 2022-09-17 19:43

from django.db import migrations


def add_company_to_client(apps, schema_editor):
    # noinspection PyPep8Naming
    CompanyClient = apps.get_model('companies', 'CompanyClient')
    for company_client in CompanyClient.objects.all():
        client = company_client.client
        client.company = company_client.company
        client.invoice_current_count = company_client.invoice_current_count
        client.save()


def add_client_to_company_client(apps, schema_editor):
    CompanyClient = apps.get_model('companies', 'CompanyClient')
    Client = apps.get_model('clients', 'Client')
    for client in Client.objects.all():
        CompanyClient.objects.create(
            company=client.company,
            client=client.client,
            invoice_current_count=client.invoice_current_count,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0018_client_company'),
    ]

    operations = [
        migrations.RunPython(add_company_to_client, reverse_code=add_client_to_company_client),
    ]