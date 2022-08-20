from dal import autocomplete
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from core.models import Language, WordWithTranslation
from wiktionary import FROM_LANGUAGES

class ModelSelect2Bootstrap5(autocomplete.ModelSelect2):
    @property
    def media(self):
        # TODO: could make that it keeps the super().media() and adds
        # the specific ones for Kamus (instead of a full overwrite)
        return forms.Media(
            js=(
                'admin/js/vendor/select2/select2.full.js',
                'autocomplete_light/autocomplete_light.js',
                'autocomplete_light/select2.js',
                'js/setup-autocomplete.js', # added
                'js/swap-from-to.js', # added
            ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2.css',
                    'admin/css/autocomplete.css',
                    'https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css', # added
                ),
            })

class CaseSensitiveModelChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        # Copied from Python's implementation... with a small
        # change for allowing multiple values (for capitalisation)
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or "pk"
            if isinstance(value, self.queryset.model):
                value = getattr(value, key)
            db_values = self.queryset.filter(**{key: value})
            # There can be more than one... if there are words with
            # different capitalization. For example apple and Apple
            for db_value in db_values:
                if getattr(db_value, key) == value:
                    return db_value
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(
                self.error_messages["invalid_choice"],
                code="invalid_choice",
                params={"value": value},
            )
        return value


class SearchForm(forms.Form):
    FORM_NAME = "search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["from"] = forms.CharField(label="From", widget=forms.Select(choices=FROM_LANGUAGES.items()))
        self.fields["to"] = forms.ModelChoiceField(label="To",
                                                   queryset=Language.objects.all().order_by("name"),
                                                   to_field_name="code",
                                                   )

        self.fields["word"] = CaseSensitiveModelChoiceField(label=mark_safe("<abbr>W</abbr>ord"),
                                                     queryset=WordWithTranslation.objects.all().order_by("word"),
                                                     widget=ModelSelect2Bootstrap5("autocomplete-word-with-translation", forward=["from"],  attrs={"data-minimum-input-length": 2}),
                                                     to_field_name="word",
                                                     )

        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_action = "translate"

        self.helper.layout = Layout(
            Div(
                Div("from", css_class="col-5 col-lg-2"),
                Div(HTML('{% include "_arrow.html" %}'), css_class="col-2 col-lg-1 text-center"),
                Div("to", css_class="col-5 col-lg-2"),
                Div("word", css_class="col-7 col-lg-5"),
                Div(HTML('{% include "_submit_button.html" %}'), css_class="col-5 col-lg-2"),
                css_class="row"
            )
        )