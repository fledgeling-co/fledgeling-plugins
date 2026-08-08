#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the dossier-report icon.

Direction "The Folded Sheet": Tahoe gel-glass sub-register (a), porcelain cushion
tile carrying one coloured gel object, crossed with the device bank's #23
(fold / self-shadow ribbon), #16 (the icon performs the verb), #21 (authored
overlap) and #20 (data-as-glyph abstraction).

The subject is a skill that publishes one self-contained report page per topic,
designed from scratch around its own subject, with every claim carrying a source.
So the icon is a page: blank on the outside, because no two of them look alike,
and carrying the evidence on the INSIDE, where only a fold can show you. A large
sheet of frosted gel has been creased once along a diagonal and the panel above
that crease has swung down and forward over the rest of the page, so its
underside now faces the viewer - vermilion, ruled, plotted. The crease is the
only place the two states meet, and it is where the colour comes out.

Every visible edge of the flap is a mapped image of a real page edge, because the
whole flap is authored in UNFOLDED PAGE SPACE and pushed through one fold map:
reflect across the crease, compress by |cos(theta)| along the crease normal. That
is the true orthographic projection of a planar region rotated about a line in
its own plane, so the crease, the flap outline, the flap's edge thickness and the
chart rule printed on the page's reverse cannot drift out of register - they are
one matrix. Rounded page corners come through it for free.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
Every constant below is named; a fidelity round is a parameter edit, never path
surgery.
"""

import math
import pathlib
import re

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ------------------------------------------------------------------ geometry

# The unfolded page, in canvas coordinates. Only the part on the base side of the
# crease is ever seen unfolded; the rest is the flap and arrives folded.
PAGE_X0, PAGE_X1 = 220.0, 800.0
PAGE_Y0, PAGE_Y1 = 180.0, 845.0
PAGE_R = 42.0                    # page corner radius

# The crease: two points on the page outline. It runs from the bottom edge up to
# the right edge, so the flap is the page's lower-right region and the page keeps
# its whole top edge and three of its four corners - it has to still read as a
# page before it reads as a fold. The cut is deliberately large: a third of the
# sheet on a 46-degree crease is a fold, where a small corner would be a page
# curl, which the corpus lists as legacy-era drag.
CREASE_A = (300.0, 845.0)        # on the bottom edge
CREASE_B = (800.0, 320.0)        # on the right edge
FLAP_CORNER = (800.0, 845.0)     # the page corner the crease cuts off: the flap side

# How far the flap has come over, as |cos(theta)| of the fold angle. 0 = caught
# at 90 degrees (flap edge-on, invisible); 1 = folded flat onto itself.
FOLD_K = 0.800

THICK_PAGE = 15.0                # the gel slab's own thickness, page's free edges
THICK_FLAP = 13.0                # the same slab seen along the flap's free edges
CREASE_ROLL = 26.0               # width of the rolled crest along the crease
FILLET_PAGE = 20.0               # roll width on the page's own arrises

# The chart printed on the page's reverse, authored in unfolded page space inside
# the flap's source region and carried into view by the same fold map. Its ruled
# baseline runs down the page (+y) and its values step across it (+x), because
# THAT is the pair of page-space axes this crease maps to screen-horizontal and
# screen-up: a chart drawn the obvious way lands on its side. The residual shear
# is left in - it is the cue that says the flap is a turned plane, not a decal.
CHART_BASE_X = 592.0             # page-space x of the ruled baseline
CHART_Y0, CHART_Y1 = 578.0, 826.0   # its two ends, down the page
CHART_STEPS = ((0.00, 12.0), (0.29, 70.0), (0.56, 70.0), (0.79, 132.0),
               (1.00, 132.0))   # (fraction along the baseline, rise across it)
CHART_W = 18.0                   # stroke width of the plotted line
CHART_BASE_W = 15.0

# ------------------------------------------------------------------- material
# Sampled out of the corpus before a line was authored: apple-05 (Infuse, the
# fold/self-shadow ribbon on porcelain), apple-23 Safari, apple-26 Reminders,
# apple-31 News, plus the two Engine C rasters. Numbers in icon-notes.md.

# porcelain cushion: L 0.985 at the crown, 0.955 at the flanks, 0.925 at the foot
GROUND_TOP = "#FFFCF6"
GROUND_MID = "#F8F3EB"
GROUND_BOT = "#F1ECE2"
GROUND_VIGNETTE = "#9C8B70"
RIM_RING = "#FFFFFF"

# the sheet's outer face. Deliberately NOT darker than its ground: measured, the
# corpus's porcelain objects sit at the ground's own luminance (C1 sheet p25-p75
# 0.943-0.979 against a ground of 0.935-0.989) and are separated by shadow,
# thickness and rim - never by value. Assuming "object darker than ground" here
# would have cost the register.
PAGE_LIT = "#FFFEFB"
PAGE_MID = "#F9F5EE"
PAGE_LOW = "#EFE9DE"
# Measured, r02: the reference's slab edge crests only +0.03 over the face it
# belongs to (0.918 face -> 0.951 crest). The first draft ran it at pure white and
# rendered a 0.996 hairline against a 0.865 page - a cut edge, not a rolled one.
PAGE_EDGE_LIT = "#F7F1E4"
PAGE_EDGE_LOW = "#D8CEBB"

# the vermilion inner face. Infuse's inner face measures #D93621 (L 0.34, H 7,
# S 0.848) against an outer face of #ED722E (L 0.53, H 21, S 0.806): darker, hue
# rotated 14 degrees TOWARD red, and MORE saturated. A translucent body keeps its
# chroma where it turns away, which is the whole material claim of the era.
FLAP_FREE = "#F87A4D"            # the free-edge end, most open to the sky
FLAP_MID = "#EC5C31"             # the plane's own tone
FLAP_DEEP = "#D8471F"            # toward the crease, where the V closes
FLAP_AO = "#8E1E04"              # the V's own occlusion, along the crease
CREASE_CREST = "#FFD3B4"         # the rolled crest, where the colour comes out
CREASE_CREST_2 = "#F9834F"
RIM_SCATTER = "#FCC0A4"          # L 0.795, S 0.35 - measured off both references
FLAP_CREST = "#FFD8BE"           # the flap's own cut face, turned up into the key
FLAP_CREST_W = 17.0              # measured: the reference's crest runs 12-16px
BOUNCE = "#FF9A62"               # what the inner face throws onto the page

CHART_FROST = "#FFF0E6"          # frosted white, ground hue bleeding through
CHART_OPACITY = 0.90
CHART_BASE_OPACITY = 0.80

SHADOW = "#6B5334"               # warm; nothing in this scene emits cool light
AO_CREASE_OPACITY = 0.30
AO_CREASE_DEEP = 0.62            # the narrow band right in the V
AO_DEEP = "#7A1602"
AO_DEEP_W = 20.0
KEY = (-0.44, -0.90)             # the one light: top, biased left. Unit-ish.

# ---------------------------------------------------------------- path helpers


def _cubic(p0, p1, p2, p3, n):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
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


def poly(pts, close=True):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    return d + ("Z" if close else "")


def rounded_rect_poly(x0, y0, x1, y1, r, seg=10):
    """The page outline as a polyline, so the fold map can carry its corners."""
    out = []
    corners = (((x1 - r, y0 + r), -90, 0),      # top-right
               ((x1 - r, y1 - r), 0, 90),       # bottom-right
               ((x0 + r, y1 - r), 90, 180),     # bottom-left
               ((x0 + r, y0 + r), 180, 270))    # top-left
    for (cx, cy), a0, a1 in corners:
        for i in range(seg + 1):
            a = math.radians(a0 + (a1 - a0) * i / seg)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def split_by_line(pts, a, b):
    """Split a closed polygon by the infinite line ab. Returns (side<0, side>0),
    each a closed polygon with the two intersection points inserted."""
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay

    def side(p):
        return (p[0] - ax) * dy - (p[1] - ay) * dx

    neg, pos = [], []
    n = len(pts)
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        sp, sq = side(p), side(q)
        (neg if sp <= 0 else pos).append(p)
        if (sp < 0 < sq) or (sq < 0 < sp):
            t = sp / (sp - sq)
            x = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
            neg.append(x)
            pos.append(x)
    return neg, pos


def make_fold(a, b, k):
    """Rotate a planar region about the line ab by theta and project
    orthographically: reflect across ab, then compress by k=|cos theta| along the
    line's normal. Exact for any planar figure, so the page's rounded corners,
    its edge bands and the marks printed on its reverse all ride the same map."""
    ax, ay = a
    dx, dy = b[0] - ax, b[1] - ay
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux

    def fold(p):
        px, py = p[0] - ax, p[1] - ay
        cu = px * ux + py * uy
        cn = px * nx + py * ny
        return (ax + ux * cu - nx * k * cn, ay + uy * cu - ny * k * cn)

    return fold, (ux, uy), (nx, ny)


def offset_poly(pts, d, ux, uy):
    return [(x + d * ux, y + d * uy) for x, y in pts]


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


def _nearest(pts, q):
    return min(range(len(pts)), key=lambda i: (pts[i][0] - q[0]) ** 2 + (pts[i][1] - q[1]) ** 2)


def free_arc(pts, a, b):
    """The part of a split polygon's boundary that is a REAL page edge.

    Both halves of the split share the crease as a straight segment between the
    two crossing points. A fold has no material edge - the sheet turns and keeps
    going - so the slab's thickness, and the arris roll that goes with it, must
    follow this arc and stop at the crease. Drawing them all the way round is
    what made the first draft's fold read as a cut."""
    i, j = _nearest(pts, a), _nearest(pts, b)
    n = len(pts)
    arc1 = [pts[(i + t) % n] for t in range((j - i) % n + 1)]
    arc2 = [pts[(j + t) % n] for t in range((i - j) % n + 1)]
    return arc1 if len(arc1) > len(arc2) else arc2


def ribbon(arc, dx, dy):
    """A slab edge: the free arc, and the same arc pushed by the slab's thickness."""
    return arc + list(reversed(shift(arc, dx, dy)))


# ------------------------------------------------------------------- assembly

def build():
    page = rounded_rect_poly(PAGE_X0, PAGE_Y0, PAGE_X1, PAGE_Y1, PAGE_R)
    A, B = CREASE_A, CREASE_B

    fold, (ux, uy), (nx, ny) = make_fold(A, B, FOLD_K)

    half_a, half_b = split_by_line(page, A, B)

    def side(p):
        return ((p[0] - A[0]) * (B[1] - A[1]) - (p[1] - A[1]) * (B[0] - A[0]))

    flap_side = side(FLAP_CORNER)
    src = half_a if flap_side <= 0 else half_b
    base_poly = half_b if flap_side <= 0 else half_a
    flap_poly = [fold(p) for p in src]

    # orient the crease normal so +n points from the crease INTO the base half:
    # every gradient axis, AO offset and crease roll below is hung off it.
    bc = (sum(p[0] for p in base_poly) / len(base_poly),
          sum(p[1] for p in base_poly) / len(base_poly))
    if (bc[0] - A[0]) * nx + (bc[1] - A[1]) * ny < 0:
        nx, ny = -nx, -ny

    # the slab's thickness, on real page edges only
    base_free = free_arc(base_poly, A, B)
    flap_free = free_arc(flap_poly, A, B)
    page_edge = ribbon(base_free, THICK_PAGE * 0.26, THICK_PAGE)
    flap_edge = ribbon(flap_free, THICK_FLAP * 0.24, THICK_FLAP)

    # The flap folded over lands wholly inside the base half, so the object's
    # outline IS the base half: a page with one corner cut away on the diagonal.
    sil = base_poly

    # the chart, printed on the page's reverse and carried by the same map
    def cy(f):
        return CHART_Y0 + (CHART_Y1 - CHART_Y0) * f
    step_pts = [(CHART_BASE_X + rise, cy(f)) for f, rise in CHART_STEPS]
    # squared step corners: a run along the baseline, then a riser across it
    stepped = [step_pts[0]]
    for i in range(1, len(step_pts)):
        stepped.append((stepped[-1][0], step_pts[i][1]))
        stepped.append(step_pts[i])
    chart_line = [fold(p) for p in stepped]
    chart_base = [fold((CHART_BASE_X, CHART_Y0)), fold((CHART_BASE_X, CHART_Y1))]

    # gradient axes, all hung off the one key light (top, biased left) or off the
    # crease frame, so no field can disagree with another about the light
    creaseC = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    far = max(flap_poly, key=lambda p: (p[0] - creaseC[0]) * nx + (p[1] - creaseC[1]) * ny)
    fdist = (far[0] - creaseC[0]) * nx + (far[1] - creaseC[1]) * ny

    # the lit half of each outline, for the directional arris roll: a rolled edge
    # is bright where it faces the key and dark where it turns away, and a rim
    # stroked evenly all the way round is the single most common way an authored
    # SVG announces that nobody decided where the light was.
    def lit_arc(pts, lo=True, closed=True):
        cx = sum(q[0] for q in pts) / len(pts)
        cy = sum(q[1] for q in pts) / len(pts)
        out, run = [], []
        n = len(pts)
        last = n if closed else n - 1
        for i in range(last):
            a1, b1 = pts[i], pts[(i + 1) % n]
            ex, ey = b1[0] - a1[0], b1[1] - a1[1]
            nrm = (ey, -ex)
            mx, my = (a1[0] + b1[0]) / 2 - cx, (a1[1] + b1[1]) / 2 - cy
            if nrm[0] * mx + nrm[1] * my < 0:       # make it point outward
                nrm = (-nrm[0], -nrm[1])
            if (nrm[0] * KEY[0] + nrm[1] * KEY[1] > 0) == lo:
                run.append(a1)
            elif run:
                out.append(run + [a1])
                run = []
        if run:
            out.append(run)
        return [a for a in out if len(a) > 2]

    g = []
    g.append(f'''<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1024" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="0.52" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/></linearGradient>''')
    g.append(f'''<radialGradient id="crown" cx="430" cy="120" r="740" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.90"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>''')
    g.append(f'''<radialGradient id="vig" cx="512" cy="500" r="690" gradientUnits="userSpaceOnUse">
      <stop offset="0.62" stop-color="{GROUND_VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{GROUND_VIGNETTE}" stop-opacity="0.13"/></radialGradient>''')
    g.append(f'''<linearGradient id="pageFace" x1="{PAGE_X0 - 90}" y1="{PAGE_Y0 - 70}" x2="{PAGE_X1 + 60}" y2="{PAGE_Y1 + 80}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{PAGE_LIT}"/><stop offset="0.44" stop-color="{PAGE_MID}"/>
      <stop offset="1" stop-color="{PAGE_LOW}"/></linearGradient>''')
    g.append(f'''<linearGradient id="pageEdge" x1="{PAGE_X0}" y1="{PAGE_Y0}" x2="{PAGE_X1}" y2="{PAGE_Y1}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{PAGE_EDGE_LIT}"/><stop offset="0.58" stop-color="#EBE3D3"/>
      <stop offset="1" stop-color="{PAGE_EDGE_LOW}"/></linearGradient>''')
    # the flap's face runs along the crease NORMAL: darkest in the V, opening out
    g.append(f'''<linearGradient id="flapFace" x1="{creaseC[0]:.1f}" y1="{creaseC[1]:.1f}" x2="{creaseC[0] + nx * fdist:.1f}" y2="{creaseC[1] + ny * fdist:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{FLAP_DEEP}"/><stop offset="0.34" stop-color="{FLAP_MID}"/>
      <stop offset="1" stop-color="{FLAP_FREE}"/></linearGradient>''')
    g.append(f'''<linearGradient id="flapAcross" x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7E1A02" stop-opacity="0.22"/>
      <stop offset="0.46" stop-color="#FFFFFF" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.13"/></linearGradient>''')
    g.append(f'''<linearGradient id="creaseRoll" x1="{creaseC[0]:.1f}" y1="{creaseC[1]:.1f}" x2="{creaseC[0] + nx * CREASE_ROLL:.1f}" y2="{creaseC[1] + ny * CREASE_ROLL:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{CREASE_CREST}"/><stop offset="0.42" stop-color="{CREASE_CREST_2}"/>
      <stop offset="1" stop-color="{FLAP_MID}" stop-opacity="0"/></linearGradient>''')
    g.append(f'''<linearGradient id="flapEdge" x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#C33812"/><stop offset="0.55" stop-color="#F0793F"/>
      <stop offset="1" stop-color="#B92C0A"/></linearGradient>''')
    g.append(f'''<radialGradient id="bounce" cx="{creaseC[0]:.1f}" cy="{creaseC[1]:.1f}" r="430" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{BOUNCE}" stop-opacity="0.40"/>
      <stop offset="0.55" stop-color="{BOUNCE}" stop-opacity="0.09"/>
      <stop offset="1" stop-color="{BOUNCE}" stop-opacity="0"/></radialGradient>''')

    f = []
    f.append('<filter id="bS" x="-30%" y="-30%" width="160%" height="160%">'
             '<feGaussianBlur stdDeviation="24"/></filter>')
    f.append('<filter id="bM" x="-30%" y="-30%" width="160%" height="160%">'
             '<feGaussianBlur stdDeviation="12"/></filter>')
    f.append('<filter id="bF" x="-30%" y="-30%" width="160%" height="160%">'
             '<feGaussianBlur stdDeviation="4.5"/></filter>')
    f.append('<filter id="bXL" x="-40%" y="-40%" width="180%" height="180%">'
             '<feGaussianBlur stdDeviation="44"/></filter>')

    clips = [f'<clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>',
             f'<clipPath id="pageClip" clip-rule="evenodd"><path d="{poly(base_poly)}"/></clipPath>',
             f'<clipPath id="flapClip" clip-rule="evenodd"><path d="{poly(flap_poly)}"/></clipPath>']

    # ------------------------------------------------------------------ layers
    bg = [f'<path d="{SQUIRCLE}" fill="url(#ground)"/>',
          f'<path d="{SQUIRCLE}" fill="url(#crown)"/>',
          f'<path d="{SQUIRCLE}" fill="url(#vig)"/>',
          f'<path d="{SQUIRCLE}" fill="none" stroke="{RIM_RING}" stroke-opacity="0.60" stroke-width="3"/>']

    mid = [
        # the sheet's contact shadow on the porcelain: three radii, all warm.
        # Measured r05: the darkest pixel under the reference's page reads 0.647
        # where the first draft only reached 0.804, so the sheet was floating
        # rather than resting. The tight radius is what actually seats it.
        f'<g filter="url(#bXL)" opacity="0.19"><path d="{poly(shift(sil, 8, 42))}" fill="{SHADOW}"/></g>',
        f'<g filter="url(#bS)" opacity="0.30"><path d="{poly(shift(sil, 5, 22))}" fill="{SHADOW}"/></g>',
        f'<g filter="url(#bM)" opacity="0.34"><path d="{poly(shift(sil, 2, 10))}" fill="{SHADOW}"/></g>',
        # the slab's own thickness, on the page's real edges only
        f'<path d="{poly(page_edge)}" fill="url(#pageEdge)"/>',
        # the page's outer face: blank, because no two published pages look alike
        f'<path d="{poly(base_poly)}" fill="url(#pageFace)"/>',
        # what the inner face throws back onto it
        f'<g clip-path="url(#pageClip)"><path d="{poly(base_poly)}" fill="url(#bounce)"/></g>',
        # the flap's shadow on the page: hinged at the crease, so the gap - and
        # the shadow - grow with distance from it
        f'<g clip-path="url(#pageClip)"><g filter="url(#bM)" opacity="0.30">'
        f'<path d="{poly(shift(flap_poly, 8, 26))}" fill="{SHADOW}"/></g></g>',
        f'<g clip-path="url(#pageClip)"><g filter="url(#bS)" opacity="0.22">'
        f'<path d="{poly(shift(flap_poly, 14, 48))}" fill="#B8471A"/></g></g>',
    ]

    fg = [
        # the inner face
        f'<path d="{poly(flap_poly)}" fill="url(#flapFace)"/>',
        f'<g clip-path="url(#flapClip)"><path d="{poly(flap_poly)}" fill="url(#flapAcross)"/></g>',
        # the V's own occlusion, hugging the crease from inside the flap. Two
        # widths, because they answer different measurements: the wide soft one
        # sets the core (L 0.461 against the references' 0.466 and 0.469) and the
        # narrow deep one sets the DARKEST pixel, which is a separate check - r01
        # fixed the core and left the dark end at 0.388 where the two references
        # read 0.337 and 0.212. A ramp with the right middle can still have no
        # bottom.
        #
        # Both bands sit BEYOND the crease roll, on the +n side, because +n points
        # into the half the flap folded onto and therefore into the flap. Authored
        # the other way for six rounds, they were clipped almost entirely away by
        # flapClip - which is why the darkest pixel would not move however hard the
        # opacity was pushed. A material that will not respond to its own constant
        # is a clipping question, not a colour one.
        f'<g clip-path="url(#flapClip)"><g filter="url(#bM)" opacity="{AO_CREASE_OPACITY}">'
        f'<path d="{poly(offset_poly([A, B], CREASE_ROLL * 0.5, nx, ny) + offset_poly([B, A], CREASE_ROLL + 30, nx, ny))}" fill="{FLAP_AO}"/></g></g>',
        f'<g clip-path="url(#flapClip)"><g filter="url(#bF)" opacity="{AO_CREASE_DEEP}">'
        f'<path d="{poly(offset_poly([A, B], CREASE_ROLL * 0.62, nx, ny) + offset_poly([B, A], CREASE_ROLL + AO_DEEP_W, nx, ny))}" fill="{AO_DEEP}"/></g></g>',
        # the evidence, printed on the page's reverse and folded into view
        f'<g clip-path="url(#flapClip)">'
        f'<path d="{poly(chart_base, close=False)}" fill="none" stroke="{CHART_FROST}" '
        f'stroke-opacity="{CHART_BASE_OPACITY}" stroke-width="{CHART_BASE_W}" stroke-linecap="round"/>'
        f'<path d="{poly(chart_line, close=False)}" fill="none" stroke="{CHART_FROST}" '
        f'stroke-opacity="{CHART_OPACITY}" stroke-width="{CHART_W}" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</g>',
    ]

    hl = [
        # the crease: a rolled crest, the object's own outline down its lower
        # right, and the one place the inside of the page comes out
        f'<g clip-path="url(#flapClip)"><path d="{poly(offset_poly([A, B], -3, nx, ny) + offset_poly([B, A], CREASE_ROLL, nx, ny))}" '
        f'fill="url(#creaseRoll)" filter="url(#bF)"/></g>',
        # rim scatter: a translucent body gains luminance and LOSES saturation at
        # grazing angles, in every quadrant, not only where the key can reach
        f'<g clip-path="url(#flapClip)"><path d="{poly(flap_poly)}" fill="none" stroke="{RIM_SCATTER}" '
        f'stroke-width="30" stroke-opacity="0.50" filter="url(#bM)"/></g>',
        # the flap's own slab thickness: its cut face, turned up into the key and
        # toward the viewer, so it reads as a crest inside the silhouette. Measured
        # off the reference at +0.36 over the flap face across 12-16px. r02 also
        # carried the reference's ~30px falloff behind it and was REJECTED for it:
        # the flap's free edge is a live figure-ground boundary, and a wide lift
        # inside it fills the value gap the 32px read depends on (self_contrast
        # 0.365 -> 0.339). The crest survives because it is 0.5px at 32px; the
        # falloff does not, because it is 1.3px of a wide band. Fade the frost
        # where no boundary lives, never across one.
    ] + [
        f'<g clip-path="url(#flapClip)"><path d="{poly(arc, close=False)}" fill="none" '
        f'stroke="{FLAP_CREST}" stroke-width="{FLAP_CREST_W:.0f}" stroke-opacity="0.88" '
        f'stroke-linecap="butt" filter="url(#bF)"/></g>'
        for arc in lit_arc(flap_free, True, closed=False)
    ] + [
        f'<g clip-path="url(#flapClip)"><path d="{poly(arc, close=False)}" fill="none" '
        f'stroke="{FLAP_AO}" stroke-width="{FLAP_CREST_W * 1.1:.0f}" stroke-opacity="0.30" '
        f'stroke-linecap="butt" filter="url(#bF)"/></g>'
        for arc in lit_arc(flap_free, False, closed=False)
    ]
    # the page's own arris roll, split by whether the edge faces the key
    for arc in lit_arc(base_poly, True):
        hl.append(f'<g clip-path="url(#pageClip)"><path d="{poly(arc, close=False)}" fill="none" '
                  f'stroke="#FFFFFF" stroke-width="{FILLET_PAGE}" stroke-opacity="0.80" '
                  f'stroke-linecap="round" filter="url(#bM)"/></g>')
    for arc in lit_arc(base_poly, False):
        hl.append(f'<g clip-path="url(#pageClip)"><path d="{poly(arc, close=False)}" fill="none" '
                  f'stroke="{SHADOW}" stroke-width="{FILLET_PAGE * 1.3:.0f}" stroke-opacity="0.16" '
                  f'stroke-linecap="round" filter="url(#bM)"/></g>')
    hl.append(
        # the crest catches the key hardest along the whole spine: one hairline
        f'<g clip-path="url(#flapClip)"><path d="{poly(offset_poly([A, B], 0, nx, ny) + offset_poly([B, A], 6, nx, ny))}" '
        f'fill="#FFFFFF" fill-opacity="0.55" filter="url(#bF)"/></g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">
<defs>
{chr(10).join(g)}
{chr(10).join(f)}
{chr(10).join(clips)}
</defs>
<g clip-path="url(#tile)">
<g id="bg">
{chr(10).join(bg)}
</g>
<g id="mid">
{chr(10).join(mid)}
</g>
<g id="fg">
{chr(10).join(fg)}
</g>
<g id="highlight">
{chr(10).join(hl)}
</g>
</g>
</svg>
'''
    return svg, dict(A=A, B=B, base=base_poly, flap=flap_poly, sil=sil)


if __name__ == "__main__":
    svg, info = build()
    out = ASSETS / "icon.svg"
    out.write_text(svg)
    xs = [p[0] for p in info["sil"]]
    ys = [p[1] for p in info["sil"]]
    print(f"wrote {out} ({len(svg)} bytes)")
    print(f"  crease  A={info['A']}  B={info['B']}")
    print(f"  focal bbox x {min(xs):.0f}..{max(xs):.0f}  y {min(ys):.0f}..{max(ys):.0f}")
    print(f"  focal    {(max(xs)-min(xs))/W*100:.1f}% of tile width, "
          f"{(max(ys)-min(ys))/W*100:.1f}% of height")
    print(f"  margins  L {min(xs):.0f}  R {W-max(xs):.0f}  T {min(ys):.0f}  B {W-max(ys):.0f}")
