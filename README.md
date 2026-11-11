# Personal site (GitHub Pages)

Pages: **home** (name + a "start" button leading to info), **info** (paragraph, contact incl. ORCID, grants and awards, interests), **publications** (articles and conference papers, published notebooks), **explore** (visualisations and notebooks).

## Files

| File | What it is |
|---|---|
| `content.py` | All the text: name, info paragraph, contact, ORCID, grants and awards, interests, publications, published notebooks. Edit this. |
| `build.py` | Generates the HTML pages. Run it after any change. |
| `theme-retro.css` | The retro-technical look (boxes, tabs, window title bars, monospaced headings), loaded on top of `style.css`. |
| `theme-lab.css` | The lab look, inspired by NotesLab (WordPress.com) and forensic-architecture.org: warm grey page, large light name, hairline rules, red index numbers, Satoshi + Gambetta (Fontshare), menu in a box at the top right. Select with `THEME = "lab"`. |
| `theme-retro-variant.css` | The same retro look with other fonts: Erode for the name, the titles and the info introduction, Satoshi for everything else (both from Fontshare). |
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

Pages cross-fade and the name glides between its home position and the top (CSS view transitions, in `style.css`). This works in Chrome, Edge and Safari once the site is online (or served over `http://`); it does not animate when you open the files straight from disk. Firefox is excluded on purpose (the transition delayed scrolling there), so it switches pages instantly. It is switched off automatically for people who prefer reduced motion.

## Explore cards (retro look)

Each figure and notebook is a card: title, short description, preview picture and links.

- **Title and description:** edit `EXPLORE` at the bottom of `content.py` (key = file name without extension). Without an entry the card shows the file name only.
- **Preview picture:** `plots/<name>-preview.webp` (also .png/.jpg). If there is none, `plots/<name>.png` is used when it exists. Run `python3 make_previews.py` to make previews for new interactive figures (one-time setup in the file). For a notebook: `notebooks/<name>-preview.webp`.

## Looks (themes)

`THEME` in `content.py` picks the look: `"lab"` (`theme-lab.css`: ruled and hairline, no shadows or movement; Satoshi for headings and labels, Gambetta for text, both from Fontshare; menu in a box at the top right; titles carry a red index number; the cards carry codes "I.01", "I.02"), `"retro-variant"` (`theme-retro-variant.css` on top of `style.css`: Erode for the name, titles and info introduction, Satoshi for the rest; both fonts come from Fontshare, see `FONTS` in `build.py`), `"retro"` (`theme-retro.css`: monospaced headings) or `"classic"` (`style.css` alone, the original look). Change it and run `python3 build.py`. `style.css` is not modified by the retro themes, so going back is always one word. The two retro files and `theme-lab.css` are independent files: a change to the colours or layout has to be made in both.

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

## Companion page (secret, passcode-protected)

A page for the thesis manuscript, built like *explore* (one section per chapter, one tile per visualisation, a viewer page per figure) but encrypted and at an unlisted address. It is not in the menu, `sitemap.xml` or `robots.txt`, and carries `noindex`.

**How it stays private.** The readable pages are built in a temporary folder outside the repo, encrypted with [StatiCrypt](https://github.com/robinmoisson/staticrypt) (AES, passcode-derived key) and only the encrypted files are written to `companion-<slug>/`. Your source figures live in `COMPANION_SRC` (outside the repo), and so does the wording of the page: heading, introduction, chapters, titles, descriptions and methodology are in `COMPANION_SRC/companion_config.py`, **not** in `content.py`, because `content.py` is public on GitHub. Back that file up yourself: it is not in git. The build refuses to finish if anything readable is left in the output. The passcode is never stored in the repo: it is read from the environment.

**Build / update** (needs Node.js for `npx`):

```bash
cd path/to/personal-site
COMPANION_PASSCODE="your passphrase" python3 build.py
git add -A && git commit -m "Update companion" && git push
```

Without `COMPANION_PASSCODE` the build skips the companion and leaves the encrypted folder as it is. The first build creates `.staticrypt.json` (a public salt shared by all companion pages, so one unlock opens every page): commit it. Always rebuild with the **same** passcode unless you want to change it.

**Add a figure while you write.**
1. Export the Plotly `.html` into `COMPANION_SRC`. Then make its tile pictures (light and dark) with `python3 make_companion_previews.py` (one-time setup: see the top of that file). They are saved next to the figure as `<name>-preview.webp` and `<name>-preview-dark.webp`; existing ones are kept, delete one to redo it. Without them the tile has no picture.
2. Add an entry under its chapter in `COMPANION` in `COMPANION_SRC/companion_config.py`: `file` (name without `.html`), `number`, `title`, `description`, `methodology`. A new chapter is a new dict with `chapter` and `figures`.
3. Build and push (above). Files in `COMPANION_SRC` that are not in `COMPANION` are listed as "not published".

**Good to know**
- The folder name `COMPANION_SLUG` is in the link and the QR code in the manuscript: never change it after printing. To rotate the passcode, rebuild with a new one (the old one stops working for the new files; share the new one).
- Use a long passphrase (5+ random words): anyone can try guesses offline against the public encrypted files.
- Each Plotly export carries a ~4.8 MB copy of plotly.js; the companion swaps it for the plotly.js CDN `<script>`, so pages stay small but need an internet connection to draw.
- The prompt has "Remember me" ticked by default (stores a salted hash in the browser's localStorage), so a reader enters the passcode once per device.
- The QR code should encode only the link, never the passcode.
- Same copyright rule as the rest of the site: no article text longer than 15 words (the build warns about long text/hover strings in a figure).
- Not in `plots/` or `notebooks/`: those are public. Never copy companion figures there.
