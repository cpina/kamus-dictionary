import json

from dal import autocomplete

from .models import Language, WordWithTranslation


class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        qs = qs.order_by("name")

        return qs

class WordWithTranslationAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_value(self, word_with_translation):
        return word_with_translation.word

    def get_result_label(self, word_with_translation):
        return word_with_translation.word

    def get_queryset(self):
        forwarded_values = self.request.GET["forward"]
        forwarded_values = json.loads(forwarded_values)
        from_language = Language.objects.get(code=forwarded_values["from"])

        qs = WordWithTranslation.objects.all()

        qs = qs.filter(language=from_language)

        if self.q:
            qs = qs.filter(word__istartswith=self.q)

        qs = qs.order_by("word")

        return qs