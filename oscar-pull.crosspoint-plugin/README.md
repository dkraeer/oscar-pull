Oscar Daily Pull

Pulls today's dashboard sleep screen and briefing EPUB from Oscar's
daily feed onto the reader.

WHAT IT DOES
- On the reader: Home > Plugins > Oscar Daily Pull lists today's files
  from the feed; tap one to download it. The dashboard lands at /sleep.bmp
  (the top-priority custom sleep screen) and the briefing at
  /briefing.epub (shows in the library).
- In the browser WebUI (Settings > Oscar Daily Pull): set the feed base
  URL and pull either file, or both, with one tap.

SETUP
1. The feed is one small file served over HTTPS: catalog.json, listing
   today's items with absolute download URLs (the files themselves may
   live on another host). Oscar refreshes the catalog every morning
   with the briefing.
2. Open the WebUI plugin once and save the feed base URL. It is stored
   on the SD card at /.crosspoint/oscar-pull.json and shared by both
   surfaces. You can also edit that file directly; it contains one line:
   {"base": "https://your-feed.example/x4-daily"}
3. On the reader, set Settings > Display > Sleep Screen to Custom so
   the pulled dashboard is the sleep screen.

NOTES
- Downloads do not follow redirects; the feed must serve files directly.
- No accounts or tokens are bundled. If the feed is ever protected, the
  token lives only on your SD card.
