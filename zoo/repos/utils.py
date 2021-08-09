import hashlib
import importlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

import structlog
from django.core.serializers.json import DjangoJSONEncoder
from prance import ResolvingParser, ValidationError
from prance.util.formats import ParseError
from prance.util.url import ResolutionError
from yaml.composer import ComposerError
from yaml.scanner import ScannerError

from ..base import redis
from .exceptions import MissingFilesError, RepositoryNotFoundError

OPENAPI_SCAN_EXCLUDE = ["k8s", "test", ".gitlab", ".github"]
OPENAPI_INVALID_MARKER = "invalid"
OPENAPI_FINGERPRINT_MAX_AGE = 360 * 24 * 60 * 60  # ~1 year

log = structlog.get_logger()


def get_scm_module(provider):
    """Return correct zoo.repos modul for Git API according to provider value.

    e.g.: repository.provider = 'gitlab' => return zoo.repos.gitlab
    """
    current_module = ".".join(__name__.split(".")[:-1])
    return importlib.import_module(f".{provider}", current_module)


def download_repository(repository, fake_dir, sha=None):
    scm_module = get_scm_module(repository.provider)

    try:
        project = scm_module.get_project(repository.remote_id)
    except RepositoryNotFoundError as e:
        raise RepositoryNotFoundError(
            f"{repository} is private or doesn't exist."
        ) from e

    with tempfile.SpooledTemporaryFile(max_size=(10 * 1024 * 1024)) as archive:
        try:
            archive = scm_module.download_archive(project, archive, sha)
        except MissingFilesError as e:
            raise MissingFilesError(f"{repository} doesn't have any files.") from e

        try:
            archive.seek(0)
            with tarfile.open(fileobj=archive) as tar:
                inner_folder = tar.next().name
                tar.extractall(fake_dir)
        except tarfile.ReadError as e:
            raise MissingFilesError(f"{repository} doesn't have any files.") from e

    return Path(fake_dir) / inner_folder


def _parse_file(path, base=None):
    try:
        parser = ResolvingParser(str(path), strict=False)
        return parser.specification
    except (
        AssertionError,
        AttributeError,
        ComposerError,
        FileNotFoundError,
        ResolutionError,
        ScannerError,
        UnicodeDecodeError,
        ValidationError,
        ParseError,
        TypeError,
    ) as err:
        log.info(
            "repos.utils.openapi.invalid", path=str(path.relative_to(base)), error=err
        )


def openapi_definition(repository, request=None, repo_path=None):
    redis_conn = redis.get_connection(decode_responses=True)
    tmp_dir = None
    specs = []

    if repo_path is None:
        try:
            log.debug("repos.utils.openapi.download", repo=repository)
            tmp_dir = tempfile.mkdtemp()
            repo_path = download_repository(repository, tmp_dir)
            log.debug(
                "repos.utils.openapi.downloaded",
                repo=repository,
                repo_path=repo_path,
            )
        except (
            FileExistsError,
            PermissionError,
            MissingFilesError,
            RepositoryNotFoundError,
        ) as err:
            log.info("repos.utils.openapi.download_error", repo=repository, error=err)
            return []

    log.info("repos.utils.openapi.storage", repo_path=repo_path)

    for ext in ("json", "yml", "yaml"):
        for path in repo_path.glob(f"**/*.{ext}"):
            if any(directory in str(path) for directory in OPENAPI_SCAN_EXCLUDE):
                log.debug(
                    "repos.utils.openapi.exclude", repo=repository, file=path.name
                )
                continue

            fingerprint = f"{ext}-{hashlib.md5(path.read_text().encode()).hexdigest()}"
            log.debug("repos.utils.openapi.scan", repo=repository, file=path.name)

            if specification := redis_conn.get(fingerprint):
                log.debug(
                    "repos.utils.openapi.cache_hit",
                    repo=repository,
                    file=path.name,
                    fingerprint=fingerprint,
                )
                # We store all file fingerprints in redis, valid or invalid, to avoid
                # attempting to parse the same file over and over if it hasn't
                # changed at all
                if specification != OPENAPI_INVALID_MARKER:
                    log.debug(
                        "repos.utils.openapi.cache_invalid",
                        repo=repository,
                        fingerprint=fingerprint,
                    )
                    specs.append(json.loads(specification))

            else:
                parsed = _parse_file(path, repo_path)
                specs.append(parsed)
                redis_conn.set(
                    fingerprint,
                    json.dumps(parsed, cls=DjangoJSONEncoder)
                    if parsed
                    else OPENAPI_INVALID_MARKER,
                    ex=OPENAPI_FINGERPRINT_MAX_AGE,
                )
                log.debug(
                    "repos.utils.openapi.cache_store",
                    repo=repository,
                    fingerprint=fingerprint,
                )

    if tmp_dir is not None:
        shutil.rmtree(tmp_dir)

    log.info("repos.utils.openapi.done", repo=repository, specs=len(specs))
    return list(filter(None, specs))


def delete_none(_dict):
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value is None:
            _dict.pop(key)

    return _dict
