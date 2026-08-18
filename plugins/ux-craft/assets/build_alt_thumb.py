#!/usr/bin/env python3
"""Engine A, second hand-authored take — "The Thumb's Measure".

media-gen-pro's vector engine is a third opinion, not a second one, so Engine A
runs twice here: this take and the crossing-envelopes take in `build_icon.py`
are two genuinely different compositions on one spec, judged on the sheet.

The device: the human is the measure. A thumb of graphite gel comes in from the
bottom edge, cut by the mask so it belongs to someone off the tile, and its pad
lands on a vermilion gel key that is plainly narrower than the pad is. Every one
of the four target-size figures this skill keeps in a table — 24 CSS px, 44 CSS
px, 44 pt, 48 dp — exists because of that one object, and they disagreed in three
of its own files because nobody had drawn it.

    python3 build_alt_thumb.py       # writes icon-engineA2-thumb.svg
"""

from __future__ import annotations

import math
from pathlib import Path

from build_icon import (ACCENT, ACCENT_DEEP, ACCENT_HI, BOUNCE, KEY_R_FRAC, GEL_HI,
                        GEL_LO, GEL_MID, GEL_RIM, GROUND_EDGE, GROUND_HI, GROUND_MID,
                        LIGHT_ANGLE_DEG, LX, LY, RIM_INNER, S, SHADOW, SQUIRCLE,
                        VIGNETTE, VIGNETTE_A, rr)

# ---------------------------------------------------------------- geometry
# The thumb's axis: tip inside the tile, base off the bottom-right so the mask
# cuts it as a boundary rather than clipping it as an accident.
TIP = (470.0, 372.0)
BASE = (742.0, 1180.0)
# half-width along the axis: pad, joint waist, then the shaft widening off-tile
WIDTH_STOPS = [(0.00, 118.0), (0.30, 158.0), (0.56, 140.0), (0.84, 166.0), (1.00, 180.0)]
NAIL_AT = 0.20            # where the nail plate sits along the axis
NAIL_L, NAIL_W = 150.0, 112.0
CREASES = (0.42, 0.68)    # the two flexion creases, as fractions of the axis

KEY_SIDE = 176.0          # the control, plainly narrower than the pad (2 x 158)
KEY_GAP = 118.0           # tip-to-key-centre along the axis

LIGHT_DEG = LIGHT_ANGLE_DEG


def sm(t: float) -> float:
    return t * t * (3 - 2 * t)


def half_width(s: float) -> float:
    for i in range(len(WIDTH_STOPS) - 1):
        s0, w0 = WIDTH_STOPS[i]
        s1, w1 = WIDTH_STOPS[i + 1]
        if s0 <= s <= s1:
            return w0 + (w1 - w0) * sm((s - s0) / (s1 - s0))
    return WIDTH_STOPS[-1][1]


def axis():
    dx, dy = BASE[0] - TIP[0], BASE[1] - TIP[1]
    L = math.hypot(dx, dy)
    return dx / L, dy / L, L


def digit(n: int = 84) -> str:
    ux, uy, L = axis()
    nx, ny = -uy, ux
    left, right = [], []
    for i in range(n + 1):
        s = i / n
        cx, cy = TIP[0] + ux * L * s, TIP[1] + uy * L * s
        w = half_width(s)
        left.append((cx + nx * w, cy + ny * w))
        right.append((cx - nx * w, cy - ny * w))
    # The tip cap is sampled rather than written as an A command: a sweep flag
    # here inverts into a bite out of the pad in one renderer and reads correctly
    # in another, and the bug looks like a design decision.
    r0 = half_width(0.0)
    cap = []
    for i in range(1, 24):
        th = math.pi * i / 24
        # from the right side round the front of the pad to the left side
        px = TIP[0] - nx * r0 * math.cos(th) - ux * r0 * math.sin(th)
        py = TIP[1] - ny * r0 * math.cos(th) - uy * r0 * math.sin(th)
        cap.append((px, py))
    d = [f"M{left[0][0]:.1f},{left[0][1]:.1f}"]
    d += [f"L{p[0]:.1f},{p[1]:.1f}" for p in left[1:]]
    d.append(f"L{right[-1][0]:.1f},{right[-1][1]:.1f}")
    d += [f"L{p[0]:.1f},{p[1]:.1f}" for p in reversed(right[:-1])]
    d += [f"L{p[0]:.1f},{p[1]:.1f}" for p in cap]
    d.append("Z")
    return " ".join(d)


def build() -> str:
    ux, uy, L = axis()
    ang = math.degrees(math.atan2(uy, ux))
    body = digit()
    kcx = TIP[0] - ux * KEY_GAP
    kcy = TIP[1] - uy * KEY_GAP
    tile = SQUIRCLE.read_text().strip()

    p: list[str] = []
    add = p.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')
    add("<defs>")
    add(f'''<radialGradient id="ground" cx="0.40" cy="0.32" r="0.86">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.58" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<radialGradient id="vign" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.55" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="{VIGNETTE_A}"/>
    </radialGradient>''')
    # across-the-digit ramp: lit flank up-light, shaded flank down-light
    nx, ny = -uy, ux
    add(f'''<linearGradient id="flesh" gradientUnits="userSpaceOnUse"
      x1="{TIP[0] + nx * 210:.1f}" y1="{TIP[1] + ny * 210:.1f}"
      x2="{TIP[0] - nx * 210:.1f}" y2="{TIP[1] - ny * 210:.1f}">
      <stop offset="0" stop-color="{GEL_HI}"/>
      <stop offset="0.48" stop-color="{GEL_MID}"/>
      <stop offset="1" stop-color="{GEL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="rim" gradientUnits="userSpaceOnUse"
      x1="{TIP[0] + nx * 200:.1f}" y1="{TIP[1] + ny * 200:.1f}"
      x2="{TIP[0] - nx * 200:.1f}" y2="{TIP[1] - ny * 200:.1f}">
      <stop offset="0" stop-color="{GEL_RIM}" stop-opacity="0.92"/>
      <stop offset="0.44" stop-color="{GEL_RIM}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{BOUNCE}" stop-opacity="0.34"/>
    </linearGradient>''')
    add(f'''<linearGradient id="key" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.52" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="keyrim" gradientUnits="objectBoundingBox"
      x1="{0.5 - LX * 0.5:.3f}" y1="{0.5 - LY * 0.5:.3f}"
      x2="{0.5 + LX * 0.5:.3f}" y2="{0.5 + LY * 0.5:.3f}">
      <stop offset="0" stop-color="#FFD9BE" stop-opacity="0.85"/>
      <stop offset="0.5" stop-color="#FFD9BE" stop-opacity="0.08"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}" stop-opacity="0.5"/>
    </linearGradient>''')
    add(f'''<radialGradient id="kiss" gradientUnits="userSpaceOnUse"
      cx="{TIP[0]:.1f}" cy="{TIP[1]:.1f}" r="240">
      <stop offset="0" stop-color="{ACCENT_HI}" stop-opacity="0.34"/>
      <stop offset="0.5" stop-color="{ACCENT_HI}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{ACCENT_HI}" stop-opacity="0"/>
    </radialGradient>''')
    add('<filter id="cast" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="22"/></filter>')
    add('<filter id="castwide" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="52"/></filter>')
    add('<filter id="soft" x="-70%" y="-70%" width="240%" height="240%">'
        '<feGaussianBlur stdDeviation="30"/></filter>')
    add('<filter id="crease" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="15"/></filter>')
    add('<filter id="keyshadow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="12"/></filter>')
    add(f'<clipPath id="tile"><path d="{tile}"/></clipPath>')
    add(f'<clipPath id="bodyClip"><path d="{body}"/></clipPath>')
    add("</defs>")
    add('<g clip-path="url(#tile)">')

    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vign)"/>')
    add("</g>")

    # ---- the control, and the shadow it sits in
    add('<g id="mid">')
    add(f'<g filter="url(#keyshadow)"><path d="{rr(kcx - KEY_SIDE / 2 + LX * 16, kcy - KEY_SIDE / 2 + LY * 16, KEY_SIDE, KEY_SIDE, KEY_SIDE * KEY_R_FRAC)}" '
        f'fill="{SHADOW}" fill-opacity="0.34"/></g>')
    key = rr(kcx - KEY_SIDE / 2, kcy - KEY_SIDE / 2, KEY_SIDE, KEY_SIDE, KEY_SIDE * KEY_R_FRAC)
    add(f'<path d="{key}" fill="url(#key)"/>')
    add(f'<path d="{key}" fill="none" stroke="url(#keyrim)" stroke-width="6"/>')
    add("</g>")

    # ---- the thumb
    add('<g id="fg">')
    add(f'<g filter="url(#castwide)"><path d="{body}" transform="translate({LX * 46:.1f},{LY * 46:.1f})" '
        f'fill="{SHADOW}" fill-opacity="0.13"/></g>')
    add(f'<g filter="url(#cast)"><path d="{body}" transform="translate({LX * 22:.1f},{LY * 22:.1f})" '
        f'fill="{SHADOW}" fill-opacity="0.24"/></g>')
    add(f'<path d="{body}" fill="url(#flesh)"/>')
    add('<g clip-path="url(#bodyClip)">')
    # the two flexion creases: what stops a tapered shaft reading as a pen
    for s in CREASES:
        cx, cy = TIP[0] + ux * L * s, TIP[1] + uy * L * s
        add(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({ang:.1f})">'
            f'<ellipse rx="26" ry="200" fill="{SHADOW}" fill-opacity="0.34" '
            f'filter="url(#crease)"/></g>')
    # one soft catch on the lit flank; no hard specular anywhere
    hx = TIP[0] + ux * L * 0.30 + nx * 86
    hy = TIP[1] + uy * L * 0.30 + ny * 86
    add(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({ang:.1f})">'
        f'<ellipse rx="46" ry="240" fill="#FFFFFF" fill-opacity="0.11" '
        f'filter="url(#soft)"/></g>')
    # the nail plate: a lighter gel plate with its own rim, not a ferrule cap
    ncx, ncy = TIP[0] + ux * L * NAIL_AT, TIP[1] + uy * L * NAIL_AT
    add(f'<g transform="translate({ncx:.1f},{ncy:.1f}) rotate({ang - 90:.1f})">'
        f'<path d="{rr(-NAIL_W, -NAIL_L, NAIL_W * 2, NAIL_L * 2, NAIL_W * 0.86)}" '
        f'fill="{GEL_HI}" fill-opacity="0.50"/>'
        f'<path d="{rr(-NAIL_W, -NAIL_L, NAIL_W * 2, NAIL_L * 2, NAIL_W * 0.86)}" '
        f'fill="none" stroke="{GEL_RIM}" stroke-opacity="0.30" stroke-width="5"/></g>')
    # the warm kiss the key throws back onto the pad — tight, in the paler hue
    add(f'<rect width="{S}" height="{S}" fill="url(#kiss)"/>')
    add("</g>")
    # rim light up-light, porcelain bounce down-light: one stroke, one axis
    add(f'<path d="{body}" fill="none" stroke="url(#rim)" stroke-width="9"/>')
    add("</g>")

    add('<g id="highlight">')
    add(f'<path d="{tile}" fill="none" stroke="{RIM_INNER}" stroke-opacity="0.72" '
        f'stroke-width="7"/>')
    add("</g>")

    add("</g>")
    add("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "icon-engineA2-thumb.svg"
    out.write_text(build())
    print(f"wrote {out}")
