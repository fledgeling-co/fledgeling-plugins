#!/usr/bin/env python3
"""Build the mac-design-digest Engine A2 take — "The Inlaid Plate".

A second hand-authored take, written because Engine B (Arrow) refused the
commission on 19 Aug 2026 with "A positive credit balance is required for all
requests, including BYOK". The three-engine floor is a floor of *takes*, and the
skill's own rule for an unavailable engine is to widen Engine A rather than to
present one take as three — so this is a real artifact, not a recolour of the
master with a new filename.

It attacks the two checks the shipping master measurably loses.

  #7 figure-ground. The master is porcelain-on-porcelain: plate #F7F4ED against
     ground #E7E4DC is 1.16:1, so the object's mass separates by hairline and
     shadow rather than by value. Here the plate is graphite-glazed and the
     ground stays the family porcelain, so the mass separates by value.
  #10 variant robustness. When the ground carries the identity, changing the
     ground register takes the identity with it. A dark mass, one bright bar and
     one warm disc is a value relationship rather than a colour one.

Three constructions differ from the master, so the comparison is not a palette
swap:

  1. Two materials, not one. The plate is a graphite glaze over a porcelain
     body, and every mark on it is that body showing through — the measurement
     is *inlaid* rather than printed, each inlay carrying the glaze's own dark
     cut edge along its lit side.
  2. The socket is a countersink through the glaze into the body, so the seal is
     seated on a porcelain collar. That collar is also what keeps the seal
     legible: vermilion on graphite measures 2.86:1, vermilion on the collar
     3.34:1, and the collar is the surface it actually sits against.
  3. A porcelain fillet along the plate's far bottom-right edge — bounce off the
     ground, the behaviour sampled from apple-12 and apple-27 in the corpus,
     which the master does not carry at all.

Geometry is held identical to `build_icon.py` on purpose: plate box, seal
centre, socket radius and lobe count are the same numbers, so the audit sheet's
#7 delta is attributable to value and material rather than to a relayout.

    python3 build_icon_a2.py        # writes icon-A2-inlaid.svg beside this file
"""

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground: the family porcelain, unchanged from the master
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"

# ---- the value-plate: graphite glaze over a porcelain body.
#      Same box as the master, so the #7 delta is about value, not layout.
PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R = 172, 232, 680, 536, 60
GLAZE_HI = "#535A66"    # top-left, catching the key
GLAZE_MID = "#3A4048"   # the figure-ground number is quoted off this
GLAZE_LO = "#262B32"    # bottom-right, falling away
GLAZE_RIM = "#C2C9D5"   # narrow specular on the lit top-left arris
GLAZE_EDGE = "#191D23"  # the glaze's own dark cut edge
FILLET = "#EFEAE0"      # porcelain bounce off the ground, far bottom-right

# ---- the porcelain body, seen wherever the glaze is cut
BODY_HI = "#FFFEFB"
BODY_MID = "#F3EFE6"
BODY_LO = "#DCD6C9"

# ---- the recorded value, inlaid: a thin label rule, one heavy figure bar,
#      one thin footnote rule. Never glyphs.
LABEL_X, LABEL_Y, LABEL_W, LABEL_H = 240, 328, 236, 20
VALUE_X, VALUE_Y, VALUE_W, VALUE_H, VALUE_R = 240, 392, 336, 66, 22
FOOT_X, FOOT_Y, FOOT_W, FOOT_H = 240, 500, 168, 18

# ---- the seal: the one warm accent, the family vermilion, spent here only
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ACCENT_DEEP = "#B23F1C"
SEAL_CX, SEAL_CY = 692, 594
SEAL_R_OUT, SEAL_R_IN, SEAL_LOBES = 112, 95, 12
SEAL_RING_R = 66
SEAL_BOSS_R = 40
SOCKET_R = 132          # countersink through the glaze; the collar is 20px wide

# ---- relief tuning
CONTACT = "#6B5F4C"     # warm, for the plate's shadow on the porcelain ground
CUT_DARK = "#12151A"    # inside the glaze, where light does not reach


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


def inlay(x, y, w, h, r, fill, edge_op):
    """One inlaid mark: the porcelain body showing through a cut in the glaze.

    An inlay is not a printed bar. The glaze has thickness, so its cut edge sits
    proud of the fill on the lit side and casts a hairline across it — that
    hairline is the whole reason this reads as inlaid rather than drawn on.
    """
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>']
    out.append(f'<path d="M{x + r},{y + 1.5} h{max(w - 2 * r, 1)}" fill="none" '
               f'stroke="{CUT_DARK}" stroke-width="3" stroke-opacity="{edge_op}" '
               f'stroke-linecap="round"/>')
    return out


def build() -> str:
    parts: list[str] = []
    add = parts.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ---------------- defs
    add('<defs>')
    add(f'''<radialGradient id="gnd" cx="0.42" cy="0.34" r="0.82">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.62" stop-color="{GROUND_LO}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<linearGradient id="glaze" x1="0.1" y1="0" x2="0.88" y2="1">
      <stop offset="0" stop-color="{GLAZE_HI}"/>
      <stop offset="0.52" stop-color="{GLAZE_MID}"/>
      <stop offset="1" stop-color="{GLAZE_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="body" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{BODY_HI}"/>
      <stop offset="0.55" stop-color="{BODY_MID}"/>
      <stop offset="1" stop-color="{BODY_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="inlaid" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0" stop-color="{BODY_MID}"/>
      <stop offset="1" stop-color="{BODY_HI}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="wax" x1="0.14" y1="0.04" x2="0.86" y2="0.96">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.42" stop-color="{ACCENT}"/>
      <stop offset="0.82" stop-color="#D64A22"/>
      <stop offset="1" stop-color="{ACCENT_DEEP}"/>
    </linearGradient>''')
    add('''<linearGradient id="die" x1="0.2" y1="0.1" x2="0.8" y2="0.9">
      <stop offset="0" stop-color="#F27A4C"/>
      <stop offset="1" stop-color="#DB4A22"/>
    </linearGradient>''')
    add(f'''<filter id="plateshadow" x="-25%" y="-25%" width="150%" height="165%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="{CONTACT}"
                    flood-opacity="0.38"/>
    </filter>''')
    add(f'''<filter id="sealshadow" x="-45%" y="-45%" width="190%" height="200%">
      <feDropShadow dx="7" dy="13" stdDeviation="11" flood-color="{CUT_DARK}"
                    flood-opacity="0.55"/>
    </filter>''')
    add(f'<clipPath id="plateclip"><path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # One silhouette across the family: the superellipse is a clip, never a
    # baked corner. Named strata so `fidelity.py structure` can count the plan.
    add('<g id="art" clip-path="url(#tile)">')

    # ---------------- bg: the porcelain ground, unchanged from the master
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#gnd)"/>')
    add('</g>')

    # ---------------- mid: the glazed plate, its dark arris and its bounce
    add('<g id="mid">')
    add('<g filter="url(#plateshadow)">')
    add(f'<path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}" fill="url(#glaze)"/>')
    add('</g>')
    add(f'<path d="{rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)}" fill="none" '
        f'stroke="{GLAZE_EDGE}" stroke-width="3" stroke-opacity="0.75"/>')
    # narrow specular on the lit top-left arris
    add(f'<path d="M{PLATE_X + PLATE_R},{PLATE_Y + 3} h{PLATE_W - 2 * PLATE_R}" fill="none" '
        f'stroke="{GLAZE_RIM}" stroke-width="4" stroke-opacity="0.55" stroke-linecap="round"/>')
    add(f'<path d="M{PLATE_X + 3},{PLATE_Y + PLATE_R} v{PLATE_H - 2 * PLATE_R}" fill="none" '
        f'stroke="{GLAZE_RIM}" stroke-width="4" stroke-opacity="0.38" stroke-linecap="round"/>')
    # porcelain bounce off the ground along the far bottom-right edge
    add(f'<path d="M{PLATE_X + PLATE_R},{PLATE_Y + PLATE_H - 3} h{PLATE_W - 2 * PLATE_R}" fill="none" '
        f'stroke="{FILLET}" stroke-width="5" stroke-opacity="0.30" stroke-linecap="round"/>')
    add('</g>')

    add('<g clip-path="url(#plateclip)">')

    # ---------------- fg: the measurement, inlaid, and the countersink
    add('<g id="fg">')
    for chunk in inlay(LABEL_X, LABEL_Y, LABEL_W, LABEL_H, LABEL_H / 2,
                       BODY_MID, 0.30):
        add(chunk)
    for chunk in inlay(VALUE_X, VALUE_Y, VALUE_W, VALUE_H, VALUE_R,
                       "url(#inlaid)", 0.42):
        add(chunk)
    for chunk in inlay(FOOT_X, FOOT_Y, FOOT_W, FOOT_H, FOOT_H / 2,
                       BODY_LO, 0.26):
        add(chunk)

    # The countersink: the glaze cut away to the porcelain body, leaving a 20px
    # collar around the seal. A recess reads inverted to a raised object, so the
    # near top-left inner edge is in shadow and the far bottom-right wall is lit.
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SOCKET_R}" fill="url(#body)"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SOCKET_R - 5, 135, 315)}" fill="none" '
        f'stroke="{CUT_DARK}" stroke-width="11" stroke-opacity="0.34" stroke-linecap="round"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SOCKET_R - 5, 315, 135)}" fill="none" '
        f'stroke="{BODY_HI}" stroke-width="9" stroke-opacity="0.95" stroke-linecap="round"/>')
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SOCKET_R}" fill="none" '
        f'stroke="{GLAZE_EDGE}" stroke-width="3" stroke-opacity="0.55"/>')
    add('</g>')

    # ---------------- highlight: the seal, proud of the collar
    add('<g id="highlight">')
    add('<g filter="url(#sealshadow)">')
    add(f'<path d="{scalloped(SEAL_CX, SEAL_CY, SEAL_R_OUT, SEAL_R_IN, SEAL_LOBES)}" '
        f'fill="url(#wax)"/>')
    add('</g>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SEAL_R_IN - 3, 150, 300)}" fill="none" '
        f'stroke="#FFC3A6" stroke-width="6" stroke-opacity="0.70" stroke-linecap="round"/>')
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SEAL_RING_R}" fill="none" '
        f'stroke="{ACCENT_DEEP}" stroke-width="9" stroke-opacity="0.55"/>')
    add(f'<circle cx="{SEAL_CX}" cy="{SEAL_CY}" r="{SEAL_BOSS_R}" fill="url(#die)"/>')
    add(f'<path d="{arc(SEAL_CX, SEAL_CY, SEAL_BOSS_R - 3, 155, 295)}" fill="none" '
        f'stroke="#FFD3BC" stroke-width="5" stroke-opacity="0.55" stroke-linecap="round"/>')
    add('</g>')

    add('</g>')  # plateclip
    add('</g>')  # art / tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-A2-inlaid.svg"
    out.write_text(build())
    print(f"wrote {out}")
