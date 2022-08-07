from django.core.management.base import BaseCommand

from core.models import Language
from wiktionary import ALL_LANGUAGES


class Command(BaseCommand):
    def handle(self, *args, **options):
        for code, name in ALL_LANGUAGES.items():
            try:
                Language.objects.create(code=code, name=name)
            except:
                print("error with:", code, name)
                raise
