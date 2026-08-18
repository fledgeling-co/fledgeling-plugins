#!/usr/bin/env python3
"""build_icon.py - Engine A master for the `mockup-fidelity` icon.

Direction 2 (Tahoe gel-glass), sub-register (a): porcelain cushion tile carrying
one coloured gel object, in the fledgeling-plugins house palette lifted from its
siblings (`test-campaign` and `resume-session` share the #F8F5EE -> #E4DDCB
ground; the accent family is `#E4652E`, kin to Fledgeling's `#C4622D`).

CONCEPT - "The Overlay". The reference is scribed into the tile itself: a
rectangle cut in porcelain with registration brackets at its corners, because in
this skill the mock is the authority and the authority is not another card. The
implementation is a clay-gel slab of exactly the same size laid over it and
misregistered by a measured (100, 76). Nothing else is on the tile.

That single misregistration carries the plugin's whole ledger, all three states
at once and with no extra props:

  PRESENT    where the slab covers the scribed rectangle, and you can see the
             scribed line and the far bracket THROUGH the gel - the mock is
             still visible under the implementation, which is what makes this a
             measurement rather than a claim.
  DIVERGENT  the slab riding proud past the scribed line at the bottom-right -
             the app-extra element, drawn as an overhang with its own contact
             shadow on the porcelain.
  ABSENT     the L of exposed reference at the top-left, lit ember. Every one of
             those pixels is a mock element the build never covered, and the
             strip is drawn to scale, so the icon reports the size of the
             difference instead of asserting a match.

SIGNATURE MOVE - the exposed sliver is the mark. The accent is spent on the gap
between the two, never on either object, so what the eye lands on first is the
disagreement.

Separated deliberately from three near neighbours: `improve-skill` owns a
before/after boundary (two states of one object), `be-my-witness` owns comparing
a capture against an expectation through a lens, and `should-compact` owns two
slabs squeezing a symmetric seam. This one is an overlay, off register, with an
asymmetric L - and its accent sits in the exposed reference rather than between
two equals.

Corpus numbers this was authored against (sampled off
`create-mac-icon/references/corpus/apple-2026/`, porcelain register - apple-05,
apple-11, apple-18, apple-23, apple-26, apple-28):

  ground        L 0.99-1.00 at the top, 0.92-0.93 at the bottom corners,
                brightest toward the top-left; shallow vignette, never flat
  contact       a soft, shallow dip - apple-18's ground goes 0.929 -> 0.877
  shadow        under the object, over roughly a tenth of the tile
  accent        the register's saturated pixels sit at L 0.28-0.52, S 0.64-0.85
                (Calendar's today dot is rgb(237,76,72), L 0.43, S 0.70)
  dark faces    darkest in-tile pixel L 0.12-0.14 - cool in Apple's own set
                (hue 200-214), warm here, because the fledgeling family's
                shadows are warm and set kinship outranks the corpus on hue

    python3 build_icon.py > icon.svg
"""

import pathlib
import sys

SQ = (pathlib.Path(__file__).resolve().parents[2] / "create-mac-icon" / "assets"
      / "squircle-path.txt")

S = 1024

# ── palette ─────────────────────────────────────────────────────────────────
# Two hue families and no more: warm porcelain/clay, and the one ember accent.
# The ground is calibrated to the siblings rather than to Apple's own porcelain,
# which runs about 0.10 brighter at the bottom corners: measured on the shelf,
# `test-campaign` and `resume-session` read TL 0.92-0.93 / BL 0.81 / top-mid
# 0.95, and matching the shelf is what makes a set read as a set.
GROUND_TOP, GROUND_MID, GROUND_BOT = "#F9F6EE", "#F3EFE4", "#E4DDCB"
RIM = "#FFFDF8"
SHADOW = "#4A3F2E"

# The mock, scribed into the porcelain. Its floor is one step below the cushion
# so the reference reads as an area rather than an outline. A recess lit from the
# upper left is dark on its NEAR inner wall and lit on its FAR one - the first
# draft had that backwards, which put a white hairline exactly where the shadow
# belongs.
MOCK_FLOOR_TOP, MOCK_FLOOR_BOT = "#F0E9D9", "#DFD5BE"
SCRIBE = "#8A7A61"

# The build. A porcelain slab on a porcelain cushion measures about 1.1:1 and
# reads as white on white at every size (measured on `test-campaign`), so
# the implementation is the family's clay gel and carries the figure-ground.
GEL_TOP, GEL_MID, GEL_BOT = "#8A7D64", "#6B6049", "#443A2B"
GEL_WALL_TOP, GEL_WALL_BOT = "#4B4133", "#342C21"
GEL_DEEP = "#332C21"                        # the scribe seen through the gel

# The one accent, reserved for the divergence. The gap is a TROUGH of light:
# hottest against the slab's own wall, deepest at the scribed line, so the
# saturated pixels sit in the corpus's measured band (L 0.28-0.52) instead of
# washing to cream.
ACCENT, ACCENT_HI, ACCENT_CORE = "#E4652E", "#F79A61", "#FFD3A2"
ACCENT_LO, ACCENT_EDGE = "#B8390F", "#8E2E0C"

# ── geometry ────────────────────────────────────────────────────────────────
# Same size for both rectangles: the only difference between the reference and
# the implementation is that one of them is in the wrong place.
MX, MY, MW, MH, R = 196, 196, 540, 540, 76         # the mock, scribed
DX, DY = 100, 76                                   # the misregistration, to scale
BX, BY = MX + DX, MY + DY                          # the build slab
WALL = 24                                          # the slab's visible thickness
LIP = 3                                            # the scribe groove's lit lip
INSET = 26                                         # porcelain margin the light leaves
BRACKET_L, BRACKET_W, BRACKET_GAP = 46, 7, 30      # registration brackets

# Union of both rectangles plus the wall: x 196..836, y 196..836, centred 516.
# One soft key up and to the left, as everywhere else in the set.


def rr(x: float, y: float, w: float, h: float, r: float) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}"'


def bracket(cx: float, cy: float, sx: int, sy: int) -> str:
    """One registration bracket - an L of two strokes, set off the corner.

    Diegetic garnish in the sanctioned sense: sub-legible at Dock size, a real
    feature of the thing being drawn at 1024. `sx`/`sy` point the L outward.
    """
    x = cx + sx * BRACKET_GAP
    y = cy + sy * BRACKET_GAP
    return (f'<path d="M{x:.0f} {y:.0f} h{sx * BRACKET_L}" stroke-width="{BRACKET_W}"/>'
            f'<path d="M{x:.0f} {y:.0f} v{sy * BRACKET_L}" stroke-width="{BRACKET_W}"/>')


def svg() -> str:
    d = SQ.read_text().strip() if SQ.exists() else ""
    if not d:
        print("squircle-path.txt not found - the family shares one silhouette",
              file=sys.stderr)
        raise SystemExit(1)

    mock = f'{rr(MX, MY, MW, MH, R)}'
    build = f'{rr(BX, BY, MW, MH, R)}'
    # A rounded rect offset by (+n,+n) and clipped to the mock leaves lines on the
    # TOP and LEFT inner edges only; offset by (-n,-n) leaves the BOTTOM and RIGHT.
    # That is how a recess gets a shadowed near wall and a lit far one out of two
    # strokes and no new geometry.
    wall_near = rr(MX + LIP, MY + LIP, MW, MH, R)
    wall_far = rr(MX - LIP, MY - LIP, MW, MH, R)
    # The lit area of the gap, held INSET inside the reference's own frame. Filling
    # the whole exposed strip made the reference read as an orange plate; leaving a
    # porcelain margin keeps the scribed rectangle reading as porcelain that has
    # been cut, which is what makes it the authority rather than another card.
    lit = rr(MX + INSET, MY + INSET, MW - 2 * INSET, MH - 2 * INSET, R - INSET * .55)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <!-- cushion: never flat. Calibrated to the siblings, not to Apple's ground -->
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".54" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vig" cx=".40" cy=".36" r=".80">
      <stop offset=".52" stop-color="{SHADOW}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity=".13"/>
    </radialGradient>

    <linearGradient id="mockFloor" x1="0" y1="0" x2=".55" y2="1">
      <stop offset="0" stop-color="{MOCK_FLOOR_TOP}"/>
      <stop offset="1" stop-color="{MOCK_FLOOR_BOT}"/>
    </linearGradient>

    <!-- the slab: one key up and to the left, so top-left is the lit corner -->
    <linearGradient id="gel" x1="{BX + MW * .16}" y1="{BY}" x2="{BX + MW * .34}" y2="{BY + MH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GEL_TOP}"/>
      <stop offset=".52" stop-color="{GEL_MID}"/>
      <stop offset="1" stop-color="{GEL_BOT}"/>
    </linearGradient>
    <!-- the second direction is a second layer, never a lean on the first: a
         gradient carries one axis, and a lateral lean written into a mostly
         vertical vector projects past offset 1 and renders flat (clarify, r-lean) -->
    <linearGradient id="gelSide" x1="{BX + MW * .45}" y1="0" x2="{BX + MW}" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity=".17"/>
    </linearGradient>
    <!-- a wall ramps COLOUR, not opacity: an opacity ramp dissolves the wall on
         the unlit side and the slab loses its thickness (mac-doctor, r07) -->
    <linearGradient id="gelWall" x1="{BX}" y1="0" x2="{BX + MW}" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GEL_WALL_TOP}"/>
      <stop offset="1" stop-color="{GEL_WALL_BOT}"/>
    </linearGradient>
    <linearGradient id="satin" x1="0" y1="{BY}" x2="0" y2="{BY + MH * .55}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".08"/>
      <stop offset="1" stop-color="{RIM}" stop-opacity="0"/>
    </linearGradient>
    <!-- the gap's light grazing the two faces that look into it, and reaching a
         little way INTO the gel, because the slab is a translucent body -->
    <linearGradient id="bounceTop" x1="0" y1="{BY}" x2="0" y2="{BY + 150}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{ACCENT_HI}" stop-opacity=".21"/>
      <stop offset="1" stop-color="{ACCENT_HI}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bounceLeft" x1="{BX}" y1="0" x2="{BX + 170}" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{ACCENT_HI}" stop-opacity=".18"/>
      <stop offset="1" stop-color="{ACCENT_HI}" stop-opacity="0"/>
    </linearGradient>
    <!-- a translucent body carries a rim of transmitted light just inside its
         outline; without it a gel slab reads as a lit opaque plane -->
    <linearGradient id="transmit" x1="{BX}" y1="{BY}" x2="{BX + MW * .7}" y2="{BY + MH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".17"/>
      <stop offset=".55" stop-color="{RIM}" stop-opacity=".09"/>
      <stop offset="1" stop-color="{RIM}" stop-opacity=".20"/>
    </linearGradient>
    <radialGradient id="ao" cx=".82" cy=".86" r=".62">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity=".34"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </radialGradient>

    <filter id="soft" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="11"/>
    </filter>
    <filter id="edgeSoft" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <filter id="bloom" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="contact" x="-35%" y="-35%" width="170%" height="190%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>

    <clipPath id="tile"><path d="{d}"/></clipPath>
    <clipPath id="mockClip">{mock}/></clipPath>
    <clipPath id="buildClip">{build}/></clipPath>
    <!-- mock MINUS build. A two-subpath clipPath would union them under the
         default nonzero rule, so the subtraction is a mask, not a clip. -->
    <mask id="exposed" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
      {mock} fill="#fff"/>
      {build} fill="#000"/>
    </mask>
  </defs>

  <g clip-path="url(#tile)">
    <g id="bg">
      <!-- the cushion, and the ember reaching the porcelain past the scribe -->
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>
      <g filter="url(#bloom)" opacity=".26">
        <g mask="url(#exposed)">{mock} fill="{ACCENT}"/></g>
      </g>

      <!-- the reference: an area cut into the tile, its groove, its far lit
           wall, and the registration bracket on the corner the build left bare -->
      {mock} fill="url(#mockFloor)"/>
      <g stroke="{SCRIBE}" fill="none" stroke-linecap="round" opacity=".58">
        {bracket(MX, MY, -1, -1)}
      </g>
      <g clip-path="url(#mockClip)">
        {wall_far} fill="none" stroke="{RIM}" stroke-width="5" opacity=".60"/>
        {wall_near} fill="none" stroke="{SCRIBE}" stroke-width="5" opacity=".30"/>
      </g>
      {mock} fill="none" stroke="{SCRIBE}" stroke-width="5" opacity=".50"/>
    </g>

    <g id="mid">
      <!-- ABSENT: the exposed reference, lit. Drawn to scale - the strip IS the
           misregistration, so the icon reports the size of the difference. Built
           as a trough: hot against the slab's wall, deepest at the scribed line,
           because one gradient carries one axis and an L has two arms. -->
      <g mask="url(#exposed)">
        {lit} fill="{ACCENT}"/>
        <g filter="url(#soft)">
          {lit} fill="none" stroke="{ACCENT_LO}" stroke-width="72" opacity=".92"/>
        </g>
        <g filter="url(#soft)">
          {build} fill="none" stroke="{ACCENT_HI}" stroke-width="46" opacity=".88"/>
        </g>
        <g filter="url(#edgeSoft)">
          {build} fill="none" stroke="{ACCENT_CORE}" stroke-width="13" opacity=".78"/>
        </g>
        <!-- the light stops inside the reference's own frame, so the scribed
             rectangle stays porcelain and stays legible as the authority -->
        {lit} fill="none" stroke="{ACCENT_EDGE}" stroke-width="6" opacity=".45"/>
      </g>

      <!-- the overhang's contact shadow, on the porcelain it rides onto -->
      <g filter="url(#contact)" opacity=".33">
        {rr(BX + 10, BY + WALL + 16, MW, MH, R)} fill="{SHADOW}"/>
      </g>
    </g>

    <g id="fg">
      <!-- DIVERGENT / PRESENT: the implementation, off register. Its thickness
           is a colour ramp on an opaque wall, not a faded copy of the face. -->
      {rr(BX, BY + WALL, MW, MH, R)} fill="url(#gelWall)"/>
      {build} fill="url(#gel)"/>

      <!-- the mock read THROUGH the gel: its floor tone stops exactly at the
           scribed line, and the line, the far wall's catch and the far bracket
           carry on underneath. This is the signature craft moment - authored
           overlap, Tahoe tell 5, and the reason this is a measurement. -->
      <g clip-path="url(#buildClip)">
        <g clip-path="url(#mockClip)">
          {mock} fill="{MOCK_FLOOR_TOP}" opacity=".10"/>
          {wall_far} fill="none" stroke="{RIM}" stroke-width="5" opacity=".18"/>
        </g>
        {mock} fill="none" stroke="{GEL_DEEP}" stroke-width="6" opacity=".46"/>
        <g stroke="{GEL_DEEP}" fill="none" stroke-linecap="round" opacity=".38">
          {bracket(MX + MW, MY + MH, 1, 1)}
        </g>
      </g>
    </g>

    <g id="highlight">
      <!-- lighting only: droppable without the mark stopping being itself -->
      <g clip-path="url(#buildClip)">
        {rr(BX, BY, MW, MH * .55, R)} fill="url(#satin)"/>
        {rr(BX, BY, MW, 150, R)} fill="url(#bounceTop)"/>
        {rr(BX, BY, 170, MH, R)} fill="url(#bounceLeft)"/>
        {build} fill="url(#gelSide)"/>
        {build} fill="url(#ao)"/>
        <!-- transmitted rim: a stroke on the inside of the outline, so the body
             reads as gel rather than as a lit opaque plane -->
        {rr(BX + 7, BY + 7, MW - 14, MH - 14, R - 7)} fill="none"
              stroke="url(#transmit)" stroke-width="15"/>
      </g>
      <path d="M{BX + R} {BY + 5} H{BX + MW - R}" stroke="{RIM}" stroke-width="8"
            stroke-linecap="round" opacity=".28"/>
      <path d="M{BX + 5} {BY + R} V{BY + MH - R}" stroke="{ACCENT_CORE}" stroke-width="7"
            stroke-linecap="round" opacity=".30"/>
      <path d="M{BX + MW - 5} {BY + R} V{BY + MH - R}" stroke="{SHADOW}" stroke-width="7"
            stroke-linecap="round" opacity=".22"/>
      <!-- the cushion's inner rim light -->
      <path d="{d}" fill="none" stroke="{RIM}" stroke-width="7" opacity=".80"/>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    print(svg())
