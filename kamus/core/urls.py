from django.urls import path

from . import views, autocompletes

urlpatterns = [
    path("translate/", views.Translate.as_view(), name="translate"),
    path("autocomplete/languages/", autocompletes.LanguageAutocomplete.as_view(), name="autocomplete-languages"),
    path("autocomplete/words-with-translation/", autocompletes.WordWithTranslationAutocomplete.as_view(), name="autocomplete-word-with-translation"),
    path("about/", views.About.as_view(), name="about"),
    path("shortcuts/", views.Shortcuts.as_view(), name="shortcuts"),
    path("imports/", views.Imports.as_view(), name="imports"),

    path("", views.Homepage.as_view(), name="homepage"),
]
