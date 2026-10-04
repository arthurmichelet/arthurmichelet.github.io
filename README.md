# Personal site (GitHub Pages)

Pages: **home** (name + a "start" button leading to info), **info** (paragraph, contact incl. ORCID, grants and awards, interests), **publications** (articles and conference papers, published notebooks), **explore** (visualisations and notebooks).

## Files

| File | What it is |
|---|---|
| `content.py` | All the text: name, info paragraph, contact, ORCID, grants and awards, interests, publications, published notebooks. Edit this. |
| `build.py` | Generates the HTML pages. Run it after any change. |
| `theme-retro.css` | The retro-technical look (boxes, tabs, window title bars), loaded on top of `style.css`. |
| `style.css` | The look, mirroring `plot_style.py`. Highlight colour is `--accent`. |
| `assets/` | `bg.webp` and `bg-portrait.webp`: the grainy background (generated, but committed so the site can use it). |
| `make_background.py` | Generates those two images in your palette. Optional: `pip3 install numpy pillow`, then `python3 make_background.py 12` (any number = a different pattern). Edit `PALETTE` / the blob lists at the top to change colours and where they sit. |
| `make_previews.py` | Optional: makes the preview pictures for the explore cards from your interactive figures (see below). |
| `plots/` | Drop exported figures here (`.html` and/or `.png`). |
| `notebooks/` | Drop `.ipynb` notebooks here (save them with outputs). |

Everything else (`index.html`, `info.html`, `publications.html`, `explore.html`, `notebooks/*.html`, `plots/_png/`) is generated: do not edit it by hand.

## Update the site

```bash
cd path/to/figures-site
pip3 install nbconvert nbformat   # once
python3 build.py
git add -A
git commit -m "Update site"
git push
```

The site refreshes a minute or two after the push.

- **New or updated figure:** put the file in `plots/` (same name replaces the old one). A figure that exists as both `x.html` and `x.png` appears as one row with two pills. `-notitle` variants are ignored.
- **Notebook:** put the `.ipynb` in `notebooks/`. Its title is the first `# Heading`, or the file name.
- **Text:** edit `content.py` (replace the dummy publications and the placeholder e-mail).
- **Remove something:** delete its file(s) and rebuild.

## One-time GitHub setup

1. Create a **public** repository on github.com.
2. In this folder: `git init`, commit, `git branch -M main`, `git remote add origin <repo url>`, `git push -u origin main`.
3. In the repo: **Settings → Pages → Build and deployment**: *Deploy from a branch*, branch `main`, folder `/ (root)`.
4. The site is live at `https://<username>.github.io/<repo-name>/`.

## Before publishing a figure or notebook

When a notebook is converted, `build.py` renders Plotly figures that were saved only as JSON, leaves out printed outputs longer than 20 000 characters (e.g. a DataFrame dump), and prints a WARNING when a figure's hover text includes titles or text. Read those warnings, and clear or edit the outputs in the notebook if needed.

Everything in the repo is public. Interactive Plotly figures embed whatever you pass as `text`, `hover_data`, `hover_name` or `customdata`, and notebooks keep their saved outputs. Make sure none of it contains article text you do not have the right to redistribute.

## Licence

`LICENSE` in the repo root: content (text, figures, plots, notebook narration) under CC BY-NC 4.0, code under MIT, and the article openings shown in the plots are explicitly excluded (they stay the publishers' property). Each viewer page carries a one-line reminder (see `write_viewer` in `build.py`). To change the licence, edit `LICENSE`, that line, and the comment in the notebook's export cell.

## Page transitions

Pages cross-fade and the name glides between its home position and the top (CSS view transitions, in `style.css`). This works in Chrome, Edge and Safari once the site is online (or served over `http://`); it does not animate when you open the files straight from disk, and Firefox switches pages instantly. It is switched off automatically for people who prefer reduced motion.

## Explore cards (retro look)

Each figure and notebook is a card: title, short description, preview picture and links.

- **Title and description:** edit `EXPLORE` at the bottom of `content.py` (key = file name without extension). Without an entry the card shows the file name only.
- **Preview picture:** `plots/<name>-preview.webp` (also .png/.jpg). If there is none, `plots/<name>.png` is used when it exists. Run `python3 make_previews.py` to make previews for new interactive figures (one-time setup in the file). For a notebook: `notebooks/<name>-preview.webp`.

## Looks (themes)

`THEME` in `content.py` picks the look: `"retro"` (default, `theme-retro.css` on top of `style.css`) or `"classic"` (`style.css` alone, the original look). Change it and run `python3 build.py`. `style.css` is not modified by the retro theme, so going back is always one word.

## Style

`#fafafa` background, `#333333` text, `#e8e8e8` rules, EB Garamond bold headings, Google Sans Flex body, white pill badges with a 1.2 px `#333333` border. The grainy mint/green background (with orange at the corners) is `assets/bg.webp`, drawn by `make_background.py` from your `NP_COLORS` palette; dark and saturated colours stay at the edges so the text remains readable, and phones get a lighter version. For a plain `#fafafa` page, delete the `body.site::before` block in `style.css`.

## Viewer pages (retro look)

In the retro look, clicking a card on *explore* opens `view/<name>.html`: the figure or notebook in a
frame on the left, **description** and **methodology** on the right. These pages are generated by
`build.py` (the `view/` folder is rebuilt on every run, do not edit it by hand). Fixed-size Plotly
figures are scaled down to fit the frame; "open full page" links to the raw file.

The text comes from `EXPLORE` in `content.py`:

- `description`: one or two sentences (also shown on the card);
- `about`: optional longer text for the viewer page, replaces `description` there;
- `methodology`: a string or a list of strings (each one shown as a paragraph); text accepts `[link](url)`, `**bold**` and `*italic*`;
- `hidden`: `True` keeps the file in `plots/` or `notebooks/` but leaves it out of the site (no card, no viewer page, no converted notebook).

Notebooks use the same keys, with the notebook's file name (without `.ipynb`) as the key. With
`THEME = "classic"` no viewer pages are made and the old layout is used.

## Dark mode (retro look)

The retro look follows the visitor's system / browser setting (`prefers-color-scheme`). A button on the
right of the menu row switches between light and dark; the choice is remembered in the browser
(`localStorage`) and wins over the system setting. The button and the small script are defined in
`build.py` (`THEME_TOGGLE`, `THEME_SCRIPT`) and styled at the end of `theme-retro.css`.

The colours are variables at the top of `theme-retro.css`: the light values in `:root`, the dark ones in
the two dark blocks just below (the same list, once for the system setting and once for the button).
Figures, previews and notebooks keep a light frame, since they are drawn for a light background.

## Publications (Chicago style)

References on the publications page follow Chicago notes-bibliography. In `content.py`, write the
authors as "Last, First, and First Last", and put everything after the title (container, editors,
pages, publisher, year) in `venue`, with `*asterisks*` for italics. The DOI / link is printed at the
end of the reference. A pill without a link (no `url`) is shown with a solid colour; pills that link
somewhere stay white.

## Research interests (bricks)

On the info page, `INTERESTS` in `content.py` is a list of `(name, [topics])`: each pair becomes a
rounded slab with its box of topics, joined by a curved line. They are grey until you hover a slab or its box; then both take the slab's colour (`BRICK_COLOURS` in `build.py`; box offsets: `BRICK_LAYOUT`). On touch screens the colours are always on. On a phone the
bricks stack one under the other. A plain list of strings still works and gives a simple boxed list.
