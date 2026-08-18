#!/usr/bin/env python3
"""silhouette.py — rubric #3 check: is the glyph nameable as a filled solid?

Takes icon.svg, keeps the two graphite masses, flattens every fill and stroke to black
on a white tile and drops the ground, the bloom and the contact shadow, so the mass is
the shape and nothing else.  The seam is deliberately NOT ink: it is light in a gap, so
in a filled silhouette it is the space between the masses rather than an object.  That
is the whole claim this check has to test.  Renders to silhouette.png at 512.
"""
import pathlib
import re
import subprocess

here = pathlib.Path(__file__).resolve().parent
src = (here / "icon.svg").read_text()
sq = (here / "squircle-path.txt").read_text().strip()

masses = re.findall(r'<g id="mass-(?:left|right)">.*?</g>', src, re.S)
if len(masses) != 2:
    raise SystemExit(f"expected two mass groups in icon.svg, found {len(masses)}")

body = "\n".join(masses)
body = re.sub(r'fill="(?!none)[^"]+"', 'fill="#000"', body)
body = re.sub(r'stroke="(?!none)[^"]+"', 'stroke="#000"', body)
body = re.sub(r'(fill|stroke)-opacity="[^"]+"', r'\1-opacity="1"', body)

out = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" '
       'width="1024" height="1024">'
       f'<clipPath id="sq"><path d="{sq}"/></clipPath>'
       '<rect width="1024" height="1024" fill="#fff"/>'
       f'<g clip-path="url(#sq)">{body}</g></svg>')
(here / "silhouette.svg").write_text(out)
subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", str(here / "silhouette.svg"),
                "-o", str(here / "silhouette.png")], check=True)
print("wrote silhouette.svg + silhouette.png")
