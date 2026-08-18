#!/usr/bin/env python3
"""Build the deck-craft icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

Metaphor: the letterboxed stage. One 16:9 plate of porcelain gel floats inside a
shallow recess, so it reads as being *inside* a frame, with the letterbox margin
showing as a band of the recess above and below it. A single vermilion rule runs
the full width of the plate's bottom edge — the zero baseline every slide is
built up from, and the one thing in the tile that is allowed to be warm.

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

# ---- the recess: same porcelain hue, two value steps down, so the plate can be
#      the brightest thing in the tile without leaving the family palette. The
#      range is deliberately tight — the letterbox bands above and below have to
#      read as a matched pair, so the recess is one value, not a ramp.
WELL_TOP = "#BCB5A5"   # the shaded upper inner wall
WELL_BOT = "#CBC5B5"   # the floor toward the lower lip
WELL_EDGE = "#ADA593"  # hairline where the recess cuts the ground
WELL_LIP = "#FFFFFF"   # the frame's lower lip catching the key light
WELL_SHADE = "#5E5847"  # the inner-shadow tint

# ---- the frame. Height is derived so the letterbox band is exact top and bottom.
WELL_X, WELL_W, WELL_R = 140, 744, 60
PLATE_INSET_X = 48     # side margin between frame and plate
LETTERBOX = 88         # the band of recess visible above and below the plate

# ---- the plate: 16:9, porcelain gel, key light from the top-left
PLATE_HI = "#FFFFFE"
PLATE_LO = "#EDEAE1"
PLATE_RIM = "#FFFFFF"
PLATE_EDGE = "#C6BFB0"
PLATE_R = 18

# ---- accent (one warm hue, nothing else)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
RULE_H = 34            # the zero baseline, full plate width, never truncated

SHADOW = "#3A3126"

# ---- derived geometry
PLATE_W = WELL_W - 2 * PLATE_INSET_X
PLATE_H = int(PLATE_W * 9 / 16)
WELL_H = PLATE_H + 2 * LETTERBOX
WELL_Y = (S - WELL_H) // 2
PLATE_X = WELL_X + PLATE_INSET_X
PLATE_Y = WELL_Y + LETTERBOX


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def build() -> str:
    well = rounded(WELL_X, WELL_Y, WELL_W, WELL_H, WELL_R)
    plate = rounded(PLATE_X, PLATE_Y, PLATE_W, PLATE_H, PLATE_R)
    rule_y = PLATE_Y + PLATE_H - RULE_H

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
    add(f'''<linearGradient id="wellfill" x1="0" y1="0" x2="0.18" y2="1">
      <stop offset="0" stop-color="{WELL_TOP}"/>
      <stop offset="1" stop-color="{WELL_BOT}"/>
    </linearGradient>''')
    # the inner shadow lives only in the top sliver and the lit lip only in the
    # bottom sliver, so the two letterbox bands hold the same value between them
    add(f'''<linearGradient id="wellshadeV" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{WELL_SHADE}" stop-opacity="0.28"/>
      <stop offset="0.022" stop-color="{WELL_SHADE}" stop-opacity="0.09"/>
      <stop offset="0.046" stop-color="{WELL_SHADE}" stop-opacity="0"/>
      <stop offset="0.976" stop-color="{WELL_LIP}" stop-opacity="0"/>
      <stop offset="1" stop-color="{WELL_LIP}" stop-opacity="0.20"/>
    </linearGradient>''')
    add(f'''<linearGradient id="wellshadeH" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{WELL_SHADE}" stop-opacity="0.20"/>
      <stop offset="0.035" stop-color="{WELL_SHADE}" stop-opacity="0"/>
      <stop offset="0.968" stop-color="{WELL_LIP}" stop-opacity="0"/>
      <stop offset="1" stop-color="{WELL_LIP}" stop-opacity="0.14"/>
    </linearGradient>''')
    add(f'''<linearGradient id="platefill" x1="0.1" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{PLATE_HI}"/>
      <stop offset="0.58" stop-color="#F8F5EE"/>
      <stop offset="1" stop-color="{PLATE_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="sheen" x1="0" y1="0" x2="0.25" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0" y1="0" x2="0.22" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>''')
    add(f'''<radialGradient id="bloom" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.15"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    add(f'''<filter id="platesh" x="-20%" y="-20%" width="140%" height="170%">
      <feDropShadow dx="0" dy="16" stdDeviation="17" flood-color="{SHADOW}"
                    flood-opacity="0.36"/>
    </filter>''')
    add('''<filter id="softglow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>''')
    add(f'<clipPath id="wellclip"><path d="{well}"/></clipPath>')
    add(f'<clipPath id="plateclip"><path d="{plate}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ---------------- ground
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')

    # ---------------- the frame's lower lip, peeking below the recess boundary
    add(f'<path d="{rounded(WELL_X, WELL_Y + 4, WELL_W, WELL_H, WELL_R)}" fill="none" '
        f'stroke="{WELL_LIP}" stroke-width="5" stroke-opacity="0.75"/>')

    # ---------------- the recess
    add(f'<path d="{well}" fill="url(#wellfill)"/>')
    add(f'<path d="{well}" fill="none" stroke="{WELL_EDGE}" stroke-width="2.5" '
        f'stroke-opacity="0.7"/>')
    add('<g clip-path="url(#wellclip)">')
    add(f'<rect x="{WELL_X}" y="{WELL_Y}" width="{WELL_W}" height="{WELL_H}" '
        f'fill="url(#wellshadeV)"/>')
    add(f'<rect x="{WELL_X}" y="{WELL_Y}" width="{WELL_W}" height="{WELL_H}" '
        f'fill="url(#wellshadeH)"/>')

    # ---------------- the plate, floating in the recess
    add('<g filter="url(#platesh)">')
    add(f'<path d="{plate}" fill="url(#platefill)"/>')
    add('</g>')
    # seat line all round, then a lit rim on the top-left edges only
    add(f'<path d="{plate}" fill="none" stroke="{PLATE_EDGE}" stroke-width="2.5" '
        f'stroke-opacity="0.75"/>')
    add(f'<path d="M{PLATE_X + 2},{PLATE_Y + PLATE_H - PLATE_R} '
        f'V{PLATE_Y + PLATE_R} a{PLATE_R},{PLATE_R} 0 0 1 {PLATE_R},{-PLATE_R} '
        f'h{PLATE_W - 2 * PLATE_R}" fill="none" stroke="{PLATE_RIM}" '
        f'stroke-width="4" stroke-opacity="0.95" stroke-linecap="round"/>')
    # a soft specular across the upper plate so it reads as gel, not paper
    add('<g clip-path="url(#plateclip)">')
    add(f'<rect x="{PLATE_X}" y="{PLATE_Y}" width="{PLATE_W}" '
        f'height="{int(PLATE_H * 0.62)}" fill="url(#sheen)" opacity="0.42"/>')
    add('</g>')

    # ---------------- warm bounce, sitting below the rule so it lights the lower
    #                  letterbox band rather than washing the plate
    add(f'<ellipse cx="{PLATE_X + PLATE_W / 2}" cy="{rule_y + RULE_H * 1.5:.0f}" '
        f'rx="{PLATE_W * 0.46:.0f}" ry="{RULE_H * 1.2:.0f}" fill="url(#bloom)" '
        f'filter="url(#softglow)"/>')
    add('</g>')  # wellclip

    # ---------------- the signature: one vermilion rule, the plate's full width
    add('<g clip-path="url(#plateclip)">')
    add(f'<rect x="{PLATE_X}" y="{rule_y}" width="{PLATE_W}" height="{RULE_H}" '
        f'fill="url(#accent)"/>')
    add(f'<rect x="{PLATE_X}" y="{rule_y}" width="{PLATE_W}" height="4" '
        f'fill="{ACCENT_HI}" fill-opacity="0.85"/>')
    add('</g>')

    add('</g>')  # tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
