# Generated by Django 2.2.12 on 2020-08-27 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0022_add_pagerduty_service"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="pagerduty_url",
        ),
    ]
