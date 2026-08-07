#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the improve-skill icon.

Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object,
crossed with device bank #16 (the icon performs the verb) and #5 (dual-function primitive).

A curled shaving was authored and cut at round 3: in flat vector it read as a coat hanger
rather than as removed material, and the two-state split is already the evidence that
something came off. Two objects on the tile, not three.

The whole tile is the workpiece. A worn plane iron lies on a rising diagonal mid-pass.
Everything on the finished side of that diagonal is brighter and truer than the side
still to come, and the one vermilion hone line IS the boundary between them.

Geometry is authored in the blade's own local frame (local x runs along the cutting
edge, local y runs away from the cut into the un-planed region) and mapped onto the
1024 canvas by a single matrix, so the grain, the split and the blade cannot drift
out of register with each other.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import pathlib

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- frame
ANGLE = math.radians(33.0)                    # rising diagonal
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)    # along the cutting edge, up-and-right
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)   # away from the cut, into the rough side

BLADE_LEN = 640.0
BLADE_THICK = 168.0
EDGE_MID = (552.0, 560.0)                     # midpoint of the cutting edge, on the canvas
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2         # local origin: cutting edge, leading end

MATRIX = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},{AX:.3f},{AY:.3f})"


def to_canvas(lx, ly):
    return (AX + UX * lx + NX * ly, AY + UY * lx + NY * ly)


def to_local(px, py):
    dx, dy = px - AX, py - AY
    return (UX * dx + UY * dy, NX * dx + NY * dy)


# The boundary is local y = 0, extended to the canvas edges.
def boundary_at_x(x):
    # y such that n . ((x,y) - A) = 0  ->  NX*(x-AX) + NY*(y-AY) = 0
    return AY - NX * (x - AX) / NY


B_LEFT = boundary_at_x(0)
B_RIGHT = boundary_at_x(W)

# deterministic jitter, so a rebuild is byte-identical
_seed = 20260807


def rnd():
    global _seed
    _seed = (_seed * 1103515245 + 12345) % (1 << 31)
    return _seed / (1 << 31)


# ---------------------------------------------------------------- blade path
def blade_path():
    """Rounded plane iron in local space. Cutting edge (y=0) dead straight and honed;
    back edge worn, with a shallow sag and unequal corner radii."""
    L, T = BLADE_LEN, BLADE_THICK
    r_cut_lead, r_cut_trail = 11.0, 8.0        # corners on the honed edge: crisp, it is sharpened
    r_back_lead, r_back_trail = 40.0, 30.0     # corners on the worn back
    return (
        f"M {r_cut_lead:.1f} 0 "
        f"L {L - r_cut_trail:.1f} 0 "
        f"Q {L} 0 {L} {r_cut_trail:.1f} "
        f"L {L} {T - r_back_trail:.1f} "
        f"Q {L} {T} {L - r_back_trail:.1f} {T} "
        # worn back edge: a shallow sag through the middle
        f"C {L * 0.66:.1f} {T - 7.5:.1f} {L * 0.34:.1f} {T - 7.5:.1f} {r_back_lead:.1f} {T} "
        f"Q 0 {T} 0 {T - r_back_lead:.1f} "
        f"L 0 {r_cut_lead:.1f} "
        f"Q 0 0 {r_cut_lead:.1f} 0 Z"
    )


# ---------------------------------------------------------------- grain
def grain():
    """One family of grain lines running along the travel direction. The SAME line
    crosses the boundary: torn and broken on the un-planed side, continuous and fine
    on the trued side. That continuity is what makes the split read as one surface in
    two states rather than as two different materials."""
    rough, true = [], []
    x = -420.0
    while x < 1070:
        # --- trued side (local y < 0): long, even, barely there. A sheen, not a stripe.
        if rnd() < 0.62:
            op = 0.016 + rnd() * 0.020
            true.append(
                f'<path d="M {x:.1f} -20 L {x:.1f} -880" stroke="#8C7F6A" '
                f'stroke-opacity="{op:.3f}" stroke-width="{1.0 + rnd() * 0.6:.2f}"/>'
            )
        # --- un-planed side (local y > 0): short broken tooth marks. Some lines tear
        #     badly, some hardly at all, which is what stops it reading as ruled rain.
        tear = 0.30 + rnd() * 0.90
        y = 176.0
        while y < 800:
            seg = 6 + rnd() * 22 * tear
            gap = 7 + rnd() * 20
            op = (0.05 + rnd() * 0.10) * tear
            wid = 1.1 + rnd() * 1.9
            rough.append(
                f'<path d="M {x + (rnd() - 0.5) * 4:.1f} {y:.1f} '
                f'L {x + (rnd() - 0.5) * 4:.1f} {y + seg:.1f}" stroke="#6B6152" '
                f'stroke-opacity="{op:.3f}" stroke-width="{wid:.2f}"/>'
            )
            y += seg + gap
        x += 15.0 + rnd() * 7.0
    return "\n      ".join(rough), "\n      ".join(true)


ROUGH_GRAIN, TRUE_GRAIN = grain()
BLADE = blade_path()

# ---------------------------------------------------------------- document
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}" role="img" aria-label="improve-skill">
<title>improve-skill</title>
<!--
  Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object.
  The tile is the workpiece. A worn plane iron lies mid-pass on a rising diagonal; the
  surface behind it is brighter and truer than the surface ahead, and the single
  vermilion hone line IS the boundary between the two states.
  Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
  Full-bleed 1024 artwork; the squircle is a CLIP for preview only. No baked corners,
  no baked drop shadow. Generated by build_icon.py - edit there, not here.
-->
<defs>
  <clipPath id="tileMask"><path d="{SQUIRCLE}"/></clipPath>
  <!-- everything the pass has already trued, used to keep the hone glow off the rough side -->
  <clipPath id="truedSide">
    <path d="M0 {B_LEFT:.1f} L{W} {B_RIGHT:.1f} L{W} {W} L0 {W} Z"/>
  </clipPath>

  <!-- the un-planed side: cooler, greyer, losing light as it nears the cut -->
  <linearGradient id="roughField" x1="120" y1="58" x2="520" y2="676" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#E4E1D8"/>
    <stop offset="0.52" stop-color="#D3CEC3"/>
    <stop offset="1" stop-color="#BEB8AB"/>
  </linearGradient>

  <!-- the trued side: brighter and warmer, brightest right at the fresh cut -->
  <linearGradient id="truedField" x1="330" y1="420" x2="900" y2="1000" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFFFFE"/>
    <stop offset="0.42" stop-color="#FCFAF3"/>
    <stop offset="1" stop-color="#F1EBDD"/>
  </linearGradient>

  <!-- blade body: lit on the worn back, near-black at the honed edge -->
  <linearGradient id="bladeBody" x1="0" y1="{BLADE_THICK}" x2="0" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#4B5159"/>
    <stop offset="0.30" stop-color="#31363D"/>
    <stop offset="0.74" stop-color="#1E2126"/>
    <stop offset="1" stop-color="#101215"/>
  </linearGradient>

  <!-- the honed bevel face, picking up the hone's own warmth -->
  <linearGradient id="bevelFace" x1="0" y1="34" x2="0" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#22252A" stop-opacity="0"/>
    <stop offset="0.50" stop-color="#3B2C2A" stop-opacity="0.80"/>
    <stop offset="1" stop-color="#6E3A2A" stop-opacity="1"/>
  </linearGradient>

  <!-- the hone glow spilling onto the surface it has just trued -->
  <linearGradient id="honeBloom" x1="0" y1="0" x2="0" y2="-46" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#F2542D" stop-opacity="0.20"/>
    <stop offset="0.30" stop-color="#F4703F" stop-opacity="0.06"/>
    <stop offset="1" stop-color="#FFB38A" stop-opacity="0"/>
  </linearGradient>

  <linearGradient id="honeCore" x1="0" y1="0" x2="{BLADE_LEN}" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#C4341A"/>
    <stop offset="0.32" stop-color="#F2542D"/>
    <stop offset="0.64" stop-color="#FF7C46"/>
    <stop offset="1" stop-color="#D33F1F"/>
  </linearGradient>

  <radialGradient id="vignette" cx="0.44" cy="0.36" r="0.76">
    <stop offset="0.50" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#3A3226" stop-opacity="0.26"/>
  </radialGradient>

  <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
    <feGaussianBlur stdDeviation="15"/>
  </filter>
  <filter id="honeGlow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="7"/>
  </filter>
</defs>

<g clip-path="url(#tileMask)">

  <g id="bg">
    <!-- the surface still to be trued -->
    <path d="M0 0 L{W} 0 L{W} {B_RIGHT:.1f} L0 {B_LEFT:.1f} Z" fill="url(#roughField)"/>
    <!-- the surface already trued: brighter, warmer, and truer -->
    <path d="M0 {B_LEFT:.1f} L{W} {B_RIGHT:.1f} L{W} {W} L0 {W} Z" fill="url(#truedField)"/>
    <!-- cushion: a gentle edge vignette, so the tile is a cushion and not a print -->
    <rect width="{W}" height="{W}" fill="url(#vignette)"/>
  </g>

  <g id="mid" fill="none" stroke-linecap="round">
    <!-- one grain family crossing the boundary: torn above it, true below it -->
    <g transform="{MATRIX}">
      {TRUE_GRAIN}
      {ROUGH_GRAIN}
    </g>

    <!-- contact shadow, from the one soft top-left light -->
    <g filter="url(#softShadow)">
      <path d="{BLADE}" transform="translate(15,19) {MATRIX}" fill="#5B5346" fill-opacity="0.28"/>
    </g>

    <!-- the hone's light on the surface it just cut. Clipped to the trued side and drawn
         under the blade, so it can only ever read as spill from the edge. -->
    <g clip-path="url(#truedSide)">
      <path d="M 15 0 L {BLADE_LEN - 12:.0f} 0 L {BLADE_LEN - 12:.0f} -46 L 15 -46 Z"
            transform="{MATRIX}" fill="url(#honeBloom)"/>
      <path d="M 24 0 L {BLADE_LEN - 20:.0f} 0" transform="{MATRIX}" stroke="#FF7038"
            stroke-opacity="0.62" stroke-width="15" filter="url(#honeGlow)"/>
    </g>
  </g>

  <g id="fg">
    <g transform="{MATRIX}">
      <!-- the plane iron: one solid chunky silhouette, the carrying shape at every size -->
      <path d="{BLADE}" fill="url(#bladeBody)"/>
      <!-- the honed bevel face -->
      <path d="M 20 0 L {BLADE_LEN - 16:.0f} 0 L {BLADE_LEN - 16:.0f} 34 L 20 34 Z" fill="url(#bevelFace)"/>
      <!-- wear on the back: two faint grind striations -->
      <path d="M 78 134 L {BLADE_LEN - 98:.0f} 134" stroke="#7E8797" stroke-opacity="0.17" stroke-width="3"/>
      <path d="M 128 112 L {BLADE_LEN - 152:.0f} 112" stroke="#7E8797" stroke-opacity="0.10" stroke-width="2"/>
    </g>
  </g>

  <g id="highlight" fill="none">
    <g transform="{MATRIX}">
      <!-- the vermilion hone line: the cutting edge, and the before/after boundary, one shape -->
      <path d="M 15 0.5 L {BLADE_LEN - 12:.0f} 0.5" stroke="url(#honeCore)" stroke-width="11.5"
            stroke-linecap="butt"/>
      <path d="M 58 -0.4 L {BLADE_LEN - 62:.0f} -0.4" stroke="#FFD2B2" stroke-opacity="0.95"
            stroke-width="3.4" stroke-linecap="round"/>
      <!-- rim light along the worn back, from the same top-left source -->
      <path d="M 46 {BLADE_THICK - 2:.0f} C {BLADE_LEN * 0.34:.0f} {BLADE_THICK - 9:.0f} {BLADE_LEN * 0.66:.0f} {BLADE_THICK - 9:.0f} {BLADE_LEN - 36:.0f} {BLADE_THICK - 2:.0f}"
            stroke="#A6B0BE" stroke-opacity="0.55" stroke-width="4.5" stroke-linecap="round"/>
    </g>
    <!-- cushion rim light around the tile perimeter -->
    <path d="{SQUIRCLE}" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="3"/>
  </g>

</g>
</svg>
"""

(ASSETS / "icon.svg").write_text(svg)
print(f"wrote icon.svg  boundary (0,{B_LEFT:.0f}) -> ({W},{B_RIGHT:.0f})")
xs = [to_canvas(x, y)[0] for x in (0, BLADE_LEN) for y in (0, BLADE_THICK)]
ys = [to_canvas(x, y)[1] for x in (0, BLADE_LEN) for y in (0, BLADE_THICK)]
print(f"blade bbox x {min(xs):.0f}-{max(xs):.0f} ({max(xs)-min(xs):.0f}px = {(max(xs)-min(xs))/W*100:.1f}% of tile)")
print(f"           y {min(ys):.0f}-{max(ys):.0f}   focal centre ({(min(xs)+max(xs))/2:.0f},{(min(ys)+max(ys))/2:.0f})")
print(f"safe-zone margins  L{min(xs):.0f} R{W-max(xs):.0f} T{min(ys):.0f} B{W-max(ys):.0f}")
