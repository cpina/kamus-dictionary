import unittest

from wiktionary.search import get_translation, get_senses


class SearchTests(unittest.TestCase):
    def test_get_translation(self):
        test_params = [
            {
                "language_code": "ca",
                "text": "* Basque: {{tt+|eu|kaixo}}\n* Catalan: {{tt+|ca|hola}}",
                "translations": [{"translation": "hola"}],
            },
            {
                "language_code": "abs",
                "text": "* Ambonese Malay: {{tt|abs|wai}}",
                "translations": [{"translation": "wai"}],
            },
            {
                "language_code": "ca",
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"},
                                 {"translation": "mani'm"}],
            },
            {
                "language_code": "ca",
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"},
                                 {"translation": "mani'm"}],
            },
            {
                "language_code": "ca",
                "text": "* Catalan: {{tt+|ca|hola|alt=hola?}}, {{tt|ca|na maria?}}",
                "translations": [{"translation": "hola", "alternatives": [{"translation": "hola?"}]},
                                 {"translation": "na maria?"}],
            },
            {
                "language_code": "ca",
                "translations": [{"translation": "radiador", "gender": "m"}],
                "text": "* Catalan: {{t+|ca|radiador|m}}"
            },
            {
                "language_code": "ca",
                "translations": [{"translation": "pilotes", "gender": "f", "number": "p"}],
                "text": "* Catalan: {{t+|ca|pilotes|f-p}}"
            },
        ]

        for param in test_params:
            with self.subTest(params=param):
                self.assertEqual(param["translations"], get_translation(param["language_code"], param["text"]))

    def test_get_senses(self):
        test_params = [
            {
                "text": """blah blah
{{trans-top|short greeting}}
* Catalan: {{t+|ca|adéu}}
{{trans-bottom}}something more""",
                "senses": [{'endpos': 81, 'sense': 'short greeting', 'startpos': 10}]
            },
            {
                "text": """blah blah
{{trans-top|short greeting}}
* Catalan: {{t+|ca|adéu}}
{{trans-bottom}}something more
{{trans-top|something else}}
* Spanish something
{{trans-bottom}}footnote""",
                "senses": [{'endpos': 81, 'sense': 'short greeting', 'startpos': 10}, {'endpos': 161, 'sense': 'something else', 'startpos': 96}]
            }
        ]

        for param in test_params:
            with self.subTest(params=param):
                self.assertEqual(get_senses(param["text"]), param["senses"])