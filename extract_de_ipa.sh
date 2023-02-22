python3 ./extract_de_ipa.py  > de_dewikt_raw.csv
LC_ALL=C sort -u -o de_dewikt.csv < de_dewikt_raw.csv
