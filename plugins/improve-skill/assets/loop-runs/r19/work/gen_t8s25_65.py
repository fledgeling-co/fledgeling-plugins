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
ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent
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

# ---------------------------------------------------------------- the cast shadow
# ROUND 18. Named so the penumbra can be measured rather than guessed. Marching
# perpendicular to each image's own hone line and normalising each profile by its
# own far field (the only way to read a shadow through a 0.22 palette offset),
# ours and C2's agree at contact - 0.670 vs 0.662 of far field in the first 8px,
# 0.636 vs 0.614 at 8-16px - so the two layers below are already right and are left
# alone. What differed was REACH: ours was back to 0.965 of far field by 60-85px
# and 1.003 by 85-115px, while C2's was still 0.865 at 60-85 and 0.940 at 85-115,
# reaching its far field only past 150px. Half-recovery ours ~26px against C2's
# ~64px: the tail was 2.4x too short. At 32px that whole gradient lived inside one
# or two cells and at 16px inside less than one, so the lowest-frequency fact in
# the icon - that the solid is sitting on the ground - did not survive downsampling.
CAST_BLUR = 26.0
CAST_DX = 30.0
CAST_DY = 34.0
CAST_OP = 0.35
CONTACT_BLUR = 9.0
CONTACT_DX = 9.0
CONTACT_DY = 12.0
CONTACT_OP = 0.42
# Widening the cast blur to buy that reach was measured and rejected: it moves the
# far bins onto C2 (+0.0085 at 1024, +0.0064 at 256) but a single Gaussian has a
# slope peak, and at 32px that peak IS an edge - 24 new edge cells appeared in a
# diagonal chain along the blade's lower flank, where C2's own |grad| is 0.04-0.25
# and the widened cast's was 0.41-0.55. C2's ramp has no such inflection. So the
# tail is carried by a separate layer instead: same silhouette, blurred wide enough
# that its peak slope stays under the 32px edge threshold, and weak enough that it
# only supplies the 0.03-0.06 of far field the far bins were missing. Contact is
# untouched, which is the point - the near bins already matched.
HALO_BLUR = 105.0
HALO_DX = 58.0
HALO_DY = 66.0
HALO_OP = 0.30


# ---------------------------------------------------------------- ground texture
# The ground's own luminance, fitted quadratically over each masked plane of the
# render (x, y in units of the 1024 tile; rms residual 0.035 rough / 0.019 trued).
# A ridge has to know what it is drawn on. A fixed-opacity dark stroke loses its
# contrast wherever the field darkens, which is exactly why the master's texture
# faded out away from the key while the reference's held flat: measured band sd
# 0.0114 near the key falling to 0.0039 far from it, against a reference that sits
# at 0.013-0.022 the whole way across.
GROUND_ROUGH = (+0.98889, -0.85663, -0.53139, +0.38975, +0.04117, +0.73688)
GROUND_TRUED = (-1.08929, +2.33595, +3.19389, -0.54761, -1.13929, -2.24668)

GRAIN_DARK, GRAIN_DARK_L = "#4E4636", 0.277    # the shadowed flank of a torn ridge
GRAIN_LITE, GRAIN_LITE_L = "#FFF4DE", 0.960    # its lit flank, half a stroke keyward
GRAIN_OFFSET = 1.7                             # flank separation
GRAIN_PIECE = 190.0                            # re-solve the field every this far
GRAIN_AMP_A = 0.055      # travel-direction family: luminance swing, held flat in r
GRAIN_AMP_B = 0.055      # along-blade family: the second half of the cross-hatch
GRAIN_TRUE_F = 0.13      # the trued plane's share of it
# The lit flanks all paint over the shadowed ones (one group each, so the file can
# carry the colour once instead of 1500 times), so a little of every dark flank is
# erased at a crossing; and on the trued plane the ground is already at 0.85, so an
# off-white twin has almost no headroom left and clips against its own ceiling.
# These are the measured corrections. Rendered against a grain-free ground the pair
# now moves the un-planed plane by -0.0002 and the trued plane by +0.0001.
GRAIN_BAL_ROUGH = 1.00
GRAIN_BAL_TRUED = 1.45

# ROUND 13 (detail). The tear population was authored FLAT across the un-planed plane -
# amplitude held constant in radius on purpose, because r10's instrument said the
# reference's was flat too. Re-measured on the coordinate the reference's own pixels
# actually depend on (`loop-runs/r11/work/m8.py`: bin the local rms of the 3-13px
# high-pass by each candidate coordinate, keep the one with the least within-bin
# residual), relief amplitude is a function of CANVAS Y and of almost nothing else:
# canvas y explains 65.3% of it, distance from the key 22.0%, and distance out from the
# cut - the coordinate r08 read this same fall-off on - only 35.2%.
#
# Down that coordinate the master is already right for two thirds of the plane and then
# falls off a cliff. Reference/master rms per 64px band: 0.86, 0.97, 0.88, 0.93, 1.16
# from y 64 to 384, then 2.18, 2.97, 3.40, 3.15, 3.08, 2.87, 2.44 from y 384 to 832.
# The top of the tile sits inside the key's own hot spot, where the field is up at
# L 0.82 and micro relief has no contrast left to show; the lower band is where the
# light rakes, and that is the only part of a rough plane where tearing is legible.
# 78% of the reference's un-planed edge pixels are in it, against 18% of ours.
#
# GRAIN_PROF is that profile: the amplitude the tear should carry at a canvas height,
# as a multiple of what r10 authored. Held at 1 above y 320 because that part measures
# right already, and eased rather than stepped from y 320 to y 512 - a step would put a
# horizontal edge across the plane, and there is no boundary there to hang it on.
# The band's own peak is pulled to 2.4 against the measured 3.4: the last third of the
# fault is not affordable inside the cap below, and a tear that reads at 16px as noise
# costs the rubric more than the composite pays.
GRAIN_PROF = ((0.0, 1.00), (320.0, 1.05), (384.0, 1.55), (448.0, 2.10),
              (512.0, 2.40), (576.0, 2.40), (640.0, 2.28), (704.0, 2.22),
              (768.0, 2.08), (832.0, 1.80), (1100.0, 1.80))
# ...and it is carried by the GRADIENT THAT PAINTS THE STROKE, not by the geometry.
# A ridge is emitted in GRAIN_PIECE-long pieces, so authoring the profile in the
# geometry means breaking every piece at every knot: measured, that is +622 paths and
# +79KB, which alone puts the file 50KB over its envelope. A linearGradient in the
# grain's own user space, running along the canvas-y direction with stop-opacity as
# the profile, costs four gradients and about 700 bytes, resolves continuously instead
# of per-piece, and multiplies BOTH flanks of every pair by the same factor - so the
# mean-neutrality the whole construction rests on survives untouched.
GRAIN_CAP = 0.55         # the most opacity a single flank may carry

# The second and third faults in the same band, from the same patch spectra
# (`work/m7.py`): the reference's lattice there runs 1.3-1.8x finer than ours (mean
# wavelength 6.0px against 10.9 at the left edge, 28.2 against 35.9 mid-plane), and it
# is dominated by the ALONG-TRAVEL family - peaks at +48, +58 and +72 canvas degrees,
# against family A's +57 - where ours is dominated by the across-pass family at -42 and
# reads anisotropy 13.7 against the reference's 4.68. A pass tears the fibres along the
# direction it travelled, so the profile is split unevenly between the families: A
# takes 1.36 of the combined amplitude and B 0.76, which turns a 1:2 power split into
# 1.6:1 without adding one path. The pitch fault went the same way, as shorter dashes
# inside the band; ROUND 14 below measured the mark itself and retired that band scale.
GRAIN_FAM_A = 1.3625     # family A's share of the combined amplitude profile
GRAIN_FAM_B = 0.7560     # family B's, so sqrt((A^2 + 2 B^2)/3) = 1: same total, new bias
GRAIN_PEAK_A = max(g for _, g in GRAIN_PROF) * GRAIN_FAM_A
GRAIN_PEAK_B = max(g for _, g in GRAIN_PROF) * GRAIN_FAM_B

# ROUND 14 (detail). r13 closed by saying amplitude was solved and the next detail
# round belonged to mark LENGTH and COUNT. Measured, on connected components of the
# 3-13px relief at five clean stations (`loop-runs/r12/work/w3.py`), that is exactly
# the whole of the remaining fault, and coverage is not part of it:
#
#   station          coverage        marks / 10k px     median len      aspect
#   un-planed left   23.5 / 20.7     199 /  87          3.9 / 6.2       1.9 / 3.6
#   un-planed mid    18.8 / 18.5     108 /  40          3.8 / 8.3       1.9 / 3.9
#   un-planed low    20.4 / 17.4     105 /  36          4.5 / 7.1       1.7 / 3.6
#   above-band       17.0 / 17.8      83 /  44          4.4 / 7.6       2.0 / 4.2
#   trued            22.8 / 22.7     192 /  77          3.8 / 10.2      1.8 / 4.8
#                    (reference / ours)
#
# We put the right amount of ink on the plane and spend it on 2.3-2.9x too few marks,
# each 1.6-2.7x too long. The reference's mark is the same everywhere - median 3.8-4.5
# units, p90 8.3-13.1, width 2.0-2.5, aspect 1.7-2.0 at every station on both planes -
# so it is ONE distribution, not a field of them, and r13's band-local dash scale was a
# proxy for this global fault fitted before the fault had been measured. It retires.
#
# Two constants carry the fix and neither is amplitude. GRAIN_MARK_* is the reference's
# own mark-length distribution, drawn per dash. GRAIN_GAP_MIN is the one that fixes the
# trued plane on its own: a gap narrower than the stroke that crosses it is not a break
# once the renderer antialiases it, and the trued plane's `tear` of 0.05-0.20 was
# putting gaps of 0.3-2.0 units into strokes 1.2-2.0 wide - a dasharray that renders as
# a ruled line. Flooring the gap at the stroke's own width is what turns it into flecks.
GRAIN_WID = 1.20         # the reference's mark is wider than ours at every station:
                         # median 2.0-2.5 against r13's 1.7-2.0. Coverage is linear in
                         # it, and shortening the marks spends coverage, so this is
                         # where that is bought back - one factor over all four widths,
                         # and the lit twin's solve is a ratio so the pair is untouched.
GRAIN_MARK_MIN = 1.4     # the reference's shortest legible tear
GRAIN_MARK_RUN = 10.0    # ...and the reach of its tail
GRAIN_MARK_SKEW = 2.2    # rnd()**skew, so the median lands on the measured 3.6, not 5.7
# The floor is swept, not guessed (`loop-runs/r12/work/sweep.py`), and it has a clear
# interior optimum: at 1.15 stroke widths the marks fuse HARDER than r13's did (median
# length 8.1, count 84/10k), at 1.9 the field breaks (4.5, 124), and past 2.4 the gap
# eats the period faster than it wins breaks and both fall away again (4.6, 106 at 3.0).
# 1.9 is where a break survives the renderer's antialiasing with a pixel to spare.
GRAIN_GAP_MIN = 1.9      # a break must be at least this many stroke widths to be one

# ROUND 15 (detail). r14 closed by naming the fault it could not reach: the plane is a
# LATTICE where the reference is a FIELD, and that is a placement fault, not a density
# one. Every instrument this loop has used so far is a statistic of the marks
# THEMSELVES - count, length, width, aspect, coverage, band rms - and all of them are
# blind to how the marks are ARRANGED. Two that are not (`loop-runs/r13/work/w4.py`):
#
#   VOID     the distance from each unmarked pixel to the nearest mark. A lattice of
#            dashed tracks leaves closed cells of bare ground; a field does not.
#   BEARING  each mark's own PCA bearing, binned to 15 canvas degrees, as normalised
#            entropy. Two families of ruled lines put every mark in two bins.
#
#   station          void mean      void p90      bearing entropy   top-2 bin share
#   un-planed left   1.74 / 3.60    3.0 /  7.0    0.927 / 0.552     0.311 / 0.788
#   above-band       3.43 / 8.79    7.0 / 22.0    0.722 / 0.562     0.608 / 0.694
#   trued            1.69 / 3.08    3.0 /  6.0    0.984 / 0.674     0.241 / 0.554
#                    (reference / r14)
#
# The un-planed left station carries the finding: coverage there is 20.2% against the
# reference's 23.5%, so we put very nearly the right amount of ink on the plane, and
# still leave holes twice as wide. That is arrangement and nothing else, which is why
# this round is free - it moves marks that already exist rather than buying more. It
# also has to be: 1514 of the file's 1726 paths are grain, at 153 bytes each, and the
# envelope's remaining headroom is 26,643 bytes.
#
# Three placement constants, all of them micro-geometry:
#
# GRAIN_WANDER. A ridge is a polyline whose nodes are jittered perpendicular to its
# axis. At r14 that jitter was +-1.7 units against an inter-ridge pitch of 11-25 - a
# straight line with a wobble on it, so the marks stayed locked to their track and the
# ground between tracks was never reached. Set to half the pitch and a ridge crosses
# into its neighbours' cells, which is what fills them. This is the constant the void
# statistic is a function of.
#
# GRAIN_NODE. The wander only bends the line where there IS a node; between nodes it is
# straight, and a 47-unit straight run holds a dozen 4-unit marks in a row. Closer nodes
# cost bytes and nothing else - one extra vertex on every grain path is 21,196 of them -
# which is what the coordinate precision below pays for.
#
# GRAIN_SKEW_*. Each family's per-ridge bearing scatter, and the term the bearing
# entropy is most sensitive to. r10 set it to a deliberate +-11/13 deg to keep the
# crossings out of register; the reference wants far more than out-of-register, it wants
# the two families not to be readable as families at all.
GRAIN_WANDER = 3.4       # peak-to-peak node jitter, perpendicular to the ridge
GRAIN_NODE = 60.0        # ...and how far apart those nodes sit along it
GRAIN_SKEW_A = 38.0      # family A's per-ridge bearing scatter, degrees either way
GRAIN_SKEW_B = 40.0      # family B's
GRAIN_PREC = 0           # decimals on a grain vertex; see the byte note above

# ---------------------------------------------------------------- the step at the cut
# ROUND 16 (detail). The cut is this icon's longest boundary and the master drew it as a
# colour change with no geometry: a monotonic ramp from the un-planed field to the trued
# one, plateau to plateau, and nothing in between. C2 draws a STEP. Each image's own cut
# was fitted rather than assumed (`loop-runs/r14/work/w4.py` searches inclination and
# offset for the line of greatest mean-luminance step: ours 34.0 deg, C2's 41.0), and
# luminance was binned by true perpendicular distance d from it. C2's cross-section at
# three stations along the block-free strip is the same four-part signature every time:
#
#   station      un-planed   crest        trough        peak         trued
#   x  20-130      0.500     0.528 @ -3   0.470 @ +2    0.623 @ +7   0.557
#   x 130-240      0.549     0.616 @ -1   0.529 @ +4    0.757 @ +8   0.646
#   x 240-350      0.564     0.596 @ -1   0.543 @ +6    0.865 @ +9   0.697
#
# That is one shaving's thickness of material removed, drawn honestly: the un-planed
# surface's own arris catches the key (+7.8% of its own plateau, mean of the three), the
# riser beneath it faces away from an overhead source and sits in shadow (-18.6% of the
# TRUED plateau), the freshly cut arris at the foot of the riser flares (+17.7%), and
# only then does the trued plane begin. Ours had a +2.5% overshoot where the arris
# belongs and no trough anywhere. The feature survives coarsening - on LANCZOS
# downsamples of C2 the lip still reads +10.8% of its plateau at 256 and +5.4% at 128 -
# so it is ornament that works at icon sizes, not pixel-peeping.
#
# Two of the three amplitudes transfer as measured; the arris does not, and the reason
# is the master's own brightness. C2's trued plane sits at L 0.63 where ours, at the cut,
# measures 0.882, and the brightest paint this icon owns is GRAIN_LITE at 0.960. That
# leaves 8.8% of headroom against C2's 24.1% arris - the step cannot be lit past the
# source. STEP_ARRIS is therefore the largest amplitude that still leaves the band
# translucent (alpha 0.80, +7.1%), and the shortfall is recorded rather than tuned away;
# closing it means moving the trued plane's value, which is a palette round, not this
# one. Nothing here adds a palette entry: the pair is GRAIN_LITE over GRAIN_DARK, the
# same two colours the tear is already made of. All three alphas are solved against the
# fields the RENDER actually has beside the cut - un-planed 0.570, trued 0.882 - not
# against the smeared values the line fit reports.
STEP_UP = 6.0            # the band's reach into the un-planed side, local units
STEP_DOWN = 12.0         # ...and into the trued side. Both are perpendicular distance,
                         # so the whole step is inside measure.py's +-60 skip band and
                         # cannot touch the split polarity.
STEP_CREST = 0.114       # GRAIN_LITE on the un-planed arris, 2 units up: +7.8% of 0.570
STEP_RISER = 0.324       # GRAIN_DARK in the riser, 3.5 units down: -22.2% of 0.882, and
                         # it RAISES saturation there (0.126 -> 0.30), which is what C2
                         # does too (seam 0.167 against its trued plateau's 0.124)
STEP_ARRIS = 0.800       # GRAIN_LITE on the cut arris, 8 units down: +7.1%, at the roof

# The step's amplitude swells along the cut. C2's does - trough -0.087/-0.117/-0.155 and
# peak +0.066/+0.111/+0.168 at the three stations, both growing left to right - and the
# reason is geometric: the cut runs closest to the key at canvas x 478, so that is where
# a raking source lights the arris most squarely. The swell is one gradient along LOCAL
# X, used as a mask over the band. It is anchored on the LAST MEASURED station rather
# than on that geometric peak, which the block occludes: extrapolating to x 478 and
# normalising there would put every visible part of the cut at 60% of an amplitude
# nothing can check. Anchored at x 300 the fit reproduces C2's own stations - -15.0%
# against its measured -15.6% at x 20-130, -18.2% against about -17% at x 135-179.
STEP_SWELL_X = 300.0     # canvas x of the last station the swell was measured at
STEP_SWELL_EDGE = 0.62   # ...and the share of full amplitude left at the tile edges


def step_stops():
    """The whole measured cross-section as one gradient's stops, in the local frame.

    One path, one paint. A step is four features in eighteen units and authoring it as
    four shapes means four edges to keep in register; as stops on a single band it is
    one shape whose profile is continuous by construction, and the colour switch at the
    cut costs a duplicated offset rather than a second element."""
    span = STEP_UP + STEP_DOWN
    prof = [(STEP_UP, GRAIN_LITE, 0.000), (3.5, GRAIN_LITE, 0.045),
            (2.0, GRAIN_LITE, STEP_CREST), (0.8, GRAIN_LITE, 0.050),
            (0.0, GRAIN_LITE, 0.000),
            (-0.2, GRAIN_DARK, 0.070), (-1.2, GRAIN_DARK, 0.190),
            (-3.5, GRAIN_DARK, STEP_RISER), (-5.6, GRAIN_DARK, 0.170),
            (-6.4, GRAIN_DARK, 0.000),
            (-6.6, GRAIN_LITE, 0.120), (-7.4, GRAIN_LITE, 0.480),
            (-8.0, GRAIN_LITE, STEP_ARRIS), (-8.8, GRAIN_LITE, 0.440),
            (-9.8, GRAIN_LITE, 0.140), (-STEP_DOWN, GRAIN_LITE, 0.000)]
    return "".join(
        f'<stop offset="{(STEP_UP - y) / span:.4f}" stop-color="{c}" '
        f'stop-opacity="{a:.3f}"/>' for y, c, a in prof)


def step_swell_stops():
    """The swell along the cut, as mask stops. The frame is a rotation, so a canvas x on
    the cut is one division away from its local x, and the tile's two ends are just the
    local x of the cut where it leaves the canvas."""
    lx = lambda cx: (cx - AX) / UX
    lo, hi, peak = lx(0.0), lx(float(W)), lx(STEP_SWELL_X)
    stops = [(lo, STEP_SWELL_EDGE), (peak, 1.00), (hi, STEP_SWELL_EDGE)]
    return lo, hi, "".join(
        f'<stop offset="{(x - lo) / (hi - lo):.4f}" stop-color="#FFFFFF" '
        f'stop-opacity="{a:.3f}"/>' for x, a in stops)


STEP_SWELL_LO, STEP_SWELL_HI, STEP_SWELL_STOPS = step_swell_stops()


def grain_gain(cy):
    """The tear's combined amplitude at a canvas height, from the reference's profile."""
    for (y0, g0), (y1, g1) in zip(GRAIN_PROF, GRAIN_PROF[1:]):
        if cy <= y1:
            return g0 + (g1 - g0) * (cy - y0) / (y1 - y0)
    return GRAIN_PROF[-1][1]


def tear_profile(gid, colour, fam):
    """The amplitude profile as a stroke paint, in the grain's own frame.

    The frame is a rotation, so canvas y is affine in local coordinates: the point
    s*(UY,NY) sits at canvas y = AY + s. The gradient therefore runs from the local
    image of canvas y 0 to that of y 1024, and offset is canvas height, linearly."""
    p0, p1 = -AY, 1024.0 - AY
    peak = max(g for _, g in GRAIN_PROF) * fam
    stops = "".join(
        f'<stop offset="{y / 1024.0:.4f}" stop-color="{colour}" '
        f'stop-opacity="{g * fam / peak:.3f}"/>'
        for y, g in GRAIN_PROF if y <= 1024.0)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{p0 * UY:.1f}" y1="{p0 * NY:.1f}" '
            f'x2="{p1 * UY:.1f}" y2="{p1 * NY:.1f}">{stops}</linearGradient>')


def ground_lum(coef, px, py):
    x, y = px / 1024.0, py / 1024.0
    a, b, c, d, e, f = coef
    return min(0.94, max(0.42, a + b * x + c * y + d * x * x + e * y * y + f * x * y))


def _key_local():
    """The one key light, re-expressed in the blade's frame, so the lit flank of a
    ridge faces the same source as every other highlight in the icon."""
    lx, ly = LIGHT
    kx, ky = -(UX * lx + UY * ly), -(NX * lx + NY * ly)
    m = math.hypot(kx, ky)
    return kx / m, ky / m


def _dash(tear, wid):
    """Four numbers, so the break pattern's period is two marks rather than one -
    long enough that a stroke reads as torn rather than ruled, and cheap enough to
    put a whole run of a ridge in one path element instead of thirty.

    The MARK is drawn from the reference's own measured length distribution and is
    the same distribution everywhere, because the reference's is (median 3.8-4.5
    units at five stations on both planes). The GAP is then whatever holds this
    ridge's duty cycle - which is what coverage is made of, and coverage already
    matches - except that it may never fall below GRAIN_GAP_MIN stroke widths. That
    floor is the load-bearing half: the old pattern let `tear` set the gap outright,
    so a faint near-continuous ridge asked for gaps of a third of a pixel and got a
    ruled line, and a run of a dozen marks fused into one 170-unit streak. Duty falls
    out of `tear` instead, which is what `tear` meant all along."""
    duty = 0.72 - 0.20 * tear
    v = []
    for _ in range(2):
        mark = GRAIN_MARK_MIN + rnd() ** GRAIN_MARK_SKEW * GRAIN_MARK_RUN
        rnd()                             # keep the jitter stream where r13 left it
        v.append(f"{mark:.1f}")
        v.append(f"{max(GRAIN_GAP_MIN * wid, mark * (1.0 - duty) / duty):.1f}")
    return " ".join(v)


def _clip_span(px, py, dx, dy, t0, t1):
    """Trim a ridge to the part that can actually land on the tile. The frame is a
    rotation, so a unit of t is a unit of canvas; without this, family B's ridges
    each run the full 1500-unit diagonal of the local frame and most of every one
    of them is paths spent outside the artboard."""
    cx, cy = to_canvas(px, py)
    ex, ey = to_canvas(px + dx, py + dy)
    lo, hi = t0, t1
    for p, v in ((cx, ex - cx), (cy, ey - cy)):
        if abs(v) < 1e-9:
            if p < -30.0 or p > W + 30.0:
                return None
            continue
        s0, s1 = (-30.0 - p) / v, (W + 30.0 - p) / v
        lo, hi = max(lo, min(s0, s1)), min(hi, max(s0, s1))
    return (lo, hi) if hi - lo > 8.0 else None


def _ridge(dark, lite, coef, px, py, dx, dy, t0, t1, amp, wid, tear, bal):
    """One ridge as a lit/shadowed pair, emitted in GRAIN_PIECE-long pieces, each
    piece a short polyline that wanders off its own axis. A tear in end grain is not
    a ruled line, and two exactly perpendicular families of ruled lines at an even
    pitch read as brickwork, which is what the first cut of this looked like.

    Each piece solves for the opacities that put a luminance swing of exactly +-amp
    on the ground it actually lands on, and that make the pair mean-neutral: the
    dark flank removes as much light as the twin adds. That balance is the whole
    reason this can be dense. r02's texture was dense too, and it moved the plane's
    mean, so it cost lum on every size and was rejected.

    The mark length is one distribution everywhere, taken off the reference; see
    _dash. The amplitude profile is NOT applied here - it rides the stroke's
    gradient; see tear_profile."""
    span = _clip_span(px, py, dx, dy, t0, t1)
    if span is None:
        return
    t0, t1 = span
    kx, ky = _key_local()
    ox, oy = -dy, dx
    if ox * kx + oy * ky < 0:
        ox, oy = -ox, -oy
    ox, oy = ox * GRAIN_OFFSET, oy * GRAIN_OFFSET
    ux, uy = ox / GRAIN_OFFSET, oy / GRAIN_OFFSET
    wl = wid * 1.15
    t = t0
    while t < t1:
        e = min(t + GRAIN_PIECE, t1)
        cx, cy = to_canvas(px + dx * (t + e) / 2, py + dy * (t + e) / 2)
        g = ground_lum(coef, cx, cy)
        # the reference does not merely hold its texture away from the key, it gains
        # a little: band sd 0.0166 at r 160-320 against 0.0202 at r 800-960
        a = amp * (0.90 + 0.35 * math.hypot(cx - 75.0, cy - 25.0) / 1000.0)
        # If the shadowed flank runs out of opacity, the pair is no longer neutral:
        # the twin would still deliver a swing its partner cannot match. Solve the
        # twin against the amplitude actually ACHIEVED, so a clip costs contrast and
        # never costs the plane's mean.
        head = max(g - GRAIN_DARK_L, 0.10)
        od = a / head
        if od > GRAIN_CAP:
            od, a = GRAIN_CAP, GRAIN_CAP * head
        ol = min(GRAIN_CAP, bal * a * wid / (wl * max(GRAIN_LITE_L - g, 0.10)))
        n = max(2, int((e - t) / GRAIN_NODE) + 1)
        pts = []
        for i in range(n + 1):
            s = t + (e - t) * i / n
            j = (rnd() - 0.5) * GRAIN_WANDER
            pts.append((px + dx * s + ux * j, py + dy * s + uy * j))
        d = _dash(tear, wl)
        seg = "M " + " L ".join(f"{x:.{GRAIN_PREC}f} {y:.{GRAIN_PREC}f}" for x, y in pts)
        dark.append(f'<path d="{seg}" stroke-opacity="{od:.3f}" '
                    f'stroke-width="{wid:.2f}" stroke-dasharray="{d}"/>')
        seg = "M " + " L ".join(f"{x + ox:.{GRAIN_PREC}f} {y + oy:.{GRAIN_PREC}f}"
                                for x, y in pts)
        lite.append(f'<path d="{seg}" stroke-opacity="{ol:.3f}" '
                    f'stroke-width="{wl:.2f}" stroke-dasharray="{d}"/>')
        t = e


def grain():
    """Two crossing families of grain, and the SAME lines cross the boundary: torn
    and broken on the un-planed side, near-continuous and faint on the trued side.
    That continuity is what makes the split read as one surface in two states rather
    than as two different materials. Drawn right across the tile and clipped per
    side, so the block sits ON the grain rather than beside it.

    Two families, not one, because that is what the reference has. Measured on a
    clean patch of un-planed ground it is a cross-hatched torn lattice with cells of
    20-30px, band sd 0.0587 against the master's 0.0046, and an anisotropy of 3.0;
    the master's trued plane read 13.1 - ruled lines, not a worked surface. The
    families run along the travel direction and along the blade, which is what a
    plane leaves: the pass and the tear-out across it.

    ROUND 13 splits the un-planed side's two families into their own groups, because
    each now carries its own amplitude profile down the tile as a stroke gradient and
    the two profiles are not the same: the reference's band is torn ALONG the pass,
    ours was torn across it."""
    rough_a_d, rough_a_l, rough_b_d, rough_b_l = [], [], [], []
    true_d, true_l = [], []

    def skew(deg):
        """A ridge's own bearing. Two families held at exactly 0 and 90 degrees make
        a grid; the reference's lattice scatters by a good ten degrees either way,
        which is what stops the crossings falling into register."""
        a = math.radians((rnd() - 0.5) * 2 * deg)
        return math.cos(a), math.sin(a)

    # --- family A: along the travel direction (local x fixed)
    x = LX_MIN - 40
    while x < LX_MAX + 40:
        tear = 0.52 + rnd() * 0.48
        sy, sx = skew(GRAIN_SKEW_A)
        _ridge(rough_a_d, rough_a_l, GROUND_ROUGH, x, 0.0, sx, sy, 4.0, LY_MAX + 30,
               GRAIN_AMP_A * GRAIN_PEAK_A * (0.7 + rnd() * 0.6), GRAIN_WID * (1.5 + rnd() * 0.9),
               tear, GRAIN_BAL_ROUGH)
        sy, sx = skew(GRAIN_SKEW_A)
        _ridge(true_d, true_l, GROUND_TRUED, x, 0.0, sx, -sy, 4.0, -(LY_MIN - 30),
               GRAIN_AMP_A * GRAIN_TRUE_F * (0.7 + rnd() * 0.6),
               GRAIN_WID * (1.3 + rnd() * 0.7), 0.06 + rnd() * 0.16, GRAIN_BAL_TRUED)
        x += 11.0 + rnd() * 14.0
    # --- family B: along the blade (local y fixed), the tear-out across the pass.
    #     Same amplitude and near enough the same pitch as family A, because a
    #     lattice with one strong family and one weak one is still a ruled field:
    #     the first cut of this made B two thirds of A's amplitude at a third
    #     less density, and the far patch's anisotropy went UP, 5.4 to 9.6.
    y = 9.0
    while y < LY_MAX + 30:
        sx, sy = skew(GRAIN_SKEW_B)
        _ridge(rough_b_d, rough_b_l, GROUND_ROUGH, 0.0, y, sx, sy,
               LX_MIN - 40, LX_MAX + 40,
               GRAIN_AMP_B * GRAIN_PEAK_B * (0.7 + rnd() * 0.6), GRAIN_WID * (1.4 + rnd() * 1.0),
               0.68 + rnd() * 0.32, GRAIN_BAL_ROUGH)
        y += 12.0 + rnd() * 15.0
    y = -9.0
    while y > LY_MIN - 30:
        sx, sy = skew(GRAIN_SKEW_B)
        _ridge(true_d, true_l, GROUND_TRUED, 0.0, y, sx, sy, LX_MIN - 40, LX_MAX + 40,
               GRAIN_AMP_B * GRAIN_TRUE_F * (0.7 + rnd() * 0.6),
               GRAIN_WID * (1.2 + rnd() * 0.8), 0.05 + rnd() * 0.14, GRAIN_BAL_TRUED)
        y -= 12.0 + rnd() * 15.0

    def wrap(*layers):
        return "\n      ".join(f'<g stroke="{paint}">\n      ' +
                               "\n      ".join(items) + '\n      </g>'
                               for items, paint in layers)

    return (wrap((rough_a_d, "url(#tearAD)"), (rough_b_d, "url(#tearBD)"),
                 (rough_a_l, "url(#tearAL)"), (rough_b_l, "url(#tearBL)")),
            wrap((true_d, GRAIN_DARK), (true_l, GRAIN_LITE)))


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

# ROUND 8, coarse structure. Both of C2's rims were FITTED rather than eyeballed: three
# points were read off each silhouette arc and the circle through them solved.
#
#     near rim  centre (294, 253)  R 115      residual under 2px over a 240px arc
#     far rim   centre (359, 186)  R 121
#
# Three things fall out of that fit, and the roll here disagreed with all three.
#   * Both rims are CIRCLES. A circle projects to a circle only when its plane is
#     parallel to the image plane, so C2's roll axis points essentially straight at the
#     viewer and there is NO in-plane compression of the section left to draw.
#   * The centres are 93px apart, against R 115. The roll is far wider than it is long -
#     2.5:1 on diameter - where this was built at 1.36:1 and read as a length of pipe
#     lying on the boards.
#   * The offset between them subtends 45.9 deg, not the blade's 33 deg. The roll has
#     tipped off the edge it came from.
# The ribbon also leaves C2's blade as a 40px stub off the roll's lower flank, not as the
# 150px straight chute that ran up from this roll's upper-right entry.

CURL_C      = (308.0, 278.0)        # centre of the roll. Sited off the blade rather than
                                    # copied as a canvas coordinate: C2's roll clears its
                                    # own blade's back edge by 53px, and this one clears
                                    # THIS blade's back edge by 50.
CURL_R      = 115.0                 # measured on C2. Was 78.
CURL_R_END  = 102.0                 # the same gentle tightening as before, 0.89 of R
CURL_TURNS  = 0.78                  # PARTIALLY unrolled, which is the whole point: an open
                                    # hook, not a closed ring. Past a full turn the swept
                                    # ribbon closes into a tube and reads as a roll of tape;
                                    # short of one, the cross-section is an arc, so no
                                    # complete far ellipse is ever drawn and the tail runs
                                    # up through the gap the way C2's does.
CURL_PHI0   = math.radians(34.0)    # entry on the roll's LOWER flank, the side facing the
                                    # blade, so the tail is C2's short stub instead of the
                                    # long straight chute the old upper-flank entry needed.
                                    # It unwinds anticlockwise on screen from there to a
                                    # free end at the upper left, which is where C2's is.
CURL_BASE_L = (289.0, BLADE_THICK - 22.0)
                                    # where it leaves the blade, in the BLADE's own frame,
                                    # 22 units inside the worn back edge - the same inset
                                    # it has always had, carried onto the deeper top face.
                                    # Derived rather than written out, so a future change of
                                    # face depth cannot leave the shaving emerging from the
                                    # middle of the iron instead of over its back.
                                    # Held in local coords so the pitch carries it: when
                                    # the top face shears, the tail's exit point rides with
                                    # it instead of floating off the metal.
CURL_BASE   = to_top(*CURL_BASE_L)
CURL_SWEEP  = 93.0                  # ribbon width: the measured distance between the two
                                    # fitted rim centres. Against R 115 that is 0.81:1, so
                                    # the two rims overlap heavily, the bore stays open and
                                    # the thing reads as a hoop of shaving seen nearly
                                    # end-on rather than as a cylinder seen along its side.
CURL_TILT   = math.radians(12.9)    # the roll has tipped off the cutting edge, so its axis
                                    # is the blade axis rolled this far toward the vertical:
                                    # 33 + 12.9 = the 45.9 deg the two fitted rim centres
                                    # actually subtend. Derived from the blade frame rather
                                    # than authored on the canvas, so the pitch still owns it.
_CT, _ST    = math.cos(CURL_TILT), math.sin(CURL_TILT)
TUX, TUY    = UX * _CT + UY * _ST, -UX * _ST + UY * _CT
SX, SY      = -TUX * CURL_SWEEP, -TUY * CURL_SWEEP
# The rim the sweep lands on is the one NEARER the viewer, so the roll recedes UP-RIGHT,
# with the ground; the open end faces the viewer and the interior shows on the lower-left.
# That is C2's read, and it is why the shading test below leans against SU rather than with it.

CURL_FORE   = 1.00                  # measured: C2's rims fit CIRCLES, so the section is not
                                    # compressed in the picture plane at all. The tin-can
                                    # read this constant was put in to fight came from the
                                    # sweep being LONGER than the bore, not from the section
                                    # being round; at 0.81 R the bore stays open on its own.

SU = (-TUX, -TUY)                   # the roll's axis, running away from the viewer
SP = (-SU[1], SU[0])                # and its perpendicular, in the picture plane

LIGHT = (-0.36, -0.93)              # the one soft top-left source, mostly overhead


def _fore(dx, dy):
    a = (dx * SU[0] + dy * SU[1]) * CURL_FORE
    b = dx * SP[0] + dy * SP[1]
    return (a * SU[0] + b * SP[0], a * SU[1] + b * SP[1])

OUT_LIT   = (216, 208, 192)         # outer face, square to the light. Was (243, 234, 216),
                                    # which made the lit flank a specular white ribbon the
                                    # material cannot produce: inside the curl's own footprint
                                    # ours read p90 +0.170 and p99 +0.247 above the board
                                    # immediately around it, where C2 reads +0.1165 / +0.1685.
                                    # A shaving is one thickness of the SAME wood as the board,
                                    # under the same one soft key, so its lit face is a little
                                    # brighter than the board and nothing like a highlight.
                                    # Both of C2's ratios come out at 0.68, so the face's excess
                                    # over its board is scaled by that; this triple is solved
                                    # against the rebuilt measurement (p99 +0.168, p90 +0.122),
                                    # not read off a score sweep. The bore's floor is untouched:
                                    # TRANSMIT and CURL_BORE were fitted to C2 in an earlier
                                    # round and measured right.
OUT_DARK  = (134, 118,  97)         # outer face, turned away
IN_LIT    = (198, 180, 156)         # inner face at the mouth of the roll
IN_DARK   = ( 84,  72,  60)         # inner face, deep
TRANSMIT  = (250, 241, 221)         # what comes through thin material from behind

# How much of that gets through. A planed shaving is one thickness of wood, not a
# solid; measured on C2, its loop never falls more than 0.35 L below the ground it
# covers and its bore reads L p10 0.672 / med 0.737 against ground beside the loop
# at 0.727/0.776 - i.e. the inside of its roll sits only 0.05-0.11 under open board.
# Ours was running a mean 0.388 under, because the interior had a hard occlusion
# term and a transmitted term that went to zero exactly where the roll is deepest.
# These three are the light that arrives THROUGH the material, so none of them
# falls off with depth into the roll.
CURL_TRANSMIT = 0.42                # one thickness, key on the far side of the face
CURL_BORE     = 0.54                # the bore is walled by lit shaving on every side
CURL_SHEEN    = 0.22                # ambient pushed through the sheet, key aside


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
        outer = (nx * SU[0] + ny * SU[1]) < 0      # is the outer face the one we see?
        t = i / last
        tap = _taper(t)

        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            # Turned from the key, an outer band is not in shadow - it is backlit,
            # because the key is then on the other side of one thickness of wood.
            col = _lerp(col, TRANSMIT, CURL_SHEEN + CURL_TRANSMIT * max(0.0, -lam))
            op = tap
        else:
            lin = -nx * LIGHT[0] - ny * LIGHT[1]   # lambert on the INNER face
            dux, duy = _unit(mx - CURL_C[0], my - CURL_C[1])
            depth = 0.5 + 0.5 * duy                # 1 at the floor of the roll
            ao = 1.0 - 0.74 * depth                # the roll shades its own interior
            col = _lerp(IN_DARK, IN_LIT, max(0.0, min(1.0, (lin + 0.30) / 1.24)) * ao)
            # ...but it cannot shade it to black: the wall doing the occluding is
            # itself lit and thin, so the bore is floored by what comes through it.
            col = _lerp(col, TRANSMIT, CURL_BORE + CURL_TRANSMIT * max(0.0, lam))
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

  <!-- ROUND 11 - the un-planed field's COORDINATE, not its profile. Round 10 measured
       C2's falloff correctly and then hung it on the wrong geometry: a straight ramp
       along the key's 45deg diagonal. Fit test on C2's own un-planed pixels (bin by a
       candidate coordinate, take the within-bin residual sd; the coordinate that
       explains the field best wins; n=112206 with the block dilated out AND C2's
       translucent curl boxed out, since it reads 0.85-0.95 over 0.70-0.80 ground at
       exactly the radii this ramp is authored from):
           radial about (75,25)   sd 0.02934   <- winner
           best straight ramp 50deg  sd 0.03616
           our authored 45deg        sd 0.03661
       19% less unexplained variance, i.e. C2's key is a POINT SOURCE just off the
       top-left corner, not a plane wave. Attribution control on the render: adopting
       C2's profile while keeping the 45deg axis scores -0.0091; keeping our profile
       and only re-indexing it by r scores +0.0299. The gain is the coordinate.
       Stops are the old field colour at the same distance scaled by target_L/current_L
       (round 10's rule), so every hue survives untouched - the per-knot ratios run
       0.965..1.059 and the colours barely move. What moves is where they sit.
       The trued side stays LINEAR: on C2 its geometry is not strongly determined
       (best radial 0.02389 vs best linear 0.02507) and re-indexing it radially scored
       -0.0219 alone, so it keeps riding the shared axis. -->
  <radialGradient id="roughField" cx="75" cy="25" r="1000" fx="75" fy="25"
                  gradientUnits="userSpaceOnUse">
    <stop offset="0.0000" stop-color="#FFF8E8"/>  <!-- r    0  target L 0.940 -->
    <stop offset="0.0350" stop-color="#F8F1E1"/>  <!-- r   35  target L 0.917 -->
    <stop offset="0.0950" stop-color="#E8E1D2"/>  <!-- r   95  target L 0.865 -->
    <stop offset="0.1550" stop-color="#DBD4C5"/>  <!-- r  155  target L 0.815 -->
    <stop offset="0.2300" stop-color="#C9C3B5"/>  <!-- r  230  target L 0.752 -->
    <stop offset="0.2900" stop-color="#C2BCAC"/>  <!-- r  290  target L 0.718 -->
    <stop offset="0.3500" stop-color="#BAB4A5"/>  <!-- r  350  target L 0.681 -->
    <stop offset="0.4100" stop-color="#B3AC9D"/>  <!-- r  410  target L 0.652 -->
    <stop offset="0.4700" stop-color="#B2AB9B"/>  <!-- r  470  target L 0.650 -->
    <stop offset="0.5300" stop-color="#ACA495"/>  <!-- r  530  target L 0.625 -->
    <stop offset="0.5900" stop-color="#A69F8F"/>  <!-- r  590  target L 0.602 -->
    <stop offset="0.6500" stop-color="#A29B89"/>  <!-- r  650  target L 0.578 -->
    <stop offset="0.7100" stop-color="#A09987"/>  <!-- r  710  target L 0.566  ambient floor -->
    <stop offset="0.8300" stop-color="#A29985"/>  <!-- r  830  target L 0.564 -->
    <stop offset="1.0000" stop-color="#99907B"/>  <!-- r 1000  target L 0.548 -->
  </radialGradient>

  <!-- ROUND 10 - the trued side on the SAME axis, so the finish is a step ON the key's
       ramp rather than a second light. Round 9 recorded C2's ground polarity as
       inverted (its trued 0.610 below its rough 0.642); that was a geometry confound -
       the un-planed plane owns the near-key region and the trued plane the far one.
       Controlled for u, C2's trued plane is BRIGHTER than its rough at matched u
       (+0.076 at u=720). Polarity is not inverted, only its magnitude differs: ours
       was +0.300 at matched u. So the ramp is C2's own measured trued profile times a
       single finish gain g = 1.34. The gain rule was fixed before scoring: the
       smallest gain holding simulated 32px self_contrast >=1.5% above the gate's
       floor (g=1.32 gives 0.605 against a 0.607 floor; g=1.34 gives 0.616). It lands
       measure.py polarity at +0.174, the separation the icon has carried since round 4.
       At 16 and 32px p90 is ~100% this plane and p10 ~100% the block, so a uniform
       drop here is spent straight against that floor - which is how round 5 died. -->
  <linearGradient id="truedField" x1="0" y1="0" x2="{W}" y2="{W}" gradientUnits="userSpaceOnUse">
    <stop offset="0.4558" stop-color="#F6F3EA"/>  <!-- u  660  target L 0.863 -->
    <stop offset="0.5248" stop-color="#F5F1E7"/>  <!-- u  760  target L 0.871 -->
    <stop offset="0.5939" stop-color="#F4EEE3"/>  <!-- u  860  target L 0.869 -->
    <stop offset="0.6629" stop-color="#EFE9DD"/>  <!-- u  960  target L 0.852 -->
    <stop offset="0.7320" stop-color="#EFE9DB"/>  <!-- u 1060  target L 0.848 -->
    <stop offset="0.8010" stop-color="#E8E1D2"/>  <!-- u 1160  target L 0.809 -->
    <stop offset="0.8701" stop-color="#DCD5C5"/>  <!-- u 1260  target L 0.747 -->
    <stop offset="0.9391" stop-color="#D7CFBE"/>  <!-- u 1360  target L 0.700 -->
    <stop offset="0.9999" stop-color="#DDD4C0"/>  <!-- u 1448  target L 0.683 -->
  </linearGradient>

  <!-- ROUND 13. The tear's amplitude down the un-planed plane, one gradient per family
       per flank, in the grain's own frame. Both flanks of a pair take the SAME profile,
       so the pair stays mean-neutral wherever it lands; A and B take different shares
       of it, which is what re-aims the band's lattice along the pass. -->
  {tear_profile("tearAD", GRAIN_DARK, GRAIN_FAM_A)}
  {tear_profile("tearAL", GRAIN_LITE, GRAIN_FAM_A)}
  {tear_profile("tearBD", GRAIN_DARK, GRAIN_FAM_B)}
  {tear_profile("tearBL", GRAIN_LITE, GRAIN_FAM_B)}

  <!-- ROUND 16. The cut's own cross-section, in the local frame: crest, shadowed riser,
       lit arris, trued plane. Measured off C2 at three stations - see the STEP_ block in
       the generator - and carried entirely by these stops, so the four features cannot
       drift out of register with each other. -->
  <linearGradient id="cutStep" gradientUnits="userSpaceOnUse"
                  x1="0" y1="{STEP_UP}" x2="0" y2="{-STEP_DOWN}">{step_stops()}</linearGradient>
  <mask id="cutSwell" maskUnits="userSpaceOnUse"
        x="{STEP_SWELL_LO - 8:.1f}" y="{-STEP_DOWN - 2:.1f}"
        width="{STEP_SWELL_HI - STEP_SWELL_LO + 16:.1f}" height="{STEP_UP + STEP_DOWN + 4:.1f}">
    <linearGradient id="cutSwellRamp" gradientUnits="userSpaceOnUse"
                    x1="{STEP_SWELL_LO:.1f}" y1="0" x2="{STEP_SWELL_HI:.1f}" y2="0">{STEP_SWELL_STOPS}</linearGradient>
    <rect x="{STEP_SWELL_LO - 8:.1f}" y="{-STEP_DOWN - 2:.1f}"
          width="{STEP_SWELL_HI - STEP_SWELL_LO + 16:.1f}" height="{STEP_UP + STEP_DOWN + 4:.1f}"
          fill="url(#cutSwellRamp)"/>
  </mask>


  <!-- top face of the iron: facing the soft top-left light. ROUND 7 - the intent here
       was always "warm-leaning graphite, not blue steel", but the constants never said
       so: the old ramp ran #2E3238 -> #5D636B, every stop with B ten points above R, and
       the rendered face measured a flat cool cast (sat 0.13-0.15, B>R) end to end.
       Measured off C2: its top face is NEUTRAL through the body (sat 0.004-0.04) and
       drifts WARM at the back edge (0.319,0.311,0.302 -> 0.378,0.354,0.332) where the
       timber bounces up into it. The LUMINANCE ramp below is unchanged to within 0.01
       at every stop - only the hue moves - so this isolates the cast from the modelling. -->
  <!-- ROUND 9. The hue was right and the VALUE was not. Sampled as a cross-section
       perpendicular to each block's own hone, at five stations along the length: the
       front face matches C2 to within 0.05 over its whole body (depths 20-56px), and
       the top face runs +0.05 to +0.14 too light at EVERY station (depths 72-190px).
       Face means: ours 0.338, C2's 0.243. Its across-depth ramp was overdone too -
       ours climbed +0.101 from hone edge to back edge where C2's climbs +0.068 - so
       the face read as moulded plastic catching a broad sheen rather than as stone.
       The stops below are the old ramp under L' = 0.245 + 0.70*(L - 0.338), which
       lands the rendered face on 0.215 -> 0.283 across depth: C2's own two numbers.
       The dark end is no longer near-neutral. C2's darkest 3% of top face is
       (0.173,0.145,0.131), sat 0.240; ours was sat 0.110 - the face was desaturating
       into shadow, which is the thing round 1 caught on the ground and this face had
       kept doing. The offset-0 stop IS that measured colour, scaled to its own L. -->
  <linearGradient id="topFace" x1="0" y1="0" x2="0" y2="{BLADE_THICK}" gradientUnits="userSpaceOnUse"
                  gradientTransform="{MATRIX_TOP}">
    <stop offset="0" stop-color="#2A2420"/>
    <stop offset="0.34" stop-color="#39312E"/>
    <stop offset="0.78" stop-color="#423D3A"/>
    <stop offset="1" stop-color="#494542"/>
  </linearGradient>

  <!-- a soft sheen where the top-left light lands hardest on the top face. Was a cool
       #CBD5E2 at 0.25 and too tight: it swung the top face 1.63:1 ALONG its length,
       where C2's swings only 1.24:1 - a spotlight on a plane rather than stone. Warmer,
       weaker and broader, so the face's volume comes from its across-depth ramp.
       ROUND 9: 0.13 -> 0.06. Measured in the block's own frame the swing was still
       1.35:1 against C2's 1.13:1, and on a face this dark the same opacity reads as a
       bigger step than it did before. Nearly all of this face's modelling should be
       the across-depth ramp; almost none of it should be a bright spot. -->
  <radialGradient id="topSheen" cx="0.32" cy="0.70" r="0.86">
    <stop offset="0" stop-color="#DED9CD" stop-opacity="0.06"/>
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

  <filter id="castShadow" x="-45%" y="-45%" width="190%" height="190%">
    <feGaussianBlur stdDeviation="{CAST_BLUR}"/>
  </filter>
  <filter id="haloShadow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="{HALO_BLUR}"/>
  </filter>
  <filter id="contactShadow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="{CONTACT_BLUR}"/>
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
  <filter id="hemBlur" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.5"/>
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

    <!-- ROUND 16. The cut is a STEP, not a colour change: a shaving's thickness of
         timber has gone. Sixteen local units of band, one paint, drawn over the grain
         because an arris is geometry and the tear does not cross it - and drawn UNDER
         the block's shadows, which fall across the step as they should. -->
    <g transform="{MATRIX}"><g mask="url(#cutSwell)">
      <path d="M{LX_MIN:.1f} {STEP_UP} H{LX_MAX:.1f} V{-STEP_DOWN} H{LX_MIN:.1f} Z"
            fill="url(#cutStep)"/>
    </g></g>

    <!-- the solid's own shadow, from the one soft top-left light: a wide weak tail,
         a deep soft cast, plus a tight occlusion where it actually touches down -->
    <g filter="url(#haloShadow)">
      <path d="{poly([(x + HALO_DX, y + HALO_DY) for x, y in SILHOUETTE])}" fill="#4B4133" fill-opacity="{HALO_OP}"/>
    </g>
    <g filter="url(#castShadow)">
      <path d="{poly([(x + CAST_DX, y + CAST_DY) for x, y in SILHOUETTE])}" fill="#4B4133" fill-opacity="{CAST_OP}"/>
    </g>
    <g filter="url(#contactShadow)">
      <path d="{poly([(x + CONTACT_DX, y + CONTACT_DY) for x, y in SILHOUETTE])}" fill="#3C3327" fill-opacity="{CONTACT_OP}"/>
    </g>
    <g clip-path="url(#roughSide)" filter="url(#hemBlur)">
      <path d="{open_poly(CHAIN_UPPER)}" fill="none" stroke="#332A1E" stroke-opacity="0.65"
            stroke-width="8.0" stroke-linecap="round"/>
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
    <!-- wear on the back: two faint grind striations, on the top face. Opacities halved
         with the face: at 0.16 over a base of 0.245 they would read as a LARGER step
         than they did over 0.338, and the round's whole point is that this face is
         quieter than we had it. Same rule for the sheen and the rim above and below. -->
    <g transform="{MATRIX_TOP}" fill="none">
      <path d="M 78 122 L {BLADE_LEN - 98:.0f} 122" stroke="#9A9285" stroke-opacity="0.08" stroke-width="3"/>
      <path d="M 128 100 L {BLADE_LEN - 152:.0f} 100" stroke="#9A9285" stroke-opacity="0.045" stroke-width="2"/>
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
         is WARM (0.378,0.354,0.332), lit by bounce off the timber behind. ROUND 9: 0.52
         -> 0.30, because the face it sits on dropped to 0.281 at the back edge. C2's
         top face peaks at 0.389 in its brightest 3%; ours peaked at 0.487. 0.30 is the
         opacity that puts this rim on 0.389, so the peak is measured, not tuned. -->
    <path d="M 46 {BLADE_THICK - 2:.0f} C {BLADE_LEN * 0.34:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN * 0.66:.0f} {BLADE_THICK - 10:.0f} {BLADE_LEN - 36:.0f} {BLADE_THICK - 2:.0f}"
          transform="{MATRIX_TOP}" stroke="#ABA294" stroke-opacity="0.30" stroke-width="5"
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
