import unittest

from wiktionary.search import WordInformation


class SearchTests(unittest.TestCase):
    def test_get_translation(self):
        test_params = [
            {
                "language_code": "en",
                "from_lang": "es",
                "text": "{{t+|en|jump|,|leap|,|spring|,|hop|}}",
                "translations": [{"translation": "jump",
                                  "alternatives": [{"translation": "leap"}, {"translation": "spring"},
                                                   {"translation": "hop"}]}],
            },
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
            },
            {
                "language_code": "ja",
                "from_lang": "en",
                "translations": [{'transcription': 'maji?', 'translation': 'マジ？'}],
                "text": "{{tt|ja|[[マジ]]？|tr=maji?}}"
            },
            {
                "language_code": "en",
                "from_lang": "ca",
                "translations": [{'translation': 'silent something'}],
                "text": "* {{en}}: {{trad|en|silent [[something]]}}",
                # Words with [[ something ]] in Wiktionary are a link to the
                # word (ignored in Kamus)
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
                "text":
                    """
                    blah blah
                    {{trans-top|short greeting}}
                    * Catalan: {{t+|ca|adéu}}
                    {{trans-bottom}}something more
                    """,
                "from_lang": "en",
                "senses": [{'sense': 'short greeting'}]
            },
            {
                "text":
                    """
                    blah blah
                    {{trans-top|short greeting}}
                    * Catalan: {{t+|ca|adéu}}
                    {{trans-bottom}}something more
                    {{trans-top|something else}}
                    * Spanish something
                    {{trans-bottom}}footnote
                    """,
                "from_lang": "en",
                "senses": [{'sense': 'short greeting'},
                           {'sense': 'something else'}]
            },
            {
                "text":
                    """
                    blah blah
                    {{trans-top-also|short greeting|goodbye}}
                    * Catalan: {{t+|ca|adéu}}
                    {{trans-bottom}}something more
                    """,
                "from_lang": "en",
                "senses": [{'also': ['goodbye'], 'sense': 'short greeting'}]
            },
            {
                "text":
                    """"
                    blah blah
                    {{trans-top-also|short greeting|goodbye|somethingelse}}
                    * Catalan: {{t+|ca|adéu}}
                    {{trans-bottom}}something more
                    """,
                "from_lang": "en",
                "senses": [{'also': ['goodbye', 'somethingelse'], 'sense': 'short greeting'}]
            },
            {
                "text":
                    """
                    blah blah
                    {{trans-top-see|short greeting|goodbye|somethingelse}}
                    * Catalan: {{t+|ca|adéu}}
                    {{trans-bottom}}something more
                    """,
                    "from_lang": "en",
                    "senses": [{'also': ['goodbye', 'somethingelse'], 'sense': 'short greeting'}]
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
                "senses": [{"see": [{"word": "something else"}]}],
            },
            {
                "text":
                    """
                    blah blah
                    {{trans-see|to break wind|break wind}}
                    note that no trans-bottom for this one.
                    {{trans-top|type of fruit}}
                    """,
                "from_lang": "en",
                "senses": [{"see": [{"word": "to break wind"}, {"word": "break wind"}]}]
            },
            {
                "text":
                    """
                    blah blah
                    {{-trad-}}
                    {{inici|Moble}}
                    * {{af}}: {{trad|af|tafel}}
                    {{final}}

                    {{inici|Matriu de files i columnes}}
                    * {{sq}}: {{trad|sq|tabelë|f}}
                    {{final}}
                    blah blah
                    """,
                    "from_lang": "ca",
                    "senses": [
                        {"sense": "Moble"},
                        {"sense": "Matriu de files i columnes"}
                    ]
            },
            {
                "text":
                    """
                    blah blah
                    {{inici}}
                    something
                    {{final}}
                    something else
                    """,
                "from_lang": "ca",
                "senses": [{"sense": ""}]
            },
            {
                "text":
                    """
                    blah blah
                    {{{{trad-arriba|[1] mueble}}
                    something
                    {{trad-abajo}}
                    """,
                "from_lang": "es",
                "senses": [{"sense": "mueble"}]
            },
            {
                "text":
                    """
                    {{trans-top|id=Q283|clear liquid H₂O}}
                    something
                    {{trans-bottom}}
                    """,
                "from_lang": "en",
                "senses": [{'sense': 'clear liquid H₂O'}]
            }
        ]

        for param in test_params:
            with self.subTest(params=param):
                word_information = WordInformation("some_word", param["from_lang"], "xx", param["text"])
                self.assertEqual(word_information._get_senses()["senses"], param["senses"])
