#!/usr/bin/env python3
"""Build the career-kit icon master.

Geometry and material live here as named constants, so a later change is a parameter edit
rather than path surgery.

    python3 build_icon.py            # writes icon.svg (the master) and icon-engineA-handauthored.svg

THE SUBJECT: "The ladder is the page"
-------------------------------------
A ladder standing on the porcelain bench, drawn straight on with a slight taper. Its rungs are
also the ruled lines of a résumé: two rails for the page's edges, five rungs for its lines.

SIGNATURE MOVE: one rung is ember. It is the current role, the line the document is written
around, and the only warm colour in the tile. The research this plugin ships found that twenty
years at one employer should read as a promotion ladder with each role dated separately; the
icon is that sentence.

MEASURED VALUES
---------------
Ground ramp, vignette, contact shadow, body darks and accent are the fledgeling family's, lifted
unchanged from plugins/home-craft/assets/build_icon.py (measured there against create-mac-icon's
apple-2026 corpus). Sampled again for this commission at 128px from apple-12, apple-23, apple-26
and apple-18: the darkest object pixel sits at L 0.08 to 0.10 and is faintly cool (19,23,26),
and the porcelain-register medians sit at L 0.85 to 0.94. The corpus darks are cool where the
family's are warm; the family wins for shelf consistency.

MATERIAL, FROM THE RASTER TAKE
------------------------------
The raster take (icon-engineC-raster-*.png) drew the rails and rungs as lit tubes: a bright
shoulder a quarter of the way across, a shaded belly, and the shadow pooled at the right foot.
Those three things were rebuilt here as gradient stops and one pool ellipse. They were matched
by eye. The fidelity scorer could not measure material on this machine (torch is not
installed), so no score stands behind the match.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / ".." / ".." / "create-mac-icon" / "skills" / "create-mac-icon" / "assets" / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- geometry
TOP_Y, BOT_Y = 150.0, 850.0          # where the rails start and stand
TOP_HALF, BOT_HALF = 172.0, 236.0    # half the distance between rail centres, top and bottom
CX = 512.0                           # the ladder's axis; the glyph is optically centred on it
RAIL_W = 62.0                        # rail thickness
RAIL_R = 31.0                        # rail end radius (fully rounded)
RUNGS = 5                            # lines on the page
RUNG_H = 50.0                        # rung thickness
RUNG_FIRST, RUNG_LAST = 0.14, 0.86   # first and last rung as a fraction of the rail length
EMBER_RUNG = 1                       # 0 is the top rung; the ember one is second from the top
RUNG_INSET = 6.0                     # how far a rung tucks under each rail
SHADOW_DX, SHADOW_DY = 44.0, 30.0    # the cast shadow on the bench, down and right
FLANK = 18.0                         # body depth, extruded down and slightly right
FLANK_DX = 6.0

# ---------------------------------------------------------------- palette
GROUND_HI = "#FDFCF9"
GROUND_MID = "#F3EFE7"
GROUND_LO = "#E7E1D5"
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"
POOL = "#B7AA90"
SEAT_DARK = "#5E4F3A"

RAIL_HI, RAIL_FACE, RAIL_LO = "#8C7D70", "#4F453D", "#27211D"   # a lit tube: bright left shoulder, dark right
RAIL_FLANK = "#25201C"
RUNG_HI, RUNG_FACE, RUNG_LO = "#DDD4C7", "#B0A28F", "#746656"   # warm taupe tube: lit top, shaded belly
RUNG_FLANK = "#4A4037"
ACCENT = "#E9562A"
ACCENT_HI = "#F58A5E"
ACCENT_LO = "#B93F1B"
GLINT = "#FFFFFF"


def half_at(t):
    """Half-distance between rail centres at fraction t down the ladder."""
    return TOP_HALF + (BOT_HALF - TOP_HALF) * t


def y_at(t):
    return TOP_Y + (BOT_Y - TOP_Y) * t


def rail(side, dx=0.0, dy=0.0):
    """One rail as a tapered capsule. side is -1 for left, +1 for right."""
    xt, xb = CX + side * TOP_HALF + dx, CX + side * BOT_HALF + dx
    yt, yb = TOP_Y + dy, BOT_Y + dy
    h = RAIL_W / 2
    return (f'M{xt - h:.1f},{yt:.1f} A{h:.1f},{h:.1f} 0 0 1 {xt + h:.1f},{yt:.1f} '
            f'L{xb + h:.1f},{yb:.1f} A{h:.1f},{h:.1f} 0 0 1 {xb - h:.1f},{yb:.1f} Z')


def rung(i, dx=0.0, dy=0.0, grow=0.0):
    """Rung i as a rounded bar spanning between the rails' inner faces."""
    t = RUNG_FIRST + (RUNG_LAST - RUNG_FIRST) * i / (RUNGS - 1)
    y = y_at(t) + dy
    half = half_at(t) - RAIL_W / 2 + RUNG_INSET + grow
    x0, x1 = CX - half + dx, CX + half + dx
    r = RUNG_H / 2 + grow
    return (f'M{x0 + r:.1f},{y - r:.1f} H{x1 - r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x1 - r:.1f},{y + r:.1f} '
            f'H{x0 + r:.1f} A{r:.1f},{r:.1f} 0 0 1 {x0 + r:.1f},{y - r:.1f} Z'), y, x0, x1


def swept(path_fn, fill):
    """A shape swept down and right by FLANK, so rounded ends stay round."""
    return "".join(f'<path d="{path_fn(FLANK_DX * k / FLANK, k)}" fill="{fill}"/>'
                   for k in range(2, int(FLANK) + 1, 2))


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
    add(f'''<linearGradient id="railL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{RAIL_FACE}"/><stop offset="0.24" stop-color="{RAIL_HI}"/>
      <stop offset="0.58" stop-color="{RAIL_FACE}"/>
      <stop offset="1" stop-color="{RAIL_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="rung" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{RUNG_FACE}"/><stop offset="0.22" stop-color="{RUNG_HI}"/>
      <stop offset="0.6" stop-color="{RUNG_FACE}"/>
      <stop offset="1" stop-color="{RUNG_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="ember" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ACCENT}"/><stop offset="0.24" stop-color="{ACCENT_HI}"/>
      <stop offset="0.6" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_LO}"/></linearGradient>''')
    add('<filter id="pool" x="-35%" y="-35%" width="170%" height="170%"><feGaussianBlur stdDeviation="30"/></filter>')
    add('<filter id="cast" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter>')
    add('<filter id="seat" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="8"/></filter>')
    add('<filter id="glow" x="-30%" y="-150%" width="160%" height="400%"><feGaussianBlur stdDeviation="20"/></filter>')
    add('<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5"/></filter>')
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    add('</defs>')

    add('<g clip-path="url(#tile)">')
    # ------------------------------------------------------------ bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<path d="{sq}" fill="none" stroke="{RIM_TILE}" stroke-width="7" stroke-opacity="0.55"/>')
    add('</g>')

    # ------------------------------------------------------------ mid: shadows, then rungs
    add('<g id="mid">')
    # the cast shadow of the whole ladder on the bench, down and right
    add(f'<g filter="url(#cast)" fill="{POOL}" fill-opacity="0.50">')
    for side in (-1, 1):
        add(f'<path d="{rail(side, SHADOW_DX, SHADOW_DY)}"/>')
    for i in range(RUNGS):
        d, _, _, _ = rung(i, SHADOW_DX, SHADOW_DY)
        add(f'<path d="{d}"/>')
    add('</g>')
    add(f'<ellipse cx="{CX + BOT_HALF + 70:.1f}" cy="{BOT_Y + 26:.1f}" rx="150" ry="34" fill="{POOL}" '
        f'fill-opacity="0.55" filter="url(#pool)"/>')
    # contact seats where the two feet stand
    for side in (-1, 1):
        fx = CX + side * BOT_HALF
        add(f'<ellipse cx="{fx + 10:.1f}" cy="{BOT_Y + RAIL_W / 2 + 6:.1f}" rx="66" ry="15" fill="{SEAT_DARK}" '
            f'fill-opacity="0.55" filter="url(#seat)"/>')
    # rungs: flank, face, lit top edge. The ember rung is drawn in fg.
    for i in range(RUNGS):
        if i == EMBER_RUNG:
            continue
        add(swept(lambda dx, dy, i=i: rung(i, dx, dy)[0], RUNG_FLANK))
        d, y, x0, x1 = rung(i)
        add(f'<path d="{d}" fill="url(#rung)"/>')
        add(f'<path d="M{x0 + 34:.1f},{y - RUNG_H / 2 + 9:.1f} H{x1 - 34:.1f}" stroke="{GLINT}" stroke-width="5" '
            f'stroke-opacity="0.45" stroke-linecap="round" filter="url(#soft)"/>')
    add('</g>')

    # ------------------------------------------------------------ fg: the ember rung, then the rails over it
    add('<g id="fg">')
    d_glow, y, x0, x1 = rung(EMBER_RUNG, 0, 6, 10)
    add(f'<path d="{d_glow}" fill="{ACCENT}" fill-opacity="0.55" filter="url(#glow)"/>')
    add(swept(lambda dx, dy: rung(EMBER_RUNG, dx, dy, 3)[0], ACCENT_LO))
    d, y, x0, x1 = rung(EMBER_RUNG, 0, 0, 3)
    add(f'<path d="{d}" fill="url(#ember)"/>')
    for side in (-1, 1):
        add(swept(lambda dx, dy, side=side: rail(side, dx, dy), RAIL_FLANK))
        add(f'<path d="{rail(side)}" fill="url(#railL)"/>')
    add('</g>')

    # ------------------------------------------------------------ highlight
    add('<g id="highlight">')
    add(f'<path d="M{x0 + 38:.1f},{y - RUNG_H / 2 + 8:.1f} H{x1 - 38:.1f}" stroke="{GLINT}" stroke-width="6" '
        f'stroke-opacity="0.55" stroke-linecap="round" filter="url(#soft)"/>')
    for side in (-1, 1):
        xt, xb = CX + side * TOP_HALF - RAIL_W * 0.24, CX + side * BOT_HALF - RAIL_W * 0.24
        add(f'<path d="M{xt:.1f},{TOP_Y + 4:.1f} L{xb:.1f},{BOT_Y - 4:.1f}" stroke="{GLINT}" stroke-width="7" '
            f'stroke-opacity="0.22" stroke-linecap="round" filter="url(#soft)"/>')
    add('</g>')

    add('</g>')
    add('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    svg = build()
    (HERE / "icon.svg").write_text(svg)
    (HERE / "icon-engineA-handauthored.svg").write_text(svg)
    print(f"wrote {HERE / 'icon.svg'} and the Engine A alternate")
