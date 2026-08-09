#!/usr/bin/env python3
"""Engine A — the hand-authored layered SVG master for the token-discipline icon.

Direction: "The Set Stop". Geometry and material live as named constants so a fidelity round is a
parameter edit, not path surgery.

Material sampled from references/corpus/apple-2026/apple-19.png (Slack: porcelain cushion carrying
saturated gel capsules) rather than assumed:
  - near-white centre falling to a soft vignette, plus an inner rim light at the very edge
  - each gel body carries a thin BRIGHT rim on its top edge and a DARKER side wall at its bottom,
    which is what makes it read extruded rather than printed
  - contact shadows are tight, short and directly beneath; zero hard speculars
  - one hue family per object, carried as a value ramp, never a hue shift

Warm scene: the accent is vermilion and the light is warm, so every shadow is warm-biased.

ROUND 2 — what the first render got wrong, read off the render rather than reasoned about:
  1. It read as a CHESS ROOK. The shaft stopped AT the ring, so the parts stacked instead of one
     passing through the others. Fix: the shaft now runs THROUGH the guide and its tip shows below,
     which is the whole difference between a stop and a stack.
  2. The guide was a wide pedestal, which is what supplied the trophy read. Fix: narrower than the
     collar, so the silhouette steps OUT at the accent and back IN below it.
  3. Uniform graduations read as grip ribs. Fix: alternating long/short rules — the thing that says
     "scale" rather than "texture".
  4. The guide is now translucent frosted glass with the shaft visible, cooled, inside it. Authored
     overlap is the era's craft tell and the one thing a flat raster cannot fake.

Layers map 1:1 onto the #10 plan: #bg / #mid / #fg / #highlight.
"""
from pathlib import Path

W = 1024
SQUIRCLE = (Path(__file__).parent / "squircle-path.txt").read_text().strip()

# ---- Geometry -------------------------------------------------------------------------------
# Silhouette steps: shaft (narrow) -> collar (widest, and it is the accent) -> guide (mid) -> tip.
# The accent sits at the widest step so the eye lands on the thing that stopped the travel.
SHAFT_W = 236
SHAFT_X = (W - SHAFT_W) / 2
SHAFT_TOP, SHAFT_BOT = 214, 830                 # runs through everything; tip shows below the guide
SHAFT_R = SHAFT_W / 2

COLLAR_W, COLLAR_H = 452, 112
COLLAR_X, COLLAR_Y = (W - COLLAR_W) / 2, 540
COLLAR_R = 30

GUIDE_W, GUIDE_H = 360, 178
GUIDE_X, GUIDE_Y = (W - GUIDE_W) / 2, COLLAR_Y + COLLAR_H   # hard contact, no gap
GUIDE_R = 32

# Graduations: alternating long/short, so it reads as a scale and not as a grip.
GRAD_TOP, GRAD_COUNT, GRAD_GAP = 292, 6, 38

GROUND = ("#FFFDFA", "#F7F4EE", "#EBE6DC")
VIGNETTE = "#8A7A5E"
GRAPHITE = ("#79818A", "#4A525B", "#2E353D", "#212730")
VERMILION = ("#FB8A5E", "#F0603A", "#D8431F", "#A82C0C")
SHADOW = "#6E5636"


def rr(x, y, w, h, r, **kw):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{r:.1f}"{extra}/>')


def build() -> str:
    grads = ""
    for i in range(GRAD_COUNT):
        long_ = i % 2 == 0
        inset = 30 if long_ else 52
        grads += (f'<rect x="{SHAFT_X + inset:.1f}" y="{GRAD_TOP + i * GRAD_GAP:.1f}" '
                  f'width="{SHAFT_W - 2 * inset:.1f}" height="{6 if long_ else 5}" rx="3" '
                  f'fill="#9AA2AB" opacity="{0.52 if long_ else 0.32:.2f}"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
<defs>
  <clipPath id="squircle"><path d="{SQUIRCLE}"/></clipPath>
  <clipPath id="guideClip">{rr(GUIDE_X, GUIDE_Y, GUIDE_W, GUIDE_H, GUIDE_R)}</clipPath>

  <radialGradient id="ground" cx="50%" cy="36%" r="78%">
    <stop offset="0%" stop-color="{GROUND[0]}"/>
    <stop offset="58%" stop-color="{GROUND[1]}"/>
    <stop offset="100%" stop-color="{GROUND[2]}"/>
  </radialGradient>
  <radialGradient id="vignette" cx="50%" cy="42%" r="76%">
    <stop offset="70%" stop-color="{VIGNETTE}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{VIGNETTE}" stop-opacity="0.20"/>
  </radialGradient>

  <linearGradient id="shaft" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{GRAPHITE[2]}"/>
    <stop offset="24%" stop-color="{GRAPHITE[1]}"/>
    <stop offset="60%" stop-color="{GRAPHITE[1]}"/>
    <stop offset="100%" stop-color="{GRAPHITE[3]}"/>
  </linearGradient>
  <linearGradient id="collar" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{VERMILION[0]}"/>
    <stop offset="30%" stop-color="{VERMILION[1]}"/>
    <stop offset="76%" stop-color="{VERMILION[2]}"/>
    <stop offset="100%" stop-color="{VERMILION[3]}"/>
  </linearGradient>
  <linearGradient id="guide" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
    <stop offset="45%" stop-color="#F4F1EA" stop-opacity="0.72"/>
    <stop offset="100%" stop-color="#DCD6C9" stop-opacity="0.86"/>
  </linearGradient>
  <linearGradient id="bloom" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{VERMILION[2]}" stop-opacity="0.50"/>
    <stop offset="100%" stop-color="{VERMILION[2]}" stop-opacity="0"/>
  </linearGradient>

  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="17"/>
  </filter>
  <filter id="tight" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="7"/>
  </filter>
</defs>

<g clip-path="url(#squircle)">
  <g id="bg">
    <rect width="{W}" height="{W}" fill="url(#ground)"/>
    <rect width="{W}" height="{W}" fill="url(#vignette)"/>
  </g>

  <g id="mid">
    <ellipse cx="{W/2}" cy="{GUIDE_Y + GUIDE_H + 14:.1f}" rx="{GUIDE_W*0.60:.1f}" ry="26"
             fill="{SHADOW}" opacity="0.38" filter="url(#soft)"/>
    <rect x="{COLLAR_X - 4:.1f}" y="{COLLAR_Y + COLLAR_H - 12:.1f}" width="{COLLAR_W + 8:.1f}"
          height="28" rx="14" fill="{SHADOW}" opacity="0.32" filter="url(#tight)"/>
  </g>

  <g id="fg">
    <!-- the shaft, drawn once, full length: it PASSES THROUGH rather than stacking -->
    <g fill="url(#shaft)">{rr(SHAFT_X, SHAFT_TOP, SHAFT_W, SHAFT_BOT - SHAFT_TOP, SHAFT_R)}</g>
    {grads}

    <!-- the guide: translucent frosted glass. The shaft inside it is cooled and dimmed, which is
         the authored overlap — real transparency between real layers. -->
    <g clip-path="url(#guideClip)">
      <rect x="{SHAFT_X:.1f}" y="{GUIDE_Y:.1f}" width="{SHAFT_W:.1f}" height="{GUIDE_H:.1f}"
            fill="#8B939C" opacity="0.55"/>
    </g>
    <g fill="url(#guide)">{rr(GUIDE_X, GUIDE_Y, GUIDE_W, GUIDE_H, GUIDE_R)}</g>
    {rr(GUIDE_X, GUIDE_Y, GUIDE_W, GUIDE_H, GUIDE_R, fill="none", stroke="#B9AF9C", stroke_width="3", opacity="0.85")}
    <rect x="{GUIDE_X + 8:.1f}" y="{GUIDE_Y:.1f}" width="{GUIDE_W - 16:.1f}" height="30"
          rx="15" fill="url(#bloom)"/>

    <!-- the collar: the accent, and the widest step -->
    <g fill="url(#collar)">{rr(COLLAR_X, COLLAR_Y, COLLAR_W, COLLAR_H, COLLAR_R)}</g>
  </g>

  <g id="highlight" fill="#FFFFFF">
    <rect x="{SHAFT_X + 20:.1f}" y="{SHAFT_TOP + 11:.1f}" width="{SHAFT_W - 40:.1f}" height="7"
          rx="3.5" opacity="0.42"/>
    <rect x="{COLLAR_X + 20:.1f}" y="{COLLAR_Y + 6:.1f}" width="{COLLAR_W - 40:.1f}" height="8"
          rx="4" opacity="0.55"/>
    <rect x="{GUIDE_X + 20:.1f}" y="{GUIDE_Y + 5:.1f}" width="{GUIDE_W - 40:.1f}" height="6"
          rx="3" opacity="0.40"/>
    <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.55"/>
  </g>
</g>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent / "icon.svg"
    out.write_text(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
