#!/usr/bin/env python3
"""Build the mac-design-digest icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

Metaphor — "The Stamped Value": a porcelain value-plate carrying one recorded
figure, with a vermilion seal seated proud in a countersunk impression at its
corner. The seal is a SEPARATE physical object from the value it marks — it has
its own body, its own rim light and its own contact shadow falling on the plate,
and the socket it was pressed into is still visible around it. That is the
skill's whole argument: a number and its provenance are two things, and the
second is stamped onto the first rather than being part of it.

    python3 build_icon.py            # writes icon-src.svg beside this file
"""

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground (porcelain; the family constant, shared with tui-craft et al.)
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"

# ---- the value-plate: porcelain object standing ABOVE the ground
PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R = 172, 232, 680, 536, 60
PLATE_HI = "#FFFEFB"   # top-left, catching the key light
PLATE_MID = "#F7F4ED"
PLATE_LO = "#E4DFD3"   # bottom-right
PLATE_RIM = "#FFFFFF"  # lit rim on the top-left edge
PLATE_EDGE = "#C9C3B7"  # hairline so porcelain-on-porcelain still separates

# ---- the recorded value: three neutral marks, no glyphs
#      a thin label rule, one heavy figure bar, one thin footnote rule
MARK_HI = "#5A626E"
MARK_LO = "#39404A"
MARK = "#4E5560"
LABEL_X, LABEL_Y, LABEL_W, LABEL_H = 240, 328, 236, 20
VALUE_X, VALUE_Y, VALUE_W, VALUE_H, VALUE_R = 240, 392, 336, 66, 22
FOOT_X, FOOT_Y, FOOT_W, FOOT_H = 240, 500, 168, 18

# ---- the seal (the one warm accent, spent here and nowhere else)
#      ACCENT_DEEP is a shade of the same vermilion, not a second hue.
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ACCENT_DEEP = "#B23F1C"
SEAL_CX, SEAL_CY = 692, 594
SEAL_R_OUT, SEAL_R_IN, SEAL_LOBES = 112, 95, 12
SEAL_RING_R = 66      # debossed concentric ring inside the seal
SEAL_BOSS_R = 40      # the raised die at its centre
SOCKET_R = 132        # countersunk impression in the plate

# ---- shadow / relief tuning
SOCKET_DARK = "#9B9384"
CONTACT = "#6B5F4C"


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def scalloped(cx, cy, r_out, r_in, lobes):
    """A notarial-seal rim: quadratic lobes between valley points."""
    step = 2 * math.pi / lobes

    def pt(radius, angle):
        return (cx + radius * math.cos(angle), cy + radius * math.sin(angle))

    x0, y0 = pt(r_in, -step / 2)
    d = [f'M{x0:.2f},{y0:.2f}']
    for i in range(lobes):
        peak = i * step
        valley = peak + step / 2
        px, py = pt(r_out * 1.06, peak)
        vx, vy = pt(r_in, valley)
        d.append(f'Q{px:.2f},{py:.2f} {vx:.2f},{vy:.2f}')
    d.append('z')
    return ' '.join(d)


def arc(cx, cy, r, a0, a1):
    """Stroke path for the arc from a0 to a1 (degrees, screen space)."""
    x0 = cx + r * math.cos(math.radians(a0))
    y0 = cy + r * math.sin(math.radians(a0))
    x1 = cx + r * math.cos(math.radians(a1))
    y1 = cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    return f'M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f}'


def build() -> str:
    parts: list[str] = []
    add = parts.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ---------------- defs
    add('<defs>')
    add(f'''<radialGradient id="ground" cx="0.42" cy="0.34" r="0.82">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.62" stop-color="{GROUND_LO}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<linearGradient id="plate" x1="0.1" y1="0" x2="0.88" y2="1">
      <stop offset="0" stop-color="{PLATE_HI}"/>
      <stop offset="0.5" stop-color="{PLATE_MID}"/>
      <stop offset="1" stop-color="{PLATE_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="mark" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0" stop-color="{MARK_HI}"/>
      <stop offset="1" stop-color="{MARK_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="seal" x1="0.14" y1="0.04" x2="0.86" y2="0.96">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.42" stop-color="{ACCENT}"/>
      <stop offset="0.82" stop-color="#D64A22"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="boss" x1="0.2" y1="0.1" x2="0.8" y2="0.9">
      <stop offset="0" stop-color="#F27A4C"/>
      <stop offset="1" stop-color="#DB4A22"/>
    </linearGradient>''')
    add(f'''<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.42"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    add(f'''<filter id="plateshadow" x="-25%" y="-25%" width="150%" height="165%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="{CONTACT}"
                    flood-opacity="0.32"/>
    </filter>''')
    add(f'''<filter id="sealshadow" x="-45%" y="-45%" width="190%" height="200%">
      <feDropShadow dx="7" dy="13" stdDeviation="11" flood-color="{CONTACT}"
                    flood-opacity="0.42"/>
    </filter>''')
    add('''<filter id="softglow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>''')
    add(f'<clipPath id="plateclip"><path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ---------------- ground
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')

    # ---------------- the value-plate
    add('<g filter="url(#plateshadow)">')
    add(f'<path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}" fill="url(#plate)"/>')
    add('</g>')
    add(f'<path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}" fill="none" '
        f'stroke="{PLATE_EDGE}" stroke-width="2.5" stroke-opacity="0.7"/>')
    # rim light along the lit (top-left) edge
    add(f'<path d="M{PLATE_X + PLATE_R},{PLATE_Y + 2.5} h{PLATE_W - 2 * PLATE_R}" fill="none" '
        f'stroke="{PLATE_RIM}" stroke-width="4" stroke-opacity="0.95" stroke-linecap="round"/>')
    add(f'<path d="M{PLATE_X + 2.5},{PLATE_Y + PLATE_R} v{PLATE_H - 2 * PLATE_R}" fill="none" '
        f'stroke="{PLATE_RIM}" stroke-width="4" stroke-opacity="0.7" stroke-linecap="round"/>')

    add('<g clip-path="url(#plateclip)">')

    # ---------------- the recorded value: rules and one heavy bar, never glyphs
    add(f'<rect x="{LABEL_X}" y="{LABEL_Y}" width="{LABEL_W}" height="{LABEL_H}" rx="{LABEL_H / 2}" '
        f'fill="{MARK}" fill-opacity="0.30"/>')
    add(f'<rect x="{VALUE_X}" y="{VALUE_Y}" width="{VALUE_W}" height="{VALUE_H}" '
        f'rx="{VALUE_R}" fill="url(#mark)"/>')
    add(f'<rect x="{VALUE_X}" y="{VALUE_Y}" width="{VALUE_W}" height="{VALUE_H}" '
        f'rx="{VALUE_R}" fill="none" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="2"/>')
    add(f'<rect x="{FOOT_X}" y="{FOOT_Y}" width="{FOOT_W}" height="{FOOT_H}" rx="{FOOT_H / 2}" '
        f'fill="{MARK}" fill-opacity="0.24"/>')

    # ---------------- the socket: the impression the seal was pressed into.
    # A recess reads inverted to a raised object — shadow on the near (top-left)
    # inner edge, a lit wall on the far (bottom-right) one.
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SOCKET_R}" fill="none" '
        f'stroke="{SOCKET_DARK}" stroke-width="2.5" stroke-opacity="0.45"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SOCKET_R - 4, 135, 315)}" fill="none" '
        f'stroke="{SOCKET_DARK}" stroke-width="7" stroke-opacity="0.34" stroke-linecap="round"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SOCKET_R - 4, 315, 135)}" fill="none" '
        f'stroke="#FFFFFF" stroke-width="7" stroke-opacity="0.95" stroke-linecap="round"/>')

    # ---------------- the seal: a separate object, proud of the plate
    add(f'<ellipse cx="{SEAL_CX}" cy="{SEAL_CY}" rx="{SEAL_R_OUT * 1.5}" '
        f'ry="{SEAL_R_OUT * 1.5}" fill="url(#glow)" filter="url(#softglow)"/>')
    add('<g filter="url(#sealshadow)">')
    add(f'<path d="{scalloped(SEAL_CX, SEAL_CY, SEAL_R_OUT, SEAL_R_IN, SEAL_LOBES)}" '
        f'fill="url(#seal)"/>')
    add('</g>')
    # lit rim on the seal's top-left, the mirror of the socket's shading
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SEAL_R_IN - 3, 150, 300)}" fill="none" '
        f'stroke="#FFC3A6" stroke-width="6" stroke-opacity="0.65" stroke-linecap="round"/>')
    # the die: one debossed concentric ring and a raised centre boss
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SEAL_RING_R}" fill="none" '
        f'stroke="{ACCENT_DEEP}" stroke-width="9" stroke-opacity="0.55"/>')
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SEAL_BOSS_R}" fill="url(#boss)"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SEAL_BOSS_R - 3, 155, 295)}" fill="none" '
        f'stroke="#FFD3BC" stroke-width="5" stroke-opacity="0.55" stroke-linecap="round"/>')

    add('</g>')  # plateclip
    add('</g>')  # tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
