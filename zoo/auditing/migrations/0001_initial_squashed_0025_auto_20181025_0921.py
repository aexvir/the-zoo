# Generated by Django 2.1.3 on 2018-11-15 16:38

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import zoo.auditing.models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("repos", "0002_add_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="Issue",
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
                ("object_id", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "new"), ("fixed", "fixed")],
                        default=zoo.auditing.models.Issue.Status("new"),
                        max_length=100,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.ContentType",
                    ),
                ),
                ("kind_key", models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name="issue", name="kind_key", field=models.CharField(max_length=500)
        ),
        migrations.AlterField(
            model_name="issue",
            name="status",
            field=models.CharField(
                choices=[("new", "new"), ("fixed", "fixed")],
                default="new",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="details",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True, default=dict
            ),
        ),
        migrations.AddField(
            model_name="issue",
            name="gitlab_issue_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="issue",
            name="comment",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="issue",
            name="last_check",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="issue",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "new"),
                    ("fixed", "fixed"),
                    ("wontfix", "wontfix"),
                    ("not found", "not found"),
                    ("reopened", "reopened"),
                ],
                default="new",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="content_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="contenttypes.ContentType",
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="object_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="issue",
            name="repository",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="issues",
                to="repos.Repository",
            ),
            preserve_default=False,
        ),
        migrations.RunSQL(
            sql="UPDATE auditing_issue SET repository_id = object_id",
            reverse_sql="UPDATE auditing_issue SET object_id = repository_id, content_type_id = (SELECT id FROM django_content_type WHERE app_label = 'repos' AND model = 'repository')",
        ),
        migrations.RemoveField(model_name="issue", name="content_type"),
        migrations.RemoveField(model_name="issue", name="object_id"),
        migrations.RenameField(
            model_name="issue", old_name="gitlab_issue_id", new_name="remote_issue_id"
        ),
    ]
