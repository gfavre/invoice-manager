from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0004_auto_20210406_0615"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="bcc_email",
            field=models.EmailField(
                blank=True,
                help_text="Email address that will receive every sent invoice in bcc",
                max_length=254,
                verbose_name="Copy of invoices",
            ),
        ),
    ]
