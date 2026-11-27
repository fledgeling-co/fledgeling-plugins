#!/usr/bin/env python3
"""build_icon.py — the `changelog` icon: "The Open Ring".

Porcelain cushion tile carrying one toy-scale object, in the fledgeling set's
register (create-mac-icon direction 2a, porcelain + gel object): a timeline
spine. A graphite rail runs top to bottom; four markers sit on it, each with a
porcelain entry card beside it. The three older markers are closed graphite
beads. The newest, at the top, is an open ember ring.

Why this object. It is the changelog page's own device: the timeline rail the
page draws down its left side, where a closed dot means an entry has nothing
remaining and an open ring means work is still to do. The skill keeps a record
newest first, so the newest entry is the top one, and it is usually the one
still in progress.

Signature move: THE NEWEST MARKER IS OPEN, AND IT IS THE ONLY LIGHT. Finished
entries are closed and cold; the one at the top is a ring rather than a bead,
larger than the rest and standing proud of the rail, and it is the only ember on
the tile. The record's whole claim, that what is done stays done and the newest
entry is still being written, is the difference between a bead and a ring.

Separation from its nearest neighbours. `agent-voice` and `report` are flat
cards of horizontal rules, seen face-on; this is a vertical rail with objects
standing on it. `reckon` is a row of uprights; `test-campaign`'s bars rise from
a baseline. Nothing else in the set is a vertical line of markers.

One light, upper left. Beads are lit spheres with a specular point upper left;
cards ramp lit-left to shaded-right; every shadow is warm and falls lower
right. Material values are the family's, which `status-update`'s build script
sampled from references/corpus/apple-2026/ (apple-05, apple-06, apple-18):
warm-brown dark faces rather than neutral black, a contact shadow only ~13%
darker than the ground, and an emissive amber palest at its core.

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
WARM_SHADOW = "#3E2A18"

G_HI = "#8A8273"         # a bead's lit cap
G_TOP = "#6E675A"
G_LIT = "#5A5449"
G_SHADE = "#332E27"
G_DEEP = "#221E18"

CARD_HI = "#FFFDF8"
CARD_MID = "#F3EDE1"
CARD_LO = "#E2D9C7"
CARD_EDGE = "#CFC4AE"

EMBER_DEEP = "#BC3A14"
EMBER = "#DE5A28"
EMBER_MID = "#F58F4A"
EMBER_HI = "#FFB661"
EMBER_CORE = "#FFD9A8"

# --- geometry -------------------------------------------------------------
RAIL_X = 352.0           # the spine's centre line
RAIL_W = 30.0
RAIL_Y0, RAIL_Y1 = 236.0, 800.0

ROWS = [300.0, 444.0, 588.0, 732.0]          # marker centres, newest first
BEAD_R = 36.0            # a closed, finished entry
RING_R = 64.0            # the open one: 1.8x a bead, so it leads at every size
RING_W = 30.0            # ring thickness
RING_PROUD = (-6.0, -4.0)   # nearer the viewer: up and left, toward the key

CARD_X0 = 440.0
CARD_X1 = [790.0, 726.0, 756.0, 690.0]       # ragged right edge, like real entries
CARD_H = 70.0
CARD_R = 22.0


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


def build() -> str:
    o: list[str] = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')

    # ---------------------------------------------------------------- defs
    a("<defs>")
    a(f'<linearGradient id="ground" x1="0" y1="0" x2="0.18" y2="1">'
      f'<stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>')
    a('<radialGradient id="key" cx="0.30" cy="0.18" r="0.86">'
      '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.60"/>'
      '<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.11"/>'
      '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.76">'
      f'<stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/></radialGradient>')

    # The rail: a graphite rod, lit along its left flank.
    a(f'<linearGradient id="rail" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{G_TOP}"/><stop offset="0.35" stop-color="{G_LIT}"/>'
      f'<stop offset="0.8" stop-color="{G_SHADE}"/><stop offset="1" stop-color="{G_DEEP}"/></linearGradient>')

    # A finished bead: a lit sphere, cap upper left, core falling to warm-brown.
    a(f'<radialGradient id="bead" cx="0.36" cy="0.32" r="0.72">'
      f'<stop offset="0" stop-color="{G_HI}"/><stop offset="0.38" stop-color="{G_LIT}"/>'
      f'<stop offset="0.82" stop-color="{G_SHADE}"/><stop offset="1" stop-color="{G_DEEP}"/></radialGradient>')

    # The open ring: an emissive ember torus, hottest at its lit upper-left.
    a(f'<linearGradient id="ring" x1="0.15" y1="0.1" x2="0.85" y2="0.95">'
      f'<stop offset="0" stop-color="{EMBER_HI}"/><stop offset="0.35" stop-color="{EMBER_MID}"/>'
      f'<stop offset="0.7" stop-color="{EMBER}"/><stop offset="1" stop-color="{EMBER_DEEP}"/></linearGradient>')
    a(f'<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{EMBER_HI}" stop-opacity="0.42"/>'
      f'<stop offset="0.55" stop-color="{EMBER}" stop-opacity="0.14"/>'
      f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>')

    # A porcelain entry card, raised off the ground: lit left, shaded right.
    a(f'<linearGradient id="card" x1="0" y1="0" x2="1" y2="0.6">'
      f'<stop offset="0" stop-color="{CARD_HI}"/><stop offset="0.55" stop-color="{CARD_MID}"/>'
      f'<stop offset="1" stop-color="{CARD_LO}"/></linearGradient>')
    a(f'<linearGradient id="rim" x1="0" y1="0" x2="0.7" y2="1">'
      f'<stop offset="0" stop-color="{TILE_RIM}" stop-opacity="0.85"/>'
      f'<stop offset="0.5" stop-color="{TILE_RIM}" stop-opacity="0.2"/>'
      f'<stop offset="1" stop-color="{TILE_RIM}" stop-opacity="0"/></linearGradient>')

    a('<filter id="soft" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="20"/></filter>')
    a('<filter id="mid" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="9"/></filter>')
    a('<filter id="tight" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="3.5"/></filter>')
    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a("</defs>")

    a('<g clip-path="url(#tile)">')

    # ================================================================= bg
    a('<g id="bg">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#key)"/>')
    a("</g>")

    # ================================================================ mid
    a('<g id="mid">')
    # Contact shadows: one long pool under the rail, one under each card. Warm,
    # offset lower right, soft pool plus a tighter core.
    a(f'<path d="{rrect(RAIL_X - 10, RAIL_Y0 + 30, RAIL_X + 34, RAIL_Y1 + 18, 22)}" '
      f'fill="{WARM_SHADOW}" opacity="0.20" filter="url(#soft)"/>')
    for y, x1 in zip(ROWS, CARD_X1):
        a(f'<path d="{rrect(CARD_X0 + 10, y - CARD_H / 2 + 14, x1 + 14, y + CARD_H / 2 + 16, CARD_R)}" '
          f'fill="{WARM_SHADOW}" opacity="0.18" filter="url(#soft)"/>')
        a(f'<path d="{rrect(CARD_X0 + 4, y - CARD_H / 2 + 6, x1 + 6, y + CARD_H / 2 + 6, CARD_R)}" '
          f'fill="{WARM_SHADOW}" opacity="0.20" filter="url(#mid)"/>')
    # The ring's light lands on the ground and on the card beside it.
    rx, ry = RAIL_X + RING_PROUD[0], ROWS[0] + RING_PROUD[1]
    a(f'<ellipse cx="{rx + 60:.1f}" cy="{ry + 10:.1f}" rx="230" ry="150" fill="url(#bloom)"/>')
    a("</g>")

    # ================================================================= fg
    a('<g id="fg">')
    # Entry cards.
    for i, (y, x1) in enumerate(zip(ROWS, CARD_X1)):
        a(f'<path d="{rrect(CARD_X0, y - CARD_H / 2 + 4, x1, y + CARD_H / 2 + 4, CARD_R)}" fill="{CARD_EDGE}"/>')
        a(f'<path d="{rrect(CARD_X0, y - CARD_H / 2, x1, y + CARD_H / 2, CARD_R)}" fill="url(#card)"/>')
        # One line of "text" on each card, graphite, two-thirds of its width.
        tw = (x1 - CARD_X0) * (0.62 if i else 0.70)
        a(f'<path d="{rrect(CARD_X0 + 26, y - 7, CARD_X0 + 26 + tw, y + 7, 7)}" fill="{G_SHADE}" opacity="0.55"/>')
    # The newest card catches the ring's warmth along its left end.
    a(f'<clipPath id="newest"><path d="{rrect(CARD_X0, ROWS[0] - CARD_H / 2, CARD_X1[0], ROWS[0] + CARD_H / 2, CARD_R)}"/></clipPath>')
    a(f'<ellipse cx="{CARD_X0:.1f}" cy="{ROWS[0]:.1f}" rx="150" ry="70" fill="url(#bloom)" clip-path="url(#newest)"/>')

    # The rail.
    a(f'<path d="{rrect(RAIL_X - RAIL_W / 2, RAIL_Y0, RAIL_X + RAIL_W / 2, RAIL_Y1, RAIL_W / 2)}" fill="url(#rail)"/>')

    # The rail's lit left flank, drawn before the beads so it passes behind them.
    a(f'<path d="M{RAIL_X - RAIL_W / 2 + 5:.1f},{RAIL_Y0 + 20:.1f} L{RAIL_X - RAIL_W / 2 + 5:.1f},{RAIL_Y1 - 30:.1f}" '
      f'stroke="{TILE_RIM}" stroke-width="3" stroke-linecap="round" opacity="0.22"/>')

    # Finished entries: closed beads, each with its own small shadow on the rail.
    for y in ROWS[1:]:
        a(f'<circle cx="{RAIL_X + 8:.1f}" cy="{y + 10:.1f}" r="{BEAD_R:.1f}" fill="{WARM_SHADOW}" opacity="0.30" filter="url(#mid)"/>')
        a(f'<circle cx="{RAIL_X:.1f}" cy="{y:.1f}" r="{BEAD_R:.1f}" fill="url(#bead)"/>')

    # The open entry: an ember ring standing proud of the rail.
    a(f'<circle cx="{rx + 10:.1f}" cy="{ry + 14:.1f}" r="{RING_R:.1f}" fill="none" stroke="{WARM_SHADOW}" '
      f'stroke-width="{RING_W:.1f}" opacity="0.28" filter="url(#mid)"/>')
    a(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{RING_R:.1f}" fill="none" stroke="url(#ring)" stroke-width="{RING_W:.1f}"/>')
    # Inner lip in shade, so the ring reads as a torus with a hole, not a flat stroke.
    a(f'<circle cx="{rx + 3:.1f}" cy="{ry + 3:.1f}" r="{RING_R - RING_W / 2 + 2:.1f}" fill="none" '
      f'stroke="{EMBER_DEEP}" stroke-width="5" opacity="0.55" filter="url(#tight)"/>')
    # The rail shows through the open centre: the entry is not closed yet.
    a("</g>")

    # ========================================================== highlight
    a('<g id="highlight">')
    for y in ROWS[1:]:
        a(f'<ellipse cx="{RAIL_X - 12:.1f}" cy="{y - 14:.1f}" rx="11" ry="7" fill="{TILE_RIM}" opacity="0.55" '
          f'transform="rotate(-30 {RAIL_X - 12:.1f} {y - 14:.1f})"/>')
    # Specular arc on the ring's lit upper-left, where the key meets the torus.
    a(f'<path d="M{rx - RING_R * 0.82:.1f},{ry - RING_R * 0.20:.1f} A{RING_R:.1f},{RING_R:.1f} 0 0 1 '
      f'{rx - RING_R * 0.10:.1f},{ry - RING_R * 0.85:.1f}" fill="none" stroke="{EMBER_CORE}" '
      f'stroke-width="8" stroke-linecap="round" opacity="0.85"/>')
    # Rim light along each card's top-left arris and the rail's left flank.
    for y, x1 in zip(ROWS, CARD_X1):
        a(f'<path d="{rrect(CARD_X0 + 1.5, y - CARD_H / 2 + 1.5, x1 - 1.5, y + CARD_H / 2 - 1.5, CARD_R - 1.5)}" '
          f'fill="none" stroke="url(#rim)" stroke-width="2.5"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" stroke-width="3" opacity="0.55"/>')
    a("</g>")

    a("</g>")
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    sys.stdout.write(build() + "\n")
