import pytest

from zoo.repos.entities_yaml import generate, validate
from zoo.repos.models import Repository

pytestmark = pytest.mark.django_db


def test_generate_base_component(group_factory, component_base_factory, link_factory):
    group = group_factory(id=1, product_owner="john", project_owner="doe")
    component = component_base_factory(
        id=1,
        name="base",
        label="Base",
        type="database",
        description="This is my fancy component",
        kind="component",
        owner="platform",
        service=None,
        library=None,
        group=group,
        source__id=1,
        source__remote_id=1,
        source__owner="jasckson",
        source__name="thiwer",
        source__url="https://gitlab.com/thiwer/thiwer",
    )

    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component,
    )
    link_factory(
        id=2,
        name="Sentry",
        url="https://sentry.skypicker.com",
        entity=component,
    )

    expected = """
apiVersion: v1alpha1
kind: component
metadata:
  name: base
  label: Base
  owner: platform
  group:
    product_owner: john
    project_owner: doe
    maintainers: []
  description: This is my fancy component
  tags: []
  links:
  - name: Datadog
    url: https://dashboard.datadog.com
    icon: poop
  - name: Sentry
    url: https://sentry.skypicker.com
spec:
  type: database
"""
    repository = Repository.objects.get(pk=1)
    content = generate(repository)
    assert validate(content)
    assert expected.strip() == content.strip()


def test_generate_component_service(
    component_base_factory,
    service_factory,
    group_factory,
    link_factory,
    repository_factory,
    environment_factory,
):
    repository = repository_factory(
        id=22,
        remote_id=22,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )

    service = service_factory(
        owner="platform",
        name="my-service",
        lifecycle="production",
        impact="employees",
        repository=repository,
        slack_channel="#platform-software",
        docs_url="https://docs.com",
    )
    environment_factory(
        name="production",
        service=service,
        health_check_url="https://health.com",
        dashboard_url="https://dashboard.datadog.com",
        service_urls=["https://service.com"],
    )
    group = group_factory(id=1, product_owner="john", project_owner="doe")
    component_service = component_base_factory(
        id=1,
        name="service",
        label="Service",
        type="service",
        description="This is my fancy service",
        kind="component",
        owner="platform",
        service=service,
        library=None,
        group=group,
        source=repository,
    )
    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component_service,
    )
    expected = """
apiVersion: v1alpha1
kind: component
metadata:
  name: service
  label: Service
  owner: platform
  group:
    product_owner: john
    project_owner: doe
    maintainers: []
  description: This is my fancy service
  tags: []
  links:
  - name: Datadog
    url: https://dashboard.datadog.com
    icon: poop
spec:
  type: service
  lifecycle: production
  impact: employees
  analysis: []
  environments:
  - name: production
    dashboard_url: https://dashboard.datadog.com
    health_check_url: https://health.com
    service_urls:
    - https://service.com
  integrations:
    slack_channel: '#platform-software'
"""
    repository = Repository.objects.get(pk=22)
    content = generate(repository)
    assert validate(content)
    assert expected.strip() == content.strip()


def test_generate_component_library(
    component_base_factory,
    group_factory,
    link_factory,
    repository_factory,
    library_factory,
):
    repository = repository_factory(
        id=22,
        remote_id=22,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    group = group_factory(id=1, product_owner="john", project_owner="doe")
    lib = library_factory(
        id=1,
        owner="platform",
        name="fancy one",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack",
        sonarqube_project="sonar",
        repository=repository,
    )
    component_service = component_base_factory(
        id=1,
        name="library",
        label="Lib",
        type="library",
        description="This is my fancy library",
        kind="component",
        owner="platform",
        service=None,
        library=lib,
        group=group,
        source=repository,
    )
    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component_service,
    )

    expected = """
apiVersion: v1alpha1
kind: component
metadata:
  name: library
  label: Lib
  owner: platform
  group:
    product_owner: john
    project_owner: doe
    maintainers: []
  description: This is my fancy library
  tags: []
  links:
  - name: Datadog
    url: https://dashboard.datadog.com
    icon: poop
spec:
  type: library
  lifecycle: fixed
  impact: employees
  analysis: []
  integrations:
    sonarqube_project: sonar
    slack_channel: '#slack'
"""
    repository = Repository.objects.get(pk=22)
    content = generate(repository)
    assert validate(content)
    assert expected.strip() == content.strip()


def test_generate_multiple_components(
    component_base_factory,
    group_factory,
    link_factory,
    repository_factory,
    library_factory,
    service_factory,
    environment_factory,
):
    repository = repository_factory(
        id=22,
        remote_id=22,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    group = group_factory(id=1, product_owner="john", project_owner="doe")
    group_service = group_factory(id=2, product_owner="jason", project_owner="jasenson")
    lib = library_factory(
        id=1,
        owner="platform",
        name="fancy one",
        lifecycle="fixed",
        impact="employees",
        slack_channel="#slack",
        sonarqube_project="sonar",
        repository=repository,
    )
    service = service_factory(
        owner="platform",
        name="my-service",
        lifecycle="production",
        impact="employees",
        repository=repository,
        slack_channel="#platform-software",
        docs_url="https://docs.com",
    )
    environment_factory(
        name="production",
        service=service,
        health_check_url="https://health.com",
        dashboard_url="https://dashboard.datadog.com",
        service_urls=["https://service.com"],
    )
    component_lib = component_base_factory(
        id=1,
        name="library",
        label="Lib",
        type="library",
        description="This is my fancy library",
        kind="component",
        owner="platform",
        service=None,
        library=lib,
        group=group,
        source=repository,
    )
    component_service = component_base_factory(
        id=2,
        name="service",
        label="Service",
        type="service",
        description="This is my fancy service",
        kind="component",
        owner="platform",
        service=service,
        library=None,
        group=group_service,
        source=repository,
    )
    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component_lib,
    )
    link_factory(
        id=2,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component_service,
    )

    expected = """
apiVersion: v1alpha1
kind: component
metadata:
  name: library
  label: Lib
  owner: platform
  group:
    product_owner: john
    project_owner: doe
    maintainers: []
  description: This is my fancy library
  tags: []
  links:
  - name: Datadog
    url: https://dashboard.datadog.com
    icon: poop
spec:
  type: library
  lifecycle: fixed
  impact: employees
  analysis: []
  integrations:
    sonarqube_project: sonar
    slack_channel: '#slack'
---
apiVersion: v1alpha1
kind: component
metadata:
  name: service
  label: Service
  owner: platform
  group:
    product_owner: jason
    project_owner: jasenson
    maintainers: []
  description: This is my fancy service
  tags: []
  links:
  - name: Datadog
    url: https://dashboard.datadog.com
    icon: poop
spec:
  type: service
  lifecycle: production
  impact: employees
  analysis: []
  environments:
  - name: production
    dashboard_url: https://dashboard.datadog.com
    health_check_url: https://health.com
    service_urls:
    - https://service.com
  integrations:
    slack_channel: '#platform-software'
"""
    repository = Repository.objects.get(pk=22)
    content = generate(repository)
    assert validate(content)
    assert expected.strip() == content.strip()
