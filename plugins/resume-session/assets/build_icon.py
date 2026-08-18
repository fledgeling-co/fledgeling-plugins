#!/usr/bin/env python3
"""build_icon.py — the `resume-session` icon master and its two scored alternates.

Direction: Tahoe gel-glass, porcelain sub-register (a) — a warm porcelain cushion
carrying one dark object with a soft cast shadow. Runner-up was Direction 1
(Object Tile, Tahoe-softened); the cushion register won because five siblings
already share it and the shelf has to read as one family.

Device (take A, the master): "The Kept Place" — a closed bound ledger lying on the
cushion, seen in a mild oblique from above and in front, with a single vermilion
register ribbon slipping out from between the leaves at the fore-edge, folding
over the edge and lying flat on the tile. The signature move is that crossing:
the ribbon is the one thing that leaves a shut session, and it is the only
saturated element on the tile.

Every value below was measured rather than assumed:

  * the key light's bearing — the family's own ground is brightest at x0.08 y0.08
    on all six siblings sampled, so the key is upper-left and shadows fall
    down-right;
  * the graphite/porcelain relation — 7.7:1 to 9.5:1 on the Engine C raster,
    8.1:1 on apple-12 (Calculator), which is the whole reason this rebuild is
    dark-on-porcelain rather than pale-on-porcelain;
  * the page block is NOT ivory. Measured on the raster it is a warm tan at
    Y 0.397, hue 33, sat 0.31 — 1.43:1 against the ground it sits beside and
    4.98:1 against the boards that flank it. Authored near-white it dissolves,
    which is exactly how the predecessor lost half its composition;
  * the ribbon is deeper than it looks: Y 0.132-0.138 on the raster's lit faces,
    0.088 in the fold. A "vermilion" at the family's median accent luminance
    (0.24) measures 2.7:1 against this ground and fails rubric #7.

Takes B and C are real alternates, not strawmen: same cushion, same light model,
same accent, different device. Both are scored on the sheet and both lost.

Usage:  python3 build_icon.py            # write all three SVGs + the PNG exports
        python3 build_icon.py --svg-only
"""

from __future__ import annotations

import argparse
import colorsys
import math
import pathlib
import subprocess
import sys

ASSETS = pathlib.Path(__file__).resolve().parent
SQ_FILE = ASSETS.parents[1] / "create-mac-icon" / "assets" / "squircle-path.txt"
TILE = 1024

# ── Light model ───────────────────────────────────────────────────────────────
# One soft key from the upper left. KEY_BEARING is the direction the light
# TRAVELS across the tile, measured clockwise from +x; every gradient axis and
# every cast shadow in this file is derived from it, so the whole scene turns
# together if it changes.
KEY_BEARING_DEG = 48.0
KEY = (math.cos(math.radians(KEY_BEARING_DEG)), math.sin(math.radians(KEY_BEARING_DEG)))
# The same key as a world vector, for Lambert terms on the ledger's faces:
# +x runs along the spine (screen right), +y from spine to fore-edge (toward the
# viewer), +z up out of the tile.
KEY_WORLD = (-0.35, -0.46, 0.82)
AMBIENT = 0.16

# ── Cell geometry: the oblique projection the ledger is built in ──────────────
# P is the spine direction on screen; Q is spine -> fore-edge, foreshortened.
# The book lies with its spine along the far edge so the leaves and the ribbon
# face the viewer.
P_DEG = 6.5
Q_DEG = 64.0
Q_FORESHORTEN = 0.62
P_DIR = (math.cos(math.radians(P_DEG)), math.sin(math.radians(P_DEG)))
Q_DIR = (math.cos(math.radians(Q_DEG)) * Q_FORESHORTEN,
         math.sin(math.radians(Q_DEG)) * Q_FORESHORTEN)

BOOK_L = 452.0          # along the spine, head -> tail
BOOK_W = 436.0          # spine -> fore-edge
BOOK_T = 152.0          # total thickness, boards + block. A thin one reads as a
                        # mortarboard with the ribbon for a tassel; measured on a
                        # render at 512px, and no material work touches it.
SQUARE = 22.0           # the cover's overhang past the page block
BOARD_T = 34.0          # one board's thickness
SPINE_W = 42.0          # the spine's roll, measured in Q
HINGE_IN = 48.0         # the joint groove's distance from the far edge, in Q
CORNER_R = 28.0         # the casting's radius; the spine corners get 1.55x
SPINE_R_K = 1.55
LEAVES = 10             # leaf lines drawn on the page block

# The ribbon. RIB_W is what decides whether the accent exists at 16px:
# 104 / 64 = 1.63 display px, against the 1.5px floor this skill measured on
# better-goal. Arc length is free; the width is what is scarce.
RIB_W = 110.0
RIB_AT = 0.545          # where it leaves the fore-edge, as a fraction of BOOK_L
RIB_RUN = 215.0         # how far it lies across the tile, in Q
RIB_SKEW = 0.55         # and how far along the spine over that run: a ribbon that
                        # runs straight down the Q axis hangs; one that leans reads
                        # as lying on the tile
RIB_TAIL = 34.0         # the swallowtail's depth

CENTRE = (512.0, 492.0)  # the ink's optical centre: centred, lifted 20px

# ── Palette, as (hue°, saturation, target relative luminance) ─────────────────
# Solved to an exact sRGB hex by `tone()` so a luminance can be stated as a
# luminance. Ground and pages carry the tile's warm hue; the graphite is
# deliberately cool (kin to anvil-errand's, away from improve-skill's warm
# charcoal); the accent is the family's ember with this subject's own hue point.
GROUND_LIT = (36.0, 0.070, 0.845)
GROUND_DIM = (34.0, 0.165, 0.615)
VIGNETTE = (32.0, 0.52, 0.055)
RIM_LIGHT = (40.0, 0.030, 0.960)

GRAPHITE_HUE, GRAPHITE_SAT = 218.0, 0.14
COVER_LIT = (GRAPHITE_HUE, 0.12, 0.063)
COVER_DIM = (GRAPHITE_HUE, 0.18, 0.024)
FORE_LIT = (GRAPHITE_HUE, 0.15, 0.027)
FORE_DIM = (GRAPHITE_HUE, 0.19, 0.015)
HEAD_LIT = (GRAPHITE_HUE, 0.13, 0.049)   # the left face turns toward the key, so
HEAD_DIM = (GRAPHITE_HUE, 0.17, 0.026)   # it is the lighter of the two side faces
TAIL_LIT = (GRAPHITE_HUE, 0.17, 0.021)   # (kept: takes B and C use this ramp)
TAIL_DIM = (GRAPHITE_HUE, 0.20, 0.012)
SPINE_LIT = (214.0, 0.12, 0.060)
SPINE_DIM = (GRAPHITE_HUE, 0.17, 0.028)

PAGE_LIT = (34.0, 0.30, 0.395)
PAGE_DIM = (33.0, 0.37, 0.255)
PAGE_LINE = (32.0, 0.42, 0.165)
PAGE_LIP = (36.0, 0.20, 0.560)

ACCENT_HUE, ACCENT_SAT = 16.0, 0.82
# The accent's luminance is set by rubric #7, not by taste: at Y 0.205 the flat
# run measured 2.87:1 against this ground by the dilated-ring method and failed.
# The raster's own ribbon sits at Y 0.132; these land the run's median near 0.16,
# which is 3.5:1 against the ground and HSL L 0.44 — the family's shared accent
# lightness, so it does not read brown on the shelf beside its siblings.
RIB_FLAT_LIT = (ACCENT_HUE, ACCENT_SAT, 0.185)
RIB_FLAT_TIP = (ACCENT_HUE, ACCENT_SAT + 0.03, 0.135)
RIB_DRAPE_LIT = (ACCENT_HUE, ACCENT_SAT + 0.02, 0.112)
RIB_DRAPE_DIM = (ACCENT_HUE - 1.0, ACCENT_SAT + 0.06, 0.075)
RIB_ROLL = (26.0, 0.44, 0.520)   # the fold's rolled edge, in the scene's own
                                 # rim-scatter hue — never white
SHADOW = (28.0, 0.50, 0.030)
BOUNCE = (38.0, 0.15, 0.780)     # porcelain throwing light back up into the body


def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _relY(rgb) -> float:
    r, g, b = (_lin(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def tone(spec) -> str:
    """(hue°, sat, target relative luminance) -> sRGB hex, by bisection on value."""
    hue, sat, target = spec
    lo, hi = 0.0, 1.0
    for _ in range(46):
        mid = (lo + hi) / 2
        rgb = [c * 255 for c in colorsys.hsv_to_rgb(hue / 360.0, sat, mid)]
        if _relY(rgb) < target:
            lo = mid
        else:
            hi = mid
    rgb = [round(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, sat, (lo + hi) / 2)]
    return "#%02X%02X%02X" % tuple(max(0, min(255, c)) for c in rgb)


def lambert(normal, lit_spec, dim_spec):
    """Pick a face's ramp ends from its normal, so no face is lit by eye."""
    d = sum(n * k for n, k in zip(normal, KEY_WORLD))
    t = AMBIENT + (1 - AMBIENT) * max(0.0, d)
    lo, hi = dim_spec[2], lit_spec[2]
    y = lo + (hi - lo) * t
    return tone((lit_spec[0], lit_spec[1], y))


# ── Geometry helpers ─────────────────────────────────────────────────────────
_OFFSET = [0.0, 0.0]


def pt(u: float, v: float, z: float = 0.0):
    """World (along-spine, spine->fore-edge, up) -> screen, with the ink centred."""
    x = u * P_DIR[0] + v * Q_DIR[0] + _OFFSET[0]
    y = u * P_DIR[1] + v * Q_DIR[1] - z + _OFFSET[1]
    return (x, y)


def d(points, close=True) -> str:
    body = " L ".join(f"{x:.2f} {y:.2f}" for x, y in points)
    return f"M {body}" + (" Z" if close else "")


def rounded(points, r: float, radii=None) -> str:
    """Rounded polygon: each corner trimmed and closed with a tangent arc.

    The tangent length is r / tan(theta/2), not r. Trimming by the radius itself
    is correct only at a right angle: on this projection's 154-degree corners it
    put the trim points nearly two radii apart, so the "corner" rendered as a
    protruding half-disc off each of them — twice, on the silhouette, at 512px.
    """
    n = len(points)
    out = []
    for i in range(n):
        p0, p1, p2 = points[(i - 1) % n], points[i], points[(i + 1) % n]
        v0 = (p0[0] - p1[0], p0[1] - p1[1])
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        l0 = math.hypot(*v0) or 1.0
        l1 = math.hypot(*v1) or 1.0
        u0 = (v0[0] / l0, v0[1] / l0)
        u1 = (v1[0] / l1, v1[1] / l1)
        theta = math.acos(max(-1.0, min(1.0, u0[0] * u1[0] + u0[1] * u1[1])))
        want = radii[i] if radii else r
        if theta < 1e-3 or theta > math.pi - 1e-3:
            out.append((p1, p1, 0.0, 0))
            continue
        t = min(want / math.tan(theta / 2), 0.46 * l0, 0.46 * l1)
        rr = max(0.5, t * math.tan(theta / 2))
        a = (p1[0] + u0[0] * t, p1[1] + u0[1] * t)
        b = (p1[0] + u1[0] * t, p1[1] + u1[1] * t)
        cross = v0[0] * v1[1] - v0[1] * v1[0]
        sweep = 0 if cross > 0 else 1
        out.append((a, b, rr, sweep))
    segs = [f"M {out[0][1][0]:.2f} {out[0][1][1]:.2f}"]
    for i in range(1, n + 1):
        a, b, rr, sweep = out[i % n]
        segs.append(f"L {a[0]:.2f} {a[1]:.2f}")
        if rr > 0.5:
            segs.append(f"A {rr:.2f} {rr:.2f} 0 0 {sweep} {b[0]:.2f} {b[1]:.2f}")
    return " ".join(segs) + " Z"


def axis(frm, to) -> str:
    return (f'gradientUnits="userSpaceOnUse" x1="{frm[0]:.1f}" y1="{frm[1]:.1f}" '
            f'x2="{to[0]:.1f}" y2="{to[1]:.1f}"')


def key_axis(centre, span):
    """A gradient axis hung on the one key, through a point: lit end first."""
    return ((centre[0] - KEY[0] * span, centre[1] - KEY[1] * span),
            (centre[0] + KEY[0] * span, centre[1] + KEY[1] * span))


def squircle() -> str:
    if SQ_FILE.exists():
        text = SQ_FILE.read_text().strip()
        if text:
            return text
    raise SystemExit(f"missing the family squircle: {SQ_FILE}")


# ── The shared tile ──────────────────────────────────────────────────────────
def tile_defs() -> str:
    return f"""
    <radialGradient id="ground" gradientUnits="userSpaceOnUse"
        cx="{TILE*0.20:.0f}" cy="{TILE*0.16:.0f}" r="{TILE*1.02:.0f}">
      <stop offset="0" stop-color="{tone(GROUND_LIT)}"/>
      <stop offset="0.55" stop-color="{tone((GROUND_LIT[0], GROUND_LIT[1]+0.05, (GROUND_LIT[2]+GROUND_DIM[2])/2 + 0.045))}"/>
      <stop offset="1" stop-color="{tone(GROUND_DIM)}"/>
    </radialGradient>
    <radialGradient id="vignette" gradientUnits="userSpaceOnUse"
        cx="{TILE*0.44:.0f}" cy="{TILE*0.42:.0f}" r="{TILE*0.70:.0f}">
      <stop offset="0.58" stop-color="{tone(VIGNETTE)}" stop-opacity="0"/>
      <stop offset="1" stop-color="{tone(VIGNETTE)}" stop-opacity="0.155"/>
    </radialGradient>
    <radialGradient id="softShadow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{tone(SHADOW)}" stop-opacity="0.40"/>
      <stop offset="0.55" stop-color="{tone(SHADOW)}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{tone(SHADOW)}" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur18" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="blur34" x="-55%" y="-55%" width="210%" height="210%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <filter id="blur7" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <clipPath id="squircle"><path d="{squircle()}"/></clipPath>"""


def tile_bg() -> str:
    sq = squircle()
    return f"""  <g id="bg">
    <rect width="{TILE}" height="{TILE}" fill="url(#ground)"/>
    <rect width="{TILE}" height="{TILE}" fill="url(#vignette)"/>
    <path d="{sq}" fill="none" stroke="{tone(RIM_LIGHT)}" stroke-width="7" opacity="0.80"/>
  </g>"""


def wrap(defs: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TILE} {TILE}" '
            f'width="{TILE}" height="{TILE}">\n  <defs>{tile_defs()}{defs}\n  </defs>\n'
            f'  <g clip-path="url(#squircle)">\n{tile_bg()}\n{body}\n  </g>\n</svg>\n')


# ══════════════════════════════════════════════════════════════════════════════
# Take A — "The Kept Place": the master
# ══════════════════════════════════════════════════════════════════════════════
def centre_ink():
    """Solve the translation that puts the whole mark's bbox centre at CENTRE."""
    _OFFSET[0] = _OFFSET[1] = 0.0
    xs, ys = [], []
    for u, v, z in [(0, 0, BOOK_T), (BOOK_L, 0, BOOK_T), (BOOK_L, BOOK_W, BOOK_T),
                    (0, BOOK_W, BOOK_T), (0, BOOK_W, 0), (BOOK_L, BOOK_W, 0),
                    (0, 0, 0),
                    (BOOK_L * RIB_AT + RIB_SKEW * RIB_RUN - 16, BOOK_W + RIB_RUN, 0),
                    (BOOK_L * RIB_AT + RIB_W + RIB_SKEW * RIB_RUN + 8, BOOK_W + RIB_RUN, 0)]:
        x, y = pt(u, v, z)
        xs.append(x)
        ys.append(y)
    _OFFSET[0] = CENTRE[0] - (min(xs) + max(xs)) / 2
    _OFFSET[1] = CENTRE[1] - (min(ys) + max(ys)) / 2


def take_ledger() -> str:
    centre_ink()
    # Which side faces this projection actually reveals is a property of the axes,
    # not a choice: Q travels down-RIGHT, so the tile shows the top, the near
    # (fore-edge) face and the LEFT (head) face, and the tail face folds back onto
    # the cover. Painting the tail face instead left the head unpainted, and the
    # silhouette's own fill showed through it as a dark tab on the left.
    pz0, pz1 = BOARD_T, BOOK_T - BOARD_T
    bu0, bu1 = SQUARE, BOOK_L - SQUARE          # the block, recessed by the square
    bv = BOOK_W - SQUARE

    # ---- the casting: one convex hexagon so every visible edge shares a radius
    top = [pt(0, 0, BOOK_T), pt(BOOK_L, 0, BOOK_T),
           pt(BOOK_L, BOOK_W, BOOK_T), pt(0, BOOK_W, BOOK_T)]
    hull = [top[0], top[1], top[2], pt(BOOK_L, BOOK_W, 0),
            pt(0, BOOK_W, 0), pt(0, 0, 0)]
    hull_r = [CORNER_R * SPINE_R_K, CORNER_R * SPINE_R_K, CORNER_R,
              CORNER_R, CORNER_R, CORNER_R * SPINE_R_K]
    cover_top = rounded(top, CORNER_R,
                        [CORNER_R * SPINE_R_K, CORNER_R * SPINE_R_K, CORNER_R, CORNER_R])
    fore_face = d([pt(0, BOOK_W, BOOK_T), pt(BOOK_L, BOOK_W, BOOK_T),
                   pt(BOOK_L, BOOK_W, 0), pt(0, BOOK_W, 0)])
    head_face = d([pt(0, 0, BOOK_T), pt(0, BOOK_W, BOOK_T),
                   pt(0, BOOK_W, 0), pt(0, 0, 0)])

    # ---- the page block, set back behind the boards on both visible sides ------
    # Its outer profile bows inward: a real fore-edge is concave, and that bow is
    # most of what stops a dark cover over a pale band reading as an open laptop.
    def bow(a, b, k):
        mx, my = (a[0] + b[0]) / 2 - KEY[0] * k, (a[1] + b[1]) / 2 - KEY[1] * k
        return f"Q {mx:.2f} {my:.2f} {b[0]:.2f} {b[1]:.2f}"

    pa, pb = pt(bu0, bv, pz1), pt(bu1, bv, pz1)
    pc, pd = pt(bu1, bv, pz0), pt(bu0, bv, pz0)
    page_fore = (f"M {pa[0]:.2f} {pa[1]:.2f} {bow(pa, pb, 5.0)} "
                 f"L {pc[0]:.2f} {pc[1]:.2f} {bow(pc, pd, -5.0)} Z")
    ha, hb = pt(bu0, SPINE_W, pz1), pt(bu0, bv, pz1)
    hc, hd = pt(bu0, bv, pz0), pt(bu0, SPINE_W, pz0)
    page_head = d([ha, hb, hc, hd])

    leaf_fore, leaf_head = [], []
    for i in range(1, LEAVES + 1):
        z = pz0 + (pz1 - pz0) * i / (LEAVES + 1)
        a, b = pt(bu0 + 16, bv, z), pt(bu1 - 16, bv, z)
        leaf_fore.append(f'<path d="M {a[0]:.2f} {a[1]:.2f} {bow(a, b, 4.0)}" '
                         f'stroke="{tone(PAGE_LINE)}" stroke-width="2.4" '
                         f'opacity="{0.22 + 0.20 * (i % 2):.2f}" fill="none"/>')
        a, b = pt(bu0, SPINE_W + 12, z), pt(bu0, bv - 12, z)
        leaf_head.append(f'<path d="{d([a, b], close=False)}" stroke="{tone(PAGE_LINE)}" '
                         f'stroke-width="2.2" opacity="{0.16 + 0.16 * (i % 2):.2f}" fill="none"/>')

    # ---- the spine: its roll, its joint groove, three raised bands ------------
    spine_band = d([pt(0, 0, BOOK_T), pt(BOOK_L, 0, BOOK_T),
                    pt(BOOK_L, SPINE_W, BOOK_T), pt(0, SPINE_W, BOOK_T)])
    hinge = d([pt(24, HINGE_IN, BOOK_T), pt(BOOK_L - 24, HINGE_IN, BOOK_T)], close=False)
    bands = []
    for frac in (0.235, 0.5, 0.765):
        u = BOOK_L * frac
        bands.append(
            f'<path d="{d([pt(u - 14, -2, BOOK_T), pt(u + 14, -2, BOOK_T), pt(u + 14, SPINE_W + 13, BOOK_T), pt(u - 14, SPINE_W + 13, BOOK_T)])}" '
            f'fill="url(#spineBand)" opacity="0.80"/>')

    # ---- the ribbon ----------------------------------------------------------
    u0, u1 = BOOK_L * RIB_AT, BOOK_L * RIB_AT + RIB_W
    root_z = pz0 + (pz1 - pz0) * 0.44          # it comes out from between leaves
    fold_z = -5.0                              # just below the bottom board
    drape = d([pt(u0, bv, root_z), pt(u1, bv, root_z),
               pt(u1, BOOK_W, fold_z), pt(u0, BOOK_W, fold_z)])
    lean = RIB_SKEW * RIB_RUN
    f0, f1 = pt(u0, BOOK_W, fold_z), pt(u1, BOOK_W, fold_z)
    t0 = pt(u0 + lean - 16, BOOK_W + RIB_RUN, 0)
    t1 = pt(u1 + lean + 8, BOOK_W + RIB_RUN, 0)
    m0 = pt(u0 + lean * 0.46 + 6, BOOK_W + RIB_RUN * 0.50, 0)
    m1 = pt(u1 + lean * 0.46 + 34, BOOK_W + RIB_RUN * 0.50, 0)
    notch = pt((u0 + u1) / 2 + lean, BOOK_W + RIB_RUN - RIB_TAIL, 0)
    flat = (f"M {f0[0]:.2f} {f0[1]:.2f} L {f1[0]:.2f} {f1[1]:.2f} "
            f"C {m1[0]:.2f} {m1[1]:.2f} {t1[0]+8:.2f} {t1[1]-16:.2f} {t1[0]:.2f} {t1[1]:.2f} "
            f"L {notch[0]:.2f} {notch[1]:.2f} L {t0[0]:.2f} {t0[1]:.2f} "
            f"C {t0[0]-6:.2f} {t0[1]-16:.2f} {m0[0]:.2f} {m0[1]:.2f} {f0[0]:.2f} {f0[1]:.2f} Z")
    fold_edge = d([pt(u0 + 18, BOOK_W, fold_z), pt(u1 - 18, BOOK_W, fold_z)], close=False)
    slot = d([pt(u0 - 4, bv, root_z + 13), pt(u1 + 4, bv, root_z + 13),
              pt(u1 + 4, bv, root_z - 4), pt(u0 - 4, bv, root_z - 4)])

    # ---- shadows -------------------------------------------------------------
    foot = [pt(0, 0, 0), pt(BOOK_L, 0, 0), pt(BOOK_L, BOOK_W, 0), pt(0, BOOK_W, 0)]

    def shifted(pts, k):
        return [(x + KEY[0] * k, y + KEY[1] * k) for x, y in pts]
    tight = rounded(shifted(foot, 15), CORNER_R)
    wide = rounded(shifted(foot, 52), CORNER_R * 1.6)
    rib_shadow = (f"M {f0[0]-9:.2f} {f0[1]+7:.2f} L {f1[0]+7:.2f} {f1[1]+9:.2f} "
                  f"L {t1[0]+11:.2f} {t1[1]+13:.2f} L {t0[0]-7:.2f} {t0[1]+15:.2f} Z")

    # ---- gradients -----------------------------------------------------------
    a_top = key_axis(pt(BOOK_L / 2, BOOK_W / 2, BOOK_T), 320)
    a_fore = key_axis(pt(BOOK_L / 2, BOOK_W, BOOK_T / 2), 290)
    a_head = key_axis(pt(0, BOOK_W / 2, BOOK_T / 2), 220)
    a_spine = key_axis(pt(BOOK_L / 2, SPINE_W / 2, BOOK_T), 290)
    ribc = ((f0[0] + t1[0]) / 2, (f0[1] + t1[1]) / 2)
    a_rib = key_axis(ribc, 225)

    defs = f"""
    <clipPath id="castingClip"><path d="{rounded(hull, CORNER_R, hull_r)}"/></clipPath>
    <clipPath id="coverClip"><path d="{cover_top}"/></clipPath>
    <radialGradient id="coverBloom" gradientUnits="userSpaceOnUse"
        cx="{pt(BOOK_L*0.34, BOOK_W*0.30, BOOK_T)[0]:.1f}"
        cy="{pt(BOOK_L*0.34, BOOK_W*0.30, BOOK_T)[1]:.1f}" r="{BOOK_L*0.72:.0f}">
      <stop offset="0" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0.085"/>
      <stop offset="0.55" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0.030"/>
      <stop offset="1" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="coverTop" {axis(*a_top)}>
      <stop offset="0" stop-color="{lambert((0,0,1), COVER_LIT, COVER_DIM)}"/>
      <stop offset="1" stop-color="{tone(COVER_DIM)}"/>
    </linearGradient>
    <linearGradient id="foreFace" {axis(*a_fore)}>
      <stop offset="0" stop-color="{lambert((0,1,0), FORE_LIT, FORE_DIM)}"/>
      <stop offset="1" stop-color="{tone(FORE_DIM)}"/>
    </linearGradient>
    <linearGradient id="headFace" {axis(*a_head)}>
      <stop offset="0" stop-color="{lambert((-1,0,0), HEAD_LIT, HEAD_DIM)}"/>
      <stop offset="1" stop-color="{tone(HEAD_DIM)}"/>
    </linearGradient>
    <linearGradient id="spineTop" {axis(*a_spine)}>
      <stop offset="0" stop-color="{tone(SPINE_LIT)}"/>
      <stop offset="1" stop-color="{tone(SPINE_DIM)}"/>
    </linearGradient>
    <linearGradient id="spineBand" {axis(*a_spine)}>
      <stop offset="0" stop-color="{tone((SPINE_LIT[0], SPINE_LIT[1], SPINE_LIT[2]*1.30))}"/>
      <stop offset="1" stop-color="{tone((SPINE_DIM[0], SPINE_DIM[1], SPINE_DIM[2]*0.82))}"/>
    </linearGradient>
    <linearGradient id="pageFore" {axis(*a_fore)}>
      <stop offset="0" stop-color="{tone(PAGE_LIT)}"/>
      <stop offset="1" stop-color="{tone(PAGE_DIM)}"/>
    </linearGradient>
    <linearGradient id="pageHead" {axis(*a_head)}>
      <stop offset="0" stop-color="{tone((PAGE_LIT[0], PAGE_LIT[1] + 0.03, PAGE_LIT[2]*0.90))}"/>
      <stop offset="1" stop-color="{tone((PAGE_DIM[0], PAGE_DIM[1] + 0.02, PAGE_DIM[2]*0.86))}"/>
    </linearGradient>
    <linearGradient id="ribFlat" {axis(*a_rib)}>
      <stop offset="0" stop-color="{tone(RIB_FLAT_LIT)}"/>
      <stop offset="1" stop-color="{tone(RIB_FLAT_TIP)}"/>
    </linearGradient>
    <linearGradient id="ribDrape" gradientUnits="userSpaceOnUse"
        x1="0" y1="{pt(u0, bv, root_z)[1]:.1f}" x2="0" y2="{pt(u0, BOOK_W, fold_z)[1]:.1f}">
      <stop offset="0" stop-color="{tone(RIB_DRAPE_DIM)}"/>
      <stop offset="1" stop-color="{tone(RIB_DRAPE_LIT)}"/>
    </linearGradient>
    <linearGradient id="bounceFore" gradientUnits="userSpaceOnUse"
        x1="0" y1="{pt(0, BOOK_W, 0)[1]:.1f}" x2="0" y2="{pt(0, BOOK_W, BOOK_T*0.58)[1]:.1f}">
      <stop offset="0" stop-color="{tone(BOUNCE)}" stop-opacity="0.24"/>
      <stop offset="1" stop-color="{tone(BOUNCE)}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rimCatch" {axis(*a_top)}>
      <stop offset="0" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0.16"/>
      <stop offset="0.34" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0.10"/>
      <stop offset="0.70" stop-color="{tone(RIM_LIGHT)}" stop-opacity="0"/>
    </linearGradient>"""

    body = f"""  <g id="mid">
    <path d="{wide}" fill="url(#softShadow)" filter="url(#blur34)" opacity="0.72"/>
    <path d="{tight}" fill="{tone(SHADOW)}" opacity="0.32" filter="url(#blur18)"/>
    <path d="{rib_shadow}" fill="{tone(SHADOW)}" opacity="0.22" filter="url(#blur7)"/>
    <!-- Every face is clipped to the one rounded silhouette. Without it each sharp
         quad's corner pokes past the casting's radius: the head face's top corner
         rendered as a horn off the spine, visible at 1024 and nowhere else. -->
    <g clip-path="url(#castingClip)">
    <path d="{rounded(hull, CORNER_R, hull_r)}" fill="url(#foreFace)"/>
    <path d="{head_face}" fill="url(#headFace)"/>
    <path d="{page_head}" fill="url(#pageHead)"/>
    {chr(10).join('    ' + s for s in leaf_head)}
    <path d="{d([ha, hb], close=False)}" stroke="{tone(SHADOW)}" stroke-width="12"
          opacity="0.38" fill="none" filter="url(#blur7)"/>
    <path d="{fore_face}" fill="url(#foreFace)"/>
    <path d="{page_fore}" fill="url(#pageFore)"/>
    {chr(10).join('    ' + s for s in leaf_fore)}
    <path d="M {pa[0]:.2f} {pa[1]:.2f} {bow(pa, pb, 5.0)}" stroke="{tone(SHADOW)}"
          stroke-width="14" opacity="0.44" fill="none" filter="url(#blur7)"/>
    <path d="M {pd[0]:.2f} {pd[1]:.2f} {bow(pd, pc, -5.0)}" stroke="{tone(PAGE_LIP)}"
          stroke-width="3" opacity="0.28" fill="none"/>
    <path d="{fore_face}" fill="url(#bounceFore)"/>
    <path d="{cover_top}" fill="url(#coverTop)"/>
    <g clip-path="url(#coverClip)">
      <path d="{cover_top}" fill="url(#coverBloom)"/>
      <path d="{spine_band}" fill="url(#spineTop)" opacity="0.30"/>
      {chr(10).join('      ' + s for s in bands)}
      <path d="{hinge}" stroke="{tone((GRAPHITE_HUE, 0.22, 0.010))}" stroke-width="5"
            opacity="0.66" fill="none"/>
      <path d="{hinge}" stroke="{tone(RIM_LIGHT)}" stroke-width="2" opacity="0.09"
            fill="none" transform="translate(-2.2,-3.0)"/>
    </g>
    </g>
  </g>
  <g id="fg">
    <path d="{slot}" fill="{tone((ACCENT_HUE, 0.34, 0.020))}" opacity="0.90"/>
    <path d="{flat}" fill="url(#ribFlat)"/>
    <path d="{drape}" fill="url(#ribDrape)"/>
  </g>
  <g id="highlight">
    <path d="{cover_top}" fill="none" stroke="url(#rimCatch)" stroke-width="2.2"
          clip-path="url(#castingClip)"/>
    <path d="{fold_edge}" stroke="{tone(RIB_ROLL)}" stroke-width="4.2" opacity="0.44"
          fill="none" stroke-linecap="round"/>
    <path d="{d([pt(u0 + 14, BOOK_W + 26, 0), pt(u0 + lean * 0.80 + 2, BOOK_W + RIB_RUN * 0.80, 0)], close=False)}"
          stroke="{tone(RIB_ROLL)}" stroke-width="3.6" opacity="0.22" fill="none"
          stroke-linecap="round"/>
  </g>"""
    return wrap(defs, body)


# ══════════════════════════════════════════════════════════════════════════════
# Take B — "The Dovetail Key": a graphite board split, the break bridged
# ══════════════════════════════════════════════════════════════════════════════
def take_key() -> str:
    L, R, T, B, TH = 206.0, 818.0, 322.0, 654.0, 74.0
    board = [(L, T), (R, T), (R, B), (L, B)]
    face = [(L, B), (R, B), (R, B + TH), (L, B + TH)]
    split_x = (L + R) * 0.505
    # the split: a jagged porcelain-filled parting, top edge to bottom edge
    jag = [0.0, 22.0, -16.0, 26.0, -10.0, 18.0, -20.0, 14.0]
    left, right = [], []
    for i, dx in enumerate(jag):
        y = T + (B + TH - T) * i / (len(jag) - 1)
        left.append((split_x + dx - 9, y))
        right.append((split_x + dx + 9, y))
    crack = d(left + list(reversed(right)))
    kx, ky, kw, kh, waist = split_x, (T + B) / 2, 318.0, 224.0, 106.0
    key = [(kx - kw / 2, ky - kh / 2), (kx - waist / 2, ky - kh * 0.15),
           (kx - waist / 2, ky + kh * 0.15), (kx - kw / 2, ky + kh / 2),
           (kx + kw / 2, ky + kh / 2), (kx + waist / 2, ky + kh * 0.15),
           (kx + waist / 2, ky - kh * 0.15), (kx + kw / 2, ky - kh / 2)]
    a_board = key_axis(((L + R) / 2, (T + B) / 2), 420)
    a_key = key_axis((kx, ky), 220)
    defs = f"""
    <linearGradient id="kBoard" {axis(*a_board)}>
      <stop offset="0" stop-color="{lambert((0,0,1), COVER_LIT, COVER_DIM)}"/>
      <stop offset="1" stop-color="{tone(COVER_DIM)}"/>
    </linearGradient>
    <linearGradient id="kFace" {axis(*a_board)}>
      <stop offset="0" stop-color="{tone(FORE_LIT)}"/>
      <stop offset="1" stop-color="{tone(FORE_DIM)}"/>
    </linearGradient>
    <linearGradient id="kKey" {axis(*a_key)}>
      <stop offset="0" stop-color="{tone(RIB_FLAT_LIT)}"/>
      <stop offset="1" stop-color="{tone(RIB_DRAPE_DIM)}"/>
    </linearGradient>"""
    body = f"""  <g id="mid">
    <path d="{rounded([(x + KEY[0]*46, y + KEY[1]*46) for x, y in face], 40)}"
          fill="url(#softShadow)" filter="url(#blur34)" opacity="0.60"/>
    <path d="{rounded(face, 26)}" fill="url(#kFace)"/>
    <path d="{rounded(board, 30)}" fill="url(#kBoard)"/>
    <path d="{crack}" fill="{tone(GROUND_DIM)}" opacity="0.92"/>
    <path d="{crack}" fill="none" stroke="{tone((GRAPHITE_HUE,0.24,0.008))}" stroke-width="4" opacity="0.55"/>
  </g>
  <g id="fg">
    <path d="{rounded(key, 12)}" fill="url(#kKey)"/>
    <path d="{rounded(key, 12)}" fill="none" stroke="{tone((ACCENT_HUE,0.55,0.055))}"
          stroke-width="4" opacity="0.55"/>
  </g>
  <g id="highlight">
    <path d="{rounded(board, 30)}" fill="none" stroke="url(#rimCatch)" stroke-width="4"/>
    <path d="{d([(kx - kw/2 + 22, ky - kh/2 + 9), (kx - waist/2 - 4, ky - kh*0.15 + 6)], close=False)}"
          stroke="{tone(RIB_ROLL)}" stroke-width="5" opacity="0.42" fill="none" stroke-linecap="round"/>
  </g>"""
    return wrap(defs, body)


# ══════════════════════════════════════════════════════════════════════════════
# Take C — "The Handed Baton": the carried object, half out of its cradle
# ══════════════════════════════════════════════════════════════════════════════
def take_baton() -> str:
    ang = -25.0
    cx, cy, ln, th = 512.0, 486.0, 528.0, 128.0
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    x1, y1 = cx - dx * ln / 2, cy - dy * ln / 2
    x2, y2 = cx + dx * ln / 2, cy + dy * ln / 2
    a_bat = key_axis((cx, cy), 210)
    a_col = key_axis((cx, cy), 110)
    chock = rounded([(x2 - 118, y2 + 46), (x2 + 34, y2 + 46),
                     (x2 + 34, y2 + 146), (x2 - 118, y2 + 146)], 22)
    defs = f"""
    <linearGradient id="bBody" {axis(*a_bat)}>
      <stop offset="0" stop-color="{lambert((0,0,1), COVER_LIT, COVER_DIM)}"/>
      <stop offset="1" stop-color="{tone(TAIL_DIM)}"/>
    </linearGradient>
    <linearGradient id="bCollar" {axis(*a_col)}>
      <stop offset="0" stop-color="{tone(RIB_FLAT_LIT)}"/>
      <stop offset="1" stop-color="{tone(RIB_DRAPE_DIM)}"/>
    </linearGradient>
    <linearGradient id="bCradle" {axis(*a_col)}>
      <stop offset="0" stop-color="{tone(FORE_LIT)}"/>
      <stop offset="1" stop-color="{tone(TAIL_DIM)}"/>
    </linearGradient>"""
    body = f"""  <g id="mid">
    <ellipse cx="{cx + KEY[0]*46:.0f}" cy="{cy + KEY[1]*66 + 108:.0f}" rx="248" ry="58"
             fill="url(#softShadow)" filter="url(#blur34)" opacity="0.70"/>
    <path d="{chock}" fill="url(#bCradle)"/>
  </g>
  <g id="fg">
    <path d="{d([(x1,y1),(x2,y2)], close=False)}" stroke="url(#bBody)" stroke-width="{th}"
          stroke-linecap="round" fill="none"/>
    <path d="{d([(cx - dx*74, cy - dy*74), (cx + dx*74, cy + dy*74)], close=False)}"
          stroke="url(#bCollar)" stroke-width="{th + 6}" fill="none"/>
  </g>
  <g id="highlight">
    <path d="{d([(x1 + dx*40 - dy*40, y1 + dy*40 + dx*40), (x2 - dx*40 - dy*40, y2 - dy*40 + dx*40)], close=False)}"
          stroke="url(#rimCatch)" stroke-width="6" fill="none" stroke-linecap="round"/>
  </g>"""
    return wrap(defs, body)


TAKES = {"icon.svg": take_ledger,
         "icon-alt-key.svg": take_key,
         "icon-alt-baton.svg": take_baton}
EXPORTS = [(1024, "icon.png"), (256, "icon-256.png"), (128, "icon-128.png"),
           (64, "icon-64.png"), (32, "icon-32.png"), (16, "icon-16.png")]


# ══════════════════════════════════════════════════════════════════════════════
# The banner, generated from the same constants as the icon
# ══════════════════════════════════════════════════════════════════════════════
# The family ships 3200x1040, which is this 1600x520 layout at deviceScaleFactor
# 2. Every colour, angle and proportion below is read out of the constants above
# rather than sampled off a sibling's banner, so an icon change carries into the
# banner by rebuilding rather than by remembering.
BANNER_W, BANNER_H = 1600, 520
BANNER_FONT = "Instrument Sans"          # the set's plurality wordmark face
BANNER_WEIGHT = 600
ICON_BOX = 300                            # the icon's displayed size
DETAIL_H = 172.0                          # the fore-edge crop's total height
DETAIL_W = 396.0                          # and its width, clear of the wordmark

WORDMARK = ("resume", "-", "session")
ESSENCE_HEAD = "Reads the session that stopped, from any coding CLI, and hands the next model"
ESSENCE_TAIL = "what it needs to carry on."


def _data_uri(path: pathlib.Path) -> str:
    import base64
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def banner_src() -> str:
    """Emit banner-src.html. The artwork is inlined because the rendering engine
    does not fetch file:// subresources from a file:// page and reports no error
    when it fails, so a referenced icon renders as an empty box that still passes
    every size assertion."""
    icon_png = ASSETS / "icon.png"
    if not icon_png.exists():
        raise SystemExit("render icon.png before the banner: it is inlined into the source")

    # The icon's own light: the shadow is offset along KEY, at the same bearing
    # the tile's faces and cast shadows use.
    sh_dx, sh_dy = KEY[0] * 17, KEY[1] * 17
    ink = tone((GRAPHITE_HUE, 0.14, 0.028))          # wordmark, a step under the cover
    muted = tone((GRAPHITE_HUE, 0.10, 0.165))        # the essence line
    accent = tone(RIB_FLAT_LIT)                      # the ribbon's own lit face

    # The device on the right is a magnified crop of the icon's own fore-edge, in
    # elevation: horizontally along the spine, vertically through the thickness.
    # Board, page block with its leaves, board, and the ribbon crossing them as a
    # vertical band of exactly its own width. Every dimension is the icon's, scaled
    # by DETAIL_H / BOOK_T. The first draft drew graded strata with an accent rail
    # through them, which is better-goal's banner almost exactly — a banner that
    # quotes a sibling is the drift the family sheet exists to catch.
    k = DETAIL_H / BOOK_T
    board_h = BOARD_T * k
    block_h = (BOOK_T - 2 * BOARD_T) * k
    top_y = round(BANNER_H / 2 - DETAIL_H / 2, 1)
    leaves = []
    for i in range(1, LEAVES + 1):
        y = round(top_y + board_h + block_h * i / (LEAVES + 1), 1)
        frac = (0.94, 0.72, 1.00, 0.80, 0.90, 0.68, 0.98, 0.76, 0.86, 0.74)[i % 10]
        leaves.append(f'<div class="leaf" style="top:{y}px;left:{(1 - frac) * 150:.0f}px;'
                      f'opacity:{0.26 + 0.22 * (i % 2):.2f}"></div>')
    rib_w = RIB_W * k
    rib_top = round(top_y + board_h + block_h * 0.40, 1)
    rib_h = round(DETAIL_H - board_h - block_h * 0.40 + 74, 1)
    rib_left = round(DETAIL_W * 0.46, 1)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={BANNER_FONT.replace(' ', '+')}:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; box-sizing: border-box; }}

  /* The ground is the icon's own cushion: the same two stops, the same key. */
  body {{
    width: {BANNER_W}px;
    height: {BANNER_H}px;
    overflow: hidden;
    position: relative;
    background:
      radial-gradient(120% 220% at 13% 10%,
        {tone(GROUND_LIT)} 0%,
        {tone((GROUND_LIT[0], GROUND_LIT[1] + 0.05, (GROUND_LIT[2] + GROUND_DIM[2]) / 2 + 0.045))} 52%,
        {tone(GROUND_DIM)} 100%);
    font-family: "{BANNER_FONT}", ui-sans-serif, system-ui, sans-serif;
    color: {ink};
  }}

  .lockup {{
    position: absolute;
    left: 92px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    gap: 60px;
    z-index: 2;
  }}

  .icon {{
    width: {ICON_BOX}px;
    height: {ICON_BOX}px;
    filter: drop-shadow({sh_dx:.0f}px {sh_dy:.0f}px 34px rgba(62, 45, 31, 0.26));
  }}

  .wordmark {{
    font-size: 88px;
    font-weight: {BANNER_WEIGHT};
    letter-spacing: -0.028em;
    line-height: 1.02;
    white-space: nowrap;
  }}

  .wordmark .hyphen {{ color: {accent}; }}

  .essence {{
    margin-top: 18px;
    max-width: 640px;
    font-size: 25px;
    font-weight: 400;
    line-height: 1.42;
    color: {muted};
  }}

  .essence b {{ color: {ink}; font-weight: 500; }}

  /* The fore-edge crop. It fades out into the ground on both sides rather than
     being cut by the frame. */
  .detail {{
    position: absolute;
    left: {BANNER_W - DETAIL_W - 26}px;
    top: 0;
    width: {DETAIL_W}px;
    height: {BANNER_H}px;
    opacity: 0.92;
    mask-image: linear-gradient(to right, rgba(0,0,0,0) 0%, #000 24%, #000 66%, rgba(0,0,0,0) 100%);
    -webkit-mask-image: linear-gradient(to right, rgba(0,0,0,0) 0%, #000 24%, #000 66%, rgba(0,0,0,0) 100%);
  }}

  .board, .block, .leaf, .ribbon {{ position: absolute; }}

  .board {{
    left: 0;
    width: {DETAIL_W}px;
    height: {board_h:.1f}px;
    background: linear-gradient(to bottom, {tone(FORE_LIT)}, {tone(FORE_DIM)});
  }}

  .block {{
    left: 0;
    width: {DETAIL_W}px;
    top: {top_y + board_h:.1f}px;
    height: {block_h:.1f}px;
    background: linear-gradient(to bottom, {tone(PAGE_LIT)}, {tone(PAGE_DIM)});
  }}

  .leaf {{
    width: {DETAIL_W}px;
    height: 3px;
    border-radius: 1.5px;
    background: {tone(PAGE_LINE)};
  }}

  .ribbon {{
    left: {rib_left}px;
    top: {rib_top}px;
    width: {rib_w:.1f}px;
    height: {rib_h}px;
    background: linear-gradient(to bottom, {tone(RIB_DRAPE_DIM)} 0%, {tone(RIB_DRAPE_LIT)} 46%, {accent} 62%, {tone(RIB_FLAT_TIP)} 100%);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 50% {100 - RIB_TAIL / RIB_W * 100 * 0.62:.0f}%, 0 100%);
  }}
</style>
</head>
<body>
  <div class="detail">
    <div class="board" style="top:{top_y}px"></div>
    <div class="block"></div>
{chr(10).join('    ' + l for l in leaves)}
    <div class="board" style="top:{top_y + board_h + block_h:.1f}px"></div>
    <div class="ribbon"></div>
  </div>

  <div class="lockup">
    <img class="icon" src="{_data_uri(icon_png)}" alt="resume-session icon">
    <div>
      <div class="wordmark">{WORDMARK[0]}<span class="hyphen">{WORDMARK[1]}</span>{WORDMARK[2]}</div>
      <div class="essence">{ESSENCE_HEAD} <b>{ESSENCE_TAIL}</b></div>
    </div>
  </div>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--svg-only", action="store_true")
    ap.add_argument("--banner-only", action="store_true")
    args = ap.parse_args()

    if not args.banner_only:
        for name, fn in TAKES.items():
            (ASSETS / name).write_text(fn(), encoding="utf-8")
            print(f"wrote {name}")
        if args.svg_only:
            return 0
        master = ASSETS / "icon.svg"
        for dim, out in EXPORTS:
            subprocess.run(["rsvg-convert", "-w", str(dim), "-h", str(dim),
                            str(master), "-o", str(ASSETS / out)], check=True)
            print(f"rendered {out} ({dim}px)")

    (ASSETS / "banner-src.html").write_text(banner_src(), encoding="utf-8")
    print("wrote banner-src.html (icon inlined as a data URI)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
