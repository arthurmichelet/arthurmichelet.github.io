#!/usr/bin/env python3
"""Make the preview images shown on the explore cards, from your interactive figures.

For every plots/<name>.html without a plots/<name>-preview.webp, this opens the figure in
a headless browser, takes a picture of the Plotly chart and saves it as <name>-preview.webp.
Existing previews are kept (delete one to redo it). Then run build.py.

One-time setup:  pip3 install playwright pillow && python3 -m playwright install chromium
Usage:           python3 make_previews.py
"""
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

PLOTS = Path(__file__).parent / "plots"
todo = [p for p in sorted(PLOTS.glob("*.html"))
        if not p.stem.endswith(("-notitle", "-preview")) and not (PLOTS / f"{p.stem}-preview.webp").exists()]

if not todo:
    print("All figures already have a preview.")
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for html_file in todo:
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(html_file.resolve().as_uri())
        page.wait_for_timeout(6000)                      # let the (big) figure draw
        chart = page.query_selector(".js-plotly-plot")
        target = PLOTS / f"{html_file.stem}-preview.webp"
        tmp = PLOTS / f"{html_file.stem}-preview.tmp.png"
        (chart or page).screenshot(path=str(tmp))
        img = Image.open(tmp).convert("RGB")
        img.thumbnail((900, 900))
        img.save(target, "WEBP", quality=82, method=6)
        tmp.unlink()
        page.close()
        print("made", target.name)
    browser.close()
