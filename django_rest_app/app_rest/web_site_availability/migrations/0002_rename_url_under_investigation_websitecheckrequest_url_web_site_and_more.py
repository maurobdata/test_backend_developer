# Generated by Django 4.0.dev20210622105104 on 2021-07-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web_site_availability", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="websitecheckrequest",
            old_name="url_under_investigation",
            new_name="url_web_site",
        ),
        migrations.AddField(
            model_name="singlecheckrequest",
            name="lib_request_type",
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="websitecheckrequest",
            name="lib_request_type",
            field=models.CharField(editable=False, max_length=200, null=True),
        ),
    ]
