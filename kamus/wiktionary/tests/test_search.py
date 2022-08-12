import unittest

from wiktionary.search import WordInformation


class SearchTests(unittest.TestCase):
    def test_get_translation(self):
        test_params = [
            {
                "language_code": "ca",
                "from_lang": "en",
                "text": "* Basque: {{tt+|eu|kaixo}}\n* Catalan: {{tt+|ca|hola}}",
                "translations": [{"translation": "hola"}],
            },
            {
                "language_code": "abs",
                "from_lang": "en",
                "text": "* Ambonese Malay: {{tt|abs|wai}}",
                "translations": [{"translation": "wai"}],
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"},
                                 {"translation": "mani'm"}],
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "text": "* Catalan: {{tt+|ca|digui}}, {{tt+|ca|si}}, {{tt+|ca|hola}}, {{tt|ca|mani'm}}",
                "translations": [{"translation": "digui"}, {"translation": "si"}, {"translation": "hola"},
                                 {"translation": "mani'm"}],
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "text": "* Catalan: {{tt+|ca|hola|alt=hola?}}, {{tt|ca|na maria?}}",
                "translations": [{"translation": "hola", "alternatives": [{"translation": "hola?"}]},
                                 {"translation": "na maria?"}],
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "translations": [{"translation": "radiador", "gender": "m"}],
                "text": "* Catalan: {{t+|ca|radiador|m}}"
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "translations": [{"translation": "pilotes", "gender": "f", "number": "p"}],
                "text": "* Catalan: {{t+|ca|pilotes|f-p}}"
            },
            {
                "language_code": "la",
                "from_lang": "en",
                "translations": [{"translation": "rationarium", "gender": "n"}],
                "text": "* Latin: {{tt|la|rationarium|n}}"
            },
            {
                "language_code": "cmn",
                "from_lang": "en",
                "translations": [{"translation": "你好", "transcription": "nǐ hǎo"}],
                "text": "*: Mandarin: {{tt+|cmn|你好|tr=nǐ hǎo}}",
            },
            {
                "language_code": "ca",
                "from_lang": "en",
                "translations": [{"translation": "passar-ho bé", "alternatives": [{'translation': 'passa-ho bé'}],
                                  "qualifier": "informal"}, {'translation': 'somethingelse'}],
                "text": "* Catalan: {{t|ca|passar-ho bé|alt=passa-ho bé}} {{q|informal}}, {{t|ca|somethingelse}}",
            },
            {
                "language_code": "nl",
                "from_lang": "en",
                "translations": [{'translation': 'doei', "qualifier": "informal"}],
                "text": "* Dutch: {{t+|nl|doei}} {{qualifier|informal}}",
            },
            {
                "language_code": "hu",
                "from_lang": "en",
                "translations": [{'translation': 'agyő', 'qualifier': 'dated'}],
                "text": "* Hungarian: {{q|dated}} {{t|hu|agyő}}",
            },
            {
                "language_code": "hu",
                "from_lang": "en",
                "translations": [{'translation': 'agyő', 'qualifier': 'dated'}],
                "text": "* Hungarian: {{qualifier|dated}} {{t|hu|agyő}}",
            },
            {
                "language_code": "es",
                "from_lang": "ca",
                "translations": [{'translation': 'mesa'}],
                "text": "* {{es}}: {{trad|es|mesa}}",
            },
            {
                "language_code": "en",
                "from_lang": "es",
                "translations": [{'translation': 'hello', 'alternatives': [{'translation': 'hi'}]}],
                "text": "{{t+|en|1|hello|,|hi}}",
            }
        ]

        for param in test_params:
            with self.subTest(params=param):
                self.assertEqual(param["translations"],
                                 WordInformation._get_translation(param["from_lang"], param["language_code"],
                                                                  param["text"]))

    def test_get_senses(self):
        test_params = [
            {
                "text": """blah blah
{{trans-top|short greeting}}
* Catalan: {{t+|ca|adéu}}
{{trans-bottom}}something more""",
                "from_lang": "en",
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
                "from_lang": "en",
                "senses": [{'endpos': 81, 'sense': 'short greeting', 'startpos': 10},
                           {'endpos': 161, 'sense': 'something else', 'startpos': 96}]
            },
            {
                "text": """blah blah
        {{trans-top-also|short greeting|goodbye}}
        * Catalan: {{t+|ca|adéu}}
        {{trans-bottom}}something more""",
                "from_lang": "en",
                "senses": [{'also': ['goodbye'], 'endpos': 118, 'sense': 'short greeting', 'startpos': 18}]
            },
            {
                "text": """blah blah
        {{trans-top-also|short greeting|goodbye|somethingelse}}
        * Catalan: {{t+|ca|adéu}}
        {{trans-bottom}}something more""",
                "from_lang": "en",
                "senses": [
                    {'also': ['goodbye', 'somethingelse'], 'endpos': 132, 'sense': 'short greeting', 'startpos': 18}]
            },
            {
                "text": """blah blah
                {{trans-top-see|short greeting|goodbye|somethingelse}}
                * Catalan: {{t+|ca|adéu}}
                {{trans-bottom}}something more""",
                "from_lang": "en",
                "senses": [
                    {'also': ['goodbye', 'somethingelse'], 'endpos': 155, 'sense': 'short greeting', 'startpos': 26}]
            },
            {
                "text":
                    """
                    blah blah
                    {{trans-see|something else}}
                    note that no trans-bottom for this one.
                    {{trans-top|type of fruit}}
                    """,
                "from_lang": "en",
                "senses": [
                    {"see": ["something else"], "startpos": 51, "endpos": 130},
                    ],
            },
            {
                "text": """blah blah
                {{-trad-}}
                {{inici|Moble}}
                * {{af}}: {{trad|af|tafel}}
                {{final}}

                {{inici|Matriu de files i columnes}}
                * {{sq}}: {{trad|sq|tabelë|f}}
                {{final}}
                blah blah""",
                "from_lang": "ca",
                "senses": [{"sense": "Moble", "startpos": 53, "endpos": 138},
                           {"sense": "Matriu de files i columnes", "startpos": 156, "endpos": 265}]
            },
            {
                "text": """blah blah
            {{inici}}
            something
            {{final}}
            something else
            """,
            "from_lang": "ca",
            "senses": [{"sense": "", "startpos": 22, "endpos": 75}]
            },
            {
                "text": """blah blah
            {{{{trad-arriba|[1] mueble}}
            something
            {{trad-abajo}}
            """,
            "from_lang": "es",
            "senses": [{"sense": "mueble", "startpos": 24, "endpos": 99}]
            }

        ]

        for param in test_params:
            with self.subTest(params=param):
                word_information = WordInformation(param["from_lang"], "xx", param["text"])
                self.assertEqual(word_information._get_senses(), param["senses"])
