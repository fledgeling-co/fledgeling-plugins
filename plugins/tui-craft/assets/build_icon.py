#!/usr/bin/env python3
"""Build the tui-craft icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

Metaphor: a terminal panel with its character grid ruled across it, one glyph
occupying TWO cells, and a caliper measuring that width. That is the skill in
one image — the difference between counting characters and measuring cells.

    python3 build_icon.py            # writes icon-src.svg beside this file
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground (sampled from the marketplace family: proctor, discipline, should-compact)
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"

# ---- device
DEV_HI = "#39404A"     # top-left, catching the key light
DEV_LO = "#171B21"     # bottom-right
DEV_RIM = "#59626F"    # 1px rim on the lit edge
DEV_X, DEV_Y, DEV_W, DEV_H, DEV_R = 168, 236, 688, 560, 64

# ---- grid
CELL_W, CELL_H = 56, 68
GRID_PAD_X, GRID_PAD_Y = 40, 46
GRID_LINE = "#8A94A3"
GRID_OPACITY = 0.22

# ---- accent (one warm hue, nothing else)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ACCENT_GLOW = "#E8542A"

# ---- dim text runs
TEXT_DIM = "#78838F"


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def build() -> str:
    gx0 = DEV_X + GRID_PAD_X
    gy0 = DEV_Y + GRID_PAD_Y
    cols = (DEV_W - 2 * GRID_PAD_X) // CELL_W
    rows = (DEV_H - 2 * GRID_PAD_Y) // CELL_H

    # The lit glyph sits on the middle row, and is two cells wide.
    lit_col, lit_row, lit_span = 4, 3, 2
    lx = gx0 + lit_col * CELL_W
    ly = gy0 + lit_row * CELL_H
    lw = lit_span * CELL_W

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
    add(f'''<linearGradient id="device" x1="0.12" y1="0" x2="0.9" y2="1">
      <stop offset="0" stop-color="{DEV_HI}"/>
      <stop offset="0.55" stop-color="#232932"/>
      <stop offset="1" stop-color="{DEV_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>''')
    add(f'''<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT_GLOW}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{ACCENT_GLOW}" stop-opacity="0"/>
    </radialGradient>''')
    add('''<filter id="devshadow" x="-25%" y="-25%" width="150%" height="160%">
      <feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#3A3126"
                    flood-opacity="0.34"/>
    </filter>''')
    add('''<filter id="softglow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>''')
    add(f'<clipPath id="devclip"><path d="{rounded(DEV_X, DEV_Y, DEV_W, DEV_H, DEV_R)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{SQUIRCLE.read_text().strip()}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    # The four named layers below are the layer plan the audit sheet claims and
    # `fidelity.py structure` requires: bg / mid / fg / highlight. They are pure
    # wrappers carrying no presentation attributes, so grouping is free — adding
    # them left the 1024 render byte-identical. The ids cannot reuse `ground`,
    # `device` or `accent`, which are gradient ids already live in <defs>.
    add('<g id="art" clip-path="url(#tile)">')

    # ---------------- bg: ground
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add('</g>')

    # ---------------- mid: device shell and its rim light
    add('<g id="mid">')
    add(f'<g filter="url(#devshadow)">')
    add(f'<path d="{rounded(DEV_X, DEV_Y, DEV_W, DEV_H, DEV_R)}" fill="url(#device)"/>')
    add('</g>')

    # rim light along the top and left edge
    add(f'<path d="{rounded(DEV_X, DEV_Y, DEV_W, DEV_H, DEV_R)}" fill="none" '
        f'stroke="{DEV_RIM}" stroke-width="3" stroke-opacity="0.55"/>')
    add(f'<path d="M{DEV_X + DEV_R},{DEV_Y + 2} h{DEV_W - 2 * DEV_R}" fill="none" '
        f'stroke="#7C8695" stroke-width="3" stroke-opacity="0.5" stroke-linecap="round"/>')
    add('</g>')

    add('<g clip-path="url(#devclip)">')

    # ---------------- fg: grid
    add(f'<g id="fg" stroke="{GRID_LINE}" stroke-opacity="{GRID_OPACITY}" stroke-width="2">')
    for c in range(cols + 1):
        x = gx0 + c * CELL_W
        add(f'<line x1="{x}" y1="{gy0}" x2="{x}" y2="{gy0 + rows * CELL_H}"/>')
    for r in range(rows + 1):
        y = gy0 + r * CELL_H
        add(f'<line x1="{gx0}" y1="{y}" x2="{gx0 + cols * CELL_W}" y2="{y}"/>')
    add('</g>')

    # ---------------- dim text runs, so the panel reads as a screen with content
    runs = [(0, 0, 3), (0, 4, 2), (1, 0, 2), (1, 3, 4), (2, 0, 5),
            (3, 0, 3), (3, 7, 1), (4, 0, 2), (4, 3, 3)]
    for r, c, span in runs:
        if r == lit_row and not (c + span <= lit_col or c >= lit_col + lit_span):
            continue
        x = gx0 + c * CELL_W + 8
        y = gy0 + r * CELL_H + CELL_H * 0.30
        w = span * CELL_W - 16
        add(f'<rect x="{x}" y="{y:.0f}" width="{w}" height="{CELL_H * 0.34:.0f}" rx="6" '
            f'fill="{TEXT_DIM}" fill-opacity="0.30"/>')

    # ---------------- highlight: the lit glyph, TWO cells wide, and its caliper
    add('<g id="highlight">')
    add(f'<ellipse cx="{lx + lw / 2}" cy="{ly + CELL_H / 2}" rx="{lw * 0.95}" '
        f'ry="{CELL_H * 1.1}" fill="url(#glow)" filter="url(#softglow)"/>')
    add(f'<rect x="{lx + 5}" y="{ly + 5}" width="{lw - 10}" height="{CELL_H - 10}" rx="8" '
        f'fill="url(#accent)"/>')
    # the cell division inside the glyph — this is the whole idea, one glyph across two cells
    add(f'<line x1="{lx + CELL_W}" y1="{ly + 14}" x2="{lx + CELL_W}" y2="{ly + CELL_H - 14}" '
        f'stroke="#FFF2EC" stroke-opacity="0.45" stroke-width="3"/>')

    # ---------------- caliper measuring those two cells
    cy = ly + CELL_H + 34
    tick = 20
    add(f'<g stroke="{ACCENT}" stroke-width="7" stroke-linecap="round" fill="none">')
    add(f'<line x1="{lx + 4}" y1="{cy - tick}" x2="{lx + 4}" y2="{cy + tick}"/>')
    add(f'<line x1="{lx + lw - 4}" y1="{cy - tick}" x2="{lx + lw - 4}" y2="{cy + tick}"/>')
    add(f'<line x1="{lx + 4}" y1="{cy}" x2="{lx + lw - 4}" y2="{cy}"/>')
    add('</g>')

    add('</g>')  # highlight
    add('</g>')  # devclip
    add('</g>')  # art / tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
