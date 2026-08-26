#!/usr/bin/env python3
"""build_icon.py — the layered SVG master for the `eli5` skill icon.

Concept: "The cut face". A soft, volumetric solid with a clean quarter-section
removed. The section plane slicing a soft volume is the signature move: smooth
shell outside, crisp ordered mechanism inside. The one warm accent lands on the
exposed cut face — the interior surface the section reveals — because that cut
is the skill's whole move.

Two solids are authored from the same material constants so the audit sheet can
judge the host form rather than the palette:

    SOLID = "drum"    stepped quarter-section through a soft cylinder: a
                      horizontal shelf showing concentric layers and a core,
                      plus two vertical section walls showing the same layers
                      in strata. Ships as icon.svg.
    SOLID = "sphere"  quarter-wedge through a soft ball: two flat half-disc
                      faces meeting at the axis, layers as concentric shells.

Geometry and material are named constants, so a later fidelity round is a
parameter edit rather than path surgery.

    python3 build_icon.py            # writes icon.svg + icon-engineA2-sphere.svg
    python3 build_icon.py --export   # ...and icon.png / icon-256.png / icon-128.png
"""

from __future__ import annotations

import math
import pathlib
import subprocess
import sys

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- palette
# Sampled, not invented. Ground and accent are read off the marketplace set
# (icon-256.png of flagship / reckon / clarify / launch-craft: ground top
# ~(249,246,240) falling to ~(229,222,205) at the base, accent clustering
# #D66B32-#E47828 around Fledgeling's #C4622D). The porcelain ramp and the
# top-light position are read off references/corpus/apple-2026/ in the same
# register (apple-23 Safari, apple-26 Reminders, apple-28 Photos, apple-31
# News: tile 255 at the top falling to ~235 at the base, brightest point at
# ~0.36 of the width and 0.05 of the height, shaded faces warm-dark not blue).
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFDF7", "#F6F1E6", "#E2D9C5"
VIGNETTE = "#9C8D74"

# The shell is a warm-neutral graphite: the darkest pixel in a shaded face on
# the corpus captures is warm, so the shell's shadow end carries a little red
# rather than going blue.
SHELL_TOP_HI, SHELL_TOP_LO = "#8C9299", "#30343A"
SHELL_HI, SHELL_MID, SHELL_LO = "#6C7279", "#353A40", "#1D2024"
SHELL_BOUNCE = "#3E444D"
RIM = "#CBD3DB"

# One warm accent, reserved for the cut face and nothing else.
EMBER_CORE, EMBER_HOT = "#FFD9AC", "#F58F4A"
EMBER, EMBER_SHADE, EMBER_DEEP = "#C4622D", "#9E4A20", "#79331580"
EMBER_LINE = "#7A3315"
SHADOW = "#6E5C44"

# ---------------------------------------------------------------- geometry
CX = 512

# drum
R = 318.0            # outer radius, screen x
K = 0.42             # ellipse foreshortening (view elevation)
RK = R * K
TOP_Y = 384.0        # centre of the top face ellipse
BODY_H = 236.0       # side-wall height
CUT_D = 156.0        # how far the section drops before the shelf
T1, T2 = 26.0, 116.0  # wedge azimuths; the 90 degrees between them is removed
SPH_T1, SPH_T2 = 58.0, 126.0  # the sphere take cuts a narrower wedge, kept off-centre
SHELF_Y = TOP_Y + CUT_D
BOT_Y = TOP_Y + BODY_H

# layer radii, shared by the shelf rings and the wall strata so the mechanism
# reads as one solid rather than two decorated faces
TAPER = 0.955        # bottom radius / top radius: a soft draft angle
LAYERS = (0.16, 0.40, 0.64, 0.86)
TICKS = 10           # gear-like radial ticks between the two outer layers
SUNBURST = 22        # fine ticks radiating from the core, lit by it

# sphere
SPH_CX, SPH_CY, SPH_R = 512.0, 486.0, 300.0

CONTACT_Y = 748.0


def pol(t_deg: float, cy: float, rx: float = R, ry: float = RK) -> tuple[float, float]:
    """A point on the horizontal ellipse at azimuth t, centred (CX, cy)."""
    t = math.radians(t_deg)
    return CX + rx * math.cos(t), cy + ry * math.sin(t)


def f(v: float) -> str:
    return f"{v:.1f}"


def p(pt: tuple[float, float]) -> str:
    return f"{f(pt[0])} {f(pt[1])}"


# ---------------------------------------------------------------- drum take

def drum_defs() -> str:
    return f"""
    <linearGradient id="wall" x1="{f(CX - R)}" y1="0" x2="{f(CX + R)}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{SHELL_HI}"/>
      <stop offset="0.30" stop-color="{SHELL_MID}"/>
      <stop offset="0.74" stop-color="{SHELL_LO}"/>
      <stop offset="1" stop-color="{SHELL_BOUNCE}"/>
    </linearGradient>
    <linearGradient id="wallShade" x1="0" y1="{f(TOP_Y)}" x2="0" y2="{f(BOT_Y + RK)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.07"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.30"/>
    </linearGradient>
    <radialGradient id="topFace" cx="{f(CX - 0.42 * R)}" cy="{f(TOP_Y - 0.62 * RK)}" r="{f(1.55 * R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{SHELL_TOP_HI}"/>
      <stop offset="0.55" stop-color="#474D56"/>
      <stop offset="1" stop-color="{SHELL_TOP_LO}"/>
    </radialGradient>
    <radialGradient id="shelf" cx="{f(CX)}" cy="{f(SHELF_Y)}" r="{f(R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_HOT}"/>
      <stop offset="0.30" stop-color="#DB7538"/>
      <stop offset="0.68" stop-color="{EMBER}"/>
      <stop offset="1" stop-color="{EMBER_SHADE}"/>
    </radialGradient>
    <linearGradient id="faceLit" x1="{f(CX)}" y1="{f(TOP_Y)}" x2="{p(pol(T1, TOP_Y))}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_HOT}"/>
      <stop offset="0.5" stop-color="#DB7538"/>
      <stop offset="1" stop-color="{EMBER}"/>
    </linearGradient>
    <linearGradient id="faceShade" x1="{f(CX)}" y1="{f(TOP_Y)}" x2="{p(pol(T2, TOP_Y))}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B0562A"/>
      <stop offset="0.55" stop-color="#8C3F1B"/>
      <stop offset="1" stop-color="#6F2E13"/>
    </linearGradient>
    <linearGradient id="wallLift" x1="0" y1="{f(TOP_Y)}" x2="0" y2="{f(SHELF_Y + RK)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE0B8" stop-opacity="0.26"/>
      <stop offset="0.62" stop-color="#FFE0B8" stop-opacity="0"/>
      <stop offset="1" stop-color="#4A1D0A" stop-opacity="0.26"/>
    </linearGradient>
    <linearGradient id="notchAO" x1="0" y1="{f(TOP_Y)}" x2="0" y2="{f(SHELF_Y + 40)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3A1608" stop-opacity="0.34"/>
      <stop offset="0.45" stop-color="#3A1608" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#3A1608" stop-opacity="0.32"/>
    </linearGradient>
    <radialGradient id="coreBloom" cx="{f(CX)}" cy="{f(SHELF_Y - 6)}" r="{f(0.62 * R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFC98A" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="#F58F4A" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#F58F4A" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="leftRim" x1="0" y1="{f(TOP_Y)}" x2="0" y2="{f(BOT_Y)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{RIM}" stop-opacity="0.75"/>
      <stop offset="1" stop-color="{RIM}" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="shelfCast" x1="{p(pol(T2, SHELF_Y))}" x2="{p(pol(T1 + 22, SHELF_Y))}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4A1D0A" stop-opacity="0.42"/>
      <stop offset="0.55" stop-color="#4A1D0A" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#4A1D0A" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fillet" x1="{f(CX - R)}" y1="{f(TOP_Y - RK)}" x2="{f(CX + R)}" y2="{f(TOP_Y + RK)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#99A1AA" stop-opacity="0.32"/>
      <stop offset="0.45" stop-color="#6E757E" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#171B20" stop-opacity="0.40"/>
    </linearGradient>
    <radialGradient id="coreFlare" cx="{f(CX)}" cy="{f(SHELF_Y)}" r="{f(0.19 * R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF6E4"/>
      <stop offset="0.35" stop-color="#FFD9AC"/>
      <stop offset="0.72" stop-color="#F9A45C" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#F58F4A" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="bodyClip"><path d="{drum_body()}"/></clipPath>
    <clipPath id="shelfClip"><path d="{shelf_sector()}"/></clipPath>
    <clipPath id="faceRClip"><path d="{face_quad(T1)}"/></clipPath>
    <clipPath id="faceLClip"><path d="{face_quad(T2)}"/></clipPath>
    <clipPath id="voidClip"><path d="{void_region()}"/></clipPath>"""


def drum_body() -> str:
    r2 = R * TAPER
    return (f"M {f(CX - R)} {f(TOP_Y)} A {f(R)} {f(RK)} 0 0 1 {f(CX + R)} {f(TOP_Y)} "
            f"L {f(CX + r2)} {f(BOT_Y)} A {f(r2)} {f(r2 * K)} 0 0 1 {f(CX - r2)} {f(BOT_Y)} Z")


def shelf_sector(frac: float = 1.0) -> str:
    a, b = pol(T1, SHELF_Y, R * frac, RK * frac), pol(T2, SHELF_Y, R * frac, RK * frac)
    return (f"M {f(CX)} {f(SHELF_Y)} L {p(a)} "
            f"A {f(R * frac)} {f(RK * frac)} 0 0 1 {p(b)} Z")


def face_quad(t: float, f_in: float = 0.0, f_out: float = 1.0) -> str:
    """The section wall at azimuth t, between two layer radii."""
    i_top, o_top = pol(t, TOP_Y, R * f_in, RK * f_in), pol(t, TOP_Y, R * f_out, RK * f_out)
    return (f"M {p(i_top)} L {p(o_top)} "
            f"L {f(o_top[0])} {f(o_top[1] + CUT_D)} L {f(i_top[0])} {f(i_top[1] + CUT_D)} Z")


def void_region() -> str:
    a_top, b_top = pol(T1, TOP_Y), pol(T2, TOP_Y)
    a_sh, b_sh = pol(T1, SHELF_Y), pol(T2, SHELF_Y)
    return (f"M {f(CX)} {f(TOP_Y)} L {p(a_top)} L {p(a_sh)} "
            f"A {f(R)} {f(RK)} 0 0 1 {p(b_sh)} L {p(b_top)} Z")


def drum_svg() -> str:
    a_top, b_top = pol(T1, TOP_Y), pol(T2, TOP_Y)
    a_sh, b_sh = pol(T1, SHELF_Y), pol(T2, SHELF_Y)

    # shelf: concentric layer rings, then gear-like radial ticks
    rings = []
    for i, fr in enumerate(LAYERS):
        s, e = pol(T1, SHELF_Y, R * fr, RK * fr), pol(T2, SHELF_Y, R * fr, RK * fr)
        rings.append(f'<path d="M {p(s)} A {f(R * fr)} {f(RK * fr)} 0 0 1 {p(e)}" fill="none" '
                     f'stroke="{EMBER_LINE}" stroke-opacity="0.42" stroke-width="5"/>')
        rings.append(f'<path d="M {f(s[0])} {f(s[1] - 4)} A {f(R * fr)} {f(RK * fr)} 0 0 1 {f(e[0])} {f(e[1] - 4)}" '
                     f'fill="none" stroke="#FFE0B8" stroke-opacity="0.30" stroke-width="2.5"/>')
    for i in range(9):
        fr = 0.26 + 0.075 * i
        s, e = pol(T1, SHELF_Y, R * fr, RK * fr), pol(T2, SHELF_Y, R * fr, RK * fr)
        rings.append(f'<path d="M {p(s)} A {f(R * fr)} {f(RK * fr)} 0 0 1 {p(e)}" fill="none" '
                     f'stroke="{EMBER_LINE}" stroke-opacity="0.18" stroke-width="2.5"/>')
    ticks = []
    for i in range(1, TICKS):
        t = T1 + (T2 - T1) * i / TICKS
        s, e = pol(t, SHELF_Y, R * LAYERS[2], RK * LAYERS[2]), pol(t, SHELF_Y, R * LAYERS[3], RK * LAYERS[3])
        ticks.append(f'<path d="M {p(s)} L {p(e)}" stroke="{EMBER_LINE}" stroke-opacity="0.18" stroke-width="4"/>')
    for i in range(1, SUNBURST):
        t = T1 + (T2 - T1) * i / SUNBURST
        s, e = pol(t, SHELF_Y, R * 0.21, RK * 0.21), pol(t, SHELF_Y, R * LAYERS[1], RK * LAYERS[1])
        ticks.append(f'<path d="M {p(s)} L {p(e)}" stroke="#FFE8C6" stroke-opacity="0.34" stroke-width="2.5"/>')

    # walls: the same layers seen in section, as strata parallel to the axis
    strata = []
    for t, grad, seam in ((T1, "faceLit", 0.22), (T2, "faceShade", 0.17)):
        strata.append(f'<path d="{face_quad(t)}" fill="url(#{grad})"/>')
        strata.append(f'<path d="{face_quad(t)}" fill="url(#wallLift)"/>')
        for j, fr in enumerate(LAYERS):
            edge_top = pol(t, TOP_Y, R * fr, RK * fr)
            strata.append(f'<path d="M {p(edge_top)} L {f(edge_top[0])} {f(edge_top[1] + CUT_D)}" '
                          f'stroke="{EMBER_LINE}" stroke-opacity="{seam}" stroke-width="3.4"/>')
        # a value step per stratum, so the layers read without a second hue
        for j, (lo, hi, op) in enumerate(((0.0, LAYERS[0], -0.34), (LAYERS[0], LAYERS[1], 0.10),
                                          (LAYERS[1], LAYERS[2], 0.0), (LAYERS[2], LAYERS[3], 0.09),
                                          (LAYERS[3], 1.0, 0.17))):
            if op == 0:
                continue
            col = "#FFD9AC" if op < 0 else "#5A2410"
            strata.append(f'<path d="{face_quad(t, lo, hi)}" fill="{col}" fill-opacity="{abs(op):.2f}"/>')

    return document(drum_defs(), f"""
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
    </g>

    <g id="mid">
      <g filter="url(#castShadow)">
        <ellipse cx="{f(CX + 14)}" cy="{f(CONTACT_Y)}" rx="{f(R * 0.90)}" ry="{f(RK * 0.40)}" fill="{SHADOW}" fill-opacity="0.42"/>
      </g>
      <ellipse cx="{f(CX + 6)}" cy="{f(CONTACT_Y - 12)}" rx="{f(R * 0.70)}" ry="{f(RK * 0.24)}" fill="{SHADOW}" fill-opacity="0.20" filter="url(#softBlur)"/>
      <g clip-path="url(#bodyClip)">
        <path d="{drum_body()}" fill="url(#wall)"/>
        <path d="{drum_body()}" fill="url(#wallShade)"/>
        <!-- occlusion in the fillet under the lid, then the lid over its inner half -->
        <path d="M {f(CX - R)} {f(TOP_Y + 8)} A {f(R)} {f(RK)} 0 0 0 {f(CX + R)} {f(TOP_Y + 8)}" fill="none"
              stroke="#000000" stroke-opacity="0.22" stroke-width="30"/>
        <ellipse cx="{f(CX)}" cy="{f(TOP_Y)}" rx="{f(R)}" ry="{f(RK)}" fill="url(#topFace)"/>
        <ellipse cx="{f(CX)}" cy="{f(TOP_Y)}" rx="{f(R)}" ry="{f(RK)}" fill="none"
                 stroke="url(#fillet)" stroke-width="26"/>
        <path d="M {f(CX - R)} {f(TOP_Y)} A {f(R)} {f(RK)} 0 0 0 {f(CX + R)} {f(TOP_Y)}" fill="none"
              stroke="{RIM}" stroke-opacity="0.42" stroke-width="4"/>
        <path d="M {p(pol(196, TOP_Y))} A {f(R)} {f(RK)} 0 0 1 {p(pol(268, TOP_Y))}" fill="none"
              stroke="#FFFFFF" stroke-opacity="0.38" stroke-width="6" stroke-linecap="round"/>
        <path d="M {f(CX - R)} {f(TOP_Y)} L {f(CX - R * TAPER)} {f(BOT_Y)}" stroke="url(#leftRim)" stroke-width="7"/>
        <path d="M {f(CX - R * TAPER)} {f(BOT_Y)} A {f(R * TAPER)} {f(R * TAPER * K)} 0 0 0 {f(CX + R * TAPER)} {f(BOT_Y)}" fill="none"
              stroke="#C7B191" stroke-opacity="0.26" stroke-width="7"/>
        <ellipse cx="{f(CX - 0.34 * R)}" cy="{f(TOP_Y - 0.30 * RK)}" rx="{f(0.44 * R)}" ry="{f(0.42 * RK)}"
                 fill="#FFFFFF" fill-opacity="0.15" filter="url(#softBlur)"/>
      </g>
    </g>

    <g id="fg">
      <g clip-path="url(#voidClip)">
        <path d="{shelf_sector()}" fill="url(#shelf)"/>
        <g clip-path="url(#shelfClip)">
          {''.join(ticks)}
          {''.join(rings)}
          <ellipse cx="{f(CX)}" cy="{f(SHELF_Y)}" rx="{f(R * 0.19)}" ry="{f(RK * 0.19)}" fill="url(#coreFlare)"/>
          <ellipse cx="{f(CX)}" cy="{f(SHELF_Y)}" rx="{f(R * 0.055)}" ry="{f(RK * 0.055)}" fill="#FFFDF4"/>
          <path d="{shelf_sector()}" fill="url(#shelfCast)"/>
        </g>
        {''.join(strata)}
        <path d="{void_region()}" fill="url(#notchAO)"/>
        <path d="{void_region()}" fill="url(#coreBloom)"/>
      </g>

      <!-- the section's own arrises: the machined edges that make the cut read clean -->
      <g fill="none" stroke="#FFF0DC" stroke-opacity="0.88" stroke-width="3.4" stroke-linecap="round">
        <path d="M {f(CX)} {f(TOP_Y)} L {p(a_top)}"/>
        <path d="M {f(CX)} {f(TOP_Y)} L {p(b_top)}"/>
      </g>
      <g fill="none" stroke="#FFD9AC" stroke-opacity="0.55" stroke-width="2.6">
        <path d="M {p(a_top)} L {p(a_sh)}"/>
        <path d="M {p(b_top)} L {p(b_sh)}"/>
        <path d="M {p(a_sh)} A {f(R)} {f(RK)} 0 0 1 {p(b_sh)}"/>
        <path d="M {f(CX)} {f(SHELF_Y)} L {p(a_sh)}" stroke-opacity="0.30"/>
        <path d="M {f(CX)} {f(SHELF_Y)} L {p(b_sh)}" stroke-opacity="0.24"/>
      </g>
      <path d="M {f(CX)} {f(TOP_Y)} L {f(CX)} {f(SHELF_Y)}" stroke="#5A2410" stroke-opacity="0.35" stroke-width="3"/>
    </g>

    <g id="highlight">
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="0.80" stroke-width="8"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#C7B9A0" stroke-opacity="0.35" stroke-width="2"/>
    </g>""")


# -------------------------------------------------------------- sphere take

def half_disc_open(theta_deg: float, frac: float, n: int = 22) -> str:
    """The curved arris only — where a flat face meets the sphere's surface."""
    return half_disc(theta_deg, frac, n=n)[:-2]


def half_disc(theta_deg: float, frac: float, cy_off: float = 0.0, n: int = 22) -> str:
    """Projection of a half-disc of radius frac*SPH_R lying in the vertical
    plane at azimuth theta: the flat face a quarter-cut exposes."""
    t = math.radians(theta_deg)
    ux, uy = math.cos(t), K * math.sin(t)
    pts = []
    for i in range(n + 1):
        phi = -math.pi / 2 + math.pi * i / n
        a, b = math.cos(phi), math.sin(phi)
        pts.append((SPH_CX + SPH_R * frac * a * ux,
                    SPH_CY + cy_off + SPH_R * frac * (a * uy - b)))
    return "M " + " L ".join(p(q) for q in pts) + " Z"


def sphere_svg() -> str:
    bands = []
    for t, grad in ((SPH_T1, "faceLit"), (SPH_T2, "faceShade")):
        bands.append(f'<path d="{half_disc(t, 1.0)}" fill="url(#{grad})"/>')
        for j, fr in enumerate(reversed(LAYERS)):
            tone = ("#5A2410", "#8C3F1B", "#D0713A", EMBER_CORE)[j]
            op = (0.20, 0.30, 0.55, 1.0)[j]
            if t == SPH_T2:                     # the shaded plane keeps its own ramp
                op = op * 0.78
            bands.append(f'<path d="{half_disc(t, fr)}" fill="{tone}" fill-opacity="{op:.2f}"/>')
            bands.append(f'<path d="{half_disc(t, fr)}" fill="none" stroke="{EMBER_LINE}" '
                         f'stroke-opacity="0.30" stroke-width="3"/>')
    return document(f"""
    <radialGradient id="ball" cx="{f(SPH_CX - 0.40 * SPH_R)}" cy="{f(SPH_CY - 0.46 * SPH_R)}" r="{f(1.42 * SPH_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{SHELL_TOP_HI}"/>
      <stop offset="0.42" stop-color="{SHELL_MID}"/>
      <stop offset="1" stop-color="#1B1F24"/>
    </radialGradient>
    <linearGradient id="faceLit" x1="{f(SPH_CX)}" y1="{f(SPH_CY - SPH_R)}" x2="{f(SPH_CX + SPH_R)}" y2="{f(SPH_CY + SPH_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_HOT}"/>
      <stop offset="1" stop-color="{EMBER}"/>
    </linearGradient>
    <linearGradient id="faceShade" x1="{f(SPH_CX)}" y1="{f(SPH_CY - SPH_R)}" x2="{f(SPH_CX - SPH_R)}" y2="{f(SPH_CY + SPH_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER}"/>
      <stop offset="1" stop-color="#8C3F1B"/>
    </linearGradient>
    <radialGradient id="coreBloom" cx="{f(SPH_CX)}" cy="{f(SPH_CY)}" r="{f(0.75 * SPH_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFC98A" stop-opacity="0.50"/>
      <stop offset="1" stop-color="#F58F4A" stop-opacity="0"/>
    </radialGradient>""", f"""
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
    </g>

    <g id="mid">
      <g filter="url(#castShadow)">
        <ellipse cx="{f(SPH_CX + 16)}" cy="{f(SPH_CY + SPH_R + 44)}" rx="{f(SPH_R * 0.94)}" ry="{f(SPH_R * 0.17)}" fill="{SHADOW}" fill-opacity="0.42"/>
      </g>
      <circle cx="{f(SPH_CX)}" cy="{f(SPH_CY)}" r="{f(SPH_R)}" fill="url(#ball)"/>
      <path d="M {f(SPH_CX - SPH_R)} {f(SPH_CY)} A {f(SPH_R)} {f(SPH_R)} 0 0 1 {f(SPH_CX)} {f(SPH_CY - SPH_R)}"
            fill="none" stroke="{RIM}" stroke-opacity="0.40" stroke-width="5"/>
      <path d="M {f(SPH_CX + SPH_R)} {f(SPH_CY)} A {f(SPH_R)} {f(SPH_R)} 0 0 1 {f(SPH_CX)} {f(SPH_CY + SPH_R)}"
            fill="none" stroke="#8B939C" stroke-opacity="0.35" stroke-width="6"/>
    </g>

    <g id="fg">
      {''.join(bands)}
      <path d="M {f(SPH_CX)} {f(SPH_CY - SPH_R)} L {f(SPH_CX)} {f(SPH_CY + SPH_R)}" stroke="#5A2410" stroke-opacity="0.32" stroke-width="3"/>
      <circle cx="{f(SPH_CX)}" cy="{f(SPH_CY)}" r="{f(0.60 * SPH_R)}" fill="url(#coreBloom)"/>
      <g fill="none" stroke="#FFF0DC" stroke-opacity="0.85" stroke-width="3.4">
        <path d="{half_disc_open(SPH_T1, 1.0)}"/>
        <path d="{half_disc_open(SPH_T2, 1.0)}"/>
      </g>
    </g>

    <g id="highlight">
      <ellipse cx="{f(SPH_CX - 0.40 * SPH_R)}" cy="{f(SPH_CY - 0.52 * SPH_R)}" rx="{f(0.30 * SPH_R)}" ry="{f(0.20 * SPH_R)}"
               fill="#FFFFFF" fill-opacity="0.16" filter="url(#softBlur)" transform="rotate(-28 {f(SPH_CX - 0.40 * SPH_R)} {f(SPH_CY - 0.52 * SPH_R)})"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="0.80" stroke-width="8"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#C7B9A0" stroke-opacity="0.35" stroke-width="2"/>
    </g>""")


# ---------------------------------------------------------------- document

def document(defs: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>
    <radialGradient id="ground" cx="368" cy="266" r="980" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.52" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="512" cy="512" r="740" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="0.72" stop-color="{VIGNETTE}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.17"/>
    </radialGradient>
    <filter id="castShadow" x="-30%" y="-60%" width="160%" height="260%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="softBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>{defs}
  </defs>
  <g clip-path="url(#tile)">{body}
  </g>
</svg>
"""


# ---------------------------------------------------------------- exports

def export(master: pathlib.Path):
    for size, name in ((1024, "icon.png"), (256, "icon-256.png"), (128, "icon-128.png")):
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                        str(master), "-o", str(ASSETS / name)], check=True)
        print(f"  exported {name}")


def main():
    (ASSETS / "icon.svg").write_text(drum_svg())
    print("  wrote icon.svg (drum, stepped quarter-section — the master)")
    (ASSETS / "icon-engineA2-sphere.svg").write_text(sphere_svg())
    print("  wrote icon-engineA2-sphere.svg (sphere, quarter wedge)")
    if "--export" in sys.argv:
        export(ASSETS / "icon.svg")


if __name__ == "__main__":
    main()
