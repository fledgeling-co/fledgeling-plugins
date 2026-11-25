"""Build a styled Word résumé from the same Markdown the HTML/PDF is built from.

    <python-with-python-docx> make_docx.py <in.md> <out.docx> --name "Jane Doe"

Needs python-docx, which is usually not on the system interpreter:

    python3 -m venv /tmp/dv && /tmp/dv/bin/pip install python-docx

Portals ask for .docx and parse it; people read the PDF. Both come from one Markdown file
so a figure cannot differ between them. The styling here mirrors build_resume.py's CSS:
Arial 11pt on EXACT 13pt lines, A4 with 20mm margins on every side, 14pt sentence-case navy
headings with a rule under each, a right tab stop for dates, and a PAGE/NUMPAGES field footer.

Line spacing is exact points, never a multiple. Word's "1.15" is about 1.32x the type size for
Arial while the PDF's CSS 1.15 is 1.15x; in the source session that difference ran the Word file
to three pages while the PDF held two, and only opening the file in Word showed it. Word adds
space-after and space-before together where CSS collapses margins, so each space_before below is
the CSS gap less the space_after of the paragraph that usually precedes it.

Arial rather than a brand font on purpose: in the source session `pdffonts` showed the
specified Aptos and Calibri were not installed and the document had silently fallen back,
so the two outputs looked different for a reason nobody could see in the Markdown.
"""
import sys, re, argparse
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT, WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--name", default="")
ap.add_argument("--accent", default="1F2B5B")
a = ap.parse_args()

ACCENT = RGBColor(*bytes.fromhex(a.accent.lstrip("#")))
INK, INK2, RULE = RGBColor(0x16, 0x18, 0x1D), RGBColor(0x3D, 0x43, 0x50), "B9BEC8"
FONT = "Arial"

d = Document()
s = d.sections[0]
s.page_width, s.page_height = Mm(210), Mm(297)
s.left_margin = s.right_margin = Mm(20)
s.top_margin, s.bottom_margin, s.footer_distance = Mm(20), Mm(20), Mm(9)
LH = Pt(13)
st = d.styles["Normal"]
st.font.name, st.font.size, st.font.color.rgb = FONT, Pt(11), INK
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.line_spacing = LH
W = Mm(210 - 40)

def run(p,t,bold=False,color=None,size=None):
    # <Missing Thing> marks information nobody has supplied yet. It is set in red.
    # ==text== marks a suggested figure the person has not confirmed. It is highlighted yellow.
    r=None
    for j,seg in enumerate(re.split(r"==(.+?)==",t)):
        for k,part in enumerate(re.split(r"(<[^<>\n/][^<>\n]{1,70}>)",seg)):
            if not part: continue
            r=p.add_run(part); r.bold=bold or k%2==1; r.font.name=FONT
            if k%2==1: r.font.color.rgb=RGBColor(0xC0,0x00,0x00)
            elif color is not None: r.font.color.rgb=color
            if size: r.font.size=Pt(size)
            if j%2==1: r.font.highlight_color=WD_COLOR_INDEX.YELLOW
    return r if r is not None else p.add_run("")

def border(p, color=RULE, sz=5):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", str(sz)), ("space", "3"), ("color", color)):
        e.set(qn(f"w:{k}"), v)
    b.append(e); pPr.append(b)

def titled(parts, size, space_before, emp=False):
    p = d.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = Pt(15) if emp else LH
    p.paragraph_format.tab_stops.add_tab_stop(W, WD_TAB_ALIGNMENT.RIGHT)
    p.paragraph_format.keep_with_next = True
    date = parts[-1] if len(parts) > 1 else ""
    head = parts[:-1] if len(parts) > 1 else parts
    run(p, head[0], bold=True, size=size)
    for x in head[1:]:
        run(p, "  ·  " + x, color=INK2, size=size if emp else 10)
    if date:
        # Non-breaking spaces: Word wrapped "May 2025 - Present" across two lines otherwise.
        run(p, "\t" + date.replace(" ", " "), color=INK2, size=None if emp else 10)

title, after_h1, in_skills, prev_role = a.name, False, False, False
for line in open(a.src).read().splitlines():
    if not line.strip():
        continue
    m = re.match(r"(#+) (.*)", line)
    if m:
        lvl, t = len(m.group(1)), m.group(2)
        if lvl == 1:
            title = title or t
            p = d.add_paragraph(); p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = Pt(24)
            run(p, t, bold=True, color=ACCENT, size=20); after_h1 = True
        elif lvl == 2:
            in_skills = t.lower() == "key skills"
            p = d.add_paragraph()
            # 12pt above in the CSS, less the 5pt after the paragraph that usually precedes it.
            p.paragraph_format.space_before = Pt(7)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = Pt(17)
            p.paragraph_format.keep_with_next = True
            run(p, t, bold=True, color=ACCENT, size=14)   # sentence case, as written
            border(p)
        else:
            # A role heading straight after another (the one-line earliest roles) sits close.
            before = 0 if lvl == 3 or prev_role else 4
            titled([x.strip() for x in t.split("|")], 12 if lvl == 3 else 10.5, before, emp=(lvl == 3))
            prev_role = lvl == 4
        continue
    prev_role = False
    if line.startswith("- "):
        p = d.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Mm(4.6)
        p.paragraph_format.first_line_indent = Mm(-4.6)
        p.paragraph_format.line_spacing = LH
        run(p, line[2:]); continue
    if after_h1:
        p = d.add_paragraph(); p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = Pt(14)
        run(p, line.replace(" | ", "   ·   "), color=INK2, size=10); after_h1 = False; continue
    p = d.add_paragraph()
    if in_skills and re.match(r"^[A-Z][A-Za-z ,]+: ", line):
        k, v = line.split(": ", 1)
        p.paragraph_format.space_after = Pt(4)
        run(p, k + ": ", bold=True); run(p, v)
    else:
        run(p, line)

fp = s.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
def field(p, code):
    for typ, txt in (("begin", None), (None, code), ("end", None)):
        r = p.add_run(); r.font.size = Pt(8.5); r.font.color.rgb = INK2; r.font.name = FONT
        if typ:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), typ); r._r.append(f)
        else:
            it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = txt
            r._r.append(it)
for t, c in ((f"{title}  ·  page ", None), (None, "PAGE"), (" of ", None), (None, "NUMPAGES")):
    if t: run(fp, t, color=INK2, size=8.5)
    else: field(fp, c)

d.core_properties.author = title
d.core_properties.title = f"{title} — Résumé"
d.save(a.out)
print("wrote", a.out)
