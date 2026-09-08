#!/usr/bin/env python3
"""Engine A master generator — atlas-review, direction "Tahoe Gel-Glass (porcelain)".

The device: **the stroke you broke to prove it.** Its sibling `atlas-publish`
takes the capital A of the Atlas script wordmark, re-pours it as a graphite gel
monoline on warm porcelain, and stands a vermilion gate where the next stroke
would begin — a stroke that stops. This icon takes the same letterform in the
same material and does the opposite thing to it: one clean fracture, cut square
across the descending stem, with vermilion filling the void so the break reads
as lit from inside rather than as missing material.

The letterform continues on both sides and the mark holds. That is the whole
idea. The skill's claim is that a check which cannot fail is not a check, and
that reading one tells you nothing — so it breaks the code a test covers and
watches the test go red. The break is not damage. The break is the evidence.

Every material constant below is the sibling's, lifted rather than re-derived,
because these two icons must read as a pair: the same ground, the same warm-lit
graphite ramp, the same vermilion, the same three-part cast shadow, the same
rim-and-bounce construction. What is new here is the cut, and the recess inside
it — a groove whose upper wall falls into shadow and whose lower wall catches
the key, which is the one material this family did not already own.

Cut geometry is measured, not eyeballed. `CUT_AT` and `CUT_SLOPE` come from
sampling the rasterised glyph down rows 490-565, where the stem is the only ink
on its scanline and porcelain lies open on both sides — so the two flat faces
have nothing to touch and cannot read as an overlap.

Tried and dropped, so a later round does not re-run them:

- **Cutting the bowl's left flank.** It splits the letter's enclosure, and a
  broken enclosure reads as damage to the mark. Severing the stem leaves the
  bowl whole, which is what lets the icon say the mark survived it.
- **A jagged fracture.** Says something broke. Two flat parallel faces say
  somebody did it on purpose and is watching what happens.
- **Leaving the gap empty porcelain.** At 32px an unfilled gap closes up and the
  glyph reads as an ordinary A. Filled with the accent it survives as a bright
  interruption, which is the one thing that must not be lost at size.
- **Two cuts.** Reads as damage. One reads as a measurement.

Geometry and material are named constants; every fidelity round is a parameter
edit here, never path surgery in icon.svg.

    python3 build_icon.py

Emits 1024x1024 full-bleed layered artwork (bg / mid / fg / highlight) plus the
1024 / 256 / 128 exports the marketplace ships. The superellipse is a CLIP,
never a baked corner radius and never a baked drop shadow.
"""

from __future__ import annotations

import math
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
# Material — the sibling's, verbatim. See the module docstring.
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
ACCENT_SHADE = "#C9481C"
ACCENT_DEEP = "#BC3A14"
ACCENT_RIM = "#F6D3AC"

SHADOW = "#6E6049"            # warm. Nothing in a porcelain scene emits cool.
CONTACT = "#41372A"           # the hard occlusion line under a seated object

CAST_DX, CAST_DY, CAST_BLUR, CAST_A = 13, 21, 22, 0.30
CORE_DX, CORE_DY, CORE_BLUR, CORE_A = 6, 9, 7, 0.20
OCCL_DX, OCCL_DY, OCCL_BLUR, OCCL_A = 3, 9, 6, 0.34

RIM_BAND = 15.0               # how far the key's light reaches down a stroke
RIM_SOFT = 9.0
RIM_A = 0.44
LIFT_BAND = 17.0              # how far the ground bounce reaches up a stroke
LIFT_SOFT = 11.0
LIFT_A = 0.22
EXTRUDE = 15.0                # the thickness seen under the front face. Raised
                              # from the sibling's 11 after Engine C: its rasters
                              # carry a rounder, deeper under-edge and the body
                              # reads as a solid rather than a sticker for it.
                              # At 19 the shelf detaches and reads as a second
                              # object under the letter.
SEAT_W = 2.6

# ---------------------------------------------------------------------------
# Geometry, in the brand mark's own 1024 space, then placed as one object.
# ---------------------------------------------------------------------------
GLYPH_BBOX = (104.11, 381.59, 356.00, 644.72)   # measured off glyph-path.txt

# The cut. Measured off the rasterised glyph: down rows 490-565 the descending
# stem is the only ink on its scanline, its centreline runs at dx/dy = -0.4254,
# and its perpendicular thickness holds at 40 units.
CUT_AT = (270.2, 527.0)       # a point on the stem's centreline
CUT_SLOPE = -0.4254           # dx/dy of that centreline
CUT_REACH = 34.0              # half-length of the band. The stem's perpendicular
                              # half-thickness is 20, so this overruns it by 14
                              # into open porcelain at each end and stops there.
                              # At 130 the same band ran on and clipped the
                              # bowl's upper arch as well: two voids, which
                              # reads as damage rather than as a measurement.
GAP_TILE = 66.0               # the void's width in TILE px. Below ~46 it closes
                              # up at 32px and the glyph reads as an ordinary A.
                              # Above ~74 the stem reads severed rather than
                              # cut, and the claim is that the mark HOLDS.
GLOW_TILE = 18.0              # how far the accent bleeds out of the void
LIP_HI_TILE = 11.0            # the upper piece's cut face: a BOTTOM edge, dark
LIP_LO_TILE = 8.0            # the lower piece's cut face: a TOP edge, lit
LIP_HI_A = 0.50
LIP_LO_A = 0.20               # at 0.52 over a wide blur this face stopped being
                              # a lit edge and became a gloss streak down the
                              # stroke, which is the failure the family's own
                              # notes warn about for cream on a warm-lit body.
                              # A cut face is narrow and hard, not polished.

VOID = "filled"               # "filled" ships. "open" is the alternate take:
                              # the cut goes clean through to porcelain and the
                              # accent survives only as a hair on the rim. It is
                              # built and scored because it is the honest test of
                              # this icon's one size claim, and it loses it — see
                              # icon-notes.md.

OBJECT_SPAN_FRAC = 0.625      # the object's LONGER side as a fraction of the
                              # tile. The sibling sized on width because its
                              # gate widened the object; this one is a bare
                              # letterform, so the taller side governs.
OPTICAL_CX = 472.0            # 40px left of centre, which carries the cut —
                              # sitting right of the glyph's own middle — back
                              # toward the tile's optical centre
OPTICAL_CY = 492.0            # 20px above true centre; the cast shadow below
                              # carries visual weight of its own


def read(name: str) -> str:
    return (HERE / name).read_text().strip()


SQUIRCLE = read("squircle-path.txt")
GLYPH = read("glyph-path.txt")

OBJ = GLYPH_BBOX
SCALE = (S * OBJECT_SPAN_FRAC) / max(OBJ[2] - OBJ[0], OBJ[3] - OBJ[1])
TX = OPTICAL_CX - SCALE * (OBJ[0] + OBJ[2]) / 2.0
TY = OPTICAL_CY - SCALE * (OBJ[1] + OBJ[3]) / 2.0


def g(v: float) -> float:
    """A tile-pixel quantity expressed in the object's own (pre-scale) units."""
    return v / SCALE


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


# The cut's own frame. `d` runs DOWN the stroke, `n` across it — the band's long
# axis — so the band is a rect of thickness GAP rotated by n's angle.
_dn = math.hypot(CUT_SLOPE, 1.0)
DX_, DY_ = CUT_SLOPE / _dn, 1.0 / _dn
NX_, NY_ = DY_, -DX_                       # n = d rotated -90deg: (+x, +y)
CUT_ANGLE = math.degrees(math.atan2(NY_, NX_))
GAP = g(GAP_TILE)
CUT_HI = (CUT_AT[0] - DX_ * GAP / 2, CUT_AT[1] - DY_ * GAP / 2)   # upper wall
CUT_LO = (CUT_AT[0] + DX_ * GAP / 2, CUT_AT[1] + DY_ * GAP / 2)   # lower wall


def band(t: float, thickness: float) -> str:
    """A rect parallel to the cut, its centre `t` units down-stroke of it.

    The cut opens two faces the glyph did not have, and neither the rim mask nor
    the bounce mask can see them: both are keyed on the whole letterform's
    silhouette, so a boundary that only exists because of the cut goes unlit and
    the void flattens into a painted stripe. These bands light them by hand.
    """
    cx, cy = CUT_AT[0] + DX_ * t, CUT_AT[1] + DY_ * t
    return (f'<rect x="{f(cx - CUT_REACH)}" y="{f(cy - thickness / 2)}" '
            f'width="{f(2 * CUT_REACH)}" height="{f(thickness)}" '
            f'transform="rotate({CUT_ANGLE:.3f},{f(cx)},{f(cy)})"')


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

  <!-- the void's floor, lit along the same key axis as everything else -->
  <linearGradient id="void" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{ACCENT_HI}"/>
    <stop offset=".52" stop-color="{ACCENT}"/>
    <stop offset="1" stop-color="{ACCENT_SHADE}"/>
  </linearGradient>

  <!-- The groove's two walls, running ACROSS the cut. The upper wall faces
       away from a top-left key and falls into shadow; the lower wall faces
       back into it and catches the light. Without this pair the void reads as
       a painted stripe rather than as material taken out. -->
  <linearGradient id="depth" gradientUnits="userSpaceOnUse"
                  x1="{f(CUT_HI[0])}" y1="{f(CUT_HI[1])}"
                  x2="{f(CUT_LO[0])}" y2="{f(CUT_LO[1])}">
    <stop offset="0" stop-color="{CONTACT}" stop-opacity=".88"/>
    <stop offset=".16" stop-color="{ACCENT_DEEP if VOID == 'filled' else CONTACT}" stop-opacity=".74"/>
    <stop offset=".46" stop-color="{ACCENT_DEEP if VOID == 'filled' else CONTACT}" stop-opacity=".18"/>
    <stop offset=".78" stop-color="{ACCENT_HI if VOID == 'filled' else BOUNCE}" stop-opacity=".10"/>
    <stop offset="1" stop-color="{ACCENT_RIM if VOID == 'filled' else BOUNCE}" stop-opacity=".34"/>
  </linearGradient>

  <linearGradient id="rimFall" gradientUnits="userSpaceOnUse"
                  x1="{f(ax0)}" y1="{f(ay0)}" x2="{f(ax1)}" y2="{f(ay1)}">
    <stop offset="0" stop-color="{RIM_SCATTER}" stop-opacity=".70"/>
    <stop offset=".42" stop-color="{RIM_SCATTER}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{RIM_SCATTER}" stop-opacity="0"/>
  </linearGradient>

  {blur("soft", g(CAST_BLUR), 60)}
  {blur("tight", g(CORE_BLUR), 50)}
  {blur("hair", g(OCCL_BLUR), 40)}
  {blur("rimSoft", RIM_SOFT, 40)}
  {blur("liftSoft", LIFT_SOFT, 40)}
  {blur("glow", g(GLOW_TILE), 90)}
  {blur("lipHi", g(4.0), 70)}
  {blur("lipLo", g(2.2), 70)}
  <filter id="tileRim" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="3.5"/>
  </filter>

  <path id="glyph" d="{GLYPH}"/>
  <rect id="cut" x="{f(CUT_AT[0] - CUT_REACH)}" y="{f(CUT_AT[1] - GAP / 2)}"
        width="{f(2 * CUT_REACH)}" height="{f(GAP)}"
        transform="rotate({CUT_ANGLE:.3f},{f(CUT_AT[0])},{f(CUT_AT[1])})"/>

  <!-- Which side of the cut a thing is painted on. `mHeld` is the letterform
       minus the void; `mVoid` is the void alone. -->
  <mask id="mHeld" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <rect width="{S}" height="{S}" fill="#fff"/>
    <use xlink:href="#cut" fill="#000"/>
  </mask>
  <mask id="mVoid" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <use xlink:href="#cut" fill="#fff"/>
  </mask>

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

  <!-- evenodd: the letterform carries a counter, and a clipPath with more than
       one subpath unions them under the default nonzero rule. -->
  <clipPath id="cGlyph" clip-rule="evenodd"><use xlink:href="#glyph"/></clipPath>"""

    bg = f"""
      <rect width="{S}" height="{S}" fill="url(#dome)"/>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity=".72"
            stroke-width="10" filter="url(#tileRim)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-opacity=".20"
            stroke-width="2.5"/>"""

    mid = "\n      ".join([
        cast("glyph", CAST_DX, CAST_DY, SHADOW, CAST_A, "soft"),
        cast("glyph", CORE_DX, CORE_DY, SHADOW, CORE_A, "tight"),
        cast("glyph", OCCL_DX, OCCL_DY, CONTACT, OCCL_A, "hair"),
    ])

    fg = f"""
      <!-- the thickness under the front face, and the void's own deeper floor -->
      <use xlink:href="#glyph" fill="url(#inkUnder)" transform="translate(0,{f(EXTRUDE)})"/>
      <g clip-path="url(#cGlyph)" mask="url(#mVoid)">
        <use xlink:href="#glyph" fill="{ACCENT_DEEP}"
             transform="translate(0,{f(EXTRUDE * 0.7)})"/>
      </g>

      <!-- the seat edge, drawn WITH the front face and before anything set
           into it: run afterwards it draws a seam down the up-light side -->
      <use xlink:href="#glyph" fill="{INK_SEAT}" stroke="{INK_SEAT}"
           stroke-width="{f(SEAT_W)}" stroke-linejoin="round" opacity=".55"/>

      <!-- the void, poured and then hollowed: floor, then the groove's two
           walls, then the hair line where each graphite face meets it -->
      <g clip-path="url(#cGlyph)" mask="url(#mVoid)">
        <rect width="{S}" height="{S}" fill="url(#{'void' if VOID == 'filled' else 'dome'})"/>
        <rect width="{S}" height="{S}" fill="url(#depth)"/>
      </g>

      <!-- the letterform itself, poured everywhere the void is not -->
      <g clip-path="url(#cGlyph)" mask="url(#mHeld)">
        <rect width="{S}" height="{S}" fill="url(#ink)"/>
      </g>"""

    highlight = f"""
      <!-- the key's rim light, and the porcelain bouncing back into the body's
           lower edge (apple-12 holds that edge above its own middle) -->
      <g clip-path="url(#cGlyph)" mask="url(#mHeld)">
        <g mask="url(#mTopGlyph)">
          <rect width="{S}" height="{S}" fill="url(#rimFall)" opacity="{RIM_A}"/>
        </g>
        <g mask="url(#mBotGlyph)">
          <rect width="{S}" height="{S}" fill="{BOUNCE}" opacity="{LIFT_A}"/>
        </g>
      </g>

      <!-- The two faces the cut opened. Above the void is a bottom edge and
           falls away from the key; below it is a top edge and catches it. Drawn
           on the graphite and held out of the void, so each face reads as the
           end of a solid rather than as the edge of a painted band. -->
      <g clip-path="url(#cGlyph)" mask="url(#mHeld)">
        <g filter="url(#lipHi)">
          {band(-(GAP + g(LIP_HI_TILE)) / 2, g(LIP_HI_TILE))} fill="{INK_SEAT}"
                opacity="{LIP_HI_A}"/>
        </g>
        <g filter="url(#lipLo)">
          {band((GAP + g(LIP_LO_TILE)) / 2, g(LIP_LO_TILE))} fill="{RIM_SCATTER}"
                opacity="{LIP_LO_A}"/>
        </g>
      </g>

      <!-- lit from inside: the accent bleeding a little way out of the void and
           across the graphite either side of it. This is what stops the cut
           reading as a gap someone forgot to fill. The blur is a level ABOVE
           the mask on purpose — a filter and a mask on one element apply filter
           first and mask second, so the bleed is clipped straight back to the
           void it came from and nothing reaches the graphite at all. -->
      <g clip-path="url(#cGlyph)" opacity="{'.22' if VOID == 'filled' else '.10'}">
        <g filter="url(#glow)">
          <g mask="url(#mVoid)">
            <use xlink:href="#glyph" fill="{ACCENT_HI}"/>
          </g>
        </g>
      </g>
      {'' if VOID == 'filled' else f"""
      <g clip-path="url(#cGlyph)">
        <use xlink:href="#cut" fill="none" stroke="{ACCENT}"
             stroke-width="{f(g(6))}" stroke-opacity=".85"/>
      </g>"""}"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>atlas-review</title>
  <desc>The Atlas script A, re-poured as graphite gel, with one clean fracture
  cut square across its descending stem and vermilion filling the void. The
  marketplace superellipse is a clip, not a baked corner radius, and no drop
  shadow is baked into the tile.</desc>
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
    global VOID
    alt = "--alt" in sys.argv
    if alt:
        VOID = "open"
    out = HERE / ("icon-engineA2-open-3f19c4.svg" if alt else "icon.svg")
    out.write_text(build())
    for px in ((1024,) if alt else EXPORTS):
        name = ("icon-engineA2-open-3f19c4.png" if alt else
                ("icon.png" if px == 1024 else f"icon-{px}.png"))
        subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px),
                        "-o", str(HERE / name), str(out)], check=True)
    print(f"wrote {out.name} (scale {SCALE:.4f}, cut {CUT_ANGLE:.2f}deg, "
          f"gap {GAP_TILE:.0f}px) and "
          f"{', '.join(str(p) for p in ((1024,) if alt else EXPORTS))}px exports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
