#!/usr/bin/env python3
"""Build the better-goal icon master.

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying one
gel/graphite object, hybridised with device #20 (data-as-glyph: the reading with a
single accent datum) and, in the shipping take, #18 (edge-bleed physicality) at the
one place the gate stands proud of the bezel.

better-goal keeps the dial and the target band — that is its recorded device in the
set's shelf register, and `better-loop` was rebuilt away from it on 2026-08-18 so
this one could keep it. So the commission is a **value** problem inside a decided
device: the predecessor was a pale cream dial on a pale cream cushion, measured at
1.05:1 face-against-tile against a 3:1 requirement, and 0.1142 RMS at 16px against
a family median of 0.2002. The fix is the relation the family's successful icons
already use — a *dark* object on porcelain, not a pale one.

Device: **the accept band with a hard stop.** A machined graphite dial whose face
carries one vermilion sector, cut through the graduations and out to the rim — the
band the reading has to be inside — with a graphite pawl straddling the band's
counter-clockwise end and standing proud of the bezel. The porcelain needle has
climbed into the band and the pawl is behind it.

The signature move is that **the band is open on one side and stopped on the
other**, so the tile says the needle can only arrive. That is the skill performed
rather than illustrated: a gate judged by exit code closes once, and a met goal is
not allowed to fall back. The accent is spent exactly once, at 2.52% of the tile in
one place, and it reaches the object's silhouette edge, which is the only place an
accent survives 16px (better-loop's finding, taken here). The pawl is graphite
rather than a second warm piece: the band is the semantic element and the pawl is
hardware, and a dark bar across a warm wedge puts the tile's highest-contrast edge
at exactly the one place the boundary closes.

Three hand-authored takes, because the value relation was the open question and one
image per relation is what settles it. The three-engine floor was met with these
plus two Arrow vector takes and one corpus-referenced raster:

    a1  the held needle   — graphite face, porcelain needle, band through the face
                            and out to the rim, graphite pawl proud of the bezel
                            (SHIPS, 11/12)
    a2  the latched bezel — a graphite bezel ring around a porcelain face. Its face
                            measures 1.00:1 against the tile, so the predecessor's
                            defect survives inside the ring (8/12)
    a3  the sunk dial     — the dial half-buried in a housing that bleeds off both
                            edges. The disc reads 1.18:1 against the housing and the
                            two merge into one lump (7/12)

Everything geometric or material is a named constant, so a fidelity round is a
parameter edit rather than path surgery, and a banner can be derived from the same
numbers: LIGHT_ANGLE_DEG / LIGHT_AXIS for the light, ACCENT* for the one warm hue,
band_a0 / band_a1 / needle_deg for the cell. `scale` sizes the whole instrument and
`cy` places it; both are swept curves, and the comments on those two fields carry
the numbers.

    python3 build_icon.py                        # writes icon.svg (take a1)
    python3 build_icon.py --variant a2 --out icon-takeA2-latched-bezel.svg
    python3 build_icon.py --set band_a0=-26 --out /tmp/try.svg
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
# One soft key light from the upper left, at the family's angle. Sampled rather
# than assumed: across the porcelain corpus exemplars (apple-05, apple-10,
# apple-23, apple-28) the brightest ground pixel sits in the top-left quadrant in
# every one of them. Shared with better-loop and anvil-errand, so a shelf of them
# is lit by one lamp.
LIGHT_ANGLE_DEG = 118.0
LIGHT_AXIS = (math.cos(math.radians(LIGHT_ANGLE_DEG)),
              math.sin(math.radians(LIGHT_ANGLE_DEG)))      # ≈ (-0.47, +0.88)

# ---------------------------------------------------------------- the cushion
# Porcelain/daylight, lifted off the family rather than invented: deck-craft
# #FCFAF4→#DED5C2, test-campaign #F8F5EE→#E4DDCB, whats-left #F6F3EA→#E0D9C8.
# Measured against apple-23's porcelain, whose tile ground reads #F5F5F5 (Y 0.915)
# at the left edge and #EAEBEB (Y 0.828) under the object, so this ground sits
# inside it.
GROUND_HI = "#FCFAF4"
GROUND_MID = "#F3EDE1"
GROUND_LO = "#DED5C2"
GROUND_RIM = "#FFFDF8"       # the inner rim light every Tahoe tile carries
GROUND_VIGNETTE = "#8B7F66"
SHADOW = "#3B3327"           # warm — the corpus's cast shadows are warm even
                             # where the object casting them is cool

# ---------------------------------------------------------------- the graphite
# The whole commission is here. apple-12 (Calculator) is the corpus's dark-object-
# on-porcelain exemplar and its satin charcoal body measures #343233 against a
# #CECECC ground: **8.11:1**. apple-23 (Safari) is the corpus's dial-on-porcelain
# and takes the cheaper route, a saturated blue face at 2.01:1 (top) to 2.80:1
# (mid) — under the rubric's own 3:1, which is worth knowing before treating the
# reference as an authority. This dial takes apple-12's relation, not apple-23's.
#
# Pushed a touch warmer and darker than better-loop's rail (#5E6570→#1C2027, hue
# 212-228) so the two do not share a value as well as a shelf: hue here runs
# 218-222 at a lower lightness.
DIAL_HI = "#454B57"          # the domed face's lit crown
DIAL_MID = "#2C313A"
DIAL_LO = "#161A20"          # its shaded foot
DIAL_EDGE = "#0B0D11"        # the seat edge all round
BEZEL_HI = "#7C848F"         # the raised rim's top-left, where the key lands
BEZEL_MID = "#3D434C"
BEZEL_LO = "#191D23"         # its down-light side
BEZEL_CATCH = "#CBD3DE"      # the hairline the key leaves on a machined edge
FACE_BLOOM = "#8FA3BE"       # apple-23's dial reads as domed glass with a soft
                             # top bloom; this is that bloom, cool and very faint

# ---------------------------------------------------------------- the graduations
# Cream, not white. The ticks are value-separated rather than hue-separated, which
# is what apple-23 does and the reason its ticks survive 32px. On graphite they run
# about 9:1, so they are the free contrast in the tile.
TICK_MINOR = "#CFC6B0"
TICK_MAJOR = "#FFF8EA"

# ---------------------------------------------------------------- the needle
# Porcelain, the same material as the cushion, so the object carries the ground's
# own hue into its brightest element — the family's warm-neutral read. Against the
# graphite face it is the second thing the eye finds after the disc itself.
NEEDLE_HI = "#FFFCF4"
NEEDLE_MID = "#EFE8D8"
NEEDLE_LO = "#B9B09A"
NEEDLE_EDGE = "#7C7361"

# ---------------------------------------------------------------- the bearing
# Deliberately NOT the predecessor's hub. That was a 112px graphite disc with a
# 34px cream centre, and better-loop shipped the same part, which is how the two
# became one icon. This is a small steel collar around a graphite core: it holds
# the needle down and adds nothing to the small read.
HUB_HI = "#A9B2BE"
HUB_MID = "#6E7784"
HUB_LO = "#3A414A"
HUB_CORE = "#12151A"

# ---------------------------------------------------------------- the accent
# One warm hue, spent once, as one contiguous piece: the band plus the lug at its
# stopped end. Family band: report #E46235, whats-left #DF612E, deck-craft
# #DE5A28, better-loop #DE5A28, dossier-report #EA5B34 — kin to Fledgeling
# #C4622D. Corroborated against apple-05 (hue 9-32°, saturation 0.81-0.85) and
# apple-12, whose single bounded accent — the orange operator column — measures
# 2.29:1 against its own charcoal body and 3.54:1 against the ground. That is the
# same asymmetry this band has, and the corpus solves it the same way: the accent
# sits where it touches the pale ground.
ACCENT = "#DE5A28"
ACCENT_HI = "#F2823C"        # the lit end of the arc
ACCENT_DEEP = "#BC3A14"      # its shaded end. apple-05's darkest accent pixel is
                             # #D22D1E — still saturated, still warm, so a shaded
                             # warm face must not drift to brown or grey
ACCENT_SHADE = "#C9481C"     # the band's down-light end. #BC3A14 is the
                             # corpus's darkest accent pixel and at 58° of arc it
                             # drags the open end towards brown; this keeps the
                             # saturation and loses only the last few points of value
ACCENT_RIM = "#F6D3AC"       # apple-05's lightest accent pixel is #EDD0A3: the
                             # catch on a vermilion gel edge is warm cream, never
                             # white and never pink

# ---------------------------------------------------------------- the housing (a3)
HOUSE_HI = "#5A616C"
HOUSE_MID = "#343A43"
HOUSE_LO = "#1D2128"
HOUSE_EDGE = "#0E1115"


@dataclass
class Spec:
    """Every geometric decision in one place, so a round is a parameter edit."""

    variant: str = "a1"

    cx: float = 512.0
    cy: float = 470.0            # optical centring: the shadow falls down-right, so
                                 # the geometry sits high — and how high is the second
                                 # measured lever on shelf collision, after `scale`.
                                 # Swept against the worst 16px signature correlation
                                 # over the other 37 icons in the set:
                                 #   cy 526  0.830 braindump
                                 #   cy 498  0.810 geminify   (dead centre + 14)
                                 #   cy 486  0.805 geminify
                                 #   cy 478  0.800 geminify
                                 #   cy 470  0.797 shipyard
                                 #   cy 466  0.795 shipyard
                                 # 470 is the first setting with real headroom under
                                 # the 0.80 bar, and it costs 0.0006 of 16px contrast.
                                 # The lift is 42px on a 1024 canvas — inside what the
                                 # cast shadow's own reach below the disc accounts
                                 # for, so the composition reads no higher.
    r_face: float = 282.0        # the graphite face
    bezel: float = 36.0          # the raised rim's radial thickness. Outer radius
                                 # is r_face + bezel = 322, so the object is 644px
                                 # = 62.9% of the tile, inside the grammar's 55-65%
    r_tick_out: float = 262.0
    tick_minor: float = 15.0
    tick_major: float = 42.0
    tick_a0: float = -172.0      # the scale runs from the lower left, clockwise, and
    tick_a1: float = -27.0       # stops where the band starts. A graduation ring that
                                 # closes all the way round is a clock face, and the
                                 # first two rounds here shipped exactly that: a full
                                 # 36-tick ring with a pale needle near vertical reads
                                 # as a stopwatch at every size. An open sector in the
                                 # lower right makes it an instrument with a travel
                                 # direction, and the direction is what the icon is about
    tick_step: float = 10.0      # degrees between graduations
    tick_major_every: int = 3
    band_a0: float = -21.0       # the accept band's stopped (counter-clockwise) end
    band_a1: float = 37.0        # its open end — the headroom above the mark
    band_r_in: float = 202.0     # how deep the band cuts into the face. THIS is the
                                 # measurement that decides whether the icon has an
                                 # accent at 16px. Authored first as a 36px-thick
                                 # inlay in the bezel only, the band was 0.56px thick
                                 # at 16px and simply was not there: the tile rendered
                                 # as a plain dark disc and the whole device was gone
                                 # exactly where it has to survive. At 116px deep it
                                 # is 1.8px at 16px and reads
    pawl_w: float = 46.0         # the stop's inner wall, tangentially
    boss_w: float = 96.0         # its boss on the rim. Wide and short: the same part
                                 # at 54 wide and 32 proud read as a stick poking out
                                 # of the dial rather than as a boss cast into it
    boss_proud: float = 22.0     # how far it stands past the bezel. Swept at 14 / 22
                                 # / 38 against the 32px render: under about 16 it is
                                 # a bump and the circle still reads as closed, over
                                 # about 32 it reads as a second object stuck on
    needle_deg: float = 8.0      # inside the band, clear of the lug. Dead vertical
                                 # reads as a static speedometer; 4° off says the
                                 # needle came to rest somewhere specific
    needle_reach: float = 252.0
    needle_half: float = 30.0    # half-width at the hub — a gauge pointer is
                                 # stubbier than a clock hand, and that is most of
                                 # what separates the two reads
    needle_tail: float = 76.0
    r_hub: float = 58.0
    r_core: float = 24.0
    scale: float = 0.96          # one knob on the whole instrument's diameter, and
                                 # the measured lever on how much this tile reads as
                                 # its neighbours. Swept against the worst 16px
                                 # signature correlation across the other 37 icons in
                                 # the set, and against its own 16px RMS contrast:
                                 #   scale  width   RMS      worst pair
                                 #   0.84   52.3%   0.2710   0.871 proctor
                                 #   0.88   55.1%   0.2792   0.853 proctor
                                 #   0.92   57.8%   0.2867   0.827 proctor
                                 #   0.94   58.6%   0.2902   0.811 proctor
                                 #   0.96   60.2%   0.2935   0.810 geminify
                                 #   0.98   60.9%   0.2967   0.821 tui-craft
                                 #   1.00   62.5%   0.2998   0.840 mockup-fidelity
                                 # No setting clears the 0.80 collision bar: shrink
                                 # the disc and the flag moves from the dark-slab
                                 # cluster onto proctor's dark box rather than going
                                 # away, which is the structural convergence
                                 # shelf_check's own docstring predicts — porcelain,
                                 # one warm accent and a volumetric object leave
                                 # shape and accent placement as the only axes. 0.96
                                 # is where the worst pair is least bad, sits
                                 # mid-grammar on the 55-65% focal band, and gives up
                                 # 0.006 of contrast. Note the direction too:
                                 # ux-craft's commission scaled its object UP to buy
                                 # contrast, and the same knob run the other way buys
                                 # distinctiveness. Publish the curve rather than
                                 # defending a size.
    cast_dx: float = 11.0
    cast_dy: float = 21.0
    cast_blur: float = 19.0
    cast_opacity: float = 0.36
    # a2 only — the pale face inside a graphite bezel ring
    ring_thick: float = 84.0
    # a3 only — the housing the dial is sunk into
    house_top: float = 636.0
    house_lip: float = 26.0
    bleed: float = 64.0

    @property
    def r_out(self) -> float:
        return self.r_face + self.bezel

    @property
    def r_tick_in_minor(self) -> float:
        return self.r_tick_out - self.tick_minor

    @property
    def r_tick_in_major(self) -> float:
        return self.r_tick_out - self.tick_major


# --------------------------------------------------------------------- geometry


def polar(sp: Spec, r: float, deg: float) -> tuple[float, float]:
    """0° is 12 o'clock, positive clockwise — the way a gauge is read."""
    a = math.radians(deg - 90.0)
    return sp.cx + r * math.cos(a), sp.cy + r * math.sin(a)


def arc(sp: Spec, r: float, a0: float, a1: float, sweep: int = 1) -> str:
    x0, y0 = polar(sp, r, a0)
    x1, y1 = polar(sp, r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {large} {sweep} {x1:.1f},{y1:.1f}"


def sector(sp: Spec, r_in: float, r_out: float, a0: float, a1: float) -> str:
    """A closed annular sector — the band and the tick-ring wedges are these."""
    ox0, oy0 = polar(sp, r_out, a0)
    ox1, oy1 = polar(sp, r_out, a1)
    ix1, iy1 = polar(sp, r_in, a1)
    ix0, iy0 = polar(sp, r_in, a0)
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f"M{ox0:.1f},{oy0:.1f} "
            f"A{r_out:.1f},{r_out:.1f} 0 {large} 1 {ox1:.1f},{oy1:.1f} "
            f"L{ix1:.1f},{iy1:.1f} "
            f"A{r_in:.1f},{r_in:.1f} 0 {large} 0 {ix0:.1f},{iy0:.1f} Z")


def band_path(sp: Spec) -> str:
    """The accept band: a wedge cut through the graduations and out to the rim."""
    return sector(sp, sp.band_r_in, sp.r_out, sp.band_a0, sp.band_a1)


def _bar(sp: Spec, deg: float, r0: float, r1: float, half: float) -> str:
    """A constant-width radial bar. Not a sector: a sector fans outward and the
    first pawl here read as a folded ribbon tab at every size, because a machined
    stop has parallel flanks and that is the whole difference between hardware and
    a bookmark."""
    a = math.radians(deg - 90.0)
    ux, uy = math.cos(a), math.sin(a)          # outward, along the bar's axis
    px, py = -uy, ux                           # across it
    pts = [(sp.cx + ux * r0 + px * half, sp.cy + uy * r0 + py * half),
           (sp.cx + ux * r1 + px * half, sp.cy + uy * r1 + py * half),
           (sp.cx + ux * r1 - px * half, sp.cy + uy * r1 - py * half),
           (sp.cx + ux * r0 - px * half, sp.cy + uy * r0 - py * half)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def pawl_path(sp: Spec) -> str:
    """The stop's inner wall: it caps the band's counter-clockwise end.

    Graphite rather than a second warm piece, for two reasons. The accent is spent
    once, and the band is the semantic element — the window the reading has to be
    inside — while the pawl is hardware. And a dark bar across a warm wedge is the
    highest-contrast edge in the tile, so the one place the boundary is closed is
    also the one place it is unmissable at 32px.
    """
    return _bar(sp, sp.band_a0, sp.band_r_in - 12, sp.r_out - 2, sp.pawl_w / 2)


def boss_path(sp: Spec) -> str:
    """The stop's outer boss, on and proud of the rim.

    It stands proud deliberately. A stop flush with the bezel is a tick and the
    circle still reads as closed, and a closed circle is what every other ring in
    this family already is — the silhouette break is what stops this tile reading
    as `mac-doctor` or `be-my-witness` at 32px. Short and wide rather than long and
    narrow: at 54px wide and 32px proud the same part read as a stick poking out of
    the dial.
    """
    return _bar(sp, sp.band_a0, sp.r_out - sp.bezel * 0.5,
                sp.r_out + sp.boss_proud, sp.boss_w / 2)


def pawl_flank(sp: Spec, r0: float, r1: float, half: float, side: int) -> str:
    """One flank of the stop, over a given radial span.

    The span matters: authored once as a single line from the wall's foot to the
    boss's crown at the *boss's* half-width, the catch floated clear of the wall
    for the whole inner half of its length and rendered at 256px as a stray pale
    rectangle beside the block. A flank belongs to one part.
    """
    a = math.radians(sp.band_a0 - 90.0)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    return (f"M{sp.cx + ux * r0 + px * half * side:.1f},"
            f"{sp.cy + uy * r0 + py * half * side:.1f} "
            f"L{sp.cx + ux * r1 + px * half * side:.1f},"
            f"{sp.cy + uy * r1 + py * half * side:.1f}")


def needle_path(sp: Spec) -> str:
    """A tapered blade with a short counterweight tail, so it reads as an
    instrument needle rather than as a stroke drawn from the centre."""
    d = sp.needle_deg
    tip = polar(sp, sp.needle_reach, d)
    l = polar(sp, sp.needle_half, d - 90.0)
    r = polar(sp, sp.needle_half, d + 90.0)
    tail_l = polar(sp, sp.needle_tail, d + 180.0 - 9.0)
    tail_r = polar(sp, sp.needle_tail, d + 180.0 + 9.0)
    return (f"M{tip[0]:.1f},{tip[1]:.1f} L{r[0]:.1f},{r[1]:.1f} "
            f"L{tail_r[0]:.1f},{tail_r[1]:.1f} L{tail_l[0]:.1f},{tail_l[1]:.1f} "
            f"L{l[0]:.1f},{l[1]:.1f} Z")


def axis_points(x0: float, y0: float, x1: float, y1: float,
                spread: float = 0.62) -> tuple[float, ...]:
    """Start and end of the key light's axis across a box, in user space.

    Every face gradient hangs on this one axis so the parts read as one object
    under one light rather than as adjacent panels — anvil-errand's finding, which
    cost that commission a round to learn.
    """
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lx, ly = LIGHT_AXIS
    r = max(x1 - x0, y1 - y0) * spread
    return (cx + lx * r, cy - ly * r, cx - lx * r, cy + ly * r)


def ticks(sp: Spec, minor: str, major: str) -> list[str]:
    out = []
    n = int(round((sp.tick_a1 - sp.tick_a0) / sp.tick_step)) + 1
    for i in range(n):
        deg = sp.tick_a1 - i * sp.tick_step
        is_major = i % sp.tick_major_every == 0
        r_in = sp.r_tick_in_major if is_major else sp.r_tick_in_minor
        x1, y1 = polar(sp, sp.r_tick_out, deg)
        x2, y2 = polar(sp, r_in, deg)
        out.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{major if is_major else minor}" '
            f'stroke-width="{11.0 if is_major else 6.0}" stroke-linecap="round" '
            f'stroke-opacity="{0.92 if is_major else 0.50}"/>')
    return out


def rounded(x: float, y: float, w: float, h: float, r: float) -> str:
    r = min(r, w / 2, h / 2)
    return (f"M{x + r:.1f},{y:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} v{h - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{r:.1f} h{-(w - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{-r:.1f} v{-(h - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{-r:.1f} z")


# ------------------------------------------------------------------------ build


def defs(sp: Spec, squircle: str) -> list[str]:
    d: list[str] = ["<defs>"]
    d.append(f'<radialGradient id="cushion" cx="0.38" cy="0.26" r="0.90">'
             f'<stop offset="0" stop-color="{GROUND_HI}"/>'
             f'<stop offset="0.54" stop-color="{GROUND_MID}"/>'
             f'<stop offset="1" stop-color="{GROUND_LO}"/></radialGradient>')
    d.append(f'<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">'
             f'<stop offset="0.54" stop-color="{GROUND_VIGNETTE}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{GROUND_VIGNETTE}" stop-opacity="0.24"/>'
             f'</radialGradient>')

    box = (sp.cx - sp.r_out, sp.cy - sp.r_out, sp.cx + sp.r_out, sp.cy + sp.r_out)

    # the raised rim: a torus, so its value range is wider than the face's
    ax = axis_points(*box, spread=0.52)
    d.append(f'<linearGradient id="bezel" gradientUnits="userSpaceOnUse" '
             f'x1="{ax[0]:.1f}" y1="{ax[1]:.1f}" x2="{ax[2]:.1f}" y2="{ax[3]:.1f}">'
             f'<stop offset="0" stop-color="{BEZEL_HI}"/>'
             f'<stop offset="0.42" stop-color="{BEZEL_MID}"/>'
             f'<stop offset="1" stop-color="{BEZEL_LO}"/></linearGradient>')

    # the face: domed glass, lighter at the crown — apple-23's construction
    axf = axis_points(*box, spread=0.72)
    d.append(f'<linearGradient id="face" gradientUnits="userSpaceOnUse" '
             f'x1="{axf[0]:.1f}" y1="{axf[1]:.1f}" x2="{axf[2]:.1f}" y2="{axf[3]:.1f}">'
             f'<stop offset="0" stop-color="{DIAL_HI}"/>'
             f'<stop offset="0.46" stop-color="{DIAL_MID}"/>'
             f'<stop offset="1" stop-color="{DIAL_LO}"/></linearGradient>')
    d.append(f'<radialGradient id="dome" cx="0.34" cy="0.19" r="0.60">'
             f'<stop offset="0" stop-color="{FACE_BLOOM}" stop-opacity="0.30"/>'
             f'<stop offset="1" stop-color="{FACE_BLOOM}" stop-opacity="0"/>'
             f'</radialGradient>')

    # the porcelain face used by a2 and a3
    d.append(f'<radialGradient id="pale" cx="0.40" cy="0.24" r="0.78">'
             f'<stop offset="0" stop-color="#FFFDF7"/>'
             f'<stop offset="0.58" stop-color="#F6F1E5"/>'
             f'<stop offset="1" stop-color="#DCD3C0"/></radialGradient>')

    # the accent, on the same axis as everything else
    bx = axis_points(*box, spread=0.46)
    d.append(f'<linearGradient id="band" gradientUnits="userSpaceOnUse" '
             f'x1="{bx[0]:.1f}" y1="{bx[1]:.1f}" x2="{bx[2]:.1f}" y2="{bx[3]:.1f}">'
             f'<stop offset="0" stop-color="{ACCENT_HI}"/>'
             f'<stop offset="0.52" stop-color="{ACCENT}"/>'
             f'<stop offset="1" stop-color="{ACCENT_SHADE}"/></linearGradient>')

    nb = (sp.cx - sp.needle_reach, sp.cy - sp.needle_reach,
          sp.cx + sp.needle_reach, sp.cy + sp.needle_reach)
    axn = axis_points(*nb, spread=0.40)
    d.append(f'<linearGradient id="needle" gradientUnits="userSpaceOnUse" '
             f'x1="{axn[0]:.1f}" y1="{axn[1]:.1f}" x2="{axn[2]:.1f}" y2="{axn[3]:.1f}">'
             f'<stop offset="0" stop-color="{NEEDLE_HI}"/>'
             f'<stop offset="0.50" stop-color="{NEEDLE_MID}"/>'
             f'<stop offset="1" stop-color="{NEEDLE_LO}"/></linearGradient>')
    d.append(f'<linearGradient id="darkneedle" gradientUnits="userSpaceOnUse" '
             f'x1="{axn[0]:.1f}" y1="{axn[1]:.1f}" x2="{axn[2]:.1f}" y2="{axn[3]:.1f}">'
             f'<stop offset="0" stop-color="{DIAL_HI}"/>'
             f'<stop offset="0.50" stop-color="{DIAL_MID}"/>'
             f'<stop offset="1" stop-color="#0E1116"/></linearGradient>')

    px = axis_points(sp.cx - sp.r_out, sp.cy - sp.r_out, sp.cx + sp.r_out,
                     sp.cy + sp.r_out, spread=0.30)
    d.append(f'<linearGradient id="pawl" gradientUnits="userSpaceOnUse" '
             f'x1="{px[0]:.1f}" y1="{px[1]:.1f}" x2="{px[2]:.1f}" y2="{px[3]:.1f}">'
             f'<stop offset="0" stop-color="{DIAL_HI}"/>'
             f'<stop offset="0.46" stop-color="{DIAL_MID}"/>'
             f'<stop offset="1" stop-color="#0E1116"/></linearGradient>')

    hb = (sp.cx - sp.r_hub, sp.cy - sp.r_hub, sp.cx + sp.r_hub, sp.cy + sp.r_hub)
    axh = axis_points(*hb, spread=0.70)
    d.append(f'<linearGradient id="hub" gradientUnits="userSpaceOnUse" '
             f'x1="{axh[0]:.1f}" y1="{axh[1]:.1f}" x2="{axh[2]:.1f}" y2="{axh[3]:.1f}">'
             f'<stop offset="0" stop-color="{HUB_HI}"/>'
             f'<stop offset="0.50" stop-color="{HUB_MID}"/>'
             f'<stop offset="1" stop-color="{HUB_LO}"/></linearGradient>')

    hx = axis_points(-sp.bleed, sp.house_top, S + sp.bleed, S + 200, spread=0.40)
    d.append(f'<linearGradient id="house" gradientUnits="userSpaceOnUse" '
             f'x1="{hx[0]:.1f}" y1="{hx[1]:.1f}" x2="{hx[2]:.1f}" y2="{hx[3]:.1f}">'
             f'<stop offset="0" stop-color="{HOUSE_HI}"/>'
             f'<stop offset="0.44" stop-color="{HOUSE_MID}"/>'
             f'<stop offset="1" stop-color="{HOUSE_LO}"/></linearGradient>')

    d.append(f'<filter id="cast" x="-45%" y="-45%" width="200%" height="210%">'
             f'<feDropShadow dx="{sp.cast_dx}" dy="{sp.cast_dy}" '
             f'stdDeviation="{sp.cast_blur}" flood-color="{SHADOW}" '
             f'flood-opacity="{sp.cast_opacity}"/></filter>')
    d.append(f'<filter id="castneedle" x="-70%" y="-70%" width="250%" height="250%">'
             f'<feDropShadow dx="7" dy="13" stdDeviation="9" flood-color="#05070A" '
             f'flood-opacity="0.44"/></filter>')
    d.append('<filter id="soften" x="-140%" y="-140%" width="380%" height="380%">'
             '<feGaussianBlur stdDeviation="14"/></filter>')
    d.append('<filter id="soften-tight" x="-140%" y="-140%" width="380%" height="380%">'
             '<feGaussianBlur stdDeviation="6"/></filter>')

    d.append(f'<clipPath id="faceclip"><circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" '
             f'r="{sp.r_face:.1f}"/></clipPath>')
    d.append(f'<clipPath id="tile"><path d="{squircle}"/></clipPath>')
    d.append("</defs>")
    return d


def band_group(sp: Spec) -> list[str]:
    """The accept band, as a wedge cut through the graduations out to the rim, and
    the graphite pawl closing its counter-clockwise end.

    Both sit on the object's silhouette edge rather than as linework inside a light
    field. That is the acid test better-loop's commission bought with a rejected
    direction, and it is why the accent still reads at 16px here where the
    predecessor's floating bracket arc did not.
    """
    out: list[str] = []
    band = band_path(sp)
    out.append(f'<path d="{band}" fill="url(#band)"/>')
    # the warm-cream catch along the outer arc — the corpus's lightest pixel on a
    # vermilion gel edge is #EDD0A3, so this is cream and not white
    out.append(f'<path d="{arc(sp, sp.r_out - 4, sp.band_a0, sp.band_a1)}" '
               f'fill="none" stroke="{ACCENT_RIM}" stroke-width="6" '
               f'stroke-opacity="0.88"/>')
    # its seat against the face, in the accent's own shaded value rather than
    # graphite: a graphite seam here reads at 256px as a gap between the two
    out.append(f'<path d="{arc(sp, sp.band_r_in + 3, sp.band_a0, sp.band_a1)}" '
               f'fill="none" stroke="{ACCENT_DEEP}" stroke-width="5" '
               f'stroke-opacity="0.8"/>')
    # the wedge's open end, cut square: this is the side the reading came in from,
    # so it gets an edge and not a stop
    e0 = polar(sp, sp.band_r_in + 2, sp.band_a1)
    e1 = polar(sp, sp.r_out - 2, sp.band_a1)
    out.append(f'<path d="M{e0[0]:.1f},{e0[1]:.1f} L{e1[0]:.1f},{e1[1]:.1f}" '
               f'fill="none" stroke="{ACCENT_DEEP}" stroke-width="4" '
               f'stroke-opacity="0.55"/>')
    return out


def pawl_group(sp: Spec) -> list[str]:
    """The stop, in two parts through the rim: the wall that caps the band, and the
    boss standing proud of the bezel. One material, one gradient axis, so they read
    as one abutment cast through the body rather than as two parts bolted on."""
    out: list[str] = []
    wall, boss = pawl_path(sp), boss_path(sp)
    out.append(f'<path d="{wall}" fill="url(#pawl)"/>')
    out.append(f'<path d="{boss}" fill="url(#pawl)"/>')
    out.append(f'<path d="{wall}" fill="none" stroke="{DIAL_EDGE}" '
               f'stroke-width="3.5" stroke-opacity="0.85"/>')
    out.append(f'<path d="{boss}" fill="none" stroke="{DIAL_EDGE}" '
               f'stroke-width="3.5" stroke-opacity="0.9"/>')
    # the machined catch down each part's up-light flank only — the key is up-light
    # of the crown, so the down-light flanks get nothing
    wall_r = (sp.band_r_in - 6, sp.r_out - 4)
    boss_r = (sp.r_out - sp.bezel * 0.5 + 3, sp.r_out + sp.boss_proud - 5)
    out.append(f'<path d="{pawl_flank(sp, *wall_r, sp.pawl_w / 2 - 4, -1)}" '
               f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="4" '
               f'stroke-opacity="0.5" stroke-linecap="round"/>')
    out.append(f'<path d="{pawl_flank(sp, *boss_r, sp.boss_w / 2 - 5, -1)}" '
               f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="5" '
               f'stroke-opacity="0.66" stroke-linecap="round"/>')
    # and across the boss's outer face, which the key reaches square on
    a = math.radians(sp.band_a0 - 90.0)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    h = sp.boss_w / 2 - 5
    r = sp.r_out + sp.boss_proud - 4
    out.append(f'<path d="M{sp.cx + ux * r - px * h:.1f},{sp.cy + uy * r - py * h:.1f} '
               f'L{sp.cx + ux * r + px * h:.1f},{sp.cy + uy * r + py * h:.1f}" '
               f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="5" '
               f'stroke-opacity="0.5" stroke-linecap="round"/>')
    # the warm bounce the band throws onto the wall's down-light flank. Tight and
    # bright, in the pale spill hue: at the accent's own hue over graphite it reads
    # as rust rather than as light (better-loop's round 5).
    out.append(f'<path d="{pawl_flank(sp, sp.band_r_in + 4, sp.r_out - 8, sp.pawl_w / 2 - 3, 1)}" '
               f'fill="none" stroke="{ACCENT_RIM}" stroke-width="7" '
               f'stroke-opacity="0.40" filter="url(#soften-tight)"/>')
    return out


def build(sp: Spec) -> str:
    squircle = SQUIRCLE_PATH.read_text().strip()
    out: list[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" '
                      f'height="{S}" viewBox="0 0 {S} {S}">']
    out += defs(sp, squircle)
    add = out.append

    add('<g clip-path="url(#tile)">')

    # -------------------------------------------------------------------- bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#cushion)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vignette)"/>')
    add(f'<path d="{squircle}" fill="none" stroke="{GROUND_RIM}" stroke-width="7" '
        f'stroke-opacity="0.85"/>')
    add("</g>")

    # ------------------------------------------------------------------- mid
    # The instrument: the disc, its graduations, and the band the reading has to
    # be inside.
    add('<g id="mid">')

    # what the instrument casts on the cushion. One light, so one direction; the
    # lug casts too, because it stands proud of the rim and a stop with no shadow
    # reads as a printed mark rather than as a part.
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_out:.1f}" '
        f'fill="{SHADOW}" filter="url(#cast)"/>')
    add(f'<path d="{pawl_path(sp)}" fill="{SHADOW}" filter="url(#cast)"/>')

    # the raised rim
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_out:.1f}" '
        f'fill="url(#bezel)"/>')
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_out:.1f}" '
        f'fill="none" stroke="{DIAL_EDGE}" stroke-width="3" stroke-opacity="0.8"/>')

    if sp.variant == "a2":
        # a graphite bezel RING around a porcelain face: the value relation the
        # commission was asked to sweep against a1's filled dark face
        r_in = sp.r_out - sp.ring_thick
        add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{r_in:.1f}" '
            f'fill="url(#pale)"/>')
        add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{r_in:.1f}" '
            f'fill="none" stroke="{DIAL_EDGE}" stroke-width="5" '
            f'stroke-opacity="0.55"/>')
        # occlusion where the pale pan meets the rim on the up-light side
        add('<g clip-path="url(#faceclip)">')
        add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy - 12:.1f}" r="{r_in - 4:.1f}" '
            f'fill="none" stroke="{SHADOW}" stroke-width="26" stroke-opacity="0.14" '
            f'filter="url(#soften-tight)"/>')
        add("</g>")
        sp_ticks = replace(sp, r_tick_out=r_in - 26, tick_minor=13, tick_major=34)
        for t in ticks(sp_ticks, "#A99B7E", "#4A4436"):
            add(t)
    else:
        add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_face:.1f}" '
            f'fill="url(#face)"/>')
        # the domed-glass bloom apple-23 carries at the crown, kept faint
        add('<g clip-path="url(#faceclip)">')
        add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_face:.1f}" '
            f'fill="url(#dome)"/>')
        add("</g>")
        # the terminator where the dome falls away from the key, down-light side.
        # Authored as a ring offset UP-light so what survives the clip is the far
        # arc: an inner shadow on the up-light side instead would fight the face
        # gradient, and two planes disagreeing about where the lamp is costs #8.
        add('<g clip-path="url(#faceclip)">')
        add(f'<circle cx="{sp.cx - 9:.1f}" cy="{sp.cy - 17:.1f}" '
            f'r="{sp.r_face - 10:.1f}" fill="none" stroke="#05070A" '
            f'stroke-width="34" stroke-opacity="0.26" filter="url(#soften-tight)"/>')
        add("</g>")
        for t in ticks(sp, TICK_MINOR, TICK_MAJOR):
            add(t)

    # the machined catch along the rim's lit arc — what makes graphite read as cut
    add(f'<path d="{arc(sp, sp.r_out - 4.5, -150.0, -36.0)}" fill="none" '
        f'stroke="{BEZEL_CATCH}" stroke-width="6" stroke-opacity="0.78" '
        f'stroke-linecap="round"/>')
    # the turned rim's inner lip, continuous all the way round. Salvaged from both
    # engine takes: the Arrow vector and the GPT-Image raster each drew the bezel as
    # a complete pale annulus, and that unbroken line is what makes a rim read as
    # turned on a lathe. The master had the catch on the lit arc only, so the rim
    # read as a highlight rather than as a part — a full-circle hairline at a sixth
    # of the lit arc's opacity is the whole fix.
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_face + 5:.1f}" '
        f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="3" '
        f'stroke-opacity="0.13"/>')
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_face + 1.5:.1f}" '
        f'fill="none" stroke="{DIAL_EDGE}" stroke-width="4" '
        f'stroke-opacity="0.45"/>')
    add(f'<path d="{arc(sp, sp.r_face + 5, -140.0, -42.0)}" fill="none" '
        f'stroke="{BEZEL_CATCH}" stroke-width="3.5" stroke-opacity="0.30" '
        f'stroke-linecap="round"/>')

    # the travel: one engraved groove from the foot of the scale to the band's open
    # end. It is what fills the dial without adding graduations, and it says the
    # motion was one-way — the empty sector clockwise of the band is the part of the
    # circle the reading never visits.
    if sp.variant != "a2":
        add(f'<path d="{arc(sp, sp.band_r_in - 10, sp.tick_a0, sp.band_a1)}" '
            f'fill="none" stroke="#05070A" stroke-width="10" '
            f'stroke-opacity="0.50" stroke-linecap="round"/>')
        add(f'<path d="{arc(sp, sp.band_r_in - 6.5, sp.tick_a0, sp.band_a1)}" '
            f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="2.5" '
            f'stroke-opacity="0.14" stroke-linecap="round"/>')

    for line in band_group(sp):
        add(line)
    for line in pawl_group(sp):
        add(line)

    # the rim's seat edge, re-run AFTER the band and the boss. Measured: the band's
    # own vermilion reads 2.46:1 against this very pale porcelain — a warm gel object
    # is squeezed between a Y 0.84 ground and a Y 0.08 body and cannot clear 3:1
    # against both. The corpus does not solve that with a value; apple-12 puts its
    # orange keys inside a charcoal body, so the boundary the eye uses is the body's
    # edge at 12:1 rather than the accent's own. Running the seat edge over the band
    # buys exactly that, and costs nothing.
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_out:.1f}" '
        f'fill="none" stroke="{DIAL_EDGE}" stroke-width="4" stroke-opacity="0.7"/>')

    if sp.variant == "a3":
        hx0, hx1 = -sp.bleed, S + sp.bleed
        house = (f"M{hx0:.1f},{sp.house_top:.1f} H{hx1:.1f} "
                 f"V{S + 200:.1f} H{hx0:.1f} Z")
        add(f'<path d="{house}" fill="url(#house)"/>')
        add(f'<path d="M{hx0:.1f},{sp.house_top:.1f} H{hx1:.1f}" fill="none" '
            f'stroke="{HOUSE_EDGE}" stroke-width="4" stroke-opacity="0.7"/>')
        add(f'<path d="M{hx0:.1f},{sp.house_top + sp.house_lip:.1f} H{hx1:.1f}" '
            f'fill="none" stroke="{BEZEL_CATCH}" stroke-width="4" '
            f'stroke-opacity="0.35"/>')
        add(f'<path d="M{hx0:.1f},{sp.house_top + 2.5:.1f} H{hx1:.1f}" fill="none" '
            f'stroke="{BEZEL_CATCH}" stroke-width="4.5" stroke-opacity="0.6"/>')

    add("</g>")

    # -------------------------------------------------------------------- fg
    # The reading: the needle, at rest inside the band with the stop behind it.
    add('<g id="fg">')
    npath = needle_path(sp)
    fill = "url(#darkneedle)" if sp.variant == "a2" else "url(#needle)"
    edge = "#050709" if sp.variant == "a2" else NEEDLE_EDGE
    add(f'<path d="{npath}" fill="#05070A" filter="url(#castneedle)" '
        f'opacity="0.7"/>')
    add(f'<path d="{npath}" fill="{fill}"/>')
    add(f'<path d="{npath}" fill="none" stroke="{edge}" stroke-width="2.5" '
        f'stroke-opacity="0.55"/>')

    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_hub:.1f}" '
        f'fill="url(#hub)"/>')
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_hub:.1f}" '
        f'fill="none" stroke="#0A0D11" stroke-width="3" stroke-opacity="0.7"/>')
    add(f'<circle cx="{sp.cx:.1f}" cy="{sp.cy:.1f}" r="{sp.r_core:.1f}" '
        f'fill="{HUB_CORE}"/>')
    add("</g>")

    # -------------------------------------------------------------- highlight
    add('<g id="highlight">')
    # the key's catch along the needle's up-light flank
    d = sp.needle_deg
    ctip = polar(sp, sp.needle_reach - 8, d)
    cbase = polar(sp, sp.needle_half + 4, d - 84.0)
    add(f'<path d="M{cbase[0]:.1f},{cbase[1]:.1f} L{ctip[0]:.1f},{ctip[1]:.1f}" '
        f'fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.55" '
        f'stroke-linecap="round"/>')
    # the bearing's specular crescent
    add(f'<path d="{arc(sp, sp.r_hub - 8, -150.0, -60.0)}" fill="none" '
        f'stroke="#FFFFFF" stroke-width="5" stroke-opacity="0.5" '
        f'stroke-linecap="round"/>')
    # the band's own faint spill into the daylight just outside the rim. Warm, and
    # tight: widen it and the porcelain beside the accent goes muddy with every hex
    # still correct — better-loop's round 5.
    mid_band = (sp.band_a0 + sp.band_a1) / 2
    gx, gy = polar(sp, sp.r_out + 20, mid_band)
    add(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="72" ry="27" fill="{ACCENT}" '
        f'fill-opacity="0.075" filter="url(#soften)" '
        f'transform="rotate({mid_band:.1f} {gx:.1f} {gy:.1f})"/>')
    add("</g>")

    add("</g>")   # tile
    add("</svg>")
    return "\n".join(out)


NUMERIC = {"cx", "cy", "r_face", "bezel", "r_tick_out", "tick_minor", "tick_major",
           "tick_a0", "tick_a1", "tick_step", "band_a0", "band_a1", "band_r_in",
           "pawl_w", "boss_w", "boss_proud", "scale", "needle_deg", "needle_reach",
           "needle_half", "needle_tail", "r_hub", "r_core", "cast_dx", "cast_dy",
           "cast_blur", "cast_opacity", "ring_thick", "house_top", "house_lip",
           "bleed"}

PRESETS = {
    "a1": {},
    "a2": {"ring_thick": 84.0, "needle_reach": 214.0, "r_hub": 52.0},
    "a3": {"cy": 452.0, "r_face": 268.0, "bezel": 28.0, "r_tick_out": 238.0,
           "needle_reach": 228.0, "house_top": 636.0, "boss_proud": 22.0},
}


# Every radial dimension, so one knob sizes the whole instrument. This exists
# because the object's diameter turned out to be the single lever on shelf
# distinctiveness, and hand-scaling fourteen constants to move it is how a sweep
# stops being reproducible.
RADIAL = ("r_face", "bezel", "r_tick_out", "tick_minor", "tick_major", "band_r_in",
          "pawl_w", "boss_w", "boss_proud", "scale", "needle_reach", "needle_half",
          "needle_tail", "r_hub", "r_core")


def spec_for(variant: str, overrides: dict[str, float]) -> Spec:
    sp = replace(Spec(), variant=variant, **PRESETS[variant])
    if overrides:
        sp = replace(sp, **overrides)
    if sp.scale != 1.0:
        sp = replace(sp, **{k: getattr(sp, k) * sp.scale for k in RADIAL})
    return sp


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="a1", choices=sorted(PRESETS))
    ap.add_argument("--out", default=None)
    ap.add_argument("--set", action="append", default=[],
                    help="override a numeric Spec field, e.g. --set band_a1=42")
    a = ap.parse_args()
    ov: dict[str, float] = {}
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in NUMERIC:
            raise SystemExit(f"unknown or non-numeric field: {k}")
        ov[k] = float(v)
    sp = spec_for(a.variant, ov)
    out = Path(a.out) if a.out else HERE / "icon.svg"
    out.write_text(build(sp))
    print(f"wrote {out}  (variant {a.variant})")


if __name__ == "__main__":
    main()
