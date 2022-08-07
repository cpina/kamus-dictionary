import time
from pathlib import Path

import MySQLdb
import django.db.utils
from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree

from core.models import Language, WordWithTranslation


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        import_words(options["filename"])



@transaction.atomic
def import_words(file_path):
    file_path = Path(file_path)

    if file_path.stem.startswith("enwiktionary-"):
        language = Language.objects.get(code="en")
    else:
        # needs to fix, let's see which languages and how the files are named
        raise ValueError("Cannot determine languagecode from filename")

    WordWithTranslation.objects.all().delete()

    f = file_path.open(mode="rb")

    context = etree.iterparse(f, events=("start", "end"))

    title = None

    counter = 0

    start_time = time.time()

    for event, elem in context:
        tag = etree.QName(elem.tag).localname

        if event == "start" and tag == "page":
            in_page = True

        if event == "end" and tag == "title":
            title = elem.text

        if event == "end" and tag == "text":
            if elem.text is not None and "{{trans-top|" in elem.text:
                # The word is translated: add it to the table
                if len(title) > 100:
                    print("Too long title:", title)
                else:
                    word_with_translation, created = WordWithTranslation.objects.get_or_create(word=title, language=language)
                    if created is False:
                        print("Duplicated entry:", title)

                    counter += 1

                    if counter % 1000 == 0:
                        print("Imported ", counter, "words")

        if event == "end" and tag == "page":
            title = None
            elem.clear()
            del elem

    f.close()

    print("Minutes to import file: ", (time.time()-start_time)/60)