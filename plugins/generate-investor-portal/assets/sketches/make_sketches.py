#!/usr/bin/env python3
"""Low-fi value sketches used as the direction decision instrument.

Kept as trajectory data: these are the shapes that were tried and rejected on
the way to "The Strongroom, Open". Three values plus the accent, no material —
the question each one answers is whether the composition names anything at
16px, and six of these nine did not.

    python3 make_sketches.py     # writes sketch-*.svg + the contact strips
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQ = (HERE / ".." / ".." / ".." / "create-mac-icon" / "assets" / "squircle-path.txt").read_text().strip()

VOID, GRAPH, GRAPH_L, GRAPH_D = "#171A1E", "#343A42", "#4E555F", "#22262C"
EMBER, EMBER_HI, PALE = "#E8542A", "#F79350", "#F4F1E9"


def wrap(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">'
            f'<defs><clipPath id="t"><path d="{SQ}"/></clipPath>'
            f'<radialGradient id="g" cx="0.46" cy="0.26" r="0.85">'
            f'<stop offset="0" stop-color="#FDFCFA"/><stop offset="1" stop-color="#DFDBD2"/></radialGradient>'
            f'<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0.4">'
            f'<stop offset="0" stop-color="#FFD9A8"/><stop offset="0.45" stop-color="#F7873F" stop-opacity="0.9"/>'
            f'<stop offset="1" stop-color="#E8542A" stop-opacity="0"/></linearGradient></defs>'
            f'<g clip-path="url(#t)"><rect width="1024" height="1024" fill="url(#g)"/>{body}</g></svg>')


def rr(x, y, w, h, r):
    return (f'M{x+r},{y} h{w-2*r} a{r},{r} 0 0 1 {r},{r} v{h-2*r} a{r},{r} 0 0 1 {-r},{r} '
            f'h{-(w-2*r)} a{r},{r} 0 0 1 {-r},{-r} v{-(h-2*r)} a{r},{r} 0 0 1 {r},{-r}z')


SKETCHES = {
    # round 1 — ember as a field
    "a": (f'<circle cx="512" cy="512" r="322" fill="{GRAPH}"/>'
          f'<circle cx="512" cy="512" r="212" fill="{EMBER}"/>'
          f'<rect x="330" y="452" width="364" height="120" rx="26" fill="{PALE}" transform="rotate(-9 512 512)"/>'),
    "b": (f'<rect x="188" y="188" width="648" height="648" rx="150" fill="{GRAPH}"/>'
          f'<circle cx="512" cy="470" r="176" fill="{EMBER}"/>'
          f'<path d="M512,294 a176,176 0 0 1 0,352 a120,176 0 0 0 0,-352z" fill="{GRAPH_D}"/>'
          f'<rect x="330" y="720" width="364" height="26" rx="13" fill="{GRAPH_D}"/>'),
    "c": (f'<rect x="196" y="236" width="632" height="560" rx="88" fill="{GRAPH_D}"/>'
          f'<rect x="252" y="292" width="520" height="448" rx="56" fill="{EMBER}"/>'
          f'<rect x="368" y="330" width="288" height="466" rx="34" fill="{GRAPH}"/>'),
    # round 2 — large dark mass, compact ember
    "d": (f'<path d="{rr(236,196,552,700,96)}" fill="{VOID}"/>'
          f'<rect x="236" y="820" width="552" height="204" fill="{VOID}"/>'
          f'<path d="M236,470 L512,470 L512,896 L236,896z" fill="{EMBER}" opacity="0.55"/>'
          f'<path d="M420,300 h190 v560 h-190z" fill="{PALE}"/>'),
    "d2": (f'<path d="M236,896 L236,472 a276,276 0 0 1 552,0 L788,896z" fill="{VOID}"/>'
           f'<rect x="236" y="860" width="552" height="164" fill="{VOID}"/>'
           f'<path d="M420,330 h190 v530 h-190z" fill="{PALE}"/>'
           f'<circle cx="330" cy="560" r="52" fill="{EMBER}"/>'),
    "e": (f'<g transform="rotate(-6 512 512)">'
          f'<path d="M228,236 h432 l136,136 v416 a72,72 0 0 1 -72,72 h-424 a72,72 0 0 1 -72,-72 v-480 '
          f'a72,72 0 0 1 72,-72z" fill="{GRAPH}"/>'
          f'<path d="M660,236 l136,136 h-136z" fill="{GRAPH_L}"/>'
          f'<circle cx="392" cy="596" r="86" fill="{EMBER}"/></g>'),
    # round 3 — the accent as light rather than paint
    "h": (f'<path d="{rr(176,176,672,672,150)}" fill="#CFC9BE"/>'
          f'<path d="{rr(196,196,632,632,138)}" fill="{VOID}"/>'
          f'<path d="M300,250 L820,300 L820,760 L300,800z" fill="url(#beam)" opacity="0.95"/>'
          f'<g transform="rotate(-7 240 512)"><path d="{rr(208,206,600,612,132)}" fill="{GRAPH}"/>'
          f'<path d="M760,230 l48,26 v520 l-48,26z" fill="{GRAPH_L}"/></g>'),
    "i": (f'<path d="M300,120 h300 v784 h-300z" fill="{GRAPH}"/>'
          f'<path d="M600,120 l84,52 v680 l-84,52z" fill="{GRAPH_L}"/>'
          f'<path d="M684,300 L980,400 L980,640 L684,520z" fill="url(#beam)"/>'
          f'<circle cx="450" cy="330" r="96" fill="{VOID}"/>'
          f'<circle cx="450" cy="330" r="62" fill="{EMBER_HI}"/>'),
    "j": (f'<path d="M232,180 h560 v664 h-560z" fill="{VOID}"/>'
          f'<path d="M300,240 L760,300 L760,730 L300,790z" fill="url(#beam)"/>'
          f'<path d="M232,180 L520,262 L520,780 L232,844z" fill="{GRAPH}"/>'
          f'<path d="M520,262 L578,286 L578,756 L520,780z" fill="{GRAPH_L}"/>'
          f'<circle cx="380" cy="512" r="70" fill="{GRAPH_D}"/>'),
}

if __name__ == "__main__":
    from PIL import Image
    for name, body in SKETCHES.items():
        p = HERE / f"sketch-{name}.svg"
        p.write_text(wrap(body))
        for s in (1024, 128, 32, 16):
            subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(p),
                            "-o", str(HERE / f"sketch-{name}-{s}.png")], check=True)
    for tag, names in (("1", "abc"), ("2", ("d", "d2", "e")), ("3", "hij")):
        rows = []
        for n in names:
            ims = [Image.open(HERE / f"sketch-{n}-{s}.png").convert("RGBA")
                   .resize((160, 160), Image.NEAREST if s < 64 else Image.LANCZOS)
                   for s in (1024, 128, 32, 16)]
            strip = Image.new("RGBA", (160 * 4 + 90, 160), (255, 255, 255, 255))
            x = 0
            for im in ims:
                strip.alpha_composite(im, (x, 0))
                x += 190
            rows.append(strip)
        out = Image.new("RGBA", (rows[0].width, 200 * len(rows)), (255, 255, 255, 255))
        for i, r in enumerate(rows):
            out.alpha_composite(r, (0, i * 200))
        out.convert("RGB").save(HERE / f"_sketch-strip{tag}.png")
    print(f"wrote {len(SKETCHES)} sketches + 3 contact strips into {HERE}")
