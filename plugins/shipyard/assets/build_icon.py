#!/usr/bin/env python3
"""build_icon.py — the shipyard icon's layered SVG master, emitted from constants.

    python3 build_icon.py            # writes icon.svg

Direction: Tahoe gel-glass, porcelain sub-register (a) — a lit slate object on a
porcelain cushion tile with one bounded warm accent.

Device (subject-mined): a hull mid-build on its keel blocks. The stern half is
planked into a smooth slate gel skin; the bow half is still open frames with the
porcelain showing between them.

Signature move — "the next plank arrives lit": the single strake at the boundary
between planked and open is an emissive ember bar standing proud of the sheer,
lighting the frames it is about to join and spilling warm light through the open
bay onto the ground. It is the stage in progress, and the only chroma in the tile.

Corpus numbers this was authored against (sampled from
references/corpus/apple-2026/, interior only):
  porcelain ground        L p50 0.96, p95 1.00 top, p05 0.90 bottom  (apple-05/06)
  contact shadow floor    L 0.88 — shadows on porcelain are shallow and wide
  warm accent ramp        H 30-48, S 0.39-1.00, V 0.98-1.00, L 0.62 -> 0.92 (apple-06 Home)
                          H 6-36,  S 0.63-0.85, V 0.84-0.95, L 0.33 -> 0.74 (apple-05 Infuse)
  dark object shadow face rgb(28,36,51) H219 S0.45 V0.20 — cool slate, not warm
                          (apple-12 Calculator, apple-10 ChatGPT)
Everything below is a named constant so a fidelity round is a parameter edit.
"""
from __future__ import annotations

import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / "icon.svg"
SQ = (pathlib.Path(__file__).resolve().parent / "squircle-path.txt").read_text().strip()

W = 1024

# ---------------------------------------------------------------- palette
# One key light: top, tilted a little left. One accent family (ember), one
# body family (slate). The ground is neutral porcelain.
KEY = ((330.0, 236.0), (700.0, 726.0))          # key axis, userSpaceOnUse

GROUND_HI = "#FDFCF9"
GROUND_MID = "#F6F4EF"
GROUND_LO = "#E5E0D6"
VIGNETTE = "#8B8070"

HULL_HI = "#8395AC"      # lit upper strakes
HULL_MID = "#586A80"
HULL_LO = "#37455A"
HULL_DEEP = "#1F2937"    # = corpus rgb(31,41,55), the measured shadow face
HULL_RIM = "#C6D2E2"

FRAME_HI = "#7A8CA2"
FRAME_LO = "#28323F"
FRAME_RIM = "#A9B8CB"

KEEL_HI = "#3E4D60"
KEEL_LO = "#19222E"

BLOCK_TOP = "#DFE5EC"
BLOCK_HI = "#B3BECB"
BLOCK_LO = "#7C8B9C"
BLOCK_EDGE = "#7C8A9A"

EMBER_LIP = "#FFE0B0"    # hot lip, H38 S0.31 V1.00
EMBER_HI = "#FFA344"     # H33 S0.73 V1.00
EMBER_CORE = "#F8681B"   # H23 S0.89 V0.97
EMBER_LO = "#D2430A"     # H17 S0.95 V0.82
EMBER_DEEP = "#A22F06"   # stays saturated in shadow (the gel rule)
EMBER_GLOW = "#FF7A22"

SHADOW = "#2B333F"

# r02, sampled from icon-engineC-b3fcac.png at x=700/760 and y=520:
#   hull body L 0.18-0.22, nearly flat, deep only in the last tenth
#   plank seams L 0.04-0.08 — dark grooves, and no lit lip at every seam
#   the near sheer's top edge is a single bright line at L 0.58-0.61
#   frames L 0.20-0.35 across their width, gaps are clean ground at 0.95
SEAM = "#070B11"
SEAM_OP = 0.82
SHEER_LIP = "#8296AF"    # L 0.58 in sRGB value space — the lit gunwale
SHEER_LIP_W = 7.0
FRAME_LIT = "#4B5C70"   # L 0.35, the reference's lit frame edge
FRAME_MID = "#33404F"   # L 0.25
FRAME_DARK = "#1B242F"  # L 0.14

# ---------------------------------------------------------------- geometry
DX = -8.0                # geometry-space nudge, kept small and readable
DY = 0.0
SCALE = 1.08             # r01: the object carries too little of the tile at 1.0
OFFSET = (-18.0, -6.0)   # r08: measured off the render — the ink bbox centres on 512
MOUTH = (26.0, -30.0)    # r01: offset to the far sheer — the three-quarter tell

# hull outline, bow left. Four cubics, closed.
BOW = (236, 310)
SHEER = (BOW, (386, 452), (648, 434), (824, 372))          # deck line
TRANSOM = ((824, 372), (832, 456), (814, 534), (794, 602))  # raked stern
KEEL = ((794, 602), (640, 646), (460, 654), (338, 642))     # keel, slight rocker
FOREFOOT = ((338, 642), (258, 634), (222, 452), BOW)        # forefoot into the stem

PLANK_BOUND = 496.0      # x where the planking has reached
FRAME_X = (306, 368, 430, 492)             # open frames, forward of the boundary
FRAME_W = (30, 32, 33, 33)                 # sided width, bottom
FRAME_W_TOP = (23, 25, 26, 26)

BACKBONE_W = 30.0        # keel + stem, stroked
STRAKE_OFFSETS = (-34.0, -76.0, -122.0, -170.0)   # seams below the sheer, aft only

EMBER_X0, EMBER_X1 = 266.0, 548.0
EMBER_LIFT0 = 30.0       # forward end still up in the air …
EMBER_LIFT1 = 2.5        # … aft end almost seated: the plank is mid-fit
EMBER_T = 38.0           # plank thickness — r04: holds a pixel at 16px
EMBER_TAPER = 0.72       # thickness at the forward tip, as a fraction
EMBER_TAPER_AFT = 0.55   # r06: and at the aft end, so it is not a blunt cut

BLOCK_X = (388, 556, 716)
BLOCK_W = (108, 104, 98)
GROUND_Y = 726.0         # the yard floor the cradle stands on

SOLE_X = (296.0, 812.0)  # r06: the slipway sole plate the keel blocks stand on
SOLE_H = 29.0


# ---------------------------------------------------------------- curves
def cub(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return (a * x0 + b * x1 + c * x2 + d * x3, a * y0 + b * y1 + c * y2 + d * y3)


def cub_tan(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    a, b, c = 3 * u * u, 6 * u * t, 3 * t * t
    return (a * (x1 - x0) + b * (x2 - x1) + c * (x3 - x2),
            a * (y1 - y0) + b * (y2 - y1) + c * (y3 - y2))


def normal(p, t):
    """Unit normal pointing away from the hull's interior — up, on the sheer."""
    tx, ty = cub_tan(p, t)
    n = math.hypot(tx, ty) or 1.0
    return (ty / n, -tx / n)


def t_at_x(p, x, lo=0.0, hi=1.0):
    for _ in range(48):
        m = (lo + hi) / 2
        if cub(p, m)[0] < x:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def sample(p, t0, t1, n):
    return [t0 + (t1 - t0) * i / (n - 1) for i in range(n)]


def offset_curve(p, t0, t1, d, n=44):
    pts = []
    for t in sample(p, t0, t1, n):
        (x, y), (nx, ny) = cub(p, t), normal(p, t)
        pts.append((x + nx * d, y + ny * d))
    return pts


def band(p, t0, t1, d_lo, d_hi, n=44):
    """Closed polygon between two offsets of the same curve."""
    a = offset_curve(p, t0, t1, d_hi, n)
    b = offset_curve(p, t0, t1, d_lo, n)
    return a + b[::-1]


def lerp_band(p, t0, t1, lift0, lift1, thick, taper, n=44, a=-0.5, b=0.5):
    """A plank whose stand-off and thickness both vary along the run.

    The signature move lives here: lift0 > lift1 means the forward end is still
    in the air while the aft end has almost landed, which is what makes the
    plank read as arriving rather than as a stripe. `a`/`b` cut one slice of
    the cross-section, so the material ramp is authored as stacked faces that
    follow the curve instead of one vertical gradient that does not.
    """
    top, bot = [], []
    for i, t in enumerate(sample(p, t0, t1, n)):
        f = i / (n - 1)
        lift = lift0 + (lift1 - lift0) * f
        th = thick * (taper + (1 - taper) * min(1.0, f * 2.2))
        th *= EMBER_TAPER_AFT + (1 - EMBER_TAPER_AFT) * min(1.0, (1 - f) * 7)
        (x, y), (nx, ny) = cub(p, t), normal(p, t)
        top.append((x + nx * (lift + th * b), y + ny * (lift + th * b)))
        bot.append((x + nx * (lift + th * a), y + ny * (lift + th * a)))
    return top + bot[::-1], top


def taper_band(pts_c, w_a, w_b):
    """Closed polygon around a centreline, width lerped a->b."""
    n = len(pts_c)
    left, right = [], []
    for i, (x, y) in enumerate(pts_c):
        j = min(n - 1, i + 1)
        k = max(0, i - 1)
        tx, ty = pts_c[j][0] - pts_c[k][0], pts_c[j][1] - pts_c[k][1]
        m = math.hypot(tx, ty) or 1.0
        nx, ny = ty / m, -tx / m
        w = (w_a + (w_b - w_a) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def poly(pts, close=True):
    d = "M" + " L".join(f"{x + DX:.1f},{y + DY:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def cpath(*curves):
    """Emit a run of cubics sharing endpoints as one path."""
    (x0, y0) = curves[0][0]
    d = f"M{x0 + DX:.1f},{y0 + DY:.1f}"
    for c in curves:
        d += (f" C{c[1][0] + DX:.1f},{c[1][1] + DY:.1f}"
              f" {c[2][0] + DX:.1f},{c[2][1] + DY:.1f}"
              f" {c[3][0] + DX:.1f},{c[3][1] + DY:.1f}")
    return d + " Z"


# ---------------------------------------------------------------- derived
HULL_D = cpath(SHEER, TRANSOM, KEEL, FOREFOOT)

# the bottom boundary as a lookup, so a frame's heel lands on the real keel
_bottom = ([cub(FOREFOOT, 1 - t) for t in sample(None, 0, 1, 60)]
           + [cub(KEEL, 1 - t) for t in sample(None, 0, 1, 60)])
_bottom = sorted(_bottom, key=lambda p: p[0])


def keel_y(x):
    for (x0, y0), (x1, y1) in zip(_bottom, _bottom[1:]):
        if x0 <= x <= x1:
            f = (x - x0) / ((x1 - x0) or 1)
            return y0 + (y1 - y0) * f
    return _bottom[-1][1]


def sheer_pt(x):
    return cub(SHEER, t_at_x(SHEER, x))


def frame_curve(x, n=26):
    """One frame: heel on the keel, head at the sheer, flaring forward."""
    hx, hy = x, keel_y(x) - 4
    tx, ty = sheer_pt(x)
    flare = 16 + 26 * max(0.0, (460 - x) / 260)      # bow frames sweep forward
    c1 = (hx - flare * 0.45, hy - (hy - ty) * 0.42)
    c2 = (tx - flare, ty + (hy - ty) * 0.34)
    return [cub(((hx, hy), c1, c2, (tx, ty)), i / (n - 1)) for i in range(n)]


T_EMBER = (t_at_x(SHEER, EMBER_X0), t_at_x(SHEER, EMBER_X1))
T_BOUND = t_at_x(SHEER, PLANK_BOUND)

def ember_slice(a, b):
    return lerp_band(SHEER, T_EMBER[0], T_EMBER[1], EMBER_LIFT0, EMBER_LIFT1,
                     EMBER_T, EMBER_TAPER, 40, a, b)[0]


EMBER_POLY = ember_slice(-0.5, 0.5)
EMBER_FACES = (                     # stacked cross-section faces, lit lip on top
    (ember_slice(-0.50, -0.20), "url(#emberdeep)"),
    (ember_slice(-0.22, 0.16), "url(#embercore)"),
    (ember_slice(0.14, 0.40), EMBER_HI),
    (ember_slice(0.34, 0.50), EMBER_LIP),
)

BACKBONE = ([cub(FOREFOOT, t) for t in sample(None, 0.06, 1, 30)]
            + [cub(KEEL, t) for t in sample(None, 0, 0.99, 30)][::-1])
BACKBONE = sorted(set(BACKBONE), key=lambda p: p[0])


def shift(pts, d=MOUTH):
    return [(x + d[0], y + d[1]) for x, y in pts]


def mouth_band(t0, t1, n=34):
    """The deck opening: near sheer below, far sheer above, dark interior between.

    Looking slightly down on the hull puts the far side of the rim above the
    near one; the band between them is the inside of the vessel, and it is the
    single cheapest volume cue the raster reference has that a flat elevation
    does not.
    """
    near = offset_curve(SHEER, t0, t1, 0, n)
    far = shift(near)
    return near + far[::-1], far


def g(tag):
    return "\n    ".join(tag)


# ---------------------------------------------------------------- svg
def build() -> str:
    (kx1, ky1), (kx2, ky2) = KEY
    # one transform for every object plane, so gradients, filters and geometry
    # all ride the same scale instead of being re-derived per layer
    tf = (f'transform="translate({512 + OFFSET[0]},{512 + OFFSET[1]}) '
          f'scale({SCALE}) translate(-512,-512)"')
    frames = [frame_curve(x) for x in FRAME_X]
    frame_polys = [taper_band(c, w, wt) for c, w, wt in zip(frames, FRAME_W, FRAME_W_TOP)]
    frame_grads = []
    for i, (c, w) in enumerate(zip(frames, FRAME_W)):
        cx = sum(x for x, _ in c) / len(c)
        frame_grads.append(
            f'<linearGradient id="fr{i}" gradientUnits="userSpaceOnUse" '
            f'x1="{cx - w * 0.62 + DX:.1f}" y1="0" x2="{cx + w * 0.75 + DX:.1f}" y2="0">'
            f'<stop offset="0" stop-color="{FRAME_LIT}"/>'
            f'<stop offset="0.26" stop-color="{FRAME_MID}"/>'
            f'<stop offset="1" stop-color="{FRAME_DARK}"/></linearGradient>')

    blocks = []
    for cx, bw in zip(BLOCK_X, BLOCK_W):
        top = keel_y(cx) - 2
        blocks.append((cx, bw, top))

    defs = f"""
  <defs>
    <!-- the tile is a cushion: bright near the key, vignetted at the rim -->
    <radialGradient id="cushion" cx="0.36" cy="0.20" r="0.98">
      <stop offset="0"    stop-color="{GROUND_HI}"/>
      <stop offset="0.50" stop-color="{GROUND_MID}"/>
      <stop offset="1"    stop-color="{GROUND_LO}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.48" r="0.74">
      <stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1"    stop-color="{VIGNETTE}" stop-opacity="0.17"/>
    </radialGradient>

    <!-- one key, one axis: every body plane hangs off this segment -->
    <linearGradient id="hull" gradientUnits="userSpaceOnUse"
        x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}">
      <stop offset="0"    stop-color="{HULL_HI}"/>
      <stop offset="0.22" stop-color="{HULL_MID}"/>
      <stop offset="0.78" stop-color="{HULL_LO}"/>
      <stop offset="1"    stop-color="{HULL_DEEP}"/>
    </linearGradient>
    <linearGradient id="bilge" gradientUnits="userSpaceOnUse"
        x1="0" y1="470" x2="0" y2="{GROUND_Y - 40}">
      <stop offset="0"    stop-color="{HULL_DEEP}" stop-opacity="0"/>
      <stop offset="0.66" stop-color="{HULL_DEEP}" stop-opacity="0.26"/>
      <stop offset="1"    stop-color="#131A24" stop-opacity="0.50"/>
    </linearGradient>
    <linearGradient id="bounceup" gradientUnits="userSpaceOnUse"
        x1="0" y1="{GROUND_Y - 130}" x2="0" y2="{GROUND_Y - 52}">
      <stop offset="0"    stop-color="#93A6BE" stop-opacity="0"/>
      <stop offset="1"    stop-color="#93A6BE" stop-opacity="0.34"/>
    </linearGradient>
    <linearGradient id="sheerstrake" gradientUnits="userSpaceOnUse"
        x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}">
      <stop offset="0"    stop-color="#93A5BC"/>
      <stop offset="0.55" stop-color="#69798F"/>
      <stop offset="1"    stop-color="#44536A"/>
    </linearGradient>
    <linearGradient id="mouth" gradientUnits="userSpaceOnUse"
        x1="0" y1="{BOW[1] - 40}" x2="0" y2="{BOW[1] + 190}">
      <stop offset="0"    stop-color="#0F151E"/>
      <stop offset="0.55" stop-color="#1C2632"/>
      <stop offset="1"    stop-color="#2E3B4C"/>
    </linearGradient>
    <linearGradient id="farsheer" gradientUnits="userSpaceOnUse"
        x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}">
      <stop offset="0"    stop-color="#9FB0C6"/>
      <stop offset="1"    stop-color="#5A6B81"/>
    </linearGradient>
    <linearGradient id="framedeep" gradientUnits="userSpaceOnUse"
        x1="0" y1="380" x2="0" y2="{GROUND_Y}">
      <stop offset="0"    stop-color="{FRAME_LO}" stop-opacity="0"/>
      <stop offset="0.62" stop-color="{FRAME_LO}" stop-opacity="0.18"/>
      <stop offset="1"    stop-color="#0E141C" stop-opacity="0.55"/>
    </linearGradient>
    <linearGradient id="keel" gradientUnits="userSpaceOnUse"
        x1="0" y1="560" x2="0" y2="646">
      <stop offset="0"    stop-color="{KEEL_HI}"/>
      <stop offset="1"    stop-color="{KEEL_LO}"/>
    </linearGradient>
    <linearGradient id="block" gradientUnits="userSpaceOnUse"
        x1="0" y1="612" x2="0" y2="{GROUND_Y}">
      <stop offset="0"    stop-color="{BLOCK_HI}"/>
      <stop offset="1"    stop-color="{BLOCK_LO}"/>
    </linearGradient>
    <linearGradient id="prop" gradientUnits="userSpaceOnUse"
        x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}">
      <stop offset="0"    stop-color="#BAC5D2"/>
      <stop offset="1"    stop-color="#78879A"/>
    </linearGradient>

    <!-- the accent: an emissive bar, saturated all the way into its shadow.
         Authored as stacked faces along the run, because one vertical gradient
         cannot stay perpendicular to a curve that drops 130px across the tile. -->
    <linearGradient id="embercore" gradientUnits="userSpaceOnUse"
        x1="{EMBER_X0}" y1="0" x2="{EMBER_X1}" y2="0">
      <stop offset="0"    stop-color="{EMBER_CORE}"/>
      <stop offset="0.48" stop-color="#FF8A33"/>
      <stop offset="1"    stop-color="{EMBER_CORE}"/>
    </linearGradient>
    <linearGradient id="emberdeep" gradientUnits="userSpaceOnUse"
        x1="{EMBER_X0}" y1="0" x2="{EMBER_X1}" y2="0">
      <stop offset="0"    stop-color="{EMBER_DEEP}"/>
      <stop offset="0.60" stop-color="{EMBER_LO}"/>
      <stop offset="1"    stop-color="{EMBER_DEEP}"/>
    </linearGradient>
    <linearGradient id="emberfade" gradientUnits="userSpaceOnUse"
        x1="{EMBER_X0}" y1="0" x2="{EMBER_X1}" y2="0">
      <stop offset="0"    stop-color="#fff" stop-opacity="0.62"/>
      <stop offset="0.30" stop-color="#fff" stop-opacity="1"/>
      <stop offset="1"    stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <radialGradient id="bounce" gradientUnits="userSpaceOnUse"
        cx="{EMBER_X1 - 70 + DX:.0f}" cy="{sheer_pt(EMBER_X1 - 70)[1] + 40:.0f}" r="200">
      <stop offset="0"    stop-color="{EMBER_GLOW}" stop-opacity="0.62"/>
      <stop offset="0.34" stop-color="{EMBER_GLOW}" stop-opacity="0.26"/>
      <stop offset="1"    stop-color="{EMBER_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="bounceHull" cx="0" cy="0.5" r="1">
      <stop offset="0"    stop-color="{EMBER_GLOW}" stop-opacity="0.42"/>
      <stop offset="0.55" stop-color="{EMBER_GLOW}" stop-opacity="0.13"/>
      <stop offset="1"    stop-color="{EMBER_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"    stop-color="{EMBER_GLOW}" stop-opacity="0.30"/>
      <stop offset="0.45" stop-color="{EMBER_GLOW}" stop-opacity="0.12"/>
      <stop offset="1"    stop-color="{EMBER_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" gradientUnits="userSpaceOnUse"
        x1="{EMBER_X0}" y1="0" x2="820" y2="0">
      <stop offset="0"    stop-color="{HULL_RIM}" stop-opacity="0.9"/>
      <stop offset="0.55" stop-color="{HULL_RIM}" stop-opacity="0.5"/>
      <stop offset="1"    stop-color="{HULL_RIM}" stop-opacity="0.12"/>
    </linearGradient>

    <mask id="embermask" maskUnits="userSpaceOnUse" x="0" y="0" width="1024" height="1024">
      <rect x="0" y="0" width="1024" height="1024" fill="url(#emberfade)"/>
    </mask>

    <filter id="blurS" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <filter id="blurM" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="17"/>
    </filter>
    <filter id="blurL" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    {g(frame_grads)}
    <clipPath id="hullClip"><path d="{HULL_D}"/></clipPath>
    <clipPath id="aftClip"><rect x="{PLANK_BOUND + DX:.1f}" y="0" width="600" height="1024"/></clipPath>
    <clipPath id="frameClip" clip-rule="nonzero">
      {"".join(f'<path d="{poly(p)}"/>' for p in frame_polys)}
    </clipPath>
  </defs>"""

    # ---- bg: the cushion tile
    bg = f"""
  <g id="bg">
    <rect width="1024" height="1024" fill="url(#cushion)"/>
    <rect width="1024" height="1024" fill="url(#vignette)"/>
    <ellipse cx="{430 + DX + OFFSET[0]:.0f}" cy="{424 + OFFSET[1]:.0f}" rx="196" ry="120" fill="url(#halo)" opacity="0.42"/>
  </g>"""

    # ---- mid: floor shadow and the cradle the hull stands on
    block_svg = []
    for cx, bw, top in blocks:
        h = GROUND_Y - top
        block_svg.append(
            f'<path d="M{cx - bw / 2 + DX:.1f},{top + 8:.1f} '
            f'Q{cx - bw / 2 + DX:.1f},{top:.1f} {cx - bw / 2 + 9 + DX:.1f},{top:.1f} '
            f'L{cx + bw / 2 - 9 + DX:.1f},{top:.1f} '
            f'Q{cx + bw / 2 + DX:.1f},{top:.1f} {cx + bw / 2 + DX:.1f},{top + 8:.1f} '
            f'L{cx + bw / 2 - 3 + DX:.1f},{GROUND_Y - SOLE_H:.1f} '
            f'L{cx - bw / 2 + 3 + DX:.1f},{GROUND_Y - SOLE_H:.1f} Z" fill="url(#block)"/>')
        block_svg.append(
            f'<rect x="{cx - bw / 2 + 6 + DX:.1f}" y="{top + 1:.1f}" width="{bw - 12:.1f}" '
            f'height="5" rx="2.5" fill="{BLOCK_TOP}" opacity="0.85"/>')
        block_svg.append(
            f'<rect x="{cx - bw / 2 + 4 + DX:.1f}" y="{top + h * 0.46:.1f}" width="{bw - 8:.1f}" '
            f'height="3" rx="1.5" fill="{BLOCK_EDGE}" opacity="0.30"/>')

    sole = (
        f'<rect x="{SOLE_X[0] + DX:.1f}" y="{GROUND_Y - SOLE_H:.1f}" '
        f'width="{SOLE_X[1] - SOLE_X[0]:.1f}" height="{SOLE_H:.1f}" rx="9" fill="url(#prop)"/>'
        f'<rect x="{SOLE_X[0] + 8 + DX:.1f}" y="{GROUND_Y - SOLE_H + 2:.1f}" '
        f'width="{SOLE_X[1] - SOLE_X[0] - 16:.1f}" height="5" rx="2.5" fill="{BLOCK_TOP}" opacity="0.8"/>')

    mid = f"""
  <g id="mid" {tf}>
    <ellipse cx="{520 + DX}" cy="{GROUND_Y + 12:.0f}" rx="366" ry="46"
             fill="{SHADOW}" opacity="0.09" filter="url(#blurL)"/>
    <ellipse cx="{512 + DX}" cy="{GROUND_Y + 6:.0f}" rx="286" ry="24"
             fill="{SHADOW}" opacity="0.26" filter="url(#blurM)"/>
    {sole}
    {g(block_svg)}
    {g(f'<ellipse cx="{cx + DX}" cy="{GROUND_Y - SOLE_H + 3:.0f}" rx="{bw / 2 + 4:.0f}" ry="8" fill="{SHADOW}" opacity="0.26" filter="url(#blurS)"/>' for cx, bw, _ in blocks)}
  </g>"""

    # ---- fg: backbone, frames, planked skin
    strakes = []
    for i, d in enumerate(STRAKE_OFFSETS):
        pts = offset_curve(SHEER, T_BOUND - 0.04, 1.0, d, 30)
        strakes.append(f'<path d="{poly(pts, False)}" fill="none" stroke="{SEAM}" '
                       f'stroke-opacity="{SEAM_OP - i * 0.04:.2f}" stroke-width="4.5"/>')
    # the one lit lip the reference does carry: the first plank below the sheer
    strakes.append(
        f'<path d="{poly(offset_curve(SHEER, T_BOUND - 0.04, 1.0, -16.0, 30), False)}" '
        f'fill="none" stroke="{HULL_RIM}" stroke-opacity="0.30" stroke-width="5"/>')

    fg = f"""
  <g id="fg" {tf}>
    <g id="farside">
      {g(f'<path d="{poly(shift(p))}" fill="#2B3746"/>' for p in frame_polys)}
      <path d="{poly(mouth_band(0.02, 1.0)[0])}" fill="url(#mouth)"/>
      <path d="{poly(shift(offset_curve(SHEER, 0.02, 1.0, 0, 34)), False)}" fill="none"
            stroke="url(#farsheer)" stroke-width="13" stroke-linecap="round"/>
      <path d="{poly(shift(offset_curve(SHEER, 0.06, 1.0, 5.5, 34)), False)}" fill="none"
            stroke="{HULL_RIM}" stroke-opacity="0.42" stroke-width="3" stroke-linecap="round"/>
    </g>

    <path d="{poly(BACKBONE, False)}" fill="none" stroke="url(#keel)"
          stroke-width="{BACKBONE_W}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="{poly(BACKBONE, False)}" fill="none" stroke="{HULL_RIM}" stroke-opacity="0.26"
          stroke-width="3" stroke-linecap="round" transform="translate(0,-11)"/>

    <g id="frames">
      {g(f'<path d="{poly(p)}" fill="url(#fr{i})"/>' for i, p in enumerate(frame_polys))}
      {g(f'<path d="{poly(p)}" fill="url(#framedeep)"/>' for p in frame_polys)}
      {g(f'<ellipse cx="{c[0][0] + DX:.0f}" cy="{c[0][1] + 6:.0f}" rx="17" ry="7" fill="#0E141C" opacity="0.30" filter="url(#blurS)"/>' for c in frames)}
    </g>

    <g clip-path="url(#hullClip)">
      <g clip-path="url(#aftClip)">
        <path d="{HULL_D}" fill="url(#hull)"/>
        <path d="{HULL_D}" fill="url(#bilge)"/>
        <path d="{HULL_D}" fill="url(#bounceup)"/>
        <path d="{poly(band(SHEER, T_BOUND - 0.05, 1.0, -SHEER_LIP_W, 0.0, 30))}" fill="{SHEER_LIP}"/>
        {g(strakes)}
        <path d="{poly(offset_curve(SHEER, T_BOUND - 0.05, T_BOUND + 0.02, 0, 8) + [(PLANK_BOUND + 6, 660), (PLANK_BOUND - 60, 660)])}"
              fill="#0E141C" opacity="0.22" filter="url(#blurM)"/>
      </g>
    </g>
  </g>"""

    # ---- highlight: the plank being fitted, and everything its light touches
    hl = f"""
  <g id="highlight">
   <g {tf}>
    <ellipse cx="{(EMBER_X0 + EMBER_X1) / 2 + DX:.0f}" cy="418" rx="184" ry="96"
             fill="url(#halo)"/>
    <path d="{poly(EMBER_POLY)}" fill="{EMBER_GLOW}" opacity="0.62" filter="url(#blurM)"/>
    <path d="{poly(EMBER_POLY)}" fill="#FFB258" opacity="0.28" filter="url(#blurL)"/>

    <g clip-path="url(#frameClip)">
      <rect x="{DX + 200:.0f}" y="280" width="420" height="420" fill="url(#bounce)"/>
    </g>
    <g clip-path="url(#hullClip)">
      <g clip-path="url(#aftClip)">
        <ellipse cx="{PLANK_BOUND + DX:.0f}" cy="470" rx="230" ry="150"
                 fill="url(#bounceHull)"/>
      </g>
    </g>

    <g mask="url(#embermask)">
      <path d="{poly(EMBER_POLY)}" fill="{EMBER_GLOW}" opacity="0.30" filter="url(#blurS)"/>
      {g(f'<path d="{poly(p)}" fill="{f_}"/>' for p, f_ in EMBER_FACES)}
    </g>

    <ellipse cx="{EMBER_X1 - 34 + DX:.0f}" cy="{sheer_pt(EMBER_X1 - 34)[1] + 12:.0f}" rx="52" ry="11"
             fill="#0E141C" opacity="0.34" filter="url(#blurS)"/>
    {g(f'<path d="{poly(p)}" fill="{f_}"/>' for p, f_ in EMBER_FACES[:1])}
    <path d="{poly(offset_curve(SHEER, T_BOUND, 1.0, -1.6, 26), False)}" fill="none"
          stroke="url(#rim)" stroke-width="3.6" stroke-linecap="round"/>
    <path d="{poly(offset_curve(FOREFOOT, 0.30, 0.98, 13, 22), False)}" fill="none"
          stroke="{HULL_RIM}" stroke-opacity="0.34" stroke-width="3" stroke-linecap="round"/>

    <ellipse cx="{404 + DX}" cy="{GROUND_Y + 2:.0f}" rx="182" ry="34"
             fill="{EMBER_GLOW}" opacity="0.22" filter="url(#blurL)"/>
    <ellipse cx="{404 + DX}" cy="{GROUND_Y - 4:.0f}" rx="104" ry="18"
             fill="#FFC178" opacity="0.28" filter="url(#blurM)"/>

   </g>
    <path d="{SQ}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="5"
          transform="translate(3.07,3.07) scale(0.994)"/>
  </g>"""

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" '
            f'viewBox="0 0 {W} {W}">\n'
            '  <title>shipyard — a hull mid-build, and the next plank arriving lit</title>'
            f'{defs}{bg}{mid}{fg}{hl}\n</svg>\n')


if __name__ == "__main__":
    OUT.write_text(build())
    print(f"wrote {OUT}  ({OUT.stat().st_size / 1024:.1f} KB)")
