import pywikibot
import re


def expand_gender_plural(word):
    m = re.search(r"(?P<word>.+?)\|(?P<gender>[mfn])?-?(?P<number>[ps])?-?(tr=(?P<transcription>.+))?", word)

    if m is not None:
        translation = {"translation": m.group("word")}

        if m.group("gender"):
            translation["gender"] = m.group("gender")

        if m.group("number"):
            translation["number"] = m.group("number")

        if m.group("transcription"):
            translation["transcription"] = m.group("transcription")
    else:
        translation = {"translation": word}

    return translation


def translation_text_to_dictionary(translation_text):
    """
    From hola|m returns {"translation": "hola", "gender": "m"}
    From hola|m returns {"translation": "hola", "gender": "m"}
    # From hola|alt=hola? returns {"translation": "hola", "alternatives": [{"translation": "hola"}]
    """

    m = re.search(r"(.+?)\|alt=(.+)$", translation_text)
    if m is not None:
        translation = {**expand_gender_plural(m.group(1)), "alternatives": [{"translation": m.group(2)}]}
    else:
        translation = {**expand_gender_plural(translation_text)}

    return translation


def get_translation(language_code, text):
    # To find in text: : '* Basque: {{tt+|eu|kaixo}}
    #                     * Catalan: {{tt+|ca|hola}}'
    qualifier_pre = r"({{q(ualifier)?\|(?P<qualifier_pre>.+?)}})?"
    qualifier_post = r"({{q(ualifier)?\|(?P<qualifier_post>.+?)}})?"
    translations = re.finditer(qualifier_pre + r" ?{{tt?\+?\|" + language_code + r"\|(?P<translation>.+?)}} ?" + qualifier_post, text)

    result = []

    for translation in translations:
        translation_text = translation.group("translation")

        translation_dictionary = translation_text_to_dictionary(translation_text)

        if translation.group("qualifier_post"):
            translation_dictionary["qualifier"] = translation.group("qualifier_post")

        if translation.group("qualifier_pre"):
            # It assumes that qualifier_pre and post does not exist. Never seen it
            translation_dictionary["qualifier"] = translation.group("qualifier_pre")

        result.append(translation_dictionary)

    return result


def get_senses(text):
    result = []

    # trans-top: https://en.wiktionary.org/wiki/Template:trans-top
    # trans-top-also: https://en.wiktionary.org/wiki/Template:trans-top-also
    # trans-top-see: https://en.wiktionary.org/wiki/Template:trans-see
    #                TODO: implement for trans-top-see no gloss (only "also...")

    for trans_top in re.finditer(r"{{trans-top(?P<also>-also)?(?P<see>-see)?\|(?P<parameters>.+)}}", text):
        trans_bottom = re.search(r"{{trans-bottom}}", text[trans_top.start():])

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

def search(source, to, word):
    site = pywikibot.Site(source, "wiktionary")
    page = pywikibot.Page(site, word)

    result = {}

    result["source"] = page.full_url()

    result["senses"] = get_senses(page.text)

    for sense in result["senses"]:
        translations_section = page.text[sense["startpos"]:sense["endpos"]]

        if (translations := get_translation(to, translations_section)) is not None:
            sense["translations"] = translations

    # sorts the translations to have the ones without a translation at the bottom
    result["senses"].sort(key=lambda t: len(t["translations"]) == 0)

    return result
