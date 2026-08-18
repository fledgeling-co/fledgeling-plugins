#!/usr/bin/env python3
"""Icon master generator — agent-voice, direction "the cursor speaks".

One terminal block cursor in clay, standing in shade, with two quote strokes cut
clean through its upper half and lit from behind. That is the whole semantic: the
block is what an agent emits, and the voice is the part where light gets through.
The accent is spent on the two cuts and nowhere else.

The first take set the strokes BESIDE a notched block, and it failed on three
counts worth keeping as a record rather than rediscovering: the notch read as a
folded document corner rather than as a caret, the strokes floated with no visual
link to the block, and the mass piled into the lower left with the accents
stranded top-right. Cutting the strokes through the body fixes all three at once,
because one shape cannot come apart, and it is the version that survives 128px —
a dark block with two bright slashes near the top.

Geometry and material are named constants; a revision is a parameter edit here,
never path surgery in icon.svg.

    python3 build_icon.py [out.svg]
    python3 build_icon.py --take t2 icon-take2.svg

The losing takes are reproducible rather than described, because a contact sheet
exists to show what lost. Take 1 is the exception and is prose-only: it had a
different path structure (strokes beside a notched block) that this file no
longer contains, and reinstating dead geometry to photograph it would be worse
than saying so.

Emits 1024x1024 full-bleed layered artwork (bg / mid / fg / highlight). The
marketplace superellipse is a CLIP, never a baked corner radius and never a baked
drop shadow, so system tinting and the site's own rounding both still work.
"""
import pathlib
import sys

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ---------------------------------------------------------------- geometry
# The cursor is a BLOCK, so a rounded rect rather than the set's capsule
# primitive: a capsule reads as a pill or a battery, and a terminal caret is
# square-shouldered. 380x500 at r=54 reads as a caret; the first take's 300x560
# read as a phone.
# Presence: the block occupies 53% of the tile's width and 72% of its height.
# Measured off the siblings at 128px rather than guessed - geminify's leaves fill
# about 65% of the tile, tui-craft's panel 72%, clarify's stack 78%. Three takes
# here sat at 29-48% and each read as a small tile adrift in a large field.
CUR_W, CUR_H, CUR_R = 546, 736, 84
CUR_X = (S - CUR_W) / 2
CUR_Y = (S - CUR_H) / 2 + 8      # a shade low, so the cuts sit on the optical centre

# Two quote strokes cut THROUGH the body. Each is a chisel wedge: broad at the
# top, tapering down, the shape a nib actually makes. They sit in the upper half
# so the solid mass below reads as the block they were cut from, and they are
# wide enough that each survives as its own mark at 128px rather than merging.
# Taper is modest on purpose. At 82->30 the cuts read as fangs rather than as
# quote marks: a typographic quote is closer to parallel-sided with a wedge foot.
CUT_W_TOP, CUT_W_BOT = 108, 50
CUT_H = 486   # reaches 63% down the block: the marks lead, the base frames
CUT_GAP = 66                     # between the two cuts, measured at the top
CUT_LEAN = 7                     # degrees; both lean the same way
# The cuts START ABOVE the block's top edge and are clipped to the body, so each
# arrives as an OPEN notch in the top rather than an enclosed slot. That single
# change is what stops the icon reading as a light-switch plate: a plain rounded
# rectangle with two enclosed vertical slots is a switch plate, and no amount of
# material work argues with a silhouette. Broken at the top it reads as two quote
# strokes descending into the block, and the silhouette is its own.
CUT_Y = CUR_Y - 40
OPEN_TOP = True                  # the master lets the cuts break the top edge
CUT_FOOT = 11                    # the rounded heel where a nib lifts off
_PAIR_W = CUT_W_TOP * 2 + CUT_GAP
CUT1_X = CUR_X + (CUR_W - _PAIR_W) / 2
CUT2_X = CUT1_X + CUT_W_TOP + CUT_GAP

# ---------------------------------------------------------------- material
# Ground is the set's, unchanged, so this icon sits on the same shelf as its
# siblings: measured off apple-26 for clarify, reused by geminify, reused here.
GROUND = ("#FFFEFB", "#F5F0E5", "#E2D8C2")
VIGNETTE = "#9C8D74"                    # 0.996 -> 0.930 diagonal
RIM_WHITE, RIM_HAIR = 0.72, "#C7B9A0"

# The cursor sits WELL below the ground on the value ramp. A porcelain glyph on a
# porcelain field has no separation at 16px and the object goes to a pale blob;
# that failure is on record for clarify.
#
# Two takes tried clay here and both rendered as mud, because a mid-value warm
# body under a warm ground has nowhere to go: its lights merge with the field and
# its darks turn brown. The set already has a vocabulary for a terminal, and it is
# tui-craft's deep slate device - reused at its own values, so the two
# terminal-subject icons read as kin without reading as duplicates.
FACE = ("#39404A", "#171B21")           # slate device, key light upper-left
MID = "#232932"                         # authored mid-stop; see the ramp note below
SCATTER = "#7C8695"                     # cool lit edge on a slate body; a warm
SCATTER_A, SCATTER_W = 0.62, 6          # scatter here reads as dust on glass
CROWN_A = 0.20                          # broad soft highlight across the crown,
                                        # not a hairline along the outline

SHADOW = "#6E6049"                      # warm; nothing here emits cool
CONTACT = "#41372A"                     # the hard dark line under the lower edge
SHADOW_DX, SHADOW_DY = 14, 24

# One vermilion, kin to Fledgeling's #C4622D, spent on the two cuts and nowhere
# else. Vibrancy is emission rather than saturation: a hot core BEHIND the cuts
# lighting the aperture, then the aperture itself, then a bloom in front of it.
GEL = ("#F4794A", "#E8542A", "#B93A16")
# A pale outline all the way round each cut flattened them into stickers.
# A full-perimeter pale stroke read as a sticker edge at 1024px. The wall and
# the bloom already carry the aperture; the rim only has to hint at it.
CUT_RIM, CUT_RIM_A, CUT_RIM_W = "#FFF2EC", 0.20, 3
CORE, CORE_A = "#E8542A", 0.85
BLOOM, BLOOM_A = "#E8542A", 0.20

# A cut through a body has a WALL, and the wall is what makes it an aperture
# rather than a painted stripe. The lit face of that wall is the LOWER inner
# edge, because the light in this family comes from the upper left and falls
# across the opening onto the far side. Assuming highlight-is-above has failed
# here three times on record, so the direction is a named constant.
WALL = "#0A0D11"
WALL_A, WALL_W = 0.66, 20
LIP, LIP_A = "#FFC9A8", 0.40


# ---------------------------------------------------------------- takes
# Each losing take is the parameter set that produced it, so the sheet's
# comparison renders come out of this file rather than out of memory.
TAKES = {
    "t2": dict(CUR_W=380, CUR_H=500, CUR_R=54, CUT_W_TOP=82, CUT_W_BOT=30,
               CUT_H=196, CUT_GAP=48, CUT_Y_OFF=82, CUT_FOOT=14, OPEN_TOP=False,
               FACE=("#C2B49B", "#4E4433"), MID="#8A7355",
               SCATTER="#FFFBF2", SCATTER_A=0.62, SCATTER_W=13, CROWN_A=0.50,
               GEL=("#FFC08A", "#F0813B", "#C9490F"), CORE="#FF7A33",
               WALL="#33291C", LIP="#FFE6C8", BLOOM="#F9C48E", BLOOM_A=0.34,
               CUT_RIM_A=0.80, CUT_RIM_W=8),
    "t3": dict(CUR_W=452, CUR_H=624, CUR_R=70, CUT_W_TOP=108, CUT_W_BOT=50,
               CUT_H=434, CUT_GAP=66, CUT_Y_OFF=152, CUT_FOOT=11, OPEN_TOP=False,
               FACE=("#CDBDA2", "#5C4B34"), MID="#8A7355",
               SCATTER="#FFFBF2", SCATTER_A=0.70, SCATTER_W=9, CROWN_A=0.34,
               GEL=("#FFC08A", "#F0813B", "#C9490F"), CORE="#FF7A33",
               WALL="#33291C", LIP="#FFE6C8", BLOOM="#F9C48E", BLOOM_A=0.34,
               CUT_RIM_A=0.42, CUT_RIM_W=5),
}


def apply_take(key):
    """Rebind the module globals a take overrides, then recompute what derives
    from them. Derived values are recomputed rather than overridden so a take
    cannot silently disagree with itself."""
    global CUR_W, CUR_H, CUR_R, CUR_X, CUR_Y
    global CUT_W_TOP, CUT_W_BOT, CUT_H, CUT_GAP, CUT_Y, CUT_FOOT, OPEN_TOP
    global CUT1_X, CUT2_X, FACE, MID, SCATTER, SCATTER_A, SCATTER_W, CROWN_A
    global GEL, CORE, WALL, LIP, BLOOM, BLOOM_A, CUT_RIM_A, CUT_RIM_W
    t = TAKES[key]
    CUR_W, CUR_H, CUR_R = t["CUR_W"], t["CUR_H"], t["CUR_R"]
    CUR_X = (S - CUR_W) / 2
    CUR_Y = (S - CUR_H) / 2 + 10
    CUT_W_TOP, CUT_W_BOT = t["CUT_W_TOP"], t["CUT_W_BOT"]
    CUT_H, CUT_GAP, CUT_FOOT = t["CUT_H"], t["CUT_GAP"], t["CUT_FOOT"]
    OPEN_TOP = t["OPEN_TOP"]
    CUT_Y = CUR_Y + t["CUT_Y_OFF"]
    pair = CUT_W_TOP * 2 + CUT_GAP
    CUT1_X = CUR_X + (CUR_W - pair) / 2
    CUT2_X = CUT1_X + CUT_W_TOP + CUT_GAP
    FACE, MID = t["FACE"], t["MID"]
    SCATTER, SCATTER_A, SCATTER_W = t["SCATTER"], t["SCATTER_A"], t["SCATTER_W"]
    CROWN_A, GEL, CORE = t["CROWN_A"], t["GEL"], t["CORE"]
    WALL, LIP, BLOOM, BLOOM_A = t["WALL"], t["LIP"], t["BLOOM"], t["BLOOM_A"]
    CUT_RIM_A, CUT_RIM_W = t["CUT_RIM_A"], t["CUT_RIM_W"]


# ---------------------------------------------------------------- helpers
def lin(i, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<linearGradient id="{i}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}" gradientUnits="userSpaceOnUse">{s}</linearGradient>')


def rad(i, cx, cy, r, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"'
                + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                for o, c, a in stops)
    return (f'<radialGradient id="{i}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'gradientUnits="userSpaceOnUse">{s}</radialGradient>')


def mix(a, b, t):
    """Interpolate two hex colours, so a luminance-range edit stays a two-value
    edit rather than four literals kept in sync by hand."""
    pa = tuple(int(a[i:i + 2], 16) for i in (1, 3, 5))
    pb = tuple(int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


def body_path():
    x, y, w, h, r = CUR_X, CUR_Y, CUR_W, CUR_H, CUR_R
    return (f"M{x + r:.1f},{y:.1f} H{x + w - r:.1f} "
            f"Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} "
            f"V{y + h - r:.1f} Q{x + w:.1f},{y + h:.1f} {x + w - r:.1f},{y + h:.1f} "
            f"H{x + r:.1f} Q{x:.1f},{y + h:.1f} {x:.1f},{y + h - r:.1f} "
            f"V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} Z")


def cut_path(x):
    """One quote stroke: a chisel wedge, broad at the top, tapering down, with a
    rounded heel where the nib lifts. The top is squared off rather than rounded,
    because a rounded top reads as a droplet and a droplet is not a quote mark."""
    y, wt, wb, h = CUT_Y, CUT_W_TOP, CUT_W_BOT, CUT_H
    inset = (wt - wb) * 0.62         # the taper runs mostly off the left edge
    xl, xr = x + inset, x + inset + wb
    return (f"M{x:.1f},{y + 6:.1f} "
            f"Q{x:.1f},{y:.1f} {x + 8:.1f},{y:.1f} "
            f"H{x + wt - 8:.1f} Q{x + wt:.1f},{y:.1f} {x + wt:.1f},{y + 6:.1f} "
            f"L{xr:.1f},{y + h - CUT_FOOT:.1f} "
            f"Q{xr:.1f},{y + h:.1f} {(xl + xr) / 2:.1f},{y + h:.1f} "
            f"Q{xl:.1f},{y + h:.1f} {xl:.1f},{y + h - CUT_FOOT:.1f} Z")


def cuts():
    """Both cuts, with the shared lean expressed about the pair's own centre so
    they stay parallel: leaning each about its own centre splays them."""
    cx = (CUT1_X + CUT2_X + CUT_W_TOP) / 2
    cy = CUT_Y + CUT_H / 2
    lean = f"rotate({CUT_LEAN} {cx:.1f} {cy:.1f})"
    return [(cut_path(CUT1_X), lean), (cut_path(CUT2_X), lean)]


# ---------------------------------------------------------------- layers
def defs():
    d = [f'<clipPath id="mask"><path d="{SQUIRCLE}"/></clipPath>']
    d.append(rad("ground", S * 0.34, S * 0.26, S * 0.96,
                 [(0, GROUND[0], None), (0.52, GROUND[1], None), (1, GROUND[2], None)]))
    d.append(rad("vig", S * 0.5, S * 0.5, S * 0.72,
                 [(0, VIGNETTE, "0"), (0.72, VIGNETTE, "0.05"), (1, VIGNETTE, "0.17")]))
    # Warm mid-stops, authored rather than interpolated: a straight ramp between
    # a warm light and a warm dark passes through desaturated ground, and the
    # body rendered gunmetal for two rounds because of it.
    d.append(lin("face", CUR_X, CUR_Y, CUR_X + CUR_W * 0.55, CUR_Y + CUR_H,
                 [(0, FACE[0], None), (0.55, MID, None), (1, FACE[1], None)]))
    d.append(lin("gel", CUT1_X, CUT_Y, CUT2_X + CUT_W_TOP, CUT_Y + CUT_H,
                 [(0, GEL[0], None), (0.46, GEL[1], None), (1, GEL[2], None)]))
    d.append(rad("crown", CUR_X + CUR_W * 0.40, CUR_Y + CUR_H * 0.06, CUR_W * 0.92,
                 [(0, "#FFFFFF", f"{CROWN_A}"), (0.58, "#FFFFFF", "0.11"),
                  (1, "#FFFFFF", "0")]))
    d.append(f'<clipPath id="body"><path d="{body_path()}"/></clipPath>')
    # The cuts as a clip, so the aperture wall and the lip can only ever land on
    # the real opening.
    inner = "".join(f'<path d="{p}" transform="{t}"/>' for p, t in cuts())
    # clip-rule is stated rather than left to the default: two subpaths under
    # nonzero UNION, which is what is wanted here (one clip region covering both
    # apertures). Leaving it implicit makes a reader re-derive the intent, and the
    # audit script flags it for exactly that reason.
    d.append(f'<clipPath id="cuts" clip-rule="nonzero">{inner}</clipPath>')
    for f, sd in (("soft", 24), ("softL", 40), ("tight", 11), ("hair", 4)):
        d.append(f'<filter id="{f}" x="-50%" y="-50%" width="200%" height="200%">'
                 f'<feGaussianBlur stdDeviation="{sd}"/></filter>')
    return d


def background():
    return [
        f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#ground)"/>',
        f'<rect x="0" y="0" width="{S}" height="{S}" fill="url(#vig)"/>',
        f'<path d="{SQUIRCLE}" fill="none" stroke="#FFFFFF" stroke-width="7" '
        f'opacity="{RIM_WHITE}"/>',
        f'<path d="{SQUIRCLE}" fill="none" stroke="{RIM_HAIR}" stroke-width="2" '
        f'opacity="0.30"/>',
    ]


def mid():
    """Shadow, then the light behind the cuts, then the body itself.

    Order matters: the core sits BEHIND the block so it reads as light coming
    through an opening rather than as paint applied on top of one.
    """
    p = body_path()
    out = [
        f'<path d="{p}" fill="{SHADOW}" opacity="0.28" filter="url(#soft)" '
        f'transform="translate({SHADOW_DX} {SHADOW_DY})"/>',
        f'<path d="{p}" fill="{CONTACT}" opacity="0.32" filter="url(#tight)" '
        f'transform="translate({SHADOW_DX * 0.4:.1f} {SHADOW_DY * 0.6:.1f})"/>',
    ]
    out.append(f'<path d="{p}" fill="url(#face)"/>')
    return out


def fg():
    """The crown on the body, then the apertures with their walls."""
    out = [f'<g clip-path="url(#body)">'
           f'<ellipse cx="{CUR_X + CUR_W * 0.42:.1f}" cy="{CUR_Y + CUR_H * 0.12:.1f}" '
           f'rx="{CUR_W * 0.60:.1f}" ry="{CUR_H * 0.22:.1f}" fill="url(#crown)" '
           f'filter="url(#softL)"/></g>']
    # OPEN_TOP clips the apertures to the body, so a cut that starts above the
    # top edge arrives as an open notch. A closed-top take needs no clip because
    # its cuts already sit inside the body.
    open_g, close_g = ('<g clip-path="url(#body)">', '</g>') if OPEN_TOP else ('', '')
    out.append(open_g)
    for path, lean in cuts():
        # The core behind each aperture, then the aperture itself.
        out.append(f'<path d="{path}" transform="{lean}" fill="{CORE}" '
                   f'opacity="{CORE_A}" filter="url(#soft)"/>')
    for path, lean in cuts():
        out.append(f'<path d="{path}" transform="{lean}" fill="url(#gel)"/>')
    out.append(close_g)
    # The aperture wall: a dark inner band on the cut's own boundary, clipped to
    # the cuts so it reads as depth through the body rather than as an outline.
    out.append('<g clip-path="url(#body)"><g clip-path="url(#cuts)">')
    for path, lean in cuts():
        out.append(f'<path d="{path}" transform="{lean}" fill="none" '
                   f'stroke="{WALL}" stroke-width="{WALL_W}" opacity="{WALL_A}" '
                   f'filter="url(#hair)"/>')
    out.append('</g></g>')
    return out


def highlight():
    out = [
        # Body rim scatter, clipped to the body: a full outline reads as a sticker.
        f'<g clip-path="url(#body)">'
        f'<path d="{body_path()}" fill="none" stroke="{SCATTER}" '
        f'stroke-width="{SCATTER_W}" opacity="{SCATTER_A}"/>'
        f'</g>',
    ]
    # The lit lip on each aperture's LOWER inner edge, and a warm catch on the
    # outer boundary so the opening has a rim as well as a wall.
    out.append('<g clip-path="url(#body)"><g clip-path="url(#cuts)">')
    for path, lean in cuts():
        out.append(f'<path d="{path}" transform="{lean} translate(0 -11)" fill="none" '
                   f'stroke="{LIP}" stroke-width="8" opacity="{LIP_A}" '
                   f'filter="url(#hair)"/>')
    out.append('</g></g>')
    out.append('<g clip-path="url(#body)">')
    for path, lean in cuts():
        out.append(f'<path d="{path}" transform="{lean}" fill="none" '
                   f'stroke="{CUT_RIM}" stroke-width="{CUT_RIM_W}" '
                   f'opacity="{CUT_RIM_A}"/>')
    out.append('</g>')
    # The bloom in front of the pair: the voice's own light on the body around it.
    out.append(f'<g clip-path="url(#body)">'
               f'<ellipse cx="{(CUT1_X + CUT2_X + CUT_W_TOP) / 2:.1f}" '
               f'cy="{CUT_Y + CUT_H * 0.42:.1f}" rx="215" ry="150" fill="{BLOOM}" '
               f'opacity="{BLOOM_A}" filter="url(#softL)"/></g>')
    return out


def build():
    groups = "".join(
        f'<g id="{name}">' + "".join(items) + "</g>"
        for name, items in (("bg", background()), ("mid", mid()),
                            ("fg", fg()), ("highlight", highlight()))
    )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
            f'viewBox="0 0 {S} {S}">'
            f'<defs>{"".join(defs())}</defs>'
            f'<g clip-path="url(#mask)">{groups}</g></svg>\n')


if __name__ == "__main__":
    argv = sys.argv[1:]
    if argv and argv[0] == "--take":
        apply_take(argv[1])
        argv = argv[2:]
    out = pathlib.Path(argv[0]) if argv else ASSETS / "icon.svg"
    out.write_text(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
