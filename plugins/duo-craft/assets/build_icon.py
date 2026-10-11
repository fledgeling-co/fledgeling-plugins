#!/usr/bin/env python3
"""Build the duo-craft icon master.

Geometry and material live here as named constants so a fidelity round is a
parameter edit rather than path surgery.

    python3 build_icon.py            # writes icon.svg beside this file

THE SUBJECT — "Two panes at a fold"
-----------------------------------
A book-style foldable standing open on the bench, spine away from us, its two
inner panes facing the viewer like an open book. The left pane holds a list of
three rows; the right pane holds the detail of the one selected.

SIGNATURE MOVE: the selection carries across the hinge. The only ember in the
tile is the selected row's mark on the left pane and the detail's title bar on
the right — one choice, shown on both sides of the fold. That is the skill's
central pattern (list and detail split at the fold) in a single read, and it
is why the accent sits on the screens rather than on the device.

Not a phone silhouette with a crease drawn on it: the device is a physical
object with thickness, a spine and a contact shadow, worked in the same
porcelain-and-dark-object register as its siblings.

MEASURED VALUES
---------------
Ground, contact shadow and accent are the fledgeling family's, lifted from
plugins/mac-craft/assets/build_icon.py, which measured them against
create-mac-icon/references/corpus/apple-2026/: apple-18's porcelain ramp
(L 0.986 -> 0.884, a narrow high fall), its wide shallow pool plus narrow seat
contact shadow, and the shared accent #E9562A. apple-30's per-face separation
(top:flank about 2.3:1) sets the body's face-to-flank ratio here.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = (HERE / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt")
S = 1024

# ---------------------------------------------------------------- geometry
# The spine is farther away (higher, shorter); the outer edges are nearer
# (lower, taller). Each pane is a vertical-sided quad, mapped bilinearly.
SPINE_TOP = (512.0, 236.0)
SPINE_BOT = (512.0, 690.0)
OUTER_X = 150.0             # left outer edge x; the right mirrors it
OUTER_TOP_Y = 300.0
OUTER_BOT_Y = 800.0
THICK = 30.0                # the body's flank, extruded straight down
SPINE_W = 22.0
BEZEL_U, BEZEL_V = 0.06, 0.05     # screen inset as a fraction of the pane
BODY_R = 34.0               # body corner radius, px
SCREEN_R = 22.0             # screen corner radius, px
PILL_R = 0.5                # rows and bars are pills: radius as a fraction of their height
JOIN = 14.0                 # rounded-join stroke that softens the body's corners

# ---------------------------------------------------------------- palette
KEY_A, KEY_B = (170.0, 40.0), (880.0, 920.0)
GROUND_HI = "#FDFCF9"
GROUND_MID = "#F3EFE7"
GROUND_LO = "#E7E1D5"
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"
POOL = "#B7AA90"
SEAT_DARK = "#5E4F3A"

BODY_FACE = "#4B423B"       # the bezel, L ~0.29
BODY_FLANK = "#25201C"      # the extruded flank, L ~0.13 (about 2.3:1)
BODY_ARRIS = "#8F8274"      # the lit catch along the top edges
RIM_HI, RIM_LO = "#B9AD9F", "#3A332D"   # the metal band round the body, lit upper-left
SPINE_HI = "#6A5F55"
SPINE_LO = "#1E1A17"

SCREEN_L_HI, SCREEN_L_LO = "#F4F0E9", "#E3DCD0"   # the left pane faces away from the key
SCREEN_R_HI, SCREEN_R_LO = "#FFFDF9", "#EEE8DE"   # the right pane faces into it
INK_SOFT = "#CFC6B8"        # row dots and text lines
INK_FAINT = "#DDD5C8"
PHOTO_HI, PHOTO_LO = "#D9CDBB", "#BFB09A"
ACCENT = "#E9562A"
ACCENT_TINT = "#F7D5C6"
CREASE = "#8E8070"


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


LEFT = ((OUTER_X, OUTER_TOP_Y), SPINE_TOP, SPINE_BOT, (OUTER_X, OUTER_BOT_Y))
RIGHT = (SPINE_TOP, (S - OUTER_X, OUTER_TOP_Y), (S - OUTER_X, OUTER_BOT_Y), SPINE_BOT)


def M(quad, u, v):
    """Bilinear map: u 0->1 across (top-left -> top-right), v 0->1 down."""
    tl, tr, br, bl = quad
    return lerp(lerp(tl, tr, u), lerp(bl, br, u), v)


def screen(quad, su, sv):
    return M(quad, BEZEL_U + su * (1 - 2 * BEZEL_U), BEZEL_V + sv * (1 - 2 * BEZEL_V))


def poly(pts, close=True):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


def rect(quad, u0, v0, u1, v1, n=1):
    top = [screen(quad, u0 + (u1 - u0) * i / n, v0) for i in range(n + 1)]
    bot = [screen(quad, u1 - (u1 - u0) * i / n, v1) for i in range(n + 1)]
    return top + bot


def rrect_pane(quad, u0, v0, u1, v1, r_px, n=6, in_screen=False):
    """A rounded rectangle in pane (or screen) space, mapped through the quad. r_px is converted
    to u and v separately using the pane's mean width and height, so corners stay round."""
    import math
    tl, tr, br, bl = quad
    w = (abs(tr[0] - tl[0]) + abs(br[0] - bl[0])) / 2
    h = (abs(bl[1] - tl[1]) + abs(br[1] - tr[1])) / 2
    if in_screen:
        w *= (1 - 2 * BEZEL_U); h *= (1 - 2 * BEZEL_V)
    ru = min(r_px / w, (u1 - u0) / 2); rv = min(r_px / h, (v1 - v0) / 2)
    f = screen if in_screen else M
    pts = []
    for cu, cv, a0 in ((u1 - ru, v0 + rv, -90), (u1 - ru, v1 - rv, 0), (u0 + ru, v1 - rv, 90), (u0 + ru, v0 + rv, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append(f(quad, cu + ru * math.cos(a), cv + rv * math.sin(a)))
    return pts


def pill(quad, u0, v0, u1, v1):
    tl, tr, br, bl = quad
    h = (abs(bl[1] - tl[1]) + abs(br[1] - tr[1])) / 2 * (1 - 2 * BEZEL_V)
    return rrect_pane(quad, u0, v0, u1, v1, (v1 - v0) * h * PILL_R, in_screen=True)


def ellipse(quad, cu, cv, ru, rv, n=24):
    import math
    return [screen(quad, cu + ru * math.cos(2 * math.pi * k / n), cv + rv * math.sin(2 * math.pi * k / n))
            for k in range(n)]


def build() -> str:
    sq = SQUIRCLE.read_text().strip()
    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    add('<defs>')
    add(f'''<linearGradient id="ground" gradientUnits="userSpaceOnUse" x1="350" y1="0" x2="600" y2="{S}">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/></linearGradient>''')
    add(f'''<radialGradient id="vig" cx="0.42" cy="0.30" r="0.85">
      <stop offset="0.62" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.22"/></radialGradient>''')
    add(f'''<linearGradient id="scrL" gradientUnits="userSpaceOnUse" x1="{KEY_A[0]}" y1="{KEY_A[1]}" x2="{KEY_B[0]}" y2="{KEY_B[1]}">
      <stop offset="0" stop-color="{SCREEN_L_HI}"/><stop offset="1" stop-color="{SCREEN_L_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="scrR" gradientUnits="userSpaceOnUse" x1="{KEY_A[0]}" y1="{KEY_A[1]}" x2="{KEY_B[0]}" y2="{KEY_B[1]}">
      <stop offset="0" stop-color="{SCREEN_R_HI}"/><stop offset="1" stop-color="{SCREEN_R_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="photo" x1="0" y1="0" x2="0.4" y2="1">
      <stop offset="0" stop-color="{PHOTO_HI}"/><stop offset="1" stop-color="{PHOTO_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="spine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SPINE_LO}"/><stop offset="0.45" stop-color="{SPINE_HI}"/>
      <stop offset="1" stop-color="{SPINE_LO}"/></linearGradient>''')
    # the fold valley: a soft shade either side of the spine, darkest at the hinge
    for side, (x0, x1) in (("creaseL", (512, 452)), ("creaseR", (512, 572))):
        add(f'''<linearGradient id="{side}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x1}" y2="0">
          <stop offset="0" stop-color="{CREASE}" stop-opacity="0.34"/>
          <stop offset="1" stop-color="{CREASE}" stop-opacity="0"/></linearGradient>''')
    add('<filter id="pool" x="-35%" y="-35%" width="170%" height="170%"><feGaussianBlur stdDeviation="40"/></filter>')
    add('<filter id="seat" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>')
    add('<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>')
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    add(f'<clipPath id="scrLclip"><path d="{poly(rrect_pane(LEFT, 0, 0, 1, 1, SCREEN_R, in_screen=True))}"/></clipPath>')
    add(f'<clipPath id="scrRclip"><path d="{poly(rrect_pane(RIGHT, 0, 0, 1, 1, SCREEN_R, in_screen=True))}"/></clipPath>')
    add('</defs>')

    add('<g clip-path="url(#tile)">')
    # ------------------------------------------------------------ bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<path d="{sq}" fill="none" stroke="{RIM_TILE}" stroke-width="7" stroke-opacity="0.55"/>')
    add('</g>')

    # ------------------------------------------------------------ mid: shadow + body
    add('<g id="mid">')
    lb, sb, rb = LEFT[3], SPINE_BOT, RIGHT[2]
    pool = [(lb[0] + 30, lb[1] - 30), (sb[0] + 40, sb[1] - 10), (rb[0] + 50, rb[1] - 20),
            (rb[0] + 70, rb[1] + 70), (sb[0] + 40, sb[1] + 120), (lb[0] + 50, lb[1] + 80)]
    add(f'<path d="{poly(pool)}" fill="{POOL}" fill-opacity="0.55" filter="url(#pool)"/>')
    seat = [(x, y + THICK) for x, y in (lb, sb, rb)]
    add(f'<path d="{poly(seat, close=False)}" fill="none" stroke="{SEAT_DARK}" stroke-width="22" '
        f'stroke-opacity="0.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#seat)"/>')
    # the flank: each rounded pane, swept straight down by THICK, so the corners stay round
    for quad in (LEFT, RIGHT):
        body = rrect_pane(quad, 0, 0, 1, 1, BODY_R)
        for k in range(0, int(THICK) + 1, 3):
            add(f'<path d="{poly([(x, y + k) for x, y in body])}" fill="{BODY_FLANK}"/>')
    for quad in (LEFT, RIGHT):
        body = rrect_pane(quad, 0, 0, 1, 1, BODY_R)
        add(f'<path d="{poly(body)}" fill="{BODY_FACE}" stroke="url(#rim)" stroke-width="7"/>')
    add('</g>')

    # ------------------------------------------------------------ fg: screens
    add('<g id="fg">')
    add(f'<path d="{poly(rrect_pane(LEFT, 0, 0, 1, 1, SCREEN_R, in_screen=True))}" fill="url(#scrL)"/>')
    add(f'<path d="{poly(rrect_pane(RIGHT, 0, 0, 1, 1, SCREEN_R, in_screen=True))}" fill="url(#scrR)"/>')

    # left pane: three rows, the middle one selected
    add('<g clip-path="url(#scrLclip)">')
    rows = [(0.10, 0.30), (0.38, 0.58), (0.66, 0.86)]
    for i, (v0, v1) in enumerate(rows):
        sel = i == 1
        if sel:
            add(f'<path d="{poly(rrect_pane(LEFT, 0.05, v0 - 0.01, 0.95, v1 + 0.01, 16, in_screen=True))}" fill="{ACCENT_TINT}"/>')
        cv = (v0 + v1) / 2
        add(f'<path d="{poly(ellipse(LEFT, 0.17, cv, 0.075, 0.055))}" fill="{ACCENT if sel else INK_SOFT}"/>')
        add(f'<path d="{poly(pill(LEFT, 0.32, cv - 0.045, 0.86, cv + 0.005))}" '
            f'fill="{"#E9A88E" if sel else INK_SOFT}"/>')
        add(f'<path d="{poly(pill(LEFT, 0.32, cv + 0.035, 0.66, cv + 0.07))}" '
            f'fill="{"#F0C2AE" if sel else INK_FAINT}"/>')
    add(f'<rect x="452" y="0" width="60" height="{S}" fill="url(#creaseL)"/>')
    add('</g>')

    # right pane: the detail of the selected row
    add('<g clip-path="url(#scrRclip)">')
    add(f'<path d="{poly(rrect_pane(RIGHT, 0.10, 0.09, 0.80, 0.18, 12, in_screen=True))}" fill="{ACCENT}"/>')
    add(f'<path d="{poly(rrect_pane(RIGHT, 0.10, 0.25, 0.90, 0.56, 14, in_screen=True))}" fill="url(#photo)"/>')
    for v, u1 in ((0.65, 0.88), (0.74, 0.80), (0.83, 0.58)):
        add(f'<path d="{poly(pill(RIGHT, 0.10, v, u1, v + 0.035))}" fill="{INK_SOFT}"/>')
    add(f'<rect x="512" y="0" width="60" height="{S}" fill="url(#creaseR)"/>')
    add('</g>')

    # the spine between the panes
    st, sb2 = SPINE_TOP, SPINE_BOT
    add(f'<rect x="{st[0] - SPINE_W / 2:.1f}" y="{st[1] - 6:.1f}" width="{SPINE_W}" '
        f'height="{sb2[1] - st[1] + THICK + 8:.1f}" rx="{SPINE_W / 2}" fill="url(#spine)"/>')
    add('</g>')

    # ------------------------------------------------------------ highlight
    add('<g id="highlight">')
    # a faint glare across the right pane's upper area, from the key
    glare = [screen(RIGHT, 0.55, 0.0), screen(RIGHT, 0.85, 0.0), screen(RIGHT, 0.35, 1.0), screen(RIGHT, 0.05, 1.0)]
    add(f'<path d="{poly(glare)}" fill="#FFFFFF" fill-opacity="0.22" filter="url(#soft)" '
        f'clip-path="url(#scrRclip)"/>')
    add('</g>')

    add('</g>')
    add('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    (HERE / "icon.svg").write_text(build())
    print(f"wrote {HERE / 'icon.svg'}")
