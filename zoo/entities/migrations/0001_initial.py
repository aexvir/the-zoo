# Generated by Django 2.2.19 on 2021-07-27 08:29

import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("label", models.CharField(max_length=100)),
                ("owner", models.CharField(max_length=50)),
                (
                    "kind",
                    models.CharField(
                        blank=True,
                        choices=[("component", "component")],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("type", models.CharField(max_length=32)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_owner", models.CharField(max_length=100)),
                ("project_owner", models.CharField(max_length=100)),
                (
                    "maintainers",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        default=list,
                        help_text="List of maintainers",
                        size=None,
                        validators=[django.core.validators.EmailValidator],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32)),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="https://fomantic-ui.com/elements/icon.html",
                        max_length=16,
                        null=True,
                    ),
                ),
                ("url", models.URLField()),
                (
                    "entity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        related_query_name="link",
                        to="entities.Entity",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="entity",
            name="group",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="entities.Group",
            ),
        ),
        migrations.AddField(
            model_name="entity",
            name="library",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="libraries.Library",
            ),
        ),
        migrations.AddField(
            model_name="entity",
            name="service",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="services.Service",
            ),
        ),
        migrations.AddField(
            model_name="entity",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="entities",
                related_query_name="entity",
                to="repos.Repository",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="entity",
            unique_together={("name", "source")},
        ),
    ]
