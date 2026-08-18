#!/usr/bin/env python3
"""build_icon_A2.py — the second hand-authored take: "The Wide File".

Engine B (Arrow, `svg: true`) refused on 19 Aug 2026 with "A positive credit
balance is required for all requests, including BYOK", so the pipeline's
media-gen-pro vector lane did not run. The skill's stated fallback is to widen
Engine A rather than to present one take as three, and this is that widening: a
genuinely different hand-authored take on the same committed idea, briefed
against the two liabilities the master's own audit sheet measured.

What differs from the master, and why each difference is there:

1. The focal group is re-proportioned INTO the composition band. Cards 560x72
   fanned 40px per row give a group 640px wide and 651px tall — 62.5% and 63.6%
   of the tile, against the master's 37.9% solid / 51.2% with halo and 57.2%.
   The master's own sheet names scaling the group while keeping the gap
   proportional as the obvious first experiment; this is it, and the fan is
   scaled with the card (40/560 = 7.1%, against the master's 24/340 = 7.1%) so
   the filed-paper read is preserved rather than diluted.

2. The lit plane is value-carried, not outline-carried. The master's lifted card
   fills at 1.23:1 against the ground and depends entirely on a 7px edge stroke
   that thins with the icon. Here the gradient carries stop-opacity: opaque
   through the upper two thirds, falling to 0.72 only in the lower third, so the
   spill still reads through where it matters and the card separates by fill
   everywhere else. Its rim is #C4622D, the family's anchor ember, darker than
   the master's #DD6413 and therefore a wider gap against porcelain.

3. Each filed card carries a bright lit arris (#EFE7D6) instead of a dark cap.
   Filed paper edges do catch a key light, and this is the half of the identity
   that survives a ground swap: under a dark ground the three dark faces
   collapse toward the ground while three bright edges keep drawing three lines.
   That is a #10 argument made in shape and value rather than in colour.

4. The lifted card is tilted -4 degrees about its own centre, so it reads as
   held rather than hovering, and its cast shadow on the top card's face is
   skewed to match. The tilt is the reason this is a different take and not a
   scale parameter: at 16px it is a non-parallel warm plane over parallel dark
   bars, which is a different silhouette read from the master's stack of
   parallels.

What is unchanged, deliberately: the subject (a column of filed cards low, one
card taken out and held high, the air between them as the subject), the
porcelain ground constants, the single light behind and above the lifted card,
the warm cast shadow, and the bg / mid / fg / highlight layer plan.

    python3 build_icon_A2.py > icon-A2-wide.svg
"""
from __future__ import annotations
import pathlib, sys

S = 1024
SQUIRCLE = (pathlib.Path(__file__).resolve().parents[2]
            / "create-mac-icon" / "assets" / "squircle-path.txt")

# Family ground, lifted verbatim from the master. A second take differentiates on
# composition and material, never on the house ground register.
GROUND_TOP  = "#F8F5EE"
GROUND_BOT  = "#E4DDCB"
TILE_RIM    = "#FFFDF8"
VIGNETTE    = "#8A7A62"

CARD_FACE   = "#5A5449"
CARD_ARRIS  = "#EFE7D6"   # the key light on a paper edge — bright, not a dark cap
CARD_DEEP   = "#221E18"
WARM_SHADOW = "#3E2A18"

LIT_TOP     = "#FFE2B6"
LIT_MID     = "#F6B274"
LIT_BOT     = "#E38C3C"
EMBER       = "#C4622D"   # the family anchor accent
SPILL       = "#FFB661"

# Geometry. Every number here is chosen against the 1024 canvas so the group
# lands inside the 55-65% composition band on BOTH axes.
CW, CH, FAN, PITCH, CX = 560, 72, 40, 84, 232
COL_TOP = 592                     # first filed card's top edge
LW, LH, LY = 544, 172, 200        # the lifted card
TILT = -4                         # degrees, about the lifted card's own centre


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def card(x, y, w, h, r=22):
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
    # Light spill on the porcelain, not the card's identity. Smaller than the
    # master's halo (rx 320/ry 200 against 262/224) because nothing below depends
    # on it: drop this ellipse and the lifted card still reads by fill.
    a(f'<radialGradient id="spill" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{SPILL}" stop-opacity="0.62"/>'
      f'<stop offset="0.44" stop-color="{SPILL}" stop-opacity="0.24"/>'
      f'<stop offset="1" stop-color="{SPILL}" stop-opacity="0"/></radialGradient>')
    # stop-opacity is what makes this take's lit plane value-carried: opaque
    # through the upper two thirds, translucent only in the lower third.
    a(f'<linearGradient id="lit" x1="0.08" y1="0" x2="0.22" y2="1">'
      f'<stop offset="0" stop-color="{LIT_TOP}" stop-opacity="1"/>'
      f'<stop offset="0.58" stop-color="{LIT_MID}" stop-opacity="1"/>'
      f'<stop offset="1" stop-color="{LIT_BOT}" stop-opacity="0.72"/></linearGradient>')
    # A cast shadow with a hard edge reads as a stain on the card rather than as
    # light being blocked. rsvg renders feGaussianBlur inconsistently across
    # versions, so the falloff is a radial gradient instead of a filter.
    a(f'<radialGradient id="cast" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{WARM_SHADOW}" stop-opacity="0.40"/>'
      f'<stop offset="0.55" stop-color="{WARM_SHADOW}" stop-opacity="0.26"/>'
      f'<stop offset="1" stop-color="{WARM_SHADOW}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="vig" cx="0.5" cy="0.5" r="0.72">'
      f'<stop offset="0.62" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.20"/></radialGradient>')
    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a('</defs>')

    a('<g id="art" clip-path="url(#tile)">')
    a('<g id="bg">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a(f'<ellipse cx="512" cy="300" rx="320" ry="200" fill="url(#spill)"/>')
    a('</g>')

    a('<g id="mid">')
    for i in range(3):
        x = CX + (i - 1) * FAN
        top = COL_TOP + i * PITCH
        a(f'<path d="{card(x, top + 10, CW, CH)}" fill="{CARD_DEEP}" opacity="0.42"/>')
        a(f'<path d="{card(x, top, CW, CH)}" fill="{CARD_FACE}"/>')
        a(f'<path d="{card(x + 12, top + 4, CW - 24, 10, 5)}" fill="{CARD_ARRIS}" opacity="0.82"/>')

    # Skewed to the tilt of the card casting it, and landing on the top card's
    # face (y 592-664) rather than behind the column.
    a(f'<ellipse cx="498" cy="622" rx="200" ry="26" fill="url(#cast)" '
      f'transform="rotate({TILT} 498 622)"/>')
    a('</g>')

    a('<g id="fg">')
    LX = 512 - LW // 2
    a(f'<g transform="rotate({TILT} 512 {LY + LH // 2})">')
    a(f'<path d="{card(LX, LY, LW, LH, 28)}" fill="url(#lit)"/>')
    a(f'<path d="{card(LX, LY, LW, LH, 28)}" fill="none" stroke="{EMBER}" stroke-width="8"/>')
    a(f'<rect x="{LX+52}" y="{LY+54}" width="{LW-236}" height="11" rx="5.5" fill="{EMBER}" opacity="0.30"/>')
    a(f'<rect x="{LX+52}" y="{LY+96}" width="{LW-356}" height="11" rx="5.5" fill="{EMBER}" opacity="0.20"/>')
    a('</g>')
    a('</g>')

    a('<g id="highlight">')
    a(f'<path d="{squircle()}" fill="url(#vig)"/>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" stroke-width="3" opacity="0.8"/>')
    a('</g>')
    a('</g></svg>')
    return "\n".join(o)


if __name__ == "__main__":
    sys.stdout.write(build())
