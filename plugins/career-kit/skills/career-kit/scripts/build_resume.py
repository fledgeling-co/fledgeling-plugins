"""Render a résumé written in a small Markdown subset into print-ready A4 HTML.

    python3 build_resume.py <copy.md> <out.html> [--name "Jane Doe"] [--accent "#1F2B5B"]

Pages break automatically: the sheet has a min-height of 297mm and no fixed height, so
content that outgrows one page flows onto the next instead of being clipped. A fixed-height
container silently cut the last two bullets of a résumé in the source session and the HTML
gave no error, which is why this renderer never sets `height`.

Markdown subset:
    # Name                     document title
    (line after the H1)        contact line, " | " becomes a separator dot
    ## Section
    ### Employer | Dates       employer row, right-aligned date
    #### Role | Team | Dates   role row, middle parts render as muted "· Team"
    - bullet
    Label: text               (inside a "Key skills" section) bold label, inline text
    <Missing Thing>           renders in red, where information has not been supplied yet
    [anything in brackets]    renders as a yellow highlight (the earlier gap marker)

Highlighted brackets are the gap marker. They print, deliberately: an unconfirmed figure
should be impossible to miss rather than plausible prose.
"""
import re, html, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--name", default="", help="footer name; defaults to the H1 text")
ap.add_argument("--accent", default="#1F2B5B")
ap.add_argument("--lang", default="en-AU")
a = ap.parse_args()

def inline(t):
    t = html.escape(t)
    t = re.sub(r"\[([^\]]+)\]", r'<mark class="todo">[\1]</mark>', t)
    # <Missing Thing> marks information nobody has supplied yet. It prints in red.
    return re.sub(r"&lt;([^&\n/][^&\n]{1,70}?)&gt;", r'<span class="gap">&lt;\1&gt;</span>', t)

body, ul, title = [], False, ""
for ln in open(a.src).read().splitlines():
    if not ln.strip():
        if ul: body.append("</ul>"); ul = False
        continue
    if ln.startswith("- "):
        if not ul: body.append("<ul>"); ul = True
        body.append(f"<li>{inline(ln[2:])}</li>"); continue
    if ul: body.append("</ul>"); ul = False
    m = re.match(r"(#+) (.*)", ln)
    if m:
        lvl, t = len(m.group(1)), m.group(2)
        if lvl == 1:
            title = t; body.append(f"<h1>{inline(t)}</h1>")
        elif lvl == 2:
            body.append(f"<h2>{inline(t)}</h2>")
        else:
            parts = [p.strip() for p in t.split("|")]
            date = parts[-1] if len(parts) > 1 else ""
            head_parts = parts[:-1] if len(parts) > 1 else parts
            head = inline(head_parts[0]) + "".join(
                f' <span class="org">· {inline(x)}</span>' for x in head_parts[1:])
            cls = "emp" if lvl == 3 else "role"
            body.append(f'<h3 class="{cls}"><span>{head}</span>'
                        f' <span class="date">{inline(date)}</span></h3>')
        continue
    if body and body[-1].startswith("<h1"):
        body.append(f'<p class="contact">{inline(ln).replace(" | ", " &nbsp;·&nbsp; ")}</p>')
    elif re.match(r"^[A-Z][A-Za-z ,]+: ", ln) and len(ln.split(": ", 1)[0]) < 42:
        k, v = ln.split(": ", 1)
        body.append(f'<p class="skill"><b>{html.escape(k)}:</b> {inline(v)}</p>')
    elif " | " in ln:
        left, right = ln.rsplit(" | ", 1)
        body.append(f'<p class="line"><span>{inline(left)}</span>'
                    f' <span class="date">{inline(right)}</span></p>')
    else:
        body.append(f"<p>{inline(ln)}</p>")
if ul: body.append("</ul>")

name = a.name or title
# Type and spacing: inside the AU research ranges (Arial 10.5-11pt; 13-14pt headings; Word line
# spacing 1.05-1.15; 18-22 mm margins) and inside typesetting guidance for reading (line height
# 1.2-1.45x the type). Line height is in points so make_docx.py can set the same EXACT value:
# Word's "1.15" multiple is about 1.32x the type for Arial, where CSS's 1.15 is 1.15x.
CSS = """
@page{size:A4;margin:18mm 20mm 18mm;@bottom-center{content:"__NAME__  ·  page " counter(page)
 " of " counter(pages);font:8.5pt Arial,sans-serif;color:#3D4350}}
:root{--ink:#16181D;--ink2:#3D4350;--rule:#B9BEC8;--accent:__ACCENT__}
*{box-sizing:border-box}
html{background:#E9EBEF}
body{margin:0;color:var(--ink);font:10.5pt/13pt Arial,"Helvetica Neue",Helvetica,sans-serif;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:210mm;min-height:297mm;margin:10mm auto;background:#fff;padding:18mm 20mm 18mm;
 box-shadow:0 1px 4px rgba(0,0,0,.18)}
h2,h3{break-after:avoid}li,h3+p{break-inside:avoid}h3.role+p{break-after:avoid}
h1{font-size:22pt;line-height:26pt;margin:0 0 4pt;letter-spacing:.01em;color:var(--accent)}
.contact{margin:0 0 4pt;color:var(--ink2);font-size:10pt;line-height:14pt}
h2{font-size:13pt;line-height:16pt;letter-spacing:.09em;text-transform:uppercase;color:var(--accent);
 margin:14pt 0 6pt;padding-bottom:3pt;border-bottom:.6pt solid var(--rule)}
h3{margin:8pt 0 3pt;font-size:10.5pt;line-height:13pt;display:flex;justify-content:space-between;gap:6mm;
 align-items:baseline}
h3.emp{font-size:12pt;line-height:15pt;margin-top:2pt}
h3.role+h3.role{margin-top:3pt}
h3 .org{font-weight:400;color:var(--ink2);white-space:nowrap}
h3 .date,.line .date{font-weight:400;color:var(--ink2);white-space:nowrap}
p{margin:0 0 6pt}
.skill{margin-bottom:5pt}
.line{display:flex;justify-content:space-between;gap:6mm;margin-bottom:3pt}
.line span:first-child{font-weight:600}
ul{margin:0 0 4pt;padding-left:4.6mm}
li{margin-bottom:4.5pt}
mark.todo{background:#FFE36E;color:#16181D;padding:0 .6mm;border-radius:.6mm}
.gap{color:#C00000;font-weight:700}
.banner{width:210mm;margin:8mm auto 0;font:13px/1.5 system-ui,sans-serif;color:#3D4350;
 background:#FFF6CC;border:1px solid #E5C94A;border-radius:6px;padding:10px 14px}
@media print{html{background:#fff}.sheet{margin:0;box-shadow:none;padding:0;width:auto;
 min-height:0}.banner{display:none}}
""".replace("__NAME__", name.replace('"', "")).replace("__ACCENT__", a.accent)

open(a.out, "w").write(
    f'<!doctype html><html lang="{a.lang}"><head><meta charset="utf-8">'
    f'<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<title>{html.escape(name)} — Résumé</title><style>{CSS}</style></head><body>\n'
    f'<div class="banner">To make the PDF: File → Print → Save as PDF, paper size A4, '
    f'default margins. Pages break automatically. This note does not print.</div>\n'
    f'<section class="sheet">\n' + "\n".join(body) + "\n</section>\n</body></html>")
print("wrote", a.out)
