#!/usr/bin/env python3
"""build_icon.py — the `stocktake` icon: "The Card Held to the Light".

Porcelain cushion tile carrying one toy-scale object, per create-mac-icon's
icon-directions: a short column of filed cards with ONE card lifted clear of it
and lit from behind, so that card alone is translucent and saturated.

Why this object. The skill's claim is that a board is a set of assertions nobody
checks, and that checking means taking one out and holding it up. The column is
the board — orderly, uniform, unexamined. The lifted card is the act. It is the
only warm thing on the tile because it is the only thing that has been looked at.

Signature move: the lifted card is TRANSLUCENT and the column is opaque. Same
width, same corner radius, same silhouette — one has been put under a light and
the others have not. Nothing else in this marketplace has a backlit plane above
an opaque stack.

Separation from its nearest neighbour: `whats-left` is a warm keystone hanging
clear of a dark arch — an extruded solid with a hole through it. This is flat
planes seen near-on, and its accent GLOWS rather than reflects.

One light, behind and above the lifted card. The column's top arrises catch it
and their faces fall away; the cast shadow goes warm, because a blue shadow in a
warm scene is the tell.

    python3 build_icon.py > icon.svg
"""
from __future__ import annotations
import pathlib, sys

S = 1024
SQUIRCLE = (pathlib.Path(__file__).resolve().parents[2]
            / "create-mac-icon" / "assets" / "squircle-path.txt")

GROUND_TOP  = "#F8F5EE"
GROUND_BOT  = "#E4DDCB"
TILE_RIM    = "#FFFDF8"
VIGNETTE    = "#8A7A62"

CARD_FACE   = "#5A5449"
CARD_TOP    = "#6E675A"
CARD_DEEP   = "#221E18"
WARM_SHADOW = "#3E2A18"

GLOW_CORE   = "#FFD9A8"
GLOW_EDGE   = "#DD6413"
GLOW_HALO   = "#FFB661"


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def card(x, y, w, h, r=14):
    return (f'M{x+r},{y} h{w-2*r} a{r},{r} 0 0 1 {r},{r} v{h-2*r} '
            f'a{r},{r} 0 0 1 -{r},{r} h-{w-2*r} a{r},{r} 0 0 1 -{r},-{r} '
            f'v-{h-2*r} a{r},{r} 0 0 1 {r},-{r} z')


def build() -> str:
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    a('<defs>')
    a(f'<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>')
    a(f'<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{GLOW_HALO}" stop-opacity="0.80"/>'
      f'<stop offset="0.46" stop-color="{GLOW_HALO}" stop-opacity="0.30"/>'
      f'<stop offset="1" stop-color="{GLOW_HALO}" stop-opacity="0"/></radialGradient>')
    a(f'<linearGradient id="lit" x1="0.1" y1="0" x2="0.9" y2="1">'
      f'<stop offset="0" stop-color="#FFE3B4"/>'
      f'<stop offset="0.5" stop-color="{GLOW_CORE}"/>'
      f'<stop offset="1" stop-color="#EC9A4A"/></linearGradient>')
    a(f'<radialGradient id="vig" cx="0.5" cy="0.5" r="0.72">'
      f'<stop offset="0.62" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.20"/></radialGradient>')
    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a('</defs>')

    a('<g clip-path="url(#tile)">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a('<ellipse cx="512" cy="378" rx="262" ry="224" fill="url(#halo)"/>')

    # The column sits LOW and the lifted card sits HIGH, because the gap between
    # them is the subject. A card resting flush on the stack reads as the top of
    # the stack; a card with air under it reads as having been taken out.
    #
    # The cards fan by FAN px per row so the column reads as filed paper rather
    # than as three identical bars — which is what an evenly stacked set becomes
    # at 64px, and it looked like a server rack.
    CW, CH, CX, FAN = 340, 62, 342, 24
    for i, top in enumerate((672, 748, 824)):
        x = CX + (i - 1) * FAN
        a(f'<path d="{card(x, top + 9, CW, CH)}" fill="{CARD_DEEP}" opacity="0.40"/>')
        a(f'<path d="{card(x, top, CW, CH)}" fill="{CARD_FACE}"/>')
        a(f'<path d="{card(x + 6, top + 3, CW - 12, 11, 5.5)}" fill="{CARD_TOP}" opacity="0.85"/>')

    # The cast shadow lands ON the face of the top card, not behind it, so the
    # air under the lifted card is visible rather than implied.
    a(f'<ellipse cx="500" cy="700" rx="118" ry="14" fill="{WARM_SHADOW}" opacity="0.38"/>')

    LX, LY, LW, LH = CX + 4, 300, CW - 8, 168
    # Translucent, not opaque: the halo behind reads through the lower half, which
    # is the whole difference between this card and the ones it came from.
    a(f'<path d="{card(LX, LY, LW, LH, 18)}" fill="url(#lit)" opacity="0.97"/>')
    a(f'<path d="{card(LX, LY, LW, LH, 18)}" fill="none" stroke="{GLOW_EDGE}" stroke-width="7"/>')
    a(f'<rect x="{LX+34}" y="{LY+52}" width="{LW-150}" height="9" rx="4.5" fill="{GLOW_EDGE}" opacity="0.34"/>')
    a(f'<rect x="{LX+34}" y="{LY+88}" width="{LW-230}" height="9" rx="4.5" fill="{GLOW_EDGE}" opacity="0.22"/>')

    a(f'<path d="{squircle()}" fill="url(#vig)"/>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" stroke-width="3" opacity="0.8"/>')
    a('</g></svg>')
    return "\n".join(o)


if __name__ == "__main__":
    sys.stdout.write(build())
