#!/usr/bin/env python3
"""Build the ux-craft icon master.

Geometry and material live here as named constants so a revision is a parameter
edit rather than path surgery.

Metaphor: the state grid — an instrument panel of six states, five of them poured
as lit porcelain gel keys in relief, one of them vermilion because that is the
state the flow is actually in. The sixth is not a key of another colour. It is a
hole: the panel is cut clean through at that cell, the bench shows at the bottom
of it, and its inner wall carries the occlusion of a real aperture. The lattice
reads complete for a beat and then the eye falls into the gap, which is the whole
thesis — the state nobody designed is the one the user will find.

    python3 build_icon.py            # writes icon-src.svg beside this file
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024  # canvas

# ---- ground (porcelain, the family register)
GROUND_HI = "#FDFCFA"
GROUND_LO = "#E7E4DC"
GROUND_EDGE = "#D8D3C9"
SHADOW = "#3A3126"     # the family's warm shadow ink

# ---- the lattice, which sizes the panel rather than the other way round
COLS, ROWS = 3, 2
CELL = 176             # square cells, so the void is as tall as it is wide
GUTTER = 24            # rib between cells
BEZEL = 38             # panel edge to the outer cells
CELL_R = 34
VOID_CELL = (1, 1)     # row, col — the state nobody designed
ACCENT_CELL = (0, 0)   # row, col — the state the flow is in

# ---- the panel
PANEL_W = COLS * CELL + (COLS - 1) * GUTTER + 2 * BEZEL
PANEL_H = ROWS * CELL + (ROWS - 1) * GUTTER + 2 * BEZEL
PANEL_X = (S - PANEL_W) // 2
PANEL_Y = (S - PANEL_H) // 2
PANEL_R = 62
PANEL_HI = "#FBF8F2"
PANEL_LO = "#E0DACD"
PANEL_EDGE = "#C2B9A6"

# ---- the keys, poured into relief
KEY_HI = "#FFFFFE"
KEY_LO = "#EBE5D9"

# ---- the void: an aperture, not a fill. Nothing is painted into it except the
#      occlusion any real cut edge would carry. Under a top-left key an aperture's
#      top and left inner walls are back-facing and its bottom and right walls are
#      lit, so that asymmetry is what separates a hole from a darker tile.
VOID_FLOOR = 0.05      # how much the bench darkens where the panel is missing
VOID_DEPTH = 0.34      # ambient inside the aperture
VOID_LIP = 54          # how far the shaded top wall reaches in
VOID_WALL = 48         # how far the shaded left wall reaches in

# ---- accent (one warm hue; ACCENT_LO is the same hue kept saturated in shadow,
#      because a gel that goes brown where it turns away reads opaque)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ACCENT_LO = "#C63C15"

# ---- material
SHEEN_H = 30           # the soft top-edge sheen on each key


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def build() -> str:
    def cell_xy(row, col):
        return (PANEL_X + BEZEL + col * (CELL + GUTTER),
                PANEL_Y + BEZEL + row * (CELL + GUTTER))

    vx, vy = cell_xy(*VOID_CELL)
    void = rounded(vx, vy, CELL, CELL, CELL_R)
    panel = rounded(PANEL_X, PANEL_Y, PANEL_W, PANEL_H, PANEL_R)

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
    add(f'''<linearGradient id="panel" x1="0.08" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{PANEL_HI}"/>
      <stop offset="0.55" stop-color="#EFEADE"/>
      <stop offset="1" stop-color="{PANEL_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="key" x1="0.05" y1="0" x2="0.9" y2="1">
      <stop offset="0" stop-color="{KEY_HI}"/>
      <stop offset="0.55" stop-color="#F7F3EA"/>
      <stop offset="1" stop-color="{KEY_LO}"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0.05" y1="0" x2="0.9" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.52" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_LO}"/>
    </linearGradient>''')
    add(f'''<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    # one soft key from the top-left: every rim stroke reads off this
    add('''<linearGradient id="rim" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.80"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>''')
    add('''<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.48"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>''')
    # a cut edge runs the other way from a raised one: the lip the light enters
    # over is occluded, the far lip catches the bounce off the bench
    add(f'''<linearGradient id="cut" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.46"/>
      <stop offset="0.55" stop-color="{SHADOW}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.62"/>
    </linearGradient>''')
    add(f'''<linearGradient id="hollow" x1="0.05" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="{VOID_DEPTH}"/>
      <stop offset="0.5" stop-color="{SHADOW}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="wall" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.48"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.42"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<filter id="panelshadow" x="-25%" y="-25%" width="150%" height="165%">
      <feDropShadow dx="0" dy="18" stdDeviation="21" flood-color="{SHADOW}"
                    flood-opacity="0.32"/>
    </filter>''')
    add(f'''<filter id="keyshadow" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="6" dy="11" stdDeviation="9" flood-color="{SHADOW}"
                    flood-opacity="0.30"/>
    </filter>''')
    add('''<filter id="softglow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>''')
    add(f'<clipPath id="voidclip"><path d="{void}"/></clipPath>')
    tile = SQUIRCLE.read_text().strip()
    add(f'<clipPath id="tile"><path d="{tile}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#tile)">')

    # ---------------- ground: a cushion, not a print
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<path d="{tile}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" '
        f'stroke-width="7"/>')

    # ---------------- the panel, cut clean through at the void cell
    add('<g filter="url(#panelshadow)">')
    add(f'<path d="{panel} {void}" fill-rule="evenodd" fill="url(#panel)"/>')
    add('</g>')
    add(f'<path d="{panel}" fill="none" stroke="{PANEL_EDGE}" stroke-opacity="0.55" '
        f'stroke-width="2"/>')
    add(f'<path d="{panel}" fill="none" stroke="url(#rim)" stroke-width="4"/>')

    # ---------------- the aperture: nothing is painted here but the occlusion a
    #                  real cut edge carries, so the bench shows through
    add('<g clip-path="url(#voidclip)">')
    add(f'<rect x="{vx}" y="{vy}" width="{CELL}" height="{CELL}" fill="{SHADOW}" '
        f'fill-opacity="{VOID_FLOOR}"/>')
    add(f'<rect x="{vx}" y="{vy}" width="{CELL}" height="{CELL}" fill="url(#hollow)"/>')
    add(f'<rect x="{vx}" y="{vy}" width="{CELL}" height="{VOID_LIP}" fill="url(#lip)"/>')
    add(f'<rect x="{vx}" y="{vy}" width="{VOID_WALL}" height="{CELL}" fill="url(#wall)"/>')
    add('</g>')
    add(f'<path d="{void}" fill="none" stroke="url(#cut)" stroke-width="5"/>')

    # ---------------- the keys
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) == VOID_CELL:
                continue
            x, y = cell_xy(row, col)
            keypath = rounded(x, y, CELL, CELL, CELL_R)
            is_accent = (row, col) == ACCENT_CELL

            if is_accent:
                add(f'<ellipse cx="{x + CELL / 2}" cy="{y + CELL / 2}" '
                    f'rx="{CELL * 0.60}" ry="{CELL * 0.60}" fill="url(#glow)" '
                    f'filter="url(#softglow)"/>')

            add('<g filter="url(#keyshadow)">')
            add(f'<path d="{keypath}" fill="url(#{"accent" if is_accent else "key"})"/>')
            add('</g>')
            # soft top-edge sheen: thick gel, one key light, no hard specular
            add(f'<path d="{rounded(x + 9, y + 8, CELL - 18, SHEEN_H, 16)}" '
                f'fill="url(#sheen)"/>')
            add(f'<path d="{keypath}" fill="none" stroke="url(#rim)" stroke-width="3"/>')

    add('</g>')  # tile
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
