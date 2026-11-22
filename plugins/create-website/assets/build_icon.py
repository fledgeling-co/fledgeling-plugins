#!/usr/bin/env python3
"""Build the create-website icon master.

Geometry and material live here as named constants, so a later change is a parameter edit
rather than path surgery.

    python3 build_icon.py            # writes icon.svg and icon-engineA-handauthored.svg

THE SUBJECT: "The parting stack"
--------------------------------
Three page sections of one website, lifted apart along the z-axis and seen in plan-oblique
from above and slightly left, so the broad top face of every section reads as a page. The
sections stay exactly registered in plan — this is an exploded view of one page, not a fan of
separate cards — and the air gap grows upward.

SIGNATURE MOVE: the top layer is the hero, and it is the only warm thing in the tile. It floats
highest, over the widest gap, and it throws the stack's one ember shadow down onto the section
beneath it.

WHY NOT A FAN OF CARDS: deck-craft already owns the diagonal fan of porcelain slides, and
clarify owns the pale drawn card. Registration, a value ladder instead of three porcelain
plates, and a parting that grows upward are what keep this one its own mark on the shelf.

MEASURED VALUES
---------------
Ground ramp, vignette, pool and rim are the fledgeling family's, lifted from
plugins/career-kit/assets/build_icon.py (measured there against create-mac-icon's apple-2026
corpus). Re-sampled for this commission from apple-26, apple-28, apple-30 and apple-31: the
porcelain-register median sits at L 0.68 to 0.96 and the darkest object pixel at L 0.09 to
0.14, faintly cool. The family's darks are warm; the family wins for shelf consistency.

Plan geometry was fitted to the Engine C raster (icon-engineC-raster-ab01f2.png), not guessed.
On that render the hero slab's top face is a parallelogram with a width axis of (565, 142) and
a depth axis of (231, -142) — both axes drop or rise by the same 142, which is why the left and
right corners sit level. Scaled to 0.83 so the object is 64% of the tile instead of the
raster's 78%, that is U = (468, 118) and V = (192, -118). Centre-column pitches measured 252
and 182 on the raster; the ember gap is opened a little wider here because the parting is the
subject.

MATERIAL, FROM THE RASTER TAKE
------------------------------
Four things were rebuilt from the raster rather than reasoned about: the top face ramps along
the light axis and carries a separate soft dome bloom near the key's bearing (one axis per
gradient — a second direction is a second layer); the wall is a darker vertical ramp, not a
flat flank; each floating slab drops a real contact shadow onto the top face of the slab below,
clipped to that face and painted before the slab above it; and the rim catch is one stroke
whose opacity dies along the light axis rather than per-edge arcs.

WHERE THE REFERENCE IS WRONG, AND HELD AGAINST
----------------------------------------------
The raster's ember sits at relative luminance 0.58 on its lit face, which measures about
1.6:1 against this porcelain ground and fails rubric #7. The family accent band (HSL lightness
0.42 to 0.58, hue 14 to 18) puts the hero's median near Y 0.25, which measures about 3:1. The
accent is held at the family value; converging it onto the raster would buy similarity to a
weakness, which is the documented failure mode of this loop.

The raster also carries a heavy grey corner vignette that the porcelain register does not have.
It is not copied.
"""

from pathlib import Path
import math

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- plan geometry
CX = 512.0                 # the stack's axis; every section is registered on it
UX, UY = 468.0, 118.0      # width axis of a section's top face, down-right
VX, VY = 192.0, 118.0      # depth axis of a section's top face, up-right
CORNER_R = 34.0            # plan-space corner radius of a section
THICK = 32.0               # section thickness, drawn straight down
SWEEP_STEP = 1.6           # how finely the wall silhouette is swept

CY_HERO = 318.0            # top-face centre of each section, top to bottom
PITCH_HERO = 215.0         # hero to middle: the wide gap, the parting
PITCH_BASE = 165.0         # middle to base: the stack still closing up

# the ember hero's headline bar, inset into its top face
HEADLINE = False       # it rendered as a smear at 128px; see loop-runs/r07
HEADLINE_T = 0.30          # how far down the depth axis the bar sits
HEADLINE_SPAN = 0.50       # fraction of the width axis it covers
HEADLINE_H = 15.0          # bar thickness along the depth axis

# ---------------------------------------------------------------- light
LIGHT_DX, LIGHT_DY = -0.62, -0.78   # key bearing, upper-left
BLOOM_T, BLOOM_U = 0.70, 0.30       # where the dome bloom sits on the top face
BLOOM_R = 300.0
BLOOM_A = 0.085

# ---------------------------------------------------------------- palette
GROUND_HI = "#FDFCF9"
GROUND_MID = "#F3EFE7"
GROUND_LO = "#E7E1D5"
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"
POOL = "#B7AA90"
GLINT = "#FFFFFF"

# a section is a lit top face, a shaded wall and a seat edge between them.
# Three value bands, measured against each neighbour they touch:
#   base graphite  Y 0.07-0.11   middle stone  Y 0.47-0.63   hero ember  Y 0.20-0.33
SECTIONS = [
    # face_hi      face_mid     face_lo      wall_hi      wall_lo      seat
    ("#F7995F", "#EC6A31", "#D14E1C", "#C65129", "#A03B16", "#6E2409"),   # hero, ember
    ("#FEFAF0", "#F5EBD8", "#E0D2B6", "#BCAA8C", "#8E7C60", "#5E4F36"),   # middle, stone
    ("#6E6258", "#4B423A", "#332C26", "#201B18", "#110E0D", "#0A0808"),   # base, graphite
]
AO = "#4A3B2C"             # the shadow a floating section drops on the one below
AO_A = 0.60
AO_SLIP = 0.26           # how far the shadow slides along the ground plane per unit of height
EMBER_SPILL = "#F6D3AC"    # the hero's warm bounce, in the pale spill hue, never the accent's


def norm(x, y):
    m = math.hypot(x, y)
    return x / m, y / m


def face_pts(cy):
    """The four corners of one section's top face, left, near, right, far."""
    hx, hy = UX / 2, UY / 2
    gx, gy = VX / 2, VY / 2
    return [
        (CX - hx - gx, cy - hy + gy),   # left
        (CX + hx - gx, cy + hy + gy),   # near
        (CX + hx + gx, cy + hy - gy),   # right
        (CX - hx + gx, cy - hy - gy),   # far
    ]


def rounded_poly(pts, r):
    """A convex polygon with every corner trimmed by r/tan(theta/2), not by r.

    Trimming by the radius and arcing at that radius is tangent only at 90 degrees; on the
    shallow corners of a plan-oblique parallelogram it renders as a protruding half-disc.
    The tangent length is clamped to 0.46 of each edge and the radius recomputed from it.
    """
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    # y points down, so a positive shoelace area is a clockwise traverse on screen, and a
    # convex corner on a clockwise traverse arcs in SVG's positive direction, sweep 1.
    # Getting this backwards does not error: every corner renders as a concave bite, and the
    # section reads as a cloakroom ticket.
    sweep = 1 if area > 0 else 0
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = norm(a[0] - b[0], a[1] - b[1])
        v2 = norm(c[0] - b[0], c[1] - b[1])
        cos = max(-1.0, min(1.0, v1[0] * v2[0] + v1[1] * v2[1]))
        theta = math.acos(cos)
        if theta < 1e-3 or abs(math.pi - theta) < 1e-3:
            out.append(("L", b))
            continue
        t = r / math.tan(theta / 2)
        t = min(t, 0.46 * math.hypot(a[0] - b[0], a[1] - b[1]), 0.46 * math.hypot(c[0] - b[0], c[1] - b[1]))
        re = max(1.0, t * math.tan(theta / 2))
        p1 = (b[0] + v1[0] * t, b[1] + v1[1] * t)
        p2 = (b[0] + v2[0] * t, b[1] + v2[1] * t)
        out.append(("A", p1, p2, re))
    d = []
    first = out[0]
    start = first[1]
    d.append(f"M{start[0]:.1f},{start[1]:.1f}")
    for item in out:
        if item[0] == "L":
            d.append(f"L{item[1][0]:.1f},{item[1][1]:.1f}")
        else:
            _, p1, p2, re = item
            if d[-1] != f"M{p1[0]:.1f},{p1[1]:.1f}":
                d.append(f"L{p1[0]:.1f},{p1[1]:.1f}")
            d.append(f"A{re:.1f},{re:.1f} 0 0 {sweep} {p2[0]:.1f},{p2[1]:.1f}")
    d.append("Z")
    return "".join(d)


def face_path(cy, grow=0.0, dx=0.0, dy=0.0):
    """One section's top face, optionally grown outward and displaced."""
    pts = face_pts(cy)
    cxx = sum(p[0] for p in pts) / 4
    cyy = sum(p[1] for p in pts) / 4
    scaled = []
    for x, y in pts:
        ux, uy = norm(x - cxx, y - cyy)
        scaled.append((x + ux * grow + dx, y + uy * grow + dy))
    r = max(4.0, CORNER_R + grow * 0.5)
    return rounded_poly(scaled, r)


def on_face(cy, u, v):
    """A point on a section's top face in face coordinates: u along width, v along depth."""
    x = CX + (u - 0.5) * UX + (v - 0.5) * VX
    y = cy + (u - 0.5) * UY - (v - 0.5) * VY
    return x, y


def headline_path(cy):
    """A bar lying on the hero's top face, parallel to its width axis."""
    u0, u1 = (1 - HEADLINE_SPAN) / 2, (1 + HEADLINE_SPAN) / 2
    hv = HEADLINE_H / max(1.0, math.hypot(VX, VY))
    v0, v1 = HEADLINE_T - hv, HEADLINE_T + hv
    pts = [on_face(cy, u0, v0), on_face(cy, u1, v0), on_face(cy, u1, v1), on_face(cy, u0, v1)]
    return rounded_poly(pts, 12.0)


def swept(cy, fill, grow=0.0, depth=THICK, dx=0.0, dy=0.0, extra=""):
    """A section's body: its top face swept straight down, which is exactly the solid's
    silhouette, so the wall's outline needs no separate construction."""
    steps = max(1, int(depth / SWEEP_STEP))
    return "".join(
        f'<path d="{face_path(cy, grow, dx, dy + depth * k / steps)}" fill="{fill}"{extra}/>'
        for k in range(steps + 1)
    )


def build() -> str:
    sq = SQUIRCLE.read_text().strip()
    lx, ly = norm(LIGHT_DX, LIGHT_DY)
    cys = [CY_HERO, CY_HERO + PITCH_HERO, CY_HERO + PITCH_HERO + PITCH_BASE]

    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    add("<defs>")
    add(f'''<linearGradient id="ground" gradientUnits="userSpaceOnUse" x1="330" y1="0" x2="620" y2="{S}">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/></linearGradient>''')
    add(f'''<radialGradient id="vig" cx="0.42" cy="0.30" r="0.86">
      <stop offset="0.60" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.22"/></radialGradient>''')

    for i, cy in enumerate(cys):
        hi, mid, lo, whi, wlo, seat = SECTIONS[i]
        # the top face ramps along the light axis: lit at the upper-left corner, shaded at the
        # lower-right. One axis per gradient; the dome bloom is a separate layer.
        half = (abs(UX) + abs(VX)) / 2
        # the lit end of the ramp is placed where the key comes FROM, so it carries the
        # light vector's own sign. Negating it puts the highlight on the shaded side and
        # every face reads as lit from the wrong quarter.
        x1 = CX + lx * half * 1.05
        y1 = cy + ly * (UY + VY) * 0.9
        x2 = CX - lx * half * 1.05
        y2 = cy - ly * (UY + VY) * 0.9
        add(f'''<linearGradient id="face{i}" gradientUnits="userSpaceOnUse"
      x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">
      <stop offset="0" stop-color="{hi}"/><stop offset="0.46" stop-color="{mid}"/>
      <stop offset="1" stop-color="{lo}"/></linearGradient>''')
        add(f'''<linearGradient id="wall{i}" gradientUnits="userSpaceOnUse"
      x1="0" y1="{cy + UY / 2 - 6:.1f}" x2="0" y2="{cy + UY / 2 + THICK + 10:.1f}">
      <stop offset="0" stop-color="{whi}"/><stop offset="1" stop-color="{wlo}"/></linearGradient>''')
        bx, by = on_face(cy, BLOOM_U, BLOOM_T)
        add(f'''<radialGradient id="bloom{i}" gradientUnits="userSpaceOnUse"
      cx="{bx:.1f}" cy="{by:.1f}" r="{BLOOM_R:.1f}">
      <stop offset="0" stop-color="{GLINT}" stop-opacity="{BLOOM_A}"/>
      <stop offset="1" stop-color="{GLINT}" stop-opacity="0"/></radialGradient>''')
        add(f'''<linearGradient id="rim{i}" gradientUnits="userSpaceOnUse"
      x1="{CX + lx * half:.1f}" y1="{cy + ly * (UY + VY) * 0.8:.1f}"
      x2="{CX - lx * half:.1f}" y2="{cy - ly * (UY + VY) * 0.8:.1f}">
      <stop offset="0" stop-color="{GLINT}" stop-opacity="0.92"/>
      <stop offset="0.42" stop-color="{GLINT}" stop-opacity="0.20"/>
      <stop offset="1" stop-color="{GLINT}" stop-opacity="0"/></linearGradient>''')
        add(f'<clipPath id="facec{i}"><path d="{face_path(cy)}"/></clipPath>')

    add('<filter id="pool" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="19"/></filter>')
    add('<filter id="cast" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="20"/></filter>')
    add('<filter id="ao" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="13"/></filter>')
    add('<filter id="soft" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="3"/></filter>')
    add('<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="26"/></filter>')
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    add("</defs>")

    add('<g clip-path="url(#tile)">')

    # ------------------------------------------------------------ bg: the cushion
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<path d="{sq}" fill="none" stroke="{RIM_TILE}" stroke-width="7" stroke-opacity="0.55"/>')
    add("</g>")

    # ------------------------------------------------------------ mid: the ground shadow and the two lower sections
    add('<g id="mid">')
    # the whole stack's shadow on the bench, thrown away from the key
    base_cy = cys[-1]
    add(f'<g filter="url(#pool)" fill="{POOL}" fill-opacity="0.82">')
    add(f'<path d="{face_path(base_cy, -6, -lx * 26, -ly * 26 + THICK + 10)}"/>')
    add("</g>")
    add(f'<ellipse cx="{CX - lx * 30:.1f}" cy="{base_cy + UY / 2 + THICK + 30:.1f}" rx="250" ry="34" '
        f'fill="{POOL}" fill-opacity="0.60" filter="url(#cast)"/>')

    def section(i, cy, group_tag):
        """One section: wall, top face, dome bloom, seat edge, rim catch."""
        s = []
        s.append(swept(cy, f"url(#wall{i})"))
        s.append(f'<path d="{face_path(cy)}" fill="url(#face{i})"/>')
        s.append(f'<path d="{face_path(cy)}" fill="url(#bloom{i})"/>')
        # the seat edge belongs to the face it ends, so it is drawn with it
        s.append(f'<path d="{face_path(cy)}" fill="none" stroke="{SECTIONS[i][5]}" '
                 f'stroke-width="3" stroke-opacity="0.55"/>')
        s.append(f'<path d="{face_path(cy)}" fill="none" stroke="url(#rim{i})" '
                 f'stroke-width="5" stroke-opacity="0.85" filter="url(#soft)"/>')
        return "".join(s)

    def contact(i_upper, cy_upper, cy_lower, i_lower):
        """What a floating section drops on the top face of the section below it.

        Painted after that face and before the body above it, and clipped to it, so the
        shadow cannot leak past the surface receiving it.
        """
        s = [f'<g clip-path="url(#facec{i_lower})">']
        drop = cy_lower - cy_upper
        # the height axis already projects straight down, so `drop` is the whole vertical
        # term. Adding the key's screen-y on top of it walks the patch off the near edge of
        # the surface it is cast on, where the clip removes it.
        s.append(f'<path d="{face_path(cy_upper, -10, -lx * drop * AO_SLIP, drop + UY * AO_SLIP)}" '
                 f'fill="{AO}" fill-opacity="{AO_A}" filter="url(#ao)"/>')
        s.append(f'<path d="{face_path(cy_upper, -66, -lx * drop * AO_SLIP * 0.6, drop + UY * AO_SLIP * 0.6)}" '
                 f'fill="{AO}" fill-opacity="0.24" filter="url(#ao)"/>')
        s.append("</g>")
        return "".join(s)

    add(section(2, cys[2], "base"))
    add(contact(1, cys[1], cys[2], 2))
    add(section(1, cys[1], "middle"))
    add("</g>")

    # ------------------------------------------------------------ fg: the hero's shadow and the hero
    add('<g id="fg">')
    add(contact(0, cys[0], cys[1], 1))
    # the hero's warm bounce onto the stone below: an edge kiss in the pale spill hue,
    # clipped to the surface receiving it, never the accent's own colour
    add(f'<g clip-path="url(#facec1)">')
    add(f'<path d="{face_path(cys[0], -58, 0, PITCH_HERO)}" fill="{EMBER_SPILL}" '
        f'fill-opacity="0.30" filter="url(#glow)"/>')
    add("</g>")
    add(section(0, cys[0], "hero"))
    add("</g>")

    # ------------------------------------------------------------ highlight: the hero's headline and the key catch
    add('<g id="highlight">')
    if HEADLINE:
        add(f'<g clip-path="url(#facec0)">')
        add(f'<path d="{headline_path(cys[0])}" fill="{GLINT}" fill-opacity="0.17"/>')
        add(f'<path d="{headline_path(cys[0] - 4)}" fill="{SECTIONS[0][5]}" fill-opacity="0.14" '
            f'filter="url(#soft)"/>')
        add("</g>")
    # one short catch where the key strikes the hero's far-left corner
    fx, fy = on_face(cys[0], 0.10, 0.80)
    gx, gy = on_face(cys[0], 0.52, 0.97)
    add(f'<path d="M{fx:.1f},{fy:.1f} L{gx:.1f},{gy:.1f}" stroke="{GLINT}" stroke-width="6" '
        f'stroke-opacity="0.34" stroke-linecap="round" filter="url(#soft)"/>')
    add("</g>")

    add("</g>")
    add("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    svg = build()
    (HERE / "icon.svg").write_text(svg)
    (HERE / "icon-engineA-handauthored.svg").write_text(svg)
    print(f"wrote {HERE / 'icon.svg'} and the Engine A alternate")
