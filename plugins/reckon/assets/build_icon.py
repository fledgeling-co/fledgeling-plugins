#!/usr/bin/env python3
"""build_icon.py — the `reckon` icon: "The Rod That Casts No Shadow".

Porcelain cushion tile carrying one toy-scale object, per create-mac-icon's
icon-directions: five counting rods stood in a row. Four are solid, lit from
the upper left, each sitting on its own contact shadow. The fifth is drawn as
edges only — a wireframe rod, warm, with nothing under it.

Why this object. A reckoning counts what is there. The skill's claim is that a
remaining-work list has a third category between done and broken: the thing
nobody measured, which is neither and must stay visible. A row of rods is a
count; the wireframe one is the item you can see the shape of and know nothing
about.

Signature move: the accent object CASTS NO SHADOW. Every solid rod has a warm
contact shadow pooling to its lower right, because a shadow is what an object
leaves behind when a light has actually reached it. The wireframe rod has
none — no evidence beneath it. Nothing else in this marketplace has an object
that is present and unlit.

Separation from its nearest neighbours. `stocktake` is an opaque column with
one translucent card LIFTED OUT and backlit — its special item gains light and
leaves the set. This one's special item loses substance and stays in the row:
same footprint, same height, same place in the count, no surface and no
shadow. `whats-left` is a warm keystone clear of a dark arch, an extruded
solid with a hole through it; this is a row of uprights seen near-on.

One light, upper left and slightly forward. Rod tops catch it, left faces stay
lit, right faces fall away, and shadows go warm — a blue shadow in a warm scene
is the tell.

    python3 build_icon.py > icon.svg
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

ROD_TOP = "#6E675A"      # the cap, facing the key light
ROD_LIT = "#5A5449"      # left face
ROD_SHADE = "#332E27"    # right face, falling away
ROD_DEEP = "#221E18"     # the arris at the foot
WARM_SHADOW = "#3E2A18"

ACCENT_EDGE = "#DD6413"  # the ember, family-standard
ACCENT_MID = "#FFB661"
ACCENT_CORE = "#FFD9A8"

# --- geometry -------------------------------------------------------------
ROD_W = 100
ROD_H = 400
ROD_R = 50               # capsule ends; reads as a rod rather than a bar
GAP = 54
COUNT = 5
HOLLOW_INDEX = 3         # 0-based; fourth of five, off-centre on purpose

FLOOR_Y = 762            # where every rod's foot sits
TOP_Y = FLOOR_Y - ROD_H

TOTAL_W = COUNT * ROD_W + (COUNT - 1) * GAP
LEFT_X = (S - TOTAL_W) / 2
OPTICAL_LIFT = 14        # objects sit slightly above true centre


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def rod_path(x: float, y: float, w: float, h: float, r: float) -> str:
    return (f"M{x + r:.1f},{y:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} "
            f"v{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},{r:.1f} "
            f"h-{w - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},-{r:.1f} "
            f"v-{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},-{r:.1f} z")


def build() -> str:
    o: list[str] = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
      f'viewBox="0 0 {S} {S}">')

    # ---------------------------------------------------------------- defs
    a("<defs>")
    a(f'<linearGradient id="ground" x1="0" y1="0" x2="0.18" y2="1">'
      f'<stop offset="0" stop-color="{GROUND_TOP}"/>'
      f'<stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>')

    # Key light pooling from the upper left across the tile floor.
    a(f'<radialGradient id="key" cx="0.30" cy="0.20" r="0.85">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.62"/>'
      f'<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.12"/>'
      f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')

    a(f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.76">'
      f'<stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/>'
      f'</radialGradient>')

    # A rod is one solid with three tones: cap, lit face, shaded face.
    a(f'<linearGradient id="rodface" x1="0" y1="0" x2="1" y2="0.12">'
      f'<stop offset="0" stop-color="#6B6456"/>'
      f'<stop offset="0.30" stop-color="{ROD_LIT}"/>'
      f'<stop offset="0.72" stop-color="{ROD_SHADE}"/>'
      f'<stop offset="1" stop-color="{ROD_DEEP}"/></linearGradient>')

    a(f'<linearGradient id="rodfoot" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{ROD_DEEP}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{ROD_DEEP}" stop-opacity="0.72"/>'
      f'</linearGradient>')

    a(f'<linearGradient id="rodcap" x1="0" y1="0" x2="0.6" y2="1">'
      f'<stop offset="0" stop-color="#8A8274"/>'
      f'<stop offset="1" stop-color="{ROD_TOP}"/></linearGradient>')

    # The wireframe's edge: warmest where the key light would have struck it.
    a(f'<linearGradient id="edge" x1="0.1" y1="0" x2="0.9" y2="1">'
      f'<stop offset="0" stop-color="{ACCENT_CORE}"/>'
      f'<stop offset="0.42" stop-color="{ACCENT_MID}"/>'
      f'<stop offset="1" stop-color="{ACCENT_EDGE}"/></linearGradient>')

    # A ring, not a fill. The interior of the hollow rod must stay porcelain:
    # an orange wash inside it reads as a full rod lit from within, which is
    # the opposite of what the object is for.
    a(f'<radialGradient id="emberhalo" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{ACCENT_MID}" stop-opacity="0"/>'
      f'<stop offset="0.52" stop-color="{ACCENT_MID}" stop-opacity="0"/>'
      f'<stop offset="0.70" stop-color="{ACCENT_MID}" stop-opacity="0.20"/>'
      f'<stop offset="1" stop-color="{ACCENT_MID}" stop-opacity="0"/>'
      f'</radialGradient>')

    a('<filter id="soft" x="-40%" y="-40%" width="180%" height="180%">'
      '<feGaussianBlur stdDeviation="14"/></filter>')
    a('<filter id="tight" x="-40%" y="-40%" width="180%" height="180%">'
      '<feGaussianBlur stdDeviation="5"/></filter>')

    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a("</defs>")

    # --------------------------------------------------------------- ground
    a('<g clip-path="url(#tile)">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#key)"/>')

    a(f'<g transform="translate(0,{-OPTICAL_LIFT})">')

    # ------------------------------------------------------- contact shadows
    # Drawn first, all of them behind every rod. The hollow rod is absent from
    # this loop, and that absence is the whole idea: no light has reached it,
    # so it has left nothing behind.
    for i in range(COUNT):
        if i == HOLLOW_INDEX:
            continue
        x = LEFT_X + i * (ROD_W + GAP)
        a(f'<ellipse cx="{x + ROD_W * 0.72:.1f}" cy="{FLOOR_Y + 12:.1f}" '
          f'rx="{ROD_W * 0.92:.1f}" ry="20" fill="{WARM_SHADOW}" '
          f'opacity="0.30" filter="url(#soft)"/>')
        a(f'<ellipse cx="{x + ROD_W * 0.60:.1f}" cy="{FLOOR_Y + 6:.1f}" '
          f'rx="{ROD_W * 0.54:.1f}" ry="11" fill="{WARM_SHADOW}" '
          f'opacity="0.44" filter="url(#tight)"/>')

    # ----------------------------------------------------------- solid rods
    for i in range(COUNT):
        if i == HOLLOW_INDEX:
            continue
        x = LEFT_X + i * (ROD_W + GAP)
        a(f'<path d="{rod_path(x, TOP_Y, ROD_W, ROD_H, ROD_R)}" '
          f'fill="url(#rodface)"/>')
        # Cap: the ellipse of the rod's top, catching the key light.
        a(f'<ellipse cx="{x + ROD_W / 2:.1f}" cy="{TOP_Y + ROD_R * 0.42:.1f}" '
          f'rx="{ROD_W / 2 - 3:.1f}" ry="{ROD_R * 0.40:.1f}" '
          f'fill="url(#rodcap)"/>')
        # A narrow rim light down the left arris.
        a(f'<rect x="{x + 8:.1f}" y="{TOP_Y + ROD_R:.1f}" width="6" '
          f'height="{ROD_H - ROD_R * 2:.1f}" rx="3" fill="{TILE_RIM}" '
          f'opacity="0.26"/>')
        # The foot darkens where it meets the floor.
        a(f'<path d="{rod_path(x, TOP_Y, ROD_W, ROD_H, ROD_R)}" '
          f'fill="url(#rodfoot)"/>')

    # -------------------------------------------------------- the hollow rod
    hx = LEFT_X + HOLLOW_INDEX * (ROD_W + GAP)

    # A faint ember bloom around — never inside — the wireframe, so it reads
    # as warm rather than as a hole punched in the row. It sits behind the
    # edge and never touches the floor.
    a(f'<ellipse cx="{hx + ROD_W / 2:.1f}" cy="{TOP_Y + ROD_H / 2:.1f}" '
      f'rx="{ROD_W * 1.5:.1f}" ry="{ROD_H * 0.62:.1f}" '
      f'fill="url(#emberhalo)"/>')

    # The rod itself: edges only. Same path, same width, same footprint,
    # standing in the same row — everything the solid rods have except a
    # surface, and except a shadow.
    a(f'<path d="{rod_path(hx, TOP_Y, ROD_W, ROD_H, ROD_R)}" fill="none" '
      f'stroke="url(#edge)" stroke-width="15" stroke-linejoin="round"/>')
    # Its cap drawn as an open ellipse — you can see through it.
    a(f'<ellipse cx="{hx + ROD_W / 2:.1f}" cy="{TOP_Y + ROD_R * 0.42:.1f}" '
      f'rx="{ROD_W / 2 - 3:.1f}" ry="{ROD_R * 0.40:.1f}" fill="none" '
      f'stroke="url(#edge)" stroke-width="9" opacity="0.80"/>')

    a("</g>")
    a(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    # Tile rim: the porcelain edge catching the same key light.
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" '
      f'stroke-width="3" opacity="0.55"/>')
    a("</g>")
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    sys.stdout.write(build() + "\n")
