#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the create-skill icon.

Direction "The Pour": Tahoe gel-glass sub-register (a), porcelain + gel object,
crossed with device bank #16 (the icon performs the verb), #18 (edge-bleed
physicality) and #22 (emissive interior as the sanctioned second light).

The subject is a skill that turns a vague intention into a specified, built
thing, so the icon is that turn caught in the act: a two-part porcelain casting
flask stands open on the tile, and molten vermilion pours down into it from
somewhere above the frame. The stream is CAUGHT MID-AIR - its leading drop hangs
clear of the pool, with one detached droplet falling between them - and the
finished form is implied only by the pool already gathered in the cavity, still
liquid, still lighting its own walls.

The sibling create-mac-icon shows a FINISHED tile leaving a mould. This one is
the opposite half of the same physics and must never be confused with it:
nothing here is solid yet, nothing is leaving, and the vessel is round where
that one's is the set's own superellipse.

Geometry is authored on a single dimetric ground plane (one foreshortening
constant, KY) and every part of the flask is an ellipse on that plane, so the
outer body, the rim annulus, the cavity and the pool cannot drift out of
register with each other. The extrusion is a pure screen-vertical sweep of that
plane, so the solid cannot drift either. The pour is a swept ribbon - a
centreline with a width profile - never an outline, because an outline reads as
a flat noodle rather than as material in flight.

Every constant is named; a fidelity round is a parameter edit, never path
surgery.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import pathlib

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- ground plane
# One foreshortening constant for the whole icon. Everything that lies on the
# tile's floor is a circle of radius r drawn as an ellipse (r, r * KY); every
# horizontal surface inside the flask uses the same number, so the mouth, the
# cavity and the pool are the same disc seen at three heights.
KY = 0.515

CX, CY = 512.0, 560.0            # centre of the flask's mouth, on the canvas

R_OUT = 285.0                    # flask outer radius, ground units  -> 55.7% of tile
WALL_T = 74.0                    # porcelain wall thickness
R_IN = R_OUT - WALL_T            # cavity radius

BODY_H = 212.0                   # how far the body drops below the mouth plane
CAV_D = 150.0                    # how deep the cavity is cut
POOL_D = 86.0                    # how far below the mouth the pool's surface sits

# MEASURED, not chosen. The visible mouth is NOT the outer ellipse scaled: on the
# reference the near rim band reads 52px and the far band 30px at matched x, where
# a concentric annulus would make both 41. The lip is rolled over, so the opening
# we actually see sits ABOVE the rim's top plane by half that difference. Encoding
# it as a rise keeps one ellipse family (the cavity and the pool still ride the
# same disc) while killing the concentric-primitive tell.
MOUTH_RISE = 11.0

SPLIT_Y = 0.54                   # the horizontal parting, as a fraction of BODY_H
# MEASURED off the reference: its key is a tall narrow tab, 56px wide and 85px
# high straddling the parting, not the short wide one this master carried.
KEY_W, KEY_H = 56.0, 80.0        # the interlocking key on the vertical parting

# ---------------------------------------------------------------- the notch
# The parting key of a two-part casting flask, cut as a real slot through the
# outer wall rather than drawn on it. MEASURED off the reference: the slot sits
# 6.7 deg left of dead front (centre x 478 against a vessel centre of 514 and a
# radius of 309), opens ~55px wide at the lip, closes to a hairline about 110px
# down, and carries melt in its upper ~75px before the seam continues to the
# foot with its interlocking key. A plain circle is what makes an object read as
# defaulted; this is the one path that makes it read as designed.
NOTCH_U = -0.117                 # notch centre as sin(theta) around the mouth
NOTCH_W = 80.0                   # slot width at the lip
NOTCH_D = 96.0                   # how far down the slot stays open
NOTCH_MELT = 82.0                # how far the melt runs down inside it

# light: one soft key, up and to the left. The molten material is the sanctioned
# second source and is emissive - it lights, it does not cast.
# MEASURED: on the reference the ground runs 0.946 at its left-middle edge down
# to 0.440 at the bottom-right corner, the cylinder's terminator wraps monotonic
# from L 0.87 at the left silhouette to 0.30 at the right, and the cast shadow's
# centroid sits 294px right and 115px down from the base centre - 21 deg below
# horizontal, not the near-vertical drop this master had.
SHADOW_DX, SHADOW_DY = 122.0, 48.0
SHADOW_LONG = (296.0, 116.0)     # where the far end of the cast lands

# ---------------------------------------------------------------- the pour
# A centreline plus a width profile, swept. It enters through the TOP EDGE of the
# mask (device #18: the tile is a window on a bigger scene, not a print) left of
# centre, and leans right as it falls, because a stream leaving a lip off-frame
# to the upper left arcs toward the vessel rather than dropping like a plumb line.
POUR_P0 = (420.0, -46.0)
POUR_P1 = (446.0, 140.0)
POUR_P2 = (492.0, 336.0)
POUR_P3 = (517.0, 470.0)         # centre of the leading drop; the cap adds its radius

# half-width along the stream: wide at the lip, thinned by acceleration, then
# gathered into the leading bulb where surface tension collects the flow.
POUR_PROFILE = [(0.00, 41.0), (0.20, 35.0), (0.42, 28.0),
                (0.64, 24.0), (0.86, 23.0), (1.00, 38.0)]

DROP_C = (531.0, 582.0)          # the detached droplet: the signature move, literal
DROP_R = 24.0

# ---------------------------------------------------------------- palette
# Two hue families only: warm-neutral porcelain, and one molten vermilion kin to
# Fledgeling's #C4622D, spent on the pour and the pool and nowhere else.
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFDF8", "#F6EFE1", "#DDD0B7"
VIGNETTE = "#8A7A62"
KEYFALL = "#7A6448"              # the key's own falloff, toward the shadow corner

PORC_HI, PORC_MID, PORC_LO = "#FFFFFD", "#F3EEE2", "#CEC2AC"
WALL_L_HI, WALL_L_MID, WALL_L_LO = "#FDF7E9", "#F0E5D0", "#D2C0A4"
WALL_R_HI, WALL_R_MID, WALL_R_LO = "#D8CDB8", "#A99B80", "#7C6B54"
CAV_HI, CAV_MID, CAV_LO = "#E2D0B2", "#C4B49A", "#A2917A"

# MEASURED, not chosen. Sampled against the Engine C raster on matched geometry, the
# first two drafts' melt sat at L 0.57-0.80 and hue 20-25 where the reference's sits at
# L 0.42-0.53 and hue 5-9. "Molten" had been authored as bright-and-yellow on the
# assumption that hot means light; material at temperature actually reads as a deep
# saturated RED at middling luminance, with the yellow end reserved for a small core and
# for the thin far edge where the melt is shallow. The whole ramp moved 17 degrees
# toward red and about 0.22 down in luminance.
#
# What that correction MISSED, and this round fixes: the reference's pool is not one
# deep red, it is a light SOURCE. Its top-2% core reaches L 0.913 at hue 45 inside a
# 110x163px patch, its rim bottoms out at L 0.132 at hue 3, and the whole pool spans
# p10 0.217 to p90 0.667. The shipped master spanned p10 0.404 to p90 0.525 - a filled
# shape, more saturated than the reference and still muted, because vibrancy here is
# emission, not saturation. The ramp below is that measured spread, and the hot core
# now lights the cavity wall above it (measured #FC6C26, L 0.51, S 0.84 - where this
# master had unlit porcelain at L 0.91, S 0.11).
MELT_BLOOM = "#FFE9A8"           # the emitter's core, L 0.90
MELT_CORE = "#FCCF47"            # L 0.81 H 45   (reference: #FCCF47 at the core)
MELT_HOT = "#FBAE2E"             # L 0.71 H 38
MELT_HI = "#FB6108"              # L 0.49 H 22
MELT_1 = "#FB4604"               # L 0.41 H 16
MELT_2 = "#EC2A05"               # L 0.32 H 10
MELT_3 = "#D61501"               # L 0.24 H  6
MELT_4 = "#C40C01"               # L 0.19 H  3
MELT_DEEP = "#960B01"            # L 0.14
GLOW_IN = "#FF5A12"              # what the melt throws onto its OWN walls: red-hot
WALL_LIT = "#FC6C26"             # measured: the cavity wall where the pool lights it
LIP_LIT = "#FFEDDA"              # measured: the near lip, L 0.916 S 0.16
BOUNCE = "#FF9C60"               # what leaks past the rim onto porcelain: peach

# ---------------------------------------------------------------- primitives


def ellipse(cx, cy, r, n=132):
    """A ground-plane circle of radius r, seen at the icon's one foreshortening."""
    return [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * KY * math.sin(2 * math.pi * i / n)) for i in range(n)]


def chains(pts):
    """Split a convex outline at its leftmost and rightmost points into
    (upper chain, lower chain), each running left to right."""
    imin = min(range(len(pts)), key=lambda i: pts[i][0])
    imax = max(range(len(pts)), key=lambda i: pts[i][0])

    def walk(a, b):
        out, i = [pts[a]], a
        while i != b:
            i = (i + 1) % len(pts)
            out.append(pts[i])
        return out

    a, b = walk(imin, imax), walk(imax, imin)
    return (a, b[::-1]) if (sum(p[1] for p in a) / len(a)
                            < sum(p[1] for p in b) / len(b)) else (b[::-1], a)


def band(chain, h):
    """A chain swept straight down the screen by h: the face it sweeps out."""
    return chain + [(x, y + h) for x, y in reversed(chain)]


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def d(pts, close=True):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def solid(pts, h):
    """An outline swept down the screen: (silhouette, lower-face band)."""
    up, low = chains(pts)
    sil = up + [(x, y + h) for x, y in reversed(low)] + [(low[0][0], low[0][1] + h)]
    return sil, band(low, h)


# ---------------------------------------------------------------- the ribbon


def _cubic_pt(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def _profile(t):
    ps = POUR_PROFILE
    for i in range(len(ps) - 1):
        (t0, w0), (t1, w1) = ps[i], ps[i + 1]
        if t <= t1:
            k = (t - t0) / (t1 - t0)
            k = k * k * (3 - 2 * k)                     # smoothstep between knots
            return w0 + (w1 - w0) * k
    return ps[-1][1]


def centreline(n=96):
    return [_cubic_pt(POUR_P0, POUR_P1, POUR_P2, POUR_P3, i / n) for i in range(n + 1)]


def ribbon(scale=1.0, n=96):
    """The pour as a SWEPT SURFACE: the centreline offset by its own width profile
    on each side, closed at the leading end by a real hemispherical cap. Built this
    way the leading drop is part of the same body as the stream - drawn as an
    outline instead, the bulb reads as a separate blob stuck on the end."""
    pts = centreline(n)
    left, right = [], []
    for i, p in enumerate(pts):
        t = i / n
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        m = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / m, tx / m
        w = _profile(t) * scale
        left.append((p[0] - nx * w, p[1] - ny * w))
        right.append((p[0] + nx * w, p[1] + ny * w))
    # hemispherical cap around the last centreline point
    end = pts[-1]
    prev = pts[-2]
    ang = math.atan2(end[1] - prev[1], end[0] - prev[0])
    r = _profile(1.0) * scale
    cap = [(end[0] + r * math.cos(ang - math.pi / 2 + math.pi * k / 22),
            end[1] + r * math.sin(ang - math.pi / 2 + math.pi * k / 22))
           for k in range(1, 22)]
    return right + cap + left[::-1]


def core_ribbon(n=96):
    """The hot core seen through the stream's own translucency: a narrower ribbon
    pushed toward the lit side, never a symmetric inner copy - a core that sits on
    the axis reads as a printed stripe."""
    pts = centreline(n)
    left, right = [], []
    for i, p in enumerate(pts):
        t = i / n
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        m = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / m, tx / m
        w = _profile(t) * 0.26
        off = -_profile(t) * 0.32                       # toward the key, up and left
        left.append((p[0] + nx * (off - w), p[1] + ny * (off - w)))
        right.append((p[0] + nx * (off + w), p[1] + ny * (off + w)))
    return right + left[::-1]


def edge_chain(side, n=96, trim=0.06):
    """One flank of the stream, as an open polyline, for the rim light along it."""
    pts = centreline(n)
    out = []
    for i, p in enumerate(pts):
        t = i / n
        if t < trim or t > 0.965:
            continue
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        m = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / m, tx / m
        w = _profile(t) * 0.88 * side
        out.append((p[0] + nx * w, p[1] + ny * w))
    return out


def teardrop(cx, cy, r, h=2.3, n=40):
    """The detached droplet, falling point-up: a circle whose upper half is drawn
    out into a tail, because a plain circle reads as a bubble."""
    out = []
    for i in range(n + 1):
        a = math.pi * 1.5 - 2 * math.pi * i / n
        x, y = math.cos(a), math.sin(a)
        k = max(0.0, -y) ** 1.6                          # 1 at the top, 0 at the base
        out.append((cx + x * r * (1 - 0.72 * k), cy + y * r * (1 + (h - 1) * k)))
    return out


# ---------------------------------------------------------------- geometry
mouth_out = ellipse(CX, CY, R_OUT)
# NOT the outer ellipse scaled: raised by the measured lip roll, so the near band
# reads thicker than the far one exactly as the reference's does.
mouth_in = ellipse(CX, CY - MOUTH_RISE, R_IN)

body_sil, body_low_band = solid(mouth_out, BODY_H)
out_up, out_low = chains(mouth_out)
in_up, in_low = chains(mouth_in)

body_face = band(out_low, BODY_H)

# the cavity: the far inner wall, and the pool sitting part-way down it
cav_wall = band(in_up, CAV_D)
pool = shift(mouth_in, 0.0, POOL_D)
pool_up, pool_low = chains(pool)

# the parting lines that make it a two-part flask rather than a bowl
part_y = BODY_H * SPLIT_Y
seam_h = [(x, y + part_y) for x, y in out_low]

# ---------------------------------------------------------------- the notch
# A real cut, not a drawn line. The slot is a tapered wedge on the near face,
# centred on the parting; its top edge is the mouth's own near arc (so the
# opening is interrupted rather than concentric), its sides close to a hairline
# NOTCH_D down, and the seam then carries on to the foot with the key jog.
NOTCH_X = CX + NOTCH_U * R_OUT


def _arc_y(x, r, cy):
    """Where the near arc of a ground-plane circle of radius r sits at this x."""
    k = max(0.0, 1.0 - ((x - CX) / r) ** 2)
    return cy + r * KY * math.sqrt(k)


NOTCH_TOP_L = _arc_y(NOTCH_X - NOTCH_W / 2, R_IN, CY - MOUTH_RISE)
NOTCH_TOP_R = _arc_y(NOTCH_X + NOTCH_W / 2, R_IN, CY - MOUTH_RISE)
NOTCH_TOP_C = _arc_y(NOTCH_X, R_IN, CY - MOUTH_RISE)
NOTCH_RIM = _arc_y(NOTCH_X, R_OUT, CY)          # where it breaks the outer edge

# the slot: mouth arc across the top, taper to a hairline at the bottom
notch_slot = [
    (NOTCH_X - NOTCH_W / 2, NOTCH_TOP_L),
    (NOTCH_X - NOTCH_W * 0.30, NOTCH_TOP_C + NOTCH_D * 0.40),
    (NOTCH_X - 4.0, NOTCH_TOP_C + NOTCH_D),
    (NOTCH_X + 4.0, NOTCH_TOP_C + NOTCH_D),
    (NOTCH_X + NOTCH_W * 0.30, NOTCH_TOP_C + NOTCH_D * 0.40),
    (NOTCH_X + NOTCH_W / 2, NOTCH_TOP_R),
    (NOTCH_X, NOTCH_TOP_C + 2.0),
]
# the melt that has run into the top of it
notch_melt = [
    (NOTCH_X - NOTCH_W / 2 + 1, NOTCH_TOP_L - 3),
    (NOTCH_X - NOTCH_W * 0.20, NOTCH_TOP_C + NOTCH_MELT * 0.60),
    (NOTCH_X - 3.5, NOTCH_TOP_C + NOTCH_MELT),
    (NOTCH_X + 3.5, NOTCH_TOP_C + NOTCH_MELT),
    (NOTCH_X + NOTCH_W * 0.20, NOTCH_TOP_C + NOTCH_MELT * 0.60),
    (NOTCH_X + NOTCH_W / 2 - 1, NOTCH_TOP_R - 3),
    (NOTCH_X, NOTCH_TOP_C - 12.0),
]

# vertical parting below the slot, with the interlocking key. Drawn from where
# the slot closes down to the base, so the cut and the seam are one run.
_vy0 = NOTCH_TOP_C + NOTCH_D - 8.0
_vy1 = NOTCH_RIM + BODY_H
_ky0 = NOTCH_RIM + part_y - KEY_H / 2
_ky1 = NOTCH_RIM + part_y + KEY_H / 2
seam_v = [(NOTCH_X, _vy0),
          (NOTCH_X, _ky0),
          (NOTCH_X + KEY_W, _ky0),
          (NOTCH_X + KEY_W, _ky1),
          (NOTCH_X, _ky1),
          (NOTCH_X, _vy1)]

# the horizontal parting is INTERRUPTED by the key rather than run under it -
# an interlock, not a box laid on a line
seam_h_l = [(x, y) for x, y in seam_h if x <= NOTCH_X]
seam_h_r = [(x, y) for x, y in seam_h if x >= NOTCH_X + KEY_W]

# ---------------------------------------------------------------- the cast
# The shadow is a disc on the ground plane, not a copy of the silhouette: the
# base ellipse, stretched along the key's own axis and slid down it.
_base = ellipse(CX, CY + BODY_H, R_OUT)


def _cast(dx, dy, sx):
    return [(CX + (x - CX) * sx + dx, y + dy) for x, y in _base]


cast_long = _cast(SHADOW_LONG[0], SHADOW_LONG[1], 1.22)
cast_mid = _cast(SHADOW_DX, SHADOW_DY, 1.06)




POUR = ribbon()
POUR_GLOW = ribbon(scale=1.30)
POUR_CORE = core_ribbon()
POUR_EDGE_L = edge_chain(-1.0)
POUR_EDGE_R = edge_chain(+1.0)
DROP = teardrop(*DROP_C, DROP_R)

BB_L = min(x for x, _ in body_sil)
BB_R = max(x for x, _ in body_sil)
BB_T = min(y for _, y in body_sil)
BB_B = max(y for _, y in body_sil)

# ---------------------------------------------------------------- emit


def lin(i, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<linearGradient id="{i}" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}"'
            f' y2="{y2:.0f}" gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def rad(i, cx, cy, r, stops, ry=None):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    tr = (f' gradientTransform="translate({cx:.0f} {cy:.0f}) scale(1 {ry / r:.4f})'
          f' translate({-cx:.0f} {-cy:.0f})"') if ry else ""
    return (f'<radialGradient id="{i}" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}"'
            f' gradientUnits="userSpaceOnUse"{tr}>{s}</radialGradient>')


defs = [
    f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>',
    f'<clipPath id="cavClip"><path d="{d(mouth_in)}"/></clipPath>',
    f'<clipPath id="bodyClip"><path d="{d(body_sil)}"/></clipPath>',
    # NOTE the clip-rule. Without it the two subpaths wind the same way, nonzero
    # unions them, and "the rim annulus" silently becomes the whole outer disc -
    # so every warm veil meant for the porcelain was being painted across the melt
    # as well. That is a third peach veil over the accent, on top of the two this
    # loop already caught, and it is most of why the emitter read as a flat fill.
    f'<clipPath id="rimClip" clip-rule="evenodd">'
    f'<path clip-rule="evenodd" d="{d(mouth_out)} {d(mouth_in)}"/></clipPath>',
    f'<clipPath id="pourClip"><path d="{d(POUR)}"/></clipPath>',
    # everything that is NOT the flask, so a highlight meant for the porcelain
    # cannot spill onto the pour that passes in front of it
    f'<mask id="notPour"><rect width="{W}" height="{W}" fill="#fff"/>'
    f'<path d="{d(POUR)}" fill="#000"/></mask>',

    # cushion ground: a lit dome with an edge vignette, never a flat print.
    # MEASURED: the reference's ground peaks at its LEFT-MIDDLE edge (L 0.946) and
    # bottoms at the bottom-right corner (0.440). This master's peaked top-left and
    # ran only 0.90 to 0.75 - flat, and with no agreement between where the light
    # is and where the shadow goes.
    rad("ground", 236, 336, 1060, [("0", GROUND_HI, None), (".42", GROUND_MID, None),
                                   ("1", GROUND_LO, None)]),
    # the key's own falloff, on the single axis from the key corner to the shadow
    lin("keyfall", 0, 432, 1024, 1024,
        [("0", KEYFALL, "0"), (".34", KEYFALL, ".03"), (".68", KEYFALL, ".14"),
         ("1", KEYFALL, ".28")]),
    rad("vig", 430, 400, 760, [("0", VIGNETTE, "0"), (".46", VIGNETTE, ".02"),
                               (".76", VIGNETTE, ".08"), ("1", VIGNETTE, ".22")]),
    # what the open flask throws back onto the tile it stands on
    rad("spill", CX - 26, CY + 40, 470, [("0", BOUNCE, ".34"), (".38", BOUNCE, ".17"),
                                         (".72", BOUNCE, ".06"), ("1", BOUNCE, "0")],
        ry=470 * 0.62),

    # porcelain
    lin("rimFace", CX - 300, CY - 170, CX + 280, CY + 180,
        [("0", PORC_HI, None), (".46", PORC_MID, None), ("1", PORC_LO, None)]),
    # the terminator, transcribed off the reference's own wall at y=760: L 0.87 at
    # the left silhouette, a fast cosine fall to 0.52 by 40% across, an ambient
    # plateau through the shadow side, and a grazing darkening at the right edge.
    # The old ramp brightened again at 12% and at the far right - two counter-lights
    # in a one-key scene, which is what made the light model unrankable.
    lin("wall", CX - R_OUT, CY, CX + R_OUT, CY,
        [("0", "#F5DCC5", None), (".05", "#F2D9C2", None), (".12", "#E0C4AC", None),
         (".20", "#D1B39B", None), (".30", "#C4A68D", None), (".41", "#AA8C73", None),
         (".58", "#9D8069", None), (".73", "#9E816A", None), (".86", "#95755E", None),
         (".94", "#8A6C56", None), ("1", "#6E4C36", None)]),
    # the base goes to shade before it meets its own contact shadow
    lin("wallFoot", CX, CY + BODY_H - 96, CX, CY + BODY_H + R_OUT * KY,
        [("0", "#000000", "0"), (".50", "#3E3324", ".09"), ("1", "#3E3324", ".34")]),

    # the cavity's far wall. MEASURED: on the reference this wall is lit by the
    # pool along its whole height (#EC723B at the lip, #FC6724 at the waterline,
    # L 0.51-0.54, S 0.75-0.86). This master had it as unlit porcelain at L 0.91,
    # S 0.11 - the emitter was a fill, so it lit nothing.
    lin("cavWall", CX, CY - R_IN * KY - MOUTH_RISE,
        CX, CY - R_IN * KY - MOUTH_RISE + CAV_D * 0.92,
        [("0", "#F0854A", None), (".26", "#FB7A2E", None), (".58", WALL_LIT, None),
         (".82", "#FB5A18", None), ("1", "#F84E10", None)]),
    # and the light the pool actually throws up it
    rad("cavGlow", CX, CY + POOL_D - MOUTH_RISE, 360,
        [("0", GLOW_IN, ".86"), (".34", GLOW_IN, ".64"), (".68", GLOW_IN, ".34"),
         (".90", GLOW_IN, ".12"), ("1", GLOW_IN, "0")], ry=360 * 0.86),
    # the bounce the emitter puts on the rim's top face: strongest at the far side,
    # where the rolled inner lip turns toward the melt (reference: #FCA76D, S 0.57
    # at the back, falling to S 0.15 on the near band)
    lin("rimGlow", CX, CY - R_OUT * KY, CX, CY + R_OUT * KY,
        [("0", "#FF7A2E", ".26"), (".05", "#FF7A2E", ".62"), (".10", "#FF8637", ".40"),
         (".50", BOUNCE, ".10"), (".82", BOUNCE, ".14"), ("1", BOUNCE, ".07")]),

    # the molten pool as an EMITTER: a hot core under the impact point falling away
    # to a deep red rim. Measured spread on the reference is p10 0.217 / median
    # 0.396 / p90 0.667 with a top-2% core at L 0.913; this master shipped 0.404 /
    # 0.477 / 0.525, i.e. one filled colour.
    rad("pool", DROP_C[0], CY + POOL_D - MOUTH_RISE - 30, R_IN * 1.16,
        [("0", MELT_BLOOM, None), (".06", MELT_CORE, None), (".13", MELT_HOT, None),
         (".21", MELT_HI, None), (".30", MELT_1, None), (".44", MELT_2, None),
         (".60", MELT_3, None), (".78", MELT_4, None), ("1", MELT_DEEP, None)],
        ry=R_IN * 1.16 * KY),
    # the bloom above it - the layer that makes the core read as light rather than
    # as a lighter fill
    rad("bloom", DROP_C[0], CY + POOL_D - MOUTH_RISE - 26, R_IN * 0.62,
        [("0", MELT_BLOOM, ".72"), (".34", MELT_CORE, ".40"), (".68", MELT_HOT, ".14"),
         ("1", MELT_HI, "0")], ry=R_IN * 0.62 * KY * 1.25),
    lin("meniscus", CX - R_IN, CY + POOL_D, CX + R_IN, CY + POOL_D,
        [("0", "#FA5A0C", ".54"), (".5", "#FF9A3C", ".70"), ("1", "#FA5A0C", ".42")]),

    # the notch: a cut, so its interior is porcelain in deep shade, and the melt
    # that ran into it is the same material as the pool it came from
    lin("notchDark", NOTCH_X, NOTCH_TOP_C, NOTCH_X, NOTCH_TOP_C + NOTCH_D,
        [("0", "#5C4630", None), (".45", "#6E543A", None), ("1", "#8A6E4E", None)]),
    lin("notchMelt", NOTCH_X, NOTCH_TOP_C - 12, NOTCH_X, NOTCH_TOP_C + NOTCH_MELT,
        [("0", MELT_HOT, None), (".26", MELT_HI, None), (".62", MELT_2, None),
         ("1", "#8E0A01", None)]),


    # the pour. Along its length first: cooler and denser where it is thick at the
    # lip, brightening as it thins and stretches, hottest in the gathered drop.
    lin("pourBody", 430, 0, 540, POUR_P3[1] + 46,
        [("0", "#C61403", None), (".46", "#D91E03", None), (".82", "#E92C05", None),
         ("1", "#F43C06", None)]),
    lin("pourCore", 430, 0, 545, POUR_P3[1] + 30,
        [("0", "#8E0F02", ".34"), (".45", "#A81102", ".28"), ("1", "#B81403", ".20")]),
    lin("pourEdgeL", 420, 0, 520, POUR_P3[1],
        [("0", "#EC7440", ".62"), (".45", "#F08A52", ".82"), ("1", "#F79A62", ".88")]),
    lin("pourEdgeR", 420, 0, 520, POUR_P3[1],
        [("0", "#F03A02", ".48"), (".55", "#FE4F03", ".66"), ("1", "#FF6410", ".72")]),
    rad("pourGlow", 486, 300, 400,
        [("0", GLOW_IN, ".17"), (".45", GLOW_IN, ".07"), ("1", GLOW_IN, "0")]),
    # the leading bulb entering the emitter's field. MEASURED on the reference:
    # the stream's tip reads #FCD784 at L 0.85 where its shaft is L 0.21-0.30 -
    # the pour is lit by the pool it is about to join, not by the key.
    rad("tipGlow", POUR_P3[0], POUR_P3[1] + 16, 96,
        [("0", MELT_CORE, ".92"), (".26", MELT_HOT, ".72"), (".58", MELT_HI, ".34"),
         ("1", MELT_1, "0")]),
    rad("dropGrad", DROP_C[0] - 5, DROP_C[1] + 4, DROP_R * 2.1,
        [("0", "#FFB854", None), (".30", "#F97A12", None), (".66", "#E63404", None),
         ("1", "#B41203", None)]),

    # porcelain rim lights. One key, up and to the left: the run peaks at the
    # left-upper silhouette and dies before the terminator, rather than reappearing
    # on the shadow side.
    lin("rimLight", CX - 300, CY - 175, CX + 200, CY + 40,
        [("0", "#FFFFFF", ".26"), (".20", "#FFFFFF", ".72"), (".46", "#FFFFFF", ".62"),
         (".74", "#FFFFFF", ".16"), ("1", "#FFFFFF", "0")]),
    # the inner lip, lit by the melt and not by the key: warm, not white
    # (reference: #FDE6D4, L 0.916, S 0.16)
    lin("lipLight", CX - 210, CY - 120, CX + 170, CY + 30,
        [("0", LIP_LIT, ".62"), (".62", LIP_LIT, ".26"), ("1", LIP_LIT, ".06")]),


    '<filter id="bXS" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="3.5"/></filter>',
    '<filter id="bS" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="8"/></filter>',
    '<filter id="bM" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="17"/></filter>',
    '<filter id="bL" x="-80%" y="-80%" width="260%" height="260%">'
    '<feGaussianBlur stdDeviation="34"/></filter>',
    '<filter id="bXL" x="-80%" y="-80%" width="260%" height="260%">'
    '<feGaussianBlur stdDeviation="62"/></filter>',
]

# ---- bg: the cushion tile, and the warmth the open flask throws back onto it
bg = [
    f'<rect width="{W}" height="{W}" fill="url(#ground)"/>',
    f'<rect width="{W}" height="{W}" fill="url(#keyfall)"/>',
    f'<rect width="{W}" height="{W}" fill="url(#vig)"/>',
    f'<rect width="{W}" height="{W}" fill="url(#spill)"/>',
]

# ---- mid: the flask, its cavity, and the pool already gathered in it
mid = [
    # the flask's own shadow. One key up and to the left means one long cast down
    # and to the RIGHT: the reference's shadow centroid lands 294px right and 115px
    # down from the base centre (21 deg below horizontal). This master dropped its
    # shadow almost straight down, which is why the light model read as unresolved.
    # The cast is built from the BASE disc, not the silhouette, so it lies on the
    # ground plane instead of climbing the wall it belongs to.
    f'<g filter="url(#bXL)"><path d="{d(cast_long)}" fill="#6A5A40"'
    f' fill-opacity=".24"/></g>',
    f'<g filter="url(#bL)"><path d="{d(cast_mid)}" fill="#5F5138" fill-opacity=".34"/></g>',
    f'<g filter="url(#bM)"><path d="{d(shift(out_low, SHADOW_DX * 0.22, BODY_H + 8))}"'
    f' fill="#3D3120" fill-opacity=".66"/></g>',

    # body: two faces, so the round wall has real volume rather than one ramp
    f'<path d="{d(body_face)}" fill="url(#wall)"/>',
    f'<g clip-path="url(#bodyClip)"><rect width="{W}" height="{W}" fill="url(#wallFoot)"/></g>',

    # the horizontal parting - this is a flask that comes apart, not a bowl
    f'<g clip-path="url(#bodyClip)" fill="none" stroke-linecap="round">'
    f'<path d="{d(seam_h_l, False)}" stroke="#8E7E63" stroke-opacity=".66" stroke-width="4"/>'
    f'<path d="{d(seam_h_r, False)}" stroke="#8E7E63" stroke-opacity=".66" stroke-width="4"/>'
    f'<path d="{d(shift(seam_h_l, 0, 3.5), False)}" stroke="#FFFFFF" stroke-opacity=".40"'
    f' stroke-width="3"/>'
    f'<path d="{d(shift(seam_h_r, 0, 3.5), False)}" stroke="#FFFFFF" stroke-opacity=".40"'
    f' stroke-width="3"/>'
    f'</g>',

    # the rim annulus: the flat top face of the porcelain wall
    f'<path d="{d(mouth_out)} {d(mouth_in)}" fill-rule="evenodd" fill="url(#rimFace)"/>',
    # the emitter's bounce on that face, strongest where the lip turns toward it
    f'<g clip-path="url(#rimClip)"><rect width="{W}" height="{W}" fill="url(#rimGlow)"/></g>',

    # the recess, bounded by its own mouth
    '<g clip-path="url(#cavClip)">',
    f'<path d="{d(cav_wall)}" fill="url(#cavWall)"/>',
    # ambient occlusion where the far wall runs down toward the melt
    f'<g filter="url(#bM)"><path d="{d(shift(in_up, 0, 16), False)}" fill="none"'
    f' stroke="#6B6049" stroke-opacity=".20" stroke-width="40"/></g>',
    # the light the pool throws back up that wall - the sanctioned second source
    f'<rect width="{W}" height="{W}" fill="url(#cavGlow)"/>',
    # the melt itself
    f'<path d="{d(pool)}" fill="url(#pool)"/>',
    # and its bloom: the layer that makes the core a light source rather than a
    # lighter fill (material-recipes: emissive interior)
    f'<g filter="url(#bM)"><path d="{d(pool)}" fill="url(#bloom)"/></g>',
    # two faint rings, the pour's own disturbance still spreading
    f'<path d="{d(ellipse(DROP_C[0], CY + POOL_D - MOUTH_RISE - 4, R_IN * 0.42))}"'
    f' fill="none" stroke="#FFC24E" stroke-opacity=".16" stroke-width="7"/>',
    f'<path d="{d(ellipse(DROP_C[0], CY + POOL_D - MOUTH_RISE - 4, R_IN * 0.70))}"'
    f' fill="none" stroke="#FF9A3C" stroke-opacity=".12" stroke-width="6"/>',
    # the meniscus climbing the wall where the melt wets the porcelain
    f'<g filter="url(#bXS)"><path d="{d(pool_up, False)}" fill="none"'
    f' stroke="url(#meniscus)" stroke-width="13"/></g>',
    # and the shade under the near lip, so the mouth reads as a cut, not a printed ring
    f'<g filter="url(#bS)"><path d="{d(mouth_in)}" fill="none" stroke="#7C6E54"'
    f' stroke-opacity=".34" stroke-width="26"/></g>',
    '</g>',

    # the near lip, lit from below by the melt rather than from above by the key
    f'<g filter="url(#bXS)"><path d="{d(in_low, False)}" fill="none" stroke="{LIP_LIT}"'
    f' stroke-opacity=".72" stroke-width="5" stroke-linecap="round"/></g>',

    # the melt's glow leaking out over the near rim onto the porcelain
    f'<g clip-path="url(#rimClip)"><g filter="url(#bL)">'
    f'<path d="{d(shift(mouth_in, 0, 10))}" fill="{BOUNCE}" fill-opacity=".54"/></g></g>',

    # ---- the notch: the parting key, cut rather than drawn -------------------
    f'<g clip-path="url(#bodyClip)">',
    # the slot's own interior, in deep shade
    f'<path d="{d(notch_slot)}" fill="url(#notchDark)"/>',
    # ambient occlusion where the cut breaks the rim's top face
    f'<g filter="url(#bXS)"><path d="{d(notch_slot)}" fill="none" stroke="#5A452E"'
    f' stroke-opacity=".55" stroke-width="7"/></g>',
    # the melt that has run into it, still connected to the pool it came from
    f'<g filter="url(#bS)"><path d="{d(notch_melt)}" fill="{GLOW_IN}"'
    f' fill-opacity=".60"/></g>',
    f'<path d="{d(notch_melt)}" fill="url(#notchMelt)"/>',
    # the cut faces: the left one turns toward the key, the right one away
    f'<g fill="none" stroke-linecap="round">'
    f'<path d="{d(notch_slot[:3], False)}" stroke="#FFF6E8" stroke-opacity=".62"'
    f' stroke-width="4"/>'
    f'<path d="{d(notch_slot[3:6], False)}" stroke="#4A3520" stroke-opacity=".52"'
    f' stroke-width="5"/>'
    # and the seam it becomes, with the interlocking key
    f'<path d="{d(seam_v, False)}" stroke="#6E583C" stroke-opacity=".80" stroke-width="5"/>'
    f'<path d="{d(shift(seam_v, -3.5, 3.0), False)}" stroke="#FFFFFF" stroke-opacity=".38"'
    f' stroke-width="3"/>'
    f'</g>',
    f'</g>',
]


# ---- fg: the pour, caught mid-air
fg = [
    # what the stream throws onto everything behind it
    f'<g filter="url(#bL)"><path d="{d(POUR_GLOW)}" fill="url(#pourGlow)"/></g>',
    # the body: one swept surface, cap included, so the leading drop is the stream
    f'<path d="{d(POUR)}" fill="url(#pourBody)"/>',
    # the hot core, seen through the material rather than painted on it
    f'<g clip-path="url(#pourClip)"><g filter="url(#bS)">'
    f'<path d="{d(POUR_CORE)}" fill="url(#pourCore)"/></g></g>',
    # the leading bulb, lit by the pool it is about to enter
    f'<g clip-path="url(#pourClip)"><rect width="{W}" height="{W}" fill="url(#tipGlow)"/></g>',
    # the detached droplet: the moment the pour is caught in, made literal
    f'<g filter="url(#bL)"><ellipse cx="{DROP_C[0]:.0f}" cy="{DROP_C[1]:.0f}"'
    f' rx="{DROP_R * 3.2:.0f}" ry="{DROP_R * 3.2:.0f}" fill="{GLOW_IN}"'
    f' fill-opacity=".13"/></g>',
    f'<path d="{d(DROP)}" fill="url(#dropGrad)"/>',
]

# ---- highlight: rim lights, the stream's lit and shaded flanks, the cushion rim
hl = [
    '<g mask="url(#notPour)">',
    # the flask's lit upper edge, and the inner lip catching the same key
    f'<g clip-path="url(#bodyClip)"><path d="{d(out_up, False)}" fill="none"'
    f' stroke="url(#rimLight)" stroke-width="9" stroke-linecap="round"/></g>',
    f'<path d="{d(in_up, False)}" fill="none" stroke="url(#lipLight)" stroke-width="7"'
    f' stroke-linecap="round"/>',
    '</g>',
    # the stream's flanks: lit toward the key, deepened away from it
    f'<g clip-path="url(#pourClip)" fill="none" stroke-linecap="round">'
    f'<path d="{d(POUR_EDGE_L, False)}" stroke="url(#pourEdgeL)" stroke-width="15"/>'
    f'<path d="{d(POUR_EDGE_R, False)}" stroke="url(#pourEdgeR)" stroke-width="22"/>'
    f'</g>',
    # one small specular on the droplet, the only place a highlight is that tight
    f'<ellipse cx="{DROP_C[0] - 4:.0f}" cy="{DROP_C[1] + 2:.0f}" rx="4" ry="6"'
    f' fill="{MELT_CORE}" fill-opacity=".78"/>',
    # the cushion's inner rim: the tell that the ground is a lit surface
    f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity=".78"'
    f' stroke-width="7"/>',
]


def layer(name, body):
    return f'<g id="{name}">' + "".join(body) + "</g>"


svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}"'
    f' viewBox="0 0 {W} {W}" role="img" aria-label="create-skill">\n'
    '<title>create-skill</title>\n'
    '<!--\n'
    '  create-skill app icon master. Direction "The Pour" (porcelain register).\n'
    '  A two-part porcelain casting flask receives a stream of molten vermilion that\n'
    '  enters through the top edge of the mask and is caught MID-AIR: the leading drop\n'
    '  hangs clear of the pool, one detached droplet between them. Nothing here has set\n'
    '  yet - the finished form is implied only by the melt already gathered in the\n'
    '  cavity, which is also the icon\'s second, emissive light source.\n'
    '  Full-bleed 1024 artwork; the squircle is a CLIP, never a baked corner or shadow.\n'
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

if __name__ == "__main__":
    out = ASSETS / "icon.svg"
    out.write_text(svg)
    print(f"wrote {out}  ({len(svg)} bytes)")
    print(f"flask bbox  x {BB_L:.0f}..{BB_R:.0f}  ({(BB_R - BB_L) / W * 100:.1f}% of tile)")
    print(f"            y {BB_T:.0f}..{BB_B:.0f}  ({(BB_B - BB_T) / W * 100:.1f}% of tile)")
    print(f"margins     l {BB_L:.0f}  r {W - BB_R:.0f}  t {BB_T:.0f}  b {W - BB_B:.0f}")
