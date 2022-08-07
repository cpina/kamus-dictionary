from dal import autocomplete
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms

from core.models import Language, WordWithTranslation
from wiktionary import FROM_LANGUAGES, ALL_LANGUAGES

class ModelSelect2Bootstrap5(autocomplete.ModelSelect2):
    @property
    def media(self):
        return forms.Media(
            js=(
                'admin/js/vendor/select2/select2.full.js',
                'autocomplete_light/autocomplete_light.js',
                'autocomplete_light/select2.js',
                'js/enable-select2-bootstrap5-theme.js', # added
            ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2.css',
                    'admin/css/autocomplete.css',
                    'https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css', # added
                ),
            })

class SearchForm(forms.Form):
    FORM_NAME = "search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["from"] = forms.CharField(label="From", widget=forms.Select(choices=FROM_LANGUAGES.items()))
        self.fields["to"] = forms.ModelChoiceField(label="To",
                                                   queryset=Language.objects.all().order_by("name"),
                                                   # widget=autocomplete.ModelSelect2("autocomplete-languages"),
                                                   to_field_name="code",
                                                   )
        # self.fields["word"] = forms.CharField(label="Word")
        self.fields["word"] = forms.ModelChoiceField(label="Word",
                                                     queryset=WordWithTranslation.objects.all().order_by("word"),
                                                     widget=ModelSelect2Bootstrap5("autocomplete-word-with-translation", attrs={"data-minimum-input-length": 3}),
                                                     to_field_name="word",
                                                     )

        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_action = "translate"

        self.helper.layout = Layout(
            Div(
                Div("from", css_class="col-3"),
                Div("to", css_class="col-3"),
                Div("word", css_class="col-6"),
                css_class="row"
            ),
            FormActions(
                Submit("translate", "Translate")
            )
        )