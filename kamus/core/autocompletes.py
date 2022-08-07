from dal import autocomplete

from .models import Language, WordWithTranslation


class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Language.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class WordWithTranslationAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_value(self, word_with_translation):
        return word_with_translation.word

    def get_result_label(self, word_with_translation):
        return word_with_translation.word

    def get_queryset(self):
        qs = WordWithTranslation.objects.all()

        if self.q:
            qs = qs.filter(word__istartswith=self.q)

        return qs