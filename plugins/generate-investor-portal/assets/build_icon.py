#!/usr/bin/env python3
"""Build the generate-investor-portal icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

Metaphor — "The withheld cell": a porcelain relief of a figures-table fragment,
three hairline rules bleeding off the tile so it reads as a torn-out piece of a
larger record. The filled cells are shallow, low-contrast blocks that recede.
One cell is empty — a crisply finished porcelain chip standing proud in the
column where a figure should be, the brightest thing on the tile — and a
vermilion bracket sits in the gap to mark it. The number that is not there is
the point: a missing figure becomes a marked placeholder, never an invented
value.

    python3 build_icon.py            # writes icon-src.svg beside this file
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground (porcelain; the family constant, shared with tui-craft et al.)
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"

# ---- the rules: three hairlines bleeding off both edges, so the record reads as
#      a fragment of something larger. The middle one runs behind the withheld
#      cell and is interrupted by it — only its stubs survive.
RULE_Y = (320, 512, 704)
RULE_W = 4
RULE_DARK = "#3F4652"
RULE_DARK_OP = 0.17
RULE_LIT = "#FFFFFF"
RULE_LIT_OP = 0.9

# ---- the withheld row: only the chip's own contact shadow marks it out, so the
#      three rules above stay the only ruling on the tile
# ---- the filled cells: they recede, so nothing here is ever the focal.
#      figures share the withheld cell's right edge — a column, with no grid.
BLOCK = "#4E5560"
BLOCK_OP_LABEL = 0.24
BLOCK_OP_FIG = 0.19
BLOCK_H = 42
BLOCK_R = 11
# (x, y, w, opacity) — the outer rows fall outside the ruled pair, so they read as
# the record continuing past the fragment and never crowd the withheld cell
BLOCKS = (
    (148, 252, 176, BLOCK_OP_LABEL),
    (556, 252, 236, BLOCK_OP_FIG),
    (96, 444, 116, BLOCK_OP_LABEL),   # stub, cut short by the withheld cell
    (148, 720, 196, BLOCK_OP_LABEL),
    (600, 720, 192, BLOCK_OP_FIG),
)

# ---- the withheld cell: the object of the icon. A crisply finished porcelain
#      chip standing proud where a figure should be — brightest, and empty.
WELL_X, WELL_Y, WELL_W, WELL_H, WELL_R = 232, 396, 560, 232, 44
WELL_HI = "#FFFFFF"
WELL_LO = "#F3F0E8"
WELL_RIM = "#FFFFFF"
WELL_EDGE = "#B2A996"
CONTACT = "#6B5F4C"

# ---- the bracket (the one warm accent, spent here and nowhere else)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
BR_STROKE = 32
BR_H = 128
BR_ARM = 66
BR_GAP = 320             # outer span of the pair; the void it holds open is 188


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def bracket(x, y, arm, h, left=True):
    """One half of a square bracket, drawn as strokes: arm, spine, arm."""
    sign = 1 if left else -1
    return (f'M{x + sign * arm},{y} H{x} V{y + h} H{x + sign * arm}')


def build() -> str:
    parts: list[str] = []
    add = parts.append

    br_cx = WELL_X + WELL_W / 2
    br_cy = WELL_Y + WELL_H / 2
    br_left = br_cx - BR_GAP / 2
    br_right = br_cx + BR_GAP / 2
    br_top = br_cy - BR_H / 2

    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ---------------- defs
    add('<defs>')
    add(f'''<radialGradient id="ground" cx="0.42" cy="0.34" r="0.82">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.62" stop-color="{GROUND_LO}"/>
      <stop offset="1" stop-color="{GROUND_EDGE}"/>
    </radialGradient>''')
    add(f'''<linearGradient id="floor" x1="0.08" y1="0" x2="0.92" y2="1">
      <stop offset="0" stop-color="{WELL_HI}"/>
      <stop offset="1" stop-color="{WELL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.4" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="#D9491F"/>
    </linearGradient>''')
    add(f'''<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    add('''<filter id="softglow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>''')
    add(f'''<filter id="chipshadow" x="-30%" y="-40%" width="160%" height="200%">
      <feDropShadow dx="0" dy="13" stdDeviation="15" flood-color="{CONTACT}"
                    flood-opacity="0.36"/>
    </filter>''')
    add(f'<clipPath id="wellclip"><path d="{rounded(WELL_X, WELL_Y, WELL_W, WELL_H, WELL_R)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ---------------- ground
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')

    # ---------------- three rules, bleeding off both edges: a fragment, not a grid
    for y in RULE_Y:
        add(f'<rect x="-8" y="{y}" width="{S + 16}" height="{RULE_W}" '
            f'fill="{RULE_DARK}" fill-opacity="{RULE_DARK_OP}"/>')
        add(f'<rect x="-8" y="{y + RULE_W}" width="{S + 16}" height="{RULE_W}" '
            f'fill="{RULE_LIT}" fill-opacity="{RULE_LIT_OP}"/>')

    # ---------------- the filled cells, receding
    for x, y, w, op in BLOCKS:
        add(f'<rect x="{x}" y="{y}" width="{w}" height="{BLOCK_H}" rx="{BLOCK_R}" '
            f'fill="{BLOCK}" fill-opacity="{op}"/>')

    # ---------------- the withheld cell: a finished chip standing proud, empty
    add('<g filter="url(#chipshadow)">')
    add(f'<path d="{rounded(WELL_X, WELL_Y, WELL_W, WELL_H, WELL_R)}" fill="url(#floor)"/>')
    add('</g>')
    # rim light on the lit (top-left) edges, the mark of a raised object
    add(f'<path d="M{WELL_X + WELL_R},{WELL_Y + 2.5} h{WELL_W - 2 * WELL_R}" fill="none" '
        f'stroke="{WELL_RIM}" stroke-width="4" stroke-opacity="0.95" stroke-linecap="round"/>')
    add(f'<path d="M{WELL_X + 2.5},{WELL_Y + WELL_R} v{WELL_H - 2 * WELL_R}" fill="none" '
        f'stroke="{WELL_RIM}" stroke-width="4" stroke-opacity="0.7" stroke-linecap="round"/>')
    # the crisp cut edge — this is what makes the empty cell the finished one
    add(f'<path d="{rounded(WELL_X, WELL_Y, WELL_W, WELL_H, WELL_R)}" fill="none" '
        f'stroke="{WELL_EDGE}" stroke-width="3" stroke-opacity="0.8"/>')

    # ---------------- the bracket holding the gap open
    add('<g clip-path="url(#wellclip)">')
    add(f'<ellipse cx="{br_cx}" cy="{br_cy}" rx="{BR_GAP * 1.1}" ry="{BR_H * 1.5}" '
        f'fill="url(#glow)" filter="url(#softglow)"/>')
    add('</g>')
    add(f'<g fill="none" stroke="url(#accent)" stroke-width="{BR_STROKE}" '
        f'stroke-linecap="round" stroke-linejoin="round">')
    add(f'<path d="{bracket(br_left, br_top, BR_ARM, BR_H, left=True)}"/>')
    add(f'<path d="{bracket(br_right, br_top, BR_ARM, BR_H, left=False)}"/>')
    add('</g>')

    add('</g>')  # tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
