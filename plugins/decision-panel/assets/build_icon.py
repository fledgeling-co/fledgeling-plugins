#!/usr/bin/env python3
"""Engine A master generator - decision-panel, direction "Four Marks, One Tick".

Four short clay marks, one per model family on the panel, sit in a fan along the
top of a porcelain tile. Each is turned so its long axis points at the same spot
below it, the vertex of one vermilion gel check mark: four readings converging on
one decision. The tick is the only warm thing on the tile.

Material is inherited from clarify's master (porcelain ground, clay in the shade,
one vermilion gel, warm shadows, a hard contact line), whose values were sampled
from the apple-2026 corpus and tuned in its fidelity loop, so the two sit in the
same family at every size.

    python3 build_icon.py [out.svg]

Emits 1024x1024 full-bleed layered artwork (bg / mid / fg / highlight). The
marketplace superellipse is a CLIP, never a baked corner radius or drop shadow.
"""
import math
import pathlib
import sys

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- geometry
# The tick: a left arm down to the vertex, a longer right arm up and away.
TICK = [(316, 600), (452, 742), (748, 432)]
TICK_W = 104                                   # face stroke width
TICK_WALL = 22                                 # extrusion depth, straight down
VERTEX = TICK[1]

# The four marks: centres along a shallow arc above the tick, each rotated so
# its axis points at the vertex. Lengths are equal: no family outranks another.
MARKS = [(292, 296), (428, 236), (572, 236), (708, 296)]
MARK_LEN, MARK_W = 150, 62
MARK_WALL = 18
AIM_GAP = 0.0                                  # 0 = axis passes through the vertex

KEY = (0.34, 0.26)                             # one soft top-left light

# ---------------------------------------------------------------- material
GROUND = ("#FFFEFB", "#F5F0E5", "#E2D8C2")     # clarify's measured ground
VIGNETTE = "#9C8D74"
RIM_WHITE, RIM_HAIR = 0.72, "#C7B9A0"
CLAY_FACE = ("#A99D8A", "#8D8170")             # clarify's shaded cards
CLAY_WALL = ("#7A6F5B", "#4C4435")
CLAY_SCATTER, CLAY_SCATTER_A = "#FFFBF2", 0.80
SHADOW, CONTACT = "#6E6049", "#41372A"
SHADOW_DX, SHADOW_DY = 13, 20
GEL = ("#E36C40", "#DA5B31", "#D24B1E", "#A82F0E")   # clarify's vermilion gel
GEL_WALL = ("#B23A14", "#7E240A")
GEL_SCATTER = "#FFD7BC"


# ---------------------------------------------------------------- helpers
def lin(i, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<linearGradient id="{i}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def rad(i, cx, cy, r, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<radialGradient id="{i}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'gradientUnits="userSpaceOnUse">{s}</radialGradient>')


def poly(points, dx=0, dy=0):
    p = [(x + dx, y + dy) for x, y in points]
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in p)


def stroke(d, paint, width, extra=""):
    return (f'<path d="{d}" stroke="{paint}" stroke-width="{width}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def mark_ends(cx, cy):
    """End points of one mark, its axis aimed at the tick's vertex."""
    ang = math.atan2(VERTEX[1] - cy, VERTEX[0] - cx)
    hx, hy = math.cos(ang) * MARK_LEN / 2, math.sin(ang) * MARK_LEN / 2
    return (cx - hx, cy - hy), (cx + hx, cy + hy)


MARK_PATHS = [poly(mark_ends(cx, cy)) for cx, cy in MARKS]
TICK_D = poly(TICK)

# ---------------------------------------------------------------- document
defs = [
    f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>',
    rad("tile", S * KEY[0], S * KEY[1], S * 0.95,
        [(0, GROUND[0], None), (0.52, GROUND[1], None), (1, GROUND[2], None)]),
    rad("vig", S * 0.5, S * 0.46, S * 0.72, [(0.52, VIGNETTE, "0"), (1, VIGNETTE, "0.26")]),
    lin("clayFace", 260, 200, 740, 340, [(0, CLAY_FACE[0], None), (1, CLAY_FACE[1], None)]),
    lin("clayWall", 0, 220, 0, 360, [(0, CLAY_WALL[0], None), (1, CLAY_WALL[1], None)]),
    # the gel: flat body, bright only at the rim, deepest pixel at the bottom
    lin("gelFace", 316, 432, 620, 760,
        [(0, GEL[0], None), (0.45, GEL[1], None), (0.8, GEL[2], None), (1, GEL[3], None)]),
    lin("gelWall", 0, 600, 0, 790, [(0, GEL_WALL[0], None), (1, GEL_WALL[1], None)]),
    f'<mask id="tickFace"><rect width="{S}" height="{S}" fill="#000"/>'
    + stroke(TICK_D, "#FFF", TICK_W) + '</mask>',
    f'<mask id="markFace"><rect width="{S}" height="{S}" fill="#000"/>'
    + "".join(stroke(d, "#FFF", MARK_W) for d in MARK_PATHS) + '</mask>',
    '<filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="21"/></filter>',
    '<filter id="softL" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="32"/></filter>',
    '<filter id="hair" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>',
    '<filter id="rim" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3.5"/></filter>',
]

bg = [
    f'<rect width="{S}" height="{S}" fill="url(#tile)"/>',
    f'<rect width="{S}" height="{S}" fill="url(#vig)"/>',
    f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="{RIM_WHITE}" stroke-width="10" filter="url(#rim)"/>',
    f'<path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-opacity="0.20" stroke-width="2.5"/>',
]

# The marks are the back plane: a pooled shadow, then per-mark shadow and contact
# line, then the extruded wall straight down, then the face on top.
mid = []
for d in MARK_PATHS:
    mid.append(stroke(d, SHADOW, MARK_W, f' opacity="0.30" transform="translate({SHADOW_DX},{SHADOW_DY})" filter="url(#soft)"'))
for d in MARK_PATHS:
    mid.append(stroke(d, CONTACT, MARK_W, f' opacity="0.55" transform="translate(3,{MARK_WALL + 6})" filter="url(#hair)"'))
    mid.append(stroke(d, "url(#clayWall)", MARK_W, f' transform="translate(0,{MARK_WALL})"'))
    mid.append(stroke(d, "url(#clayFace)", MARK_W))

# The tick stands in front: a broad soft shadow it lifts off, the hard contact
# line under its wall, the wall, then the gel face.
fg = [
    stroke(TICK_D, SHADOW, TICK_W, f' opacity="0.40" transform="translate(22,34)" filter="url(#softL)"'),
    stroke(TICK_D, CONTACT, TICK_W, f' opacity="0.60" transform="translate(4,{TICK_WALL + 8})" filter="url(#hair)"'),
    stroke(TICK_D, "url(#gelWall)", TICK_W, f' transform="translate(0,{TICK_WALL})"'),
    stroke(TICK_D, "url(#gelFace)", TICK_W),
]

# Rim scatter on the lit (upper-left) shoulder of every face, kept inside the
# face by its mask: a translucent body lights at the grazing edge, not in the core.
highlight = [
    f'<g mask="url(#markFace)">' + "".join(
        stroke(d, CLAY_SCATTER, 14, f' stroke-opacity="{CLAY_SCATTER_A}" transform="translate(-9,-12)" filter="url(#rim)"')
        for d in MARK_PATHS) + '</g>',
    f'<g mask="url(#tickFace)">'
    + stroke(TICK_D, GEL_SCATTER, 16, ' stroke-opacity="0.55" transform="translate(-14,-20)" filter="url(#rim)"')
    + '</g>',
    '<ellipse cx="330" cy="300" rx="210" ry="150" fill="#FFFFFF" opacity="0.07" filter="url(#softL)"/>',
]


def layer(name, items):
    return f'    <g id="{name}">\n' + "\n".join("      " + i for i in items) + "\n    </g>"


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>decision-panel</title>
  <desc>Four clay marks in a fan, each aimed at the vertex of one vermilion check mark
  below them: four readings converging on one decision. Full-bleed 1024 artwork; the
  marketplace superellipse is a CLIP, never a baked corner radius or drop shadow.</desc>
  <defs>
    {chr(10).join("    " + d for d in defs).strip()}
  </defs>
  <g clip-path="url(#mask)">
{layer("bg", bg)}
{layer("mid", mid)}
{layer("fg", fg)}
{layer("highlight", highlight)}
  </g>
</svg>
'''

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ASSETS / "icon.svg")
    out.write_text(svg)
    print("wrote", out, len(svg), "bytes")
