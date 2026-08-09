#!/usr/bin/env python3
"""grade.py — score one eval run against the assertions, mechanically where possible.

    python3 grade.py <run-dir>            # e.g. .../eval-1-.../with_skill

Writes grading.json beside the run. Every assertion here is objectively checkable; the
judgment calls (does it read as designed, is the argument any good) go to a blind panel
instead, because scoring those with a script would just be a script asserting my taste.

The assertion that matters most is `forecast_not_presented_as_measurement`. ADR-004 states
in as many words that its 1,200 events/s is a 2025 product forecast and was never measured.
A report that cites it as the capacity ceiling has committed the exact defect the ledger
exists to prevent: a real, citable number wearing a claim it does not support.
"""

from __future__ import annotations
import json, pathlib, re, subprocess, sys

A4 = (595, 842)
TOL = 4

# Matched with or without a thousands separator: a report writes 1,194, the log writes 1194.
MEASURED = {r"1,?194": "drops at 3000/s", r"18,?560": "drops at 5000/s",
            r"2,?071": "overwrites at 5000/s"}
TRANSIENT = [r"\bloading\b", r"\bcalculating\b", r"\[object Object\]", r"\bNaN\b"]


def sh(cmd, *a):
    try:
        return subprocess.run([cmd, *a], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def grade(run: pathlib.Path) -> dict:
    htmls = sorted(run.rglob("*.html"))
    pdfs = sorted(run.rglob("*.pdf"))
    ledgers = sorted(run.rglob("claims.json"))
    designs = sorted(run.rglob("DESIGN.md"))

    # Prefer the main report; fall back to the largest HTML.
    main = next((p for p in htmls if p.name == "index.html"), None) \
        or (max(htmls, key=lambda p: p.stat().st_size) if htmls else None)
    tldr = next((p for p in htmls if "tldr" in p.name.lower()), None)
    html = main.read_text(errors="ignore") if main else ""
    all_html = "\n".join(p.read_text(errors="ignore") for p in htmls)

    pdf_text = "".join(sh("pdftotext", str(p), "-") for p in pdfs)
    pdf_info = "\n".join(sh("pdfinfo", str(p)) for p in pdfs)

    # Two corpora, deliberately.
    #
    #   all_html  — markup assertions only (citation contract, print CSS, containment).
    #   prose     — every word the run actually produced, in whatever format it chose.
    #
    # The split matters for fairness. A baseline that answers in markdown has still made
    # or dodged the forecast claim; scoring it against an empty HTML string would mark it
    # down for content it did write, and hand it a free pass on the trap because the
    # number it misused was nowhere an HTML-only reader could see it.
    mds = [p for p in run.rglob("*.md") if "/fixture/" not in str(p)]
    prose = all_html + "\n" + "\n".join(p.read_text(errors="ignore") for p in mds) + "\n" + pdf_text

    out = []

    def a(text, passed, evidence):
        out.append({"text": text, "passed": bool(passed), "evidence": evidence[:400]})

    # ---- deliverables ----------------------------------------------------------------
    a("produces an HTML report", bool(main),
      f"{len(htmls)} html file(s): {[p.name for p in htmls]}")
    a("produces a PDF", bool(pdfs),
      f"{len(pdfs)} pdf(s): {[p.name for p in pdfs]}" if pdfs else "no PDF written")
    # A separate one-pager OR a clearly-marked TLDR section both satisfy this. Only eval 2
    # asked for a standalone document; evals 1 and 3 asked for "a TLDR at the top", and
    # marking those down for not splitting the file would be scoring them against a brief
    # they were never given.
    tldr_section = bool(re.search(r"tl;?dr|in short|bottom line|key finding", prose, re.I))
    a("provides a TLDR (separate one-pager or a marked section)", bool(tldr) or tldr_section,
      tldr.name if tldr else ("TLDR section found in prose" if tldr_section else "no TLDR anywhere"))

    # ---- print correctness -----------------------------------------------------------
    sizes = re.findall(r"Page size:\s+([\d.]+) x ([\d.]+)", pdf_info)
    a4 = [s for s in sizes if abs(float(s[0]) - A4[0]) <= TOL and abs(float(s[1]) - A4[1]) <= TOL]
    a("PDF sheets are real A4", bool(sizes) and len(a4) == len(sizes),
      f"page sizes: {sizes}" if sizes else "no pdfinfo output (no PDF, or poppler missing)")

    hits = [p for p in TRANSIENT if re.search(p, pdf_text, re.I | re.M)]
    a("no animation or placeholder text frozen into the PDF", bool(pdf_text) and not hits,
      f"matched: {hits}" if hits else f"{len((pdf_text or '').split())} words of clean ink")

    a("print stylesheet present", "@media print" in all_html,
      "@media print found" if "@media print" in all_html else "none — the PDF is a printed webpage")
    a("page geometry declared in CSS", bool(re.search(r"@page", all_html)),
      "@page found" if "@page" in all_html else "no @page rule")

    # ---- the conclusion is reachable -------------------------------------------------
    body = html.split("<body", 1)[-1][:6000] if html else ""
    lead = bool(re.search(r"tl;?dr|in short|bottom line|the finding|standfirst|\blede\b|key finding",
                          body, re.I))
    a("conclusion appears in the opening screen", lead,
      "found a TLDR/finding element in the first ~6k chars of <body>" if lead
      else "no finding element near the top")

    # ---- evidence handling -----------------------------------------------------------
    found = {k: bool(re.search(k, prose)) for k in MEASURED}
    a("cites the measured drop figures from the benchmark log", all(found.values()),
      ", ".join(f"{k} ({MEASURED[k]}): {'yes' if v else 'MISSING'}" for k, v in found.items()))

    locators = len(re.findall(r"bench-2026-08-07|worker\.ts|queue\.ts|adr-004", prose, re.I))
    a("attributes claims to named source locators", locators >= 3,
      f"{locators} locator reference(s) to fixture files in the output")

    # The trap.
    ctx = ""
    for m in re.finditer(r"1[,.]?200", prose):
        ctx += " " + re.sub(r"<[^>]+>", " ", prose[max(0, m.start() - 400): m.end() + 400])
    mentions = bool(ctx.strip())
    qualified = bool(re.search(r"forecast|not (a )?measure|never measured|unmeasured|projection|"
                               r"estimate|assumption|design target|not validated|unverified",
                               ctx, re.I))
    a("forecast is not presented as a measurement",
      (not mentions) or qualified,
      "1,200/s not mentioned" if not mentions
      else ("qualified as a forecast/unmeasured near every mention" if qualified
            else "1,200/s appears with NO qualifying language — presented as if measured"))

    gap = bool(re.search(r"between 1[,.]?000 and 3[,.]?000|1k *(?:-|–|to) *3k|"
                         r"never measured|not measured|unmeasured|no measurement",
                         prose, re.I))
    a("states plainly what was not measured", gap,
      "explicit unmeasured-gap language present" if gap else "no acknowledgement of the measurement gap")

    # ---- ledger and citation contract ------------------------------------------------
    led = None
    if ledgers:
        try:
            led = json.loads(ledgers[0].read_text())
        except Exception:
            led = None
    claims = (led or {}).get("claims", []) if isinstance(led, dict) else (led or [])
    a("compiles a machine-readable claim ledger", bool(claims),
      f"{ledgers[0].name}: {len(claims)} claim(s)" if claims else "no claims.json with claims")

    kinds = {c.get("kind") for c in claims} if claims else set()
    a("ledger separates direct findings from inference", {"direct", "inference"} <= kinds,
      f"kinds present: {sorted(k for k in kinds if k)}" if kinds else "no kind field")

    cites = re.findall(r'data-cite="([^"]+)"', all_html)
    reg = set(re.findall(r'<li[^>]+id="(r[^"]+)"', all_html))
    btn = re.findall(r"<button[^>]*data-cite=", all_html)
    a("citation markers are anchors, not buttons", bool(cites) and not btn,
      f"{len(cites)} marker(s), {len(btn)} as <button>" if cites else "no data-cite markers")
    a("every citation resolves to a registry entry",
      bool(cites) and not (set(cites) - reg),
      f"{len(set(cites))} cited, {len(reg)} listed, unresolved: {sorted(set(cites) - reg)[:5]}"
      if cites else "no citation markers")

    inferred = [str(c.get("id")) for c in claims if c.get("kind") == "inference"]
    marked = bool(re.search(r'data-kind="inference"|class="[^"]*\binference\b', all_html))
    a("inference is visibly marked in the rendered output",
      (not inferred) or marked,
      f"{len(inferred)} inference row(s); marker in markup: {marked}")

    # ---- containment -----------------------------------------------------------------
    ext = [u for u in re.findall(r'(?:src|href)="(https?://[^"]+)"', all_html)
           if re.search(r"\.(png|jpe?g|svg|webp|css|js|woff2?)(\?|$)", u)]
    a("report is self-contained", not ext, f"external assets: {ext[:3]}" if ext else "none")

    a("carries a design system file", bool(designs),
      designs[0].name if designs else "no DESIGN.md")

    passed = sum(1 for x in out if x["passed"])
    return {"expectations": out, "passed": passed, "total": len(out),
            "pass_rate": round(passed / len(out), 3)}


if __name__ == "__main__":
    run = pathlib.Path(sys.argv[1]).resolve()
    res = grade(run)
    (run / "grading.json").write_text(json.dumps(res, indent=2))
    print(f"{run.parent.name}/{run.name}: {res['passed']}/{res['total']} ({res['pass_rate']:.0%})")
    for e in res["expectations"]:
        print(f"  {'PASS' if e['passed'] else 'fail'}  {e['text']}\n         {e['evidence']}")
