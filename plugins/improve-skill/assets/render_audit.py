#!/usr/bin/env python3
"""Render every take at the audit sizes. Rasters are squircle-masked first so all
takes are judged on the same mask, per the mac-design-studio pipeline."""
import base64, pathlib, subprocess

A = pathlib.Path(__file__).resolve().parent
OUT = A / "audit-renders"; OUT.mkdir(exist_ok=True)
SQ = (A / "squircle-path.txt").read_text().strip()
SIZES = [1024, 256, 64, 32]

def svg_sizes(src, tag):
    for s in SIZES:
        subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(src),
                        "-o", str(OUT / f"{tag}-{s}.png")], check=True)

def raster_sizes(src, tag):
    b64 = base64.b64encode(src.read_bytes()).decode()
    wrap = A / f".mask-{tag}.svg"
    wrap.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 1024 1024" width="1024" height="1024">'
        f'<defs><clipPath id="m"><path d="{SQ}"/></clipPath></defs>'
        f'<g clip-path="url(#m)"><image xlink:href="data:image/png;base64,{b64}" '
        f'x="0" y="0" width="1024" height="1024" preserveAspectRatio="xMidYMid slice"/></g></svg>')
    svg_sizes(wrap, tag)
    wrap.unlink()

svg_sizes(A / "icon.svg", "A")
svg_sizes(A / "icon-engineB-arrow-a2a087.svg", "B")
raster_sizes(A / "icon-engineC-cfd884.png", "C1")
raster_sizes(A / "icon-engineC-f5665d-2.png", "C2")

# The shipping icon is take C2 (the raster), chosen by the user over the higher-scoring
# vector master. icon.png / icon-256.png / icon-128.png are all derived from it, NOT from
# icon.svg, which is kept as the editable alternate. Regenerate them from C2 only.
ship = A / "icon-engineC-f5665d-2.png"
b64 = base64.b64encode(ship.read_bytes()).decode()
wrap = A / ".ship.svg"
wrap.write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'viewBox="0 0 1024 1024" width="1024" height="1024">'
    f'<defs><clipPath id="m"><path d="{SQ}"/></clipPath></defs>'
    f'<g clip-path="url(#m)"><image xlink:href="data:image/png;base64,{b64}" x="0" y="0" '
    f'width="1024" height="1024" preserveAspectRatio="xMidYMid slice"/></g></svg>')
for s, name in ((1024, "icon.png"), (256, "icon-256.png"), (128, "icon-128.png")):
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(wrap),
                    "-o", str(A / name)], check=True)
wrap.unlink()
print("rendered:", sorted(p.name for p in OUT.iterdir()))
