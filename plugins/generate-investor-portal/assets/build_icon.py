#!/usr/bin/env python3
"""Build the generate-investor-portal icon master — "The Strongroom, Open".

Geometry and material live here as named constants so a later round is a
parameter edit rather than path surgery.

Device (subject-mined from the skill, not from a category)
---------------------------------------------------------
The skill generates one validated record and refuses the write until a gate has
read it back: nothing is published until it is held and proven, and what is held
is shown. So the tile is the porcelain wall of a disclosure room. A portal is
cast into it with a real reveal, and the graphite door stands swung inward — its
outer face foreshortened, its hub and keyway visible, its leading edge warmed by
the light behind it. Inside, one pale record slab stands raked by that light.

Signature move: the accent is spent only as interior light. It lands on the
door's leading edge, on the record's lit face and right edge, on the sill, and
as a scatter on the porcelain just outside the opening — nowhere else. The room
is otherwise dark, which is the other half of the claim: what is held is lit,
and what is not held is simply absent rather than invented.

Light model: one soft exterior key from the top, slightly left (the family's own
convention: ground radial near 0.44/0.28, shadows dx +6 dy +16), plus the one
sanctioned second light — the emissive interior (Tahoe grammar #6).

Values sampled off `apple-2026/apple-12.png` (Calculator: porcelain cushion +
one dark satin body + warm accent, Apple's own take on this register) and
`apple-31.png` (News):

    tile above the body        L 0.874      brightest point, near the key
    tile below the body        L 0.674      the vignette's depth
    body interior             L 0.120      a dark satin mass on porcelain
    body edge facing the key   L 0.365      the rim catch, ~3x the body
    body edge away             L 0.214      shaded flank, still above the tile's floor
    cast shadow beside body    L 0.446      deep, and warm-neutral rather than blue
    amber key                  #FF941B      H 32, S 0.89, V 1.00 — the accent is BRIGHT
    News coral gel             L 0.471, S 0.63

Two of those changed the build: the accent's hot core is authored near V 1.0
rather than at the family accent's own value (vibrancy is emission, not
saturation), and every shadow is warm-neutral because nothing in this scene
emits cool light.

    python3 build_icon.py            # writes icon.svg beside this file
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---------------------------------------------------------------- light
# One key light, one axis. Every porcelain and graphite ramp hangs on this
# segment in userSpaceOnUse, so the multi-material scene is coherent by
# construction rather than by eye (material-recipes: "one key, one axis").
KEY = ((150, 40), (900, 990))
GROUND_CX, GROUND_CY = 0.44, 0.28      # the family's own ground centre
SHADOW_DX, SHADOW_DY = 6, 16           # the family's own shadow vector

# ---------------------------------------------------------------- ground
# The family triad, unchanged: every sibling porcelain tile uses these three.
GROUND_HI = "#FDFCFA"
GROUND_MID = "#EFECE5"
GROUND_LO = "#D8D3C9"
RIM_LIGHT = "#FFFFFF"

# ---------------------------------------------------------------- the opening
# 55% x 66% of the tile, optically centred 8px above the geometric centre so the
# dark mass does not read as sitting low.
OP_X, OP_Y, OP_W, OP_H, OP_R = 228, 166, 568, 676, 46
REVEAL = 22                            # the wall's cut depth, visible as four faces
RM_X, RM_Y = OP_X + REVEAL, OP_Y + REVEAL
RM_W, RM_H, RM_R = OP_W - 2 * REVEAL, OP_H - 2 * REVEAL, 32

# The reveal's four faces. A recess lit from above shows a dark soffit and a lit
# sill; the jambs sit between. Porcelain a step down from the wall's front face,
# because a cut face in the same material is darker, not a different colour.
REV_SOFFIT = "#6F6A62"
REV_SOFFIT_LO = "#524E47"
REV_SILL_HI = "#E3DED4"
REV_SILL_LO = "#BAB4AA"
REV_JAMB_L = "#8F8A82"                 # in shadow: its face turns away from the key
REV_JAMB_R = "#C6C1B8"                 # lit by the key AND by the room, so it is the bright one
REV_LIP = "#FFFDF8"                    # the eased outer lip, catching the key

# ---------------------------------------------------------------- the room
ROOM_HI = "#262B31"                    # near the sill, where the bounce reaches
ROOM_LO = "#080A0C"                    # under the soffit
ROOM_FLOOR = "#141920"
FLOOR_Y = 762                          # where the room's floor meets its back

# ---------------------------------------------------------------- the door
# Hinged on the left jamb, swung inward. The near edge sits in the wall plane at
# full height; the leading edge is deeper into the room, so it converges on the
# opening's own centre. FAR_SHRINK is that convergence, and EDGE_* is the door's
# thickness seen from the right — the surface the interior light actually hits.
DOOR_NEAR_X = RM_X
DOOR_FAR_X = 474
DOOR_FAR_SHRINK = 0.755
DOOR_EDGE_X = 514
DOOR_EDGE_SHRINK = 0.715
DOOR_FACE_HI = "#5A6270"               # near the key
DOOR_FACE_LO = "#343A44"               # away from it
DOOR_EDGE_HI = "#6A7280"
DOOR_EDGE_LO = "#414852"
DOOR_CORNER = 30                       # the slab's rounding on its leading corners
DOOR_TOP_CATCH = "#C4CAD4"             # rim catch on the door's top edge
HUB_HI, HUB_LO = "#78818E", "#33394200"[:7]
HUB_RING = "#6E7681"
WHEEL_HI = "#9AA3B0"                    # the wheel's own lit value
HINGE_HI, HINGE_LO = "#565E69", "#2A2F36"
KEYWAY = "#14171B"
BOLT_HI, BOLT_LO = "#6E7783", "#2B3038"

# ---------------------------------------------------------------- the record
# One slab, standing on the room's floor, raked from the right. Porcelain, so it
# belongs to the wall's material rather than being a foreign white.
REC_X, REC_Y, REC_W, REC_H, REC_R = 552, 508, 138, 240, 10
REC_EDGE_W = 16                        # its own thickness, on the lit side
REC_LEAN = -2.8                        # degrees: a plate leans, a book stands
REC_FACE_HI = "#F2EDE2"
REC_FACE_LO = "#B9B2A3"
REC_EDGE = "#FFE2C2"                   # the edge nearest the emitter
REC_TOP = "#FFFFFF"

# ---------------------------------------------------------------- the ember
# The one accent, and it is a light source rather than a fill. Kin to the
# family's #E8542A, with a hot core authored near V 1.0 — apple-12's amber key
# measures V 1.00, and a filled shape at the accent's own value reads as paint.
#
# Sized on the shelf rather than in the reference: the first draft ran EMIT_R at
# 300 and filled the right half of the room, which reads as a furnace at 1024 and
# as an orange blob at 32. The dark mass is what carries small-size contrast; the
# accent only has to be the brightest thing, not the biggest.
EMBER_CORE = "#FFD8A6"
EMBER_HOT = "#FA9247"
EMBER = "#E8542A"
EMBER_DEEP = "#B33B14"
EMIT_CX, EMIT_CY = 802, 452            # deeper in the room, past its right edge
EMIT_R = 268

# ---------------------------------------------------------------- shadows
# Warm-neutral, never blue: nothing in this scene emits cool light.
CONTACT = "#6B5C46"
AO = "#5A4C39"


def rr(x, y, w, h, r):
    """Rounded rectangle as one path."""
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r}z')


def quad(pts):
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = pts
    return f'M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f} L{cx:.1f},{cy:.1f} L{dx:.1f},{dy:.1f}z'


def quad_r(pts, radii):
    """A quadrilateral with a per-corner radius, as one path.

    A slab with sharp corners reads as a cut-out; the raster take that won the
    material judgment rounds every edge of the door. Each corner is trimmed by
    `r` along both of its edges and bridged with a quadratic through the corner
    itself, which is the cheapest rounding that survives an oblique quad.
    """
    n = len(pts)
    out = []
    for i in range(n):
        px, py = pts[(i - 1) % n]
        cx, cy = pts[i]
        nx, ny = pts[(i + 1) % n]
        r = radii[i]
        if r <= 0:
            out.append(("L" if out else "M", cx, cy))
            continue
        for (ax, ay), tag in (((px, py), "in"), ((nx, ny), "out")):
            dx, dy = ax - cx, ay - cy
            ln = max((dx * dx + dy * dy) ** 0.5, 1e-6)
            k = min(r / ln, 0.48)
            if tag == "in":
                ix, iy = cx + dx * k, cy + dy * k
            else:
                ox, oy = cx + dx * k, cy + dy * k
        out.append(("L" if out else "M", ix, iy))
        out.append(("Q", cx, cy, ox, oy))
    d = ""
    for seg in out:
        if seg[0] == "Q":
            d += f'Q{seg[1]:.1f},{seg[2]:.1f} {seg[3]:.1f},{seg[4]:.1f} '
        else:
            d += f'{seg[0]}{seg[1]:.1f},{seg[2]:.1f} '
    return d.strip() + "z"


def far_edge(shrink):
    """The y-range of a vertical edge pushed back into the room by `shrink`.

    One function, so the door's leading edge and its thickness face converge on
    the same centre and cannot drift apart later.
    """
    cy = RM_Y + RM_H / 2
    half = (RM_H / 2) * shrink
    return cy - half, cy + half


def build() -> str:
    parts: list[str] = []
    add = parts.append

    (kx1, ky1), (kx2, ky2) = KEY
    d_top, d_bot = far_edge(DOOR_FAR_SHRINK)
    e_top, e_bot = far_edge(DOOR_EDGE_SHRINK)
    rec_e_top = REC_Y + 11
    rec_e_bot = REC_Y + REC_H - 6

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ------------------------------------------------------------------ defs
    add('<defs>')
    add(f'''<radialGradient id="ground" cx="{GROUND_CX}" cy="{GROUND_CY}" r="0.74">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.5" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </radialGradient>''')
    # Every material ramp below shares this one axis.
    for name, hi, lo in (("doorface", DOOR_FACE_HI, DOOR_FACE_LO),
                         ("dooredge", DOOR_EDGE_HI, DOOR_EDGE_LO),
                         ("recface", REC_FACE_HI, REC_FACE_LO),
                         ("sill", REV_SILL_HI, REV_SILL_LO),
                         ("soffit", REV_SOFFIT_LO, REV_SOFFIT),
                         ("hub", HUB_HI, HUB_LO),

                         ("bolt", BOLT_HI, BOLT_LO)):
        add(f'''<linearGradient id="{name}" gradientUnits="userSpaceOnUse"
          x1="{kx1}" y1="{ky1}" x2="{kx2}" y2="{ky2}">
          <stop offset="0" stop-color="{hi}"/><stop offset="1" stop-color="{lo}"/>
        </linearGradient>''')
    add(f'''<linearGradient id="hinge" gradientUnits="userSpaceOnUse"
      x1="{DOOR_NEAR_X - 16}" y1="0" x2="{DOOR_NEAR_X + 16}" y2="0">
      <stop offset="0" stop-color="{HINGE_HI}"/><stop offset="1" stop-color="{HINGE_LO}"/>
    </linearGradient>''')
    # The room: darkest under the soffit, lifting toward the sill where the
    # interior light bounces off the floor.
    add(f'''<linearGradient id="room" gradientUnits="userSpaceOnUse"
      x1="{RM_X}" y1="{RM_Y}" x2="{RM_X + 90}" y2="{RM_Y + RM_H}">
      <stop offset="0" stop-color="{ROOM_LO}"/>
      <stop offset="0.62" stop-color="{ROOM_FLOOR}"/>
      <stop offset="1" stop-color="{ROOM_HI}"/>
    </linearGradient>''')
    # The emitter. One radial, used by the light itself, its bloom and every
    # surface it lights, so they cannot drift apart.
    add(f'''<radialGradient id="emit" gradientUnits="userSpaceOnUse"
      cx="{EMIT_CX}" cy="{EMIT_CY}" r="{EMIT_R}">
      <stop offset="0" stop-color="{EMBER_CORE}"/>
      <stop offset="0.17" stop-color="{EMBER_HOT}"/>
      <stop offset="0.46" stop-color="{EMBER}" stop-opacity="0.78"/>
      <stop offset="1" stop-color="{EMBER_DEEP}" stop-opacity="0"/>
    </radialGradient>''')
    add(f'''<radialGradient id="bloom" gradientUnits="userSpaceOnUse"
      cx="{EMIT_CX}" cy="{EMIT_CY}" r="{EMIT_R + 150}">
      <stop offset="0" stop-color="{EMBER_HOT}" stop-opacity="0.34"/>
      <stop offset="0.45" stop-color="{EMBER}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
    </radialGradient>''')
    # Scatter on the porcelain outside the opening: light escaping a real
    # aperture lands on the wall around it, and this is the cue that says the
    # ember is a source rather than a painted shape.
    add(f'''<radialGradient id="scatter" gradientUnits="userSpaceOnUse"
      cx="{EMIT_CX - 30}" cy="{FLOOR_Y + 30}" r="330">
      <stop offset="0" stop-color="{EMBER_HOT}" stop-opacity="0.22"/>
      <stop offset="0.5" stop-color="{EMBER}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
    </radialGradient>''')
    # The bounce that warms the door's leading edge — the accent's whole job.
    add(f'''<linearGradient id="edgebounce" gradientUnits="userSpaceOnUse"
      x1="{DOOR_EDGE_X}" y1="{e_top}" x2="{DOOR_EDGE_X}" y2="{e_bot}">
      <stop offset="0" stop-color="{EMBER}" stop-opacity="0.12"/>
      <stop offset="0.42" stop-color="{EMBER_HOT}" stop-opacity="0.88"/>
      <stop offset="0.78" stop-color="{EMBER}" stop-opacity="0.52"/>
      <stop offset="1" stop-color="{EMBER_DEEP}" stop-opacity="0.20"/>
    </linearGradient>''')
    # The record's lit face: warm at the emitter's side, falling away to the left.
    add(f'''<linearGradient id="recwarm" gradientUnits="userSpaceOnUse"
      x1="{REC_X + REC_W}" y1="{REC_Y}" x2="{REC_X - 34}" y2="{REC_Y + REC_H}">
      <stop offset="0" stop-color="{EMBER_CORE}" stop-opacity="0.52"/>
      <stop offset="0.4" stop-color="{EMBER_HOT}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="facebounce" gradientUnits="userSpaceOnUse"
      x1="0" y1="{RM_Y + RM_H}" x2="0" y2="{RM_Y + RM_H - 190}">
      <stop offset="0" stop-color="{REV_SILL_HI}" stop-opacity="0.20"/>
      <stop offset="0.55" stop-color="{REV_SILL_LO}" stop-opacity="0.07"/>
      <stop offset="1" stop-color="{REV_SILL_LO}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="tilerim" gradientUnits="userSpaceOnUse"
      x1="0" y1="0" x2="0" y2="{S}">
      <stop offset="0" stop-color="{RIM_LIGHT}" stop-opacity="0.60"/>
      <stop offset="0.45" stop-color="{RIM_LIGHT}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{RIM_LIGHT}" stop-opacity="0.24"/>
    </linearGradient>''')
    add(f'''<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.62" stop-color="{AO}" stop-opacity="0"/>
      <stop offset="1" stop-color="{AO}" stop-opacity="0.17"/>
    </radialGradient>''')
    add(f'''<linearGradient id="topcatch" gradientUnits="userSpaceOnUse"
      x1="{DOOR_NEAR_X}" y1="0" x2="{DOOR_EDGE_X}" y2="0">
      <stop offset="0" stop-color="{DOOR_TOP_CATCH}" stop-opacity="0.30"/>
      <stop offset="0.45" stop-color="{DOOR_TOP_CATCH}" stop-opacity="0.82"/>
      <stop offset="1" stop-color="{DOOR_TOP_CATCH}" stop-opacity="0.22"/>
    </linearGradient>''')

    add(f'<filter id="soft" x="-45%" y="-45%" width="190%" height="190%">'
        f'<feGaussianBlur stdDeviation="26"/></filter>')
    add(f'<filter id="softer" x="-60%" y="-60%" width="220%" height="220%">'
        f'<feGaussianBlur stdDeviation="52"/></filter>')
    add(f'<filter id="tight" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feGaussianBlur stdDeviation="9"/></filter>')
    add(f'<filter id="doorcast" x="-30%" y="-30%" width="180%" height="180%">'
        f'<feDropShadow dx="{SHADOW_DX + 8}" dy="{SHADOW_DY}" stdDeviation="22" '
        f'flood-color="{CONTACT}" flood-opacity="0.55"/></filter>')

    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add(f'<clipPath id="roomclip"><path d="{rr(RM_X, RM_Y, RM_W, RM_H, RM_R)}"/></clipPath>')
    add(f'<clipPath id="openclip"><path d="{rr(OP_X, OP_Y, OP_W, OP_H, OP_R)}"/></clipPath>')
    add('</defs>')

    # Everything inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ============================================================ bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vignette)"/>')
    add('</g>')

    # ============================================================ mid
    add('<g id="mid">')

    # The wall's own ambient occlusion around a recess: a soft dark halo away
    # from the key, so the opening reads as cut into the tile rather than drawn
    # on it.
    add(f'<g filter="url(#soft)" opacity="0.17">'
        f'<path d="{rr(OP_X + 10, OP_Y + 16, OP_W, OP_H, OP_R)}" fill="{AO}"/></g>')

    # Light escaping onto the porcelain below the opening. Painted before the
    # reveal so the reveal's lit lip stays on top of it.
    add(f'<rect x="{OP_X - 200}" y="{OP_Y + OP_H - 320}" width="{OP_W + 400}" '
        f'height="520" fill="url(#scatter)"/>')

    # The reveal: four cut faces of the same porcelain, a step down in value.
    add(f'<path d="{rr(OP_X, OP_Y, OP_W, OP_H, OP_R)}" fill="url(#sill)"/>')
    add(f'<g clip-path="url(#openclip)">')
    add(f'<path d="M{OP_X},{OP_Y} h{OP_W} v{REVEAL + 22} h{-OP_W}z" fill="url(#soffit)"/>')
    add(f'<path d="M{OP_X},{OP_Y} v{OP_H} h{REVEAL + 3} v{-OP_H}z" '
        f'fill="{REV_JAMB_L}" fill-opacity="0.92"/>')
    add(f'<path d="M{OP_X + OP_W},{OP_Y} v{OP_H} h{-(REVEAL + 3)} v{-OP_H}z" '
        f'fill="{REV_JAMB_R}" fill-opacity="0.9"/>')
    # The sill catches the interior light — the one place the escape is literal.
    add(f'<path d="M{OP_X},{OP_Y + OP_H - REVEAL - 20} h{OP_W} v{REVEAL + 20} h{-OP_W}z" '
        f'fill="url(#sill)"/>')
    add(f'<path d="M{OP_X},{OP_Y + OP_H - REVEAL - 20} h{OP_W} v{REVEAL + 20} h{-OP_W}z" '
        f'fill="url(#scatter)" opacity="0.9"/>')
    add('</g>')

    # The room itself.
    add(f'<path d="{rr(RM_X, RM_Y, RM_W, RM_H, RM_R)}" fill="url(#room)"/>')

    add('<g clip-path="url(#roomclip)">')
    # The soffit's cast shadow on the back of the room.
    add(f'<rect x="{RM_X}" y="{RM_Y}" width="{RM_W}" height="120" fill="{ROOM_LO}" '
        f'opacity="0.85" filter="url(#tight)"/>')
    # The emitter: the interior light itself, plus its bloom.
    add(f'<rect x="{RM_X}" y="{RM_Y}" width="{RM_W}" height="{RM_H}" fill="url(#bloom)"/>')
    add(f'<circle cx="{EMIT_CX}" cy="{EMIT_CY}" r="{EMIT_R}" fill="url(#emit)" '
        f'opacity="0.92"/>')
    # The floor, and the bounce along it.
    add(f'<rect x="{RM_X}" y="{FLOOR_Y}" width="{RM_W}" height="{RM_Y + RM_H - FLOOR_Y}" '
        f'fill="{ROOM_FLOOR}" opacity="0.72"/>')
    add(f'<rect x="{RM_X}" y="{FLOOR_Y - 6}" width="{RM_W}" height="{RM_Y + RM_H - FLOOR_Y + 6}" '
        f'fill="url(#scatter)" opacity="0.6"/>')

    # The record: one slab standing on the floor, raked from the right.
    add(f'<ellipse cx="{REC_X + REC_W / 2 + 14}" cy="{FLOOR_Y + 8}" rx="{REC_W * 0.72}" '
        f'ry="19" fill="{CONTACT}" opacity="0.62" filter="url(#tight)"/>')
    add(f'<g transform="rotate({REC_LEAN} {REC_X + REC_W / 2:.1f} {REC_Y + REC_H:.1f})">')
    rec_edge = quad(((REC_X + REC_W, REC_Y),
                     (REC_X + REC_W + REC_EDGE_W, rec_e_top),
                     (REC_X + REC_W + REC_EDGE_W, rec_e_bot),
                     (REC_X + REC_W, REC_Y + REC_H)))
    add(f'<path d="{rec_edge}" fill="{REC_EDGE}" fill-opacity="0.93"/>')
    rec_top = quad(((REC_X + REC_R * 0.6, REC_Y), (REC_X + REC_W, REC_Y),
                    (REC_X + REC_W + REC_EDGE_W, rec_e_top),
                    (REC_X + REC_R * 0.6 + REC_EDGE_W, rec_e_top)))
    add(f'<path d="{rec_top}" fill="{REC_TOP}" fill-opacity="0.5"/>')
    add(f'<path d="{rr(REC_X, REC_Y, REC_W, REC_H, REC_R)}" fill="url(#recface)"/>')
    add(f'<path d="{rr(REC_X, REC_Y, REC_W, REC_H, REC_R)}" fill="url(#recwarm)"/>')
    add(f'<path d="M{REC_X + REC_R},{REC_Y + 3} h{REC_W - 2 * REC_R}" fill="none" '
        f'stroke="{REC_TOP}" stroke-width="5" stroke-opacity="0.85" stroke-linecap="round"/>')
    add('</g>')
    add('</g>')
    add('</g>')  # /mid

    # ============================================================ fg
    #
    # Three things here came out of the Engine C raster, which independently
    # produced this composition from the same spec and beat the master on
    # material: the door is a rounded slab rather than a sharp quad, its hinge
    # edge carries two barrel hinges, and the handwheel is a modelled torus
    # rather than a stroked ellipse. All three are physical features the object
    # would actually have — which is the thing that separates an object that was
    # observed from one that was constructed.
    add('<g id="fg">')
    door_face = quad_r(((DOOR_NEAR_X, RM_Y), (DOOR_FAR_X, d_top),
                        (DOOR_FAR_X, d_bot), (DOOR_NEAR_X, RM_Y + RM_H)),
                       (10, DOOR_CORNER, DOOR_CORNER, 10))
    # One solid silhouette for the whole slab, so the face and its thickness
    # cannot leave a gap at the rounded corner.
    door_solid = quad_r(((DOOR_NEAR_X, RM_Y), (DOOR_EDGE_X, e_top),
                         (DOOR_EDGE_X, e_bot), (DOOR_NEAR_X, RM_Y + RM_H)),
                        (10, DOOR_CORNER, DOOR_CORNER, 10))
    door_lead = quad_r(((DOOR_FAR_X, d_top), (DOOR_EDGE_X, e_top),
                        (DOOR_EDGE_X, e_bot), (DOOR_FAR_X, d_bot)),
                       (0, DOOR_CORNER, DOOR_CORNER, 0))

    # The hinges, standing proud into the reveal on the hinge side.
    for t in (0.17, 0.83):
        hy = RM_Y + RM_H * t
        add(f'<path d="{rr(DOOR_NEAR_X - 15, hy - 44, 30, 88, 14)}" fill="url(#hinge)"/>')
        add(f'<path d="M{DOOR_NEAR_X - 10},{hy - 31} v62" fill="none" stroke="{HUB_RING}" '
            f'stroke-width="4" stroke-opacity="0.42" stroke-linecap="round"/>')

    add('<g filter="url(#doorcast)">')
    add(f'<path d="{door_solid}" fill="url(#dooredge)"/>')
    add('</g>')
    # The leading edge — the door's own thickness, seen from the lit side.
    add(f'<path d="{door_lead}" fill="url(#dooredge)"/>')
    add(f'<path d="{door_lead}" fill="url(#edgebounce)"/>')
    add(f'<path d="{door_face}" fill="url(#doorface)"/>')
    add(f'<path d="{door_face}" fill="url(#facebounce)"/>')

    # The handwheel: the one physical feature that makes this a strongroom door
    # rather than a room door. Foreshortened with the face — an ellipse with
    # three spokes, not a circle laid on top of it, because a concentric
    # primitive is the tell of an object constructed rather than observed. The
    # first draft drew a hub with a rounded slot in it and read as a house
    # keyhole, which is a different product's icon.
    hub_cx = DOOR_NEAR_X + (DOOR_FAR_X - DOOR_NEAR_X) * 0.46
    hub_cy = RM_Y + RM_H / 2
    hub_rx, hub_ry = 44, 108
    # A torus needs a dark side and a lit side; one stroke is a decal. The wheel
    # also sits proud of the face, so it occludes it.
    add(f'<ellipse cx="{hub_cx + 5:.1f}" cy="{hub_cy + 9:.1f}" rx="{hub_rx + 7}" '
        f'ry="{hub_ry + 7}" fill="none" stroke="{KEYWAY}" stroke-width="18" '
        f'stroke-opacity="0.34" filter="url(#tight)"/>')
    for dx, dy in ((0, -1), (0.92, 0.5), (-0.92, 0.5)):
        add(f'<path d="M{hub_cx:.1f},{hub_cy:.1f} l{dx * (hub_rx - 4):.1f},'
            f'{dy * (hub_ry - 6):.1f}" stroke="{HUB_LO}" stroke-width="15" '
            f'stroke-linecap="round"/>')
        add(f'<path d="M{hub_cx - 2:.1f},{hub_cy - 3:.1f} l{dx * (hub_rx - 6):.1f},'
            f'{dy * (hub_ry - 9):.1f}" stroke="{WHEEL_HI}" stroke-width="9" '
            f'stroke-opacity="0.9" stroke-linecap="round"/>')
    add(f'<ellipse cx="{hub_cx:.1f}" cy="{hub_cy:.1f}" rx="{hub_rx}" ry="{hub_ry}" '
        f'fill="none" stroke="{HUB_LO}" stroke-width="19"/>')
    add(f'<ellipse cx="{hub_cx - 2:.1f}" cy="{hub_cy - 4:.1f}" rx="{hub_rx}" ry="{hub_ry}" '
        f'fill="none" stroke="{WHEEL_HI}" stroke-width="11" stroke-opacity="0.92"/>')
    add(f'<ellipse cx="{hub_cx:.1f}" cy="{hub_cy:.1f}" rx="19" ry="29" fill="{HUB_LO}"/>')
    add(f'<ellipse cx="{hub_cx - 2:.1f}" cy="{hub_cy - 3:.1f}" rx="15" ry="23" '
        f'fill="{WHEEL_HI}" fill-opacity="0.88"/>')

    # Two dogging bolts, on the face, following the same foreshortening.
    # Their values are their own, not the scene ramp's: hung on the shared key axis
    # the lower bolt's body landed at the ramp's dark end, so its offset shadow was
    # the only thing that rendered and the bolt read as a crescent.
    for t in (0.2, 0.8):
        by = RM_Y + 46 + (RM_H - 92) * t
        bx = DOOR_NEAR_X + (DOOR_FAR_X - DOOR_NEAR_X) * 0.80
        add(f'<ellipse cx="{bx + 3:.1f}" cy="{by + 5:.1f}" rx="14" ry="21" fill="{KEYWAY}" '
            f'fill-opacity="0.34"/>')
        add(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="13" ry="20" fill="{BOLT_LO}"/>')
        add(f'<ellipse cx="{bx - 1.5:.1f}" cy="{by - 2:.1f}" rx="10" ry="16" fill="{BOLT_HI}" '
            f'fill-opacity="0.92"/>')
    add('</g>')  # /fg

    # ============================================================ highlight
    add('<g id="highlight">')
    # The reveal's eased outer lip, catching the key along the top and left.
    add(f'<path d="M{OP_X + OP_R},{OP_Y + 3} h{OP_W - 2 * OP_R}" fill="none" '
        f'stroke="{REV_LIP}" stroke-width="4" stroke-opacity="0.45" stroke-linecap="round"/>')
    add(f'<path d="M{OP_X + 3},{OP_Y + OP_R} v{OP_H - 2 * OP_R - 60}" fill="none" '
        f'stroke="{REV_LIP}" stroke-width="4" stroke-opacity="0.28" stroke-linecap="round"/>')
    # The door's top edge catch.
    add(f'<path d="M{DOOR_NEAR_X + 4},{RM_Y + 4} L{DOOR_FAR_X - 3},{d_top + 4}" fill="none" '
        f'stroke="url(#topcatch)" stroke-width="7" stroke-linecap="round"/>')
    # The bloom over everything inside the room, so the light reads emissive
    # rather than as a coloured region.
    add(f'<g clip-path="url(#roomclip)">'
        f'<circle cx="{EMIT_CX}" cy="{EMIT_CY}" r="{EMIT_R - 60}" fill="url(#bloom)" '
        f'filter="url(#softer)"/></g>')
    # The tile's own cushion rim.
    add(f'<path d="{SQUIRCLE.read_text().strip()}" fill="none" stroke="url(#tilerim)" '
        f'stroke-width="4"/>')
    add('</g>')

    add('</g>')  # /tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(build())
    print(f"wrote {out}")
