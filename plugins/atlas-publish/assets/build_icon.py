#!/usr/bin/env python3
"""Engine A master generator — atlas-publish, direction "Tahoe Gel-Glass (porcelain)".

The device: **the stroke that stops at the gate.** Atlas ships under a black
script wordmark. Its capital A is lifted verbatim from that mark, cut at the
exact point where the letterform hands over to the `t`, and re-poured as a
soft-extruded graphite gel monoline on warm porcelain. Where the next stroke
would begin, a vermilion gate stands instead, and the script's exit stroke butts
flush against its flat left face. The porcelain beyond the gate is bare, and the
object sits 28px left of centre so that emptiness is wider than the margin in
front of the letter. The skill archives, uploads and registers a release and
then stops; making it live is a human's move. That is the whole icon.

Device #19 from the create-mac-icon catalogue (re-materialised brand mark):
silhouette untouched, material swapped. The only liberty taken with the mark is
a 9-unit uniform outset on the stroke, so a monoline drawn for a 1024 wordmark
still carries mass at 16px.

Tried and dropped, so a later round does not re-run them:

- **The whole word.** "Atlas" is 810 x 272 in the mark's own space; at 16px it
  is a horizontal smear with no mass, and it trips the catalogue's own no-text
  rule (rubric #12, failure mode #4). Measured against "At" and "Atl" as well,
  both already illegible at 16px. A single letterform is the sanctioned form.
- **A pill-shaped gate.** With BAR_R = BAR_W/2 the accent reads as a text caret
  sitting after a letter, not as a barrier. A slab with a flat left face gives
  the stroke something to press against.
- **Darkening the glyph's bottom edges.** Reversed after the corpus: apple-12
  holds its dark body's bottom edge at V 0.318 against a middle of V 0.133,
  because the porcelain bounces into it. The band along the bottom is now a
  lift, not a shade.
- **The second concept, a sealed bundle held at the lip of a stage.** Built and
  rendered; it lost. icon-notes.md records why.

Geometry and material are named constants; every fidelity round is a parameter
edit here, never path surgery in icon.svg.

    python3 build_icon.py

Emits 1024x1024 full-bleed layered artwork (bg / mid / fg / highlight) plus the
1024 / 256 / 128 exports the marketplace ships. The superellipse is a CLIP,
never a baked corner radius and never a baked drop shadow.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = 1024
EXPORTS = (1024, 256, 128)

# ---------------------------------------------------------------------------
# Light — one soft top-left key, shared by every gradient in the file.
# ---------------------------------------------------------------------------
KEY = (0.34, 0.26)

# ---------------------------------------------------------------------------
# Material. Ground and accent are the family's, measured off the shipped
# siblings; the graphite is the warm-lit ramp the corpus supports for a dark
# object under a warm key (apple-12 holds satin charcoal #343233 against a
# #CECECC ground at 8.11:1).
# ---------------------------------------------------------------------------
GROUND = ("#FCFAF4", "#F3EDE1", "#DED5C2")
VIGNETTE = "#8B7F66"
RIM_HAIR = "#C7B9A0"

INK_HI, INK_MID, INK_LO = "#454B57", "#2C313A", "#161A20"
INK_UNDER = ("#1E242A", "#0B0D11")
INK_SEAT = "#0B0D11"
RIM_SCATTER = "#FFF3E2"       # warm cream. #FFFFFF on a warm-lit body reads as
                              # a gloss streak rather than as volume.
BOUNCE = "#E2D8C2"            # porcelain lifting the body's lower edge

ACCENT = "#DE5A28"            # family luminance L~0.447, hue taken from Atlas
ACCENT_HI = "#F2823C"
ACCENT_SHADE = "#C9481C"      # keeps saturation; #BC3A14 over a long run browns
ACCENT_DEEP = "#BC3A14"
ACCENT_RIM = "#F6D3AC"

SHADOW = "#6E6049"            # warm. Nothing in a porcelain scene emits cool.
CONTACT = "#41372A"           # the hard occlusion line under a seated object

# Shadow stack, in TILE pixels. The object is drawn in the brand mark's own
# coordinate space and then scaled, so every one of these is divided by that
# scale on the way in — the numbers here mean what they mean at 1024.
CAST_DX, CAST_DY, CAST_BLUR, CAST_A = 13, 21, 22, 0.30
CORE_DX, CORE_DY, CORE_BLUR, CORE_A = 6, 9, 7, 0.20
OCCL_DX, OCCL_DY, OCCL_BLUR, OCCL_A = 3, 9, 6, 0.34
# No pooled shadow here. It is a stacked-object construction — under one
# compact body it renders as a visible soft box behind the artwork, which is
# what r04 shipped. The three-part cast below carries the seat on its own.

RIM_BAND = 15.0               # how far the key's light reaches down a stroke
RIM_SOFT = 9.0                # the falloff inside the mask: light, never a band
RIM_A = 0.44
LIFT_BAND = 17.0              # how far the ground bounce reaches up a stroke
LIFT_SOFT = 11.0
LIFT_A = 0.22
EXTRUDE = 11.0                # the thickness seen under the front face
SEAT_W = 2.6                  # the dark boundary drawn with the front face

# ---------------------------------------------------------------------------
# Geometry, in the brand mark's own 1024 space, then placed as one object.
# ---------------------------------------------------------------------------
GLYPH_BBOX = (104.11, 381.59, 356.00, 644.72)   # measured off glyph-path.txt
CUT_X = 356.00               # where the A hands over to the t: the gate's face

BAR_W = 62.0
BAR_TOP = 368.0              # stands a little proud of the glyph, top and bottom
BAR_BOT = 662.0
BAR_R = 13.0                 # a slab, not a pill: a pill reads as a text caret,
                             # and the stroke needs a flat face to press against

OBJECT_WIDTH_FRAC = 0.655    # focal object as a fraction of the tile. 0.68 was
                             # called out for crowding the tile edges in a blind
                             # read; the catalogue's own band is 0.55-0.65 and
                             # this sits just above it, which the letterform's
                             # thin stroke earns.
OPTICAL_CX = 487.0           # 28px left of centre, so the porcelain BEYOND the
                             # gate is wider than the margin before the glyph
OPTICAL_CY = 497.0           # 15px above true centre; the cast shadow below
                             # carries visual weight of its own


def read(name: str) -> str:
    return (HERE / name).read_text().strip()


SQUIRCLE = read("squircle-path.txt")
GLYPH = read("glyph-path.txt")

OBJ = (GLYPH_BBOX[0], min(GLYPH_BBOX[1], BAR_TOP),
       CUT_X + BAR_W, max(GLYPH_BBOX[3], BAR_BOT))
SCALE = (S * OBJECT_WIDTH_FRAC) / (OBJ[2] - OBJ[0])
TX = OPTICAL_CX - SCALE * (OBJ[0] + OBJ[2]) / 2.0
TY = OPTICAL_CY - SCALE * (OBJ[1] + OBJ[3]) / 2.0


def g(v: float) -> float:
    """A tile-pixel quantity expressed in the object's own (pre-scale) units."""
    return v / SCALE


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def blur(fid: str, sd: float, pad: int) -> str:
    return (f'<filter id="{fid}" x="-{pad}%" y="-{pad}%" '
            f'width="{100 + 2 * pad}%" height="{100 + 2 * pad}%">'
            f'<feGaussianBlur stdDeviation="{f(sd)}"/></filter>')


def cast(href: str, dx: float, dy: float, colour: str, alpha: float, fid: str) -> str:
    return (f'<use xlink:href="#{href}" fill="{colour}" opacity="{alpha}" '
            f'filter="url(#{fid})" transform="translate({f(g(dx))},{f(g(dy))})"/>')


def build() -> str:
    kx, ky = KEY[0] * S, KEY[1] * S
    ax0, ay0, ax1, ay1 = OBJ            # one shared light axis for the object

    defs = f"""
  <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>

  <radialGradient id="dome" cx="{f(kx)}" cy="{f(ky)}" r="{f(0.95 * S)}"
                  gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{GROUND[0]}"/>
    <stop offset=".52" stop-color="{GROUND[1]}"/>
    <stop offset="1" stop-color="{GROUND[2]}"/>
  </radialGradient>
  <radialGradient id="vig" cx="{f(0.5 * S)}" cy="{f(0.46 * S)}" r="{f(0.82 * S)}"
                  gradientUnits="userSpaceOnUse">
    <stop offset=".52" stop-color="{VIGNETTE}" stop-opacity="0"/>
    <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".15"/>
  </radialGradient>

  <linearGradient id="ink" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{INK_HI}"/>
    <stop offset=".46" stop-color="{INK_MID}"/>
    <stop offset="1" stop-color="{INK_LO}"/>
  </linearGradient>
  <linearGradient id="inkUnder" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{INK_UNDER[0]}"/>
    <stop offset="1" stop-color="{INK_UNDER[1]}"/>
  </linearGradient>
  <linearGradient id="bar" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{ACCENT_HI}"/>
    <stop offset=".52" stop-color="{ACCENT}"/>
    <stop offset="1" stop-color="{ACCENT_SHADE}"/>
  </linearGradient>

  <!-- The rim's own decay along the shared key axis: full at the lit corner,
       gone by the shaded one. On a letterform that faces every direction at
       once, this lights the correct edges for free. -->
  <linearGradient id="rimFall" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{RIM_SCATTER}" stop-opacity=".70"/>
    <stop offset=".42" stop-color="{RIM_SCATTER}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{RIM_SCATTER}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="barLean" gradientUnits="userSpaceOnUse"
                  x1="{f(CUT_X)}" y1="0" x2="{f(CUT_X + BAR_W)}" y2="0">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".13"/>
    <stop offset=".40" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000000" stop-opacity=".15"/>
  </linearGradient>
  <linearGradient id="barRimFall" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{ACCENT_RIM}" stop-opacity=".72"/>
    <stop offset=".55" stop-color="{ACCENT_RIM}" stop-opacity=".18"/>
    <stop offset="1" stop-color="{ACCENT_RIM}" stop-opacity="0"/>
  </linearGradient>

  {blur("soft", g(CAST_BLUR), 60)}
  {blur("tight", g(CORE_BLUR), 50)}
  {blur("hair", g(OCCL_BLUR), 40)}
  {blur("rimSoft", RIM_SOFT, 40)}
  {blur("liftSoft", LIFT_SOFT, 40)}
  {blur("press", 5, 60)}
  <filter id="tileRim" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="3.5"/>
  </filter>

  <path id="glyph" d="{GLYPH}"/>
  <rect id="gate" x="{f(CUT_X)}" y="{f(BAR_TOP)}" width="{f(BAR_W)}"
        height="{f(BAR_BOT - BAR_TOP)}" rx="{f(BAR_R)}"/>

  <!-- Edge bands built from a blurred offset knock-out rather than a filter on
       the paint, so the light falls off instead of banding and the renderer
       has nothing to drop silently. -->
  <mask id="mTopGlyph" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <rect width="{S}" height="{S}" fill="#fff"/>
    <use xlink:href="#glyph" fill="#000" filter="url(#rimSoft)"
         transform="translate({f(-RIM_BAND * 0.5)},{f(RIM_BAND)})"/>
  </mask>
  <mask id="mBotGlyph" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <rect width="{S}" height="{S}" fill="#fff"/>
    <use xlink:href="#glyph" fill="#000" filter="url(#liftSoft)"
         transform="translate(0,{f(-LIFT_BAND)})"/>
  </mask>
  <mask id="mTopGate" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <rect width="{S}" height="{S}" fill="#fff"/>
    <use xlink:href="#gate" fill="#000" filter="url(#rimSoft)"
         transform="translate({f(-RIM_BAND * 0.5)},{f(RIM_BAND)})"/>
  </mask>
  <mask id="mBotGate" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <rect width="{S}" height="{S}" fill="#fff"/>
    <use xlink:href="#gate" fill="#000" filter="url(#liftSoft)"
         transform="translate(0,{f(-LIFT_BAND)})"/>
  </mask>

  <!-- evenodd: the letterform carries a counter, and a clipPath with more than
       one subpath unions them under the default nonzero rule. -->
  <clipPath id="cGlyph" clip-rule="evenodd"><use xlink:href="#glyph"/></clipPath>
  <clipPath id="cGate"><use xlink:href="#gate"/></clipPath>"""

    bg = f"""
      <rect width="{S}" height="{S}" fill="url(#dome)"/>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity=".72"
            stroke-width="10" filter="url(#tileRim)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-opacity=".20"
            stroke-width="2.5"/>"""

    mid = "\n      ".join([
        cast("glyph", CAST_DX, CAST_DY, SHADOW, CAST_A, "soft"),
        cast("gate", CAST_DX, CAST_DY, SHADOW, CAST_A, "soft"),
        cast("glyph", CORE_DX, CORE_DY, SHADOW, CORE_A, "tight"),
        cast("gate", CORE_DX, CORE_DY, SHADOW, CORE_A, "tight"),
        cast("glyph", OCCL_DX, OCCL_DY, CONTACT, OCCL_A, "hair"),
        cast("gate", OCCL_DX, OCCL_DY, CONTACT, OCCL_A, "hair"),
    ])

    fg = f"""
      <!-- the thickness under each front face -->
      <use xlink:href="#glyph" fill="url(#inkUnder)" transform="translate(0,{f(EXTRUDE)})"/>
      <use xlink:href="#gate" fill="{ACCENT_DEEP}" transform="translate(0,{f(EXTRUDE * 0.7)})"/>

      <!-- the seat edge, drawn WITH the front face and before anything set
           into it: run afterwards it draws a seam down the up-light side -->
      <use xlink:href="#glyph" fill="{INK_SEAT}" stroke="{INK_SEAT}"
           stroke-width="{f(SEAT_W)}" stroke-linejoin="round" opacity=".55"/>

      <!-- the script, poured -->
      <g clip-path="url(#cGlyph)">
        <rect width="{S}" height="{S}" fill="url(#ink)"/>
      </g>

      <!-- the gate, poured -->
      <g clip-path="url(#cGate)">
        <rect width="{S}" height="{S}" fill="url(#bar)"/>
        <rect width="{S}" height="{S}" fill="url(#barLean)"/>
      </g>

      <!-- where the stroke presses into the gate: the one place the two objects
           touch, and the only thing that says stopped rather than beside -->
      <g clip-path="url(#cGate)">
        <rect x="{f(CUT_X)}" y="{f(GLYPH_BBOX[3] - 92)}" width="20" height="104"
              fill="{ACCENT_DEEP}" opacity=".46" filter="url(#press)"/>
      </g>"""

    highlight = f"""
      <!-- the key's rim light, and the porcelain bouncing back into the bodies'
           lower edges (apple-12 holds that edge above its own middle) -->
      <g clip-path="url(#cGlyph)" mask="url(#mTopGlyph)">
        <rect width="{S}" height="{S}" fill="url(#rimFall)" opacity="{RIM_A}"/>
      </g>
      <g clip-path="url(#cGlyph)" mask="url(#mBotGlyph)">
        <rect width="{S}" height="{S}" fill="{BOUNCE}" opacity="{LIFT_A}"/>
      </g>
      <g clip-path="url(#cGate)" mask="url(#mTopGate)">
        <rect width="{S}" height="{S}" fill="url(#barRimFall)" opacity="{RIM_A}"/>
      </g>
      <g clip-path="url(#cGate)" mask="url(#mBotGate)">
        <rect width="{S}" height="{S}" fill="{BOUNCE}" opacity="{LIFT_A * 0.7:.2f}"/>
      </g>

      <!-- the gate's own boundary, re-run last. It is the one body touching
           porcelain directly, and on a sibling this single path took its edge
           against the tile from 2.44:1 to 3.36:1. -->
      <use xlink:href="#gate" fill="none" stroke="{ACCENT_DEEP}"
           stroke-width="{f(g(5))}" stroke-opacity=".80"/>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>atlas-publish</title>
  <desc>The Atlas script A, re-poured as graphite gel, its exit stroke stopped
  flush against a vermilion gate. The marketplace superellipse is a clip, not a
  baked corner radius, and no drop shadow is baked into the tile.</desc>
  <defs>{defs}
  </defs>
  <g clip-path="url(#tile)">
    <g id="bg">{bg}
    </g>
    <g transform="translate({TX:.3f},{TY:.3f}) scale({SCALE:.5f})">
      <g id="mid">
      {mid}
      </g>
      <g id="fg">{fg}
      </g>
      <g id="highlight">{highlight}
      </g>
    </g>
  </g>
</svg>
"""


def main() -> int:
    out = HERE / "icon.svg"
    out.write_text(build())
    for px in EXPORTS:
        name = "icon.png" if px == 1024 else f"icon-{px}.png"
        subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px),
                        "-o", str(HERE / name), str(out)], check=True)
    print(f"wrote icon.svg (scale {SCALE:.4f}) and "
          f"{', '.join(str(p) for p in EXPORTS)}px exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
