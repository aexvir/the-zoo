import attr
from django import forms
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, JsonResponse
from django.views.generic import ListView, TemplateView

from ..services import models as service_models
from . import models
from .steps import STEPS


def get_service_steps(service):
    checklist = [
        (tag, steps)
        for tag, steps in STEPS.items()
        if tag in ["general", *service.tags]
    ]
    return sorted(checklist, key=lambda x: x[0])


class GlobalChecklistsView(ListView):
    model = service_models.Service
    template_name = "checklists/global_checklists.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(lifecycle=service_models.Lifecycle.BETA.value)
            .prefetch_related("checkmarks")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_list"] = [
            {
                "name": service.name,
                "owner_slug": service.owner_slug,
                "name_slug": service.name_slug,
                "completed_checklist_steps": service.checkmarks.count,
                "total_checklist_steps": sum(
                    len(steps) for tag, steps in get_service_steps(service)
                ),
            }
            for service in self.get_queryset()
        ]

        return context


class ServiceChecklistView(TemplateView):
    template_name = "checklists/service_checklist.html"

    def get_context_data(self, **kwargs):
        service_owner_slug = kwargs.get("service_owner_slug")
        service_name_slug = kwargs.get("service_name_slug")

        if not service_owner_slug or not service_name_slug:
            raise SuspiciousOperation

        context = super().get_context_data(**kwargs)
        try:
            service = service_models.Service.objects.get(
                owner_slug=service_owner_slug,
                name_slug=service_name_slug,
                lifecycle=service_models.Lifecycle.BETA.value,
            )
        except service_models.Service.DoesNotExist:
            raise Http404

        context["service"] = service
        context["steps"] = [
            {
                "tag": tag,
                "name": next(iter(steps.values())).category_name,
                "steps": [
                    attr.evolve(
                        step,
                        is_checked=service.checkmarks.filter(step_key=key).exists(),
                    )
                    for key, step in steps.items()
                ],
            }
            for tag, steps in get_service_steps(service)
        ]

        return context


class UpdateServiceCheklistForm(forms.Form):
    checked = forms.BooleanField(required=False)


def update_service_checklist(request, checklist_item_key, *args, **kwargs):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    request_data_form = UpdateServiceCheklistForm(request.POST)

    if not request_data_form.is_valid():
        return JsonResponse(
            {"error": request_data_form.errors.as_json(escape_html=True)}, status=400
        )

    step_checked = request_data_form["checked"].value()
    owner_slug = kwargs.get("service_owner_slug")
    name_slug = kwargs.get("service_name_slug")

    if step_checked:
        try:
            service = service_models.Service.objects.get(
                owner_slug=owner_slug, name_slug=name_slug
            )
            checkmark = models.Checkmark(service=service, step_key=checklist_item_key)
            checkmark.full_clean()
            checkmark.save()
            return JsonResponse({}, status=200)

        except service_models.Service.DoesNotExist:
            return JsonResponse(
                {"error": "The service specified does not exist"}, status=404
            )
    else:
        try:
            models.Checkmark.objects.get(
                step_key=checklist_item_key,
                service__owner_slug=owner_slug,
                service__name_slug=name_slug,
            ).delete()
            return JsonResponse({}, status=200)

        except models.Checkmark.DoesNotExist:
            return JsonResponse(
                {"error": "The step tried to check does not exist"}, status=404
            )
