import pywikibot
import re


class Config:
    CONFIG = {
        "en":
            {
                "header_translation_table": r"{{trans-top(?P<also>-also)?(?P<see>-see)?\|(?P<parameters>.+)}}",
                "footer_translation_table": r"{{trans-bottom}}",
                "tt_before_word": r" ?{{tt?\+?\|",
                "tt_after_word":  r"\|(?P<translation>.+?)}} ?",
                "translation_tables": ["{{trans-top|", "{{see translation subpage"]
            },
        "ca":
            {
                "header_translation_table": r"{{inici\|(?P<parameters>.*)}}",
                "footer_translation_table": r"{{final}}",
                "tt_before_word": r"{{trad\|",
                "tt_after_word": r"\|(?P<translation>.+?)}} ?",
                "translation_tables": ["{{-trad-}}"]
            }
    }

    @classmethod
    def get_config(cls, from_lang, parameter):
        if from_lang not in cls.CONFIG.keys():
            raise NotImplementedError(f"{from_lang} not implemented")

        return cls.CONFIG[from_lang].get(parameter, cls.CONFIG["en"][parameter])


class WordInformation:
    def __init__(self, from_lang, to_lang, text):
        self._from_lang = from_lang
        self._to_lang = to_lang
        self._text = text

    def get_word_information(self):
        result = {}

        result["senses"] = self._get_senses()

        for sense in result["senses"]:
            translations_section = self._text[sense["startpos"]:sense["endpos"]]

            if (translations := self._get_translation(self._from_lang, self._to_lang, translations_section)) is not None:
                sense["translations"] = translations

        # sorts the translations to have the ones without a translation at the bottom
        result["senses"].sort(key=lambda t: len(t["translations"]) == 0)

        return result

    @staticmethod
    def _get_information_from_translation(translation_macro):
        m = re.search(r"(?P<word>.+?)\|(?P<gender>[mfn])?-?(?P<number>[ps])?-?(tr=(?P<transcription>.+))?",
                      translation_macro)

        if m is not None:
            translation = {"translation": m.group("word")}

            if m.group("gender"):
                translation["gender"] = m.group("gender")

            if m.group("number"):
                translation["number"] = m.group("number")

            if m.group("transcription"):
                translation["transcription"] = m.group("transcription")
        else:
            translation = {"translation": translation_macro}

        return translation

    @classmethod
    def _translation_text_to_dictionary(cls, translation_text):
        """
        From hola|m returns {"translation": "hola", "gender": "m"}
        From hola|m returns {"translation": "hola", "gender": "m"}
        # From hola|alt=hola? returns {"translation": "hola", "alternatives": [{"translation": "hola"}]
        """

        m = re.search(r"(.+?)\|alt=(.+)$", translation_text)
        if m is not None:
            translation = {**cls._get_information_from_translation(m.group(1)),
                           "alternatives": [{"translation": m.group(2)}]}
        else:
            translation = {**cls._get_information_from_translation(translation_text)}

        return translation

    @classmethod
    def _get_translation(cls, from_lang, to_lang, table_text):
        # To find in text: : '* Basque: {{tt+|eu|kaixo}}
        #                     * Catalan: {{tt+|ca|hola}}'
        qualifier_pre = r"({{q(ualifier)?\|(?P<qualifier_pre>.+?)}})?"
        qualifier_post = r"({{q(ualifier)?\|(?P<qualifier_post>.+?)}})?"
        translations = re.finditer(
            qualifier_pre + Config.get_config(from_lang, "tt_before_word") + to_lang + Config.get_config(from_lang, "tt_after_word") + qualifier_post, table_text)

        result = []

        for translation in translations:
            translation_text = translation.group("translation")

            translation_dictionary = cls._translation_text_to_dictionary(translation_text)

            if translation.group("qualifier_post"):
                translation_dictionary["qualifier"] = translation.group("qualifier_post")

            if translation.group("qualifier_pre"):
                # It assumes that qualifier_pre and post does not exist. Never seen both of them
                translation_dictionary["qualifier"] = translation.group("qualifier_pre")

            result.append(translation_dictionary)

        return result

    def _get_senses(self):
        result = []
        # Finds the senses of the word in self._text
        # For example:
        #
        #    ====Translations====
        #    {{trans-top|item of furniture}}
        #    {{multitrans|data=
        #    * Afrikaans: {{tt|af|tafel}}
        # Returns a dictionary with the senses (Item of furniture) and the
        # beginning an

        # trans-top: https://en.wiktionary.org/wiki/Template:trans-top
        # trans-top-also: https://en.wiktionary.org/wiki/Template:trans-top-also
        # trans-top-see: https://en.wiktionary.org/wiki/Template:trans-see
        #                TODO: implement for trans-top-see no gloss (only "also...")

        for trans_top in re.finditer(Config.get_config(self._from_lang, "header_translation_table"), self._text):
            trans_bottom = re.search(Config.get_config(self._from_lang, "footer_translation_table"),
                                     self._text[trans_top.start():])

            if trans_bottom is None:
                # TODO: log, Wiktionary page broken
                continue

            parameters = trans_top.group("parameters").split("|")

            main_sense = parameters[0]

            also = {}
            if len(parameters) > 1:
                also["also"] = parameters[1:]

            result.append({"sense": main_sense, **also, "startpos": trans_top.start(),
                           "endpos": trans_top.start() + trans_bottom.end()})

        return result


def get_word_information(from_lang, to_lang, word):
    """Lookup word in the Wiktionary from source language and get for to."""
    site = pywikibot.Site(from_lang, "wiktionary")
    page = pywikibot.Page(site, word)

    text = page.text

    word_information = WordInformation(from_lang, to_lang, text)

    result = word_information.get_word_information()

    result["source"] = page.full_url()

    return result


if __name__ == "__main__":
    print(get_word_information("en", "es", "table"))
