#!/usr/bin/env python3
"""Build the motion-craft icon master — "Onion-skin ghosts".

Geometry and material live here as named constants so a revision is a parameter
edit rather than path surgery.

The device: one gel capsule shown at three moments of a move, the way an animator's
onion skin or motion-craft's own contact sheet shows a film: successive frames laid
over each other. The two earlier frames are frosted graphite ghosts, thinner the
older they are; the frame it lands on is the only solid thing in the tile, poured
vermilion gel lit from inside.

The signature move is the SPACING. The gap between frames shrinks as the capsule
arrives (GAP_1 > GAP_2), which is an ease-out drawn in space: the long-tailed
arrival that the skill's craft rules put on every entrance. The ghosts overlap
where they are closest, and the overlap doubles the frost, so the trail reads as
translucent layers rather than three stickers (the Photos petals in the corpus,
apple-28, carry depth the same way).

Corpus values: ground and shadow ink are the family's (sampled for ux-craft off
apple-28: V 0.999 under the key, falling about 0.08 to the far edge); the accent's
inner glow follows apple-06 (Home): pale core #FFF1B6, body #FFB442, rim a step
deeper, re-hued to the family vermilion #EA4A24.

    python3 build_icon.py            # writes icon.svg beside this file
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "skills" / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- light model
LIGHT_ANGLE_DEG = 118.0                      # one soft key, down and to the right
LX = math.cos(math.radians(LIGHT_ANGLE_DEG))
LY = math.sin(math.radians(LIGHT_ANGLE_DEG))

# ---------------------------------------------------------------- geometry
# The move: three capsule positions on a shallow arc rising left to right, then
# settling. Positions are the arc parameter at each frame; the shrinking gap is
# the ease-out.
ARC_CX, ARC_CY, ARC_R = 512.0, 1700.0, 1360.0  # a long, shallow arc: the frames share one orientation
ARC_START_DEG = 212.0                          # first frame (lower left)
GAP_1 = 12.5                                   # degrees between frame 1 and 2
GAP_2 = 8.5                                    # degrees between frame 2 and 3: the ease-out
CAP_L = 320.0                                  # capsule length
CAP_W = 156.0                                  # capsule width (full-round ends)
CAP_THICK = 14.0                               # the edge band that makes it an object
TILT_EXTRA = 0.0                               # 0 lays each capsule along the path
LIFT = -6.0                                    # optical offset of the group (negative lowers it)

# ---------------------------------------------------------------- ground
GROUND_HI = "#FDFBF6"
GROUND_MID = "#F4EFE3"
GROUND_EDGE = "#E1D9C8"
RIM_INNER = "#FFFEFA"
VIGNETTE = "#8B7F66"
VIGNETTE_A = 0.22
SHADOW = "#3A3126"                             # warm shadow ink, never blue

# ---------------------------------------------------------------- the ghosts
# Frosted graphite: the older the frame, the thinner the frost.
GHOST_HI = "#E9E5DD"
GHOST_LO = "#9C968B"
GHOST_ALPHA = (0.50, 0.78)                     # frame 1, frame 2 (frosted, not graphite)
GHOST_RIM = "#E8E1D3"
GHOST_SHADOW_A = (0.06, 0.11)

# ---------------------------------------------------------------- the frame it lands on
ACCENT_CORE = "#FFD7B0"                        # the lit-from-inside core (apple-06 logic)
ACCENT_HI = "#F5793C"
ACCENT = "#EA4A24"                             # the family accent
ACCENT_DEEP = "#7A2008"                        # the far rim, where the gel is thickest
ACCENT_WALL = "#B8320F"
SPEC_A = 0.85                                  # the one specular sliver
LAND_SHADOW_A = 0.34


def capsule(cx: float, cy: float, angle: float, length: float, width: float) -> str:
    """A full-round capsule centred on (cx, cy), rotated to angle (degrees)."""
    r = width / 2
    half = length / 2 - r
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)          # along the capsule
    nx, ny = -uy, ux                           # across it
    p1 = (cx - ux * half + nx * r, cy - uy * half + ny * r)
    p2 = (cx + ux * half + nx * r, cy + uy * half + ny * r)
    p3 = (cx + ux * half - nx * r, cy + uy * half - ny * r)
    p4 = (cx - ux * half - nx * r, cy - uy * half - ny * r)
    return (f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 0 {p3[0]:.1f},{p3[1]:.1f} "
            f"L{p4[0]:.1f},{p4[1]:.1f} A{r:.1f},{r:.1f} 0 0 0 {p1[0]:.1f},{p1[1]:.1f} Z")


def frames() -> list[tuple[float, float, float]]:
    """(cx, cy, angle) for the three frames along the arc."""
    out = []
    t = ARC_START_DEG
    for step in (0.0, GAP_1, GAP_2):
        t += step
        a = math.radians(t)
        cx = ARC_CX + ARC_R * math.cos(a)
        cy = ARC_CY + ARC_R * math.sin(a) - LIFT
        out.append((cx, cy, t + 90.0 + TILT_EXTRA))
    # centre the group horizontally on the tile
    xs = [f[0] for f in out]
    dx = S / 2 - (min(xs) + max(xs)) / 2
    ys = [f[1] for f in out]
    dy = S / 2 - (min(ys) + max(ys)) / 2 - LIFT
    return [(x + dx, y + dy, ang) for x, y, ang in out]


def build() -> str:
    tile = SQUIRCLE.read_text().strip()
    fr = frames()
    p: list[str] = []
    add = p.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    add("<defs>")
    add(f'''<radialGradient id="ground" cx="0.40" cy="0.30" r="0.88">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.56" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/></radialGradient>''')
    add(f'''<radialGradient id="vign" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.54" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="{VIGNETTE_A}"/></radialGradient>''')
    lx0, ly0, lx1, ly1 = 0.5 - LX * 0.5, 0.5 - LY * 0.5, 0.5 + LX * 0.5, 0.5 + LY * 0.5
    add(f'''<linearGradient id="ghost" x1="{lx0:.3f}" y1="{ly0:.3f}" x2="{lx1:.3f}" y2="{ly1:.3f}">
      <stop offset="0" stop-color="{GHOST_HI}"/><stop offset="1" stop-color="{GHOST_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="ghostrim" x1="{lx0:.3f}" y1="{ly0:.3f}" x2="{lx1:.3f}" y2="{ly1:.3f}">
      <stop offset="0" stop-color="{GHOST_RIM}" stop-opacity="0.85"/>
      <stop offset="0.5" stop-color="{GHOST_RIM}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{GHOST_RIM}" stop-opacity="0"/></linearGradient>''')
    add(f'''<linearGradient id="wall" x1="{lx0:.3f}" y1="{ly0:.3f}" x2="{lx1:.3f}" y2="{ly1:.3f}">
      <stop offset="0" stop-color="{ACCENT_WALL}"/><stop offset="1" stop-color="{ACCENT_DEEP}"/></linearGradient>''')
    cx3, cy3, a3 = fr[2]
    add(f'''<radialGradient id="land" gradientUnits="userSpaceOnUse" cx="{cx3 - LX * 40:.1f}" cy="{cy3 - LY * 30:.1f}" r="{CAP_L * 0.62:.1f}">
      <stop offset="0" stop-color="{ACCENT_CORE}"/><stop offset="0.38" stop-color="{ACCENT_HI}"/>
      <stop offset="0.80" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT_DEEP}"/></radialGradient>''')
    add(f'''<linearGradient id="landrim" x1="{lx0:.3f}" y1="{ly0:.3f}" x2="{lx1:.3f}" y2="{ly1:.3f}">
      <stop offset="0" stop-color="#FFE9D6" stop-opacity="0.95"/>
      <stop offset="0.45" stop-color="{ACCENT_HI}" stop-opacity="0.15"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}" stop-opacity="0.55"/></linearGradient>''')
    add('<filter id="cast" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="22"/></filter>')
    add('<filter id="castwide" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="46"/></filter>')
    add('<filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14"/></filter>')
    add('<filter id="bloom" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="38"/></filter>')
    add(f'<clipPath id="tile"><path d="{tile}"/></clipPath>')
    add(f'<clipPath id="landface"><path d="{capsule(cx3, cy3, a3, CAP_L, CAP_W)}"/></clipPath>')
    add("</defs>")
    add('<g clip-path="url(#tile)">')

    # ---- bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vign)"/>')
    add("</g>")

    # ---- mid: contact shadows, then the two ghosts (older first)
    add('<g id="mid">')
    for i, (cx, cy, a) in enumerate(fr):
        sa = GHOST_SHADOW_A[i] if i < 2 else LAND_SHADOW_A
        add(f'<g filter="url(#castwide)"><path d="{capsule(cx + LX * 20, cy + CAP_THICK + LY * 34, a, CAP_L * 1.02, CAP_W * 1.02)}" '
            f'fill="{SHADOW}" fill-opacity="{sa * 0.55:.3f}"/></g>')
        add(f'<g filter="url(#cast)"><path d="{capsule(cx + LX * 8, cy + CAP_THICK * 0.9 + LY * 14, a, CAP_L * 0.98, CAP_W * 0.96)}" '
            f'fill="{SHADOW}" fill-opacity="{sa:.3f}"/></g>')
    for i in (0, 1):
        cx, cy, a = fr[i]
        al = GHOST_ALPHA[i]
        add(f'<path d="{capsule(cx, cy + CAP_THICK * 0.6, a, CAP_L, CAP_W)}" fill="{GHOST_LO}" fill-opacity="{al * 0.35:.3f}"/>')
        add(f'<path d="{capsule(cx, cy, a, CAP_L, CAP_W)}" fill="url(#ghost)" fill-opacity="{al:.3f}"/>')
        add(f'<path d="{capsule(cx, cy, a, CAP_L - 6, CAP_W - 6)}" fill="none" stroke="url(#ghostrim)" '
            f'stroke-width="5" stroke-opacity="{min(1.0, al * 1.6):.3f}"/>')
    add("</g>")

    # ---- fg: the frame it lands on
    add('<g id="fg">')
    add(f'<path d="{capsule(cx3, cy3 + CAP_THICK, a3, CAP_L, CAP_W)}" fill="url(#wall)"/>')
    add(f'<path d="{capsule(cx3, cy3, a3, CAP_L, CAP_W)}" fill="url(#land)"/>')
    add(f'<g clip-path="url(#landface)"><path d="{capsule(cx3 + LX * 26, cy3 + LY * 30, a3, CAP_L * 0.96, CAP_W * 0.86)}" '
        f'fill="none" stroke="{ACCENT_DEEP}" stroke-opacity="0.30" stroke-width="22" filter="url(#soft)"/></g>')
    add(f'<path d="{capsule(cx3, cy3, a3, CAP_L - 5, CAP_W - 5)}" fill="none" stroke="url(#landrim)" stroke-width="5"/>')
    add("</g>")

    # ---- highlight: one specular sliver on the lit shoulder, the escaping glow, the tile rim
    add('<g id="highlight">')
    ang = math.radians(a3)
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    if nx * LX + ny * LY > 0:                 # pick the across-axis side that faces the key
        nx, ny = -nx, -ny
    sx, sy = cx3 + nx * CAP_W * 0.22, cy3 + ny * CAP_W * 0.22
    add(f'<g clip-path="url(#landface)"><path d="{capsule(sx, sy, a3, CAP_L * 0.70, CAP_W * 0.24)}" '
        f'fill="#FFFFFF" fill-opacity="{SPEC_A}" filter="url(#soft)"/></g>')
    add(f'<path d="{capsule(cx3, cy3, a3, CAP_L, CAP_W)}" fill="{ACCENT}" fill-opacity="0.22" filter="url(#bloom)"/>')
    add(f'<path d="{tile}" fill="none" stroke="{RIM_INNER}" stroke-opacity="0.72" stroke-width="7"/>')
    add("</g>")

    add("</g>")
    add("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(build())
    print(f"wrote {out}")
