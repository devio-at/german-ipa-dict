pageTitle = ""
langFound = False
pronFound = False

format = "csv"

with open('dewiktionary-20221120-pages-meta-current.xml', newline='') as f:
    while True:
        line = f.readline()
        if not line:
            break
        
        if line.find("</page>") > -1:
            pageTitle = ""
            pronFound = False
            continue

        if line.find("<title>") > -1:
            pt = line.replace("<title>", "").replace("</title>", "").strip()
            if pt.find(":") > -1:    # skip pages in namespaces
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
            continue
        elif line.startswith("{{"):
            pronFound = False
            continue

        if not pronFound:
            continue

        if line.startswith(":{{IPA}}"):     # or line.startswith("** {{IPA|de|"):
            items = line.replace(":{{IPA}}", "").strip().split(",")
            for item in items:
                parts = item.strip().split("{{Lautschrift|")
                ipa = ""
                desc = ""

                if len(parts) == 1:
                    ipa = parts[0].replace("}}", "").strip()
                    
                elif len(parts) == 2:
                    ipa = parts[1].replace("}}", "").strip()
                    desc = parts[0].replace("''", "").replace("[[", "").replace("]]", "").strip()

            #if format == "all":
            #    print("page: " + pageTitle + "; IPA de: " + ipa
            #        + (("; " + (", ".join(
            #            map(lambda p: p.replace("|", ":").replace("}}", "").strip(), parts[2:]))))
            #            if len(parts) > 2 else ""))

                if format == "csv":
                    print(pageTitle + ",/" 
                        + (ipa if ipa.find(",")==-1 else ("\"" + ipa + "\"")) + "/"
                        + (",\"" + desc + "\"" if len(desc) > 1 else "")
                            #+ (", ".join(
                            #    map(lambda p: 
                            #        p.replace("|", ":").replace("}}", "").replace("\"", "'").strip(), 
                            #    parts[2:])))
                            #+ "\"")
                            #if len(parts) > 2 else "")
                    )

f.close()
