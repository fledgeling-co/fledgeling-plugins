#!/usr/bin/env python3
"""Build the deck-craft icon master.

Direction 2 (Tahoe gel-glass), sub-register (a): a porcelain cushion carrying gel
objects. Device: **the running order** — four identical 16:9 slide plates standing
in sequence, the one you are on in front as a graphite gel slab, the rest of the
deck receding behind it in frosted porcelain, and the same vermilion title band on
every single face.

The signature move is that the accent belongs to the sequence rather than to a
slide: one mark, at the same place on every plate, and its climb from front to
back *is* the running order. Re-order a plate and the climb breaks. That performs
the skill's own claim — the titles read in order are the deck's argument — instead
of illustrating it.

Everything geometric or material is a named constant, so a fidelity round is a
parameter edit rather than path surgery and a banner can be derived from the same
numbers: LIGHT_ANGLE_DEG / LIGHT_AXIS for the light, Spec.plate_w with
PLATE_ASPECT for the cell, Spec.step_x / step_y for the sequence, and
ACCENT / ACCENT_HI / ACCENT_DEEP for the one warm hue.

    python3 build_icon.py                      # writes icon.svg beside this file
    python3 build_icon.py --set step_y=64 --out /tmp/try.svg
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field, replace
from pathlib import Path

HERE = Path(__file__).resolve().parent
SQUIRCLE_PATH = (HERE / ".." / ".." / "create-mac-icon" / "assets"
                 / "squircle-path.txt")

S = 1024                     # canvas — full bleed, masked by the family squircle
PLATE_ASPECT = 16 / 9        # the fixed stage every plate is cut to

# ---------------------------------------------------------------- light model
# One soft key light from the upper left. Every cast, catch and ramp reads this
# pair, so a derived banner can light itself from the same two numbers.
LIGHT_ANGLE_DEG = 118.0
LIGHT_AXIS = (math.cos(math.radians(LIGHT_ANGLE_DEG)),
              math.sin(math.radians(LIGHT_ANGLE_DEG)))      # ≈ (-0.47, +0.88)

# ---------------------------------------------------------------- the cushion
# Porcelain/daylight, sampled off the family rather than invented:
# create-test-suite #F8F5EE→#E4DDCB, whats-left #F6F3EA→#E0D9C8,
# proctor #F8F4EC→#E9E2D4.
GROUND_HI = "#FCFAF4"
GROUND_MID = "#F3EDE1"
GROUND_LO = "#DED5C2"
GROUND_RIM = "#FFFDF8"       # the inner rim light every Tahoe tile carries
GROUND_VIGNETTE = "#8B7F66"
SHADOW = "#3B3327"           # warm, never blue — the corpus's shaded faces are warm

# ---------------------------------------------------------------- the accent
# One warm hue, spent once — on the title band, which is the semantic element.
# Family band measured off the siblings: report #E46235, whats-left #DF612E,
# clarify #E0612E, dossier-report #EA5B34 — kin to Fledgeling #C4622D.
ACCENT = "#DE5A28"
ACCENT_HI = "#F79155"
ACCENT_DEEP = "#A63B14"

# ------------------------------------------------------------ the plate faces
# The plate you are on is a warm graphite gel slab — deck-craft's own dark-canvas
# register — and the deck behind it is frosted porcelain, each plate a value step
# flatter as it recedes. The order is carried by value and position rather than by
# hue, which is what keeps it legible in grayscale and under a system tint.
PLATE_FACES = [
    #  hi         lo         seat edge   side face (the slab's own thickness)
    ("#6E6353", "#413929", "#241E13", "#332C1F"),   # the plate you are on
    ("#FFFEFB", "#EFE7D5", "#B0A48A", "#CFC4AC"),
    ("#F7F1E3", "#E2D9C4", "#A79A7F", "#C3B9A0"),
    ("#EDE6D6", "#D3C9B4", "#9A8D72", "#B5AA90"),
]


@dataclass
class Spec:
    """Every geometric decision in one place, so a round is a parameter edit."""

    n_plates: int = 4
    plate_w: float = 444            # one fixed 16:9 stage, repeated without scaling
    step_x: float = 112             # how far each plate stands to the right
    step_y: float = 76              # and how far back it stands — the order climbs
    tilt: float = -3.0              # the whole deck, barely tipped
    corner: float = 22
    thickness: float = 10           # the slab's own side face, on the plates behind
    rule_top: float = 0.335         # the title band, as a fraction of plate height
    rule_h: float = 0.115           # a display-tier band, not a hairline
    translucency: float = 0.90      # gel: what is behind bleeds faintly through
    cast_dx: float = 9
    cast_dy: float = 14
    cast_blur: float = 13
    contact_opacity: float = 0.38   # the leading plate onto the cushion
    stack_opacity: float = 0.34     # each plate onto the plate standing behind it
    lift: float = 10                # optical centring nudge: the shadows fall
                                    # down-right, so the geometry sits a little high
    faces: list = field(default_factory=lambda: [tuple(f) for f in PLATE_FACES])

    @property
    def plate_h(self) -> float:
        return round(self.plate_w / PLATE_ASPECT)       # the 16:9 contract

    def origins(self) -> list[tuple[float, float]]:
        """Plate origins in local space, the plate you are on first."""
        return [(i * self.step_x, -i * self.step_y) for i in range(self.n_plates)]


def rounded(x: float, y: float, w: float, h: float, r: float) -> str:
    r = min(r, w / 2, h / 2)
    return (f"M{x + r:.1f},{y:.1f} h{w - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{r:.1f} v{h - 2 * r:.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{r:.1f} h{-(w - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {-r:.1f},{-r:.1f} v{-(h - 2 * r):.1f} "
            f"a{r:.1f},{r:.1f} 0 0 1 {r:.1f},{-r:.1f} z")


def placement(sp: Spec) -> tuple[float, float]:
    """Translation that centres the tilted deck optically on the tile."""
    t = math.radians(sp.tilt)
    pts = []
    for ox, oy in sp.origins():
        for cx, cy in ((ox, oy), (ox + sp.plate_w, oy), (ox, oy + sp.plate_h),
                       (ox + sp.plate_w, oy + sp.plate_h)):
            pts.append((cx * math.cos(t) - cy * math.sin(t),
                        cx * math.sin(t) + cy * math.cos(t)))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    return (S - bw) / 2 - min(xs), (S - bh) / 2 - min(ys) + sp.lift


def build(sp: Spec) -> str:
    squircle = SQUIRCLE_PATH.read_text().strip()
    tx, ty = placement(sp)
    origins = sp.origins()
    w, h = sp.plate_w, sp.plate_h
    rule_y, rule_h = h * sp.rule_top, h * sp.rule_h
    lx, ly = LIGHT_AXIS

    out: list[str] = []
    add = out.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">')

    # ------------------------------------------------------------------ defs
    add("<defs>")
    add(f'<radialGradient id="cushion" cx="0.40" cy="0.28" r="0.88">'
        f'<stop offset="0" stop-color="{GROUND_HI}"/>'
        f'<stop offset="0.56" stop-color="{GROUND_MID}"/>'
        f'<stop offset="1" stop-color="{GROUND_LO}"/></radialGradient>')
    add(f'<radialGradient id="vignette" cx="0.5" cy="0.5" r="0.72">'
        f'<stop offset="0.56" stop-color="{GROUND_VIGNETTE}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{GROUND_VIGNETTE}" stop-opacity="0.26"/>'
        f'</radialGradient>')
    for i, (hi, lo, _e, _s) in enumerate(sp.faces[:sp.n_plates]):
        add(f'<linearGradient id="face{i}" x1="{0.5 + lx * 0.85:.3f}" '
            f'y1="{0.5 - ly * 0.85:.3f}" x2="{0.5 - lx * 0.85:.3f}" '
            f'y2="{0.5 + ly * 0.85:.3f}">'
            f'<stop offset="0" stop-color="{hi}"/>'
            f'<stop offset="1" stop-color="{lo}"/></linearGradient>')
    add('<linearGradient id="sheen" x1="0.05" y1="0" x2="0.38" y2="1">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.72"/>'
        '<stop offset="0.46" stop-color="#FFFFFF" stop-opacity="0.15"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    add(f'<linearGradient id="rulefill" x1="0" y1="0" x2="0.03" y2="1">'
        f'<stop offset="0" stop-color="{ACCENT_HI}"/>'
        f'<stop offset="0.36" stop-color="{ACCENT}"/>'
        f'<stop offset="1" stop-color="{ACCENT_DEEP}"/></linearGradient>')
    add(f'<linearGradient id="rulebloom" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{ACCENT}" stop-opacity="0.26"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>')
    add(f'<filter id="cast" x="-40%" y="-40%" width="190%" height="200%">'
        f'<feDropShadow dx="{sp.cast_dx}" dy="{sp.cast_dy}" '
        f'stdDeviation="{sp.cast_blur}" flood-color="{SHADOW}" '
        f'flood-opacity="{sp.stack_opacity}"/></filter>')
    add(f'<filter id="castfront" x="-40%" y="-40%" width="190%" height="205%">'
        f'<feDropShadow dx="{sp.cast_dx + 2}" dy="{sp.cast_dy + 8}" '
        f'stdDeviation="{sp.cast_blur + 8}" flood-color="{SHADOW}" '
        f'flood-opacity="{sp.contact_opacity}"/></filter>')
    add('<filter id="soften" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="9"/></filter>')
    for i, (ox, oy) in enumerate(origins):
        add(f'<clipPath id="pc{i}"><path d="'
            f'{rounded(ox, oy, w, h, sp.corner)}"/></clipPath>')
    add(f'<clipPath id="tile"><path d="{squircle}"/></clipPath>')
    add("</defs>")

    add('<g clip-path="url(#tile)">')

    # -------------------------------------------------------------------- bg
    add('<g id="bg">')
    add(f'<rect width="{S}" height="{S}" fill="url(#cushion)"/>')
    add(f'<rect width="{S}" height="{S}" fill="url(#vignette)"/>')
    add(f'<path d="{squircle}" fill="none" stroke="{GROUND_RIM}" stroke-width="7" '
        f'stroke-opacity="0.85"/>')
    add("</g>")

    add(f'<g transform="translate({tx:.1f} {ty:.1f}) rotate({sp.tilt})">')

    def plate(i: int) -> list[str]:
        ox, oy = origins[i]
        hi, lo, edge, side = sp.faces[i]
        behind = i > 0
        body = rounded(ox, oy, w, h, sp.corner)
        p: list[str] = []
        # 1 · what this plate casts — onto the cushion if it leads, onto the plate
        #     standing behind it otherwise. One light, so one shadow direction.
        p.append(f'<path d="{body}" fill="{SHADOW}" '
                 f'filter="url(#{"cast" if behind else "castfront"})"/>')
        # 2 · the slab's own thickness, showing along its right edge
        if behind and sp.thickness:
            p.append(f'<path d="'
                     f'{rounded(ox + w - sp.thickness, oy, sp.thickness * 2, h, sp.corner)}" '
                     f'fill="{side}"/>')
        # 3 · the gel face, ramped along the light axis. The porcelain plates are
        #     translucent, so what stands behind them bleeds faintly through.
        p.append(f'<path d="{body}" fill="url(#face{i})"'
                 + (f' fill-opacity="{sp.translucency}"' if behind else "") + "/>")
        # 4 · gel sheen across the upper face
        p.append(f'<g clip-path="url(#pc{i})">'
                 f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{w:.1f}" '
                 f'height="{h * 0.60:.1f}" fill="url(#sheen)" '
                 f'opacity="{0.34 if behind else 0.52}"/></g>')
        # 5 · the title band — the same mark, at the same height, on every plate.
        #     Read front to back it climbs, and that climb is the running order.
        #     The warm bounce is a kiss on the face just under the band, never a
        #     wash: a broad low-alpha veil browns a whole face while every
        #     measurement of the palette still says the colours are right.
        p.append(f'<g clip-path="url(#pc{i})">')
        p.append(f'<rect x="{ox:.1f}" y="{oy + rule_y + rule_h:.1f}" width="{w:.1f}" '
                 f'height="{rule_h * 0.85:.1f}" fill="url(#rulebloom)" '
                 f'filter="url(#soften)"/>')
        p.append(f'<rect x="{ox:.1f}" y="{oy + rule_y:.1f}" width="{w:.1f}" '
                 f'height="{rule_h:.1f}" fill="url(#rulefill)"/>')
        p.append(f'<rect x="{ox:.1f}" y="{oy + rule_y:.1f}" width="{w:.1f}" '
                 f'height="{max(3.0, rule_h * 0.13):.1f}" fill="{ACCENT_HI}" '
                 f'fill-opacity="0.92"/>')
        p.append("</g>")
        # 6 · seat edge all round, then the key light's catch on the top and left
        #     edges only — the two faces it actually reaches
        p.append(f'<path d="{body}" fill="none" stroke="{edge}" stroke-width="2.5" '
                 f'stroke-opacity="0.85"/>')
        p.append(f'<path d="M{ox + 1.5:.1f},{oy + h - sp.corner:.1f} '
                 f'V{oy + sp.corner:.1f} a{sp.corner},{sp.corner} 0 0 1 '
                 f'{sp.corner},{-sp.corner} h{w - 2 * sp.corner:.1f}" '
                 f'fill="none" stroke="{"#FFFFFF" if behind else "#FFEBCF"}" '
                 f'stroke-width="3.5" stroke-opacity="{0.55 if behind else 0.92}" '
                 f'stroke-linecap="round"/>')
        return p

    add('<g id="mid">')                     # the deck behind, furthest first
    for i in range(sp.n_plates - 1, 0, -1):
        out.extend(plate(i))
    add("</g>")
    add('<g id="fg">')                      # the plate you are on
    out.extend(plate(0))
    add("</g>")
    add('<g id="highlight">')               # the bounce the leading band throws
    add(f'<rect x="{-14:.1f}" y="{rule_y + rule_h * 0.6:.1f}" '
        f'width="{w + 28:.1f}" height="{rule_h * 1.1:.1f}" fill="url(#rulebloom)" '
        f'opacity="0.20" filter="url(#soften)"/>')
    add("</g>")
    add("</g>")

    add("</g>")   # tile
    add("</svg>")
    return "\n".join(out)


NUMERIC = {"n_plates", "plate_w", "step_x", "step_y", "tilt", "corner", "thickness",
           "rule_top", "rule_h", "translucency", "cast_dx", "cast_dy", "cast_blur",
           "contact_opacity", "stack_opacity", "lift"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--set", action="append", default=[],
                    help="override a numeric Spec field, e.g. --set step_y=64")
    a = ap.parse_args()
    sp = Spec()
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in NUMERIC:
            raise SystemExit(f"unknown or non-numeric field: {k}")
        sp = replace(sp, **{k: int(v) if k == "n_plates" else float(v)})
    out = Path(a.out) if a.out else HERE / "icon.svg"
    out.write_text(build(sp))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
