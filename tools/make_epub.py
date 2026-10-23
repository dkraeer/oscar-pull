#!/usr/bin/env python3
"""Build a small EPUB from plain text.

Text format (line-based):
- "# " line  -> <h1>
- "## " line -> <h2>
- consecutive "- " lines -> a <ul> of <li> items
- other non-empty lines -> paragraphs (consecutive lines join; a blank
  line ends the paragraph)
- Markdown **bold** markers are stripped.

A small stylesheet keeps heading sizes modest on readers whose default
heading styles are oversized.

Usage: python3 make_epub.py --title "Briefing — Friday, October 23, 2026" \
    --id urn:oscar:briefing-2026-10-23 --text briefing.txt --out briefing.epub
"""
import argparse
import html
import re
import zipfile

CSS = """body { font-family: serif; line-height: 1.35; margin: 0 2%; }
h1 { font-size: 1.25em; margin: 0.6em 0 0.3em; }
h2 { font-size: 1.1em; margin: 0.8em 0 0.25em; }
p { font-size: 1em; margin: 0.3em 0; }
ul { margin: 0.25em 0 0.5em; padding-left: 1.2em; }
li { font-size: 1em; margin: 0.15em 0; }
"""


def clean(text):
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text).replace("**", "")


def to_blocks(lines):
    blocks = []
    para = []
    items = []

    def flush_para():
        if para:
            blocks.append(f"<p>{html.escape(clean(' '.join(para)))}</p>")
            para.clear()

    def flush_list():
        if items:
            lis = "".join(f"<li>{html.escape(clean(i))}</li>" for i in items)
            blocks.append(f"<ul>{lis}</ul>")
            items.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_para()
            flush_list()
        elif line.startswith("## "):
            flush_para()
            flush_list()
            blocks.append(f"<h2>{html.escape(clean(line[3:]))}</h2>")
        elif line.startswith("# "):
            flush_para()
            flush_list()
            blocks.append(f"<h1>{html.escape(clean(line[2:]))}</h1>")
        elif line.startswith("- "):
            flush_para()
            items.append(line[2:])
        else:
            flush_list()
            para.append(line)
    flush_para()
    flush_list()
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    lines = open(args.text, encoding="utf-8").read().splitlines()
    body = "\n".join(to_blocks(lines))

    xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>{html.escape(args.title)}</title>
<style type="text/css">
{CSS}</style></head>
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
