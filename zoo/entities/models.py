from django.contrib.postgres import fields as pg_fields
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models

from zoo.entities.enums import Kind


class Group(models.Model):
    product_owner = models.CharField(max_length=100)
    project_owner = models.CharField(max_length=100)
    maintainers = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        help_text="List of maintainers",
        validators=[EmailValidator],
    )


class Link(models.Model):
    name = models.CharField(max_length=32)
    icon = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text="https://fomantic-ui.com/elements/icon.html",
    )
    url = models.URLField()
    entity = models.ForeignKey(
        "entities.Entity",
        related_name="links",
        related_query_name="link",
        on_delete=models.CASCADE,
    )


class Entity(models.Model):
    class Meta:
        unique_together = ("name", "source")

    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    owner = models.CharField(max_length=50)
    kind = models.CharField(
        choices=((item.value, item.value) for item in Kind),
        null=True,
        blank=True,
        max_length=32,
    )
    type = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)
    tags = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50),
        blank=True,
        default=list,
    )
    group = models.OneToOneField(
        "entities.Group",
        on_delete=models.CASCADE,
        default=None,
    )
    source = models.ForeignKey(
        "repos.Repository",
        related_name="entities",
        related_query_name="entity",
        on_delete=models.PROTECT,
    )
    service = models.OneToOneField(
        "services.Service", on_delete=models.CASCADE, null=True, blank=True
    )
    library = models.OneToOneField(
        "libraries.Library", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}/{self.source.name}"

    def clean(self):
        if self.service and self.library:
            raise ValidationError(
                "Entity instance can be related to Service or "
                "Library at the same time."
            )
