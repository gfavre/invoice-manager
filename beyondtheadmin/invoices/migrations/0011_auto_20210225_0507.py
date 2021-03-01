# Generated by Django 3.1.7 on 2021-02-25 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0010_auto_20210217_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='pdf',
            field=models.FileField(null=True, upload_to='invoices/', verbose_name='PDF'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='pdf_version',
            field=models.PositiveIntegerField(editable=False, null=True, verbose_name='Version of PDF'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='version',
            field=models.PositiveIntegerField(default=1, editable=False, verbose_name='Version'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='code',
            field=models.CharField(blank=True, editable=False, max_length=30, verbose_name='Code'),
        ),
    ]