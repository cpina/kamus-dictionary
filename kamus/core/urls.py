from django.urls import path

from . import views

urlpatterns = [
    path("translate/", views.Translate.as_view(), name="translate"),
    path("", views.Homepage.as_view(), name="homepage"),
]
