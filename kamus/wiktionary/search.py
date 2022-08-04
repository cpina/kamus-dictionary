import pywikibot
import re


def expand_gender_plural(word):
    m = re.search(r"(?P<word>.+?)\|(?P<gender>[mf])-?(?P<number>[ps])?", word)

    if m is not None:
        translation = {"translation": m.group("word")}

        if m.group("gender"):
            translation["gender"] = m.group("gender")

        if m.group("number"):
            translation["number"] = m.group("number")
    else:
        translation = {"translation": word}

    return translation


def translation_text_to_dictionary(translation_text):
    """
    From hola|m returns {"translation": "hola", "gender": "m"}
    From hola|m returns {"translation": "hola", "gender": "m"}
    # From hola|alt=hola? returns {"translation": "hola", "alternatives": [{"translation": "hola"}]
    """
    # if

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


def search(source, to, word):
    site = pywikibot.Site(source, "wiktionary")
    page = pywikibot.Page(site, word)

    result = {}

    result["source"] = page.full_url()

    result["senses"] = []

    for trans_top in re.finditer(r"trans-top\|(.+)}}", page.text):
        trans_bottom = re.search(r"trans-bottom", page.text[trans_top.start():])

        if trans_bottom is None:
            # TODO: log, Wiktionary page broken
            continue

        result["senses"].append({"sense": trans_top.group(1), "startpos": trans_top.start(),
                                 "endpos": trans_top.start() + trans_bottom.end()})

    for sense in result["senses"]:
        translations_section = page.text[sense["startpos"]:sense["endpos"]]

        if (translations := get_translation(to, translations_section)) is not None:
            sense["translations"] = translations

    # sorts the translations to have the ones without a translation at the bottom
    result["senses"].sort(key=lambda t: len(t["translations"]) == 0)

    return result
