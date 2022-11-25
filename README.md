# german-ipa-dict
German IPA dictionary as extracted from wiktionary

## Generate de.csv

- Download `enwiktionary-****-pages-meta-current.xml` dump from [Wikimedia](https://dumps.wikimedia.org/backup-index.html)
- `$ python3 ./extract_de_ipa.py  > de_raw.csv`
- `$ sort < de_raw.csv > de.csv`
