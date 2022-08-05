#!/usr/bin/env python3


# Just testing if it's feasible to download pages to detect if they have
# translations. Or better use some dump?
import sys
from pathlib import Path

import pywikibot

def main():
    outdir = Path(sys.argv[1])
    Path.mkdir(outdir, exist_ok=True)

    site = pywikibot.Site("en", "wiktionary")
    site.login()

    lemmas = pywikibot.Category(site, "English_lemmas")

    for page in lemmas.articles():
        title = page.title()

        print(page.title())

        with open(outdir / Path(title.replace("/", "_")), "w") as outfile:
            print(title, file=outfile)
            print("", file=outfile)
            print(page.text, file=outfile)

if __name__ == "__main__":
    main()