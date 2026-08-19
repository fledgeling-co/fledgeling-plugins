#!/usr/bin/env python3
"""Take A1 — "The Fold", in porcelain. The superseded master, kept whole.

This artwork shipped from 9 Aug 2026 to 19 Aug 2026 as `icon.svg`. On 19 Aug the user
chose the inverted take over it and it was renamed rather than deleted: it writes
`icon-A1-porcelain.svg` and rasterises nothing, so running it cannot touch the shipped
`icon.png` / `icon-256.png` / `icon-128.png`. The shipping master is `icon.svg`, built
by `build_icon.py`.

It was not displaced for losing the audit — it scored 11/12, the same as the take that
replaced it, and the audit's own recommendation was to keep it. It was displaced because
its one failure is in the register everyone sees: 1.04:1 sheet-to-ground on Default,
4 grayscale levels of 255, held together by drop shadows and a 2.5px hairline. On Dark
the same artwork measures 11.72:1, which is the strength it takes with it.

Direction "The Fold": one sheet, creased once across its width, doing two things at
once. Above the crease it is a single uninterrupted column of ruling — the report as it
reads on screen, continuous, no seams. Below the crease the same sheet has separated
into two stacked leaves, each carrying a shorter run of ruling — the same document
paginated onto A4. The crease is the only place the two states meet and it is where the
colour comes out.

That is the skill's whole architecture in one silhouette: one source, two renderings.
It is deliberately NOT dossier-report's icon, which is a page with a diagonal corner
flap. This crease is horizontal, spans the full width, and what it reveals is a stack
rather than an underside — different axis, different object, same family.

Legibility at 32px was the constraint that set every proportion: two leaves rather
than five, one crease rather than a fold sequence, ruling that reads as texture rather
than as countable lines. The silhouette survives flattening to a single tone.
`icon-notes.md` records why the first cut's three leaves became two; this docstring said
three for a file that has always drawn `range(2)`, and was corrected on 19 Aug.

Layers are the named groups bg / mid / fg / highlight in the output. They used to be
XML comments with those words in them, which read as a layer plan and satisfied nothing:
`fidelity.py structure` counts `<g id=…>` and reported zero. A fidelity round is a
parameter edit here, never path surgery in the output.
"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE.parent.parent / "create-mac-icon" / "assets" / "squircle-path.txt")
OUT = "icon-A1-porcelain.svg"

# ── geometry ────────────────────────────────────────────────────────────────────────
S = 1024
SHEET_X, SHEET_W = 236.0, 552.0          # the sheet, centred with optical breathing room
SHEET_Y = 142.0
CREASE_Y = 505.0                          # low enough that the scroll half reads as the subject
LEAF_H = 122.0                             # each paginated leaf
LEAF_STEP_X = 34.0
LEAF_INSET = 46.0   # the paginated half is narrower than the scroll half, so the
                    # silhouette itself steps — the one difference that survives 32px                        # lateral step of the stack
LEAF_GAP = 56.0
CORNER = 16.0

RULE_X_PAD = 58.0
LEAF_RULE_PAD = 40.0
RULE_H = 15.0
RULE_R = 7.5

# ── palette: warm porcelain ground, vermilion accent (the family's one warm note) ──
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFDF8", "#F7F2E9", "#EFE8DB"
PAPER_HI, PAPER_LO = "#FFFEFC", "#F2ECE1"
PAPER_EDGE = "#DCD2BF"
RULE_INK = "#B4AA96"
ACCENT_HI, ACCENT_MID, ACCENT_LO = "#F4763F", "#E2521F", "#C03A0E"


def rule(x, y, w):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{RULE_H}" rx="{RULE_R}"/>'


def build() -> str:
    squircle = SQUIRCLE.read_text().strip()
    rx = SHEET_X + RULE_X_PAD
    rw_full = SHEET_W - RULE_X_PAD * 2

    # Above the crease: one continuous column. Uneven lengths so it reads as prose,
    # not as a placeholder block.
    scroll = []
    y = SHEET_Y + 96
    for frac in (1.0, 0.92, 1.0, 0.78, 0.96, 0.88, 0.55):
        scroll.append(rule(rx, y, rw_full * frac))
        y += 40

    # Below the crease: three leaves, each stepping right, each with two short runs.
    leaves, leaf_rules = [], []
    ly = CREASE_Y + 58
    for i in range(2):
        lx = SHEET_X + LEAF_INSET + LEAF_STEP_X * i
        lw = SHEET_W - LEAF_INSET * 2 - LEAF_STEP_X * 2 * i
        leaves.append(
            f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{LEAF_H:.1f}" '
            f'rx="{CORNER}" fill="url(#paper)" stroke="{PAPER_EDGE}" stroke-width="2.5"/>'
        )
        for j, frac in enumerate((0.88, 0.60)):
            leaf_rules.append(
                rule(lx + LEAF_RULE_PAD, ly + 34 + j * 44, (lw - LEAF_RULE_PAD * 2) * frac)
            )
        ly += LEAF_H + LEAF_GAP

    scroll_h = CREASE_Y - SHEET_Y

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<defs>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="{S}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{GROUND_HI}"/><stop offset="0.54" stop-color="{GROUND_MID}"/>
    <stop offset="1" stop-color="{GROUND_LO}"/></linearGradient>
  <radialGradient id="crown" cx="420" cy="110" r="760" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
    <stop offset="0.56" stop-color="#FFFFFF" stop-opacity="0.18"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
  <radialGradient id="vig" cx="512" cy="500" r="700" gradientUnits="userSpaceOnUse">
    <stop offset="0.62" stop-color="#9C8B70" stop-opacity="0"/>
    <stop offset="1" stop-color="#9C8B70" stop-opacity="0.14"/></radialGradient>
  <linearGradient id="paper" x1="{SHEET_X}" y1="{SHEET_Y}" x2="{SHEET_X+SHEET_W}" y2="900"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{PAPER_HI}"/><stop offset="1" stop-color="{PAPER_LO}"/></linearGradient>
  <linearGradient id="crease" x1="{SHEET_X}" y1="{CREASE_Y}" x2="{SHEET_X+SHEET_W}" y2="{CREASE_Y+38}"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{ACCENT_LO}"/><stop offset="0.42" stop-color="{ACCENT_MID}"/>
    <stop offset="1" stop-color="{ACCENT_HI}"/></linearGradient>
  <linearGradient id="creaseRoll" x1="0" y1="{CREASE_Y}" x2="0" y2="{CREASE_Y+38}"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#FFD9C2" stop-opacity="0.85"/>
    <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.10"/>
    <stop offset="1" stop-color="#7E1A02" stop-opacity="0.28"/></linearGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="20"/></filter>
  <filter id="tight" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="tile"><path d="{squircle}"/></clipPath>
</defs>

<g id="art" clip-path="url(#tile)">
  <g id="bg">
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#crown)"/>
  </g>

  <!-- mid: the sheet's cast shadow, then the continuous half -->
  <g id="mid">
    <g filter="url(#soft)" opacity="0.30">
      <rect x="{SHEET_X+10}" y="{SHEET_Y+26}" width="{SHEET_W}" height="{scroll_h+250}"
            rx="{CORNER}" fill="#6B5A3E"/>
    </g>
    <rect x="{SHEET_X}" y="{SHEET_Y}" width="{SHEET_W}" height="{scroll_h:.1f}"
          rx="{CORNER}" fill="url(#paper)" stroke="{PAPER_EDGE}" stroke-width="2.5"/>
    <g fill="{RULE_INK}" opacity="0.92">
      {''.join(scroll)}
    </g>
  </g>

  <!-- fg: the paginated leaves, each with its own contact shadow, then the crease -->
  <g id="fg">
    <g filter="url(#tight)" opacity="0.22">
      <rect x="{SHEET_X+LEAF_INSET+6}" y="{CREASE_Y+64}" width="{SHEET_W-LEAF_INSET*2}" height="{LEAF_H*2+LEAF_GAP:.1f}"
            rx="{CORNER}" fill="#6B5A3E"/>
    </g>
    {''.join(leaves)}
    <g fill="{RULE_INK}" opacity="0.92">
      {''.join(leaf_rules)}
    </g>

    <!-- the crease: the only place the two states meet, and where the colour is -->
    <rect x="{SHEET_X-6}" y="{CREASE_Y:.1f}" width="{SHEET_W+12}" height="38" rx="19"
          fill="url(#crease)"/>
    <rect x="{SHEET_X-6}" y="{CREASE_Y:.1f}" width="{SHEET_W+12}" height="38" rx="19"
          fill="url(#creaseRoll)"/>
  </g>

  <g id="highlight">
    <rect width="{S}" height="{S}" fill="url(#vig)"/>
  </g>
</g>
</svg>
"""


def main() -> int:
    (HERE / OUT).write_text(build())
    print(f"wrote {OUT} — the superseded porcelain master, kept for the audit sheet. "
          f"It does not ship, so nothing here rasterises icon.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
