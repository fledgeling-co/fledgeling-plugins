import pathlib, subprocess, tempfile
from PIL import Image
A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
OUT = A / "loop-runs/r16/work"
REF = A / "icon-engineC-f5665d-2.png"


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


tiles = []
for size in (16, 32, 64):
    k = 512 // size
    c = render_svg(A / "icon.svg", size).convert("RGB").resize((512, 512), Image.NEAREST)
    r = Image.open(REF).convert("RGB").resize((size, size), Image.LANCZOS).resize((512, 512), Image.NEAREST)
    tiles.append((size, c, r))

sheet = Image.new("RGB", (512 * 2 + 24, 512 * 3 + 48), (30, 30, 30))
for i, (size, c, r) in enumerate(tiles):
    sheet.paste(c, (0, i * (512 + 16)))
    sheet.paste(r, (512 + 24, i * (512 + 16)))
sheet.save(OUT / "smallsizes.png")
print("wrote smallsizes.png  (left column = master, right = reference; rows 16/32/64)")
