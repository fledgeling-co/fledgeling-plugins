"""Check that every figure in a generated document traces to the confirmed-facts file.

    python3 facts_lint.py --facts facts/confirmed.md output/*.md output/*.html
    python3 facts_lint.py --facts facts/confirmed.md --verbs verbs.json output/resume.md

The gate behind "never invent a fact". An agent writing career documents produces plausible
numbers — a headcount rounded up, a percentage nobody measured, a date inferred from the
next role's start — and plausible is exactly what a background check and an interview panel
test. Everything numeric in an output has to appear in the facts file first.

Exit 0 when every figure traces. Exit 1 with a list of the ones that do not.

How a figure is matched: digits are compared after stripping commas, currency symbols and
the words about/approximately, so "about 20,000" in a document matches "20000" in the facts
file. Years 1900-2100 that appear in a date range are matched the same way, so an inferred
end date fails unless the facts file states it. Ordinary small numbers in prose that carry no
claim (a bullet count, "two-week sprints") pass when the facts file contains them; add them
to the facts file rather than to an ignore list, because an ignore list is where an invented
figure hides.

--verbs takes a JSON file of scope rules, which is the second failure the source session hit
repeatedly: reviewers caught "shipped" where the truth was "supported", "runs" where it was
"coordinates", and "owns the squad's backlog" where she owned one backlog in the squad.

    {"supported": ["shipped", "led", "drove", "delivered"],
     "coordinated": ["ran", "owned", "managed"]}

Each key is the verb the person confirmed; each value lists stronger verbs that must not
appear near the same object. The check is a plain substring scan and reports candidates for
a human or a review panel to judge, as warnings rather than failures, because "led" is
correct somewhere else in the same document.
"""
import re, sys, json, html, argparse, os

ap = argparse.ArgumentParser()
ap.add_argument("--facts", required=True, help="file holding every confirmed fact")
ap.add_argument("--verbs", default="", help="JSON map of confirmed verb -> stronger verbs")
ap.add_argument("--min-digits", type=int, default=2,
                help="ignore numbers shorter than this many digits (default 2)")
ap.add_argument("files", nargs="+")
a = ap.parse_args()

def text_of(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith((".html", ".htm")):
        raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    return raw

NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)")
def figures(text):
    out = set()
    for m in NUM.finditer(text):
        v = m.group(1).replace(",", "")
        if len(v.replace(".", "").lstrip("0")) >= a.min_digits:
            out.add(v.rstrip(".").rstrip("0").rstrip(".") if "." in v else v)
    return out

facts_text = text_of(a.facts)
known = figures(facts_text)
verbs = json.load(open(a.verbs)) if a.verbs else {}

failed, warned = 0, 0
for path in a.files:
    if not os.path.exists(path):
        print(f"MISSING {path}", file=sys.stderr); failed += 1; continue
    body = text_of(path)
    unknown = sorted(figures(body) - known, key=lambda s: (len(s), s))
    for v in unknown:
        line = next((l.strip() for l in body.splitlines() if v in l.replace(",", "")), "")
        print(f"FAIL {path}: figure {v} is not in {a.facts}")
        if line:
            print(f"     {line[:160]}")
        failed += 1
    low = body.lower()
    for confirmed, stronger in verbs.items():
        if confirmed.lower() not in low:
            continue
        for s in stronger:
            if re.search(rf"\b{re.escape(s.lower())}\b", low):
                print(f"WARN {path}: '{s}' appears in a document whose confirmed verb is "
                      f"'{confirmed}'. Check the object it attaches to.")
                warned += 1

total = len(a.files)
print(f"\nchecked {total} file(s) against {a.facts}: "
      f"{failed} untraced figure(s), {warned} verb warning(s)")
sys.exit(1 if failed else 0)
