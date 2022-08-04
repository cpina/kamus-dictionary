import pywikibot
import re

def expand_gender_plural(word):
    m = re.search(r"(.+?)\|([mf])", word)

    if m is not None:
        return {"translation": m.group(1), "gender": m.group(2)}
    else:
        return {"translation": word}


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

        # translation_text could be like: "hola|alt=hola?"
        # if it has "alt=..." we remove it and add it as
        # alternative

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

        result["senses"].append({"sense": trans_top.group(1), "startpos": trans_top.start(), "endpos": trans_top.start() + trans_bottom.end()})

    for sense in result["senses"]:
        translations_section = page.text[sense["startpos"]:sense["endpos"]]

        if (translations := get_translation(to, translations_section)) is not None:
            sense["translations"] = translations

    return result

if __name__ == "__main__":
    print(search("table"))
