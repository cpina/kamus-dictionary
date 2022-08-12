from django.urls import reverse
from django.views.generic import TemplateView

from core.forms import SearchForm
from core.models import Language, WordWithTranslation
from wiktionary.search import get_word_information

def get_languages_config(session):
    return {"from": session.get("from", "en"),
            "to": session.get("to", None)
            }

class Homepage(TemplateView):
    template_name = "kamus/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = SearchForm(initial=get_languages_config(self.request.session))
        # context["search"] = SearchForm()

        return context

class Information(TemplateView):
    template_name = "kamus/information.html"


class Translate(TemplateView):
    template_name = "kamus/translation.html"

    def _add_urls(self, senses):
        for sense in senses["senses"]:
            if "see" in sense:
                for sense_information in sense["see"]:
                    sense_information["url"] = self._link_to_word(sense_information["word"])

    def _link_to_word(self, word):
        url_parameters = self.request.GET.copy()
        url_parameters["word"] = word

        return reverse("translate") + "?" + url_parameters.urlencode()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)

        assert search_form.is_valid()

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

        context["word"] = word
        context["translations"] = get_word_information(from_language, to_language, word)

        url_parameters_without_word = self.request.GET.copy()
        del url_parameters_without_word["word"]

        context["base_link_to_word"] = "?" + url_parameters_without_word.urlencode()
        context["search"] = SearchForm(initial={"from": from_language, "to": to_language})

        self._add_urls(context["translations"])

        return context
