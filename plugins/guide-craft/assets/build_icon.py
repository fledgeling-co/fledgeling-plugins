#!/usr/bin/env python3
"""Build the guide-craft icon master ("Folio and season tab").

Geometry and material live here as named constants so both fidelity edits and the
marketplace banner derive directly from this file.

    python3 build_icon.py   # writes icon.svg and icon-engineA-handauthored.svg

THE SUBJECT: "Folio and season tab"
-----------------------------------
A thick tactical field-guide folio seen in gentle plan-oblique from upper-left: a warm
slate-charcoal hardcover with a wrapped U-spine and recessed hinge crease, thick frosted
ivory-glass page layers visible along the bottom and right fore-edges, and one luminous
translucent vermilion-ember gel bookmark tab emerging cleanly from the top-right page edge
to flag the live season.

MEASURED VALUES
---------------
Porcelain cushion ground, vignette, inner rim, and light vector are lifted from the
fledgeling-plugins family (`plugins/create-website/assets/build_icon.py`, measured against
`create-mac-icon/references/corpus/apple-2026/{apple-26,apple-28,apple-31,apple-22}.png`).
Oblique folio geometry, spine groove, 3-layer frosted fore-edge, and top-right vermilion
tab placement were measured from Engine C raster take 2 (`icon-engineC-raster-d56987-2.png`)
and optically centered at ~68% tile span so the folio breathes cleanly on the porcelain shelf.
"""

from pathlib import Path
import math

HERE = Path(__file__).resolve().parent
SQUIRCLE = HERE / "squircle-path.txt"
S = 1024

# ---------------------------------------------------------------- light
LIGHT_DX, LIGHT_DY = -0.62, -0.78   # key bearing, upper-left (shared with banner)

# ---------------------------------------------------------------- plan-oblique geometry
CX, CY = 498.0, 446.0      # optically centers folio + book thickness in 1024 tile
UX, UY = 414.0, 116.0      # width vector (spine -> fore-edge)
VX, VY = -204.0, 344.0     # height vector (top -> bottom along spine)
CORNER_R = 46.0            # cover outer corner radius
SPINE_R = 46.0             # rounded spine corner radius
BOOK_THICK = 114.0         # vertical thickness from top cover to back board top
BACK_THICK = 22.0          # bottom hardcover board thickness
COVER_THICK = 22.0         # top hardcover board thickness
SPINE_GROOVE_U = 0.145     # recessed hinge crease fraction along U

# Vermilion gel season bookmark tab projecting from upper-right page edge
TAB_U0, TAB_U1 = 0.72, 0.94
TAB_OUT = 108.0            # projection past top edge along -V
TAB_R = 28.0
TAB_THICK = 22.0

# ---------------------------------------------------------------- fledgeling family palette
GROUND_HI = "#FDFCF9"
GROUND_MID = "#F3EFE7"
GROUND_LO = "#E7E1D5"
VIGNETTE = "#C4B899"
RIM_TILE = "#FFFFFF"
POOL = "#B7AA90"
AO = "#4A3B2C"

# Warm slate-charcoal hardcover (matching fledgeling's warm dark band)
COVER_HI = "#6B645E"
COVER_MID = "#4A4541"
COVER_LO = "#302D2A"
COVER_WALL_HI = "#3A3633"
COVER_WALL_LO = "#1E1C1A"
SPINE_HI = "#7D766F"
SPINE_MID = "#48433F"
SPINE_LO = "#262321"

# Frosted ivory-glass page block
PAGE_HI = "#FFFBF3"
PAGE_MID = "#F0E3D0"
PAGE_LO = "#D4BFA4"
PAGE_RIB_HI = "#FFFDF9"
PAGE_RIB_LO = "#C4AD8F"

# Vermilion-ember gel bookmark tab (HSL L 0.44-0.58, ~3:1+ contrast on porcelain)
TAB_HI = "#FF9656"
TAB_MID = "#EC6A31"
TAB_LO = "#C44D1B"
TAB_WALL = "#9B3510"
TAB_RIM = "#FFD2B2"
EMBER_SPILL = "#F6D3AC"


def norm(x: float, y: float) -> tuple[float, float]:
    m = math.hypot(x, y)
    return x / m, y / m


def pt(u: float, v: float, dy: float = 0.0, dx: float = 0.0) -> tuple[float, float]:
    """Point on the folio plane: u in [0,1] left->right, v in [0,1] top->bottom."""
    x = CX + (u - 0.5) * UX + (v - 0.5) * VX + dx
    y = CY + (u - 0.5) * UY + (v - 0.5) * VY + dy
    return x, y


def rounded_poly(pts: list[tuple[float, float]], radii: list[float] | float) -> str:
    n = len(pts)
    r_list = [radii] * n if isinstance(radii, (int, float)) else list(radii)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sweep = 1 if area > 0 else 0
    out = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = r_list[i]
        v1 = norm(a[0] - b[0], a[1] - b[1])
        v2 = norm(c[0] - b[0], c[1] - b[1])
        cos = max(-1.0, min(1.0, v1[0] * v2[0] + v1[1] * v2[1]))
        theta = math.acos(cos)
        if r <= 0.5 or theta < 1e-3 or abs(math.pi - theta) < 1e-3:
            out.append(("L", b))
            continue
        t = r / math.tan(theta / 2)
        t = min(t, 0.45 * math.hypot(a[0] - b[0], a[1] - b[1]), 0.45 * math.hypot(c[0] - b[0], c[1] - b[1]))
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


def cover_quad(dy: float = 0.0, dx: float = 0.0, u0: float = 0.0, u1: float = 1.0, v0: float = 0.0, v1: float = 1.0) -> list[tuple[float, float]]:
    return [
        pt(u0, v0, dy, dx),
        pt(u1, v0, dy, dx),
        pt(u1, v1, dy, dx),
        pt(u0, v1, dy, dx),
    ]


def tab_quad(dy: float = 0.0, dx: float = 0.0) -> list[tuple[float, float]]:
    vx_n, vy_n = norm(VX, VY)
    out_dx, out_dy = -vx_n * TAB_OUT, -vy_n * TAB_OUT
    p_bl = pt(TAB_U0, 0.22, dy, dx)
    p_br = pt(TAB_U1, 0.22, dy, dx)
    p_tr = (pt(TAB_U1, 0.0, dy, dx)[0] + out_dx, pt(TAB_U1, 0.0, dy, dx)[1] + out_dy)
    p_tl = (pt(TAB_U0, 0.0, dy, dx)[0] + out_dx, pt(TAB_U0, 0.0, dy, dx)[1] + out_dy)
    return [p_tl, p_tr, p_br, p_bl]


def swept_stack(path_fn, y0: float, y1: float, steps: int, fill: str, extra: str = "") -> str:
    """Extrude a rounded polygon cleanly along +Y using minimal steps (keeps path count tight)."""
    parts = []
    for k in range(steps, -1, -1):
        yy = y0 + (y1 - y0) * k / steps
        parts.append(f'<path d="{path_fn(yy)}" fill="{fill}"{extra}/>')
    return "\n".join(parts)


def build() -> str:
    sq = SQUIRCLE.read_text().strip()
    lx, ly = norm(LIGHT_DX, LIGHT_DY)

    y_back_bot = BOOK_THICK + BACK_THICK
    y_back_top = BOOK_THICK
    y_page_bot = BOOK_THICK + 4.0
    y_page_top = 18.0
    y_cov_bot = COVER_THICK
    y_cov_top = 0.0

    # Page block slightly inset on right & bottom fore-edges so covers frame it cleanly
    u_pg0, u_pg1 = 0.055, 0.975
    v_pg0, v_pg1 = 0.035, 0.965

    def cover_at(yy: float, dx: float = 0.0) -> str:
        return rounded_poly(cover_quad(yy, dx=dx), [SPINE_R, CORNER_R, CORNER_R, SPINE_R])

    def page_at(yy: float) -> str:
        return rounded_poly(cover_quad(yy, u0=u_pg0, u1=u_pg1, v0=v_pg0, v1=v_pg1), [32, 38, 38, 32])

    def tab_at(yy: float) -> str:
        return rounded_poly(tab_quad(yy), [TAB_R, TAB_R, 12, 12])

    p_cov_top = cover_at(y_cov_top)
    p_cov_bot = cover_at(y_cov_bot)
    p_back_bot = cover_at(y_back_bot)
    p_page_bot = page_at(y_page_bot)
    p_page_top = page_at(y_page_top)

    # Smooth U-spine casing: flush left strip swept cleanly from top cover to back board
    def spine_strip_at(yy: float) -> str:
        frac = (yy - y_cov_top) / max(1.0, (y_back_bot - y_cov_top))
        bow = -3.5 * math.sin(math.pi * frac)
        return rounded_poly(cover_quad(yy, dx=bow, u0=0.0, u1=0.11, v0=0.0, v1=1.0), [SPINE_R, 16, 16, SPINE_R])

    # Spine hinge groove line on top cover
    gr0 = pt(SPINE_GROOVE_U, 0.02, y_cov_top + 2)
    gr1 = pt(SPINE_GROOVE_U, 0.98, y_cov_top + 2)

    # Subtle debossed readout bars on front cover
    bar1 = rounded_poly(cover_quad(y_cov_top, u0=0.30, u1=0.77, v0=0.41, v1=0.47), 10)
    bar2 = rounded_poly(cover_quad(y_cov_top, u0=0.30, u1=0.57, v0=0.53, v1=0.58), 9)

    # Vermilion gel bookmark tab seated neatly between top cover and upper pages
    tab_y = y_page_top + 12.0
    p_tab_top = tab_at(tab_y)
    tq = tab_quad(tab_y)
    tab_cx = sum(p[0] for p in tq) / 4
    tab_cy = sum(p[1] for p in tq) / 4

    # Fore-edge corner coordinate for luminous frosted highlight
    pg_br = pt(u_pg1, v_pg1, (y_page_top + y_page_bot) * 0.5)
    pg_tr = pt(u_pg1, v_pg0, y_page_top + 24)

    # Ground shadow displaced away from upper-left key
    sh_dx, sh_dy = -lx * 42.0, -ly * 48.0
    p_shadow_far = cover_at(y_back_bot + sh_dy * 0.42, dx=sh_dx * 0.58)
    p_shadow_near = cover_at(y_back_bot + 14.0, dx=8.0)

    out = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">')
    add("<defs>")
    add(f'<clipPath id="tile"><path d="{sq}"/></clipPath>')
    add(f'<clipPath id="covTop"><path d="{p_cov_top}"/></clipPath>')
    add(f'<clipPath id="tabTop"><path d="{p_tab_top}"/></clipPath>')

    # Porcelain cushion tile ground
    add(f'''<linearGradient id="ground" gradientUnits="userSpaceOnUse" x1="310" y1="0" x2="640" y2="{S}">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.54" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/></linearGradient>''')
    add(f'''<radialGradient id="vig" cx="0.40" cy="0.28" r="0.88">
      <stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.24"/></radialGradient>''')

    # Warm ember bounce pool near top-right tab
    add(f'''<radialGradient id="emberSpill" gradientUnits="userSpaceOnUse" cx="{tab_cx + 26:.1f}" cy="{tab_cy + 115:.1f}" r="275">
      <stop offset="0" stop-color="{EMBER_SPILL}" stop-opacity="0.58"/>
      <stop offset="0.55" stop-color="{EMBER_SPILL}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{EMBER_SPILL}" stop-opacity="0"/></radialGradient>''')

    # Cover face gradient along key light axis
    add(f'''<linearGradient id="coverFace" gradientUnits="userSpaceOnUse" x1="250" y1="150" x2="740" y2="730">
      <stop offset="0" stop-color="{COVER_HI}"/><stop offset="0.48" stop-color="{COVER_MID}"/>
      <stop offset="1" stop-color="{COVER_LO}"/></linearGradient>''')
    add(f'''<radialGradient id="coverBloom" gradientUnits="userSpaceOnUse" cx="385" cy="280" r="360">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0.03"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>''')
    add(f'''<linearGradient id="coverWall" gradientUnits="userSpaceOnUse" x1="200" y1="470" x2="780" y2="750">
      <stop offset="0" stop-color="{COVER_WALL_HI}"/><stop offset="1" stop-color="{COVER_WALL_LO}"/></linearGradient>''')
    add(f'''<linearGradient id="spineGrad" gradientUnits="userSpaceOnUse" x1="175" y1="440" x2="310" y2="520">
      <stop offset="0" stop-color="{SPINE_HI}"/><stop offset="0.45" stop-color="{SPINE_MID}"/>
      <stop offset="1" stop-color="{SPINE_LO}"/></linearGradient>''')

    # Frosted ivory-glass page block gradient
    add(f'''<linearGradient id="pageGrad" gradientUnits="userSpaceOnUse" x1="220" y1="670" x2="840" y2="480">
      <stop offset="0" stop-color="{PAGE_LO}"/><stop offset="0.46" stop-color="{PAGE_MID}"/>
      <stop offset="0.72" stop-color="{PAGE_HI}"/><stop offset="1" stop-color="{PAGE_MID}"/></linearGradient>''')
    add(f'''<radialGradient id="pageCornerGlow" gradientUnits="userSpaceOnUse" cx="{pg_br[0]:.1f}" cy="{pg_br[1]:.1f}" r="145">
      <stop offset="0" stop-color="#FFFDF8" stop-opacity="0.78"/>
      <stop offset="0.55" stop-color="#FBE8D2" stop-opacity="0.24"/>
      <stop offset="1" stop-color="#FBE8D2" stop-opacity="0"/></radialGradient>''')

    # Vermilion gel bookmark tab gradients
    add(f'''<linearGradient id="tabGrad" gradientUnits="userSpaceOnUse" x1="{tq[0][0]:.1f}" y1="{tq[0][1]:.1f}" x2="{tq[2][0]:.1f}" y2="{tq[2][1]:.1f}">
      <stop offset="0" stop-color="{TAB_HI}"/><stop offset="0.48" stop-color="{TAB_MID}"/>
      <stop offset="1" stop-color="{TAB_LO}"/></linearGradient>''')
    add(f'''<radialGradient id="tabGlow" gradientUnits="userSpaceOnUse" cx="{tab_cx - 10:.1f}" cy="{tab_cy - 18:.1f}" r="96">
      <stop offset="0" stop-color="#FFD8BA" stop-opacity="0.56"/>
      <stop offset="0.65" stop-color="#FF9656" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#FF9656" stop-opacity="0"/></radialGradient>''')

    # Lit rim gradient dying away from key light
    add(f'''<linearGradient id="covRim" gradientUnits="userSpaceOnUse" x1="220" y1="160" x2="770" y2="720">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.44"/>
      <stop offset="0.52" stop-color="#FFFFFF" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.02"/></linearGradient>''')

    add('<filter id="shFar" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="28"/></filter>')
    add('<filter id="shNear" x="-15%" y="-15%" width="130%" height="130%"><feGaussianBlur stdDeviation="9"/></filter>')
    add('<filter id="aoSoft" x="-15%" y="-15%" width="130%" height="130%"><feGaussianBlur stdDeviation="7"/></filter>')
    add("</defs>")

    # Master tile clipped to shared squircle
    add('<g clip-path="url(#tile)">')

    # LAYER 1: bg — porcelain cushion tile + warm bounce + ground contact shadow
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#ground)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vig)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#emberSpill)"/>')
    add(f'<path d="{p_shadow_far}" fill="{AO}" opacity="0.16" filter="url(#shFar)"/>')
    add(f'<path d="{p_shadow_near}" fill="{AO}" opacity="0.22" filter="url(#shNear)"/>')
    add('</g>')

    # LAYER 2: mid — back board, wrapped spine, vermilion gel season tab, and frosted glass page block
    add('<g id="mid">')
    # Back hardcover board extruded cleanly
    add(swept_stack(cover_at, y_back_top, y_back_bot, 4, COVER_WALL_LO))
    add(f'<path d="{cover_at(y_back_top)}" fill="{COVER_LO}"/>')

    # Smooth wrapped spine connecting back board to top cover
    add(swept_stack(spine_strip_at, y_cov_top + 6.0, y_back_bot - 2.0, 24, "url(#spineGrad)"))

    # Vermilion gel bookmark tab (extruded cleanly with zero gap)
    add(swept_stack(tab_at, tab_y + 2.0, tab_y + TAB_THICK, 10, TAB_WALL))
    add(f'<path d="{p_tab_top}" fill="url(#tabGrad)"/>')
    add(f'<path d="{p_tab_top}" fill="url(#tabGlow)"/>')
    add(f'<g clip-path="url(#tabTop)"><path d="{p_tab_top}" fill="none" stroke="{TAB_RIM}" stroke-width="5" opacity="0.74"/></g>')

    # Frosted ivory-glass page block extruded cleanly with three crisp page-layer seams
    add(swept_stack(page_at, y_page_top, y_page_bot, 24, "url(#pageGrad)"))
    for frac in (0.30, 0.58, 0.84):
        yy = y_page_top + (y_page_bot - y_page_top) * frac
        add(f'<path d="{page_at(yy)}" fill="none" stroke="{PAGE_RIB_LO}" stroke-width="3.6" opacity="0.54"/>')
        add(f'<path d="{page_at(yy + 3.0)}" fill="none" stroke="{PAGE_RIB_HI}" stroke-width="2.4" opacity="0.76"/>')
    # Luminous glass corner catch + warm ember spill on upper-right pages
    add(f'<circle cx="{pg_br[0]:.1f}" cy="{pg_br[1]:.1f}" r="145" fill="url(#pageCornerGlow)"/>')
    add(f'<circle cx="{pg_tr[0]-6:.1f}" cy="{pg_tr[1]+10:.1f}" r="85" fill="{TAB_MID}" opacity="0.18" filter="url(#shFar)"/>')
    # Ambient occlusion cast by front cover onto top of page block
    add(f'<path d="{p_cov_bot}" transform="translate(3,11)" fill="{AO}" opacity="0.30" filter="url(#aoSoft)"/>')
    add('</g>')

    # LAYER 3: fg — front slate hardcover slab, hinge crease, and subtle debossed index bars
    add('<g id="fg">')
    add(swept_stack(cover_at, y_cov_top + 4.0, y_cov_bot, 5, "url(#coverWall)"))
    add(f'<path d="{p_cov_top}" fill="url(#coverFace)"/>')
    add(f'<path d="{p_cov_top}" fill="url(#coverBloom)"/>')
    add('<g clip-path="url(#covTop)">')
    add(f'<line x1="{gr0[0]-36:.1f}" y1="{gr0[1]-10:.1f}" x2="{gr1[0]-36:.1f}" y2="{gr1[1]-10:.1f}" stroke="#FFFFFF" stroke-width="18" opacity="0.10"/>')
    add(f'<line x1="{gr0[0]:.1f}" y1="{gr0[1]:.1f}" x2="{gr1[0]:.1f}" y2="{gr1[1]:.1f}" stroke="#141211" stroke-width="7.5" opacity="0.56"/>')
    add(f'<line x1="{gr0[0]+5.5:.1f}" y1="{gr0[1]+1.5:.1f}" x2="{gr1[0]+5.5:.1f}" y2="{gr1[1]+1.5:.1f}" stroke="#FFFFFF" stroke-width="2.6" opacity="0.18"/>')
    add(f'<path d="{bar1}" fill="#1E1C1A" opacity="0.42"/>')
    add(f'<path d="{bar1}" transform="translate(0,2.2)" fill="none" stroke="#FFFFFF" stroke-width="1.8" opacity="0.10"/>')
    add(f'<path d="{bar2}" fill="#1E1C1A" opacity="0.34"/>')
    add(f'<path d="{bar2}" transform="translate(0,2.0)" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.08"/>')
    add('</g>')
    add('</g>')

    # LAYER 4: highlight — cover lit rim catch + porcelain cushion inner ring
    add('<g id="highlight">')
    add(f'<g clip-path="url(#covTop)"><path d="{p_cov_top}" fill="none" stroke="url(#covRim)" stroke-width="5"/></g>')
    add(f'<path d="{sq}" fill="none" stroke="{RIM_TILE}" stroke-width="10" opacity="0.55"/>')
    add('</g>')

    add('</g>')
    add("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    svg = build()
    (HERE / "icon.svg").write_text(svg, encoding="utf-8")
    (HERE / "icon-engineA-handauthored.svg").write_text(svg, encoding="utf-8")
    print(f"Wrote icon.svg and icon-engineA-handauthored.svg ({len(svg):,} bytes)")
