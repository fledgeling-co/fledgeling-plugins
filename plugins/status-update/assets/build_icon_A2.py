#!/usr/bin/env python3
"""build_icon_A2.py — take A2: "The Split-Flap Cell (Two-Bar Front-Facing)".

Porcelain cushion tile carrying one toy-scale object, per create-mac-icon's
icon-directions (direction 2a, porcelain + gel object, Tahoe-softened
3D-miniature): a split-flap status board caught in the act of correcting
itself. One settled row sits cold at the top. Below it, a single flap has
fallen off its hinge line and juts forward toward the viewer, and the row it is
uncovering burns warm behind it.

Why this object. A split-flap board is the status display that stays on the
wall: everyone reads the same one, and it is re-read rather than scrolled past.
That is the skill's whole claim — Claude's status update runs long and scrolls
away, so this replaces it with two pages that stay put. And a split-flap board
is the only public display whose defining behaviour is retracting what it said
a moment ago, in front of everyone, and putting something else there.

Signature move: THE CORRECTION IS GIVEN MORE ROOM THAN THE CLAIM, and it is the
only lit thing on the board. The settled row is 112 tall and unlit. The
aperture below it is 188 — 1.68x — and it is where all the light is. That
proportion is the skill's founding measurement: nine independent mining passes
over 2,400 real status reports each reported that the section correcting an
earlier claim gets more room than the wins. Everything the board already said
sits in flat graphite; the one line it is taking back carries the ember.

Second move, and the reason the silhouette is not a rectangle: the flap
overhangs the board's left and right edges by 24. It is nearer the viewer, so
perspective makes it wider than the aperture it came out of — the correction
does not fit inside the thing it corrects.

Separation from its nearest neighbours. `report` is a flat dark card of rules
with an ember rule through it, seen face-on; this is a machine with a moving
part, a real extrusion and a contact shadow. `email-digest` is a full-bleed
dark tile with ember bars; this is a graphite object floating on porcelain.
`should-compact` is two slabs meeting at an ember seam — a join, held still.
`reckon` is a row of uprights. Nothing else in the set has a plane that has
left the plane of its own face.

One light, upper left and slightly forward, plus the one sanctioned second
light: an emissive interior under the flap (icon-directions device #22). Board
faces ramp lit-left to shaded-right, the extrusion's top face catches the key,
and every shadow is warm — a blue shadow in a warm scene is the tell.

Material sampled from references/corpus/apple-2026/ rather than assumed:
apple-05 (Infuse) for the fold, whose inner face is both DARKER and REDDER than
its lit faces (#D93922 against #ED712E / #EF9937) — so the flap's edge thickness
here is warm-brown, not neutral-black; apple-18 for the toy-on-porcelain
treatment, whose contact shadow is a soft pool with a brighter bounce streak
beside it, only ~13% darker than the ground rather than a hard blob; apple-06
(Home) for an amber interior reading as backlit, palest at the core.

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

# Warm graphite ramp — the same one `reckon` and `report` stand their objects
# in, so this board is made of the family's material.
G_TOP = "#6E675A"        # the extrusion's top face, square to the key
G_LIT = "#5A5449"        # front face, left
G_SHADE = "#332E27"      # front face, right
G_DEEP = "#221E18"       # the arris at the foot
G_WELL = "#17130F"       # inside the settled recess: no light gets in

FLAP_LIT = "#7C7466"     # the flap tilts UP toward the key, so it is the
FLAP_MID = "#5E5749"     # brightest graphite on the tile
FLAP_SHADE = "#3B352C"
FLAP_EDGE = "#2E241A"    # its own thickness — warm-brown per apple-05, not black

# The one ember. Family-standard hexes.
EMBER_DEEP = "#BC3A14"
EMBER = "#DE5A28"
EMBER_MID = "#F58F4A"
EMBER_HI = "#FFB661"
EMBER_CORE = "#FFD9A8"

# --- geometry -------------------------------------------------------------
# Board front face. 552 wide = 54% of the tile, inside the 55-65% composition
# constant once the flap's overhang is counted.
BX0, BX1 = 236.0, 788.0
BY0, BY1 = 298.0, 720.0
BR = 46.0                # face corner radius; concentric with the tile's

EDX, EDY = 44.0, -30.0   # extrusion: the body sits up and to the right, so the
                         # top face is lit and the right face falls away

INSET = 40.0             # rows are inset from the face edge by this
RX0, RX1 = BX0 + INSET, BX1 - INSET

SETTLED_Y0, SETTLED_Y1 = 340.0, 452.0    # the claim: 112 tall, and unlit
APERTURE_Y0, APERTURE_Y1 = 478.0, 666.0  # the correction: 188 tall — 1.68x
HINGE_Y = 574.0                          # where the flap is hinged
FLAP_LEAD_Y = 650.0                      # its leading edge, 116 nearer the viewer
FLAP_OVERHANG = 0.0                     # past the board's edges, both sides

ROW_R = 14.0             # row corner radius


def squircle() -> str:
    return SQUIRCLE.read_text().strip()


def rrect(x0: float, y0: float, x1: float, y1: float, r: float) -> str:
    """Rounded rectangle as an explicit path, so every corner is a real arc."""
    w, h = x1 - x0, y1 - y0
    r = min(r, w / 2, h / 2)
    return (f"M{x0 + r:.1f},{y0:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} "
            f"v{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},{r:.1f} "
            f"h-{w - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 -{r:.1f},-{r:.1f} "
            f"v-{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},-{r:.1f} z")


def flap_path(shrink: float = 0.0, drop: float = 0.0) -> str:
    """The flap's visible top surface, as a trapezoid.

    Hinged along HINGE_Y and fallen forward, so in projection its leading edge
    is both lower and WIDER than its hinge edge. The widening is the whole
    argument: a correction that has left the plane of the board is nearer the
    viewer than the row it replaces, so it cannot be contained by it.
    """
    x0, x1 = RX0 + shrink, RX1 - shrink
    lx0 = BX0 - FLAP_OVERHANG + shrink
    lx1 = BX1 + FLAP_OVERHANG - shrink
    return (f"M{x0:.1f},{HINGE_Y + drop:.1f} L{x1:.1f},{HINGE_Y + drop:.1f} "
            f"L{lx1:.1f},{FLAP_LEAD_Y + drop:.1f} "
            f"L{lx0:.1f},{FLAP_LEAD_Y + drop:.1f} Z")


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

    # Key light pooling from the upper left. apple-05's porcelain runs #FFFFFF
    # at the top to #E8E7E8 at the foot — an 8-9% fall — with the brightest
    # point high. This is that fall, warmed to the family's cream.
    a(f'<radialGradient id="key" cx="0.30" cy="0.18" r="0.86">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.60"/>'
      f'<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.11"/>'
      f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')

    a(f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.76">'
      f'<stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/>'
      f'</radialGradient>')

    # The extruded body seen past the front face: its top edge takes the key,
    # its right edge falls away. One gradient does both faces.
    a(f'<linearGradient id="body" x1="0.1" y1="0" x2="1" y2="0.9">'
      f'<stop offset="0" stop-color="{G_TOP}"/>'
      f'<stop offset="0.38" stop-color="#4C463B"/>'
      f'<stop offset="1" stop-color="{G_DEEP}"/></linearGradient>')

    # The front face: lit left, falling away right, darkening at the foot.
    a(f'<linearGradient id="face" x1="0" y1="0.05" x2="1" y2="0.85">'
      f'<stop offset="0" stop-color="#645D4F"/>'
      f'<stop offset="0.34" stop-color="{G_LIT}"/>'
      f'<stop offset="0.78" stop-color="{G_SHADE}"/>'
      f'<stop offset="1" stop-color="{G_DEEP}"/></linearGradient>')

    # A recess under a top light is darkest at its own top edge, where the lip
    # overhangs it, and lifts very slightly toward the bottom.
    a(f'<linearGradient id="recess" x1="0" y1="0" x2="0.15" y2="1">'
      f'<stop offset="0" stop-color="{G_WELL}"/>'
      f'<stop offset="0.62" stop-color="#241F19"/>'
      f'<stop offset="1" stop-color="#2E2820"/></linearGradient>')

    # The uncovered row. The light is inside the machine, so it is hottest
    # deepest in — at the bottom of the band, hard against the hinge — and
    # falls off upward. apple-06's amber reads backlit for the same reason:
    # palest at the core, saturating outward.
    a(f'<linearGradient id="well" x1="0" y1="0" x2="0.08" y2="1">'
      f'<stop offset="0" stop-color="{EMBER_DEEP}"/>'
      f'<stop offset="0.30" stop-color="{EMBER}"/>'
      f'<stop offset="0.72" stop-color="{EMBER_MID}"/>'
      f'<stop offset="1" stop-color="{EMBER_CORE}"/></linearGradient>')

    # The flap's top surface. It has fallen forward, so it now faces up-and-out
    # and is the brightest graphite on the tile — brighter than the face it
    # came out of, which is what makes it read as having moved.
    a(f'<linearGradient id="flapface" x1="0.05" y1="0" x2="0.95" y2="0.75">'
      f'<stop offset="0" stop-color="{FLAP_LIT}"/>'
      f'<stop offset="0.42" stop-color="{FLAP_MID}"/>'
      f'<stop offset="1" stop-color="{FLAP_SHADE}"/></linearGradient>')

    # Ember bounce along the flap's hinge edge: the well is directly behind it.
    a(f'<linearGradient id="bounce" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{EMBER_HI}" stop-opacity="0.72"/>'
      f'<stop offset="0.5" stop-color="{EMBER}" stop-opacity="0.26"/>'
      f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>'
      f'</linearGradient>')

    a(f'<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{EMBER_HI}" stop-opacity="0.40"/>'
      f'<stop offset="0.55" stop-color="{EMBER}" stop-opacity="0.16"/>'
      f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>'
      f'</radialGradient>')

    a(f'<radialGradient id="floorpool" cx="0.5" cy="0.5" r="0.5">'
      f'<stop offset="0" stop-color="{EMBER_MID}" stop-opacity="0.30"/>'
      f'<stop offset="0.58" stop-color="{EMBER}" stop-opacity="0.10"/>'
      f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>'
      f'</radialGradient>')

    # Rim light: strongest at the top-left arris, gone by the lower right.
    a(f'<linearGradient id="rim" x1="0" y1="0" x2="0.7" y2="1">'
      f'<stop offset="0" stop-color="{TILE_RIM}" stop-opacity="0.55"/>'
      f'<stop offset="0.45" stop-color="{TILE_RIM}" stop-opacity="0.14"/>'
      f'<stop offset="1" stop-color="{TILE_RIM}" stop-opacity="0"/>'
      f'</linearGradient>')

    a('<filter id="soft" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="22"/></filter>')
    a('<filter id="mid" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="10"/></filter>')
    a('<filter id="tight" x="-45%" y="-45%" width="190%" height="190%">'
      '<feGaussianBlur stdDeviation="4"/></filter>')

    a(f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>')
    a(f'<clipPath id="aperture"><path d="'
      f'{rrect(RX0, APERTURE_Y0, RX1, APERTURE_Y1, ROW_R)}"/></clipPath>')
    a(f'<clipPath id="boardface"><path d="{rrect(BX0, BY0, BX1, BY1, BR)}"/>'
      f'</clipPath>')
    a("</defs>")

    a('<g clip-path="url(#tile)">')

    # ================================================================= bg
    a('<g id="bg">')
    a(f'<path d="{squircle()}" fill="url(#ground)"/>')
    a(f'<rect width="{S}" height="{S}" fill="url(#key)"/>')
    a("</g>")

    # ================================================================ mid
    a('<g id="mid">')

    # Contact shadow. Warm, offset to the lower right because the key is upper
    # left; a soft pool plus a tight core, per apple-18, where the pool is only
    # a shade darker than the porcelain rather than a hard blob.
    a(f'<ellipse cx="{(BX0 + BX1) / 2 + 26:.1f}" cy="{BY1 + 26:.1f}" '
      f'rx="{(BX1 - BX0) * 0.56:.1f}" ry="42" fill="{WARM_SHADOW}" '
      f'opacity="0.22" filter="url(#soft)"/>')
    a(f'<ellipse cx="{(BX0 + BX1) / 2 + 14:.1f}" cy="{BY1 + 10:.1f}" '
      f'rx="{(BX1 - BX0) * 0.46:.1f}" ry="18" fill="{WARM_SHADOW}" '
      f'opacity="0.36" filter="url(#mid)"/>')

    # The ember reaching the floor in front of the machine. The second light is
    # a real light, so it has to land somewhere.
    a(f'<ellipse cx="{(BX0 + BX1) / 2:.1f}" cy="{BY1 + 30:.1f}" '
      f'rx="300" ry="66" fill="url(#floorpool)"/>')

    # The extruded body, seen past the front face on the top and right.
    a(f'<path d="{rrect(BX0 + EDX, BY0 + EDY, BX1 + EDX, BY1 + EDY, BR)}" '
      f'fill="url(#body)"/>')

    # The front face.
    a(f'<path d="{rrect(BX0, BY0, BX1, BY1, BR)}" fill="url(#face)"/>')
    a("</g>")

    # ================================================================= fg
    a('<g id="fg">')

    # --- the settled row: what the board already said, and nothing lights it.
    a(f'<path d="{rrect(RX0, SETTLED_Y0, RX1, SETTLED_Y1, ROW_R)}" '
      f'fill="url(#recess)"/>')
    # The lip above it throws a short shadow down into the recess.
    a(f'<rect x="{RX0:.1f}" y="{SETTLED_Y0:.1f}" width="{RX1 - RX0:.1f}" '
      f'height="16" fill="#000000" opacity="0.34" filter="url(#tight)" '
      f'clip-path="url(#boardface)"/>')
    # and the recess's bottom lip catches a thread of the key.
    a(f'<rect x="{RX0 + 14:.1f}" y="{SETTLED_Y1 - 4:.1f}" '
      f'width="{RX1 - RX0 - 28:.1f}" height="3" rx="1.5" fill="{TILE_RIM}" '
      f'opacity="0.16"/>')

    # --- the uncovered row. Everything below is clipped to the aperture, so
    # the light cannot spill onto the face except where it is meant to.
    a('<g clip-path="url(#aperture)">')
    a(f'<rect x="{RX0:.1f}" y="{APERTURE_Y0:.1f}" width="{RX1 - RX0:.1f}" '
      f'height="{APERTURE_Y1 - APERTURE_Y0:.1f}" fill="url(#well)"/>')
    # The hottest sliver sits hard against the hinge — the deepest part of the
    # opening, where the source is.
    a(f'<rect x="{RX0:.1f}" y="{HINGE_Y - 22:.1f}" width="{RX1 - RX0:.1f}" '
      f'height="22" fill="{EMBER_CORE}" opacity="0.60" filter="url(#tight)"/>')
    # The aperture's own top lip shades the well beneath it.
    a(f'<rect x="{RX0:.1f}" y="{APERTURE_Y0:.1f}" width="{RX1 - RX0:.1f}" '
      f'height="14" fill="{EMBER_DEEP}" opacity="0.75" filter="url(#tight)"/>')
    a("</g>")

    # The bloom the aperture throws onto the face around itself.
    a(f'<ellipse cx="{(RX0 + RX1) / 2:.1f}" cy="{(APERTURE_Y0 + HINGE_Y) / 2:.1f}" '
      f'rx="{(RX1 - RX0) * 0.62:.1f}" ry="118" fill="url(#bloom)"/>')

    # --- the flap's shadow, thrown down the face it has left.
    a(f'<path d="{flap_path(shrink=10, drop=26)}" fill="{WARM_SHADOW}" '
      f'opacity="0.42" filter="url(#mid)" clip-path="url(#boardface)"/>')

    # --- the flap. Its own edge thickness first, warm-brown per apple-05,
    # then the surface over it, so a sliver of edge shows along the lead.
    a(f'<path d="{flap_path(drop=11)}" fill="{FLAP_EDGE}"/>')
    a(f'<path d="{flap_path()}" fill="url(#flapface)"/>')
    a("</g>")

    # ========================================================== highlight
    a('<g id="highlight">')

    # The well is directly behind the flap's hinge edge, so that edge is where
    # the second light lands on it.
    a(f'<path d="M{RX0:.1f},{HINGE_Y:.1f} L{RX1:.1f},{HINGE_Y:.1f} '
      f'L{RX1 + 14:.1f},{HINGE_Y + 30:.1f} L{RX0 - 14:.1f},{HINGE_Y + 30:.1f} Z" '
      f'fill="url(#bounce)"/>')

    # A thread of key light along the flap's leading arris — the one edge
    # square to the source now that the flap has tilted up.
    a(f'<path d="M{BX0 - FLAP_OVERHANG + 22:.1f},{FLAP_LEAD_Y - 2:.1f} '
      f'L{BX1 + FLAP_OVERHANG - 22:.1f},{FLAP_LEAD_Y - 2:.1f}" '
      f'stroke="{TILE_RIM}" stroke-width="3.5" opacity="0.42" '
      f'stroke-linecap="round"/>')

    # The board's own rim light, top-left arris into nothing at the foot.
    a(f'<path d="{rrect(BX0 + 1.5, BY0 + 1.5, BX1 - 1.5, BY1 - 1.5, BR - 1.5)}" '
      f'fill="none" stroke="url(#rim)" stroke-width="3"/>')

    # Tile vignette and the porcelain edge catching the same key.
    a(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    a(f'<path d="{squircle()}" fill="none" stroke="{TILE_RIM}" '
      f'stroke-width="3" opacity="0.55"/>')
    a("</g>")

    a("</g>")
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    sys.stdout.write(build() + "\n")
