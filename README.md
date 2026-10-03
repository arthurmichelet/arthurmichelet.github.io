# Figures & Notebooks

A minimal GitHub Pages site. Drop in files, run one command, push.

## Adding content

1. Put exported Plotly figures in `plots/` (the `.html` files from `export_with_and_without_title`; `-notitle.html` variants are ignored).
2. Put notebooks in `notebooks/` (`.ipynb`, ideally with outputs saved).
3. Build:

   ```bash
   pip install nbconvert nbformat   # once
   python build.py
   ```

4. Publish:

   ```bash
   git add -A
   git commit -m "Update site"
   git push
   ```

Titles come from the file name (`my-figure.html` becomes "My figure") or, for notebooks, from the first `# Heading`.

## One-time GitHub setup

1. On github.com, create a new repository (e.g. `figures`). It must be **public** on a free account.
2. In this folder:

   ```bash
   git init
   git add -A
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/figures.git
   git push -u origin main
   ```

3. In the repo: **Settings → Pages → Build and deployment**. Source: *Deploy from a branch*. Branch: `main`, folder `/ (root)`. Save.
4. After a minute the site is live at `https://<your-username>.github.io/figures/`.

## Style

`style.css` mirrors `plot_style.py`: `#fafafa` background, `#333333` text, `#e8e8e8` rules, EB Garamond bold headings, Google Sans Flex body, and white pill badges with a 1.2 px `#333333` border. The orange hover colour (`#FF4D14`) is the only addition; change `--accent` in `style.css` to taste.

Figures already carry their own styling from `apply_template`, so they match the site with no extra work.
