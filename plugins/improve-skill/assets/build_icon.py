#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the improve-skill icon.

Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object,
crossed with device bank #16 (the icon performs the verb) and #5 (dual-function primitive).

MATERIAL REBUILD (round 4). The first master read flat: a slab with a line under it.
This one is built as a real extruded solid - a top face lifted off the ground and a
front face dropping back down to it - so the block has the mass the raster take had.
The ground contact of that front face IS the local y=0 line, which IS the before/after
boundary, which IS the vermilion hone. One line still does three jobs; it now also
does a fourth, being where the object meets the ground.

Polarity is the fix the raster never made: the trued side must measure BRIGHTER than
the un-planed side. Verified by measure.py on every render, not eyeballed.

The whole tile is the workpiece. A worn plane iron lies on a rising diagonal mid-pass.
Everything on the finished side of that diagonal is brighter and truer than the side
still to come, and the one vermilion hone line IS the boundary between them.

Geometry is authored in the blade's own local frame (local x runs along the cutting
edge, local y runs away from the cut into the un-planed region) and mapped onto the
1024 canvas by a single matrix, so the grain, the split and the blade cannot drift
out of register with each other. The extrusion is a pure screen-vertical sweep of
that frame, so the solid cannot drift out of register either.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import os
import pathlib

# round-4 test: does the shaving curl survive simplification at small sizes?
SHAVING = os.environ.get("SHAVING", "0") == "1"

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- frame
ANGLE = math.radians(33.0)                    # rising diagonal
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)    # along the cutting edge, up-and-right
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)   # away from the cut, into the rough side

BLADE_LEN = 640.0
BLADE_THICK = 152.0                           # depth of the top face
RISE = 88.0                                   # extrusion height: screen-vertical
EDGE_MID = (543.0, 604.0)                     # midpoint of the cutting edge, on the canvas
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2         # local origin: cutting edge, leading end

MATRIX = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},{AX:.3f},{AY:.3f})"

# a screen-vertical rise of RISE, expressed in the local frame
RISE_LY = RISE * math.cos(ANGLE)


def to_canvas(lx, ly):
    return (AX + UX * lx + NX * ly, AY + UY * lx + NY * ly)


def to_local(px, py):
    dx, dy = px - AX, py - AY
    return (UX * dx + UY * dy, NX * dx + NY * dy)


# The boundary is local y = 0, extended to the canvas edges.
def boundary_at_x(x):
    return AY - NX * (x - AX) / NY


B_LEFT = boundary_at_x(0)
B_RIGHT = boundary_at_x(W)

# how far the canvas reaches in the local frame, so texture can cover it exactly
_c = [to_local(x, y) for x in (0, W) for y in (0, W)]
LX_MIN, LX_MAX = min(p[0] for p in _c), max(p[0] for p in _c)
LY_MIN, LY_MAX = min(p[1] for p in _c), max(p[1] for p in _c)

# deterministic jitter, so a rebuild is byte-identical
_seed = 20260807


def rnd():
    global _seed
    _seed = (_seed * 1103515245 + 12345) % (1 << 31)
    return _seed / (1 << 31)


# ---------------------------------------------------------------- outline
def _quad(p0, p1, p2, n=8):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def _cubic(p0, p1, p2, p3, n=20):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def blade_outline():
    """Rounded plane iron in local space, flattened to a polyline so the extrusion
    can be derived from it exactly. Cutting edge (y=0) dead straight and honed;
    back edge worn, with a shallow sag and unequal corner radii."""
    L, T = BLADE_LEN, BLADE_THICK
    r_cl, r_ct = 12.0, 9.0        # corners on the honed edge: crisp, it is sharpened
    r_bl, r_bt = 46.0, 36.0       # corners on the worn back
    pts = [(r_cl, 0.0), (L - r_ct, 0.0)]
    pts += _quad((L - r_ct, 0), (L, 0), (L, r_ct))
    pts.append((L, T - r_bt))
    pts += _quad((L, T - r_bt), (L, T), (L - r_bt, T))
    pts += _cubic((L - r_bt, T), (L * 0.66, T - 8.5), (L * 0.34, T - 8.5), (r_bl, T))
    pts += _quad((r_bl, T), (0, T), (0, T - r_bl))
    pts.append((0.0, r_cl))
    pts += _quad((0, r_cl), (0, 0), (r_cl, 0))
    return pts


def poly(pts):
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def open_poly(pts):
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + ""


OUTLINE_L = blade_outline()
# the top face, lifted off the ground by the extrusion height
TOP = [(cx, cy - RISE) for cx, cy in (to_canvas(x, y) for x, y in OUTLINE_L)]
# the footprint: where the solid actually meets the ground
FOOT = [to_canvas(x, y) for x, y in OUTLINE_L]

N = len(TOP)
i_min = min(range(N), key=lambda i: TOP[i][0])
i_max = max(range(N), key=lambda i: TOP[i][0])


def _walk(a, b):
    out, i = [TOP[a]], a
    while i != b:
        i = (i + 1) % N
        out.append(TOP[i])
    return out


_fwd = _walk(i_min, i_max)          # i_min -> i_max one way round
_bwd = _walk(i_max, i_min)          # i_max -> i_min the other way
if sum(p[1] for p in _fwd) / len(_fwd) > sum(p[1] for p in _bwd) / len(_bwd):
    CHAIN_LOWER, CHAIN_UPPER = _fwd, _bwd            # lower runs i_min -> i_max
else:
    CHAIN_LOWER, CHAIN_UPPER = _bwd[::-1], _fwd[::-1]

# the front face: the lower silhouette chain swept straight down to the ground
FRONT_FACE = CHAIN_LOWER + [(x, y + RISE) for x, y in reversed(CHAIN_LOWER)]
# the whole solid, for the cast shadow
SILHOUETTE = CHAIN_UPPER[::-1] + [(x, y + RISE) for x, y in reversed(CHAIN_LOWER)]
# the ground contact line, which is also the before/after boundary
CONTACT = [(x, y + RISE) for x, y in CHAIN_LOWER]


# ---------------------------------------------------------------- ground texture
def grain():
    """One family of grain lines running along the travel direction. The SAME line
    crosses the boundary: torn and broken on the un-planed side, continuous and fine
    on the trued side. That continuity is what makes the split read as one surface in
    two states rather than as two different materials. Drawn right across the tile and
    clipped per side, so the block sits ON the grain rather than beside it."""
    rough, true = [], []
    x = LX_MIN - 40
    while x < LX_MAX + 40:
        # --- trued side (local y < 0): long, even, fine. A sheen, not a stripe - but
        #     present, because a trued plane still carries the mark of the pass.
        if rnd() < 0.72:
            op = 0.030 + rnd() * 0.042
            true.append(
                f'<path d="M {x:.1f} -8 L {x:.1f} {LY_MIN - 20:.0f}" stroke="#8A7C64" '
                f'stroke-opacity="{op:.3f}" stroke-width="{1.1 + rnd() * 0.8:.2f}"/>'
            )
        if rnd() < 0.34:
            op = 0.020 + rnd() * 0.026
            true.append(
                f'<path d="M {x + 6:.1f} -8 L {x + 6:.1f} {LY_MIN - 20:.0f}" stroke="#FFFFFF" '
                f'stroke-opacity="{op:.3f}" stroke-width="{1.4 + rnd() * 1.2:.2f}"/>'
            )
        # --- un-planed side (local y > 0): short broken tooth marks. Some lines tear
        #     badly, some hardly at all, which is what stops it reading as ruled rain.
        tear = 0.34 + rnd() * 0.92
        y = 8.0
        while y < LY_MAX + 20:
            seg = 6 + rnd() * 23 * tear
            gap = 7 + rnd() * 20
            op = (0.07 + rnd() * 0.13) * tear
            wid = 1.2 + rnd() * 2.1
            rough.append(
                f'<path d="M {x + (rnd() - 0.5) * 4:.1f} {y:.1f} '
                f'L {x + (rnd() - 0.5) * 4:.1f} {y + seg:.1f}" stroke="#6A5F4C" '
                f'stroke-opacity="{op:.3f}" stroke-width="{wid:.2f}"/>'
            )
            y += seg + gap
        x += 14.0 + rnd() * 8.0
    return "\n      ".join(rough), "\n      ".join(true)


def mottle():
    """Warm cloudy unevenness, so each plane reads as a worked material rather than a
    printed field. Big and soft enough that it dissolves rather than speckles small."""
    rough, true = [], []
    for _ in range(30):
        lx = LX_MIN - 160 + rnd() * (LX_MAX - LX_MIN + 320)
        ly = -60 + rnd() * (LY_MAX + 120)
        rx, ry = 90 + rnd() * 230, 70 + rnd() * 190
        op = 0.028 + rnd() * 0.055
        col = "#8C7A5E" if rnd() < 0.62 else "#FFF6E4"
        rough.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                     f'fill="{col}" fill-opacity="{op:.3f}"/>')
    for _ in range(22):
        lx = LX_MIN - 160 + rnd() * (LX_MAX - LX_MIN + 320)
        ly = LY_MIN - 60 + rnd() * (60 - LY_MIN)
        rx, ry = 130 + rnd() * 280, 90 + rnd() * 200
        op = 0.022 + rnd() * 0.042
        col = "#9C8A6C" if rnd() < 0.5 else "#FFFFFF"
        true.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                    f'fill="{col}" fill-opacity="{op:.3f}"/>')
    return "\n      ".join(rough), "\n      ".join(true)


def stone():
    """Faint blotching on the iron's own top face, so the graphite reads as a worn
    ground surface rather than as a fill. Local-frame coords, clipped to the face."""
    out = []
    for _ in range(34):
        lx = -20 + rnd() * (BLADE_LEN + 40)
        ly = rnd() * BLADE_THICK
        rx, ry = 28 + rnd() * 96, 16 + rnd() * 46
        op = 0.038 + rnd() * 0.070
        col = "#8E97A4" if rnd() < 0.55 else "#14171B"
        out.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                   f'fill="{col}" fill-opacity="{op:.3f}"/>')
    return "\n        ".join(out)


def shaving_curl():
    """The physical evidence of what came away: a rolled shaving standing behind the
    iron. Authored as a tapering spiral ribbon rather than an annulus, because an
    annulus is what read as a coat hanger the first two times it was tried."""
    cx, cy, r0, w, turns, phase = 214.0, 252.0, 104.0, 44.0, 1.55, math.radians(-58)
    k = (r0 - 42.0) / (turns * 2 * math.pi)
    outer, inner = [], []
    n = 132
    for i in range(n + 1):
        th = turns * 2 * math.pi * i / n
        r = r0 - k * th
        ww = w * (1.0 - 0.34 * (th / (turns * 2 * math.pi)))
        a = th + phase
        outer.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        inner.append((cx + (r - ww) * math.cos(a), cy + (r - ww) * math.sin(a)))
    return poly(outer + inner[::-1]), open_poly(outer)


SHAVING_BODY, SHAVING_RIM = shaving_curl()

ROUGH_GRAIN, TRUE_GRAIN = grain()
ROUGH_MOTTLE, TRUE_MOTTLE = mottle()
STONE = stone()

# ---------------------------------------------------------------- document
SHAVING_GRAD = (f"""  <linearGradient id="shavingGel" x1="120" y1="360" x2="330" y2="150" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.62"/>
    <stop offset="0.55" stop-color="#F4EEE1" stop-opacity="0.34"/>
    <stop offset="1" stop-color="#E7DFCD" stop-opacity="0.50"/>
  </linearGradient>

""" if SHAVING else "")

SHAVING_BLOCK = (f"""<!-- the shaving: what the pass has already taken off -->
    <g transform="translate(0,{-RISE * 0.86:.0f})">
      <path d="{SHAVING_BODY}" transform="{MATRIX}" fill="url(#shavingGel)"/>
      <path d="{SHAVING_RIM}" transform="{MATRIX}" fill="none" stroke="#FFFFFF"
            stroke-opacity="0.72" stroke-width="3.2"/>
    </g>""" if SHAVING else "")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}" role="img" aria-label="improve-skill">
<title>improve-skill</title>
<!--
  Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object.
  The tile is the workpiece. A worn plane iron lies mid-pass on a rising diagonal; the
  surface behind it is brighter and truer than the surface ahead, and the single
  vermilion hone line IS the boundary between the two states - and IS the line where
  the solid meets the ground.
  Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
  Full-bleed 1024 artwork; the squircle is a CLIP for preview only. No baked corners,
  no baked drop shadow. Generated by build_icon.py - edit there, not here.
-->
<defs>
  <clipPath id="tileMask"><path d="{SQUIRCLE}"/></clipPath>
  <clipPath id="topFaceClip"><path d="{poly(TOP)}"/></clipPath>
  <!-- everything the pass has already trued -->
  <clipPath id="truedSide">
    <path d="M0 {B_LEFT:.1f} L{W} {B_RIGHT:.1f} L{W} {W} L0 {W} Z"/>
  </clipPath>
  <!-- everything still to come -->
  <clipPath id="roughSide">
    <path d="M0 0 L{W} 0 L{W} {B_RIGHT:.1f} L0 {B_LEFT:.1f} Z"/>
  </clipPath>

  <!-- the un-planed side: cooler, greyer, losing light as it nears the cut -->
  <linearGradient id="roughField" x1="86" y1="30" x2="540" y2="700" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#D8D2C4"/>
    <stop offset="0.50" stop-color="#C5BDAC"/>
    <stop offset="1" stop-color="#ABA391"/>
  </linearGradient>

  <!-- the trued side: brighter and warmer, brightest right at the fresh cut -->
  <linearGradient id="truedField" x1="300" y1="440" x2="960" y2="1030" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFFDF6"/>
    <stop offset="0.40" stop-color="#FCF7EC"/>
    <stop offset="1" stop-color="#F1EAD9"/>
  </linearGradient>

  <!-- top face of the iron: facing the soft top-left light. Warm-leaning graphite,
       not blue steel - the raster take's stone read is what this is chasing. -->
  <linearGradient id="topFace" x1="0" y1="0" x2="0" y2="{BLADE_THICK}" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#2E3238"/>
    <stop offset="0.34" stop-color="#41464C"/>
    <stop offset="0.78" stop-color="#525860"/>
    <stop offset="1" stop-color="#5D636B"/>
  </linearGradient>

  <!-- a soft sheen where the top-left light lands hardest on the top face -->
  <radialGradient id="topSheen" cx="0.30" cy="0.72" r="0.62">
    <stop offset="0" stop-color="#CBD5E2" stop-opacity="0.25"/>
    <stop offset="1" stop-color="#CBD5E2" stop-opacity="0"/>
  </radialGradient>

  <!-- front face: in shadow at the top, lit from below by the hone itself -->
  <linearGradient id="frontFace" x1="0" y1="{RISE_LY:.2f}" x2="0" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#181B20"/>
    <stop offset="0.42" stop-color="#1E2026"/>
    <stop offset="0.74" stop-color="#3A2521"/>
    <stop offset="0.92" stop-color="#8A3418"/>
    <stop offset="1" stop-color="#C2431C"/>
  </linearGradient>

  <!-- the hone glow spilling onto the surface it has just trued. Every edge of this
       shape is blurred away, because light has no edges; only the boundary clip
       stops it, which is correct - the spill cannot reach the un-planed side. -->
  <linearGradient id="honeWide" x1="0" y1="0" x2="0" y2="-118" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#EF5A2A" stop-opacity="0.20"/>
    <stop offset="0.30" stop-color="#F4813F" stop-opacity="0.075"/>
    <stop offset="0.66" stop-color="#FFC79A" stop-opacity="0.022"/>
    <stop offset="1" stop-color="#FFE2C8" stop-opacity="0"/>
  </linearGradient>

  <linearGradient id="honeCore" x1="0" y1="0" x2="{BLADE_LEN}" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#C4341A"/>
    <stop offset="0.30" stop-color="#FA6231"/>
    <stop offset="0.62" stop-color="#FF9159"/>
    <stop offset="1" stop-color="#D8451F"/>
  </linearGradient>

{SHAVING_GRAD}  <radialGradient id="vignette" cx="0.46" cy="0.40" r="0.86">
    <stop offset="0.56" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#3A3226" stop-opacity="0.16"/>
  </radialGradient>

  <filter id="castShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="26"/>
  </filter>
  <filter id="contactShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="honeGlow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="13"/>
  </filter>
  <filter id="stoneBlur" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="15"/>
  </filter>
  <filter id="mottleBlur" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="46"/>
  </filter>
  <filter id="bloomBlur" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="30"/>
  </filter>
  <filter id="honeGlowTight" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="4"/>
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

  <g id="mid">
    <!-- warm cloudy unevenness in each plane: worked material, not printed field -->
    <g clip-path="url(#roughSide)"><g filter="url(#mottleBlur)"><g transform="{MATRIX}">
      {ROUGH_MOTTLE}
    </g></g></g>
    <g clip-path="url(#truedSide)"><g filter="url(#mottleBlur)"><g transform="{MATRIX}">
      {TRUE_MOTTLE}
    </g></g></g>

    <!-- one grain family crossing the boundary: torn above it, true below it -->
    <g fill="none" stroke-linecap="round">
      <g clip-path="url(#truedSide)"><g transform="{MATRIX}">
        {TRUE_GRAIN}
      </g></g>
      <g clip-path="url(#roughSide)"><g transform="{MATRIX}">
        {ROUGH_GRAIN}
      </g></g>
    </g>

    <!-- the solid's own shadow, from the one soft top-left light: a deep soft cast
         plus a tight occlusion where it actually touches down -->
    <g filter="url(#castShadow)">
      <path d="{poly([(x + 30, y + 34) for x, y in SILHOUETTE])}" fill="#4B4133" fill-opacity="0.35"/>
    </g>
    <g filter="url(#contactShadow)">
      <path d="{poly([(x + 9, y + 12) for x, y in SILHOUETTE])}" fill="#3C3327" fill-opacity="0.42"/>
    </g>

    <!-- the hone's light on the surface it just cut. Clipped to the trued side and drawn
         under the blade, so it can only ever read as spill from the edge. The wide
         bloom is a tapered shape pushed through a heavy blur, so it has no edge of
         its own anywhere - it decays into the trued plane instead of ending. -->
    <g clip-path="url(#truedSide)">
      <g filter="url(#bloomBlur)">
        <path d="M -30 6 L {BLADE_LEN + 26:.0f} 6 L {BLADE_LEN - 74:.0f} -118 L 74 -118 Z"
              transform="{MATRIX}" fill="url(#honeWide)"/>
      </g>
      <path d="M 30 0 L {BLADE_LEN - 26:.0f} 0" transform="{MATRIX}" stroke="#FF7A3C"
            stroke-opacity="0.52" stroke-width="26" filter="url(#honeGlow)"/>
    </g>
  </g>

  <g id="fg">
    {SHAVING_BLOCK}
    <!-- the plane iron as a real solid: a front face dropping to the ground, and a top
         face lifted clear of it. The silhouette is one chunky block at every size. -->
    <path d="{poly(FRONT_FACE)}" fill="url(#frontFace)"/>
    <path d="{poly(TOP)}" fill="url(#topFace)"/>
    <g clip-path="url(#topFaceClip)"><g filter="url(#stoneBlur)"><g transform="translate(0,{-RISE})"><g transform="{MATRIX}">
        {STONE}
    </g></g></g></g>
    <path d="{poly(TOP)}" fill="url(#topSheen)"/>
    <!-- wear on the back: two faint grind striations, on the top face -->
    <g transform="translate(0,{-RISE})" fill="none">
      <g transform="{MATRIX}">
        <path d="M 78 122 L {BLADE_LEN - 98:.0f} 122" stroke="#8A93A3" stroke-opacity="0.16" stroke-width="3"/>
        <path d="M 128 100 L {BLADE_LEN - 152:.0f} 100" stroke="#8A93A3" stroke-opacity="0.09" stroke-width="2"/>
      </g>
    </g>
  </g>

  <g id="highlight" fill="none">
    <!-- chamfer between top face and front face: what makes the solid read as a solid -->
    <path d="{open_poly(CHAIN_LOWER)}" stroke="#848E9C" stroke-opacity="0.56" stroke-width="4.4"
          stroke-linecap="round"/>
    <!-- rim light along the worn back, from the same top-left source -->
    <g transform="translate(0,{-RISE})">
      <path d="M 46 {BLADE_THICK - 2:.0f} C {BLADE_LEN * 0.34:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN * 0.66:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN - 36:.0f} {BLADE_THICK - 2:.0f}"
            transform="{MATRIX}" stroke="#B6C0CE" stroke-opacity="0.64" stroke-width="5"
            stroke-linecap="round"/>
    </g>
    <!-- the vermilion hone line: the cutting edge, the before/after boundary, and the
         line where the solid meets the ground. One shape, four jobs. -->
    <path d="M 10 0 L {BLADE_LEN - 8:.0f} 0" transform="{MATRIX}" stroke="#FF8A50"
          stroke-opacity="0.75" stroke-width="16" filter="url(#honeGlowTight)"/>
    <path d="M 10 0 L {BLADE_LEN - 8:.0f} 0" transform="{MATRIX}" stroke="url(#honeCore)"
          stroke-width="12" stroke-linecap="butt"/>
    <path d="M 56 -0.6 L {BLADE_LEN - 58:.0f} -0.6" transform="{MATRIX}" stroke="#FFE3CD"
          stroke-opacity="0.96" stroke-width="4.2" stroke-linecap="round"/>
    <!-- cushion rim light around the tile perimeter -->
    <path d="{SQUIRCLE}" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="3"/>
  </g>

</g>
</svg>
"""

(ASSETS / "icon.svg").write_text(svg)
print(f"wrote icon.svg  boundary (0,{B_LEFT:.0f}) -> ({W},{B_RIGHT:.0f})")
xs = [p[0] for p in SILHOUETTE]
ys = [p[1] for p in SILHOUETTE]
print(f"solid bbox x {min(xs):.0f}-{max(xs):.0f} ({max(xs)-min(xs):.0f}px = {(max(xs)-min(xs))/W*100:.1f}% of tile)")
print(f"          y {min(ys):.0f}-{max(ys):.0f} ({max(ys)-min(ys):.0f}px)"
      f"   focal centre ({(min(xs)+max(xs))/2:.0f},{(min(ys)+max(ys))/2:.0f})")
print(f"safe-zone margins  L{min(xs):.0f} R{W-max(xs):.0f} T{min(ys):.0f} B{W-max(ys):.0f}")
