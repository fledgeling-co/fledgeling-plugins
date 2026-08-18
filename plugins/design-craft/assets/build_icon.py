#!/usr/bin/env python3
"""Build the design-craft icon master.

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel
objects. Device: **the sample fan** — three material leaves pinned on one rivet,
splayed. Two of them cluster 19 degrees apart in matte slate and frosted cream;
the third stands 40 degrees clear of both and is the only one finished, poured in
vermilion gel with its specular, its rim catch and its own contact shadow.

The signature move is the *gap*. A category's rut and its predictable opposite
are the same neighbourhood, so the two rejects sit next to each other; the
committed direction is the one that leaves the neighbourhood. That gap is a hole
in the silhouette rather than a difference in colour, so it survives to 16px,
where the read is a hot leaf standing apart from a pale pair.

Only the chosen leaf carries specular, bloom and a full contact shadow: three
material families explored, one taken to finish. That is design-craft's first
claim — name the rut, derive past it and its obvious opposite, commit to one
direction — performed by the artwork instead of illustrated by it.

Everything geometric or material is a named constant, so a fidelity round is a
parameter edit and a banner can be derived from the same numbers:
LIGHT_ANGLE_DEG / LIGHT_AXIS for the light, Spec.leaf_w / leaf_len / top_r /
base_taper for the cell, Spec.rut_deg / opposite_deg / committed_deg for the splay,
and ACCENT / ACCENT_HI / ACCENT_DEEP for the one warm hue. `placement()` derives the
rivet from the splay, so the fan re-centres itself when any angle moves.

    python3 build_icon.py                        # writes icon.svg beside this file
    python3 build_icon.py --set committed_deg=22 --out /tmp/try.svg
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
# One soft key light from above, a little to the left. Sampled rather than
# chosen: across the porcelain corpus captures (apple-23/26/28/31) the brightest
# 0.5% of the tile sits at x = 0.43-0.50, y = 0.01-0.03 of the tile box.
# Every ramp, rim, cast and bounce reads this pair, so a derived banner can light
# itself from the same two numbers.
LIGHT_ANGLE_DEG = 112.0
LIGHT_AXIS = (math.cos(math.radians(LIGHT_ANGLE_DEG)),
              math.sin(math.radians(LIGHT_ANGLE_DEG)))      # ≈ (-0.375, +0.927)
# Unit vector from a surface toward the shade — the direction every shadow falls.
SHADE_DIR = (-LIGHT_AXIS[0], LIGHT_AXIS[1])

# ---------------------------------------------------------------- the cushion
# Porcelain/daylight, sampled off the family's shipped tiles rather than
# invented: deck-craft #FAF7F0→#EDE7DA, proctor #FBF9F3→#EFEADF,
# whats-left #FCFAF6→#EFEBE0, create-test-suite #F7F4EC→#E8E2D5.
GROUND_HI = "#FDFAF4"
GROUND_MID = "#F0EADD"
GROUND_LO = "#DCD3C0"
GROUND_RIM = "#FFFDF8"       # the inner rim light every Tahoe tile carries
GROUND_VIGNETTE = "#8B7F66"
SHADOW = "#3B3327"           # warm, never blue — the corpus's shaded faces are warm

# ---------------------------------------------------------------- the accent
# One warm hue, spent once, on the one leaf that was taken to finish. Family band
# measured off the siblings: proctor #E35721, clarify #DF6435, report #D65B30,
# create-test-suite #E46B35 — hue 16-21°, saturation 0.67-0.85 — kin to
# Fledgeling #C4622D. The corpus's own gel objects sit at lightness 0.50-0.60
# (Photos #DC6324, News #EC4B61), which is where this lands.
ACCENT = "#CE4A18"
ACCENT_HI = "#E5793C"
ACCENT_DEEP = "#93300E"
ACCENT_EDGE = "#88300E"      # the seat edge: the accent's own hue deepened,
ACCENT_RIM = "#FFDCC0"       # never a grey — sampled off apple-31's darkest pixel

# ------------------------------------------------------------ the three leaves
# Three material families, not three colours — and the two rejects are the two
# looks this skill names as the category's own defaults (ai-slop-check §9): the
# dark moody slab every dev-tool brief lands on, and the blank cream minimal that
# is its predictable opposite. Matte slate, frosted cream, gel resin.
#
# The value order runs cream (lightest) → gel → slate (darkest), so the fan reads
# in grayscale and under a system tint, where hue has gone; and the frosted leaf
# sits over the slate one, which is what makes its translucency visible instead of
# merely declared. Each entry is (face hi, face lo, seat edge, side face).
SLATE = ("#5E5339", "#28200E", "#120E06", "#1F190D")    # the rut
CREAM = ("#FCF7EB", "#CEBF9C", "#9C8E70", "#BCAE8E")    # its predictable opposite
GEL = (ACCENT_HI, ACCENT_DEEP, ACCENT_EDGE, "#87300F")  # the committed direction
PIN = ("#4E4334", "#221C11", "#15100A")                  # the rivet that pins them


@dataclass
class Spec:
    """Every geometric decision in one place, so a round is a parameter edit."""

    leaf_w: float = 238            # one sample leaf, repeated without scaling
    leaf_len: float = 586          # measured from the rivet to the far edge
    top_r: float = 119             # the far end: a full capsule at leaf_w / 2
    base_taper: float = 0.74       # the leaf narrows into its tab at the rivet
    # The splay. The rut and its predictable opposite sit 19° apart because they
    # are the same neighbourhood; the committed leaf stands 40° clear of the nearer
    # one. The ratio between those two gaps is the argument, so move them together.
    rut_deg: float = -40.0
    opposite_deg: float = -21.0
    committed_deg: float = 19.0
    thickness: float = 11          # the leaf's own side face, away from the light
    pin_r: float = 46              # the rivet
    frost_opacity: float = 0.72    # what stands behind a frosted leaf bleeds through
    gel_opacity: float = 0.955     # gel resin is denser, but not opaque
    sheen_gel: float = 0.34        # only the finished leaf gets a full sheen
    sheen_frost: float = 0.17
    sheen_matte: float = 0.12      # matte: a hint of diffuse fall, no specular
    cast_blur: float = 12
    cast_reject: float = 0.34      # what a leaf standing behind casts
    cast_front: float = 0.40       # the finished leaf, standing clear
    spec_w: float = 0.22           # the specular, as a fraction of the leaf
    spec_len: float = 0.58
    spec_opacity: float = 0.34
    ao_opacity: float = 0.34       # tucked under each overlap, not a global blur
    bounce: float = 0.30           # the warm kiss the gel throws on the frost face
    lift: float = 16               # optical centring: the shadows fall down-right,
                                   # so the geometry sits a little high

    def leaves(self) -> list[tuple[float, tuple[str, str, str, str]]]:
        """Back to front: the rut, its opposite, then the one that ships."""
        return [(self.rut_deg, SLATE),
                (self.opposite_deg, CREAM),
                (self.committed_deg, GEL)]

    @property
    def commitment_gap(self) -> float:
        """How far the committed leaf stands clear of the nearer reject."""
        return self.committed_deg - max(self.rut_deg, self.opposite_deg)


# ---------------------------------------------------------------- geometry

def rot(x: float, y: float, deg: float) -> tuple[float, float]:
    t = math.radians(deg)
    return x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)


def leaf_path(sp: Spec, deg: float, px: float, py: float,
              dx: float = 0.0, dy: float = 0.0, grow: float = 0.0) -> str:
    """One sample leaf, already rotated into tile space.

    Rotating the geometry rather than wrapping it in a rotate() group is
    deliberate: a userSpaceOnUse gradient inside a rotated group rotates with it,
    which lights every leaf from its own direction and reads as three objects
    under three lights. Circular arcs are rotation-invariant, so only the
    endpoints move — radii and flags are untouched.
    """
    hw, L = sp.leaf_w / 2 + grow, sp.leaf_len + grow
    hb = max(6.0, sp.leaf_w * sp.base_taper / 2 + grow)      # the tab at the rivet
    # A shrunken copy (grow < 0) is how the AO, the side face and the bounce are
    # cut, so the corner radius has to be clamped rather than shifted with the
    # body: a negative rx renders as a straight chord and puts a hard diagonal cut
    # across the face.
    tr = max(4.0, min(sp.top_r + grow, hw, L * 0.45))
    capsule = tr >= hw - 0.5
    pts = ([(-hb, 0.0), (-hw, -(L - tr)), (hw, -(L - tr)), (hb, 0.0)] if capsule
           else [(-hb, 0.0), (-hw, -(L - tr)), (-hw + tr, -L),
                 (hw - tr, -L), (hw, -(L - tr)), (hb, 0.0)])
    p = [(px + a + dx, py + b + dy) for a, b in (rot(x, y, deg) for x, y in pts)]
    top = (f"A{tr:.1f},{tr:.1f} 0 0 1 {p[2][0]:.1f},{p[2][1]:.1f} " if capsule
           else (f"A{tr:.1f},{tr:.1f} 0 0 1 {p[2][0]:.1f},{p[2][1]:.1f} "
                 f"L{p[3][0]:.1f},{p[3][1]:.1f} "
                 f"A{tr:.1f},{tr:.1f} 0 0 1 {p[4][0]:.1f},{p[4][1]:.1f} "))
    return (f"M{p[0][0]:.1f},{p[0][1]:.1f} L{p[1][0]:.1f},{p[1][1]:.1f} "
            + top
            + f"L{p[-1][0]:.1f},{p[-1][1]:.1f} "
            f"A{hb:.1f},{hb:.1f} 0 0 1 {p[0][0]:.1f},{p[0][1]:.1f} Z")


def slab_path(cx: float, cy: float, w: float, h: float, r: float, deg: float) -> str:
    """A rounded slab centred at (cx, cy), rotated — used for the specular."""
    hw, hh = w / 2, h / 2
    r = min(r, hw, hh)
    pts = [(-hw + r, -hh), (hw - r, -hh), (hw, -hh + r), (hw, hh - r),
           (hw - r, hh), (-hw + r, hh), (-hw, hh - r), (-hw, -hh + r)]
    q = [(cx + a, cy + b) for a, b in (rot(x, y, deg) for x, y in pts)]
    return (f"M{q[0][0]:.1f},{q[0][1]:.1f} L{q[1][0]:.1f},{q[1][1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {q[2][0]:.1f},{q[2][1]:.1f} "
            f"L{q[3][0]:.1f},{q[3][1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {q[4][0]:.1f},{q[4][1]:.1f} "
            f"L{q[5][0]:.1f},{q[5][1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {q[6][0]:.1f},{q[6][1]:.1f} "
            f"L{q[7][0]:.1f},{q[7][1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {q[0][0]:.1f},{q[0][1]:.1f} Z")


def outline_samples(sp: Spec, deg: float) -> list[tuple[float, float]]:
    """Enough points to bound a rotated leaf, arcs included."""
    hw, L = sp.leaf_w / 2, sp.leaf_len
    hb, tr = sp.leaf_w * sp.base_taper / 2, min(sp.top_r, hw)
    pts = [(-hw, -(L - tr)), (hw, -(L - tr)), (-hb, 0.0), (hb, 0.0)]
    for i in range(7):                                   # the far end
        a = math.pi / 2 * i / 6
        pts.append((-(hw - tr) - tr * math.cos(a), -(L - tr) - tr * math.sin(a)))
        pts.append(((hw - tr) + tr * math.cos(a), -(L - tr) - tr * math.sin(a)))
    for i in range(13):                                  # the tab at the rivet
        a = math.pi * i / 12
        pts.append((hb * math.cos(a), hb * math.sin(a)))
    return [rot(x, y, deg) for x, y in pts]


def placement(sp: Spec) -> tuple[float, float]:
    """The rivet position that centres the whole fan optically on the tile."""
    pts = [p for deg, _ in sp.leaves() for p in outline_samples(sp, deg)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (S / 2 - (min(xs) + max(xs)) / 2,
            S / 2 - (min(ys) + max(ys)) / 2 - sp.lift)


def axis_gradient(gid: str, path_pts: list[tuple[float, float]],
                  stops: list[tuple[float, str, float]]) -> str:
    """A gradient hung on the shared light axis, across one object's own extent.

    One light direction, one ramp per object: the corpus's gel objects each run
    light at their lit edge to dark at their shaded edge, rather than sharing one
    ramp across the whole tile.
    """
    xs, ys = [p[0] for p in path_pts], [p[1] for p in path_pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    r = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2
    lx, ly = LIGHT_AXIS
    x1, y1 = cx + lx * r, cy - ly * r          # the lit end
    x2, y2 = cx - lx * r, cy + ly * r          # the shaded end
    body = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>'
                   for o, c, a in stops)
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">{body}'
            f'</linearGradient>')


# ---------------------------------------------------------------- the master

def build(sp: Spec) -> str:
    squircle = SQUIRCLE_PATH.read_text().strip()
    px, py = placement(sp)
    lx, ly = LIGHT_AXIS
    sx, sy = SHADE_DIR
    leaves = sp.leaves()
    paths = [leaf_path(sp, deg, px, py) for deg, _ in leaves]
    world = [[(x + px, y + py) for x, y in outline_samples(sp, deg)]
             for deg, _ in leaves]

    out: list[str] = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ------------------------------------------------------------------ defs
    add("<defs>")
    add(f'<radialGradient id="cushion" cx="0.44" cy="0.24" r="0.90">'
        f'<stop offset="0" stop-color="{GROUND_HI}"/>'
        f'<stop offset="0.54" stop-color="{GROUND_MID}"/>'
        f'<stop offset="1" stop-color="{GROUND_LO}"/></radialGradient>')
    add(f'<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">'
        f'<stop offset="0.56" stop-color="{GROUND_VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{GROUND_VIGNETTE}" stop-opacity="0.24"/>'
        f'</radialGradient>')

    for i, (deg, (hi, lo, _e, _s)) in enumerate(leaves):
        stops = ([(0, hi, 1), (0.46, ACCENT, 1), (1, lo, 1)] if i == 2
                 else [(0, hi, 1), (1, lo, 1)])
        add(axis_gradient(f"face{i}", world[i], stops))
        # The rim: one stroke round the whole outline whose opacity dies along the
        # light axis, so the lit edges catch and the shaded ones do not. Cheaper
        # and steadier than authoring per-edge arcs on a rotated body.
        rim = ACCENT_RIM if i == 2 else "#FFFFFF"
        add(axis_gradient(f"rim{i}", world[i],
                          [(0, rim, 0.95 if i == 2 else 0.85),
                           (0.42, rim, 0.18), (1, rim, 0)]))
        add(axis_gradient(f"sheen{i}", world[i],
                          [(0, "#FFFFFF", 0.78), (0.34, "#FFFFFF", 0.16),
                           (1, "#FFFFFF", 0)]))
    add(axis_gradient("pinface", [(px - sp.pin_r, py - sp.pin_r),
                                  (px + sp.pin_r, py + sp.pin_r)],
                      [(0, PIN[0], 1), (1, PIN[1], 1)]))
    add(f'<linearGradient id="bounce" gradientUnits="userSpaceOnUse" '
        f'x1="{px:.1f}" y1="{py - sp.leaf_len:.1f}" x2="{px:.1f}" y2="{py:.1f}">'
        f'<stop offset="0" stop-color="{ACCENT}" stop-opacity="0.34"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0.06"/>'
        f'</linearGradient>')

    for name, blur, op in (("castback", sp.cast_blur, sp.cast_reject),
                           ("castfront", sp.cast_blur + 7, sp.cast_front)):
        add(f'<filter id="{name}" x="-45%" y="-45%" width="200%" height="200%">'
            f'<feDropShadow dx="{sx * 16:.1f}" dy="{sy * 22:.1f}" '
            f'stdDeviation="{blur}" flood-color="{SHADOW}" '
            f'flood-opacity="{op}"/></filter>')
    add('<filter id="soften" x="-70%" y="-70%" width="240%" height="240%">'
        '<feGaussianBlur stdDeviation="11"/></filter>')
    add('<filter id="soften-tight" x="-70%" y="-70%" width="240%" height="240%">'
        '<feGaussianBlur stdDeviation="5"/></filter>')
    for i, d in enumerate(paths):
        add(f'<clipPath id="lc{i}"><path d="{d}"/></clipPath>')
    # The thickness copy sits under the body it belongs to, so on a translucent
    # leaf it blocks the very transmission that makes the leaf read as glass: an
    # 11px offset copy covers ~95% of the body, and the frosted leaf then
    # composites over an opaque pale slab instead of over the dark leaf behind it.
    # Masked to the sliver that actually sticks out, it is a side face again.
    for i, d in enumerate(paths):
        add(f'<mask id="outside{i}" maskUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{S}" height="{S}">'
            f'<rect width="{S}" height="{S}" fill="#FFFFFF"/>'
            f'<path d="{d}" fill="#000000"/></mask>')
    add(f'<mask id="frost-not-gel" maskUnits="userSpaceOnUse" x="0" y="0" '
        f'width="{S}" height="{S}">'
        f'<path d="{paths[1]}" fill="#FFFFFF"/>'
        f'<path d="{leaf_path(sp, sp.committed_deg, px, py, 0, 0, 2)}" fill="#000000"/>'
        f'</mask>')
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

    def leaf(i: int) -> list[str]:
        deg, (hi, lo, edge, side) = leaves[i]
        d = paths[i]
        finished = i == len(leaves) - 1
        p: list[str] = []
        # 1 · what this leaf casts. One light, so one direction for all three.
        p.append(f'<path d="{d}" fill="{SHADOW}" '
                 f'filter="url(#{"castfront" if finished else "castback"})"/>')
        # 2 · ambient occlusion tucked under this leaf, on whatever it stands on.
        #     It goes down BEFORE this leaf's own body: clipped to the leaf behind
        #     and painted after, it covers the whole overlap region and reads as a
        #     hard diagonal cut across this face, because the leaf behind continues
        #     underneath this one.
        if i:
            p.append(f'<g clip-path="url(#lc{i - 1})">'
                     f'<path d="{leaf_path(sp, deg, px, py, sx * 13, sy * 13)}" '
                     f'fill="{SHADOW}" fill-opacity="{sp.ao_opacity}" '
                     f'filter="url(#soften-tight)"/></g>')
        # 3 · the leaf's own thickness, showing on the side away from the light
        p.append(f'<g mask="url(#outside{i})">'
                 f'<path d="{leaf_path(sp, deg, px, py, sx * sp.thickness, sy * sp.thickness)}" '
                 f'fill="{side}"/></g>')
        # 4 · the face, ramped along the shared light axis. Frost is translucent,
        #     so the clay leaf behind it visibly bleeds through the overlap — the
        #     authored blend is the era's signature craft moment, and baking it
        #     into one shape is what dies under a system tint.
        op = (sp.gel_opacity if finished
              else sp.frost_opacity if i == 1 else 1.0)
        p.append(f'<path d="{d}" fill="url(#face{i})" fill-opacity="{op}"/>')
        # 5 · the diffuse fall across the lit half. Only the finished leaf gets a
        #     full sheen; matte clay gets a hint and no specular at all.
        sheen = sp.sheen_gel if finished else sp.sheen_frost if i == 1 else sp.sheen_matte
        p.append(f'<g clip-path="url(#lc{i})">'
                 f'<path d="{d}" fill="url(#sheen{i})" opacity="{sheen}"/></g>')
        # 6 · the specular sliver near the lit edge — the tell that separates a gel
        #     object from a printed one, and the thing the two rejects lack
        if finished:
            sw = sp.leaf_w * sp.spec_w
            # in leaf-local space: along the lit side, over the upper reach
            cx, cy = rot(-(sp.leaf_w / 2 - sw / 2 - 14), -sp.leaf_len * 0.60, deg)
            p.append(f'<g clip-path="url(#lc{i})">'
                     f'<path d="{slab_path(px + cx, py + cy, sw, sp.leaf_len * sp.spec_len, sw / 2, deg)}" '
                     f'fill="#FFFFFF" fill-opacity="{sp.spec_opacity}" '
                     f'filter="url(#soften)"/></g>')
        # 7 · seat edge all round, then the rim catch, dying along the light axis.
        #     Both belong to this leaf: run as one pass at the end they paint the
        #     rejects' bright edges across whatever stands in front of them.
        p.append(f'<path d="{d}" fill="none" stroke="{edge}" stroke-width="2.6" '
                 f'stroke-opacity="{0.9 if finished else 0.8}"/>')
        p.append(f'<path d="{d}" fill="none" stroke="url(#rim{i})" '
                 f'stroke-width="{4.0 if finished else 3.2}" stroke-linejoin="round"/>')
        return p

    add('<g id="mid">')                     # the rut and its predictable opposite
    for i in (0, 1):
        out.extend(leaf(i))
    add("</g>")

    add('<g id="fg">')                      # the one that was taken to finish
    out.extend(leaf(2))
    # the rivet — one origin, pinning all three. Drawn last because it goes
    # through the stack rather than under it.
    add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sp.pin_r + 6:.1f}" '
        f'fill="{SHADOW}" fill-opacity="0.24" filter="url(#soften-tight)"/>')
    add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sp.pin_r:.1f}" fill="url(#pinface)"/>')
    add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sp.pin_r:.1f}" fill="none" '
        f'stroke="{PIN[2]}" stroke-width="2.4" stroke-opacity="0.85"/>')
    ca = math.degrees(math.atan2(-ly, lx))          # where the key light lands
    r0 = sp.pin_r * 0.70
    a0, a1 = math.radians(ca - 52), math.radians(ca + 52)
    add(f'<path d="M{px + r0 * math.cos(a0):.1f},{py + r0 * math.sin(a0):.1f} '
        f'A{r0:.1f},{r0:.1f} 0 0 1 '
        f'{px + r0 * math.cos(a1):.1f},{py + r0 * math.sin(a1):.1f}" fill="none" '
        f'stroke="#FFEEDA" stroke-width="4.2" stroke-opacity="0.60" '
        f'stroke-linecap="round"/>')
    add("</g>")

    add('<g id="highlight">')
    # the warm kiss the gel leaf throws onto the frosted leaf beside it. Tight and
    # bright rather than wide and dim: a broad low-alpha wash browns a whole face
    # while every hex in the palette still measures correct.
    add(f'<g mask="url(#frost-not-gel)">'
        f'<path d="{leaf_path(sp, sp.committed_deg, px - sx * 26, py - sy * 26)}" '
        f'fill="url(#bounce)" fill-opacity="{sp.bounce}" '
        f'filter="url(#soften)"/></g>')
    add("</g>")

    add("</g>")   # tile
    add("</svg>")
    return "\n".join(out)


NUMERIC = {"leaf_w", "leaf_len", "top_r", "base_taper", "rut_deg", "opposite_deg", "committed_deg",
           "thickness", "pin_r", "frost_opacity", "gel_opacity", "sheen_gel",
           "sheen_frost", "sheen_matte", "cast_blur", "cast_reject", "cast_front",
           "spec_w", "spec_len", "spec_opacity", "ao_opacity", "bounce", "lift"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--set", action="append", default=[],
                    help="override a numeric Spec field, e.g. --set committed_deg=22")
    a = ap.parse_args()
    sp = Spec()
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in NUMERIC:
            raise SystemExit(f"unknown or non-numeric field: {k}")
        sp = replace(sp, **{k: float(v)})
    out = Path(a.out) if a.out else HERE / "icon.svg"
    out.write_text(build(sp))
    print(f"wrote {out}  (commitment gap {sp.commitment_gap:.0f}°)")


if __name__ == "__main__":
    main()
