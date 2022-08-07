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
    # TODO: use https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create
    # with (maybe!) "ignore_conflicts" would speed up this process.
    # In a laptop from 2013 importing all the 110K English words takes
    # about 11 minutes (but since checking the duplicates towards the end if
    # inserts the words in a way slower speed).
    # (perhaps allowing duplicates is not the end of the world in this case,
    # or could be checked in memory before inserting it?)
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
                    WordWithTranslation.objects.create(word=title, language=language)
                    counter += 1

                    if counter % 1000 == 0:
                        print("Imported ", counter, "words")

        if event == "end" and tag == "page":
            title = None
            elem.clear()
            del elem

    f.close()

    print("Minutes to import file: ", (time.time()-start_time)/60)