#!/usr/bin/env python3
"""Build a minimal valid EPUB (sample briefing) for the Oscar Daily Pull feed."""
import zipfile

XHTML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Briefing — Friday, October 23, 2026</title></head>
<body>
<h1>Friday, October 23, 2026</h1>
<p><i>Sample briefing EPUB — the real one lands with the 7 AM briefing.</i></p>
<h2>Today</h2>
<p>Morning — office: set up speakers.</p>
<p>1:00 PM — WS08 workshop (Teams). Out the door by 1:45 PM.</p>
<h2>Flights — AA, confirmation AYSXWW</h2>
<p>AA 2929, OKC to DFW, 3:14–4:29 PM, seat 12F.</p>
<p>52-minute layover at DFW.</p>
<p>AA 2784, DFW to LAS, 5:21–6:15 PM, seat 18A.</p>
<h2>Tonight in Vegas</h2>
<p>Circus Circus — check-in. Itinerary 73570255816424.</p>
<p>Adison meets you there. Sunny, 72 / 59.</p>
<h2>Ahead</h2>
<p>Sunday Oct 25 — Fontainebleau check-in. Conf 5100403898-1.</p>
<p>Monday Oct 26 — Guidewire Connections begins.</p>
</body></html>
"""

OPF = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:identifier id="bookid">urn:oscar:briefing-2026-10-23</dc:identifier>
    <dc:title>Briefing — Friday, October 23, 2026</dc:title>
    <dc:creator>Oscar</dc:creator>
    <dc:language>en</dc:language>
  </metadata>
  <manifest><item id="briefing" href="briefing.xhtml" media-type="application/xhtml+xml"/></manifest>
  <spine><itemref idref="briefing"/></spine>
</package>
"""

CONTAINER = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""

out = "/home/hatch/workspace/xteink/oscar-pull/server/briefing.epub"
with zipfile.ZipFile(out, "w") as z:
    z.writestr("mimetype", "application/epub+zip", zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml", CONTAINER, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/content.opf", OPF, zipfile.ZIP_DEFLATED)
    z.writestr("OEBPS/briefing.xhtml", XHTML, zipfile.ZIP_DEFLATED)
print("wrote", out)
