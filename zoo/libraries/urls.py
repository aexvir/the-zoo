"""Libraries URL Configuration."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.LibraryList.as_view(), name="library_list"),
    path(
        "<str:owner_slug>/<str:name_slug>",
        views.LibraryDetail.as_view(),
        name="library_detail",
    ),
]
