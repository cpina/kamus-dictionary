from django.urls import path

from . import views, autocompletes

urlpatterns = [
    path("translate/", views.Translate.as_view(), name="translate"),
    path("autocomplete/languages", autocompletes.LanguageAutocomplete.as_view(), name="autocomplete-languages"),
    path("", views.Homepage.as_view(), name="homepage"),
]
