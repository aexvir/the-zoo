import re

from django.conf import settings
from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from djangoql.schema import DjangoQLSchema

from zoo.services.constants import Impact, Lifecycle


class Library(models.Model):
    class Meta:
        unique_together = ("owner", "name")
        verbose_name_plural = "libraries"

    owner = pg_fields.CICharField(max_length=100)
    name = pg_fields.CICharField(max_length=100)
    lifecycle = models.CharField(
        choices=((item.value, item.value) for item in Lifecycle),
        null=True,
        blank=True,
        max_length=100,
    )
    impact = models.CharField(
        choices=((item.value, item.value) for item in Impact),
        null=True,
        blank=True,
        max_length=100,
    )
    slack_channel = models.CharField(max_length=22, null=True, blank=True)
    sonarqube_project = models.CharField(max_length=250, null=True, blank=True)
    repository = models.ForeignKey(
        "repos.Repository",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="libraries",
    )
    docs_url = models.URLField(max_length=500, null=True, blank=True)
    library_url = models.URLField(max_length=500, null=True, blank=True)
    owner_slug = models.SlugField(max_length=140)
    name_slug = models.SlugField(max_length=140)
    tags = pg_fields.ArrayField(
        base_field=models.CharField(max_length=50), blank=True, default=list
    )

    def get_absolute_url(self):
        return reverse("library_detail", args=[self.owner_slug, self.name_slug])

    @property
    def key(self):
        return f"{self.owner}/{self.name}"

    @property
    def owner_url(self):
        if self.repository:
            return f"{settings.GITLAB_URL}/{self.repository.owner}"

    @property
    def gitlab_url(self):
        if self.repository:
            return (
                f"{settings.GITLAB_URL}/{self.repository.owner}/{self.repository.name}"
            )

    @property
    def slack_url(self):
        if self.slack_channel:
            return f"{settings.SLACK_URL}/messages/{self.slack_channel}"

    def __str__(self):
        return f"{self.key}"


def slugify_attribute(attribute):
    return re.sub("[^0-9a-zA-Z]+", "-", attribute)


@receiver(models.signals.pre_save, sender=Library)
def generate_slugs(sender, instance, *args, **kwargs):
    instance.owner_slug = slugify_attribute(instance.owner)
    instance.name_slug = slugify_attribute(instance.name)


class LibraryQLSchema(DjangoQLSchema):
    include = (Library,)

    def get_fields(self, model):
        if isinstance(model, Library):
            return ["name", "owner", "lifecycle", "impact", "library_url"]
        return super().get_fields(model)
