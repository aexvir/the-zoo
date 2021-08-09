import re

import structlog
from django.db.models import Q
from django.http import Http404
from django.views import generic as generic_views
from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search

from ..auditing.models import Issue
from ..checklists.steps import STEPS
from . import models

log = structlog.get_logger()


class LibraryMixin:
    def get_object(self, queryset=None):
        """Return the library based on owner and name from the URL."""
        if queryset is None:
            queryset = self.get_queryset()

        try:
            return queryset.get(
                owner_slug=self.kwargs["owner_slug"], name_slug=self.kwargs["name_slug"]
            )

        except queryset.model.DoesNotExist:
            raise Http404("Library.DoesNotExist")


class LibraryDetail(LibraryMixin, generic_views.DetailView):
    model = models.Library

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("repository")
            .prefetch_related("checkmarks")
        )

    def get_checklists_context(self):
        if self.object.status != models.Status.BETA.value:
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

        context["checklist"] = self.get_checklists_context()

        return context


class LibraryList(generic_views.ListView):
    model = models.Library
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
                    | Q(status__icontains=queryterm)
                    | Q(impact__icontains=queryterm)
                )

            elif re.match(URL_QUERY_PATTERN, queryterm):
                queryset = queryset.filter(
                    Q(docs_url__icontains=queryterm)
                    | Q(library_url__icontains=queryterm)
                    | Q(health_check_url__icontains=queryterm)
                )

            else:
                try:
                    queryset = apply_search(
                        queryset, queryterm, models.LibrarySQLSchema
                    )
                except DjangoQLError:
                    log.exception("libraries.query_error", queryterm=queryterm)
                    return self.model.objects.none()

        return queryset.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["project_links"] = ["Support", "Repository", "Documentation"]
        return context
