#!/usr/bin/env python3
"""build_icon.py : Icon master & render pipeline for `resume-session`.

Concept A: The Golden Thread
- Superellipse porcelain ground (#F8F5EE -> #E4DDCB) with tactile rim highlight (#FFFDF8).
- Muted obsidian / graphite transcript ribbon on the left (historical session memory, verified ledger strata).
- Tahoe gel-glass optical coupler node at center (the resume lens and splice anchor).
- Radiant golden-vermilion filament on the right (resumed active execution, energized forward velocity).
- Precision macOS multi-scale assets generated via rsvg-convert / sips.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent
SQ_FILE = ASSETS_DIR.parents[1] / "create-mac-icon" / "assets" / "squircle-path.txt"

# ── Color Palette ─────────────────────────────────────────────────────────────
GROUND_TOP, GROUND_BOT = "#F8F5EE", "#E4DDCB"
RIM_COLOR = "#FFFDF8"
GRAPHITE_TOP, GRAPHITE_BOT = "#3A424D", "#1A2026"
GRAPHITE_SHADOW = "#0D1115"
ACCENT_START, ACCENT_MID, ACCENT_HI, ACCENT_CORE = "#DE5F2C", "#FF763B", "#FFAE6B", "#FFF3E6"
GEL_BODY = "#EDE7DB"
GEL_EDGE = "#FFFDF9"
CARD_WHITE = "#FFFFFF"


def build_svg() -> str:
    squircle_d = ""
    if SQ_FILE.exists():
        squircle_d = SQ_FILE.read_text().strip()
    if not squircle_d:
        squircle_d = "M 512 0 C 137.6 0 0 137.6 0 512 C 0 886.4 137.6 1024 512 1024 C 886.4 1024 1024 886.4 1024 512 C 1024 137.6 886.4 0 512 0 Z"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GROUND_TOP}"/>
      <stop offset="100%" stop-color="{GROUND_BOT}"/>
    </linearGradient>
    <radialGradient id="vignette" cx="50%" cy="40%" r="75%">
      <stop offset="60%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#4A3F2E" stop-opacity="0.16"/>
    </radialGradient>

    <!-- Graphite Left Block -->
    <linearGradient id="graphiteGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GRAPHITE_TOP}"/>
      <stop offset="100%" stop-color="{GRAPHITE_BOT}"/>
    </linearGradient>

    <!-- Golden Vermilion Active Pulse -->
    <linearGradient id="pulseGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT_START}"/>
      <stop offset="50%" stop-color="{ACCENT_MID}"/>
      <stop offset="85%" stop-color="{ACCENT_HI}"/>
      <stop offset="100%" stop-color="{ACCENT_CORE}"/>
    </linearGradient>

    <!-- Right Card -->
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F2EDE2"/>
    </linearGradient>

    <!-- Tahoe Gel Coupler Gradient -->
    <linearGradient id="gelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="{GEL_BODY}" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#C5BCAB" stop-opacity="0.90"/>
    </linearGradient>

    <!-- Glow & Soft Filters -->
    <radialGradient id="glowBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{ACCENT_MID}" stop-opacity="0.85"/>
      <stop offset="40%" stop-color="{ACCENT_START}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{ACCENT_START}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="shadowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#14181C" stop-opacity="0.38"/>
      <stop offset="60%" stop-color="#14181C" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#14181C" stop-opacity="0"/>
    </radialGradient>

    <filter id="blurFilter" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <clipPath id="squircleClip">
      <path d="{squircle_d}"/>
    </clipPath>
  </defs>

  <g clip-path="url(#squircleClip)">
    <!-- Base Cushion Plate -->
    <rect width="1024" height="1024" fill="url(#groundGrad)"/>
    <rect width="1024" height="1024" fill="url(#vignette)"/>
    <path d="{squircle_d}" fill="none" stroke="{RIM_COLOR}" stroke-width="8" opacity="0.88"/>

    <!-- Contact Floor Shadows -->
    <ellipse cx="330" cy="740" rx="170" ry="42" fill="url(#shadowGrad)"/>
    <ellipse cx="690" cy="740" rx="170" ry="42" fill="url(#shadowGrad)"/>
    <ellipse cx="512" cy="512" rx="280" ry="140" fill="url(#glowBloom)" opacity="0.55"/>

    <!-- ── LEFT: Past Session Ledger Block (Graphite / Obsidian) ── -->
    <g id="pastSessionBlock">
      <!-- Outer Card with 3D drop shadow & inner highlight -->
      <rect x="200" y="300" width="250" height="400" rx="42" fill="url(#graphiteGrad)"/>
      <rect x="200" y="300" width="250" height="400" rx="42" fill="none" stroke="{RIM_COLOR}" stroke-width="2" stroke-opacity="0.25"/>
      <path d="M 242 302 h 166" stroke="#FFF" stroke-width="4" stroke-linecap="round" opacity="0.4"/>

      <!-- Transcript Memory Strata Lines -->
      <rect x="240" y="360" width="170" height="20" rx="10" fill="#FFF" opacity="0.35"/>
      <rect x="240" y="400" width="130" height="16" rx="8" fill="#FFF" opacity="0.20"/>
      <rect x="240" y="435" width="150" height="16" rx="8" fill="#FFF" opacity="0.20"/>
      <rect x="240" y="470" width="100" height="16" rx="8" fill="#FFF" opacity="0.20"/>
      <rect x="240" y="505" width="140" height="16" rx="8" fill="#FFF" opacity="0.20"/>

      <!-- Verified Ledger Strata Tick -->
      <circle cx="325" cy="605" r="34" fill="{ACCENT_START}" opacity="0.25"/>
      <circle cx="325" cy="605" r="26" fill="url(#pulseGrad)"/>
      <path d="M 314 605 L 322 613 L 338 597" fill="none" stroke="#FFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <!-- ── RIGHT: Active Resumed Forward Block (Ceramic / Radiant) ── -->
    <g id="resumedActiveBlock">
      <rect x="574" y="260" width="250" height="440" rx="42" fill="url(#cardGrad)"/>
      <rect x="574" y="260" width="250" height="440" rx="42" fill="none" stroke="#DCD5C5" stroke-width="3" opacity="0.85"/>
      <path d="M 616 263 h 166" stroke="#FFF" stroke-width="5" stroke-linecap="round" opacity="0.95"/>

      <!-- Resumed Execution Task Lines -->
      <rect x="614" y="330" width="170" height="22" rx="11" fill="{GRAPHITE_TOP}" opacity="0.80"/>
      <rect x="614" y="375" width="140" height="18" rx="9" fill="#998E7E" opacity="0.50"/>
      <rect x="614" y="412" width="155" height="18" rx="9" fill="#998E7E" opacity="0.50"/>
      <rect x="614" y="449" width="120" height="18" rx="9" fill="#998E7E" opacity="0.50"/>
      <rect x="614" y="486" width="150" height="18" rx="9" fill="#998E7E" opacity="0.50"/>

      <!-- Forward Velocity Chevron -->
      <circle cx="699" cy="605" r="34" fill="{ACCENT_START}" opacity="0.18"/>
      <polygon points="684,577 684,633 728,605" fill="url(#pulseGrad)"/>
    </g>

    <!-- ── CENTER: The Golden Thread & Tahoe Gel Coupler Node ── -->
    <g id="goldenThreadHandover">
      <!-- Ambient Thread Glow -->
      <path d="M 400 512 C 450 512, 470 512, 620 512" fill="none" stroke="{ACCENT_START}" stroke-width="40" opacity="0.30" filter="url(#blurFilter)"/>
      
      <!-- Primary Core Thread Splicing Past into Future -->
      <path d="M 370 512 L 490 512" fill="none" stroke="{GRAPHITE_TOP}" stroke-width="18" stroke-linecap="round"/>
      <path d="M 480 512 L 650 512" fill="none" stroke="url(#pulseGrad)" stroke-width="22" stroke-linecap="round"/>

      <!-- Tahoe Gel-Glass Coupler Prism Node -->
      <circle cx="512" cy="512" r="52" fill="url(#gelGrad)"/>
      <circle cx="512" cy="512" r="52" fill="none" stroke="{GEL_EDGE}" stroke-width="4" opacity="0.95"/>
      <ellipse cx="512" cy="482" rx="30" ry="12" fill="#FFF" opacity="0.75"/>
      
      <!-- Central Optical Focus Beam -->
      <circle cx="512" cy="512" r="22" fill="url(#pulseGrad)"/>
      <circle cx="512" cy="512" r="10" fill="#FFFFFF"/>
      <circle cx="512" cy="512" r="14" fill="#FFFFFF" filter="url(#blurFilter)" opacity="0.8"/>
    </g>
  </g>
</svg>
"""


def render_all() -> None:
    """Render master SVG and PNG exports."""
    svg_data = build_svg()
    out_svg = ASSETS_DIR / "icon.svg"
    out_svg.write_text(svg_data, encoding="utf-8")
    print(f"✓ Wrote master SVG: {out_svg}")

    sizes = [
        (1024, "icon.png"),
        (256, "icon-256.png"),
        (128, "icon-128.png"),
        (64, "icon-64.png"),
        (32, "icon-32.png"),
        (16, "icon-16.png"),
    ]

    for dim, filename in sizes:
        dest = ASSETS_DIR / filename
        cmd = ["rsvg-convert", "-w", str(dim), "-h", str(dim), str(out_svg), "-o", str(dest)]
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ Rendered {filename} ({dim}x{dim})")
        except Exception as e:
            print(f"Error rendering {filename} with rsvg-convert: {e}")


if __name__ == "__main__":
    render_all()
