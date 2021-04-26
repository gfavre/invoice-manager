# Generated by Django 3.1.7 on 2021-04-26 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20210406_0630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='default_hourly_rate',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=5, verbose_name='Default hourly rate'),
        ),
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.CharField(help_text='Used to generate invoice code', max_length=10, verbose_name='Slug'),
        ),
    ]
