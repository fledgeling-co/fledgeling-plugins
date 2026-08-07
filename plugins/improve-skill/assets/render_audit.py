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

# The shipping icon is take A, the hand-authored layered vector master (icon.svg),
# by the user's direction after the round-4 material rebuild. icon.png / icon-256.png /
# icon-128.png are rendered from it. C2 stays on disk as the reference raster take.
for s, name in ((1024, "icon.png"), (256, "icon-256.png"), (128, "icon-128.png")):
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(A / "icon.svg"),
                    "-o", str(A / name)], check=True)
print("rendered:", sorted(p.name for p in OUT.iterdir()))
