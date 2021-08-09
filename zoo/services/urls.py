"""services URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ServiceList.as_view(), name="service_list"),
    path(
        "<str:owner_slug>/<str:name_slug>",
        views.ServiceDetail.as_view(),
        name="service_detail",
    ),
    path(
        "<str:owner_slug>/<str:name_slug>/openapi",
        views.ServiceOpenApiDefinition.as_view(),
        name="service_openapi",
    ),
]
