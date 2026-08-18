#!/usr/bin/env python3
"""Build the mac-craft icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

    python3 build_icon.py            # writes icon.svg beside this file

THE SUBJECT — "The Registered Line"
-----------------------------------
A joiner's marking gauge registered on the outer edge of a small glazed sash,
having scribed one line parallel to that edge.

mac-craft's thesis is that a value in a token table carries where it came from:
`(specified)(canon)` is not interchangeable with `(estimated)(inferred)`, and
dropping a mark is how a single-surface guess becomes a platform value one file
downstream. A scribed line is the physical form of that idea. Its position is
not chosen — the stock is pressed against the reference face and the pin cuts
where the beam says, so the mark is a *consequence of the registration*. Slide
the stock off the edge and the line means nothing.

SIGNATURE MOVE: the stock is clamped hard on the sash's outer edge, over the
porcelain, and the scribed line runs parallel to that edge inside the member.
The line's parallelism is the whole read — it is the only straight vermilion in
the tile and it is derived, not placed.

Not a plain window with traffic lights: the sash is a mitred physical frame
lying on a bench, worked on rather than depicted. No dots, no ruler
graduations, no chrome band.

MEASURED VALUES (nothing here was assumed)
------------------------------------------
Ground truth, `create-mac-icon/references/corpus/apple-2026/`:
  apple-18 (porcelain + toy object) — ground L 0.993 at frac (0.33, 0.00)
    falling to 0.923 at the bottom edge: a NARROW, HIGH ramp of ~0.07 L, not
    the cream 0.94/0.83 pair the predecessor used.
  apple-18 contact shadow — a WIDE SHALLOW pool at L 0.877 against clean ground
    0.935 (only -0.058) plus a NARROW SEAT at 0.821 (-0.114). Hue preserved,
    faintly cool-neutral. Not a dark offset blob.
  apple-30 (toy object, warm ground) — per-face separation on ONE material:
    top face 0.968, front face 0.769, flank 0.413. Top:flank = 2.34:1. That
    ratio is the cheapest volumetric move there is, so it is authored here.

Engine C rasters (`icon-engineC-*.png`), measured with a dilated-ring figure-
ground per material-recipes § harbour (f):
  timber L p50 0.628 / 0.697 against a 45px porcelain ring at 0.882 — 1.40:1
    and 1.27:1. THE REFERENCE FAILS RUBRIC #7. The master deliberately walks
    the timber down the value ramp instead of converging on it (rubric outranks
    gate), which is also what fixes the predecessor's 16px collapse.
  accent H 17-20 deg, S 0.84-0.91 — hue kept verbatim; LUMINANCE taken from the
    family instead (L 0.447, the siblings' shared #E9562A), because at the
    raster's own L 0.30 the cut read brown on a shelf strip beside them.
  accent thickness 13px on a 1024 canvas — a hairline that dies by 32px. The
    master runs 46px, which lands 36 of 256 pixels still reading warm at 16px
    against the rasters' zero.
  tool darks H 31-40 deg, S 0.39-0.50 — the tool is WARM in the dark, not
    neutral graphite. Authored as dark rosewood, one hue family with the timber.

PROJECTION
----------
Cavalier oblique, not isometric: the u axis (the sash's width) is tilted only
-6 deg so the frame still reads as a window, while the v axis recedes down and
left to give volume. Both raster takes chose different, steeper projections and
neither silhouette said "window" any more. One affine basis, so every gradient
and texture rides the geometry for free.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024

# ---------------------------------------------------------------- projection
# P(u, v) = O + u*E1 + v*E2.  Cavalier oblique; E1 carries the -6 deg tilt.
O = (288.0, 290.0)
E1 = (1.0, -0.055)          # the sash's width axis, running slightly uphill
E2 = (-0.075, 0.955)        # the depth axis, receding down-left
WALL = 52.0                 # the frame's thickness, extruded straight down

# ---------------------------------------------------------------- the sash
UW, VH = 500.0, 470.0       # outer plan size, local units
RAIL_TOP = 96.0
RAIL_BOT = 118.0            # a sash's bottom rail is always the deepest
STILE = 116.0               # the registered member — wide enough to carry the mark
CORNER = 16.0               # the members' arris, softened not rounded
REBATE = 26.0               # the glazing rebate's visible step

# ---------------------------------------------------------------- the gauge
# The stock is registered on the LEFT STILE'S OUTER EDGE (u = 0), so the beam
# runs across the work in +u and its tail sticks out behind over the porcelain.
# That is the honest anatomy AND it keeps the tail inside the tile — registering
# on the top rail points the tail straight out of frame, which is what the first
# draft did and why the gauge read as a separate object stuck on.
STOCK_UD = 106.0            # how far the stock stands off the reference edge
STOCK_V0, STOCK_VL = 30.0, 158.0
STOCK_H = 66.0              # its height above the sash's top face
BEAM_W = 76.0
# The tail runs off the tile's left edge on purpose (device #18, edge-bleed):
# the tool is longer than the frame it is working. A tail that stops just inside
# the mask reads as an accident; one that is cut by it reads as a boundary.
BEAM_U0, BEAM_U1 = -400.0, 58.0   # tail over the porcelain -> pin in the stile
BEAM_H = 30.0
SCREW_R = 34.0
PIN_U = 58.0                # the set distance: 58 of the stile's 116

# ---------------------------------------------------------------- the mark
# LINE_V0 sits just inside the beam's own lower edge so the cut visibly
# EMERGES from under the tool rather than starting near it with a gap.
LINE_V0, LINE_V1 = 143.0, 442.0
LINE_W = 46.0                     # 13px on the raster died by 32px; this holds

# ---------------------------------------------------------------- palette
# One key light, upper-left. One shared ramp axis in userSpaceOnUse for every
# face, so a multi-material object cannot acquire two light directions.
KEY_A, KEY_B = (170.0, 40.0), (880.0, 920.0)

GROUND_HI = "#FDFCF9"       # L 0.986 — brightest at frac (0.34, 0.02)
GROUND_MID = "#F3EFE7"      # L 0.943
GROUND_LO = "#E7E1D5"       # L 0.884 — the measured 0.07 fall, warm H 39
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"

TIMBER_HI = "#BCA47A"       # top face, lit end   L 0.601
TIMBER_LO = "#6B5940"       # top face, far end   L 0.372
WALL_RIGHT = "#5A4A34"      # L 0.297
WALL_BOT = "#453722"        # L 0.244 — top:flank 2.35:1, per apple-30
ARRIS = "#D2C1A0"           # the lit edge catch on the top and left arrises
MITRE_DARK = "#5F5039"
SEAT_DARK = "#6E5C3E"       # the narrow contact seat, -0.114 L
POOL = "#A99775"            # the wide shallow pool, -0.058 L, hue preserved

PANE_HI = "#A7B2AB"         # L 0.694 — cool gel, S 0.06
PANE_LO = "#8A968F"         # L 0.585
PANE_SHEEN = "#FFFFFF"
REBATE_SHADE = "#3E3324"

TOOL_TOP = "#4A3D2E"        # L 0.246
TOOL_TOP_LO = "#3A2F22"
TOOL_RIGHT = "#382D20"      # L 0.190
TOOL_FRONT = "#2A2116"      # L 0.135 — warm in the dark, H 33 S 0.46
TOOL_ARRIS = "#8A7554"
STEEL = "#C2BAA6"
STEEL_HI = "#F2EEE4"
STEEL_LO = "#8B8474"

ACCENT = "#DE5A1E"          # L 0.447 H 19.0 S 0.865 — family luminance, own hue
ACCENT_DEEP = "#93300B"     # the groove's shadowed near wall
ACCENT_BEAD = "#F59450"     # brightest at the pin, where the cut is fresh
GROOVE_LIP = "#C6AE86"      # timber catching light off the groove's far wall
GROOVE_SHADE = "#4A3C26"    # the groove's near flank — shadowed TIMBER, not accent


# ---------------------------------------------------------------- helpers

def P(u, v, lift=0.0):
    """Project a plan point. `lift` raises it above the plan, straight up."""
    return (O[0] + u * E1[0] + v * E2[0],
            O[1] + u * E1[1] + v * E2[1] - lift)


def poly(pts, close=True):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d + " Z" if close else d


def quad(u0, v0, u1, v1, lift=0.0):
    return [P(u0, v0, lift), P(u1, v0, lift), P(u1, v1, lift), P(u0, v1, lift)]


def chamfered(u0, v0, u1, v1, c, lift=0.0):
    """A plan rectangle with its four corners cut — an arris, not a radius."""
    pts = [(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c),
           (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)]
    return [P(u, v, lift) for u, v in pts]


def wall(pa, pb, depth):
    """The extruded face hanging below edge pa->pb."""
    return [pa, pb, (pb[0], pb[1] + depth), (pa[0], pa[1] + depth)]


def lin(gid, colours, a=KEY_A, b=KEY_B, opac=None):
    stops = []
    n = len(colours)
    for i, c in enumerate(colours):
        off = 0 if n == 1 else i / (n - 1)
        o = "" if opac is None else f' stop-opacity="{opac[i]}"'
        stops.append(f'<stop offset="{off:.3f}" stop-color="{c}"{o}/>')
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}">'
            + "".join(stops) + '</linearGradient>')


def build() -> str:
    out: list[str] = []
    add = out.append

    # plan landmarks
    IU0, IU1 = STILE, UW - STILE                 # the opening
    IV0, IV1 = RAIL_TOP, VH - RAIL_BOT
    outer = chamfered(0, 0, UW, VH, CORNER)
    inner = chamfered(IU0, IV0, IU1, IV1, CORNER * 0.5)
    A, B, C, D = P(0, 0), P(UW, 0), P(UW, VH), P(0, VH)

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ------------------------------------------------------------ defs
    add('<defs>')
    add(f'''<radialGradient id="ground" cx="0.34" cy="0.02" r="1.06">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.52" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </radialGradient>''')
    add(f'''<radialGradient id="vig" cx="0.42" cy="0.36" r="0.72">
      <stop offset="0.62" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.30"/>
    </radialGradient>''')
    add(lin("topface", [TIMBER_HI, TIMBER_LO]))
    add(lin("rightwall", [WALL_RIGHT, "#4A3D2B"]))
    add(lin("botwall", ["#6E5B3C", WALL_BOT]))
    add(lin("pane", [PANE_HI, PANE_LO]))
    add(lin("tooltop", [TOOL_TOP, TOOL_TOP_LO]))
    add(lin("toolright", [TOOL_RIGHT, "#2B2318"]))
    add(lin("toolfront", ["#33291C", TOOL_FRONT]))
    add(lin("groove", [ACCENT, ACCENT_DEEP]))
    add(f'''<linearGradient id="cut" gradientUnits="userSpaceOnUse"
      x1="{P(PIN_U - LINE_W / 2, LINE_V0)[0]:.1f}" y1="0"
      x2="{P(PIN_U + LINE_W / 2, LINE_V0)[0]:.1f}" y2="0">
      <stop offset="0" stop-color="{ACCENT_DEEP}" stop-opacity="0.74"/>
      <stop offset="0.15" stop-color="{ACCENT_DEEP}" stop-opacity="0.22"/>
      <stop offset="0.52" stop-color="{ACCENT_DEEP}" stop-opacity="0"/>
      <stop offset="0.88" stop-color="{ACCENT_DEEP}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}" stop-opacity="0.46"/>
    </linearGradient>''')
    add(f'''<linearGradient id="screw" gradientUnits="userSpaceOnUse"
      x1="{KEY_A[0]}" y1="{KEY_A[1]}" x2="{KEY_B[0]}" y2="{KEY_B[1]}">
      <stop offset="0" stop-color="{STEEL_HI}"/>
      <stop offset="0.55" stop-color="{STEEL}"/>
      <stop offset="1" stop-color="{STEEL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="sheen" x1="0.02" y1="0" x2="0.86" y2="1">
      <stop offset="0" stop-color="{PANE_SHEEN}" stop-opacity="0.28"/>
      <stop offset="0.34" stop-color="{PANE_SHEEN}" stop-opacity="0.10"/>
      <stop offset="0.72" stop-color="{PANE_SHEEN}" stop-opacity="0"/>
    </linearGradient>''')
    # The bounce off the cut onto the timber beside it. A kiss on the surfaces
    # that FACE the groove, 0.20 falling to 0 — a wide wash browns a whole face
    # while every measurement of the ramp still says the colours are right
    # (material-recipes, ship-feature (e)).
    add(f'''<linearGradient id="bounce" gradientUnits="userSpaceOnUse"
      x1="{P(PIN_U + LINE_W / 2, LINE_V0)[0]:.1f}" y1="0"
      x2="{P(PIN_U + LINE_W / 2 + 46, LINE_V0)[0]:.1f}" y2="0">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </linearGradient>''')
    add('<filter id="pool" x="-35%" y="-35%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="46"/></filter>')
    add('<filter id="seat" x="-40%" y="-40%" width="190%" height="190%">'
        '<feGaussianBlur stdDeviation="11"/></filter>')
    add('<filter id="soft" x="-40%" y="-40%" width="190%" height="190%">'
        '<feGaussianBlur stdDeviation="5"/></filter>')
    add('<filter id="toolshadow" x="-45%" y="-45%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="17"/></filter>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add(f'<clipPath id="opening"><path d="{poly(inner)}"/></clipPath>')
    add(f'<clipPath id="stileclip"><path d="{poly(chamfered(0, 0, IU0, VH, CORNER))}"/></clipPath>')
    add('</defs>')

    add('<g clip-path="url(#tile)">')

    # ============================================================ bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<path d="{SQUIRCLE.read_text().strip()}" fill="none" '
        f'stroke="{RIM_TILE}" stroke-width="7" stroke-opacity="0.55"/>')
    add('</g>')

    # ============================================================ mid
    add('<g id="mid">')

    # the wide shallow pool, measured at -0.058 L, thrown down-right
    pool = [(x + 54, y + 66) for x, y in
            chamfered(-14, -14, UW + 30, VH + 26, CORNER * 2)]
    add(f'<path d="{poly(pool)}" fill="{POOL}" fill-opacity="0.56" '
        f'filter="url(#pool)"/>')

    # the narrow seat where the walls meet the bench
    seat = [(x, y + WALL) for x, y in (D, C, B)]
    add(f'<path d="{poly([(D[0] - 6, D[1] + WALL - 14), *seat, (B[0] + 10, B[1] + WALL)], close=False)}" '
        f'fill="none" stroke="{SEAT_DARK}" stroke-width="30" stroke-opacity="0.52" '
        f'stroke-linecap="round" filter="url(#seat)"/>')

    # the two visible extruded faces
    add(f'<path d="{poly(wall(D, C, WALL))}" fill="url(#botwall)"/>')
    add(f'<path d="{poly(wall(C, B, WALL))}" fill="url(#rightwall)"/>')
    # the arris between the top face and the extruded flank — one pixel of the
    # key reaching over the edge is what stops the flank reading as a black bar
    add(f'<path d="{poly([D, C, B], close=False)}" fill="none" '
        f'stroke="{ARRIS}" stroke-width="3" stroke-opacity="0.22"/>')

    # the frame's top face: outer minus the opening
    add(f'<path d="{poly(outer)} {poly(inner)}" fill="url(#topface)" '
        f'fill-rule="evenodd"/>')

    # the mitres — four joint lines from each outer corner to its inner one
    for (uo, vo), (ui, vi) in (((0, 0), (IU0, IV0)), ((UW, 0), (IU1, IV0)),
                               ((UW, VH), (IU1, IV1)), ((0, VH), (IU0, IV1))):
        p0, p1 = P(uo, vo), P(ui, vi)
        add(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" '
            f'y2="{p1[1]:.1f}" stroke="{MITRE_DARK}" stroke-width="3.5" '
            f'stroke-opacity="0.34"/>')

    # the glazing rebate, then the pane seated in it
    add('<g clip-path="url(#opening)">')
    add(f'<path d="{poly(inner)}" fill="url(#pane)"/>')
    # authored overlap: the timber's colour bleeding through the pane's edge
    add(f'<path d="{poly(inner)}" fill="{TIMBER_LO}" fill-opacity="0.22" '
        f'filter="url(#soft)" transform="translate(9,-7)"/>')
    add(f'<path d="{poly(inner)}" fill="url(#pane)" fill-opacity="0.82"/>')
    # the rebate's own shadow, on the far walls only (top and left of the hole)
    reb = [P(IU0, IV0), P(IU1, IV0), P(IU1, IV1), P(IU0, IV1)]
    add(f'<path d="{poly([reb[1], reb[0], reb[3]], close=False)}" fill="none" '
        f'stroke="{REBATE_SHADE}" stroke-width="{REBATE}" stroke-opacity="0.42" '
        f'filter="url(#soft)"/>')
    add(f'<path d="{poly(inner)}" fill="url(#sheen)"/>')
    streak = [P(IU0 + 34, IV0 + 12), P(IU0 + 88, IV0 + 12),
              P(IU0 + 30, IV1 - 8), P(IU0 - 6, IV1 - 8)]
    add(f'<path d="{poly(streak)}" fill="{PANE_SHEEN}" fill-opacity="0.13"/>')
    add('</g>')
    # the lit lip on the near inner edges — the rebate read from the other side
    add(f'<path d="{poly([reb[3], reb[2], reb[1]], close=False)}" fill="none" '
        f'stroke="{ARRIS}" stroke-width="4" stroke-opacity="0.34"/>')
    add('</g>')

    # ============================================================ fg
    add('<g id="fg">')

    # ---- the mark. A V-groove down the registered stile. The flank on the +u
    #      side faces back toward the key, so it is the LIT one; the -u flank
    #      faces away and goes to shadow. Assuming "highlight = lighter than its
    #      surroundings" on both sides is the repeat trap in material-recipes.
    add('<g clip-path="url(#stileclip)">')
    gl0, gl1 = P(PIN_U, LINE_V0), P(PIN_U, LINE_V1)
    hw = LINE_W / 2
    # the near flank's own shadow: a hairline hard against the cut, not a band.
    # A blurred 13px band on one side and a lit lip on the other is the grammar
    # of a RAISED bar with a drop shadow, which is what the previous round drew.
    add(f'<path d="{poly([(gl0[0] - hw - 2, gl0[1]), (gl1[0] - hw - 2, gl1[1])], close=False)}" '
        f'fill="none" stroke="{GROOVE_SHADE}" stroke-width="5" stroke-opacity="0.62"/>')
    add(f'<path d="{poly([gl0, gl1], close=False)}" fill="none" '
        f'stroke="url(#groove)" stroke-width="{LINE_W}" stroke-linecap="butt"/>')
    # the cross-section: deep on the shadowed flank, warm on the lit one
    add(f'<path d="{poly([gl0, gl1], close=False)}" fill="none" '
        f'stroke="url(#cut)" stroke-width="{LINE_W}" stroke-linecap="butt"/>')
    add(f'<path d="{poly([(gl0[0] + hw + 2, gl0[1] + 6), (gl1[0] + hw + 2, gl1[1])], close=False)}" '
        f'fill="none" stroke="{GROOVE_LIP}" stroke-width="2.5" stroke-opacity="0.40"/>')
    add('</g>')

    # ---- the beam, laid across the work, and its shadow on the timber
    bv0 = STOCK_V0 + STOCK_VL / 2 - BEAM_W / 2
    bv1 = bv0 + BEAM_W
    beam_top = quad(BEAM_U0, bv0, BEAM_U1, bv1, BEAM_H)
    add(f'<path d="{poly([(x + 14, y + 22) for x, y in quad(BEAM_U0, bv0, BEAM_U1, bv1)])}" '
        f'fill="{SEAT_DARK}" fill-opacity="0.40" filter="url(#toolshadow)"/>')
    add(f'<path d="{poly(wall(beam_top[3], beam_top[2], BEAM_H))}" fill="url(#toolfront)"/>')
    add(f'<path d="{poly(wall(beam_top[2], beam_top[1], BEAM_H))}" fill="url(#toolright)"/>')
    add(f'<path d="{poly(beam_top)}" fill="url(#tooltop)"/>')
    add(f'<path d="{poly([beam_top[0], beam_top[1]], close=False)} '
        f'{poly([beam_top[0], beam_top[3]], close=False)}" fill="none" '
        f'stroke="{TOOL_ARRIS}" stroke-width="4" stroke-opacity="0.55"/>')

    # ---- the pin: where the set distance lands on the work
    pin = P(PIN_U, bv1, BEAM_H)
    add(f'<path d="M{pin[0] - 8:.1f},{pin[1] - 14:.1f} L{pin[0] + 8:.1f},{pin[1] - 14:.1f} '
        f'L{pin[0] + 5:.1f},{pin[1] + 7:.1f} L{pin[0] - 3:.1f},{pin[1] + 7:.1f} Z" '
        f'fill="url(#screw)" fill-opacity="0.92"/>')

    # ---- the stock, clamped on the reference edge: the icon's whole argument
    st_top = chamfered(-STOCK_UD, STOCK_V0, 0, STOCK_V0 + STOCK_VL, 8, STOCK_H)
    add(f'<path d="{poly([(x + 16, y + 26) for x, y in chamfered(-STOCK_UD, STOCK_V0, 0, STOCK_V0 + STOCK_VL, 8)])}" '
        f'fill="{SEAT_DARK}" fill-opacity="0.44" filter="url(#toolshadow)"/>')
    for i in (2, 3, 4):
        add(f'<path d="{poly(wall(st_top[i], st_top[i + 1], STOCK_H))}" '
            f'fill="url(#tool{"right" if i < 4 else "front"})"/>')
    add(f'<path d="{poly(st_top)}" fill="url(#tooltop)"/>')
    # the arris along the registered face — the edge that does the work
    add(f'<path d="{poly([st_top[1], st_top[2], st_top[3]], close=False)}" '
        f'fill="none" stroke="{TOOL_ARRIS}" stroke-width="5" stroke-opacity="0.70"/>')
    add(f'<path d="{poly([st_top[7], st_top[0], st_top[1]], close=False)}" '
        f'fill="none" stroke="{TOOL_ARRIS}" stroke-width="4" stroke-opacity="0.45"/>')

    # ---- the thumbscrew: what locks the set distance so it cannot drift
    sc = P(-STOCK_UD * 0.50, STOCK_V0 + STOCK_VL * 0.50, STOCK_H)
    add(f'<ellipse cx="{sc[0]:.1f}" cy="{sc[1] + 9:.1f}" rx="{SCREW_R:.0f}" '
        f'ry="{SCREW_R * 0.60:.0f}" fill="#1F1810" fill-opacity="0.55" '
        f'filter="url(#soft)"/>')
    add(f'<ellipse cx="{sc[0]:.1f}" cy="{sc[1]:.1f}" rx="{SCREW_R:.0f}" '
        f'ry="{SCREW_R * 0.60:.0f}" fill="url(#screw)"/>')
    for k in range(-3, 4):
        kx = sc[0] + k * SCREW_R * 0.24
        add(f'<line x1="{kx:.1f}" y1="{sc[1] - SCREW_R * 0.40:.1f}" x2="{kx:.1f}" '
            f'y2="{sc[1] + SCREW_R * 0.40:.1f}" stroke="{STEEL_LO}" '
            f'stroke-width="2.5" stroke-opacity="0.30"/>')
    add('</g>')

    # ============================================================ highlight
    add('<g id="highlight">')
    # the arris catch on the frame's top and left outer edges only
    add(f'<path d="{poly([P(CORNER, 0), P(UW - CORNER, 0)], close=False)}" '
        f'fill="none" stroke="{ARRIS}" stroke-width="6" stroke-opacity="0.80"/>')
    add(f'<path d="{poly([P(0, CORNER), P(0, VH - CORNER)], close=False)}" '
        f'fill="none" stroke="{ARRIS}" stroke-width="5" stroke-opacity="0.55"/>')
    # the fresh bead of cut at the pin — brightest where the pin is working
    bead = [(gl0[0] - hw + 2, gl0[1] + 1), (gl0[0] + hw - 2, gl0[1] + 1),
            (gl0[0] + hw - 2, gl0[1] + 26), (gl0[0] - hw + 2, gl0[1] + 26)]
    add(f'<path d="{poly(bead)}" fill="{ACCENT_BEAD}" fill-opacity="0.42"/>')
    # the thumbscrew's catch
    add(f'<ellipse cx="{sc[0] - SCREW_R * 0.22:.1f}" cy="{sc[1] - SCREW_R * 0.24:.1f}" '
        f'rx="{SCREW_R * 0.44:.0f}" ry="{SCREW_R * 0.19:.0f}" fill="{STEEL_HI}" '
        f'fill-opacity="0.55" filter="url(#soft)"/>')
    add('</g>')

    add('</g>')   # tile
    add('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    (HERE / "icon.svg").write_text(build())
    print(f"wrote {HERE / 'icon.svg'}")
