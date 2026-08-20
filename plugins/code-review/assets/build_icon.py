#!/usr/bin/env python3
"""build_icon.py — the layered SVG master for the `code-review` plugin icon.

Geometry and material live here as named constants so a later fidelity round is
a parameter edit rather than path surgery. Run it and it writes icon.svg beside
itself; `--concept seam` writes the losing take instead, which the audit sheet
scores.

The concept, in one line: a graphite ledger slab whose rows run into a column
that has been cut clean out of it, the cut wall chamfered in vermilion, the
porcelain ground showing through. The signature move is the through-cut — an
absence that was machined rather than one that merely happened, which is the
coverage ledger's not-checked column made physical.

House values were sampled out of the marketplace's own icons rather than
guessed: the porcelain runs #FBF7F0 at the top to #DED4C2 at the bottom across
atlas-publish, clarify and test-campaign, and the accent sits at #C4622D with
highlights near #EC7F4C and shadows near #BA3E19.

Two sizing rules from the skill's recipe library are load-bearing here:

  * an element the identity depends on needs its SMALLEST dimension over ~96px
    at 1024, because 96/64 is 1.5px at the 16px display size. The aperture is
    168px wide (2.6px) and every graphite margin around the chamfer clears
    100px, so the cut reads as an interior hole rather than a notch off an edge.

  * an accent touching the ground directly cannot clear 3:1 against both the
    porcelain and the body, so the chamfer's outer boundary is re-stroked with
    the slab's own seat edge and borrows the body's 12:1 instead.
"""

from __future__ import annotations

import argparse
import pathlib

W = 1024

# ---------------------------------------------------------------- ground
GROUND_TOP = "#FBF7F0"
GROUND_BOT = "#DED4C2"
CUSHION_AT = (300, 236)
CUSHION_R = 720
CUSHION_OPACITY = 0.62
VIGNETTE = "#7A6544"
VIGNETTE_OPACITY = 0.11

# ---------------------------------------------------------------- the slab
#
# Narrowed from 784x704 to match the raster reference's measured 701x718 body
# and its generous porcelain margin, which is what makes the tile read as an
# object on a shelf rather than as a card filling its frame.
SLAB = (152, 158, 720, 716)          # x, y, w, h
SLAB_R = 104
SLAB_TOP = "#45464B"                 # ref slab mean is (55,52,53); the first
SLAB_MID = "#313339"                 # take ran (41,42,47) — too dark, too blue
SLAB_BOT = "#23242A"
SLAB_UNDER = "#16171A"               # the body's own thickness, seen at the foot
SLAB_LIFT = (10, 16)                 # how far that thickness shows, dx / dy
SLAB_RIM = 0.13                      # white stroke around the body
SLAB_TOP_BAND = 0.22                 # extra light on the top face
SLAB_FOOT_BAND = 0.36                # the underside going to shadow
SLAB_SHEEN = 0.07                    # broad diagonal gel sheen
SLAB_FORM = 0.22                     # form shadow in the unlit bottom-right
# Both of these are OFF, and measured rather than assumed. r03 added them
# together and the gate rejected at all five sizes; r04 and r05 split them into
# one edit each and both still lost (cushion -0.0736, inner AO -0.0164). The
# reference's body is darker and flatter than either instinct wanted, and the
# blind out-of-family judge flipped its answer when the pair was swapped, which
# the panel protocol records as a tie rather than as support. Left as named
# constants so the finding survives; do not switch them on without re-scoring.
SLAB_CUSHION = 0.00                  # the key light pooling on the top-left face
SLAB_INNER_AO = 0.00                 # occlusion just inside the body's own edge

SHADOW_TINT = "#3A2A18"              # warm, never blue: corpus lesson
SHADOW_FAR = (34, 28, 0.28)          # dy, blur, opacity
SHADOW_NEAR = (12, 11, 0.22)

# ---------------------------------------------------------------- the rows
ROW_X = 208
ROW_W = 280                          # stops 20px short of the cut: the rows run
ROW_H = 18                           # into the column that is missing
ROW_YS = (372, 468, 564, 660)
ROW_INK = "#161719"
ROW_INK_OPACITY = 0.66
ROW_LIP = "#5C5F66"                  # the engraved row's lit lower lip
ROW_LIP_OPACITY = 0.30

# ---------------------------------------------------------------- the cut
APERTURE = (552, 306, 168, 420)      # x, y, w, h — 168 wide is 2.6px at 16px
APERTURE_R = 46
CHAMFER = 40                         # the visible thickness of the cut wall

# Every graphite margin around the chamfer clears 100px, so the cut reads as an
# interior hole at 16px rather than as a notch bitten out of an edge.
ACCENT_LIT = "#F09A63"
ACCENT_MID = "#D4703A"
ACCENT_CORE = "#B85326"
ACCENT_DEEP = "#93380E"               # ref accent bottoms out at (151,30,2)
SEAT_EDGE = "#121316"
SEAT_EDGE_OPACITY = 0.58
CHAMFER_SPECULAR = 0.42
SPECULAR_WHITE = "#FFE6D2"            # warm; a pure white specular over the
                                      # accent blew to (255,255,170) in take r00

FLOOR_SHADED = "#CCBEA3"             # porcelain under the slab, in shadow
FLOOR_LIT = "#F6ECD8"
FLOOR_BOUNCE = "#C4622D"
FLOOR_BOUNCE_OPACITY = 0.30
BLEED_OPACITY = 0.42                 # light escaping the cut onto the ground

# ---------------------------------------------------------------- losing take
SEAM_Y = 512
SEAM_H = 46
WEDGES = (  # (tip_x, tip_y, back_x, back_y, half_width_at_back)
    (452, 486, 132, 262, 84),
    (556, 480, 596, 220, 92),
    (628, 542, 918, 762, 88),
)


def rrect(x: float, y: float, w: float, h: float, r: float) -> str:
    """A rounded rectangle as a closed path, so it can join a compound path."""
    r = min(r, w / 2, h / 2)
    return (
        f"M{x + r:.1f},{y:.1f} H{x + w - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + r:.1f} "
        f"V{y + h - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w - r:.1f},{y + h:.1f} "
        f"H{x + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x:.1f},{y + h - r:.1f} "
        f"V{y + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y:.1f} Z"
    )


def squircle() -> str:
    p = pathlib.Path(__file__).resolve().parent / "squircle-path.txt"
    return p.read_text().strip()


def defs(concept: str) -> str:
    sx, sy, sw, sh = SLAB
    ax, ay, aw, ah = APERTURE
    ox, oy = ax - CHAMFER, ay - CHAMFER
    ow, oh = aw + 2 * CHAMFER, ah + 2 * CHAMFER

    d = [
        f'<clipPath id="tile"><path d="{squircle()}"/></clipPath>',

        f'<linearGradient id="ground" x1="0" y1="0" x2="0" y2="{W}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{GROUND_TOP}"/>'
        f'<stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>',

        f'<radialGradient id="cushion" cx="{CUSHION_AT[0]}" cy="{CUSHION_AT[1]}" '
        f'r="{CUSHION_R}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{CUSHION_OPACITY}"/>'
        f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',

        f'<radialGradient id="vignette" cx="512" cy="512" r="716" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="{VIGNETTE_OPACITY}"/>'
        f'</radialGradient>',

        f'<filter id="blurFar" x="-25%" y="-25%" width="150%" height="150%">'
        f'<feGaussianBlur stdDeviation="{SHADOW_FAR[1]}"/></filter>',
        f'<filter id="blurNear" x="-25%" y="-25%" width="150%" height="150%">'
        f'<feGaussianBlur stdDeviation="{SHADOW_NEAR[1]}"/></filter>',
        '<filter id="blurSoft" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="9"/></filter>',
        '<filter id="blurTight" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="4"/></filter>',
    ]

    if concept == "cut":
        d += [
            f'<linearGradient id="slab" x1="0" y1="{sy}" x2="0" y2="{sy + sh}" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{SLAB_TOP}"/>'
            f'<stop offset="0.58" stop-color="{SLAB_MID}"/>'
            f'<stop offset="1" stop-color="{SLAB_BOT}"/></linearGradient>',

            f'<radialGradient id="cushionSlab" cx="{sx + sw * 0.30}" cy="{sy + sh * 0.24}" '
            f'r="{sw * 0.72}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{SLAB_CUSHION}"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',

            f'<radialGradient id="form" cx="{sx + sw * 0.86}" cy="{sy + sh * 0.92}" '
            f'r="{sw * 0.78}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#0A0906" stop-opacity="{SLAB_FORM}"/>'
            f'<stop offset="1" stop-color="#0A0906" stop-opacity="0"/></radialGradient>',

            f'<linearGradient id="topband" x1="0" y1="{sy}" x2="0" y2="{sy + 96}" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{SLAB_TOP_BAND}"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>',

            f'<linearGradient id="footband" x1="0" y1="{sy + sh - 130}" x2="0" y2="{sy + sh}" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#0C0D0F" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#0C0D0F" stop-opacity="{SLAB_FOOT_BAND}"/>'
            f'</linearGradient>',

            f'<linearGradient id="sheen" x1="{sx}" y1="{sy}" x2="{sx + sw * 0.7}" '
            f'y2="{sy + sh * 0.8}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{SLAB_SHEEN}"/>'
            f'<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>',

            # The cut wall. Top and left faces turn toward the key light and go
            # bright; the bottom and right faces turn away. A single axis from
            # the opening's top-left to its bottom-right carries both.
            f'<linearGradient id="wall" x1="{ox + 30}" y1="{oy + 10}" '
            f'x2="{ox + ow - 20}" y2="{oy + oh}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{ACCENT_LIT}"/>'
            f'<stop offset="0.34" stop-color="{ACCENT_MID}"/>'
            f'<stop offset="0.70" stop-color="{ACCENT_CORE}"/>'
            f'<stop offset="1" stop-color="{ACCENT_DEEP}"/></linearGradient>',

            # The floor of the cut is the porcelain the slab stands on, so it is
            # shaded by the near wall at the top-left and lit at the bottom-right.
            f'<linearGradient id="floor" x1="{ax}" y1="{ay}" x2="{ax + aw}" '
            f'y2="{ay + ah}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{FLOOR_SHADED}"/>'
            f'<stop offset="0.55" stop-color="#E9DDC8"/>'
            f'<stop offset="1" stop-color="{FLOOR_LIT}"/></linearGradient>',

            # Light that got through the cut and landed on the porcelain under
            # the slab's foot. It is the cue that says the opening is a hole
            # rather than a panel, and the raster reference carries it plainly:
            # its accent pixels run to y=951, well below the body's own y=875.
            f'<radialGradient id="bleed" cx="{ax + aw / 2}" cy="{sy + sh + 14}" '
            f'r="{aw * 1.5}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{FLOOR_BOUNCE}" stop-opacity="{BLEED_OPACITY}"/>'
            f'<stop offset="1" stop-color="{FLOOR_BOUNCE}" stop-opacity="0"/></radialGradient>',

            f'<radialGradient id="bounce" cx="{ax + aw * 0.72}" cy="{ay + ah * 0.80}" '
            f'r="{aw * 1.15}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{FLOOR_BOUNCE}" stop-opacity="{FLOOR_BOUNCE_OPACITY}"/>'
            f'<stop offset="1" stop-color="{FLOOR_BOUNCE}" stop-opacity="0"/></radialGradient>',

            f'<clipPath id="slabClip"><path d="{rrect(sx, sy, sw, sh, SLAB_R)}"/></clipPath>',
            f'<clipPath id="apertureClip"><path d="{rrect(ax, ay, aw, ah, APERTURE_R)}"/></clipPath>',
        ]
    else:
        d += [
            f'<linearGradient id="seam" x1="0" y1="{SEAM_Y - SEAM_H}" x2="0" '
            f'y2="{SEAM_Y + SEAM_H}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{ACCENT_LIT}"/>'
            f'<stop offset="0.5" stop-color="{ACCENT_CORE}"/>'
            f'<stop offset="1" stop-color="{ACCENT_DEEP}"/></linearGradient>',
            f'<linearGradient id="wedge" x1="0" y1="180" x2="0" y2="820" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#41444B"/>'
            f'<stop offset="1" stop-color="#1D1F24"/></linearGradient>',
            f'<radialGradient id="seamGlow" cx="512" cy="{SEAM_Y}" r="470" '
            f'gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{FLOOR_BOUNCE}" stop-opacity="0.26"/>'
            f'<stop offset="1" stop-color="{FLOOR_BOUNCE}" stop-opacity="0"/></radialGradient>',
        ]
    return "\n    ".join(d)


def layer_bg() -> str:
    return (
        '  <g id="bg">\n'
        f'    <rect width="{W}" height="{W}" fill="url(#ground)"/>\n'
        f'    <rect width="{W}" height="{W}" fill="url(#cushion)"/>\n'
        f'    <rect width="{W}" height="{W}" fill="url(#vignette)"/>\n'
        '  </g>'
    )


def concept_cut() -> str:
    sx, sy, sw, sh = SLAB
    ax, ay, aw, ah = APERTURE
    ox, oy = ax - CHAMFER, ay - CHAMFER
    ow, oh = aw + 2 * CHAMFER, ah + 2 * CHAMFER

    body = rrect(sx, sy, sw, sh, SLAB_R)
    hole = rrect(ax, ay, aw, ah, APERTURE_R)
    chamfer_outer = rrect(ox, oy, ow, oh, APERTURE_R + CHAMFER)

    rows = "\n".join(
        f'    <path d="{rrect(ROW_X, y, ROW_W, ROW_H, ROW_H / 2)}" fill="{ROW_INK}" '
        f'fill-opacity="{ROW_INK_OPACITY}"/>\n'
        f'    <path d="{rrect(ROW_X, y + ROW_H - 5, ROW_W, 5, 2.5)}" fill="{ROW_LIP}" '
        f'fill-opacity="{ROW_LIP_OPACITY}"/>'
        for y in ROW_YS
    )

    return f"""  <g id="shadow">
    <!-- Light through the opening, reaching the porcelain past the slab's foot.
         Drawn before the body so the body occludes it, which is what makes the
         glow read as coming from underneath rather than as painted on top. -->
    <rect x="{ax - aw}" y="{sy + sh - 150}" width="{aw * 3}" height="330" fill="url(#bleed)"/>
    <path d="{rrect(sx + 6, sy + SHADOW_FAR[0], sw - 12, sh, SLAB_R)}" fill="{SHADOW_TINT}"
          fill-opacity="{SHADOW_FAR[2]}" filter="url(#blurFar)"/>
    <path d="{rrect(sx + 14, sy + SHADOW_NEAR[0], sw - 28, sh, SLAB_R)}" fill="{SHADOW_TINT}"
          fill-opacity="{SHADOW_NEAR[2]}" filter="url(#blurNear)"/>
  </g>

  <g id="slab">
    <!-- The body's own thickness, showing at the foot and the shaded flank. -->
    <path d="{rrect(sx + SLAB_LIFT[0], sy + SLAB_LIFT[1], sw, sh, SLAB_R)}"
          fill="{SLAB_UNDER}"/>
    <!-- Body and cut as one compound path: the opening really is a hole, so the
         ground beneath is what shows through it rather than a pasted-on panel. -->
    <path d="{body} {hole}" fill-rule="evenodd" fill="url(#slab)"/>
    <g clip-path="url(#slabClip)">
      <rect x="{sx}" y="{sy}" width="{sw}" height="96" fill="url(#topband)"/>
      <rect x="{sx}" y="{sy + sh - 130}" width="{sw}" height="130" fill="url(#footband)"/>
      <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#cushionSlab)"/>
      <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#sheen)"/>
      <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#form)"/>
      <path d="{body}" fill="none" stroke="#0B0A08" stroke-opacity="{SLAB_INNER_AO}"
            stroke-width="18" filter="url(#blurSoft)"/>
    </g>
    <path d="{body}" fill="none" stroke="#FFFFFF" stroke-opacity="{SLAB_RIM}" stroke-width="3"/>
  </g>

  <g id="rows">
{rows}
  </g>

  <g id="cut">
    <!-- The floor of the opening: porcelain in the slab's shadow, with the warm
         bounce off the lit wall landing where the light actually reaches. -->
    <g clip-path="url(#apertureClip)">
      <path d="{hole}" fill="url(#floor)"/>
      <path d="{hole}" fill="url(#bounce)"/>
      <path d="{rrect(ax - 26, ay - 30, aw + 52, 56, 28)}" fill="#4A3418" fill-opacity="0.30"
            filter="url(#blurSoft)"/>
      <path d="{rrect(ax - 30, ay - 20, 56, ah + 40, 28)}" fill="#4A3418" fill-opacity="0.22"
            filter="url(#blurSoft)"/>
    </g>

    <!-- The chamfered wall: the slab's own thickness, exposed by the cut. -->
    <path d="{chamfer_outer} {hole}" fill-rule="evenodd" fill="url(#wall)"/>

    <!-- Specular along the top face of the wall, which is the face turned into
         the key light. -->
    <path d="{rrect(ox + 50, oy + 8, ow - 100, 14, 7)}" fill="{SPECULAR_WHITE}"
          fill-opacity="{CHAMFER_SPECULAR}" filter="url(#blurTight)"/>
    <path d="{rrect(ox + 7, oy + 60, 13, oh - 190, 6)}" fill="{SPECULAR_WHITE}"
          fill-opacity="{CHAMFER_SPECULAR * 0.55}" filter="url(#blurTight)"/>

    <!-- The seat edge, drawn a second time over the accent so the boundary the
         eye uses is the graphite body's rather than the accent's own. -->
    <path d="{chamfer_outer}" fill="none" stroke="{SEAT_EDGE}"
          stroke-opacity="{SEAT_EDGE_OPACITY}" stroke-width="4"/>
    <path d="{hole}" fill="none" stroke="#6B4520" stroke-opacity="0.40" stroke-width="5"/>
  </g>"""


def concept_seam() -> str:
    wedges = []
    for tx, ty, bx, by, half in WEDGES:
        dx, dy = bx - tx, by - ty
        n = (dx * dx + dy * dy) ** 0.5
        px, py = -dy / n * half, dx / n * half
        wedges.append(
            f'    <path d="M{tx:.0f},{ty:.0f} L{bx + px:.0f},{by + py:.0f} '
            f'L{bx - px:.0f},{by - py:.0f} Z" fill="url(#wedge)" '
            f'stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="3" '
            f'stroke-linejoin="round"/>'
        )
    return (
        '  <g id="seam">\n'
        f'    <rect x="0" y="{SEAM_Y - 470}" width="{W}" height="940" fill="url(#seamGlow)"/>\n'
        f'    <rect x="0" y="{SEAM_Y - SEAM_H / 2:.0f}" width="{W}" height="{SEAM_H}" '
        'fill="url(#seam)"/>\n'
        '  </g>\n\n'
        '  <g id="wedges">\n' + "\n".join(wedges) + "\n  </g>"
    )


def build(concept: str) -> str:
    art = concept_cut() if concept == "cut" else concept_seam()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}"
     viewBox="0 0 {W} {W}">
  <title>code-review</title>
  <defs>
    {defs(concept)}
  </defs>
  <g clip-path="url(#tile)">
{layer_bg()}

{art}
  </g>
</svg>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--concept", choices=("cut", "seam"), default="cut")
    ap.add_argument("--out")
    args = ap.parse_args()
    here = pathlib.Path(__file__).resolve().parent
    out = pathlib.Path(args.out) if args.out else here / (
        "icon.svg" if args.concept == "cut" else "icon-engineA-seam.svg")
    out.write_text(build(args.concept), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
