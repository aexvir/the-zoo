# Generated by Django 2.2.16 on 2020-09-15 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instance", "0005_auto_20200915_0841"),
    ]

    operations = [
        migrations.AddField(
            model_name="helpers",
            name="service_exclusions",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="placeholders",
            name="service_exclusions",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
