#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the create-mac-icon icon.

Direction "The Cast": Tahoe gel-glass sub-register (a), porcelain + gel object,
crossed with device bank #16 (the icon performs the verb), #17 (tile-as-machine
with a diegetic aperture), #5 (dual-function primitive) and #21 (authored overlap).

The subject is a skill that produces mac app icons, so the icon produces one on
camera: a vermilion gel tile has just been lifted out of an open plaster mould,
and the cavity it came from is still open beside it, empty except for the warmth
it kept. Solid and void, the same shape twice.

The signature move is that both the cast tile and the mould cavity are the SET'S
OWN SUPERELLIPSE - the exact path in squircle-path.txt that masks every icon in
this marketplace - so the artwork literally contains the thing it makes, at two
removes: the outer mask, the cavity, the cast. One curve, three scales.

Geometry is authored in the mould's own plate frame (u along one ground axis, v
along the other) and mapped to the canvas by a single dimetric matrix, so the
mould, the cavity and the cast tile cannot drift out of register with each other.
Extrusion is a pure screen-vertical sweep of that frame, so the solids cannot
drift either. Every constant below is named; a fidelity round is a parameter
edit, never path surgery.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import pathlib
import re

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- the set's curve

def _cubic(p0, p1, p2, p3, n):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def parse_path(d):
    """Flatten the marketplace squircle (M + a chain of absolute C) to a polyline."""
    toks = re.findall(r"[MCZz]|-?\d+(?:\.\d+)?", d)
    pts, cur, i = [], (0.0, 0.0), 0
    while i < len(toks):
        t = toks[i]
        if t == "M":
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            pts.append(cur)
            i += 3
        elif t == "C":
            p1 = (float(toks[i + 1]), float(toks[i + 2]))
            p2 = (float(toks[i + 3]), float(toks[i + 4]))
            p3 = (float(toks[i + 5]), float(toks[i + 6]))
            pts += _cubic(cur, p1, p2, p3, 2)
            cur = p3
            i += 7
        else:
            i += 1
    return pts


def _simplify(pts, tol):
    """Douglas-Peucker, so the shape stays exact where it curves and cheap where it doesn't."""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    den = math.hypot(dx, dy) or 1.0
    worst, idx = 0.0, 0
    for k in range(1, len(pts) - 1):
        p = pts[k]
        d = abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / den
        if d > worst:
            worst, idx = d, k
    if worst <= tol:
        return [a, b]
    return _simplify(pts[:idx + 1], tol)[:-1] + _simplify(pts[idx:], tol)


_raw = parse_path(SQUIRCLE)
_norm = [((x - 512.0) / 512.0, (y - 512.0) / 512.0) for x, y in _raw]
if math.dist(_norm[0], _norm[-1]) < 1e-6:
    _norm = _norm[:-1]
# Douglas-Peucker degenerates on a closed loop (its two endpoints coincide), so
# simplify the curve in four open arcs and stitch them back into the ring.
_q = len(_norm) // 4
UNIT = []
for k in range(4):
    seg = _norm[k * _q: (k + 1) * _q + 1] if k < 3 else _norm[3 * _q:] + [_norm[0]]
    UNIT += _simplify(seg, 0.0011)[:-1]

# ---------------------------------------------------------------- the plate frame
# dimetric: a plate point (u,v) lands on the canvas at
#   x = CX + (u - v) * KX ,  y = CY + (u + v) * KY
KX = 1.00
KY = 0.5150                                   # foreshortening of the ground plane

CX, CY = 512.0, 545.0                         # mould centre on the canvas

R_MOULD = 190.0                               # mould block half-extent, plate units
R_CAV = 128.0                                 # cavity half-extent  == the cast tile
MOULD_H = 78.0                                # block height, screen px
CAV_D = 56.0                                  # cavity depth, screen px
TILE_H = 84.0                                 # cast tile thickness, screen px

LIFT = 128.0                                  # how far the cast has risen, screen px
SLIDE = 118.0                                 # and how far it slid along -u, plate units

# Arris fillets, measured off the reference rather than assumed. Nothing on
# either object is a cut edge there; every convex arris is a rolled fillet, and
# the roll is wide enough to be a surface rather than a stroke:
#   block, top face -> front wall   L 0.950 holds to the arris, then rolls
#                                   monotonically to the wall's 0.680 over 26px
#                                   (midpoint 0.815 about 11px below the arris);
#   gel,   face -> side wall        0.518 -> 0.302 over 21-27px, and NO bright
#                                   line anywhere on the wall side of it;
#   gel crest                       sits on the FACE side instead, +0.09 over
#                                   the face at the lit left corner and gone by
#                                   the right one - a wrap highlight on the
#                                   shoulder, not a seam on the wall.
# These are stroke widths, centred on the arris, so half of each lies on the
# turned face; the blur (sigma 7) carries the roll out to the measured width.
FILLET_BLOCK = 26.0
FILLET_GEL = 22.0
FILLET_LIP = 16.0                             # bounded on purpose - see icon-notes.md

# Rim scatter on the cast. Binning the reference by depth inside each object's
# own silhouette says the gel is LIGHTER and LESS SATURATED at its rim than in
# its body, and says it in all four quadrants at once:
#   gel      dL +0.075 / +0.085 / +0.121 / +0.090  (NW/NE/SW/SE, d3 -> d34)
#            dS -0.084 / -0.108 / -0.171 / -0.135     mean +0.093 / -0.125
#   plaster  dL +0.011 (far top edge) against +0.128 (near bottom roll)
# The plaster's rim lift is directional, so it is the key light rolling over an
# arris. The gel's is not, so it cannot be: an omnidirectional edge lift is the
# short optical path through a translucent body at grazing angles. Same light,
# two materials, and only the translucent one carries a rim. The master had
# 44% of it (mean dL +0.041) and only where the shoulder highlight happened to
# sit, so the effect read as a lit top rather than as a material property.
RIM_SCATTER = 17.0                            # stroke half-width; under bM
                                              # (sigma 14) this decays to zero
                                              # ~40px in, the measured ramp
RIM_SCATTER_A = 0.26
# Scatter needs light behind the edge. The reference's cast has open, lit
# porcelain all the way round its rim, so it shows the effect at full strength
# everywhere and says nothing about the case where a rim overhangs its own cast
# shadow - which is exactly where this master's lower-left rim sits. Run at full
# strength there and the cast's lower-left boundary falls to 1.05:1 against the
# shadow it is standing in (2.4x worse than the reference's own 1.58:1 on that
# octant), which is prior learning #3 on a live figure-ground boundary. So the
# wash is attenuated where the cast overhangs the block's top face.
RIM_SHADED = 0.15                             # what survives over the mouth

TILE_CX = CX - SLIDE * KX
TILE_CY = CY - SLIDE * KY - LIFT

# light: one soft source, up and to the left
SHADOW_DX, SHADOW_DY = 26.0, 34.0
# where the cast's near shadow lands on the mould, named once so the shadow and
# the mask that has to agree with it cannot drift apart
CAST_NEAR = (SHADOW_DX * 0.6, SHADOW_DY * 0.5 + LIFT * 0.34)
KEY_OCCLUSION = 0.88                          # how much of the key the cast eats


def project(pts, cx, cy, s):
    return [(cx + (u - v) * s * KX, cy + (u + v) * s * KY) for u, v in pts]


def outline(cx, cy, r):
    return project(UNIT, cx, cy, r)


def d(pts, close=True):
    body = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return body + ("Z" if close else "")


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def chains(pts):
    """Split a convex outline at its leftmost and rightmost points into the
    upper chain (left to right over the top) and the lower chain (right to left
    under the bottom)."""
    imin = min(range(len(pts)), key=lambda i: pts[i][0])
    imax = min(range(len(pts)), key=lambda i: -pts[i][0])
    def walk(a, b):
        out, i = [pts[a]], a
        while i != b:
            i = (i + 1) % len(pts)
            out.append(pts[i])
        return out
    a = walk(imin, imax)
    b = walk(imax, imin)
    ay = sum(p[1] for p in a) / len(a)
    by = sum(p[1] for p in b) / len(b)
    return (a, b) if ay < by else (b, a)


def _band(c, h):
    return c + [(x, y + h) for x, y in reversed(c)]


def split_faces(chain, h, at_bottom=True):
    """One extrusion band cut at its own corner into the two faces the light hits
    differently: (left-front, right-front)."""
    key = (lambda k: chain[k][1]) if at_bottom else (lambda k: -chain[k][1])
    i = max(range(len(chain)), key=key)
    a, b = chain[:i + 1], chain[i:]
    if chain[0][0] > chain[-1][0]:
        a, b = b, a
    return _band(a, h), _band(b, h)


def solid(pts, h):
    """An outline swept straight down the screen: (silhouette, wall, left face, right face)."""
    up, low = chains(pts)
    sil = up + [(x, y + h) for x, y in reversed(list(reversed(low)))]
    left, right = split_faces(low, h, at_bottom=True)
    return sil, _band(low, h), left, right


def recess(pts, depth):
    """Looking into a hole: (visible far wall, floor). Both want clipping to the
    aperture - what you can see of a recess is bounded by its own mouth."""
    up, _ = chains(pts)
    left, right = split_faces(up, depth, at_bottom=False)
    floor = [(x, y + depth) for x, y in pts]
    return _band(up, depth), floor, left, right


# ---------------------------------------------------------------- palette
# two families only: warm-neutral porcelain/plaster, and one vermilion accent
# kin to Fledgeling's #C4622D, spent on the cast and nowhere else.
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFEFC", "#F7F3ED", "#E8E1D6"
VIGNETTE = "#8A7A62"

PLASTER_HI, PLASTER_MID, PLASTER_LO = "#FFFFFD", "#F4F0E6", "#DCD4C3"
WALL_HI, WALL_MID, WALL_LO = "#F0EADC", "#CDC2AB", "#A2957C"
CAV_HI, CAV_MID, CAV_LO = "#D0C6AE", "#A99D84", "#7C7057"

GEL_HI, GEL_1, GEL_2, GEL_3 = "#FFE0C0", "#FC9053", "#F05821", "#D8451A"
GEL_WALL_HI, GEL_WALL_LO, GEL_RIM = "#E85A22", "#D33A12", "#BC2E0C"
GEL_SCATTER = "#FFD7BC"                       # the rim wash: lighter and less
                                              # saturated in one move, which is
                                              # what one measurement of each said
BOUNCE = "#FF9C60"

# ---------------------------------------------------------------- geometry
mould_top = outline(CX, CY, R_MOULD)
mould_sil, mould_wall, mould_wl, mould_wr = solid(mould_top, MOULD_H)

cav_top = outline(CX, CY, R_CAV)
cav_far, cav_floor, cav_fl, cav_fr = recess(cav_top, CAV_D)

tile_top = outline(TILE_CX, TILE_CY, R_CAV)
tile_sil, tile_wall, tile_wl, tile_wr = solid(tile_top, TILE_H)

mould_up, mould_low = chains(mould_top)
cav_up, cav_low = chains(cav_top)
tile_up, tile_low = chains(tile_top)

# a slightly inset copy of the tile's top face, for the gel shoulder
tile_in = outline(TILE_CX, TILE_CY, R_CAV * 0.90)

BB_L = min(x for x, _ in tile_sil + mould_sil)
BB_R = max(x for x, _ in tile_sil + mould_sil)
BB_T = min(y for _, y in tile_sil + mould_sil)
BB_B = max(y for _, y in tile_sil + mould_sil)

# ---------------------------------------------------------------- emit

def lin(i, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<linearGradient id="{i}" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def rad(i, cx, cy, r, stops, fx=None, fy=None):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    f = f' fx="{fx:.0f}" fy="{fy:.0f}"' if fx is not None else ""
    return (f'<radialGradient id="{i}" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}"{f}'
            f' gradientUnits="userSpaceOnUse">{s}</radialGradient>')


defs = [
    f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>',
    f'<clipPath id="cavClip"><path d="{d(cav_top)}"/></clipPath>',
    f'<clipPath id="mouldFace"><path d="{d(mould_top)}"/></clipPath>',
    f'<clipPath id="tileFace"><path d="{d(tile_top)}"/></clipPath>',
    f'<clipPath id="tileWallClip"><path d="{d(tile_wall)}"/></clipPath>',
    f'<clipPath id="tileSil"><path d="{d(tile_sil)}"/></clipPath>',
    f'<clipPath id="mouldWallClip"><path d="{d(mould_wall)}"/></clipPath>',
    # What the mould's rim lights are allowed to see of the key. The cast cuts
    # its own silhouette out, and its near shadow dims what lies under it: a rim
    # highlight at full strength inside a cast shadow is the light model
    # contradicting itself, and it was leaving a white stub of the far lip
    # hanging beside the cast (L 0.845 against a local 0.384).
    f'<mask id="mouldKey"><rect x="0" y="0" width="{W}" height="{W}" fill="#fff"/>'
    f'<g filter="url(#bM)"><path d="{d(shift(tile_sil, *CAST_NEAR))}" fill="#000"'
    f' fill-opacity="{KEY_OCCLUSION}"/></g>'
    f'<path d="{d(tile_sil)}" fill="#000"/></mask>',
    # Where the cast's rim scatter is allowed to run at full strength. The
    # reference carries its rim lift evenly round the whole silhouette, but its
    # cast stands on open plaster on every side but two; ours overhangs the open
    # mouth on its lower-left, where the backing is the shaded far wall
    # (L 0.515 against the reference's 0.832 on the same octant). Run the wash
    # at full strength over that and the lower-left figure-ground boundary goes
    # to 1.05:1. So the wash is held back over the mouth, and only there.
    f'<mask id="rimLit"><rect x="0" y="0" width="{W}" height="{W}" fill="#fff"/>'
    f'<g filter="url(#bM)"><path d="{d(cav_top)}" fill="#000"'
    f' fill-opacity="{1 - RIM_SHADED:.2f}"/></g></mask>',

    # cushion ground: a lit dome, not a flat print
    rad("ground", 400, 330, 940, [("0", GROUND_HI, None), (".52", GROUND_MID, None),
                                  ("1", GROUND_LO, None)]),
    rad("vig", 512, 470, 700, [("0", VIGNETTE, "0"), (".45", VIGNETTE, ".02"),
                               (".78", VIGNETTE, ".06"), ("1", VIGNETTE, ".16")]),

    # plaster block
    lin("plasterFace", CX - 300, CY - 150, CX + 290, CY + 170,
        [("0", PLASTER_HI, None), (".55", PLASTER_MID, None), ("1", PLASTER_LO, None)]),
    lin("wallL", CX - 300, CY + 40, CX - 40, CY + MOULD_H + 200,
        [("0", "#F6F1E5", None), (".50", WALL_HI, None), ("1", "#C8BDA6", None)]),
    lin("wallR", CX + 40, CY + 40, CX + 300, CY + MOULD_H + 200,
        [("0", WALL_MID, None), (".55", "#B4A88F", None), ("1", WALL_LO, None)]),

    # the recess: far wall in shade, floor holding the warmth the cast left behind
    lin("cavL", CX - 200, CY - 130, CX - 30, CY + CAV_D,
        [("0", CAV_MID, None), (".60", "#BCB199", None), ("1", CAV_HI, None)]),
    lin("cavR", CX + 30, CY - 130, CX + 200, CY + CAV_D,
        [("0", CAV_LO, None), (".55", CAV_MID, None), ("1", "#BFB49B", None)]),
    lin("cavFloor", CX - 180, CY - 40, CX + 190, CY + 190,
        [("0", "#DDD0B6", None), (".50", "#EDE1CB", None), ("1", "#F5EDDC", None)]),
    rad("bounce", CX - 18, CY + CAV_D - 74, 250,
        [("0", BOUNCE, ".92"), (".46", BOUNCE, ".60"), (".82", BOUNCE, ".24"),
         ("1", BOUNCE, ".06")]),

    # the cast
    lin("gelFace", TILE_CX - 170, TILE_CY - 105, TILE_CX + 175, TILE_CY + 115,
        [("0", GEL_HI, None), (".30", GEL_1, None), (".70", GEL_2, None), ("1", GEL_3, None)]),
    lin("gelWallL", TILE_CX - 230, TILE_CY + 30, TILE_CX - 30, TILE_CY + TILE_H + 120,
        [("0", "#F86E2C", None), (".55", GEL_WALL_HI, None), ("1", "#CC3510", None)]),
    lin("gelWallR", TILE_CX + 30, TILE_CY + 30, TILE_CX + 230, TILE_CY + TILE_H + 120,
        [("0", "#DE4A18", None), (".55", GEL_WALL_LO, None), ("1", GEL_RIM, None)]),
    lin("gelShoulder", TILE_CX - 160, TILE_CY - 110, TILE_CX + 120, TILE_CY + 90,
        [("0", "#FFE6D2", ".92"), (".45", "#FFC49B", ".40"), ("1", "#FFA271", "0")]),
    rad("gelBloom", TILE_CX - 96, TILE_CY - 74, 208,
        [("0", "#FFF0E0", ".40"), (".46", "#FFDCC0", ".14"), ("1", "#FFC49B", "0")]),
    # the wrap highlight on the gel's lower shoulder: measured strongest at the
    # lit left corner and extinct by the right one, so it dies along +x.
    lin("gelArris", TILE_CX - 240, TILE_CY, TILE_CX + 240, TILE_CY,
        [("0", "#FFC79E", ".82"), (".55", "#FFAE7E", ".18"), ("1", "#FF9E6B", "0")]),

    # plaster rim light along the block's lit upper edge
    lin("rimLight", CX - 300, CY - 155, CX + 230, CY + 70,
        [("0", "#FFFFFF", ".18"), (".30", "#FFFFFF", ".60"), (".58", "#FFFFFF", ".72"),
         (".82", "#FFFFFF", ".30"), ("1", "#FFFFFF", "0")]),
    lin("cavLip", CX - 200, CY - 110, CX + 150, CY + 40,
        [("0", "#FFFFFF", ".70"), (".70", "#FFFFFF", ".22"), ("1", "#FFFFFF", "0")]),

    '<filter id="bS" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="7"/></filter>',
    '<filter id="bM" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="14"/></filter>',
    '<filter id="bL" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="34"/></filter>',
    '<filter id="bXL" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="58"/></filter>',
]

# ---- bg: the cushion tile
bg = [
    f'<rect x="0" y="0" width="{W}" height="{W}" fill="url(#ground)"/>',
    f'<rect x="0" y="0" width="{W}" height="{W}" fill="url(#vig)"/>',
]

# ---- mid: the mould, its recess, and the shadow the cast throws back into it
tile_shadow_sil = shift(tile_sil, SHADOW_DX, SHADOW_DY + LIFT * 0.42)

mid = [
    # the block's own shadow on the porcelain
    f'<g filter="url(#bXL)"><path d="{d(shift(mould_sil, SHADOW_DX * 1.5, SHADOW_DY * 1.7))}"'
    f' fill="#6E5F49" fill-opacity=".34"/></g>',
    f'<g filter="url(#bM)"><path d="{d(shift(mould_low, SHADOW_DX * 0.4, MOULD_H + 6))}"'
    f' fill="#544731" fill-opacity=".54"/></g>',

    # block
    f'<path d="{d(mould_wl)}" fill="url(#wallL)"/>',
    f'<path d="{d(mould_wr)}" fill="url(#wallR)"/>',
    f'<path d="{d(mould_top)} {d(cav_top)}" fill-rule="evenodd" fill="url(#plasterFace)"/>',

    # the block's arris is a fillet, not a cut: the top face's own paint carried
    # down over the wall and faded out across the measured 26px roll, so both
    # gradients stay registered and the roll inherits their lateral variation.
    f'<g clip-path="url(#mouldWallClip)"><g filter="url(#bS)">'
    f'<path d="{d(mould_low, False)}" fill="none" stroke="url(#plasterFace)"'
    f' stroke-width="{FILLET_BLOCK:.0f}" stroke-linecap="round"/></g></g>',

    # the recess, bounded by its own mouth
    '<g clip-path="url(#cavClip)">',
    f'<path d="{d(cav_floor)}" fill="url(#cavFloor)"/>',
    f'<path d="{d(cav_fl)}" fill="url(#cavL)"/>',
    f'<path d="{d(cav_fr)}" fill="url(#cavR)"/>',
    # ambient occlusion where the far wall meets the floor
    f'<g filter="url(#bM)"><path d="{d(shift(cav_up, 0, CAV_D + 26))}" fill="none"'
    f' stroke="#6B6049" stroke-opacity=".40" stroke-width="46"/></g>',
    # and the warmth the cast left in the floor
    f'<path d="{d(cav_floor)}" fill="url(#bounce)"/>',
    # the mouth is a rolled lip, not a cut: the top face turns over the rim and
    # carries its own paint a bounded way inside, all round the ring.
    f'<g filter="url(#bS)"><path d="{d(cav_top)}" fill="none" stroke="url(#plasterFace)"'
    f' stroke-width="{FILLET_LIP:.0f}"/></g>',
    '</g>',

    # occlusion belongs BELOW the lip's crest, inside the recess, not on it: the
    # ring pushed FILLET_LIP into the mouth, which the clip drops on the near
    # side where the lip's inside face is the lit floor.
    f'<g clip-path="url(#cavClip)"><g filter="url(#bS)">'
    f'<path d="{d(shift(cav_top, 0, FILLET_LIP))}" fill="none"'
    f' stroke="#87795E" stroke-opacity=".46" stroke-width="26"/></g></g>',

    # the cast's shadow, falling across the rim and down into the open cavity
    f'<g filter="url(#bL)"><path d="{d(tile_shadow_sil)}" fill="#77644B" fill-opacity=".40"/></g>',
    f'<g clip-path="url(#mouldFace)"><g filter="url(#bM)">'
    f'<path d="{d(shift(tile_sil, *CAST_NEAR))}"'
    f' fill="#5F4E38" fill-opacity=".44"/></g></g>',
]

# ---- fg: the cast tile
fg = [
    f'<path d="{d(tile_wl)}" fill="url(#gelWallL)"/>',
    f'<path d="{d(tile_wr)}" fill="url(#gelWallR)"/>',
    f'<path d="{d(tile_top)}" fill="url(#gelFace)"/>',
    # the gel's own body shade, deepest at the down-right shoulder
    f'<g clip-path="url(#tileFace)"><g filter="url(#bM)">'
    f'<path d="{d(shift(tile_low, 0, -14))}" fill="none" stroke="{GEL_3}"'
    f' stroke-opacity=".62" stroke-width="38"/></g></g>',
    # where the wall meets the face, a rolled shoulder rather than a printed edge:
    # the face's own paint carried down over the wall across the measured 22px
    # roll. The reference is monotone dark under this arris, so nothing bright
    # goes on the wall side of it.
    f'<g clip-path="url(#tileWallClip)"><g filter="url(#bS)">'
    f'<path d="{d(tile_low, False)}" fill="none" stroke="url(#gelFace)"'
    f' stroke-width="{FILLET_GEL:.0f}" stroke-linecap="round"/></g></g>',
    # the crest of that shoulder, on the FACE side where the measurement puts it
    f'<g clip-path="url(#tileFace)"><g filter="url(#bS)">'
    f'<path d="{d(tile_low, False)}" fill="none" stroke="url(#gelArris)"'
    f' stroke-width="15" stroke-linecap="round"/></g></g>',
    # rim scatter: the whole silhouette, not one lit side. Stroked on the cast's
    # own outline and clipped back to it, so only the inward half survives, and
    # blurred so it decays over the measured ~40px instead of ending in a band.
    f'<g mask="url(#rimLit)"><g clip-path="url(#tileSil)"><g filter="url(#bM)">'
    f'<path d="{d(tile_sil)}" fill="none" stroke="{GEL_SCATTER}"'
    f' stroke-opacity="{RIM_SCATTER_A}" stroke-width="{RIM_SCATTER * 2:.0f}"'
    f' stroke-linejoin="round"/></g></g></g>',
]

# ---- highlight: rim lights and the one soft bloom
hl = [
    '<g mask="url(#mouldKey)"><g clip-path="url(#mouldFace)">',
    # the block's lit upper edge
    f'<path d="{d(mould_up, False)}" fill="none" stroke="url(#rimLight)" stroke-width="9"'
    f' stroke-linecap="round"/>',
    # the cavity's far lip, catching the same light
    f'<path d="{d(cav_up, False)}" fill="none" stroke="url(#cavLip)" stroke-width="7"'
    f' stroke-linecap="round"/>',
    '</g></g>',
    # the cast's rounded shoulder
    f'<g clip-path="url(#tileFace)">'
    f'<path d="{d(tile_up, False)}" fill="none" stroke="url(#gelShoulder)" stroke-width="17"'
    f' stroke-linecap="round"/>'
    f'<path d="{d(tile_in)}" fill="url(#gelBloom)"/>'
    f'</g>',
    # the cushion's inner rim, the tell that the ground is a lit surface
    f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity=".78"'
    f' stroke-width="7"/>',
]


def layer(name, body):
    return f'<g id="{name}">' + "".join(body) + "</g>"


svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">\n'
    '<!--\n'
    '  create-mac-icon app icon master. Direction "The Cast" (porcelain register).\n'
    '  Full-bleed 1024 artwork; the squircle is a CLIP, never a baked corner or shadow.\n'
    '  The cast tile and the mould cavity are the marketplace squircle itself, at 0.211\n'
    '  scale on a dimetric ground plane - the icon contains the shape it makes.\n'
    '  Generated by build_icon.py; edit the constants there, never this file.\n'
    '  Four layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.\n'
    '-->\n'
    "<defs>" + "".join(defs) + "</defs>\n"
    '<g clip-path="url(#mask)">\n'
    + layer("bg", bg) + "\n"
    + layer("mid", mid) + "\n"
    + layer("fg", fg) + "\n"
    + layer("highlight", hl) + "\n"
    "</g>\n</svg>\n"
)

out = ASSETS / "icon.svg"
out.write_text(svg)
print(f"wrote {out}  ({len(svg)} bytes, {len(UNIT)} outline points)")
print(f"focal bbox  x {BB_L:.0f}..{BB_R:.0f}  ({(BB_R - BB_L) / W * 100:.1f}% of tile)")
print(f"            y {BB_T:.0f}..{BB_B:.0f}  ({(BB_B - BB_T) / W * 100:.1f}% of tile)")
print(f"margins     l {BB_L:.0f}  r {W - BB_R:.0f}  t {BB_T:.0f}  b {W - BB_B:.0f}")
