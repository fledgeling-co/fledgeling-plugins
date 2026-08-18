#!/usr/bin/env python3
"""Build the proctor icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

    python3 build_icon.py            # writes icon.svg beside this file

THE SUBJECT — "The Side Port"
-----------------------------
A sealed graphite instrument case, three-quarter oblique on porcelain, whose
front face is a bolted-shut access cover with nothing to operate, and whose
right flank carries a raised boss with an ember drive quill seated in it — a hex
union nut, a short shaft and a chamfered end ring.

Proctor's proudest mechanism is the *process-directed plane*: it actuates a Mac
app through IPC — accessibility actions, Apple Events, the app's own declared
scripting contract — rather than through the one shared system event stream. So
it reaches windows that are not frontmost, that are occluded, that are on
another Space, and it reaches them **without stealing focus**. The synthetic
plane is the other option, and it needs the app in front, disturbing whoever is
using the machine.

That is what this object says, and it says it as one physical fact rather than
as a diagram: the front is sealed, and the drive goes in the side.

SIGNATURE MOVE: the front face carries no control of any kind — a recessed
panel with four fasteners — while the only warm thing in the tile is the quill
entering the flank. The accent is on the semantic element and nowhere else.

Not a window stack: the predecessor drew a line-art window outline with a
decorative orange mosaic field, was the only outline in a family of modelled
objects, and measured 0.108 luminance std at 16px against a family median of
0.176. It also shared a three-grey-circles window device with mac-craft. No
panels, no plates in depth (mockup-fidelity), no reticle (design-review), no
lens (be-my-witness).

MEASURED VALUES (nothing here was assumed)
------------------------------------------
Ground truth, `create-mac-icon/references/corpus/apple-2026/`:
  apple-12 (Calculator — a dark machined instrument on porcelain with warm
    accent keys; the closest register in the corpus to this commission):
      ground L 0.874 at the top falling to 0.740 at the bottom — a WIDE ramp of
        0.134, essentially neutral (S 0.004-0.016, H 60);
      graphite front face L 0.159 at its upper edge rising to 0.303 at its
        lower edge — the body is LIGHTER at the bottom, because the porcelain
        bounces up into it. Authored here; a monotonic top-lit ramp gets this
        backwards.
      warm accent H 31.1, S 0.834, V 0.988 -> L 0.645. Apple's accent on a
        graphite body is brighter and yellower than this family's #E9562A
        (L 0.447). The hue stays the family's; the LIT crest borrows Apple's
        luminance, because at the family value alone the quill goes brown
        against porcelain.
  apple-27 (loupe — anodised graphite on a porcelain-blue ground):
      barrel flanks L 0.115-0.122, front face L 0.181, lit top rim L 0.651.
      darkest 1% of the tile: L 0.086 at H 0 / S 0.033 — the darkest graphite
        pixel is NEUTRAL, faintly warm. Not blue. (material-recipes carries
        three separate entries on shadows authored blue in a warm-lit scene.)
  apple-30 (boxy toy machine, warm ground) — per-face separation on ONE
    material: top 0.965, front 0.752, flank 0.413. top:flank = 2.34:1.
  apple-18 (porcelain + toy object) — ground 0.996 falling to 0.922, a NARROW
    high ramp of 0.074; contact shadow a WIDE SHALLOW pool at -0.058 L plus a
    NARROW SEAT at -0.114 L, hue preserved, faintly cool-neutral.

This master takes apple-18's high narrow ground ramp (the object is very dark,
so the ground is spent on figure-ground rather than on drama) with apple-12's
per-face graphite values and its bottom-edge bounce. Measured back off the
shipped 1024 render: top face L 0.328, front face L 0.141, flank L 0.10, so
top:flank is 3.3:1 — between apple-30's matte 2.34 and apple-27's anodised 5.6,
because a graphite box whose three faces sit within 0.05 L of each other reads as
one black blob at 128px, and the first draft did.

PROJECTION
----------
Cavalier oblique. u = the case's width, running very slightly uphill so the
front face is not a dead rectangle; v = depth, receding up-and-right,
foreshortened to 0.59; w = height, straight up. One affine basis, so every
gradient rides the geometry for free.

Visible faces: top (+w), front (-v), right flank (+u). The flank is the darkest
of the three and it is the one the drive enters, which puts the ember against
the deepest graphite in the tile.

LIGHT AND CURVED SURFACES
-------------------------
One key, upper-left and in front: KEY_DIR in (u, v, w). Flat faces take the
measured constants above.

Every cylinder is ONE path whose fill is a multi-stop gradient *derived* from
the same key: for each angle round the visible arc, the band's Lambert term
gives the colour and its projected offset perpendicular to the tube's own axis
gives the stop position. The gradient's iso-lines are therefore parallel to the
tube axis by construction. The first draft banded each cylinder into 28 flat
quads instead, and rsvg antialiased every seam into a thin light line — the
quill read as corrugated hose. Derive the gradient; do not tile the surface.

A cylinder's own outline is its two cap ellipses' convex hull, not the swept
front-facing band. The band leaves the back of each cross-section unpainted, so
the piece behind shows through as a stray ellipse — and a per-assembly falloff
laid over a convex hull washes the porcelain in every concavity the hull bridges.
Paint the hull, cap it, and give a cylinder no falloff along its own axis at all:
its normal has no component along that axis, so the Lambert term is constant
there and any ramp along it is invented light.

WHY THE QUILL ENDS IN A HEX
---------------------------
It ended in a round barrel for one draft, and a graphite box with a coaxial
round barrel on its face is a camera — which is the single worst read available
in this family, since design-review owns the reticle and be-my-witness owns the
lens. A hex union nut, torqued flat against the boss and low on the flank rather
than centred on it, reads as a fitting and cannot read as an optic. Its three
visible flats also take three separate Lambert values (0.80, 0.77, 0.03), which
is more per-face separation than a smooth barrel of the same size can carry.
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024

# ------------------------------------------------------------------ projection
# P(u, v, w) = O + u*E1 + v*E2 + w*E3
O = (291.0, 764.0)          # the casting's front-bottom-left corner, on the ground
E1 = (1.0, -0.035)          # width axis, running slightly uphill to the right
E2 = (0.40, -0.430)         # depth axis, receding up-right, 0.59 foreshortened
E3 = (0.0, -1.0)            # height axis

# ------------------------------------------------------------------- the case
UW = 292.0                  # width — PORTRAIT, deliberately: a landscape case
VD = 216.0                  # with a coaxial fitting on its flank is a camcorder,
HH = 424.0                  # whatever the fitting is shaped like
PLINTH_H = 0.0              # flush; see the note in the mid layer
PLINTH_OUT = 20.0           # only read when PLINTH_H > 0
TOPW = PLINTH_H + HH
ARRIS_W = 9.0               # the lit-edge catch on the top and left arrises

# The bolted access panel on the front face: recessed, no controls, four
# fasteners. Per material-recipes (anvil-errand) a recess's walls are not lit
# bands — fill it with the shadow it casts and skip the walls entirely.
BODY_R = 34.0               # the casting's radius on the body
PLINTH_R = 16.0             # and on the plinth
FILLET_W = 20.0             # the dark fillet along the front/flank arris
PANEL_R = 18.0              # the access cover's own corner radius
PANEL_INSET_U = 44.0
PANEL_INSET_W = 52.0
PANEL_DEPTH = 15.0
FASTENER_R = 9.5
FASTENER_PAD = 27.0

# --------------------------------------------------------------- the side drive
# A stepped coaxial assembly entering the flank at u = UW. Offsets below are in
# u from that flank. Boss = the case's own casting, so graphite: the accent is
# reserved for the part Proctor brings. Each outward step is thinner than the
# last, so the quill reads as seated rather than as a separate object.
DRIVE_V = VD / 2            # mid-depth on the flank
DRIVE_W = PLINTH_H + HH * 0.40   # LOW on the flank, not centred on it — a
                                 # centred round protrusion reads as a lens
BOSS_R, BOSS_U0, BOSS_U1 = 76.0, 0.0, 34.0      # the case's own casting
NUT_R, NUT_U0, NUT_U1 = 82.0, 32.0, 106.0       # hex union nut, circumradius
SHAFT_R, SHAFT_U0, SHAFT_U1 = 44.0, 102.0, 192.0
END_R, END_U0, END_U1 = 53.0, 186.0, 210.0      # the chamfered end ring
ARC_STOPS = 22              # gradient stops round each cylinder's visible arc

# ---------------------------------------------------------------------- light
KEY_DIR = (-0.42, -0.48, 0.77)      # unit: upper-left, in front, above
VIEW_DIR = (0.371, -0.883, 0.287)   # toward the viewer, derived from E1/E2/E3

# ---------------------------------------------------------------------- palette
GROUND_HI = "#FDFCFA"       # L 0.987 — apple-18's brightest, at frac (0.34,0.02)
GROUND_MID = "#F5F2EC"      # L 0.951
GROUND_LO = "#E9E4DA"       # L 0.897 — the measured 0.074 fall, warm
VIGNETTE = "#C9BFAC"
RIM_TILE = "#FFFFFF"

SHADOW_POOL = "#C2BBAD"     # the wide shallow pool, -0.058 L, hue preserved
SHADOW_SEAT = "#928A7C"     # the narrow seat, -0.114 L
SHADOW_CONTACT = "#6A6357"  # the line of true contact under the front arris
SEAT_OUT = 22.0             # how far the seat spreads past the footprint

TOP_HI = "#6C6966"          # top face, lit end        L 0.404
TOP_LO = "#403D3B"          # top face, far end        L 0.242
FRONT_LO = "#242322"        # front face, upper edge   L 0.139
FRONT_HI = "#302E2C"        # front face, lower edge   L 0.182 (+ bounce below)
FLANK_HI = "#1B1A19"        # flank, near edge         L 0.104
FLANK_LO = "#141313"        # flank, far edge          L 0.079 (apple-27's floor)
PANEL_FACE = "#302E2C"      # the recessed panel       L 0.182
PANEL_SHADE = "#111010"     # the shadow the recess casts into itself
FASTENER = "#403D3B"
FASTENER_LIT = "#7C7673"
PLINTH_TOP = "#5A5654"      # same normal as the body top, so the same value
PLINTH_FRONT = "#2A2827"    # ditto the front
PLINTH_FLANK = "#1A1918"    # ditto the flank
ARRIS_CATCH = "#9A938E"     # the lit-edge catch, L 0.58
FILLET_DARK = "#100F0F"     # the arris fillet's floor, L 0.062
BOUNCE = "#E0AE78"          # porcelain bounce into the body's lower edge

EMBER_CREST = "#FFB77F"     # crest,        L 0.755 — Apple's accent luminance
EMBER_HI = "#FA7C3D"        # key-lit,      L 0.572
EMBER_MID = "#E9562A"       # the family's shared accent, L 0.447
EMBER_LO = "#A63419"        # turning away, L 0.298
EMBER_DEEP = "#57190A"      # terminator,   L 0.146
EMBER_BOUNCE = "#F6A873"    # the underside catch off the porcelain

GRAPHITE_RAMP = [(-1.0, "#0D0C0C"), (-0.2, "#161514"), (0.15, "#282625"),
                 (0.50, "#4B4746"), (0.91, "#8A8380")]
EMBER_RAMP = [(-1.0, EMBER_DEEP), (-0.15, "#78230F"), (0.10, EMBER_LO),
              (0.42, EMBER_MID), (0.68, EMBER_HI), (0.91, EMBER_CREST)]


# ------------------------------------------------------------------- utilities
def P(u: float, v: float, w: float) -> tuple[float, float]:
    return (O[0] + u * E1[0] + v * E2[0] + w * E3[0],
            O[1] + u * E1[1] + v * E2[1] + w * E3[1])


def poly(pts) -> str:
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


def face(pts3) -> str:
    return poly([P(*p) for p in pts3])


def hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_hex(c) -> str:
    return "#" + "".join(f"{max(0, min(255, round(x * 255))):02X}" for x in c)


def ramp(stops, t: float) -> str:
    """Sample a (Lambert -> hex) ramp in sRGB. One ramp per material, one key."""
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            a, b = hex_rgb(c0), hex_rgb(c1)
            return rgb_hex([a[i] + (b[i] - a[i]) * f for i in range(3)])
    return stops[-1][1]


def lambert(nv) -> float:
    return sum(KEY_DIR[i] * nv[i] for i in range(3))


def hull(points):
    """Monotone-chain convex hull. Used for the mask that keeps the tile's rim
    light off an occluder standing in front of it, and for the cast shadow."""
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2:
                (x1, y1), (x2, y2) = out[-2], out[-1]
                if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) > 0:
                    break
                out.pop()
            out.append(p)
        return out

    return half(pts)[:-1] + half(pts[::-1])[:-1]


# ------------------------------------------------------------ curved surfaces
def circle3(u, vc, wc, r, theta):
    """A point on a circle in the (v, w) plane at fixed u. theta = 90 deg is +w
    (up); theta = 180 deg faces the viewer."""
    return (u, vc + r * math.cos(theta), wc + r * math.sin(theta))


def visible_arc():
    """The angular range whose normals face the viewer — solved from VIEW_DIR
    rather than guessed: cos(t)*VIEW_v + sin(t)*VIEW_w > 0."""
    t = math.atan2(VIEW_DIR[2], VIEW_DIR[1])
    return t - math.pi / 2 + 0.015, t + math.pi / 2 - 0.015


def unit(p):
    n = math.hypot(*p)
    return (p[0] / n, p[1] / n)


def arc_gradient(ident, u0, u1, vc, wc, r, stops):
    """The multi-stop gradient for one cylinder, derived from the one key.

    Axis = the cross-section's extent measured PERPENDICULAR to the tube's own
    screen axis, so the gradient's iso-lines run along the tube. Each stop's
    colour is that angle's Lambert term; its offset is where that angle projects
    onto the axis. Nothing is placed by eye.
    """
    t0, t1 = visible_arc()
    thetas = [t0 + (t1 - t0) * k / (ARC_STOPS - 1) for k in range(ARC_STOPS)]
    e1 = unit(E1)
    nperp = (-e1[1], e1[0])
    umid = 0.5 * (u0 + u1)
    mid = [P(*circle3(umid, vc, wc, r, th)) for th in thetas]
    s = [(q[0] - mid[0][0]) * nperp[0] + (q[1] - mid[0][1]) * nperp[1] for q in mid]
    lo, hi = min(s), max(s)
    a = (mid[0][0] + (lo - s[0]) * nperp[0], mid[0][1] + (lo - s[0]) * nperp[1])
    b = (mid[0][0] + (hi - s[0]) * nperp[0], mid[0][1] + (hi - s[0]) * nperp[1])
    seen = sorted(((sv - lo) / (hi - lo),
                   ramp(stops, lambert((0.0, math.cos(th), math.sin(th)))))
                  for th, sv in zip(thetas, s))
    body = "".join(f'<stop offset="{o:.4f}" stop-color="{c}"/>' for o, c in seen)
    return (f'<linearGradient id="g{ident}" x1="{a[0]:.2f}" y1="{a[1]:.2f}" '
            f'x2="{b[0]:.2f}" y2="{b[1]:.2f}" gradientUnits="userSpaceOnUse">'
            f'{body}</linearGradient>')


def ring(u, vc, wc, r, n=60):
    return [P(*circle3(u, vc, wc, r, 2 * math.pi * k / n)) for k in range(n)]


def tube(u0, u1, vc, wc, r, stops, ident):
    """A cylinder along +u: its own outline (the convex hull of both cap
    ellipses, so no cross-section is left unpainted) filled with the derived
    gradient. Returns (paths, outline, gradient)."""
    sil = hull(ring(u0, vc, wc, r) + ring(u1, vc, wc, r))
    paths = [f'<path id="{ident}" d="{poly(sil)}" fill="url(#g{ident})"/>']
    return paths, sil, arc_gradient(ident, u0, u1, vc, wc, r, stops)


def cap(u, vc, wc, r, stops, ident):
    """The shoulder facing +u. KEY_DIR[0] < 0, so every outward shoulder in this
    assembly is in shade — which is exactly what makes the steps read."""
    pts = ring(u, vc, wc, r)
    col = ramp(stops, lambert((1.0, 0.0, 0.0)))
    return f'<path id="{ident}" d="{poly(pts)}" fill="{col}"/>', pts


# ------------------------------------------------------------------ rounded box
def round_poly(pts, r):
    """A closed path through pts with every corner cut back by r and joined with
    a quadratic through the original vertex. A box in this projection has a
    convex hexagonal silhouette, so one rounded hexagon per box is enough to
    give the whole casting a radius — which is the raster takes' loudest
    material cue and the one a hard-edged oblique box cannot fake."""
    n = len(pts)
    out = []
    for i in range(n):
        prev, cur, nxt = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        d0 = math.hypot(cur[0] - prev[0], cur[1] - prev[1])
        d1 = math.hypot(nxt[0] - cur[0], nxt[1] - cur[1])
        f0 = min(r, d0 * 0.45) / max(d0, 1e-6)
        f1 = min(r, d1 * 0.45) / max(d1, 1e-6)
        a = (cur[0] + (prev[0] - cur[0]) * f0, cur[1] + (prev[1] - cur[1]) * f0)
        b = (cur[0] + (nxt[0] - cur[0]) * f1, cur[1] + (nxt[1] - cur[1]) * f1)
        out.append((a, cur, b))
    d = f"M{out[0][0][0]:.2f},{out[0][0][1]:.2f}"
    for i, (a, c, b) in enumerate(out):
        if i:
            d += f" L{a[0]:.2f},{a[1]:.2f}"
        d += f" Q{c[0]:.2f},{c[1]:.2f} {b[0]:.2f},{b[1]:.2f}"
    return d + " Z"


def box_silhouette(u0, u1, v0, v1, w0, w1):
    """The six-vertex convex outline of an axis-aligned box in this projection:
    top-front-left, top-back-left, top-back-right, bottom-back-right,
    bottom-front-right, bottom-front-left."""
    return [P(u0, v0, w1), P(u0, v1, w1), P(u1, v1, w1),
            P(u1, v1, w0), P(u1, v0, w0), P(u0, v0, w0)]


def box_faces(u0, u1, v0, v1, w0, w1):
    """The three faces this projection shows, in painting order (top, flank,
    front — nearest last)."""
    return {
        "top": [(u0, v0, w1), (u1, v0, w1), (u1, v1, w1), (u0, v1, w1)],
        "flank": [(u1, v0, w0), (u1, v1, w0), (u1, v1, w1), (u1, v0, w1)],
        "front": [(u0, v0, w0), (u1, v0, w0), (u1, v0, w1), (u0, v0, w1)],
    }


# --------------------------------------------------------------- the hex fitting
HEX_PHI = [math.radians(60 * k) for k in range(7)]      # vertices at 0, 60, ...


def hex_ring(u, vc, wc, R):
    return [P(*circle3(u, vc, wc, R, phi)) for phi in HEX_PHI[:6]]


def hexprism(u0, u1, vc, wc, R, stops, ident):
    """A hex prism along +u. Only the flats whose normals face the viewer are
    drawn, each flat-filled from its own Lambert term — three separate values on
    one fitting, which is what makes it read as machined rather than turned."""
    t0, t1 = visible_arc()
    paths = []
    for k in range(6):
        pa, pb = HEX_PHI[k], HEX_PHI[k + 1]
        nrm = 0.5 * (pa + pb)                     # the flat's outward normal angle
        if not (t0 <= nrm <= t1):
            continue
        col = ramp(stops, lambert((0.0, math.cos(nrm), math.sin(nrm))))
        q = [P(*circle3(u0, vc, wc, R, pa)), P(*circle3(u1, vc, wc, R, pa)),
             P(*circle3(u1, vc, wc, R, pb)), P(*circle3(u0, vc, wc, R, pb))]
        paths.append(f'<path id="{ident}-f{k}" d="{poly(q)}" fill="{col}"/>')
    sil = hull(hex_ring(u0, vc, wc, R) + hex_ring(u1, vc, wc, R))
    return paths, sil


def hexcap(u, vc, wc, R, stops, ident):
    col = ramp(stops, lambert((1.0, 0.0, 0.0)))
    pts = hex_ring(u, vc, wc, R)
    return f'<path id="{ident}" d="{poly(pts)}" fill="{col}"/>', pts


# ------------------------------------------------------------------- the build
def build() -> str:
    sq = SQUIRCLE.read_text().strip()
    L: list[str] = []
    add = L.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')
    add("<title>proctor — The Side Port</title>")

    # -------------------------------------------------------- drive, geometry
    # Offsets are in u from the flank at u = UW; each outward step is thinner
    # than the last, so the quill reads as seated rather than as an attachment.
    boss, boss_o, boss_g = tube(UW + BOSS_U0, UW + BOSS_U1, DRIVE_V, DRIVE_W,
                                BOSS_R, GRAPHITE_RAMP, "boss")
    boss_cap, boss_cap_o = cap(UW + BOSS_U1, DRIVE_V, DRIVE_W, BOSS_R,
                               GRAPHITE_RAMP, "boss-cap")
    nut, nut_o = hexprism(UW + NUT_U0, UW + NUT_U1, DRIVE_V, DRIVE_W, NUT_R,
                          EMBER_RAMP, "nut")
    nut_cap, nut_cap_o = hexcap(UW + NUT_U1, DRIVE_V, DRIVE_W, NUT_R,
                                EMBER_RAMP, "nut-cap")
    shaft, shaft_o, shaft_g = tube(UW + SHAFT_U0, UW + SHAFT_U1, DRIVE_V, DRIVE_W,
                                   SHAFT_R, EMBER_RAMP, "shaft")
    endr, end_o, end_g = tube(UW + END_U0, UW + END_U1, DRIVE_V, DRIVE_W,
                              END_R, EMBER_RAMP, "endring")
    end_cap, end_cap_o = cap(UW + END_U1, DRIVE_V, DRIVE_W, END_R,
                             EMBER_RAMP, "end-cap")
    drive_hull = hull(boss_o + boss_cap_o + nut_o + nut_cap_o + shaft_o +
                      end_o + end_cap_o)

    # ------------------------------------------------------------------- defs
    add("<defs>")
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    add(f'<radialGradient id="ground" cx="{0.34 * S:.0f}" cy="{0.02 * S:.0f}" '
        f'r="{1.06 * S:.0f}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{GROUND_HI}"/>'
        f'<stop offset="0.52" stop-color="{GROUND_MID}"/>'
        f'<stop offset="1" stop-color="{GROUND_LO}"/></radialGradient>')
    add(f'<radialGradient id="vig" cx="{0.5 * S:.0f}" cy="{0.46 * S:.0f}" '
        f'r="{0.72 * S:.0f}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0.55" stop-color="{VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.28"/>'
        f'</radialGradient>')

    def lin(ident, a, b, c0, c1, o0=1.0, o1=1.0):
        add(f'<linearGradient id="{ident}" x1="{a[0]:.1f}" y1="{a[1]:.1f}" '
            f'x2="{b[0]:.1f}" y2="{b[1]:.1f}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{c0}" stop-opacity="{o0}"/>'
            f'<stop offset="1" stop-color="{c1}" stop-opacity="{o1}"/>'
            f'</linearGradient>')

    lin("gTop", P(0, 0, TOPW), P(UW, VD, TOPW), TOP_HI, TOP_LO)
    lin("gFront", P(0, 0, TOPW), P(0, 0, 0), FRONT_LO, FRONT_HI)
    lin("gFlank", P(UW, 0, 0), P(UW, VD, TOPW), FLANK_HI, FLANK_LO)
    lin("gPanel", P(0, 0, TOPW), P(0, 0, 0), "#1D1C1B", PANEL_FACE)
    lin("gBounceFront", P(0, 0, PLINTH_H + 40), P(0, 0, PLINTH_H),
        BOUNCE, BOUNCE, 0.0, 0.38)
    lin("gBounceFlank", P(UW, 0, PLINTH_H + 40), P(UW, 0, PLINTH_H),
        BOUNCE, BOUNCE, 0.0, 0.34)
    lin("gArris", P(0, 0, TOPW), P(UW, VD, TOPW), ARRIS_CATCH, ARRIS_CATCH,
        0.95, 0.08)
    lin("gFilletFront", P(UW - FILLET_W, 0, 0), P(UW, 0, 0),
        FRONT_HI, FILLET_DARK)
    lin("gFilletFlank", P(UW, 0, 0), P(UW, FILLET_W, 0),
        FILLET_DARK, FLANK_HI)
    lin("gSeat", P(UW, DRIVE_V, DRIVE_W), P(UW + NUT_U1, DRIVE_V, DRIVE_W),
        "#0A0908", "#0A0908", 0.66, 0.0)
    add(boss_g)
    add(shaft_g)
    add(end_g)

    add('<filter id="soft" x="-30%" y="-30%" width="160%" height="160%">'
        '<feGaussianBlur stdDeviation="22"/></filter>')
    add('<filter id="softer" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="40"/></filter>')
    add('<filter id="tight" x="-30%" y="-30%" width="160%" height="160%">'
        '<feGaussianBlur stdDeviation="8"/></filter>')
    add(f'<clipPath id="bodyClip"><path d="{round_poly(box_silhouette(0, UW, 0, VD, PLINTH_H, TOPW), BODY_R)}"/></clipPath>')
    add(f'<clipPath id="plinthClip"><path d="{round_poly(box_silhouette(-PLINTH_OUT, UW + PLINTH_OUT, -PLINTH_OUT, VD + PLINTH_OUT, 0, PLINTH_H), PLINTH_R)}"/></clipPath>')
    add(f'<mask id="noDrive" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="{S}" height="{S}">'
        f'<rect width="{S}" height="{S}" fill="#fff"/>'
        f'<path d="{poly(drive_hull)}" fill="#000"/></mask>')
    add("</defs>")

    # --------------------------------------------------------------------- bg
    add('<g id="bg" clip-path="url(#tile)">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add("</g>")

    # -------------------------------------------------------------------- mid
    add('<g id="mid" clip-path="url(#tile)">')
    # Contact shadow, apple-18's two-part reading: a wide shallow pool at
    # -0.058 L and a narrow seat at -0.114 L. Not a dark offset blob.
    px, py = P(UW / 2 + 26, VD / 2 + 20, 0)
    add(f'<ellipse cx="{px:.1f}" cy="{py + 14:.1f}" rx="{UW * 0.98:.0f}" '
        f'ry="62" fill="{SHADOW_POOL}" opacity="0.9" filter="url(#softer)"/>')
    seat = [(-SEAT_OUT, -SEAT_OUT, 0), (UW + SEAT_OUT, -SEAT_OUT, 0),
            (UW + SEAT_OUT, VD + SEAT_OUT, 0), (-SEAT_OUT, VD + SEAT_OUT, 0)]
    add(f'<path d="{face(seat)}" fill="{SHADOW_SEAT}" opacity="0.9" '
        f'filter="url(#soft)"/>')
    # And the narrow line of true contact, tight against the front-bottom arris.
    # Without it the casting reads as hovering over its own pool.
    tight = [(2, -6, 0), (UW - 2, -6, 0), (UW - 2, 16, 0), (2, 16, 0)]
    add(f'<path d="{face(tight)}" fill="{SHADOW_CONTACT}" opacity="0.85" '
        f'filter="url(#tight)"/>')
    # The quill is held off the ground, so it throws its own soft smear. It
    # binds the drive into the scene instead of leaving it floating.
    sm = [(x + 22, y + 232) for x, y in drive_hull]
    add(f'<path d="{poly(sm)}" fill="{SHADOW_POOL}" opacity="0.40" '
        f'filter="url(#softer)"/>')

    # ------------------------------------------------------------ the plinth
    # PLINTH_H = 0 ships the casting flush on the porcelain. A base flange was
    # authored and dropped: with its own values it read as a separate flat tray
    # under the case, and with the body's values it added a step that carried no
    # meaning. The seat shadow does the standing.
    if PLINTH_H > 0:
        pf = box_faces(-PLINTH_OUT, UW + PLINTH_OUT, -PLINTH_OUT,
                       VD + PLINTH_OUT, 0, PLINTH_H)
        add('<g clip-path="url(#plinthClip)">')
        add(f'<path id="plinth-top" d="{face(pf["top"])}" fill="{PLINTH_TOP}"/>')
        add(f'<path id="plinth-flank" d="{face(pf["flank"])}" fill="{PLINTH_FLANK}"/>')
        add(f'<path id="plinth-front" d="{face(pf["front"])}" fill="{PLINTH_FRONT}"/>')
        add("</g>")

    # -------------------------------------------------------------- the body
    bf = box_faces(0, UW, 0, VD, PLINTH_H, TOPW)
    add(f'<g clip-path="url(#bodyClip)">')
    add(f'<path id="body-top" d="{face(bf["top"])}" fill="url(#gTop)"/>')
    add(f'<path id="body-flank" d="{face(bf["flank"])}" fill="url(#gFlank)"/>')
    add(f'<path id="body-front" d="{face(bf["front"])}" fill="url(#gFront)"/>')
    # The arris between front and flank turns away from the key, so its fillet
    # is a DARK band, not a lit one. A radius reads as a value transition; a
    # radius drawn as a line reads as a scribe mark.
    fw = FILLET_W
    add(f'<path id="arris-fr" d="{face([(UW - fw, 0, PLINTH_H), (UW, 0, PLINTH_H), (UW, 0, TOPW), (UW - fw, 0, TOPW)])}" fill="url(#gFilletFront)"/>')
    add(f'<path id="arris-fl" d="{face([(UW, 0, PLINTH_H), (UW, fw, PLINTH_H), (UW, fw, TOPW), (UW, 0, TOPW)])}" fill="url(#gFilletFlank)"/>')

    # The bolted access panel: the shadow the recess casts, its floor, and four
    # fasteners. No walls — a lit wall band reads as a scribe mark, not depth.
    pu0, pu1 = PANEL_INSET_U, UW - PANEL_INSET_U
    pw0, pw1 = PLINTH_H + PANEL_INSET_W, TOPW - PANEL_INSET_W
    add(f'<path id="panel-shade" d="{round_poly([P(pu0, 0, pw0), P(pu1, 0, pw0), P(pu1, 0, pw1), P(pu0, 0, pw1)], PANEL_R)}" fill="{PANEL_SHADE}"/>')
    d = PANEL_DEPTH
    add(f'<path id="panel-face" d="{round_poly([P(pu0 + d * 0.75, 0, pw0 + d * 0.30), P(pu1, 0, pw0 + d * 0.30), P(pu1, 0, pw1 - d * 0.85), P(pu0 + d * 0.75, 0, pw1 - d * 0.85)], PANEL_R)}" fill="url(#gPanel)"/>')
    for fu in (pu0 + FASTENER_PAD + 8, pu1 - FASTENER_PAD):
        for fw2 in (pw0 + FASTENER_PAD, pw1 - FASTENER_PAD):
            cx, cy = P(fu, 0, fw2)
            add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{FASTENER_R}" '
                f'fill="{FASTENER}"/>')
            add(f'<circle cx="{cx - 2.4:.1f}" cy="{cy - 2.9:.1f}" '
                f'r="{FASTENER_R * 0.50:.1f}" fill="{FASTENER_LIT}" '
                f'opacity="0.60"/>')

    # apple-12's measurement: the graphite is LIGHTER at its lower edge, where
    # the porcelain bounces up into it. Tight, and brighter than seems right.
    add(f'<path d="{face([(0, 0, PLINTH_H), (UW, 0, PLINTH_H), (UW, 0, PLINTH_H + 40), (0, 0, PLINTH_H + 40)])}" fill="url(#gBounceFront)"/>')
    add(f'<path d="{face([(UW, 0, PLINTH_H), (UW, VD, PLINTH_H), (UW, VD, PLINTH_H + 40), (UW, 0, PLINTH_H + 40)])}" fill="url(#gBounceFlank)"/>')
    add("</g>")
    add("</g>")

    # --------------------------------------------------------------------- fg
    add('<g id="fg" clip-path="url(#tile)">')
    # The boss is the case's own casting, so it stays graphite: the accent is
    # reserved for the part Proctor brings.
    L.extend(boss)
    add(boss_cap)
    # A tight ring of shade where the nut is torqued down onto the boss.
    add(f'<path d="{poly(nut_o)}" fill="url(#gSeat)" filter="url(#tight)" '
        f'opacity="0.9"/>')
    L.extend(nut)
    add(nut_cap)
    L.extend(shaft)
    L.extend(endr)
    add(end_cap)
    # The warm spill the quill throws back onto the flank it is seated in.
    bx, by = P(UW + BOSS_U1 * 0.35, DRIVE_V, DRIVE_W)
    add(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{BOSS_R * 1.30:.0f}" '
        f'ry="{BOSS_R * 1.10:.0f}" fill="{EMBER_BOUNCE}" opacity="0.15" '
        f'filter="url(#soft)"/>')
    add("</g>")

    # -------------------------------------------------------------- highlight
    add('<g id="highlight" clip-path="url(#tile)">')
    a = ARRIS_W
    add(f'<path d="{face([(0, 0, TOPW), (UW, 0, TOPW), (UW, 0, TOPW - a), (0, 0, TOPW - a)])}" fill="url(#gArris)"/>')
    add(f'<path d="{face([(0, 0, TOPW), (0, VD, TOPW), (a * 0.8, VD, TOPW), (a * 0.8, 0, TOPW)])}" fill="url(#gArris)" opacity="0.85"/>')
    add(f'<path d="{face([(0, 0, PLINTH_H), (a * 0.7, 0, PLINTH_H), (a * 0.7, 0, TOPW), (0, 0, TOPW)])}" fill="{ARRIS_CATCH}" opacity="0.32"/>')
    # The quill's specular: one band along the crest, whose angle is solved from
    # the key rather than placed by eye.
    t0, t1 = visible_arc()
    tc = math.atan2(KEY_DIR[2], KEY_DIR[1])
    hw = (t1 - t0) / 44.0
    for u0, u1, r, op in ((SHAFT_U0, SHAFT_U1, SHAFT_R, 0.5),
                          (END_U0, END_U1, END_R, 0.38)):
        spec = [P(*circle3(UW + u0, DRIVE_V, DRIVE_W, r, tc - hw)),
                P(*circle3(UW + u1, DRIVE_V, DRIVE_W, r, tc - hw)),
                P(*circle3(UW + u1, DRIVE_V, DRIVE_W, r, tc + hw)),
                P(*circle3(UW + u0, DRIVE_V, DRIVE_W, r, tc + hw))]
        add(f'<path d="{poly(spec)}" fill="{EMBER_CREST}" opacity="{op}" '
            f'filter="url(#tight)"/>')
    # The tile's inner rim light, masked out of the drive: a highlight in this
    # layer otherwise paints a pale scratch across whatever stands in front of
    # it (material-recipes, anvil-errand).
    add(f'<g mask="url(#noDrive)"><path d="{sq}" fill="none" '
        f'stroke="{RIM_TILE}" stroke-width="3.4" opacity="0.6"/></g>')
    add("</g>")

    add("</svg>")
    return "\n".join(L)


if __name__ == "__main__":
    (HERE / "icon.svg").write_text(build())
    print(f"wrote {HERE / 'icon.svg'}")
