# Generated by Django 3.2.18 on 2023-07-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_alter_client_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.TextField(blank=True, verbose_name='Name'),
        ),
    ]
