#!/usr/bin/env python3
"""Build the better-loop icon master.

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel
objects, hybridised with device #17 (tile-as-machine) and #18 (edge-bleed
physicality). Device: **the stepped rail** — one graphite rail runs dead level
across most of the tile, bleeding off both edges because the state it carries
started before this window and continues after it, and then rises by exactly one
step. A vermilion gel shim is set in at the step, and a porcelain follower shoe
rides the raised tread just past it.

The signature move is that **the accent is the height difference, not the
height** — the shim is a separate physical piece whose whole dimension is the
change, so what the tile hands you is the delta rather than the state. Everything
else is quiet by construction: the long flat run carries only a hairline catch,
and the one place the profile moves is the one place any colour appears. That is
the skill's own rule (a wake must carry new information) performed rather than
illustrated.

Deliberately not encoded: the doubling backoff. Two or three decaying risers were
sketched and dropped — a second and third accent spends the family's one warm hue
three times and reads as a bar chart at 48px.

Everything geometric or material is a named constant, so a fidelity round is a
parameter edit rather than path surgery and a banner can be derived from the same
numbers: LIGHT_ANGLE_DEG / LIGHT_AXIS for the light, DEPTH for the extrusion,
Spec.step_x / step_h / shim_w for the cell, ACCENT* for the one warm hue.

    python3 build_icon.py                       # writes icon.svg beside this file
    python3 build_icon.py --set step_h=196 --out /tmp/try.svg
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE_PATH = (HERE / ".." / ".." / "create-mac-icon" / "assets"
                 / "squircle-path.txt")

S = 1024                     # canvas — full bleed, masked by the family squircle

# ---------------------------------------------------------------- light model
# One soft key light from the upper left. Sampled, not assumed: across the
# porcelain corpus exemplars (apple-05, apple-10, apple-28) the brightest ground
# pixel sits at (0.02-0.05, 0.00) — top-left corner — in every one of them.
LIGHT_ANGLE_DEG = 118.0
LIGHT_AXIS = (math.cos(math.radians(LIGHT_ANGLE_DEG)),
              math.sin(math.radians(LIGHT_ANGLE_DEG)))      # ≈ (-0.47, +0.88)

# The shallow oblique that gives every horizontal surface a second face. A
# profile has one visible face and one face can carry one gradient, which is
# how anvil-errand's predecessor measured 77.3% locally uniform; extruding is
# the fix, and the treads are what there is to extrude here.
DEPTH = (22.0, -32.0)        # back edges shift right and up

# ---------------------------------------------------------------- the cushion
# Porcelain/daylight, lifted off the family rather than invented:
# deck-craft #FCFAF4→#DED5C2, create-test-suite #F8F5EE→#E4DDCB,
# whats-left #F6F3EA→#E0D9C8. Measured against better-goal's own render, whose
# ground runs Y 0.739 → 0.974, and against apple-05's porcelain at Y 0.774 →
# 1.000, so this ground sits inside both.
GROUND_HI = "#FCFAF4"
GROUND_MID = "#F3EDE1"
GROUND_LO = "#DED5C2"
GROUND_RIM = "#FFFDF8"       # the inner rim light every Tahoe tile carries
GROUND_VIGNETTE = "#8B7F66"
SHADOW = "#3B3327"           # warm — the corpus's cast shadows are warm even
                             # where the object casting them is cool

# ---------------------------------------------------------------- the graphite
# Cool graphite, measured off apple-10: its dark mass on porcelain runs hue 228
# to 233 at saturation 0.20, Y 0.008 → 0.150. Pushed a little darker than
# better-goal's hub (#282F37 → #5A626B at hue 212) so the two do not share a
# value as well as a shelf.
RAIL_HI = "#5E6570"          # the lit tread, top-left end
RAIL_MID = "#3A4048"
RAIL_LO = "#1C2027"          # the shaded base
RAIL_EDGE = "#111419"        # the seat edge all round
RAIL_TREAD_HI = "#7A828E"    # the tread's own top face, which the key reaches
RAIL_TREAD_LO = "#4A515B"
RAIL_CATCH = "#CBD3DE"       # the hairline the key leaves on a lit top edge

# ---------------------------------------------------------------- the accent
# One warm hue, spent once — on the shim, which is the semantic element.
# Family band: report #E46235, whats-left #DF612E, deck-craft #DE5A28,
# dossier-report #EA5B34 — kin to Fledgeling #C4622D. Corroborated against
# apple-05, the corpus's porcelain-plus-warm-gel exemplar: hue 9-32°,
# saturation 0.81-0.85, Y 0.166 → 0.502 across the object.
ACCENT = "#DE5A28"
ACCENT_HI = "#F2823C"        # the lit upper third of the shim's face
ACCENT_DEEP = "#BC3A14"      # its shaded foot. apple-05's darkest accent pixel
                             # is #D22D1E — still saturated and still warm, so a
                             # shaded warm face must not drift to brown or grey.
ACCENT_RIM = "#F6D3AC"       # apple-05's lightest accent pixel is #EDD0A3: the
                             # catch on a vermilion gel edge is warm cream, not
                             # white and not pink.

# ---------------------------------------------------------------- the follower
# Machined steel, one value band above the rail and well below the cushion. It
# was porcelain for two rounds and that is a measurement error rather than a
# taste one: a porcelain object on a porcelain ground runs about 1.15:1, so the
# part of the saddle that stands above the rail simply was not there. Steel
# reads against both, and it keeps the palette to one cool hue family plus the
# one warm accent.
YOKE_HI = "#AEB7C3"
YOKE_MID = "#828C9B"
YOKE_LO = "#565E6B"
YOKE_EDGE = "#262B33"
YOKE_TREAD_HI = "#AFB9C6"
YOKE_TREAD_LO = "#7E8795"


@dataclass
class Spec:
    """Every geometric decision in one place, so a round is a parameter edit."""

    bleed: float = 64            # how far the rail runs past the tile edge
    thick: float = 124           # the rail is one constant-section band. A solid
                                 # plinth was tried first and its raised half is
                                 # a 300px block of graphite: the tile reads as a
                                 # floor with a step in it rather than as a
                                 # reading that moved once.
    low_top: float = 606          # the quiet run's tread height
    step_x: float = 552          # where the reading changed: right of centre, so
                                 # the run that says nothing dominates the tile
    step_h: float = 200          # the change itself. Swept at 178 / 212 / 240
                                 # against the 32px render: under about 190 the two
                                 # runs merge into one thick band with a notch,
                                 # over about 230 they read as two separate bars
                                 # and the family already has a stack of those
    shim_w: float = 88           # the delta, as a piece with a width
    shim_proud: float = 8        # it stands this far above the tread it raised
    shim_over: float = 12        # and laps this far over the run it lifted from
    shim_lap: float = 0          # the foot lands on the quiet run's tread, so the
                                 # shim's visible height is exactly the change and
                                 # nothing crosses its face
    corner: float = 9            # the rail's edge radius — machined, not soft
    yoke_w: float = 142          # the follower: a saddle clipped over the tread
    yoke_gap: float = 74         # clear of the shim: it has already climbed
    yoke_arm: float = 68         # how tall it stands above the tread
    yoke_back: float = 34        # how far its lip laps down over the rail's face
    yoke_corner: float = 26      # salvaged from the raster takes: both rendered
                                 # the follower as a clip WRAPPED over the rail,
                                 # and a generous top radius with one arc catch
                                 # reads as machined where a boxy block read as a
                                 # tray
    yoke_jaw: float = 13         # the graphite pad it actually bears on
    lift: float = -70            # optical centring: the shadows fall down-right,
                                 # so the geometry sits a little high
    cast_dx: float = 11
    cast_dy: float = 21
    cast_blur: float = 19
    contact_opacity: float = 0.36
    yoke_cast_opacity: float = 0.30
    bounce: float = 0.52         # the shim's warm spill onto the tread beside it.
                                 # Tight, bright, and in the pale spill hue: at
                                 # the accent's own hue over cool graphite it
                                 # reads as rust rather than as light

    @property
    def high_top(self) -> float:
        return self.low_top - self.step_h

    @property
    def x0(self) -> float:
        return -self.bleed

    @property
    def x1(self) -> float:
        return S + self.bleed

    @property
    def shim_x0(self) -> float:
        return self.step_x - self.shim_over

    @property
    def shim_x1(self) -> float:
        return self.step_x + self.shim_w

    def yoke_box(self) -> tuple[float, float, float, float]:
        """Outer bounds of the follower saddle, clipped over the raised tread."""
        x = self.shim_x1 + self.yoke_gap
        y = self.high_top - self.yoke_arm
        return x, y, self.yoke_w, self.yoke_arm + self.yoke_back


def rounded(x: float, y: float, w: float, h: float, r: float) -> str:
    r = min(r, w / 2, h / 2)
    return (f"M{x + r:.1f},{y:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} v{h - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{r:.1f} h{-(w - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{-r:.1f} v{-(h - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{-r:.1f} z")


def top_face(x0: float, x1: float, y: float) -> str:
    """The horizontal surface of a run or a block, seen at a shallow angle."""
    dx, dy = DEPTH
    return (f"M{x0:.1f},{y:.1f} H{x1:.1f} "
            f"l{dx:.1f},{dy:.1f} H{x0 + dx:.1f} z")


def axis_points(x0: float, y0: float, x1: float, y1: float) -> tuple[float, ...]:
    """Start and end of the key light's axis across a box, in user space.

    Every face gradient hangs on this one axis so the faces read as one object
    under one light rather than as adjacent panels — anvil-errand's finding,
    which cost that commission a round to learn.
    """
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = LIGHT_AXIS
    r = max(x1 - x0, y1 - y0) * 0.62
    return (cx + lx * r, cy - ly * r, cx - lx * r, cy + ly * r)


def yoke_path(sp: Spec) -> str:
    """The follower, as a saddle whose lip laps down over the rail's own face.

    Two shapes were tried and dropped, and both failures were about the same
    thing — how a pale object reads against a dark rail:

    · a plain block on the tread, with two graphite roller pins under it. The
      pins sat at 0.26 and 0.74 of its width and read as a pair of eyes at every
      size down to 32px, so the follower stopped being hardware and became a
      face;
    · a yoke the rail passes through, open on its up-light side. Pale jaws
      interlocking with a dark band is a figure-ground ambiguity, and what it
      resolves to is a belt buckle.

    A saddle avoids both: it breaks the band's silhouette upward only, and it
    grips a surface rather than threading through one.
    """
    x, y, w, h = sp.yoke_box()
    r = sp.yoke_corner
    x1, y1 = x + w, y + h
    return (f"M{x:.1f},{y + r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{-r:.1f} "
            f"H{x1 - r:.1f} a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} "
            f"V{y1 - r:.1f} a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{r:.1f} "
            f"H{x + r:.1f} a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{-r:.1f} z")


def build(sp: Spec) -> str:
    squircle = SQUIRCLE_PATH.read_text().strip()
    dx, dy = DEPTH
    ht, lt, T = sp.high_top, sp.low_top, sp.thick
    sx0, sx1 = sp.shim_x0, sp.shim_x1
    yx, yy, yw, yh = sp.yoke_box()

    # The band, as one staircase polygon. The stretch between the step and the
    # shim's right edge fills solid: that is the step's own body, and the shim is
    # the plate on its face.
    band = (f"M{sp.x0:.1f},{lt:.1f} H{sp.step_x:.1f} V{ht:.1f} H{sp.x1:.1f} "
            f"V{ht + T:.1f} H{sx1:.1f} V{lt + T:.1f} H{sp.x0:.1f} z")

    out: list[str] = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ------------------------------------------------------------------ defs
    add("<defs>")
    add(f'<radialGradient id="cushion" cx="0.38" cy="0.26" r="0.90">'
        f'<stop offset="0" stop-color="{GROUND_HI}"/>'
        f'<stop offset="0.54" stop-color="{GROUND_MID}"/>'
        f'<stop offset="1" stop-color="{GROUND_LO}"/></radialGradient>')
    add(f'<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">'
        f'<stop offset="0.54" stop-color="{GROUND_VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{GROUND_VIGNETTE}" stop-opacity="0.24"/>'
        f'</radialGradient>')

    ax = axis_points(sp.x0, ht, sp.x1, lt + T)
    add(f'<linearGradient id="railface" gradientUnits="userSpaceOnUse" '
        f'x1="{ax[0]:.1f}" y1="{ax[1]:.1f}" x2="{ax[2]:.1f}" y2="{ax[3]:.1f}">'
        f'<stop offset="0" stop-color="{RAIL_HI}"/>'
        f'<stop offset="0.44" stop-color="{RAIL_MID}"/>'
        f'<stop offset="1" stop-color="{RAIL_LO}"/></linearGradient>')
    add(f'<linearGradient id="railtread" gradientUnits="userSpaceOnUse" '
        f'x1="{sp.x0:.1f}" y1="0" x2="{sp.x1:.1f}" y2="0">'
        f'<stop offset="0" stop-color="{RAIL_TREAD_HI}"/>'
        f'<stop offset="1" stop-color="{RAIL_TREAD_LO}"/></linearGradient>')

    axs = axis_points(sx0, ht - sp.shim_proud, sx1, lt)
    add(f'<linearGradient id="shimface" gradientUnits="userSpaceOnUse" '
        f'x1="{axs[0]:.1f}" y1="{axs[1]:.1f}" x2="{axs[2]:.1f}" y2="{axs[3]:.1f}">'
        f'<stop offset="0" stop-color="{ACCENT_HI}"/>'
        f'<stop offset="0.40" stop-color="{ACCENT}"/>'
        f'<stop offset="1" stop-color="{ACCENT_DEEP}"/></linearGradient>')
    add(f'<linearGradient id="shimtop" gradientUnits="userSpaceOnUse" '
        f'x1="{sx0:.1f}" y1="0" x2="{sx1 + dx:.1f}" y2="0">'
        f'<stop offset="0" stop-color="{ACCENT_RIM}"/>'
        f'<stop offset="1" stop-color="{ACCENT_HI}"/></linearGradient>')
    add(f'<linearGradient id="bounce" gradientUnits="userSpaceOnUse" '
        f'x1="{sx0 - 62:.1f}" y1="0" x2="{sx0 + 2:.1f}" y2="0">'
        f'<stop offset="0" stop-color="{ACCENT_RIM}" stop-opacity="0"/>'
        f'<stop offset="0.62" stop-color="{ACCENT_RIM}" stop-opacity="0.75"/>'
        f'<stop offset="1" stop-color="{ACCENT_RIM}" stop-opacity="1"/>'
        f'</linearGradient>')

    axh = axis_points(yx, yy, yx + yw, yy + yh)
    add(f'<linearGradient id="yokeface" gradientUnits="userSpaceOnUse" '
        f'x1="{axh[0]:.1f}" y1="{axh[1]:.1f}" x2="{axh[2]:.1f}" y2="{axh[3]:.1f}">'
        f'<stop offset="0" stop-color="{YOKE_HI}"/>'
        f'<stop offset="0.50" stop-color="{YOKE_MID}"/>'
        f'<stop offset="1" stop-color="{YOKE_LO}"/></linearGradient>')
    add(f'<linearGradient id="yoketread" gradientUnits="userSpaceOnUse" '
        f'x1="{yx:.1f}" y1="0" x2="{yx + yw + dx:.1f}" y2="0">'
        f'<stop offset="0" stop-color="{YOKE_TREAD_HI}"/>'
        f'<stop offset="1" stop-color="{YOKE_TREAD_LO}"/></linearGradient>')
    add('<linearGradient id="sheen" x1="0.04" y1="0" x2="0.34" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.62"/>'
        '<stop offset="0.44" stop-color="#FFFFFF" stop-opacity="0.12"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')

    add(f'<filter id="cast" x="-45%" y="-45%" width="200%" height="220%">'
        f'<feDropShadow dx="{sp.cast_dx}" dy="{sp.cast_dy}" '
        f'stdDeviation="{sp.cast_blur}" flood-color="{SHADOW}" '
        f'flood-opacity="{sp.contact_opacity}"/></filter>')
    add(f'<filter id="castyoke" x="-70%" y="-70%" width="260%" height="280%">'
        f'<feDropShadow dx="{sp.cast_dx - 4}" dy="{sp.cast_dy - 9}" '
        f'stdDeviation="{sp.cast_blur - 8}" flood-color="{SHADOW}" '
        f'flood-opacity="{sp.yoke_cast_opacity}"/></filter>')
    add('<filter id="soften" x="-140%" y="-140%" width="380%" height="380%">'
        '<feGaussianBlur stdDeviation="12"/></filter>')
    add('<filter id="soften-tight" x="-140%" y="-140%" width="380%" height="380%">'
        '<feGaussianBlur stdDeviation="5"/></filter>')

    add(f'<clipPath id="railclip"><path d="{band}"/></clipPath>')
    add(f'<clipPath id="treadclip"><path d="{top_face(sp.x0, sx0, lt)}"/>'
        f'</clipPath>')
    add(f'<clipPath id="yokeclip"><path d="{yoke_path(sp)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{squircle}"/></clipPath>')
    add("</defs>")

    add('<g clip-path="url(#tile)">')

    # -------------------------------------------------------------------- bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#cushion)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vignette)"/>')
    add(f'<path d="{squircle}" fill="none" stroke="{GROUND_RIM}" stroke-width="7" '
        f'stroke-opacity="0.85"/>')
    add("</g>")

    add(f'<g transform="translate(0 {sp.lift})">')

    # ------------------------------------------------------------------- mid
    # The reading: one rail of constant section, two levels, and the piece that
    # raised it.
    add('<g id="mid">')

    # 1 · what the band casts on the cushion. One light, so one direction.
    add(f'<path d="{band}" fill="{SHADOW}" filter="url(#cast)"/>')

    # 2 · the treads — the horizontal surfaces the key light reaches. A profile
    #     has one visible face and one face can carry one gradient, so the run
    #     is extruded and its top surface is a second, brighter plane.
    add(f'<path d="{top_face(sp.step_x, sp.x1, ht)}" fill="url(#railtread)"/>')
    add(f'<path d="{top_face(sp.x0, sx0, lt)}" fill="url(#railtread)"/>')
    add(f'<path d="M{sp.step_x + dx:.1f},{ht + dy:.1f} H{sp.x1 + dx:.1f}" '
        f'fill="none" stroke="{RAIL_LO}" stroke-width="3" stroke-opacity="0.45"/>')

    # 3 · the front face, one gradient on one axis across the whole band, then
    #     its seat edge. The edge goes on before the shim, not after: run after
    #     it and the step's own vertical edge draws a dark seam down the shim's
    #     up-light side, which reads at 256px as a gap between the two.
    add(f'<path d="{band}" fill="url(#railface)"/>')
    add(f'<path d="{band}" fill="none" stroke="{RAIL_EDGE}" stroke-width="2.5" '
        f'stroke-opacity="0.75"/>')

    # 4 · THE SHIM — the delta as a piece. Its exposed height is the change and
    #     nothing else: it starts proud of the tread it raised and ends on the
    #     tread it lifted from, so the eye can read the difference off it
    #     directly without comparing two levels.
    shim_top = ht - sp.shim_proud
    shim_bot = lt + sp.shim_lap   # 0 by default: the foot lands on the tread
    add(f'<path d="{top_face(sx0, sx1, shim_top)}" fill="url(#shimtop)"/>')
    add(f'<path d="{rounded(sx0, shim_top, sx1 - sx0, shim_bot - shim_top, 5)}" '
        f'fill="url(#shimface)"/>')
    #     its own top-edge catch, warm cream rather than white: the corpus's
    #     lightest pixel on a vermilion gel object is #EDD0A3, not white
    add(f'<path d="M{sx0 + 3:.1f},{shim_top + 2.5:.1f} H{sx1 - 3:.1f}" fill="none" '
        f'stroke="{ACCENT_RIM}" stroke-width="4.5" stroke-opacity="0.92"/>')
    #     its own seat edge, in the accent's shaded value rather than graphite
    add(f'<path d="{rounded(sx0, shim_top, sx1 - sx0, shim_bot - shim_top, 5)}" '
        f'fill="none" stroke="{ACCENT_DEEP}" stroke-width="2.5" '
        f'stroke-opacity="0.8"/>')
    #     the shadow it throws along the raised run, immediately down-light of it
    add('<g clip-path="url(#railclip)">')
    add(f'<rect x="{sx1:.1f}" y="{ht:.1f}" width="54" height="{T:.1f}" '
        f'fill="{RAIL_LO}" fill-opacity="0.55" filter="url(#soften-tight)"/>')
    add("</g>")

    # 5 · ambient occlusion in the inside corner where the shim rises out of the
    #     quiet run. Occlusion, not a cast shadow: the key is up-light of this
    #     corner, so what darkens it is the sky the shim blocks, and it belongs
    #     on the tread rather than on the face.
    add('<g clip-path="url(#railclip)">')
    add(f'<rect x="{sx0 - 74:.1f}" y="{lt - 30:.1f}" width="80" height="40" '
        f'fill="{RAIL_LO}" fill-opacity="0.5" filter="url(#soften-tight)"/>')
    add("</g>")

    # 6 · the key's hairline along each lit top edge. The quiet run gets that
    #     hairline and nothing else — the long flat stretch is meant to be almost
    #     nothing, so the one place the profile moves is the one place there is
    #     anything to look at.
    add(f'<path d="M{sp.x0:.1f},{lt + 1.5:.1f} H{sx1:.1f}" fill="none" '
        f'stroke="{RAIL_CATCH}" stroke-width="3" stroke-opacity="0.70"/>')
    add(f'<path d="M{sx1:.1f},{ht + 1.75:.1f} H{sp.x1:.1f}" fill="none" '
        f'stroke="{RAIL_CATCH}" stroke-width="3.5" stroke-opacity="0.88"/>')

    # 8 · the warm bounce. Tight, brighter than seems right, and clipped to the
    #     graphite — widen or dim it and the flank goes muddy with every hex
    #     still correct.
    add('<g clip-path="url(#treadclip)">')
    add(f'<rect x="{sx0 - 62:.1f}" y="{lt + dy - 4:.1f}" width="66" '
        f'height="{-dy + 8:.1f}" fill="url(#bounce)" opacity="{sp.bounce}"/>')
    add("</g>")
    add("</g>")

    # -------------------------------------------------------------------- fg
    # The watcher: a follower shoe riding the raised tread, already past the
    # step. It is porcelain, so it reads against the rail rather than against
    # the ground, and it is the only element that is not part of the reading.
    add('<g id="fg">')
    yoke = yoke_path(sp)
    add(f'<path d="{yoke}" fill="{SHADOW}" filter="url(#castyoke)"/>')
    #     its own top surface — lit brighter than its front face, with a crisp
    #     far edge. Rendered as a large pale parallelogram with no far edge it
    #     read as a torn flap; darkening the whole face to fix that inverted the
    #     light and made it a trough.
    add(f'<path d="{top_face(yx, yx + yw, yy)}" fill="url(#yoketread)"/>')
    add(f'<path d="M{yx + dx:.1f},{yy + dy:.1f} H{yx + yw + dx:.1f}" fill="none" '
        f'stroke="{YOKE_EDGE}" stroke-width="3" stroke-opacity="0.55"/>')
    add(f'<path d="{yoke}" fill="url(#yokeface)"/>')
    add('<g clip-path="url(#yokeclip)">')
    add(f'<rect x="{yx:.1f}" y="{yy:.1f}" width="{yw:.1f}" '
        f'height="{yh * 0.52:.1f}" fill="url(#sheen)" opacity="0.5"/>')
    #     the lip that laps down over the rail's face is in the rail's own
    #     shadow, so it goes darker and slightly cooler than the body
    add(f'<rect x="{yx:.1f}" y="{ht:.1f}" width="{yw:.1f}" '
        f'height="{sp.yoke_back:.1f}" fill="{YOKE_MID}" fill-opacity="0.9"/>')
    add(f'<rect x="{yx:.1f}" y="{ht:.1f}" width="{yw:.1f}" height="4" '
        f'fill="{YOKE_EDGE}" fill-opacity="0.55"/>')
    #     and the bearing line it actually sits on, one value under the body
    add(f'<rect x="{yx:.1f}" y="{ht - sp.yoke_jaw:.1f}" width="{yw:.1f}" '
        f'height="{sp.yoke_jaw:.1f}" fill="{YOKE_MID}" fill-opacity="0.55"/>')
    add("</g>")
    add(f'<path d="{yoke}" fill="none" stroke="{YOKE_EDGE}" stroke-width="2.5" '
        f'stroke-opacity="0.8"/>')
    #     the wrap: one arc catch across the crown, so the top reads as turned
    #     over the rail rather than cut flat
    add(f'<path d="M{yx + 6:.1f},{yy + sp.yoke_corner + 10:.1f} '
        f'q{yw / 2 - 6:.1f},{-(sp.yoke_corner + 6):.1f} {yw - 12:.1f},0" '
        f'fill="none" stroke="{YOKE_HI}" stroke-width="7" stroke-opacity="0.5" '
        f'stroke-linecap="round"/>')
    add("</g>")

    # -------------------------------------------------------------- highlight
    add('<g id="highlight">')
    # the key's catch on the yoke's lit edges — top and up-light side, the two
    # faces it actually reaches
    add(f'<path d="M{yx + 2:.1f},{yy + sp.yoke_arm:.1f} '
        f'V{yy + sp.yoke_corner:.1f} a{sp.yoke_corner},{sp.yoke_corner} 0 0 1 '
        f'{sp.yoke_corner},{-sp.yoke_corner} h{yw - 2 * sp.yoke_corner:.1f}" '
        f'fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.62" '
        f'stroke-linecap="round"/>')
    # the shim's spill onto the yoke's up-light edge — a kiss on the edge only,
    # clipped to the yoke so the highlight layer cannot paint over the thing
    # standing in front of it. At 42px wide and 0.22 alpha it combined with the
    # lip below it into a brown stripe; the accent is 74px away from this part,
    # so what reaches it is an edge, not a wash.
    add('<g clip-path="url(#yokeclip)">')
    add(f'<rect x="{yx - 8:.1f}" y="{yy + sp.yoke_corner:.1f}" width="18" '
        f'height="{yh - sp.yoke_corner:.1f}" fill="{ACCENT_HI}" '
        f'fill-opacity="0.16" filter="url(#soften-tight)"/>')
    add("</g>")
    # and the shim's own faint glow into the daylight just above the step
    add(f'<rect x="{sx0 - 22:.1f}" y="{ht - sp.shim_proud - 30:.1f}" '
        f'width="{sx1 - sx0 + 44:.1f}" height="40" fill="{ACCENT}" '
        f'fill-opacity="0.14" filter="url(#soften)"/>')
    add("</g>")

    add("</g>")   # lift
    add("</g>")   # tile
    add("</svg>")
    return "\n".join(out)


NUMERIC = {"bleed", "thick", "low_top", "step_x", "step_h", "shim_w",
           "shim_proud", "shim_over", "shim_lap", "corner", "yoke_w", "yoke_gap", "yoke_arm",
           "yoke_back", "yoke_corner", "yoke_jaw", "lift", "cast_dx", "cast_dy", "cast_blur",
           "contact_opacity", "yoke_cast_opacity", "bounce"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--set", action="append", default=[],
                    help="override a numeric Spec field, e.g. --set step_h=196")
    a = ap.parse_args()
    sp = Spec()
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in NUMERIC:
            raise SystemExit(f"unknown or non-numeric field: {k}")
        sp = replace(sp, **{k: float(v)})
    out = Path(a.out) if a.out else HERE / "icon.svg"
    out.write_text(build(sp))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
