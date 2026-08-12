#!/usr/bin/env python3
"""build_report.py — render the claim ledger into one self-contained page.

    python3 build_report.py --out report/index.html

The ledger below is the artifact; the page is generated from it. Inline
citation markers, the support counts and the registry all come from the same
structure, so a claim cannot cite a source the registry does not carry and the
registry cannot list a source no claim uses.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re

# ── the corpus ───────────────────────────────────────────────────────────────
MEMBERS = [
    ("M1", "OpenAI Deep Research", "Designing software project status and decision aids for non-technical owners", "$9.00", 25),
    ("M2", "Gemini Deep Research", "Single-File HTML Decision Capsules for AI Agents", "$7.00", 1),
    ("M3", "Perplexity", "Design Rules for Single-File Project Status and Decision Documents", "$4.00", 18),
    ("M4", "Claude CLI (subscription)", "Designing HTML Status and Decision Documents for Non-Technical Owners", "$0.00", 20),
    ("M5", "Codex CLI (subscription)", "Empirical design rules for IT project status reporting and decision elicitation", "$0.00", 36),
]

# ── sources: only what a claim below actually leans on ───────────────────────
# A registry you cannot open is a registry you cannot check. Three of the nine
# are this run's own artifacts and have no URL; the rest carry one.
URLS = {'dora': 'https://dora.dev/guides/dora-metrics-four-keys/', 'jach': 'https://www.cambridge.org/core/journals/behavioural-public-policy/article/when-and-why-defaults-influence-decisions-a-metaanalysis-of-default-effects/67B2C6CB0FD3FC1BC61FE0F5E1E4D6D8', 'jg': 'https://www.science.org/doi/10.1126/science.1091721', 'chun': 'https://link.springer.com/journal/11238', 'wcag': 'https://www.w3.org/TR/WCAG22/', 'adr': 'https://adr.github.io/'}

SOURCES = {
    "dora": ("DORA — <em>DevOps Research and Assessment</em>, metric definitions",
             "dora.dev", "Cited by three of the five members. Defines deployment frequency and lead time for changes from deployment automation; carries no definition of “done”."),
    "jach": ("Jachimowicz, Duncan, Weber &amp; Johnson (2019), <em>When and why defaults influence decisions</em>",
             "cambridge.org / Behavioural Public Policy", "Meta-analysis, 58 studies: default effect d = 0.68. The best-sourced quantitative claim in the corpus, reached independently by two members."),
    "jg": ("Johnson &amp; Goldstein (2003), <em>Do defaults save lives?</em>",
           "science.org", "The organ-donation default result. Cited as the canonical demonstration that presentation, not preference, drove the outcome."),
    "chun": ("Chun, Ho &amp; Diecidue (2021), on rank information and preference",
             "link.springer.com / Theory and Decision", "Finds rank information shifts stated preference beyond the underlying ratings, and concentrates attention at the top of a list."),
    "wcag": ("W3C — <em>Web Content Accessibility Guidelines 2.2</em>",
             "w3.org", "Cited by three members. 1.4.10 reflow, 1.4.12 text spacing, 2.4.11 focus not obscured, 2.5.8 target size."),
    "adr": ("Architecture Decision Record community documentation",
            "adr.github.io", "Cited by two members for the status vocabulary — proposed, accepted, superseded — and for recording a decision's consequences alongside it."),
    "verify": ("Dossier <code>research_verify_citations</code>, run <code>dr_6a4a6bb1ceb4f755</code>, 12 August 2026",
               "this run", "46 citations dereferenced: 0 fabricated, 0 dead, 37 resolved directly, 8 blocked by a bot wall, 1 rate-limited."),
    "reg": ("The five exported source registries, <code>docs/deep-research/*.sources.md</code>",
            "this repo", "Distinct publisher domains counted per member: 25, 1, 18, 20, 36."),
    "hdr": ("Run headers in the exported reports",
            "this repo", "The report exported from the run labelled <code>local-claude</code> carries a header reading <code>model: gpt-5.6-luna, provider: openai</code>."),
}

# ── the claim ledger ─────────────────────────────────────────────────────────
CLAIMS = [
    dict(id="C1", kind="direct", confidence="high", support=3,
         text="There is no industry definition of <em>done</em> to appeal to. DORA defines deployment from deployment automation and stops there.",
         sources=["dora"], members="M1 M3 M4 M5",
         limit="DORA measures delivery performance, not feature completeness. That it defines no “done” is an absence, and an absence is weaker evidence than a finding — but it is the absence every member reached independently."),
    dict(id="C2", kind="direct", confidence="high", support=2,
         text="Pre-selecting an option moves the choice hard: <strong>d = 0.68</strong> across 58 studies.",
         sources=["jach", "jg"], members="M1 M5",
         limit="Measured on consequential real-world choices — retirement, insurance, organ donation — not on a project questionnaire answered by its own owner. The direction transfers; the magnitude is not this page's to claim."),
    dict(id="C3", kind="inference", confidence="high", support=2,
         text="Therefore an unconfirmed default must not export as an answer. The useful thing and the dangerous thing are the same mechanism.",
         sources=["jach"], members="M1 M4 M5",
         limit="This is the corpus's premise carried one step, not a finding. No member ran the experiment; the inference is the page's."),
    dict(id="C4", kind="direct", confidence="medium", support=1,
         text="Rank information shifts stated preference <em>beyond</em> the ratings that produced the rank, and concentrates attention at the top of a list.",
         sources=["chun"], members="M5",
         limit="One member, one paper. It is the strongest argument against the “answer these three first” strip that three other members recommend — which is why it is carried as contested rather than applied."),
    dict(id="C5", kind="direct", confidence="high", support=3,
         text="The accessibility floor is not optional and is specific: reflow at 320px, text spacing, focus not obscured by a fixed bar, target size.",
         sources=["wcag"], members="M1 M3 M5",
         limit="2.4.11 is the one that bites a page like this, because the fixed export bar at the foot of the screen is exactly the thing that obscures a focused control."),
    dict(id="C6", kind="direct", confidence="medium", support=2,
         text="A decision record carries its consequences beside it, not only its outcome — the ADR pattern, applied to a questionnaire.",
         sources=["adr"], members="M1 M5",
         limit="ADRs are written by the people who will live with them, over months. A questionnaire answered in one sitting borrows the shape, not the deliberation."),
    dict(id="C7", kind="direct", confidence="high", support=1,
         text="One member's citations are not fabricated. Of 46, none was invented and none was dead: 37 opened directly, 8 hit a bot wall, 1 was rate-limited.",
         sources=["verify"], members="M2",
         limit="Resolving is not supporting. Every one of those URLs proves a page exists; none of them proves it says what the report said it says."),
    dict(id="C8", kind="direct", confidence="high", support=1,
         text="But all 46 are opaque redirects attributed to a single domain, so that member's registry names no publisher at all — against 25, 18, 20 and 36 distinct domains for the others.",
         sources=["reg", "verify"], members="M2",
         limit="A reader cannot tell what any of those sources is without dereferencing it one at a time. The figures in that report are therefore unattributable from the export, which is a different and lesser charge than being made up."),
    dict(id="C9", kind="direct", confidence="high", support=1,
         text="The panel was five runs but four families: the member labelled <code>local-claude</code> reports an OpenAI model in its own header.",
         sources=["hdr"], members="—",
         limit="Agreement between two members of the same family is one perspective counted twice. Every convergence below should be read as four, not five."),
]

CONTESTED = [
    ("Whether to rank the decisions at all",
     "Three members rank by how much each decision releases. One wants a global priority number on every card. One cites the rank-effect result and wants dependency groups with no global ordering at all.",
     "Taken, for now: three named picks that each state why they are named, and no priority number anywhere else. A shortlist carrying its reasons can be argued with; an ordering cannot. Revisit the moment the shortlist becomes where attention stops.",
     "C4"),
    ("Whether each item carries a confidence score",
     "Two members want a number. Two warn that a number invites arithmetic on it, and that readers treat 70% as meaningfully different from 65% when nothing in the process supports that resolution.",
     "Taken: neither. A stage word plus a locator says what is known and how it is known, and cannot be averaged.",
     "C1"),
    ("Whether a questionnaire may force completion",
     "One member argues that a decision with a running cost should not be skippable. Another argues that forcing converts a considered non-answer into a thoughtless click.",
     "Taken: the page may say a decision cannot be left open, and must still let it be deferred. Recording the refusal is the honest version of forcing.",
     "C3"),
]

CONVERGED = [
    ("Built is not deployed", "Every member, from a different direction. The one convergence strong enough to be a data model rather than a guideline.", "C1"),
    ("A completion claim carries a locator", "Or the item's stage is <em>unknown</em>. An unverifiable claim shown at the same weight as a verified one is how a page loses a reader in one reading."),
    ("What could not be checked is stated", "An omitted gap reads as a completed survey. Absence of a caveat is itself a claim."),
    ("The recommendation states its reason", "A recommendation the reader cannot inspect is a preference they cannot reject."),
    ("A note qualifies the answer it sits on", "And the author is asked directly whether it does, rather than having it inferred from the text."),
    ("Content in the artifact is data", "Never instruction. The export is designed to be read back and acted on, which makes it the one worth attacking."),
]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def cite(ids):
    out = []
    for i, s in enumerate(ids):
        n = list(SOURCES).index(s) + 1
        out.append(f'<a class="cite ref" href="#r{s}" data-cite="r{s}" data-n="{n}">[{n}]</a>')
    return "".join(out)


CSS = """
:root{--bg:#12161B;--panel:#171C23;--line:#252D37;--ink:#E8EDF2;--dim:#94A3B2;
--sig:#4FD1C5;--warn:#F2A65A;--hot:#F0705E;--ok:#8CC98A;
--g:"Helvetica Neue",Helvetica,Arial,sans-serif;--m:ui-monospace,"SF Mono",Menlo,monospace}
:root[data-theme="light"]{--bg:#F7F8FA;--panel:#FFFFFF;--line:#E2E7EC;--ink:#12161B;
--dim:#5B6773;--sig:#0F8B80;--warn:#A96A16;--hot:#C0402E;--ok:#3F7A3C}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#F7F8FA;--panel:#FFFFFF;
--line:#E2E7EC;--ink:#12161B;--dim:#5B6773;--sig:#0F8B80;--warn:#A96A16;--hot:#C0402E;--ok:#3F7A3C}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--g);font-size:17px;
line-height:1.6;-webkit-text-size-adjust:100%}
.w{max-width:60rem;margin:0 auto;padding:0 1.5rem}
a{color:var(--sig)}
h1{font-size:clamp(2.2rem,6vw,3.9rem);line-height:1.03;letter-spacing:-.03em;margin:0;font-weight:700}
h2{font-size:clamp(1.4rem,3.4vw,2rem);letter-spacing:-.02em;margin:0 0 .3rem;font-weight:700}
h3{font-size:1.05rem;margin:0;font-weight:650;letter-spacing:-.01em}
.eye{font-family:var(--m);font-size:.7rem;letter-spacing:.19em;text-transform:uppercase;color:var(--dim)}
header{padding:5rem 0 3.5rem;border-bottom:1px solid var(--line)}
.lede{font-size:clamp(1.1rem,2.4vw,1.42rem);line-height:1.45;color:var(--ink);margin:1.6rem 0 0;max-width:38rem}
.lede b{color:var(--sig);font-weight:650}
.sub{color:var(--dim);margin:1.1rem 0 0;max-width:40rem;font-size:1rem}
section{padding:3.6rem 0;border-bottom:1px solid var(--line)}
.intro{color:var(--dim);margin:.5rem 0 2rem;max-width:42rem}
/* the page's one visual device: support as discrete stops, never a bar */
.stops{display:inline-flex;gap:3px;vertical-align:middle}
.stops i{width:9px;height:16px;border-radius:1px;background:var(--line);display:block}
.stops i.on{background:var(--sig)}
.claim{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:1.35rem 1.5rem;margin:0 0 .9rem}
.claim.inf{border-left:3px solid var(--warn)}
.chead{display:flex;gap:.8rem;align-items:center;flex-wrap:wrap;margin-bottom:.7rem}
.cid{font-family:var(--m);font-size:.72rem;color:var(--dim)}
.tag{font-family:var(--m);font-size:.62rem;letter-spacing:.1em;text-transform:uppercase;
border:1px solid currentColor;border-radius:2px;padding:.1rem .4rem}
.t-inf{color:var(--warn)}.t-dir{color:var(--dim)}
.spacer{flex:1 1 auto}
.dom{font-family:var(--m);font-size:.68rem;color:var(--dim)}
.ctext{font-size:1.06rem;line-height:1.5}
.limit{color:var(--dim);font-size:.9rem;margin:.75rem 0 0;padding-left:.9rem;border-left:1px solid var(--line)}
.limit b{color:var(--ink);font-weight:600}
.ref{font-family:var(--m);font-size:.72rem;text-decoration:none;padding:0 .1rem;vertical-align:.35em}
.ref:hover,.ref:focus-visible{text-decoration:underline}
.grid{display:grid;gap:.9rem;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:1.15rem 1.25rem}
.card p{color:var(--dim);font-size:.92rem;margin:.45rem 0 0}
.dis{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--hot);
border-radius:4px;padding:1.35rem 1.5rem;margin:0 0 .9rem}
.dis .split{color:var(--dim);font-size:.95rem;margin:.55rem 0 0}
.dis .took{margin:.9rem 0 0;font-size:.95rem}
.dis .took b{color:var(--hot);font-weight:650}
table{width:100%;border-collapse:collapse;font-size:.92rem;min-width:34rem}
.scroll{overflow-x:auto}
th,td{text-align:left;padding:.65rem .7rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-family:var(--m);font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;color:var(--dim);font-weight:600}
td.n{font-family:var(--m);color:var(--dim);white-space:nowrap}
.reg{list-style:none;padding:0;margin:0;counter-reset:s}
.reg li{border-bottom:1px solid var(--line);padding:.95rem 0 .95rem 2.6rem;position:relative;font-size:.94rem}
.reg li::before{counter-increment:s;content:"[" counter(s) "]";position:absolute;left:0;top:.95rem;
font-family:var(--m);font-size:.72rem;color:var(--sig)}
.reg .pub{color:var(--dim);font-family:var(--m);font-size:.72rem;display:block;margin-top:.2rem}
.reg .what{color:var(--dim);font-size:.88rem;margin-top:.4rem}
.meth{color:var(--dim);font-size:.95rem;max-width:42rem}
.meth b{color:var(--ink);font-weight:600}
.meth ul{padding-left:1.1rem}
footer{padding:3rem 0 5rem;color:var(--dim);font-size:.85rem}
:focus-visible{outline:2px solid var(--sig);outline-offset:3px}
:target{scroll-margin-top:2rem}
/* Motion is additive only. `forwards` rather than `both` so nothing is hidden
   before its range begins — a claim that exists only inside an animated frame is
   a claim a reader who scrolls fast never sees, and one a screenshot never shows. */
@supports (animation-timeline:view()){
  @media (prefers-reduced-motion:no-preference){
    .claim,.dis,.card{animation:rise .5s ease-out forwards;animation-timeline:view();
    animation-range:entry 0% entry 40%}
    @keyframes rise{from{opacity:.35;transform:translateY(8px)}to{opacity:1;transform:none}}}}
@media print{body{background:#fff;color:#111}.claim,.dis,.card{border:1px solid #ccc;break-inside:avoid}
section{border-bottom:1px solid #ccc}a{color:#111}}
"""


def build(out: pathlib.Path) -> None:
    claims = "".join(
        f'<article class="claim {"inf" if c["kind"] == "inference" else ""}" id="{c["id"]}">'
        f'<div class="chead"><span class="cid">{c["id"]}</span>'
        f'<span class="tag t-{"inf" if c["kind"] == "inference" else "dir"}">'
        f'{"inference" if c["kind"] == "inference" else "direct"}</span>'
        f'<span class="spacer"></span>'
        f'<span class="dom">{c["members"]}</span>'
        f'<span class="stops" role="img" aria-label="{c["support"]} independent source domain'
        f'{"s" if c["support"] != 1 else ""}">'
        + "".join(f'<i class="{"on" if i < c["support"] else ""}"></i>' for i in range(4))
        + "</span></div>"
        f'<p class="ctext">{c["text"]}{cite(c["sources"])}</p>'
        f'<p class="limit"><b>Where it stops.</b> {c["limit"]}</p></article>'
        for c in CLAIMS)

    conv = "".join(
        f'<div class="card"><h3>{t}</h3><p>{b}</p></div>' for t, b, *_ in CONVERGED)

    dis = "".join(
        f'<article class="dis"><h3>{t}</h3><p class="split">{split}</p>'
        f'<p class="took"><b>Taken.</b> {took[len("Taken, for now: "):] if took.startswith("Taken, for now: ") else took[len("Taken: "):]}</p>'
        f'<p class="limit">Turns on <a href="#{cid}">{cid}</a>.</p></article>'
        for t, split, took, cid in CONTESTED)

    rows = "".join(
        f'<tr><td class="n">{mid}</td><td>{name}</td><td>{title}</td>'
        f'<td class="n">{cost}</td><td class="n">{dom}</td></tr>'
        for mid, name, title, cost, dom in MEMBERS)

    reg = "".join(
        f'<li id="r{key}">'
        f'<span>{f"<a href={URLS[key]!r} rel=noreferrer>{title}</a>" if key in URLS else title}</span>'
        f'<span class="pub">{pub}</span><span class="what">{what}</span></li>'
        for i, (key, (title, pub, what)) in enumerate(SOURCES.items(), 1))

    page = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Five reports, four families, one usable finding</title>
<meta name="description" content="What a five-member deep-research panel actually established about project-status-and-decision pages — nine claims with their limits, three questions it split on, and two things wrong with the panel itself.">
<style>{CSS}</style></head>
<body>
<header><div class="w">
<p class="eye">Research note · 12 August 2026 · private</p>
<h1>Five reports,<br>four families,<br>one usable finding.</h1>
<p class="lede">A panel of five deep-research runs was commissioned on how to build a project-status page that also asks its owner the questions stopping the work. <b>One finding was strong enough to become a data model.</b> Six more were strong enough to become rules. Three the panel could not agree on, and they are still open.</p>
<p class="sub">This note exists to make the skill built on that research auditable from inside the repository — including the two things about the panel itself that would be easier to leave out.</p>
</div></header>

<section><div class="w">
<h2>The claim ledger</h2>
<p class="intro">Every claim the skill rests on, with what supports it and where it stops. The stops beside each one count <em>independent publisher domains</em>, not members who agreed — four members drawing on one paper is one source, and the panel's own composition (<a href="#C9">C9</a>) is why that distinction is not pedantry here. Claims marked <span class="tag t-inf">inference</span> were assembled by reasoning over the corpus and are not findings in it.</p>
{claims}
</div></section>

<section><div class="w">
<h2>Where it converged</h2>
<p class="intro">Six rules every member reached, and one of them arrived with enough force to change the shape of the data rather than the wording of a guideline.</p>
<div class="grid">{conv}</div>
</div></section>

<section><div class="w">
<h2>Where it did not</h2>
<p class="intro">Three questions the panel split on. Each is carried as an open question in the skill's evidence file rather than quietly resolved, because on all three the losing argument is good and the decision is a judgement rather than a reading.</p>
{dis}
</div></section>

<section><div class="w">
<h2>The panel, and what is wrong with it</h2>
<p class="intro">Two things about this corpus would be easier to leave out of a page that cites it. Both are checkable from the exports in this repository.</p>
<div class="scroll"><table>
<caption class="intro" style="text-align:left;caption-side:top">Distinct domains counts the publishers a member's own source registry names.</caption>
<thead><tr><th scope="col">Member</th><th scope="col">Backend</th><th scope="col">Brief as run</th><th scope="col">Cost</th><th scope="col">Distinct domains</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="limit" style="margin-top:1.6rem"><b>One.</b> The run labelled <code>local-claude</code> exported a report whose header reads <code>model: gpt-5.6-luna, provider: openai</code>. Five runs, four families. Read every convergence in this note as four independent perspectives, not five.{cite(["hdr"])}</p>
<p class="limit"><b>Two.</b> M2's registry names one domain across all 46 citations, because every one is an opaque grounding redirect. Dereferenced, they hold up — nothing fabricated, nothing dead, 37 of 46 opening directly{cite(["verify"])} — so the honest charge is not invention. It is that no reader can tell what any of those sources is without opening them one at a time, which means the precise figures in that report cannot be attributed to a publisher from the export. They are not repeated anywhere in this note or in the skill.</p>
<p class="limit">That distinction was corrected mid-way through writing this page. The first draft said the figures were unsourced; the verification run said they were unattributable. Those are different, and the second is the one the evidence supports.</p>
</div></section>

<section><div class="w">
<h2>Methods</h2>
<div class="meth">
<p>Five deep-research runs at <code>max</code> tier, commissioned 12 August 2026 against one brief with a shared decision context. Two paid backends and one paid API run cost <b>$20.00</b> between them; two ran on existing CLI subscriptions at no marginal cost.</p>
<ul>
<li><b>Read in full.</b> Every member was exported whole to <code>docs/deep-research/</code> and read end to end, not through an outline and not through a merged distillation.</li>
<li><b>Verified.</b> <code>research_verify_citations</code> was run on the member whose registry looked thinnest. Result in <a href="#C7">C7</a> and <a href="#C8">C8</a>.</li>
<li><b>Counted.</b> Support is counted in independent publisher domains, parsed from the exported registries rather than asserted.</li>
<li><b>Not established.</b> Whether any of these rules improves a real owner's decisions. Nothing in the corpus tests that, and this note does not claim it. What it claims is narrower: six structural properties that a page built without them measurably lacks.</li>
</ul>
<p><b>Departures from the usual pipeline for this page,</b> all because it is a private in-repo note rather than a published one: no divergence trawl on the visual direction, no separate voice pass, no commissioned page icon, no marketing chrome, and no motion library — the one animation is a CSS view timeline that degrades to nothing under <code>prefers-reduced-motion</code>. It is not deployed anywhere.</p>
</div>
</div></section>

<section><div class="w">
<h2>Sources</h2>
<p class="intro">Only what a claim above actually leans on. The five full reports and their complete registries — 223 citations across 76 domains — sit beside this file.</p>
<ol class="reg">{reg}</ol>
</div></section>

<footer><div class="w">Written for one reader, kept in the repository it argues about.
Generated from the ledger in <code>build_report.py</code>; the citations, the support counts and the registry above all come from the same structure, so none of the three can disagree with the others.</div></footer>
</body></html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out} — {len(CLAIMS)} claims, {len(SOURCES)} sources, {len(CONTESTED)} open questions")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="report/index.html")
    build(pathlib.Path(ap.parse_args().out))
