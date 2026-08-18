#!/usr/bin/env python3
"""Build the mac-craft icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

Metaphor: the measured sill. The top-left corner of a macOS window as a thick
slab of porcelain gel, cropped hard so the corner and its titlebar band are the
whole tile and the rest of the window bleeds off the edge. The traffic lights are
three recessed wells rather than three coloured dots, because the family spends
exactly one hue and it is not spent here. It is spent on the caliper: a scale
ruled down the height of the band, whose zero graduation is vermilion and lands
exactly on the band's lower edge. The icon states a measurement, it does not
depict a window.

    python3 build_icon.py            # writes icon-src.svg beside this file
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground (the family porcelain: tui-craft, proctor, discipline, should-compact)
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"
# the key light is top-left, so the ground the corner sits against is pushed to
# the darker end of the same ramp — that separation is what makes the corner read.
GROUND_CX, GROUND_CY = 0.66, 0.60

# ---- the slab. Runs off the right and bottom edges: only the corner is in frame.
PLATE_X, PLATE_Y, PLATE_R = 118, 250, 104
PLATE_SPAN = 1500
BEVEL = 14                 # chamfer catching the key light — the slab's thickness

BEVEL_HI = "#FFFFFF"
BEVEL_LO = "#F2EFE6"
SEAT = "#BEB7A6"           # hairline where the slab meets the ground
OCCLUSION = "#7E7664"      # soft contact darkening around the corner

# ---- the sill: the titlebar band, lit, over a body that recedes. The band takes
#      the largest share of the tile — the crop exists to make it the subject.
BAND_H = 430
BAND_HI = "#FBF9F3"
BAND_LO = "#F0EDE3"
BODY_HI = "#E3DED3"
BODY_LO = "#D4CEC1"
DIVIDER = "#B6AE9C"        # the band's lower edge — what the caliper measures to

# ---- traffic lights as recessed wells
WELL_R = 50
WELL_GAP = 138
WELL_X0 = PLATE_X + 124
WELL_TOP = "#BAB2A1"
WELL_BOT = "#DDD9CE"
WELL_SHADE = "#7A7260"
WELL_LIP = "#FFFFFF"
WELL_EDGE = "#A79F8C"      # hairline defining the hole at every size
WELL_ARC_INSET = 5         # the shading sits inside the rim, not straddling it

# ---- the caliper
CAL_X = 626
CAL_TOP_INSET = 30         # keeps the top graduation clear of the slab's chamfer
CAL_STEM = "#948C79"
CAL_TICK = "#7C7462"
TICK_DATUM = 142           # the top graduation, on the sill's upper surface
TICK_MINOR = 76
TICK_ZERO = 244            # the vermilion one, on the band's lower edge
INTERVALS = 4

# ---- accent (one warm hue, nothing else)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ZERO_H = 30                # the notch that has to survive 32px


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def half_arc(cx, cy, r, lit):
    """Semicircular arc on a well's rim. lit=False is the shaded top-left half."""
    k = 0.7071067811865476
    a = (cx - k * r, cy + k * r)
    b = (cx + k * r, cy - k * r)
    p, q = (b, a) if lit else (a, b)
    return f'M{p[0]:.1f},{p[1]:.1f} A{r},{r} 0 0 1 {q[0]:.1f},{q[1]:.1f}'


def build() -> str:
    plate = rounded(PLATE_X, PLATE_Y, PLATE_SPAN, PLATE_SPAN, PLATE_R)
    face = rounded(PLATE_X + BEVEL, PLATE_Y + BEVEL,
                   PLATE_SPAN - 2 * BEVEL, PLATE_SPAN - 2 * BEVEL, PLATE_R - BEVEL)
    band_top = PLATE_Y + BEVEL
    band_bot = PLATE_Y + BAND_H              # the band's lower edge
    cal_top = band_top + CAL_TOP_INSET
    step = (band_bot - cal_top) / INTERVALS
    well_cy = cal_top + (band_bot - cal_top) / 2

    parts: list[str] = []
    add = parts.append

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ---------------- defs
    add('<defs>')
    add(f'''<radialGradient id="ground" cx="{GROUND_CX}" cy="{GROUND_CY}" r="0.82">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.62" stop-color="{GROUND_LO}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<linearGradient id="bevel" x1="0" y1="0" x2="0.5" y2="1">
      <stop offset="0" stop-color="{BEVEL_HI}"/>
      <stop offset="1" stop-color="{BEVEL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="band" x1="0.05" y1="0" x2="0.8" y2="1">
      <stop offset="0" stop-color="{BAND_HI}"/>
      <stop offset="1" stop-color="{BAND_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="body" x1="0.05" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{BODY_HI}"/>
      <stop offset="1" stop-color="{BODY_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="sillcast" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{OCCLUSION}" stop-opacity="0.36"/>
      <stop offset="1" stop-color="{OCCLUSION}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="wellfill" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="{WELL_TOP}"/>
      <stop offset="1" stop-color="{WELL_BOT}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0" y1="0" x2="0.18" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>''')
    add(f'''<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.38"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    add('''<filter id="ao" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="13"/>
    </filter>''')
    add('''<filter id="wellsoft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.6"/>
    </filter>''')
    add('''<filter id="softglow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>''')
    add(f'<clipPath id="faceclip"><path d="{face}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ---------------- ground
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')

    # ---------------- contact occlusion hugging the corner, so the slab reads thick
    add(f'<path d="{plate}" fill="none" stroke="{OCCLUSION}" stroke-width="30" '
        f'stroke-opacity="0.22" filter="url(#ao)"/>')

    # ---------------- the slab: bevel catching the key light, then its face
    add(f'<path d="{plate}" fill="url(#bevel)"/>')
    add(f'<path d="{plate}" fill="none" stroke="{SEAT}" stroke-width="2.5" '
        f'stroke-opacity="0.8"/>')

    add('<g clip-path="url(#faceclip)">')
    # the sill, then the body it sits above
    add(f'<rect x="{PLATE_X}" y="{PLATE_Y}" width="{PLATE_SPAN}" '
        f'height="{band_bot - PLATE_Y}" fill="url(#band)"/>')
    add(f'<rect x="{PLATE_X}" y="{band_bot}" width="{PLATE_SPAN}" '
        f'height="{PLATE_SPAN}" fill="url(#body)"/>')
    add(f'<rect x="{PLATE_X}" y="{band_bot}" width="{PLATE_SPAN}" height="30" '
        f'fill="url(#sillcast)"/>')
    add(f'<line x1="{PLATE_X}" y1="{band_bot}" x2="{PLATE_X + PLATE_SPAN}" '
        f'y2="{band_bot}" stroke="{DIVIDER}" stroke-width="2.5"/>')

    # ---------------- traffic lights as three recessed wells: a floor, a hairline
    #                  rim, and soft shading off the near and far inner walls
    ar = WELL_R - WELL_ARC_INSET
    for i in range(3):
        cx = WELL_X0 + i * WELL_GAP
        add(f'<circle cx="{cx}" cy="{well_cy:.1f}" r="{WELL_R}" '
            f'fill="url(#wellfill)"/>')
        add(f'<g filter="url(#wellsoft)" stroke-width="9" fill="none" '
            f'stroke-linecap="round">')
        add(f'<path d="{half_arc(cx, well_cy, ar, lit=False)}" '
            f'stroke="{WELL_SHADE}" stroke-opacity="0.50"/>')
        add(f'<path d="{half_arc(cx, well_cy, ar, lit=True)}" '
            f'stroke="{WELL_LIP}" stroke-opacity="0.80"/>')
        add('</g>')
        add(f'<circle cx="{cx}" cy="{well_cy:.1f}" r="{WELL_R}" fill="none" '
            f'stroke="{WELL_EDGE}" stroke-width="2.5" stroke-opacity="0.8"/>')

    # ---------------- the caliper, ruled down the height of the band
    add(f'<line x1="{CAL_X}" y1="{cal_top:.1f}" x2="{CAL_X}" y2="{band_bot}" '
        f'stroke="{CAL_STEM}" stroke-width="5" stroke-opacity="0.95"/>')
    add(f'<g stroke="{CAL_TICK}" stroke-width="7" stroke-opacity="0.9" '
        f'stroke-linecap="round">')
    for k in range(INTERVALS):
        y = cal_top + k * step
        length = TICK_DATUM if k == 0 else TICK_MINOR
        add(f'<line x1="{CAL_X}" y1="{y:.1f}" x2="{CAL_X + length}" y2="{y:.1f}"/>')
    add('</g>')

    # ---------------- the signature: the zero graduation, on the band's lower edge
    add(f'<ellipse cx="{CAL_X + TICK_ZERO / 2}" cy="{band_bot}" '
        f'rx="{TICK_ZERO * 0.62:.0f}" ry="{ZERO_H * 2.4:.0f}" fill="url(#bloom)" '
        f'filter="url(#softglow)"/>')
    add(f'<rect x="{CAL_X}" y="{band_bot - ZERO_H / 2:.1f}" width="{TICK_ZERO}" '
        f'height="{ZERO_H}" rx="{ZERO_H / 2}" fill="url(#accent)"/>')
    add(f'<rect x="{CAL_X + 6}" y="{band_bot - ZERO_H / 2 + 3:.1f}" '
        f'width="{TICK_ZERO - 12}" height="5" rx="2.5" fill="{ACCENT_HI}" '
        f'fill-opacity="0.85"/>')

    add('</g>')  # faceclip

    # ---------------- lit rim on the slab's top and left edges only
    add(f'<path d="M{PLATE_X + 2},{PLATE_Y + PLATE_SPAN} '
        f'V{PLATE_Y + PLATE_R} a{PLATE_R},{PLATE_R} 0 0 1 {PLATE_R},{-PLATE_R} '
        f'h{PLATE_SPAN - 2 * PLATE_R}" fill="none" stroke="#FFFFFF" '
        f'stroke-width="5" stroke-opacity="0.95"/>')

    add('</g>')  # tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
