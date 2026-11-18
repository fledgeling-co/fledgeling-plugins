#!/usr/bin/env python3
"""Build the home-craft icon master.

Geometry and material live here as named constants, so a fidelity round is a parameter edit
rather than path surgery.

    python3 build_icon.py            # writes icon.svg (the master) and icon-engineA-handauthored.svg

THE SUBJECT — "One tile, two screens"
--------------------------------------
Two dark displays on the porcelain bench: a square countertop display on a wedge stand, set back
on the left, and a wide car display in front of it on the right, set into a curved dash. Each
screen shows a few pale tiles.

SIGNATURE MOVE: the same small widget glows on both screens. It is the only ember in the tile,
and it sits in the same corner of each screen, so the eye reads one thing shown twice. That is the
skill's central fact in one read: HomeView has no SDK, and an app reaches the counter and the car
as the same small widget (or the same CarPlay app) from one phone.

MEASURED VALUES
---------------
Ground ramp, contact shadow and accent are the fledgeling family's, lifted unchanged from
plugins/duo-craft/assets/build_icon.py (itself measured against create-mac-icon's apple-2026
corpus via mac-craft). Sampled for this commission from the corpus at 128px:
apple-04 / apple-22 / apple-18 / apple-30 put the darkest object pixel at L 0.13-0.14 and the
porcelain median at L 0.57-0.85. The corpus darks are faintly cool (21,25,28); the family's are
warm, and the family wins for shelf consistency. Body face L ~0.29, flank L ~0.13 (about 2.3:1),
as apple-30's per-face separation.
"""

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "skills" / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- geometry
# Countertop display: a square panel on a wedge stand, set back at top right (higher, smaller).
HOME_X, HOME_Y, HOME_W = 498.0, 146.0, 392.0      # panel top-left and side
HOME_R = 58.0                                      # panel corner radius
HOME_BEZEL = 26.0
STAND_TOP_W, STAND_BOT_W, STAND_H = 120.0, 236.0, 128.0
# Car display: a wide panel in front at bottom left, lower and nearer, set into a dash lip.
CAR_X, CAR_Y, CAR_W, CAR_H = 120.0, 540.0, 556.0, 252.0
CAR_R = 48.0
CAR_BEZEL = 22.0
LIP_OUT = 64.0          # how far the dash lip reaches past the display on each side
LIP_RISE = 0.42         # where the lip's ends meet the display, as a fraction of its height
LIP_DEPTH = 64.0        # the lip's depth below the display
VENT_W, VENT_H = 40.0, 70.0   # the vents in the lip's two ends
THICK = 26.0            # body flank, extruded down and slightly right
FLANK_DX = 8.0
# The widget: identical rounded square in the same corner of both screens.
WIDGET_FRAC = 0.40      # side as a fraction of the HomeView screen's side
WIDGET_R_FRAC = 0.24    # corner radius as a fraction of its side
GAP_FRAC = 0.07         # inset from the screen corner, as a fraction of the screen's short side

# ---------------------------------------------------------------- palette
GROUND_HI = "#FDFCF9"
GROUND_MID = "#F3EFE7"
GROUND_LO = "#E7E1D5"
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"
POOL = "#B7AA90"
SEAT_DARK = "#5E4F3A"

BODY_FACE = "#4B423B"
BODY_FLANK = "#25201C"
RIM_HI, RIM_LO = "#B9AD9F", "#3A332D"
STAND_HI, STAND_LO = "#5A4F46", "#2A241F"
DASH_HI, DASH_LO = "#A89A86", "#6F6253"   # warm taupe, L ~0.6 -> 0.4: a dash, not a second dark object
VENT_SLAT = "#3A322B"

SCREEN_HI, SCREEN_LO = "#FFFDF9", "#ECE5DA"
TILE_A, TILE_B = "#DCD3C5", "#E6DFD3"
ACCENT = "#E9562A"
ACCENT_HI = "#F58A5E"
ACCENT_GLOW = "#E9562A"
GLINT = "#FFFFFF"


def rrect(x, y, w, h, r):
    return (f'M{x + r:.1f},{y:.1f} H{x + w - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + r:.1f} '
            f'V{y + h - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + w - r:.1f},{y + h:.1f} '
            f'H{x + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x:.1f},{y + h - r:.1f} '
            f'V{y + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y:.1f} Z')


def flank(x, y, w, h, r, fill):
    """The body swept down and right by THICK, so the rounded corners stay round."""
    steps = []
    for k in range(0, int(THICK) + 1, 2):
        t = k / THICK
        steps.append(f'<path d="{rrect(x + FLANK_DX * t, y + k, w, h, r)}" fill="{fill}"/>')
    return "".join(steps)


def widget(sx, sy, side, glow_id):
    """The shared widget at (sx, sy), side px: a soft glow, the ember tile, its lit top edge, a glyph."""
    r = side * WIDGET_R_FRAC
    out = [
        f'<path d="{rrect(sx - 6, sy - 4, side + 12, side + 12, r + 6)}" fill="{ACCENT_GLOW}" '
        f'fill-opacity="0.38" filter="url(#{glow_id})"/>',
        f'<path d="{rrect(sx, sy, side, side, r)}" fill="url(#ember)"/>',
        f'<path d="{rrect(sx + 2, sy + 2, side - 4, side * 0.48, r * 0.9)}" fill="{GLINT}" fill-opacity="0.18"/>',
    ]
    # glyph: a white ring with a filled centre, the same on both screens
    cx, cy = sx + side / 2, sy + side / 2
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{side * 0.22:.1f}" fill="none" stroke="#FFFFFF" '
               f'stroke-width="{side * 0.075:.1f}" stroke-opacity="0.95"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{side * 0.075:.1f}" fill="#FFFFFF" fill-opacity="0.95"/>')
    return "".join(out)


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
    add(f'''<linearGradient id="screen" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0" stop-color="{SCREEN_HI}"/><stop offset="1" stop-color="{SCREEN_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{RIM_HI}"/><stop offset="1" stop-color="{RIM_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="stand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{STAND_HI}"/><stop offset="1" stop-color="{STAND_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="dash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{DASH_HI}"/><stop offset="1" stop-color="{DASH_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="ember" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/><stop offset="1" stop-color="{ACCENT}"/></linearGradient>''')
    add('<filter id="pool" x="-35%" y="-35%" width="170%" height="170%"><feGaussianBlur stdDeviation="38"/></filter>')
    add('<filter id="seat" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="9"/></filter>')
    add('<filter id="glowA" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>')
    add('<filter id="glowB" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="12"/></filter>')
    add('<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>')
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    hs_x, hs_y = HOME_X + HOME_BEZEL, HOME_Y + HOME_BEZEL
    hs_w = HOME_W - 2 * HOME_BEZEL
    cs_x, cs_y = CAR_X + CAR_BEZEL, CAR_Y + CAR_BEZEL
    cs_w, cs_h = CAR_W - 2 * CAR_BEZEL, CAR_H - 2 * CAR_BEZEL
    add(f'<clipPath id="homeScreen"><path d="{rrect(hs_x, hs_y, hs_w, hs_w, HOME_R - HOME_BEZEL * 0.6)}"/></clipPath>')
    add(f'<clipPath id="carScreen"><path d="{rrect(cs_x, cs_y, cs_w, cs_h, CAR_R - CAR_BEZEL * 0.6)}"/></clipPath>')
    add('</defs>')

    add('<g clip-path="url(#tile)">')
    # ------------------------------------------------------------ bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<path d="{sq}" fill="none" stroke="{RIM_TILE}" stroke-width="7" stroke-opacity="0.55"/>')
    add('</g>')

    # ------------------------------------------------------------ mid: shadows, stand, bodies
    add('<g id="mid">')
    # contact pools under both objects
    add(f'<ellipse cx="{HOME_X + HOME_W / 2 + 20:.1f}" cy="{HOME_Y + HOME_W + STAND_H + 6:.1f}" rx="190" ry="42" '
        f'fill="{POOL}" fill-opacity="0.55" filter="url(#pool)"/>')
    add(f'<ellipse cx="{CAR_X + CAR_W / 2 + 24:.1f}" cy="{CAR_Y + CAR_H + 22:.1f}" rx="320" ry="40" '
        f'fill="{POOL}" fill-opacity="0.6" filter="url(#pool)"/>')
    # the countertop display's wedge stand
    sx_mid = HOME_X + HOME_W / 2
    st_top = HOME_Y + HOME_W - 10
    stand = (f'M{sx_mid - STAND_TOP_W / 2:.1f},{st_top:.1f} L{sx_mid + STAND_TOP_W / 2:.1f},{st_top:.1f} '
             f'L{sx_mid + STAND_BOT_W / 2:.1f},{st_top + STAND_H:.1f} L{sx_mid - STAND_BOT_W / 2:.1f},{st_top + STAND_H:.1f} Z')
    add(f'<path d="M{sx_mid - STAND_BOT_W / 2 + 10:.1f},{st_top + STAND_H + 4:.1f} H{sx_mid + STAND_BOT_W / 2 + 10:.1f}" '
        f'stroke="{SEAT_DARK}" stroke-width="16" stroke-opacity="0.5" stroke-linecap="round" filter="url(#seat)"/>')
    add(f'<path d="{stand}" fill="url(#stand)" stroke="{STAND_LO}" stroke-width="6" stroke-linejoin="round"/>')
    # countertop display body
    add(flank(HOME_X, HOME_Y, HOME_W, HOME_W, HOME_R, BODY_FLANK))
    add(f'<path d="{rrect(HOME_X, HOME_Y, HOME_W, HOME_W, HOME_R)}" fill="{BODY_FACE}" stroke="url(#rim)" stroke-width="7"/>')
    # the dash lip: a curved band that cradles the car display, an air vent in each end
    lx0, lx1 = CAR_X - LIP_OUT, CAR_X + CAR_W + LIP_OUT
    ly_end = CAR_Y + CAR_H * LIP_RISE
    ly_bot = CAR_Y + CAR_H + LIP_DEPTH
    lip = (f'M{lx0:.1f},{ly_end:.1f} C{lx0:.1f},{ly_bot:.1f} {lx0 + 60:.1f},{ly_bot:.1f} {lx0 + 140:.1f},{ly_bot:.1f} '
           f'H{lx1 - 140:.1f} C{lx1 - 60:.1f},{ly_bot:.1f} {lx1:.1f},{ly_bot:.1f} {lx1:.1f},{ly_end:.1f} '
           f'C{lx1:.1f},{ly_end - 26:.1f} {lx1 - 30:.1f},{ly_end - 30:.1f} {lx1 - 46:.1f},{ly_end - 30:.1f} '
           f'H{lx0 + 46:.1f} C{lx0 + 30:.1f},{ly_end - 30:.1f} {lx0:.1f},{ly_end - 26:.1f} {lx0:.1f},{ly_end:.1f} Z')
    add(f'<path d="M{lx0 + 40:.1f},{ly_bot + 8:.1f} H{lx1 - 20:.1f}" stroke="{SEAT_DARK}" stroke-width="20" '
        f'stroke-opacity="0.45" stroke-linecap="round" filter="url(#seat)"/>')
    add(f'<path d="{lip}" fill="url(#dash)"/>')
    add(f'<path d="M{lx0 + 6:.1f},{ly_end - 4:.1f} C{lx0 + 14:.1f},{ly_end - 26:.1f} {lx0 + 30:.1f},{ly_end - 30:.1f} {lx0 + 46:.1f},{ly_end - 30:.1f} '
        f'H{lx1 - 46:.1f}" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.5" stroke-linecap="round"/>')
    for vx in (lx0 + 12, lx1 - 12 - VENT_W):
        vy = ly_end + 6
        add(f'<path d="{rrect(vx, vy, VENT_W, VENT_H, 12)}" fill="{VENT_SLAT}"/>')
        for k in range(1, 4):
            y = vy + VENT_H * k / 4
            add(f'<path d="M{vx + 7:.1f},{y:.1f} H{vx + VENT_W - 7:.1f}" stroke="{DASH_HI}" stroke-width="3" stroke-opacity="0.75"/>')
    # car display body
    add(flank(CAR_X, CAR_Y, CAR_W, CAR_H, CAR_R, BODY_FLANK))
    add(f'<path d="{rrect(CAR_X, CAR_Y, CAR_W, CAR_H, CAR_R)}" fill="{BODY_FACE}" stroke="url(#rim)" stroke-width="7"/>')
    add('</g>')

    # ------------------------------------------------------------ fg: screens and the shared widget
    add('<g id="fg">')
    side = hs_w * WIDGET_FRAC
    gap_home = hs_w * GAP_FRAC
    # countertop screen: a 2x2 grid; top-left is the widget
    add(f'<path d="{rrect(hs_x, hs_y, hs_w, hs_w, HOME_R - HOME_BEZEL * 0.6)}" fill="url(#screen)"/>')
    add('<g clip-path="url(#homeScreen)">')
    cell = (hs_w - 3 * gap_home) / 2
    for i, j in ((1, 0), (0, 1), (1, 1)):
        x = hs_x + gap_home + i * (cell + gap_home)
        y = hs_y + gap_home + j * (cell + gap_home)
        add(f'<path d="{rrect(x, y, cell, cell, cell * WIDGET_R_FRAC)}" fill="{TILE_A if (i + j) % 2 else TILE_B}"/>')
    add('</g>')
    add(widget(hs_x + gap_home, hs_y + gap_home, cell, "glowA"))
    # car screen: the same widget at the same corner, then wide pale tiles
    add(f'<path d="{rrect(cs_x, cs_y, cs_w, cs_h, CAR_R - CAR_BEZEL * 0.6)}" fill="url(#screen)"/>')
    gap_car = cs_h * GAP_FRAC * 1.25
    wside = cs_h - 2 * gap_car
    wside = min(wside, cell)
    add('<g clip-path="url(#carScreen)">')
    tx = cs_x + gap_car + wside + gap_car
    add(f'<path d="{rrect(tx, cs_y + gap_car, cs_x + cs_w - gap_car - tx, wside * 0.46, 18)}" fill="{TILE_A}"/>')
    add(f'<path d="{rrect(tx, cs_y + gap_car + wside * 0.54, (cs_x + cs_w - gap_car - tx) * 0.62, wside * 0.46, 18)}" fill="{TILE_B}"/>')
    add('</g>')
    add(widget(cs_x + gap_car, cs_y + gap_car, wside, "glowB"))
    add('</g>')

    # ------------------------------------------------------------ highlight
    add('<g id="highlight">')
    glare_home = (f'M{hs_x + hs_w * 0.55:.1f},{hs_y:.1f} L{hs_x + hs_w * 0.85:.1f},{hs_y:.1f} '
                  f'L{hs_x + hs_w * 0.35:.1f},{hs_y + hs_w:.1f} L{hs_x + hs_w * 0.05:.1f},{hs_y + hs_w:.1f} Z')
    add(f'<path d="{glare_home}" fill="{GLINT}" fill-opacity="0.16" filter="url(#soft)" clip-path="url(#homeScreen)"/>')
    glare_car = (f'M{cs_x + cs_w * 0.62:.1f},{cs_y:.1f} L{cs_x + cs_w * 0.80:.1f},{cs_y:.1f} '
                 f'L{cs_x + cs_w * 0.66:.1f},{cs_y + cs_h:.1f} L{cs_x + cs_w * 0.48:.1f},{cs_y + cs_h:.1f} Z')
    add(f'<path d="{glare_car}" fill="{GLINT}" fill-opacity="0.18" filter="url(#soft)" clip-path="url(#carScreen)"/>')
    add('</g>')

    add('</g>')
    add('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    svg = build()
    (HERE / "icon.svg").write_text(svg)
    (HERE / "icon-engineA-handauthored.svg").write_text(svg)
    print(f"wrote {HERE / 'icon.svg'} and the Engine A alternate")
