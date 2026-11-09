#!/usr/bin/env python3
"""Engine A master generator - app-store-connect, direction "Tagged at the Prompt".

A graphite luggage tag hangs at a slight tilt from a clay split ring threaded
through its punched hole. On its face a vermilion gel prompt, a chevron and an
underscore cursor, is the only warm thing on the tile: an identity issued from a
terminal, which is what a bundle ID provisioned through asc is.

Material is inherited from decision-panel and clarify (porcelain ground, clay in
the shade, one vermilion gel, warm shadows, a hard contact line), whose values
were sampled from the apple-2026 corpus and tuned in clarify's fidelity loop.
The graphite body follows tui-craft and atlas-publish, the family's dark objects.

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
TAG_C = (548, 530)                  # tag centre on the canvas
TAG_TILT = -14                      # degrees; the tag hangs down-right from the ring
TAG_W, TAG_H = 640, 364
TAG_CHAMFER = 112                   # the cut corners at the hole end
TAG_R = 46                          # rounded corners at the free end
TAG_WALL = 24                       # extrusion depth, straight down
HOLE = (-TAG_W / 2 + 88, 0)         # hole centre, tag-local
HOLE_R = 38

PROMPT = [(-92, -96), (26, 0), (-92, 96)]   # the chevron, tag-local
CURSOR = [(88, 96), (218, 96)]              # the underscore, tag-local
PROMPT_W = 58
PROMPT_WALL = 12

RING_OFFSET = (-46, -104)           # ring centre relative to the hole, canvas
RING_W = 24
RING_WALL = 10

KEY = (0.34, 0.26)                  # one soft top-left light

# ---------------------------------------------------------------- material
GROUND = ("#FFFEFB", "#F5F0E5", "#E2D8C2")     # clarify's measured ground
VIGNETTE = "#9C8D74"
RIM_WHITE, RIM_HAIR = 0.72, "#C7B9A0"
GRAPHITE_FACE = ("#55545A", "#3A393F", "#2A292E")
GRAPHITE_WALL = ("#1E1D22", "#131216")
GRAPHITE_SCATTER, GRAPHITE_SCATTER_A = "#E9E4DA", 0.50
CLAY_FACE = ("#A99D8A", "#8D8170")             # clarify's shaded clay
CLAY_WALL = ("#7A6F5B", "#4C4435")
CLAY_SCATTER = "#FFFBF2"
SHADOW, CONTACT = "#6E6049", "#41372A"
GEL = ("#E36C40", "#DA5B31", "#D24B1E", "#A82F0E")   # clarify's vermilion gel
GEL_WALL = ("#B23A14", "#7E240A")
GEL_SCATTER = "#FFD7BC"


# ---------------------------------------------------------------- helpers
def stops(items):
    return "".join(f'<stop offset="{o}" stop-color="{c}"'
                   + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                   for o, c, a in items)


def lin(i, x1, y1, x2, y2, items):
    return (f'<linearGradient id="{i}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" gradientUnits="userSpaceOnUse">{stops(items)}</linearGradient>')


def rad(i, cx, cy, r, items):
    return (f'<radialGradient id="{i}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'gradientUnits="userSpaceOnUse">{stops(items)}</radialGradient>')


def poly(points):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)


def stroke(d, paint, width, extra=""):
    return (f'<path d="{d}" stroke="{paint}" stroke-width="{width}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def to_canvas(p, dy=0.0):
    a = math.radians(TAG_TILT)
    x, y = p
    return (TAG_C[0] + x * math.cos(a) - y * math.sin(a),
            TAG_C[1] + x * math.sin(a) + y * math.cos(a) + dy)


def to_local(p):
    a = -math.radians(TAG_TILT)
    x, y = p[0] - TAG_C[0], p[1] - TAG_C[1]
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def inside_tag(p):
    """Tag-local point inside the tag body (chamfer included, hole excluded)."""
    x, y = p
    x0, x1, y0, y1 = -TAG_W / 2, TAG_W / 2, -TAG_H / 2, TAG_H / 2
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    if x - x0 + (y - y0) < TAG_CHAMFER or x - x0 + (y1 - y) < TAG_CHAMFER:
        return False
    return math.hypot(x - HOLE[0], y - HOLE[1]) > HOLE_R


x0, x1, y0, y1 = -TAG_W / 2, TAG_W / 2, -TAG_H / 2, TAG_H / 2
c, r = TAG_CHAMFER, TAG_R
TAG_BODY = (f"M {x0 + c} {y0} L {x1 - r} {y0} Q {x1} {y0} {x1} {y0 + r} "
            f"L {x1} {y1 - r} Q {x1} {y1} {x1 - r} {y1} L {x0 + c} {y1} "
            f"L {x0} {y1 - c} L {x0} {y0 + c} Z")
HOLE_D = (f"M {HOLE[0] + HOLE_R} {HOLE[1]} a {HOLE_R} {HOLE_R} 0 1 0 {-2 * HOLE_R} 0 "
          f"a {HOLE_R} {HOLE_R} 0 1 0 {2 * HOLE_R} 0 Z")
TAG_D = TAG_BODY + " " + HOLE_D
PROMPT_D, CURSOR_D = poly(PROMPT), poly(CURSOR)


def tag_xf(dx=0.0, dy=0.0):
    return f'translate({TAG_C[0] + dx:.1f},{TAG_C[1] + dy:.1f}) rotate({TAG_TILT})'


# The ring passes through the hole: it runs over the face between the hole and
# the near edge, and under the tag on the far side.
hole_c = to_canvas(HOLE)
RING_C = (hole_c[0] + RING_OFFSET[0], hole_c[1] + RING_OFFSET[1])
RING_R = math.hypot(*RING_OFFSET)
theta_h = math.atan2(hole_c[1] - RING_C[1], hole_c[0] - RING_C[0])


def ring_pt(t):
    return (RING_C[0] + RING_R * math.cos(t), RING_C[1] + RING_R * math.sin(t))


def exit_angle(direction):
    t = theta_h + direction * (HOLE_R + 2) / RING_R
    while inside_tag(to_local(ring_pt(t))):
        t += direction * 0.01
    return t


t_plus, t_minus = exit_angle(1), exit_angle(-1)
t_end = t_plus if abs(t_plus - theta_h) < abs(t_minus - theta_h) else t_minus
FRONT_ARC = [ring_pt(theta_h + (t_end - theta_h) * k / 24 + math.copysign(0.06, t_end - theta_h) * (k / 24))
             for k in range(25)]
RING_FRONT_D = poly(FRONT_ARC)
RING_FULL = (f"M {RING_C[0] + RING_R:.1f} {RING_C[1]:.1f} "
             f"a {RING_R:.1f} {RING_R:.1f} 0 1 0 {-2 * RING_R:.1f} 0 "
             f"a {RING_R:.1f} {RING_R:.1f} 0 1 0 {2 * RING_R:.1f} 0")

# ---------------------------------------------------------------- document
defs = [
    f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>',
    rad("tile", S * KEY[0], S * KEY[1], S * 0.95,
        [(0, GROUND[0], None), (0.52, GROUND[1], None), (1, GROUND[2], None)]),
    rad("vig", S * 0.5, S * 0.46, S * 0.72, [(0.52, VIGNETTE, "0"), (1, VIGNETTE, "0.26")]),
    # tag-local gradients: lit at the top-left shoulder, deepest at the free end's foot
    lin("graphiteFace", x0, y0, x1 * 0.7, y1,
        [(0, GRAPHITE_FACE[0], None), (0.5, GRAPHITE_FACE[1], None), (1, GRAPHITE_FACE[2], None)]),
    lin("graphiteWall", 0, y0, 0, y1, [(0, GRAPHITE_WALL[0], None), (1, GRAPHITE_WALL[1], None)]),
    lin("clayFace", RING_C[0] - RING_R, RING_C[1] - RING_R, RING_C[0] + RING_R, RING_C[1] + RING_R,
        [(0, CLAY_FACE[0], None), (1, CLAY_FACE[1], None)]),
    lin("clayWall", 0, RING_C[1] - RING_R, 0, RING_C[1] + RING_R,
        [(0, CLAY_WALL[0], None), (1, CLAY_WALL[1], None)]),
    lin("gelFace", -80, -90, 200, 100,
        [(0, GEL[0], None), (0.45, GEL[1], None), (0.8, GEL[2], None), (1, GEL[3], None)]),
    lin("gelWall", 0, -90, 0, 100, [(0, GEL_WALL[0], None), (1, GEL_WALL[1], None)]),
    f'<mask id="tagFace" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">'
    f'<rect width="{S}" height="{S}" fill="#000"/>'
    f'<path d="{TAG_D}" fill="#FFF" fill-rule="evenodd" transform="{tag_xf()}"/></mask>',
    f'<mask id="gelFaceM" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">'
    f'<rect width="{S}" height="{S}" fill="#000"/><g transform="{tag_xf()}">'
    + stroke(PROMPT_D, "#FFF", PROMPT_W) + stroke(CURSOR_D, "#FFF", PROMPT_W) + '</g></mask>',
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

# The ring is the back plane: its shadow, contact line, wall, then clay face.
mid = [
    stroke(RING_FULL, SHADOW, RING_W, ' opacity="0.30" transform="translate(12,18)" filter="url(#soft)"'),
    stroke(RING_FULL, CONTACT, RING_W, f' opacity="0.45" transform="translate(2,{RING_WALL + 5})" filter="url(#hair)"'),
    stroke(RING_FULL, "url(#clayWall)", RING_W, f' transform="translate(0,{RING_WALL})"'),
    stroke(RING_FULL, "url(#clayFace)", RING_W),
    stroke(RING_FULL, CLAY_SCATTER, 6, ' stroke-opacity="0.55" transform="translate(-4,-6)" filter="url(#rim)"'),
]

# The tag stands in front: a broad soft shadow, the hard contact line under its
# wall, the wall straight down, the graphite face, then the raised gel prompt.
fg = [
    f'<path d="{TAG_D}" fill="{SHADOW}" fill-rule="evenodd" opacity="0.42" transform="{tag_xf(22, 34)}" filter="url(#softL)"/>',
    f'<path d="{TAG_D}" fill="{CONTACT}" fill-rule="evenodd" opacity="0.60" transform="{tag_xf(4, TAG_WALL + 8)}" filter="url(#hair)"/>',
    f'<path d="{TAG_D}" fill="url(#graphiteWall)" fill-rule="evenodd" transform="{tag_xf(0, TAG_WALL)}"/>',
    f'<path d="{TAG_D}" fill="url(#graphiteFace)" fill-rule="evenodd" transform="{tag_xf()}"/>',
    # the hole's inner wall, seen on its lower lip
    f'<g transform="{tag_xf()}"><path d="{HOLE_D}" fill="none" stroke="{GRAPHITE_WALL[1]}" stroke-width="7" opacity="0.9"/></g>',
    f'<g transform="{tag_xf(0, PROMPT_WALL)}">'
    + stroke(PROMPT_D, "url(#gelWall)", PROMPT_W) + stroke(CURSOR_D, "url(#gelWall)", PROMPT_W) + '</g>',
    f'<g transform="{tag_xf()}">'
    + stroke(PROMPT_D, "url(#gelFace)", PROMPT_W) + stroke(CURSOR_D, "url(#gelFace)", PROMPT_W) + '</g>',
    # the ring's near run, over the face between the hole and the cut edge
    stroke(RING_FRONT_D, CONTACT, RING_W, ' opacity="0.55" transform="translate(4,10)" filter="url(#hair)"'),
    stroke(RING_FRONT_D, "url(#clayWall)", RING_W, f' transform="translate(0,{RING_WALL})"'),
    stroke(RING_FRONT_D, "url(#clayFace)", RING_W),
    stroke(RING_FRONT_D, CLAY_SCATTER, 6, ' stroke-opacity="0.55" transform="translate(-4,-6)" filter="url(#rim)"'),
]

# Rim scatter on the lit (upper-left) shoulder of each face, kept inside it by a
# mask: a translucent body lights at the grazing edge, not in the core.
highlight = [
    f'<g mask="url(#tagFace)"><path d="{TAG_BODY}" fill="none" stroke="{GRAPHITE_SCATTER}" '
    f'stroke-opacity="{GRAPHITE_SCATTER_A}" stroke-width="16" transform="{tag_xf(-8, -11)}" filter="url(#rim)"/></g>',
    f'<g mask="url(#gelFaceM)"><g transform="{tag_xf(-10, -14)}">'
    + stroke(PROMPT_D, GEL_SCATTER, 14, ' stroke-opacity="0.55"')
    + stroke(CURSOR_D, GEL_SCATTER, 14, ' stroke-opacity="0.55"') + '</g></g>',
    '<ellipse cx="330" cy="300" rx="210" ry="150" fill="#FFFFFF" opacity="0.07" filter="url(#softL)"/>',
]


def layer(name, items):
    return f'    <g id="{name}">\n' + "\n".join("      " + i for i in items) + "\n    </g>"


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>app-store-connect</title>
  <desc>A graphite luggage tag on a clay split ring, a vermilion prompt chevron and cursor
  raised on its face: an identity issued from a terminal. Full-bleed 1024 artwork; the
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
