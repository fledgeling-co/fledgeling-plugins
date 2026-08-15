#!/usr/bin/env python3
"""
Engine A — hand-authored layered SVG master for the ship-feature icon.

Direction "The Launch": Tahoe gel-glass sub-register (a) — porcelain cushion +
one gel object with a real contact shadow — crossed with device bank #16 (the
icon performs the verb), #21 (overlap-as-identity) and #22 (emissive interior
as the sanctioned second light).

Subject: ship-feature takes ONE feature all the way to merged. So the icon is
one complete vessel at the single instant of launch — stern still riding the
slipway rails, bow already down through the water, throwing an ember-lit bow
wave. Not three hulls (ship-armada), not a hull on a cradle (the shipyard
icon), not a dark trawler (trawl), and deliberately not the pale amber dinghy
poised dry on blue trestles that create-swe-project already owns: this vessel
is decked and complete, the palette is warm porcelain and graphite rather than
cool blue, the accent has moved off the hull and onto the water, and the moment
is motion rather than repose.

SIGNATURE MOVE — the waterline crosses the hull. One object in two states at
once: the stern half is dry gel above the line, the bow half reads *through* a
translucent water plane below it, and the ember bow wave breaks exactly where
the two meet. That crossing is the mark. It is authored as a literal overlap
(hull drawn whole, water plane painted over it at partial opacity) so the blend
is real geometry rather than a baked gradient, which is what keeps rubric #10
honest under Dark/Clear/Tinted.

Geometry lives in the hull's own keel frame (u from stern to bow along the
keel, v down from the sheer) and reaches the canvas through ONE rotation +
translation, so the hull, the deck plane, the deckhouse, the rails and the
wave's entry point cannot drift out of register. The deck is the same frame
displaced by one shared FAR vector, which is what gives the hull a top face
without a second projection to keep in sync. Every constant is named; a
fidelity round is a parameter edit, never path surgery.

Corpus-measured values this master is built from (apple-2026 captures 06 Home,
18 telescope, 28 Photos, 30 box, sampled inside the tile):
  · porcelain ground ramps 1.000 at top centre → 0.922 at bottom centre, a
    0.078 luminance drop, key light top and very slightly left;
  · the warm gel object's median is #FFBD4A (hue 38, S 0.71) and its SHADOW end
    is #F69E37 — saturation RISES 0.71 → 0.78 as value falls, so a gel that
    desaturates in shadow reads opaque;
  · the contact shadow under a warm object is warm, not dark: (235,226,213)
    against a (235,235,235) ground, ΔL only 0.034 at contact, fully recovered
    by ~20px on a 412 tile (~50px at 1024).

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import pathlib
import re

W = 1024
HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE / "squircle-path.txt").read_text().strip()

# ------------------------------------------------------------------ palette
# Family 1 — warm neutral: porcelain ground, stone slipway, graphite hull.
GROUND_TOP = "#FAF7F1"
GROUND_MID = "#F2ECE2"
GROUND_BOT = "#E4DBCB"
RIM_LIGHT = "#FFFFFF"
VIGNETTE = "#B3A793"

WATER_FAR = "#C6BDAC"          # at the waterline, reflecting the bright sky
WATER_MID = "#ADA492"
WATER_NEAR = "#8E8572"         # nearest the viewer, deepest
WATER_EDGE = "#F7F3EB"         # the lit lip along the waterline itself

STONE_TOP = "#DED5C6"          # slipway top surface, catching the key
STONE_FACE = "#B9AD98"
STONE_DEEP = "#93866F"
RAIL_TOP = "#7A6E5C"
RAIL_FACE = "#514637"

HULL_LIT = "#5A616A"           # topside strake, facing the key
HULL_BODY = "#3C424B"
HULL_SHADE = "#262B33"
HULL_DEEP = "#181A20"
HULL_WARM_AO = "#2C2420"       # the darkest pixel is WARM: nothing here emits cool light
DECK_LIT = "#F2ECE1"           # the deck plane — frosted porcelain, the era's material
DECK_SHADE = "#D2C9B9"
HOUSE_LIT = "#F7F3EB"
HOUSE_SHADE = "#C6BCAB"
SHEER_STRAKE = "#EBE4D7"

# Family 2 — ember. Reserved entirely for the bow wave and the light it throws.
EMBER_CORE = "#FF8A3D"
EMBER_MID = "#E9682F"
EMBER_DEEP = "#B93C19"
EMBER_FOAM = "#FFD9B6"
EMBER_BLOOM = "#FFA35C"

# ------------------------------------------------------------------ geometry
WATER_Y = 636.0                # the waterline, canvas y

# hull keel frame → canvas: rotate by HULL_DEG, then translate STERN
STERN = (140.0, 350.0)         # sheer at the transom, canvas
HULL_DEG = 18.6                # bow-down rake; steeper than the ramp's 16.4°,
                               # which is exactly what "the stern is still on the
                               # rails and the bow has already dropped" looks like
HULL_LEN = 682.0               # ≈63% of the tile along the keel
HULL_DEP = 162.0               # sheer to keel

# the near-side hull and the far-side deck edge differ by ONE displacement, so
# the top face exists without a second projection to keep in register
FAR = (21.0, -27.0)

RAMP_DEG = 16.4                # the slipway's own slope
RAMP_ORIGIN = (-60.0, 430.0)
RAMP_LEN = 940.0
RAMP_THICK = 46.0
RAIL_GAUGE = 52.0              # perpendicular offset between the two rails

DECKHOUSE_U0, DECKHOUSE_U1 = 0.170, 0.408
DECKHOUSE_H = 84.0

_c, _s = math.cos(math.radians(HULL_DEG)), math.sin(math.radians(HULL_DEG))


def hull(u, v, far=0.0):
    """Keel frame (u along the keel 0→1, v down from the sheer in px) → canvas.

    `far` in [0,1] slides the point across to the far side of the vessel along
    the one shared displacement, so deck, sheer and flank share a frame.
    """
    x, y = u * HULL_LEN, v
    return (STERN[0] + x * _c - y * _s + FAR[0] * far,
            STERN[1] + x * _s + y * _c + FAR[1] * far)


_rc, _rs = math.cos(math.radians(RAMP_DEG)), math.sin(math.radians(RAMP_DEG))


def ramp(t, v):
    x, y = t * RAMP_LEN, v
    return (RAMP_ORIGIN[0] + x * _rc - y * _rs, RAMP_ORIGIN[1] + x * _rs + y * _rc)


def sheer(u):
    """Deck edge, keel-frame v. Negative is above the transom's sheer.

    A real sheer dips amidships and lifts at both ends, hardest at the bow.
    One sine plus one bow term keeps it a two-parameter curve a round can move.
    """
    return 11.0 * math.sin(math.pi * u) - 46.0 * (max(0.0, u - 0.46) / 0.54) ** 2.0


def keel(u):
    """Bottom of the hull, keel-frame v."""
    if u < 0.09:                                   # transom tuck
        return HULL_DEP - 30.0 + 3700.0 * u * u / 30.0
    if u > 0.70:                                   # forefoot sweeping up to the stem
        t = (u - 0.70) / 0.30
        return HULL_DEP - (HULL_DEP - sheer(1.0) - 14.0) * (t ** 2.1)
    return HULL_DEP


def fmt(pts, close=True):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


N = 96


def flank_outline():
    """The near side of the hull: sheer over keel."""
    top = [hull(i / N, sheer(i / N)) for i in range(N + 1)]
    bot = [hull(i / N, keel(i / N)) for i in range(N, -1, -1)]
    return top + bot


def deck_plane():
    """The top face: near sheer, then the far sheer coming back."""
    near = [hull(i / N, sheer(i / N)) for i in range(N + 1)]
    far = [hull(i / N, sheer(i / N) + 4.0, far=1.0) for i in range(N, -1, -1)]
    return near + far


def strake(a, b):
    top = [hull(i / N, sheer(i / N) + a) for i in range(N + 1)]
    bot = [hull(i / N, sheer(i / N) + b) for i in range(N, -1, -1)]
    return top + bot


def deckhouse():
    u0, u1, n = DECKHOUSE_U0, DECKHOUSE_U1, 20
    roof = [hull(u0 + (u1 - u0) * i / n, sheer(u0 + (u1 - u0) * i / n) - DECKHOUSE_H, far=0.62)
            for i in range(n + 1)]
    sill = [hull(u0 + (u1 - u0) * i / n, sheer(u0 + (u1 - u0) * i / n) - 2.0, far=0.62)
            for i in range(n, -1, -1)]
    return roof + sill


def deckhouse_roof():
    """The roof overhangs the house on every side — one eaves constant, so the
    overhang cannot drift away from the wall it belongs to."""
    u0, u1, n = DECKHOUSE_U0 - 0.018, DECKHOUSE_U1 + 0.018, 20
    y = -DECKHOUSE_H - 6.0
    near = [hull(u0 + (u1 - u0) * i / n, sheer(u0 + (u1 - u0) * i / n) + y, far=0.46)
            for i in range(n + 1)]
    far = [hull(u0 + (u1 - u0) * i / n, sheer(u0 + (u1 - u0) * i / n) + y + 13.0, far=1.20)
           for i in range(n, -1, -1)]
    return near + far


# where the forefoot pierces the waterline — the wave's anchor, derived not guessed
def stem_entry():
    lo, hi = 0.70, 1.0                              # forefoot runs deep → shallow
    for _ in range(60):
        mid = (lo + hi) / 2
        if hull(mid, keel(mid))[1] > WATER_Y:
            lo = mid
        else:
            hi = mid
    return hull(lo, keel(lo)), lo


ENTRY, ENTRY_U = stem_entry()
BOW_TIP = hull(1.0, sheer(1.0))

# ------------------------------------------------------------------ squircle


def _cubic(p0, p1, p2, p3, n):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def parse_path(d):
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


TILE_D = fmt(parse_path(SQUIRCLE))


# ------------------------------------------------------------------ the wave
# A breaking bow wave is a SWEPT SURFACE, not an outline: a spine curve (the
# crest line the hull is throwing) with a thickness profile along it. Authoring
# it as an outline is the documented way to get a flat coil instead of a curl
# (material-recipes, "curl / ribbon volume").
#
# It is built in TWO halves that straddle the hull, which is what stops the
# accent from swallowing the silhouette it is supposed to be lighting: a PLUME
# rising behind the bow, drawn before the hull so the stem cuts it, and a low
# CRESCENT running in front along the waterline, drawn after. Both spines start
# from the derived entry point, so the whole wave stays welded to the bow when
# the rake changes.

PLUME_CTRL = (34.0, -86.0)    # relative to the entry
PLUME_TIP = (104.0, -138.0)
CRESC_FWD = 176.0              # how far forward of the entry the crescent runs
CRESC_AFT = 268.0              # …and aft
WASH_AFT = 360.0               # the wake behind that


def _bez(a, c, b, n):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1])
            for t in (i / n for i in range(n + 1))]


def ribbon(spine, wfn, bias=0.0):
    """Sweep a thickness profile along a spine; returns a closed outline.

    `wfn(t)` is the full width at parameter t, so a crescent (fat in the
    middle, nothing at the ends) and a plume (fat at the base, a point at the
    tip) come off the same generator rather than out of two code paths.
    `bias` pushes the thickness to one side, which is what makes a breaking
    crest sit heavier on its windward face than on its hollow.
    """
    left, right = [], []
    n = len(spine) - 1
    for i, (x, y) in enumerate(spine):
        w = wfn(i / n) * 0.5
        j = min(max(i, 1), n)
        dx, dy = spine[j][0] - spine[j - 1][0], spine[j][1] - spine[j - 1][1]
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m, dx / m
        left.append((x + nx * w * (1 + bias), y + ny * w * (1 + bias)))
        right.append((x - nx * w * (1 - bias), y - ny * w * (1 - bias)))
    return left + right[::-1]


def plume_spine(n=28, lift=0.0):
    ex, _ = ENTRY
    return _bez((ex - 44, WATER_Y + 16),
                (ex + PLUME_CTRL[0], WATER_Y + PLUME_CTRL[1] - lift),
                (ex + PLUME_TIP[0], WATER_Y + PLUME_TIP[1] - lift), n)


# r08, the third wave scaffold and the one that holds. The first gave the wave
# a legible shape and no water in it; the second gave it water and no shape.
# What both missed is the single feature that says "breaking" rather than
# "hill": an ASYMMETRIC profile whose lip overhangs its own hollow. That is not
# something a symmetric envelope can be persuaded into, so the crest's top edge
# is an explicit control polyline — a long windward rise, the peak just forward
# of the stem, then a short steep fall — resampled with smoothstep and given
# the chop broken water carries.
CREST_PROFILE = ((-262, 0), (-208, 9), (-160, 15), (-116, 29), (-78, 25),
                 (-40, 45), (-6, 60), (28, 66), (54, 62), (78, 51),
                 (98, 35), (116, 18), (134, 0))
LIP_ARC = ((-28, 52), (20, 70), (62, 65), (94, 49), (116, 33))
CREST_H = 66.0                # the profile's own peak, for normalising


def _profile(scale=1.0, lift=0.0, rough=1.0, n=8):
    out = []
    for k in range(len(CREST_PROFILE) - 1):
        (x0, h0), (x1, h1) = CREST_PROFILE[k], CREST_PROFILE[k + 1]
        for i in range(n):
            t = i / n
            x = x0 + (x1 - x0) * t
            h = h0 + (h1 - h0) * (t * t * (3 - 2 * t))          # smoothstep
            g = (k + t) / (len(CREST_PROFILE) - 1)
            h += rough * 5.0 * (h / CREST_H) * math.sin(g * 31.0 + 0.6)
            out.append((x, max(0.0, h) * scale + (lift if h > 3 else 0.0)))
    out.append((CREST_PROFILE[-1][0], 0.0))
    return out


def foam_crest(n=150, scale=1.0, lift=0.0, rough=1.0):
    ex, _ = ENTRY
    prof = _profile(scale, lift, rough)
    top = [(ex + x, WATER_Y + 12 - h) for x, h in prof]
    bot = [(ex + x, WATER_Y + 12 - h * 0.04 + 15 * (h / CREST_H) ** 1.15 * scale)
           for x, h in prof]
    return top + bot[::-1]


def _lip_spine(out=0.0, n=7):
    ex, _ = ENTRY
    pts = []
    for i in range(len(LIP_ARC) - 1):
        (x0, h0), (x1, h1) = LIP_ARC[i], LIP_ARC[i + 1]
        for k in range(n):
            t = k / n
            x = x0 + (x1 - x0) * t
            h = h0 + (h1 - h0) * (t * t * (3 - 2 * t))
            pts.append((ex + x, WATER_Y + 12 - h - out))
    pts.append((ex + LIP_ARC[-1][0], WATER_Y + 12 - LIP_ARC[-1][1] - out))
    return pts


def crest_lip():
    """The rolled edge, reaching PAST the crest body so the lip overhangs."""
    return ribbon(_lip_spine(),
                  lambda t: 4.5 + 12.0 * math.sin(math.pi * min(1.0, t * 1.18)) ** 0.6)


def crest_hollow():
    """The shadowed water the lip is curling over — what says 'breaking'."""
    sp = _lip_spine(out=-19)
    half = sp[len(sp) // 2:]
    return half + [(half[-1][0] - 30, half[-1][1] + 38), (half[0][0] + 8, half[0][1] + 46)]


def wash_spine(n=24):
    ex, _ = ENTRY
    return _bez((ex - CRESC_AFT + 20, WATER_Y + 30),
                (ex - WASH_AFT * 0.6, WATER_Y + 12),
                (ex - WASH_AFT, WATER_Y + 44), n)


def w_plume(t):
    return 66.0 * (1.0 - t) ** 1.35 + 7.0


def w_crescent(t):
    return 64.0 * math.sin(math.pi * t) ** 0.8 + 5.0


def w_foam(t):
    return 20.0 * math.sin(math.pi * t) ** 0.6 + 3.0


def w_wash(t):
    return 26.0 * (1.0 - t) + 5.0


def glint(dy, w, op, x0=-1.0, x1=1.0):
    """A horizontal band of reflected sky. Water at icon scale reads as
    horizontal banding, never as concentric rings on a floor."""
    return (f'<rect x="{x0 * 60:.0f}" y="{WATER_Y + dy:.1f}" width="{(x1 - x0) * 620:.0f}" '
            f'height="{w:.1f}" rx="{w / 2:.1f}" fill="{WATER_EDGE}" fill-opacity="{op}" filter="url(#fHair)"/>')


# ------------------------------------------------------------------ emit

def svg():
    ex, ey = ENTRY
    flank_d = fmt(flank_outline())
    p = []
    A = p.append

    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">')
    A("<defs>")

    A(f'''<radialGradient id="gGround" cx="0.50" cy="0.04" r="1.10">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset="0.55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </radialGradient>''')
    A(f'''<radialGradient id="gVignette" cx="0.5" cy="0.48" r="0.76">
      <stop offset="0.60" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.32"/>
    </radialGradient>''')

    A(f'''<linearGradient id="gWater" x1="0" y1="{WATER_Y}" x2="0" y2="{W + 20}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{WATER_FAR}"/>
      <stop offset="0.40" stop-color="{WATER_MID}"/>
      <stop offset="1" stop-color="{WATER_NEAR}"/>
    </linearGradient>''')

    A(f'''<linearGradient id="gStone" x1="0.20" y1="0" x2="0.58" y2="1">
      <stop offset="0" stop-color="{STONE_TOP}"/>
      <stop offset="0.48" stop-color="{STONE_FACE}"/>
      <stop offset="1" stop-color="{STONE_DEEP}"/>
    </linearGradient>''')
    A(f'''<linearGradient id="gRail" x1="0.2" y1="0" x2="0.5" y2="1">
      <stop offset="0" stop-color="{RAIL_TOP}"/>
      <stop offset="1" stop-color="{RAIL_FACE}"/>
    </linearGradient>''')

    # every hull face hangs off ONE axis in user space, so no face acquires a
    # private light direction (objectBoundingBox units are the documented trap)
    kx0, ky0 = hull(0.0, -DECKHOUSE_H - 40.0)
    kx1, ky1 = hull(0.0, HULL_DEP + 40.0)
    A(f'''<linearGradient id="gFlank" x1="{kx0:.1f}" y1="{ky0:.1f}" x2="{kx1:.1f}" y2="{ky1:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0.24" stop-color="{HULL_LIT}"/>
      <stop offset="0.40" stop-color="{HULL_BODY}"/>
      <stop offset="0.76" stop-color="{HULL_SHADE}"/>
      <stop offset="1" stop-color="{HULL_DEEP}"/>
    </linearGradient>''')
    A(f'''<linearGradient id="gDeckPlane" x1="{kx0:.1f}" y1="{ky0:.1f}" x2="{kx1:.1f}" y2="{ky1:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0.18" stop-color="{DECK_LIT}"/>
      <stop offset="0.42" stop-color="{DECK_SHADE}"/>
    </linearGradient>''')
    A(f'''<linearGradient id="gHouse" x1="{kx0:.1f}" y1="{ky0:.1f}" x2="{kx1:.1f}" y2="{ky1:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0.02" stop-color="{HOUSE_LIT}"/>
      <stop offset="0.30" stop-color="{HOUSE_SHADE}"/>
    </linearGradient>''')
    A(f'''<linearGradient id="gEmberOnHull" x1="{ex:.1f}" y1="{ey - 40:.1f}" x2="{hull(0.34, 30)[0]:.1f}" y2="{hull(0.34, 30)[1]:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_CORE}" stop-opacity="0.22"/>
      <stop offset="0.15" stop-color="{EMBER_MID}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{EMBER_MID}" stop-opacity="0"/>
    </linearGradient>''')

    A(f'''<radialGradient id="gBloom" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{EMBER_CORE}" stop-opacity="0.92"/>
      <stop offset="0.32" stop-color="{EMBER_BLOOM}" stop-opacity="0.44"/>
      <stop offset="1" stop-color="{EMBER_BLOOM}" stop-opacity="0"/>
    </radialGradient>''')
    # the wave's own body: deepest along its thickest path, brightest at the lip
    A(f'''<linearGradient id="gWave" x1="{ex - 60:.1f}" y1="{WATER_Y + 40:.1f}" x2="{ex + 130:.1f}" y2="{WATER_Y - 250:.1f}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_DEEP}"/>
      <stop offset="0.42" stop-color="{EMBER_MID}"/>
      <stop offset="0.82" stop-color="{EMBER_CORE}"/>
      <stop offset="1" stop-color="{EMBER_FOAM}"/>
    </linearGradient>''')
    A(f'''<linearGradient id="gLip" x1="{ex - 120:.1f}" y1="0" x2="{ex + 250:.1f}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_FOAM}" stop-opacity="0.24"/>
      <stop offset="0.42" stop-color="{EMBER_FOAM}" stop-opacity="0.84"/>
      <stop offset="1" stop-color="#FFF3E6" stop-opacity="0.90"/>
    </linearGradient>''')
    # What separates spray from FLAME is the value ramp along each filament:
    # water thins as it flies and goes white, so the tips are foam and only the
    # roots are hot. Each filament is genuinely its own object with its own
    # axis here — the ramp is the water thinning along its length, not the
    # scene light — so objectBoundingBox units are correct rather than the
    # usual multi-part-object trap.
    A(f'''<linearGradient id="gSpray" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="{EMBER_MID}" stop-opacity="0.95"/>
      <stop offset="0.34" stop-color="{EMBER_CORE}" stop-opacity="0.88"/>
      <stop offset="0.72" stop-color="{EMBER_FOAM}" stop-opacity="0.70"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.28"/>
    </linearGradient>''')

    A('<filter id="fSoft" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="15"/></filter>')
    A('<filter id="fSoftLg" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="36"/></filter>')
    A('<filter id="fTight" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="7"/></filter>')
    A('<filter id="fHair" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="2.6"/></filter>')

    A(f'<clipPath id="cTile" clip-rule="evenodd"><path d="{TILE_D}"/></clipPath>')
    A(f'<clipPath id="cWater" clip-rule="evenodd"><path d="{fmt([(-30, WATER_Y), (W + 30, WATER_Y), (W + 30, W + 30), (-30, W + 30)])}"/></clipPath>')
    A(f'<clipPath id="cFlank" clip-rule="evenodd"><path d="{flank_d}"/></clipPath>')
    A(f'<clipPath id="cHouse" clip-rule="evenodd"><path d="{fmt(deckhouse())}"/></clipPath>')
    A("</defs>")

    A('<g clip-path="url(#cTile)">')

    # ================================================================= bg
    A('<g id="bg">')
    A(f'<rect width="{W}" height="{W}" fill="url(#gGround)"/>')
    A(f'<rect width="{W}" height="{W}" fill="url(#gVignette)"/>')
    A("</g>")

    # ================================================================= mid
    A('<g id="mid">')

    # slipway — drawn before the water so the water drowns its lower end
    A(f'<path d="{fmt([ramp(0, -RAMP_THICK * 0.34), ramp(1, -RAMP_THICK * 0.34), ramp(1, RAMP_THICK), ramp(0, RAMP_THICK)])}" fill="url(#gStone)"/>')
    A(f'<path d="{fmt([ramp(0, -RAMP_THICK * 0.34), ramp(1, -RAMP_THICK * 0.34), ramp(1, -RAMP_THICK * 0.34 + 10), ramp(0, -RAMP_THICK * 0.34 + 10)])}" '
      f'fill="{RIM_LIGHT}" fill-opacity="0.60"/>')
    for off in (-RAIL_GAUGE * 0.5 - 4, RAIL_GAUGE * 0.5 + 4):
        A(f'<path d="{fmt([ramp(0, off - 7), ramp(1, off - 7), ramp(1, off + 7), ramp(0, off + 7)])}" fill="url(#gRail)"/>')
        A(f'<path d="{fmt([ramp(0, off - 7), ramp(1, off - 7), ramp(1, off - 3), ramp(0, off - 3)])}" fill="{RIM_LIGHT}" fill-opacity="0.36"/>')

    # the ramp's contact shadow on the porcelain: warm and shallow, per the corpus
    A(f'<path d="{fmt([ramp(0, RAMP_THICK), ramp(1, RAMP_THICK), ramp(1, RAMP_THICK + 40), ramp(0, RAMP_THICK + 40)])}" '
      f'fill="{HULL_WARM_AO}" fill-opacity="0.15" filter="url(#fSoft)"/>')

    # the hull's cast shadow down the ramp
    sh = [hull(i / 44.0, keel(i / 44.0) + 4) for i in range(45)] + \
         [hull(i / 44.0, keel(i / 44.0) + 60) for i in range(44, -1, -1)]
    A(f'<path d="{fmt(sh)}" fill="{HULL_WARM_AO}" fill-opacity="0.30" filter="url(#fSoft)"/>')

    A("</g>")

    # ================================================================= fg
    A('<g id="fg">')

    # THE PLUME, behind the hull. Drawn before the vessel so the stem cuts it —
    # the wave rises out from behind the bow instead of pasting over it.
    A(f'<ellipse cx="{ex + 60:.1f}" cy="{WATER_Y - 96:.1f}" rx="210" ry="180" fill="url(#gBloom)" opacity="0.46" filter="url(#fSoftLg)"/>')
    A(f'<path d="{fmt(foam_crest(scale=1.30, lift=2, rough=1.6))}" fill="url(#gWave)" fill-opacity="0.90"/>')
    for t, r in ((0.24, 50), (0.44, 38), (0.62, 27), (0.78, 18), (0.92, 11)):
        px, py = plume_spine(12)[max(0, min(12, round(t * 12)))]
        A(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r}" ry="{r * 0.86:.1f}" fill="url(#gWave)" fill-opacity="0.94"/>')
        A(f'<ellipse cx="{px - r * 0.22:.1f}" cy="{py - r * 0.42:.1f}" rx="{r * 0.52:.1f}" ry="{r * 0.34:.1f}" fill="{EMBER_FOAM}" opacity="0.55" filter="url(#fHair)"/>')
    for cx_, cy_, r_, op in ((ex + 112, WATER_Y - 118, 9, 0.78),
                             (ex + 152, WATER_Y - 90, 7, 0.62),
                             (ex + 84, WATER_Y - 150, 5, 0.46),
                             (ex + 158, WATER_Y - 142, 4, 0.34),
                             (ex + 36, WATER_Y - 126, 3, 0.28)):
        A(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{r_}" fill="{EMBER_FOAM}" opacity="{op}"/>')

    # the vessel, whole — the water plane is painted over it afterwards
    A(f'<path d="{flank_d}" fill="url(#gFlank)"/>')

    # occlusion tucked under the deck edge and inside the forefoot
    A('<g clip-path="url(#cFlank)">')
    A(f'<path d="{fmt(strake(16.0, 96.0))}" fill="{HULL_WARM_AO}" fill-opacity="0.30" filter="url(#fTight)"/>')
    A(f'<ellipse cx="{hull(0.04, HULL_DEP * 0.62)[0]:.1f}" cy="{hull(0.04, HULL_DEP * 0.62)[1]:.1f}" rx="66" ry="52" fill="{HULL_WARM_AO}" fill-opacity="0.34" filter="url(#fSoft)"/>')
    A("</g>")

    # the deck: the top face, in the era's frosted porcelain
    A(f'<path d="{fmt(deck_plane())}" fill="url(#gDeckPlane)"/>')
    # sheer strake — the lit band where deck meets flank
    A(f'<path d="{fmt(strake(1.0, 12.0))}" fill="{SHEER_STRAKE}" fill-opacity="0.95"/>')
    A(f'<path d="{fmt(strake(12.0, 19.0))}" fill="{HULL_DEEP}" fill-opacity="0.26"/>')

    # deckhouse: side face, then roof
    A(f'<path d="{fmt(deckhouse())}" fill="url(#gHouse)"/>')
    A('<g clip-path="url(#cHouse)">')
    # the forward face, turned away from the key
    A(f'<path d="{fmt([hull(DECKHOUSE_U1 - 0.046, -DECKHOUSE_H - 14, 0.62), hull(DECKHOUSE_U1, -DECKHOUSE_H - 14, 0.62), hull(DECKHOUSE_U1, 40, 0.62), hull(DECKHOUSE_U1 - 0.046, 40, 0.62)])}" '
      f'fill="{HULL_SHADE}" fill-opacity="0.30"/>')
    # one window band — the detail that names a wheelhouse
    wu0, wu1 = DECKHOUSE_U0 + 0.024, DECKHOUSE_U1 - 0.052
    wband = [hull(wu0 + (wu1 - wu0) * i / 12, sheer(wu0 + (wu1 - wu0) * i / 12) - DECKHOUSE_H + 16, 0.62) for i in range(13)] + \
            [hull(wu0 + (wu1 - wu0) * i / 12, sheer(wu0 + (wu1 - wu0) * i / 12) - DECKHOUSE_H + 44, 0.62) for i in range(12, -1, -1)]
    A(f'<path d="{fmt(wband)}" fill="{HULL_SHADE}" fill-opacity="0.80"/>')
    A(f'<path d="{fmt(wband[:13] + [hull(wu0 + (wu1 - wu0) * i / 12, sheer(wu0 + (wu1 - wu0) * i / 12) - DECKHOUSE_H + 23, 0.62) for i in range(12, -1, -1)])}" '
      f'fill="{RIM_LIGHT}" fill-opacity="0.30"/>')
    # occlusion under the eaves
    A(f'<path d="{fmt(strake(-DECKHOUSE_H - 6, -DECKHOUSE_H + 12))}" fill="{HULL_WARM_AO}" fill-opacity="0.30" filter="url(#fHair)"/>')
    A("</g>")
    A(f'<path d="{fmt(deckhouse_roof())}" fill="{RIM_LIGHT}" fill-opacity="0.90"/>')

    A("</g>")

    # ============================================== the crossing: water over hull
    A('<g id="waterplane" clip-path="url(#cWater)">')
    A(f'<rect x="-30" y="{WATER_Y}" width="{W + 60}" height="{W}" fill="url(#gWater)" fill-opacity="0.90"/>')
    A(f'<rect x="-30" y="{WATER_Y - 2}" width="{W + 60}" height="5" fill="{WATER_EDGE}" fill-opacity="0.55" filter="url(#fHair)"/>')
    A(f'<rect x="-30" y="{WATER_Y + 3}" width="{W + 60}" height="26" fill="{WATER_EDGE}" fill-opacity="0.20" filter="url(#fTight)"/>')
    # the submerged mass darkening the water it displaces
    A(f'<path d="{flank_d}" fill="{HULL_DEEP}" fill-opacity="0.34" filter="url(#fTight)"/>')
    A(f'<path d="{fmt(ribbon(wash_spine(), w_wash))}" fill="{WATER_EDGE}" fill-opacity="0.60" filter="url(#fTight)"/>')
    for k, (dy, sc, op) in enumerate(((16, 1.00, 0.34), (44, 1.44, 0.22), (86, 1.92, 0.13))):
        A(f'<path d="M{ex + 30:.1f},{WATER_Y + dy - 6:.1f} '
          f'Q{ex - 150 * sc:.1f},{WATER_Y + dy + 10 * sc:.1f} {ex - 300 * sc:.1f},{WATER_Y + dy + 34 * sc:.1f} '
          f'L{ex - 300 * sc:.1f},{WATER_Y + dy + 34 * sc + 7 * sc:.1f} '
          f'Q{ex - 150 * sc:.1f},{WATER_Y + dy + 10 * sc + 11 * sc:.1f} {ex + 30:.1f},{WATER_Y + dy + 6:.1f} Z" '
          f'fill="{WATER_EDGE}" fill-opacity="{op}" filter="url(#fHair)"/>')
    A(glint(46, 9, 0.30, -0.10, 0.62))
    A(glint(92, 13, 0.20, 0.05, 0.90))
    A(glint(158, 17, 0.13, -0.10, 0.55))
    A(glint(252, 22, 0.09, 0.20, 1.00))
    # the vessel's own reflection: one mirrored copy, blurred and faded down
    A(f'<g transform="translate(0,{2 * WATER_Y:.1f}) scale(1,-0.86)" mask="mReflect" opacity="0.22">')
    A(f'<path d="{flank_d}" fill="{HULL_SHADE}" filter="url(#fSoftLg)"/>')
    A("</g>")
    # the ember's reflection, stretched into the water as a vertical streak
    A(f'<ellipse cx="{ex + 12:.1f}" cy="{WATER_Y + 132:.1f}" rx="62" ry="150" fill="url(#gBloom)" opacity="0.60" filter="url(#fSoft)"/>')
    A(f'<ellipse cx="{ex + 12:.1f}" cy="{WATER_Y + 46:.1f}" rx="96" ry="44" fill="url(#gBloom)" opacity="0.55" filter="url(#fSoft)"/>')
    for dy, rx, ry, op in ((60, 74, 7, 0.50), (104, 96, 8, 0.34), (166, 118, 9, 0.22), (240, 140, 11, 0.14)):
        A(f'<ellipse cx="{ex + 12:.1f}" cy="{WATER_Y + dy:.1f}" rx="{rx}" ry="{ry}" fill="{EMBER_FOAM}" opacity="{op}" filter="url(#fTight)"/>')
    A("</g>")

    # ================================================================= highlight
    A('<g id="highlight">')

    # THE CREST, in front of the hull: the water the forefoot is shouldering
    # aside, peaking exactly at the entry so it frames the stem rather than
    # hiding it, and lumpy because broken water is.
    # the mist: three soft masses riding the crest arc, largest at the stem
    for dx, dy, rx, ry, op in ((-90, -18, 76, 42, 0.36), (-10, -40, 96, 62, 0.52),
                               (66, -22, 64, 42, 0.34), (126, -4, 38, 25, 0.22)):
        A(f'<ellipse cx="{ex + dx:.1f}" cy="{WATER_Y + dy:.1f}" rx="{rx}" ry="{ry}" '
          f'fill="url(#gBloom)" opacity="{op}" filter="url(#fSoft)"/>')
    # the body of displaced water, softened so it never reads as a moulded lump
    A(f'<path d="{fmt(foam_crest(scale=1.30, lift=6, rough=2.0))}" fill="{EMBER_MID}" fill-opacity="0.40" filter="url(#fSoft)"/>')
    A(f'<path d="{fmt(foam_crest())}" fill="url(#gWave)" fill-opacity="0.96"/>')
    A(f'<path d="{fmt(crest_hollow())}" fill="{EMBER_DEEP}" fill-opacity="0.44" filter="url(#fHair)"/>')
    # emissive core inside it — the sanctioned second light
    A(f'<ellipse cx="{ex - 8:.1f}" cy="{WATER_Y - 6:.1f}" rx="88" ry="28" fill="{EMBER_CORE}" opacity="0.68" filter="url(#fSoft)"/>')
    A(f'<ellipse cx="{ex - 18:.1f}" cy="{WATER_Y - 1:.1f}" rx="56" ry="12" fill="{EMBER_FOAM}" opacity="0.70" filter="url(#fHair)"/>')
    A(f'<ellipse cx="{ex - 22:.1f}" cy="{WATER_Y - 4:.1f}" rx="38" ry="8" fill="{EMBER_FOAM}" opacity="0.60" filter="url(#fHair)"/>')
    # the rolled lit edge along its windward face
    A(f'<path d="{fmt(crest_lip())}" fill="url(#gLip)" filter="url(#fHair)"/>')

    # the light the wave throws back onto the hull's bow flare
    A(f'<g clip-path="url(#cFlank)"><rect width="{W}" height="{W}" fill="url(#gEmberOnHull)"/></g>')

    # one soft key-light rim along the far deck edge
    rim = [hull(i / 60, sheer(i / 60) + 1.0, far=1.0) for i in range(61)] + \
          [hull(i / 60, sheer(i / 60) + 7.0, far=1.0) for i in range(60, -1, -1)]
    A(f'<path d="{fmt(rim)}" fill="{RIM_LIGHT}" fill-opacity="0.70" filter="url(#fHair)"/>')

    # the cushion's inner rim light + edge line, last so nothing paints over them
    A(f'<path d="{TILE_D}" fill="none" stroke="{RIM_LIGHT}" stroke-opacity="0.70" stroke-width="7"/>')
    A(f'<path d="{TILE_D}" fill="none" stroke="{VIGNETTE}" stroke-opacity="0.18" stroke-width="2"/>')

    A("</g>")
    A("</g>")
    A("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(svg())
    print(f"wrote {out}  ({out.stat().st_size} bytes)")
    print(f"  waterline y={WATER_Y}   entry u={ENTRY_U:.3f} at ({ENTRY[0]:.1f},{ENTRY[1]:.1f})")
    print(f"  bow tip ({BOW_TIP[0]:.1f},{BOW_TIP[1]:.1f})   transom sheer {STERN}")
