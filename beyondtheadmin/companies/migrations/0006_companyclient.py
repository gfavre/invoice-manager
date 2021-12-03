# Generated by Django 3.1.7 on 2021-08-17 21:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_remove_client_company'),
        ('companies', '0005_company_bcc_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('invoice_current_count', models.IntegerField(default=0, help_text='Used to generate invoice code', verbose_name='Current count of invoices')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='clients.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='companies.company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
