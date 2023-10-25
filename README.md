# german-ipa-dict
German IPA dictionary as extracted from wiktionary

## Generate de.csv from en.wiktionary

- Download `enwiktionary-****-pages-meta-current.xml` dump from [Wikimedia](https://dumps.wikimedia.org/backup-index.html)
- `$ python3 ./extract_de_ipa_en.py  > de_enwikt_raw.csv`
- `$ sort < de_enwikt_raw.csv > de_enwikt.csv`

## Generate de.csv from de.wiktionary

- Download `dewiktionary-****-pages-meta-current.xml` dump from [Wikimedia](https://dumps.wikimedia.org/backup-index.html)
- Change `INFILE` at the top of `extract_de_ipa.py` to point to the `.xml.bz2` file you downloaded
- `$ python3 ./extract_de_ipa.py`

## Documentation

- [German IPA from en.wiktionary](https://linglangchang.wordpress.com/2022/12/26/german-ipa-from-en-wiktionary/)
- [German IPA from de.wiktionary](https://linglangchang.wordpress.com/2023/01/07/german-ipa-from-de-wiktionary/)
- [An Update on German IPA from de.wiktionary](https://linglangchang.wordpress.com/2023/02/22/an-update-on-german-ipa-from-de-wiktionary/)
