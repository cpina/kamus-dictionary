import unittest

from wiktionary.search import get_translation


class SearchTests(unittest.TestCase):
    def test_get_translation(self):
        test_params = [
            {
             "language_code": "ca",
             "translations": ["hola"],
             "text": "* Basque: {{tt+|eu|kaixo}}\n* Catalan: {{tt+|ca|hola}}"
             },
            {
                "language_code": "abs",
                "translations": ["wai"],
                "text": "* Ambonese Malay: {{tt|abs|wai}}"
            },
            {
                "language_code": "ca",
                "translations": ['digui', 'si', 'hola', "mani'm"],
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}"
            },
        ]

        for param in test_params:
            with self.subTest(params=param):
                self.assertEqual(param["translations"], get_translation(param["language_code"], param["text"]))
