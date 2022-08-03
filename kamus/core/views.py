from django.views.generic import TemplateView

from core.forms import SearchForm
from wikidictionary.search import search

def get_languages_config(session):
    return {"from": session.get("from", "en"),
            "to": session.get("to", "ca")
            }

class Homepage(TemplateView):
    template_name = "kamus/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = SearchForm(initial=get_languages_config(self.request.session))

        return context


class Translate(TemplateView):
    template_name = "kamus/translation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = SearchForm(self.request.GET)

        assert search_form.is_valid()

        word = search_form.cleaned_data["word"]
        source = search_form.cleaned_data["from"]
        to = search_form.cleaned_data["to"]

        self.request.session['source'] = source
        self.request.session['to'] = to

        context["word"] = word
        context["translations"] = search(source, to, word)

        context["search"] = SearchForm(initial=get_languages_config(self.request.session))

        return context