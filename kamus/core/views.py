from django.shortcuts import render

from django.views.generic import TemplateView


class Homepage(TemplateView):
    template_name = "kamus/homepage.html"


class Translate(TemplateView):
    template_name = "kamus/translation.html"

    def get_context_data(self, **kwargs):
        word = self.request.GET.get("word", None)

        if word is None:
            word = "error"

        context = {}
        context["word"] = word

        return context