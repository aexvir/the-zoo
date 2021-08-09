from random import choice, randint

from django.conf import settings
from factory import (
    Factory,
    Faker,
    LazyAttribute,
    LazyFunction,
    SelfAttribute,
    SubFactory,
)
from factory.django import DjangoModelFactory
from faker import Faker as OriginalFaker

from zoo.analytics.models import Dependency, DependencyType, DependencyUsage
from zoo.analytics.tasks.repo_analyzers import unpack_version
from zoo.api.models import ApiToken
from zoo.auditing.check_discovery import Kind
from zoo.auditing.models import Issue
from zoo.datacenters.models import InfraNode
from zoo.entities.models import Entity, Group, Link
from zoo.libraries.models import Library
from zoo.repos.models import Repository, RepositoryEnvironment
from zoo.services.constants import Lifecycle
from zoo.services.models import Environment, Impact, Service, Tier


class RepositoryFactory(DjangoModelFactory):
    class Meta:
        model = Repository

    remote_id = Faker("pyint")
    owner = Faker("user_name")
    name = Faker("domain_word")
    provider = "gitlab"
    url = LazyAttribute(lambda o: f"https://gitlab.com/{o.owner}/{o.name}")


class RepositoryEnvironmentFactory(DjangoModelFactory):
    class Meta:
        model = RepositoryEnvironment

    name = Faker("domain_word")
    repository = SubFactory(RepositoryFactory)
    external_url = LazyAttribute(lambda o: f"https://gitlab.com/{o.name}/{o.name}")


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    repository = SubFactory(RepositoryFactory)
    kind_key = LazyAttribute(
        lambda o: "{}:{}".format(
            OriginalFaker().domain_word(), OriginalFaker().domain_word()
        )
    )


class TierFactory(DjangoModelFactory):
    class Meta:
        model = Tier
        django_get_or_create = ["level"]

    level = Faker("pyint")
    name = LazyAttribute(lambda o: f"Tier {o.level}")
    description = Faker("paragraph", nb_sentences=3)


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service

    owner = Faker("user_name")
    name = Faker("slug")
    lifecycle = LazyFunction(
        lambda: choice([item.value for item in Lifecycle] + [None])
    )
    impact = LazyFunction(lambda: choice([item.value for item in Impact] + [None]))
    tier = SubFactory(TierFactory, level=LazyFunction(lambda: randint(1, 4)))
    repository = SubFactory(
        RepositoryFactory, owner=SelfAttribute("..owner"), name=SelfAttribute("..name")
    )
    slack_channel = LazyAttribute(lambda o: f"#{o.name}")
    docs_url = LazyAttribute(lambda o: f"https://example.com/#{o.name}")


class EnvironmentFactory(DjangoModelFactory):
    class Meta:
        model = Environment

    name = Faker("domain_word")
    service = SubFactory(ServiceFactory)
    health_check_url = Faker("uri")
    dashboard_url = Faker("uri")
    service_urls = [Faker("uri"), Faker("uri")]


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = Faker("user_name")
    email = Faker("email")


class ApiTokenFactory(DjangoModelFactory):
    class Meta:
        model = ApiToken

    purpose = "test"


class DependencyFactory(DjangoModelFactory):
    class Meta:
        model = Dependency

    name = Faker("name")
    type = choice([dtype.value for dtype in DependencyType])


class DependencyUsageFactory(DjangoModelFactory):
    class Meta:
        model = DependencyUsage

    def __init__(self, *args, **kwargs):
        self.version = f"{randint(0,10)}.{randint(0,10)}.{randint(0,10)}"
        unpacked_version = unpack_version(self.version)
        self.major_version = unpacked_version["major_version"]
        self.minor_version = unpacked_version["minor_version"]
        self.patch_version = unpacked_version["patch_version"]

    dependency = SubFactory(DependencyFactory)
    repo = SubFactory(RepositoryFactory)
    for_production = choice(["t", "f"])


class LinkFactory(DjangoModelFactory):
    class Meta:
        model = Link

    name = Faker("domain_word")
    url = Faker("uri")


class KindFactory(Factory):
    class Meta:
        model = Kind

    namespace = Faker("domain_word")
    category = Faker("domain_word")
    id = Faker("domain_word")
    title = Faker("sentence")
    description = Faker("paragraph")


class InfraNodeFactory(Factory):
    class Meta:
        model = InfraNode

    kind = Faker("domain_word")
    value = Faker("slug")


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    product_owner = Faker("user_name")
    project_owner = Faker("user_name")


class LibraryFactory(DjangoModelFactory):
    class Meta:
        model = Library

    owner = Faker("user_name")
    name = Faker("domain_word")
    lifecycle = LazyFunction(
        lambda: choice([item.value for item in Lifecycle] + [None])
    )
    impact = LazyFunction(lambda: choice([item.value for item in Impact] + [None]))
    slack_channel = Faker("domain_word")
    sonarqube_project = Faker("domain_word")
    repository = SubFactory(RepositoryFactory)


class ComponentBaseFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = Faker("domain_word")
    label = Faker("domain_word")
    type = "database"
    description = Faker("paragraph")
    kind = "component"
    owner = Faker("user_name")
    source = SubFactory(RepositoryFactory)
    service = None
    library = None
    group = SubFactory(GroupFactory)


class ComponentServiceFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = Faker("domain_word")
    label = Faker("domain_word")
    type = "service"
    description = Faker("paragraph")
    kind = Faker("domain_word")
    owner = Faker("user_name")
    source = SubFactory(RepositoryFactory)
    service = SubFactory(ServiceFactory)
    library = None
    group = SubFactory(GroupFactory)


class ComponentLibraryFactory(DjangoModelFactory):
    class Meta:
        model = Entity

    name = Faker("domain_word")
    label = Faker("domain_word")
    type = Faker("domain_word")
    description = Faker("paragraph")
    kind = Faker("domain_word")
    owner = Faker("user_name")
    source = SubFactory(RepositoryFactory)
    service = None
    library = SubFactory(LibraryFactory)
    group = SubFactory(GroupFactory)
