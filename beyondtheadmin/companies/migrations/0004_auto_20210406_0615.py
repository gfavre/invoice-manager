# Generated by Django 3.1.7 on 2021-04-06 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20210406_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='from_email',
            field=models.CharField(default='Gregory Favre <greg@beyondthewall.ch>', max_length=255, verbose_name='From email'),
        ),
    ]