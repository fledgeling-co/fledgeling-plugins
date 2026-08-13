#!/usr/bin/env python3
"""Engine A for the `proctor` icon — direction "Out of True".

One macOS window form registered three times, once per observer, offset so the
three read as a stack in depth. Where they agree the tile is quiet porcelain;
where they disagree the delta is vermilion. That is the tri-observer check
drawn rather than described: the accessibility tree, the layer geometry and the
captured pixels each describe the same instant, and the disagreement is the
finding.

    the tree      a slate keyline           — structure, no substance (at back)
    the geometry  a solid porcelain plane   — the one with mass (in the middle)
    the capture   a run of discrete samples — pixels, and only pixels (in front)

The accent is the disagreement and nothing else: vermilion appears only in the
run of samples the capture reports past the true edge, and — faintly — where
the tree's keyline strays outside the true form. Everything the three planes
agree on stays porcelain. (be-my-witness: the accent is the disagreement,
located and directional, never decoration.)

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery. Re-run to emit icon.svg.

Measured off the marketplace family before authoring (icon-notes.md § spec):
    ground TL L 0.94, BR L 0.87, warm; accent hue 8-20 deg, S 0.77-0.97
    slate near-neutral cool, S ~.26; design-review is the cool-ground sibling,
    this one stays warm.
"""
from __future__ import annotations

import math
import pathlib
import random

# ----------------------------------------------------------------- geometry

TILE = 1024

W, H = 548.0, 380.0          # the window form, drawn identically three times
R = 34.0                     # its corner radius
TB = 78.0                    # titlebar height
CX, CY = 512.0, 512.0        # the registration centre

# Registration deltas. Large enough now to read as three stacked windows in
# depth rather than one ghosted double — the read the raster takes won and the
# small-offset draft lost. Still identical in size (a stack varies in scale, a
# misregistration does not) and still only offset + a hair of rotation, so the
# near band stays a wedge rather than a colourised drop shadow.
AX = dict(dx=-70.0, dy=-62.0, rot=-1.3)   # the accessibility tree  (back)
GEO = dict(dx=0.0, dy=0.0, rot=0.0)       # the layer geometry      (middle)
CAP = dict(dx=68.0, dy=60.0, rot=1.4)     # the captured pixels     (front)

CELL = 24.0                  # the capture's sample pitch
GAP = 2.4                    # kerf between samples, so they read as discrete
SCATTER = 1.7                # how many cells the delta dissolves past the frame
SEED = 7                     # so the dissolve is the same every build

# ----------------------------------------------------------------- material

GROUND = ("#FCFAF5", "#F3EEE3", "#DCD3C1")      # cushion, key at top-left
VIGNETTE = "#8A7A62"

PORCELAIN_FACE = ("#FFFEFB", "#F3EDE2", "#DCD3C2")
CHROME = ("#FFFDF9", "#F5F0E6")                 # the titlebar band
FIELD = ("#F6F1E7", "#E4DCCC")                  # the content field
ROW = "#A99C84"                                 # content rows on the solid
DOT = "#D8CEBB"                                 # solid-plane traffic dots
RIM_LIT = "#FFFFFF"
RIM_DARK = "#A2957E"
SHADOW = "#6E5F45"                              # inter-plane + ground shadow

SLATE = "#333C4A"                               # near-neutral cool, S .26

# What the capture reports back. Faint over empty field, firm over content: a
# capture's dirty-rect summary is exactly this, and a uniform sheet of samples
# greys the porcelain out — the earlier draft's largest single defect, so the
# field and chrome samples stay very light and only the rows carry weight.
SAMPLE = {
    "chrome": ("#E7ECF3", 0.12),
    "field":  ("#E0E5ED", 0.12),
    "row":    ("#8B97A9", 0.50),
}
# Warmed toward the raster takes' vivid orange — less deep red, more vermilion.
DELTA_HOT = "#FF7C33"
DELTA_MID = "#F4551C"
DELTA_DEEP = "#D33E0B"
SPILL = "#FF9257"


# ------------------------------------------------------------------ helpers

def rot(px, py, cx, cy, deg):
    a = math.radians(deg)
    dx, dy = px - cx, py - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a),
            cy + dx * math.sin(a) + dy * math.cos(a))


def frame(reg):
    """The window rect for one registration, plus that form's own centre."""
    x = CX - W / 2 + reg["dx"]
    y = CY - H / 2 + reg["dy"]
    return x, y, x + W / 2, y + H / 2


def rrect(x, y, w, h, r, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r:.2f}" ry="{r:.2f}" {extra}/>')


def inside_rrect(px, py, x, y, w, h, r):
    """Point-in-rounded-rect — what decides whether a sample is a delta."""
    if not (x <= px <= x + w and y <= py <= y + h):
        return False
    for cx, cy in ((x + r, y + r), (x + w - r, y + r),
                   (x + r, y + h - r), (x + w - r, y + h - r)):
        in_x = (px < x + r) if cx == x + r else (px > x + w - r)
        in_y = (py < y + r) if cy == y + r else (py > y + h - r)
        if in_x and in_y:
            return (px - cx) ** 2 + (py - cy) ** 2 <= r * r
    return True


# Two content rows only. A screenshot's worth of rows reads as a screenshot
# rather than a glyph and dies at 32px (anti-checklist #4/#5). They span the
# content width now that there is no sidebar.
ROWS = [(0.20, 0.13), (0.52, 0.13)]
ROW_INSET = 44.0


def probe(px, py):
    """What the layer geometry says is at this canvas point.

    Every capture sample is looked up against the geometry beneath it, so the
    two planes cannot drift apart anywhere except where they are offset.
    `delta` is the capture reporting content where the geometry says none.
    """
    gx, gy, _, _ = frame(GEO)
    if not inside_rrect(px, py, gx, gy, W, H, R):
        return "delta"
    ly = py - gy
    if ly < TB:
        return "chrome"
    fy = (ly - TB) / (H - TB)
    for t, hh in ROWS:
        if t <= fy <= t + hh:
            return "row"
    return "field"


# ------------------------------------------------------------------- layers

def defs():
    gx, gy, _, _ = frame(GEO)
    ax, ay, _, _ = frame(AX)
    cx_, cy_, _, _ = frame(CAP)
    return f"""
  <defs>
    <!-- Tahoe grammar: the tile is a cushion, key top-left, warm. -->
    <radialGradient id="cushion" cx="0.30" cy="0.24" r="0.95">
      <stop offset="0"    stop-color="{GROUND[0]}"/>
      <stop offset="0.52" stop-color="{GROUND[1]}"/>
      <stop offset="1"    stop-color="{GROUND[2]}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.60" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1"    stop-color="{VIGNETTE}" stop-opacity="0.20"/>
    </radialGradient>

    <!-- one key, one axis: top-left to bottom-right, on every plane -->
    <linearGradient id="face" gradientUnits="userSpaceOnUse"
        x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx + W:.1f}" y2="{gy + H:.1f}">
      <stop offset="0"    stop-color="{PORCELAIN_FACE[0]}"/>
      <stop offset="0.54" stop-color="{PORCELAIN_FACE[1]}"/>
      <stop offset="1"    stop-color="{PORCELAIN_FACE[2]}"/>
    </linearGradient>
    <linearGradient id="chrome" gradientUnits="userSpaceOnUse"
        x1="{gx:.1f}" y1="{gy:.1f}" x2="{gx + W * 0.8:.1f}" y2="{gy + TB:.1f}">
      <stop offset="0" stop-color="{CHROME[0]}"/>
      <stop offset="1" stop-color="{CHROME[1]}"/>
    </linearGradient>
    <linearGradient id="field" gradientUnits="userSpaceOnUse"
        x1="{gx:.1f}" y1="{gy + TB:.1f}" x2="{gx + W:.1f}" y2="{gy + H:.1f}">
      <stop offset="0" stop-color="{FIELD[0]}"/>
      <stop offset="1" stop-color="{FIELD[1]}"/>
    </linearGradient>

    <!-- The delta ramp runs along the registration offset itself, so the
         disagreement is hottest where the planes first part company and cools
         as it runs away from the true edge. -->
    <linearGradient id="delta" gradientUnits="userSpaceOnUse"
        x1="{gx + W * 0.40:.1f}" y1="{gy + H * 0.40:.1f}"
        x2="{cx_ + W:.1f}" y2="{cy_ + H:.1f}">
      <stop offset="0"    stop-color="{DELTA_HOT}"/>
      <stop offset="0.48" stop-color="{DELTA_MID}"/>
      <stop offset="1"    stop-color="{DELTA_DEEP}"/>
    </linearGradient>
    <linearGradient id="deltaLine" gradientUnits="userSpaceOnUse"
        x1="{ax:.1f}" y1="{ay + H * 0.30:.1f}"
        x2="{ax + W * 0.42:.1f}" y2="{ay:.1f}">
      <stop offset="0"    stop-color="{DELTA_MID}" stop-opacity="0"/>
      <stop offset="0.32" stop-color="{DELTA_MID}"/>
      <stop offset="0.72" stop-color="{DELTA_HOT}"/>
      <stop offset="1"    stop-color="{DELTA_HOT}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="spill" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"    stop-color="{SPILL}" stop-opacity="0.30"/>
      <stop offset="0.46" stop-color="{SPILL}" stop-opacity="0.11"/>
      <stop offset="1"    stop-color="{SPILL}" stop-opacity="0"/>
    </radialGradient>

    <clipPath id="capClip">{rrect(cx_, cy_, W, H, R)}</clipPath>
    <clipPath id="geoClip">{rrect(gx, gy, W, H, R)}</clipPath>

    <!-- Everything OUTSIDE the true geometry. Two subpaths with an explicit
         clip-rule: SVG's nonzero default would silently union them. -->
    <clipPath id="outsideTrue" clipPathUnits="userSpaceOnUse">
      <path clip-rule="evenodd" d="M0,0 H{TILE} V{TILE} H0 Z
        M{gx + R:.2f},{gy:.2f} H{gx + W - R:.2f}
        A{R},{R} 0 0 1 {gx + W:.2f},{gy + R:.2f} V{gy + H - R:.2f}
        A{R},{R} 0 0 1 {gx + W - R:.2f},{gy + H:.2f} H{gx + R:.2f}
        A{R},{R} 0 0 1 {gx:.2f},{gy + H - R:.2f} V{gy + R:.2f}
        A{R},{R} 0 0 1 {gx + R:.2f},{gy:.2f} Z"/>
    </clipPath>

    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="softer" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>
  </defs>"""


def plane_shadow(reg, dx, dy, blur, op):
    """A soft shadow a plane casts onto the plane behind it — the depth cue the
    stack lives on. Offset down-right, on the one key light."""
    x, y, _, _ = frame(reg)
    return (f'<g filter="url(#{blur})" opacity="{op}">'
            + rrect(x + dx, y + dy, W, H, R, f'fill="{SHADOW}"') + '</g>')


def layer_bg():
    gx, gy, _, _ = frame(GEO)
    return "\n    ".join([
        f'<rect width="{TILE}" height="{TILE}" fill="url(#cushion)"/>',
        f'<rect width="{TILE}" height="{TILE}" fill="url(#vignette)"/>',
        f'<rect x="3" y="3" width="{TILE - 6}" height="{TILE - 6}" fill="none" '
        f'stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="4"/>',
        # the whole stack's ground contact shadow, thrown from its centre mass
        f'<g filter="url(#softer)" opacity="0.40">'
        + rrect(gx + 26, gy + 54, W, H, R, f'fill="{SHADOW}"') + '</g>',
    ])


def wireframe():
    """The accessibility tree: the same window, structure only, at the back.

    Drawn slate throughout, then re-stroked in vermilion where it falls outside
    the true geometry — a faint hairline, because a hairline is all the tree
    ever has to say with. Secondary to the capture's overhang; the ramp fades
    it at both ends so it is a found segment, not a second outline.
    """
    ax, ay, acx, acy = frame(AX)
    parts = [
        rrect(ax, ay, W, H, R, 'fill="none" stroke="{S}" stroke-opacity="{O}" stroke-width="{A}"'),
        f'<path d="M{ax:.2f},{ay + TB:.2f} H{ax + W:.2f}" fill="none" '
        'stroke="{S}" stroke-opacity="{O2}" stroke-width="{B}"/>',
    ]
    for i in range(3):
        parts.append(f'<circle cx="{ax + 40 + i * 46:.1f}" cy="{ay + TB / 2:.1f}" r="15.5" '
                     'fill="none" stroke="{S}" stroke-opacity="{O2}" stroke-width="{B}"/>')
    body = "\n      ".join(parts)
    t = f'rotate({AX["rot"]},{acx:.1f},{acy:.1f})'
    return (f'<g transform="{t}">\n      '
            + body.format(S=SLATE, O=0.72, O2=0.44, A=6.0, B=3.2)
            + f'\n    </g>\n    <g transform="{t}" clip-path="url(#outsideTrue)">\n      '
            + body.format(S="url(#deltaLine)", O=0.85, O2=0.0, A=5.4, B=0.0)
            + '\n    </g>')


def window_solid():
    """The layer geometry: the only one of the three with mass. Clean porcelain
    now — no dark sidebar greying the focal plane; value is carried by the tree
    keyline, the content rows and the accent, as it is in the raster takes."""
    gx, gy, _, _ = frame(GEO)
    o = [rrect(gx, gy, W, H, R, 'fill="url(#face)"'), '<g clip-path="url(#geoClip)">',
         f'<rect x="{gx:.2f}" y="{gy + TB:.2f}" width="{W}" height="{H - TB:.2f}" fill="url(#field)"/>',
         f'<rect x="{gx:.2f}" y="{gy:.2f}" width="{W}" height="{TB}" fill="url(#chrome)"/>',
         f'<rect x="{gx:.2f}" y="{gy + TB - 1.6:.2f}" width="{W}" height="1.6" '
         f'fill="{RIM_DARK}" fill-opacity="0.30"/>']
    # faint filled traffic dots — the solid is a real window, like the raster
    # takes' middle pane; they sit clear of the tree's circles at this offset.
    for i in range(3):
        o.append(f'<circle cx="{gx + 40 + i * 46:.1f}" cy="{gy + TB / 2:.1f}" r="11" '
                 f'fill="{DOT}"/>')
    for t, hh in ROWS:
        y = gy + TB + (H - TB) * t
        hgt = (H - TB) * hh
        o.append(rrect(gx + ROW_INSET, y, W - ROW_INSET * 2, hgt, hgt / 2,
                       f'fill="{ROW}" fill-opacity="0.55"'))
    o.append('</g>')
    return "\n    ".join(o)


def capture():
    """The captured pixels, each sample looked up against the geometry beneath.

    Agreement is quiet; samples that fall where the geometry says there is
    nothing come back vermilion. Past the capture's own frame the band does not
    stop cleanly — it dissolves into a few loose samples, which reads as an
    instrument disagreeing rather than a border. Seeded, so identical on every
    build. Tighter scatter now, so it is a clean extrusion, not confetti.
    """
    cx_, cy_, ccx, ccy = frame(CAP)
    rng = random.Random(SEED)
    corner = (cx_ + W, cy_ + H)
    pad = int(math.ceil(SCATTER))
    quiet, hot = [], []
    for iy in range(-pad, int(math.ceil(H / CELL)) + pad):
        for ix in range(-pad, int(math.ceil(W / CELL)) + pad):
            lx, ly = cx_ + ix * CELL, cy_ + iy * CELL
            mx, my = lx + CELL / 2, ly + CELL / 2
            px, py = rot(mx, my, ccx, ccy, CAP["rot"])
            kind = probe(px, py)
            in_cap = inside_rrect(mx, my, cx_, cy_, W, H, R)
            cell = (f'<rect x="{lx:.2f}" y="{ly:.2f}" width="{CELL - GAP:.2f}" '
                    f'height="{CELL - GAP:.2f}" rx="3" ')
            if kind != "delta":
                if in_cap:
                    col, op = SAMPLE[kind]
                    quiet.append(cell + f'fill="{col}" fill-opacity="{op}"/>')
                continue
            d = math.hypot(px - corner[0], py - corner[1])
            a = max(0.32, min(1.0, 1.12 - d / 560.0))
            if in_cap:
                hot.append(cell + f'fill="url(#delta)" fill-opacity="{a:.2f}"/>')
                continue
            # Only on the two edges where the capture actually overhangs the
            # geometry — measuring the box distance in all four directions
            # rings the whole object in confetti.
            ox = max(mx - (cx_ + W), 0.0)
            oy = max(my - (cy_ + H), 0.0)
            if ox == 0.0 and oy == 0.0:
                continue
            out = math.hypot(ox, oy) / CELL
            if out > SCATTER:
                continue
            keep = 1.0 - out / SCATTER
            if rng.random() > (keep ** 3) * (a * a):
                continue
            sz = (CELL - GAP) * (0.64 + 0.36 * keep)
            hot.append(f'<rect x="{lx:.2f}" y="{ly:.2f}" width="{sz:.2f}" '
                       f'height="{sz:.2f}" rx="3" fill="url(#delta)" '
                       f'fill-opacity="{a * keep:.2f}"/>')
    hot_s = "".join(hot)
    return "\n    ".join([
        f'<g transform="rotate({CAP["rot"]},{ccx:.1f},{ccy:.1f})">',
        f'<g clip-path="url(#capClip)">' + "\n      ".join(quiet) + '</g>',
        f'<g filter="url(#bloom)" opacity="0.36">{hot_s}</g>',
        "\n      ".join(hot),
        '</g>',
    ])


def highlights():
    gx, gy, _, _ = frame(GEO)
    cx_, cy_, ccx, ccy = frame(CAP)
    return "\n    ".join([
        # the solid plane's lit top-left edges, and its dark bottom-right keyline
        f'<path d="M{gx:.2f},{gy + H - R:.2f} V{gy + R:.2f} '
        f'A{R},{R} 0 0 1 {gx + R:.2f},{gy:.2f} H{gx + W - R:.2f}" fill="none" '
        f'stroke="{RIM_LIT}" stroke-opacity="0.92" stroke-width="3.0"/>',
        f'<path d="M{gx + W:.2f},{gy + R:.2f} V{gy + H - R:.2f} '
        f'A{R},{R} 0 0 1 {gx + W - R:.2f},{gy + H:.2f} H{gx + R:.2f}" fill="none" '
        f'stroke="{RIM_DARK}" stroke-opacity="0.40" stroke-width="2.4"/>',
        # the capture's own aperture edge, cool against the warm ground
        f'<g transform="rotate({CAP["rot"]},{ccx:.1f},{ccy:.1f})">'
        + rrect(cx_, cy_, W, H, R,
                'fill="none" stroke="#8E99A8" stroke-opacity="0.34" stroke-width="2.2"')
        + '</g>',
    ])


def build():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{TILE}" height="{TILE}"
     viewBox="0 0 {TILE} {TILE}">
  <title>proctor — three registrations of one window, and the delta between them</title>
{defs()}

  <g id="bg">
    {layer_bg()}
  </g>

  <g id="tree">
    {wireframe()}
  </g>

  <g id="mid">
    {plane_shadow(GEO, 20, 30, "soft", 0.34)}
    {window_solid()}
  </g>

  <g id="fg">
    {plane_shadow(CAP, 16, 24, "soft", 0.26)}
    {capture()}
    <ellipse cx="{frame(CAP)[0] + W * 0.86:.1f}" cy="{frame(CAP)[1] + H * 0.92:.1f}" rx="300" ry="240" fill="url(#spill)"/>
  </g>

  <g id="highlight">
    {highlights()}
  </g>
</svg>
"""


if __name__ == "__main__":
    out = pathlib.Path(__file__).resolve().parent / "icon.svg"
    out.write_text(build())
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")
