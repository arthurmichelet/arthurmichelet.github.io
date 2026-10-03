#!/usr/bin/env python3
"""Build the site.

1. Converts every notebooks/*.ipynb to notebooks/*.html (styled like the site).
2. Writes index.html listing everything in plots/ and notebooks/.

Usage:  python build.py
"""
import html
import re
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

# ── Edit these ────────────────────────────────────────────────────────────────
SITE_TITLE = "Figures & Notebooks"
SITE_SUBTITLE = "Interactive plots and analysis notebooks."
# ──────────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
PLOTS = ROOT / "plots"
NOTEBOOKS = ROOT / "notebooks"

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;700'
    '&family=Google+Sans+Flex&display=swap" rel="stylesheet">'
)

# Applied on top of nbconvert's JupyterLab theme.
NOTEBOOK_CSS = """
<style>
:root {
  --jp-layout-color0: #fafafa;
  --jp-layout-color1: #fafafa;
  --jp-ui-font-family: 'Google Sans Flex', sans-serif;
  --jp-content-font-family: 'Google Sans Flex', sans-serif;
  --jp-content-font-color1: #333333;
  --jp-border-color2: #e8e8e8;
  --jp-cell-editor-background: #f3f3f3;
}
html, body, body.jp-Notebook { background: #fafafa !important; color: #333333; }
.jp-RenderedHTMLCommon h1, .jp-RenderedHTMLCommon h2, .jp-RenderedHTMLCommon h3 {
  font-family: 'EB Garamond', serif; font-weight: 700;
}
.site-back {
  max-width: 1100px; margin: 0 auto; padding: 24px 24px 0;
  font-family: 'Google Sans Flex', sans-serif; font-size: 13px;
}
.site-back a { color: #333333; text-decoration: none; }
.site-back a:hover { color: #FF4D14; }
</style>
"""

BACK_LINK = '<div class="site-back"><a href="../index.html">&larr; All figures &amp; notebooks</a></div>'


def pretty(stem: str) -> str:
    s = re.sub(r"[-_]+", " ", stem).strip()
    return s[:1].upper() + s[1:]


def notebook_title(nb_path: Path) -> str:
    """First '# Heading' in the notebook, else the prettified file name."""
    nb = nbformat.read(nb_path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            for line in cell.source.splitlines():
                if line.startswith("# "):
                    return line[2:].strip()
    return pretty(nb_path.stem)


def convert_notebooks():
    exporter = HTMLExporter(template_name="lab")
    items = []
    for nb in sorted(NOTEBOOKS.glob("*.ipynb")):
        body, _ = exporter.from_filename(str(nb))
        body = body.replace("</head>", FONTS + NOTEBOOK_CSS + "</head>", 1)
        body = re.sub(r"(<body[^>]*>)", r"\1" + BACK_LINK, body, count=1)
        out = nb.with_suffix(".html")
        out.write_text(body, encoding="utf-8")
        items.append((notebook_title(nb), f"notebooks/{out.name}"))
    return items


def list_plots():
    # "-notitle" variants (made for LaTeX captions) are not listed.
    files = [p for p in sorted(PLOTS.glob("*.html")) if not p.stem.endswith("-notitle")]
    return [(pretty(p.stem), f"plots/{p.name}") for p in files]


def section(heading: str, pill: str, items) -> str:
    if not items:
        return f"<h2>{heading}</h2><p class='empty'>Nothing here yet.</p>"
    rows = "\n".join(
        f'<li><a href="{html.escape(href)}">{html.escape(title)}</a>'
        f'<span class="pill">{pill}</span></li>'
        for title, href in items
    )
    return f"<h2>{heading}</h2>\n<ul class='items'>\n{rows}\n</ul>"


def build_index(plots, notebooks):
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(SITE_TITLE)}</title>
{FONTS}
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<h1>{html.escape(SITE_TITLE)}</h1>
<p class="subtitle">{html.escape(SITE_SUBTITLE)}</p>
{section("Figures", "interactive", plots)}
{section("Notebooks", "notebook", notebooks)}
</main>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    notebooks = convert_notebooks()
    plots = list_plots()
    build_index(plots, notebooks)
    print(f"Built index.html: {len(plots)} figure(s), {len(notebooks)} notebook(s).")
