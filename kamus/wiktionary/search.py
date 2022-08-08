import pywikibot
import re


def expand_gender_plural(word):
    m = re.search(r"(?P<word>.+?)\|(?P<gender>[mf])?-?(?P<number>[ps])?-?(?P<lexical_categories>[n]?)?", word)

    if m is not None:
        translation = {"translation": m.group("word")}

        if m.group("gender"):
            translation["gender"] = m.group("gender")

        if m.group("number"):
            translation["number"] = m.group("number")

        if m.group("lexical_categories"):
            translation["lexical_categories"] = m.group("lexical_categories")
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
    translations = re.finditer(r"\{\{tt?\+?\|" + language_code + r"\|(.+?)}}", text)

    result = []

    for translation in translations:
        translation_text = translation.group(1)

        result.append(translation_text_to_dictionary(translation_text))

    return result


def get_senses(text):
    result = []

    for trans_top in re.finditer(r"{{trans-top(-also)?\|(.+)}}", text):
        trans_bottom = re.search(r"{{trans-bottom}}", text[trans_top.start():])

        if trans_bottom is None:
            # TODO: log, Wiktionary page broken
            continue

        senses = trans_top.group(2).split("|")

        main_sense = senses[0]

        also = {}
        if len(senses) > 1:
            also["also"] = senses[1:]

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
