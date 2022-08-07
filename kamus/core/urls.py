from django.urls import path

from . import views, autocompletes

urlpatterns = [
    path("translate/", views.Translate.as_view(), name="translate"),
    path("autocomplete/languages/", autocompletes.LanguageAutocomplete.as_view(), name="autocomplete-languages"),
    path("autocomplete/words-with-translation/", autocompletes.WordWithTranslationAutocomplete.as_view(), name="autocomplete-word-with-translation"),
    path("information/", views.Information.as_view(), name="information"),
    path("", views.Homepage.as_view(), name="homepage"),
]
