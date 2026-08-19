#!/usr/bin/env python3
"""Hand-authored layered SVG master for the `report` icon — "The Fold, inverted".

This is the shipped master. It writes `icon.svg` and rasterises 1024 / 256 / 128,
which are what the root README, skills.fledgeling.app and the digest email display.

It began as take A2, written on 19 Aug 2026 because Engine B (Arrow) refused the
commission on a credit balance and the pipeline's floor is three takes made by real
engines rather than three variations dressed as three. It was the widened Engine A
the skill's own fallback clause calls for, and the audit recommended keeping the
porcelain original. **The user chose this take instead, on 19 Aug 2026**, because it
is legible in the register everyone actually sees: 10.03:1 sheet-to-ground on Default
against the porcelain take's 1.04:1. The porcelain artwork it displaced is preserved
whole as `icon-A1-porcelain.svg`, rebuilt by `build_icon_a1_porcelain.py`, and both
takes are scored side by side in `audit.html`.

Same direction, same signature move. One sheet, creased once across its full width;
above the crease a single uninterrupted column of ruling, below it the same sheet
separated into two stepped leaves. What changes against the porcelain take:

  * the sheet is warm graphite instead of porcelain, so the object is the dark
    thing on a porcelain ground rather than a pale thing on a pale ground. The
    porcelain take measures 1.04:1 paper-to-ground and 1.96:1 ink-to-paper; this
    measures 8.4-13.2:1 sheet-to-ground and 7.4-12.5:1 ruling-to-sheet.
  * the ruling is knocked out in porcelain rather than printed in warm grey, so
    the texture is light coming through rather than pigment sitting on top.
  * the crease is a recessed illuminated slit rather than a raised band: the
    vermilion is light escaping the fold, and it bleeds a short glow onto the
    graphite above and below it, which is what makes the fold read as a fold on a
    dark face.
  * the sheet carries a 1.5px inner rim light on its top and left edges, which the
    porcelain take does not have at all.

Layers are the named groups bg / mid / fg / highlight, as `fidelity.py structure`
counts them. Geometry is deliberately identical to `build_icon_a1_porcelain.py` so the
two takes differ on value and material only — that is the comparison the audit sheet
makes. Two liabilities ship with this take and are on the record in `audit.html`:
rubric #8, because the slit spans y=512-536 and touches neither the sheet's lower edge
at y=505 nor the first leaf's upper edge at y=563; and Dark, where the graphite sheet
falls to 1.10:1 against the ground and legibility rests on the ruling's 6.90:1 against
its own face. A fidelity round is a parameter edit here, never path surgery in the
output; both liabilities are single named constants below.
"""

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (HERE.parent.parent / "create-mac-icon" / "assets" / "squircle-path.txt")
OUT = "icon.svg"

# ── geometry: shared verbatim with build_icon_a1_porcelain.py, so nothing but value moves ──
S = 1024
SHEET_X, SHEET_W = 236.0, 552.0
SHEET_Y = 142.0
CREASE_Y = 505.0
LEAF_H = 122.0
LEAF_STEP_X = 34.0
LEAF_INSET = 46.0
LEAF_GAP = 56.0
CORNER = 16.0

RULE_X_PAD = 58.0
LEAF_RULE_PAD = 40.0
RULE_H = 15.0
RULE_R = 7.5

# ── palette: porcelain ground kept, sheet inverted to warm graphite ────────────────
GROUND_HI, GROUND_MID, GROUND_LO = "#FFFDF8", "#F7F2E9", "#EFE8DB"
SHEET_HI, SHEET_LO = "#4B463E", "#2B2822"          # 8.39:1 and 13.18:1 vs GROUND_MID
LEAF_HI, LEAF_LO = "#565046", "#332F28"            # the leaves sit forward of the sheet
SHEET_EDGE = "#221F1A"
RIM = "#8B8272"                                     # the inner rim light, top and left
RULE_INK = "#F2ECE1"                                # knocked out, not printed
RULE_OPACITY = 0.82                                 # 12.50:1 against SHEET_LO at full
ACCENT_HI, ACCENT_MID, ACCENT_LO = "#F4763F", "#E2521F", "#C03A0E"
SLIT_GLOW = "#FF8A4C"


def rule(x, y, w):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{RULE_H}" rx="{RULE_R}"/>'


def build() -> str:
    squircle = SQUIRCLE.read_text().strip()
    rx = SHEET_X + RULE_X_PAD
    rw_full = SHEET_W - RULE_X_PAD * 2

    scroll = []
    y = SHEET_Y + 96
    for frac in (1.0, 0.92, 1.0, 0.78, 0.96, 0.88, 0.55):
        scroll.append(rule(rx, y, rw_full * frac))
        y += 40

    leaves, leaf_rules, leaf_rims, faces, leaf_shadows = [], [], [], [], []
    ly = CREASE_Y + 58
    for i in range(2):
        lx = SHEET_X + LEAF_INSET + LEAF_STEP_X * i
        lw = SHEET_W - LEAF_INSET * 2 - LEAF_STEP_X * 2 * i
        faces.append(
            f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{LEAF_H:.1f}" rx="{CORNER}"/>'
        )
        # One contact shadow per leaf, not one slab behind both. The porcelain take
        # casts a single blurred rect spanning LEAF_H*2 + LEAF_GAP, so its middle shows
        # through the gap between the leaves as a grey panel floating on the porcelain —
        # visible in that take's own 1024 render. Per-leaf shadows put the darkness only
        # where a leaf actually rests on something.
        leaf_shadows.append(
            f'<rect x="{lx+7:.1f}" y="{ly+9:.1f}" width="{lw:.1f}" height="{LEAF_H:.1f}" '
            f'rx="{CORNER}" fill="#4A3F2C"/>'
        )
        leaves.append(
            f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{LEAF_H:.1f}" '
            f'rx="{CORNER}" fill="url(#leaf)" stroke="{SHEET_EDGE}" stroke-width="2"/>'
        )
        leaf_rims.append(
            f'<path d="M{lx+CORNER:.1f} {ly+1.2:.1f} H{lx+lw-CORNER:.1f}" '
            f'stroke="{RIM}" stroke-width="1.5" stroke-opacity="0.55" fill="none"/>'
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
  <linearGradient id="sheet" x1="{SHEET_X}" y1="{SHEET_Y}" x2="{SHEET_X+SHEET_W}" y2="{CREASE_Y}"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{SHEET_HI}"/><stop offset="1" stop-color="{SHEET_LO}"/></linearGradient>
  <linearGradient id="leaf" x1="{SHEET_X}" y1="{CREASE_Y}" x2="{SHEET_X+SHEET_W}" y2="900"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{LEAF_HI}"/><stop offset="1" stop-color="{LEAF_LO}"/></linearGradient>
  <linearGradient id="slit" x1="{SHEET_X}" y1="{CREASE_Y}" x2="{SHEET_X+SHEET_W}" y2="{CREASE_Y}"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{ACCENT_LO}"/><stop offset="0.46" stop-color="{ACCENT_MID}"/>
    <stop offset="1" stop-color="{ACCENT_HI}"/></linearGradient>
  <linearGradient id="bleed" x1="0" y1="{CREASE_Y-46}" x2="0" y2="{CREASE_Y+84}"
    gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{SLIT_GLOW}" stop-opacity="0"/>
    <stop offset="0.36" stop-color="{SLIT_GLOW}" stop-opacity="0.34"/>
    <stop offset="0.5" stop-color="{SLIT_GLOW}" stop-opacity="0.46"/>
    <stop offset="0.64" stop-color="{SLIT_GLOW}" stop-opacity="0.30"/>
    <stop offset="1" stop-color="{SLIT_GLOW}" stop-opacity="0"/></linearGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="20"/></filter>
  <filter id="tight" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6"/></filter>
  <filter id="glow" x="-40%" y="-140%" width="180%" height="380%">
    <feGaussianBlur stdDeviation="16"/></filter>
  <clipPath id="tile"><path d="{squircle}"/></clipPath>
  <!-- The slit's glow is clipped to the paper faces it falls on. Unclipped, its blur
       spilled a warm haze across the porcelain in the gap between the two leaves,
       which reads as a smudge rather than as light escaping a fold. -->
  <clipPath id="faces">
    <rect x="{SHEET_X}" y="{SHEET_Y}" width="{SHEET_W}" height="{scroll_h:.1f}" rx="{CORNER}"/>
    {''.join(faces)}
  </clipPath>
</defs>

<g id="art" clip-path="url(#tile)">
  <g id="bg">
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#crown)"/>
  </g>

  <!-- mid: the sheet's cast shadow, the graphite face, its rim light, the knocked-out ruling -->
  <g id="mid">
    <g filter="url(#soft)" opacity="0.34">
      <rect x="{SHEET_X+10}" y="{SHEET_Y+26}" width="{SHEET_W}" height="{scroll_h+28:.1f}"
            rx="{CORNER}" fill="#4A3F2C"/>
    </g>
    <rect x="{SHEET_X}" y="{SHEET_Y}" width="{SHEET_W}" height="{scroll_h:.1f}"
          rx="{CORNER}" fill="url(#sheet)" stroke="{SHEET_EDGE}" stroke-width="2"/>
    <path d="M{SHEET_X+CORNER} {SHEET_Y+1.4:.1f} H{SHEET_X+SHEET_W-CORNER}" stroke="{RIM}"
          stroke-width="1.6" stroke-opacity="0.62" fill="none"/>
    <path d="M{SHEET_X+1.4:.1f} {SHEET_Y+CORNER} V{CREASE_Y-CORNER:.1f}" stroke="{RIM}"
          stroke-width="1.6" stroke-opacity="0.40" fill="none"/>
    <g fill="{RULE_INK}" opacity="{RULE_OPACITY}">
      {''.join(scroll)}
    </g>
  </g>

  <!-- fg: the paginated leaves, then the slit the light comes out of -->
  <g id="fg">
    <g filter="url(#tight)" opacity="0.30">
      {''.join(leaf_shadows)}
    </g>
    {''.join(leaves)}
    {''.join(leaf_rims)}
    <g fill="{RULE_INK}" opacity="{RULE_OPACITY}">
      {''.join(leaf_rules)}
    </g>

    <!-- the crease, as a recessed slit: glow bleeding onto the graphite, then the light itself -->
    <g filter="url(#glow)" clip-path="url(#faces)">
      <rect x="{SHEET_X-2}" y="{CREASE_Y-46:.1f}" width="{SHEET_W+4}" height="130"
            fill="url(#bleed)"/>
    </g>
    <rect x="{SHEET_X-6}" y="{CREASE_Y+7:.1f}" width="{SHEET_W+12}" height="24" rx="12"
          fill="url(#slit)"/>
    <rect x="{SHEET_X-6}" y="{CREASE_Y+7:.1f}" width="{SHEET_W+12}" height="9" rx="4.5"
          fill="#FFD2B4" opacity="0.55"/>
  </g>

  <g id="highlight">
    <rect width="{S}" height="{S}" fill="url(#vig)"/>
  </g>
</g>
</svg>
"""


def main() -> int:
    (HERE / OUT).write_text(build())
    for size in (1024, 256, 128):
        name = "icon.png" if size == 1024 else f"icon-{size}.png"
        subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size),
             str(HERE / OUT), "-o", str(HERE / name)],
            check=True,
        )
        print(f"wrote {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
