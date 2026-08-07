#!/usr/bin/env python3
"""Builder for the Fledgeling brand icon — Engine A layered master.
Design-space geometry -> optical-centring affine -> layered 1024 SVG.
"""
import math, re, sys

# ---------------------------------------------------------------- squircle
def squircle(n=5.0, N=64, a=512.0, cx=512.0):
    def pt(t):
        c, s = math.cos(t), math.sin(t)
        return (cx + a * math.copysign(abs(c) ** (2.0 / n), c),
                cx + a * math.copysign(abs(s) ** (2.0 / n), s))
    P = [pt(2 * math.pi * i / N) for i in range(N)]
    f = lambda v: f"{v:.1f}".rstrip('0').rstrip('.')
    d = f"M{f(P[0][0])} {f(P[0][1])}"
    for i in range(N):
        p0, p1, p2, p3 = P[(i - 1) % N], P[i], P[(i + 1) % N], P[(i + 2) % N]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + " Z"

TILE = squircle()

# ------------------------------------------------- design-space geometry
S, DX, DY = 1.06, -12, 68

# stalk: confident wide base -> narrow sprouting tip that clears the upper leaf
STEM = ("M470 864 C456 736 452 604 525 464 A17 17 0 0 1 555 476 "
        "C534 604 528 736 546 856 A42 42 0 0 1 470 864 Z")
STEM_RIM = "M470 864 C456 736 452 604 525 464 A17 17 0 0 1 555 476"

# lower-left leaf/wing — blunt end tucked INSIDE the stalk, so it grows out of it
WING_LO = ("M268 556 C374 544 476 588 520 664 C512 700 500 724 486 734 "
           "C398 754 316 700 268 556 Z")
LO_RIM = "M268 556 C374 544 476 588 520 664"

# upper-right leaf/wing — slimmer, rising toward the ember
WING_HI = ("M500 586 C528 500 612 428 742 428 C716 512 638 566 552 592 "
           "C528 600 510 598 500 586 Z")
HI_RIM = "M500 586 C528 500 612 428 742 428"

EMBER = (752.0, 314.0, 54.0)

# ------------------------------------------------------------- transform
def tx(x, y):
    return ((x - 512.0) * S + 512.0 + DX, (y - 512.0) * S + 512.0 - DY)

_TOK = re.compile(r'[MLCAZ]|-?\d*\.?\d+')

def xform_path(d):
    out, toks, i, cmd = [], _TOK.findall(d), 0, None
    f = lambda v: f"{v:.1f}".rstrip('0').rstrip('.')
    while i < len(toks):
        t = toks[i]
        if t in ('M', 'L', 'C', 'A', 'Z'):
            cmd = t; i += 1
        if cmd == 'Z':
            out.append('Z'); continue
        if cmd in 'ML':
            X, Y = tx(float(toks[i]), float(toks[i + 1])); i += 2
            out.append(f"{cmd}{f(X)} {f(Y)}")
        elif cmd == 'C':
            pts = []
            for k in range(3):
                X, Y = tx(float(toks[i + 2 * k]), float(toks[i + 2 * k + 1])); pts += [f(X), f(Y)]
            i += 6; out.append("C" + " ".join(pts))
        elif cmd == 'A':
            rx, ry = float(toks[i]) * S, float(toks[i + 1]) * S
            rot, laf, sf = toks[i + 2], toks[i + 3], toks[i + 4]
            X, Y = tx(float(toks[i + 5]), float(toks[i + 6])); i += 7
            out.append(f"A{f(rx)} {f(ry)} {rot} {laf} {sf} {f(X)} {f(Y)}")
    return " ".join(out)

P = {k: xform_path(v) for k, v in dict(
    stem=STEM, stemRim=STEM_RIM, lo=WING_LO, loRim=LO_RIM, hi=WING_HI, hiRim=HI_RIM).items()}
EX, EY = tx(*EMBER[:2]); ER = EMBER[2] * S
fn = lambda v: f"{v:.1f}".rstrip('0').rstrip('.')

# ------------------------------------------------------------------ swatches
GROUND_HI, GROUND, GROUND_LO = "#3B362D", "#2A2620", "#211E19"
CREAM_LIT, CREAM, CREAM_DEEP = "#FFFCF5", "#EFE7D8", "#D3C6AF"
EMBER_HOT, EMBER_MID, EMBER_DEEP = "#F8B978", "#C4622D", "#9C4A1E"

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024" role="img" aria-label="Fledgeling">
  <title>Fledgeling</title>
  <defs>
    <!-- ground: a cushion, not a print — lifted at the top, vignetted into the corners -->
    <linearGradient id="ground" x1="0" y1="0" x2="0.12" y2="1">
      <stop offset="0" stop-color="{GROUND_HI}"/>
      <stop offset="0.55" stop-color="{GROUND}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </linearGradient>
    <radialGradient id="vignette" cx="50%" cy="42%" r="74%">
      <stop offset="0.5" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.10"/>
    </radialGradient>
    <linearGradient id="tileRim" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="#FFF8EA" stop-opacity="0.22"/>
      <stop offset="0.4" stop-color="#FFF8EA" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFF8EA" stop-opacity="0.04"/>
    </linearGradient>

    <!-- glyph: poured cream gel, one soft top light. Each form lit on its own axis. -->
    <linearGradient id="gelStem" x1="0.1" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{CREAM_LIT}"/>
      <stop offset="0.40" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="{CREAM_DEEP}"/>
    </linearGradient>
    <linearGradient id="gelLo" x1="0.25" y1="0" x2="0.62" y2="1">
      <stop offset="0" stop-color="{CREAM_LIT}"/>
      <stop offset="0.38" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="{CREAM_DEEP}"/>
    </linearGradient>
    <linearGradient id="gelHi" x1="0.2" y1="0" x2="0.55" y2="1">
      <stop offset="0" stop-color="{CREAM_LIT}"/>
      <stop offset="0.42" stop-color="{CREAM}"/>
      <stop offset="1" stop-color="{CREAM_DEEP}"/>
    </linearGradient>
    <linearGradient id="rim" x1="0.15" y1="0" x2="0.7" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="0.45" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.85" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="emberCore" cx="35%" cy="28%" r="80%">
      <stop offset="0" stop-color="{EMBER_HOT}"/>
      <stop offset="0.52" stop-color="{EMBER_MID}"/>
      <stop offset="1" stop-color="{EMBER_DEEP}"/>
    </radialGradient>
    <radialGradient id="emberHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0.2" stop-color="#E8823A" stop-opacity="0.30"/>
      <stop offset="0.55" stop-color="#C4622D" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#C4622D" stop-opacity="0"/>
    </radialGradient>

    <filter id="ao" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="15"/></filter>
    <filter id="cast" x="-25%" y="-25%" width="150%" height="150%"><feGaussianBlur stdDeviation="12"/></filter>
    <filter id="rimBlur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4"/></filter>
    <filter id="spec" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="8"/></filter>

    <path id="tileShape" d="{TILE}"/>
    <clipPath id="clipTile"><use href="#tileShape"/></clipPath>
    <clipPath id="clipStem"><path d="{P['stem']}"/></clipPath>
    <clipPath id="clipLo"><path d="{P['lo']}"/></clipPath>
    <clipPath id="clipHi"><path d="{P['hi']}"/></clipPath>
    <clipPath id="clipEmber"><circle cx="{fn(EX)}" cy="{fn(EY)}" r="{fn(ER)}"/></clipPath>
  </defs>

  <!-- ===== bg — the cushion tile ===== -->
  <g id="bg">
    <use href="#tileShape" fill="url(#ground)"/>
    <use href="#tileShape" fill="url(#vignette)"/>
    <g clip-path="url(#clipTile)">
      <use href="#tileShape" fill="none" stroke="url(#tileRim)" stroke-width="7"/>
    </g>
  </g>

  <!-- ===== mid — the object's shadow on the tile + ember halo (both droppable) ===== -->
  <g id="mid">
    <g filter="url(#ao)" fill="#0F0C08" fill-opacity="0.38" transform="translate(0 14)">
      <path d="{P['stem']}"/><path d="{P['lo']}"/><path d="{P['hi']}"/>
    </g>
    <circle cx="{fn(EX)}" cy="{fn(EY)}" r="{fn(ER * 2.1)}" fill="url(#emberHalo)"/>
  </g>

  <!-- ===== fg — one poured object: stalk, two leaves growing out of it, ember ===== -->
  <g id="fg">
    <path id="stem" d="{P['stem']}" fill="url(#gelStem)" fill-opacity="0.97"/>

    <!-- lower leaf casts onto the stalk, then sits on it -->
    <g clip-path="url(#clipStem)">
      <path d="{P['lo']}" fill="#6B5230" fill-opacity="0.22" filter="url(#cast)" transform="translate(4 9)"/>
    </g>
    <path id="wing-lower" d="{P['lo']}" fill="url(#gelLo)" fill-opacity="0.97"/>

    <!-- upper leaf: the most translucent form — the stalk telegraphs faintly through it -->
    <g clip-path="url(#clipStem)">
      <path d="{P['hi']}" fill="#6B5230" fill-opacity="0.20" filter="url(#cast)" transform="translate(4 8)"/>
    </g>
    <path id="wing-upper" d="{P['hi']}" fill="url(#gelHi)" fill-opacity="0.95"/>

    <circle id="ember" cx="{fn(EX)}" cy="{fn(EY)}" r="{fn(ER)}" fill="url(#emberCore)"/>
  </g>

  <!-- ===== highlight — rim light on the lit edges only, ember bloom ===== -->
  <g id="highlight">
    <g clip-path="url(#clipStem)">
      <path d="{P['stemRim']}" fill="none" stroke="url(#rim)" stroke-width="9" filter="url(#rimBlur)"/>
    </g>
    <g clip-path="url(#clipLo)">
      <path d="{P['loRim']}" fill="none" stroke="url(#rim)" stroke-width="9" filter="url(#rimBlur)"/>
    </g>
    <g clip-path="url(#clipHi)">
      <path d="{P['hiRim']}" fill="none" stroke="url(#rim)" stroke-width="9" filter="url(#rimBlur)"/>
    </g>
    <g clip-path="url(#clipEmber)">
      <circle cx="{fn(EX)}" cy="{fn(EY)}" r="{fn(ER)}" fill="none"
              stroke="#FFE8C6" stroke-opacity="0.6" stroke-width="8" filter="url(#rimBlur)"/>
    </g>
    <ellipse cx="{fn(EX - ER * 0.28)}" cy="{fn(EY - ER * 0.40)}" rx="{fn(ER * 0.32)}" ry="{fn(ER * 0.23)}"
             fill="#FFF0D6" fill-opacity="0.6" filter="url(#spec)"/>
  </g>
</svg>
'''

out = sys.argv[1] if len(sys.argv) > 1 else "/Users/lukerhodes/Dev/fledgeling-plugins/assets/fledgeling-icon.svg"
open(out, "w").write(SVG)
print(f"wrote {out} ({len(SVG)} bytes)")
