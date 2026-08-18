#!/usr/bin/env python3
"""
build_icon.py — Engine A: the hand-authored layered SVG master for be-my-witness.

Geometry and material are named constants and the script emits the SVG, so a
fidelity round is a parameter edit rather than path surgery. That is the whole
reason this is a script and not a hand-written .svg file.

DEVICE  A witness's loupe laid on a plane of evidence. The lattice outside the
        glass is soft and unjudged; under the glass it resolves AND steps up in
        scale, so the lens is visibly doing work rather than sitting on a decal.
        Exactly one cell in the resolved region has slipped off its gridline: the
        chip is drawn in ember where it actually is, with a faint outline still
        showing where it was expected. That single warm mark is the verdict — the
        one difference the witness caught — and it is the only chroma in the tile.

        Subject-mining: device #20 (data-as-glyph with one accent datum, à la
        Calendar's single red "today" dot; Safari's needle runs 1.77% of the tile
        at S 0.96, measured off corpus/apple-2026/apple-23.png) crossed with #16
        (the composition performs the verb).

        Kept clear of design-review, whose device is glass panels plus a crosshair
        reticle: that icon sights a target, this one examines evidence. At 32px
        one reads as stacked rectangles with a cross, the other as a knurled ring
        with a warm pip.

REGISTER  Tahoe gel-glass, sub-register (a): porcelain cushion carrying one lit
          object. Ground lifted from the fledgeling family rather than invented —
          #F9F5EE -> #DED7C5 is the warm porcelain 20-odd siblings share (measured
          off whats-left, test-campaign, clarify, proctor), with the ember
          accent kin to Fledgeling's #C4622D. Corpus values sampled from
          apple-23 (Safari: porcelain #FFFFFF -> #DFE3EB, L 1.000 -> 0.898, one
          high-chroma warm accent at 1.77% of the tile on an otherwise cool
          instrument) and apple-27 (Preview: knurled loupe barrel, glass showing
          the ground through it).

          Two hue families: warm neutral (porcelain, graphite barrel, milled
          metal, lattice ink) and the ember accent. The glass is held at S <= 0.14
          so frost reads as frost without becoming a third family.

          The previous master was a periwinkle-to-violet ground with no accent at
          all — the only icon in the marketplace at 0.0% warm pixels, with 77% of
          its pixels in the cold 180-285 band. The lens device and its material
          survived that re-ground; the palette did not.

DECORATIVE, NOT PRODUCTION. This ships as a PNG in a marketplace README, so the
material lives in the file. Do NOT strip the gradients and shadows for Icon
Composer rules; nothing downstream would put them back.

USAGE   python3 build_icon.py > icon.svg
"""
from __future__ import annotations

import math

S = 1024                      # canvas
CX, CY = 512, 484             # optical centre, nudged up: the barrel carries weight low

# ── palette ───────────────────────────────────────────────────────────────────
GROUND_TOP  = "#F9F5EE"       # porcelain cushion, brightest under the key
GROUND_MID  = "#F1EBDF"
GROUND_BOT  = "#DED7C5"
LENS_PLANE  = "#FBF7F0"       # the plane as the glass resolves it — still warm
TILE_RIM    = "#FFFDF8"       # inner rim light on the squircle
VIGNETTE    = "#8A7A62"       # warm edge darkening, never grey

GRID_SOFT   = "#B9AE97"       # the plane before it is looked at
GRID_INK    = "#4A4234"       # the same plane, resolved under the glass
GRID_FINE   = "#8E8674"       # sub-division ticks, resolved only

BARREL_HI   = "#6E5F4E"       # graphite cylinder, warm-neutral not navy
BARREL_MID  = "#3E342A"
BARREL_LO   = "#221B14"
KNURL_HI    = "#8A7C67"       # milled metal, lit from upper-left. Swept, not
KNURL_MID   = "#3C352C"       #   chosen: on the family's p90:p10 luminance measure
KNURL_LO    = "#14100C"       #   a pale rim put this icon at 1.44:1 against a
                              #   34-icon median of 1.65:1 — below-median figure-
                              #   ground on the one register where the object has to
                              #   carry it. Four settings were measured; warm
                              #   gunmetal plus a wider bezel took it to 2.37:1 and
                              #   the 16px contrast statistic from 0.314 to 0.502
                              #   (family median 0.344). Curve in audit.html.
BEZEL       = "#2B231B"       # the dark annulus between knurl and glass
CATCH_OUT   = "#F6EFE0"       # annulus edge catch (material-recipes, mac-doctor)
CATCH_IN    = "#A89C88"

GLASS_HI    = "#FDFEFF"       # frost: neutral, faintly cool, low saturation
GLASS_MID   = "#E4E8EC"
GLASS_LO    = "#C2C9D1"

ACCENT_HI   = "#F0854F"       # the caught difference — the only chroma
ACCENT      = "#DA5526"
ACCENT_LO   = "#A93E16"
GHOST       = "#C4622D"       # where the cell was expected to be

SHADOW      = "#4A3A22"       # warm shadow; a blue shadow in a warm scene is the
                              # material failure this skill has recorded most often

# ── geometry ──────────────────────────────────────────────────────────────────
R_OUTER  = 300                # knurled rim outer radius -> 59% of tile width
R_KNURL  = 266                # inner edge of the milled band
R_BEZEL  = 258                # inner edge of the dark bezel
R_LENS   = 230                # the glass
NOTCHES  = 88                 # milled teeth: FINE. At 36 with long teeth this read
                              # as a gear, which is a different object entirely.

PLANE_TILT = -5.5             # the evidence plane is laid, not printed
SP_OUT     = 84.0             # unresolved lattice pitch
SP_IN      = 132.0            # resolved lattice pitch -> 1.57x, the magnification
FINE_DIV   = 4                # sub-division ticks inside the glass

CELL_GX    = 0.55             # caught cell's expected centre, in inner-cell units
CELL_GY    = 0.34             #   from the lens centre
CELL_DX    = 0.245            # how far it slipped, in the same units
CELL_DY    = 0.205
CELL_W     = SP_IN * 0.80     # the chip: a cell-sized tile, not a dot
CELL_H     = SP_IN * 0.62
CELL_R     = 22               # chip corner radius


def notch_ring(cx: float, cy: float, r_in: float, r_out: float, n: int) -> str:
    """The milled edge. Trapezoids rather than rects so the teeth taper like real
    knurling; at 16px this collapses to a clean circle, which is the point.

    Milled INTO the band (r_out inside R_OUTER): teeth that overhang the rim read
    as fringe along the lower-right silhouette, where nothing lights them."""
    out = []
    for i in range(n):
        a0 = (i + 0.28) * 2 * math.pi / n
        a1 = (i + 0.72) * 2 * math.pi / n
        p = []
        for r, a in ((r_in, a0), (r_out, a0 + 0.006), (r_out, a1 - 0.006), (r_in, a1)):
            p.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
        out.append(f'<polygon points="{" ".join(p)}" fill="url(#milled)" opacity=".93"/>')
    return "\n        ".join(out)


def lattice(spacing: float, stroke: str, width: float, opacity: str,
            reach: float = 760.0, filt: str | None = None) -> str:
    """The lattice, drawn about the lens centre so both scales share an origin —
    that is what makes the step in pitch at the glass edge read as magnification
    rather than as two unrelated grids."""
    lines = []
    k = int(reach / spacing) + 2
    for i in range(-k, k + 1):
        v = (i + 0.5) * spacing                       # half-offset: the lens centre
        lines.append(f'<path d="M{CX + v:.1f} {CY - reach:.0f} '                # sits in a
                     f'L{CX + v:.1f} {CY + reach:.0f}"/>')                      # cell, not
        lines.append(f'<path d="M{CX - reach:.0f} {CY + v:.1f} '                # on a
                     f'L{CX + reach:.0f} {CY + v:.1f}"/>')                      # crossing
    f = f' filter="url(#{filt})"' if filt else ""
    return (f'<g stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" '
            f'fill="none" stroke-linecap="square"{f}>\n        '
            + "\n        ".join(lines) + "\n      </g>")


# The expected cell centre, and where the cell actually landed.
GX = CX + CELL_GX * SP_IN
GY = CY + CELL_GY * SP_IN
AX = GX + CELL_DX * SP_IN
AY = GY + CELL_DY * SP_IN

SQUIRCLE = ("M1024.00,512.00C1024.00,569.33 1023.85,646.20 1023.56,683.99C1023.27,721.78 "
            "1022.83,723.03 1022.24,738.75C1021.66,754.47 1020.92,766.39 1020.04,778.30C1019.16,"
            "790.20 1018.13,800.36 1016.95,810.17C1015.77,819.99 1014.44,828.75 1012.95,837.17C"
            "1011.47,845.58 1009.83,853.28 1008.04,860.66C1006.25,868.04 1004.30,874.89 1002.19,"
            "881.45C1000.08,888.01 997.81,894.14 995.37,900.02C992.94,905.90 990.34,911.43 "
            "987.56,916.73C984.79,922.03 981.85,927.02 978.72,931.81C975.59,936.59 972.29,941.11 "
            "968.79,945.43C965.29,949.75 961.62,953.83 957.72,957.72C953.83,961.62 949.75,965.29 "
            "945.43,968.79C941.11,972.29 936.59,975.59 931.81,978.72C927.02,981.85 922.03,984.79 "
            "916.73,987.56C911.43,990.34 905.90,992.94 900.02,995.37C894.14,997.81 888.01,1000.08 "
            "881.45,1002.19C874.89,1004.30 868.04,1006.25 860.66,1008.04C853.28,1009.83 845.58,"
            "1011.47 837.17,1012.95C828.75,1014.44 819.99,1015.77 810.17,1016.95C800.36,1018.13 "
            "790.20,1019.16 778.30,1020.04C766.39,1020.92 754.47,1021.66 738.75,1022.24C723.03,"
            "1022.83 721.78,1023.27 683.99,1023.56C646.20,1023.85 569.33,1024.00 512.00,1024.00C"
            "454.67,1024.00 377.80,1023.85 340.01,1023.56C302.22,1023.27 300.97,1022.83 285.25,"
            "1022.24C269.53,1021.66 257.61,1020.92 245.70,1020.04C233.80,1019.16 223.64,1018.13 "
            "213.83,1016.95C204.01,1015.77 195.25,1014.44 186.83,1012.95C178.42,1011.47 170.72,"
            "1009.83 163.34,1008.04C155.96,1006.25 149.11,1004.30 142.55,1002.19C135.99,1000.08 "
            "129.86,997.81 123.98,995.37C118.10,992.94 112.57,990.34 107.27,987.56C101.97,984.79 "
            "96.98,981.85 92.19,978.72C87.41,975.59 82.89,972.29 78.57,968.79C74.25,965.29 "
            "70.17,961.62 66.28,957.72C62.38,953.83 58.71,949.75 55.21,945.43C51.71,941.11 "
            "48.41,936.59 45.28,931.81C42.15,927.02 39.21,922.03 36.44,916.73C33.66,911.43 "
            "31.06,905.90 28.63,900.02C26.19,894.14 23.92,888.01 21.81,881.45C19.70,874.89 "
            "17.75,868.04 15.96,860.66C14.17,853.28 12.53,845.58 11.05,837.17C9.56,828.75 "
            "8.23,819.99 7.05,810.17C5.87,800.36 4.84,790.20 3.96,778.30C3.08,766.39 2.34,754.47 "
            "1.76,738.75C1.17,723.03 0.73,721.78 0.44,683.99C0.15,646.20 0.00,569.33 0.00,512.00C"
            "0.00,454.67 0.15,377.80 0.44,340.01C0.73,302.22 1.17,300.97 1.76,285.25C2.34,269.53 "
            "3.08,257.61 3.96,245.70C4.84,233.80 5.87,223.64 7.05,213.83C8.23,204.01 9.56,195.25 "
            "11.05,186.83C12.53,178.42 14.17,170.72 15.96,163.34C17.75,155.96 19.70,149.11 "
            "21.81,142.55C23.92,135.99 26.19,129.86 28.63,123.98C31.06,118.10 33.66,112.57 "
            "36.44,107.27C39.21,101.97 42.15,96.98 45.28,92.19C48.41,87.41 51.71,82.89 55.21,"
            "78.57C58.71,74.25 62.38,70.17 66.28,66.28C70.17,62.38 74.25,58.71 78.57,55.21C"
            "82.89,51.71 87.41,48.41 92.19,45.28C96.98,42.15 101.97,39.21 107.27,36.44C112.57,"
            "33.66 118.10,31.06 123.98,28.63C129.86,26.19 135.99,23.92 142.55,21.81C149.11,19.70 "
            "155.96,17.75 163.34,15.96C170.72,14.17 178.42,12.53 186.83,11.05C195.25,9.56 "
            "204.01,8.23 213.83,7.05C223.64,5.87 233.80,4.84 245.70,3.96C257.61,3.08 269.53,2.34 "
            "285.25,1.76C300.97,1.17 302.22,0.73 340.01,0.44C377.80,0.15 454.67,0.00 512.00,0.00C"
            "569.33,0.00 646.20,0.15 683.99,0.44C721.78,0.73 723.03,1.17 738.75,1.76C754.47,2.34 "
            "766.39,3.08 778.30,3.96C790.20,4.84 800.36,5.87 810.17,7.05C819.99,8.23 828.75,9.56 "
            "837.17,11.05C845.58,12.53 853.28,14.17 860.66,15.96C868.04,17.75 874.89,19.70 "
            "881.45,21.81C888.01,23.92 894.14,26.19 900.02,28.63C905.90,31.06 911.43,33.66 "
            "916.73,36.44C922.03,39.21 927.02,42.15 931.81,45.28C936.59,48.41 941.11,51.71 "
            "945.43,55.21C949.75,58.71 953.83,62.38 957.72,66.28C961.62,70.17 965.29,74.25 "
            "968.79,78.57C972.29,82.89 975.59,87.41 978.72,92.19C981.85,96.98 984.79,101.97 "
            "987.56,107.27C990.34,112.57 992.94,118.10 995.37,123.98C997.81,129.86 1000.08,"
            "135.99 1002.19,142.55C1004.30,149.11 1006.25,155.96 1008.04,163.34C1009.83,170.72 "
            "1011.47,178.42 1012.95,186.83C1014.44,195.25 1015.77,204.01 1016.95,213.83C1018.13,"
            "223.64 1019.16,233.80 1020.04,245.70C1020.92,257.61 1021.66,269.53 1022.24,285.25C"
            "1022.83,300.97 1023.27,302.22 1023.56,340.01C1023.85,377.80 1024.00,454.67 "
            "1024.00,512.00Z")

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <title>be-my-witness</title>
  <desc>A witness's loupe on a plane of evidence; under the glass the lattice resolves and
one cell has slipped off its gridline, marked in ember with its expected position ghosted.</desc>
  <defs>
    <!-- Porcelain cushion. Range and falloff sampled off corpus apple-23 (Safari):
         L 1.000 at the key down to 0.898 at the far edge, saturation under 0.10. -->
    <linearGradient id="ground" x1="0" y1="0" x2="0.18" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".54" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>

    <!-- One soft key, upper-left. Zero hard speculars anywhere in the tile. -->
    <radialGradient id="key" cx=".26" cy=".16" r=".92">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".62"/>
      <stop offset=".48" stop-color="#FFFFFF" stop-opacity=".14"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <!-- Warm edge vignette. A grey vignette on warm porcelain reads as dirt. -->
    <radialGradient id="vignette" cx=".5" cy=".46" r=".76">
      <stop offset=".52" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset=".84" stop-color="{VIGNETTE}" stop-opacity=".10"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".26"/>
    </radialGradient>

    <linearGradient id="barrel" x1=".16" y1="0" x2=".88" y2="1">
      <stop offset="0" stop-color="{BARREL_HI}"/>
      <stop offset=".42" stop-color="{BARREL_MID}"/>
      <stop offset="1" stop-color="{BARREL_LO}"/>
    </linearGradient>

    <!-- Milled metal: non-monotonic so the band carries local highlight geometry
         rather than one sweep (material-recipes, metallic accent). -->
    <linearGradient id="milled" x1=".08" y1="0" x2=".92" y2="1">
      <stop offset="0" stop-color="{KNURL_HI}"/>
      <stop offset=".34" stop-color="{KNURL_MID}"/>
      <stop offset=".62" stop-color="{KNURL_HI}" stop-opacity=".82"/>
      <stop offset="1" stop-color="{KNURL_LO}"/>
    </linearGradient>

    <!-- Annulus edge catch: outer catch strong and dying by 75%, inner bounce
         weaker and inverted. Both live outside any blur group. -->
    <linearGradient id="catchOuter" x1="0" y1="0" x2=".25" y2="1">
      <stop offset="0" stop-color="{CATCH_OUT}" stop-opacity=".90"/>
      <stop offset=".38" stop-color="{CATCH_OUT}" stop-opacity=".22"/>
      <stop offset=".75" stop-color="{CATCH_OUT}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="catchInner" x1="0" y1="1" x2=".2" y2="0">
      <stop offset="0" stop-color="{CATCH_IN}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{CATCH_IN}" stop-opacity="0"/>
    </linearGradient>

    <!-- The glass. Bright where the key lands, cooling to the edge so it reads as
         a lens rather than a disc; held at S <= 0.14 so it is not a hue family. -->
    <radialGradient id="glass" cx=".33" cy=".24" r=".94">
      <stop offset="0" stop-color="{GLASS_HI}" stop-opacity=".30"/>
      <stop offset=".56" stop-color="{GLASS_MID}" stop-opacity=".15"/>
      <stop offset="1" stop-color="{GLASS_LO}" stop-opacity=".44"/>
    </radialGradient>
    <!-- Biased away from the key, so the far wall of the barrel darkens under the
         glass and the lens reads as a tube rather than a printed disc. -->
    <radialGradient id="well" cx=".40" cy=".34" r=".72">
      <stop offset=".46" stop-color="{SHADOW}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity=".34"/>
    </radialGradient>
    <linearGradient id="specular" x1=".18" y1="0" x2=".72" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".78"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <!-- The barrel's own silhouette catch. Without it the protruding crescent is
         an unlit black edge and the loupe reads as a ring with a shadow cut
         behind it rather than as a cylinder. -->
    <linearGradient id="barrelCatch" x1=".3" y1=".18" x2=".92" y2=".96">
      <stop offset=".38" stop-color="{KNURL_MID}" stop-opacity="0"/>
      <stop offset="1" stop-color="{KNURL_HI}" stop-opacity=".58"/>
    </linearGradient>

    <!-- The caught cell: a gel chip, top-lit, so the accent is an object on the
         plane rather than a swatch of colour. -->
    <linearGradient id="chip" x1=".2" y1="0" x2=".7" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/>
      <stop offset=".46" stop-color="{ACCENT}"/>
      <stop offset="1" stop-color="{ACCENT_LO}"/>
    </linearGradient>
    <radialGradient id="bloom" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity=".46"/>
      <stop offset=".55" stop-color="{ACCENT}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>

    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6.5"/>
    </filter>
    <filter id="contact" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>
    <filter id="tight" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="11"/>
    </filter>

    <!-- The marketplace squircle, from create-mac-icon/assets/squircle-path.txt.
         One silhouette across the family; a bespoke radius reads as a mistake. -->
    <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>
    <clipPath id="lens"><circle cx="{CX}" cy="{CY}" r="{R_LENS}"/></clipPath>
  </defs>

  <!-- ══ bg — the cushion tile ══════════════════════════════════════════════ -->
  <g id="bg" clip-path="url(#tile)">
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#key)"/>
    <rect width="{S}" height="{S}" fill="url(#vignette)"/>
  </g>

  <!-- ══ mid — the plane of evidence, and the body of the instrument ═════════ -->
  <g id="mid" clip-path="url(#tile)">
    <g transform="rotate({PLANE_TILT} {CX} {CY})">
      {lattice(SP_OUT, GRID_SOFT, 3.2, ".30", filt="soft")}
    </g>

    <!-- contact shadows: broad ambient, then a tight one under the barrel. The
         highest ratio-of-effect-to-bytes layer there is. -->
    <ellipse cx="{CX + 30}" cy="{CY + R_OUTER - 6}" rx="{R_OUTER - 26}" ry="76"
             fill="{SHADOW}" opacity=".30" filter="url(#contact)"/>
    <ellipse cx="{CX + 20}" cy="{CY + R_OUTER + 12}" rx="{R_OUTER - 96}" ry="30"
             fill="{SHADOW}" opacity=".40" filter="url(#tight)"/>

    <!-- barrel: offset down-right of the rim so the loupe reads as a solid body -->
    <circle cx="{CX + 22}" cy="{CY + 30}" r="{R_OUTER - 18}" fill="url(#barrel)"/>
    <path d="M{CX - 164} {CY + 214} A {R_OUTER - 18} {R_OUTER - 18} 0 0 0 {CX + 262} {CY + 122}"
          fill="none" stroke="{KNURL_MID}" stroke-opacity=".42" stroke-width="8"/>
    <!-- and the catch along that silhouette. Drawn here, not in `highlight`: the
         rim disc paints over the arc everywhere the barrel is hidden, so only the
         protruding crescent keeps its lit edge. -->
    <circle cx="{CX + 22}" cy="{CY + 30}" r="{R_OUTER - 20}" fill="none"
            stroke="url(#barrelCatch)" stroke-width="8"/>
  </g>

  <!-- ══ fg — the milled rim, the glass, and what the glass resolves ═════════ -->
  <g id="fg" clip-path="url(#tile)">
    <circle cx="{CX}" cy="{CY}" r="{R_OUTER - 2}" fill="url(#milled)"/>
    <g>
        {notch_ring(CX, CY, R_KNURL + 14, R_OUTER - 3, NOTCHES)}
    </g>
    <circle cx="{CX}" cy="{CY}" r="{R_BEZEL}" fill="{BEZEL}" opacity=".90"/>

    <g clip-path="url(#lens)">
      <!-- the resolved plane: same origin, wider pitch — the lens magnifies -->
      <circle cx="{CX}" cy="{CY}" r="{R_LENS}" fill="{LENS_PLANE}"/>
      <g transform="rotate({PLANE_TILT} {CX} {CY})">
        {lattice(SP_IN / FINE_DIV, GRID_FINE, 1.2, ".30", reach=420.0)}
        {lattice(SP_IN, GRID_INK, 3.2, ".84", reach=420.0)}

        <!-- the verdict: where the cell was expected, and where it actually is -->
        <rect x="{GX - CELL_W / 2:.1f}" y="{GY - CELL_H / 2:.1f}"
              width="{CELL_W:.1f}" height="{CELL_H:.1f}" rx="{CELL_R}"
              fill="none" stroke="{GHOST}" stroke-opacity=".62" stroke-width="4"
              stroke-dasharray="15 11"/>
        <ellipse cx="{AX:.1f}" cy="{AY:.1f}" rx="{CELL_W * 1.35:.1f}" ry="{CELL_H * 1.5:.1f}"
                 fill="url(#bloom)"/>
        <rect x="{AX - CELL_W / 2 + 7:.1f}" y="{AY - CELL_H / 2 + 11:.1f}"
              width="{CELL_W:.1f}" height="{CELL_H:.1f}" rx="{CELL_R}"
              fill="{SHADOW}" opacity=".34" filter="url(#tight)"/>
        <rect x="{AX - CELL_W / 2:.1f}" y="{AY - CELL_H / 2:.1f}"
              width="{CELL_W:.1f}" height="{CELL_H:.1f}" rx="{CELL_R}"
              fill="url(#chip)"/>
        <path d="M{AX - CELL_W / 2 + 9:.1f} {AY - CELL_H / 2 + 8:.1f}
                 h{CELL_W - 18:.1f}" fill="none" stroke="#FFFFFF" stroke-opacity=".30"
              stroke-width="3.5" stroke-linecap="round"/>
      </g>

      <!-- the glass film itself, over the resolved plane so the plane reads
           THROUGH it — authored translucency, not a tint -->
      <circle cx="{CX}" cy="{CY}" r="{R_LENS}" fill="url(#glass)"/>
      <circle cx="{CX}" cy="{CY}" r="{R_LENS}" fill="url(#well)"/>

      <!-- the meniscus. Salvaged from the engine C2 raster, which was the one
           thing it had that the master did not: real glass shows a bright ring
           where its curved edge meets the bezel, with a thin dark line inboard
           of it giving the glass its thickness. -->
      <circle cx="{CX}" cy="{CY}" r="{R_LENS - 5}" fill="none"
              stroke="{GLASS_HI}" stroke-opacity=".38" stroke-width="7"/>
      <circle cx="{CX}" cy="{CY}" r="{R_LENS - 13}" fill="none"
              stroke="{SHADOW}" stroke-opacity=".18" stroke-width="7"/>
    </g>
  </g>

  <!-- ══ highlight — speculars, edge catches, tile rim ═══════════════════════ -->
  <g id="highlight" clip-path="url(#tile)">
    <path d="M{CX - 196} {CY - 88} A 214 214 0 0 1 {CX + 34} {CY - 238}
             A {R_LENS} {R_LENS} 0 0 0 {CX - 196} {CY - 88} Z"
          fill="url(#specular)" opacity=".52"/>
    <circle cx="{CX}" cy="{CY}" r="{R_LENS - 3}" fill="none"
            stroke="#FFFFFF" stroke-opacity=".50" stroke-width="4"
            stroke-dasharray="440 900" transform="rotate(-150 {CX} {CY})"/>
    <circle cx="{CX}" cy="{CY}" r="{R_OUTER + 3}" fill="none"
            stroke="url(#catchOuter)" stroke-width="9"/>
    <circle cx="{CX}" cy="{CY}" r="{R_KNURL + 5}" fill="none"
            stroke="url(#catchInner)" stroke-width="7"/>
    <path d="{SQUIRCLE}" fill="none" stroke="{TILE_RIM}" stroke-opacity=".70"
          stroke-width="3"/>
  </g>
</svg>
'''

if __name__ == "__main__":
    print(SVG)
