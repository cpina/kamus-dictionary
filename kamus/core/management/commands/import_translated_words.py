import subprocess
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree

from core.models import Language, WordWithTranslation
from wiktionary.search import Config


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", type=str, help="https:// or local file")

    def handle(self, *args, **options):
        import_words(options["filename"])



def open_wiktionary(file_path):
    if file_path.startswith("https://"):
        result = subprocess.Popen(["bash", "-c", f"curl {file_path} | bunzip2"], stdout=subprocess.PIPE)
        return result.stdout
    else:
        return open(file_path, "rb")

def language_from_file_path(file_path):
    file_name = file_path.split("/")[-1]

    language_code = file_name[0:2]

    try:
        return Language.objects.get(code=language_code)
    except Language.DoesNotExist:
        raise NotImplemented(f"Filename handling for {file_name} not implemented")

def has_translation_table(from_lang, entry):
    for translation_table_tag in Config.get_config(from_lang, "translation_tables"):
        if translation_table_tag in entry:
            return True

    return False

@transaction.atomic
def import_words(file_path):
    # TODO: use https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create
    # with (maybe!) "ignore_conflicts" would speed up this process.
    # In a laptop from 2013 importing all the 110K English words takes
    # about 11 minutes (but since checking the duplicates towards the end if
    # inserts the words in a way slower speed).
    # (perhaps allowing duplicates is not the end of the world in this case,
    # or could be checked in memory before inserting it?)
    # Example file: https://dumps.wikimedia.org/cawiktionary/latest/cawiktionary-latest-pages-articles.xml.bz2


    language = language_from_file_path(file_path)

    file_with_words = open_wiktionary(file_path)

    WordWithTranslation.objects.all().filter(language=language).delete()

    context = etree.iterparse(file_with_words, events=("start", "end"))

    title = None

    counter = 0

    start_time = time.time()

    added_words = set()

    for event, elem in context:
        tag = etree.QName(elem.tag).localname

        if event == "end" and tag == "title":
            title = elem.text

        if event == "end" and tag == "text":
            if elem.text is not None and has_translation_table(language.code, elem.text):
                # The word is translated: add it to the table
                if len(title) > 100:
                    print("Too long title:", title)
                elif title in added_words:
                    print("Duplicated word:", title)
                elif title.endswith("/translations"):
                    print("Subpage:", title)
                else:
                    WordWithTranslation.objects.create(word=title, language=language)
                    # Save memory
                    # added_words.add(title)
                    counter += 1

                    if counter % 1000 == 0:
                        print("\nImported ", counter, "words")

        if event == "end" and tag == "page":
            title = None

            for ancestor in elem.xpath("ancestor-or-self::*"):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

            elem.clear()
            del elem


    print("Minutes to import file: ", (time.time()-start_time)/60)