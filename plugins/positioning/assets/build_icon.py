#!/usr/bin/env python3
"""build_icon.py — the layered SVG master for the `positioning` skill icon.

Concept: "the cocked hat". A navigator takes three bearings on three different
landmarks and plots them. No bearing is perfect, so the three lines do not meet
at a point — they enclose a small triangle, and that triangle is where the
vessel is. Navigators call it the cocked hat.

The glyph is the intersection, never a marker. Nothing here is a pin, a dot or
a reticle: three translucent bearing battens cross the chart at different
angles and different lengths, and the one warm accent is the shard of ember
light left in the pocket the three of them fail to close. Delete a line and the
fix stops existing, which is the point the skill makes about evidence.

Two takes are authored from one geometry so the sheet judges the material
rather than the layout:

    TAKE = "gel"    graphite gel rods lying on a porcelain chart, translucent
                    enough that each crossing multiplies darker, with the fix
                    glowing up through the pocket between them. Ships as icon.svg.
    TAKE = "chart"  the paper-chart register: inked bearing lines ruled thin on
                    the porcelain, and the cocked hat as a solid ember prism with
                    real thickness sitting on top of them.

Geometry and material are named constants, so a fidelity round is a parameter
edit rather than path surgery.

    python3 build_icon.py            # writes icon.svg + icon-engineA2-chart.svg
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
# Sampled, not invented.
#
# Ground: read off the marketplace set at icon-256 (flagship, reckon, clarify,
# launch-craft, eli5) — top band (250-253, 248-251, 243-245) falling to
# (227-234, 218-226, 198-211) at the base. The family's porcelain is warm where
# Apple's is neutral; the family rule wins, the corpus sets the ramp's shape.
#
# Light: read off references/corpus/apple-2026/ in the porcelain register
# (apple-23 Safari, apple-26 Reminders, apple-28 Photos, apple-05). The tile's
# brightest pixel sits at x=0.35-0.38, y=0.01-0.08 in all four, and the tile
# falls 255 -> 236 top to bottom. So the key light is high and left of centre,
# and GROUND_KEY is placed there rather than at the tile's middle.
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFDF7", "#F6F1E6", "#E2D9C5"
GROUND_KEY = (372.0, 168.0)   # centre of the ground ramp = the key light
VIGNETTE = "#9C8D74"

# The chart the bearings are plotted on. Sanctioned garnish (icon-directions
# grammar #8: ultra-low-contrast patterned grounds) — a graticule, not an idea.
GRATICULE = "#8A7458"
GRAT_OP, GRAT_MERIDIAN_OP = 0.050, 0.085
GRAT_STEP = 118.0

# The battens are a cool graphite: the darkest pixel inside a shaded face on the
# four porcelain captures is (25-31, 28-35, 31-39) — cool, not warm — so the
# rods go blue-grey at their shadow end and the ground keeps the warmth.
BAT_LIT, BAT_UPPER, BAT_CORE, BAT_DEEP, BAT_BOUNCE = (
    "#828B96", "#3C424B", "#252A31", "#171A1F", "#414954")
BAT_LIT_OP, BAT_UPPER_OP, BAT_CORE_OP, BAT_DEEP_OP, BAT_BOUNCE_OP = (
    0.58, 0.76, 0.82, 0.84, 0.70)
RIM = "#D3DAE2"
RIM_OP = 0.62
SHADOW = "#6E5C44"            # the ground's own hue darkened, never blue

# One warm accent, spent on the fix and nothing else.
EMBER_CORE, EMBER_HOT = "#FFE6C4", "#F58F4A"
EMBER, EMBER_SHADE, EMBER_DEEP = "#C4622D", "#9E4A20", "#7A3315"
ARRIS = "#FFF0DC"

# ---------------------------------------------------------------- geometry
# The fix: where the vessel actually is. Off the optical centre and up-left, so
# the composition runs down and to the right instead of sitting on the axis.
FIX = (486.0, 470.0)

# Three bearings taken on three landmarks in different directions. Screen
# degrees, y down. The angular gaps are 64 / 45 / 71 — deliberately uneven, so
# the set reads as three separate observations rather than a three-spoke
# asterisk.
BEARINGS = (4.0, 68.0, -41.0)

# ...and the error in each. No bearing is perfect: each line misses the true fix
# by this many pixels, on the side the sign gives. These three numbers ARE the
# cocked hat — set them all to zero and the triangle collapses to a point.
ERRORS = (-46.0, 68.0, 52.0)

# Batten widths differ, because a bearing on a near landmark is a heavier line
# than one on a far one.
WIDTHS = (56.0, 48.0, 44.0)

# How far each batten runs from the foot of the fix, before and after it. A
# bearing line comes from a landmark off the chart, so most ends bleed through
# the mask (device #18); the ends that stop inside the tile stop with a rounded
# cap, and no two lines stop at the same distance.
EXTENTS = ((-780.0, 780.0), (-780.0, 392.0), (-486.0, 780.0))

# Draw order: the long baseline lies underneath, the steep bearing on top.
STACK = (0, 2, 1)

SHADOW_OFF = (17.0, 23.0)     # the rods sit a little above the chart
SHADOW_OP = 0.30
LIGHT = (-0.55, -0.84)        # unit-ish direction the key light comes from

BLOOM_R = 258.0               # how far the fix's light travels along the lines
GROUND_BLOOM_R = 330.0        # and how far it spills onto the chart


def f(v: float) -> str:
    return f"{v:.1f}"


def p(pt: tuple[float, float]) -> str:
    return f"{f(pt[0])} {f(pt[1])}"


def unit(theta_deg: float) -> tuple[float, float]:
    t = math.radians(theta_deg)
    return math.cos(t), math.sin(t)


def normal(theta_deg: float) -> tuple[float, float]:
    t = math.radians(theta_deg)
    return -math.sin(t), math.cos(t)


def line(i: int, inset: float = 0.0) -> tuple[tuple[float, float], float]:
    """Bearing i as (unit normal, offset). `inset` walks the line toward the
    fix by that many pixels — which is how the pocket's edges are derived from
    the battens' edges rather than drawn as their own shape."""
    n = normal(BEARINGS[i])
    e = ERRORS[i]
    d = n[0] * FIX[0] + n[1] * FIX[1] + e - math.copysign(inset, e)
    return n, d


def cross(i: int, j: int, inset: float = 0.0) -> tuple[float, float]:
    (a, b), c = line(i, inset if isinstance(inset, float) else 0.0)
    (d, e), g = line(j, inset if isinstance(inset, float) else 0.0)
    det = a * e - b * d
    return ((c * e - b * g) / det, (a * g - c * d) / det)


def cross_inset(i: int, j: int) -> tuple[float, float]:
    """The pocket vertex: where the two battens' INNER edges meet."""
    (a, b), c = line(i, WIDTHS[i] / 2)
    (d, e), g = line(j, WIDTHS[j] / 2)
    det = a * e - b * d
    return ((c * e - b * g) / det, (a * g - c * d) / det)


def hat(inset: bool = False) -> list[tuple[float, float]]:
    fn = cross_inset if inset else (lambda i, j: cross(i, j))
    return [fn(0, 1), fn(1, 2), fn(2, 0)]


def tri_path(pts: list[tuple[float, float]]) -> str:
    return "M " + " L ".join(p(q) for q in pts) + " Z"


def foot(i: int) -> tuple[float, float]:
    """The point on bearing i closest to the fix — the origin for its extents."""
    n, d = line(i)
    k = d - (n[0] * FIX[0] + n[1] * FIX[1])
    return FIX[0] + n[0] * k, FIX[1] + n[1] * k


def ends(i: int) -> tuple[tuple[float, float], tuple[float, float]]:
    u, o, (t0, t1) = unit(BEARINGS[i]), foot(i), EXTENTS[i]
    return (o[0] + u[0] * t0, o[1] + u[1] * t0), (o[0] + u[0] * t1, o[1] + u[1] * t1)


def lit_side(i: int) -> float:
    """+1 or -1: which of the batten's two edges faces the key light."""
    n = normal(BEARINGS[i])
    return -1.0 if (n[0] * LIGHT[0] + n[1] * LIGHT[1]) > 0 else 1.0


def edge_path(i: int, frac: float) -> str:
    """The batten's centreline, walked `frac` of its half-width toward the lit
    edge (negative walks toward the shaded one)."""
    n, s = normal(BEARINGS[i]), lit_side(i)
    off = -s * frac * WIDTHS[i] / 2          # -s: the lit edge is at -s*n
    a, b = ends(i)
    return (f"M {f(a[0] + n[0] * off)} {f(a[1] + n[1] * off)} "
            f"L {f(b[0] + n[0] * off)} {f(b[1] + n[1] * off)}")


def batten_path(i: int) -> str:
    a, b = ends(i)
    return f"M {p(a)} L {p(b)}"


# ---------------------------------------------------------------- gel take

def gel_defs() -> str:
    grads = []
    for i in range(3):
        n, s = normal(BEARINGS[i]), lit_side(i)
        o, w = foot(i), WIDTHS[i] / 2
        x1, y1 = o[0] - s * n[0] * w, o[1] - s * n[1] * w      # lit edge
        x2, y2 = o[0] + s * n[0] * w, o[1] + s * n[1] * w      # shaded edge
        grads.append(f"""
    <linearGradient id="bat{i}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{BAT_LIT}" stop-opacity="{BAT_LIT_OP}"/>
      <stop offset="0.20" stop-color="{BAT_UPPER}" stop-opacity="{BAT_UPPER_OP}"/>
      <stop offset="0.58" stop-color="{BAT_CORE}" stop-opacity="{BAT_CORE_OP}"/>
      <stop offset="0.87" stop-color="{BAT_DEEP}" stop-opacity="{BAT_DEEP_OP}"/>
      <stop offset="1" stop-color="{BAT_BOUNCE}" stop-opacity="{BAT_BOUNCE_OP}"/>
    </linearGradient>""")
        a, b = ends(i)
        # Along the length: brighter where the rod runs toward the key light,
        # falling away from it. One light, no second source.
        near = 0 if (a[0] * LIGHT[0] + a[1] * LIGHT[1]) < (b[0] * LIGHT[0] + b[1] * LIGHT[1]) else 1
        p0, p1 = (a, b) if near == 0 else (b, a)
        grads.append(f"""
    <linearGradient id="run{i}" x1="{p(p0)}" x2="{p(p1)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#0C0F13" stop-opacity="0.16"/>
    </linearGradient>""")
    v = hat()
    return f"""{''.join(grads)}
    <radialGradient id="shard" cx="{f(FIX[0] - 14)}" cy="{f(FIX[1] - 10)}" r="150" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_CORE}"/>
      <stop offset="0.26" stop-color="{EMBER_HOT}"/>
      <stop offset="0.64" stop-color="{EMBER}"/>
      <stop offset="1" stop-color="{EMBER_SHADE}"/>
    </radialGradient>
    <radialGradient id="flare" cx="{f(FIX[0] - 10)}" cy="{f(FIX[1] - 6)}" r="58" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFCF3"/>
      <stop offset="0.34" stop-color="{EMBER_CORE}"/>
      <stop offset="0.74" stop-color="{EMBER_HOT}" stop-opacity="0.62"/>
      <stop offset="1" stop-color="{EMBER_HOT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="bloom" cx="{f(FIX[0])}" cy="{f(FIX[1])}" r="{f(BLOOM_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFCB95" stop-opacity="0.52"/>
      <stop offset="0.40" stop-color="{EMBER_HOT}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{EMBER_HOT}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="spill" cx="{f(FIX[0])}" cy="{f(FIX[1])}" r="{f(GROUND_BLOOM_R)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F9A45C" stop-opacity="0.20"/>
      <stop offset="0.55" stop-color="#F9A45C" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#F9A45C" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="pocketAO" cx="{f(FIX[0] - 8)}" cy="{f(FIX[1] - 4)}" r="112" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_DEEP}" stop-opacity="0"/>
      <stop offset="0.62" stop-color="{EMBER_DEEP}" stop-opacity="0.04"/>
      <stop offset="1" stop-color="{EMBER_DEEP}" stop-opacity="0.46"/>
    </radialGradient>
    <clipPath id="hatClip"><path d="{tri_path(v)}"/></clipPath>
    <clipPath id="pocketClip"><path d="{tri_path(hat(inset=True))}"/></clipPath>
    <clipPath id="battensClip">
      <path d="{batten_path(0)}" stroke-width="{f(WIDTHS[0])}" stroke-linecap="round"/>
      <path d="{batten_path(1)}" stroke-width="{f(WIDTHS[1])}" stroke-linecap="round"/>
      <path d="{batten_path(2)}" stroke-width="{f(WIDTHS[2])}" stroke-linecap="round"/>
    </clipPath>"""


def graticule() -> str:
    lines = []
    n = int(S / GRAT_STEP) + 2
    for k in range(-1, n):
        x = GRAT_STEP * k + 34
        y = GRAT_STEP * k + 62
        heavy = k % 3 == 1
        op = GRAT_MERIDIAN_OP if heavy else GRAT_OP
        wd = 2.6 if heavy else 1.6
        lines.append(f'<path d="M {f(x)} 0 L {f(x)} {S}" stroke="{GRATICULE}" '
                     f'stroke-opacity="{op}" stroke-width="{wd}"/>')
        lines.append(f'<path d="M 0 {f(y)} L {S} {f(y)}" stroke="{GRATICULE}" '
                     f'stroke-opacity="{op}" stroke-width="{wd}"/>')
    return "".join(lines)


def battens() -> str:
    out = []
    for i in STACK:
        w = WIDTHS[i]
        d = batten_path(i)
        out.append(f'<g id="bearing{i}">')
        # the rod's body: one stroke carrying the cross-section ramp
        out.append(f'<path d="{d}" stroke="url(#bat{i})" stroke-width="{f(w)}" '
                   f'stroke-linecap="round" fill="none"/>')
        out.append(f'<path d="{d}" stroke="url(#run{i})" stroke-width="{f(w)}" '
                   f'stroke-linecap="round" fill="none"/>')
        # the lit arris, then the far edge going to shadow and its bounce
        out.append(f'<path d="{edge_path(i, 0.80)}" stroke="{RIM}" stroke-opacity="{RIM_OP}" '
                   f'stroke-width="{f(w * 0.11)}" stroke-linecap="round" fill="none"/>')
        out.append(f'<path d="{edge_path(i, -0.86)}" stroke="#0E1115" stroke-opacity="0.22" '
                   f'stroke-width="{f(w * 0.13)}" stroke-linecap="round" fill="none"/>')
        out.append(f'<path d="{edge_path(i, -0.97)}" stroke="#8A94A2" stroke-opacity="0.26" '
                   f'stroke-width="{f(w * 0.05)}" stroke-linecap="round" fill="none"/>')
        out.append("</g>")
    return "".join(out)


def batten_shadows() -> str:
    out = []
    for i in STACK:
        a, b = ends(i)
        dx, dy = SHADOW_OFF
        out.append(f'<path d="M {f(a[0] + dx)} {f(a[1] + dy)} L {f(b[0] + dx)} {f(b[1] + dy)}" '
                   f'stroke="{SHADOW}" stroke-opacity="{SHADOW_OP}" stroke-width="{f(WIDTHS[i] * 1.04)}" '
                   f'stroke-linecap="round" fill="none"/>')
    return f'<g filter="url(#castShadow)">{"".join(out)}</g>'


def gel_svg() -> str:
    v, pv = hat(), hat(inset=True)
    arris = "".join(
        f'<path d="M {p(pv[k])} L {p(pv[(k + 1) % 3])}" stroke="{ARRIS}" '
        f'stroke-opacity="{op}" stroke-width="{wd}" stroke-linecap="round" fill="none"/>'
        for k, (op, wd) in enumerate(((0.90, 3.6), (0.62, 3.0), (0.74, 3.2))))
    return document(gel_defs(), f"""
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <g id="chart">{graticule()}</g>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
      <rect width="{S}" height="{S}" fill="url(#spill)"/>
    </g>

    <g id="mid">
      {batten_shadows()}
      <!-- the fix, seated under the rods so its light bleeds beneath them -->
      <g clip-path="url(#hatClip)">
        <path d="{tri_path(v)}" fill="url(#shard)"/>
        <path d="{tri_path(v)}" fill="url(#pocketAO)"/>
        <circle cx="{f(FIX[0] - 10)}" cy="{f(FIX[1] - 6)}" r="58" fill="url(#flare)"/>
      </g>
      {battens()}
    </g>

    <g id="fg">
      <!-- the fix's light running back out along the lines that made it -->
      <g clip-path="url(#battensClip)">
        <circle cx="{f(FIX[0])}" cy="{f(FIX[1])}" r="{f(BLOOM_R)}" fill="url(#bloom)"/>
      </g>
      <!-- the pocket's own machined edges: where each rod catches the fix -->
      {arris}
      <circle cx="{f(FIX[0] - 10)}" cy="{f(FIX[1] - 6)}" r="16" fill="#FFFDF6" fill-opacity="0.92"/>
    </g>

    <g id="highlight">
      <ellipse cx="330" cy="250" rx="330" ry="250" fill="#FFFFFF" fill-opacity="0.10" filter="url(#softBlur)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="0.80" stroke-width="8"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#C7B9A0" stroke-opacity="0.35" stroke-width="2"/>
    </g>""")


# -------------------------------------------------------------- chart take

CHART_INK = "#2B3038"
CHART_W = 13.0
PRISM_H = 34.0                # the cocked hat given real thickness


def chart_svg() -> str:
    v = hat()
    order = sorted(range(3), key=lambda k: -v[k][1])       # lowest vertex first
    side_paths = []
    for k in range(3):
        a, b = v[k], v[(k + 1) % 3]
        if (a[1] + b[1]) / 2 < min(q[1] for q in v) + 4:
            continue
        side_paths.append(
            f'<path d="M {p(a)} L {p(b)} L {f(b[0])} {f(b[1] + PRISM_H)} '
            f'L {f(a[0])} {f(a[1] + PRISM_H)} Z" fill="url(#prismSide)"/>')
    rules = "".join(
        f'<path d="{batten_path(i)}" stroke="{CHART_INK}" stroke-opacity="0.82" '
        f'stroke-width="{f(CHART_W)}" stroke-linecap="round" fill="none"/>'
        f'<path d="{edge_path(i, 0.55)}" stroke="#FFFFFF" stroke-opacity="0.30" '
        f'stroke-width="3" stroke-linecap="round" fill="none"/>'
        for i in STACK)
    return document(f"""
    <linearGradient id="prismTop" x1="{f(FIX[0] - 130)}" y1="{f(FIX[1] - 130)}" x2="{f(FIX[0] + 130)}" y2="{f(FIX[1] + 130)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_CORE}"/>
      <stop offset="0.34" stop-color="{EMBER_HOT}"/>
      <stop offset="1" stop-color="{EMBER}"/>
    </linearGradient>
    <linearGradient id="prismSide" x1="0" y1="{f(FIX[1])}" x2="0" y2="{f(FIX[1] + PRISM_H + 60)}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_SHADE}"/>
      <stop offset="1" stop-color="{EMBER_DEEP}"/>
    </linearGradient>
    <radialGradient id="spill" cx="{f(FIX[0])}" cy="{f(FIX[1])}" r="300" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F9A45C" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#F9A45C" stop-opacity="0"/>
    </radialGradient>""", f"""
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <g id="chart">{graticule()}</g>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
      <rect width="{S}" height="{S}" fill="url(#spill)"/>
    </g>

    <g id="mid">{rules}</g>

    <g id="fg">
      <g filter="url(#castShadow)">
        <path d="{tri_path([(q[0] + 20, q[1] + PRISM_H + 24) for q in v])}" fill="{SHADOW}" fill-opacity="0.38"/>
      </g>
      {''.join(side_paths)}
      <path d="{tri_path(v)}" fill="url(#prismTop)"/>
      <path d="{tri_path(v)}" fill="none" stroke="{ARRIS}" stroke-opacity="0.80" stroke-width="3.4"/>
      <circle cx="{f(FIX[0] - 8)}" cy="{f(FIX[1] - 4)}" r="46" fill="#FFF3DF" fill-opacity="0.34" filter="url(#softBlur)"/>
    </g>

    <g id="highlight">
      <ellipse cx="330" cy="250" rx="330" ry="250" fill="#FFFFFF" fill-opacity="0.10" filter="url(#softBlur)"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="0.80" stroke-width="8"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#C7B9A0" stroke-opacity="0.35" stroke-width="2"/>
    </g>""")


# ---------------------------------------------------------------- document

def document(defs: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>
    <radialGradient id="ground" cx="{f(GROUND_KEY[0])}" cy="{f(GROUND_KEY[1])}" r="1010" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.50" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="512" cy="512" r="740" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="0.72" stop-color="{VIGNETTE}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.17"/>
    </radialGradient>
    <filter id="castShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
    <filter id="softBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="34"/>
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
    (ASSETS / "icon.svg").write_text(gel_svg())
    print("  wrote icon.svg (gel rods on a chart, the fix glowing in the pocket — the master)")
    (ASSETS / "icon-engineA2-chart.svg").write_text(chart_svg())
    print("  wrote icon-engineA2-chart.svg (inked chart lines, the hat as a raised prism)")
    if "--export" in sys.argv:
        export(ASSETS / "icon.svg")


if __name__ == "__main__":
    main()
