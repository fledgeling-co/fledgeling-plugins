#!/usr/bin/env python3
"""Engine A — the hand-authored layered SVG master for `harbourmaster`.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery. Run it to regenerate `icon.svg`.

DIRECTION: 2 Tahoe gel-glass, sub-register (a) — porcelain cushion tile carrying
a graphite object with one warm accent. Runner-up: the port register (an open
ledger with berth rows). Rejected because a book is a category glyph — it says
"records" and not "authority" — and because the ledger is the smallest of this
skill's three jobs.

THE GLYPH, subject-mined. A harbourmaster decides which vessel may enter. The
instrument of that decision is not a book and not a harbour: it is the PIER-HEAD
LIGHT, the squat tapered tower at a harbour mouth whose entire purpose is to say
enter or wait. Its lantern is the only lit thing in the tile.

r01 REJECTED, kept at icon-engineA-lamp-r01.svg. It drew the same idea as a slim
mast under a trapezoid hood, which is the silhouette of a domestic table lamp —
a category glyph rather than a harbour object. The lens sat under the hood and
read as a bulb under a shade, and the light was a hard-edged triangle that lay
on top of the scene instead of falling through it. Scored ~6/12. The fix was the
device, not its parameters: a tapered tower with a glazed lantern room and a
gallery railing is unmistakably a harbour light, carries far more mass at 16px,
and shares nothing with any sibling silhouette.

SIGNATURE MOVE: the lamp's light lands. A wedge of warm light falls from the
lantern across the quay below, and the three berth marks it reaches are lit
while the two beyond it stay graphite. The composition performs the argument —
admission is not a property of the berth, it is something the light confers.

FAMILY FIT, and the deliberate difference. `ship-fleet` is a plan-view harbour
of piers and slips; `shipyard` a hull in its cradle; `ship-feature` a slipway.
All three are horizontal, ground-level and seen from outside. This is the only
vertical mass in the nautical set and the only one that emits rather than
receives light, so it never collides with them in a grid while sharing their
porcelain ground and single ember accent.

VALUES SAMPLED FROM THE SIBLINGS, which sampled the corpus rather than assuming:
ground #FDFCF9 -> #E5E0D6 top-to-bottom with the brightest point at the TOP, so
the key light is above; the darkest in-tile pixel is the cool near-black
#1F2937 that `shipyard` measured off corpus rgb(31,41,55); the warm accent sits
at hue 9-14 degrees, value 0.82-1.00, which is `mac-doctor`'s measured ember.

16px SURVIVAL: at the squint the tile is a graphite wedge, widest at its foot,
with one warm block near its top and a warm dashed run to its right. The lantern
is 134px across on a 1024 canvas (13.1%, comfortably above the 8% floor where an
accent dissolves), and nothing else in the tile is warm.
"""

from __future__ import annotations
import pathlib

S = 1024
HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE / "squircle-path.txt").read_text().strip()

# ── geometry ────────────────────────────────────────────────────────────────
# The tower sits left of centre so its light has somewhere to land. The optical
# centre of the whole composition (tower + lit run) falls on the tile centre;
# the tower alone does not, and that is deliberate.
TOWER_CX = 404.0
BASE_W = 238.0           # width where the tower meets the quay
TOP_W = 150.0            # width at the gallery — the taper is 37%, enough to
                         # read as a tower rather than a column
TOWER_TOP = 358.0        # where the shaft ends and the gallery begins
QUAY_Y = 792.0           # top surface of the quay
QUAY_H = 232.0           # runs to the tile edge: r02 left the lower fifth of
                         # the tile near-white, so the tower stood on a stripe
                         # above nothing and the composition read bottom-empty

GALLERY_W = 212.0        # the walkway ring, wider than the shaft it caps
GALLERY_H = 30.0
GALLERY_Y = TOWER_TOP - GALLERY_H

RAIL_H = 34.0            # the railing standing on the gallery
RAIL_N = 5               # balusters

ROOM_W = 134.0           # the glazed lantern room — 11.5% of the tile
ROOM_H = 130.0
ROOM_Y = GALLERY_Y - RAIL_H - ROOM_H + 8
MULLIONS = 2             # glazing bars: what makes it a lantern, not a bulb

CAP_W = 166.0            # the roof over the lantern room
CAP_H = 52.0

# Berth marks along the quay: (x, lit). Three the light reaches, two beyond it.
# Held clear of the tile edge: the squircle cuts the corners, so a mark at 966
# was clipped in r02 and one at 944 read as touching in r05, because the
# squircle curves inward there. The last one ends at 966, leaving 58px of
# straight edge beyond it.
BERTHS = ((572.0, True), (662.0, True), (752.0, True), (836.0, False), (908.0, False))
BERTH_W = 58.0
BERTH_H = 18.0

BAND_TOP = 552.0         # the painted band, one third up the shaft
BAND_H = 80.0


# ── material ────────────────────────────────────────────────────────────────
GROUND_HI, GROUND_MID, GROUND_LO = "#FDFCF9", "#F6F4EF", "#E5E0D6"
VIGNETTE = "#8B8070"

GRAPHITE_HI = "#5A6675"   # strake facing the key light, up and left
GRAPHITE_MID = "#3A4551"
GRAPHITE_LO = "#232D39"
GRAPHITE_DEEP = "#1F2937"  # corpus rgb(31,41,55) — the measured shadow face
GRAPHITE_RIM = "#AEBAC9"   # edge catch where the key grazes a top edge

EMBER_CORE = "#FFD8B0"     # the filament itself, hottest and least saturated
EMBER_HI = "#F98A45"
EMBER_MID = "#EC6640"
EMBER_LO = "#C4441F"
EMBER_GLOW = "#F0642E"

KEY = ((300.0, 180.0), (720.0, 860.0))   # key axis, userSpaceOnUse


def berth(x: float, lit: bool) -> str:
    """One berth mark on the quay. Lit ones carry the lamp's colour."""
    top = EMBER_HI if lit else GRAPHITE_HI
    body = EMBER_MID if lit else GRAPHITE_MID
    y = QUAY_Y + 18
    return (
        f'<g>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{BERTH_W}" height="{BERTH_H}" rx="6" fill="{body}"/>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{BERTH_W}" height="6" rx="3" fill="{top}" opacity=".8"/>'
        f'</g>'
    )


def railing() -> str:
    """Balusters on the gallery. Five slim uprights and a top rail.

    This is the detail that separates a harbour light from a bollard with a
    glow on it: a gallery you could stand on implies a keeper, and a keeper is
    the harbourmaster the icon is named for.
    """
    y = GALLERY_Y - RAIL_H
    left = TOWER_CX - GALLERY_W / 2 + 14
    span = GALLERY_W - 28
    step = span / (RAIL_N - 1)
    posts = "".join(
        f'<rect x="{left + i * step - 3:.1f}" y="{y:.1f}" width="6" height="{RAIL_H:.1f}" '
        f'rx="3" fill="{GRAPHITE_LO}"/>'
        for i in range(RAIL_N)
    )
    return (
        posts
        + f'<rect x="{left - 10:.1f}" y="{y - 7:.1f}" width="{span + 20:.1f}" height="10" '
          f'rx="5" fill="url(#hood)"/>'
        + f'<rect x="{left - 10:.1f}" y="{y - 7:.1f}" width="{span + 20:.1f}" height="3" '
          f'rx="1.5" fill="{GRAPHITE_RIM}" opacity=".55"/>'
    )


def lantern_room() -> str:
    """The glazed room, its mullions, and the lit lens behind them.

    Order matters: glass, then the ember, then the bars ON TOP. Bars drawn under
    the glow read as scratches on a ball; drawn over it, the ember is
    unmistakably behind glass, which is the whole difference between a lantern
    and a bulb.
    """
    x = TOWER_CX - ROOM_W / 2
    bars = "".join(
        f'<rect x="{x + ROOM_W * (i + 1) / (MULLIONS + 1) - 3:.1f}" y="{ROOM_Y:.1f}" '
        f'width="6" height="{ROOM_H:.1f}" fill="{GRAPHITE_LO}" opacity=".92"/>'
        for i in range(MULLIONS)
    )
    return f"""
    <rect x="{x:.1f}" y="{ROOM_Y:.1f}" width="{ROOM_W}" height="{ROOM_H}" rx="10" fill="url(#lens)"/>
    <rect x="{x:.1f}" y="{ROOM_Y:.1f}" width="{ROOM_W}" height="{ROOM_H * 0.42:.1f}" rx="10"
          fill="#FFFFFF" opacity=".20"/>
    {bars}
    <rect x="{x:.1f}" y="{ROOM_Y:.1f}" width="{ROOM_W}" height="{ROOM_H}" rx="10"
          fill="none" stroke="{GRAPHITE_LO}" stroke-width="7"/>"""


def svg() -> str:
    bl, br = TOWER_CX - BASE_W / 2, TOWER_CX + BASE_W / 2
    tl, tr = TOWER_CX - TOP_W / 2, TOWER_CX + TOP_W / 2
    lens_cy = ROOM_Y + ROOM_H / 2

    # The band follows the taper, so its edges are parallel to the quay rather
    # than to each other. r02 drew it as a chevron by interpolating the wrong
    # pair of corners, which read as a tent pitched on the tower.
    def half_at(y: float) -> float:
        t = (QUAY_Y + 4 - y) / (QUAY_Y + 4 - TOWER_TOP)
        return (BASE_W + (TOP_W - BASE_W) * t) / 2

    band_l_hi = TOWER_CX - half_at(BAND_TOP)
    band_r_hi = TOWER_CX + half_at(BAND_TOP)
    band_l_lo = TOWER_CX - half_at(BAND_TOP + BAND_H)
    band_r_lo = TOWER_CX + half_at(BAND_TOP + BAND_H)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>

    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset=".55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </linearGradient>
    <radialGradient id="vign" cx=".5" cy=".42" r=".78">
      <stop offset=".62" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".20"/>
    </radialGradient>

    <linearGradient id="shaft" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GRAPHITE_HI}"/>
      <stop offset=".30" stop-color="{GRAPHITE_MID}"/>
      <stop offset=".78" stop-color="{GRAPHITE_LO}"/>
      <stop offset="1" stop-color="{GRAPHITE_DEEP}"/>
    </linearGradient>
    <linearGradient id="hood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GRAPHITE_HI}"/>
      <stop offset="1" stop-color="{GRAPHITE_LO}"/>
    </linearGradient>
    <linearGradient id="band" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#F7F2E8"/>
      <stop offset=".34" stop-color="#E8E0D0"/>
      <stop offset="1" stop-color="#B9AE99"/>
    </linearGradient>

    <linearGradient id="lens" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{EMBER_CORE}"/>
      <stop offset=".30" stop-color="{EMBER_HI}"/>
      <stop offset=".74" stop-color="{EMBER_MID}"/>
      <stop offset="1" stop-color="{EMBER_LO}"/>
    </linearGradient>
    <radialGradient id="halo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{EMBER_GLOW}" stop-opacity=".46"/>
      <stop offset=".5" stop-color="{EMBER_GLOW}" stop-opacity=".13"/>
      <stop offset="1" stop-color="{EMBER_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <!-- The beam fades along its length AND softens at both edges, so it reads
         as light falling rather than as a triangle lying on the scene. r01's
         hard-edged wedge was the single worst element in that take. -->
    <radialGradient id="pool" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{EMBER_GLOW}" stop-opacity=".38"/>
      <stop offset="1" stop-color="{EMBER_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="contact" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#6B5F4E" stop-opacity=".44"/>
      <stop offset="1" stop-color="#6B5F4E" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="quay" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#DED5C6"/>
      <stop offset="1" stop-color="#A6997F"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#tile)">
    <g id="bg">
    <!-- the porcelain cushion -->
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#vign)"/>
    </g>

    <g id="mid">
    <!-- the quay everything stands on -->
    <rect x="0" y="{QUAY_Y}" width="{S}" height="{QUAY_H}" fill="url(#quay)"/>
    <rect x="0" y="{QUAY_Y}" width="{S}" height="3" fill="#F3ECDF" opacity=".85"/>

    <!-- #mid — where the light lands. r03 drew an explicit beam polygon from
         the lantern; masked or not, its top edge stayed a visible straight line
         and read as a pale triangle laid over the tile rather than as light.
         Removing it loses nothing: the halo says the lantern is lit, the pool
         says the light reaches the quay, and the three lit berths say how far.
         The upper right is quieter for it, so nothing competes with the lantern. -->
    <ellipse cx="740" cy="{QUAY_Y + 22:.1f}" rx="380" ry="92" fill="url(#pool)"/>

    <!-- #mid — the berths the light reaches, and the two beyond it -->
    {"".join(berth(x, lit) for x, lit in BERTHS)}

    <!-- #mid — contact shadow, warm because the ground is warm -->
    <ellipse cx="{TOWER_CX:.1f}" cy="{QUAY_Y + 12:.1f}" rx="168" ry="34" fill="url(#contact)"/>

    </g>

    <g id="fg">
    <!-- the tower: one tapered mass, a painted band, a rim on the lit edge -->
    <path d="M{bl:.1f},{QUAY_Y + 4:.1f} L{tl:.1f},{TOWER_TOP:.1f}
             L{tr:.1f},{TOWER_TOP:.1f} L{br:.1f},{QUAY_Y + 4:.1f} Z" fill="url(#shaft)"/>
    <path d="M{bl:.1f},{QUAY_Y + 4:.1f} L{tl:.1f},{TOWER_TOP:.1f}
             L{tl + 9:.1f},{TOWER_TOP:.1f} L{bl + 11:.1f},{QUAY_Y + 4:.1f} Z"
          fill="{GRAPHITE_RIM}" opacity=".50"/>
    <path d="M{band_l_hi:.1f},{BAND_TOP:.1f} L{band_r_hi:.1f},{BAND_TOP:.1f}
             L{band_r_lo:.1f},{BAND_TOP + BAND_H:.1f} L{band_l_lo:.1f},{BAND_TOP + BAND_H:.1f} Z"
          fill="url(#band)" opacity=".94"/>

    <!-- #fg — gallery, railing, lantern room, cap -->
    <rect x="{TOWER_CX - GALLERY_W/2:.1f}" y="{GALLERY_Y:.1f}" width="{GALLERY_W}"
          height="{GALLERY_H}" rx="10" fill="url(#hood)"/>
    <rect x="{TOWER_CX - GALLERY_W/2:.1f}" y="{GALLERY_Y:.1f}" width="{GALLERY_W}"
          height="4" rx="2" fill="{GRAPHITE_RIM}" opacity=".62"/>
    {railing()}

    </g>

    <g id="highlight">
    <!-- halo first, then the room, so the glass clips the glow -->
    <circle cx="{TOWER_CX:.1f}" cy="{lens_cy:.1f}" r="214" fill="url(#halo)"/>
    {lantern_room()}

    <path d="M{TOWER_CX - CAP_W/2:.1f},{ROOM_Y:.1f}
             L{TOWER_CX:.1f},{ROOM_Y - CAP_H:.1f}
             L{TOWER_CX + CAP_W/2:.1f},{ROOM_Y:.1f} Z" fill="url(#hood)"/>
    <path d="M{TOWER_CX - CAP_W/2:.1f},{ROOM_Y:.1f} L{TOWER_CX:.1f},{ROOM_Y - CAP_H:.1f}"
          stroke="{GRAPHITE_RIM}" stroke-width="4" stroke-linecap="round" opacity=".6" fill="none"/>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(svg())
    print(f"wrote {out} · tower {QUAY_Y - ROOM_Y:.0f}px = {(QUAY_Y - ROOM_Y)/S:.1%} of tile · "
          f"lantern {ROOM_W:.0f}px = {ROOM_W/S:.1%}")
