#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the anvil-errand icon.

Direction "The Return Arc", rebuilt on the family register. Tahoe gel-glass
sub-register (a) - porcelain cushion carrying one dark satin object - crossed
with Direction 1's Tahoe-softened 3D-miniature idiom (matte-satin toy-scale
render with a real contact shadow) and Direction 4's emissive discipline for the
one warm source. Device bank #5 (dual-function primitive), #22 (emissive
interior as the second light), #16 (the icon performs the verb).

WHY THIS IS A REBUILD, NOT A TWEAK. The previous master put a pale steel anvil
on a #000000 -> #2C2F3E dark field. Two things were wrong with it and neither is
a matter of taste. The brand doc reserves the dark deep-sea register for `trawl`
alone, so on the shelf this icon read as trawl's sibling at 16px. And it was the
flattest icon in the set - 77.3% of interior pixels locally uniform - because the
anvil was a single silhouette carrying one linear gradient with a radial vignette
standing in for form. A profile silhouette has one face, and one face can only
ever have one gradient; the flatness was structural, not a shading failure.

So the anvil is now a SOLID rather than a silhouette: the measured profile is
extruded along a single depth axis, the horn tapering to a cone, and every
visible face takes its value from one Lambert term against one key light. That
is the "per-face gradient separation" recipe - three gradients on three faces
beats any amount of filter work on one shape - and it is what buys the material
back. Inverting the value relationship (dark object on porcelain instead of pale
object on black) is what buys the figure-ground: measured 18:1 body-to-ground
against the previous 3:1, on an icon whose whole subject is a black tool.

The signature move is unchanged, because it was right: one incandescent ribbon
leaves the horn's tip, climbs the empty upper right, turns, and comes back down
onto the billet resting on the face - thin where it departs, thick where it
arrives, so the direction of travel reads as ARRIVING. Out and back is the whole
of "errand", and it costs one stroke rather than a second object. What DID change
is its value: on black the arc was a pale ribbon on a dark ground, and on
porcelain the same colour measures 2.98:1 and fails rubric #7. Its body is now
the deep ember (4.18:1) with the hot core reserved for the landing end, where it
crosses the anvil's own dark face.

MEASURED, NOT ASSUMED. Every number in the palette below was sampled out of the
skill's macOS 26 corpus rather than reasoned about:

  porcelain ground   apple-10 / 06 / 18 / 23 all ramp #FFFFFF at 0.10 height to
                     #ECECEC at 0.83, monotonic, neutral (S <= 0.01), brightest
                     at the TOP. The fledgeling family runs the same ramp warm,
                     so this one is warm-neutral and kept light, because the
                     object below is very dark and the accent is amber.
  satin dark metal   apple-15 (Xcode's hammer head) - darkest #121315 L 0.074,
                     body #24262A L 0.148, lit facet #3D3F46 L 0.249, rim catch
                     #C4C8D3 L 0.784, hue ~220 at S 0.12-0.15. Deliberately
                     COOLER than improve-skill's warm brown-charcoal whetstone
                     (#2C241D), which is the one sibling close enough in
                     material to collide.
  amber on porcelain apple-06 (Home) - the emissive gel holds S 1.00 at its
                     darkest (#FC8700), and its spill onto the porcelain reads
                     WARM (#F9B751 tight, #EDE4D7 wide) rather than dark. An
                     emitter on a light ground brightens what it touches.
  contact shadow     apple-12 (Calculator) - darkest contact pixel #545352 at
                     L 0.326 against a local ground of L 0.74, hue 30 at S 0.02.
                     A warm-neutral, not a grey and not a blue.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight. The anvil
solid lives entirely in #mid and carries the identity by itself; every warm
element is #fg or #highlight and is droppable, which is what rubric #10 asks.

Every constant is named and the light is one term, so a fidelity round is a
parameter edit and never path surgery. The banner derives its composition from
this file: LIGHT_DIR is the light axis, DEPTH / VIEW_X / VIEW_Y are the cell
geometry, and HOT_* is the accent.
"""

import math
import pathlib

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------------- view --
# One oblique projection for the whole icon. A point (x, y, z) - x right, y down,
# z into the scene - lands on screen at (x + z*VIEW_X, y + z*VIEW_Y). The far cap
# therefore sits up and to the LEFT, which puts the camera up-left-front and
# makes the top faces, the left end faces and the near flank the visible ones.
#
# Up-LEFT rather than up-right on purpose: the mass grows into the empty upper
# left and leaves the upper right clear for the return arc, and it shows the
# heel's square end - a real rectangle of material - instead of the horn's cone
# apex, which shows nothing.
# VIEW_Y is the view's pitch and it is the one number that decides whether this
# reads as an anvil or as a wedge. At -0.76 the top plane rose 105px on screen,
# the face block became 42% of the object's height, and the horn hung off its
# lower half like a fin. -0.55 is a grazing look-down: enough to see the face you
# strike on, not enough to turn the tool into a lectern.
VIEW_X, VIEW_Y = -0.34, -0.55
DEPTH = 152.0                     # the anvil's width into the scene
HORN_Z_END = 0.10                 # the horn is a cone: depth at the tip, as a
                                  # fraction of DEPTH. Not 0 - a real horn tip is
                                  # rounded, and 0 makes the renderer alias.

# One key light, up-left-front, as a 3D direction of TRAVEL. Every face value in
# the icon is one Lambert term against this vector, so rubric #5 holds by
# construction rather than by eye.
#
# The x:z ratio is what separates the three visible tiers, and the first draft
# got it wrong. At (0.34, 0.82, 0.46) the top plane measured L 0.31 and the near
# flank's own lit end L 0.29, so the working face - the whole reason for the
# three-quarter view - vanished into the front of the tool. Leaning the key
# further left gives top L 0.303 > left end L 0.226 > near flank L 0.174: three
# tiers in the order the ordering predicate wants, brightest nearest the key,
# and a 1.66x top-to-body ratio against apple-15's measured 1.68x.
def _unit(v):
    m = math.sqrt(sum(c * c for c in v))
    return tuple(c / m for c in v)


LIGHT_DIR = _unit((0.52, 0.80, 0.30))

AMBIENT = 0.16                    # how much a face turned fully away still gets
WRAP = 0.13                       # each face's own gradient, +/- this much
                                  # Lambert along the shared key axis

# ------------------------------------------------------------------ geometry --
# The anvil in profile, horn to the right, heel to the left. These proportions
# were settled over six rounds on the previous commission and are carried over
# unchanged, because the profile was never the defect:
#   - the face is chunky enough to be a face (a thin one reads as a clothes iron)
#   - the horn is short enough to be a horn, with its tip in the face's upper
#     third, because a symmetric taper reads as a knife point
#   - the waist is about half the face and the foot about three quarters, and
#     face / waist / base centres stay stacked so it does not lean
#   - the foot is an arch between two feet, which BOTH other engines drew
#     independently where the first master had a plain slab
OFF_X, OFF_Y = 14.0, -40.0         # the one global offset; optical centring is
                                  # this pair of numbers and nothing else

FACE_TOP = 392.0                  # the working face - the near top edge
FACE_BOT = 500.0                  # underside of the face slab
HEEL_X = 240.0                    # the square left end
STEP_X = 590.0                    # where the hardened face stops
STEP_DROP = 17.0                  # the step (the "table") sits this much lower
HORN_X0 = 638.0                   # where the step stops and the horn begins
HORN_TIP = (802.0, 428.0)         # the point. This is also the arrowhead.
HORN_TIP_R = 9.0                  # a blunt tip: a third of a pixel at 32px, and
                                  # what it removes is the aliased needle

WAIST_L_TOP, WAIST_R_TOP = 288.0, 566.0
WAIST_Y = 606.0
WAIST_L, WAIST_R = 336.0, 526.0
BASE_TOP, BASE_BOT = 690.0, 782.0
BASE_L, BASE_R = 284.0, 580.0
BASE_R_CORNER = 18.0
FOOT_W = 76.0                     # each foot's width
ARCH_RISE = 42.0                  # how far the arch cuts up into the base

# The two holes every anvil has, cut into the face plane rather than drawn on it.
# A primitive silhouette reads as generic; the physical features an object would
# actually have are what make it read as observed. Both are small enough to
# dissolve harmlessly below 48px.
HARDIE_U, HARDIE_V, HARDIE_S = 300.0, 62.0, 44.0    # square, near the heel
PRITCHEL_U, PRITCHEL_V, PRITCHEL_R = 372.0, 74.0, 17.0

# The work: a billet of hot metal standing ON the face, left of the horn so the
# tool reads before the glow does. Authored in face-plane coordinates (u along
# the profile axis, v along the depth axis) and projected with the same view
# constants as the anvil, so it cannot drift out of register with the plane it
# rests on.
BILLET_U0, BILLET_U1 = 400.0, 528.0
BILLET_V0, BILLET_V1 = 44.0, 114.0
BILLET_H = 52.0                   # how far it stands above the face

# The return arc: horn tip -> up across the empty upper right -> onto the billet.
# Widths are (at the horn tip, at the billet): thin where it leaves, thick where
# it arrives. The far end tapers to nothing and fades to zero rather than
# touching the horn, because a closed loop over the tool reads as a kettle
# handle and a trajectory cannot be grasped.
ARC_W_FAR, ARC_W_NEAR = 0.6, 21.0
ARC_SAMPLES = 88

# ------------------------------------------------------------------- palette --
# Two hue families only (rubric #6): a cool graphite family for the tool, and one
# warm incandescent family - kin to Fledgeling's #C4622D - reserved for the work
# and its trajectory. The porcelain is warm-neutral and belongs to neither.

PORC_HI = "#FFFEFB"               # cushion top, matching the corpus's brightest
PORC_MID = "#F8F4EC"
PORC_LO = "#E9E2D5"               # cushion bottom
PORC_RIM = "#FFFFFF"              # inner rim light around the perimeter
VIGNETTE = "#B4A992"              # warm edge vignette, very low opacity

# The graphite ramp, indexed by Lambert. Sampled off apple-15's hammer head:
# darkest #121315, body #24262A, lit facet #3D3F46. Hue held near 220 at
# S 0.12-0.15 all the way up, because a shadow that desaturates reads opaque.
GRAPHITE = [
    (0.00, "#0F1115"),
    (0.22, "#1A1E24"),
    (0.38, "#242931"),
    (0.52, "#2F353F"),
    (0.68, "#3B424E"),
    (0.84, "#49515F"),
    (1.00, "#575F6E"),
]
RIM_CATCH = "#C3C8D3"             # measured: the hammer's lit edge, L 0.784
SATIN = "#8D96A5"                 # the broad soft sheen on a struck face
CAVITY = "#0B0D10"                # inside the holes

HOT_CORE = "#FFF3D6"              # the billet's top - the brightest pixel present
HOT_HI = "#FFC55E"
HOT_MID = "#FFA23C"
HOT_EDGE = "#F0601A"
HOT_LO = "#D2430A"                # the arc's body: 4.18:1 on porcelain
HOT_DEEP = "#A82F06"              # holds saturation in shadow (the gel rule)
BOUNCE = "#FF9A46"                # what the billet throws onto the steel
SPILL = "#FFB055"                 # what it throws onto the porcelain

SHADOW = "#4E4437"                # contact shadow, warm-neutral per apple-12
SHADOW_DX, SHADOW_DY = 26.0, 12.0  # the cast runs right and slightly down,
                                   # away from the key


# ------------------------------------------------------------------- helpers --

def f(v):
    return f"{v:.2f}"


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexs(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(v)))) for v in c)


def mix(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return hexs(tuple(ra[i] + (rb[i] - ra[i]) * t for i in range(3)))


def lam_colour(lam):
    """One ramp, one light term. Every face in the icon comes through here."""
    lam = max(0.0, min(1.0, lam))
    for i in range(len(GRAPHITE) - 1):
        a, ca = GRAPHITE[i]
        b, cb = GRAPHITE[i + 1]
        if lam <= b:
            return mix(ca, cb, (lam - a) / (b - a))
    return GRAPHITE[-1][1]


def lum(h):
    """Gamma-encoded weighted luminance - the flatness/contrast metric's L."""
    r, g, b = (v / 255 for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag(h1, h2):
    """Contrast ratio on linearised luminance - what rubric #7 actually means."""
    def rel(h):
        out = []
        for v in (v / 255 for v in rgb(h)):
            out.append(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4)
        return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]
    a, b = sorted((rel(h1), rel(h2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def bez(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
            u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1])


def bez_d(p0, p1, p2, p3, t):
    u = 1.0 - t
    return (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
            3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]))


def poly(pts, close=True):
    d = "M" + " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    return d + "Z" if close else d


# ------------------------------------------------------------- the projection --

def zdepth(x):
    """Depth at a profile x. Constant, except along the horn, which is a cone."""
    if x <= HORN_X0:
        return DEPTH
    t = min(1.0, (x - HORN_X0) / (HORN_TIP[0] - HORN_X0))
    return DEPTH * (1.0 - (1.0 - HORN_Z_END) * (t ** 0.80))


def prj(x, y, z):
    return (x + z * VIEW_X + OFF_X, y + z * VIEW_Y + OFF_Y)


def near(p):
    return prj(p[0], p[1], 0.0)


def far(p):
    return prj(p[0], p[1], zdepth(p[0]))


# ---------------------------------------------------------------- the profile --

def profile():
    """The anvil's near flank as an ordered polyline, clockwise from the heel.

    Returns (points, marks). Flattened rather than emitted as curves, because
    everything downstream - the far cap, the visible side faces, the rim catches,
    the centroid, the bbox - is computed from these points, so the
    optical-centring claim is measured off the same geometry that ships.

    The marks matter: the first draft strung the rim catch along `pts[1:34]`,
    which swept past the horn's top ridge and carried on round its UNDERSIDE,
    drawing a bright hook beneath the tip where a light from above cannot reach.
    Addressing the ridge by name is what stops that.
    """
    pts = []
    marks = {}

    def line(p):
        pts.append(p)

    def curve(c1, c2, p, n=14):
        frm = pts[-1]
        for i in range(1, n + 1):
            pts.append(bez(frm, c1, c2, p, i / n))

    hx, hy = HORN_TIP
    line((HEEL_X, FACE_TOP))
    marks["face_a"] = 0
    line((STEP_X, FACE_TOP))                       # the hardened working face
    marks["face_b"] = len(pts) - 1
    line((STEP_X, FACE_TOP + STEP_DROP))           # down onto the step
    line((HORN_X0, FACE_TOP + STEP_DROP))          # the step (the "table")
    marks["horn_a"] = len(pts) - 1

    # horn, top edge: a shallow convex sweep out to the point. The top edge runs
    # on nearly level from the step and the UNDERSIDE rises to meet it, which
    # puts the tip in the upper third - that one relationship is most of the
    # difference between a horn and a blade.
    curve((HORN_X0 + 92, FACE_TOP + STEP_DROP - 6), (hx - 74, hy - 32),
          (hx, hy - HORN_TIP_R))
    marks["horn_b"] = len(pts) - 1
    curve((hx + 8, hy - HORN_TIP_R), (hx + 8, hy + HORN_TIP_R),
          (hx, hy + HORN_TIP_R), n=6)
    curve((hx - 88, hy + 34), (HORN_X0 + 104, FACE_BOT + 6), (HORN_X0, FACE_BOT))
    marks["horn_c"] = len(pts) - 1

    line((WAIST_R_TOP, FACE_BOT))                  # underside of the face slab
    curve((WAIST_R_TOP - 28, FACE_BOT + 58), (WAIST_R, WAIST_Y - 58),
          (WAIST_R, WAIST_Y))
    curve((WAIST_R + 24, WAIST_Y + 42), (BASE_R - 24, BASE_TOP - 28),
          (BASE_R, BASE_TOP))

    line((BASE_R, BASE_BOT - BASE_R_CORNER))
    curve((BASE_R, BASE_BOT), (BASE_R - BASE_R_CORNER, BASE_BOT),
          (BASE_R - BASE_R_CORNER, BASE_BOT), n=5)
    line((BASE_R - FOOT_W, BASE_BOT))
    marks["arch_a"] = len(pts) - 1
    curve((BASE_R - FOOT_W, BASE_BOT - ARCH_RISE * 1.34),
          (BASE_L + FOOT_W, BASE_BOT - ARCH_RISE * 1.34),
          (BASE_L + FOOT_W, BASE_BOT), n=16)
    marks["arch_b"] = len(pts) - 1
    line((BASE_L + BASE_R_CORNER, BASE_BOT))
    curve((BASE_L, BASE_BOT), (BASE_L, BASE_BOT), (BASE_L, BASE_BOT - BASE_R_CORNER), n=5)
    line((BASE_L, BASE_TOP))

    curve((BASE_L + 24, BASE_TOP - 28), (WAIST_L - 24, WAIST_Y + 42),
          (WAIST_L, WAIST_Y))
    curve((WAIST_L, WAIST_Y - 58), (WAIST_L_TOP + 28, FACE_BOT + 58),
          (WAIST_L_TOP, FACE_BOT))
    line((HEEL_X, FACE_BOT))                       # up the heel's square end
    return pts, marks


def signed_area(pts):
    a = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return a * 0.5


def centroid(pts):
    a = cx = cy = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    a *= 0.5
    return cx / (6 * a), cy / (6 * a), abs(a)


# ------------------------------------------------------- the visible surfaces --
#
# A face is visible when its outward normal points back toward the camera, which
# for this projection is n . (VIEW_X, VIEW_Y) > 0 for a side face and always true
# for the near cap. Grouping consecutive visible edges into bands whose normals
# agree to within BAND_TOL gives per-face gradient separation for free: a flat
# run becomes one band with one value, and a curved run becomes a handful of
# bands whose values step round the curve.

BAND_TOL = math.radians(10.0)
MIN_BAND_AREA = 300.0             # square px; below this a band is a hairline


def surfaces(pts, skip=()):
    """Return [(polygon, lambert)] for every visible extruded side face.

    `skip` names edge indices that are inside a recess. The arch between the feet
    is one: its right-hand wall is genuinely visible through the gap and
    genuinely edge-on, so it rendered as a 10px-wide dark parallelogram lying
    along the arch's own boundary - a scribe mark on the casting, from the one
    surface in the icon that sits in shadow rather than in light. A recess is
    filled with the shadow it makes; its walls are not lit bands.
    """
    n = len(pts)
    flip = 1.0 if signed_area(pts) > 0 else -1.0
    edges = []
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        dx, dy = q[0] - p[0], q[1] - p[1]
        m = math.hypot(dx, dy)
        if m < 1e-9:
            continue
        nx, ny = (dy / m) * flip, (-dx / m) * flip
        vis = nx * VIEW_X + ny * VIEW_Y > 0.0 and i not in skip
        edges.append((i, p, q, nx, ny, vis))

    # outward test: the normal must point away from the centroid
    cx, cy, _ = centroid(pts)
    probes = sum(1 for _, p, q, nx, ny, _ in edges
                 if (((p[0] + q[0]) / 2 - cx) * nx + ((p[1] + q[1]) / 2 - cy) * ny) > 0)
    if probes < len(edges) / 2:                     # normals point inward: flip
        edges = [(i, p, q, -nx, -ny,
                  (-nx) * VIEW_X + (-ny) * VIEW_Y > 0.0 and i not in skip)
                 for i, p, q, nx, ny, _ in edges]

    bands, cur = [], None
    for i, p, q, nx, ny, vis in edges:
        if not vis:
            cur = None
            continue
        ang = math.atan2(ny, nx)
        if cur is not None and abs(math.atan2(math.sin(ang - cur["ang"]),
                                              math.cos(ang - cur["ang"]))) < BAND_TOL:
            cur["pts"].append(q)
            cur["nsum"] = (cur["nsum"][0] + nx, cur["nsum"][1] + ny)
        else:
            cur = {"pts": [p, q], "ang": ang, "nsum": (nx, ny)}
            bands.append(cur)

    out = []
    for b in bands:
        nx, ny = b["nsum"]
        m = math.hypot(nx, ny) or 1.0
        nx, ny = nx / m, ny / m
        lam = AMBIENT + (1 - AMBIENT) * max(0.0, -(nx * LIGHT_DIR[0] + ny * LIGHT_DIR[1]))
        chain = [near(p) for p in b["pts"]] + [far(p) for p in reversed(b["pts"])]
        # A band whose projected area is a hairline is not a surface, it is a
        # scratch. The right foot's inner wall - genuinely visible through the
        # arch, genuinely edge-on - rendered as a 2px dark diagonal that read as
        # a scribe mark on the casting. Same lesson as a specular narrower than
        # two rendered pixels: drop it rather than defend it.
        if abs(signed_area(chain)) < MIN_BAND_AREA:
            continue
        out.append((chain, lam))
    return out


# --------------------------------------------------------------- face-plane uv --
# u runs along the profile axis, v along the depth axis, on the plane y = h.

def uv(u, v, h=None):
    return prj(u, FACE_TOP if h is None else h, v)


def ribbon(p0, p1, p2, p3, w0, w1, n=ARC_SAMPLES):
    """A cubic swept with a linearly varying half-width, as a closed polygon.

    SVG cannot express a tapered stroke and a stroke-width gradient does not
    exist, so the taper is real geometry. That is what makes the direction of
    travel legible.
    """
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_d(p0, p1, p2, p3, t)
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m, dx / m
        w = (w0 + (w1 - w0) * (t ** 0.72)) * 0.5
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return poly(left + right[::-1])


# -------------------------------------------------------------------- build --

def build():
    pts, marks = profile()
    npts = [near(p) for p in pts]
    fpts = [far(p) for p in pts]
    allp = npts + fpts
    bx0 = min(p[0] for p in allp); bx1 = max(p[0] for p in allp)
    by0 = min(p[1] for p in allp); by1 = max(p[1] for p in allp)
    cx, cy, area = centroid(npts)

    # The one shared key axis, in user space. Every face gradient hangs on this
    # segment, so a multi-part object cannot acquire a second light direction -
    # which is what objectBoundingBox units would silently do.
    kx, ky = LIGHT_DIR[0], LIGHT_DIR[1]
    km = math.hypot(kx, ky)
    kx, ky = kx / km, ky / km
    span = (bx1 - bx0 + by1 - by0) * 0.62
    mcx, mcy = (bx0 + bx1) / 2, (by0 + by1) / 2
    KAX = (mcx - kx * span / 2, mcy - ky * span / 2,
           mcx + kx * span / 2, mcy + ky * span / 2)

    faces = surfaces(pts, skip=set(range(marks["arch_a"], marks["arch_b"] + 1)))
    near_lam = AMBIENT + (1 - AMBIENT) * LIGHT_DIR[2]      # the flank faces us
    far_lam = AMBIENT * 0.55                               # the far flank

    grads, paths = [], []
    band_paths = []

    def face_grad(gid, lam, wrap=WRAP):
        grads.append(
            f'<linearGradient id="{gid}" x1="{f(KAX[0])}" y1="{f(KAX[1])}" '
            f'x2="{f(KAX[2])}" y2="{f(KAX[3])}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{lam_colour(lam + wrap)}"/>'
            f'<stop offset="1" stop-color="{lam_colour(lam - wrap)}"/></linearGradient>')

    # --- the solid, painted far cap -> visible side faces -> near cap
    face_grad("fFar", far_lam, WRAP * 0.5)
    paths.append(('mid', f'<path d="{poly(fpts)}" fill="url(#fFar)"/>'))
    for i, (chain, lam) in enumerate(faces):
        face_grad(f"fS{i}", lam)
        band_paths.append(poly(chain))
        paths.append(('mid', f'<path d="{poly(chain)}" fill="url(#fS{i})"/>'))
    face_grad("fNear", near_lam, WRAP * 1.25)
    near_path = poly(npts)
    paths.append(('mid', f'<path d="{near_path}" fill="url(#fNear)"/>'))

    # --- the face plane and the step, which are the two surfaces the work sits
    #     on. They share a normal, so they share a Lambert; what separates them
    #     is that the higher plane CASTS onto the lower one.
    top_lam = AMBIENT + (1 - AMBIENT) * LIGHT_DIR[1]
    face_quad = [uv(HEEL_X, 0), uv(STEP_X, 0), uv(STEP_X, DEPTH), uv(HEEL_X, DEPTH)]
    step_quad = [uv(STEP_X, 0, FACE_TOP + STEP_DROP), uv(HORN_X0, 0, FACE_TOP + STEP_DROP),
                 uv(HORN_X0, DEPTH, FACE_TOP + STEP_DROP), uv(STEP_X, DEPTH, FACE_TOP + STEP_DROP)]

    # the step's cast: the face's right edge, thrown right and into the scene by
    # the key, over a drop of STEP_DROP
    cdx = LIGHT_DIR[0] / LIGHT_DIR[1] * STEP_DROP
    cdz = LIGHT_DIR[2] / LIGHT_DIR[1] * STEP_DROP
    cast = [uv(STEP_X, 0, FACE_TOP + STEP_DROP),
            uv(STEP_X + cdx, cdz, FACE_TOP + STEP_DROP),
            uv(STEP_X + cdx, DEPTH + cdz, FACE_TOP + STEP_DROP),
            uv(STEP_X, DEPTH, FACE_TOP + STEP_DROP)]

    # --- the holes, cut into the face plane
    hardie = [uv(HARDIE_U, HARDIE_V), uv(HARDIE_U + HARDIE_S, HARDIE_V),
              uv(HARDIE_U + HARDIE_S, HARDIE_V + HARDIE_S), uv(HARDIE_U, HARDIE_V + HARDIE_S)]
    hardie_wall = [uv(HARDIE_U + HARDIE_S, HARDIE_V), uv(HARDIE_U + HARDIE_S, HARDIE_V + HARDIE_S),
                   uv(HARDIE_U + HARDIE_S - 9, HARDIE_V + HARDIE_S - 3), uv(HARDIE_U + HARDIE_S - 9, HARDIE_V + 3)]
    prit = [uv(PRITCHEL_U + PRITCHEL_R * math.cos(a), PRITCHEL_V + PRITCHEL_R * math.sin(a))
            for a in [i * math.tau / 20 for i in range(20)]]

    # --- the billet, a small prism standing on the face plane, projected with
    #     the same view constants so it cannot drift off the plane it rests on
    bt = FACE_TOP - BILLET_H
    b_top = [uv(BILLET_U0, BILLET_V0, bt), uv(BILLET_U1, BILLET_V0, bt),
             uv(BILLET_U1, BILLET_V1, bt), uv(BILLET_U0, BILLET_V1, bt)]
    b_near = [uv(BILLET_U0, BILLET_V0, bt), uv(BILLET_U1, BILLET_V0, bt),
              uv(BILLET_U1, BILLET_V0), uv(BILLET_U0, BILLET_V0)]
    b_left = [uv(BILLET_U0, BILLET_V0, bt), uv(BILLET_U0, BILLET_V1, bt),
              uv(BILLET_U0, BILLET_V1), uv(BILLET_U0, BILLET_V0)]
    horn_region = ([near(pts[i]) for i in range(marks["horn_a"], marks["horn_c"] + 1)]
                   + [near((HORN_X0, FACE_TOP + STEP_DROP))])

    b_contact = [uv(BILLET_U0, BILLET_V0), uv(BILLET_U1, BILLET_V0),
                 uv(BILLET_U1, BILLET_V1), uv(BILLET_U0, BILLET_V1)]
    # the billet's whole visible outline, as one hexagon: it stands proud of the
    # face plane's far lip, so the tool's rim catch has to be kept off it
    b_hull = [uv(BILLET_U0, BILLET_V0), uv(BILLET_U1, BILLET_V0),
              uv(BILLET_U1, BILLET_V0, bt), uv(BILLET_U1, BILLET_V1, bt),
              uv(BILLET_U0, BILLET_V1, bt), uv(BILLET_U0, BILLET_V1)]
    # the seam where hot metal meets cold tool: the billet blocks the daylight, so
    # a small warm-dark shadow tucks under its near edge, thrown along the key
    seam = [uv(BILLET_U0, BILLET_V0), uv(BILLET_U1, BILLET_V0),
            uv(BILLET_U1 + 16, BILLET_V0 - 9), uv(BILLET_U0 + 8, BILLET_V0 - 9)]
    bcx = (b_top[0][0] + b_top[2][0]) / 2
    bcy = (b_top[0][1] + b_top[2][1]) / 2

    # --- the return arc. p1 is the outward flick: the ribbon leaves the tip
    #     heading away from the tool before it turns, which is what makes the
    #     trajectory read as out-and-back rather than as an arch over the anvil.
    tip = near(HORN_TIP)
    arc = ribbon((tip[0] + 12, tip[1] - 10),
                 (tip[0] + 46, tip[1] - 132),
                 (tip[0] - 196, tip[1] - 226),
                 (bcx + 26, bcy - 22),
                 ARC_W_FAR, ARC_W_NEAR)

    # --- the contact shadow: a tight cast hugging the feet, offset away from the
    #     key, plus one broad ambient pool. Measured target is a darkest contact
    #     pixel near L 0.33 against a local ground of L 0.93.
    foot_l = near((BASE_L, BASE_BOT))
    foot_r = near((BASE_R, BASE_BOT))
    fw = foot_r[0] - foot_l[0]

    # The arch between the feet is a genuine gap under the tool, so the tile shows
    # through it - and a brightly lit hole punched in the base is exactly what it
    # looked like. What belongs there is the shaded recess the anvil's own mass
    # makes, so the arch is filled with shadow before the solid is painted.
    arch_a = (BASE_R - FOOT_W, BASE_BOT)
    arch_b = (BASE_L + FOOT_W, BASE_BOT)
    recess = [near(bez(arch_a, (BASE_R - FOOT_W, BASE_BOT - ARCH_RISE * 1.34),
                       (BASE_L + FOOT_W, BASE_BOT - ARCH_RISE * 1.34), arch_b, i / 16))
              for i in range(17)]
    recess = recess + [(recess[-1][0], recess[-1][1] + 16), (recess[0][0], recess[0][1] + 16)]

    defs = [
        f'<linearGradient id="porc" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{PORC_HI}"/>'
        f'<stop offset="0.52" stop-color="{PORC_MID}"/>'
        f'<stop offset="1" stop-color="{PORC_LO}"/></linearGradient>',
        f'<radialGradient id="cushion" cx="0.34" cy="0.20" r="0.92">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>'
        f'<stop offset="0.58" stop-color="#FFFFFF" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="vig" cx="0.5" cy="0.46" r="0.74">'
        f'<stop offset="0.55" stop-color="{VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/></radialGradient>',
        f'<linearGradient id="rimtop" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{PORC_RIM}" stop-opacity="0.95"/>'
        f'<stop offset="0.42" stop-color="{PORC_RIM}" stop-opacity="0.30"/>'
        f'<stop offset="1" stop-color="{PORC_RIM}" stop-opacity="0.55"/></linearGradient>',
        # the emitter's spill onto the porcelain: warm, never dark
        f'<radialGradient id="spill" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{SPILL}" stop-opacity="0.17"/>'
        f'<stop offset="0.44" stop-color="{SPILL}" stop-opacity="0.06"/>'
        f'<stop offset="1" stop-color="{SPILL}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="pool" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{SHADOW}" stop-opacity="0.30"/>'
        f'<stop offset="0.52" stop-color="{SHADOW}" stop-opacity="0.13"/>'
        f'<stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/></radialGradient>',
        # the two top planes, and the shadow the higher one throws on the lower
        f'<linearGradient id="plane" x1="{f(KAX[0])}" y1="{f(KAX[1])}" x2="{f(KAX[2])}" y2="{f(KAX[3])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{lam_colour(top_lam + 0.10)}"/>'
        f'<stop offset="1" stop-color="{lam_colour(top_lam - 0.14)}"/></linearGradient>',
        f'<linearGradient id="stepg" x1="{f(KAX[0])}" y1="{f(KAX[1])}" x2="{f(KAX[2])}" y2="{f(KAX[3])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{lam_colour(top_lam - 0.04)}"/>'
        f'<stop offset="1" stop-color="{lam_colour(top_lam - 0.26)}"/></linearGradient>',
        f'<linearGradient id="underface" x1="0" y1="{f(FACE_BOT + OFF_Y)}" x2="0" y2="{f(FACE_BOT + OFF_Y + 168)}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#000000" stop-opacity="0.30"/>'
        f'<stop offset="0.34" stop-color="#000000" stop-opacity="0.15"/>'
        f'<stop offset="1" stop-color="#000000" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="satin" x1="{f(KAX[0])}" y1="{f(KAX[1])}" x2="{f(KAX[2])}" y2="{f(KAX[3])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0.10" stop-color="{SATIN}" stop-opacity="0"/>'
        f'<stop offset="0.34" stop-color="{SATIN}" stop-opacity="0.30"/>'
        f'<stop offset="0.66" stop-color="{SATIN}" stop-opacity="0.04"/>'
        f'<stop offset="1" stop-color="{SATIN}" stop-opacity="0"/></linearGradient>',
        # The porcelain throws light back up into everything standing on it. This
        # is a real Tahoe move and it lands exactly where the near flank is
        # flattest, so it does material work and figure-ground work at once -
        # measured on apple-10, whose gunmetal strands all carry a bottom lift.
        f'<linearGradient id="upbounce" x1="0" y1="{f(by1)}" x2="0" y2="{f(by1 - 250)}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{PORC_LO}" stop-opacity="0.36"/>'
        f'<stop offset="0.42" stop-color="{PORC_LO}" stop-opacity="0.11"/>'
        f'<stop offset="1" stop-color="{PORC_LO}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="rimg" x1="{f(KAX[0])}" y1="{f(KAX[1])}" x2="{f(KAX[2])}" y2="{f(KAX[3])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{RIM_CATCH}" stop-opacity="0.95"/>'
        f'<stop offset="0.46" stop-color="{RIM_CATCH}" stop-opacity="0.34"/>'
        f'<stop offset="1" stop-color="{RIM_CATCH}" stop-opacity="0.06"/></linearGradient>',
        # The billet is a light SOURCE, not a filled shape. Vibrancy here is
        # emission rather than saturation: a small bright core under the surface,
        # a bloom above it, and visible bounce onto everything it faces. Sides
        # deepen as they descend, because that is where the heat conducts away
        # into the cold tool - and they hold saturation as they deepen, or the
        # metal reads as painted plastic.
        f'<radialGradient id="btop" cx="0.58" cy="0.44" r="0.66">'
        f'<stop offset="0" stop-color="{HOT_CORE}"/>'
        f'<stop offset="0.20" stop-color="{HOT_HI}"/>'
        f'<stop offset="0.58" stop-color="{HOT_MID}"/>'
        f'<stop offset="1" stop-color="{HOT_EDGE}"/></radialGradient>',
        f'<linearGradient id="bside" x1="0" y1="{f(b_near[0][1])}" x2="0" y2="{f(b_near[2][1])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{HOT_EDGE}"/>'
        f'<stop offset="0.44" stop-color="{HOT_LO}"/>'
        f'<stop offset="1" stop-color="#8E2404"/></linearGradient>',
        f'<linearGradient id="bend" x1="0" y1="{f(b_left[0][1])}" x2="0" y2="{f(b_left[2][1])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{HOT_LO}"/>'
        f'<stop offset="1" stop-color="#7C1F03"/></linearGradient>',
        # A bounce is a kiss on the surfaces that face the emitter. At 188x104 and
        # 0.46 this was a wash: it browned the whole working face while every
        # measurement of the ramp said the colours were right. Tight, brighter,
        # and in the spill hue rather than the deeper bounce hue, because warm
        # light on cool graphite goes muddy long before it goes warm.
        f'<radialGradient id="bounce" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{SPILL}" stop-opacity="0.30"/>'
        f'<stop offset="0.26" stop-color="{SPILL}" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="{SPILL}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{HOT_HI}" stop-opacity="0.80"/>'
        f'<stop offset="0.40" stop-color="{HOT_EDGE}" stop-opacity="0.28"/>'
        f'<stop offset="1" stop-color="{HOT_EDGE}" stop-opacity="0"/></radialGradient>',
        f'<linearGradient id="arcg" x1="{f(tip[0])}" y1="0" x2="{f(bcx)}" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{HOT_DEEP}" stop-opacity="0"/>'
        f'<stop offset="0.26" stop-color="{HOT_LO}" stop-opacity="0.62"/>'
        f'<stop offset="0.62" stop-color="{HOT_EDGE}" stop-opacity="0.95"/>'
        f'<stop offset="1" stop-color="{HOT_HI}" stop-opacity="1"/></linearGradient>',
        f'<linearGradient id="holewall" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{lam_colour(0.30)}"/>'
        f'<stop offset="1" stop-color="{CAVITY}"/></linearGradient>',
        '<filter id="bS" x="-45%" y="-45%" width="190%" height="190%">'
        '<feGaussianBlur stdDeviation="5"/></filter>',
        '<filter id="bM" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="15"/></filter>',
        '<filter id="bL" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="42"/></filter>',
        f'<clipPath id="tileClip"><path d="{SQUIRCLE}"/></clipPath>',
        f'<clipPath id="nearClip"><path d="{near_path}"/></clipPath>',
        # Every visible surface of the solid, as one union. clip-rule is stated
        # rather than inherited: nonzero unions overlapping subpaths, which is
        # what this clip wants, and the same default silently turns an intended
        # annulus into a disc - so the intent goes in the file.
        f'<clipPath id="solidClip" clip-rule="nonzero">'
        + "".join(f'<path d="{d}"/>' for d in [near_path, poly(fpts)] + band_paths)
        + '</clipPath>',
        f'<clipPath id="planeClip"><path d="{poly(face_quad)}"/></clipPath>',
        # the working face minus its two apertures, so the billet's light cannot
        # paint a warm blob inside a hole - which is what made the pritchel read
        # as a brown smudge rather than as a hole
        f'<clipPath id="planeSolid" clip-rule="evenodd">'
        f'<path d="{poly(face_quad)}"/><path d="{poly(hardie)}"/>'
        f'<path d="{poly(prit)}"/></clipPath>',
        f'<clipPath id="stepClip"><path d="{poly(step_quad)}"/></clipPath>',
        f'<clipPath id="hornClip"><path d="{poly(horn_region)}"/></clipPath>',
        # The horn is a CONE, so its flank has to wrap. Both other engines drew it
        # as a separately-valued form - the Arrow take as a pale cone against a
        # dark body, the raster as a rounded nose - where this master had it
        # sharing one flat gradient with the face slab. Two independent engines
        # converging on a form the master lacked is the same evidence that bought
        # the arched foot last time, and it costs one clipped overlay.
        f'<linearGradient id="hornwrap" x1="0" y1="{f(near((0, FACE_TOP + STEP_DROP))[1])}" '
        f'x2="0" y2="{f(near((0, FACE_BOT))[1])}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{lam_colour(near_lam + 0.20)}" stop-opacity="0.85"/>'
        f'<stop offset="0.38" stop-color="{lam_colour(near_lam)}" stop-opacity="0.20"/>'
        f'<stop offset="1" stop-color="{lam_colour(max(0.0, near_lam - 0.22))}" stop-opacity="0.80"/>'
        f'</linearGradient>',
        # everything except the billet. evenodd, and stated: the tile rect minus
        # the billet's hull is a subtraction, which is the one case where the
        # default nonzero would give the whole tile and paint straight over it.
        f'<clipPath id="notBillet" clip-rule="evenodd">'
        f'<path d="M0,0 H{W} V{W} H0 Z"/><path d="{poly(b_hull)}"/></clipPath>',
        f'<linearGradient id="recess" x1="0" y1="{f(near((0, BASE_BOT - ARCH_RISE))[1])}" '
        f'x2="0" y2="{f(near((0, BASE_BOT))[1] + 10)}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{SHADOW}" stop-opacity="0.86"/>'
        f'<stop offset="0.62" stop-color="{SHADOW}" stop-opacity="0.52"/>'
        f'<stop offset="1" stop-color="{SHADOW}" stop-opacity="0.30"/></linearGradient>',
    ] + grads

    bg = f'''
  <rect width="{W}" height="{W}" fill="url(#porc)"/>
  <rect width="{W}" height="{W}" fill="url(#cushion)"/>
  <ellipse cx="{f(bcx + 40)}" cy="{f(bcy + 30)}" rx="430" ry="360" fill="url(#spill)"/>
  <rect width="{W}" height="{W}" fill="url(#vig)"/>
  <path d="{SQUIRCLE}" fill="none" stroke="url(#rimtop)" stroke-width="3.2"/>
  <ellipse cx="{f(foot_l[0] + fw / 2 + 34)}" cy="{f(foot_l[1] + 16)}"
           rx="{f(fw * 0.86)}" ry="52" fill="url(#pool)" filter="url(#bL)"/>
  <path d="{poly(recess)}" fill="url(#recess)" filter="url(#bS)"/>
  <path d="{poly([(foot_l[0] + 6, foot_l[1] - 6), (foot_r[0] - 6, foot_r[1] - 6),
                  (foot_r[0] + SHADOW_DX, foot_r[1] + SHADOW_DY),
                  (foot_l[0] + SHADOW_DX * 0.5, foot_l[1] + SHADOW_DY)])}"
        fill="{SHADOW}" fill-opacity="0.55" filter="url(#bM)"/>
'''

    mid_solid = "\n".join(p for layer, p in paths if layer == 'mid')
    # the satin sheen is an explicit band across the struck flank, not a stop on
    # the shared key gradient: on that axis the peak fell in the upper LEFT of
    # the bbox, which is the heel's end face and not the surface a hammer polishes
    sheen = [near((HEEL_X + 14, FACE_TOP + 26)), near((STEP_X + 120, FACE_TOP + 14)),
             near((STEP_X + 120, FACE_TOP + 60)), near((HEEL_X + 14, FACE_TOP + 78))]
    mid = f'''
{mid_solid}
  <g clip-path="url(#solidClip)">
    <rect x="0" y="{f(FACE_BOT + OFF_Y)}" width="{W}" height="210" fill="url(#underface)"/>
    <rect x="0" y="{f(by1 - 250)}" width="{W}" height="260" fill="url(#upbounce)"/>
  </g>
  <g clip-path="url(#nearClip)">
    <path d="{poly(sheen)}" fill="{SATIN}" fill-opacity="0.32" filter="url(#bM)"/>
  </g>
  <g clip-path="url(#hornClip)">
    <path d="{poly(horn_region)}" fill="url(#hornwrap)"/>
  </g>
  <path d="{poly(step_quad)}" fill="url(#stepg)"/>
  <g clip-path="url(#stepClip)">
    <path d="{poly(cast)}" fill="#000000" fill-opacity="0.42"/>
  </g>
  <path d="{poly(face_quad)}" fill="url(#plane)"/>
  <g clip-path="url(#planeClip)">
    <path d="{poly(hardie)}" fill="{CAVITY}"/>
    <path d="{poly(hardie_wall)}" fill="url(#holewall)"/>
    <path d="{poly(prit)}" fill="{CAVITY}"/>
    <ellipse cx="{f(uv(PRITCHEL_U + 4, PRITCHEL_V + 4)[0])}" cy="{f(uv(PRITCHEL_U + 4, PRITCHEL_V + 4)[1])}"
             rx="{f(PRITCHEL_R * 0.60)}" ry="{f(PRITCHEL_R * 0.44)}" fill="url(#holewall)"/>
  </g>
'''

    fg = f'''
  <g clip-path="url(#planeSolid)">
    <ellipse cx="{f(bcx)}" cy="{f((b_contact[0][1] + b_contact[2][1]) / 2)}"
             rx="122" ry="66" fill="url(#bounce)"/>
    <ellipse cx="{f(bcx)}" cy="{f((b_contact[0][1] + b_contact[2][1]) / 2)}"
             rx="98" ry="54" fill="url(#bloom)" opacity="0.55" filter="url(#bM)"/>
    <path d="{poly(seam)}" fill="{HOT_DEEP}" fill-opacity="0.42" filter="url(#bS)"/>
  </g>
  <g clip-path="url(#nearClip)">
    <ellipse cx="{f(bcx)}" cy="{f(near((BILLET_U0, FACE_TOP))[1] + 8)}"
             rx="88" ry="34" fill="url(#bounce)" opacity="0.60"/>
  </g>
  <path d="{arc}" fill="url(#arcg)" filter="url(#bS)" opacity="0.45"/>
  <path d="{arc}" fill="url(#arcg)"/>
  <path d="{poly(b_left)}" fill="url(#bend)"/>
  <path d="{poly(b_near)}" fill="url(#bside)"/>
  <path d="{poly(b_top)}" fill="url(#btop)"/>
'''

    # Rim catches, addressed by name. Three edges and no others: the face plane's
    # FAR edge (the lit lip that separates the tool from the ground behind it),
    # the horn's far top ridge fading out toward the cone's tip, and the near lip
    # where the top plane folds into the flank - a convex edge between two lit
    # faces always carries a fillet, and it is what stops the two planes reading
    # as one printed shape.
    #
    # Clipped off the billet, which stands proud of the far lip. Unclipped, that
    # stroke ran straight across the hot metal as a pale scratch - the layer plan
    # puts highlights above the foreground, so an occluding object in #fg needs
    # the highlight to know about it.
    ridge_far = [far(pts[i]) for i in range(marks["horn_a"], marks["horn_b"] + 1)]
    hl = f'''
  <g clip-path="url(#notBillet)">
    <path d="{poly([far((HEEL_X, FACE_TOP)), far((STEP_X, FACE_TOP))], close=False)}"
          fill="none" stroke="url(#rimg)" stroke-width="4.6" stroke-linecap="round"/>
    <path d="{poly(ridge_far[:-3], close=False)}"
          fill="none" stroke="url(#rimg)" stroke-width="3.2" stroke-linecap="butt"/>
  </g>
  <path d="{poly([near((HEEL_X, FACE_TOP)), near((STEP_X, FACE_TOP))], close=False)}"
        fill="none" stroke="{RIM_CATCH}" stroke-opacity="0.34" stroke-width="3"
        stroke-linecap="round" filter="url(#bS)"/>
  <path d="{poly([near(pts[i]) for i in range(marks["horn_a"], marks["horn_b"] + 1)], close=False)}"
        fill="none" stroke="{RIM_CATCH}" stroke-opacity="0.24" stroke-width="2.6"
        stroke-linecap="round" filter="url(#bS)"/>
  <ellipse cx="{f(bcx)}" cy="{f(bcy + 6)}" rx="112" ry="76" fill="url(#bloom)" filter="url(#bM)"/>
  <path d="{poly([b_top[0], b_top[1]], close=False)}" fill="none" stroke="{HOT_CORE}"
        stroke-opacity="0.55" stroke-width="2.4" stroke-linecap="round" filter="url(#bS)"/>
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}">
<defs>
{chr(10).join(defs)}
</defs>
<g clip-path="url(#tileClip)">
<g id="bg">{bg}</g>
<g id="mid">{mid}</g>
<g id="fg">{fg}</g>
<g id="highlight">{hl}</g>
</g>
</svg>
'''
    return svg, dict(bbox=(bx0, bx1, by0, by1), cx=cx, cy=cy, area=area,
                     faces=len(faces), top_lam=top_lam, near_lam=near_lam)


if __name__ == "__main__":
    svg, info = build()
    out = ASSETS / "icon.svg"
    out.write_text(svg)
    bx0, bx1, by0, by1 = info["bbox"]
    print(f"wrote {out} ({len(svg)} bytes, {svg.count('<path')} paths)")
    print(f"  focal bbox    x {bx0:.0f}..{bx1:.0f}   y {by0:.0f}..{by1:.0f}")
    print(f"  focal size    {(bx1-bx0)/W*100:.1f}% of tile width, {(by1-by0)/W*100:.1f}% of height")
    print(f"  bbox centre   ({(bx0+bx1)/2:.0f}, {(by0+by1)/2:.0f})   near-cap centroid ({info['cx']:.0f}, {info['cy']:.0f})")
    print(f"  margins       L {bx0:.0f}  R {W-bx1:.0f}  T {by0:.0f}  B {W-by1:.0f}")
    print(f"  visible faces {info['faces']} bands   top lam {info['top_lam']:.2f} -> {lam_colour(info['top_lam'])}"
          f"   near lam {info['near_lam']:.2f} -> {lam_colour(info['near_lam'])}")
    print(f"  figure-ground top plane vs porcelain   {wcag(lam_colour(info['top_lam']), PORC_MID):.2f}:1")
    print(f"                near flank vs porcelain  {wcag(lam_colour(info['near_lam']), PORC_MID):.2f}:1")
    print(f"                arc body vs porcelain    {wcag(HOT_LO, PORC_MID):.2f}:1")
    print(f"                billet vs top plane      {wcag(HOT_MID, lam_colour(info['top_lam'])):.2f}:1")
