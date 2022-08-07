from dal import autocomplete
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms

from core.models import Language
from wiktionary import FROM_LANGUAGES, ALL_LANGUAGES


class SearchForm(forms.Form):
    FORM_NAME = "search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["from"] = forms.CharField(label="From", widget=forms.Select(choices=FROM_LANGUAGES.items()))
        self.fields["to"] = forms.ModelChoiceField(label="To",
                                                   queryset=Language.objects.all().order_by(("name")),
                                                   # widget=autocomplete.ModelSelect2("autocomplete-languages"),
                                                   to_field_name="code",
                                                   )
        self.fields["word"] = forms.CharField(label="Word")

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