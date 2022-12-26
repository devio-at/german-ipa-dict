pageTitle = ""
pronFound = False

format = "csv"

with open('enwiktionary-20220120-pages-meta-current.xml', newline='') as f:
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

        if line.startswith("===Pronunciation==="):
            pronFound = True
        elif line.startswith("=="):
            pronFound = False

        if line.startswith("=="):
            continue
        if not pronFound:
            continue

        if line.startswith("* {{IPA|de|") or line.startswith("** {{IPA|de|"):
            parts = line.strip().split("{{")
            ipa = parts[1].replace("IPA|de|", "").replace("}}", "").replace("|", ",").strip()

            if format == "all":
                print("page: " + pageTitle + "; IPA de: " + ipa
                    + (("; " + (", ".join(
                        map(lambda p: p.replace("|", ":").replace("}}", "").strip(), parts[2:]))))
                        if len(parts) > 2 else ""))

            if format == "csv":
                print(pageTitle + "," 
                    + (ipa if ipa.find(",")==-1 else ("\"" + ipa + "\""))
                    + ((",\"" 
                        + (", ".join(
                            map(lambda p: 
                                p.replace("|", ":").replace("}}", "").replace("\"", "'").strip(), 
                            parts[2:])))
                        + "\"")
                        if len(parts) > 2 else "")
                )

f.close()
