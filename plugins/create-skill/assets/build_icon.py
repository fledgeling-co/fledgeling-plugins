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

SPLIT_Y = 0.54                   # the horizontal parting, as a fraction of BODY_H
KEY_W, KEY_H = 74.0, 42.0        # the interlocking key on the vertical parting

# light: one soft key, up and to the left. The molten material is the sanctioned
# second source and is emissive - it lights, it does not cast.
SHADOW_DX, SHADOW_DY = 30.0, 40.0

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
MELT_CORE = "#FFE6B8"            # the one hot specular, nothing else
MELT_HI = "#FF8A1E"
MELT_1 = "#FB4A08"
MELT_2 = "#E62405"
MELT_3 = "#C41403"
MELT_DEEP = "#8E0F02"
GLOW_IN = "#FF4A08"              # what the melt throws onto its OWN walls: red-hot
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
mouth_in = ellipse(CX, CY, R_IN)

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
seam_v = [(CX + 34.0, CY + KY * 0.0)]        # replaced below by the keyed run

# vertical parting with an interlocking key, drawn down the near face from the
# rim to the base. The jog is what says "this comes apart", which is what a
# casting flask is for.
_vx = CX + 34.0
_vy0 = CY + R_OUT * KY * math.sqrt(max(0.0, 1 - ((_vx - CX) / R_OUT) ** 2))
seam_v = [(_vx, _vy0),
          (_vx, _vy0 + part_y - KEY_H / 2),
          (_vx - KEY_W, _vy0 + part_y - KEY_H / 2),
          (_vx - KEY_W, _vy0 + part_y + KEY_H / 2),
          (_vx, _vy0 + part_y + KEY_H / 2),
          (_vx, _vy0 + BODY_H)]

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
    f'<clipPath id="rimClip"><path d="{d(mouth_out)} {d(mouth_in)}"/></clipPath>',
    f'<clipPath id="pourClip"><path d="{d(POUR)}"/></clipPath>',
    # everything that is NOT the flask, so a highlight meant for the porcelain
    # cannot spill onto the pour that passes in front of it
    f'<mask id="notPour"><rect width="{W}" height="{W}" fill="#fff"/>'
    f'<path d="{d(POUR)}" fill="#000"/></mask>',

    # cushion ground: a lit dome with an edge vignette, never a flat print
    rad("ground", 392, 322, 950, [("0", GROUND_HI, None), (".52", GROUND_MID, None),
                                  ("1", GROUND_LO, None)]),
    rad("vig", 470, 430, 720, [("0", VIGNETTE, "0"), (".40", VIGNETTE, ".03"),
                               (".72", VIGNETTE, ".11"), ("1", VIGNETTE, ".30")]),
    # what the open flask throws back onto the tile it stands on
    rad("spill", CX, CY + 24, 470, [("0", BOUNCE, ".30"), (".38", BOUNCE, ".15"),
                                    (".72", BOUNCE, ".05"), ("1", BOUNCE, "0")],
        ry=470 * 0.62),

    # porcelain
    lin("rimFace", CX - 300, CY - 170, CX + 280, CY + 180,
        [("0", PORC_HI, None), (".46", PORC_MID, None), ("1", PORC_LO, None)]),
    lin("wall", CX - R_OUT, CY, CX + R_OUT, CY,
        [("0", "#E4D8C2", None), (".12", WALL_L_HI, None), (".34", WALL_L_MID, None),
         (".55", WALL_L_LO, None), (".76", WALL_R_MID, None), (".93", WALL_R_LO, None),
         ("1", "#98876D", None)]),
    # the base goes to shade before it meets its own contact shadow
    lin("wallFoot", CX, CY + BODY_H - 96, CX, CY + BODY_H + R_OUT * KY,
        [("0", "#000000", "0"), (".50", "#3E3324", ".09"), ("1", "#3E3324", ".34")]),

    # the cavity's far wall, in its own shade before the pool lights it
    lin("cavWall", CX, CY - R_IN * KY, CX, CY - R_IN * KY + CAV_D * 0.92,
        [("0", "#8E7D69", None), (".22", "#AE6A40", None), (".52", "#CE2E06", None),
         (".80", "#DE1A02", None), ("1", "#F03A04", None)]),
    # and the light the pool actually throws up it
    rad("cavGlow", CX, CY + POOL_D, 330,
        [("0", GLOW_IN, ".78"), (".34", GLOW_IN, ".54"), (".68", GLOW_IN, ".26"),
         (".90", GLOW_IN, ".08"), ("1", GLOW_IN, "0")], ry=330 * 0.86),

    # the molten pool: hottest under the falling drop, cooling toward its own rim
    rad("pool", DROP_C[0], CY + POOL_D - 44, R_IN * 1.16,
        [("0", "#FC8014", None), (".10", "#EE3E03", None), (".27", "#D22103", None),
         (".53", "#BC1302", None), (".80", "#960B01", None), ("1", "#6E0901", None)],
        ry=R_IN * 1.16 * KY),
    lin("meniscus", CX - R_IN, CY + POOL_D, CX + R_IN, CY + POOL_D,
        [("0", "#FA5A0C", ".54"), (".5", "#FF9A3C", ".70"), ("1", "#FA5A0C", ".42")]),

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
    rad("dropGrad", DROP_C[0] - 5, DROP_C[1] + 4, DROP_R * 2.1,
        [("0", "#FFB854", None), (".30", "#F97A12", None), (".66", "#E63404", None),
         ("1", "#B41203", None)]),

    # porcelain rim lights
    lin("rimLight", CX - 300, CY - 175, CX + 240, CY + 60,
        [("0", "#FFFFFF", ".16"), (".28", "#FFFFFF", ".64"), (".56", "#FFFFFF", ".74"),
         (".82", "#FFFFFF", ".28"), ("1", "#FFFFFF", "0")]),
    lin("lipLight", CX - 210, CY - 120, CX + 170, CY + 30,
        [("0", "#FFFFFF", ".62"), (".62", "#FFFFFF", ".20"), ("1", "#FFFFFF", "0")]),

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
    f'<rect width="{W}" height="{W}" fill="url(#vig)"/>',
    f'<rect width="{W}" height="{W}" fill="url(#spill)"/>',
]

# ---- mid: the flask, its cavity, and the pool already gathered in it
mid = [
    # the flask's own shadow: a wide ambient pool plus a tight contact under the base
    f'<g filter="url(#bXL)"><path d="{d(shift(body_sil, SHADOW_DX * 1.4, SHADOW_DY * 1.5))}"'
    f' fill="#5F5138" fill-opacity=".46"/></g>',
    f'<g filter="url(#bM)"><path d="{d(shift(out_low, SHADOW_DX * 0.35, BODY_H + 8))}"'
    f' fill="#3D3120" fill-opacity=".66"/></g>',

    # body: two faces, so the round wall has real volume rather than one ramp
    f'<path d="{d(body_face)}" fill="url(#wall)"/>',
    f'<g clip-path="url(#bodyClip)"><rect width="{W}" height="{W}" fill="url(#wallFoot)"/></g>',

    # the parting lines - this is a flask that comes apart, not a bowl
    f'<g clip-path="url(#bodyClip)" fill="none" stroke-linecap="round">'
    f'<path d="{d(seam_h, False)}" stroke="#AA9C81" stroke-opacity=".62" stroke-width="4"/>'
    f'<path d="{d(shift(seam_h, 0, 3.5), False)}" stroke="#FFFFFF" stroke-opacity=".55"'
    f' stroke-width="3"/>'
    f'<path d="{d(seam_v, False)}" stroke="#AA9C81" stroke-opacity=".58" stroke-width="4"/>'
    f'<path d="{d(shift(seam_v, -3.5, 0), False)}" stroke="#FFFFFF" stroke-opacity=".42"'
    f' stroke-width="3"/>'
    f'</g>',

    # the rim annulus: the flat top face of the porcelain wall
    f'<path d="{d(mouth_out)} {d(mouth_in)}" fill-rule="evenodd" fill="url(#rimFace)"/>',

    # the recess, bounded by its own mouth
    '<g clip-path="url(#cavClip)">',
    f'<path d="{d(cav_wall)}" fill="url(#cavWall)"/>',
    # ambient occlusion where the far wall runs down toward the melt
    f'<g filter="url(#bM)"><path d="{d(shift(in_up, 0, 16), False)}" fill="none"'
    f' stroke="#6B6049" stroke-opacity=".30" stroke-width="40"/></g>',
    # the light the pool throws back up that wall - the sanctioned second source
    f'<rect width="{W}" height="{W}" fill="url(#cavGlow)"/>',
    # the melt itself
    f'<path d="{d(pool)}" fill="url(#pool)"/>',
    # two faint rings, the pour's own disturbance still spreading
    f'<path d="{d(ellipse(DROP_C[0], CY + POOL_D - 4, R_IN * 0.42))}" fill="none"'
    f' stroke="#FF9A3C" stroke-opacity=".18" stroke-width="7"/>',
    f'<path d="{d(ellipse(DROP_C[0], CY + POOL_D - 4, R_IN * 0.70))}" fill="none"'
    f' stroke="#FF9A3C" stroke-opacity=".12" stroke-width="6"/>',
    # the meniscus climbing the wall where the melt wets the porcelain
    f'<g filter="url(#bXS)"><path d="{d(pool_up, False)}" fill="none"'
    f' stroke="url(#meniscus)" stroke-width="13"/></g>',
    # and the shade under the near lip, so the mouth reads as a cut, not a printed ring
    f'<g filter="url(#bS)"><path d="{d(mouth_in)}" fill="none" stroke="#7C6E54"'
    f' stroke-opacity=".40" stroke-width="26"/></g>',
    '</g>',

    # the melt's glow leaking out over the near rim onto the porcelain
    f'<g clip-path="url(#rimClip)"><g filter="url(#bL)">'
    f'<path d="{d(shift(mouth_in, 0, 10))}" fill="{BOUNCE}" fill-opacity=".54"/></g></g>',
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
