import datetime
import re
import subprocess
import time

from pathlib import Path
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree

from core.models import Language, WordWithTranslation, Import
from wiktionary.search import Config
from django.utils import timezone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("directory", type=str, help="https:// or local directory")
        parser.add_argument("language_code", type=str, help="E.g. 'en', 'es' or 'ca'")

    def handle(self, *args, **options):
        import_words(options["directory"], options["language_code"], self.stdout, self.stderr)


def open_wiktionary(file_path):
    if not file_path.startswith("https://"):
        file_path = f"file://{file_path}"

    result = subprocess.Popen(["bash", "-c", f"curl {file_path} | bzcat"], stdout=subprocess.PIPE)
    return result.stdout


def filename_from_file_path(file_path):
    return file_path.split("/")[-1]


def has_translation_table(from_lang, entry):
    for translation_table_tag in Config.get_config(from_lang, "translation_tables"):
        if translation_table_tag in entry:
            return True

    return False


def get_latest_file_information(directory, language_code):
    result = {}

    file_name = f"{language_code}wiktionary-latest-pages-articles.xml.bz2"

    if directory.startswith("https://"):
        r = requests.get(directory)

        # TODO: stop regexps to fine the file and start using the machine readable version:
        # https://dumps.wikimedia.org/enwiktionary/20220801/dumpstatus.json

        m = re.search(
            file_name + r"</a> +(?P<date>[0-9]{2}-.{3}-[0-9]{4}) +(?P<time>[0-9]{2}:[0-9]{2}) +(?P<size>[0-9]+)",
            r.content.decode("utf-8"))

        if m is None:
            raise ValueError(f"Cannot find file {file_name} in {directory}")

        created_on = datetime.datetime.strptime(m.group("date") + " " + m.group("time"), '%d-%b-%Y %H:%M')
        created_on = created_on.replace(tzinfo=datetime.timezone.utc)

        result["created_on"] = created_on
        result["size"] = int(m.group("size"))
        result["path"] = f"{directory}/{file_name}"
        return result
    else:
        file_path = Path(directory) / file_name

        stat = file_path.lstat()

        # Using modified time on purpose for testing
        result["created_on"] = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc)
        result["size"] = stat.st_size
        result["path"] = str(file_path.absolute())

        return result


@transaction.atomic
def import_words(directory, language_code, stdout, stderr):
    # TODO: use https://docs.djangoproject.com/en/4.1/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create
    # with (maybe!) "ignore_conflicts" would speed up this process.
    # In a laptop from 2013 importing all the 110K English words takes
    # about 11 minutes (but since checking the duplicates towards the end if
    # inserts the words in a way slower speed).
    # (perhaps allowing duplicates is not the end of the world in this case,
    # or could be checked in memory before inserting it?)
    # Example file: https://dumps.wikimedia.org/cawiktionary/latest/cawiktionary-latest-pages-articles.xml.bz2

    language = Language.objects.get(code=language_code)
    file_information = get_latest_file_information(directory, language_code)
    stdout.write(f"Will start to import: {file_information}")

    try:
        imported = Import.objects.get(file_path=file_information["path"],
                                      file_created_on=file_information["created_on"],
                                      file_size=file_information["size"])
        stdout.write(f"{imported.file_path} already imported on {imported.file_created_on}, aborting")
        raise SystemExit(3)
    except Import.DoesNotExist:
        pass

    file_with_words = open_wiktionary(file_information["path"])

    words_for_language = WordWithTranslation.objects.all().filter(language=language)
    translated_words_before = words_for_language.count()

    # Deletes everything. It's in a transaction, will be re-added
    words_for_language.delete()

    context = etree.iterparse(file_with_words, events=("start", "end"))

    word = None

    translated_words = 0
    total_words = 0

    start_time = time.time()

    added_words = set()

    for event, elem in context:
        tag = etree.QName(elem.tag).localname

        if event == "end" and tag == "title":
            word = elem.text

        if event == "end" and tag == "text":
            word_text = elem.text

            total_words += 1

            # Keep memory usage low: delete ancestors and element
            # (found on internet)
            for ancestor in elem.xpath("ancestor-or-self::*"):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

            elem.clear()
            del elem

            if word_text is None or not has_translation_table(language.code, word_text):
                # Page did not have a translation
                continue

            if word in added_words:
                print("Duplicated entry:", word)
                continue

            if len(word) > 100:
                print("Too long word:", word)
                continue

            if word.endswith("/translations"):
                print("Subpage:", word)
                continue

            WordWithTranslation.objects.create(word=word, language=language)

            added_words.add(word)
            translated_words += 1

            if translated_words % 1000 == 0:
                print("\nImported ", translated_words, "words")
                print("Total number ", total_words)

    elapsed_time_minutes = (time.time() - start_time) / 60

    if translated_words_before != 0 and translated_words < translated_words_before * 0.7:
        stderr.write(f"Before this import there were {translated_words_before}, "
                     f"now {translated_words}. Aborting because the number is significantly lower")
        raise SystemExit(3)

    print(f"Import time: {elapsed_time_minutes:.2f} minutes")
    print(f"Imported words: {translated_words:,} of total number of words: {total_words:,}")
    Import.objects.create(language=language, file_path=file_information["path"], file_size=file_information["size"],
                          file_created_on=file_information["created_on"], imported_on=timezone.now(),
                          translated_words=translated_words, total_words=total_words)
