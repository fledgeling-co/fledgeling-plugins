#!/usr/bin/env python3
"""build_banner.py — the geminify banner, composed as SVG and rasterised by rsvg.

Not HTML, deliberately. The set's banners are HTML rendered through a browser, and
on this machine that route is closed: `obscura fetch --screenshot` renders at a
fixed 1280x720 with no viewport flag, and `obscura serve`'s CDP accepts a
connection to its page target but answers Page.navigate,
Emulation.setDeviceMetricsOverride and Page.captureScreenshot alike with
`-32601 No page for session`, so there is no way to capture 1600x520 at 2x. An SVG
composed here and rasterised by rsvg-convert is reproducible on this machine,
which the HTML is not.

    python3 build_banner.py            # writes banner-src.svg + banner.png (3200x1040)

Type is Superclarendon Bold: a slab serif, unused elsewhere in this set, whose
heavy verticals give the name's TWO i-stems the presence the wordmark device needs
— the same mark twice, one of them counted. It is a locally installed family
because rsvg resolves system fonts (and, measured on this build, Obscura does the
opposite: it shapes Google-hosted webfonts and ignores installed families).

The two tittles are found by MEASUREMENT rather than by guessing at x offsets: the
wordmark is rendered twice, once with dotless i (U+0131) and once with the font's
own dotted i, and the difference between the two rasters is exactly the two
tittles. Their centroids are where the gel dots go.
"""
from __future__ import annotations

import pathlib
import subprocess
import tempfile

import numpy as np
from PIL import Image

ASSETS = pathlib.Path(__file__).resolve().parent
W, H, SCALE = 1600, 520, 2

FONT = "Superclarendon"
WORD_SIZE = 96
WORD_X, WORD_BASELINE = 452, 272
TAG_SIZE = 26

INK = "#2E343D"
MUTED = "#756E60"
TAG_STRONG = "#3A414B"

# The ground is the set's own sheet, unchanged: warm porcelain, cushion-lit, and
# deliberately not page-white so it holds on GitHub's light and dark grounds alike.
GROUND = ("#FAF8F2", "#F1EEE4", "#E5E1D4")
VIGNETTE = "rgba(122,112,92,0.16)"

# The pair again at banner scale, bleeding off the right edge: same construction as
# the icon master — two capsules, the front one translucent, the tally rules landing
# in the crossing.
LEAF_W, LEAF_H = 252, 336
PAIR_CX, PAIR_TOP = 1470, 96
LEAN = 14
# The right-edge pair is drawn in the SHEET's own porcelain, not in the icon's clay
# and ember. Rendered at the icon's values it became a second, darker icon at the
# far end of the banner, competing with the real one for the eye; the set's other
# banners keep their continuation device in the paper's material and spend the
# accent only on the focal mark. Here the accent is the counted rule alone.
CLAY = ("#FBF9F4", "#F0ECE1", "#DFD9C9")
EMBER = ("#FDF6EE", "#F6E8DA", "#E8D5C2")
LENS = ("#C9A98E", "#A8846A")
RULES = [(0.44, 78), (0.57, 65), (0.70, 52)]           # y as a fraction of LEAF_H
GEL = ("#F79A54", "#EC7433", "#D9531A")


def render_svg(svg: str, out: pathlib.Path, width: int) -> None:
    """Render through a file INSIDE the assets directory, never a temp file.

    librsvg refuses to load a resource that sits outside the SVG's own directory,
    so a banner rendered from /tmp silently drops <image xlink:href="icon.png">
    and reports success — the first two versions of this banner shipped with no
    icon in them for exactly that reason. Writing the SVG beside icon.png makes
    the reference local and the load legal."""
    tmp = ASSETS / ".render.svg"
    tmp.write_text(svg)
    try:
        subprocess.run(["rsvg-convert", "-w", str(width), tmp.name, "-o", str(out)],
                       check=True, cwd=ASSETS)
    finally:
        tmp.unlink(missing_ok=True)


def tittle_centres() -> list[tuple[float, float]]:
    """Locate the two i-tittles by differencing a dotted render against a dotless
    one. Both strings are set identically, so every pixel that differs belongs to a
    tittle — no advance-width arithmetic, and no guessing at x offsets."""
    def strip(word: str, path: pathlib.Path) -> np.ndarray:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
               f'<rect width="100%" height="100%" fill="#FFFFFF"/>'
               f'<text x="{WORD_X}" y="{WORD_BASELINE}" font-family="{FONT}" '
               f'font-weight="700" font-size="{WORD_SIZE}" fill="#000000">{word}</text>'
               f'</svg>')
        render_svg(svg, path, W)
        return np.asarray(Image.open(path).convert("L")).astype(float)

    with tempfile.TemporaryDirectory() as d:
        dotted = strip("geminify", pathlib.Path(d) / "a.png")
        dotless = strip("gem&#x131;n&#x131;fy", pathlib.Path(d) / "b.png")
        diff = (dotless - dotted) > 40                 # ink present only when dotted
    cols = np.where(diff.any(axis=0))[0]
    if len(cols) == 0:
        raise SystemExit("no tittle difference found — does the font carry U+0131?")
    # split the differing columns into runs; expect exactly two
    runs, start = [], cols[0]
    for a, b in zip(cols, cols[1:]):
        if b - a > 6:
            runs.append((start, a))
            start = b
    runs.append((start, cols[-1]))
    if len(runs) != 2:
        raise SystemExit(f"expected two tittles, found {len(runs)}: {runs}")
    out = []
    for x0, x1 in runs:
        band = diff[:, x0:x1 + 1]
        rows = np.where(band.any(axis=1))[0]
        out.append(((x0 + x1) / 2, (rows[0] + rows[-1]) / 2))
    return out


def leaf(x: float, lean: float, ramp, alpha: float, gid: str) -> str:
    cx = x + LEAF_W / 2
    pivot_y = PAIR_TOP + LEAF_H * 0.92
    op = "" if alpha >= 1 else f' opacity="{alpha}"'
    return (f'<g transform="rotate({lean} {cx:.1f} {pivot_y:.1f})"{op}>'
            f'<rect x="{x:.1f}" y="{PAIR_TOP}" width="{LEAF_W}" height="{LEAF_H}" '
            f'rx="{LEAF_W / 2}" fill="url(#{gid})"/></g>')


def build() -> str:
    dots = tittle_centres()
    lx = PAIR_CX - LEAF_W / 2 - 56
    rx = PAIR_CX - LEAF_W / 2 + 56
    pivot_y = PAIR_TOP + LEAF_H * 0.92

    def ramp(gid, stops, y0, y1):
        s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        return (f'<linearGradient id="{gid}" x1="0" y1="{y0}" x2="0" y2="{y1}" '
                f'gradientUnits="userSpaceOnUse">{s}</linearGradient>')

    defs = [
        f'<linearGradient id="sheet" x1="0" y1="0" x2="0" y2="{H}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{GROUND[0]}"/>'
        f'<stop offset="0.52" stop-color="{GROUND[1]}"/>'
        f'<stop offset="1" stop-color="{GROUND[2]}"/></linearGradient>',
        f'<radialGradient id="cushion" cx="{W / 2}" cy="-40" r="{W * 0.78}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/>'
        f'<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="vig" cx="{W / 2}" cy="{H / 2}" r="{W * 0.62}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0.52" stop-color="#7A705C" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#7A705C" stop-opacity="0.16"/></radialGradient>',
        ramp("clay", ((0, CLAY[0]), (0.44, CLAY[1]), (1, CLAY[2])),
             PAIR_TOP, PAIR_TOP + LEAF_H),
        ramp("ember", ((0, EMBER[0]), (0.44, EMBER[1]), (1, EMBER[2])),
             PAIR_TOP, PAIR_TOP + LEAF_H),
        ramp("lens", ((0, LENS[0]), (1, LENS[1])), PAIR_TOP, PAIR_TOP + LEAF_H),
        ramp("gel", ((0, GEL[0]), (0.5, GEL[1]), (1, GEL[2])), 0, 14),
        f'<clipPath id="leafL"><rect x="{lx:.1f}" y="{PAIR_TOP}" width="{LEAF_W}" '
        f'height="{LEAF_H}" rx="{LEAF_W / 2}" '
        f'transform="rotate({-LEAN} {lx + LEAF_W / 2:.1f} {pivot_y:.1f})"/></clipPath>',
        f'<clipPath id="leafR"><rect x="{rx:.1f}" y="{PAIR_TOP}" width="{LEAF_W}" '
        f'height="{LEAF_H}" rx="{LEAF_W / 2}" '
        f'transform="rotate({LEAN} {rx + LEAF_W / 2:.1f} {pivot_y:.1f})"/></clipPath>',
        '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="11"/></filter>',
        '<filter id="drop" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="17"/></filter>',
    ]

    rules = []
    for i, (fy, wide) in enumerate(RULES):
        y = PAIR_TOP + LEAF_H * fy
        x = PAIR_CX - wide / 2
        if i == len(RULES) - 1:
            rules.append(f'<rect x="{x - 8:.1f}" y="{y - 4:.1f}" width="{wide + 16}" '
                         f'height="21" rx="10" fill="{GEL[1]}" opacity="0.45" '
                         f'filter="url(#glow)"/>')
            rules.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{wide}" height="13" '
                         f'rx="6.5" fill="url(#gel)"/>')
        else:
            rules.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{wide}" height="13" '
                         f'rx="6.5" fill="#6E5540" opacity="0.55"/>')

    # A gap between the two halves has to be a dx, not entities: rsvg collapses
    # &#160; here, and the halves rendered as "families.Say".
    tag = ('<tspan>One skill, two model families.</tspan>'
           f'<tspan dx="11" fill="{TAG_STRONG}" font-weight="600">'
           'Say the number, not the word.</tspan>')

    dot_svg = []
    for (cx, cy), fill in zip(dots, ("#9C8E76", GEL[1])):
        stops = ('#D2C5AD' if fill == "#9C8E76" else '#F8845A', fill)
        dot_svg.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11.5" fill="{fill}"/>'
            f'<circle cx="{cx - 2.6:.1f}" cy="{cy - 3.0:.1f}" r="4.4" '
            f'fill="{stops[0]}" opacity="0.85"/>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
        f'<defs>{"".join(defs)}</defs>'
        f'<rect width="{W}" height="{H}" fill="url(#sheet)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#cushion)"/>'
        f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
        # the pair, bleeding off the right edge
        f'<ellipse cx="{PAIR_CX}" cy="{PAIR_TOP + LEAF_H + 8}" rx="186" ry="28" '
        f'fill="#6E6049" opacity="0.20" filter="url(#drop)"/>'
        + leaf(lx, -LEAN, CLAY, 1.0, "clay")
        + leaf(rx, LEAN, EMBER, 0.84, "ember")
        + f'<g clip-path="url(#leafL)"><g clip-path="url(#leafR)">'
          f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#lens)" opacity="0.34"/>'
        + "".join(rules) + '</g></g>'
        # the icon, at the same 288 as its siblings' banners
        f'<image xlink:href="icon.png" x="96" y="116" width="288" height="288"/>'
        # wordmark, dotless, with the measured tittles poured over the stems
        f'<text x="{WORD_X}" y="{WORD_BASELINE}" font-family="{FONT}" font-weight="700" '
        f'font-size="{WORD_SIZE}" fill="{INK}" letter-spacing="-1">'
        f'gem&#x131;n&#x131;fy</text>'
        + "".join(dot_svg)
        + f'<text x="{WORD_X + 3}" y="{WORD_BASELINE + 54}" font-family="{FONT}" '
          f'font-size="{TAG_SIZE}" fill="{MUTED}">{tag}</text>'
        f'</svg>'
    )


if __name__ == "__main__":
    svg = build()
    src = ASSETS / "banner-src.svg"
    src.write_text(svg)
    render_svg(svg, ASSETS / "banner.png", W * SCALE)
    png = ASSETS / "banner.png"
    print(f"wrote {src.name} and {png.name} ({png.stat().st_size} bytes)")
