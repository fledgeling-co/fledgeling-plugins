#!/usr/bin/env python3
"""Build the design-craft icon master.

Geometry and material live here as named constants so a revision is a parameter
edit rather than path surgery.

Metaphor: the contrast step wedge — a prepress test strip lying at an angle on
the porcelain bench, its patches poured as one contiguous run of thick grey gel
into a channel machined across the tile. The steps are steps in density, not in
height, so the run is a single unbroken bar of equal patches and the eye reads
the ramp as calibration rather than as a chart.

One patch is not there, and the slot it should have filled is cut clean through
the tile. What the eye sees in it is the bench, which is why it reads as nothing
rather than as a paler patch: only the occlusion of a real cut edge is painted
into it, the neighbouring patch throws its shadow across it, and the run closes
again on the far side. Beside that hole, and nowhere else in the icon, one narrow
vermilion band marks it. That is the skill: naming what it could not measure
instead of reporting a clean sheet.

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

# ---- the strip: a run of equal patches, so density is the only thing stepping.
#      The empty slot is cut clean through the tile, so what shows in it is the
#      bench — which is why it reads as nothing rather than as a paler patch. It
#      sits where the second-darkest patch belongs, bracketed by the darkest
#      patch of all and by the marker, so local contrast is at its highest there.
BAND_W = 134
BAND_H = 300
BAND_R = 15
MARK_W = 56
SEAT_SLOT = 2
MARK_SLOT = 3
BANDS = ("#B4B0A6", "#6E7175", None, "accent", "#1F2328")

# ---- the porcelain tile the strip is cut into
TILE_PAD = 30
TILE_R = 46
TILE_HI = "#FCF9F3"
TILE_LO = "#E1DBCE"
TILE_EDGE = "#BEB5A2"
TILT = -4              # the strip lies on the bench, it is not mounted square

# ---- the channel the patches are poured into, and the slot cut through it
CHAN_R = 20
CHAN_HI = "#EFEAE0"
CHAN_LO = "#B9B0A0"
SEAT_R = 12
# A slot cut through a slab under a top-left key leaves its top and left inner
# walls back-facing and its bottom and right walls lit, so the occlusion is two
# bands rather than one diagonal wash.
SEAT_DEPTH = 0.32      # ambient inside the slot
SEAT_LIP = 50          # how far the shaded top wall reaches in
SEAT_WALL = 46         # how far the shaded left wall reaches in

# ---- accent (one warm hue; ACCENT_LO is the same hue kept saturated in shadow,
#      because a gel that goes brown where it turns away reads opaque)
ACCENT = "#E8542A"
ACCENT_HI = "#F4794A"
ACCENT_LO = "#C63C15"

# ---- material
SHEEN_H = 26           # the soft top-edge sheen along each patch
FOOT_H = 26            # ambient occlusion where a patch meets the channel floor


def rounded(x, y, w, h, r):
    return (f'M{x + r},{y} h{w - 2 * r} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r} '
            f'a{r},{r} 0 0 1 {-r},{r} h{-(w - 2 * r)} a{r},{r} 0 0 1 {-r},{-r} '
            f'v{-(h - 2 * r)} a{r},{r} 0 0 1 {r},{-r} z')


def mix(a, b, t):
    """Blend two hex colours; each patch derives its own lit and shaded ends."""
    ah, bh = a.lstrip("#"), b.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        ca, cb = int(ah[i:i + 2], 16), int(bh[i:i + 2], 16)
        ch.append(round(ca + (cb - ca) * t))
    return "#%02X%02X%02X" % tuple(ch)


def build() -> str:
    widths = [MARK_W if i == MARK_SLOT else BAND_W for i in range(len(BANDS))]
    run_w = sum(widths)
    tile_w = run_w + 2 * TILE_PAD
    tile_h = BAND_H + 2 * TILE_PAD
    tile_x = (S - tile_w) // 2
    tile_y = (S - tile_h) // 2
    run_x = tile_x + TILE_PAD
    run_y = tile_y + TILE_PAD
    present = [i for i, c in enumerate(BANDS) if c is not None]

    def slot_x(i):
        return run_x + sum(widths[:i])

    # A patch tucks under its right-hand neighbour by one corner radius, so the
    # run fuses into one bar. The patch beside the seat keeps its own corners —
    # that edge is a real cut face looking into the hole.
    def band_path(i, fused=False):
        w = widths[i] + (BAND_R if fused and (i + 1) in present else 0)
        return rounded(slot_x(i), run_y, w, BAND_H, BAND_R)

    seat_x = slot_x(SEAT_SLOT)
    tile = rounded(tile_x, tile_y, tile_w, tile_h, TILE_R)
    chan = rounded(run_x, run_y, run_w, BAND_H, CHAN_R)
    hole = rounded(seat_x, run_y, BAND_W, BAND_H, SEAT_R)

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
    add(f'''<linearGradient id="tile" x1="0.06" y1="0" x2="0.88" y2="1">
      <stop offset="0" stop-color="{TILE_HI}"/>
      <stop offset="0.55" stop-color="#F0EBE1"/>
      <stop offset="1" stop-color="{TILE_LO}"/>
    </linearGradient>''')
    # the channel is concave: shaded where the key enters, lit on the far wall
    add(f'''<linearGradient id="chan" x1="0.06" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="{CHAN_LO}"/>
      <stop offset="0.55" stop-color="{CHAN_HI}"/>
      <stop offset="1" stop-color="#FBF8F2"/>
    </linearGradient>''')
    # one soft key from the top-left: every raised rim reads off this
    add('''<linearGradient id="rim" x1="0" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.15"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>''')
    # a cut edge runs the other way: the lip the light enters over is occluded
    add(f'''<linearGradient id="cut" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.44"/>
      <stop offset="0.55" stop-color="{SHADOW}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.6"/>
    </linearGradient>''')
    add(f'''<linearGradient id="hollow" x1="0.05" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="{SEAT_DEPTH}"/>
      <stop offset="0.5" stop-color="{SHADOW}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0.02"/>
    </linearGradient>''')
    add(f'''<linearGradient id="wall" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.46"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0.40"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </linearGradient>''')
    add('''<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.44"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>''')
    add(f'''<linearGradient id="foot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0.34"/>
    </linearGradient>''')
    add(f'''<linearGradient id="accent" x1="0" y1="0" x2="0.5" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset="0.5" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_LO}"/>
    </linearGradient>''')
    add(f'''<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.34"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>''')
    # a per-patch face gradient, lit top-left, shaded bottom-right
    for i, c in enumerate(BANDS):
        if c is None or c == "accent":
            continue
        add(f'''<linearGradient id="face{i}" x1="0.05" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{mix(c, "#FFFFFF", 0.28)}"/>
      <stop offset="0.5" stop-color="{c}"/>
      <stop offset="1" stop-color="{mix(c, SHADOW, 0.28)}"/>
    </linearGradient>''')
    add(f'''<filter id="tileshadow" x="-25%" y="-40%" width="150%" height="200%">
      <feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="{SHADOW}"
                    flood-opacity="0.32"/>
    </filter>''')
    add(f'''<filter id="runshadow" x="-25%" y="-40%" width="150%" height="200%">
      <feDropShadow dx="7" dy="11" stdDeviation="9" flood-color="{SHADOW}"
                    flood-opacity="0.34"/>
    </filter>''')
    add('''<filter id="softglow" x="-90%" y="-70%" width="280%" height="240%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>''')
    add(f'<clipPath id="holeclip"><path d="{hole}"/></clipPath>')
    for i in present:
        add(f'<clipPath id="band{i}"><path d="'
            f'{rounded(slot_x(i), run_y, widths[i], BAND_H, BAND_R)}"/></clipPath>')
    sq = SQUIRCLE.read_text().strip()
    add(f'<clipPath id="squircle"><path d="{sq}"/></clipPath>')
    add('</defs>')

    # Everything lives inside the family squircle — one silhouette across the set.
    add('<g clip-path="url(#squircle)">')

    # ---------------- ground: a cushion, not a print
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<path d="{sq}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" '
        f'stroke-width="7"/>')

    # the strip lies on the bench rather than being mounted square to it
    add(f'<g transform="rotate({TILT} {S // 2} {S // 2})">')

    # ---------------- the porcelain tile, cut clean through at the empty slot
    add('<g filter="url(#tileshadow)">')
    add(f'<path d="{tile} {hole}" fill-rule="evenodd" fill="url(#tile)"/>')
    add('</g>')
    add(f'<path d="{tile}" fill="none" stroke="{TILE_EDGE}" stroke-opacity="0.5" '
        f'stroke-width="2"/>')
    add(f'<path d="{tile}" fill="none" stroke="url(#rim)" stroke-width="4"/>')

    # ---------------- the channel, and the slot that goes right through it
    add(f'<path d="{chan} {hole}" fill-rule="evenodd" fill="url(#chan)"/>')
    add(f'<path d="{chan}" fill="none" stroke="url(#cut)" stroke-width="5"/>')
    # nothing is painted into the slot but the occlusion a real cut edge carries,
    # so what the eye sees through it is the bench
    add('<g clip-path="url(#holeclip)">')
    add(f'<path d="{hole}" fill="url(#hollow)"/>')
    add(f'<rect x="{seat_x}" y="{run_y}" width="{BAND_W}" height="{SEAT_LIP}" '
        f'fill="url(#lip)"/>')
    add(f'<rect x="{seat_x}" y="{run_y}" width="{SEAT_WALL}" height="{BAND_H}" '
        f'fill="url(#wall)"/>')
    add('</g>')
    add(f'<path d="{hole}" fill="none" stroke="url(#cut)" stroke-width="5"/>')

    # ---------------- the run of patches, cast as one bar so the gap is a hole
    mx = slot_x(MARK_SLOT)
    add(f'<ellipse cx="{mx + MARK_W / 2}" cy="{run_y + BAND_H / 2}" '
        f'rx="{MARK_W * 2.2}" ry="{BAND_H * 0.72}" fill="url(#glow)" '
        f'filter="url(#softglow)"/>')

    add('<g filter="url(#runshadow)">')
    for i in present:
        fill = "accent" if BANDS[i] == "accent" else f"face{i}"
        add(f'<path d="{band_path(i, fused=True)}" fill="url(#{fill})"/>')
    add('</g>')

    # material pass, left to right so each seam's arris stays clean
    for i in present:
        x, w = slot_x(i), widths[i]
        add(f'<g clip-path="url(#band{i})">')
        # soft top-edge sheen: thick gel, one key light, no hard specular
        add(f'<rect x="{x}" y="{run_y}" width="{w}" height="{SHEEN_H}" fill="url(#sheen)"/>')
        # ambient occlusion where the patch meets the channel floor
        add(f'<rect x="{x}" y="{run_y + BAND_H - FOOT_H}" width="{w}" height="{FOOT_H}" '
            f'fill="url(#foot)"/>')
        add('</g>')
        add(f'<path d="{rounded(x, run_y, w, BAND_H, BAND_R)}" fill="none" '
            f'stroke="url(#rim)" stroke-width="3"/>')

    add('</g>')  # tilt
    add('</g>')  # squircle
    add('</svg>')
    return "\n".join(parts)


if __name__ == "__main__":
    out = HERE / "icon-src.svg"
    out.write_text(build())
    print(f"wrote {out}")
