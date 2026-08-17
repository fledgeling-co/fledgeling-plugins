#!/usr/bin/env python3
"""Engine A master generator — geminify, direction "The Second Leaf".

Two leaves of the same page, leaning together: the left one clay and in shade
(the SKILL.md, as written), the right one warm tinted glass (the gemini.md this
skill produces). Where they overlap, and ONLY there, three tally rules are
engraved into the blend — the bottom one filled and lit from inside. That is the
signature move and the whole semantic: the count exists only in the overlap. A
categorical scope stays a word until a second reading turns it into a number.

Geometry and material are named constants; every fidelity round is a parameter
edit here, never path surgery in icon.svg.

    python3 build_icon.py [out.svg]

Emits 1024x1024 full-bleed layered artwork (bg / mid / fg / highlight). The
marketplace superellipse is a CLIP, never a baked corner radius and never a
baked drop shadow.
"""
import pathlib
import sys

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- geometry
# Two leaves of one page as poured gel CAPSULES, not cards. The first pass drew
# them as 336x504 slabs at r=46 with a 120px overlap and the render read as two
# phone cases with a seam between them: a card proportion says "card", the narrow
# overlap says "edge", and neither says "a pair". A capsule is the family's
# poured-gel primitive, and an overlap of 55% of the width makes the blend zone a
# real almond - which is the identity here, not the outlines.
LEAF_W, LEAF_H, LEAF_WALL = 420, 566, 0
LEAF_R = LEAF_W / 2                                    # full capsule ends
OVERLAP = 220                                          # face-to-face, pre-rotation
L_X = 202                                              # span = W + (W - OVERLAP) = 620,
R_X = L_X + LEAF_W - OVERLAP                           # 402   61% of the tile
L_Y, R_Y = 205, 181                                    # right leaf rides higher:
                                                       # the newer file sits on top
LEAN = 11                                              # left -LEAN, right +LEAN;
                                                       # they splay from a shared base
# LEAF_WALL is 0 deliberately: with r = W/2 the extrusion band the sibling cards
# use sits entirely inside the capsule's round end, so it drew nothing. Volume
# here comes from the body's luminance RANGE plus the two side catches, and
# grounding from the two-layer contact shadow - measured as the cheapest
# depth move in this marketplace.

# The tally rules live inside the almond, which is at its widest across the
# middle - so they sit there, and their lengths fall away down the block. A hand
# does not write parallel bars of equal length; three of those read as a menu
# glyph rather than as a ledger.
RULES = [(440, 62, -3.0), (505, 52, 2.5), (570, 42, -1.5)]   # y, half-length, tilt
RULE_H = 16
RULE_CX = 512                                          # the almond's own centre line
COUNTED = 2                                            # index of the filled rule

KEY = (0.32, 0.24)                                     # one soft top-left light

# ---------------------------------------------------------------- material
# Ground is the set's, unchanged, so this icon sits on the same shelf as its
# siblings: measured off apple-26 for clarify and reused verbatim here.
GROUND = ("#FFFEFB", "#F5F0E5", "#E2D8C2")
VIGNETTE = "#9C8D74"                                   # 0.996 -> 0.930 diagonal
RIM_WHITE, RIM_HAIR = 0.72, "#C7B9A0"

# Value carries the pair, not colour. Both leaves sit BELOW the ground on the
# value ramp, because a porcelain glyph on a porcelain field has no separation
# at 16px and the whole object goes to a pale blob (measured on clarify, whose
# nine gate ACCEPTs were buying similarity to exactly that weakness).
FACE_L = ("#BDB19C", "#6E6353")                        # clay, in shade
WALL_L = ("#7A6F5B", "#4A4234")   # unused while LEAF_WALL == 0
# The right leaf is TINTED GLASS, not the accent itself: saturation has to climb
# toward the lens, so the leaf runs mid-warm and the blend below it runs deep.
FACE_R = ("#F0AE7C", "#B15A22")
WALL_R = ("#A8562A", "#79380F")   # unused while LEAF_WALL == 0

SCATTER = "#FFFBF2"                                    # rim scatter: lighter AND
SCATTER_A, SCATTER_W = 0.95, 14                        # less saturated than the face
SCATTER_R, SCATTER_R_A = "#FFE2C8", 0.80               # warm leaf gets a warm rim
FILLET = 12                                            # face->wall roll, not a step

SHADOW = "#6E6049"                                     # warm; nothing here emits cool
CONTACT = "#41372A"                                    # the hard dark line under
SHADOW_DX, SHADOW_DY = 16, 26                          # each leaf's lower edge
LIFT_DX, LIFT_DY = 24, 38                              # the right leaf stands proud

# The lens: the two translucent leaves multiplying through each other. Authored
# as a real overlap - the front leaf is drawn semi-opaque so the one behind it is
# visible THROUGH it, and the wash below only deepens what the overlap already
# does. Baking the blend as a third fill kills it under system tinting, and the
# bleed-through IS the era tell.
FACE_R_A = 0.84                                        # the front leaf's own glass
LENS = ("#8A3F1C", "#5E240C")
LENS_A = 0.55

# Engraved rules: a groove is a dark trough with its LOWER inner face catching
# the light, so the lit lip sits under the dark line, never over it. Assuming
# highlight-is-above has failed here three times on record.
GROOVE = "#42190A"
GROOVE_A = 0.78
LIP, LIP_A = "#FFD6B0", 0.30

# One vermilion, kin to Fledgeling's #C4622D, spent on the counted rule and
# nowhere else. Vibrancy is emission, not saturation: a hot core UNDER the bar
# lighting the trough it sits in, then the bar itself, then a bloom above.
GEL = ("#F79A54", "#EC7433", "#D9531A")
CORE, CORE_A = "#FF7A33", 0.62
BLOOM, BLOOM_A = "#F9C48E", 0.34


# ---------------------------------------------------------------- helpers
def rect(x, y, w, h, r, fill, extra=""):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{r}" fill="{fill}"{extra}/>')


def lin(i, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<linearGradient id="{i}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def rad(i, cx, cy, r, stops, fx=None, fy=None):
    f = "" if fx is None else f' fx="{fx:.1f}" fy="{fy:.1f}"'
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<radialGradient id="{i}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"{f} '
            f'gradientUnits="userSpaceOnUse">{s}</radialGradient>')


def mix(a, b, t):
    """Interpolate two hex colours. Used to derive the interior stops of a body's
    profile from its two endpoints, so a luminance-range edit stays a two-value
    edit rather than five hand-kept-in-sync literals."""
    pa = tuple(int(a[i:i + 2], 16) for i in (1, 3, 5))
    pb = tuple(int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


class Leaf:
    """One leaf of the page: a rounded slab with an extrusion band under its face."""

    def __init__(self, key, x, y, lean, face, wall, scatter, scatter_a,
                 lifted=False, alpha=1.0):
        self.k, self.x, self.y, self.lean = key, x, y, lean
        self.face, self.wall = face, wall
        self.scatter, self.scatter_a = scatter, scatter_a
        self.lifted, self.alpha = lifted, alpha
        self.w, self.h, self.r, self.wallh = LEAF_W, LEAF_H, LEAF_R, LEAF_WALL

    @property
    def body_h(self):
        return self.h + self.wallh

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.body_h / 2

    @property
    def spin(self):
        return f'rotate({self.lean:.2f} {self.cx:.1f} {self.cy:.1f})'

    def defs(self):
        f0, f1 = self.face
        # A monotonic two-stop fade has none of the three features that make a
        # poured body volumetric, and the first render read as two flat pebbles
        # because of it. This is the measured frosted-capsule profile: bright top
        # rim, a gentle fall, a SLOWER middle where the body's brightest in-mass
        # pixel lives, a distinct drop through the lower third, then a small lift
        # at the base. Four stops cannot express the base lift.
        mid = mix(f0, f1, 0.34)
        low = mix(f0, f1, 0.86)
        return [
            lin(f"face{self.k}", self.x, self.y, self.x, self.y + self.h,
                [(0, f0, None), (0.16, mix(f0, f1, 0.10), None),
                 (0.44, mid, None), (0.78, low, None),
                 (1, mix(f0, f1, 0.72), None)]),
            # The lateral lean is a SEPARATE layer: a gradient carries one axis, and
            # folding a sideways component into the vector above makes x dominate,
            # so every point projects past offset 1 and the whole body renders as
            # one flat colour. That failure is invisible in the source.
            lin(f"lean{self.k}", self.x, 0, self.x + self.w, 0,
                [(0, "#FFFFFF", "0.13"), (0.46, "#000000", "0"), (1, "#000000", "0.14")]),
            # Both side edges catch light, the key side harder. A top-only highlight
            # reads as a stripe on a capsule rather than as a turned edge.
            lin(f"sideL{self.k}", self.x, 0, self.x + self.w * 0.09, 0,
                [(0, self.scatter, str(round(self.scatter_a * 0.85, 2))),
                 (1, self.scatter, "0")]),
            lin(f"sideR{self.k}", self.x + self.w, 0, self.x + self.w * 0.92, 0,
                [(0, self.scatter, str(round(self.scatter_a * 0.42, 2))),
                 (1, self.scatter, "0")]),
            # The leaf's own outline as a clip, carrying its rotation, so the lens
            # below can be built as the INTERSECTION of the two clips rather than
            # as a shape somebody drew by hand at the right place.
            f'<clipPath id="leaf{self.k}"><rect x="{self.x:.1f}" y="{self.y:.1f}" '
            f'width="{self.w:.1f}" height="{self.body_h:.1f}" rx="{self.r}" '
            f'transform="{self.spin}"/></clipPath>',
            lin(f"rimGrad{self.k}", self.x, self.y, self.x + self.w,
                self.y + self.h * 0.62,
                [(0, self.scatter, str(self.scatter_a)),
                 (0.34, self.scatter, str(round(self.scatter_a * 0.45, 2))),
                 (0.62, self.scatter, "0")]),
        ]

    def shadow(self):
        dx, dy = (LIFT_DX, LIFT_DY) if self.lifted else (SHADOW_DX, SHADOW_DY)
        blur = "softL" if self.lifted else "soft"
        op = 0.50 if self.lifted else 0.42
        # A contact shadow is two layers or it is a smudge: a wide ambient falloff
        # plus a tight dark core hugging the base. The wide one alone reads as fog.
        out = [rect(self.x + dx, self.y + dy, self.w, self.body_h, self.r,
                    SHADOW, f' opacity="{op}" filter="url(#{blur})"'),
               rect(self.x + dx * 0.4, self.y + dy * 0.5, self.w, self.body_h,
                    self.r, CONTACT, ' opacity="0.34" filter="url(#tight)"')]
        return [f'<g transform="{self.spin}">'] + out + ['</g>']

    def body(self):
        """The poured body: vertical profile, lateral lean, then the side catches."""
        op = "" if self.alpha >= 1 else f' opacity="{self.alpha}"'
        return [
            f'<g transform="{self.spin}"{op}>',
            rect(self.x, self.y, self.w, self.h, self.r, f"url(#face{self.k})"),
            f'<g clip-path="url(#leaf{self.k})">'
            + rect(self.x, self.y, self.w, self.h, self.r, f"url(#lean{self.k})")
            + rect(self.x, self.y, self.w * 0.09, self.h, 0, f"url(#sideL{self.k})")
            + rect(self.x + self.w * 0.91, self.y, self.w * 0.09, self.h, 0,
                   f"url(#sideR{self.k})")
            + '</g>',
            '</g>',
        ]

    def rim(self):
        """The lit edge. The catch has to DIE where the curve turns away from the
        key, so it is a stroke painted with a fading gradient along the key's own
        axis - stroking the whole outline at one opacity rings the object and reads
        as a sticker halo rather than as a lit edge."""
        return [
            f'<g transform="{self.spin}" clip-path="url(#leaf{self.k})">',
            f'<rect x="{self.x:.1f}" y="{self.y:.1f}" width="{self.w:.1f}" '
            f'height="{self.h:.1f}" rx="{self.r}" fill="none" '
            f'stroke="url(#rimGrad{self.k})" stroke-width="{SCATTER_W}" '
            f'filter="url(#hair)"/>',
            '</g>',
        ]


LEFT = Leaf("l", L_X, L_Y, -LEAN, FACE_L, WALL_L, SCATTER, SCATTER_A)
RIGHT = Leaf("r", R_X, R_Y, LEAN, FACE_R, WALL_R, SCATTER_R, SCATTER_R_A,
             lifted=True, alpha=FACE_R_A)


def lens_defs():
    return [
        lin("lensRamp", 0, RIGHT.y, 0, LEFT.y + LEFT.body_h,
            [(0, LENS[0], None), (1, LENS[1], None)]),
        rad("coreGlow", RULE_CX, RULES[COUNTED][0] + RULE_H / 2, 118,
            [(0, CORE, str(CORE_A)), (0.55, CORE, "0.16"), (1, CORE, "0")]),
        lin("gelBar", 0, RULES[COUNTED][0], 0, RULES[COUNTED][0] + RULE_H,
            [(0, GEL[0], None), (0.5, GEL[1], None), (1, GEL[2], None)]),
    ]


def lens():
    """Everything that exists only where the two leaves cross.

    Nested clips, so this region is the real intersection of the two rotated
    outlines. Each clipPath holds a single subpath: an SVG clipPath with two
    subpaths and no clip-rule silently UNIONS them, which would spill the whole
    wash across both leaves.
    """
    out = [f'<g clip-path="url(#leafl)"><g clip-path="url(#leafr)">']
    out.append(rect(0, 0, S, S, 0, "url(#lensRamp)", f' opacity="{LENS_A}"'))
    # the emissive core sits UNDER the bar, lighting the trough it lies in
    out.append(rect(0, 0, S, S, 0, "url(#coreGlow)", ' filter="url(#softL)"'))
    for i, (y, half, tilt) in enumerate(RULES):
        x = RULE_CX - half
        spin = f'rotate({tilt:.2f} {RULE_CX} {y + RULE_H / 2:.1f})'
        if i == COUNTED:
            out.append(f'<g transform="{spin}">'
                       + rect(x, y, half * 2, RULE_H, RULE_H / 2, "url(#gelBar)")
                       + '</g>')
        else:
            out.append(f'<g transform="{spin}">'
                       + rect(x, y, half * 2, RULE_H, RULE_H / 2, GROOVE,
                              f' opacity="{GROOVE_A}"')
                       # the lit lower face of the groove
                       + rect(x + 3, y + RULE_H - 2, half * 2 - 6, 5, 2.5, LIP,
                              f' opacity="{LIP_A}" filter="url(#hair)"')
                       + '</g>')
    out.append('</g></g>')
    return out


def bloom():
    """The counted rule's light, spilling past the lens onto the leaf above it."""
    y = RULES[COUNTED][0] + RULE_H / 2
    return [
        f'<g clip-path="url(#leafr)">',
        f'<ellipse cx="{RULE_CX}" cy="{y:.1f}" rx="132" ry="74" fill="{BLOOM}" '
        f'opacity="{BLOOM_A}" filter="url(#softL)"/>',
        '</g>',
    ]


def build():
    d = []
    d.append(f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>')
    d.append(rad("ground", S * 0.34, S * 0.26, S * 0.96,
                 [(0, GROUND[0], None), (0.52, GROUND[1], None), (1, GROUND[2], None)]))
    d.append(rad("vig", S * 0.5, S * 0.5, S * 0.72,
                 [(0, VIGNETTE, "0"), (0.72, VIGNETTE, "0.05"), (1, VIGNETTE, "0.17")]))
    for f, sd in (("soft", 26), ("softL", 40), ("tight", 12), ("hair", 5)):
        d.append(f'<filter id="{f}" x="-45%" y="-45%" width="190%" height="190%">'
                 f'<feGaussianBlur stdDeviation="{sd}"/></filter>')
    d += LEFT.defs() + RIGHT.defs() + lens_defs()

    bg = [rect(0, 0, S, S, 0, "url(#ground)"),
          rect(0, 0, S, S, 0, "url(#vig)"),
          f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-width="7" '
          f'opacity="{RIM_WHITE}"/>',
          f'<path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-width="2" '
          f'opacity="0.30"/>']

    mid = LEFT.shadow() + LEFT.body() + RIGHT.shadow()
    fg = RIGHT.body() + lens()
    hi = LEFT.rim() + RIGHT.rim() + bloom()

    groups = "".join(
        f'<g id="{name}">' + "".join(items) + "</g>"
        for name, items in (("bg", bg), ("mid", mid), ("fg", fg), ("highlight", hi))
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
            f'viewBox="0 0 {S} {S}">'
            f'<defs>{"".join(d)}</defs>'
            f'<g clip-path="url(#mask)">{groups}</g></svg>\n')


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ASSETS / "icon.svg"
    out.write_text(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
