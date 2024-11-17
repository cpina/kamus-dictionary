#!/bin/bash

docker exec kamus-dictionary_kamus_1 /code/venv/bin/python3 manage.py import_translated_words https://dumps.wikimedia.org/cawiktionary/latest ca

docker exec kamus-dictionary_kamus_1 /code/venv/bin/python3 manage.py import_translated_words https://dumps.wikimedia.org/eswiktionary/latest es

docker exec kamus-dictionary_kamus_1 /code/venv/bin/python3 manage.py import_translated_words https://dumps.wikimedia.org/enwiktionary/latest en
