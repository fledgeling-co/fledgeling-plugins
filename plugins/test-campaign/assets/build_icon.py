#!/usr/bin/env python3
"""build_icon.py — Engine A master for the `test-campaign` icon.

Direction 2, sub-register (a): porcelain cushion + gel objects, in the
fledgeling-plugins house palette sampled out of its two nearest siblings
(whats-left #E06330 accent on a #F6F3EA→#E0D9C8 ground; proctor the same tile
with a #E65017 pixel edge).

Concept — the coverage grid, honest about its holes. Eight captured frames sit
in a three-by-three arrangement. One is filled vermilion: the thing the campaign
actually proved. The ninth is not there at all; in its place is an empty socket
pressed into the cushion, lit from the same top light as everything else, so the
gap is as visible as any pass. That is the whole argument of the plugin in one
shape, and it is why the missing cell is drawn rather than omitted.

Differentiated from the two icons it sits beside in the marketplace: whats-left
is a list that thins upward with one card standing forward; proctor is a stack
of windows with a dithered edge. This one is a matrix, and its subject is the
cell that has nothing in it.

    python3 build_icon.py > icon.svg
"""

import pathlib
import sys

SQ = (pathlib.Path(__file__).resolve().parents[2] / "create-mac-icon" / "assets"
      / "squircle-path.txt")

# ── palette, sampled from the siblings (see icon-notes.md for the readings) ──
GROUND_TOP, GROUND_BOT = "#F8F5EE", "#E4DDCB"
RIM = "#FFFDF8"
# Captured frames are a mid-tone gel, not a near-white card. A porcelain frame
# on a porcelain cushion measured 1.1:1 against its ground and read as white on
# white at every size; the gel register the siblings use is what buys rubric #7.
GEL_TOP, GEL_BOT = "#8B7E6A", "#665B49"
GEL_EDGE = "#544A3B"
ACCENT, ACCENT_HI = "#E4652E", "#F79A61"
SHADOW = "#4A3F2E"

# ── geometry ────────────────────────────────────────────────────────────────
# The grid is the silhouette: eight filled tiles and one absence. Nothing sits
# under them, so "a matrix with a piece missing" is what survives a fill-black.
CELL, GAP, R = 186, 44, 42
ORIGIN = 189                                  # 3*186 + 2*44 = 646, centred in 1024
STEP = CELL + GAP
MISSING = (2, 2)                              # bottom-right: the last cell, empty
PROVEN = (1, 1)                               # centre: the one saturated thing


def xy(col: int, row: int) -> tuple[int, int]:
    return ORIGIN + col * STEP, ORIGIN + row * STEP


def tiles() -> str:
    """The seven quiet frames plus the one that carries the accent (fg plane)."""
    out = []
    for row in range(3):
        for col in range(3):
            if (col, row) == MISSING:
                continue
            x, y = xy(col, row)
            hot = (col, row) == PROVEN
            fill = "url(#hot)" if hot else "url(#gel)"
            edge = ACCENT if hot else GEL_EDGE
            out.append(f"""
      <g>
        <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{R}" fill="{fill}"/>
        <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{R}" fill="none"
              stroke="{edge}" stroke-width="3" opacity=".55"/>
      </g>""")
    return "".join(out)


def tile_highlights() -> str:
    """The top-edge catch and the seated shading, as their own droppable plane.

    Kept out of the fg group on purpose: rubric #10 wants identity carried by
    shape and value, with the lighting as a layer a system tint can flatten
    without the mark stopping being itself.
    """
    out = []
    for row in range(3):
        for col in range(3):
            if (col, row) == MISSING:
                continue
            x, y = xy(col, row)
            hot = (col, row) == PROVEN
            out.append(f"""
      <g>
        <rect x="{x}" y="{y}" width="{CELL}" height="{CELL * 0.44:.0f}" rx="{R}"
              fill="{RIM}" opacity="{.16 if hot else .14}"/>
        <path d="M{x + R} {y + 4} h{CELL - 2 * R}" stroke="{RIM}" stroke-width="7"
              stroke-linecap="round" opacity="{.5 if hot else .40}"/>
        <path d="M{x + R} {y + CELL - 5} h{CELL - 2 * R}" stroke="{SHADOW}"
              stroke-width="6" stroke-linecap="round" opacity=".20"/>
      </g>""")
    return "".join(out)


def socket() -> str:
    """The absence: the cushion itself, pressed, with nothing standing in it.

    Three readings were tried and two failed the same way. A cell filled a shade
    LIGHTER than the cushion read as a third kind of tile; a cell with a floor,
    a strong inner shadow and a rim catch on its lower lip read as a raised tile
    that happened to be pale. Any filled shape in that position is an object.

    So the ninth cell has no fill. It is the ground, at ground luminance, against
    frames measuring about 3:1 darker; the only marks are a soft shadow spilling
    over its top edge from the same light as everything else, and a keyline
    saying a boundary exists. At 16px it is a gap in a grid of dark dots, which
    is the strongest read of the set and the one the plugin is about.
    """
    x, y = xy(*MISSING)
    return f"""
    <g>
      <g clip-path="url(#wellclip)">
        <rect x="{x - 12}" y="{y - 128}" width="{CELL + 24}" height="{CELL}" rx="{R}"
              fill="{SHADOW}" opacity=".34" filter="url(#soft)"/>
      </g>
      <rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{R}" fill="none"
            stroke="{SHADOW}" stroke-width="4" opacity=".20"/>
    </g>"""


def svg() -> str:
    d = SQ.read_text().strip() if SQ.exists() else ""
    if not d:
        print("squircle-path.txt not found — the family shares one silhouette", file=sys.stderr)
        raise SystemExit(1)
    mx, my = xy(*MISSING)
    drop = "".join(
        f'<rect x="{xy(c, r)[0]}" y="{xy(c, r)[1] + 14}" width="{CELL}" height="{CELL}" '
        f'rx="{R}" fill="{SHADOW}"/>'
        for r in range(3) for c in range(3) if (c, r) != MISSING)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vig" cx=".5" cy=".42" r=".78">
      <stop offset=".55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity=".17"/>
    </radialGradient>
    <linearGradient id="gel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GEL_TOP}"/><stop offset="1" stop-color="{GEL_BOT}"/>
    </linearGradient>
    <linearGradient id="hot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/><stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>
    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="15"/>
    </filter>
    <filter id="contact" x="-30%" y="-30%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <clipPath id="mask"><path d="{d}"/></clipPath>
    <clipPath id="wellclip">
      <rect x="{mx}" y="{my}" width="{CELL}" height="{CELL}" rx="{R}"/>
    </clipPath>
  </defs>

  <g clip-path="url(#mask)">
    <g id="bg">
      <!-- cushion tile: ramp, vignette, inner rim light -->
      <rect width="1024" height="1024" fill="url(#ground)"/>
      <rect width="1024" height="1024" fill="url(#vig)"/>
      <path d="{d}" fill="none" stroke="{RIM}" stroke-width="7" opacity=".82"/>
    </g>

    <g id="mid">
      <!-- the absence, and the contact shadow the frames sit on -->
      {socket()}
      <g filter="url(#contact)" opacity=".26">{drop}</g>
    </g>

    <g id="fg">
      <!-- eight frames, one of them proven: identity lives here -->
      {tiles()}
    </g>

    <g id="highlight">
      <!-- the lighting, droppable without the mark stopping being itself -->
      {tile_highlights()}
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    print(svg())
