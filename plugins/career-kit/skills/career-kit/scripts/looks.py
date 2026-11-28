"""Named looks for a résumé: what may vary inside the layout research, and nothing else.

    from looks import LOOKS, get_look, check_look

The corporate layout fixes one column, sentence-case headings, round bullets, contact details in
the body, no tables, icons or photo, and two pages. The research leaves these open, so a look may
set them, inside these ranges:

    typeface      Arial, Calibri, Aptos or Times New Roman (the four the sources name)
    body          10.5 to 12pt, lines 2pt taller than the type
    accent        one muted colour, at least 4.5:1 on white, used for the name and at most
                  two more roles (headings, job titles)
    headings      14 to 16pt, weight 600 or 700, a light rule under them or none
    name          20 to 24pt
    space above   12 to 14pt before each section heading

`check_look` refuses anything outside those, so a new look cannot drift into a layout the
research does not support. Both builders take `--look <id>`; `build_looks.py` builds several
with the same words and a page to compare them.

The first four were built for the source session on 25 November 2026, and the person helping
chose `calibri-teal` for the public copy on 26 November. The last three apply the same rules and
have not been shown to anyone yet.
"""

FONTS = {
    # family: [(file, weight, style)] for @font-face when the face is not installed system-wide.
    # Calibri and Aptos ship with Microsoft Office (Word's DFonts folder on macOS); their
    # embedding permission is "editable", so they embed in a PDF.
    "Arial": [],
    "Times New Roman": [],
    "Calibri": [("Calibri.ttf", 400, "normal"), ("Calibrib.ttf", 700, "normal"),
                ("Calibrii.ttf", 400, "italic")],
    "Aptos": [("Aptos.ttf", 400, "normal"), ("Aptos-SemiBold.ttf", 600, "normal"),
              ("Aptos-Bold.ttf", 700, "normal"), ("Aptos-Italic.ttf", 400, "italic")],
}

INK, INK2 = "#16181D", "#3D4350"

# Accents that pass on white and stay distinct in greyscale print (measured 26 Nov 2026).
ACCENTS = {
    "navy": "#1F2B5B",      # 13.5:1
    "teal": "#1F5F63",      # 7.3:1
    "slate": "#2F4A7A",     # 8.8:1
    "forest": "#2E5E3A",    # 7.6:1
    "burgundy": "#7A2E2E",  # 9.3:1
    "charcoal": "#3A3F47",  # 10.6:1
    "ink": INK,             # 17.8:1
}


def _look(id, label, what, font="Arial", pt=11, lh=13, accent="navy", h2_color="accent",
          h2_size=14, h2_weight=700, rule=True, title_color=None, name_size=20, gap=12):
    return dict(id=id, label=label, what=what, font=font, pt=pt, lh=lh, accent=accent,
                h2_color=h2_color, h2_size=h2_size, h2_weight=h2_weight, rule=rule,
                title_color=title_color, name_size=name_size, gap=gap)


LOOKS = {l["id"]: l for l in [
    _look("classic", "Classic", "Arial, with the name and headings in navy and a rule under each "
          "heading. The builders' default."),
    _look("calibri-teal", "A · Calibri", "Calibri, a federal jobs department's other named "
          "typeface. Dark headings with a light rule; the name and job titles in a muted teal. "
          "Leaves the most white space.", font="Calibri", accent="teal", h2_color="ink",
          title_color="teal", name_size=24, gap=14),
    _look("aptos-clean", "B · Aptos", "Aptos, Microsoft Office's current default. Larger "
          "semibold navy headings with no rules, for a cleaner, more modern page.", font="Aptos",
          h2_size=15, h2_weight=600, rule=False, name_size=22),
    _look("arial-roles", "C · Arial, reworked", "The same typeface as Classic, with a larger "
          "black name, black headings and navy job titles, so each role stands out.",
          accent="ink", h2_color="ink", title_color="navy", name_size=24),
    # Designed 26 Nov 2026 inside the same bounds; not yet shown to a person.
    _look("times-traditional", "D · Times New Roman", "The serif the sources name, at 12pt "
          "because it sets smaller than Arial. Black headings with a rule; suits law, finance "
          "and public-sector readers who expect a traditional page.", font="Times New Roman",
          pt=12, lh=14, accent="ink", h2_color="ink", name_size=22),
    _look("mono-print", "E · Print", "Arial in black ink only, with grey rules. For a résumé "
          "that will be printed, photocopied or faxed, where colour turns to grey anyway.",
          accent="ink", h2_color="ink", title_color=None),
    _look("calibri-slate", "F · Calibri, slate", "Calibri with slate-blue headings and no "
          "rules, the name at 22pt. Between A's warmth and B's minimalism.", font="Calibri",
          accent="slate", h2_color="accent", rule=False, name_size=22, gap=14),
]}


def _rgb(hex_):
    h = hex_.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _lum(hex_):
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in _rgb(hex_)]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b="#FFFFFF"):
    hi, lo = sorted([_lum(a), _lum(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def colour(name):
    """An accent name, a hex value, 'accent' is resolved by the caller, 'ink' is the text ink."""
    if name is None:
        return None
    return ACCENTS.get(name, name)


def resolved(look):
    """The look with every colour as a hex value."""
    l = dict(look)
    l["accent"] = colour(l["accent"])
    l["h2_color"] = l["accent"] if l["h2_color"] == "accent" else colour(l["h2_color"])
    l["title_color"] = colour(l["title_color"])
    return l


def check_look(look):
    """Raise ValueError naming every value outside the research's bounds."""
    l, bad = resolved(look), []
    if l["font"] not in FONTS:
        bad.append(f"typeface {l['font']!r} is not one the sources name ({', '.join(FONTS)})")
    if not 10.5 <= l["pt"] <= 12:
        bad.append(f"body {l['pt']}pt is outside 10.5-12pt")
    if abs(l["lh"] - l["pt"] - 2) > 0.01:
        bad.append(f"lines of {l['lh']}pt are not 2pt taller than {l['pt']}pt type")
    if not 14 <= l["h2_size"] <= 16:
        bad.append(f"headings at {l['h2_size']}pt are outside 14-16pt")
    if l["h2_weight"] not in (600, 700):
        bad.append(f"heading weight {l['h2_weight']} is not 600 or 700")
    if not 20 <= l["name_size"] <= 24:
        bad.append(f"name at {l['name_size']}pt is outside 20-24pt")
    if not 12 <= l["gap"] <= 14:
        bad.append(f"{l['gap']}pt above headings is outside 12-14pt")
    for role in ("accent", "h2_color", "title_color"):
        c = l[role]
        if c is not None and contrast(c) < 4.5:
            bad.append(f"{role} {c} is {contrast(c):.2f}:1 on white, under 4.5:1")
    if bad:
        raise ValueError(f"look {l['id']!r}: " + "; ".join(bad))
    return l


def get_look(id, accent=None):
    """A checked, resolved look; `accent` (a name or hex) overrides the look's own."""
    if id not in LOOKS:
        raise SystemExit(f"unknown look {id!r}; choose from: {', '.join(LOOKS)}")
    look = dict(LOOKS[id])
    if accent:
        look["accent"] = accent
    return check_look(look)
