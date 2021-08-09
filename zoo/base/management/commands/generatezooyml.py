from django.core.management.base import BaseCommand

from zoo.repos import entities_yaml, github, gitlab
from zoo.services.models import Service


class Command(BaseCommand):
    help = "generate .entities.yml file for all entities in the database that do not have it"

    ENTITY_YML = ".entities.yml"
    ENTITY_COMMIT_MSG = "feat(zoo): generate .entities.yml file"

    def handle(self, *args, **options):
        for service in Service.objects.all():
            remote_id, provider = (
                service.repository.remote_id,
                self.get_provider(service.repository.provider),
            )
            if not provider:
                continue

            if self.file_exists(remote_id, Command.ENTITY_YML, provider):
                continue

            yml = entities_yaml.generate(service)
            actions = [
                {"action": "create", "content": yml, "file_path": Command.ENTITY_YML}
            ]
            branch = "master"

            provider.create_remote_commit(
                remote_id, Command.ENTITY_COMMIT_MSG, actions, branch, provider
            )

    def get_provider(self, provider):
        providers = {
            "github": github,
            "gitlab": gitlab,
        }

        return providers[provider]

    def file_exists(self, remote_id, path, provider, ref="master"):
        try:
            content = provider.get_file_content(remote_id, path, ref)
            return bool(content)
        except FileNotFoundError:
            return False
