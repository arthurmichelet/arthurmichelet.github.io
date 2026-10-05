"""Everything you will want to edit on the site lives here.

After changing anything, run:  python3 build.py
"""

NAME = "Arthur Michelet"

# Look of the site: "retro" (theme-retro.css, on top of style.css) or "classic" (style.css only).
THEME = "retro"

# ── info page ────────────────────────────────────────────────────────────────
# In the paragraph below, [words](https://link) makes a link.
INFO = (
    "I am a PhD candidate at the University of Lausanne, Switzerland, working on the relationship "
    "between media, news, and organised business interests in the twentieth century. I use qualitative archive research "
    "and apply computational techniques to digitised media sources to study the news coverage "
    "and public relations of the Swiss Bankers Association (1910\u20131990). My PhD is part of the "
    "[Impresso \u2013 Media Monitoring of the Past](https://impresso-project.ch/) project, funded by the "
    "Swiss National Science Foundation and the Luxembourg Research Fund. I also teach "
    "at EPFL, Lausanne, and am a [Visiting Research Fellow](https://www.sas.ac.uk/people/arthur-michelet) "
    "at the Digital Humanities Research Hub (School of Advanced Study), in London UK."
)

# (label, text, link or None)
CONTACT = [
    ("email", "arthur.michelet@unil.ch", "mailto:arthur.michelet@unil.ch"),
    ("affiliation", "History Department, Faculty of Arts, University of Lausanne", None),
    ("office", "Anthropole 5190, 1015 Lausanne, Switzerland", None),
    ("github", "github.com/arthurmichelet", "https://github.com/arthurmichelet"),
]

# Shown as a contact row, with the LinkedIn logo, just above ORCID. Set to None to hide it.
LINKEDIN = "https://www.linkedin.com/in/arthur-michelet-aa4326248/"

# Shown as the last contact row, with the ORCID logo. Set to None to hide it.
ORCID = "0009-0006-4593-6402"

# "grants and awards" section on the info page (shown in this order).
# type: shown in the pill ("grant", "award", ...).
GRANTS_AND_AWARDS = [
    {
        "type": "award",
        "title": "Young Research Award",
        "issuer": "Humanistica, Francophone Association for Digital Humanities",
        "date": "May 2026",
    },
    {
        "type": "grant",
        "title": "Mobility Grant",
        "issuer": "Swiss National Science Foundation",
        "date": "September 2025",
    },
]

# Research interests, shown as three stacked bricks (name, then its topics).
# (A plain list of strings also works: it is shown as a simple boxed list.)
INTERESTS = [
    ("economic history", [
        "banks and credit",
        "offshore finance and euromarkets",
        "business associations",
        "multinational banks",
    ]),
    ("digital humanities", [
        "computational text analysis",
        "text embeddings",
        "language models for historical sources",
        "data visualisation",
        "NLP and machine learning",
    ]),
    ("media studies", [
        "public relations, propaganda, and marketing",
        "mass media ecosystems",
        "making and structures of news",
        "economic and financial news",
    ]),
]

# ── publications page ────────────────────────────────────────────────────────
# References are shown in Chicago style (notes-bibliography):
#   Authors. “Title.” venue. https://url
# Write "authors" in Chicago order: "Last, First, and First Last" (first author inverted).
# "venue" is everything that follows the title (container, editors, pages, publisher, year),
# written by hand; put *asterisks* around anything that should be italic. The "year" field only
# sorts the list. A notebook is shown as: Authors. *Title*. venue.
# Every field except "title" and "type" is optional. type: shown in the pill.
# url: the DOI / link, printed at the end of the reference; None = no link (and a coloured pill).

# Section "articles and conference papers"
PUBLICATIONS = [
    {
        "type": "conference paper",
        "year": 2026,
        "authors": "Ruppen Coutaz, Rapha\u00eblle, Martin Grandjean, Arthur Michelet, and Marten D\u00fcring (eds)",
        "title": "Radio and Newspapers: What Intersections for Media History?",
        "venue": "2026",   # TODO: add the volume / proceedings if there is one
        "url": "https://doi.org/10.5281/zenodo.20813962",
    },
    {
        "type": "conference paper",
        "year": 2026,
        "authors": "Michelet, Arthur, and Martin Grandjean",
        "title": "Les embeddings, nouvel outil d\u2019une histoire num\u00e9rique des grands corpus de presse?",
        "venue": "In *Actes de la Conf\u00e9rence Humanistica*, vol. 4, 175\u201381. 2026",   # TODO: add the publisher if you want it
        "url": "https://anthology.ach.org/volumes/vol0004/les-embeddings-nouvel-outil-d-une-histoire-num-rique-des/",
    },
    {
        "type": "book chapter",
        "year": 2026,
        "authors": "Michelet, Arthur",
        "title": "Construire l\u2019information bancaire\u00a0: la publicit\u00e9 de l\u2019Association suisse des banquiers et les m\u00e9dias de masse (1948\u20131975)",
        "venue": "In *L\u2019influence et ses pratiques*, edited by Yves Cohen, Irene Di Jorio, and Hugo Souza de Cursi. Presses universitaires du Septentrion, 2026. (Upcoming)",   # TODO: add the place (Chicago: Place: Publisher, year) and the page range
        "url": None,
    },
    {
        "type": "conference paper",
        "year": 2025,
        "authors": "Michelet, Arthur",
        "title": "The Transmedia Publicity of Swiss Banks: Public Relations Strategies and Mass Media Coverage (1960\u20131977)",
        "venue": "In *Transmedia History: Circulations, Reconfigurations and New Methodologies*, 67\u201371. 2025",
        "url": "https://doi.org/10.5281/zenodo.15046947",
    },
]

# Section "published notebooks"
PUBLISHED_NOTEBOOKS = [
    {
        "type": "notebook",
        "year": 2026,
        "authors": "Michelet, Arthur, and Martin Grandjean",
        "title": "Comparing Corpora Using Embeddings",
        "venue": "Computer software. Zenodo, 2026",
        "url": "https://doi.org/10.5281/zenodo.19006514",
    },
]

# ── explore page ─────────────────────────────────────────────────────────────
# Optional title and description (the "snippet" shown on the card) for each figure or
# notebook, keyed by its file name WITHOUT extension. Without an entry, the card shows
# the prettified file name and no description. Optional keys: "about" (longer text for the
# viewer page, instead of "description") and "methodology" (a string or a list of strings).
# Preview image on the card: plots/<name>-preview.webp (or .png/.jpg); if there is none,
# plots/<name>.png is used when it exists. Notebooks: notebooks/<name>-preview.webp.
EXPLORE = {
    "articles-and-contentlength-peryear-bynewspaper-stacked": {
        "hidden": True,   # not listed on the explore page (set to False or delete the line to show it again)
        "title": "Volume vs. length of coverage, per newspaper (1912\u20131940)",
        "description": "Articles and total characters per year for the ten largest newspapers; the other 69 are grouped as \u201cOther\u201d.",
        # TODO: check this methodology, add the search query and any filters you used.
        "methodology": [
            "Articles retrieved from the Swiss press archives and counted per year and per newspaper.",
            "The ten newspapers with the most articles are shown individually; the remaining 69 are aggregated as \u201cOther\u201d.",
            "Top panel: number of articles. Bottom panel: total number of characters in those articles.",
        ],
    },
    "umap-labelled-map": {   # plots/umap-labelled-map.html, exported by the notebook
        "title": "UMAP of SBA coverage, 1940\u20131999",
        "description": "Articles on the Swiss Bankers Association mapped by similarity and coloured by year, with clusters named by an LLM.",
        "about": (   # longer text for the viewer page
            "Articles mentioning the Swiss Bankers Association (SBA), mapped by semantic similarity and coloured "
            "by year, with clusters labelled by LLM. Every dot is an article; its colour is the year; clusters "
            "indicate semantic proximity. Zoom in and hover over articles to explore the map."
        ),
        # Text supports [link](url), **bold** and *italic*; each item is shown as a paragraph.
        "methodology": [
            "Corpus comprises all articles mentioning the SBA in *Neue Z\u00fcrcher Zeitung*, *Der Bund*, "
            "*Journal de Gen\u00e8ve*, and *Gazette de Lausanne*, published between 1940\u20131999.",
            "Each article is first turned into vectors (256 dimensions) using the m-GTE embedding model. It is then "
            "projected to two dimensions using UMAP (cosine distance, normalised vectors); the coordinates on X and Y "
            "represent those two dimensions. Learn more about embeddings and UMAPs in [this paper]"
            "(https://anthology.ach.org/volumes/vol0004/les-embeddings-nouvel-outil-d-une-histoire-num-rique-des/).",
            "Clusters are identified by running HDBSCAN on the UMAP coordinates. An LLM (glm-5.3-flash) is then used "
            "to name each cluster from its 30 most representative articles.",
            "The labels were manually checked against the articles of each cluster.",
            # the notebook's viewer page sits in the same folder (view/), so a bare file name works anywhere
            "Check out the full pipeline [here](embeddings-to-labelled-maps.html).",
        ],
    },
    "sba-umap-labelled-1 copy": {
        "hidden": True,   # OLD export: its hover boxes show article titles. Never publish it; delete the file.
    },
    "totalhits-peryear-1912-1940-agg-baseONE": {
        "hidden": True,   # not listed on the explore page (set to False or delete the line to show it again)
        "title": "Articles per year across all newspapers (1912\u20131940)",
        "description": "Yearly number of articles in Swiss newspapers: total, official press releases, the annual assembly (\u201cBankiertag\u201d) and other.",
        # TODO: check this methodology, add the search query used.
        "methodology": [
            "Documents retrieved via e-newspaperarchives.ch and Impresso, across all newspapers published in Switzerland.",
            "Articles are counted per year and split into the series shown: total, official press release, annual assembly (\u201cBankiertag\u201d) and other.",
        ],
    },
    # Notebook entry (key = notebooks/<name>.ipynb without extension)
    "embeddings-to-labelled-maps": {
        "description": "From embeddings to labelled maps: embeds articles, projects them with UMAP, clusters them, names the clusters with an LLM and exports an interactive map.",
        "methodology": [
            "Articles are embedded with the Impresso embedding service and reduced to two dimensions with UMAP.",
            "HDBSCAN finds the clusters; an LLM labels each one from a sample of its articles.",
            "The notebook then checks the labels (newspaper and decade shares per cluster, a skim of articles, stability under other clustering settings) and exports the interactive map, which shows only the first 15 words of each article.",
        ],
    },
    "SBA-UMAP": {
        "hidden": True,   # OLD notebook, replaced by embeddings-to-labelled-maps. Its outputs hold article data: delete the files.
    },
}
