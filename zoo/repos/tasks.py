import hashlib
import itertools
import tempfile
from collections import namedtuple
from typing import Dict, List

import structlog
from celery import shared_task
from django.conf import settings

from ..analytics.tasks import repo_analyzers
from ..auditing import runner
from ..auditing.check_discovery import CHECKS as AUDITING_CHECKS
from ..entities.builder import EntityBuilder
from ..entities.models import Entity, Link
from ..libraries.models import Library
from ..repos.models import Endpoint
from ..services.constants import EnviromentType
from ..services.models import Environment, Service
from .entities_yaml import parse, validate
from .exceptions import MissingFilesError, RepositoryNotFoundError
from .github import get_repositories as get_github_repositories
from .gitlab import get_project_enviroments
from .gitlab import get_repositories as get_gitlab_repositories
from .models import Repository, RepositoryEnvironment
from .utils import download_repository, get_scm_module, openapi_definition

log = structlog.get_logger()

# Necessary because openapi allows other keys like parameters inside the path object
# and it uses dynamic keys everywhere
HTTP_METHODS = (
    "get",
    "head",
    "post",
    "put",
    "delete",
    "connect",
    "options",
    "trace",
    "patch",
)


@shared_task
def sync_repos():

    i = 0
    for project in itertools.chain(
        get_github_repositories(), get_gitlab_repositories()
    ):
        if settings.SYNC_REPOS_SKIP_FORKS and project["is_fork"]:
            continue
        if settings.SYNC_REPOS_SKIP_PERSONAL and project["is_personal"]:
            continue
        i += 1
        log.info("sync_repos.fetch", repo_number=i, project=project)
        try:
            repo = Repository.objects.get(
                remote_id=project["id"], provider=project["provider"]
            )
        except Repository.DoesNotExist:
            try:
                repo = Repository.objects.get(
                    owner=project["owner"],
                    name=project["name"],
                    provider=project["provider"],
                )
                repo.remote_id = project["id"]
            except Repository.DoesNotExist:
                repo = Repository(remote_id=project["id"], provider=project["provider"])

        repo.owner = project["owner"]
        repo.name = project["name"]
        repo.url = project["url"]
        repo.full_clean()
        repo.save()

        if project["provider"] == "gitlab":
            log.info("sync_repos.calling.sync_enviroments_from_gitlab")
            sync_enviroments_from_gitlab(repo)

    log.info("sync_repos.total", repo_number=i)


@shared_task
def schedule_pulls():
    """Create one pull task per repo."""
    for repo in Repository.objects.all():
        # distribute pulls by delaying evenly across an hour
        pk_hash = hashlib.sha256(str(repo.pk).encode())
        delay_s = int(pk_hash.hexdigest(), 16) % (60 * 60)

        pull.apply_async(
            args=(repo.remote_id, repo.provider),
            countdown=delay_s,
            expires=delay_s + (60 * 60),
        )


@shared_task
def pull(reference, provider):
    """Run all repo tasks on one repo."""
    try:
        repository = Repository.objects.get(remote_id=int(reference), provider=provider)
    except ValueError:
        owner, name = reference.rsplit("/", 1)
        repository = Repository.objects.get(owner=owner, name=name, provider=provider)

    log.info("repos.pull", repo=repository)

    with tempfile.TemporaryDirectory() as repo_dir:
        try:
            repo_path = download_repository(repository, repo_dir)
        except (MissingFilesError, RepositoryNotFoundError) as err:
            log.info("repos.pull.git_error", repo=repository, error=err)
            return

        index_api(repository, repo_path)
        repo_analyzers.run_all(repository, repo_path)
        runner.run_checks_and_save_results(AUDITING_CHECKS, repository, repo_path)


def index_api(repository, repo_path):
    specifications = openapi_definition(repository, repo_path=repo_path)
    endpoints = []

    EpData = namedtuple("EpData", ["path", "method", "summary", "operation"])

    for spec in specifications:
        paths = spec.get("paths", [])

        for path in paths:
            for method in paths[path]:
                if method.lower() not in HTTP_METHODS:
                    continue

                log.debug("repos.index_api", repo=repository, path=path, method=method)
                endpoints.append(
                    EpData(
                        path=path,
                        method=method,
                        summary=paths[path][method].get("summary"),
                        operation=paths[path][method].get("operationId"),
                    )
                )

    for endpoint in endpoints:
        Endpoint.objects.update_or_create(
            defaults={
                "summary": endpoint.summary,
                "operation": endpoint.operation,
            },
            path=endpoint.path,
            method=endpoint.method,
            repository=repository,
        )
    log.info("repos.index_api.done", repo=repository, endpoints=len(endpoints))


@shared_task
def sync_entity_file():
    for project in itertools.chain(
        get_github_repositories(), get_gitlab_repositories()
    ):
        if settings.SYNC_REPOS_SKIP_FORKS and project["is_fork"]:
            continue
        update_project_from_entity_file.apply_async(args=project)


@shared_task
def update_project_from_entity_file(proj: Dict) -> None:
    try:
        content = get_entity_file_content(proj)
    except FileNotFoundError as err:
        log.info("repos.sync_entity_yml.file_not_found", error=err)
    else:
        if not validate(content):
            return
        update_or_create_components(parse(content), proj)


def update_or_create_components(data: List, proj: Dict) -> None:
    # Skip processing the entity file if the repository is not yet synced
    try:
        repository = Repository.objects.get(
            remote_id=int(proj["id"]), provider=proj["provider"]
        )
    except Repository.DoesNotExist:
        return

    def _do_cleanup():
        affected_entities = Entity.objects.filter(source=repository)
        Link.objects.filter(entity__in=affected_entities).delete()
        Service.objects.filter(repository=repository).delete()
        Library.objects.filter(repository=repository).delete()
        Entity.objects.filter(source=repository).delete()

    _do_cleanup()
    entity_builder = EntityBuilder()
    for component in data:
        entity_builder.sync_entities(component, repository)


def get_entity_file_content(proj: Dict) -> str:
    provider = get_scm_module(proj["provider"])
    return provider.get_file_content(proj["id"], "entities.yaml")


def sync_enviroments_from_gitlab(repo: Repository):
    gl_envs = get_project_enviroments(repo.remote_id)

    if not gl_envs:
        log.info("sync_enviroments_from_gitlab.no_envs")
        return

    envs = []
    i = 0
    log.info("sync_enviroments_from_gitlab.start")
    for gl_env in gl_envs:
        if gl_env.state != "available":
            continue
        env, _ = RepositoryEnvironment.objects.get_or_create(
            repository_id=repo.id, name=gl_env.name
        )
        env.external_url = gl_env.external_url
        env.save()
        envs.append(env)
        i += 1

    RepositoryEnvironment.objects.filter(repository_id=repo.id).exclude(
        id__in=[env.id for env in envs]
    ).delete()

    # update gitlab envs on every service
    services = Service.objects.filter(repository_id=repo.id)
    for service in services:
        Environment.objects.filter(
            service_id=service.id, type=EnviromentType.GITLAB.value
        ).exclude(name__in=[env.name for env in envs]).delete()
        for env in envs:
            service_env, _ = Environment.objects.get_or_create(
                service_id=service.id,
                name=env.name,
                type=EnviromentType.GITLAB.value,
            )
            service_env.dashboard_url = env.external_url
            service_env.save()

    log.info("sync_enviroments_from_gitlab.total.synced", envs_synced=i)
