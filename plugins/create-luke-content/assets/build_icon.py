#!/usr/bin/env python3
"""build_icon.py — Engine A master for the `create-luke-content` icon.

Direction 2 (Tahoe gel-glass), sub-register (a): porcelain cushion tile carrying
an ember precision measuring plate (Craft) underneath a translucent frosted sheet of
prose lines (Voice).

CONCEPT — "Voice over Craft". Two stacked planes:
  1. The lower plane (Craft): A precision ruled measuring plate with fine scale
     graduations and grid marks, rendered in the house warm ember accent
     (#E4652E kin to Fledgeling's #C4622D).
  2. The upper plane (Voice): A soft-extruded translucent frosted glass sheet
     carrying left-aligned ragged-right prose lines (the corpus's reliable
     signal for prose: stacked capsule lines with a trailing short last line).
  3. The signature through-read: The ember measuring rule and tick graduations
     show clearly THROUGH the frosted sheet from underneath, creating an
     authored overlap blend (Tahoe tell 5) that flat rasters cannot fake.
  4. The semicolon detail: Luke's signature punctuation habit (semicolon over
     em dash) embossed cleanly at the end of the second prose line.

DIFFERENTIATORS FROM SIBLINGS:
  · mockup-fidelity: "The Overlay" uses two same-sized clay slabs off-register
    with an exposed gap sliver. This icon is two functionally distinct planes
    (a ruled measuring plate + a translucent prose document) with through-translucency.
  · armada-sync: Stacks prose capsule lines with a vermilion seal band across
    the middle. This icon has two planes, the accent is on the lower measuring plane,
    and the hero interaction is seeing the rule *through* the sheet.

CORPUS NUMBERS (sampled from apple-2026 porcelain register):
  ground:       L 0.96 top -> 0.83 bottom corners, vignette in warm shadow
  accent:       ember L 0.38-0.50, S 0.75-0.85
  frost sheet:  white fill with ground/ember hue bleed, L 0.88-0.95
  darkest face: warm dark #2B2218, L 0.05-0.08
"""

import pathlib
import sys

SQ = pathlib.Path(__file__).resolve().parents[2] / "create-mac-icon" / "assets" / "squircle-path.txt"

S = 1024

# ── palette ─────────────────────────────────────────────────────────────────
# Two hue families: porcelain / graphite clay, and the one ember accent.
GROUND_TOP, GROUND_MID, GROUND_BOT = "#F9F6EE", "#F3EFE4", "#E4DDCB"
RIM = "#FFFDF8"
SHADOW = "#4A3F2E"
SHADOW_DEEP = "#241B12"

# Lower Plane: Ruled Measuring Plate (Craft) — glowing volumetric ember
EMBER_TOP, EMBER_MID, EMBER_BOT = "#F98848", "#E15A20", "#A62808"
EMBER_WALL_TOP, EMBER_WALL_BOT = "#8E2608", "#541202"
EMBER_CORE = "#FFD8AB"
EMBER_EDGE = "#781E04"
EMBER_RULE = "#5A1402"
EMBER_GLOW = "#F79A61"
EMBER_BOUNCE = "#FFA873"

# Upper Plane: Translucent Prose Sheet (Voice) — frosted glass/gel
FROST_TOP = "#FFFFFF"
FROST_MID = "#FAF5EC"
FROST_BOT = "#EDE3D0"
FROST_RIM = "#FFFFFF"
FROST_WALL = "#887A68"
FROST_SHADOW = "#544636"

# Prose capsule lines (Voice) — sculpted graphite clay with top rim catch
LINE_TOP, LINE_MID, LINE_BOT = "#4E4234", "#362C20", "#20180F"
LINE_RIM = "#928472"

# ── geometry ────────────────────────────────────────────────────────────────
# Lower measuring plate (Craft): width 540, height 500, radius 40
MX, MY, MW, MH, MR = 216, 256, 540, 500, 40

# Upper translucent prose sheet (Voice): width 520, height 530, radius 36
# Shifted up-right by (74, -66) relative to measuring plate
SX, SY, SW, SH, SR = 290, 190, 520, 530, 36

# Prose lines layout (relative to canvas)
# 5 lines: left-aligned, ragged-right, line 2 carries semicolon, line 5 trailing short
PROSE_LINES = [
    (354, 276, 376, 26),    # Line 1 (long)
    (354, 342, 320, 26),    # Line 2 + semicolon at x=692
    (354, 408, 400, 26),    # Line 3 (longest)
    (354, 474, 336, 26),    # Line 4 (medium)
    (354, 540, 190, 26),    # Line 5 (short trailing)
]

# Semicolon position
SEMI_X, SEMI_Y = 694, 355


def rr(x: float, y: float, w: float, h: float, r: float) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" ry="{r:.1f}"'


def make_ticks(x_start: float, x_end: float, y_base: float, tick_len_major: float, tick_len_minor: float, step: float = 16) -> str:
    """Generate horizontal ruler graduation ticks."""
    paths = []
    n = int((x_end - x_start) / step)
    for i in range(n + 1):
        x = x_start + i * step
        is_major = (i % 4 == 0)
        is_mid = (i % 2 == 0)
        tlen = tick_len_major if is_major else (tick_len_major * 0.65 if is_mid else tick_len_minor)
        w = 3.6 if is_major else (2.4 if is_mid else 1.8)
        paths.append(f'<line x1="{x:.1f}" y1="{y_base:.1f}" x2="{x:.1f}" y2="{y_base + tlen:.1f}" stroke-width="{w:.1f}"/>')
    return "".join(paths)


def make_vert_ticks(y_start: float, y_end: float, x_base: float, tick_len_major: float, tick_len_minor: float, step: float = 16) -> str:
    """Generate vertical ruler graduation ticks."""
    paths = []
    n = int((y_end - y_start) / step)
    for i in range(n + 1):
        y = y_start + i * step
        is_major = (i % 4 == 0)
        is_mid = (i % 2 == 0)
        tlen = tick_len_major if is_major else (tick_len_major * 0.65 if is_mid else tick_len_minor)
        w = 3.6 if is_major else (2.4 if is_mid else 1.8)
        paths.append(f'<line x1="{x_base:.1f}" y1="{y:.1f}" x2="{x_base + tlen:.1f}" y2="{y:.1f}" stroke-width="{w:.1f}"/>')
    return "".join(paths)


def make_grid_lines(x1: float, y1: float, w: float, h: float, step: float = 44) -> str:
    """Generate fine internal calibration grid lines for the measuring plate."""
    paths = []
    # Horizontal grid lines
    ny = int(h / step)
    for i in range(1, ny):
        y = y1 + i * step
        paths.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x1 + w:.1f}" y2="{y:.1f}" stroke-width="1.8" stroke-dasharray="6,6"/>')
    # Vertical grid lines
    nx = int(w / step)
    for i in range(1, nx):
        x = x1 + i * step
        paths.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y1 + h:.1f}" stroke-width="1.8" stroke-dasharray="6,6"/>')
    return "".join(paths)


def semicolon_d(cx: float, cy: float, size: float = 24) -> str:
    """Generate SVG path d string for an embossed semicolon."""
    r = size * 0.26
    dot_cy = cy - size * 0.38
    tail_cy = cy + size * 0.22
    dot = f"M {cx - r:.1f} {dot_cy:.1f} a {r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0 a {r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0 "
    comma = (f"M {cx - r:.1f} {tail_cy:.1f} a {r:.1f} {r:.1f} 0 1 0 {2*r:.1f} 0 a {r:.1f} {r:.1f} 0 1 0 {-2*r:.1f} 0 "
             f"M {cx + r * 0.4:.1f} {tail_cy:.1f} "
             f"Q {cx + r * 0.9:.1f} {tail_cy + size * 0.42:.1f} {cx - r * 0.7:.1f} {tail_cy + size * 0.72:.1f} "
             f"Q {cx + r * 0.1:.1f} {tail_cy + size * 0.36:.1f} {cx - r * 0.2:.1f} {tail_cy + r * 0.6:.1f} Z")
    return dot + comma


def svg() -> str:
    d = SQ.read_text().strip() if SQ.exists() else ""
    if not d:
        print("squircle-path.txt not found", file=sys.stderr)
        raise SystemExit(1)

    measuring_plate = rr(MX, MY, MW, MH, MR)
    measuring_wall = rr(MX, MY + 18, MW, MH, MR)
    prose_sheet = rr(SX, SY, SW, SH, SR)
    prose_wall = rr(SX, SY + 14, SW, SH, SR)

    # Ruler ticks
    top_ticks = make_ticks(MX + 44, MX + MW - 44, MY + 16, 26, 14, step=16)
    left_ticks = make_vert_ticks(MY + 44, MY + MH - 44, MX + 16, 26, 14, step=16)
    grid_lines = make_grid_lines(MX + 28, MY + 28, MW - 56, MH - 56, step=44)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <!-- Cushion ground: warm daylight porcelain, subtle edge vignette -->
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".54" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vig" cx=".42" cy=".38" r=".78">
      <stop offset=".50" stop-color="{SHADOW}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity=".15"/>
    </radialGradient>

    <!-- Lower plane: ember measuring plate gradients -->
    <linearGradient id="emberPlate" x1="{MX + MW * .15}" y1="{MY}" x2="{MX + MW * .75}" y2="{MY + MH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_TOP}"/>
      <stop offset=".42" stop-color="{EMBER_MID}"/>
      <stop offset="1" stop-color="{EMBER_BOT}"/>
    </linearGradient>
    <linearGradient id="emberWall" x1="{MX}" y1="{MY}" x2="{MX + MW}" y2="{MY + MH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_WALL_TOP}"/>
      <stop offset="1" stop-color="{EMBER_WALL_BOT}"/>
    </linearGradient>
    <linearGradient id="emberRim" x1="{MX}" y1="{MY}" x2="{MX + MW}" y2="{MY + MH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_CORE}" stop-opacity=".90"/>
      <stop offset=".45" stop-color="{EMBER_GLOW}" stop-opacity=".60"/>
      <stop offset="1" stop-color="{EMBER_EDGE}" stop-opacity=".80"/>
    </linearGradient>
    <linearGradient id="emberInnerGlow" x1="{MX}" y1="{MY}" x2="{MX}" y2="{MY + 150}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_CORE}" stop-opacity=".46"/>
      <stop offset="1" stop-color="{EMBER_CORE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="emberSideShade" x1="{MX + MW * .5}" y1="0" x2="{MX + MW}" y2="0"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{SHADOW_DEEP}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SHADOW_DEEP}" stop-opacity=".26"/>
    </linearGradient>

    <!-- Upper plane: translucent frosted prose sheet gradients -->
    <linearGradient id="frostFace" x1="{SX + SW * .15}" y1="{SY}" x2="{SX + SW * .70}" y2="{SY + SH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{FROST_TOP}" stop-opacity=".94"/>
      <stop offset=".40" stop-color="{FROST_MID}" stop-opacity=".86"/>
      <stop offset="1" stop-color="{FROST_BOT}" stop-opacity=".80"/>
    </linearGradient>
    <linearGradient id="frostWall" x1="{SX}" y1="{SY}" x2="{SX + SW}" y2="{SY + SH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{FROST_WALL}" stop-opacity=".88"/>
      <stop offset="1" stop-color="{FROST_SHADOW}" stop-opacity=".96"/>
    </linearGradient>
    <!-- Warm bounce from ember plate bleeding into lower-left of frost sheet -->
    <linearGradient id="frostEmberBleed" x1="{SX}" y1="{SY + SH * .20}" x2="{SX + SW * .55}" y2="{SY + SH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{EMBER_GLOW}" stop-opacity="0"/>
      <stop offset=".45" stop-color="{EMBER_GLOW}" stop-opacity=".18"/>
      <stop offset="1" stop-color="{EMBER_MID}" stop-opacity=".36"/>
    </linearGradient>
    <linearGradient id="frostRim" x1="{SX}" y1="{SY}" x2="{SX + SW}" y2="{SY + SH}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{FROST_RIM}" stop-opacity=".96"/>
      <stop offset=".50" stop-color="{FROST_RIM}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{FROST_SHADOW}" stop-opacity=".45"/>
    </linearGradient>
    <linearGradient id="frostSatin" x1="0" y1="{SY}" x2="0" y2="{SY + SH * .45}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{FROST_RIM}" stop-opacity=".32"/>
      <stop offset="1" stop-color="{FROST_RIM}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="frostAO" cx=".78" cy=".82" r=".60">
      <stop offset="0" stop-color="{SHADOW_DEEP}" stop-opacity=".24"/>
      <stop offset="1" stop-color="{SHADOW_DEEP}" stop-opacity="0"/>
    </radialGradient>

    <!-- Prose capsule line gradients -->
    <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LINE_TOP}"/>
      <stop offset=".55" stop-color="{LINE_MID}"/>
      <stop offset="1" stop-color="{LINE_BOT}"/>
    </linearGradient>
    <linearGradient id="lineRimGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LINE_RIM}" stop-opacity=".80"/>
      <stop offset="1" stop-color="{LINE_BOT}" stop-opacity=".18"/>
    </linearGradient>

    <!-- Filters -->
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
    <filter id="plateShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>
    <filter id="sheetShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="emberGlowFilter" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
    <filter id="lineEmboss" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="1.8"/>
    </filter>
    <filter id="throughFrostBlur" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="1.5"/>
    </filter>

    <!-- Clips -->
    <clipPath id="tileClip"><path d="{d}"/></clipPath>
    <clipPath id="plateClip">{measuring_plate}/></clipPath>
    <clipPath id="sheetClip">{prose_sheet}/></clipPath>
  </defs>

  <g clip-path="url(#tileClip)">
    <!-- ── #bg Layer: Ground porcelain cushion, shadows, and ember ambient bleed ── -->
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>

      <!-- Ambient ember glow under measuring plate -->
      <g filter="url(#emberGlowFilter)" opacity=".40">
        {rr(MX + 10, MY + 20, MW - 20, MH - 20, MR)} fill="{EMBER_MID}"/>
      </g>

      <!-- Contact shadow of lower measuring plate on porcelain -->
      <g filter="url(#plateShadow)" opacity=".42">
        {rr(MX + 8, MY + 26, MW, MH, MR)} fill="{SHADOW_DEEP}"/>
      </g>
    </g>

    <!-- ── #mid Layer: Lower plane (Craft) — Ember Ruled Measuring Plate ── -->
    <g id="mid">
      <!-- Measuring plate 3D wall & base -->
      {measuring_wall} fill="url(#emberWall)"/>
      {measuring_plate} fill="url(#emberPlate)"/>

      <!-- Inner rim lighting and top catch on measuring plate -->
      <g clip-path="url(#plateClip)">
        {measuring_plate} fill="url(#emberInnerGlow)"/>
        {measuring_plate} fill="url(#emberSideShade)"/>
        {rr(MX, MY, MW, MH, MR)} fill="none" stroke="url(#emberRim)" stroke-width="6"/>

        <!-- Grid lines across the measuring plate -->
        <g stroke="{EMBER_RULE}" opacity=".50">
          {grid_lines}
        </g>

        <!-- Ruler graduations and tick marks -->
        <g stroke="{EMBER_RULE}" stroke-linecap="round" opacity=".92">
          {top_ticks}
          {left_ticks}
        </g>
        <!-- Highlighted tick catches (light catching the engraved marks) -->
        <g stroke="{EMBER_CORE}" stroke-linecap="round" opacity=".52" transform="translate(0, 1)">
          {top_ticks}
          {left_ticks}
        </g>
      </g>

      <!-- Shadow cast by upper prose sheet onto lower measuring plate & ground -->
      <g filter="url(#sheetShadow)" opacity=".42">
        {rr(SX - 8, SY + 20, SW, SH, SR)} fill="{SHADOW_DEEP}"/>
      </g>
    </g>

    <!-- ── #fg Layer: Upper plane (Voice) — Translucent Prose Sheet + Lines ── -->
    <g id="fg">
      <!-- Upper sheet 3D thickness wall -->
      {prose_wall} fill="url(#frostWall)"/>
      <!-- Translucent frosted glass sheet base -->
      {prose_sheet} fill="url(#frostFace)"/>

      <!-- Translucent through-read: the ember rule seen THROUGH the frosted sheet -->
      <g clip-path="url(#sheetClip)">
        <!-- Ember warm hue bleed into frost sheet -->
        {prose_sheet} fill="url(#frostEmberBleed)"/>

        <!-- The underlying measuring plate's features softly visible through glass -->
        <g opacity=".46" filter="url(#throughFrostBlur)">
          {measuring_plate} fill="none" stroke="{EMBER_MID}" stroke-width="4"/>
          <g stroke="{EMBER_RULE}" stroke-linecap="round" opacity=".65">
            {top_ticks}
            {left_ticks}
          </g>
          <g stroke="{EMBER_RULE}" opacity=".36">
            {grid_lines}
          </g>
        </g>

        <!-- Sheet internal satin gloss & AO -->
        {rr(SX, SY, SW, SH * .45, SR)} fill="url(#frostSatin)"/>
        {prose_sheet} fill="url(#frostAO)"/>

        <!-- Sheet boundary rim / frosted edge -->
        {rr(SX, SY, SW, SH, SR)} fill="none" stroke="url(#frostRim)" stroke-width="6"/>
      </g>

      <!-- Prose capsule lines (Voice) -->
      <g>
        <!-- Contact shadow under each line for depth -->
        <g filter="url(#lineEmboss)" opacity=".34">
          {"".join(rr(x, y + 2.5, w, h, h * .5) + ' fill="' + SHADOW_DEEP + '"/>' for x, y, w, h in PROSE_LINES)}
          <path d="{semicolon_d(SEMI_X, SEMI_Y + 2.5, size=24)}" fill="{SHADOW_DEEP}"/>
        </g>

        <!-- Line bodies -->
        {"".join(rr(x, y, w, h, h * .5) + ' fill="url(#lineGrad)"/>' for x, y, w, h in PROSE_LINES)}
        <!-- Semicolon body -->
        <path d="{semicolon_d(SEMI_X, SEMI_Y, size=24)}" fill="url(#lineGrad)"/>

        <!-- Top rim light on each capsule line (sculpted depth) -->
        {"".join(f'<path d="M{x + h*.5:.1f} {y + 2:.1f} H{x + w - h*.5:.1f}" stroke="{RIM}" stroke-width="2.5" stroke-linecap="round" opacity=".60"/>' for x, y, w, h in PROSE_LINES)}
        <!-- Highlight catch on semicolon dot and comma head -->
        <circle cx="{SEMI_X:.1f}" cy="{SEMI_Y - 24 * .38 - 1:.1f}" r="3" fill="{RIM}" opacity=".50"/>
        <circle cx="{SEMI_X:.1f}" cy="{SEMI_Y + 24 * .22 - 1:.1f}" r="3" fill="{RIM}" opacity=".45"/>
      </g>
    </g>

    <!-- ── #highlight Layer: Global rim light, specular catches, tile cushion rim ── -->
    <g id="highlight">
      <!-- Lit top edge of the upper frosted sheet -->
      <path d="M{SX + SR} {SY + 2.5} H{SX + SW - SR}" stroke="{RIM}" stroke-width="5.5"
            stroke-linecap="round" opacity=".88"/>
      <!-- Soft left edge highlight on frosted sheet -->
      <path d="M{SX + 2.5} {SY + SR} V{SY + SH - SR}" stroke="{RIM}" stroke-width="4.5"
            stroke-linecap="round" opacity=".70"/>

      <!-- Lit top-left arris catch of lower measuring plate -->
      <path d="M{MX + MR} {MY + 2.5} H{MX + MW * .42}" stroke="{EMBER_CORE}" stroke-width="4.5"
            stroke-linecap="round" opacity=".85"/>
      <path d="M{MX + 2.5} {MY + MR} V{MY + MH * .42}" stroke="{EMBER_CORE}" stroke-width="4"
            stroke-linecap="round" opacity=".80"/>

      <!-- Cushion tile inner perimeter rim light (Tahoe ground tell 1) -->
      <path d="{d}" fill="none" stroke="{RIM}" stroke-width="7" opacity=".85"/>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    print(svg())
