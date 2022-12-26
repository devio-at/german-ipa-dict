# german-ipa-dict
German IPA dictionary as extracted from wiktionary

## Generate de.csv from en.wiktionary

- Download `enwiktionary-****-pages-meta-current.xml` dump from [Wikimedia](https://dumps.wikimedia.org/backup-index.html)
- `$ python3 ./extract_de_ipa_en.py  > de_enwikt_raw.csv`
- `$ sort < de_enwikt_raw.csv > de_enwikt.csv`

## Generate de.csv from de.wiktionary

- Download `dewiktionary-****-pages-meta-current.xml` dump from [Wikimedia](https://dumps.wikimedia.org/backup-index.html)
- `$ python3 ./extract_de_ipa.py  > de_dewikt_raw.csv`
- `$ sort < de_dewikt_raw.csv > de_dewikt.csv`

