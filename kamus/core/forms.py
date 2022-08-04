from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms

from wiktionary import LANGUAGES


class SearchForm(forms.Form):
    FORM_NAME = "search"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["from"] = forms.CharField(label="From", widget=forms.Select(choices=LANGUAGES.items()))
        self.fields["to"] = forms.CharField(label="To", widget=forms.Select(choices=LANGUAGES.items()))
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