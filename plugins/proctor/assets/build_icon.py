#!/usr/bin/env python3
"""Engine A for the `proctor` icon — direction "Out of True".

One macOS window form registered three times, once per observer, offset by a
hair. Where the three agree the tile is quiet porcelain; where they disagree
the delta is vermilion. That is the tri-observer check drawn rather than
described: the accessibility tree, the layer geometry and the captured pixels
each describe the same instant, and the disagreement is the finding.

    the tree      a slate keyline           — structure, no substance
    the geometry  a solid porcelain plane   — the one with mass, dead centre
    the capture   a run of discrete samples — pixels, and only pixels

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery. Re-run to emit icon.svg.

Measured off the marketplace family before the first line was authored
(see icon-notes.md § The spec):
    ground TL L 0.94, BR L 0.87, warm (create-skill, clarify, whats-left, report)
    accent hue 8-20 deg, S 0.77-0.97, V 0.88-0.98; family centre ~hue 13
    slate  #171D22 .. #343A45, S 0.25-0.32, i.e. near-neutral cool
    design-review is the one cool-ground sibling; this one stays warm, which is
    half of what keeps the two apart.
"""
from __future__ import annotations

import math
import pathlib
import random

# ----------------------------------------------------------------- geometry

TILE = 1024

W, H = 566.0, 396.0          # the window form, drawn identically three times
R = 36.0                     # its corner radius
TB = 82.0                    # titlebar height
SIDEBAR = 0.30               # sidebar split, as a fraction of W
CX, CY = 512.0, 500.0        # the registration centre

# Registration deltas. Small enough to read as "nearly aligned" rather than
# "arranged": a stack varies in scale, a misregistration does not, so all three
# forms are identical in size and only the offsets differ. The rotation is what
# keeps the near band a wedge — a pure translation reads as a drop shadow that
# has been colourised, which is the cheap version of this idea.
AX = dict(dx=-26.0, dy=-23.0, rot=-1.0)   # the accessibility tree  (drawn over)
GEO = dict(dx=0.0, dy=0.0, rot=0.0)       # the layer geometry      (the solid)
CAP = dict(dx=25.0, dy=22.0, rot=1.5)     # the captured pixels     (over the solid)

CELL = 25.0                  # the capture's sample pitch
GAP = 2.4                    # kerf between samples, so they read as discrete
SCATTER = 2.6                # how many cells the delta dissolves past the frame
SEED = 7                     # so the dissolve is the same every build

# ----------------------------------------------------------------- material

GROUND = ("#FCFAF5", "#F3EEE3", "#DCD3C1")      # cushion, key at top-left
VIGNETTE = "#8A7A62"

PORCELAIN_FACE = ("#FEFDFA", "#F2ECE0", "#DBD2C0")
CHROME = ("#FEFCF8", "#F4EFE4")                 # the titlebar band
FIELD = ("#F1EBDF", "#DBD2BF")                  # the content field
# The sidebar carries the value. Read at 16px against the siblings it will sit
# beside, the first porcelain-on-porcelain draft was the palest tile in the
# marketplace and had no separation at all — the same failure recorded against
# `clarify`, and the same fix: move part of the glyph down the value ramp and
# leave the focal plane porcelain.
PANEL = ("#838D9C", "#636D7B")                  # the sidebar, slate
ROW = "#B0A48D"
DOT = "#D6CCB9"
RIM_LIT = "#FFFFFF"
RIM_DARK = "#A2957E"

SLATE = "#333C4A"                               # near-neutral cool, S .26

# What the capture reports back. Faint over empty field, firm over content: a
# capture's dirty-rect summary is exactly this, and a uniform sheet of samples
# greys the porcelain out — the first draft's largest single defect.
SAMPLE = {
    "chrome": ("#E4EAF2", 0.13),
    "field":  ("#DCE2EB", 0.14),
    "panel":  ("#EDF1F6", 0.16),
    "row":    ("#8B97A9", 0.46),
}
DELTA_HOT = "#FF7A2E"
DELTA_MID = "#EE3B0D"
DELTA_DEEP = "#B81C02"
SPILL = "#FF9060"


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


# Two content rows only. The first draft carried four plus three sidebar rows,
# drawn three times over — twenty-one repeated elements, which reads as a
# screenshot rather than a glyph and dies at 32px. Anti-checklist #4/#5.
ROWS = [(0.16, 0.115), (0.44, 0.115)]


def probe(px, py):
    """What the layer geometry says is at this canvas point.

    This is why the capture plane is a measurement and not a texture: every
    sample is looked up against the geometry beneath it, so the two cannot
    drift apart anywhere except where they are offset. `delta` is the capture
    reporting content where the geometry says there is none.
    """
    gx, gy, _, _ = frame(GEO)
    if not inside_rrect(px, py, gx, gy, W, H, R):
        return "delta"
    ly, lx = py - gy, px - gx
    if ly < TB:
        return "chrome"
    fy = (ly - TB) / (H - TB)
    if lx < W * SIDEBAR:
        return "panel"
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
    <!-- Tahoe grammar #1: the tile is a cushion, never a print. Key top-left,
         matching every warm sibling in this marketplace. -->
    <radialGradient id="cushion" cx="0.30" cy="0.24" r="0.95">
      <stop offset="0"    stop-color="{GROUND[0]}"/>
      <stop offset="0.52" stop-color="{GROUND[1]}"/>
      <stop offset="1"    stop-color="{GROUND[2]}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">
      <stop offset="0.60" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1"    stop-color="{VIGNETTE}" stop-opacity="0.22"/>
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
    <linearGradient id="panel" gradientUnits="userSpaceOnUse"
        x1="{gx:.1f}" y1="{gy + TB:.1f}" x2="{gx + W * SIDEBAR:.1f}" y2="{gy + H:.1f}">
      <stop offset="0" stop-color="{PANEL[0]}"/>
      <stop offset="1" stop-color="{PANEL[1]}"/>
    </linearGradient>

    <!-- The delta ramp runs along the registration offset itself, so the
         disagreement is hottest where the planes first part company and cools
         as it runs away from the true edge. -->
    <linearGradient id="delta" gradientUnits="userSpaceOnUse"
        x1="{gx + W * 0.34:.1f}" y1="{gy + H * 0.34:.1f}"
        x2="{cx_ + W:.1f}" y2="{cy_ + H:.1f}">
      <stop offset="0"    stop-color="{DELTA_HOT}"/>
      <stop offset="0.48" stop-color="{DELTA_MID}"/>
      <stop offset="1"    stop-color="{DELTA_DEEP}"/>
    </linearGradient>
    <linearGradient id="deltaLine" gradientUnits="userSpaceOnUse"
        x1="{ax:.1f}" y1="{ay + H * 0.30:.1f}"
        x2="{ax + W * 0.42:.1f}" y2="{ay:.1f}">
      <stop offset="0"    stop-color="{DELTA_MID}" stop-opacity="0"/>
      <stop offset="0.30" stop-color="{DELTA_MID}"/>
      <stop offset="0.72" stop-color="{DELTA_HOT}"/>
      <stop offset="1"    stop-color="{DELTA_HOT}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="spill" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0"    stop-color="{SPILL}" stop-opacity="0.26"/>
      <stop offset="0.48" stop-color="{SPILL}" stop-opacity="0.10"/>
      <stop offset="1"    stop-color="{SPILL}" stop-opacity="0"/>
    </radialGradient>

    <clipPath id="capClip">{rrect(cx_, cy_, W, H, R)}</clipPath>
    <clipPath id="geoClip">{rrect(gx, gy, W, H, R)}</clipPath>

    <!-- Everything OUTSIDE the true geometry. Two subpaths, so it carries an
         explicit clip-rule: SVG's nonzero default silently unions them, and a
         clip that is quietly wrong reads as a material failure. -->
    <clipPath id="outsideTrue" clipPathUnits="userSpaceOnUse">
      <path clip-rule="evenodd" d="M0,0 H{TILE} V{TILE} H0 Z
        M{gx + R:.2f},{gy:.2f} H{gx + W - R:.2f}
        A{R},{R} 0 0 1 {gx + W:.2f},{gy + R:.2f} V{gy + H - R:.2f}
        A{R},{R} 0 0 1 {gx + W - R:.2f},{gy + H:.2f} H{gx + R:.2f}
        A{R},{R} 0 0 1 {gx:.2f},{gy + H - R:.2f} V{gy + R:.2f}
        A{R},{R} 0 0 1 {gx + R:.2f},{gy:.2f} Z"/>
    </clipPath>

    <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="bloom" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>"""


def layer_bg():
    cx_, cy_, _, _ = frame(CAP)
    gx, gy, _, _ = frame(GEO)
    return "\n    ".join([
        f'<rect width="{TILE}" height="{TILE}" fill="url(#cushion)"/>',
        f'<rect width="{TILE}" height="{TILE}" fill="url(#vignette)"/>',
        f'<rect x="3" y="3" width="{TILE - 6}" height="{TILE - 6}" fill="none" '
        f'stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="4"/>',
        # what the delta throws back onto the porcelain beside it
        f'<ellipse cx="{cx_ + W * 0.86:.1f}" cy="{cy_ + H * 0.90:.1f}" '
        f'rx="320" ry="255" fill="url(#spill)"/>',
        # contact shadow under the whole registration group
        '<g filter="url(#soft)" opacity="0.46">'
        + rrect(gx + 18, gy + 40, W, H, R, 'fill="#6B5C42"') + '</g>',
    ])


def window_solid():
    """The layer geometry: the only one of the three with mass."""
    gx, gy, _, _ = frame(GEO)
    o = [rrect(gx, gy, W, H, R, 'fill="url(#face)"'), '<g clip-path="url(#geoClip)">',
         f'<rect x="{gx:.2f}" y="{gy + TB:.2f}" width="{W}" height="{H - TB:.2f}" fill="url(#field)"/>',
         f'<rect x="{gx:.2f}" y="{gy:.2f}" width="{W}" height="{TB}" fill="url(#chrome)"/>',
         f'<rect x="{gx:.2f}" y="{gy + TB:.2f}" width="{W * SIDEBAR:.2f}" '
         f'height="{H - TB:.2f}" fill="url(#panel)"/>',
         f'<rect x="{gx:.2f}" y="{gy + TB - 1.8:.2f}" width="{W}" height="1.8" '
         f'fill="{RIM_DARK}" fill-opacity="0.36"/>',
         f'<rect x="{gx + W * SIDEBAR:.2f}" y="{gy + TB:.2f}" width="1.8" '
         f'height="{H - TB:.2f}" fill="{RIM_DARK}" fill-opacity="0.32"/>']
    for t, hh in ROWS:
        y = gy + TB + (H - TB) * t
        hgt = (H - TB) * hh
        o.append(rrect(gx + W * SIDEBAR + 36, y, W * (1 - SIDEBAR) - 82, hgt, hgt / 2,
                       f'fill="{ROW}" fill-opacity="0.60"'))
    # No window controls here. Each observer reports only what it can see, and
    # layer geometry sees rectangles: the controls are exposed by the tree,
    # which is the observer that actually knows what a button is. Drawing them
    # on both planes also produced six offset blobs in the titlebar.
    o.append('</g>')
    return "\n    ".join(o)


def wireframe():
    """The accessibility tree: the same window, structure only.

    Drawn slate throughout, then re-stroked in vermilion where it falls outside
    the true geometry. The tree's disagreement is a hairline, because a
    hairline is all the tree ever has to say with; the ramp fades it out at
    both ends so it is a found segment rather than a second outline.
    """
    ax, ay, acx, acy = frame(AX)
    parts = [
        rrect(ax, ay, W, H, R, 'fill="none" stroke="{S}" stroke-opacity="{O}" stroke-width="{A}"'),
        f'<path d="M{ax:.2f},{ay + TB:.2f} H{ax + W:.2f}" fill="none" '
        'stroke="{S}" stroke-opacity="{O2}" stroke-width="{B}"/>',
        f'<path d="M{ax + W * SIDEBAR:.2f},{ay + TB:.2f} V{ay + H:.2f}" fill="none" '
        'stroke="{S}" stroke-opacity="{O2}" stroke-width="{B}"/>',
    ]
    for i in range(3):
        parts.append(f'<circle cx="{ax + 38 + i * 46:.1f}" cy="{ay + TB / 2:.1f}" r="15.5" '
                     'fill="none" stroke="{S}" stroke-opacity="{O2}" stroke-width="{B}"/>')
    body = "\n      ".join(parts)
    t = f'rotate({AX["rot"]},{acx:.1f},{acy:.1f})'
    return (f'<g transform="{t}">\n      '
            + body.format(S=SLATE, O=0.70, O2=0.46, A=6.4, B=3.4)
            + f'\n    </g>\n    <g transform="{t}" clip-path="url(#outsideTrue)">\n      '
            + body.format(S="url(#deltaLine)", O=1.0, O2=0.0, A=7.0, B=0.0)
            + '\n    </g>')


def capture():
    """The captured pixels, each sample looked up against the geometry beneath.

    Agreement is quiet; samples that fall where the geometry says there is
    nothing come back vermilion. Past the capture's own frame that band does not
    stop cleanly — it dissolves into loose samples, which is the one idea worth
    keeping from the raster takes: a clean orange edge reads as a border, and a
    disintegrating one reads as an instrument disagreeing. Seeded, so the
    dissolve is identical on every build.
    """
    cx_, cy_, ccx, ccy = frame(CAP)
    rng = random.Random(SEED)
    # The disagreement is worst at the corner the two planes part company
    # furthest, and dies along both arms. Without this the delta wraps the whole
    # near edge at one strength and reads as an orange border rather than as a
    # localised finding — the opposite of what a proctor reports.
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
            a = max(0.30, min(1.0, 1.10 - d / 620.0))
            if in_cap:
                hot.append(cell + f'fill="url(#delta)" fill-opacity="{a:.2f}"/>')
                continue
            # How far past the capture's own frame this sample has strayed —
            # and only on the two edges where the capture actually overhangs the
            # geometry. Measuring the box distance in all four directions rings
            # the whole object in confetti, because a cell far enough up-left of
            # the capture frame is also outside the geometry and scores as a
            # delta it has no business reporting.
            ox = max(mx - (cx_ + W), 0.0)
            oy = max(my - (cy_ + H), 0.0)
            if ox == 0.0 and oy == 0.0:
                continue
            out = math.hypot(ox, oy) / CELL
            if out > SCATTER:
                continue
            keep = 1.0 - out / SCATTER
            # The dissolve also has to die along the arms, not just outward.
            # Probability weighted by the same corner falloff the band uses,
            # otherwise a lone sample strays out at the far end of an arm where
            # the fringe has already gone, and reads as dirt on the tile.
            if rng.random() > (keep ** 3) * (a * a):
                continue
            sz = (CELL - GAP) * (0.62 + 0.38 * keep)
            hot.append(f'<rect x="{lx:.2f}" y="{ly:.2f}" width="{sz:.2f}" '
                       f'height="{sz:.2f}" rx="3" fill="url(#delta)" '
                       f'fill-opacity="{a * keep:.2f}"/>')
    hot_s = "".join(hot)
    return "\n    ".join([
        # the dissolve deliberately escapes capClip; the quiet samples do not
        f'<g transform="rotate({CAP["rot"]},{ccx:.1f},{ccy:.1f})">',
        f'<g clip-path="url(#capClip)">' + "\n      ".join(quiet) + '</g>',
        f'<g filter="url(#bloom)" opacity="0.34">{hot_s}</g>',
        "\n      ".join(hot),
        '</g>',
    ])


def highlights():
    gx, gy, _, _ = frame(GEO)
    cx_, cy_, ccx, ccy = frame(CAP)
    return "\n    ".join([
        # the true plane's lit top-left edges, and its dark bottom-right keyline
        f'<path d="M{gx:.2f},{gy + H - R:.2f} V{gy + R:.2f} '
        f'A{R},{R} 0 0 1 {gx + R:.2f},{gy:.2f} H{gx + W - R:.2f}" fill="none" '
        f'stroke="{RIM_LIT}" stroke-opacity="0.92" stroke-width="3.2"/>',
        f'<path d="M{gx + W:.2f},{gy + R:.2f} V{gy + H - R:.2f} '
        f'A{R},{R} 0 0 1 {gx + W - R:.2f},{gy + H:.2f} H{gx + R:.2f}" fill="none" '
        f'stroke="{RIM_DARK}" stroke-opacity="0.42" stroke-width="2.6"/>',
        # the capture's own aperture edge, cool against the warm ground
        f'<g transform="rotate({CAP["rot"]},{ccx:.1f},{ccy:.1f})">'
        + rrect(cx_, cy_, W, H, R,
                'fill="none" stroke="#8E99A8" stroke-opacity="0.30" stroke-width="2.2"')
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

  <g id="mid">
    {window_solid()}
  </g>

  <g id="fg">
    {capture()}
    {wireframe()}
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
