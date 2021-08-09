import pytest

import zoo.repos.tasks as uut
from zoo.entities.models import Entity
from zoo.libraries.models import Library
from zoo.services.models import Service

pytestmark = pytest.mark.django_db


def test_create_base_component(mocker, repository_factory):
    repository = repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    repository_dict = {"id": repository.remote_id, "provider": repository.provider}

    base_component = """
apiVersion: v1alpha1
kind: component
metadata:
    name: base-component
    label: Base Component
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

    mocker.patch("zoo.repos.tasks.get_entity_file_content", return_value=base_component)
    uut.update_project_from_entity_file(proj=repository_dict)
    component_entity = Entity.objects.first()
    assert Entity.objects.all().count() == 1
    assert component_entity.kind == "component"
    assert component_entity.name == "base-component"
    assert component_entity.label == "Base Component"
    assert component_entity.owner == "platform"
    assert component_entity.service is None
    assert component_entity.library is None
    assert component_entity.type == "database"
    assert component_entity.links.all().count() == 2
    assert component_entity.group is not None


def test_create_base_component_and_service(mocker, repository_factory):
    repository = repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.co  m/john_doe1/test_proj1",
        provider="github",
    )
    repository_dict = {"id": repository.remote_id, "provider": repository.provider}

    service_component = """
apiVersion: v1alpha1
kind: component
metadata:
    name: base-service
    label: Base Service
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
    type: service
    environments:
    - name: production
      dashboard_url: https://dashboard.datadog.com
      health_check_url: https://dashboard.datadog.com
      service_urls:
        - https://service.prod.com
    - name: sandbox
      dashboard_url: https://dashboard.datadog.sandbox.com
      health_check_url: https://dashboard.datadog.sandbox.com
      service_urls:
        - https://service.sandbox.com
    impact: profit
    integrations:
      pagerduty_service: pagerduty_service1234
      sentry_project: sentry project 15234
    lifecycle: production
"""

    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content", return_value=service_component
    )
    uut.update_project_from_entity_file(proj=repository_dict)
    component_entity = Entity.objects.first()
    assert Entity.objects.all().count() == 1
    assert Service.objects.all().count() == 1
    assert component_entity.kind == "component"
    assert component_entity.name == "base-service"
    assert component_entity.label == "Base Service"
    assert component_entity.owner == "platform"
    assert component_entity.library is None
    assert component_entity.type == "service"
    assert component_entity.links.all().count() == 2
    assert component_entity.group is not None
    assert component_entity.service is not None
    assert component_entity.service.environments.all().count() == 2


def test_create_base_component_and_library(mocker, repository_factory):
    repository = repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.co  m/john_doe1/test_proj1",
        provider="github",
    )
    repository_dict = {"id": repository.remote_id, "provider": repository.provider}

    library_component = """
apiVersion: v1alpha1
kind: component
metadata:
    name: base_lib
    label: Base Lib
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
    type: library
    impact: profit
    integrations:
      sonarqube_project: sonarqube
    lifecycle: production
"""

    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content", return_value=library_component
    )
    uut.update_project_from_entity_file(proj=repository_dict)
    component_entity = Entity.objects.first()
    assert Entity.objects.all().count() == 1
    assert Library.objects.all().count() == 1
    assert component_entity.kind == "component"
    assert component_entity.name == "base_lib"
    assert component_entity.label == "Base Lib"
    assert component_entity.owner == "platform"
    assert component_entity.type == "library"
    assert component_entity.links.all().count() == 2
    assert component_entity.group is not None
    assert component_entity.service is None
    assert component_entity.library is not None


def test_create_multiple_components_one_service(mocker, repository_factory):
    multiple_components = """
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
---
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
    description: This is my fancy component
    tags: []
    links:
    - name: Datadog
      url: https://service.dashboard.datadog.com
      icon: poop
    - name: Sentry
      url: https://service..skypicker.com
spec:
    type: service
    environments:
    - name: production
      dashboard_url: https://dashboard.datadog.com
      health_check_url: https://dashboard.datadog.com
      service_urls:
        - https://service.prod.com
    - name: sandbox
      dashboard_url: https://dashboard.datadog.sandbox.com
      health_check_url: https://dashboard.datadog.sandbox.com
      service_urls:
        - https://service.sandbox.com
    impact: profit
    integrations:
        pagerduty_service: pagerduty_service1234
        sentry_project: sentry project 15234
    lifecycle: production
"""

    repository = repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    repository_dict = {"id": repository.remote_id, "provider": repository.provider}
    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content", return_value=multiple_components
    )
    uut.update_project_from_entity_file(proj=repository_dict)
    assert Entity.objects.all().count() == 2
    assert Service.objects.all().count() == 1


def test_create_multiple_components_multiple_services(mocker, repository_factory):
    multiple_components = """
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
---
apiVersion: v1alpha1
kind: component
metadata:
    name: service
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
      url: https://service.dashboard.datadog.com
      icon: poop
    - name: Sentry
      url: https://service..skypicker.com
spec:
    type: service
    environments:
    - name: production
      dashboard_url: https://dashboard.datadog.com
      health_check_url: https://dashboard.datadog.com
      service_urls:
        - https://service.prod.com
    - name: sandbox
      dashboard_url: https://dashboard.datadog.sandbox.com
      health_check_url: https://dashboard.datadog.sandbox.com
      service_urls:
        - https://service.sandbox.com
    impact: profit
    integrations:
        pagerduty_service: pagerduty_service1234
        sentry_project: sentry project 15234
    lifecycle: production
---
apiVersion: v1alpha1
kind: component
metadata:
    name: service-the-second
    label: Service The Second
    owner: platform software
    group:
      product_owner: john the first
      project_owner: doe the second
      maintainers: [john, doe]
    description: This is my fancy second service
    tags: [fancy, service, python]
    links:
    - name: Datadog
      url: https://service-second.dashboard.datadog.com
      icon: poop
    - name: Sentry
      url: https://service.second.skypicker.com
spec:
    type: service
    environments:
    - name: production
      dashboard_url: https://dashboard.second.datadog.com
      health_check_url: https://dashboard.second.datadog.com
      service_urls:
        - https://service.second.prod.com
    - name: sandbox
      dashboard_url: https://dashboard.datadog.second.sandbox.com
      health_check_url: https://dashboard.datadog.second.sandbox.com
      service_urls:
        - https://service.second.sandbox.com
    impact: profit
    integrations:
        pagerduty_service: pagerduty_service1234_second
        sentry_project: sentry project 15234 second
    lifecycle: deprecated
"""

    repository = repository_factory(
        id=1,
        remote_id=11,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    repository_dict = {"id": repository.remote_id, "provider": repository.provider}
    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content", return_value=multiple_components
    )
    uut.update_project_from_entity_file(proj=repository_dict)
    assert Entity.objects.all().count() == 3
    assert Service.objects.all().count() == 2


def test_update_base_component(
    mocker, repository_factory, component_base_factory, link_factory, group_factory
):
    group = group_factory(id=1, product_owner="Old John", project_owner="Old Doe")
    group.save()
    component = component_base_factory(
        id=1,
        name="old-component",
        label="Old Component",
        type="database",
        description="Old Component Description",
        kind="component",
        owner="platform",
        group=group,
        service=None,
        library=None,
        source__id=1,
        source__remote_id=1,
        source__owner="jasckson",
        source__name="thiwer",
        source__url="https://gitlab.com/thiwer/thiwer",
        source__provider="gitlab",
    )
    component.save()

    link_factory(
        id=1,
        name="Datadog",
        url="https://dashboard.datadog.com",
        icon="poop",
        entity=component,
    )

    base_component = """
apiVersion: v1alpha1
kind: component
metadata:
    name: new-component
    label: New Component
    owner: platform
    group:
      product_owner: New John
      project_owner: New Doe
      maintainers: []
    description: New Component Description
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

    repository_dict = {
        "id": component.source.remote_id,
        "provider": component.source.provider,
    }
    mocker.patch("zoo.repos.tasks.get_entity_file_content", return_value=base_component)

    component_entity = Entity.objects.first()
    assert Entity.objects.all().count() == 1
    assert component_entity.kind == "component"
    assert component_entity.name == "old-component"
    assert component_entity.label == "Old Component"
    assert component_entity.owner == "platform"
    assert component_entity.type == "database"
    assert component_entity.links.all().count() == 1
    assert component_entity.group is not None
    assert component_entity.group.product_owner == "Old John"
    assert component_entity.group.project_owner == "Old Doe"
    assert component_entity.service is None
    assert component_entity.library is None

    uut.update_project_from_entity_file(proj=repository_dict)

    component_entity = Entity.objects.first()
    assert Entity.objects.all().count() == 1
    assert component_entity.kind == "component"
    assert component_entity.name == "new-component"
    assert component_entity.label == "New Component"
    assert component_entity.owner == "platform"
    assert component_entity.type == "database"
    assert component_entity.links.all().count() == 2
    assert component_entity.group is not None
    assert component_entity.group.product_owner == "New John"
    assert component_entity.group.project_owner == "New Doe"
    assert component_entity.service is None
    assert component_entity.library is None


def test_update_service_library(
    mocker,
    component_base_factory,
    service_factory,
    repository_factory,
    library_factory,
    group_factory,
):
    repository = repository_factory(
        id=12345,
        remote_id=12463,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    group_1 = group_factory(id=1, product_owner="Old John", project_owner="Old Doe")
    group_1.save()

    group_2 = group_factory(id=2, product_owner="Old John", project_owner="Old Doe")
    group_2.save()
    service = service_factory(repository=repository)
    library = library_factory(repository=repository)
    component_base_factory(
        source=repository, service=service, group=group_1, type="service"
    )
    component_base_factory(
        source=repository, library=library, group=group_2, type="library"
    )

    component_service_and_library = """
apiVersion: v1alpha1
kind: component
metadata:
    name: new-service
    label: New Service
    owner: platform
    group:
      product_owner: New John
      project_owner: New Doe
      maintainers: []
    description: New Description
    tags: []
    links:
    - name: Datadog
      url: https://service.dashboard.datadog.com
      icon: poop
    - name: Sentry
      url: https://service..skypicker.com
spec:
    type: service
    environments:
    - name: production
      dashboard_url: https://dashboard.datadog.com
      health_check_url: https://dashboard.datadog.com
      service_urls:
        - https://service.prod.com
    - name: sandbox
      dashboard_url: https://dashboard.datadog.sandbox.com
      health_check_url: https://dashboard.datadog.sandbox.com
      service_urls:
        - https://service.sandbox.com
    impact: profit
    integrations:
        pagerduty_service: pagerduty_service1234
        sentry_project: sentry project 15234
    lifecycle: production
---
apiVersion: v1alpha1
kind: component
metadata:
    name: new-lib
    label: New Lib
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
    type: library
    impact: profit
    integrations:
      sonarqube_project: sonarqube
    lifecycle: production
"""

    repository_dict = {
        "id": repository.remote_id,
        "provider": repository.provider,
    }
    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content",
        return_value=component_service_and_library,
    )

    assert Entity.objects.all().count() == 2
    assert Service.objects.all().count() == 1
    assert Library.objects.all().count() == 1

    uut.update_project_from_entity_file(proj=repository_dict)

    assert Entity.objects.all().count() == 2
    assert Service.objects.all().count() == 1
    assert Library.objects.all().count() == 1

    service_entity = Entity.objects.filter(service__isnull=False).first()
    library_entity = Entity.objects.filter(library__isnull=False).first()

    assert service_entity.kind == "component"
    assert service_entity.type == "service"
    assert service_entity.name == "new-service"
    assert service_entity.label == "New Service"
    assert service_entity.owner == "platform"
    assert service_entity.links.all().count() == 2
    assert service_entity.service.environments.all().count() == 2

    assert library_entity.kind == "component"
    assert library_entity.type == "library"
    assert library_entity.name == "new-lib"
    assert library_entity.label == "New Lib"
    assert library_entity.owner == "platform"
    assert library_entity.links.all().count() == 2


def test_delete_entities(
    mocker,
    component_base_factory,
    service_factory,
    repository_factory,
    library_factory,
    group_factory,
):
    repository = repository_factory(
        id=22,
        remote_id=22,
        name="test_proj1",
        owner="john_doe1",
        url="https://github.com/john_doe1/test_proj1",
        provider="github",
    )
    group_1 = group_factory(id=1, product_owner="Old John", project_owner="Old Doe")
    group_1.save()

    group_2 = group_factory(id=2, product_owner="Old John", project_owner="Old Doe")
    group_2.save()

    service = service_factory(repository=repository)
    library = library_factory(repository=repository)
    component_base_factory(source=repository, service=service, group=group_1)
    component_base_factory(source=repository, library=library, group=group_2)

    component_service_and_library = ""

    repository_dict = {
        "id": repository.remote_id,
        "provider": repository.provider,
    }
    mocker.patch(
        "zoo.repos.tasks.get_entity_file_content",
        return_value=component_service_and_library,
    )

    assert Entity.objects.all().count() == 2
    assert Service.objects.all().count() == 1
    assert Library.objects.all().count() == 1

    uut.update_project_from_entity_file(proj=repository_dict)

    assert Entity.objects.all().count() == 0
    assert Service.objects.all().count() == 0
    assert Library.objects.all().count() == 0
