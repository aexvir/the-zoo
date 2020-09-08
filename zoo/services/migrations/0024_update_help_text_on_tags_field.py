# Generated by Django 2.2.16 on 2020-09-03 13:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0023_remove_service_pagerduty_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                help_text="Used for filtering and defining presets of checks",
                size=None,
            ),
        ),
    ]
