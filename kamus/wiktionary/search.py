import pywikibot
import re


def get_translation(language_code, text):
    translations = re.finditer(r"\{\{tt?\+?\|" + language_code + r"\|(.+?)}}", text)

    result = []

    for translation in translations:
        result.append(translation.group(1))

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
