#!/usr/bin/env python3
"""Build the ux-craft icon master — "The Spacing Circle".

Geometry and material live here as named constants so a revision is a parameter
edit rather than path surgery. A banner can be derived from the same values:
LIGHT_ANGLE_DEG fixes the key light, ENVELOPE_* and SQUASH fix the geometry,
ACCENT* fixes the one warm hue.

The device: WCAG 2.5.8's Spacing exception, made physical. Two touch targets sit
on a porcelain bench, each wearing its reach envelope as a low puck of graphite
gel — the region a fingertip claims, rather than the rectangle a designer drew.
The two envelopes are sized to the two figures that disagreed across three of
this skill's own files, at their true 44:24 ratio: the AAA / Apple craft target
and the AA minimum. They cross, which is exactly what the criterion forbids, and
the crossing is the only lit thing in the tile — where two reaches double, the
gate fires and the doubled gel glows.

The signature move is that the accent exists ONLY in the crossing. It is painted
on neither object; it is a property of their relationship. Move either control
forty units apart and the tile goes dark, which is the gate's exit code drawn as
light rather than as a badge on a thing.

Two constructions here were bought with rejected rounds and are worth keeping:
the envelopes are FORESHORTENED pucks with a visible edge band, because a
plan-view circle with a radial gradient renders as a ball bearing; and every
face on both pucks hangs off ONE user-space ramp along the light axis, so they
read as two objects under one light rather than as adjacent panels.

    python3 build_icon.py            # writes icon.svg beside this file
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024  # canvas

# ---------------------------------------------------------------- light model
# One soft key, travelling down and to the right. Every rim light, cast shadow,
# occlusion crescent and porcelain bounce below is derived from this one axis;
# nothing is placed by eye.
LIGHT_ANGLE_DEG = 118.0
LX = math.cos(math.radians(LIGHT_ANGLE_DEG))   # +0.469 → travels right
LY = math.sin(math.radians(LIGHT_ANGLE_DEG))   # +0.883 → travels down

# ---------------------------------------------------------------- geometry
# The two reach envelopes, at the ratio of the two figures that disagreed:
# 44 (WCAG 2.5.8 AAA, and Apple's 44 pt) against 24 (WCAG 2.5.8 AA minimum).
ENVELOPE_AAA = 44.0
ENVELOPE_AA = 24.0
R_BIG = 288.0                                  # the 44 envelope
R_SMALL = R_BIG * ENVELOPE_AA / ENVELOPE_AAA   # the 24 envelope, to scale
SQUASH = 0.66              # foreshortening: the bench is seen from above-front
THICK = 32.0               # each puck's own edge band — what makes it an object
OFFSET_X = 246.0           # centre-to-centre in the flat (unsquashed) plan
OFFSET_Y = 222.0
LIFT = 18.0                # optical lift off dead centre

# The controls themselves, drawn as indicative keys rather than to the standards'
# own ratio: a chip at 24/44 of its envelope's diameter turns each puck into a
# washer, and a viewer can check whether a puck reads solid but cannot check a
# ratio. The envelopes carry the arithmetic; the keys carry the meaning.
KEY_FRAC = 0.54            # key width as a fraction of its envelope radius
KEY_R_FRAC = 0.30          # key corner radius as a fraction of its width
KEY_THICK = 17.0           # the key stands proud of the puck it sits on

# ---------------------------------------------------------------- ground
# Porcelain cushion, sampled off the corpus captures in this register
# (apple-28 Photos: V 0.999 under the key, 0.960 mid, 0.923 at the far edge — a
# near-neutral warm white falling about 0.08 across the tile).
GROUND_HI = "#FDFBF6"
GROUND_MID = "#F4EFE3"
GROUND_EDGE = "#E1D9C8"
RIM_INNER = "#FFFEFA"
VIGNETTE = "#8B7F66"
VIGNETTE_A = 0.22
SHADOW = "#3A3126"         # the family's warm shadow ink — never blue

# ---------------------------------------------------------------- the gel
# Graphite gel, valued off apple-12's satin charcoal body normalised to this
# tile's brighter ground: lit shoulder V 0.36, face V 0.23, far rim V 0.14, rim
# light about 2x the face, and a porcelain bounce that lifts the far edge to
# roughly 1.7x the face rather than letting it fall to a hole.
GEL_HI = "#98917F"         # the lit shoulder, up-light end of the shared ramp
GEL_MID = "#4A443A"
GEL_LO = "#1E1B16"         # the far end, down-light
WALL_HI = "#514A3E"        # the edge band runs a step darker than the top face
WALL_LO = "#1B1813"
GEL_RIM = "#BDB1A0"
BOUNCE = "#D8CBB2"         # the tile's own light thrown back up into the band
GEL_ALPHA = 0.95           # authored translucency: the crossing doubles for real

RIM_W = 7.0                # rim-light stroke on the lit arc of each top face
BOUNCE_W = 11.0            # porcelain bounce along the far arc of each band
AO_A = 0.34                # occlusion inside the far rim of each top face
SHEEN_A = 0.13             # the one soft catch on each lit shoulder

# ---------------------------------------------------------------- the controls
# Frosted porcelain keys. White is a material here: the gel below bleeds through
# the thinner areas, which is the era's tell rather than an effect.
KEY_HI = "#FFFEFB"
KEY_LO = "#E7DFD0"
KEY_EDGE = "#B0A691"
KEY_ALPHA = 0.92

# ---------------------------------------------------------------- the accent
# One warm hue, and it exists only where the two envelopes cross. Luminance
# taken from the family (the siblings' shared accent sits at HSL L 0.539;
# #EA4A24 sits at 0.529), hue taken from the subject — a hot core seen through
# doubled gel reads redder than the family's orange.
ACCENT_CORE = "#FFC08C"    # the core of the trapped light
ACCENT_HI = "#F5793C"
ACCENT = "#EA4A24"
ACCENT_DEEP = "#4E1605"    # the boundary, where the doubled gel goes opaque
LENS_DARK_A = 0.30         # the doubled gel, before any light is put in it
BLOOM_A = 0.34             # bloom inside the gel that traps it
HALO_A = 0.07              # the little that escapes onto the porcelain
FLANK_A = 0.24             # warm kiss on the flanks that face the crossing


# ------------------------------------------------------------------ helpers
def rr(x: float, y: float, w: float, h: float, r: float) -> str:
    return (f"M{x + r:.1f},{y:.1f} h{w - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} "
            f"v{h - 2 * r:.1f} a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{r:.1f} h{-(w - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{-r:.1f} v{-(h - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{-r:.1f} z")


def ell(cx: float, cy: float, r: float) -> str:
    """A foreshortened circle, as a path so it can carry a fill-rule with a hole."""
    ry = r * SQUASH
    return (f"M{cx - r:.1f},{cy:.1f} a{r:.1f},{ry:.1f} 0 1 0 {2 * r:.1f},0 "
            f"a{r:.1f},{ry:.1f} 0 1 0 {-2 * r:.1f},0 z")


def crescent(cx: float, cy: float, r: float, inset: float,
             off: tuple[float, float]) -> str:
    """Outer foreshortened circle minus an inner one pushed off centre — one path
    that carries a crescent of occlusion, thickest where the inner one retreats."""
    ox, oy = off
    return ell(cx, cy, r) + " " + ell(cx + ox, cy + oy, r * (1 - inset))


def vesica(c1: tuple[float, float], r1: float, c2: tuple[float, float], r2: float,
           n: int = 44) -> str:
    """The crossing of the two envelopes, computed in the flat plan and then
    foreshortened. Sampled rather than arc-flagged: an A-command's sweep flag is
    exactly the kind of thing that renders one way in rsvg and the other in a
    browser, and this outline is the icon's entire accent."""
    x1, y1 = c1[0], c1[1] / SQUASH
    x2, y2 = c2[0], c2[1] / SQUASH
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0.0))
    ux, uy = dx / d, dy / d
    px, py = x1 + a * ux, y1 + a * uy
    i1 = (px - h * uy, py + h * ux)
    i2 = (px + h * uy, py - h * ux)

    def arc(c, r, start, end):
        cx, cy = c
        a0 = math.atan2(start[1] - cy, start[0] - cx)
        a1 = math.atan2(end[1] - cy, end[0] - cx)
        while a1 - a0 > math.pi:
            a1 -= 2 * math.pi
        while a0 - a1 > math.pi:
            a1 += 2 * math.pi
        return [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

    pts = arc((x1, y1), r1, i1, i2) + arc((x2, y2), r2, i2, i1)[1:]
    out = [f"M{pts[0][0]:.1f},{pts[0][1] * SQUASH:.1f}"]
    out += [f"L{p[0]:.1f},{p[1] * SQUASH:.1f}" for p in pts[1:]]
    return " ".join(out) + " Z"


def lens_centre(c1, r1, c2, r2) -> tuple[float, float]:
    """Midway between the two arc crowns — where the doubled gel is thickest."""
    x1, y1 = c1[0], c1[1] / SQUASH
    x2, y2 = c2[0], c2[1] / SQUASH
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    k1 = (x1 + r1 * ux, y1 + r1 * uy)
    k2 = (x2 - r2 * ux, y2 - r2 * uy)
    return ((k1[0] + k2[0]) / 2, (k1[1] + k2[1]) / 2 * SQUASH)


# ------------------------------------------------------------------ build
def build() -> str:
    # the two envelope centres, placed off the union's own bounding box
    union_w = R_BIG + OFFSET_X + R_SMALL
    union_h = (R_BIG + OFFSET_Y + R_SMALL) * SQUASH + THICK
    c1 = ((S - union_w) / 2 + R_BIG,
          (S - union_h) / 2 + R_BIG * SQUASH - LIFT)
    c2 = (c1[0] + OFFSET_X, c1[1] + OFFSET_Y * SQUASH)

    lens = vesica(c1, R_BIG, c2, R_SMALL)
    lcx, lcy = lens_centre(c1, R_BIG, c2, R_SMALL)
    d_flat = math.hypot(OFFSET_X, OFFSET_Y)
    lens_w = (R_BIG + R_SMALL - d_flat) / 2                     # half-width
    a_flat = (d_flat ** 2 + R_BIG ** 2 - R_SMALL ** 2) / (2 * d_flat)
    lens_h = math.sqrt(max(R_BIG ** 2 - a_flat ** 2, 0.0)) * SQUASH   # half-height

    # the one shared ramp: a single user-space axis spanning the whole object, so
    # both pucks and every face on them are lit by the same key
    ax0 = (c1[0] - LX * R_BIG * 1.15, c1[1] - LY * R_BIG * 1.15)
    ax1 = (c2[0] + LX * R_SMALL * 1.9, c2[1] + LY * R_SMALL * 1.9)

    tile = SQUIRCLE.read_text().strip()
    p: list[str] = []
    add = p.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')
    add("<defs>")

    add(f'''<radialGradient id="ground" cx="0.40" cy="0.30" r="0.88">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.56" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<radialGradient id="vign" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.54" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="{VIGNETTE_A}"/>
    </radialGradient>''')
    # one ramp for every top face, one a step darker for every edge band
    add(f'''<linearGradient id="face" gradientUnits="userSpaceOnUse"
      x1="{ax0[0]:.1f}" y1="{ax0[1]:.1f}" x2="{ax1[0]:.1f}" y2="{ax1[1]:.1f}">
      <stop offset="0" stop-color="{GEL_HI}"/>
      <stop offset="0.40" stop-color="{GEL_MID}"/>
      <stop offset="1" stop-color="{GEL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="band" gradientUnits="userSpaceOnUse"
      x1="{ax0[0]:.1f}" y1="{ax0[1]:.1f}" x2="{ax1[0]:.1f}" y2="{ax1[1]:.1f}">
      <stop offset="0" stop-color="{WALL_HI}"/>
      <stop offset="0.5" stop-color="#302B23"/>
      <stop offset="1" stop-color="{WALL_LO}"/>
    </linearGradient>''')
    # rim light and porcelain bounce: the same stroke construction, run from
    # opposite ends of the one axis
    add(f'''<linearGradient id="rim" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="{GEL_RIM}" stop-opacity="0.90"/>
      <stop offset="0.40" stop-color="{GEL_RIM}" stop-opacity="0.14"/>
      <stop offset="1" stop-color="{GEL_RIM}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="bnc" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="{BOUNCE}" stop-opacity="0"/>
      <stop offset="0.62" stop-color="{BOUNCE}" stop-opacity="0"/>
      <stop offset="0.88" stop-color="{BOUNCE}" stop-opacity="0.14"/>
      <stop offset="1" stop-color="{BOUNCE}" stop-opacity="0.38"/>
    </linearGradient>''')
    add(f'''<linearGradient id="keyface" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="{KEY_HI}"/>
      <stop offset="0.60" stop-color="#F6F0E4"/>
      <stop offset="1" stop-color="{KEY_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="keyrim" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{KEY_EDGE}" stop-opacity="0.60"/>
    </linearGradient>''')
    add(f'''<radialGradient id="core" gradientUnits="userSpaceOnUse"
      cx="{lcx:.1f}" cy="{lcy:.1f}" r="{lens_h * 1.48:.1f}"
      gradientTransform="translate({lcx:.1f},{lcy:.1f}) scale({lens_w / lens_h:.3f},1) translate({-lcx:.1f},{-lcy:.1f})">
      <stop offset="0" stop-color="{ACCENT_CORE}"/>
      <stop offset="0.44" stop-color="{ACCENT_HI}"/>
      <stop offset="0.82" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}"/>
    </radialGradient>''')
    add(f'''<linearGradient id="lensrim" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="{ACCENT_CORE}" stop-opacity="0.85"/>
      <stop offset="0.45" stop-color="{ACCENT_HI}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}" stop-opacity="0.45"/>
    </linearGradient>''')
    add(f'''<radialGradient id="flank" gradientUnits="userSpaceOnUse"
      cx="{lcx:.1f}" cy="{lcy:.1f}" r="{lens_h * 2.6:.1f}">
      <stop offset="0" stop-color="{ACCENT_HI}" stop-opacity="{FLANK_A}"/>
      <stop offset="0.5" stop-color="{ACCENT_HI}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{ACCENT_HI}" stop-opacity="0"/>
    </radialGradient>''')

    add('<filter id="cast" x="-45%" y="-60%" width="190%" height="220%">'
        '<feGaussianBlur stdDeviation="20"/></filter>')
    add('<filter id="castwide" x="-70%" y="-90%" width="240%" height="280%">'
        '<feGaussianBlur stdDeviation="48"/></filter>')
    add('<filter id="ao" x="-40%" y="-50%" width="180%" height="200%">'
        '<feGaussianBlur stdDeviation="17"/></filter>')
    add('<filter id="soft" x="-70%" y="-90%" width="240%" height="280%">'
        '<feGaussianBlur stdDeviation="30"/></filter>')
    add('<filter id="bloom" x="-110%" y="-140%" width="320%" height="380%">'
        '<feGaussianBlur stdDeviation="24"/></filter>')
    add('<filter id="halo" x="-180%" y="-220%" width="460%" height="540%">'
        '<feGaussianBlur stdDeviation="58"/></filter>')
    add('<filter id="keyshadow" x="-70%" y="-90%" width="240%" height="280%">'
        '<feGaussianBlur stdDeviation="8"/></filter>')

    add(f'<clipPath id="tile"><path d="{tile}"/></clipPath>')
    add(f'<clipPath id="faceBig"><path d="{ell(*c1, R_BIG)}"/></clipPath>')
    add(f'<clipPath id="faceSmall"><path d="{ell(*c2, R_SMALL)}"/></clipPath>')
    add(f'<clipPath id="bandSmall"><path d="{ell(c2[0], c2[1] + THICK, R_SMALL)}"/></clipPath>')
    add("</defs>")

    add('<g clip-path="url(#tile)">')

    # ============================================================== bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vign)"/>')
    add("</g>")

    # ============================================================== mid
    # Both pucks' contact shadows, then the 44 envelope.
    add('<g id="mid">')
    for c, R in ((c1, R_BIG), (c2, R_SMALL)):
        add(f'<g filter="url(#castwide)"><path d="{ell(c[0] + LX * R * 0.13, c[1] + THICK + LY * R * 0.18, R * 1.02)}" '
            f'fill="{SHADOW}" fill-opacity="0.17"/></g>')
        add(f'<g filter="url(#cast)"><path d="{ell(c[0] + LX * R * 0.06, c[1] + THICK * 0.9 + LY * R * 0.09, R * 0.97)}" '
            f'fill="{SHADOW}" fill-opacity="0.30"/></g>')
    add(puck(c1, R_BIG, "faceBig"))
    add(key(c1, R_BIG))
    add("</g>")

    # ============================================================== fg
    # The 24 envelope stands nearer the viewer, then the crossing itself.
    add('<g id="fg">')
    add(puck(c2, R_SMALL, "faceSmall"))
    add(key(c2, R_SMALL))

    # the warm kiss on the flanks that face the crossing — tight, and in the
    # paler spill hue, because a wide warm wash turns graphite to mud with every
    # hex still correct
    for cid in ("faceBig", "faceSmall"):
        add(f'<g clip-path="url(#{cid})"><rect width="{S}" height="{S}" '
            f'fill="url(#flank)"/></g>')

    # the crossing: doubled gel first, then the light trapped inside it
    add(f'<g clip-path="url(#bandSmall)"><path d="{lens}" '
        f'transform="translate(0,{THICK * 0.62:.1f})" fill="{ACCENT_DEEP}" '
        f'fill-opacity="0.55"/></g>')
    add(f'<path d="{lens}" fill="{SHADOW}" fill-opacity="{LENS_DARK_A}"/>')
    add(f'<path d="{lens}" fill="url(#core)"/>')
    add(f'<path d="{lens}" fill="none" stroke="url(#lensrim)" stroke-width="5"/>')
    add("</g>")

    # ============================================================== highlight
    # What leaves the crossing, and the tile's own inner rim. Nothing here may
    # paint over an occluder: each bloom is clipped to the gel it sits in, and
    # only the faint halo is allowed onto the porcelain.
    add('<g id="highlight">')
    for cid in ("faceBig", "faceSmall"):
        add(f'<g clip-path="url(#{cid})"><path d="{lens}" fill="{ACCENT}" '
            f'fill-opacity="{BLOOM_A}" filter="url(#bloom)"/></g>')
    add(f'<path d="{lens}" fill="{ACCENT}" fill-opacity="{HALO_A}" filter="url(#halo)"/>')
    add(f'<path d="{tile}" fill="none" stroke="{RIM_INNER}" stroke-opacity="0.72" '
        f'stroke-width="7"/>')
    add("</g>")

    add("</g>")  # tile
    add("</svg>")
    return "\n".join(p)


def puck(c: tuple[float, float], R: float, clip: str) -> str:
    """A reach envelope as a low puck of gel: edge band, top face, occlusion in
    the far rim, rim light on the lit arc, porcelain bounce along the far band,
    one soft catch on the lit shoulder."""
    cx, cy = c
    out = []
    # the edge band — the top face's outline dropped by the puck's own thickness
    out.append(f'<path d="{ell(cx, cy + THICK, R)}" fill="url(#band)"/>')
    out.append(f'<path d="{ell(cx, cy + THICK - BOUNCE_W / 2, R - BOUNCE_W / 2)}" '
               f'fill="none" stroke="url(#bnc)" stroke-width="{BOUNCE_W}"/>')
    # the top face
    out.append(f'<path d="{ell(cx, cy, R)}" fill="url(#face)" fill-opacity="{GEL_ALPHA}"/>')
    # occlusion inside the far rim: an eccentric crescent pushed against the key
    off = (-LX * R * 0.085, -LY * R * 0.085 * SQUASH)
    out.append(f'<g clip-path="url(#{clip})"><path d="{crescent(cx, cy, R, 0.11, off)}" '
               f'fill-rule="evenodd" fill="{SHADOW}" fill-opacity="{AO_A}" '
               f'filter="url(#ao)"/></g>')
    # one soft catch on the lit shoulder; no hard specular anywhere
    hx, hy = cx - LX * R * 0.44, cy - LY * R * 0.44 * SQUASH
    out.append(f'<g clip-path="url(#{clip})"><ellipse cx="{hx:.1f}" cy="{hy:.1f}" '
               f'rx="{R * 0.60:.1f}" ry="{R * 0.30 * SQUASH:.1f}" fill="#FFFFFF" '
               f'fill-opacity="{SHEEN_A}" filter="url(#soft)"/></g>')
    # rim light on the lit arc of the top face
    out.append(f'<path d="{ell(cx, cy, R - RIM_W / 2)}" fill="none" stroke="url(#rim)" '
               f'stroke-width="{RIM_W}"/>')
    return "".join(out)


def key(c: tuple[float, float], R: float) -> str:
    """The control itself: a frosted porcelain key standing proud of its puck,
    thin enough that the gel below bleeds through it. Flat #FFFFFF is the
    previous era's tell; the translucency cues are the era."""
    cx, cy = c
    w = R * KEY_FRAC
    h = w * SQUASH
    r = w * KEY_R_FRAC
    x, y = cx - w / 2, cy - h / 2
    face = rr(x, y, w, h, r)
    return "".join([
        f'<g filter="url(#keyshadow)"><path d="{rr(x + LX * 12, y + KEY_THICK + LY * 10, w, h, r)}" '
        f'fill="{SHADOW}" fill-opacity="0.42"/></g>',
        f'<path d="{rr(x, y + KEY_THICK, w, h, r)}" fill="url(#band)"/>',
        f'<path d="{face}" fill="url(#keyface)" fill-opacity="{KEY_ALPHA}"/>',
        f'<path d="{face}" fill="none" stroke="url(#keyrim)" stroke-width="3.5"/>',
    ])


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(build())
    print(f"wrote {out}")
