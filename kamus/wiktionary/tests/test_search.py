import unittest

from wiktionary.search import get_translation


class SearchTests(unittest.TestCase):
    def test_get_translation(self):
        test_params = [
            {
             "language_code": "ca",
             "translations": [{"translation": "hola"}],
             "text": "* Basque: {{tt+|eu|kaixo}}\n* Catalan: {{tt+|ca|hola}}"
             },
            {
                "language_code": "abs",
                "translations": [{"translation": "wai"}],
                "text": "* Ambonese Malay: {{tt|abs|wai}}"
            },
            {
                "language_code": "ca",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"}, {"translation": "mani'm"}],
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}"
            },
            {
                "language_code": "ca",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"}, {"translation": "mani'm"}],
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}"
            },
            {
                "language_code": "ca",
                "translations": [{"translation": "hola", "alternatives": [{"translation": "hola?"}]}, {"translation": "na maria?"}],
                "text": "* Catalan: {{tt+|ca|hola|alt=hola?}}, {{tt|ca|na maria?}}"
            }
        ]

        for param in test_params:
            with self.subTest(params=param):
                self.assertEqual(param["translations"], get_translation(param["language_code"], param["text"]))
