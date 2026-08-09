#!/usr/bin/env python3
"""Engine A master generator - clarify, direction "The Drawn Card".

Three option cards stacked as a list of choices. The recommended one is DRAWN
OUT of the stack to the right, carries a vermilion gel dot in its selection
well, and a vermilion note is written in the margin its own displacement
opened - a proofreader's caret straddling the card's edge, three jotted
strokes beside it.

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
# Cards A and C sit flush in the stack; B is the recommended option, pulled
# DRAW_OUT px to the right and drawn one step larger, so it reads as lifted
# out of the list rather than merely coloured differently.
CARD_X, CARD_W = 168, 440
CARD_R, CARD_H, CARD_WALL = 34, 150, 38
A_Y, C_Y = 238, 580                                    # bodies overlap B by OVERLAP

DRAW_OUT = 62
OVERLAP = 46                                            # >= CARD_WALL: the card behind
                                                       # must hide its own wall band
B_X, B_W = CARD_X + DRAW_OUT, 470
B_Y, B_H, B_WALL, B_R = 382, 172, 42, 38
B_R_EDGE = B_X + B_W                                   # 670 - the margin starts here

# selection well: same inset on every card, so "one of these is marked" is a
# comparison the eye can make rather than a colour it has to interpret
WELL_INSET, WELL_R = 86, 40
DOT_R = 42

# the label rule standing in for the option's text. Sub-legible by design:
# rubric #12 forbids words, and a rule is the UI primitive underneath one.
RULE_W, RULE_H = 210, 18
B_RULE_W = 240

# The margin note, written at the drawn card's own level in the space that card
# opened. Lengths fall away down the block and the whole thing is tilted off
# the horizontal, because three parallel bars of equal weight read as a menu
# glyph and a hand does not write parallel.
NOTE_X = 743
NOTE_LINES = [(444, 118, 6), (486, 92, -5), (528, 58, 4)]   # y, length, bow
NOTE_W = 27
NOTE_TILT = -4.5

KEY = (0.34, 0.26)                                     # one soft top-left light

# ---------------------------------------------------------------- material
GROUND = ("#FFFEFB", "#F5F0E5", "#E2D8C2")             # measured off apple-26:
VIGNETTE = "#9C8D74"                                   # 0.996 -> 0.930 diagonal
RIM_WHITE, RIM_HAIR = 0.72, "#C7B9A0"

# Value carries the hierarchy, not colour: the two options still in the stack
# are clay in the shade, the one drawn out of it is porcelain in the light. That
# is what survives to 16px, where a porcelain glyph on a porcelain field has no
# separation at all and the whole stack goes to a pale blob.
FACE = {                                               # top face, lit corner -> away
    "a": ("#A99D8A", "#8D8170"),
    "b": ("#FEFCF5", "#F1E9D8"),
    "c": ("#A39784", "#877B6A"),
}
WALL = {                                               # the extrusion band
    "a": ("#7A6F5B", "#4C4435"),
    "b": ("#BBAE95", "#7A7059"),
    "c": ("#736858", "#453E30"),
}
CARD_SCATTER = "#FFFBF2"                               # rim scatter: lighter AND
CARD_SCATTER_A, CARD_SCATTER_W = 0.95, 14              # less saturated than the face
FILLET_CARD = 12                                       # face->wall roll, not a step

SHADOW = "#6E6049"                                     # warm; nothing here emits cool
CONTACT = "#41372A"                                    # the hard dark line the
                                                       # reference holds at L 0.408
                                                       # directly under each card
SHADOW_DX, SHADOW_DY = 13, 20
LIFT_DX, LIFT_DY = 22, 33                              # B stands proud of the others

# a rule reads as a line of text, so it sits opposite its own card: dark on the
# lit card, pale on the two in shade
RULE_INK = {"a": "#E4DDCC", "b": "#B7A98F", "c": "#E0D9C8"}
WELL_INK = {"a": "#D7D0BE", "b": "#C6B99F", "c": "#D3CCBA"}

# One vermilion, kin to Fledgeling's #C4622D, spent on the recommendation mark
# and the margin note and nowhere else. The dark end keeps its saturation
# (material-recipes: a shadow that desaturates reads opaque).
# Fitted to the reference dot's own profile rather than assumed: the body is
# nearly FLAT at L 0.47-0.49, the bright ring lives at the rim (0.65-0.71) and
# not at the centre, and the deepest pixel sits at the bottom (0.44) keeping
# its saturation. A bright core reads as gloss; this reads as a gel bead.
GEL = ("#E36C40", "#DA5B31", "#D24B1E", "#A82F0E")
GEL_SCATTER = "#FFD7BC"
WELL_SHADE = "#A8846A"                                 # the recessed ring the
                                                       # bead sits in; measured
                                                       # at L 0.54-0.56
INK = ("#EC7F4C", "#DD5A28")


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


class Card:
    """One option card: a rounded slab with a real extrusion band under its face."""

    def __init__(self, key, x, y, w, h, r, wall, lifted=False):
        self.k, self.x, self.y, self.w, self.h = key, x, y, w, h
        self.r, self.wall, self.lifted = r, wall, lifted

    @property
    def body_h(self):
        return self.h + self.wall

    @property
    def mid_y(self):
        return self.y + self.h / 2

    def defs(self):
        f0, f1 = FACE[self.k]
        w0, w1 = WALL[self.k]
        return [
            lin(f"face{self.k}", self.x, self.y, self.x + self.w, self.y + self.h,
                [(0, f0, None), (1, f1, None)]),
            # Measured on the reference: the wall darkens DOWN its own height
            # (0.702 -> 0.628 over 24px). The lateral lean has to be a SEPARATE
            # overlay - fold it into this vector and x dominates, every point on
            # the band projects past offset 1, and the whole wall renders as one
            # flat colour. That is what a 32px-long dead-flat band was.
            lin(f"wall{self.k}", self.x, self.y + self.h, self.x,
                self.y + self.body_h, [(0, w0, None), (1, w1, None)]),
            lin(f"lean{self.k}", self.x, 0, self.x + self.w, 0,
                [(0, "#FFFFFF", "0.10"), (0.42, "#000000", "0"), (1, "#000000", "0.11")]),
            f'<clipPath id="wallClip{self.k}"><rect x="{self.x:.1f}" y="{self.y + self.h:.1f}" '
            f'width="{self.w:.1f}" height="{self.wall:.1f}"/></clipPath>',
            f'<clipPath id="faceClip{self.k}"><rect x="{self.x:.1f}" y="{self.y:.1f}" '
            f'width="{self.w:.1f}" height="{self.h:.1f}" rx="{self.r}"/></clipPath>',
        ]

    def shadow(self):
        dx, dy = (LIFT_DX, LIFT_DY) if self.lifted else (SHADOW_DX, SHADOW_DY)
        blur = "softL" if self.lifted else "soft"
        op = 0.46 if self.lifted else 0.38
        out = [rect(self.x + dx, self.y + dy, self.w, self.body_h, self.r,
                    SHADOW, f' opacity="{op}" filter="url(#{blur})"')]
        if self.lifted:                                # the tight core under the lift
            out.append(rect(self.x + 6, self.y + 9, self.w, self.body_h, self.r,
                            SHADOW, ' opacity="0.20" filter="url(#tight)"'))
        # The occlusion line. Measured on the reference under B's lower edge:
        # the wall bottoms out near 0.63, then a hard dark line at 0.408, then a
        # 50px recovery. Without that line the stack has no contact anywhere and
        # every boundary inside it is a value step of about 0.06, which is what
        # dissolves the whole thing at 32px.
        out.append(rect(self.x + 3, self.y + 10, self.w, self.body_h, self.r,
                        CONTACT, ' opacity="0.62" filter="url(#hair)"'))
        return out

    def body(self):
        """wall band, top face, and the rolled arris between them."""
        return [
            rect(self.x, self.y, self.w, self.body_h, self.r, f"url(#wall{self.k})"),
            f'<g clip-path="url(#wallClip{self.k})">'
            + rect(self.x, self.y, self.w, self.body_h, self.r, f"url(#lean{self.k})")
            + '</g>',
            rect(self.x, self.y, self.w, self.h, self.r, f"url(#face{self.k})"),
            # the face->wall transition is a fillet painted with the face's OWN
            # gradient, clipped to the wall, so the roll inherits the face's
            # lateral variation and the two cannot drift out of registration
            f'<g clip-path="url(#wallClip{self.k})">'
            f'<path d="M {self.x + self.r} {self.y + self.h} H {self.x + self.w - self.r}" '
            f'stroke="url(#face{self.k})" stroke-width="{FILLET_CARD * 2}" fill="none" '
            f'filter="url(#roll)"/></g>',
        ]

    def rim(self):
        """Top and left rim scatter, clipped inward - the lit shoulder."""
        x, y, w, h, r = self.x, self.y, self.w, self.h, self.r
        d = (f"M {x + 2} {y + h - r} V {y + r} A {r} {r} 0 0 1 {x + r} {y} "
             f"H {x + w - r}")
        return (f'<g clip-path="url(#faceClip{self.k})">'
                f'<path d="{d}" stroke="{CARD_SCATTER}" stroke-opacity="{CARD_SCATTER_A}" '
                f'stroke-width="{CARD_SCATTER_W}" fill="none" stroke-linecap="round" '
                f'filter="url(#rim)"/></g>')


A = Card("a", CARD_X, A_Y, CARD_W, CARD_H, CARD_R, CARD_WALL)
B = Card("b", B_X, B_Y, B_W, B_H, B_R, B_WALL, lifted=True)
C = Card("c", CARD_X, C_Y, CARD_W, CARD_H, CARD_R, CARD_WALL)

DOT_CX, DOT_CY = B.x + WELL_INSET, B.mid_y


def well(card):
    """An empty selection well on the options that carry no recommendation."""
    cx, cy = card.x + WELL_INSET, card.mid_y
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{WELL_R - 4}" fill="none" '
            f'stroke="{WELL_INK[card.k]}" stroke-opacity="0.82" stroke-width="8"/>'
            f'<path d="M {cx - WELL_R + 4} {cy} A {WELL_R - 4} {WELL_R - 4} 0 0 1 '
            f'{cx + WELL_R - 4} {cy}" fill="none" stroke="#4E4635" stroke-opacity="0.24" '
            f'stroke-width="7" filter="url(#rim)"/>')


def rule(card, width):
    x = card.x + WELL_INSET + WELL_R + 34
    return (f'<path d="M {x:.1f} {card.mid_y:.1f} H {x + width:.1f}" '
            f'stroke="{RULE_INK[card.k]}" stroke-opacity="0.92" stroke-width="{RULE_H}" '
            f'stroke-linecap="round" fill="none"/>')


def note_stroke(y, length, bow, x=None):
    """One jotted line: a shallow quadratic so the hand shows at 1024."""
    x = NOTE_X if x is None else x
    return (f'M {x} {y} Q {x + length / 2:.1f} {y + bow} '
            f'{x + length:.1f} {y - bow * 0.4:.1f}')


def note_paths():
    """The margin note: three jotted lines, left-aligned, lengths falling away.

    Treatments tried and dropped (audit.html carries the contact sheet): a
    proofreader's caret straddling the card edge read as an arrow bolted to the
    card; a leader stroke crossing the boundary, and the grey label rule
    continuing into vermilion past the edge, both read as a pointer rather than
    as writing. Whatever the semantics, a long stroke leaving a shape is an
    arrow. The note earns its association by sitting at the drawn card's own
    level, in the margin that card opened - which is what marginalia is.
    """
    return [note_stroke(y, l, b) for y, l, b in NOTE_LINES]

# ---------------------------------------------------------------- document
defs = [
    f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>',
    rad("tile", S * KEY[0], S * KEY[1], S * 0.95,
        [(0, GROUND[0], None), (0.52, GROUND[1], None), (1, GROUND[2], None)]),
    rad("vig", S * 0.5, S * 0.46, S * 0.72,
        [(0.52, VIGNETTE, "0"), (1, VIGNETTE, "0.26")]),
    rad("dot", DOT_CX, DOT_CY, DOT_R,
        [(0, GEL[0], None), (0.55, GEL[1], None), (0.86, GEL[2], None), (1, GEL[3], None)],
        fx=DOT_CX - DOT_R * 0.30, fy=DOT_CY - DOT_R * 0.34),
    lin("ink", NOTE_X, 438, NOTE_X, 556, [(0, INK[0], None), (1, INK[1], None)]),
    f'<mask id="backKey"><rect width="{S}" height="{S}" fill="#FFFFFF"/>'
    + rect(B.x + LIFT_DX, B.y + LIFT_DY, B.w, B.body_h, B.r, "#6E6E6E",
           ' filter="url(#softL)"')
    + rect(B.x, B.y, B.w, B.body_h, B.r, "#000000") + '</mask>',
    '<clipPath id="dotClip"><circle cx="%.1f" cy="%.1f" r="%d"/></clipPath>' % (DOT_CX, DOT_CY, DOT_R),
    '<filter id="soft" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="21"/></filter>',
    '<filter id="softL" x="-70%" y="-70%" width="240%" height="240%">'
    '<feGaussianBlur stdDeviation="32"/></filter>',
    '<filter id="tight" x="-50%" y="-50%" width="200%" height="200%">'
    '<feGaussianBlur stdDeviation="7"/></filter>',
    '<filter id="hair" x="-40%" y="-40%" width="180%" height="180%">'
    '<feGaussianBlur stdDeviation="5"/></filter>',
    '<filter id="rim" x="-40%" y="-40%" width="180%" height="180%">'
    '<feGaussianBlur stdDeviation="3.5"/></filter>',
    '<filter id="roll" x="-40%" y="-40%" width="180%" height="180%">'
    '<feGaussianBlur stdDeviation="5"/></filter>',
    '<filter id="inkShadow" x="-60%" y="-60%" width="220%" height="220%">'
    '<feGaussianBlur stdDeviation="6"/></filter>',
]
for c in (A, B, C):
    defs += c.defs()

bg = [
    f'<rect width="{S}" height="{S}" fill="url(#tile)"/>',
    f'<rect width="{S}" height="{S}" fill="url(#vig)"/>',
    f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-opacity="{RIM_WHITE}" '
    f'stroke-width="10" filter="url(#rim)"/>',
    f'<path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-opacity="0.20" '
    f'stroke-width="2.5"/>',
]

# z-order is the whole structural argument: A and C sit in the back plane, B
# stands in front of both, so B's shadow is painted AFTER them and falls
# across them. A's own shadow lands only on the ground, because whatever it
# would reach downward is occluded by the card in front.
# One shadow for the whole stack, under the three per-card ones. Three cards
# standing together cast a single pooled shadow as well as their own, and it is
# the only dark area broad enough to survive downsampling: per-card shadows are
# 30px features that average away by 16px, where this one still carries the p10.
STACK_SHADOW = rect(min(A.x, B.x) + 16, A.y + 34,
                    max(A.x + A.w, B.x + B.w) - min(A.x, B.x),
                    C.y + C.body_h - A.y - 6, B.r + 12, SHADOW,
                    ' opacity="0.26" filter="url(#softL)"')

mid = [STACK_SHADOW] + A.shadow() + A.body() + [well(A), rule(A, RULE_W)] \
    + C.shadow() + C.body() + [well(C), rule(C, RULE_W)]

fg = B.shadow() + B.body() + [
    rule(B, B_RULE_W),
    # the recommendation: one gel dot, in the same well the others leave empty
    # the bead sits IN the well the other two leave empty, so the ring reads
    # under it: measured on the reference as a dark band at L 0.54-0.56 right
    # at the bead's boundary, and no warm bloom anywhere on the card
    f'<circle cx="{DOT_CX:.1f}" cy="{DOT_CY - 1:.1f}" r="{DOT_R + 4:.1f}" '
    f'fill="{WELL_SHADE}" opacity="0.55" filter="url(#rim)"/>',
    f'<circle cx="{DOT_CX:.1f}" cy="{DOT_CY:.1f}" r="{DOT_R}" fill="url(#dot)"/>',
    # the margin note, written where the drawn card opened the space
    f'<g transform="rotate({NOTE_TILT} {NOTE_X + 62} 492)">'
    + "".join(
        f'<path d="{d}" stroke="#96703F" stroke-opacity="0.22" stroke-width="{NOTE_W}" '
        f'fill="none" stroke-linecap="round" transform="translate(3,5)" '
        f'filter="url(#inkShadow)"/>' for d in note_paths())
    + "".join(
        f'<path d="{d}" stroke="url(#ink)" stroke-width="{NOTE_W}" fill="none" '
        f'stroke-linecap="round"/>' for d in note_paths())
    + '</g>',
]

# The back plane's rim lights see a key that the drawn card both cuts out and
# shadows. Without this the highlight layer breaks z-order and C's lit top edge
# paints a white hairline straight across B's wall - and a rim at full strength
# inside a cast shadow is the single light model contradicting itself.
highlight = [f'<g mask="url(#backKey)">{A.rim()}{C.rim()}</g>', B.rim(),
             # the gel's own rim scatter: lighter and less saturated in one move,
             # all the way round, because a translucent body lights at every
             # grazing angle rather than only where the key points
             f'<g clip-path="url(#dotClip)"><circle cx="{DOT_CX:.1f}" cy="{DOT_CY:.1f}" '
             f'r="{DOT_R - 3}" fill="none" stroke="{GEL_SCATTER}" stroke-opacity="0.42" '
             f'stroke-width="9" filter="url(#rim)"/>'
             f'<path d="M {DOT_CX - DOT_R + 4:.1f} {DOT_CY + 6:.1f} '
             f'A {DOT_R - 4} {DOT_R - 4} 0 0 1 {DOT_CX + 8:.1f} {DOT_CY - DOT_R + 4:.1f}" '
             f'fill="none" stroke="{GEL_SCATTER}" stroke-opacity="0.50" stroke-width="10" '
             f'filter="url(#rim)"/></g>',
             # one soft sheen where the key actually lands
             f'<ellipse cx="330" cy="300" rx="210" ry="150" fill="#FFFFFF" opacity="0.07" '
             f'filter="url(#softL)"/>']


def layer(name, items):
    return f'    <g id="{name}">\n' + "\n".join("      " + i for i in items) + "\n    </g>"


svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>clarify</title>
  <desc>Three option cards; the recommended one drawn out of the stack with a vermilion
  dot in its selection well, and a vermilion note written in the margin beside it.
  Full-bleed 1024 artwork; the marketplace superellipse is a CLIP, never a baked corner
  radius and never a baked drop shadow.</desc>
  <defs>
    {chr(10).join("    " + d for d in defs).strip()}
  </defs>
  <g clip-path="url(#mask)">
{layer("bg", bg)}
{layer("mid", mid)}
{layer("fg", fg)}
{layer("highlight", highlight)}
  </g>
</svg>
'''

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ASSETS / "icon.svg")
    out.write_text(svg)
    print("wrote", out, len(svg), "bytes")
