# Generated by Django 4.0.dev20210622105104 on 2021-07-05 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_site_availability', '0004_remove_website_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlecheckrequest',
            name='pattern_regular_expression',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='websitecheckrequest',
            name='pattern_regular_expression',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
