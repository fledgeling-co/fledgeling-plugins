#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the anvil-errand icon.

Direction "The Return Arc": Tahoe gel-glass sub-register (c), the DARK register -
a cool forge-charcoal cushion tile - crossed with the picker's monochrome-metal
palette overlay for the steel, and Direction 4's emissive discipline for the one
warm source. Device bank #5 (dual-function primitive), #22 (emissive interior as
the second light) and #16 (the icon performs the verb).

The subject is one verb that sends a Claude Code agent to work in a container on
a machine that is not this one, and brings the result back. Anvil's own metaphor
is a forge: this Mac is the trust root, the other machine is where the work is
struck. So the icon is an anvil seen in profile - and the anvil's HORN is drawn
as a true taper to a point, so the whole tool reads a second time as an arrow
aimed away from the viewer. That is the dual function: the thing you strike work
on IS the thing that points at where the work goes.

The signature move is the return arc. One incandescent ribbon leaves the horn's
tip, climbs across the empty upper right of the tile, turns, and comes back down
onto the billet resting on the face - thin where it departs, thick where it
arrives, so the direction of travel reads as ARRIVING. Out and back is the whole
of "errand", and it costs one stroke rather than a second object.

Ground values are sampled, not assumed, from the two dark-register captures in
the skill's macOS 26 corpus (apple-03 near-black navy, grade A; apple-21
charcoal, grade B): both ramp LIGHTER AT TOP - #323550 -> #222436 and
#303031 -> #141514 - with the perimeter rim barely above the top ground and the
figure-ground work done by rim light on the object rather than by ground hue.
The steel body is therefore authored well above the ground in value so the
silhouette survives grayscale and a mono tint on shape alone; the warm accent is
reserved entirely for the focal, and it is EARNED - incandescent metal really is
that colour, which is the positive justification the corpus asks for before any
icon spends its accent.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight. The anvil body
lives in #mid and carries the identity by itself; every warm element is #fg or
#highlight and is droppable, which is what rubric #10 asks for.

Every constant below is named; a fidelity round is a parameter edit, never path
surgery.
"""

import math
import pathlib

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- palette --
# Two hue families only (rubric #6): a cool steel/navy family for tile + tool,
# and a warm incandescent family reserved for the focal work.

TILE_TOP = "#2F3242"        # measured register: apple-03 top #323550, cooled
TILE_BOT = "#191B24"        # apple-03 bottom #222436 / apple-21 #141514
TILE_RIM = "#8E96B4"        # perimeter inner rim light, very low opacity
VIGNETTE = "#0D0E14"

STEEL_HI = "#DCE2ED"        # face top, catching the key
STEEL_MID = "#A8B2C4"       # picker's monochrome-metal ramp, middle stop
# r5: these two were #4C5365 and #343A48, which MEASURED 1.81:1 at the waist and
# 1.59:1 at the base against the tile beneath them - so the bottom half of the
# tool dissolved into the ground and rubric #7's 3:1 failed on most of the
# silhouette, which is exactly why the icon kept reading as a slab on a table.
# Lifted until every part of the anvil clears 3:1 against its LOCAL ground, which
# is what the dark register costs: on a near-black tile the object cannot also be
# dark, and the corpus's own dark captures carry their objects well above it.
STEEL_LO = "#7A8394"        # waist, turning away from the key
STEEL_BASE = "#646E82"      # base slab, deepest
STEEL_RIM = "#F2F5FA"       # rim light on top edges

HOT_CORE = "#FFF3D6"        # the billet's centre - the brightest pixel present
HOT_MID = "#FFB055"
HOT_EDGE = "#F0601A"
HOT_DEEP = "#A82F06"        # the forge bloom under everything
BOUNCE = "#FF9A46"          # warm light thrown back onto the steel

# --------------------------------------------------------------- geometry --
# The anvil in profile, horn to the right. Authored around an origin that is
# then shifted once, globally, so optical centring is a single pair of numbers
# rather than an edit to twelve coordinates.

OFF_X, OFF_Y = 6.0, -6.0

# r2: the first draft's face was 88 units thick over a 652 span and its horn ran
# 236 units to a needle - at 32px that is a blade on a pedestal, and the whole
# icon read as a clothes iron. The face is now chunky enough to be a face, the
# horn short enough to be a horn, and the waist stouter than it is tall.
FACE_TOP = 330.0            # the working face - the top surface of the tool
FACE_BOT = 466.0            # underside of the face slab; the body hangs below
HEEL_X = 226.0              # the square left end
HORN_X0 = 636.0             # where the face stops and the horn begins
# r3: the tip was on the face's mid-line, so the horn tapered symmetrically and
# read as a knife point. On a real anvil the horn's TOP edge carries on nearly
# level from the face and the UNDERSIDE rises to meet it, which puts the tip in
# the face's upper third. That one number is most of the difference between a
# blade and a horn.
HORN_TIP = (846.0, 372.0)   # the point. This is the arrowhead.
HORN_TIP_R = 9.0            # r4: a blunt tip. At 32px this is a third of a pixel
                            # and invisible; what it removes is the aliased
                            # needle the renderer makes of a true point.

# r3: the waist was 118 units against a 388-unit face - 30%, which is a goblet
# stem, not an anvil. A real anvil's waist is about half its face and its foot
# flares back to about three quarters. Face centre 431, waist centre 440, base
# centre 441: the three stay stacked, which is what stops it leaning.
WAIST_L_TOP, WAIST_R_TOP = 286.0, 588.0   # body where it meets the face
WAIST_Y = 570.0
WAIST_L, WAIST_R = 338.0, 542.0           # narrowest point - 204 wide
BASE_TOP, BASE_BOT = 656.0, 748.0
BASE_L, BASE_R = 286.0, 596.0             # 310 wide
BASE_R_CORNER = 18.0
# r6, salvaged from the other two engines: BOTH the Arrow vector take and the
# GPT Image raster drew the foot as an arch between two feet, where this master
# had a plain slab. Two independent engines converging on an anatomy the master
# lacked is the strongest evidence available here that the slab was wrong, and it
# costs one curve. It also puts a hole in the silhouette's heaviest region, which
# is what stops the bottom third reading as a plinth.
FOOT_W = 78.0               # each foot's width
ARCH_RISE = 44.0            # how far the arch cuts up into the base

# The work: a billet of hot metal resting on the face, left of the horn so the
# tool still reads before the glow does.
BILLET_X0, BILLET_X1 = 452.0, 572.0
BILLET_Y0, BILLET_Y1 = 296.0, 348.0       # overlaps the face: it is ON it
BILLET_R = 26.0

# The return arc: horn tip -> up across the empty upper right -> back to the
# billet. Widths are (at the horn tip, at the billet): thin where it leaves,
# thick where it arrives.
#
# r2: the far end used to be 3 units wide at full-ish opacity and it TOUCHED the
# horn tip, which closed a loop over the tool and read as a kettle handle. It now
# tapers to nothing and fades to zero, so what is visible is a comet arriving at
# the work with its tail dissolving out past the horn - a trajectory cannot be
# grasped, which is the whole difference.
ARC_W_FAR, ARC_W_NEAR = 0.6, 19.0
ARC_SAMPLES = 96


def sh(p):
    """Apply the one global offset."""
    return (p[0] + OFF_X, p[1] + OFF_Y)


def f(v):
    return f"{v:.2f}"


# ------------------------------------------------------------ curve helpers --

def bez(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (
        u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
        u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1],
    )


def bez_d(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (
        3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
        3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]),
    )


def ribbon(p0, p1, p2, p3, w_start, w_end, n=ARC_SAMPLES):
    """A cubic swept with a linearly varying half-width, as a closed polygon.

    A tapered stroke is not something SVG can express, and faking it with a
    stroke-width gradient does not exist either - so the taper is built as real
    geometry. That is what makes the direction of travel legible.
    """
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_d(p0, p1, p2, p3, t)
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m, dx / m
        # ease the taper so the thin end does not vanish instantly
        w = (w_start + (w_end - w_start) * (t ** 0.72)) * 0.5
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    return "M" + " ".join(f"{f(x)},{f(y)}" for x, y in pts) + "Z"


# ------------------------------------------------------------- the outline --

def anvil_path():
    """The anvil silhouette, clockwise from the heel's top-left corner.

    Returns (path string, flattened point list) - the point list is what the
    centroid and bbox report below are computed from, so the optical-centring
    claim is measured off the same geometry that ships.
    """
    hx, hy = HORN_TIP
    seg = []
    pts = []

    def line_to(p):
        seg.append(f"L{f(p[0])},{f(p[1])}")
        pts.append(p)

    def curve_to(c1, c2, p, frm):
        seg.append(f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p[0])},{f(p[1])}")
        for i in range(1, 17):
            pts.append(bez(frm, c1, c2, p, i / 16))

    start = sh((HEEL_X, FACE_TOP))
    seg.append(f"M{f(start[0])},{f(start[1])}")
    pts.append(start)

    # the working face, left to right
    line_to(sh((HORN_X0, FACE_TOP)))

    # horn, top edge: a shallow convex sweep out to the point
    a = sh((HORN_X0, FACE_TOP))
    tip_hi = sh((hx, hy - HORN_TIP_R))
    tip_lo = sh((hx, hy + HORN_TIP_R))
    curve_to(sh((HORN_X0 + 104, FACE_TOP - 4)), sh((hx - 78, hy - 34)), tip_hi, a)

    # the blunt tip itself
    curve_to(sh((hx + 8, hy - HORN_TIP_R)), sh((hx + 8, hy + HORN_TIP_R)), tip_lo, tip_hi)

    # horn, underside: concave, returning to the face's underside
    b = sh((HORN_X0, FACE_BOT))
    curve_to(sh((hx - 92, hy + 34)), sh((HORN_X0 + 110, FACE_BOT + 6)), b, tip_lo)

    # underside of the face slab, right portion
    line_to(sh((WAIST_R_TOP, FACE_BOT)))

    # body: right edge in to the waist, then out to the base
    c = sh((WAIST_R_TOP, FACE_BOT))
    curve_to(sh((WAIST_R_TOP - 30, FACE_BOT + 62)), sh((WAIST_R, WAIST_Y - 62)),
             sh((WAIST_R, WAIST_Y)), c)
    d = sh((WAIST_R, WAIST_Y))
    curve_to(sh((WAIST_R + 26, WAIST_Y + 44)), sh((BASE_R - 26, BASE_TOP - 30)),
             sh((BASE_R, BASE_TOP)), d)

    # the base slab, with the arch cut up into it between two feet
    line_to(sh((BASE_R, BASE_BOT - BASE_R_CORNER)))
    e = sh((BASE_R, BASE_BOT - BASE_R_CORNER))
    curve_to(sh((BASE_R, BASE_BOT)), sh((BASE_R - BASE_R_CORNER, BASE_BOT)),
             sh((BASE_R - BASE_R_CORNER, BASE_BOT)), e)
    line_to(sh((BASE_R - FOOT_W, BASE_BOT)))
    ar = sh((BASE_R - FOOT_W, BASE_BOT))
    curve_to(sh((BASE_R - FOOT_W, BASE_BOT - ARCH_RISE * 1.34)),
             sh((BASE_L + FOOT_W, BASE_BOT - ARCH_RISE * 1.34)),
             sh((BASE_L + FOOT_W, BASE_BOT)), ar)
    line_to(sh((BASE_L + BASE_R_CORNER, BASE_BOT)))
    g = sh((BASE_L + BASE_R_CORNER, BASE_BOT))
    curve_to(sh((BASE_L, BASE_BOT)), sh((BASE_L, BASE_BOT)),
             sh((BASE_L, BASE_BOT - BASE_R_CORNER)), g)
    line_to(sh((BASE_L, BASE_TOP)))

    # body: left edge in to the waist, then back up to the face
    h = sh((BASE_L, BASE_TOP))
    curve_to(sh((BASE_L + 26, BASE_TOP - 30)), sh((WAIST_L - 26, WAIST_Y + 44)),
             sh((WAIST_L, WAIST_Y)), h)
    i = sh((WAIST_L, WAIST_Y))
    curve_to(sh((WAIST_L, WAIST_Y - 62)), sh((WAIST_L_TOP + 30, FACE_BOT + 62)),
             sh((WAIST_L_TOP, FACE_BOT)), i)

    # underside of the face slab, left portion, and up the heel
    line_to(sh((HEEL_X, FACE_BOT)))
    seg.append("Z")
    return " ".join(seg), pts


def centroid(pts):
    """Area centroid of the flattened outline - the optical-centring check."""
    a = cx = cy = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a *= 0.5
    return (cx / (6 * a), cy / (6 * a), abs(a))


# -------------------------------------------------------------------- build --

def build():
    path, pts = anvil_path()
    bx0 = min(p[0] for p in pts); bx1 = max(p[0] for p in pts)
    by0 = min(p[1] for p in pts); by1 = max(p[1] for p in pts)
    cx, cy, area = centroid(pts)

    billet = (
        f'<rect x="{f(BILLET_X0 + OFF_X)}" y="{f(BILLET_Y0 + OFF_Y)}" '
        f'width="{f(BILLET_X1 - BILLET_X0)}" height="{f(BILLET_Y1 - BILLET_Y0)}" '
        f'rx="{f(BILLET_R)}" ry="{f(BILLET_R)}"'
    )
    bcx = (BILLET_X0 + BILLET_X1) / 2 + OFF_X
    bcy = (BILLET_Y0 + BILLET_Y1) / 2 + OFF_Y

    # the return arc, horn tip -> up over the empty upper right -> the billet
    arc = ribbon(
        sh((HORN_TIP[0] + 12, HORN_TIP[1] - 6)),
        sh((HORN_TIP[0] + 66, HORN_TIP[1] - 150)),
        sh((HORN_TIP[0] - 210, HORN_TIP[1] - 250)),
        (bcx + 34, bcy - 34),
        ARC_W_FAR, ARC_W_NEAR,
    )

    defs = f'''
<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{TILE_TOP}"/><stop offset="1" stop-color="{TILE_BOT}"/>
</linearGradient>
<radialGradient id="vig" cx="0.5" cy="0.44" r="0.78">
  <stop offset="0.52" stop-color="{VIGNETTE}" stop-opacity="0"/>
  <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.55"/>
</radialGradient>
<radialGradient id="forge" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{HOT_EDGE}" stop-opacity="0.40"/>
  <stop offset="0.55" stop-color="{HOT_DEEP}" stop-opacity="0.14"/>
  <stop offset="1" stop-color="{HOT_DEEP}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="steel" x1="0" y1="{f(by0)}" x2="0" y2="{f(by1)}" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{STEEL_HI}"/>
  <stop offset="0.16" stop-color="{STEEL_MID}"/>
  <stop offset="0.62" stop-color="{STEEL_LO}"/>
  <stop offset="1" stop-color="{STEEL_BASE}"/>
</linearGradient>
<linearGradient id="underface" x1="0" y1="{f(FACE_BOT + OFF_Y)}" x2="0" y2="{f(FACE_BOT + OFF_Y + 74)}" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="#000000" stop-opacity="0.28"/>
  <stop offset="1" stop-color="#000000" stop-opacity="0"/>
</linearGradient>
<radialGradient id="bounce" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{BOUNCE}" stop-opacity="0.62"/>
  <stop offset="1" stop-color="{BOUNCE}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="hot" cx="0.42" cy="0.34" r="0.78">
  <stop offset="0" stop-color="{HOT_CORE}"/>
  <stop offset="0.44" stop-color="{HOT_MID}"/>
  <stop offset="1" stop-color="{HOT_EDGE}"/>
</radialGradient>
<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{HOT_MID}" stop-opacity="0.85"/>
  <stop offset="0.42" stop-color="{HOT_EDGE}" stop-opacity="0.34"/>
  <stop offset="1" stop-color="{HOT_EDGE}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="arcg" x1="{f(HORN_TIP[0] + OFF_X)}" y1="0" x2="{f(bcx)}" y2="0" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{HOT_EDGE}" stop-opacity="0"/>
  <stop offset="0.34" stop-color="{HOT_EDGE}" stop-opacity="0.42"/>
  <stop offset="0.66" stop-color="{HOT_MID}" stop-opacity="0.88"/>
  <stop offset="1" stop-color="{HOT_CORE}" stop-opacity="1"/>
</linearGradient>
<linearGradient id="rimtop" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{TILE_RIM}" stop-opacity="0.34"/>
  <stop offset="0.5" stop-color="{TILE_RIM}" stop-opacity="0.10"/>
  <stop offset="1" stop-color="{TILE_RIM}" stop-opacity="0.16"/>
</linearGradient>
<filter id="bS" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="5"/></filter>
<filter id="bM" x="-60%" y="-60%" width="220%" height="220%">
  <feGaussianBlur stdDeviation="16"/></filter>
<filter id="bL" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur stdDeviation="46"/></filter>
<clipPath id="tileClip"><path d="{SQUIRCLE}"/></clipPath>
<clipPath id="anvilClip"><path d="{path}"/></clipPath>
'''

    bg = f'''
  <rect width="{W}" height="{W}" fill="url(#tile)"/>
  <ellipse cx="{f(cx)}" cy="{f(by1 - 24)}" rx="470" ry="330" fill="url(#forge)"/>
  <rect width="{W}" height="{W}" fill="url(#vig)"/>
  <path d="{SQUIRCLE}" fill="none" stroke="url(#rimtop)" stroke-width="3"/>
'''

    mid = f'''
  <ellipse cx="{f(cx)}" cy="{f(by1 + 6)}" rx="212" ry="26" fill="#000000" fill-opacity="0.42" filter="url(#bM)"/>
  <path d="{path}" fill="url(#steel)"/>
  <g clip-path="url(#anvilClip)">
    <rect x="0" y="{f(FACE_BOT + OFF_Y)}" width="{W}" height="78" fill="url(#underface)"/>
    <ellipse cx="{f(bcx)}" cy="{f(FACE_TOP + OFF_Y + 6)}" rx="226" ry="118" fill="url(#bounce)"/>
  </g>
'''

    fg = f'''
  <ellipse cx="{f(bcx)}" cy="{f(bcy + 4)}" rx="150" ry="118" fill="url(#bloom)" filter="url(#bM)"/>
  <path d="{arc}" fill="url(#arcg)" filter="url(#bS)"/>
  <path d="{arc}" fill="url(#arcg)"/>
  {billet} fill="url(#hot)"/>
  {billet} fill="none" stroke="{HOT_CORE}" stroke-opacity="0.55" stroke-width="2"/>
'''

    hl = f'''
  <g clip-path="url(#anvilClip)">
    <rect x="0" y="{f(FACE_TOP + OFF_Y - 1)}" width="{W}" height="7"
          fill="{STEEL_RIM}" fill-opacity="0.92" filter="url(#bS)"/>
    <path d="{path}" fill="none" stroke="{STEEL_RIM}" stroke-opacity="0.44"
          stroke-width="6" filter="url(#bS)"/>
  </g>
  <ellipse cx="{f(bcx)}" cy="{f(bcy)}" rx="96" ry="74" fill="url(#bloom)" filter="url(#bL)"/>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">
<defs>{defs}</defs>
<g clip-path="url(#tileClip)">
<g id="bg">{bg}</g>
<g id="mid">{mid}</g>
<g id="fg">{fg}</g>
<g id="highlight">{hl}</g>
</g>
</svg>
'''
    return svg, dict(bbox=(bx0, bx1, by0, by1), cx=cx, cy=cy, area=area)


if __name__ == "__main__":
    svg, info = build()
    out = ASSETS / "icon.svg"
    out.write_text(svg)
    bx0, bx1, by0, by1 = info["bbox"]
    print(f"wrote {out} ({len(svg)} bytes)")
    print(f"  focal bbox   x {bx0:.0f}..{bx1:.0f}   y {by0:.0f}..{by1:.0f}")
    print(f"  focal size   {(bx1-bx0)/W*100:.1f}% of tile width, {(by1-by0)/W*100:.1f}% of height")
    print(f"  area centroid ({info['cx']:.0f}, {info['cy']:.0f})  vs canvas centre (512, 512)")
    print(f"  margins      L {bx0:.0f}  R {W-bx1:.0f}  T {by0:.0f}  B {W-by1:.0f}")
