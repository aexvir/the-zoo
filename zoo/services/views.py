import json
import re

import requests
import structlog
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.views import generic as generic_views
from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search

from ..auditing.models import Issue
from ..checklists.steps import STEPS
from ..repos.utils import openapi_definition
from . import models
from .models import EnviromentType, Service

log = structlog.get_logger()


class ServiceMixin:
    def get_object(self, queryset=None):
        """Return the service based on owner and name from the URL."""
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.get(
                owner_slug=self.kwargs["owner_slug"], name_slug=self.kwargs["name_slug"]
            )

        except queryset.model.DoesNotExist:
            raise Http404("Service.DoesNotExist")


class ServiceDetail(ServiceMixin, generic_views.DetailView):
    model = models.Service

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("repository")
            .prefetch_related("checkmarks")
        )

    def get_sentry_context(self):
        sentry_issues = self.object.sentry_issues.prefetch_related("stats").all()

        if not sentry_issues.exists():
            return None

        all_sentry_issues = sentry_issues.order_by("-last_seen")
        issue_histogram = all_sentry_issues.generate_sentry_histogram()
        weekly_stats = all_sentry_issues.calculate_weekly_sentry_stats()

        return {
            "weekly_events": weekly_stats["events"],
            "weekly_users": weekly_stats["users"],
            "issues": [
                {
                    "id": issue.id,
                    "instance": issue,
                    "histogram": issue_histogram[issue.id],
                }
                for issue in sentry_issues.problematic()
            ],
        }

    def get_checklists_context(self):
        if self.object.lifecycle != models.Lifecycle.BETA.value:
            return None

        return {
            "total": sum(
                len(steps) for tag, steps in STEPS.items() if tag in self.object.tags
            ),
            "completed": self.object.checkmarks.count(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.repository:
            context["issue_count"] = self.object.repository.issues.filter(
                status=Issue.Status.NEW.value
            ).count()

        context["environment_type_gitlab"] = str(EnviromentType.GITLAB)
        context["sentry_data"] = self.get_sentry_context()
        context["checklist"] = self.get_checklists_context()
        context["environment"] = self.object.get_environment(
            self.request.GET.get("environment")
        )
        context["environments_dict"] = list(self.object.environments_dict.values())[:10]

        return context


class ServiceList(generic_views.ListView):
    model = models.Service
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.select_related("repository")
        queryterm = self.request.GET.get("q", None)

        if queryterm:
            SIMPLE_QUERY_PATTERN = r"^[\w-]+$"
            URL_QUERY_PATTERN = r"^https?[:][/][/]\S+$"

            if re.match(SIMPLE_QUERY_PATTERN, queryterm):
                queryset = queryset.filter(
                    Q(name__icontains=queryterm)
                    | Q(owner__icontains=queryterm)
                    | Q(lifecycle__icontains=queryterm)
                    | Q(impact__icontains=queryterm)
                )

            elif re.match(URL_QUERY_PATTERN, queryterm):
                queryset = queryset.filter(
                    Q(docs_url__icontains=queryterm)
                    | Q(environment__health_check_url__icontains=queryterm)
                    | Q(environment__service_urls__icontains=queryterm)
                )

            else:
                try:
                    queryset = apply_search(queryset, queryterm, models.ServiceQLSchema)
                except DjangoQLError:
                    log.exception("services.query_error", queryterm=queryterm)
                    return self.model.objects.none()

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project_links"] = [
            "Support",
            "Repository",
            "Dashboard",
            "Alerts",
            "Documentation",
        ]
        return context


class ServiceOpenApiDefinition(ServiceMixin, generic_views.View):
    def dispatch(self, request, *args, **kwargs):
        if request.method != "GET":
            return

        service = self.get_object(queryset=Service.objects.all())

        specs = []
        if service:
            environments = service.environments_dict
            urls = [
                env.open_api_url for env in environments.values() if env.open_api_url
            ]
            for url in urls:
                spec = requests.get(url)
                specs.append(json.loads(spec.text))
        if specs:
            return JsonResponse(specs, safe=False)

        return JsonResponse(openapi_definition(service.repository, request), safe=False)
