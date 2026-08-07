#!/usr/bin/env python3
"""
Engine A - hand-authored layered SVG master for the improve-skill icon.

Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object,
crossed with device bank #16 (the icon performs the verb) and #5 (dual-function primitive).

MATERIAL REBUILD (round 4). The first master read flat: a slab with a line under it.
This one is built as a real extruded solid - a top face lifted off the ground and a
front face dropping back down to it - so the block has the mass the raster take had.
The ground contact of that front face IS the local y=0 line, which IS the before/after
boundary, which IS the vermilion hone. One line still does three jobs; it now also
does a fourth, being where the object meets the ground.

PITCH (round 5). Round 4 lifted the top face by ONE constant rise, so the block sat
dead level - a bar lying on the boards, not an iron taking a cut. The lift is now
LINEAR in local x: shallow where the iron is buried in the timber, deep at the
trailing end, so the front face is a wedge and the block rides nose-down the way C2's
does. Because that stays affine, the lifted top face is still ONE matrix (MATRIX_TOP,
a shear of the blade frame) and every texture and gradient rides it unchanged.

Polarity is the fix the raster never made: the trued side must measure BRIGHTER than
the un-planed side. Verified by measure.py on every render, not eyeballed.

The whole tile is the workpiece. A worn plane iron lies on a rising diagonal mid-pass.
Everything on the finished side of that diagonal is brighter and truer than the side
still to come, and the one vermilion hone line IS the boundary between them.

Geometry is authored in the blade's own local frame (local x runs along the cutting
edge, local y runs away from the cut into the un-planed region) and mapped onto the
1024 canvas by a single matrix, so the grain, the split and the blade cannot drift
out of register with each other. The extrusion is a screen-vertical sweep of that
frame - sheared along the blade's length for the pitch - so the solid cannot drift
out of register either.

Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
"""

import math
import os
import pathlib

# the shaving curl. SHAVING=0 builds the round-4 two-object tile without it.
SHAVING = os.environ.get("SHAVING", "1") == "1"

W = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- frame
ANGLE = math.radians(33.0)                    # rising diagonal
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)    # along the cutting edge, up-and-right
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)   # away from the cut, into the rough side

BLADE_LEN = 640.0
# ROUND 8 (coarse structure). The top face was 152 deep, which made the iron a slim
# bar: 4.2:1 in plan against C2's 3.1:1. Measured directly on C2, in C2's own hone
# frame, as (silhouette back edge) - (top/front shoulder) on three cross-sections over
# the leading two thirds - the span where the shoulder is a readable trough rather than
# the rolled highlight it becomes at the trailing end: 204 / 190 / 218, mean 204. No
# rise arithmetic enters that subtraction, which is why it is the number to trust; the
# back edge alone reads 248-260 but that figure carries the front face's lift with it.
BLADE_THICK = 204.0                           # depth of the top face
EDGE_MID = (543.0, 604.0)                     # midpoint of the cutting edge, on the canvas
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2         # local origin: cutting edge, leading end

MATRIX = f"matrix({UX:.5f},{UY:.5f},{NX:.5f},{NY:.5f},{AX:.3f},{AY:.3f})"

# ---------------------------------------------------------------- pitch
# ROUND 5. The block used to be lifted by ONE constant rise, so its top face was a
# parallel copy of its footprint and the front face was a band of even height: a bar
# lying flat on the boards. Nothing about it said "mid-cut". C2's block is PITCHED -
# it rides nose-down on the leading end, so the front face is a WEDGE that pinches
# almost shut where the iron is buried in the timber and opens out at the trailing
# end. Measured off C2: its ground/hone line runs 38.9 deg, its top-face shoulder
# runs 41.9 deg (+3.0 deg), and the front face goes 55px deep at the near end to
# 90px at the far end.
#
# The lift is therefore LINEAR IN LOCAL x rather than constant. That keeps the whole
# thing affine, so the lifted top face is still ONE matrix - a SHEAR of the blade's
# own frame - and the texture, the gradients and the grind marks ride it without a
# second transform. The footprint, the cutting edge and the before/after boundary all
# sit at local y = 0 and are untouched by the shear, so the signature cannot drift.
RISE_NEAR = 48.0                              # lift at the leading end (local x = 0)
RISE_FAR = 132.0                              # lift at the trailing end (local x = LEN)
RISE = (RISE_NEAR + RISE_FAR) / 2             # the mean, for anything that needs one
K_RISE = (RISE_FAR - RISE_NEAR) / BLADE_LEN   # shear rate: extra lift per unit local x

# The top face's frame: the blade frame with a screen-vertical shear applied. A point
# at local (lx, ly) lands rise(lx) above where the footprint puts it.
MATRIX_TOP = (f"matrix({UX:.5f},{UY - K_RISE:.5f},{NX:.5f},{NY:.5f},"
              f"{AX:.3f},{AY - RISE_NEAR:.3f})")

# the deepest the front face ever gets, expressed in the local frame
RISE_LY = RISE_FAR * math.cos(ANGLE)


def rise_at(lx):
    return RISE_NEAR + K_RISE * lx


def to_canvas(lx, ly):
    return (AX + UX * lx + NX * ly, AY + UY * lx + NY * ly)


def to_top(lx, ly):
    """The same point, on the lifted top face."""
    x, y = to_canvas(lx, ly)
    return (x, y - rise_at(lx))


def to_local(px, py):
    dx, dy = px - AX, py - AY
    return (UX * dx + UY * dy, NX * dx + NY * dy)


def inv_matrix(a, b, c, d, e, f):
    """The SVG matrix that undoes matrix(a,b,c,d,e,f). Used to run a filter inside a
    frame without moving what the filter is applied to: wrap the artwork in the frame,
    attach the filter there, and put the inverse on the contents. The geometry and its
    gradients come out exactly where they were; the filter sees the local frame."""
    det = a * d - c * b
    return (f"matrix({d / det:.6f},{-b / det:.6f},{-c / det:.6f},{a / det:.6f},"
            f"{(c * f - d * e) / det:.3f},{(b * e - a * f) / det:.3f})")


MATRIX_INV = inv_matrix(UX, UY, NX, NY, AX, AY)
MATRIX_TOP_INV = inv_matrix(UX, UY - K_RISE, NX, NY, AX, AY - RISE_NEAR)


def frame_azimuth(a, b, c, d):
    """The scene's one key light, re-expressed inside a frame, as an feDistantLight
    azimuth. A relief filter running in a local frame must be lit from the SAME source
    as everything else in the icon; hard-coding 225 deg would light the ground's fibre
    from a second, imaginary direction."""
    lx, ly = -0.70711, -0.70711            # unit vector pointing at the key, canvas frame
    det = a * d - c * b
    fx = (d * lx - c * ly) / det
    fy = (-b * lx + a * ly) / det
    return math.degrees(math.atan2(fy, fx)) % 360.0


# The boundary is local y = 0, extended to the canvas edges.
def boundary_at_x(x):
    return AY - NX * (x - AX) / NY


B_LEFT = boundary_at_x(0)
B_RIGHT = boundary_at_x(W)

# how far the canvas reaches in the local frame, so texture can cover it exactly
_c = [to_local(x, y) for x in (0, W) for y in (0, W)]
LX_MIN, LX_MAX = min(p[0] for p in _c), max(p[0] for p in _c)
LY_MIN, LY_MAX = min(p[1] for p in _c), max(p[1] for p in _c)

# deterministic jitter, so a rebuild is byte-identical
_seed = 20260807


def rnd():
    global _seed
    _seed = (_seed * 1103515245 + 12345) % (1 << 31)
    return _seed / (1 << 31)


# ---------------------------------------------------------------- outline
def _quad(p0, p1, p2, n=8):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


def _cubic(p0, p1, p2, p3, n=20):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


def blade_outline():
    """Rounded plane iron in local space, flattened to a polyline so the extrusion
    can be derived from it exactly. Cutting edge (y=0) dead straight and honed;
    back edge worn, with a shallow sag and unequal corner radii."""
    L, T = BLADE_LEN, BLADE_THICK
    r_cl, r_ct = 12.0, 9.0        # corners on the honed edge: crisp, it is sharpened
    r_bl, r_bt = 46.0, 36.0       # corners on the worn back
    pts = [(r_cl, 0.0), (L - r_ct, 0.0)]
    pts += _quad((L - r_ct, 0), (L, 0), (L, r_ct))
    pts.append((L, T - r_bt))
    pts += _quad((L, T - r_bt), (L, T), (L - r_bt, T))
    pts += _cubic((L - r_bt, T), (L * 0.66, T - 8.5), (L * 0.34, T - 8.5), (r_bl, T))
    pts += _quad((r_bl, T), (0, T), (0, T - r_bl))
    pts.append((0.0, r_cl))
    pts += _quad((0, r_cl), (0, 0), (r_cl, 0))
    return pts


def poly(pts):
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def open_poly(pts):
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + ""


OUTLINE_L = blade_outline()
# the top face, lifted off the ground by the pitched rise
TOP = [to_top(x, y) for x, y in OUTLINE_L]
# the footprint: where the solid actually meets the ground
FOOT = [to_canvas(x, y) for x, y in OUTLINE_L]

N = len(TOP)
i_min = min(range(N), key=lambda i: TOP[i][0])
i_max = max(range(N), key=lambda i: TOP[i][0])


def _walk(a, b):
    out, i = [a], a
    while i != b:
        i = (i + 1) % N
        out.append(i)
    return out


_fwd = _walk(i_min, i_max)          # i_min -> i_max one way round
_bwd = _walk(i_max, i_min)          # i_max -> i_min the other way
if (sum(TOP[i][1] for i in _fwd) / len(_fwd)
        > sum(TOP[i][1] for i in _bwd) / len(_bwd)):
    IDX_LOWER, IDX_UPPER = _fwd, _bwd                # lower runs i_min -> i_max
else:
    IDX_LOWER, IDX_UPPER = _bwd[::-1], _fwd[::-1]

CHAIN_LOWER = [TOP[i] for i in IDX_LOWER]
CHAIN_UPPER = [TOP[i] for i in IDX_UPPER]
FOOT_LOWER = [FOOT[i] for i in IDX_LOWER]

# the front face: the lower silhouette chain dropped to its own footprint. Because the
# drop is rise(lx) rather than one constant, this face is a wedge - shallow where the
# iron is buried, deep at the trailing end.
FRONT_FACE = CHAIN_LOWER + FOOT_LOWER[::-1]
# the whole solid, for the cast shadow
SILHOUETTE = CHAIN_UPPER[::-1] + FOOT_LOWER[::-1]
# the ground contact line, which is also the before/after boundary
CONTACT = FOOT_LOWER


# ---------------------------------------------------------------- ground texture
def grain():
    """One family of grain lines running along the travel direction. The SAME line
    crosses the boundary: torn and broken on the un-planed side, continuous and fine
    on the trued side. That continuity is what makes the split read as one surface in
    two states rather than as two different materials. Drawn right across the tile and
    clipped per side, so the block sits ON the grain rather than beside it."""
    rough, true = [], []
    x = LX_MIN - 40
    while x < LX_MAX + 40:
        # --- trued side (local y < 0): long, even, fine. A sheen, not a stripe - but
        #     present, because a trued plane still carries the mark of the pass.
        if rnd() < 0.72:
            op = 0.030 + rnd() * 0.042
            true.append(
                f'<path d="M {x:.1f} -8 L {x:.1f} {LY_MIN - 20:.0f}" stroke="#8A7C64" '
                f'stroke-opacity="{op:.3f}" stroke-width="{1.1 + rnd() * 0.8:.2f}"/>'
            )
        if rnd() < 0.34:
            op = 0.020 + rnd() * 0.026
            true.append(
                f'<path d="M {x + 6:.1f} -8 L {x + 6:.1f} {LY_MIN - 20:.0f}" stroke="#FFFFFF" '
                f'stroke-opacity="{op:.3f}" stroke-width="{1.4 + rnd() * 1.2:.2f}"/>'
            )
        # --- un-planed side (local y > 0): short broken tooth marks. Some lines tear
        #     badly, some hardly at all, which is what stops it reading as ruled rain.
        tear = 0.34 + rnd() * 0.92
        y = 8.0
        while y < LY_MAX + 20:
            seg = 6 + rnd() * 23 * tear
            gap = 7 + rnd() * 20
            op = (0.07 + rnd() * 0.13) * tear
            wid = 1.2 + rnd() * 2.1
            rough.append(
                f'<path d="M {x + (rnd() - 0.5) * 4:.1f} {y:.1f} '
                f'L {x + (rnd() - 0.5) * 4:.1f} {y + seg:.1f}" stroke="#6A5F4C" '
                f'stroke-opacity="{op:.3f}" stroke-width="{wid:.2f}"/>'
            )
            y += seg + gap
        x += 14.0 + rnd() * 8.0
    return "\n      ".join(rough), "\n      ".join(true)


def mottle():
    """Warm cloudy unevenness, so each plane reads as a worked material rather than a
    printed field. Big and soft enough that it dissolves rather than speckles small."""
    rough, true = [], []
    for _ in range(30):
        lx = LX_MIN - 160 + rnd() * (LX_MAX - LX_MIN + 320)
        ly = -60 + rnd() * (LY_MAX + 120)
        rx, ry = 90 + rnd() * 230, 70 + rnd() * 190
        op = 0.028 + rnd() * 0.055
        col = "#8C7A5E" if rnd() < 0.62 else "#FFF6E4"
        rough.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                     f'fill="{col}" fill-opacity="{op:.3f}"/>')
    for _ in range(22):
        lx = LX_MIN - 160 + rnd() * (LX_MAX - LX_MIN + 320)
        ly = LY_MIN - 60 + rnd() * (60 - LY_MIN)
        rx, ry = 130 + rnd() * 280, 90 + rnd() * 200
        op = 0.022 + rnd() * 0.042
        col = "#9C8A6C" if rnd() < 0.5 else "#FFFFFF"
        true.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                    f'fill="{col}" fill-opacity="{op:.3f}"/>')
    return "\n      ".join(rough), "\n      ".join(true)


def stone():
    """Faint blotching on the iron's own top face, so the graphite reads as a worn
    ground surface rather than as a fill. Local-frame coords, clipped to the face."""
    out = []
    for _ in range(34):
        lx = -20 + rnd() * (BLADE_LEN + 40)
        ly = rnd() * BLADE_THICK
        rx, ry = 28 + rnd() * 96, 16 + rnd() * 46
        op = 0.038 + rnd() * 0.070
        # ROUND 7: was #8E97A4 / #14171B, both blue. C2's stone mottles neutral-to-warm;
        # the iron's own blotching cannot be the one cool thing in a scene with no cool light.
        col = "#9A968C" if rnd() < 0.55 else "#191714"
        out.append(f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
                   f'fill="{col}" fill-opacity="{op:.3f}"/>')
    return "\n        ".join(out)


# ---------------------------------------------------------------- micro-relief
# ROUND 8 (detail). After the material round the master's colour was right and its
# GRANULARITY was not. Measured on matched 1024 crops, the two carry almost the same
# texture ENERGY in the un-planed field - C2 sd 10.4, ours 9.65 - but ours spends it on
# about thirty wide soft dashes and a few enormous mottle clouds, where C2 spends it on
# a dense field of torn fibres. The tell is edge density, not amplitude: over the same
# ground C2 puts 33.3% of its pixels above a gradient of 4/255 and ours puts 7.7%. On
# the iron's own face the gap is worse - C2 21.3%, ours 6.1%, and in a clean patch of
# stone C2 measures sd 4.6 against our 0.9. That is the whole of edge_f1 0.048 at 1024.
#
# Answering it with paths is the wrong instrument: matching C2's fibre count would cost
# several thousand of them. It is authored instead as a HEIGHT FIELD - one feTurbulence
# lit by feDiffuseLighting from the icon's own key, multiplied back over the surface it
# belongs to. Three properties come free and are the reason for the construction:
#   - it costs no paths at all;
#   - the light is the scene's one light, re-expressed in the surface's frame, so the
#     relief cannot introduce a second source the way hand-drawn ticks can;
#   - normalised on the flat-surface value (1/sin elevation) it is a pure MODULATION, so
#     a surface with no relief comes out unchanged and the field means - which is what
#     polarity, figure-ground and the whole small-size read are made of - do not move.
FIBRE_BF = (0.26, 0.038)      # across-grain / along-grain noise frequency, LOCAL frame.
                              # 1/0.26 ~ 4px fibres, 1/0.038 ~ 26px long: measured off C2
FIBRE_SCALE = 0.80            # surfaceScale. Calibrated in rsvg-convert against C2's
                              # sd 18.3 in its worst band; lands at 17.4 alone, ~18 once
                              # the existing tear dashes are counted
FIBRE_ELEV = 42.0             # raking, because torn end-grain is what casts these
PIT_BF = (0.55, 0.55)         # isotropic: pitting in cast stone has no direction
PIT_SCALE = 0.50              # -> sd 4.2 against C2's 4.5 in the same patch
PIT_ELEV = 50.0


def relief_filter(fid, bf, scale, elev, azimuth, seed):
    """One noise-relief modulation. feTurbulence is the height field, feDiffuseLighting
    lights it from the icon's key, and feComposite arithmetic multiplies that lighting
    back over the source with k1 = 1/sin(elevation) - the value a dead-flat surface
    returns - so flat areas come out exactly as drawn and only relief changes anything."""
    k1 = 1.0 / math.sin(math.radians(elev))
    return f"""  <filter id="{fid}" x="-1200" y="-1200" width="3400" height="3400"
          filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{bf[0]} {bf[1]}" numOctaves="3"
                  seed="{seed}" result="height"/>
    <feDiffuseLighting in="height" surfaceScale="{scale}" diffuseConstant="1"
                       lighting-color="#FFFFFF" result="lit">
      <feDistantLight azimuth="{azimuth:.1f}" elevation="{elev:.0f}"/>
    </feDiffuseLighting>
    <feComposite in="lit" in2="SourceGraphic" operator="arithmetic"
                 k1="{k1:.4f}" k2="0" k3="0" k4="0"/>
  </filter>
"""


def fibre_ramp_stops():
    """The fibre's amplitude along local y, as mask stops. Two things are encoded and
    both were measured off C2 rather than chosen: the STEP at the cut, and the fade
    toward the key. Reading C2 in the master's own frame, its texture runs sd 12.6 just
    above the cut, peaks at 18.3 about 285 local units out, and collapses to 5.6 by 513
    - the corner nearest its key light, where the field is blown near white and micro
    relief has no contrast left to show. Ours ran the wrong way round (10.1 near the cut,
    11.7 up by the light). Below the cut C2 measures sd 1.2-2.0: a planed surface is
    nearly glass. Because BOTH sides are the same noise field in the same frame, a fibre
    that crosses the cut continues on the far side at a tenth of its height - which is
    the icon's whole argument, made literally rather than by analogy."""
    span = LY_MAX - LY_MIN
    def off(ly):
        return (ly - LY_MIN) / span
    stops = [(0.0, 0.05), (off(0.0), 0.12), (off(0.0), 0.80),
             (off(285.0), 1.00), (off(513.0), 0.34), (1.0, 0.24)]
    return "\n    ".join(
        f'<stop offset="{o:.4f}" stop-color="#FFFFFF" stop-opacity="{a:.2f}"/>'
        for o, a in stops)


# ---------------------------------------------------------------- the shaving
# A shaving is a RIBBON, and the three attempts that failed all drew a spiral
# OUTLINE - a closed curve with a hole in it, which is a shell, not material.
# This one is a swept surface: ONE cross-section curve (a nearly straight tail
# leaving the blade, easing into a loose roll of just over a turn) swept along
# the blade's own axis by the ribbon's width. That surface is then cut into
# bands, and each band is shaded by its real facing angle to the single
# top-left light. Bands whose OUTER face turns toward the viewer are lit; the
# ones on the far side are seen from the INSIDE, through the open end of the
# roll, so they take the shadow family plus a small transmitted lift where the
# outer face is in light. The free end tapers in opacity, because that is the
# thinnest, most-curled material and the ground has to show through it.
#
# Measured off the C2 raster: its curl is NOT a pale shape on a dark ground.
# Its lit top sits at L 0.576 against ground at L 0.635 right beside it, and it
# falls to L 0.27 at the bottom. It reads by internal form-shading and thin rim
# edges, never by a value jump. The palette below holds to that.

CURL_C      = (326.0, 302.0)        # centre of the roll
CURL_R      = 78.0                  # radius where the tail enters the roll
CURL_R_END  = 69.0                  # radius at the free end: barely tightened, because
                                    # a shaving this fresh is loosely rolled, not a snail
CURL_TURNS  = 0.78                  # PARTIALLY unrolled, which is the whole point: an open
                                    # hook, not a closed ring. Past a full turn the swept
                                    # ribbon closes into a tube and reads as a roll of tape;
                                    # short of one, the cross-section is an arc, so no
                                    # complete far ellipse is ever drawn and the tail runs
                                    # up through the gap the way C2's does.
CURL_PHI0   = math.radians(-24.0)   # entry, on the roll's right flank
CURL_BASE_L = (289.0, 130.0)        # where it leaves the blade, in the BLADE's own frame,
                                    # just inside the worn back edge. Held in local coords
                                    # so the pitch carries it: when the top face shears,
                                    # the tail's exit point rides with it instead of
                                    # floating off the metal.
CURL_BASE   = to_top(*CURL_BASE_L)
CURL_SWEEP  = 106.0                 # ribbon width, along the blade axis. Wide against the
                                    # radius (1.7:1) because C2's runs 2.2:1 - that ratio is
                                    # what makes a roll read as a fat cylinder and not a hoop
SX, SY      = -UX * CURL_SWEEP, -UY * CURL_SWEEP
# near rim -> far rim runs DOWN-LEFT, so the open end of the roll faces the viewer
# and the interior shows on the lower-left. That is C2's read exactly.

CURL_FORE   = 0.54                  # the cross-section is a circle seen obliquely, so it
                                    # is compressed along the roll's own axis. Without this
                                    # the mouth draws as a full circle and the whole thing
                                    # reads as a tin can; C2's mouth is a narrow ellipse.

SU = (-UX, -UY)                     # the roll's axis, running away from the viewer
SP = (-SU[1], SU[0])                # and its perpendicular, in the picture plane

LIGHT = (-0.36, -0.93)              # the one soft top-left source, mostly overhead


def _fore(dx, dy):
    a = (dx * SU[0] + dy * SU[1]) * CURL_FORE
    b = dx * SP[0] + dy * SP[1]
    return (a * SU[0] + b * SP[0], a * SU[1] + b * SP[1])

OUT_LIT   = (243, 234, 216)         # outer face, square to the light
OUT_DARK  = (134, 118,  97)         # outer face, turned away
IN_LIT    = (198, 180, 156)         # inner face at the mouth of the roll
IN_DARK   = ( 84,  72,  60)         # inner face, deep
TRANSMIT  = (250, 241, 221)         # what comes through thin material from behind


def _unit(x, y):
    m = math.hypot(x, y) or 1.0
    return (x / m, y / m)


def _lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _hex(c):
    return "#%02X%02X%02X" % c


TAIL_N = 18


def _curl_section(n_roll=78, n_tail=TAIL_N):
    """The cross-section, near rim. Returns (x, y, r) where r is distance from the
    roll's axis, used as the depth key: a rolled ribbon stacks outermost-on-top."""
    total = CURL_TURNS * 2 * math.pi

    def roll_pt(t):
        phi = CURL_PHI0 - total * t
        r = CURL_R - (CURL_R - CURL_R_END) * (t ** 1.4)
        fx, fy = _fore(r * math.cos(phi), r * math.sin(phi))
        return (CURL_C[0] + fx, CURL_C[1] + fy, r)

    ex, ey, _ = roll_pt(0.0)
    # direction of travel (blade -> free end) at the entry, carried through the same
    # foreshortening so the tail meets the roll tangentially instead of kinking into it
    tx, ty = _unit(*_fore(math.sin(CURL_PHI0), -math.cos(CURL_PHI0)))
    span = math.hypot(ex - CURL_BASE[0], ey - CURL_BASE[1])
    c1 = (CURL_BASE[0] + 0.10 * (ex - CURL_BASE[0]),
          CURL_BASE[1] + 0.42 * (ey - CURL_BASE[1]))
    c2 = (ex - tx * span * 0.40, ey - ty * span * 0.40)

    pts = [(CURL_BASE[0], CURL_BASE[1], CURL_R + span)]
    for i in range(1, n_tail + 1):
        t = i / n_tail
        u = 1 - t
        pts.append((u**3 * CURL_BASE[0] + 3*u*u*t*c1[0] + 3*u*t*t*c2[0] + t**3 * ex,
                    u**3 * CURL_BASE[1] + 3*u*u*t*c1[1] + 3*u*t*t*c2[1] + t**3 * ey,
                    CURL_R + span * (1 - t)))
    for i in range(1, n_roll + 1):
        pts.append(roll_pt(i / n_roll))
    return pts


TAPER_FROM = 0.76


def _taper(t):
    """Opacity along the ribbon. C2's shaving is OPAQUE over its body and translucent
    only where it has curled right over on itself, so that is what this does: solid
    until the last fifth, then thinning hard at the free end."""
    if t <= TAPER_FROM:
        return 1.0
    return 1.0 - 0.52 * ((t - TAPER_FROM) / (1.0 - TAPER_FROM)) ** 1.1


def _runs(segs, width, colour):
    """Merge consecutive stroke segments that round to the same opacity, so the rim
    ships as a handful of polylines instead of a hundred one-segment paths."""
    out, i = [], 0
    while i < len(segs):
        op = segs[i][0]
        j = i
        chain = [segs[i][1]]
        while j < len(segs) and segs[j][0] == op:
            chain.append(segs[j][2])
            j += 1
        if op > 0.02:
            out.append(f'<path d="{open_poly(chain)}" stroke="{colour}" '
                       f'stroke-opacity="{op:.2f}" stroke-width="{width}"/>')
        i = j
    return out


def shaving():
    sec = _curl_section()
    near = [(x, y) for x, y, _ in sec]
    rad = [r for _, _, r in sec]
    far = [(x + SX, y + SY) for x, y in near]
    n = len(near)
    last = n - 2
    ys = [y for _, y in near] + [y for _, y in far]
    y_top, y_bot = min(ys), max(ys)

    bands, near_segs, far_segs = [], [], []
    for i in range(n - 1):
        p0, p1 = near[i], near[i + 1]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        tx, ty = _unit(p1[0] - p0[0], p1[1] - p0[1])
        nx, ny = -ty, tx
        if (mx - CURL_C[0]) * nx + (my - CURL_C[1]) * ny < 0:
            nx, ny = -nx, -ny                      # outward, away from the roll's axis
        lam = nx * LIGHT[0] + ny * LIGHT[1]        # lambert on the OUTER face
        outer = (nx * UX + ny * UY) > 0            # is the outer face the one we see?
        t = i / last
        tap = _taper(t)

        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            op = tap
        else:
            lin = -nx * LIGHT[0] - ny * LIGHT[1]   # lambert on the INNER face
            dux, duy = _unit(mx - CURL_C[0], my - CURL_C[1])
            depth = 0.5 + 0.5 * duy                # 1 at the floor of the roll
            ao = 1.0 - 0.74 * depth                # the roll shades its own interior
            col = _lerp(IN_DARK, IN_LIT, max(0.0, min(1.0, (lin + 0.30) / 1.24)) * ao)
            col = _lerp(col, TRANSMIT, max(0.0, lam) * 0.12)
            op = tap

        # Seam control: while a band is opaque it is grown a hair along the tangent so
        # it overlaps its neighbours and no antialiased hairline can show the ground
        # between them. Once the taper starts, overlapping would double-composite into
        # a dark seam, so the growth is dropped there instead.
        e = 0.9 if op >= 0.999 else 0.0
        a0 = (p0[0] - tx * e, p0[1] - ty * e)
        a1 = (p1[0] + tx * e, p1[1] + ty * e)
        b1 = (a1[0] + SX, a1[1] + SY)
        b0 = (a0[0] + SX, a0[1] + SY)
        amb = 1.0 - 0.20 * ((my - y_top) / max(1.0, y_bot - y_top))
        col = tuple(int(round(c * amb)) for c in col)

        bands.append(((0 if not outer else 1, rad[i]),
                      f'<path d="{poly([a0, a1, b1, b0])}" fill="{_hex(col)}"'
                      + ('' if op >= 0.999 else f' fill-opacity="{op:.3f}"') + '/>'))

        # the ribbon's cut edges: a hairline wherever the thickness catches the light
        near_segs.append((round(0.40 * max(0.0, (lam + 0.62) / 1.62) * tap, 2), p0, p1))
        far_segs.append((round(0.09 * max(0.0, (lam + 0.62) / 1.62) * tap, 2),
                         far[i], far[i + 1]))

    bands.sort(key=lambda b: b[0])

    # grain: the wood runs along the direction of travel, which is along the ribbon's
    # LENGTH, so a copy of the cross-section at a fixed sweep offset IS a grain line
    grain_lines = []
    roll = near[TAIL_N:]
    for k, op in ((0.26, 0.026), (0.42, 0.019), (0.58, 0.023), (0.75, 0.016)):
        chain = [(x + SX * k, y + SY * k) for x, y in roll]
        grain_lines.append(f'<path d="{open_poly(chain)}" stroke="#7E6E56" '
                           f'stroke-opacity="{op:.3f}" stroke-width="1.3"/>')

    body = "\n      ".join(b[1] for b in bands)
    grain_svg = "\n      ".join(grain_lines)
    near_rim = "\n      ".join(_runs(near_segs, "2.6", "#FFF8EA"))
    far_rim = "\n      ".join(_runs(far_segs, "2.0", "#FFF6E6"))
    # the free end, seen end-on: the one place the ribbon's own thickness is legible
    cut = (f'<path d="M {near[-1][0]:.1f} {near[-1][1]:.1f} L {far[-1][0]:.1f} '
           f'{far[-1][1]:.1f}" stroke="#FFF6E8" stroke-opacity="0.15" stroke-width="1.8"/>')
    sil = near + far[::-1]
    return body, grain_svg, near_rim, far_rim, cut, sil, near, far


SHAVING_BODY, SHAVING_GRAIN, SHAVING_NEAR_RIM, SHAVING_FAR_RIM, \
    SHAVING_CUT, SHAVING_SIL, _CN, _CF = shaving()

ROUGH_GRAIN, TRUE_GRAIN = grain()
ROUGH_MOTTLE, TRUE_MOTTLE = mottle()
STONE = stone()


def _fo(d):
    """A front-face gradient stop offset, from its true distance d (local units) above
    the cutting edge. Keeps the hone's falloff fixed in real distance however deep the
    wedge is cut."""
    return 1.0 - d / RISE_LY


# ---------------------------------------------------------------- document
SHAVING_GRAD = (f"""  <filter id="curlShadow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="20"/>
  </filter>
  <filter id="curlSettle" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="1.0"/>
  </filter>

""" if SHAVING else "")

# the curl's own shadow on the un-planed ground: soft, weak and high, because the
# thing casting it is thin and stands off the surface
SHAVING_SHADOW = (f"""<!-- the shaving's shadow: thin material standing off the ground -->
    <g filter="url(#curlShadow)">
      <path d="{poly([(x + 26, y + 32) for x, y in SHAVING_SIL])}"
            fill="#4B4133" fill-opacity="0.20"/>
    </g>""" if SHAVING else "")

SHAVING_BLOCK = (f"""<!-- the shaving: the evidence that the plane actually cut. A ribbon
         swept along the blade's axis and banded, not a spiral outline. -->
    <g filter="url(#curlSettle)">
      {SHAVING_BODY}
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
      {SHAVING_GRAIN}
      </g>
      <g fill="none" stroke-linecap="round" stroke-linejoin="round">
      {SHAVING_FAR_RIM}
      {SHAVING_NEAR_RIM}
      {SHAVING_CUT}
      </g>
    </g>""" if SHAVING else "")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}" role="img" aria-label="improve-skill">
<title>improve-skill</title>
<!--
  Direction "The Honed Edge": Tahoe gel-glass sub-register (a), porcelain + gel object.
  The tile is the workpiece. A worn plane iron lies mid-pass on a rising diagonal; the
  surface behind it is brighter and truer than the surface ahead, and the single
  vermilion hone line IS the boundary between the two states - and IS the line where
  the solid meets the ground.
  Layers map 1:1 onto Icon Composer: #bg / #mid / #fg / #highlight.
  Full-bleed 1024 artwork; the squircle is a CLIP for preview only. No baked corners,
  no baked drop shadow. Generated by build_icon.py - edit there, not here.
-->
<defs>
  <clipPath id="tileMask"><path d="{SQUIRCLE}"/></clipPath>
  <clipPath id="topFaceClip"><path d="{poly(TOP)}"/></clipPath>
  <!-- everything the pass has already trued -->
  <clipPath id="truedSide">
    <path d="M0 {B_LEFT:.1f} L{W} {B_RIGHT:.1f} L{W} {W} L0 {W} Z"/>
  </clipPath>
  <!-- everything still to come -->
  <clipPath id="roughSide">
    <path d="M0 0 L{W} 0 L{W} {B_RIGHT:.1f} L0 {B_LEFT:.1f} Z"/>
  </clipPath>

  <!-- the un-planed side: cooler, greyer, losing light as it nears the cut. ROUND 7 -
       the axis now also carries the light's own falloff to the right: C2's un-planed
       field runs 0.846 at the top-left down to 0.588 at the top-right (0.70x), where
       ours only fell to 0.696 (0.89x) - too flat for one soft top-left key. -->
  <linearGradient id="roughField" x1="70" y1="20" x2="700" y2="650" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#DBD5C7"/>
    <stop offset="0.50" stop-color="#C2BAA8"/>
    <stop offset="1" stop-color="#A19881"/>
  </linearGradient>

  <!-- the trued side: brighter and warmer, brightest right at the fresh cut. ROUND 7 -
       the far corner was the BUG. Measured, the old build's brightest ground was the
       BOTTOM-LEFT corner at L 0.932 and the bottom-right at 0.848, i.e. the ground was
       brightest furthest from the light: a single-light violation in our own icon, not
       just a mismatch with C2. The field now falls 0.98 -> 0.84 along the light's axis
       while holding its value AT the cut, which is where the polarity is read and where
       the hone's spill lands. -->
  <linearGradient id="truedField" x1="300" y1="430" x2="1090" y2="1120" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFFDF6"/>
    <stop offset="0.40" stop-color="#F9F3E7"/>
    <stop offset="1" stop-color="#DED4BE"/>
  </linearGradient>

  <!-- top face of the iron: facing the soft top-left light. ROUND 7 - the intent here
       was always "warm-leaning graphite, not blue steel", but the constants never said
       so: the old ramp ran #2E3238 -> #5D636B, every stop with B ten points above R, and
       the rendered face measured a flat cool cast (sat 0.13-0.15, B>R) end to end.
       Measured off C2: its top face is NEUTRAL through the body (sat 0.004-0.04) and
       drifts WARM at the back edge (0.319,0.311,0.302 -> 0.378,0.354,0.332) where the
       timber bounces up into it. The LUMINANCE ramp below is unchanged to within 0.01
       at every stop - only the hue moves - so this isolates the cast from the modelling. -->
  <linearGradient id="topFace" x1="0" y1="0" x2="0" y2="{BLADE_THICK}" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX_TOP}">
    <stop offset="0" stop-color="#35352F"/>
    <stop offset="0.34" stop-color="#494841"/>
    <stop offset="0.78" stop-color="#5A584F"/>
    <stop offset="1" stop-color="#66625A"/>
  </linearGradient>

  <!-- a soft sheen where the top-left light lands hardest on the top face. Was a cool
       #CBD5E2 at 0.25 and too tight: it swung the top face 1.63:1 ALONG its length,
       where C2's swings only 1.24:1 - a spotlight on a plane rather than stone. Warmer,
       weaker and broader, so the face's volume comes from its across-depth ramp. -->
  <radialGradient id="topSheen" cx="0.32" cy="0.70" r="0.86">
    <stop offset="0" stop-color="#DED9CD" stop-opacity="0.13"/>
    <stop offset="1" stop-color="#DED9CD" stop-opacity="0"/>
  </radialGradient>

  <!-- front face: in shadow at the top, lit from below by the hone itself. Anchored at
       local y=0 (the cutting edge) and running back to the DEEPEST the wedge ever gets,
       with every stop placed by its true distance from the edge - so light falls off
       with distance from the hone, and the pinched near end stays as dark as the deep
       trailing end at the same height above the timber.
       ROUND 7. Two errors measured out of the render, both invisible to a luminance
       range check. (1) HUE: the top two stops were #181B20 / #1E2026, i.e. BLUE-black
       (B>R), on a face whose only two light sources are a vermilion hone and bounce off
       warm timber. There is no cool light anywhere in this scene, so a blue shadow here
       is not a taste call, it is wrong. C2's front face stays warm the whole way up
       (0.286,0.236,0.218 at mid height; 0.150,0.136,0.125 at its darkest). (2) FLOOR:
       ours crushed to L 0.106-0.128 over most of the face while C2's sits at 0.17-0.25 -
       and our ground is BRIGHTER than C2's, so our bounce should be stronger, not
       weaker. Lifted to a warm 0.15-0.23 and the vermilion carried further up. -->
  <linearGradient id="frontFace" x1="0" y1="{RISE_LY:.2f}" x2="0" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#2A2622"/>
    <stop offset="{_fo(42.80):.4f}" stop-color="#382D25"/>
    <stop offset="{_fo(19.19):.4f}" stop-color="#5A3226"/>
    <stop offset="{_fo(5.90):.4f}" stop-color="#90401F"/>
    <stop offset="1" stop-color="#C94E22"/>
  </linearGradient>

  <!-- ROUND 7. The front face is lit almost entirely BY the hone, so it has to carry the
       hone's own along-length falloff. The old build had none: measured at 15px above the
       cutting edge it read a dead-flat L 0.281 from end to end, where C2 runs 0.274 at the
       leading end down to 0.138 at 66% along - it halves. This is the same physical fact as
       the hone's falloff, applied to the surface the hone lights. Warm-dark, never neutral,
       because what is being removed is warm light. -->
  <linearGradient id="frontFall" x1="0" y1="0" x2="{BLADE_LEN}" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#241A12" stop-opacity="0"/>
    <stop offset="0.30" stop-color="#241A12" stop-opacity="0.08"/>
    <stop offset="0.66" stop-color="#241A12" stop-opacity="0.28"/>
    <stop offset="1" stop-color="#1E1610" stop-opacity="0.38"/>
  </linearGradient>

  <!-- the hone glow spilling onto the surface it has just trued. Every edge of this
       shape is blurred away, because light has no edges; only the boundary clip
       stops it, which is correct - the spill cannot reach the un-planed side. -->
  <linearGradient id="honeWide" x1="0" y1="0" x2="0" y2="-118" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#EF5A2A" stop-opacity="0.20"/>
    <stop offset="0.30" stop-color="#F4813F" stop-opacity="0.075"/>
    <stop offset="0.66" stop-color="#FFC79A" stop-opacity="0.022"/>
    <stop offset="1" stop-color="#FFE2C8" stop-opacity="0"/>
  </linearGradient>

  <!-- ROUND 7. THE LARGEST MEASURED GAP OF THE ROUND. Sampled along the hone itself,
       C2 reads L 0.95-0.98 for the leading 30% of the blade and then falls off a cliff -
       0.91 / 0.74 / 0.53 / 0.30 - extinguished into the ground by about 62% along. The
       old build measured a DEAD FLAT L 0.89 for all 640px: a neon tube, not a cut.
       C2 is physically right and the reason is the icon's own premise - the glow is the
       cut happening, and the cut is happening where the iron is buried in the timber at
       the leading end; behind it the edge has already left the wood.
       This mask carries that falloff onto every layer the hone owns (bloom, glow, core,
       specular), so they cannot drift apart. It does NOT extinguish: C2 goes to zero and
       fails the rubric's two-state check for it, so this holds a floor of ~0.3 through
       the trailing end and the signature line stays unbroken at 16px. -->
  <linearGradient id="honeFallRamp" x1="0" y1="0" x2="{BLADE_LEN}" y2="0"
                  gradientUnits="userSpaceOnUse" gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.94"/>
    <stop offset="0.30" stop-color="#FFFFFF" stop-opacity="1"/>
    <stop offset="0.52" stop-color="#FFFFFF" stop-opacity="0.72"/>
    <stop offset="0.76" stop-color="#FFFFFF" stop-opacity="0.44"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.30"/>
  </linearGradient>
  <mask id="honeFall" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{W}">
    <rect width="{W}" height="{W}" fill="url(#honeFallRamp)"/>
  </mask>

  <!-- the honed edge's own colour along its length: hottest where the iron is cutting,
       cooling toward the trailing end. C2's hone core measures (0.96,0.62,0.44) at its
       brightest; the old ramp peaked in the MIDDLE, which is a tube-light read. -->
  <linearGradient id="honeCore" x1="0" y1="0" x2="{BLADE_LEN}" y2="0" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#FF8B4B"/>
    <stop offset="0.24" stop-color="#FF9159"/>
    <stop offset="0.52" stop-color="#F4602C"/>
    <stop offset="0.80" stop-color="#C93C1B"/>
    <stop offset="1" stop-color="#A83017"/>
  </linearGradient>

  <!-- the seat's own occlusion, deepening toward the trailing end where the wedge is
       deepest and the light is most shut out -->
  <linearGradient id="seatRamp" x1="0" y1="0" x2="{BLADE_LEN}" y2="0"
                  gradientUnits="userSpaceOnUse" gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#3A2F22" stop-opacity="0.10"/>
    <stop offset="0.36" stop-color="#372C20" stop-opacity="0.18"/>
    <stop offset="0.72" stop-color="#31281D" stop-opacity="0.32"/>
    <stop offset="1" stop-color="#2C2419" stop-opacity="0.40"/>
  </linearGradient>

  <!-- the rolled edge between the two faces: absent at the leading end (where C2 shows
       only occlusion), a warm roll by the trailing end where the block turns into the
       light. Never blue - nothing in this scene is. -->
  <linearGradient id="bevelRoll" x1="0" y1="0" x2="{BLADE_LEN}" y2="0"
                  gradientUnits="userSpaceOnUse" gradientTransform="{MATRIX}">
    <stop offset="0" stop-color="#8B8478" stop-opacity="0.10"/>
    <stop offset="0.42" stop-color="#948C7F" stop-opacity="0.20"/>
    <stop offset="0.78" stop-color="#A69C8D" stop-opacity="0.38"/>
    <stop offset="1" stop-color="#AFA495" stop-opacity="0.44"/>
  </linearGradient>

{SHAVING_GRAD}  <!-- ROUND 7: re-centred toward the key and deepened. C2's corners measure TL 0.869,
       TR 0.509, BL 0.556, BR 0.562 - one light, up and to the left, and every corner
       away from it falls ~0.6-0.65x. The old vignette sat near the tile's centre at 0.16
       and left the two bottom corners as the brightest ground in the icon. -->
  <radialGradient id="vignette" cx="0.36" cy="0.31" r="0.94">
    <stop offset="0.40" stop-color="#000000" stop-opacity="0"/>
    <stop offset="0.78" stop-color="#3A3226" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#332B20" stop-opacity="0.27"/>
  </radialGradient>

  <filter id="castShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="26"/>
  </filter>
  <filter id="contactShadow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="honeGlow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="13"/>
  </filter>
  <filter id="stoneBlur" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="15"/>
  </filter>
  <filter id="mottleBlur" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="46"/>
  </filter>
  <filter id="bloomBlur" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="30"/>
  </filter>
  <filter id="honeGlowTight" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="4"/>
  </filter>
  <filter id="bevelSoft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
  <filter id="seatShadow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
</defs>

<g clip-path="url(#tileMask)">

  <g id="bg">
    <!-- the surface still to be trued -->
    <path d="M0 0 L{W} 0 L{W} {B_RIGHT:.1f} L0 {B_LEFT:.1f} Z" fill="url(#roughField)"/>
    <!-- the surface already trued: brighter, warmer, and truer -->
    <path d="M0 {B_LEFT:.1f} L{W} {B_RIGHT:.1f} L{W} {W} L0 {W} Z" fill="url(#truedField)"/>
    <!-- cushion: a gentle edge vignette, so the tile is a cushion and not a print -->
    <rect width="{W}" height="{W}" fill="url(#vignette)"/>
  </g>

  <g id="mid">
    <!-- warm cloudy unevenness in each plane: worked material, not printed field -->
    <g clip-path="url(#roughSide)"><g filter="url(#mottleBlur)"><g transform="{MATRIX}">
      {ROUGH_MOTTLE}
    </g></g></g>
    <g clip-path="url(#truedSide)"><g filter="url(#mottleBlur)"><g transform="{MATRIX}">
      {TRUE_MOTTLE}
    </g></g></g>

    <!-- one grain family crossing the boundary: torn above it, true below it -->
    <g fill="none" stroke-linecap="round">
      <g clip-path="url(#truedSide)"><g transform="{MATRIX}">
        {TRUE_GRAIN}
      </g></g>
      <g clip-path="url(#roughSide)"><g transform="{MATRIX}">
        {ROUGH_GRAIN}
      </g></g>
    </g>

    <!-- the solid's own shadow, from the one soft top-left light: a deep soft cast
         plus a tight occlusion where it actually touches down -->
    <g filter="url(#castShadow)">
      <path d="{poly([(x + 30, y + 34) for x, y in SILHOUETTE])}" fill="#4B4133" fill-opacity="0.35"/>
    </g>
    <g filter="url(#contactShadow)">
      <path d="{poly([(x + 9, y + 12) for x, y in SILHOUETTE])}" fill="#3C3327" fill-opacity="0.42"/>
    </g>
    <!-- ROUND 7. Ambient occlusion in the seat itself. Measured 6px out from the base,
         C2's ground sits at 0.66x its own far field under the lit leading end and 0.41x
         under the trailing end - the occlusion DEEPENS where the wedge stands taller and
         the light cannot reach in. Ours was a flat 0.59-0.60x the whole way. A tight
         warm band hugging the contact line, ramped along the blade, supplies the
         difference; it is clipped to the trued side so it cannot leak across the split. -->
    <g clip-path="url(#truedSide)" filter="url(#seatShadow)">
      <path d="{open_poly([(x + 3, y + 5) for x, y in CONTACT])}" fill="none"
            stroke="url(#seatRamp)" stroke-width="26" stroke-linecap="round"/>
    </g>

    {SHAVING_SHADOW}

    <!-- the hone's light on the surface it just cut. Clipped to the trued side and drawn
         under the blade, so it can only ever read as spill from the edge. The wide
         bloom is a tapered shape pushed through a heavy blur, so it has no edge of
         its own anywhere - it decays into the trued plane instead of ending. The whole
         group rides the honeFall mask, so the spill on the ground fades along the blade
         exactly as the edge itself does - which is what makes C2's trued side darken
         toward the trailing end (its ground there reads 0.41x the far field, against
         0.66x under the lit leading end). -->
    <g clip-path="url(#truedSide)" mask="url(#honeFall)">
      <g filter="url(#bloomBlur)">
        <path d="M -30 6 L {BLADE_LEN + 26:.0f} 6 L {BLADE_LEN - 74:.0f} -118 L 74 -118 Z"
              transform="{MATRIX}" fill="url(#honeWide)"/>
      </g>
      <path d="M 30 0 L {BLADE_LEN - 26:.0f} 0" transform="{MATRIX}" stroke="#FF7A3C"
            stroke-opacity="0.52" stroke-width="26" filter="url(#honeGlow)"/>
    </g>
  </g>

  <g id="fg">
    {SHAVING_BLOCK}
    <!-- the plane iron as a real solid: a front face dropping to the ground, and a top
         face lifted clear of it. The silhouette is one chunky block at every size. -->
    <path d="{poly(FRONT_FACE)}" fill="url(#frontFace)"/>
    <!-- the hone's along-length falloff, carried onto the face the hone lights -->
    <path d="{poly(FRONT_FACE)}" fill="url(#frontFall)"/>
    <path d="{poly(TOP)}" fill="url(#topFace)"/>
    <g clip-path="url(#topFaceClip)"><g filter="url(#stoneBlur)"><g transform="{MATRIX_TOP}">
        {STONE}
    </g></g></g>
    <path d="{poly(TOP)}" fill="url(#topSheen)"/>
    <!-- wear on the back: two faint grind striations, on the top face -->
    <g transform="{MATRIX_TOP}" fill="none">
      <path d="M 78 122 L {BLADE_LEN - 98:.0f} 122" stroke="#9A9285" stroke-opacity="0.16" stroke-width="3"/>
      <path d="M 128 100 L {BLADE_LEN - 152:.0f} 100" stroke="#9A9285" stroke-opacity="0.09" stroke-width="2"/>
    </g>
  </g>

  <g id="highlight" fill="none">
    <!-- ROUND 7. The junction between top face and front face WAS a 4.4px #848E9C
         pinstripe at 0.56 - cool, and +72% over the face beside it. Measured across C2
         at three points along the block, that junction is the DARKEST part of the whole
         cross-section over the leading two thirds (L 0.245 -> 0.209 -> 0.201 going up
         through it) and only becomes a rolled highlight near the trailing end, where it
         reads +18% and warm. So: a soft warm occlusion trough sitting in the junction,
         and a narrower warm roll whose strength RAMPS toward the trailing end. That
         pinstripe was the single most vector-looking thing on the block. -->
    <g filter="url(#bevelSoft)">
      <path d="{open_poly([(x, y + 7) for x, y in CHAIN_LOWER])}" stroke="#241C16"
            stroke-opacity="0.30" stroke-width="15" stroke-linecap="round"/>
    </g>
    <path d="{open_poly(CHAIN_LOWER)}" stroke="url(#bevelRoll)" stroke-width="3.4"
          stroke-linecap="round"/>
    <!-- rim light along the worn back, from the same top-left source. Was #B6C0CE at
         0.64 - cool and hot. C2's back rim runs +15% to +34% over the face below it and
         is WARM (0.378,0.354,0.332), lit by bounce off the timber behind. -->
    <path d="M 46 {BLADE_THICK - 2:.0f} C {BLADE_LEN * 0.34:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN * 0.66:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN - 36:.0f} {BLADE_THICK - 2:.0f}"
          transform="{MATRIX_TOP}" stroke="#ABA294" stroke-opacity="0.52" stroke-width="5"
          stroke-linecap="round"/>
    <!-- the vermilion hone line: the cutting edge, the before/after boundary, and the
         line where the solid meets the ground. One shape, four jobs. Masked by honeFall
         so the edge cools toward the trailing end with everything else it lights. -->
    <g mask="url(#honeFall)">
      <path d="M 10 0 L {BLADE_LEN - 8:.0f} 0" transform="{MATRIX}" stroke="#FF8A50"
            stroke-opacity="0.75" stroke-width="16" filter="url(#honeGlowTight)"/>
      <path d="M 10 0 L {BLADE_LEN - 8:.0f} 0" transform="{MATRIX}" stroke="url(#honeCore)"
            stroke-width="12" stroke-linecap="butt"/>
      <path d="M 56 -0.6 L {BLADE_LEN - 58:.0f} -0.6" transform="{MATRIX}" stroke="#FFE3CD"
            stroke-opacity="0.96" stroke-width="4.2" stroke-linecap="round"/>
    </g>
    <!-- cushion rim light around the tile perimeter -->
    <path d="{SQUIRCLE}" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="3"/>
  </g>

</g>
</svg>
"""

(ASSETS / "icon.svg").write_text(svg)
print(f"wrote icon.svg  boundary (0,{B_LEFT:.0f}) -> ({W},{B_RIGHT:.0f})")
_top_ang = math.degrees(math.atan2(-(UY - K_RISE), UX))
print(f"pitch: front face {RISE_NEAR:.0f}px deep at the leading end -> {RISE_FAR:.0f}px at the"
      f" trailing end ({RISE_FAR / RISE_NEAR:.2f}:1)")
print(f"       hone line {math.degrees(ANGLE):.1f} deg, top-face edges {_top_ang:.1f} deg"
      f"  (+{_top_ang - math.degrees(ANGLE):.1f} deg of pitch)")
xs = [p[0] for p in SILHOUETTE]
ys = [p[1] for p in SILHOUETTE]
print(f"solid bbox x {min(xs):.0f}-{max(xs):.0f} ({max(xs)-min(xs):.0f}px = {(max(xs)-min(xs))/W*100:.1f}% of tile)")
print(f"          y {min(ys):.0f}-{max(ys):.0f} ({max(ys)-min(ys):.0f}px)"
      f"   focal centre ({(min(xs)+max(xs))/2:.0f},{(min(ys)+max(ys))/2:.0f})")
print(f"safe-zone margins  L{min(xs):.0f} R{W-max(xs):.0f} T{min(ys):.0f} B{W-max(ys):.0f}")
if SHAVING:
    cxs = [p[0] for p in _CN + _CF]
    cys = [p[1] for p in _CN + _CF]
    print(f"shaving bbox x {min(cxs):.0f}-{max(cxs):.0f} y {min(cys):.0f}-{max(cys):.0f}"
          f"  ({max(cxs)-min(cxs):.0f}x{max(cys)-min(cys):.0f} = "
          f"{(max(cxs)-min(cxs))*(max(cys)-min(cys))/(W*W)*100:.1f}% of tile bbox)")
