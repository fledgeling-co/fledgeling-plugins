#!/usr/bin/env python3
"""build_icon.py — Engine A master for the `whats-left` icon.

Direction 2, sub-register (a): porcelain cushion + gel objects, in the
fledgeling-plugins house palette sampled from clarify and report
(ground #F7F4EC→#E5DECD, accent #DE5F2C, receded gel #A29686).

Concept — the remainder. Three settled rows recede up the tile, each carrying a
tick and each a little quieter than the one below it. Below a clear break, one
full-weight card stands forward on its own contact shadow, carrying a filled
vermilion dial. A list, mostly done, and the last thing on it is a decision.

Differentiated from `clarify`, which sits next to it in the marketplace: that
icon is three equal cards with one chosen. This one is a stack that thins out
upward with one thing left standing — read as progress, not as choice.

    python3 build_icon.py > icon.svg
"""

import pathlib
import sys

SQ = (pathlib.Path(__file__).resolve().parents[2] / "create-mac-icon" / "assets"
      / "squircle-path.txt")

# ── palette, sampled from the siblings ──────────────────────────────────────
GROUND_TOP, GROUND_BOT = "#F8F5EE", "#E4DDCB"
RIM = "#FFFDF8"
GEL, GEL_DARK = "#A89C8B", "#8D8170"
CARD, CARD_TOP = "#FBF8F1", "#FFFFFF"
CARD_EDGE = "#D9D1BF"
ACCENT, ACCENT_HI = "#DE5F2C", "#F0854F"
INK = "#6E6455"
ROW_INK = "#5F5648"

# ── geometry ────────────────────────────────────────────────────────────────
LEFT = 258                      # settled rows share a left margin: it is a list
ROWS = [                        # (y, width, opacity) — quieter and shorter upward
    (238, 372, 0.46),
    (346, 438, 0.66),
    (454, 500, 0.88),
]
ROW_H, ROW_R = 76, 38
CARD_X, CARD_Y, CARD_W, CARD_H, CARD_R = 208, 606, 620, 172, 48
DIAL_CX, DIAL_CY, DIAL_R = 300, 692, 38


def rows() -> str:
    out = []
    for y, w, op in ROWS:
        cy = y + ROW_H / 2
        # tick, drawn chunky enough to survive 32px
        tx = LEFT + 40
        out.append(f"""
    <g opacity="{op}">
      <rect x="{LEFT}" y="{y}" width="{w}" height="{ROW_H}" rx="{ROW_R}" fill="{GEL_DARK}"/>
      <rect x="{LEFT}" y="{y}" width="{w - 0}" height="{ROW_H - 8}" rx="{ROW_R}" fill="url(#gel)"/>
      <rect x="{LEFT}" y="{y}" width="{w}" height="{ROW_H / 2:.0f}" rx="{ROW_R}" fill="{RIM}" opacity=".16"/>
      <path d="M{tx - 17} {cy + 1} l13 14 l24 -29" fill="none" stroke="{GROUND_TOP}"
            stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
      <rect x="{tx + 52}" y="{cy - 9}" width="{max(60, w - 152):.0f}" height="18" rx="9"
            fill="{ROW_INK}" opacity=".5"/>
    </g>""")
    return "".join(out)


def svg() -> str:
    d = SQ.read_text().strip() if SQ.exists() else ""
    if not d:
        print("squircle-path.txt not found — the family shares one silhouette", file=sys.stderr)
        raise SystemExit(1)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/><stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vig" cx=".5" cy=".42" r=".78">
      <stop offset=".55" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#4A3F2E" stop-opacity=".17"/>
    </radialGradient>
    <linearGradient id="gel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GEL}"/><stop offset="1" stop-color="{GEL_DARK}"/>
    </linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{CARD_TOP}"/><stop offset=".55" stop-color="{CARD}"/>
      <stop offset="1" stop-color="#F2EDE1"/>
    </linearGradient>
    <linearGradient id="dial" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{ACCENT_HI}"/><stop offset="1" stop-color="{ACCENT}"/>
    </linearGradient>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="17"/>
    </filter>
    <filter id="contact" x="-30%" y="-40%" width="160%" height="200%">
      <feGaussianBlur stdDeviation="13"/>
    </filter>
    <clipPath id="mask"><path d="{d}"/></clipPath>
  </defs>

  <g clip-path="url(#mask)">
    <!-- cushion tile: ramp, vignette, inner rim light -->
    <rect width="1024" height="1024" fill="url(#ground)"/>
    <rect width="1024" height="1024" fill="url(#vig)"/>
    <path d="{d}" fill="none" stroke="{RIM}" stroke-width="7" opacity=".82"/>

    <!-- settled: three rows, ticked, thinning upward -->
    <g filter="url(#soft)" opacity=".18">
      {"".join(f'<rect x="{LEFT}" y="{y + 9}" width="{w}" height="{ROW_H}" rx="{ROW_R}" fill="#4A3F2E" opacity="{op:.2f}"/>' for y, w, op in ROWS)}
    </g>
    {rows()}

    <!-- what is left: one card, forward, on its own contact shadow -->
    <g filter="url(#contact)" opacity=".34">
      <rect x="{CARD_X + 6}" y="{CARD_Y + 20}" width="{CARD_W}" height="{CARD_H}" rx="{CARD_R}" fill="#4A3F2E"/>
    </g>
    <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="{CARD_R}" fill="url(#card)"/>
    <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="{CARD_R}"
          fill="none" stroke="{CARD_EDGE}" stroke-width="3" opacity=".85"/>
    <path d="M{CARD_X + CARD_R} {CARD_Y + 3} h{CARD_W - 2 * CARD_R}" stroke="#FFF"
          stroke-width="6" stroke-linecap="round" opacity=".9"/>

    <!-- the decision, filled, warm: the one saturated thing on the tile -->
    <circle cx="{DIAL_CX}" cy="{DIAL_CY}" r="{DIAL_R + 5}" fill="{ACCENT}" opacity=".13"/>
    <circle cx="{DIAL_CX}" cy="{DIAL_CY}" r="{DIAL_R}" fill="url(#dial)"/>
    <path d="M{DIAL_CX - 19} {DIAL_CY - 20} a{DIAL_R} {DIAL_R} 0 0 1 27 -6" fill="none"
          stroke="#FFF" stroke-width="9" stroke-linecap="round" opacity=".45"/>
    <rect x="{DIAL_CX + 66}" y="{DIAL_CY - 15}" width="322" height="30" rx="15"
          fill="{INK}" opacity=".34"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    print(svg())
