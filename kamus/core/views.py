from urllib.parse import unquote

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from core.forms import SearchForm
from core.models import Language, WordWithTranslation, Import
from wiktionary.search import get_word_information


def get_languages_config(session, query_dict=None):
    result = {"from": session.get("from", "en"),
                "to": session.get("to", None)
            }

    # if there is a query_dict it has higher priouty

    if query_dict is not None:
        if "from" in query_dict:
            result["from"] = query_dict["from"]

        if "to" in query_dict:
            result["to"] = query_dict["to"]

    return result


class Homepage(TemplateView):
    template_name = "kamus/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = SearchForm(initial=get_languages_config(self.request.session, self.request.GET))

        return context


class Information(TemplateView):
    template_name = "kamus/information.html"


class Imports(TemplateView):
    template_name = "kamus/imports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        imports = []
        for language_dict in Import.objects.values("language__name").distinct():
            language_name = language_dict["language__name"]
            latest_import = Import.objects.filter(language__name=language_name).order_by("imported_on").first()

            imports.append({"language_name": language_name,
                            "file_created_on": latest_import.file_created_on,
                            "translated_words": latest_import.translated_words})

        context["imports"] = imports

        return context


class Translate(View):
    def _add_urls(self, senses, key):
        for sense in senses[key]:
            if "see" in sense:
                for sense_information in sense["see"]:
                    sense_information["url"] = self._link_to_word(sense_information["word"])

    def _link_to_word(self, word):
        url_parameters = self.request.GET.copy()
        url_parameters["word"] = word

        return reverse("translate") + "?" + url_parameters.urlencode()

    def get(self, request, *args, **kwargs):
        search_form = SearchForm(self.request.GET)

        is_valid = search_form.is_valid()

        if is_valid == False:
            messages.error(self.request, "Invalid parameters - please try again or get in touch")
            return redirect("homepage")

        if isinstance(search_form.cleaned_data["word"], WordWithTranslation):
            word = search_form.cleaned_data["word"].word
        else:
            # It didn't come from the autocomplete box
            word = search_form.cleaned_data["word"]

        from_language = search_form.cleaned_data["from"]
        to_language = search_form.cleaned_data["to"].code

        self.request.session["from"] = from_language
        self.request.session["to"] = to_language
        self.request.session.save()

        context = {}
        context["word"] = word
        context["translations"] = get_word_information(from_language, to_language, word)

        url_parameters_without_word = self.request.GET.copy()
        del url_parameters_without_word["word"]

        context["base_link_to_word"] = "?" + url_parameters_without_word.urlencode()
        context["search"] = SearchForm(initial={"from": from_language, "to": to_language})

        new_sources = []
        for source in context["translations"]["sources"]:
            source_decoded = unquote(source)

            new_sources.append({"url": source, "url_decoded": source_decoded})

        context["translations"]["sources"] = new_sources

        self._add_urls(context["translations"], "translated_senses")
        self._add_urls(context["translations"], "non_translated_senses")

        return render(self.request, "kamus/translation.html", context)
