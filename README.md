# Oscar Daily Pull — a CrossPoint plugin for Daniel's X4

A personal CrossPoint SD plugin that pulls two files Oscar prepares every
morning onto the reader:

- `sleep.bmp` — the day's dashboard (480x800), saved to the SD root so it
  becomes the custom sleep screen.
- `briefing.epub` — the morning briefing as a small EPUB, saved to the SD
  root so it appears in the library.

Two surfaces, one shared config (`/.crosspoint/oscar-pull.json` holding
`{"base": "<feed base URL>"}`):

- `device.json` — on-reader catalog (Home > Plugins > Oscar Daily Pull).
  Its browse feed is `<base>/catalog.json`; items carry absolute download
  URLs (see `tools/publish_feed.py`).
- `plugin.js` — WebUI Settings page to set the base URL and pull either
  file (or both) via `api.fetchToSd`.

## Layout

- `oscar-pull.crosspoint-plugin/` — the installable payload (Plugin Hub
  contract layout; directory stem matches `manifest.json -> name`).
- `feed/catalog.json` — the live feed catalog the plugin reads. The
  morning briefing regenerates it daily: the dashboard BMP and briefing
  EPUB are uploaded to file storage (links live ~48 hours) and the
  catalog points at the fresh URLs.
- `server/` — a sample feed (catalog template with relative URLs).
- `tools/publish_feed.py` — writes a publish-ready catalog (absolute
  URLs) from a dashboard BMP + briefing EPUB.
- `tools/make_epub.py` — builds an EPUB from plain text (used for the
  daily briefing EPUB).
- `tools/make_sample_epub.py` — builds the sample briefing EPUB.

## Install (manual sideload)

Copy the contents of `oscar-pull.crosspoint-plugin/` into
`/.crosspoint/plugins/oscar-pull/` on the SD card, start File Transfer
once to open the WebUI, set the feed base URL under Settings >
Oscar Daily Pull, and set the reader's Sleep Screen to Custom.

## Publishing to Plugin Hub (optional, later)

The payload follows the Plugin Hub contract: public repo, topic
`crosspoint-plugin`, one direct-child payload folder, stable Release tag
matching the manifest version (`v0.1.0`).
