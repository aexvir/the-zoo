from datetime import timedelta

from django.apps import AppConfig

from .celery import app as celery_app


class BaseConfig(AppConfig):
    name = "zoo.base"

    def ready(self):
        """Set the Celery schedule when Django signals it's ready, after apps load."""
        # pylint: disable=import-outside-toplevel

        from ..analytics import tasks as analytics_tasks
        from ..auditing import tasks as auditing_tasks
        from ..datacenters import tasks as datacenters_tasks
        from ..globalsearch import tasks as meilisearch_tasks
        from ..objectives import tasks as objective_tasks
        from ..repos import tasks as repos_tasks
        from ..services import tasks as service_tasks

        # pylint: enable=import-outside-toplevel

        celery_app.add_periodic_task(timedelta(hours=1), repos_tasks.sync_repos)
        celery_app.add_periodic_task(timedelta(hours=1), repos_tasks.schedule_pulls)
        celery_app.add_periodic_task(timedelta(days=1), repos_tasks.sync_entity_file)
        celery_app.add_periodic_task(
            timedelta(hours=1), service_tasks.schedule_sentry_sync
        )
        celery_app.add_periodic_task(
            timedelta(days=1), service_tasks.sync_sonarqube_projects
        )
        celery_app.add_periodic_task(
            timedelta(days=1), objective_tasks.schedule_objective_snapshots
        )
        celery_app.add_periodic_task(
            timedelta(days=1), auditing_tasks.take_issue_table_snapshots
        )
        celery_app.add_periodic_task(timedelta(days=1), auditing_tasks.cleanup_issues)
        celery_app.add_periodic_task(
            timedelta(days=1), analytics_tasks.take_dependency_snapshots
        )
        celery_app.add_periodic_task(
            timedelta(days=1), analytics_tasks.check_python_lib_licenses
        )
        celery_app.add_periodic_task(
            timedelta(days=1), datacenters_tasks.schedule_infra_mapping
        )
        celery_app.add_periodic_task(
            timedelta(hours=1), meilisearch_tasks.index_db_model_instances
        )
        celery_app.add_periodic_task(
            timedelta(minutes=30), meilisearch_tasks.index_openapi_definitions
        )
