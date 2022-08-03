import pywikibot
import re

from wikidictionary import LANGUAGES


def search(source, to, word):
    site = pywikibot.Site(source, "wiktionary")
    page = pywikibot.Page(site, word)

    translations = []

    for translation_match in re.finditer(r"trans-top\|(.+)}}", page.text):
        translations.append({"meaning": translation_match.group(1), "start": translation_match.start(), "end": translation_match.end()})

    result = ""
    for index in range(len(translations)):
        translation_information = translations[index]

        if index + 1 == len(translations):
            end_position = None
        else:
            end_position = translations[index+1]["end"]

        sub_page = page.text[translation_information["start"]:end_position]

        translated = re.search(r"\{\{tt?\+?\|"+to+r"\|(.+)}}", sub_page)

        if translated is not None:
            translated_word = translated.group(1)
            result += f"* {translation_information['meaning']}: {translated_word}\n\n"

    return result

if __name__ == "__main__":
    print(search("table"))
