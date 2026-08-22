#!/usr/bin/env python3
"""Engine A, take 2 — the runner-up direction, kept as the sheet's comparison.

THE GLYPH: the port register. A harbourmaster's other instrument is the book
that says which berth is taken and by what. Drawn as a card of berth rows seen
flat-on, three filled with an ember bar and two empty, with the card's own edge
lifted off the ground.

WHY IT DOES NOT SHIP: a card of rows is a category glyph — it says "a list" and
"records", which is the smallest of this skill's three jobs and the one a dozen
other icons already claim. It also has no vertical anchor, so at 16px it reduces
to a horizontal smear with a warm streak, where the tower keeps a silhouette.
Kept because the comparison is the point: it is the strongest alternative, and
seeing it lose on identity rather than on execution is what makes the tower's
selection an argument instead of a preference.
"""
from __future__ import annotations
import pathlib

S = 1024
HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE / "squircle-path.txt").read_text().strip()

CARD_X, CARD_Y = 178.0, 246.0
CARD_W, CARD_H = 668.0, 532.0
ROW_H, ROW_GAP = 74.0, 26.0
ROWS = (True, True, True, False, False)
PAD = 54.0
BAR_W = 132.0

GROUND_HI, GROUND_MID, GROUND_LO = "#FDFCF9", "#F6F4EF", "#E5E0D6"
VIGNETTE = "#8B8070"
CARD_HI, CARD_LO = "#FFFFFF", "#EDE7DB"
RULE = "#D9D0BF"
GRAPHITE_MID, GRAPHITE_LO = "#3A4551", "#232D39"
EMBER_HI, EMBER_MID, EMBER_LO = "#F98A45", "#EC6640", "#C4441F"


def rows() -> str:
    out = []
    for i, lit in enumerate(ROWS):
        y = CARD_Y + PAD + i * (ROW_H + ROW_GAP)
        bar = f'<rect x="{CARD_X + PAD:.1f}" y="{y:.1f}" width="{BAR_W}" height="{ROW_H}" rx="12" ' \
              f'fill="{"url(#ember)" if lit else GRAPHITE_LO}"/>'
        tail_w = CARD_W - PAD * 2 - BAR_W - 30
        tail = f'<rect x="{CARD_X + PAD + BAR_W + 30:.1f}" y="{y + ROW_H/2 - 9:.1f}" ' \
               f'width="{tail_w:.1f}" height="18" rx="9" fill="{RULE}" ' \
               f'opacity="{0.95 if lit else 0.55}"/>'
        out.append(bar + tail)
    return "".join(out)


def svg() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <clipPath id="tile"><path d="{SQUIRCLE}"/></clipPath>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_HI}"/><stop offset=".55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_LO}"/>
    </linearGradient>
    <radialGradient id="vign" cx=".5" cy=".42" r=".78">
      <stop offset=".62" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".20"/>
    </radialGradient>
    <linearGradient id="card" x1="0" y1="0" x2=".4" y2="1">
      <stop offset="0" stop-color="{CARD_HI}"/><stop offset="1" stop-color="{CARD_LO}"/>
    </linearGradient>
    <linearGradient id="ember" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{EMBER_HI}"/><stop offset=".7" stop-color="{EMBER_MID}"/>
      <stop offset="1" stop-color="{EMBER_LO}"/>
    </linearGradient>
    <radialGradient id="drop" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#6B5F4E" stop-opacity=".38"/>
      <stop offset="1" stop-color="#6B5F4E" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <g clip-path="url(#tile)">
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vign)"/>
    </g>
    <g id="mid">
      <ellipse cx="{CARD_X + CARD_W/2:.1f}" cy="{CARD_Y + CARD_H + 26:.1f}" rx="330" ry="52"
               fill="url(#drop)"/>
    </g>
    <g id="fg">
      <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="34" fill="url(#card)"/>
      <rect x="{CARD_X}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="34" fill="none"
            stroke="{GRAPHITE_MID}" stroke-width="9" stroke-opacity=".28"/>
      {rows()}
    </g>
    <g id="highlight">
      <rect x="{CARD_X + 14:.1f}" y="{CARD_Y + 12:.1f}" width="{CARD_W - 28:.1f}" height="5" rx="2.5"
            fill="#FFFFFF" opacity=".85"/>
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    out = HERE / "icon-engineA-register-r01.svg"
    out.write_text(svg())
    print(f"wrote {out}")
