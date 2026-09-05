#!/usr/bin/env python3
"""build_icon.py: the `throughline` icon, "One Thread Through Separate Slabs".

Porcelain cushion tile carrying one toy-scale object, matching the fledgeling
set (direction 2a, porcelain + gel object): four graphite slabs stacked with
real gaps between them, each one a paragraph, none touching. One vermilion
cord runs through all four. It enters each slab where it left the one above,
and in the gaps, where there is nothing else, it is the only thing there.

Why this object. The failure the skill fixes is a story whose paragraphs are
each fine and do not follow on; the slabs are that, deliberately separated.
The thread is the one rule the skill enforces: every paragraph takes
something from the one before it. It is unbroken, and it is the only warm
thing on the tile.

Signature move: THE THREAD IS BRIGHTEST IN THE GAPS. On a slab face it is a
cord lying on graphite; between slabs it crosses porcelain with nothing to
hold it, which is exactly the seam a reader feels when it is missing. Second
move: the slabs are not aligned. Each is a different width and sits at a
different offset, the way paragraphs are, so the thread has to bend to reach
the next one rather than fall straight through.

Three takes from one script: `master` has the thread meandering over the
faces, entering each slab at a different point; `A2-spine` runs it as a
near-vertical stitch, the flatter reading; `A3-weave` uses the master's path
but passes the cord behind the second and fourth slabs, so it is stitched
through the stack rather than laid on it.

Material sampled from create-mac-icon's corpus rather than assumed: the slabs
use the family's warm graphite ramp (the same one status-update and reckon
stand their objects in); the cord's shadow is warm brown, not black; the
contact pool under the stack is only a shade darker than the porcelain.

    python3 build_icon.py > icon.svg
    python3 build_icon.py A2-spine > icon-A2-spine.svg
    python3 build_icon.py A3-weave > icon-A3-weave.svg
"""
from __future__ import annotations

import pathlib
import sys

S = 1024
SQUIRCLE = (pathlib.Path(__file__).resolve().parents[2]
            / "create-mac-icon" / "assets" / "squircle-path.txt")

# --- family constants, lifted from the fledgeling set ----------------------
GROUND_TOP = "#F8F5EE"
GROUND_BOT = "#E4DDCB"
TILE_RIM = "#FFFDF8"
VIGNETTE = "#8A7A62"
WARM_SHADOW = "#3E2A18"

G_TOP = "#6E675A"
G_LIT = "#5A5449"
G_SHADE = "#332E27"
G_DEEP = "#221E18"

EMBER_DEEP = "#BC3A14"
EMBER = "#DE5A28"
EMBER_MID = "#F58F4A"
EMBER_HI = "#FFB661"
EMBER_CORE = "#FFD9A8"

# --- geometry -------------------------------------------------------------
# Four slabs. (x0, x1, y0, y1). Widths differ and left edges differ, the way
# paragraphs do; the stack spans 60% of the tile.
SLABS = [
    (232.0, 760.0, 236.0, 340.0),
    (262.0, 800.0, 386.0, 490.0),
    (224.0, 728.0, 536.0, 640.0),
    (272.0, 782.0, 686.0, 790.0),
]
SLAB_R = 22.0
EDX, EDY = 26.0, -18.0          # extrusion: up and to the right
THREAD_W = 34.0                 # the cord's width
GAP_GLOW_R = 44.0

# Where the thread crosses each slab's top and bottom edge, as x. The master
# meanders; the spine take runs straight.
MASTER_X = [(330, 470), (470, 640), (640, 400), (400, 560)]
SPINE_X = [(512, 512), (512, 512), (512, 512), (512, 512)]


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def rrect(x0: float, y0: float, x1: float, y1: float, r: float) -> str:
    w, h = x1 - x0, y1 - y0
    r = min(r, w / 2, h / 2)
    return (f"M{x0 + r:.1f},{y0:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} "
            f"v{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},{r:.1f} "
            f"h-{w - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},-{r:.1f} "
            f"v-{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},-{r:.1f} z")


def thread_path(xs: list[tuple[int, int]]) -> str:
    """One continuous cubic path from above the first slab to below the last.

    Each slab crossing is a straight-ish diagonal across the face; each gap is
    a smooth bend that carries the exit x of one slab to the entry x of the
    next, so the cord is visibly the same cord on both sides of every seam.
    """
    pts: list[tuple[float, float]] = []
    top0 = SLABS[0][2]
    pts.append((xs[0][0], top0 - 60))
    for (x0, x1, y0, y1), (xa, xb) in zip(SLABS, xs):
        pts.append((xa, y0))
        pts.append((xb, y1))
    pts.append((xs[-1][1], SLABS[-1][3] + 60))
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dy = (by - ay) * 0.5
        d.append(f"C{ax:.1f},{ay + dy:.1f} {bx:.1f},{by - dy:.1f} {bx:.1f},{by:.1f}")
    return " ".join(d)


def build(take: str = "master") -> str:
    xs = SPINE_X if take == "A2-spine" else MASTER_X
    o: list[str] = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
      f'viewBox="0 0 {S} {S}">')
    a("<defs>")
    a(f'<linearGradient id="ground" x1="0" y1="0" x2="0.18" y2="1">'
      f'<stop offset="0" stop-color="{GROUND_TOP}"/>'
      f'<stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>')
    a('<radialGradient id="key" cx="0.30" cy="0.18" r="0.86">'
      '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.60"/>'
      '<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.11"/>'
      '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.76">'
      f'<stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/></radialGradient>')
    a(f'<linearGradient id="body" x1="0.1" y1="0" x2="1" y2="0.9">'
      f'<stop offset="0" stop-color="{G_TOP}"/>'
      f'<stop offset="0.38" stop-color="#4C463B"/>'
      f'<stop offset="1" stop-color="{G_DEEP}"/></linearGradient>')
    a(f'<linearGradient id="face" x1="0" y1="0.05" x2="1" y2="0.85">'
      f'<stop offset="0" stop-color="#645D4F"/>'
      f'<stop offset="0.34" stop-color="{G_LIT}"/>'
      f'<stop offset="0.78" stop-color="{G_SHADE}"/>'
      f'<stop offset="1" stop-color="{G_DEEP}"/></linearGradient>')
    # The cord: lit along its upper-left edge, deep on the lower-right. One
    # gradient across the whole path, so the light stays one light.
    a(f'<linearGradient id="cord" gradientUnits="userSpaceOnUse" x1="220" y1="180" x2="820" y2="860">'
      f'<stop offset="0" stop-color="{EMBER_MID}"/>'
      f'<stop offset="0.45" stop-color="{EMBER}"/>'
      f'<stop offset="1" stop-color="{EMBER_DEEP}"/></linearGradient>')
    a(f'<linearGradient id="rim" x1="0" y1="0" x2="0.7" y2="1">'
      f'<stop offset="0" stop-color="{TILE_RIM}" stop-opacity="0.55"/>'
      f'<stop offset="0.45" stop-color="{TILE_RIM}" stop-opacity="0.14"/>'
      f'<stop offset="1" stop-color="{TILE_RIM}" stop-opacity="0"/></linearGradient>')
    a(f'<radialGradient id="gapglow" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{EMBER_HI}" stop-opacity="0.55"/>'
      f'<stop offset="0.6" stop-color="{EMBER}" stop-opacity="0.14"/>'
      f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>')
    a('<filter id="soft" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="22"/></filter>')
    a('<filter id="mid" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="9"/></filter>')
    a('<filter id="tight" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="4"/></filter>')
    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    over = "".join(f'<path d="{rrect(x0, y0, x1, y1, SLAB_R)}"/>'
                   for i, (x0, x1, y0, y1) in enumerate(SLABS) if i % 2 == 0)
    a(f'<clipPath id="overslabs">{over}</clipPath>')
    a("</defs>")

    a('<g clip-path="url(#tile)">')
    # ================================================================= bg
    a('<g id="bg">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#key)"/>')
    a("</g>")

    # ================================================================ mid
    a('<g id="mid">')
    # One contact pool under the whole stack, warm and soft.
    x0s = min(s[0] for s in SLABS); x1s = max(s[1] for s in SLABS)
    a(f'<ellipse cx="{(x0s + x1s) / 2 + 22:.1f}" cy="{SLABS[-1][3] + 26:.1f}" '
      f'rx="{(x1s - x0s) * 0.54:.1f}" ry="40" fill="{WARM_SHADOW}" '
      f'opacity="0.22" filter="url(#soft)"/>')
    # Each slab throws a short warm shadow into the gap beneath it, which is
    # what makes the gaps read as air rather than as stripes.
    for (x0, x1, y0, y1) in SLABS:
        a(f'<rect x="{x0 + 18:.1f}" y="{y1 + 4:.1f}" width="{x1 - x0 - 24:.1f}" '
          f'height="18" rx="9" fill="{WARM_SHADOW}" opacity="0.30" filter="url(#mid)"/>')
    d = thread_path(xs)
    weave = take == "A3-weave"
    if weave:
        # The whole cord sits behind the stack first; the parts that cross the
        # first and third slabs are redrawn over them in the fg group.
        a(f'<path d="{d}" fill="none" stroke="url(#cord)" stroke-width="{THREAD_W:.1f}" '
          f'stroke-linecap="round"/>')
        a(f'<path d="{d}" fill="none" stroke="{EMBER_CORE}" stroke-width="7" '
          f'stroke-linecap="round" opacity="0.55" transform="translate(-6,-7)"/>')
    # Extruded bodies, then front faces.
    for (x0, x1, y0, y1) in SLABS:
        a(f'<path d="{rrect(x0 + EDX, y0 + EDY, x1 + EDX, y1 + EDY, SLAB_R)}" '
          f'fill="url(#body)"/>')
    for (x0, x1, y0, y1) in SLABS:
        a(f'<path d="{rrect(x0, y0, x1, y1, SLAB_R)}" fill="url(#face)"/>')
        a(f'<path d="{rrect(x0 + 1.5, y0 + 1.5, x1 - 1.5, y1 - 1.5, SLAB_R - 1.5)}" '
          f'fill="none" stroke="url(#rim)" stroke-width="2.5"/>')
    a("</g>")

    # ================================================================= fg
    a('<g id="fg">')
    # The glow where the cord crosses each gap: the seam is the lit thing.
    for i in range(len(SLABS) - 1):
        gap_y = (SLABS[i][3] + SLABS[i + 1][2]) / 2
        gx = (xs[i][1] + xs[i + 1][0]) / 2
        a(f'<circle cx="{gx:.1f}" cy="{gap_y:.1f}" r="{GAP_GLOW_R * 1.6:.1f}" '
          f'fill="url(#gapglow)"/>')
    clip = ' clip-path="url(#overslabs)"' if weave else ""
    # The cord's shadow, offset lower-right, warm.
    a(f'<g{clip}><path d="{d}" fill="none" stroke="{WARM_SHADOW}" stroke-width="{THREAD_W + 4:.1f}" '
      f'stroke-linecap="round" opacity="0.38" filter="url(#mid)" '
      f'transform="translate(10,14)"/></g>')
    # The cord itself.
    a(f'<g{clip}><path d="{d}" fill="none" stroke="url(#cord)" stroke-width="{THREAD_W:.1f}" '
      f'stroke-linecap="round"/></g>')
    a("</g>")

    # ========================================================== highlight
    a('<g id="highlight">')
    # A highlight along the cord's upper-left edge: one key light, same as
    # the slabs.
    a(f'<g{clip}><path d="{d}" fill="none" stroke="{EMBER_CORE}" stroke-width="7" '
      f'stroke-linecap="round" opacity="0.55" transform="translate(-6,-7)"/></g>')
    a(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" '
      f'stroke-width="3" opacity="0.55"/>')
    a("</g>")
    a("</g>")
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    take = sys.argv[1] if len(sys.argv) > 1 else "master"
    sys.stdout.write(build(take) + "\n")
