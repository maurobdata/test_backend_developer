# Generated by Django 4.0.dev20210622105104 on 2021-07-05 00:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site_availability', '0002_rename_url_under_investigation_websitecheckrequest_url_web_site_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlecheckrequest',
            name='completed_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='singlecheckrequest',
            name='regular_expression',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator()]),
        ),
        migrations.AlterField(
            model_name='singlecheckrequest',
            name='url',
            field=models.CharField(max_length=200, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='website',
            name='completed_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='favourite',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='mnemonic_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.CharField(max_length=200, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='websitecheckrequest',
            name='completed_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='websitecheckrequest',
            name='regular_expression',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.RegexValidator()]),
        ),
    ]
