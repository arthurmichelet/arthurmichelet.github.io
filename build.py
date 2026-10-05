#!/usr/bin/env python3
"""Build the site.

Pages written to the site root:
  index.html          name + navigation
  info.html           paragraph, contact, interests      (text from content.py)
  publications.html   articles and conference papers     (text from content.py)
  explore.html        visualisations + notebooks         (from plots/ and notebooks/)

Also:
  notebooks/*.html    every notebooks/*.ipynb converted, in the site style
  plots/_png/*.html   a small viewer page for every plots/*.png (rebuilt each run)

A figure that exists as both x.html and x.png gets ONE row with two pills.
"-notitle" variants (made for LaTeX captions) are not listed.

Usage:  python3 build.py
"""
import html
import json
import re
import shutil
import uuid
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

import content

ROOT = Path(__file__).parent
PLOTS = ROOT / "plots"
PNG_VIEW = PLOTS / "_png"  # generated wrapper pages, rebuilt on every run
NOTEBOOKS = ROOT / "notebooks"
VIEW = ROOT / "view"       # generated viewer pages (retro look), rebuilt on every run

NAV = [("info", "info.html"), ("publications", "publications.html"), ("explore", "explore.html")]

# ORCID iD icon (green circle with white "iD"), shown next to the ORCID number.
ORCID_SVG = (
    '<svg class="orcid-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" '
    'width="18" height="18" aria-hidden="true">'
    '<path fill="#A6CE39" d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/>'
    '<path fill="#fff" d="M86.3 186.2H70.9V79.1h15.4v107.1zM108.9 79.1h41.6c39.6 0 57 28.3 57 53.6 0 '
    "27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7 0-21.5-13.7-39.7-43.7-39.7h-23.7"
    'v79.4zM88.7 56.8c0 5.5-4.5 10.1-10.1 10.1s-10.1-4.6-10.1-10.1c0-5.6 4.5-10.1 10.1-10.1s10.1 4.6 10.1 10.1z"/>'
    "</svg>"
)

# LinkedIn logo (the "in" square), shown next to the profile address.
LINKEDIN_SVG = (
    '<svg class="orcid-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
    'width="18" height="18" aria-hidden="true"><path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037'
    '-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 '
    '4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564'
    'v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729'
    'C24 .774 23.2 0 22.222 0h.003z"/></svg>'
)

# GitHub mark, in the text colour (so it follows light/dark mode).
GITHUB_SVG = (
    '<svg class="orcid-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" '
    'aria-hidden="true"><path fill="currentColor" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82'
    '-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084'
    '-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3'
    '-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98'
    '-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 '
    '3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 '
    '22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'
)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;700&family=IBM+Plex+Mono:wght@500;700'
    '&family=Google+Sans+Flex&display=swap" rel="stylesheet">'
)

# Applied on top of nbconvert's JupyterLab theme (the site header comes from style.css).
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
</style>
"""


# ── shared page pieces ───────────────────────────────────────────────────────
# Light/dark switch (retro look). The icon and word show the mode you switch TO (see theme-retro.css).
ICON_MOON = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/></svg>')
ICON_SUN = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
            '<path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>')
THEME_TOGGLE = (
    '<button type="button" class="theme-toggle" aria-label="switch between light and dark mode" '
    'onclick="toggleTheme()">'
    f'<span class="to-dark">{ICON_MOON}<span>dark</span></span>'
    f'<span class="to-light">{ICON_SUN}<span>light</span></span></button>'
)
# In <head>, before the page is painted: apply the saved choice (no flash). Without one, the CSS follows the system.
THEME_SCRIPT = (
    "<script>(function(){var d=document.documentElement;"
    "try{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')d.setAttribute('data-theme',t);}catch(e){}"
    "window.toggleTheme=function(){var dark=d.getAttribute('data-theme')?d.getAttribute('data-theme')==='dark':"
    "matchMedia('(prefers-color-scheme: dark)').matches;var n=dark?'light':'dark';d.setAttribute('data-theme',n);"
    "try{localStorage.setItem('theme',n);}catch(e){}};})();</script>"
)


def header(root="", current=None, wide=False, home=False):
    """Name on top, navigation underneath (on the home page: a single "start"
    button instead). `root` is the path back to the site root."""
    if home:
        nav = f'<a class="start" href="{root}info.html">start</a>'
    else:
        links = []
        for label, href in NAV:
            cls = ' class="current"' if label == current else ""
            links.append(f'<a href="{root}{href}"{cls}>{label}</a>')
        nav = f'<nav>{"".join(links)}</nav>'
    wide_cls = " wide" if wide else ""
    if getattr(content, "THEME", "classic") != "classic":
        # menu on the left, light/dark switch on the right. data-nosnippet: Google must not use these
        # button labels ("start", "dark", "light") as the text under the site name in its results.
        nav = f'<div class="nav-row" data-nosnippet>{nav}{THEME_TOGGLE}</div>'
    return (
        f'<header class="site-header{wide_cls}">'
        f'<a class="site-name" href="{root}index.html">{html.escape(content.NAME)}</a>'
        f"{nav}"
        f"</header>"
    )


def theme_link(root):
    """Extra stylesheet for the chosen look (content.THEME). "classic" = style.css alone."""
    theme = getattr(content, "THEME", "classic")
    if theme == "classic":
        return ""
    # the retro look follows the visitor's light/dark preference, unless they chose with the switch
    return ('<meta name="color-scheme" content="light dark">' + THEME_SCRIPT +
            f'<link rel="stylesheet" href="{root}theme-{theme}.css">')


def bg_preload(root):
    """Preload the textured background, only for looks that use it (classic)."""
    if getattr(content, "THEME", "classic") != "classic":
        return ""
    return (
        f'\n<link rel="preload" as="image" href="{root}assets/grain.webp">'
        f'\n<link rel="preload" as="image" href="{root}assets/bg.webp" media="(min-aspect-ratio: 1/1)">'
        f'\n<link rel="preload" as="image" href="{root}assets/bg-portrait.webp" media="(max-aspect-ratio: 1/1)">'
    )

def person_jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": content.NAME,
        "url": content.SITE_URL + "/",
        "jobTitle": "PhD candidate in history",
        "affiliation": {"@type": "CollegeOrUniversity", "name": "University of Lausanne"},
        "sameAs": [
            f"https://orcid.org/{content.ORCID}",
            "https://github.com/arthurmichelet",
            # add your UNIL profile, Google Scholar, Impresso page URLs here
        ],
    }
    if getattr(content, "LINKEDIN", None):
        data["sameAs"].append(content.LINKEDIN)
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


# Tab icon (favicon.ico also serves browsers and Google, which look for it at the site root).
# Root-absolute paths, so they work from every folder (view/, notebooks/).
FAVICON = (
    '<link rel="icon" href="/favicon.ico" sizes="48x48">'
    '<link rel="icon" type="image/png" href="/favicon.png" sizes="192x192">'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
)

def page(title, body, current=None, root="", body_class="site", main_class=""):
    main_attr = f' class="{main_class}"' if main_class else ""
    is_home = "home" in body_class.split()
    return f"""<!doctype html>
<html lang="en">
{person_jsonld() if is_home else ""}
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(content.SITE_DESCRIPTION)}">
{FONTS}{FAVICON}
<link rel="stylesheet" href="{root}style.css">
{theme_link(root)}{bg_preload(root)}
</head>
<body class="{body_class}">
{header(root, current, wide=("wide" in main_class.split()), home=is_home)}
<main data-page="{html.escape(current or "home")}"{main_attr}>
{body}
</main>
</body>
</html>
"""


def write(name, text):
    (ROOT / name).write_text(text, encoding="utf-8")


def pretty(stem: str) -> str:
    s = re.sub(r"[-_]+", " ", stem).strip()
    return s[:1].upper() + s[1:]


def md_links(text):
    """Escape text; [words](https://…) or [words](page.html) becomes a link."""
    return re.sub(r"\[([^\]]+)\]\(((?:https?://|[\w./#-])[^)\s]*)\)", r'<a href="\2">\1</a>', html.escape(text))


def rich(text):
    """Escape text; [words](https://...) -> link, **bold**, *italic*."""
    s = md_links(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def link_or_text(text, url):
    if url:
        return f'<a href="{html.escape(url)}">{html.escape(text)}</a>'
    return html.escape(text)


def list_section(heading, rows):
    """rows: [(title, [(pill label, href), ...])]. Title links to the first pill."""
    if not rows:
        return f"<h2>{heading}</h2><p class='empty'>nothing here yet.</p>"
    items = []
    for row in rows:
        title, pills = row["title"], row["pills"]
        pill_html = "".join(
            f'<a class="pill" href="{html.escape(href)}">{label}</a>' for label, href in pills
        )
        items.append(
            f'<li><a href="{html.escape(pills[0][1])}">{html.escape(title)}</a>'
            f'<span class="pills">{pill_html}</span></li>'
        )
    return f"<h2>{heading}</h2>\n<ul class='items'>\n" + "\n".join(items) + "\n</ul>"


# ── notebooks ────────────────────────────────────────────────────────────────
def notebook_title(nb_path: Path) -> str:
    """First '# Heading' in the notebook, else the prettified file name."""
    nb = nbformat.read(nb_path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            for line in cell.source.splitlines():
                if line.startswith("# "):
                    return line[2:].strip()
    return pretty(nb_path.stem)


PLOTLY_JS = "https://cdn.plot.ly/plotly-2.35.2.min.js"
try:  # use the same plotly.js version as the installed plotly, when available
    from plotly.offline import get_plotlyjs_version
    PLOTLY_JS = f"https://cdn.plot.ly/plotly-{get_plotlyjs_version()}.min.js"
except Exception:
    pass


def plotly_html(fig, include_js):
    """HTML for a Plotly figure saved in a notebook as JSON only."""
    uid = "plotly-" + uuid.uuid4().hex[:12]
    payload = lambda v: json.dumps(v).replace("</", "<\\/")
    loader = f'<script src="{PLOTLY_JS}" charset="utf-8"></script>' if include_js else ""
    return (
        f'{loader}<div id="{uid}" style="width:100%;height:{(fig.get("layout") or {}).get("height", 600)}px"></div>'
        f'<script>Plotly.newPlot("{uid}", {payload(fig.get("data", []))}, '
        f'{payload(fig.get("layout", {}))}, {{responsive: true}});</script>'
    )


MAX_TEXT_OUTPUT = 20_000   # characters; longer printed outputs are left out of the published notebook


def prepare_notebook(nb, name):
    """Make a notebook safe and complete for publishing.
    - Plotly figures saved only as JSON (no HTML) are turned into interactive HTML.
    - Very long printed outputs (typically a DataFrame dump) are replaced by a note.
    - Prints a warning when a figure's hover text contains titles or text columns."""
    first_plotly = True
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            data = out.get("data")
            if not data:
                continue
            fig_json = data.get("application/vnd.plotly.v1+json")
            if fig_json is not None and "text/html" not in data:
                data["text/html"] = plotly_html(fig_json, include_js=first_plotly)
                first_plotly = False
                for tr in fig_json.get("data", []):
                    tpl = str(tr.get("hovertemplate", "")) + str(tr.get("text", ""))
                    if re.search(r"title|text|content|headline", tpl, re.I):
                        print(f"  WARNING {name}, cell {i}: a figure's hover text includes "
                              "article titles/text. Check you may publish it.")
                        break
            plain = data.get("text/plain")
            if plain is not None and len("".join(plain)) > MAX_TEXT_OUTPUT and "text/html" not in data:
                data["text/plain"] = "[long output omitted from the published page]"
                print(f"  NOTE {name}, cell {i}: long printed output left out of the published page.")
            # drop the JSON blob: the HTML version replaces it (keeps the page small, avoids a warning)
            if "text/html" in data:
                data.pop("application/vnd.plotly.v1+json", None)
    return nb


def cards_mode():
    """The retro look shows figures and notebooks as cards that open a viewer page."""
    return getattr(content, "THEME", "classic") != "classic"


def slug(stem):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-") or "item"


def para_html(value):
    """A string or a list of strings -> one <p> per item ('' when empty). Supports rich()."""
    if not value:
        return ""
    if isinstance(value, str):
        value = [value]
    return "\n".join(f"<p>{rich(v)}</p>" for v in value)


def write_viewer(stem, title, src, info, open_label):
    """A page in the site style: the figure or notebook in a frame, with the description
    and methodology on the right. `src` is the file shown (relative to the site root)."""
    VIEW.mkdir(exist_ok=True)
    about = info.get("about") or info.get("description")
    sections = ""
    if about:
        sections += f"<h2>description</h2>\n{para_html(about)}\n"
    if info.get("methodology"):
        sections += f"<h2>methodology</h2>\n{para_html(info['methodology'])}\n"
    t = html.escape(title)
    # Plotly exports have a fixed pixel size: read it so the viewer can scale the frame to fit
    size = ""
    f = ROOT / src
    if f.suffix == ".html" and f.exists():
        m = re.search(r'style="height:\s*(\d+)px;\s*width:\s*(\d+)px;?"', f.read_text(encoding="utf-8", errors="ignore"))
        if m:
            size = f' data-h="{m.group(1)}" data-w="{m.group(2)}"'
    body = (
        '<div class="viewer">\n'
        f'<div class="viewer-frame"{size}><iframe src="../{html.escape(src)}" title="{t}" loading="lazy"></iframe></div>\n'
        '<aside class="viewer-side">\n'
        f'<h1 class="viewer-title">{t}</h1>\n{sections}'
        f'<p class="viewer-links"><a class="pill" href="../{html.escape(src)}">{open_label}</a> '
        '<a class="pill" href="../explore.html">back to explore</a></p>\n'
        '<p class="viewer-licence">&copy; Arthur Michelet &middot; <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a>. '
        'The article openings shown remain the property of their publishers.</p>\n'
        "</aside>\n</div>\n"
        "<script>(function(){document.querySelectorAll('.viewer-frame[data-w]').forEach(function(f){"
        "var w=+f.dataset.w,h=+f.dataset.h,i=f.querySelector('iframe');i.style.width=w+'px';i.style.height=h+'px';"
        "function fit(){var k=Math.min(1,f.clientWidth/w);i.style.transform='scale('+k+')';f.style.height=(h*k)+'px';}"
        "fit();addEventListener('resize',fit);if(window.ResizeObserver)new ResizeObserver(fit).observe(f);});})();</script>"
    )
    out = VIEW / f"{slug(stem)}.html"
    out.write_text(page(f"{title} \u00b7 {content.NAME}", body, current="explore", root="../", main_class="wide viewer-page"), encoding="utf-8")
    return f"view/{out.name}"


def convert_notebooks():
    """Returns rows (dicts: title, pills, description, preview, kind)."""
    cards = cards_mode()
    exporter = HTMLExporter(template_name="lab")
    if cards:   # shown inside a viewer page: no site header, just the notebook
        head_extra = FONTS + FAVICON + NOTEBOOK_CSS
    else:
        head_extra = FONTS + FAVICON + '<link rel="stylesheet" href="../style.css">' + NOTEBOOK_CSS
    if cards:   # headings in the theme's monospaced face
        head_extra += ("<style>.jp-RenderedHTMLCommon h1, .jp-RenderedHTMLCommon h2, "
                       ".jp-RenderedHTMLCommon h3 { font-family: 'IBM Plex Mono', ui-monospace, Menlo, monospace; }</style>")
    site_header = "" if cards else header("../", current="explore", wide=True)
    if cards and VIEW.exists():
        shutil.rmtree(VIEW)
    rows = []
    for nb in sorted(NOTEBOOKS.glob("*.ipynb")):
        if explore_info(nb.stem).get("hidden"):   # kept in notebooks/ but not published (see content.EXPLORE)
            continue
        node = prepare_notebook(nbformat.read(str(nb), as_version=4), nb.name)
        body, _ = exporter.from_notebook_node(node)
        body = body.replace("</head>", head_extra + "</head>", 1)
        if site_header:
            body = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + site_header, body, count=1)
        out = nb.with_suffix(".html")
        out.write_text(body, encoding="utf-8")
        info = explore_info(nb.stem)
        title = info.get("title") or notebook_title(nb)
        href = f"notebooks/{out.name}"
        if cards:
            href = write_viewer(nb.stem, title, href, info, "open full page")
        rows.append({
            "title": title,
            "pills": [("notebook", href)],
            "description": info.get("description", ""),
            "preview": find_preview(NOTEBOOKS, nb.stem),
            "kind": "notebook",
        })
    return rows


# ── figures ──────────────────────────────────────────────────────────────────
def write_png_pages():
    """A PNG opened on its own sits on the browser's default background, so
    each one gets a small page in the site style. Returns {stem: page path}."""
    if PNG_VIEW.exists():
        shutil.rmtree(PNG_VIEW)  # generated only; drops pages of deleted PNGs
    pages = {}
    for png in sorted(PLOTS.glob("*.png")):
        if png.stem.endswith(("-notitle", "-preview")):
            continue
        PNG_VIEW.mkdir(exist_ok=True)
        title = html.escape(pretty(png.stem))
        src = html.escape(png.name)
        body = (
            f"<h1>{title}</h1>\n"
            f'<img class="figure" src="../{src}" alt="{title}">\n'
            f'<p class="download"><a href="../{src}" download>download png</a></p>'
        )
        out = PNG_VIEW / f"{png.stem}.html"
        out.write_text(
            page(pretty(png.stem), body, current="explore", root="../../", main_class="wide"),
            encoding="utf-8",
        )
        pages[png.stem] = f"plots/_png/{out.name}"
    return pages


PREVIEW_EXTS = (".webp", ".png", ".jpg", ".jpeg")


def find_preview(folder, stem):
    """Preview image for a card: <stem>-preview.(webp|png|jpg), else <stem>.png if it exists."""
    for ext in PREVIEW_EXTS:
        p = folder / f"{stem}-preview{ext}"
        if p.exists():
            return f"{folder.name}/{p.name}"
    p = folder / f"{stem}.png"
    return f"{folder.name}/{p.name}" if p.exists() else None


def explore_info(stem):
    """Optional title / description from content.EXPLORE (keyed by file name without extension)."""
    return getattr(content, "EXPLORE", {}).get(stem, {})


def list_plots():
    """One row per figure name; pills for each format that exists."""
    png_pages = write_png_pages()
    stems = {}
    for p in PLOTS.glob("*.html"):
        if not p.stem.endswith(("-notitle", "-preview")):
            stems.setdefault(p.stem, {})["interactive"] = f"plots/{p.name}"
    for stem, pg in png_pages.items():
        stems.setdefault(stem, {})["png"] = pg
    rows = []
    for stem in sorted(stems):
        formats = stems[stem]
        info = explore_info(stem)
        if info.get("hidden"):   # kept in plots/ but not listed (set "hidden": True in content.EXPLORE)
            continue
        title = info.get("title") or pretty(stem)
        if cards_mode() and "interactive" in formats:
            formats["interactive"] = write_viewer(stem, title, formats["interactive"], info, "open full page")
        pills = [(label, formats[label]) for label in ("interactive", "png") if label in formats]
        rows.append({
            "title": title,
            "pills": pills,
            "description": info.get("description", ""),
            "preview": find_preview(PLOTS, stem),
            "kind": "plot",
        })
    return rows


# ── pages ────────────────────────────────────────────────────────────────────
def build_home():
    write("index.html", page(content.NAME, "", body_class="site home"))


# ── research interests as stacked "bricks" (retro look) ─────────────────────────
# Each brick: a soft, thick isometric slab (a rounded diamond, extruded) with its name + a box of topics, joined by a curved line.
# Grey until hovered; then slab, box and line take the brick's colour (top face = box colour).
BRICK_COLOURS = [   # (top face, side band) -- the site palette; the box takes the top colour
    ("#FF8A66", "#E5532B"),
    ("#40CED3", "#2D9094"),
    ("#005778", "#003C53"),
]
BRICK_COLOURS_ORIGINAL = [   # (top face, side band) -- the site palette; the box takes the top colour
    ("#FF8A66", "#E5532B"),
    ("#5DCAA5", "#1D9E75"),
    ("#1D9E75", "#0B6A50"),
]
BRICK_LAYOUT = [    # (box offset in px: + = lower than the slab's side, gap between box and slab in px)
    (-18, 70),
    (36, 52),
    (22, 84),
]


def _rounded(points, radii):
    """Closed SVG path through `points`, each corner rounded with its own radius (quadratic curves).
    Also returns the path's min and max x."""
    import math
    n = len(points)
    d, xs = [], []
    for k in range(n):
        p, prev, nxt = points[k], points[k - 1], points[(k + 1) % n]
        def toward(q):
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy)
            t = min(radii[k], L / 2) / L
            return (p[0] + dx * t, p[1] + dy * t)
        a, c = toward(prev), toward(nxt)
        d.append(("M" if k == 0 else "L") + f"{a[0]:.1f},{a[1]:.1f} Q{p[0]},{p[1]} {c[0]:.1f},{c[1]:.1f}")
        for s in range(11):                      # sample the curve for its horizontal extent
            u = s / 10
            xs.append((1 - u) ** 2 * a[0] + 2 * u * (1 - u) * p[0] + u * u * c[0])
    return " ".join(d) + " Z", min(xs), max(xs)


def slab_svg(label):
    """A rounded diamond (top face) extruded downwards; one colour for the whole side band,
    the first word of the name on its left half and the second on its right half."""
    words = label.upper().split()
    half = (len(words) + 1) // 2
    left_word, right_word = " ".join(words[:half]), " ".join(words[half:])
    t, y_tip = 42, 92                                   # thickness; y of the left/right tips
    diamond = [(200, 12), (388, y_tip), (200, 172), (12, y_tip)]
    radii = [66, 54, 66, 54]
    top, xmin, xmax = _rounded(diamond, radii)
    low, _, _ = _rounded([(x, y + t) for x, y in diamond], radii)
    rect = f'<rect x="{xmin:.1f}" y="{y_tip}" width="{xmax - xmin:.1f}" height="{t}"/>'
    right_text = (f'<text transform="translate(200 {172}) skewY(-23.35)" x="90" y="{t - 14}">{html.escape(right_word)}</text>'
                  if right_word else "")
    return (
        '<svg class="brick-slab" viewBox="0 0 400 230" aria-hidden="true" focusable="false">'
        f'<g class="outline"><path d="{low}"/>{rect}<path d="{top}"/></g>'          # thick stroke = outer outline
        f'<g class="side shape"><path d="{low}"/>{rect}<path d="{top}"/></g>'        # side colour covers the inner half
        f'<path class="top shape" d="{top}"/>'
        f'<path class="bevel" d="{top}" transform="translate(200 92) scale(.95 .9) translate(-200 -92)"/>'
        f'<text transform="translate(12 {y_tip}) skewY(23.35)" x="92" y="{t - 14}">{html.escape(left_word)}</text>'
        f"{right_text}</svg>"
    )


def connector_svg(dy, gap):
    """Curved line from the box (left end, at its centre) to the slab's side (right end).
    dy > 0: the box sits lower than the slab's side, so the line climbs."""
    pad = 4
    height = abs(dy) + 2 * pad
    y_box = (max(dy, 0)) + pad
    y_tip = y_box - dy
    return (
        f'<svg class="brick-line" width="{gap}" height="{height}" viewBox="0 0 {gap} {height}" '
        f'style="top:calc(50% - {y_box}px)" aria-hidden="true" focusable="false">'
        f'<path d="M0,{y_box} C{gap * .55:.0f},{y_box} {gap * .45:.0f},{y_tip} {gap},{y_tip}"/></svg>'
    )

def clean_urls():
    """Make links to the site's own pages extension-less: info.html -> info, index.html -> ./"""
    pat = re.compile(r'href="((?:\.\./)?(?:view/)?)([^"/#?]+)\.html((?:#[^"]*)?)"')
    def fix(m):
        base, name, frag = m.groups()
        if name == "index":
            return f'href="{base or "./"}{frag}"'
        return f'href="{base}{name}{frag}"'
    pages = [ROOT / n for n in ("index.html", "info.html", "publications.html", "explore.html")]
    for f in pages + sorted(VIEW.glob("*.html")):
        f.write_text(pat.sub(fix, f.read_text(encoding="utf-8")), encoding="utf-8")

def interests_html(interests):
    """A flat list of strings -> the plain boxed list. A list of (name, [topics]) -> bricks."""
    if interests and isinstance(interests[0], str):
        items = "\n".join(f"<li>{html.escape(i)}</li>" for i in interests)
        return f"<ul class='items'>\n{items}\n</ul>"
    bricks = []
    for n, (name, topics) in enumerate(interests):
        where = "left" if n % 2 == 0 else "right"
        top, band = BRICK_COLOURS[n % len(BRICK_COLOURS)]
        dy, gap = BRICK_LAYOUT[n % len(BRICK_LAYOUT)]
        chips = "".join(f"<li>{html.escape(t)}</li>" for t in topics)
        bricks.append(
            f'<section class="brick brick-{where}" style="z-index:{len(interests) - n};'
            f'--top:{top};--side:{band};--dy:{dy}px;--gap:{gap}px">'
            f'<h3 class="sr-only">{html.escape(name)}</h3>'
            f"{slab_svg(name)}"
            f'<div class="brick-side">{connector_svg(dy, gap)}<ul class="brick-box">{chips}</ul></div>'
            "</section>"
        )
    return '<div class="bricks">' + "".join(bricks) + "</div>"


def build_info():
    rows = []
    for label, text, url in content.CONTACT:
        if label.lower() == "github" and url:   # the GitHub row gets its logo
            cell = f'<a class="orcid" href="{html.escape(url)}">{GITHUB_SVG}{html.escape(text)}</a>'
        else:
            cell = link_or_text(text, url)
        rows.append(f"<dt>{html.escape(label)}</dt><dd>{cell}</dd>")
    linkedin = getattr(content, "LINKEDIN", None)
    if linkedin:   # above the ORCID row
        shown = re.sub(r"^https?://(www\.)?", "", linkedin).rstrip("/")
        rows.append(
            f'<dt>linkedin</dt><dd><a class="orcid" href="{html.escape(linkedin)}">{LINKEDIN_SVG}'
            f"{html.escape(shown)}</a></dd>"
        )
    if content.ORCID:
        url = f"https://orcid.org/{content.ORCID}"
        rows.append(
            f'<dt>orcid</dt><dd><a class="orcid" href="{url}">{ORCID_SVG}'
            f"{html.escape(content.ORCID)}</a></dd>"
        )
    contact = "\n".join(rows)

    awards = []
    for g in content.GRANTS_AND_AWARDS:
        date = (g.get("date") or "").replace(" ", " ")  # keep "May 2026" on one line
        meta = html.escape(" · ".join(x for x in (g.get("issuer"), date) if x))
        meta_html = f'<span class="meta">{meta}</span>' if meta else ""
        label = html.escape(g["type"])   # a "url" turns the pill into a link (e.g. the announcement)
        award_pill = (f'<a class="pill" href="{html.escape(g["url"])}">{label}</a>' if g.get("url")
                      else f'<span class="pill">{label}</span>')
        awards.append(
            f'<li><span class="entry"><span class="entry-title">{html.escape(g["title"])}</span>'
            f"{meta_html}</span>"
            f'<span class="pills">{award_pill}</span></li>'
        )
    awards_html = (
        "<h2>grants and awards</h2>\n<ul class='items'>\n" + "\n".join(awards) + "\n</ul>\n"
        if awards
        else ""
    )

    interests = interests_html(content.INTERESTS)
    body = (
        '<h1 class="sr-only">info</h1>\n'
        f"<p>{md_links(content.INFO)}</p>\n"
        f"<h2>get in touch</h2>\n<dl class='contact'>\n{contact}\n</dl>\n"
        f"{awards_html}"
        f"<h2>research interests</h2>\n{interests}"
    )
    write("info.html", page(f"info · {content.NAME}", body, current="info"))


def fmt(text):
    """Escape text; *word* becomes italics (used for titles of books and proceedings)."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(text))


def chicago_ref(e):
    """One reference in Chicago style (notes-bibliography), from the entry's fields:
    authors. “Title.” venue. url        (a notebook/software: *Title*. venue. url)
    `venue` carries everything after the title (container, pages, publisher, year), written by hand."""
    parts = []
    if e.get("authors"):
        a = e["authors"].rstrip(".")
        parts.append(fmt(a) + ".")
    t = e["title"]
    if e["type"] == "notebook":
        parts.append(f"<em>{html.escape(t)}</em>.")
    else:
        end = "" if t.rstrip()[-1] in "?!." else "."
        parts.append(f"\u201c{html.escape(t)}{end}\u201d")
    venue = e.get("venue") or (str(e["year"]) if e.get("year") else "")
    if venue:
        v = fmt(venue)
        parts.append(v if v.endswith((".", ")")) else v + ".")
    if e.get("url"):
        u = html.escape(e["url"])
        parts.append(f'<a class="ref-url" href="{u}">{u}</a>')
    return " ".join(parts)


def pub_section(heading, entries):
    """One list of publications, newest first (entries without a year go last)."""
    entries = sorted(entries, key=lambda e: e.get("year") or 0, reverse=True)
    items = []
    for e in entries:
        label = html.escape(e["type"])
        pill = (f'<a class="pill" href="{html.escape(e["url"])}">{label}</a>' if e.get("url")
                else f'<span class="pill">{label}</span>')
        items.append(
            f'<li><span class="entry"><span class="ref">{chicago_ref(e)}</span></span>'
            f'<span class="pills">{pill}</span></li>'
        )
    return f"<h2>{heading}</h2>\n<ul class='items'>\n" + "\n".join(items) + "\n</ul>"


def build_publications():
    body = (
        '<h1 class="sr-only">publications</h1>\n'
        + pub_section("articles and conference papers", content.PUBLICATIONS)
        + "\n"
        + pub_section("published notebooks", content.PUBLISHED_NOTEBOOKS)
    )
    write("publications.html", page(f"publications · {content.NAME}", body, current="publications"))


ICON_PLOT = (
    '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linejoin="round" aria-hidden="true"><path d="M3 22V4M3 22h20"/><path d="M6 17l5-6 4 3 7-9"/></svg>'
)
ICON_NOTEBOOK = (
    '<svg width="26" height="26" viewBox="0 0 26 26" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3" width="16" height="20"/>'
    '<path d="M9 8h8M9 12h8M9 16h5"/></svg>'
)


PILL_LABELS = {"interactive": "check the interactive plot", "notebook": "try the notebook"}


def card_section(heading, rows):
    """The retro look: one card per figure or notebook (title, description, preview, links)."""
    if not rows:
        return f"<h2>{heading}</h2><p class='empty'>nothing here yet.</p>"
    cards = []
    for row in rows:
        first = html.escape(row["pills"][0][1])
        icon = ICON_NOTEBOOK if row["kind"] == "notebook" else ICON_PLOT
        text = f'<p class="card-text">{html.escape(row["description"])}</p>' if row["description"] else ""
        title = html.escape(row["title"])
        preview = (
            f'<a class="card-preview" href="{first}" tabindex="-1" aria-hidden="true">'
            f'<img src="{html.escape(row["preview"])}" alt="" loading="lazy"></a>'
            if row["preview"] else ""
        )
        links = "".join(
            f'<a class="pill" href="{html.escape(href)}">{PILL_LABELS.get(label, label)}</a>'
            for label, href in row["pills"]
        )
        cards.append(
            f'<article class="card">'
            f'<span class="card-icon">{icon}</span>'
            f'<h3 class="card-title"><a href="{first}">{title}</a></h3>'
            f"{text}{preview}"
            f'<div class="card-links">{links}</div>'
            f"</article>"
        )
    return f"<h2>{heading}</h2>\n<div class='cards'>\n" + "\n".join(cards) + "\n</div>"


def build_explore(plots, notebooks):
    cards = getattr(content, "THEME", "classic") != "classic"
    section = card_section if cards else list_section
    body = (
        '<h1 class="sr-only">explore</h1>\n'
        + section("visualisations", plots)
        + "\n"
        + section("notebooks", notebooks)
    )
    write("explore.html", page(f"explore \u00b7 {content.NAME}", body, current="explore",
                               main_class="wide bare" if cards else ""))

if __name__ == "__main__":
    notebooks = convert_notebooks()
    plots = list_plots()
    build_home()
    build_info()
    build_publications()
    build_explore(plots, notebooks)

    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {content.SITE_URL}/sitemap.xml\n")
    pages = ["", "info", "publications", "explore"] + [f"view/{p.stem}" for p in sorted(VIEW.glob("*.html"))]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{content.SITE_URL}/{p}</loc></url>\n" for p in pages)
          + "</urlset>\n")

    clean_urls()
    print(f"Built 4 pages: {len(plots)} visualisation(s), {len(notebooks)} notebook(s).")
