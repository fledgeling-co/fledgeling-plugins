#!/usr/bin/env python3
"""Build the demo-video-craft icon master: "The press".

Geometry and material live here as named constants so a revision is a parameter edit rather than path surgery.

The device: a graphite video screen with one vermilion gel play triangle lit from inside, and a porcelain cursor
whose tip has just landed on the triangle. Two rings spread from the tip. The owner chose the concept ("a cursor on
a play button"); the screen around it is what keeps it from being a stock play glyph or Infuse's play ribbon
(apple-05), and the screen's graphite is the family's dark object (status-update's slot, ux-craft's discs).

The signature move is the PRESS RING. demo-video-craft's films show every click as a cursor landing with a ring
spreading from its tip, so the icon is the skill's own grammar frozen at the instant of the press. The cursor
crosses the screen's bottom edge onto the ground, so it sits over three layers at once and reads as the thing in
front, not a sticker on the screen.

Corpus values: ground and shadow ink are the family's (motion-craft's build, sampled off apple-28: V 0.999 under
the key, falling about 0.08 to the far edge; apple-05 measures 255 at the top and 228 at the bottom). The triangle's
inner glow follows apple-06 (Home): pale core, body, a deeper rim, re-hued to the family vermilion #EA4A24. The
screen face follows apple-22's glass top-edge highlight on a dark pane.

    python3 build_icon.py            # writes icon.svg beside this file
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "skills" / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- light model
# One soft key from the upper left; light travels down and to the right, so shadows fall that way.
SHADOW_DX, SHADOW_DY = 0.32, 0.95

# ---------------------------------------------------------------- the screen
SCREEN_X, SCREEN_Y = 184.0, 252.0
SCREEN_W, SCREEN_H = 656.0, 410.0
SCREEN_R = 74.0
SCREEN_THICK = 18.0                            # the edge band below the face
SCREEN_HI = "#57514A"                          # face, upper left (warm graphite)
SCREEN_LO = "#26221F"                          # face, lower right
SCREEN_WALL = "#1B1815"
SCREEN_EDGE_HI = "#9A9186"                     # the glass top-edge highlight (apple-22)
BEZEL = 17.0                                   # the raised frame around the glass (take C)
BEZEL_HI = "#77706A"
BEZEL_LO = "#2A2622"
SHEEN_A = 0.0                                  # the glass sheen across the upper left (take B)
EMBER_A = 0.30                                 # the triangle's light reaching the ground below the screen (take C)
SCREEN_GLOW_A = 0.30                           # the triangle's light spilling onto the screen
TRACK_Y = 0.865                                # progress track, as a share of the screen's height
TRACK_A, PLAYED_A = 0.16, 0.55
PLAYED = 0.38                                  # how much of the video has played

# ---------------------------------------------------------------- the play triangle
TRI_H = 268.0                                  # vertical extent
TRI_ASPECT = 0.90                              # width / height
TRI_R = 38.0                                   # corner rounding
TRI_THICK = 12.0
TRI_OFFSET_X = 10.0                            # optical centring: a triangle's centroid sits left of its box centre
ACCENT_CORE = "#FFE2C2"                        # lit from inside (apple-06 logic)
ACCENT_HI = "#F7843F"
ACCENT = "#EA4A24"                             # the family accent
ACCENT_DEEP = "#7A2008"
ACCENT_WALL = "#9E2A0C"
SPEC_A = 0.80
BLOOM_A = 0.38

# ---------------------------------------------------------------- the cursor
CURSOR = [(0.0, 0.0), (0.0, 17.6), (4.2, 13.7), (7.1, 20.3), (9.7, 19.2), (6.9, 12.7), (12.5, 12.7)]
CURSOR_SCALE = 12.4                            # about 155 x 252 px
CURSOR_TILT_DEG = -9.0
CURSOR_TIP = (0.56, 0.58)                     # where the tip lands, as shares of the screen's width and height
CURSOR_R = 9.0
CURSOR_HI = "#FFFFFF"
CURSOR_LO = "#E4DDD0"
CURSOR_KEY = "#221E1B"                         # the keyline that separates it from screen and ground alike
CURSOR_KEY_W = 10.0

# ---------------------------------------------------------------- the press rings
RINGS = [(38.0, 7.0, 0.78), (64.0, 5.0, 0.30)]  # radius, stroke, opacity
RING = "#FFF4E8"

# ---------------------------------------------------------------- ground
GROUND_HI = "#FDFBF6"
GROUND_MID = "#F4EFE3"
GROUND_EDGE = "#E1D9C8"
RIM_INNER = "#FFFEFA"
VIGNETTE = "#8B7F66"
VIGNETTE_A = 0.22
SHADOW = "#3A3126"                             # warm shadow ink, never blue


def rounded_polygon(pts: list[tuple[float, float]], r: float) -> str:
    """A closed path through pts with each corner rounded by a quadratic of reach r."""
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]

        def toward(a, b, d):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            d = min(d, L / 2.2)
            return a[0] + dx / L * d, a[1] + dy / L * d

        a = toward(p1, p0, r)
        b = toward(p1, p2, r)
        out.append(("M" if i == 0 else "L") + f"{a[0]:.1f},{a[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {b[0]:.1f},{b[1]:.1f}")
    return " ".join(out) + " Z"


def rrect(x: float, y: float, w: float, h: float, r: float) -> str:
    return (f"M{x + r:.1f},{y:.1f} H{x + w - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + r:.1f} "
            f"V{y + h - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w - r:.1f},{y + h:.1f} H{x + r:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {x:.1f},{y + h - r:.1f} V{y + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y:.1f} Z")


def triangle(dx: float = 0.0, dy: float = 0.0, grow: float = 0.0) -> list[tuple[float, float]]:
    cx = SCREEN_X + SCREEN_W / 2 + TRI_OFFSET_X + dx
    cy = SCREEN_Y + SCREEN_H * 0.47 + dy
    h = TRI_H + grow
    w = h * TRI_ASPECT
    return [(cx - w * 0.40, cy - h / 2), (cx + w * 0.60, cy), (cx - w * 0.40, cy + h / 2)]


def cursor(dx: float = 0.0, dy: float = 0.0) -> list[tuple[float, float]]:
    tx = SCREEN_X + SCREEN_W * CURSOR_TIP[0] + dx
    ty = SCREEN_Y + SCREEN_H * CURSOR_TIP[1] + dy
    a = math.radians(CURSOR_TILT_DEG)
    ca, sa = math.cos(a), math.sin(a)
    return [(tx + (x * ca - y * sa) * CURSOR_SCALE, ty + (x * sa + y * ca) * CURSOR_SCALE) for x, y in CURSOR]


def build() -> str:
    tile = SQUIRCLE.read_text().strip()
    p: list[str] = []
    add = p.append
    sx, sy, sw, sh = SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H
    tri = triangle()
    tip = cursor()[0]
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    add("<defs>")
    add(f'''<radialGradient id="ground" cx="0.38" cy="0.28" r="0.90">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.56" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/></radialGradient>''')
    add(f'''<radialGradient id="vign" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.54" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="{VIGNETTE_A}"/></radialGradient>''')
    add(f'''<linearGradient id="bezel" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{BEZEL_HI}"/><stop offset="0.5" stop-color="{SCREEN_HI}"/>
      <stop offset="1" stop-color="{BEZEL_LO}"/></linearGradient>''')
    add('''<linearGradient id="bezelrim" x1="0" y1="0" x2="0.25" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.62"/><stop offset="0.30" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>''')
    add(f'''<linearGradient id="face" x1="0" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{SCREEN_HI}"/><stop offset="1" stop-color="{SCREEN_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="faceedge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SCREEN_EDGE_HI}" stop-opacity="0.95"/>
      <stop offset="0.18" stop-color="{SCREEN_EDGE_HI}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{SCREEN_EDGE_HI}" stop-opacity="0.0"/></linearGradient>''')
    tcx = sum(x for x, _ in tri) / 3
    tcy = sum(y for _, y in tri) / 3
    add(f'''<radialGradient id="screenglow" gradientUnits="userSpaceOnUse" cx="{tcx:.1f}" cy="{tcy:.1f}" r="{sw * 0.52:.1f}">
      <stop offset="0" stop-color="{ACCENT_HI}" stop-opacity="{SCREEN_GLOW_A}"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>''')
    add(f'''<radialGradient id="gel" gradientUnits="userSpaceOnUse" cx="{tcx - 34:.1f}" cy="{tcy - 30:.1f}" r="{TRI_H * 0.78:.1f}">
      <stop offset="0" stop-color="{ACCENT_CORE}"/><stop offset="0.34" stop-color="{ACCENT_HI}"/>
      <stop offset="0.78" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT_DEEP}"/></radialGradient>''')
    add(f'''<linearGradient id="gelrim" x1="0" y1="0" x2="0.9" y2="1">
      <stop offset="0" stop-color="#FFEBD8" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="{ACCENT_HI}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}" stop-opacity="0.6"/></linearGradient>''')
    add(f'''<linearGradient id="cur" x1="0" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{CURSOR_HI}"/><stop offset="1" stop-color="{CURSOR_LO}"/></linearGradient>''')
    add('<filter id="cast" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="20"/></filter>')
    add('<filter id="castwide" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="44"/></filter>')
    add('<filter id="soft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter>')
    add('<filter id="tight" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>')
    add('<filter id="bloom" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="34"/></filter>')
    add(f'<clipPath id="tile"><path d="{tile}"/></clipPath>')
    add(f'<clipPath id="screenface"><path d="{rrect(sx + BEZEL, sy + BEZEL, sw - 2 * BEZEL, sh - 2 * BEZEL, SCREEN_R - BEZEL * 0.8)}"/></clipPath>')
    add(f'<clipPath id="triface"><path d="{rounded_polygon(tri, TRI_R)}"/></clipPath>')
    add("</defs>")
    add('<g clip-path="url(#tile)">')

    # ---- bg: the porcelain ground
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vign)"/>')
    add("</g>")

    # ---- mid: the screen, its shadows, its glow and its progress track
    add('<g id="mid">')
    add(f'<ellipse cx="{sx + sw * 0.56:.1f}" cy="{sy + sh + 46:.1f}" rx="{sw * 0.36:.1f}" ry="58" fill="{ACCENT}" '
        f'fill-opacity="{EMBER_A}" filter="url(#bloom)"/>')
    add(f'<g filter="url(#castwide)"><path d="{rrect(sx + SHADOW_DX * 26, sy + SHADOW_DY * 46, sw, sh, SCREEN_R)}" '
        f'fill="{SHADOW}" fill-opacity="0.22"/></g>')
    add(f'<g filter="url(#cast)"><path d="{rrect(sx + SHADOW_DX * 8, sy + SCREEN_THICK + SHADOW_DY * 12, sw - 6, sh - 4, SCREEN_R)}" '
        f'fill="{SHADOW}" fill-opacity="0.34"/></g>')
    add(f'<path d="{rrect(sx, sy + SCREEN_THICK, sw, sh, SCREEN_R)}" fill="{SCREEN_WALL}"/>')
    add(f'<path d="{rrect(sx, sy, sw, sh, SCREEN_R)}" fill="url(#bezel)"/>')
    add(f'<path d="{rrect(sx + 3, sy + 3, sw - 6, sh - 6, SCREEN_R - 3)}" fill="none" stroke="url(#bezelrim)" '
        f'stroke-width="5" filter="url(#tight)"/>')
    add(f'<path d="{rrect(sx + BEZEL, sy + BEZEL, sw - 2 * BEZEL, sh - 2 * BEZEL, SCREEN_R - BEZEL * 0.8)}" fill="url(#face)"/>')
    add(f'<path d="{rrect(sx + BEZEL, sy + BEZEL, sw - 2 * BEZEL, sh - 2 * BEZEL, SCREEN_R - BEZEL * 0.8)}" fill="none" stroke="#0E0B09" stroke-opacity="0.55" stroke-width="5" '
        f'filter="url(#tight)"/>')
    add('<g clip-path="url(#screenface)">')
    add(f'<ellipse cx="{sx + sw * 0.24:.1f}" cy="{sy + sh * 0.10:.1f}" rx="{sw * 0.42:.1f}" ry="{sh * 0.34:.1f}" '
        f'fill="#FFFFFF" fill-opacity="{SHEEN_A}" transform="rotate(-14 {sx + sw * 0.24:.1f} {sy + sh * 0.10:.1f})" '
        f'filter="url(#soft)"/>')
    add(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#screenglow)"/>')
    ty = sy + sh * TRACK_Y
    x0, x1 = sx + sw * 0.10, sx + sw * 0.90
    xp = x0 + (x1 - x0) * PLAYED
    add(f'<line x1="{x0:.1f}" y1="{ty:.1f}" x2="{x1:.1f}" y2="{ty:.1f}" stroke="#F4EFE3" stroke-opacity="{TRACK_A}" '
        f'stroke-width="10" stroke-linecap="round"/>')
    add(f'<line x1="{x0:.1f}" y1="{ty:.1f}" x2="{xp:.1f}" y2="{ty:.1f}" stroke="#F4EFE3" stroke-opacity="{PLAYED_A}" '
        f'stroke-width="10" stroke-linecap="round"/>')
    add(f'<circle cx="{xp:.1f}" cy="{ty:.1f}" r="13" fill="#F4EFE3" fill-opacity="{PLAYED_A + 0.2:.2f}"/>')
    add("</g>")
    add(f'<path d="{rrect(sx + 2, sy + 2, sw - 4, sh - 4, SCREEN_R - 2)}" fill="none" stroke="url(#faceedge)" stroke-width="4"/>')
    add("</g>")

    # ---- fg: the play triangle, then the cursor and its rings
    add('<g id="fg">')
    add(f'<g filter="url(#cast)"><path d="{rounded_polygon(triangle(SHADOW_DX * 10, TRI_THICK + SHADOW_DY * 14), TRI_R)}" '
        f'fill="#0E0B09" fill-opacity="0.55"/></g>')
    add(f'<path d="{rounded_polygon(triangle(0, TRI_THICK), TRI_R)}" fill="{ACCENT_WALL}"/>')
    add(f'<path d="{rounded_polygon(tri, TRI_R)}" fill="url(#gel)"/>')
    add(f'<g clip-path="url(#triface)"><path d="{rounded_polygon(triangle(18, 22, -26), TRI_R)}" fill="none" '
        f'stroke="{ACCENT_DEEP}" stroke-opacity="0.32" stroke-width="22" filter="url(#soft)"/></g>')
    add(f'<path d="{rounded_polygon(triangle(0, 0, -6), TRI_R)}" fill="none" stroke="url(#gelrim)" stroke-width="5"/>')
    for r, w, a in RINGS:
        add(f'<circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="{r}" fill="none" stroke="{RING}" stroke-width="{w}" '
            f'stroke-opacity="{a}"/>')
    cur = cursor()
    add(f'<g filter="url(#cast)"><path d="{rounded_polygon(cursor(SHADOW_DX * 18, SHADOW_DY * 24), CURSOR_R)}" '
        f'fill="{SHADOW}" fill-opacity="0.50"/></g>')
    add(f'<path d="{rounded_polygon(cur, CURSOR_R)}" fill="url(#cur)" stroke="{CURSOR_KEY}" stroke-width="{CURSOR_KEY_W}" '
        f'stroke-linejoin="round"/>')
    add("</g>")

    # ---- highlight: one specular sliver on the triangle's lit edge, the escaping glow, the tile rim
    add('<g id="highlight">')
    t0, t1, _ = tri
    add(f'<g clip-path="url(#triface)"><line x1="{t0[0] + 30:.1f}" y1="{t0[1] + 48:.1f}" x2="{t0[0] + 30:.1f}" '
        f'y2="{t0[1] + TRI_H * 0.62:.1f}" stroke="#FFFFFF" stroke-opacity="{SPEC_A}" stroke-width="16" '
        f'stroke-linecap="round" filter="url(#tight)"/></g>')
    add(f'<path d="{rounded_polygon(tri, TRI_R)}" fill="{ACCENT}" fill-opacity="{BLOOM_A}" filter="url(#bloom)"/>')
    add(f'<path d="{rounded_polygon(cur, CURSOR_R)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="3" '
        f'transform="translate(-2,-2)" stroke-linejoin="round"/>')
    c0, c1 = cur[0], cur[1]
    add(f'<line x1="{c0[0] + 16:.1f}" y1="{c0[1] + 44:.1f}" x2="{c1[0] + 16:.1f}" y2="{c1[1] - 46:.1f}" stroke="#FFFFFF" '
        f'stroke-opacity="0.9" stroke-width="9" stroke-linecap="round" filter="url(#tight)"/>')
    add(f'<path d="{tile}" fill="none" stroke="{RIM_INNER}" stroke-opacity="0.72" stroke-width="7"/>')
    add("</g>")

    add("</g>")
    add("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = HERE / "icon.svg"
    out.write_text(build())
    print(f"wrote {out}")
