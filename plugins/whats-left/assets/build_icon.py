#!/usr/bin/env python3
"""build_icon.py — Engine A master for the `whats-left` icon: "The Open Crown".

Direction 2, sub-register (a) — porcelain cushion tile carrying one toy-scale
object, per `create-mac-icon/references/icon-directions.md`. The object is a
dressed stone gateway with its keystone lifted clear of the housing in its
crown, held in the air directly above the hole it came out of.

Why this object. The skill surveys what a project still needs and hands back one
page whose two halves are a single graph: every blocked item deep-links to the
decision that releases it, and each decision names what it releases. An arch is
that graph as a physical fact — every stone is cut, laid and load-bearing in
waiting, and none of it carries anything until the last wedge drops in. Built
and released are visibly different states here rather than one averaged number,
which is the distinction the skill refuses to collapse.

Signature move: the piece and the void are the same shape, from one set of
numbers. `KEY_W_BASE`, `KEY_TAPER`, `R_IN` and `BLOCK_TOP` generate the housing's
two flanks and its seat AND the keystone's four corners, so the two cannot drift
apart in a later round. The keystone is the only saturated thing on the tile and
it hangs exactly clear of its own housing, aligned rather than tumbling, because
"this fits precisely here, and nothing works until it does" is the claim.

Separation from `clarify`, its nearest neighbour on the shelf: that icon is
taupe option cards with a selected radio, drawn flat in the plane of the tile.
This one is an extruded three-quarter solid with a hole through it, and nothing
in the marketplace has a warm mass hanging clear above a dark one.

Every visible face is one Lambert term against `LIGHT`, so rubric #5 (single
light model) holds by construction: top course 0.318 > front face 0.256 > right
flank 0.142 on the render, brightest nearest the key. The extrusion is one
oblique offset `VIEW`, so the camera is one camera.

The banner is derived from this file rather than from a sibling: `ACCENT`,
`LIGHT`, `VIEW_X/VIEW_Y`, `STONE` and the block's own extents are the readable
facts it needs.

    python3 build_icon.py > icon.svg           # the shipped master
    python3 build_icon.py --flat > mock.svg    # three-value mock, no material
"""

from __future__ import annotations

import math
import pathlib
import sys

S = 1024
SQUIRCLE = (pathlib.Path(__file__).resolve().parents[2]
            / "create-mac-icon" / "assets" / "squircle-path.txt")

# ── the oblique projection ──────────────────────────────────────────────────
# A point (x, y) on the near face lands at (x + VIEW_X, y + VIEW_Y) on the far
# face. Up and to the RIGHT puts the camera above-right-front, which makes the
# visible interior surfaces the LEFT jamb, the threshold and the housing's left
# wall — faces that all turn away from the key light, so the archway and the
# empty housing both read as recesses rather than as painted-on holes.
# (generate-investor-portal's rule (b): a recess is lit opposite to the object
# standing in front of it, and the sign is computed, never guessed.)
VIEW_X, VIEW_Y = 56.0, -24.0

# ── the one key light ───────────────────────────────────────────────────────
# A 3D direction from a surface TOWARD the light: up, left, and toward the
# viewer. Every face value in the icon is AMB + KEY * max(0, dot(N, LIGHT)),
# which puts the tiers in the order the ordering predicate wants — top faces
# brightest, front face mid, right flanks on ambient alone.
LIGHT = (-0.44, -0.82, 0.37)
AMB, KEY_GAIN = 0.22, 0.92
AO_INSIDE = 0.58        # extra occlusion on anything inside the archway or the socket
WARM_SHADOW = "#3E2A18"  # shadows go warm; a blue shadow in a warm scene is the tell

# ── geometry ────────────────────────────────────────────────────────────────
# The outer silhouette is a RECTANGULAR gateway block with the arch cut into it,
# and that is the one decision the whole icon turned on. Two three-value mocks
# died first, both drawn as a bare voussoir ring: a half-round ring severed at
# the crown read unmistakably as a perfume bottle with its stopper above it, and
# flattening the arc to a segmental span only made it a squatter bottle. The
# curved OUTER contour is the defect — sloping shoulders over vertical sides is a
# bottle whatever is done to the material. A flat top and flat sides read as
# masonry, the arch survives as the hole plus an archivolt joint, and the missing
# piece becomes a notch in a straight top edge, which is what carries at 32px.
CX = 512.0 - 22.0       # the mass grows right under the projection, so the near
                        # face sits left of centre and the INK centres
ARC_C = 730.0           # centre of the opening's arc, well below its crown
R_IN = 250.0            # the intrados: the opening itself
T_RING = 88.0          # the ring's radial thickness
R_RING = R_IN + T_RING  # the archivolt, drawn as a joint rather than an outline
PHI_SPR = 40.0          # springing angle: the arc runs 40 to 140 degrees
BLOCK_TOP = 340.0
LEG_BOT = 800.0
FOOT_H, FOOT_OVER, FOOT_R = 34.0, 20.0, 4.0    # the plinth's upper course
PLINTH_H, PLINTH_OVER = 30.0, 38.0             # and its lower one, stepped wider
COPING = 46.0           # the top course, as a joint line under the top edge

KEY_W_BASE = 134.0      # the keystone's width where it seats on the intrados
KEY_TAPER = 12.0         # degrees off vertical per flank. A radially-cut wedge at
                        # 13 degrees is what a real keystone is, and in the mock it
                        # was a bottle neck: a tapered void rising out of a
                        # round-topped opening reads as a decanter in negative
                        # space, whatever the material does. Twelve degrees is as
                        # far back as the wedge can come once the housing is
                        # painted as a solid recess rather than a through-void,
                        # which is what actually killed the bottle.
CLEAR = 42.0            # air between the lifted keystone and the slot's mouth
KEY_R = 11.0            # arris softening: gel is poured, not cut
SHADOW_OFF = (40.0, 30.0)   # the keystone's shadow on the block's top course
SOCKET_K = 0.62         # how far the housing is cut into the block's depth

VOUSSOIR_N = 2          # bed joints each side of the slot

# ── palette ─────────────────────────────────────────────────────────────────
# Ground: the family's porcelain cushion, unchanged from its siblings so the
# shelf reads as one set. Corpus check (apple-12, the one Apple capture that is
# also a dark object plus a warm accent on porcelain): its ground runs
# lum 0.874 at the top to 0.740 at the bottom, brightest nearest the key.
GROUND_TOP = "#F8F5EE"
GROUND_BOT = "#E4DDCB"
TILE_RIM = "#FFFDF8"
VIGNETTE = "#8A7A62"    # warm edge darkening, never grey

# Stone: warm-neutral basalt. Deliberately greyer than be-my-witness's warm
# graphite barrel (#3E342A) and warmer than should-compact's cool slate
# (#2E363D) — the two siblings close enough to collide in the dark-mass register.
STONE = "#565247"       # albedo; every face is this under one Lambert term
STONE_DEEP = "#171410"  # the far-face backing, and the deepest interior

# Accent: fired clay. Family luminance, own hue point — mac-craft's rule (e).
# HSL(24.5, 0.84, 0.47) against the siblings' shared H 12-19 at L 0.447.
ACCENT = "#DD6413"
ACCENT_RIM = "#FFD2A4"  # the arris catch on the keystone's lit top edge
RIM_SCATTER = "#FFF3E2"  # warm porcelain scatter on the stone's lit arris

SHADOW_TILE = "#4A3A22"  # the contact shadow on the porcelain


# ── colour helpers ──────────────────────────────────────────────────────────
def _srgb_to_lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(r: float, g: float, b: float) -> str:
    return "#%02X%02X%02X" % tuple(int(round(max(0, min(1, c)) * 255)) for c in (r, g, b))


def tone(albedo: str, illum: float) -> str:
    """Scale an albedo by one illumination term, in linear light.

    Multiplying linear RGB preserves the ratios between channels, so a shadow
    keeps the material's saturation instead of going brown — the failure "The
    Cast" r06 measured and the one a luminance-range check cannot see. A small
    warm bias goes in below half illumination, because the only light in this
    scene is warm and a neutral shadow reads as a second, cooler source.
    """
    lin = [_srgb_to_lin(c) * illum for c in _rgb(albedo)]
    if illum < 0.5:
        w = [_srgb_to_lin(c) for c in _rgb(WARM_SHADOW)]
        k = 0.16 * (0.5 - illum) / 0.5
        lin = [(1 - k) * l + k * w[i] * illum * 2.2 for i, l in enumerate(lin)]
    return _hex(*[_lin_to_srgb(c) for c in lin])


def illum(nx: float, ny: float, nz: float = 0.0, ao: float = 1.0) -> float:
    """One Lambert term against the single key, plus ambient, times occlusion."""
    n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    d = (nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]) / n
    return (AMB + KEY_GAIN * max(0.0, d)) * ao


I_FRONT = illum(0, 0, 1)          # the near face: 0.59
I_TOP = illum(0, -1, 0)           # anything facing up: 0.93
I_FLANK = illum(1, 0, 0)          # facing right, away from the key: ambient
I_SEAT = illum(0, -1, 0, AO_INSIDE)


# ── geometry helpers ────────────────────────────────────────────────────────
def P(r: float, phi_deg: float) -> tuple[float, float]:
    """A point on the near face at polar (r, phi) about the arc's centre.

    phi is a maths angle in degrees: 40 = right springing, 90 = crown, 140 = left.
    """
    a = math.radians(phi_deg)
    return (CX + r * math.cos(a), ARC_C - r * math.sin(a))


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pt(p: tuple[float, float]) -> str:
    return f"{f(p[0])} {f(p[1])}"


def quad(a, b, colour: str, extra: str = "", depth: float = 1.0) -> str:
    """One swept facet: the segment a-b on the near face, extruded along VIEW."""
    c = (b[0] + VIEW_X * depth, b[1] + VIEW_Y * depth)
    d = (a[0] + VIEW_X * depth, a[1] + VIEW_Y * depth)
    return (f'<path d="M{pt(a)}L{pt(b)}L{pt(c)}L{pt(d)}Z" fill="{colour}"{extra}/>')


def visible(nx: float, ny: float) -> bool:
    """A swept face shows only where its outward normal turns toward the camera."""
    return nx * VIEW_X + ny * VIEW_Y > 0


def sweep_arc(r: float, phi0: float, phi1: float, inward: bool, albedo: str,
              ao: float = 1.0, step: float = 2.0) -> str:
    """Facet an arc's swept surface, one Lambert value per facet.

    Faceting rather than one gradient because the normal rotates through the
    run: a single linear gradient carries one axis, and a curved band needs a
    value per facet or it reads as a printed band (material-recipes, clarify).
    """
    out = []
    n = max(1, int(round(abs(phi1 - phi0) / step)))
    for i in range(n):
        a0 = phi0 + (phi1 - phi0) * i / n
        a1 = phi0 + (phi1 - phi0) * (i + 1) / n
        mid = math.radians((a0 + a1) / 2)
        nx, ny = math.cos(mid), -math.sin(mid)
        if inward:
            nx, ny = -nx, -ny
        if not visible(nx, ny):
            continue
        # a hair of overlap, or rsvg leaves hairlines between facets
        pad = 0.22
        out.append(quad(P(r, a0 + pad), P(r, a1 - pad), tone(albedo, illum(nx, ny, 0, ao))))
    return "".join(out)


def rounded(pts: list[tuple[float, float]], r: float) -> str:
    """A closed polygon with its corners eased — the arris softening gel needs."""
    n = len(pts)
    d = []
    for i, p in enumerate(pts):
        prv, nxt = pts[(i - 1) % n], pts[(i + 1) % n]
        v0 = (prv[0] - p[0], prv[1] - p[1])
        v1 = (nxt[0] - p[0], nxt[1] - p[1])
        l0 = math.hypot(*v0) or 1.0
        l1 = math.hypot(*v1) or 1.0
        rr = min(r, l0 / 2.4, l1 / 2.4)
        a = (p[0] + v0[0] / l0 * rr, p[1] + v0[1] / l0 * rr)
        b = (p[0] + v1[0] / l1 * rr, p[1] + v1[1] / l1 * rr)
        d.append(("M" if i == 0 else "L") + pt(a))
        d.append(f"Q{pt(p)} {pt(b)}")
    return "".join(d) + "Z"


# ── the gateway's near face ─────────────────────────────────────────────────
# The slot and the keystone come out of ONE set of numbers — KEY_W_BASE,
# KEY_TAPER, R_IN, BLOCK_TOP — so the piece and the void are congruent by
# construction and cannot drift apart in a later round.
X_L_IN, X_R_IN = P(R_IN, 180 - PHI_SPR)[0], P(R_IN, PHI_SPR)[0]
Y_SPR = P(R_IN, PHI_SPR)[1]              # the impost: top of the vertical jambs
BLOCK_HALF = (X_R_IN - X_L_IN) / 2 + T_RING
BX0, BX1 = CX - BLOCK_HALF, CX + BLOCK_HALF
FOOT_TOP, FOOT_MID = LEG_BOT, LEG_BOT + FOOT_H
FOOT_BOT = FOOT_MID + PLINTH_H
FX0, FX1 = BX0 - FOOT_OVER, BX1 + FOOT_OVER
PX0, PX1 = BX0 - PLINTH_OVER, BX1 + PLINTH_OVER
CROWN_Y = BLOCK_TOP

SEAT_HALF = KEY_W_BASE / 2
SEAT_Y = ARC_C - math.sqrt(R_IN ** 2 - SEAT_HALF ** 2)   # where a flank meets the intrados
TAN_T = math.tan(math.radians(KEY_TAPER))
PHI_SEAT = math.degrees(math.atan2(ARC_C - SEAT_Y, SEAT_HALF))   # 74.7


def slot_half(y: float) -> float:
    return SEAT_HALF + (SEAT_Y - y) * TAN_T


SEAT_L, SEAT_R = (CX - SEAT_HALF, SEAT_Y), (CX + SEAT_HALF, SEAT_Y)
SLOT_TL = (CX - slot_half(BLOCK_TOP), BLOCK_TOP)
SLOT_TR = (CX + slot_half(BLOCK_TOP), BLOCK_TOP)
LIFT = (SEAT_Y - BLOCK_TOP) + CLEAR      # clear of the slot's mouth, not in it


def arch_face() -> str:
    """One closed path: the block, the arched opening, and the empty slot.

    The opening and the slot are a SINGLE void running from the threshold up
    through the top edge — the graph this skill draws, as one piece of geometry.
    The intrados carries a chord where the keystone seats, which is what the
    keystone's own underside is, so the two are the same line.
    """
    a = []
    a.append("M" + pt((BX0, FOOT_TOP)))
    a.append("L" + pt((BX0, BLOCK_TOP)))
    a.append("L" + pt(SLOT_TL))
    a.append("L" + pt(SEAT_L))                                             # slot's left flank
    a.append(f"A{f(R_IN)} {f(R_IN)} 0 0 0 {pt((X_L_IN, Y_SPR))}")          # 105 -> 140
    a.append("L" + pt((X_L_IN, FOOT_TOP)))
    a.append("L" + pt((X_R_IN, FOOT_TOP)))
    a.append("L" + pt((X_R_IN, Y_SPR)))
    a.append(f"A{f(R_IN)} {f(R_IN)} 0 0 0 {pt(SEAT_R)}")                   # 40 -> 75
    a.append("L" + pt(SLOT_TR))                                            # slot's right flank
    a.append("L" + pt((BX1, BLOCK_TOP)))
    a.append("L" + pt((BX1, FOOT_TOP)))
    a.append("Z")
    return "".join(a)


def keystone_face() -> list[tuple[float, float]]:
    """The lifted wedge: the slot's own four corners, raised by LIFT."""
    return [(SLOT_TL[0], SLOT_TL[1] - LIFT), (SLOT_TR[0], SLOT_TR[1] - LIFT),
            (SEAT_R[0], SEAT_R[1] - LIFT), (SEAT_L[0], SEAT_L[1] - LIFT)]


# ── the SVG ─────────────────────────────────────────────────────────────────
def svg(flat: bool = False) -> str:
    d = SQUIRCLE.read_text().strip() if SQUIRCLE.exists() else ""
    if not d:
        print("squircle-path.txt not found — the family shares one silhouette",
              file=sys.stderr)
        raise SystemExit(1)

    face = arch_face()
    ks = keystone_face()
    ks_path = rounded(ks, KEY_R)
    tl, tr, br, bl = ks
    # One plinth definition, reused by the near face, the far-face backing and the
    # body clip. `$` is where each use puts its own fill.
    plinth = (f'<rect x="{f(FX0)}" y="{f(FOOT_TOP)}" width="{f(FX1 - FX0)}" '
              f'height="{f(FOOT_H)}" rx="{f(FOOT_R)}" $/>'
              f'<rect x="{f(PX0)}" y="{f(FOOT_MID)}" width="{f(PX1 - PX0)}" '
              f'height="{f(PLINTH_H)}" rx="{f(FOOT_R)}" $/>')

    slot = (f'M{pt(SLOT_TL)}L{pt(SLOT_TR)}L{pt(SEAT_R)}L{pt(SEAT_L)}Z')

    if flat:
        # Three values, no material: the recognition test that has to be looked
        # at, at 1024 / 128 / 32 / 16, before any face is shaded. The housing is
        # filled with the mass here, because it is a stopped recess in the
        # shipped icon — so this is also the true filled-black silhouette that
        # rubric #3 asks about, and leaving the slot open made the mock read as a
        # bottle when the icon does not.
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'width="{S}" height="{S}">'
            f'<defs><clipPath id="m"><path d="{d}"/></clipPath></defs>'
            f'<g id="bg" clip-path="url(#m)"><rect width="{S}" height="{S}" fill="#F2EEE4"/></g>'
            f'<g id="mid" clip-path="url(#m)" fill="#2A2721">'
            f'<path d="{face}"/><path d="{slot}"/>{plinth.replace("$", "")}</g>'
            f'<g id="fg" clip-path="url(#m)"><path d="{ks_path}" fill="#DD6413"/></g>'
            f'<g id="highlight"/></svg>')

    grad_x0, grad_y0 = BX0 - 40, CROWN_Y - 40
    grad_x1, grad_y1 = BX1 + 40, FOOT_BOT + 40
    rim0, rim1 = (BX0, BLOCK_TOP), (SLOT_TL[0], BLOCK_TOP)

    defs = f"""
    <linearGradient id="ground" x1="0.14" y1="0" x2="0.72" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vig" cx=".46" cy=".40" r=".80">
      <stop offset=".52" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".20"/>
    </radialGradient>
    <linearGradient id="stoneFace" gradientUnits="userSpaceOnUse"
        x1="{f(grad_x0)}" y1="{f(grad_y0)}" x2="{f(grad_x1)}" y2="{f(grad_y1)}">
      <stop offset="0" stop-color="{tone(STONE, I_FRONT * 1.34)}"/>
      <stop offset=".52" stop-color="{tone(STONE, I_FRONT)}"/>
      <stop offset="1" stop-color="{tone(STONE, I_FRONT * 0.66)}"/>
    </linearGradient>
    <linearGradient id="keyFace" gradientUnits="userSpaceOnUse"
        x1="{f(tl[0] - 30)}" y1="{f(tl[1] - 30)}" x2="{f(br[0] + 30)}" y2="{f(br[1] + 30)}">
      <stop offset="0" stop-color="{tone(ACCENT, I_FRONT * 1.30)}"/>
      <stop offset=".46" stop-color="{tone(ACCENT, I_FRONT * 1.06)}"/>
      <stop offset="1" stop-color="{tone(ACCENT, I_FRONT * 0.80)}"/>
    </linearGradient>
    <linearGradient id="keyTop" gradientUnits="userSpaceOnUse"
        x1="{f(tl[0])}" y1="0" x2="{f(tr[0] + VIEW_X)}" y2="0">
      <stop offset="0" stop-color="{tone(ACCENT, I_TOP * 1.06)}"/>
      <stop offset="1" stop-color="{tone(ACCENT, I_TOP * 0.82)}"/>
    </linearGradient>
    <radialGradient id="keyBloom" gradientUnits="userSpaceOnUse"
        cx="{f(tl[0] + (tr[0] - tl[0]) * 0.34)}" cy="{f(tl[1] + 26)}"
        r="{f((tr[0] - tl[0]) * 0.78)}">
      <stop offset="0" stop-color="{ACCENT_RIM}" stop-opacity=".26"/>
      <stop offset=".62" stop-color="{ACCENT_RIM}" stop-opacity=".07"/>
      <stop offset="1" stop-color="{ACCENT_RIM}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="socketAO" gradientUnits="userSpaceOnUse"
        x1="0" y1="{f(BLOCK_TOP)}" x2="0" y2="{f(BLOCK_TOP + 62)}">
      <stop offset="0" stop-color="{WARM_SHADOW}" stop-opacity=".34"/>
      <stop offset="1" stop-color="{WARM_SHADOW}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="socketBounce" gradientUnits="userSpaceOnUse"
        x1="0" y1="{f(SEAT_Y)}" x2="0" y2="{f(SEAT_Y - 84)}">
      <stop offset="0" stop-color="{RIM_SCATTER}" stop-opacity=".30"/>
      <stop offset="1" stop-color="{RIM_SCATTER}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bounce" gradientUnits="userSpaceOnUse"
        x1="0" y1="{f(FOOT_BOT)}" x2="0" y2="{f(FOOT_BOT - 118)}">
      <stop offset="0" stop-color="{GROUND_BOT}" stop-opacity=".20"/>
      <stop offset="1" stop-color="{GROUND_BOT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="archRim" gradientUnits="userSpaceOnUse"
        x1="{f(rim0[0])}" y1="{f(rim0[1])}" x2="{f(rim1[0])}" y2="{f(rim1[1])}">
      <stop offset="0" stop-color="{RIM_SCATTER}" stop-opacity="0"/>
      <stop offset=".40" stop-color="{RIM_SCATTER}" stop-opacity=".62"/>
      <stop offset="1" stop-color="{RIM_SCATTER}" stop-opacity=".10"/>
    </linearGradient>
    <filter id="cast" x="-25%" y="-25%" width="160%" height="170%">
      <feGaussianBlur stdDeviation="17"/>
    </filter>
    <filter id="contact" x="-30%" y="-60%" width="170%" height="260%">
      <feGaussianBlur stdDeviation="15"/>
    </filter>
    <filter id="tight" x="-30%" y="-90%" width="170%" height="340%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <clipPath id="tile"><path d="{d}"/></clipPath>
    <clipPath id="topface"><path d="M{pt((BX0, BLOCK_TOP))}L{pt((BX1, BLOCK_TOP))}
      L{pt((BX1 + VIEW_X, BLOCK_TOP + VIEW_Y))}L{pt((BX0 + VIEW_X, BLOCK_TOP + VIEW_Y))}Z"/>
    </clipPath>
    <clipPath id="socketmouth"><rect x="0" y="{f(BLOCK_TOP)}" width="{S}" height="{S}"/></clipPath>
    <clipPath id="body" clip-rule="nonzero">
      <path d="{face}"/>{plinth.replace("$", "")}
    </clipPath>"""

    # ── mid: everything behind the near face ────────────────────────────────
    back = [
        # the far face, as a backing so no facet seam can show the ground through
        f'<g transform="translate({f(VIEW_X)} {f(VIEW_Y)})" fill="{STONE_DEEP}">'
        f'<path d="{face}"/>{plinth.replace("$", "")}</g>',
    ]

    # the ground shadows: the object's own contact patch, warm and soft
    shadow = (
        f'<g filter="url(#contact)">'
        f'<rect x="{f(PX0 + 14)}" y="{f(FOOT_BOT - 14)}" width="{f(PX1 - PX0 + 20)}" '
        f'height="34" rx="17" fill="{SHADOW_TILE}" opacity=".30"/></g>'
        f'<g filter="url(#tight)">'
        f'<rect x="{f(PX0 + 6)}" y="{f(FOOT_BOT - 9)}" width="{f(PX1 - PX0 + 6)}" '
        f'height="15" rx="7" fill="{SHADOW_TILE}" opacity=".40"/></g>')

    # The socket is DARK, and that is a deliberate departure from what a hole
    # through a wall would really show. Painted as a through-void it lit up as a
    # bright wedge continuous with the archway below, and the two together read as
    # a decanter in negative space at every size — twice, at two different tapers.
    # Filled as a recess, the porcelain shows only through the arch, the opening
    # keeps its own shape, and the slot reads as the hole the piece came out of.
    #
    # It is also a STOPPED housing rather than a cut through the full thickness:
    # a through-cut has no back wall, so the only surface the camera can see in it
    # is one side wall, which rendered as a dark tilted slab standing in the notch
    # — a loose stone, not a recess. A back wall parallel to the near face is a
    # plane the light can land on, and that is what makes the socket read as a
    # socket. SOCKET_K is how deep it is cut, as a fraction of the block's depth.
    wall_n = (SEAT_Y - SLOT_TL[1], -(SEAT_L[0] - SLOT_TL[0]))
    socket = (
        f'<g clip-path="url(#socketmouth)">'
        f'<path d="{slot}" fill="{tone(STONE, I_FRONT * 0.50)}"/>'      # the back wall
        f'{quad(SLOT_TL, SEAT_L, tone(STONE, illum(*wall_n, 0, 0.66)), depth=SOCKET_K)}'
        # the porcelain seen through the arch throws light back up into the housing:
        # the one thing that stops a recess reading as a printed dark wedge
        f'<path d="{slot}" fill="url(#socketBounce)"/>'
        f'<path d="{slot}" fill="url(#socketAO)"/></g>'
    )

    # interior swept faces — all turn away from the key, so the opening reads as
    # cut into the mass rather than printed on it
    inner = [
        sweep_arc(R_IN, PHI_SEAT + 2, 180 - PHI_SPR, True, STONE, AO_INSIDE),  # intrados
        quad((X_L_IN, Y_SPR), (X_L_IN, FOOT_TOP),
             tone(STONE, illum(1, 0, 0, AO_INSIDE))),                     # left jamb
        quad((X_L_IN, FOOT_TOP), (X_R_IN, FOOT_TOP), tone(STONE, I_SEAT)),  # threshold
    ]

    # exterior swept faces: the top course either side of the slot, the right
    # flank, and the footing's ledges
    outer = [
        quad((BX0, BLOCK_TOP), SLOT_TL, tone(STONE, I_TOP)),
        quad(SLOT_TR, (BX1, BLOCK_TOP), tone(STONE, I_TOP * 0.92)),
        quad((BX1, BLOCK_TOP), (BX1, FOOT_TOP), tone(STONE, I_FLANK)),
        quad((FX1, FOOT_TOP + FOOT_R), (FX1, FOOT_MID), tone(STONE, I_FLANK * 0.94)),
        quad((PX1, FOOT_MID + FOOT_R), (PX1, FOOT_BOT - FOOT_R), tone(STONE, I_FLANK * 0.88)),
        quad((FX0 + FOOT_R, FOOT_TOP), (BX0, FOOT_TOP), tone(STONE, I_TOP * 0.84)),
        quad((BX1, FOOT_TOP), (FX1 - FOOT_R, FOOT_TOP), tone(STONE, I_TOP * 0.84)),
        quad((PX0 + FOOT_R, FOOT_MID), (FX0, FOOT_MID), tone(STONE, I_TOP * 0.78)),
        quad((FX1, FOOT_MID), (PX1 - FOOT_R, FOOT_MID), tone(STONE, I_TOP * 0.78)),
    ]

    # ── fg: the near face, its joints, and the keystone ─────────────────────
    # Masonry is told in joints, not in outline: the archivolt is a JOINT here
    # rather than a silhouette edge, which is what keeps the block a block.
    #
    # Each joint is TWO strokes, because a recessed mortar joint is a valley and a
    # valley is dark on both flanks with its lit lip off-centre toward the key
    # (material-recipes, mac-craft (a)). One dark line alone reads as ink on the
    # stone; the pale lip 3px up-key of it is what makes the courses read as
    # separate blocks, which is most of what the raster take had and this did not.
    joints, lips = [], []

    def joint(a, b, arc: float = 0.0):
        n = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        # the lip sits on whichever side of the groove faces the key
        ox, oy = LIGHT[0] * -3.1, LIGHT[1] * -3.1
        if arc:
            joints.append(f'<path d="M{pt(a)}A{f(arc)} {f(arc)} 0 0 0 {pt(b)}"/>')
            lips.append(f'<path d="M{pt((a[0] - ox, a[1] - oy))}A{f(arc)} {f(arc)} 0 0 0 '
                        f'{pt((b[0] - ox, b[1] - oy))}"/>')
        else:
            joints.append(f'<path d="M{pt(a)}L{pt(b)}"/>')
            lips.append(f'<path d="M{pt((a[0] - ox, a[1] - oy))}L{pt((b[0] - ox, b[1] - oy))}"/>')

    joint(P(R_RING, PHI_SPR), P(R_RING, 180 - PHI_SPR), arc=R_RING)      # the archivolt
    span = PHI_SEAT - PHI_SPR
    for i in range(VOUSSOIR_N + 1):
        phi = PHI_SPR + span * i / VOUSSOIR_N
        for a in (phi, 180 - phi):
            joint(P(R_IN, a), P(R_RING, a))                              # voussoir beds
    for y in (BLOCK_TOP + COPING, 500.0):     # spandrel courses, stopped at the ring
        dy = ARC_C - y
        dx = math.sqrt(max(0.0, R_RING ** 2 - dy ** 2))
        joint((BX0, y), (CX - dx, y))
        joint((CX + dx, y), (BX1, y))
    for y in (FOOT_TOP - 92,):                # a course through both piers
        joint((BX0, y), (X_L_IN, y))
        joint((X_R_IN, y), (BX1, y))
    joint_ink = tone(STONE, I_FRONT * 0.42)
    joint_lip = tone(STONE, min(1.0, I_FRONT * 1.34))

    # The keystone hangs above the block's top course, so its shadow lands on
    # that course rather than on the near face: both are in the same plane, and a
    # cast shadow across the front of the block would be a plane error.
    key_shadow = (
        f'<g clip-path="url(#topface)"><g filter="url(#tight)">'
        f'<path d="M{pt((bl[0] + SHADOW_OFF[0], BLOCK_TOP - 4))}'
        f'L{pt((br[0] + SHADOW_OFF[0], BLOCK_TOP - 4))}'
        f'L{pt((br[0] + SHADOW_OFF[0] + VIEW_X, BLOCK_TOP + VIEW_Y + SHADOW_OFF[1]))}'
        f'L{pt((bl[0] + SHADOW_OFF[0] + VIEW_X, BLOCK_TOP + VIEW_Y + SHADOW_OFF[1]))}Z"'
        f' fill="{WARM_SHADOW}" opacity=".52"/></g></g>')

    key_top = quad(tl, tr, "url(#keyTop)")
    key_flank = quad((tr[0] - 1.6, tr[1]), (br[0] - 1.6, br[1]),
                     tone(ACCENT, illum(br[1] - tr[1], -(br[0] - tr[0]))))

    body = f"""
    <path d="{face}" fill="url(#stoneFace)"/>
    {plinth.replace("$", 'fill="url(#stoneFace)"')}
    <g clip-path="url(#body)">
      <g stroke="{joint_lip}" stroke-width="2.2" stroke-linecap="round" opacity=".34"
         fill="none">{"".join(lips)}</g>
      <g stroke="{joint_ink}" stroke-width="3.4" stroke-linecap="round" opacity=".60"
         fill="none">{"".join(joints)}</g>
      <rect x="{f(PX0)}" y="{f(FOOT_BOT - 118)}" width="{f(PX1 - PX0)}" height="118"
            fill="url(#bounce)"/>
    </g>
    {key_shadow}"""

    keystone = f"""
    {key_top}
    {key_flank}
    <path d="{ks_path}" fill="url(#keyFace)"/>
    <path d="{ks_path}" fill="url(#keyBloom)"/>"""

    # ── highlight: three arris catches and the tile's own rim light ─────────
    hi = f"""
    <path d="M{pt((BX0 + 8, BLOCK_TOP + 2.4))}L{pt((SLOT_TL[0] - 4, BLOCK_TOP + 2.4))}"
          fill="none" stroke="url(#archRim)" stroke-width="5" stroke-linecap="round"/>
    <path d="M{pt((SLOT_TR[0] + 4, BLOCK_TOP + 2.4))}L{pt((BX1 - 8, BLOCK_TOP + 2.4))}"
          fill="none" stroke="{RIM_SCATTER}" stroke-width="4" stroke-linecap="round"
          opacity=".26"/>
    <path d="M{pt((tl[0] + KEY_R * 1.6, tl[1] + 3.2))}L{pt((tr[0] - KEY_R * 1.6, tr[1] + 3.2))}"
          fill="none" stroke="{ACCENT_RIM}" stroke-width="3.6" stroke-linecap="round"
          opacity=".30"/>
    <path d="{d}" fill="none" stroke="{TILE_RIM}" stroke-width="7" opacity=".80"/>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>{defs}
  </defs>
  <g id="bg" clip-path="url(#tile)">
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#vig)"/>
  </g>
  <g id="mid" clip-path="url(#tile)">
    {shadow}
    {"".join(back)}
    {socket}
    {"".join(inner)}
    {"".join(outer)}
  </g>
  <g id="fg" clip-path="url(#tile)">{body}
    {keystone}
  </g>
  <g id="highlight" clip-path="url(#tile)">{hi}
  </g>
</svg>
"""


if __name__ == "__main__":
    print(svg(flat="--flat" in sys.argv))
