# Generated by Django 2.2.12 on 2020-08-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analytics", "0016_auto_20200311_1021"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dependencyusage",
            name="version",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
