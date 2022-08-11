#!/usr/bin/env python3

# Just a test on how to read a dump file
# to extract the pages that contain "trans-top"

from lxml import etree
from search import _get_translation

f = open("/home/carles/wiktionary/enwiktionary-20220801-pages-articles.xml", "rb")

context = etree.iterparse(f, events=("start", "end"))

in_page = False
title = None

output = open("/home/carles/wiktionary/output-test.txt", "w")
translations = None

for event, elem in context:
    tag = etree.QName(elem.tag).localname

    if event == "start" and tag == "page":
        in_page = True

    if event == "end" and tag == "title":
        title = elem.text

    if event == "end" and tag == "text":
        if elem.text is not None:
            translations = "{{trans-top|" in elem.text
            # catalan_translation = get_translation("ca", elem.text)

        print("Title", title, "has translations:", translations, file=output)

    if event == "end" and tag == "page":
        in_page = False
        title = None
        elem.clear()
        del elem

output.close()
f.close()
