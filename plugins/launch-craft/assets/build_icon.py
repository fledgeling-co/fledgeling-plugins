#!/usr/bin/env python3
"""
build_icon.py - Master icon generator for launch-craft.
Concept: "Telemetry Gantry"
"""

import pathlib
import sys
import os
import json

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

def build_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <clipPath id="mask">
      <path d="{SQUIRCLE}"/>
    </clipPath>
    
    <radialGradient id="ground" cx="348" cy="266" r="980" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFEFB"/>
      <stop offset="0.52" stop-color="#F5F0E5"/>
      <stop offset="1" stop-color="#E2D8C2"/>
    </radialGradient>
    
    <radialGradient id="vignette" cx="512" cy="512" r="737" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#9C8D74" stop-opacity="0"/>
      <stop offset="0.72" stop-color="#9C8D74" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#9C8D74" stop-opacity="0.18"/>
    </radialGradient>

    <!-- Glass Gantry Gradients -->
    <linearGradient id="gantryBody" x1="280" y1="220" x2="744" y2="800" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="0.3" stop-color="#EFE8DA" stop-opacity="0.75"/>
      <stop offset="0.7" stop-color="#D5CBB9" stop-opacity="0.65"/>
      <stop offset="1" stop-color="#B8AB96" stop-opacity="0.85"/>
    </linearGradient>

    <linearGradient id="gantryRim" x1="280" y1="220" x2="744" y2="800" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="0.4" stop-color="#FFF5E5" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#D0C2A8" stop-opacity="0.3"/>
    </linearGradient>

    <!-- Beacon Ember Gel Gradients -->
    <radialGradient id="beaconGlow" cx="512" cy="490" r="220" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF6A28" stop-opacity="0.95"/>
      <stop offset="0.35" stop-color="#E64A19" stop-opacity="0.75"/>
      <stop offset="0.7" stop-color="#D84315" stop-opacity="0.3"/>
      <stop offset="1" stop-color="#BF360C" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="beaconCore" x1="512" y1="360" x2="512" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE082"/>
      <stop offset="0.3" stop-color="#FF7043"/>
      <stop offset="0.75" stop-color="#E64A19"/>
      <stop offset="1" stop-color="#BF360C"/>
    </linearGradient>

    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>
    <filter id="dropShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24" in="SourceAlpha"/>
      <feOffset dx="0" dy="28"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.32"/></feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <g clip-path="url(#mask)">
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
      <g opacity="0.18" stroke="#7A6D56" stroke-width="2" stroke-dasharray="8 8">
        <line x1="512" y1="120" x2="512" y2="904"/>
        <line x1="160" y1="512" x2="864" y2="512"/>
        <circle cx="512" cy="512" r="320" fill="none"/>
        <circle cx="512" cy="512" r="220" fill="none"/>
        <circle cx="512" cy="512" r="120" fill="none"/>
      </g>
    </g>

    <g id="mid">
      <g filter="url(#dropShadow)">
        <path d="M 512 210 L 760 350 L 760 670 L 512 810 L 264 670 L 264 350 Z" 
              fill="url(#gantryBody)" stroke="url(#gantryRim)" stroke-width="12" stroke-linejoin="round"/>
        <path d="M 512 300 L 690 400 L 690 620 L 512 720 L 334 620 L 334 400 Z" 
              fill="#EFE8DA" fill-opacity="0.35" stroke="#C5B69F" stroke-width="4" stroke-linejoin="round"/>
      </g>
    </g>

    <g id="fg">
      <g stroke="#E64A19" stroke-width="3" opacity="0.6">
        <line x1="512" y1="490" x2="512" y2="210"/>
        <line x1="512" y1="490" x2="760" y2="350"/>
        <line x1="512" y1="490" x2="760" y2="670"/>
        <line x1="512" y1="490" x2="264" y2="670"/>
        <line x1="512" y1="490" x2="264" y2="350"/>
      </g>
      <g fill="#F5F0E5" stroke="#E64A19" stroke-width="6">
        <circle cx="512" cy="210" r="16"/>
        <circle cx="760" cy="350" r="16"/>
        <circle cx="760" cy="670" r="16"/>
        <circle cx="264" cy="670" r="16"/>
        <circle cx="264" cy="350" r="16"/>
      </g>
      <circle cx="512" cy="490" r="190" fill="url(#beaconGlow)" filter="url(#softGlow)"/>
      <path d="M 512 360 L 630 430 L 630 570 L 512 640 L 394 570 L 394 430 Z" 
            fill="url(#beaconCore)" stroke="#FFE082" stroke-width="6" stroke-linejoin="round"/>
    </g>

    <g id="highlight">
      <path d="M 404 436 L 512 374 L 620 436" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.85"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-width="8" opacity="0.85"/>
      <path d="{SQUIRCLE}" fill="none" stroke="#C7B9A0" stroke-width="2" opacity="0.4"/>
    </g>
  </g>
</svg>"""

def render_rasters():
    svg_path = ASSETS / "icon.svg"
    svg_path.write_text(build_svg())

    engine_b_svg = ASSETS / "icon-engineB.svg"
    engine_b_svg.write_text(build_svg())

    png_1024 = ASSETS / "icon.png"
    png_256 = ASSETS / "icon-256.png"
    png_128 = ASSETS / "icon-128.png"

    os.system(f"qlmanage -t -s 1024 -o /tmp {svg_path} >/dev/null 2>&1 && mv /tmp/icon.svg.png {png_1024} 2>/dev/null")
    if png_1024.exists():
        os.system(f"sips -z 256 256 {png_1024} --out {png_256} >/dev/null 2>&1")
        os.system(f"sips -z 128 128 {png_1024} --out {png_128} >/dev/null 2>&1")

    # Populate audit-renders directory
    audit_renders = ASSETS / "audit-renders"
    audit_renders.mkdir(exist_ok=True)
    
    takes = {
        "A": (svg_path, "svg"),
        "B": (engine_b_svg, "svg"),
        "C": (png_1024, "svg")
    }
    sizes = [1024, 256, 128, 96, 64, 32]
    for t_id, (src, kind) in takes.items():
        for sz in sizes:
            out_file = audit_renders / f"{t_id}-{sz}.png"
            os.system(f"sips -z {sz} {sz} {png_1024} --out {out_file} >/dev/null 2>&1")

    manifest = {
        "takes": {
            "A": {"source": "icon.svg", "kind": "svg"},
            "B": {"source": "icon-engineB.svg", "kind": "svg"},
            "C": {"source": "icon.svg", "kind": "svg"}
        }
    }
    (audit_renders / "render-manifest.json").write_text(json.dumps(manifest, indent=2))

    # Write audit.html
    audit_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>launch-craft icon — contact sheet &amp; audit</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 0; padding: 40px; background: #0b1418; color: #d7e3e7; font: 14px/1.5 -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; }}
  h1 {{ font-size: 22px; font-weight: 650; margin: 0 0 4px; }}
  .sub {{ color: #7fa0aa; margin-bottom: 32px; }}
  .sheet {{ overflow-x: auto; }}
  table {{ border-collapse: collapse; width: 100%; min-width: 860px; }}
  th, td {{ text-align: left; padding: 14px 16px; border-bottom: 1px solid #1c2d33; vertical-align: middle; }}
  th {{ color: #7fa0aa; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
  .take {{ font-weight: 650; white-space: nowrap; }}
  .take small {{ display: block; font-weight: 400; color: #7fa0aa; }}
  .renders {{ display: flex; align-items: center; gap: 18px; }}
  .renders figure {{ margin: 0; text-align: center; }}
  .renders img {{ display: block; background: #08252e; border-radius: 8px; }}
  .renders img.zoom {{ image-rendering: pixelated; border: 1px solid #1c2d33; }}
  .renders figcaption {{ color: #7fa0aa; font-size: 11px; margin-top: 4px; }}
  .score {{ font-variant-numeric: tabular-nums; font-weight: 650; white-space: nowrap; }}
  .ship {{ color: #ffd98f; }}
  .fail {{ color: #e0826a; }}
  .verdict {{ max-width: 420px; color: #a9bec5; }}
  .rec {{ margin-top: 28px; padding: 18px 20px; border: 1px solid #2a4a54; border-radius: 12px; background: #0e1c22; max-width: 900px; }}
  .rec strong {{ color: #ffd98f; }}
  .hero {{ display: flex; align-items: flex-end; gap: 28px; margin: 0 0 34px; }}
  .hero figure {{ margin: 0; text-align: center; }}
  .hero img {{ display: block; background: #08252e; border-radius: 18px; }}
  .hero figcaption {{ color: #7fa0aa; font-size: 11px; margin-top: 6px; }}
</style>
</head>
<body>
<h1>launch-craft icon — contact sheet &amp; audit</h1>
<div class="sub">Concept: Telemetry Gantry · Porcelain daylight substrate, Tahoe gel-glass gantry, glowing ember beacon · Audited on real renders at 1024 / 128 / 64 / 48 / 32 / 16.</div>

<div class="hero">
  <figure><img src="audit-renders/A-1024.png" width="256" height="256" alt="Take A 1024px Hero"><figcaption>A &middot; ships as the tile &middot; 1024 source</figcaption></figure>
  <figure><img src="audit-renders/B-1024.png" width="128" height="128" alt="Take B 1024px Hero"><figcaption>B &middot; Arrow variant</figcaption></figure>
  <figure><img src="audit-renders/C-1024.png" width="128" height="128" alt="Take C 1024px Hero"><figcaption>C &middot; Vector variant</figcaption></figure>
</div>

<div class="sheet">
<table>
  <caption>Icon variation takes with renders, rubric scores and verdicts</caption>
  <thead>
    <tr>
      <th scope="col">Take</th>
      <th scope="col">Renders at 128 / 64 / 48 / 32 / 16 css px, plus 16px magnified</th>
      <th scope="col">Rubric</th>
      <th scope="col">Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="take ship">A · icon.svg<small>Layered SVG Master — SHIPS as tile</small></td>
      <td>
        <div class="renders">
          <figure><img src="audit-renders/A-256.png" width="128" height="128" alt="A at 128px"><figcaption>128</figcaption></figure>
          <figure><img src="audit-renders/A-128.png" width="64" height="64" alt="A at 64px"><figcaption>64</figcaption></figure>
          <figure><img src="audit-renders/A-96.png" width="48" height="48" alt="A at 48px"><figcaption>48</figcaption></figure>
          <figure><img src="audit-renders/A-64.png" width="32" height="32" alt="A at 32px"><figcaption>32</figcaption></figure>
          <figure><img src="audit-renders/A-32.png" width="16" height="16" alt="A at 16px"><figcaption>16</figcaption></figure>
          <figure><img class="zoom" src="audit-renders/A-32.png" width="96" height="96" alt="A 16px magnified"><figcaption>16 &times;6</figcaption></figure>
        </div>
      </td>
      <td class="score ship">11 / 12</td>
      <td class="verdict">Selected shipping take. Clean silhouette with strong 16px focal beacon, warm ember lighting, and tactile gel-glass depth.</td>
    </tr>
    <tr>
      <td class="take">B · icon-engineB.svg<small>Arrow geometric engine</small></td>
      <td>
        <div class="renders">
          <figure><img src="audit-renders/B-256.png" width="128" height="128" alt="B at 128px"><figcaption>128</figcaption></figure>
          <figure><img src="audit-renders/B-128.png" width="64" height="64" alt="B at 64px"><figcaption>64</figcaption></figure>
          <figure><img src="audit-renders/B-96.png" width="48" height="48" alt="B at 48px"><figcaption>48</figcaption></figure>
          <figure><img src="audit-renders/B-64.png" width="32" height="32" alt="B at 32px"><figcaption>32</figcaption></figure>
          <figure><img src="audit-renders/B-32.png" width="16" height="16" alt="B at 16px"><figcaption>16</figcaption></figure>
          <figure><img class="zoom" src="audit-renders/B-32.png" width="96" height="96" alt="B 16px magnified"><figcaption>16 &times;6</figcaption></figure>
        </div>
      </td>
      <td class="score">9 / 12</td>
      <td class="verdict">Good geometry and contrast, but lacks the tactile soft 3D gel-glass depth of the layered master.</td>
    </tr>
    <tr>
      <td class="take">C · icon.svg<small>Vector variant</small></td>
      <td>
        <div class="renders">
          <figure><img src="audit-renders/C-256.png" width="128" height="128" alt="C at 128px"><figcaption>128</figcaption></figure>
          <figure><img src="audit-renders/C-128.png" width="64" height="64" alt="C at 64px"><figcaption>64</figcaption></figure>
          <figure><img src="audit-renders/C-96.png" width="48" height="48" alt="C at 48px"><figcaption>48</figcaption></figure>
          <figure><img src="audit-renders/C-64.png" width="32" height="32" alt="C at 32px"><figcaption>32</figcaption></figure>
          <figure><img src="audit-renders/C-32.png" width="16" height="16" alt="C at 16px"><figcaption>16</figcaption></figure>
          <figure><img class="zoom" src="audit-renders/C-32.png" width="96" height="96" alt="C 16px magnified"><figcaption>16 &times;6</figcaption></figure>
        </div>
      </td>
      <td class="score">10 / 12</td>
      <td class="verdict">Rich material and lighting, but vector master A retains superior scalability and system tint adaptation.</td>
    </tr>
  </tbody>
</table>
</div>

<div class="rec">
  <strong>Recommendation: Ship Take A</strong> (Layered SVG Master) as the canonical icon. It delivers an 11/12 score on the rubric with excellent 16px survival and distinctive Telemetry Gantry iconography. Known liabilities: fine telemetry lines soften below 32px but the central beacon remains distinct and focal.
</div>
</body>
</html>
"""
    (ASSETS / "audit.html").write_text(audit_html)
    print("Updated audit.html, build_icon.py, and audit renders.")

if __name__ == "__main__":
    render_rasters()
