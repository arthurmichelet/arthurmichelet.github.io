#!/usr/bin/env python3
"""Make the tile pictures of the companion page, from your Plotly figures.

For every <name>.html in COMPANION_SRC (content.py) this makes two pictures next to it:
  <name>-preview.webp        light version
  <name>-preview-dark.webp   dark version (shown when the page is in dark mode)
A picture that already exists is kept (delete it to redo it). Then run build.py.

One-time setup:  pip3 install playwright pillow && python3 -m playwright install chromium
Usage:           python3 make_companion_previews.py            (uses COMPANION_SRC)
                 python3 make_companion_previews.py <folder>   (another folder)
"""
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

if len(sys.argv) > 1:
    SRC = Path(sys.argv[1]).expanduser()
else:
    import content
    SRC = Path(content.COMPANION_SRC).expanduser()

# dark colours: keep in sync with COMPANION_THEME_JS in build.py (tiles sit on the card colour, --raised)
DARK = {"bg": "#06201a", "text": "#d9f7ec", "grid": "rgba(192,243,226,.16)"}
DARK_JS = """(c) => {
  const gd = document.querySelector('.plotly-graph-div');
  const u = {paper_bgcolor: c.bg, plot_bgcolor: c.bg, 'font.color': c.text, 'legend.font.color': c.text};
  Object.keys(gd._fullLayout).forEach(k => {
    if (/^[xy]axis\\d*$/.test(k)) { u[k + '.gridcolor'] = c.grid; u[k + '.zerolinecolor'] = c.grid; u[k + '.linecolor'] = c.grid; }
  });
  (gd.layout.annotations || []).forEach((a, i) => { u['annotations[' + i + '].font.color'] = c.text; });
  document.documentElement.style.background = document.body.style.background = c.bg;
  return Plotly.relayout(gd, u);
}"""


def save(png_bytes, target):
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img.thumbnail((900, 900))
    img.save(target, "WEBP", quality=82, method=6)
    print("made", target.name)


figures = [p for p in sorted(SRC.glob("*.html")) if not p.stem.endswith(("-preview", "-preview-dark"))]
jobs = [(p, dark) for p in figures for dark in (False, True)
        if not (SRC / f"{p.stem}-preview{'-dark' if dark else ''}.webp").exists()]
if not jobs:
    print("All figures already have their pictures.")
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for html_file, dark in jobs:
        page = browser.new_page(viewport={"width": 1300, "height": 900}, device_scale_factor=1.5)
        page.goto(html_file.resolve().as_uri())
        page.wait_for_function("() => { const g = document.querySelector('.plotly-graph-div'); return g && g._fullLayout; }")
        page.wait_for_timeout(1500)                       # let the figure draw
        if dark:
            page.evaluate(DARK_JS, DARK)
            page.wait_for_timeout(800)
        chart = page.query_selector(".plotly-graph-div")
        save((chart or page).screenshot(), SRC / f"{html_file.stem}-preview{'-dark' if dark else ''}.webp")
        page.close()
    browser.close()
