from zoo.entities.models import Entity, Group, Link
from zoo.libraries.models import Library
from zoo.services.models import Environment, Service


# TODO: refactor to registry pattern(or any better one)
class EntityBuilder:
    def sync_entities(self, data, repository):
        if data["kind"] != "component":
            return NotImplemented
        if data["spec"]["type"] == "service":
            self._build_service(data, repository)
        elif data["spec"]["type"] == "library":
            self._build_library(data, repository)
        else:
            self._build_base_component(data, repository)

    @staticmethod
    def _build_base_component(data, repository):
        group = Group.objects.create(
            product_owner=data["metadata"]["group"]["product_owner"],
            project_owner=data["metadata"]["group"]["project_owner"],
            maintainers=data["metadata"]["group"]["maintainers"],
        )

        obj = Entity.objects.create(
            name=data["metadata"]["name"],
            label=data["metadata"]["label"],
            kind=data["kind"],
            type=data["spec"]["type"],
            source=repository,
            owner=data["metadata"]["owner"],
            description=data["metadata"]["description"],
            tags=data["metadata"]["tags"],
            group=group,
        )

        for link in data["metadata"]["links"]:
            Link.objects.create(
                url=link["url"],
                entity=obj,
                name=link["name"],
                icon=getattr(link, "icon", None),
            )

        return obj

    def _build_service(self, data, repository):
        base_component = self._build_base_component(data, repository)

        service = Service.objects.create(
            name=base_component.label,
            owner=base_component.owner,
            repository=repository,
            lifecycle=data["spec"]["lifecycle"],
            impact=data["spec"]["impact"],
            sentry_project=data["spec"].get("integrations", {}).get("sentry_project"),
            sonarqube_project=data["spec"]
            .get("integrations", {})
            .get("sonarqube_project"),
            slack_channel=data["spec"].get("integrations", {}).get("slack_channel"),
            pagerduty_service=data["spec"]
            .get("integrations", {})
            .get("pagerduty_service"),
            description=data["metadata"]["description"],
        )

        for env in data["spec"]["environments"]:
            Environment.objects.create(
                service=service,
                name=env["name"],
                dashboard_url=env["dashboard_url"],
                health_check_url=env["health_check_url"],
                service_urls=env["service_urls"],
            )

        base_component.service = service
        base_component.save()

    def _build_library(self, data, repository):
        base_component = self._build_base_component(data, repository)

        library = Library.objects.create(
            name=base_component.label,
            owner=base_component.owner,
            repository=repository,
            lifecycle=data["spec"]["lifecycle"],
            impact=data["spec"]["impact"],
            sonarqube_project=data["spec"]
            .get("integrations", {})
            .get("sonarqube_project"),
            slack_channel=data["spec"].get("integrations", {}).get("slack_channel"),
        )

        base_component.library = library
        base_component.save()
