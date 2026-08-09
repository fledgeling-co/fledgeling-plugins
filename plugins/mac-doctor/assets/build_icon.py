#!/usr/bin/env python3
"""Engine A: the layered SVG master for mac-doctor.

Geometry and material live as named constants so a fidelity round is a
parameter edit rather than path surgery.

Values sampled from the corpus rather than assumed (create-mac-icon step 4):

  House porcelain, from armada-sync / dossier-report / create-mac-icon at 256:
      top    (253,253,252)   mid (245,238,231)   bottom (237,233,223)
  This is WARM. Apple's own porcelain is cool (254,255,255 -> 223,227,235);
  the family's is cream, and family consistency wins over the platform sample.

  Gel falloff, Safari dial top to bottom:
      (112,184,239) -> (57,113,241), about a 40% luminance drop at constant
  hue. The object is a value ramp, tone on tone, never a hue shift.

  Contact shadow, Safari, just under the object:
      local ground (233,234,235), shadow (205,215,232). About 12% darker and
  tinted toward the object's own hue, not a neutral grey. So the graphite
  ring casts cool and the ember wedge casts warm.

The composition is the capacity arc: a ring 290 degrees closed in graphite over
a recessed track, with one wedge lifted out of the gap in the family ember. The
gap is the message.
"""

import math
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
# assets -> mac-doctor -> plugins, then across to the canonical path
SQUIRCLE = (Path(__file__).resolve().parents[2] / "create-mac-icon" /
            "assets" / "squircle-path.txt")

# ---- geometry ---------------------------------------------------------------
S = 1024
CX = CY = 512
R = 292                 # ring radius
W = 108                 # ring stroke
GAP_MID = -55.0         # bisector of the gap, degrees, 0 = +x, y down
# Half-width of the gap. 35 made a 70 degree hole, which is 19% of the ring
# empty; the machine this was built for was at 6% free. 25 is both truer and
# more legible, because a smaller hole lets the freed wedge match its width.
GAP_HALF = 36.0
# The reclaimed segment now sits INLINE in the ring rather than floating outside
# it. Detached said "a piece came out"; inline says what the tool actually
# reports, which is three quantities at once: dark for used, ember for just
# reclaimed, and the remaining hole for free. It is also the conventional gauge
# idiom, so it reads without being learned.
#
# The segment occupies the leading part of the hole and abuts the ring's end, so
# it uses butt caps like the ring. Round caps would overlap the dark arc and
# round off the join that makes the two read as one track.
EMBER_SPAN = 44.0
SCALE = 0.93            # composition scale, keeps the lifted wedge off the edge

# ---- material ---------------------------------------------------------------
GROUND_TOP, GROUND_MID, GROUND_BOT = "#FDFDFC", "#F5EEE7", "#EDE9DF"
# Graphite gel, value ramp. Nudged bluer than the first take: the raster's body
# sampled (60,81,110) against the master's (75,85,99), and the cooler read is
# part of why its material looked richer.
RING_HI, RING_LO = "#5C6880", "#252B36"
RING_RIM = "#8E97AA"                            # top-edge rim light
EMBER_HI, EMBER_MID, EMBER_LO = "#FFB483", "#F4652C", "#D8410F"
EMBER_RIM = "#FFD3B4"
SHADOW_COOL = "#2A2F38"
SHADOW_WARM = "#C0430F"


def pt(deg, r=R):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def arc(a0, a1, large, sweep, r=R):
    x0, y0 = pt(a0, r)
    x1, y1 = pt(a1, r)
    return f"M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} {sweep} {x1:.1f} {y1:.1f}"


def build():
    squircle = SQUIRCLE.read_text().strip()

    ring_start = GAP_MID + GAP_HALF          # clockwise from here...
    ring_end = GAP_MID - GAP_HALF + 360      # ...all the way round
    ring_d = arc(ring_start, ring_end - 360, 1, 1)

    hole_start = GAP_MID - GAP_HALF          # where the dark ring stops
    wedge_d = arc(hole_start, hole_start + EMBER_SPAN, 0, 1)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
<defs>
  <!-- PLANE 1: ground. A cushion, not a print: vertical ramp, edge vignette,
       and a faint inner rim light around the perimeter. -->
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="{GROUND_TOP}"/>
    <stop offset="0.52" stop-color="{GROUND_MID}"/>
    <stop offset="1"    stop-color="{GROUND_BOT}"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.30" cy="0.26" r="0.92">
    <stop offset="0"    stop-color="#FFFFFF" stop-opacity="0.55"/>
    <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="1"    stop-color="#8C8577" stop-opacity="0.16"/>
  </radialGradient>

  <!-- PLANE 3: the gel ring. Value ramp at constant hue, per the Safari sample. -->
  <linearGradient id="ring" x1="0.18" y1="0" x2="0.82" y2="1">
    <stop offset="0"    stop-color="{RING_HI}"/>
    <stop offset="0.55" stop-color="#3B4250"/>
    <stop offset="1"    stop-color="{RING_LO}"/>
  </linearGradient>
  <linearGradient id="ringRim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="{RING_RIM}" stop-opacity="0.85"/>
    <stop offset="0.4" stop-color="{RING_RIM}" stop-opacity="0"/>
  </linearGradient>
  <!-- Edge catches fade with the light: strong where the form faces the top
       light, gone by the time the curve turns away. -->
  <linearGradient id="edgeTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="#C9D2E2" stop-opacity="0.90"/>
    <stop offset="0.38" stop-color="#C9D2E2" stop-opacity="0.22"/>
    <stop offset="0.75" stop-color="#C9D2E2" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="edgeInner" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0"    stop-color="#93A0B8" stop-opacity="0.55"/>
    <stop offset="0.45" stop-color="#93A0B8" stop-opacity="0.10"/>
    <stop offset="1"    stop-color="#93A0B8" stop-opacity="0"/>
  </linearGradient>

  <!-- PLANE 3b: the freed wedge, the one warm element in the icon. -->
  <linearGradient id="ember" x1="0.1" y1="1" x2="0.9" y2="0">
    <stop offset="0"    stop-color="{EMBER_LO}"/>
    <stop offset="0.5"  stop-color="{EMBER_MID}"/>
    <stop offset="1"    stop-color="{EMBER_HI}"/>
  </linearGradient>
  <linearGradient id="emberEdge" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="{EMBER_RIM}" stop-opacity="0.95"/>
    <stop offset="0.45" stop-color="{EMBER_RIM}" stop-opacity="0.20"/>
    <stop offset="0.8"  stop-color="{EMBER_RIM}" stop-opacity="0"/>
  </linearGradient>

  <!-- Contact shadows, tinted toward each object's own hue. -->
  <filter id="ringShadow" x="-30%" y="-30%" width="160%" height="170%">
    <feDropShadow dx="0" dy="16" stdDeviation="20"
                  flood-color="{SHADOW_COOL}" flood-opacity="0.26"/>
    <feDropShadow dx="0" dy="4" stdDeviation="5"
                  flood-color="{SHADOW_COOL}" flood-opacity="0.20"/>
  </filter>
  <filter id="emberShadow" x="-60%" y="-60%" width="220%" height="220%">
    <feDropShadow dx="0" dy="14" stdDeviation="17"
                  flood-color="{SHADOW_WARM}" flood-opacity="0.34"/>
    <feDropShadow dx="0" dy="3" stdDeviation="4"
                  flood-color="{SHADOW_WARM}" flood-opacity="0.22"/>
  </filter>

  <clipPath id="sq"><path d="{squircle}"/></clipPath>
</defs>

<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#ground)"/>
  <rect width="{S}" height="{S}" fill="url(#vignette)"/>
  <!-- inner rim light: the perimeter catch that stops the tile reading as a print -->
  <path d="{squircle}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="3"/>

  <g transform="translate({CX},{CY}) scale({SCALE}) translate({-CX},{-CY})">
    <!-- No track. This was the defect reported twice as "wrong placement of
         the red section", and the placement was correct both times: measured on
         the render, the gap centred at -54 degrees and the ember at -55, widths
         48 and 50. What was wrong was that a visible track makes the gap read as
         a filled lighter segment, so the mark said "two-tone ring with an orange
         blob nearby" instead of "ring with a piece removed, and there it is".
         The gauge convention costs more than it buys here. -->

    <!-- the filled capacity, 290 degrees of graphite gel -->
    <g filter="url(#ringShadow)">
      <path d="{ring_d}" fill="none" stroke="url(#ring)"
            stroke-width="{W}" stroke-linecap="butt"/>
    </g>
    <!-- Edge catches as CONCENTRIC strokes, not a displaced copy. A ring lit
         from above catches light along its outer top curve and bounces a
         weaker line along the inner curve; the raster take reads richer
         largely because it has both. Clipped to the filled arc so the empty
         track stays matte. -->
    <path d="{arc(ring_start, ring_end - 360, 1, 1, R + W/2 - 5)}" fill="none"
          stroke="url(#edgeTop)" stroke-width="9" stroke-linecap="round"/>
    <path d="{arc(ring_start, ring_end - 360, 1, 1, R - W/2 + 6)}" fill="none"
          stroke="url(#edgeInner)" stroke-width="7" stroke-linecap="round"/>

    <!-- the reclaimed segment, inline and abutting the ring -->
    <path d="{wedge_d}" fill="none" stroke="url(#ember)"
          stroke-width="{W}" stroke-linecap="butt"/>
    <path d="{arc(hole_start, hole_start + EMBER_SPAN, 0, 1, R + W/2 - 5)}" fill="none"
          stroke="url(#emberEdge)" stroke-width="9" stroke-linecap="round"/>
  </g>
</g>
</svg>
'''


def main():
    svg = build()
    master = OUT / "icon.svg"
    master.write_text(svg)
    for size, name in ((1024, "icon.png"), (256, "icon-256.png"), (128, "icon-128.png"),
                       (32, "icon-32.png"), (16, "icon-16.png")):
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                        str(master), "-o", str(OUT / name)], check=True)
    print(f"wrote {master} and 5 rasters")


if __name__ == "__main__":
    sys.exit(main())
