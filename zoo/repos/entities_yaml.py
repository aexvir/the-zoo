from pathlib import Path
from typing import List, Union

import structlog
import yaml
from jsonschema import ValidationError
from jsonschema import validate as schema_validate
from yaml import FullLoader, load_all, safe_dump_all

from zoo.repos.models import Repository
from zoo.repos.utils import delete_none

log = structlog.get_logger()


SCHEMAS = {
    "base_component": str(Path(__file__).parents[1])
    + "/entities/yaml_definitions/component_base.yaml",
    "service": str(Path(__file__).parents[1])
    + "/entities/yaml_definitions/component_service.yaml",
    "library": str(Path(__file__).parents[1])
    + "/entities/yaml_definitions/component_library.yaml",
}


def get_schema(entity):
    if entity["kind"] == "component":
        if entity["spec"]["type"].lower() == "service":
            return SCHEMAS["service"]
        if entity["spec"]["type"].lower() == "library":
            return SCHEMAS["library"]
        return SCHEMAS["base_component"]
    log.info("repos.sync_entity_yaml.no_schema_defined")


def validate(_yaml: str) -> bool:
    try:
        all_entities = load_all(_yaml, FullLoader)
        for entity in all_entities:  # list(list)
            schema = get_schema(entity)
            if not schema:
                raise ValidationError
            with open(schema, "r") as schema_file:
                schema_dict = yaml.load(schema_file, FullLoader)
                schema_validate(entity, schema_dict)
    except ValidationError as err:
        log.info("repos.sync_entity_yml.validation_error", error=err)
        return False
    else:
        return True


def parse(_yaml: str) -> Union[List, None]:
    return load_all(_yaml, Loader=FullLoader)


def generate_component_base(component):
    component_base_document = {
        "apiVersion": "v1alpha1",
        "kind": component.kind,
        "metadata": {
            "name": component.name,
            "label": component.label,
            "owner": component.owner,
            "group": {
                "product_owner": component.group.product_owner,
                "project_owner": component.group.project_owner,
                "maintainers": component.group.maintainers,
            },
            "description": getattr(component, "description"),
            "tags": getattr(component, "tags", []),
            "links": [],
        },
        "spec": {"type": component.type},
    }

    for link in component.links.all():
        link_document = {"name": link.name, "url": link.url}
        if link.icon:
            link_document["icon"] = link.icon
        component_base_document["metadata"]["links"].append(link_document)

    return component_base_document


def generate_component_library(component_library, component_base_doc):
    component_base_doc["spec"] = {
        "type": "library",
        "lifecycle": component_library.library.lifecycle,
        "impact": component_library.library.impact,
        "analysis": [],
        "integrations": {
            "sonarqube_project": component_library.library.sonarqube_project,
            "slack_channel": component_library.library.slack_channel,
        },
    }

    return component_base_doc


def generate_component_service(component_service, component_base_doc):
    component_base_doc["spec"] = {
        "type": "service",
        "lifecycle": component_service.service.lifecycle,
        "impact": component_service.service.impact,
        "analysis": [],
        "environments": [],
        "integrations": {
            "sonarqube_project": getattr(
                component_service.service, "sonarqube_project"
            ),
            "slack_channel": getattr(component_service.service, "slack_channel"),
            "sentry_project": getattr(component_service.service, "sentry_project"),
            "pagerduty_service": getattr(
                component_service.service, "pagerduty_service"
            ),
        },
    }

    for environment in component_service.service.environments.all():
        environment_document = {
            "name": environment.name,
            "dashboard_url": getattr(environment, "dashboard_url"),
            "health_check_url": getattr(environment, "health_check_url"),
            "service_urls": getattr(environment, "service_urls"),
        }
        component_base_doc["spec"]["environments"].append(environment_document)

    return component_base_doc


def generate(repository: Repository) -> str:
    results = []
    for entity in repository.entities.all():
        if entity.kind != "component":
            return NotImplemented
        component_base_document = generate_component_base(entity)
        if entity.type == "library":
            component_library_document = generate_component_library(
                entity, component_base_document
            )
            results.append(delete_none(component_library_document))
        elif entity.type == "service":
            component_service_document = generate_component_service(
                entity, component_base_document
            )
            results.append(delete_none(component_service_document))
        else:
            results.append(delete_none(component_base_document))

    return safe_dump_all(results, sort_keys=False)
