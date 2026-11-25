"""Build one tailored résumé per target role from a single source of facts.

    python3 make_variants.py --facts facts.md --spec variants.json --out roles/ \
        --name "Jane Doe" [--serve-url http://127.0.0.1:8942] [--docx-python /tmp/dv/bin/python]

One edit to the facts file or the spec reaches every variant, which is the point: the
source session kept five résumés, a website and a LinkedIn document consistent by
rebuilding rather than by editing each one, after a hand edit left two documents
disagreeing about the same date.

`facts.md` is the résumé written once, in the Markdown subset `build_resume.py` reads.
`variants.json` selects and reorders from it:

    {
      "sections": {"head": ["", "## Professional summary"],
                   "employer": ["### Example Bank", "#### Product Owner"],
                   "role_head": ["#### Product Owner", "- Prioritised"],
                   "tail": ["#### Business and Operations Manager", null]},
      "bullets": {"prio": "- Prioritised ...", "rel": "- Took ..."},
      "skill_blocks": {"product": "Product and agile delivery: ...",
                       "tools": "Tools: Jira, Confluence"},
      "variants": {
        "Product-Owner": {"summary": "...", "skills": ["product", "tools"],
                          "bullets": ["prio", "rel"], "max_pages": 2}
      }
    }

Each `sections` entry is a [start, end] pair of literal strings found in the facts file;
`null` as the end means "to the end of the file". Every variant's bullets and skill blocks
are keys into the shared maps, so a changed bullet changes every variant that uses it.

Outputs per variant, into --out: `<key>.md`, `<Name>-Resume-<key>.html`, `.pdf`, `.docx`,
and a printed page count. A variant over its `max_pages` is reported as OVER and exits 1,
because a résumé that quietly became three pages is the failure this check exists for.
"""
import json, re, subprocess, sys, os, html, argparse, shutil

ap = argparse.ArgumentParser()
ap.add_argument("--facts", required=True)
ap.add_argument("--spec", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--name", required=True)
ap.add_argument("--serve-url", default="", help="base URL already serving --out; enables PDF")
ap.add_argument("--docx-python", default="", help="python with python-docx for a styled .docx")
ap.add_argument("--chrome", default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
a = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
spec = json.load(open(a.spec))
base = open(a.facts).read()
os.makedirs(a.out, exist_ok=True)
slug = re.sub(r"[^A-Za-z0-9]+", "-", a.name).strip("-")

def section(pair):
    start, end = pair
    i = base.index(start) if start else 0
    j = base.index(end) if end else len(base)
    return base[i:j]

S = {k: section(v) for k, v in spec["sections"].items()}
bullets, skills = spec["bullets"], spec["skill_blocks"]
failures = []

for key, v in spec["variants"].items():
    md = (S.get("head", "")
          + "## Professional summary\n\n" + v["summary"] + "\n\n"
          + "## Key skills\n\n" + "\n\n".join(skills[s] for s in v["skills"]) + "\n\n"
          + "## Professional experience\n\n" + S.get("employer", "") + S.get("role_head", "")
          + "\n".join(bullets[b] for b in v["bullets"]) + "\n\n" + S.get("tail", ""))
    md_path = os.path.join(a.out, f"{key}.md")
    htm = os.path.join(a.out, f"{slug}-Resume-{key}.html")
    pdf = os.path.join(a.out, f"{slug}-Resume-{key}.pdf")
    docx = os.path.join(a.out, f"{slug}-Resume-{key}.docx")
    open(md_path, "w").write(md)
    subprocess.run([sys.executable, os.path.join(HERE, "build_resume.py"), md_path, htm,
                    "--name", a.name], check=True, capture_output=True)

    pages = "?"
    if a.serve_url and os.path.exists(a.chrome):
        subprocess.run([a.chrome, "--headless=new", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}",
                        f"{a.serve_url.rstrip('/')}/{os.path.basename(htm)}"],
                       capture_output=True)
        if shutil.which("pdfinfo") and os.path.exists(pdf):
            info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
            m = re.search(r"Pages:\s+(\d+)", info)
            pages = m.group(1) if m else "?"

    if a.docx_python and os.path.exists(a.docx_python):
        subprocess.run([a.docx_python, os.path.join(HERE, "make_docx.py"), md_path, docx,
                        "--name", a.name], capture_output=True)
    elif shutil.which("textutil"):
        # Plain fallback: readable in Word, unstyled. The session shipped these first and
        # the styled version was asked for immediately, so prefer --docx-python.
        tmp = os.path.join(a.out, f".{key}.tmp.html")
        out, ul = ['<html><head><meta charset="utf-8"><style>body{font-family:Calibri,Arial;'
                   'font-size:11pt}h1{font-size:20pt}h2{font-size:14pt}'
                   'h3,h4{font-size:10.5pt}</style></head><body>'], False
        for line in md.splitlines():
            if not line.strip():
                if ul: out.append("</ul>"); ul = False
                continue
            if line.startswith("- "):
                if not ul: out.append("<ul>"); ul = True
                out.append(f"<li>{html.escape(line[2:])}</li>"); continue
            if ul: out.append("</ul>"); ul = False
            m = re.match(r"(#+) (.*)", line)
            if m:
                n = min(len(m.group(1)), 4)
                text = m.group(2).upper() if n == 2 else m.group(2)
                out.append(f"<h{n}>{html.escape(text)}</h{n}>")
            else:
                out.append(f"<p>{html.escape(line)}</p>")
        open(tmp, "w").write("\n".join(out) + "</body></html>")
        subprocess.run(["textutil", "-convert", "docx", tmp, "-output", docx],
                       capture_output=True)
        os.remove(tmp)

    limit = v.get("max_pages")
    over = limit and pages.isdigit() and int(pages) > limit
    if over: failures.append(f"{key}: {pages} pages, limit {limit}")
    print(f"{'OVER ' if over else 'ok   '}{key}  pages={pages}  words={len(md.split())}")

if failures:
    print("\n".join("FAIL " + f for f in failures), file=sys.stderr)
    sys.exit(1)
