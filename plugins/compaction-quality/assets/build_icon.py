#!/usr/bin/env python3
"""Engine A master generator - direction "Load-Bearing" (v2).

v2 rebuilds C1's material and form into the layered master: rounded shoulders
top and bottom (a poured gel puck, not a hard-cut drum), the graphite wall
visibly warming around the dominant seam, dense strata, and a warm floor spill.
Discontinuous part-width hairlines are salvaged from the Engine B take.

Emits a 1024x1024 full-bleed layered SVG (bg / mid / fg / highlight). No baked
corner radius and no baked drop shadow; the squircle is a clip for preview.
"""
import math, sys

S, CX = 1024, 512
HW = 332
X0, X1 = CX - HW, CX + HW        # 664 wide = 64.8% of tile, top of the sanctioned band
SHOULDER_T, SHOULDER_B = 388, 730   # where the side walls run straight
K_TOP, K_BOT = 106.7, 109.3         # cubic handles -> apex 308 / 812
RY = 46                             # cylinder minor radius at the wall
K = RY * 4.0 / 3.0                  # cubic offset for a tangent-vertical half-ellipse

# five seams: side-y, stroke width, dominant. One dominant, one secondary glow, three quiet.
SEAMS = [(432, 6, False), (486, 9, False), (566, 34, True), (640, 8, False), (694, 13, False)]
DOM_Y, SEC_Y = 566, 486
STRATA_TOP, STRATA_BOT = 396, 786

# three layers still shedding off the top: thin discs on the cylinder's own perspective,
# fanned slightly, growing and solidifying as they near the core
SHEETS = [(190, 11, 168, -14, 0.11), (232, 14, 196, 9, 0.21), (270, 18, 226, -5, 0.36)]
BLEED_H = 148   # how far the glow warms the gel above and below the seam

BODY = ("M {x0} {st} C {x0} {ct}, {x1} {ct}, {x1} {st} L {x1} {sb} "
        "C {x1} {cb}, {x0} {cb}, {x0} {sb} Z").format(
    x0=X0, x1=X1, st=SHOULDER_T, sb=SHOULDER_B,
    ct=round(SHOULDER_T - K_TOP, 1), cb=round(SHOULDER_B + K_BOT, 1))


def squircle(n=5.0, N=192):
    a = S / 2.0
    p = []
    for i in range(N):
        t = 2 * math.pi * i / N
        ct, st = math.cos(t), math.sin(t)
        p.append((a + a * math.copysign(abs(ct) ** (2 / n), ct),
                  a + a * math.copysign(abs(st) ** (2 / n), st)))
    return "M %.2f %.2f " % p[0] + " ".join("L %.2f %.2f" % q for q in p[1:]) + " Z"


def arc(y):
    """Front-half of the circle at height y on the cylinder wall, tangent-vertical
    at both ends so it meets the silhouette without a corner."""
    return "M %d %.1f C %d %.1f, %d %.1f, %d %.1f" % (X0, y, X0, y + K, X1, y + K, X1, y)


def lcg(seed=29):
    v = seed
    while True:
        v = (v * 16807) % 2147483647
        yield v / 2147483647.0


def strata():
    """~40 hairlines tightening with depth; ~40% run part-width, the way real
    sedimentary bands pinch out (salvaged from the Engine B take)."""
    r, out, y = lcg(), [], STRATA_TOP
    blocked = [(sy - w / 2 - 5, sy + w / 2 + 5) for sy, w, _ in SEAMS]
    while y < STRATA_BOT:
        t = (y - STRATA_TOP) / (STRATA_BOT - STRATA_TOP)
        step = 9.5 - 4.2 * t + next(r) * 5.5
        if not any(a <= y <= b for a, b in blocked):
            op = 0.11 + next(r) * 0.17 + t * 0.08
            sw = 1.7 + next(r) * 2.1
            dash = ""
            if next(r) < 0.42:
                seg = 200 + next(r) * 300
                dash = ' stroke-dasharray="%.0f 1400" stroke-dashoffset="%.0f"' % (
                    seg, -next(r) * (640 - seg))
            out.append((y, op, sw, dash))
        y += step
    return out


def seam_defs():
    d = []
    for i, (_, _, dom) in enumerate(SEAMS):
        stops = ([(0, "#A8300C"), (0.18, "#F0682F"), (0.40, "#FFD9BD"),
                  (0.58, "#FF8B4F"), (1, "#B8380F")] if dom else
                 [(0, "#8E2A0A"), (0.26, "#DC5520"), (0.52, "#FF9260"), (1, "#A6320E")])
        d.append('<linearGradient id="seam%d" x1="%d" y1="0" x2="%d" y2="0" '
                 'gradientUnits="userSpaceOnUse">%s</linearGradient>'
                 % (i, X0, X1, "".join('<stop offset="%s" stop-color="%s"/>' % s for s in stops)))
    return "\n    ".join(d)


sheets = "\n".join(
    '      <g opacity="%.2f"><ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="url(#sheet)"/>'
    '<path d="M %d %d C %d %.1f, %d %.1f, %d %d" stroke="#FFFFFF" stroke-opacity="0.32" '
    'stroke-width="2.4" fill="none"/></g>'
    % (op, CX + dx, y, rx, ry,
       CX + dx - rx, y, CX + dx - rx, y - ry * 1.34, CX + dx + rx, y - ry * 1.34, CX + dx + rx, y)
    for y, ry, rx, dx, op in SHEETS)

hairs = "\n".join('          <path d="%s" stroke-width="%.1f" stroke-opacity="%.3f"%s/>'
                  % (arc(y), sw, op, dash) for y, op, sw, dash in strata())

seams = "\n".join('        <path d="%s" stroke="url(#seam%d)" stroke-width="%d" fill="none" '
                  'stroke-linecap="round"/>' % (arc(sy), i, w)
                  for i, (sy, w, _) in enumerate(SEAMS))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>compaction-quality</title>
  <defs>
    <clipPath id="squircle"><path d="{squircle()}"/></clipPath>
    <clipPath id="bodyClip"><path d="{BODY}"/></clipPath>

    <radialGradient id="tile" cx="0.36" cy="0.27" r="0.94">
      <stop offset="0" stop-color="#FFFFFE"/>
      <stop offset="0.50" stop-color="#F7F5F1"/>
      <stop offset="1" stop-color="#E4E1DA"/>
    </radialGradient>
    <radialGradient id="vig" cx="0.5" cy="0.45" r="0.74">
      <stop offset="0.58" stop-color="#C4BCB0" stop-opacity="0"/>
      <stop offset="1" stop-color="#B5AA9A" stop-opacity="0.22"/>
    </radialGradient>
    <linearGradient id="sheet" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#DCD6CB"/>
      <stop offset="1" stop-color="#BEB6A8"/>
    </linearGradient>

    <linearGradient id="wall" x1="0" y1="330" x2="0" y2="820" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#636C73"/>
      <stop offset="0.26" stop-color="#3D454D"/>
      <stop offset="0.58" stop-color="#2B2823"/>
      <stop offset="0.84" stop-color="#1D1714"/>
      <stop offset="1" stop-color="#150F0C"/>
    </linearGradient>
    <linearGradient id="round" x1="{X0}" y1="0" x2="{X1}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.44"/>
      <stop offset="0.15" stop-color="#000000" stop-opacity="0.13"/>
      <stop offset="0.36" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="0.70" stop-color="#000000" stop-opacity="0.07"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.36"/>
    </linearGradient>
    <radialGradient id="topface" cx="0.36" cy="0.30" r="0.95">
      <stop offset="0" stop-color="#6D757B"/>
      <stop offset="0.58" stop-color="#525A60"/>
      <stop offset="1" stop-color="#3E464C"/>
    </radialGradient>
    <!-- the gel visibly warms where the dominant seam glows through it -->
    <linearGradient id="bleed" x1="0" y1="{DOM_Y - BLEED_H}" x2="0" y2="{DOM_Y + BLEED_H}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#C24E1E" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#DC5E24" stop-opacity="0.40"/>
      <stop offset="1" stop-color="#B8461B" stop-opacity="0"/>
    </linearGradient>
    {seam_defs()}

    <filter id="soft" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="softer" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="44"/></filter>
    <filter id="tight" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="7"/></filter>
    <filter id="rim" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>

  <g clip-path="url(#squircle)">

    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#tile)"/>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>
      <path d="{squircle()}" fill="none" stroke="#FFFFFF" stroke-opacity="0.62" stroke-width="9" filter="url(#rim)"/>
      <path d="{squircle()}" fill="none" stroke="#BCB09C" stroke-opacity="0.20" stroke-width="2.5"/>
    </g>

    <g id="mid">
      <!-- warm spill from the glowing seam onto the porcelain floor -->
      <ellipse cx="{CX}" cy="842" rx="286" ry="34" fill="#FF7233" opacity="0.32" filter="url(#softer)"/>
      <!-- contact shadow, one light source -->
      <ellipse cx="{CX}" cy="836" rx="342" ry="32" fill="#2E2419" opacity="0.30" filter="url(#soft)"/>
      <ellipse cx="{CX}" cy="828" rx="272" ry="15" fill="#211710" opacity="0.30" filter="url(#tight)"/>
      <!-- the discarded bulk: loose sheets still shedding off the top -->
{sheets}
    </g>

    <g id="fg">
      <!-- carrying silhouette: one filled shape, identity survives tinting -->
      <path d="{BODY}" fill="url(#wall)"/>
      <g clip-path="url(#bodyClip)">
        <path d="{BODY}" fill="url(#round)"/>
        <rect x="{X0}" y="{DOM_Y - BLEED_H}" width="{HW * 2}" height="{BLEED_H * 2}" fill="url(#bleed)" filter="url(#soft)"/>
        <!-- hundreds of layers, tightening with depth, some pinching out -->
        <g fill="none" stroke="#A8B1B8" stroke-linecap="round">
{hairs}
        </g>
        <!-- the load-bearing five -->
{seams}
      </g>
      <!-- cored top face -->
      <ellipse cx="{CX}" cy="362" rx="236" ry="33" fill="url(#topface)"/>
      <g fill="none" stroke="#8D969D" stroke-opacity="0.16">
        <ellipse cx="{CX}" cy="362" rx="184" ry="25.5"/>
        <ellipse cx="{CX}" cy="362" rx="134" ry="18.5"/>
        <ellipse cx="{CX}" cy="362" rx="86" ry="12"/>
        <ellipse cx="{CX}" cy="362" rx="42" ry="6"/>
      </g>
    </g>

    <g id="highlight">
      <g clip-path="url(#bodyClip)">
        <!-- emissive interior: the seam blooms out through the gel -->
        <path d="{arc(DOM_Y)}" stroke="#FF8046" stroke-width="74" fill="none" opacity="0.62" filter="url(#tight)"/>
        <path d="{arc(DOM_Y)}" stroke="#FF6C33" stroke-width="128" fill="none" opacity="0.32" filter="url(#soft)"/>
        <path d="{arc(DOM_Y)}" stroke="#FF5E22" stroke-width="248" fill="none" opacity="0.10" filter="url(#softer)"/>
        <path d="{arc(DOM_Y)}" stroke="#FFEDDC" stroke-width="10" fill="none" opacity="0.86"/>
        <!-- the secondary seam catches some of it -->
        <path d="{arc(SEC_Y)}" stroke="#FF7A45" stroke-width="34" fill="none" opacity="0.30" filter="url(#tight)"/>
        <path d="{arc(SEC_Y)}" stroke="#FFD4B4" stroke-width="3" fill="none" opacity="0.55"/>
        <!-- one soft top-left sheen -->
        <ellipse cx="316" cy="452" rx="150" ry="108" fill="#FFFFFF" opacity="0.08" filter="url(#soft)"/>
        <!-- bounce off the porcelain floor separates the base from its own shadow -->
        <path d="M {X0} {SHOULDER_B} C {X0} {SHOULDER_B + K_BOT - 4}, {X1} {SHOULDER_B + K_BOT - 4}, {X1} {SHOULDER_B}"
              stroke="#B0A48E" stroke-width="9" fill="none" opacity="0.34" filter="url(#tight)"/>
      </g>
      <!-- shoulder rim catches the top light -->
      <path d="M {X0} {SHOULDER_T} C {X0} {SHOULDER_T - K_TOP}, {X1} {SHOULDER_T - K_TOP}, {X1} {SHOULDER_T}"
            stroke="#FFFFFF" stroke-width="5" fill="none" opacity="0.30" filter="url(#rim)"/>
      <ellipse cx="{CX}" cy="362" rx="236" ry="33" fill="none" stroke="#AEB7BE" stroke-width="3"
               opacity="0.34" filter="url(#rim)"/>
      <path d="M {X0 + 1.5} 424 L {X0 + 1.5} 706" stroke="#98A1A8" stroke-width="3" opacity="0.34" filter="url(#rim)"/>
      <path d="M {X1 - 1.5} 424 L {X1 - 1.5} 706" stroke="#98A1A8" stroke-width="3" opacity="0.28" filter="url(#rim)"/>
    </g>

  </g>
</svg>
'''

out = sys.argv[1] if len(sys.argv) > 1 else "icon.svg"
open(out, "w").write(svg)
print("wrote", out)
