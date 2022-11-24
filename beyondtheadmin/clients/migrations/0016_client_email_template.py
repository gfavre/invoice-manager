# Generated by Django 3.2.12 on 2022-05-12 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0015_alter_client_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="email_template",
            field=models.TextField(
                blank=True,
                help_text="Default text for invoices sent by mail. Use double curly braces {{ and }} as delimiters for variables.",
                verbose_name="Email Template",
            ),
        ),
    ]
