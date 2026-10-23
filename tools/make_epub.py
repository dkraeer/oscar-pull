#!/usr/bin/env python3
"""Build a small EPUB from plain text.

Text format: blank-line-separated paragraphs; a line starting with "## "
becomes a heading; the first line may be the H1 if it starts with "# ".

Usage: python3 make_epub.py --title "Briefing — Friday, October 23, 2026" \
    --id urn:oscar:briefing-2026-10-23 --text briefing.txt --out briefing.epub
"""
import argparse
import html
import zipfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    blocks = []
    for chunk in open(args.text, encoding="utf-8").read().split("\n\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        text = " ".join(line.strip() for line in chunk.splitlines())
        if text.startswith("## "):
            blocks.append(f"<h2>{html.escape(text[3:])}</h2>")
        elif text.startswith("# "):
            blocks.append(f"<h1>{html.escape(text[2:])}</h1>")
        else:
            blocks.append(f"<p>{html.escape(text)}</p>")
    body = "\n".join(blocks)

    xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>{html.escape(args.title)}</title></head>
<body>
{body}
</body></html>
"""
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:identifier id="bookid">{html.escape(args.id)}</dc:identifier>
    <dc:title>{html.escape(args.title)}</dc:title>
    <dc:creator>Oscar</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest><item id="main" href="main.xhtml" media-type="application/xhtml+xml"/></manifest>
  <spine><itemref idref="main"/></spine>
</package>
"""
    container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""
    with zipfile.ZipFile(args.out, "w") as z:
        z.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/main.xhtml", xhtml, zipfile.ZIP_DEFLATED)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
