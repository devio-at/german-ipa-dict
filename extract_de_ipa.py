import bz2
import csv
import html

import regex

INFILE = "./wikidata/dewiktionary-20231020-pages-meta-current.xml.bz2"
OUTFILE = "./de_dewikt.csv"

# modes:

check = False # or True
test = False # or True

#

patternRef = "&lt;ref.*?(?:&gt;.*?&lt;/ref|/)&gt;"                # <ref>
patternWords = "\w+(?:\s+\w+)*"
patternWordsComma = "\w+(?:[,/\s]+\w+)*"

def getPatternIpa(name: str) -> str:
    return ("\{\{Lautschrift\??\s?\|"
            + "(?:spr=[^|}]+\|)?"                   # |spr=xx|(IPA)
            + "(?P<" + name + ">[^|}]*?)"           # (IPA)
            + "(?:\|spr=[^}]+)?"                    # (IPA)|spr=xx
            + "\}\}"
    )

patternStr = ("^"
            + "(?:(?:(?:\[.+?\])|die|der|das|ein |A\)|bei Plural \d:)\s*)?"              # references [1] etc, occasional article
            + "(?:&lt;!--.*?--&gt;\s*)?"                                                # HTML comment
            + "(?P<comment0>"                                                           # various descriptions before IPA
                + "(?:\*?''.+?'')?\s*"
                + "(?:" + patternRef + ")?\s*"
                + "(?:&lt;!-- Spezialfall, NICHT löschen --&gt;)?(\{\{(?:[^}]+?)\}\})?"
                + "(?:(?:(?:" + patternWords + ")|"
                    + "\{\{nordd\.\}\} ''und \{\{md\.\}\}:''|"
                    + "''standardsprachlich \(Schweiz\)''):?)?\s*"
                + "(?:\{\{(?:nordd|südd)\.(?:\|\:)?\}\}\s*)?"
            + ")"
            # {{Lautschrift|}} template variants            
            + getPatternIpa("ipa0")                         # + "\{\{Lautschrift\??\s?\|(?P<ipa0>[^}]*?)\}\}"
                + "(?:\s*(~|oder|''oder''|&lt;small&gt;auch&lt;/small&gt;|(?:''(?:regional|, auch|auch|, beziehungsweise):?''))\s*"
                    + getPatternIpa("ipa1")                 # + "\{\{Lautschrift\??\s?\|(?P<ipa1>[^}]*?)\}\}"
                + ")?\s*"
            + "(?:[;,]?" + patternRef + ")*\s*"
            # ignore (rest of line)
            + "(?:&lt;!--.*?--&gt;\s*)?"                                                # HTML comment
            + "(?:&lt;small&gt;\(Beˈtonung fehlt\)&lt;/small&gt;\s*)?"
            + "(?:\((?:zu weiteren Aussprachevarianten siehe|vergleiche) .*?\)\s*)?"
            + "(?:\(stimmloses s im Anlaut, da nur noch in Österreich üblich\))?"
            + "(?:\(\[\[.*?\]\]\)\s*)?"
            + "(?:[\(,;]?\s*\{\{(?:Pl|Gen|Sg|Part|attr|Prät)\..+)?"
            + "(?:,\s*(?:"
                + "(?:''Varianten siehe.+?'')|"
                + "(?:weitere Aussprache(?:variante)?n siehe Haupteintrag)|"
                + "(?:sonst siehe \[\[.*?\]\])|"
                + "(?:(?:das|ein|die|der) " + getPatternIpa("dummy")    # \{\{Lautschrift\|.+?\}\}
                    + ".*)|"                 # ignore "japanisch, das japanische" etc for languages, "der achte, ein achter"
                + "(?:''schweizerisch:'' '''\?''')|"
                + "(?:\{\{(?:kSt\.|kPl\.)\}\})|"
                + "(?:&lt;!-- Spezialfall, NICHT löschen --&gt;\s*\{\{.*)"
            + "))?\s*"
            # capture comment after IPA
            + "(?P<commentAfter0>(?:"
                + "(?:[,]?\s*"
                    + "(?:" + patternWords + ")|"
                    + "(?:\((?:" + patternWords + "|DIN-Aussprache)\))|"
                    + "(?:''.+?'':?)?\s*"
                + ")?)"
            + ")"
            + "(?P<repeat>[,/;\|]\s*"                                   # repeat IPA clauses
                + "(?:" + patternRef + ")*\s*"
                + "(?:\w\))?"
                + "(?:\[.*?\])?"
                + "(?P<comment>"                                        # various descriptions before subsequent IPAs
                    + "(?:''.+?'':?)?\s*"
                    + "(?:&lt;!-- Spezialfall, NICHT löschen --&gt;)?\s*"
                    + "(?:(?:"
                        + "(?:" + patternWordsComma + ")|"
                        + "(?:''.+?'')|"
                        + "(\(''" + patternWords+ ":?'')|"
                        + "(?:\[\[" + patternWords + "\]\])|"
                        + "(?:\{\{(?:österr|reg|südd|nordd|ugs|schweiz)\.(?:\|\:)?\}\}(?: auch)?)|"
                        + "(?:\{\{K\|[^}]*\}\})|"
                        + "''ursprünglich'' und ''regional:''|(\{\{reg.\}\} ''auch:'')|&lt;small&gt;auch&lt;/small&gt;|"
                        + "&lt;small&gt;veraltet oder gehoben veraltend:&lt;/small&gt;|"
                        + "''Ost- und Westmitteldeutsch:'' und \{\{ugs\.\}\}|"
                        + "\{\{schweiz\.\}\} ''auch:''"
                    + "):?)?\s*"
                    + "(?:,?" + patternRef + ")*\s*"                    # <ref>s
                    #+ "(?P<special>(?:\{\{[^}]+?\}\}(?:\s+auch))?)\s*"
                + ")"
                + getPatternIpa("ipa")                                  # + "\{\{Lautschrift\??\s?\|(?P<ipa>[^}]*?)\}\}"
                + "(?:,?" + patternRef + ")*"                           # <ref>s
                + "\)?"
                + "\s*"
                + "(?:\((?:zu weiteren Aussprachevarianten siehe|vergleiche) .*?\)\s*)?"
                + "(?:\(sogenanntes.+?\))?"
                + "(?:\(\[\[.*?\]\]\)\s*)?"
                + "(?:[\(,;]?\s*\{\{(?:Pl|Gen|Sg|Part|attr|Prät)\..+)?"
                + "(?::\{\{Hörbeispiele\}\}\+\{\{Audio\|\}\})?"
                + "(?:; Plural .+?)?"
                + "(?:''\(?mit Plural \d\)?'')?"
                + "(?P<commentAfter>"
                    + "(?:"
                        + "(?:''\(englisch\)'')|"
                        + "(?:\((?:" + patternWords + ")\))|"
                        + "(?:(?:,\s)?immer unbetont)"
                    + ")?"
                + ")"
            + ")*"
            + "(?:&amp;nbsp;)?"
            + "[;,snəɪ\)]*"                                             # typos at end of entry
            + "$")

if check or test:
    print(patternStr)

rexEntry = regex.compile(patternStr)

rexFallback = regex.compile("^"
            + "(?:(?:(?:Hochdeutsch|original|bundesdeutsches Hochdeutsch|Positiv \d):?)\s*)?"                
            + getPatternIpa("ipa")      # + "\{\{Lautschrift\??\s?\|(?P<ipa>[^}]*?)\}\}"
            )

rexIpa = regex.compile("^:\{\{IPA(?:\|[^}]*)?\}\}\s*")


pageTitle = ""
langFound = False
pronFound = False

commentsTable = str.maketrans("", "", "'()[]{}:")

def formatColumn(s: str) -> str:
    s = regex.sub("(\u2060|\u200b)", "", html.unescape(s))
    return s

def formatComments(c: str, ca: str) -> str:
    c = c.strip().translate(commentsTable)
    ca = ca.strip().translate(commentsTable)
    if c == "":
        return ca
    if ca == "":
        return c
    return c + " " + ca

ipaChars = set()

# searchIpa = ""

def buildRow(pageTitle: str, ipa: str, comments: str = ""):
    # global searchIpa

    plainIpa = html.unescape(html.unescape(ipa))        # MediaWiki markup inside XML text
    plainIpa = regex.sub("(\u2060|\u200b)", "", plainIpa)

    #if '1' in plainIpa:
    #    searchIpa = pageTitle

    for ch in plainIpa:
        ipaChars.add(ch)

    return [
        formatColumn(pageTitle),
        formatColumn("/" + plainIpa + "/"),
        formatColumn(comments),
    ]

def isValidIpa(s: str) -> bool:
    return s != None and s.strip() != "" and not s.startswith("-") and not "…" in s

print(f'Reading file "{INFILE}"')
resultRows = []
with bz2.open(INFILE, mode="rt", newline="") as f:
    for i, line in enumerate(f):
        if i % 100_000 == 0:
            print(f"\r{i/1_000_000:,.1f} million lines processed", end="", flush=True)
        if line.find("</page>") > -1:
            pageTitle = ""
            pronFound = False
            continue

        if line.find("<title>") > -1:
            pt = line.replace("<title>", "").replace("</title>", "").strip()
            if pt.find(":") > -1:       # skip pages in namespaces
                continue
            if pt.startswith("-"):      # don't include suffixes
                continue

            pageTitle = pt
            continue

        if pageTitle == "":
            continue

        if line.startswith("==") and line.find("|Deutsch}}") > -1:
            langFound = True
            continue
        elif line.startswith("=="):
            langFound = False
            continue

        if langFound and line.startswith("{{Aussprache}}"):
            pronFound = True
            inIpa = False
            continue
        elif line.startswith("{{"):
            pronFound = False
            inIpa = False
            continue

        if not pronFound:
            continue

        if rexIpa.match(line):      # line.startswith(":{{IPA}}"):
            inIpa = True
        elif inIpa and not line.startswith("::"):
            inIpa = False

        if not inIpa:
            continue

        if inIpa:
                                    # line.removeprefix(":{{IPA}}")
            line = regex.sub(rexIpa, "", line).strip().removeprefix("::").strip().removeprefix(":").strip().removeprefix("{{IPA}}").strip()
                                    # clean-up :{{IPA}} and :: and various typos
            if len(line) == 0:      # empty :{{IPA}} heading
                continue
            if line.find("{{Lautschrift") == -1:
                continue

            match = rexEntry.match(line)
            matchFallback = rexFallback.match(line) if not match else None

            if check:
                if not match:
                    print(pageTitle + " - no regex match: " + line)

                    if not matchFallback:
                        #print(pageTitle + " - no regex match: " + line)
                        print(pageTitle + " - no fallback regex match, giving up")
                        continue

                    print("fallback ipa '{ipa}'".format(ipa = matchFallback["ipa"]))
                continue

            if test:
                print(pageTitle + " - " + line)

                if match:
                    print("ipa0 '{ipa0}' ipa1 '{ipa1}' comment '{comment}' commentAfter '{commentAfter}'".format(
                        ipa0 = match["ipa0"], ipa1 = match["ipa1"], comment = match["comment0"], commentAfter = match["commentAfter0"]
                    ))
                    l = len(match.captures("repeat"))
                    for i in range(l):
                        print("ipa '{ipa}' comment '{comment}' commentAfter '{commentAfter}'".format(
                            ipa = match.captures("ipa")[i], comment = match.captures("comment")[i],
                            commentAfter = match.captures("commentAfter")[i]
                        ))
                    continue

                if matchFallback:
                    print("fallback ipa '{ipa}'".format(ipa = matchFallback["ipa"]))
                    continue

                print(pageTitle + " - no fallback regex match, giving up")
                continue

            # prod: not check and not test

            if match:

                if not isValidIpa(match["ipa0"]):       
                    continue

                desc = formatComments(match["comment0"], match["commentAfter0"])
                resultRows.append(buildRow(pageTitle, match["ipa0"], desc))

                if isValidIpa(match["ipa1"]):           
                    resultRows.append(buildRow(pageTitle, match["ipa1"], desc))

                l = len(match.captures("repeat"))
                for i in range(l):
                    prevDesc = desc

                    desc = formatComments(match.captures("comment")[i], match.captures("commentAfter")[i])
                    if desc == "":
                        desc = prevDesc

                    ipa = match.captures("ipa")[i]

                    if isValidIpa(ipa):
                        resultRows.append(buildRow(pageTitle, ipa, desc))

            if matchFallback:

                if not isValidIpa(matchFallback["ipa"]):
                    continue

                resultRows.append(buildRow(pageTitle, matchFallback["ipa"]))
print(f"\n{i:,} lines processed")

print("Sorting rows")
resultRows.sort(key=lambda x: x[0])
print(f"Writing rows to file '{OUTFILE}'")
with open(OUTFILE, "w") as f:
    rowWriter = csv.writer(f)
    rowWriter.writerows(resultRows)
print("done.")

# used to debug IPA
#print("characters in IPA")
#print(ipaChars)
#print(searchIpa)
