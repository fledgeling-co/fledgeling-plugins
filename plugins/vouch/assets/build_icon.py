#!/usr/bin/env python3
"""build_icon.py — the `vouch` icon: "The Tie-Back".

Porcelain cushion tile carrying one toy-scale object, matching the fledgeling
family: near-white cream ground, a slate object, and exactly one emissive accent.

Why this object. Vouching is the audit act of tracing a record back to the
document it came from. So the icon is a ledger row above, the source document
below, and a single lit filament running from the row down INTO the page, with
a bloom where it lands. The row and the page are ordinary slate; the only warm
thing on the tile is the connection, because the connection is the whole claim.

Separation from its nearest neighbour. `stocktake` is a card lifted clear of a
stack and backlit — one plane glowing, floating free, planes seen near-on. The
risk of collision was real and this is the answer to it: here nothing is lifted
and nothing floats. Both objects stay put, the accent is a LINE rather than a
plane, and the glow is a filament plus the point where it enters the page. Its
light source is inside the link, not behind an object.

One light, top-left, per the family. The cast shadows go warm; a cool shadow in
a warm scene is the tell the corpus corrects.

    python3 build_icon.py > icon.svg
"""
from __future__ import annotations
import pathlib, sys

S = 1024
SQUIRCLE = pathlib.Path(
    "~/.claude/plugins/cache/fledgeling-plugins/create-mac-icon/1.4.1/"
    "skills/create-mac-icon/assets/squircle-path.txt").expanduser()

# --- ground: the family porcelain, lifted verbatim from the siblings ----------
GROUND_TOP  = "#F8F5EE"
GROUND_BOT  = "#E4DDCB"
TILE_RIM    = "#FFFDF8"
VIGNETTE    = "#8A7A62"

# --- object: slate, two faces and an arris ------------------------------------
SLATE_FACE  = "#5A5449"
SLATE_TOP   = "#6E675A"
SLATE_DEEP  = "#3A342C"
SLATE_EDGE  = "#4A443A"
RULE_INK    = "#8E8677"
WARM_SHADOW = "#3E2A18"

# --- the one accent: the filament ---------------------------------------------
EMBER_CORE  = "#FFD9A8"
EMBER_EDGE  = "#DD6413"
EMBER_HALO  = "#FFB661"

# --- geometry (named so a later note is a one-constant change) -----------------
ROW_X, ROW_Y, ROW_W, ROW_H = 220, 232, 584, 104     # the ledger row
DOC_X, DOC_Y, DOC_W, DOC_H = 276, 556, 472, 288     # the source document
DOC_FOLD   = 74                                      # folded corner, top-right
THREAD_X   = 512                                     # the filament, dead centre
THREAD_TOP = ROW_Y + ROW_H
THREAD_BOT = DOC_Y + 96                              # it lands INSIDE the page
THREAD_W   = 26                                      # survives 16px: 0.41px at 16
BLOOM_R    = 168


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def slab(x, y, w, h, r=16):
    return (f'M{x+r},{y} h{w-2*r} a{r},{r} 0 0 1 {r},{r} v{h-2*r} '
            f'a{r},{r} 0 0 1 -{r},{r} h-{w-2*r} a{r},{r} 0 0 1 -{r},-{r} '
            f'v-{h-2*r} a{r},{r} 0 0 1 {r},-{r} z')


def page_with_fold(x, y, w, h, f, r=16):
    """A document: rounded except the top-right, which is cut back by the fold.

    The fold replaces the top-right ROUNDED corner entirely, so the top run is
    `w - r - f` rather than `w - 2r - f`: the corner it is standing in for costs
    nothing. Getting that wrong leaves the right edge short by one radius, and the
    closing arc then overshoots the start point and chamfers the top-LEFT corner —
    which is what it did, and it read as a defect at 256px rather than as geometry.
    """
    return (f'M{x+r},{y} h{w-r-f} l{f},{f} v{h-r-f} '
            f'a{r},{r} 0 0 1 -{r},{r} h-{w-2*r} a{r},{r} 0 0 1 -{r},-{r} '
            f'v-{h-2*r} a{r},{r} 0 0 1 {r},-{r} z')


def build() -> str:
    o = []; a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    a('<defs>')
    a(f'<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>')
    a(f'<radialGradient id="vig" cx="0.5" cy="0.44" r="0.72">'
      f'<stop offset="0.55" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.20"/></radialGradient>')
    a(f'<linearGradient id="slate" x1="0" y1="0" x2="0.28" y2="1">'
      f'<stop offset="0" stop-color="{SLATE_TOP}"/><stop offset="1" stop-color="{SLATE_FACE}"/></linearGradient>')
    a(f'<linearGradient id="slateDeep" x1="0" y1="0" x2="0.2" y2="1">'
      f'<stop offset="0" stop-color="{SLATE_FACE}"/><stop offset="1" stop-color="{SLATE_DEEP}"/></linearGradient>')
    a(f'<linearGradient id="thread" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{EMBER_EDGE}"/>'
      f'<stop offset="0.34" stop-color="{EMBER_CORE}"/>'
      f'<stop offset="1" stop-color="{EMBER_EDGE}"/></linearGradient>')
    a(f'<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{EMBER_HALO}" stop-opacity="0.92"/>'
      f'<stop offset="0.42" stop-color="{EMBER_HALO}" stop-opacity="0.34"/>'
      f'<stop offset="1" stop-color="{EMBER_HALO}" stop-opacity="0"/></radialGradient>')
    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a('</defs>')

    a('<g clip-path="url(#tile)">')
    a('<g id="bg">')
    a(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    a('</g>')

    a('<g id="mid">')
    # warm contact shadows, offset down-right from the top-left key
    a(f'<path d="{slab(ROW_X+12, ROW_Y+20, ROW_W, ROW_H)}" fill="{WARM_SHADOW}" opacity="0.16"/>')
    a(f'<path d="{page_with_fold(DOC_X+14, DOC_Y+22, DOC_W, DOC_H, DOC_FOLD)}" '
      f'fill="{WARM_SHADOW}" opacity="0.18"/>')

    a('</g>')

    a('<g id="fg">')
    # the ledger row, with its ruled entries
    a(f'<path d="{slab(ROW_X, ROW_Y, ROW_W, ROW_H)}" fill="url(#slate)"/>')
    for i, (dx, w) in enumerate(((44, 268), (44, 150))):
        a(f'<rect x="{ROW_X+dx}" y="{ROW_Y+34+i*26}" width="{w}" height="10" rx="5" '
          f'fill="{RULE_INK}" opacity="{0.95 - i*0.20:.2f}"/>')

    # fg — the source document, fold rendered as a darker triangle
    a(f'<path d="{page_with_fold(DOC_X, DOC_Y, DOC_W, DOC_H, DOC_FOLD)}" fill="url(#slateDeep)"/>')
    a(f'<path d="M{DOC_X+DOC_W-DOC_FOLD},{DOC_Y} l{DOC_FOLD},{DOC_FOLD} h-{DOC_FOLD} z" '
      f'fill="{SLATE_TOP}" opacity="0.95"/>')
    for i in range(3):
        a(f'<rect x="{DOC_X+52}" y="{DOC_Y+150+i*36}" width="{[300,244,188][i]}" height="10" rx="5" '
          f'fill="{RULE_INK}" opacity="{0.44 - i*0.10:.2f}"/>')

    # accent — the bloom where the filament lands, then the filament itself
    a(f'<circle cx="{THREAD_X}" cy="{THREAD_BOT}" r="{BLOOM_R}" fill="url(#bloom)"/>')
    a(f'<rect x="{THREAD_X - THREAD_W//2}" y="{THREAD_TOP - 10}" width="{THREAD_W}" '
      f'height="{THREAD_BOT - THREAD_TOP + 10}" rx="{THREAD_W//2}" fill="url(#thread)"/>')
    a(f'<circle cx="{THREAD_X}" cy="{THREAD_BOT}" r="{THREAD_W*0.86:.0f}" fill="{EMBER_CORE}"/>')

    a('</g>')

    a('<g id="highlight">')
    # rim light on the lit edges only, and the tile's own rim
    a(f'<rect x="{ROW_X+18}" y="{ROW_Y+6}" width="{ROW_W-36}" height="7" rx="3.5" '
      f'fill="{TILE_RIM}" opacity="0.30"/>')
    a(f'<rect x="{DOC_X+34}" y="{DOC_Y+9}" width="{DOC_W-DOC_FOLD-84}" height="6" rx="3" '
      f'fill="{TILE_RIM}" opacity="0.20"/>')
    a('</g>')
    a('</g>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" stroke-opacity="0.55" stroke-width="3"/>')
    a('</svg>')
    return "\n".join(o)


if __name__ == '__main__':
    sys.stdout.write(build() + "\n")
