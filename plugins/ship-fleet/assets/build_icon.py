#!/usr/bin/env python3
"""build_icon.py — ship-fleet marketplace icon, Engine A (hand-authored layered SVG).

Direction: Tahoe gel-glass, sub-register (a) — porcelain/vellum cushion carrying
coloured gel objects.  Glyph: a harbour seen from above-and-angled — a quay with
four finger piers, three slips, two clay vessels held in their berths, and one
ember gel vessel already past the pier heads on a departing heading, its wake
running back into the slip it vacated.

Signature move: the ordered berth grid with one vessel about to depart.

Geometry and material live in the constant blocks below; the script emits the
SVG.  Fidelity rounds are parameter edits, never path surgery.
"""
from __future__ import annotations

import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE.parent.parent.parent / "plugins/create-mac-icon/assets/squircle-path.txt")
if not SQUIRCLE.exists():
    SQUIRCLE = pathlib.Path(
        "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/squircle-path.txt")

# ---------------------------------------------------------------- canvas
S = 1024

# ---------------------------------------------------------------- harbour geometry
# Harbour space: x runs from the quay's back edge to the pier heads,
# y runs down across the piers and slips.
PIER_W = 84          # thickness of a pier measured across the slips
SLIP_W = 124         # clear water between two piers
N_PIERS = 4
PIER_LEN = 470       # quay face -> pier head of the longest pier
# Real basins are not a comb of identical teeth.  Staggering the pier lengths
# breaks the venetian-blind read the first four-equal-bars draft had, and lets
# the plan-form open toward the water the lead vessel is leaving into.
PIER_SCALE = (0.80, 0.95, 1.05, 1.00)
QUAY_W = 60
HARBOR_H = N_PIERS * PIER_W + (N_PIERS - 1) * SLIP_W        # 688
HARBOR_W = QUAY_W + PIER_LEN                                 # 504

ROT = -7.0           # the "angled" half of above-and-angled
SCALE = 0.95
CX, CY = 418.0, 516.0        # where the harbour block's centre lands on the tile

WALL = 21.0          # extrusion depth of the stone (screen px, straight down)
HULL_WALL = 10.0     # freeboard shown on a hull
SH_X, SH_Y = 16.0, 26.0      # contact-shadow offset (key light is top-left)

# ---------------------------------------------------------------- vessels
HULL_L, HULL_B = 250.0, 80.0
EMBER_L, EMBER_B = 304.0, 103.0
BERTHS = [          # (slip index, hull centre x in harbour space)
    (1, 302.0),
    (2, 286.0),
]
EMBER_C = (758.0, 288.0)     # screen-space centre of the departing vessel
EMBER_HEADING = -30.0        # degrees; bow points up-and-right

# ---------------------------------------------------------------- palette
# Sampled off references/corpus/apple-2026: porcelain ground median L 0.96 with
# p5 0.88-0.91, brightest ground at the top-left corner; the orange gel's darkest
# pixel stays saturated and warm (rgb 213,48,32 -> hue 5.3, S 0.85) rather than
# desaturating.  The vellum ramp is the marketplace family's own warm variant.
PLATE = ("#FEFCF7", "#F8F1E4", "#EBE1CE")
VIGN = ("#8A7355", "#7A6244")
STONE_TOP = ("#FFFDF8", "#F7F0E2", "#EDE3CF")
STONE_WALL = ("#D8CAAE", "#BBA983", "#9C8A66")
BOLLARD = ("#F2E9D5", "#CFC0A0", "#A8977A")
WATER = ("#A38C61", "#8E7749", "#6E5A33")
# r04/r05: warming the clay toward the basin's hue cost 16px separation between
# a berthed vessel and the water it sits in, which is the check the whole small-size
# read depends on.  Held at the r03 values, warm-neutral but a clear step darker.
CLAY = ("#D6D0C3", "#B0A897", "#8D8471")
CLAY_WELL = ("#9C937E", "#7E7563")
CLAY_WALL = ("#B9B0A0", "#9A9080", "#7C7462")
# r03, measured off the winning raster rather than assumed: the reference gel runs
# median hue 15.3 / S 0.90 / V 0.91, and its DARKEST pixel is rgb(198,32,5) — S 0.98,
# V 0.78.  A translucent gel keeps its chroma in shadow; the first ramp lost both
# (darkest S 0.80, V 0.59, hue 0.5) and read as opaque paint.
GEL = ("#F98247", "#F2683A", "#E24A1C", "#CC3A0C")
GEL_WELL = ("#C7350C", "#AE2C06", "#97270A")
GEL_RIM = "#FFC9A4"
INK = "#6E7A86"
SHADOW = "#6B5138"

# one key light, one axis: everything material ramps along this segment
KEY = ((150.0, 110.0), (830.0, 900.0))


# ---------------------------------------------------------------- transforms
def harbor(x: float, y: float) -> tuple[float, float]:
    """Harbour space -> screen space."""
    a = math.radians(ROT)
    c, s = math.cos(a), math.sin(a)
    X = (x - HARBOR_W / 2) * SCALE
    Y = (y - HARBOR_H / 2) * SCALE
    return (CX + X * c - Y * s, CY + X * s + Y * c)


def rot_about(px: float, py: float, cx: float, cy: float, deg: float):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    dx, dy = px - cx, py - cy
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def fmt(p) -> str:
    return f"{p[0]:.2f} {p[1]:.2f}"


def path_from(cmds) -> str:
    """cmds: list of ('M', p) | ('L', p) | ('C', p1, p2, p3) | ('Z',)"""
    out = []
    for c in cmds:
        if c[0] == "Z":
            out.append("Z")
        elif c[0] == "C":
            out.append("C " + ", ".join(fmt(p) for p in c[1:]))
        else:
            out.append(f"{c[0]} {fmt(c[1])}")
    return " ".join(out)


def xform(cmds, f):
    return [(c[0],) + tuple(f(*p) for p in c[1:]) if c[0] != "Z" else ("Z",) for c in cmds]


def offset(cmds, dx, dy):
    return xform(cmds, lambda x, y: (x + dx, y + dy))


# ---------------------------------------------------------------- primitives
K = 0.5523


def rrect(x, y, w, h, r) -> list:
    r = min(r, w / 2, h / 2)
    k = r * K
    x1, y1 = x + w, y + h
    return [
        ("M", (x + r, y)),
        ("L", (x1 - r, y)),
        ("C", (x1 - r + k, y), (x1, y + r - k), (x1, y + r)),
        ("L", (x1, y1 - r)),
        ("C", (x1, y1 - r + k), (x1 - r + k, y1), (x1 - r, y1)),
        ("L", (x + r, y1)),
        ("C", (x + r - k, y1), (x, y1 - r + k), (x, y1 - r)),
        ("L", (x, y + r)),
        ("C", (x, y + r - k), (x + r - k, y), (x + r, y)),
        ("Z",),
    ]


def hull(L=HULL_L, B=HULL_B) -> list:
    """Plan-view hull, bow at +x, centred on the origin."""
    hx, hy = L / 2, B / 2
    return [
        ("M", (hx, 0.0)),
        ("C", (hx - .10 * L, -.24 * B), (hx - .20 * L, -.43 * B), (hx - .32 * L, -.50 * B)),
        ("L", (-hx + .16 * L, -hy)),
        ("C", (-hx + .06 * L, -hy), (-hx, -.46 * B), (-hx, -.39 * B)),
        ("L", (-hx, .39 * B)),
        ("C", (-hx, .46 * B), (-hx + .06 * L, hy), (-hx + .16 * L, hy)),
        ("L", (hx - .32 * L, hy)),
        ("C", (hx - .20 * L, .43 * B), (hx - .10 * L, .24 * B), (hx, 0.0)),
        ("Z",),
    ]


def hull_well(L=HULL_L, B=HULL_B) -> list:
    """Deck well, set aft and blunt so a foredeck survives (armada r2 lesson)."""
    return rrect(-L / 2 + .15 * L, -.25 * B, .55 * L, .50 * B, .20 * B)


def placed(cmds, cx, cy, deg):
    return xform(cmds, lambda x, y: rot_about(cx + x, cy + y, cx, cy, deg))


# ---------------------------------------------------------------- svg assembly
def grad_lin(gid, stops, x1, y1, x2, y2):
    body = "".join(
        f'<stop offset="{o}" stop-color="{c}"'
        + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
        for o, c, a in stops)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">{body}</linearGradient>')


def key_grad(gid, colours):
    n = len(colours) - 1
    stops = [(round(i / n, 3), c, None) for i, c in enumerate(colours)]
    return grad_lin(gid, stops, KEY[0][0], KEY[0][1], KEY[1][0], KEY[1][1])


def build() -> str:
    sq = SQUIRCLE.read_text().strip()
    defs = [f'<clipPath id="sq"><path d="{sq}"/></clipPath>']

    defs.append(
        f'<radialGradient id="plate" cx="32%" cy="26%" r="88%">'
        f'<stop offset="0" stop-color="{PLATE[0]}"/>'
        f'<stop offset=".55" stop-color="{PLATE[1]}"/>'
        f'<stop offset="1" stop-color="{PLATE[2]}"/></radialGradient>')
    defs.append(
        f'<radialGradient id="vign" cx="50%" cy="45%" r="74%">'
        f'<stop offset=".56" stop-color="{VIGN[0]}" stop-opacity="0"/>'
        f'<stop offset=".85" stop-color="{VIGN[0]}" stop-opacity=".085"/>'
        f'<stop offset="1" stop-color="{VIGN[1]}" stop-opacity=".21"/></radialGradient>')
    defs.append(
        '<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".92"/>'
        '<stop offset=".30" stop-color="#FFFFFF" stop-opacity=".20"/>'
        '<stop offset=".72" stop-color="#FFFFFF" stop-opacity=".10"/>'
        '<stop offset="1" stop-color="#FFF6E8" stop-opacity=".46"/></linearGradient>')

    defs.append(key_grad("stone", STONE_TOP))
    defs.append(key_grad("wall", STONE_WALL))
    defs.append(key_grad("bollard", BOLLARD))
    defs.append(key_grad("clay", CLAY))
    defs.append(key_grad("claywell", CLAY_WELL))
    defs.append(key_grad("gel", GEL))
    defs.append(key_grad("gelwell", GEL_WELL))
    defs.append(key_grad("claywall", CLAY_WALL))
    defs.append(
        '<linearGradient id="topcatch" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".46"/>'
        '<stop offset=".13" stop-color="#FFFFFF" stop-opacity=".18"/>'
        '<stop offset=".30" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset=".86" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity=".16"/></linearGradient>')
    # the gel's own catch is a warm peach, not white: the reference's brightest gel
    # pixel is rgb(250,156,110) at hue 22.5, and nothing in this scene emits white
    defs.append(
        '<linearGradient id="topcatchwarm" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#FFD9BE" stop-opacity=".52"/>'
        '<stop offset=".14" stop-color="#FFD9BE" stop-opacity=".20"/>'
        '<stop offset=".32" stop-color="#FFD9BE" stop-opacity="0"/>'
        '<stop offset=".84" stop-color="#FFD9BE" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#FFB187" stop-opacity=".20"/></linearGradient>')

    defs.append('<filter id="soft" x="-45%" y="-45%" width="190%" height="190%">'
                '<feGaussianBlur stdDeviation="24"/></filter>')
    defs.append('<filter id="tight" x="-40%" y="-40%" width="180%" height="180%">'
                '<feGaussianBlur stdDeviation="8"/></filter>')
    defs.append('<filter id="mist" x="-40%" y="-40%" width="180%" height="180%">'
                '<feGaussianBlur stdDeviation="15"/></filter>')
    defs.append('<filter id="hair" x="-30%" y="-30%" width="160%" height="160%">'
                '<feGaussianBlur stdDeviation="3.2"/></filter>')

    bg, mid, fg, hi = [], [], [], []

    # ---------------- bg: cushion tile
    bg.append(f'<rect width="{S}" height="{S}" fill="url(#plate)"/>')
    bg.append(f'<rect width="{S}" height="{S}" fill="url(#vign)"/>')

    # The basin: the whole ground is water, a step down the value ramp from the
    # stone laid over it.  On the family's pale vellum the stone measured 1.11:1
    # against the water it sits in and the berth grid had no figure-ground at all.
    # r08 then walked the depth back up: darkening the basin helps the PIERS and
    # hurts both vessel classes, because the vessels are dark and the piers are
    # light.  Measured across four settings, this one takes the focal to 2.18:1
    # and the berthed pair to 2.32:1 for 0.16 of pier ratio — the right trade,
    # since the piers also carry coursing, walls, mouldings and cast shadows,
    # and the vessels are what rubric #7 is actually about.
    defs.append(grad_lin("water", [(0, WATER[0], ".185"), (.55, WATER[1], ".280"),
                                   (1, WATER[2], ".380")],
                         KEY[0][0], KEY[0][1], KEY[1][0], KEY[1][1]))
    bg.append(f'<rect width="{S}" height="{S}" fill="url(#water)"/>')
    # r04/r05 (rejected, kept as a record): a broad sheen ellipse over the open
    # water was tried twice and cost ~0.002 of composite at EVERY size, including
    # the 16px read.  The tile already carries a plate radial, a vignette and the
    # water ramp; a fourth broad field is redundant, and the gate said so.

    # water ripples: short staggered marks, not ruled lines
    rip, rip_segs = [], []
    for i in range(14):
        y = 96 + i * 66
        segs = ((-60, 300), (350, 690), (760, 1120)) if i % 2 else ((-40, 430), (500, 1090),)
        for j, (x0, x1) in enumerate(segs):
            x0 += (i * 37) % 90
            p0 = rot_about(x0, y, 512, 512, ROT)
            p1 = rot_about(x1, y, 512, 512, ROT)
            op = .048 if (i + j) % 3 else .066
            rip_segs.append((p0, p1))
            rip.append(f'<path d="M {fmt(p0)} L {fmt(p1)}" stroke="{INK}" '
                       f'stroke-opacity="{op:.3f}" stroke-width="2.6" stroke-linecap="round" '
                       f'fill="none"/>')
    bg.append('<g filter="url(#hair)">' + "".join(rip) + "</g>")

    # ---------------- the departing vessel's track out of the vacated slip

    # r02 material — the wake.  A single tapered band reads as a smear; the raster
    # take is a FAN of fine foam streaks that diverge astern over a shallow trough
    # of displaced water, and that is what makes the vessel read as moving.
    wake = wake_points()
    band_l, band_r = [], []
    for i, p in enumerate(wake):
        t = i / (len(wake) - 1)
        w = 34.0 * (1 - t) + 20.0 * t
        n = normal(wake[max(i - 1, 0)], wake[min(i + 1, len(wake) - 1)], w)
        band_l.append((p[0] + n[0], p[1] + n[1]))
        band_r.append((p[0] - n[0], p[1] - n[1]))
    poly = band_l + band_r[::-1]
    bg.append('<g filter="url(#mist)"><path d="M ' + " L ".join(fmt(q) for q in poly)
              + f' Z" fill="{SHADOW}" fill-opacity=".24"/></g>')

    STREAKS = (-1.0, -0.52, 0.0, 0.52, 1.0)
    foam = []
    for k, lane in enumerate(STREAKS):
        pts = []
        for i, p in enumerate(wake):
            t = i / (len(wake) - 1)
            spread = 9.0 + 30.0 * t ** 0.8          # the fan opens astern
            n = normal(wake[max(i - 1, 0)], wake[min(i + 1, len(wake) - 1)], lane * spread)
            pts.append((p[0] + n[0], p[1] + n[1]))
        head = 0 if abs(lane) < .6 else 2           # outer streaks start further aft
        for i in range(head, len(pts) - 1):
            t = i / (len(pts) - 1)
            op = (.80 if abs(lane) < .6 else .58) * (1 - t) ** 1.25
            if op < .035:
                continue
            foam.append(f'<path d="M {fmt(pts[i])} L {fmt(pts[i+1])}" stroke="#FFFFFF" '
                        f'stroke-opacity="{op:.3f}" stroke-width="{5.4 - 1.2 * abs(lane):.1f}" '
                        f'stroke-linecap="round" fill="none"/>')
    bg.append('<g filter="url(#hair)">' + "".join(foam) + "</g>")

    # ---------------- mid: the berth structure
    # The shore is a filled apron cut by the mask on three sides — the harbour is
    # larger than the frame (device #18), and it stops the comb reading as a letter.
    solids = []          # screen space, back to front
    apron = xform(rrect(-620, -820, 620 + QUAY_W, HARBOR_H + 1640, 26), harbor)
    solids.append(apron)
    piers = []
    for i in range(N_PIERS):
        y0 = i * (PIER_W + SLIP_W)
        L = PIER_LEN * PIER_SCALE[i]
        piers.append(xform(rrect(QUAY_W - 40, y0, L + 40, PIER_W, 20), harbor))
    solids.extend(piers)

    # contact shadows first, then walls, then top faces
    sh = []
    for cmds in solids:
        sh.append(f'<path d="{path_from(offset(cmds, SH_X, SH_Y))}" '
                  f'fill="{SHADOW}" fill-opacity=".185"/>')
    mid.append('<g filter="url(#soft)">' + "".join(sh) + "</g>")
    sh2 = []
    for cmds in solids:
        sh2.append(f'<path d="{path_from(offset(cmds, SH_X * .45, SH_Y * .45))}" '
                   f'fill="{SHADOW}" fill-opacity=".155"/>')
    mid.append('<g filter="url(#tight)">' + "".join(sh2) + "</g>")

    for cmds in solids:
        mid.append(f'<path d="{path_from(offset(cmds, 0, WALL))}" fill="url(#wall)"/>')
    for cmds in solids:
        mid.append(f'<path d="{path_from(cmds)}" fill="url(#stone)"/>')

    # r01 material — slab coursing.  A stone quay is laid in courses, and the
    # joints are what stop a pale slab reading as cut paper: each joint is a dark
    # groove with a lit chamfer immediately below it, both clipped to the solid.
    for i, cmds in enumerate(solids):
        defs.append(f'<clipPath id="face{i}"><path d="{path_from(cmds)}"/></clipPath>')
    joints = []
    for i in range(N_PIERS):
        y0 = i * (PIER_W + SLIP_W)
        L = PIER_LEN * PIER_SCALE[i]
        n = int(L // 150)
        for j in range(1, n + 1):
            bx = QUAY_W - 20 + j * (L + 20) / (n + 1)
            a, b = harbor(bx, y0 - 4), harbor(bx, y0 + PIER_W + 4)
            joints.append(f'<g clip-path="url(#face{i+1})">'
                          f'<path d="M {fmt(a)} L {fmt(b)}" stroke="#9C8B6E" stroke-opacity=".13" '
                          f'stroke-width="2.6" fill="none"/>'
                          f'<path d="M {fmt((a[0]+3.0, a[1]))} L {fmt((b[0]+3.0, b[1]))}" '
                          f'stroke="#FFFCF3" stroke-opacity=".19" stroke-width="2.2" fill="none"/>'
                          f'</g>')
    apron_courses = []
    for r in range(-3, 15):
        cy_a = -80 + r * 78
        a, b = harbor(-240, cy_a), harbor(QUAY_W, cy_a)
        apron_courses.append(f'<path d="M {fmt(a)} L {fmt(b)}" stroke="#9C8B6E" '
                             f'stroke-opacity=".105" stroke-width="2.4" fill="none"/>')
        apron_courses.append(f'<path d="M {fmt((a[0], a[1]+3.0))} L {fmt((b[0], b[1]+3.0))}" '
                             f'stroke="#FFFCF3" stroke-opacity=".16" stroke-width="2.0" fill="none"/>')
        for cxj in (-190, -104, -18) if r % 2 else (-148, -60):
            a2, b2 = harbor(cxj, cy_a), harbor(cxj, cy_a + 78)
            apron_courses.append(f'<path d="M {fmt(a2)} L {fmt(b2)}" stroke="#9C8B6E" '
                                 f'stroke-opacity=".085" stroke-width="2.2" fill="none"/>')
    mid.append('<g clip-path="url(#face0)">' + "".join(apron_courses) + "</g>")
    mid.append("".join(joints))

    # bollards: mouldings with a real body and a cast shadow, not flat dots —
    # the raster's toy-scale read comes largely from these standing proud
    bol = []
    for i in range(N_PIERS):
        y0 = i * (PIER_W + SLIP_W)
        edges = []
        if i > 0:
            edges.append(y0 + 15)
        if i < N_PIERS - 1:
            edges.append(y0 + PIER_W - 15)
        for ey in edges:
            span = PIER_LEN * PIER_SCALE[i]
            for bx in (QUAY_W + span * .24, QUAY_W + span * .58, QUAY_W + span * .90):
                x, y = harbor(bx, ey)
                bol.append(f'<g filter="url(#hair)"><ellipse cx="{x+6.5:.1f}" cy="{y+7.5:.1f}" '
                           f'rx="10.5" ry="6.2" fill="{SHADOW}" fill-opacity=".30"/></g>')
                bol.append(f'<path d="{path_from(rrect(x - 7.4, y - 6.0, 14.8, 15.0, 6.4))}" '
                           f'fill="url(#bollard)"/>')
                bol.append(f'<ellipse cx="{x:.1f}" cy="{y-5.6:.1f}" rx="8.6" ry="5.4" '
                           f'fill="#F6EEDC"/>')
                bol.append(f'<ellipse cx="{x-1.6:.1f}" cy="{y-6.8:.1f}" rx="4.4" ry="2.4" '
                           f'fill="#FFFFFF" fill-opacity=".55"/>')
    mid.append("".join(bol))

    # ---------------- fg: the vessels
    for slip, hx in BERTHS:
        cy_h = slip * (PIER_W + SLIP_W) + PIER_W + SLIP_W / 2 - 7
        c = harbor(hx, cy_h)
        deg = ROT + 180.0            # bow-in: bows point at the quay
        h = placed(hull(), c[0], c[1], deg)
        w = placed(hull_well(), c[0], c[1], deg)
        fg.append(f'<g filter="url(#tight)"><path d="{path_from(offset(h, 7, 11))}" '
                  f'fill="{SHADOW}" fill-opacity=".26"/></g>')
        fg.append(f'<path d="{path_from(offset(h, 0, HULL_WALL))}" fill="url(#claywall)"/>')
        fg.append(f'<path d="{path_from(h)}" fill="url(#clay)"/>')
        fg.append(f'<path d="{path_from(w)}" fill="url(#claywell)"/>')

    ec = EMBER_C
    eh = placed(hull(EMBER_L, EMBER_B), ec[0], ec[1], EMBER_HEADING)
    ew = placed(hull_well(EMBER_L, EMBER_B), ec[0], ec[1], EMBER_HEADING)
    fg.append(f'<g filter="url(#soft)"><path d="{path_from(offset(eh, 14, 24))}" '
              f'fill="{SHADOW}" fill-opacity=".22"/></g>')
    fg.append(f'<g filter="url(#tight)"><path d="{path_from(offset(eh, 7, 12))}" '
              f'fill="{SHADOW}" fill-opacity=".17"/></g>')
    fg.append(f'<path d="{path_from(offset(eh, 0, HULL_WALL))}" fill="#A3300B"/>')
    fg.append(f'<path d="{path_from(eh)}" fill="url(#gel)"/>')
    fg.append(f'<path d="{path_from(ew)}" fill="url(#gelwell)"/>')
    # bounce off the well's far wall — an emissive-looking interior without a
    # second light source, which the era's grammar does not allow
    fg.append(f'<g clip-path="url(#emberwell)" filter="url(#tight)">'
              f'<path d="{path_from(offset(ew, -9, -13))}" fill="#F2601F" fill-opacity=".55"/>'
              f'</g>')
    # lit-edge rim: the key catches the hull's up-light side.  Clipped inside the
    # hull so it is an edge on the object, never a halo around it.
    fg.append(f'<g clip-path="url(#emberclip)" filter="url(#hair)">'
              f'<path d="{path_from(offset(eh, 5.5, 7.5))}" fill="none" stroke="{GEL_RIM}" '
              f'stroke-opacity=".62" stroke-width="7.5"/></g>')

    # Authored overlap — the era's craft tell, and the one thing a flat pre-masked
    # raster cannot fake under tinting: the basin's ripple grain is redrawn clipped
    # to the gel hull in a warm tint, so the water visibly reads THROUGH the vessel.
    defs.append(f'<clipPath id="emberclip"><path d="{path_from(eh)}"/></clipPath>')
    defs.append(f'<clipPath id="emberwell"><path d="{path_from(ew)}"/></clipPath>')
    thru = []
    for p0, p1 in rip_segs:
        thru.append(f'<path d="M {fmt(p0)} L {fmt(p1)}" stroke="#FFD9C2" '
                    f'stroke-opacity=".26" stroke-width="2.8" stroke-linecap="round" fill="none"/>')
    fg.append('<g clip-path="url(#emberclip)" filter="url(#hair)">' + "".join(thru) + "</g>")

    # ---------------- highlight: lit lips and the one soft top light
    for slip, hx in BERTHS:
        cy_h = slip * (PIER_W + SLIP_W) + PIER_W + SLIP_W / 2 - 7
        c = harbor(hx, cy_h)
        h = placed(hull(), c[0], c[1], ROT + 180.0)
        hi.append(f'<path d="{path_from(h)}" fill="url(#topcatch)"/>')
    hi.append(f'<path d="{path_from(eh)}" fill="url(#topcatchwarm)"/>')

    # stone top-edge catch: the lit lip lives on the NORTH edge only, which is
    # what one soft top light actually produces.  Clipping the offset stroke to
    # the solid keeps the south edge dark instead of ringing the shape.
    lip = []
    for i, cmds in enumerate(solids):
        defs.append(f'<clipPath id="lip{i}"><path d="{path_from(cmds)}"/></clipPath>')
        lip.append(f'<g clip-path="url(#lip{i})"><path d="{path_from(offset(cmds, 0, 3.6))}" '
                   f'fill="none" stroke="#FFFDF6" stroke-opacity=".46" stroke-width="4.2"/></g>')
    hi.append('<g filter="url(#hair)">' + "".join(lip) + "</g>")

    # foam at the departing vessel's stern — it lights the water it displaces
    stern = rot_about(ec[0] - EMBER_L / 2 - 8, ec[1], ec[0], ec[1], EMBER_HEADING)
    hi.append(f'<g filter="url(#mist)"><ellipse cx="{stern[0]:.1f}" cy="{stern[1]:.1f}" '
              f'rx="56" ry="27" fill="#FFFFFF" fill-opacity=".42" '
              f'transform="rotate({EMBER_HEADING:.1f} {stern[0]:.1f} {stern[1]:.1f})"/></g>')

    # inner rim light on the tile edge — the cushion, not a print.  Last, because
    # the apron bleeds to the mask and would otherwise cover it.
    hi.append(f'<path d="{sq}" transform="translate(512 512) scale(0.99219) translate(-512 -512)" '
              f'fill="none" stroke="url(#rim)" stroke-width="9"/>')

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" '
            'width="1024" height="1024"><title>ship-fleet</title>\n'
            "<defs>" + "".join(defs) + "</defs>\n"
            '<g clip-path="url(#sq)">\n'
            '<g id="bg">' + "".join(bg) + "</g>\n"
            '<g id="mid">' + "".join(mid) + "</g>\n"
            '<g id="fg">' + "".join(fg) + "</g>\n"
            '<g id="highlight">' + "".join(hi) + "</g>\n"
            "</g>\n</svg>\n")


# ---------------------------------------------------------------- lane + wake
def wake_points():
    ec = EMBER_C
    stern = rot_about(ec[0] - HULL_L / 2, ec[1], ec[0], ec[1], EMBER_HEADING)
    b = harbor(HARBOR_W - 20, PIER_W + SLIP_W / 2)
    a = harbor(QUAY_W + 76, PIER_W + SLIP_W / 2)
    pts = []
    for i in range(15):
        t = i / 14
        p0 = (stern[0] + (b[0] - stern[0]) * t, stern[1] + (b[1] - stern[1]) * t)
        p1 = (b[0] + (a[0] - b[0]) * t, b[1] + (a[1] - b[1]) * t)
        pts.append((p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t))
    return pts


def normal(a, b, d):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    return (-dy / n * d, dx / n * d)


if __name__ == "__main__":
    (HERE / "icon.svg").write_text(build())
    print("wrote", HERE / "icon.svg")
