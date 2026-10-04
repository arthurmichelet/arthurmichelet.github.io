#!/usr/bin/env python3
"""Generate the grainy background textures used by style.css.

Writes assets/bg.webp (landscape), assets/bg-portrait.webp (phones) and assets/grain.webp
(a small repeating grain tile). Smudged colour fields in your palette plus grain.
Colours that are too dark or too saturated to sit under black text are kept
towards the edges and corners; the centre stays light so the text stays readable.

Usage:  python3 make_background.py [seed]      (needs numpy and Pillow)
Change the PALETTE or the BLOBS below, or try another seed, then re-run.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7
LIGHTEN = 0.2   # 1 = full palette strength, lower = paler, more readable
SOFTEN = 5.0     # blur of the colour fields, in pixels of a 3200-wide working image (scaled for smaller ones); 0 = crisp speckle
GRAIN = 0.01     # strength of the grain on top
OUT_SCALE = 0.75 # size of the colour images relative to the working image (smooth, so small is fine)
OUT = Path(__file__).parent / "assets"

PALETTE = {
    "base": "#E8FDF6",    # pale mint: the paper
    "mint": "#5DCAA5",
    "neon": "#00FFA6",
    "green": "#1D9E75",
    "deep": "#085041",
    "orange": "#FF4D14",
}

# (colour, x, y, radius_x, radius_y, strength), positions as fractions of the image.
# Dark / strong colours stay at the edges; the middle only gets light ones.
LANDSCAPE = [
    ("orange", 0.04, 0.10, 0.17, 0.26, 0.95),
    ("neon",   0.09, 0.46, 0.17, 0.28, 0.90),
    ("green",  0.10, 0.84, 0.20, 0.24, 0.80),
    ("deep",   0.01, 0.98, 0.12, 0.18, 0.60),
    ("mint",   0.28, 0.20, 0.20, 0.32, 0.45),
    ("mint",   0.50, 0.62, 0.30, 0.40, 0.40),
    ("neon",   0.58, 0.14, 0.14, 0.22, 0.35),
    ("mint",   0.93, 0.18, 0.18, 0.32, 0.90),
    ("neon",   0.82, 0.40, 0.12, 0.22, 0.65),
    ("green",  0.97, 0.62, 0.14, 0.26, 0.75),
    ("orange", 0.90, 0.97, 0.20, 0.20, 0.90),
    ("deep",   1.00, 0.40, 0.07, 0.20, 0.45),
]
PORTRAIT = [
    ("orange", 0.05, 0.05, 0.38, 0.14, 0.95),
    ("neon",   0.92, 0.22, 0.30, 0.16, 0.85),
    ("green",  0.04, 0.45, 0.28, 0.18, 0.75),
    ("mint",   0.50, 0.30, 0.60, 0.20, 0.40),
    ("mint",   0.90, 0.60, 0.34, 0.20, 0.80),
    ("neon",   0.10, 0.72, 0.34, 0.16, 0.85),
    ("deep",   0.02, 0.82, 0.16, 0.12, 0.50),
    ("orange", 0.88, 0.96, 0.40, 0.12, 0.90),
    ("green",  0.50, 1.00, 0.45, 0.10, 0.70),
]


def rgb(hex_color):
    return np.array([int(hex_color[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32) / 255


def blur(a, sy, sx):
    """Gaussian blur through the FFT (sigma in pixels, different per axis)."""
    fy = np.fft.fftfreq(a.shape[0])[:, None]
    fx = np.fft.fftfreq(a.shape[1])[None, :]
    g = np.exp(-2 * np.pi ** 2 * ((sy * fy) ** 2 + (sx * fx) ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g)).astype(np.float32)


def noise(rng, shape, sy, sx):
    n = blur(rng.standard_normal(shape).astype(np.float32), sy, sx)
    return n / n.std()


def make(blobs, size, scale, seed, name):
    w, h = size  # working resolution; the final image is scale times larger
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    x, y = x / w, y / h

    # warp the coordinates so the shapes look smudged, not elliptical
    wx = x + 0.05 * noise(rng, (h, w), h * 0.10, w * 0.06)
    wy = y + 0.07 * noise(rng, (h, w), h * 0.08, w * 0.05)
    streaks = noise(rng, (h, w), h * 0.22, w * 0.012)  # vertical brush smears

    img = np.tile(rgb(PALETTE["base"]), (h, w, 1))
    for colour, bx, by, rx, ry, strength in blobs:
        d2 = ((wx - bx) / rx) ** 2 + ((wy - by) / ry) ** 2
        field = strength * np.exp(-1.3 * d2) * np.clip(1 + 0.55 * streaks, 0.1, 1.7)
        a = np.clip(field, 0, 1)
        speckle = (a > rng.random((h, w))).astype(np.float32)  # random-threshold dither
        a = 0.45 * a + 0.55 * speckle * np.clip(a * 2.2, 0, 1)
        img = img * (1 - a[..., None]) + rgb(PALETTE[colour]) * a[..., None]

    base = rgb(PALETTE["base"])
    img = base + (img - base) * LIGHTEN                                # paler colours
    soften = SOFTEN * w / 3200
    if soften:
        img = np.stack([blur(img[..., c], soften, soften) for c in range(3)], axis=-1)
    img = np.clip(img, 0, 1)
    # The colour image is smooth, so it stays small and loads fast. The grain is a
    # separate tiny tile (make_grain) that the browser repeats at full sharpness.
    out_w = int(w * OUT_SCALE) if OUT_SCALE else w
    out_h = int(h * OUT_SCALE) if OUT_SCALE else h
    big = Image.fromarray((img * 255).astype(np.uint8)).resize((out_w, out_h), Image.LANCZOS)
    arr = np.asarray(big).astype(np.float32) / 255
    arr += rng.normal(0, 0.004, arr.shape[:2] + (1,)).astype(np.float32)  # avoids colour banding
    out = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    OUT.mkdir(exist_ok=True)
    out.save(OUT / name, "WEBP", quality=88, method=6)
    print(f"{name}: {out.size[0]}x{out.size[1]}, {(OUT / name).stat().st_size / 1024:.0f} KB")


def make_grain(seed, name="grain.webp", size=512):
    """A seamless, semi-transparent grain tile (dark and light specks). style.css repeats it
    over the colour image: grain stays crisp on any screen, for a few KB instead of megabytes."""
    rng = np.random.default_rng(seed + 100)
    n = blur(rng.standard_normal((size, size)).astype(np.float32), 0.7, 0.7)  # FFT blur wraps: tiles seamlessly
    n /= n.std()
    dark = np.clip(-n, 0, None) * GRAIN * 1.4
    light = np.clip(n, 0, None) * GRAIN * 3.2
    alpha = np.clip(np.where(n < 0, dark, light), 0, 1)
    rgba = np.zeros((size, size, 4), np.uint8)
    rgba[..., :3] = np.where(n[..., None] < 0, 20, 255)
    rgba[..., 3] = (alpha * 255).round().astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(OUT / name, "WEBP", quality=75, alpha_quality=70, method=6)
    print(f"{name}: {size}x{size}, {(OUT / name).stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    make(LANDSCAPE, (3200, 2000), 2, SEED, "bg.webp")
    make(PORTRAIT, (900, 1400), 2, SEED + 1, "bg-portrait.webp")
    make_grain(SEED)
