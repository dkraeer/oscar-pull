// Oscar Daily Pull — CrossPoint browser plugin (WebUI, Settings mount).
//
// Catalog-driven: reads <base>/catalog.json (via the device relay; the
// catalog is small) and downloads each listed item with api.fetchToSd to
// "/" + item.id — sleep.bmp lands at the SD root (top-priority custom
// sleep screen) and briefing.epub at the root of the library. Item URLs
// in the catalog are absolute and may point at a different host than the
// catalog itself. fetchToSd does not follow redirects; URLs must serve
// the file directly.
//
// The base URL is shared with the on-reader device.json surface through
// /.crosspoint/oscar-pull.json ({"base": "https://..."}), written here via
// api.writeFile. No credentials are bundled with this plugin.

CrossPoint.registerPlugin(async (container, api) => {
  const CONFIG_PATH = "/.crosspoint/oscar-pull.json";
  const LS_KEY = "oscarPullBase";

  container.innerHTML = "";
  const wrap = document.createElement("div");
  wrap.style.cssText = "display:flex;flex-direction:column;gap:10px;max-width:520px";
  wrap.innerHTML = [
    '<h3 style="margin:0">Oscar Daily Pull</h3>',
    '<p style="margin:0">Downloads today\'s files listed in the feed catalog: the dashboard (<code>sleep.bmp</code>) and the briefing (<code>briefing.epub</code>).</p>',
    '<label>Feed base URL <input id="op-base" type="url" placeholder="https://example.org/feed" style="width:100%"></label>',
    '<div style="display:flex;gap:8px;flex-wrap:wrap">',
    '  <button id="op-save" type="button">Save base URL</button>',
    '  <button id="op-both" type="button">Pull today\'s files</button>',
    '  <button id="op-dash" type="button">Dashboard only</button>',
    '  <button id="op-epub" type="button">Briefing only</button>',
    "</div>",
    '<p id="op-status" style="margin:0;white-space:pre-wrap"></p>',
  ].join("");
  container.appendChild(wrap);

  const baseInput = wrap.querySelector("#op-base");
  const status = wrap.querySelector("#op-status");
  const say = (msg) => { status.textContent = msg; };

  function getBase() {
    return (baseInput.value || "").trim().replace(/\/+$/, "");
  }

  function encodeBase64Utf8(value) {
    const bytes = new TextEncoder().encode(value);
    let binary = "";
    for (const byte of bytes) binary += String.fromCharCode(byte);
    return btoa(binary);
  }

  // Pre-fill: localStorage first, then the shared on-device config file.
  const saved = localStorage.getItem(LS_KEY);
  if (saved) baseInput.value = saved;
  try {
    const res = await fetch("/download?path=" + encodeURIComponent(CONFIG_PATH));
    if (res.ok) {
      const cfg = await res.json();
      if (cfg && cfg.base) {
        baseInput.value = String(cfg.base);
        localStorage.setItem(LS_KEY, String(cfg.base));
      }
    }
  } catch (e) { /* config file may not exist yet; ignore */ }

  async function saveBase() {
    const base = getBase();
    if (!base) { say("Enter the feed base URL first."); return null; }
    localStorage.setItem(LS_KEY, base);
    try {
      const out = await api.writeFile(CONFIG_PATH, encodeBase64Utf8(JSON.stringify({ base })));
      if (out && out.ok) say("Saved. The on-reader Oscar Daily Pull screen will use this feed too.");
      else say("Saved in this browser; writing the device config returned: " + JSON.stringify(out));
    } catch (e) {
      say("Saved in this browser; device config write failed: " + e);
    }
    return base;
  }

  async function fetchCatalog() {
    const base = getBase();
    if (!base) { say("Enter the feed base URL first."); return null; }
    const r = await api.relay("GET", base + "/catalog.json");
    if (!r || r.status !== 200) {
      say("Catalog fetch failed: HTTP " + (r && r.status));
      return null;
    }
    try {
      const catalog = JSON.parse(r.body);
      if (!catalog || !Array.isArray(catalog.items)) throw new Error("no items array");
      return catalog.items;
    } catch (e) {
      say("Catalog parse failed: " + e);
      return null;
    }
  }

  async function pullItem(item) {
    say("Pulling " + item.id + " ...");
    try {
      const r = await api.fetchToSd(item.url, "/" + item.id);
      if (r && r.complete) {
        say("Done: " + item.id + " (" + r.bytes + " bytes, HTTP " + r.status + ")");
        return true;
      }
      say("Pull incomplete for " + item.id + ": " + JSON.stringify(r));
      return false;
    } catch (e) {
      say("Pull failed for " + item.id + ": " + e);
      return false;
    }
  }

  async function pullFiltered(wantId) {
    const items = await fetchCatalog();
    if (!items) return false;
    const chosen = wantId ? items.filter((i) => i.id === wantId) : items;
    if (!chosen.length) { say("Nothing in today's catalog matches."); return false; }
    let ok = true;
    for (const item of chosen) ok = (await pullItem(item)) && ok;
    if (ok) say("Today's files are on the reader.");
    return ok;
  }

  const pullToday = () => pullFiltered(null);

  wrap.querySelector("#op-save").addEventListener("click", saveBase);
  wrap.querySelector("#op-both").addEventListener("click", pullToday);
  wrap.querySelector("#op-dash").addEventListener("click", () => pullFiltered("sleep.bmp"));
  wrap.querySelector("#op-epub").addEventListener("click", () => pullFiltered("briefing.epub"));

  if (api.registerAction) api.registerAction("oscar-pull-today", pullToday);
});
