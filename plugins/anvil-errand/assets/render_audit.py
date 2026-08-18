#!/usr/bin/env python3
"""Reproduce this commission's contact-sheet renders, exactly as they ship.

This file used to hold a bespoke renderer written for the first (dark-register)
commission. It was superseded: its size tuple predated the sheet's 96px and 128px
sources, so running it left take renders missing and `audit_sheet.py check` failed
on them, and it wrote no render-manifest.json, which is what `check` reads to
prove a render is current and that a raster take was masked rather than shipped
square. That file was damaged during this rebuild and could not be restored
byte-for-byte, so rather than reconstruct it from memory it is replaced here by
the one thing worth keeping: the exact take list, delegating to the script that
owns the job.

    python3 render_audit.py

Six takes, because the sheet audits both runs: the three porcelain takes from this
commission and the three dark-field takes from the one it replaces. The raster
takes are declared `raster-mask` so they are audited on their squircle-masked
versions - a full-bleed raster with opaque corners ships as a square tile beside
squircle siblings, and only the mask kind records which it was.
"""
import pathlib
import subprocess
import sys

ASSETS = pathlib.Path(__file__).resolve().parent
# ../../create-mac-icon/skills/create-mac-icon/scripts/audit_sheet.py
SCRIPT = (ASSETS.parent.parent / "create-mac-icon" / "skills" / "create-mac-icon"
          / "scripts" / "audit_sheet.py")

TAKES = [
    ("A", "icon.svg"),
    ("B", "icon-engineB-arrow-593458.svg"),
    ("C", "icon-engineC-porcelain-c23701.png:raster-mask"),
    ("Adark", "icon-engineA-darkfield-2c2f3e.svg"),
    ("Bdark", "icon-engineB-arrow-48ee4c.svg"),
    ("Cdark", "icon-engineC-forge-9f7b8f.png:raster-mask"),
]

if __name__ == "__main__":
    if not SCRIPT.exists():
        sys.exit(f"audit_sheet.py not found at {SCRIPT} — is create-mac-icon installed "
                 f"beside this plugin?")
    args = [sys.executable, str(SCRIPT), "render", str(ASSETS)]
    for take, src in TAKES:
        args += ["--take", f"{take}={src}"]
    subprocess.run(args, check=True)
    subprocess.run([sys.executable, str(SCRIPT), "check", str(ASSETS)], check=True)
