#!/usr/bin/env python3
"""
evidence-page.py — build the living evidence page from the campaign's artifacts.

A campaign's real output is not a reply and not a markdown report: it is a
browsable surface where coverage, flows, screenshots and components sit
together, every item carries a stable id somebody can point at, and the gaps are
as visible as the passes.

This builds that page from the artifacts on disk — campaign.json, inventory.json,
cases.json and evidence/ — so it is regenerable, diffable, and cannot drift from
what was measured. Nothing is authored here that was not measured there.

Three properties the page must keep, because each answers a way these artifacts
go wrong:

  · **Denominators everywhere.** Never a count without its total. `41 of 52` is a
    result; `41` is a claim.
  · **Gaps rendered, not omitted.** An uncovered surface, an unarmed pass and a
    not-observable atom each get a visible row. A page that shows only what
    passed is the coverage theatre this whole skill exists to prevent.
  · **Stable ids as anchors.** Every row is `id="CASE-0007"`, so a review comment,
    a commit message or a later session can link straight to the evidence.

Usage:
    evidence-page.py <campaign-dir> [--out evidence.html] [--embed] [--title "..."]

`--embed` inlines every image as a data URI, producing one portable file. Without
it, images are referenced relatively and the page travels with its evidence dir.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_TONE = {
    "pass": "ok", "fail": "bad", "skip": "warn", "n/a": "mute",
    "unselected": "carried", "open": "open",
}

# Kept in step with campaign.py, which gates on them. Weakest first.
ORACLE_RUNGS = ("touch", "presence", "structural", "structural-visual",
                "outcome", "metamorphic", "raster-visual", "interactive-glass", "visual")
EFFECT_RUNGS = ("outcome", "metamorphic", "raster-visual", "interactive-glass")


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def state_of(status: str) -> str:
    s = (status or "").strip().lower()
    if s in ("pass", "fail"):
        return s
    if s.startswith("skip"):
        return "skip"
    if s.startswith("n/a"):
        return "n/a"
    # A case a selective run did not select. Its own state, because rendering it
    # as open makes a deliberate selection look like unfinished work, and
    # rendering it as pass is the coverage theatre this file exists to prevent.
    if s.startswith("unselected"):
        return "unselected"
    return "open"


def load(d: Path, name: str, default):
    p = d / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else default


def img_src(d: Path, rel: str, embed: bool) -> str:
    if not rel:
        return ""
    if rel.startswith(("http://", "https://", "data:")):
        return rel
    p = (d / rel)
    if not embed:
        return esc(rel)
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def is_image(rel: str) -> bool:
    return rel.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"))


CSS = """
:root{--bg:#F7F8FA;--panel:#FFF;--ink:#12161C;--dim:#5C6675;--line:#E2E6EC;
--ok:#127A4A;--bad:#C0392B;--warn:#9A6300;--mute:#7A8497;--open:#B4341F;--carried:#3E6D9C;
--accent:#1F3FA6;--okbg:#E8F5EE;--badbg:#FBEAE7;--warnbg:#FBF3E2;--mutebg:#F0F2F5;--openbg:#FDECE8;}
@media (prefers-color-scheme:dark){:root{--bg:#0D1117;--panel:#151B23;--ink:#E7EDF5;--dim:#98A3B3;
--line:#252D38;--ok:#5FD39B;--bad:#F08579;--warn:#E0B457;--mute:#8592A6;--open:#F0A08C;--carried:#7FB0DA;
--accent:#7EA2F5;--okbg:#12291F;--badbg:#2C1714;--warnbg:#2B2312;--mutebg:#1B222C;--openbg:#2E1A15;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.5 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.wrap{display:grid;grid-template-columns:210px minmax(0,1fr);min-height:100vh}
nav{border-right:1px solid var(--line);padding:18px 14px;position:sticky;top:0;height:100vh;overflow:auto}
nav h1{font-size:15px;margin:0 0 2px}
nav .sub{color:var(--dim);font-size:11.5px;margin-bottom:16px}
nav a{display:flex;justify-content:space-between;gap:8px;padding:6px 9px;border-radius:7px;
color:var(--ink);text-decoration:none;font-size:13px}
nav a:hover{background:var(--mutebg)} nav a .n{color:var(--dim);font-size:11px;font-variant-numeric:tabular-nums}
/* min-width:0 is load-bearing: a grid item defaults to min-width:auto, so a wide
   child pushes the track past the viewport and the BODY scrolls sideways rather
   than the child's own container. Measured at 1280: main ran to 1299. */
main{padding:22px 26px 90px;max-width:1500px;min-width:0}
section{margin-bottom:40px;scroll-margin-top:16px}
h2{font-size:19px;margin:0 0 4px} .lede{color:var(--dim);margin:0 0 14px;max-width:78ch}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:9px 13px;min-width:112px}
.stat b{display:block;font-size:20px;line-height:1.15} .stat span{color:var(--dim);font-size:11.5px}
.chip{display:inline-flex;align-items:center;gap:5px;border-radius:999px;padding:2px 9px;
font-size:11.5px;font-weight:600;white-space:nowrap}
.ok{background:var(--okbg);color:var(--ok)} .bad{background:var(--badbg);color:var(--bad)}
.warn{background:var(--warnbg);color:var(--warn)} .mute{background:var(--mutebg);color:var(--mute)}
.open{background:var(--openbg);color:var(--open)}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
table{width:100%;border-collapse:collapse;min-width:760px}
th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13px}
td.assert{min-width:260px} td.why{min-width:220px;color:var(--dim);font-size:12px}
th{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--dim);font-weight:600}
tr:last-child td{border-bottom:none}
tr:target td{background:var(--warnbg)}
.id{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--dim)}
.id a{color:inherit;text-decoration:none} .id a:hover{color:var(--accent)}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(232px,1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:11px;overflow:hidden}
.card img{width:100%;display:block;background:var(--mutebg);aspect-ratio:16/10;object-fit:cover;object-position:top}
.card .body{padding:9px 11px} .card .body b{font-size:12.5px} .card .body p{margin:3px 0 0;color:var(--dim);font-size:11.5px}
.flow{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px;margin-bottom:14px}
.steps{display:flex;gap:12px;overflow-x:auto;padding-bottom:6px}
.step{min-width:230px;max-width:230px}
.step img{width:100%;border:1px solid var(--line);border-radius:8px;display:block;background:var(--mutebg)}
.step .cap{font-size:11.5px;color:var(--dim);margin-top:5px}
.atoms{margin:5px 0 0;padding-left:15px;font-size:11.5px;color:var(--dim)}
.bar{display:flex;height:7px;border-radius:999px;overflow:hidden;background:var(--mutebg);margin:4px 0 14px}
.bar i{display:block}
#q{width:100%;max-width:420px;padding:8px 11px;border:1px solid var(--line);border-radius:9px;
background:var(--panel);color:var(--ink);font-size:13px;margin-bottom:12px}
.hidden{display:none!important}
.wall{position:relative;height:74vh;border:1px solid var(--line);border-radius:11px;overflow:hidden;
background:var(--mutebg);cursor:grab}
.wall.drag{cursor:grabbing}
.world{position:absolute;top:0;left:0;transform-origin:0 0;will-change:transform}
.cellw{position:absolute}
.cellw img{width:420px;height:262px;object-fit:cover;object-position:top;border-radius:8px;
border:1px solid var(--line);background:var(--panel);display:block}
.cellw .lab{font-size:12px;margin-top:5px;display:flex;gap:6px;align-items:center}
.hud{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);display:flex;gap:3px;
background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:5px;z-index:5}
.hud button{border:none;background:transparent;color:var(--ink);font:600 12px/1 inherit;
padding:6px 10px;border-radius:999px;cursor:pointer}
.hud button:hover{background:var(--mutebg)}
.empty{color:var(--dim);font-style:italic;padding:10px 0}
"""

JS = """
const q=document.getElementById('q');
if(q)q.addEventListener('input',()=>{const t=q.value.trim().toLowerCase();
document.querySelectorAll('[data-search]').forEach(el=>{
el.classList.toggle('hidden',t&&!el.dataset.search.includes(t));});});

// The wall: pan by drag, zoom toward the cursor. The world is transformed via a
// ref so the cells render once and never re-render while panning.
const wall=document.getElementById('wall');
if(wall){const world=wall.querySelector('.world');
let x=40,y=40,k=0.34,down=false,px=0,py=0;
const apply=()=>world.style.transform=`translate(${x}px,${y}px) scale(${k})`;
apply();
wall.addEventListener('pointerdown',e=>{down=true;px=e.clientX;py=e.clientY;wall.classList.add('drag');wall.setPointerCapture(e.pointerId);});
wall.addEventListener('pointermove',e=>{if(!down)return;x+=e.clientX-px;y+=e.clientY-py;px=e.clientX;py=e.clientY;apply();});
wall.addEventListener('pointerup',e=>{down=false;wall.classList.remove('drag');});
wall.addEventListener('wheel',e=>{e.preventDefault();const r=wall.getBoundingClientRect();
const mx=e.clientX-r.left,my=e.clientY-r.top;
if(e.ctrlKey||e.metaKey){const f=Math.exp(-e.deltaY*0.0022),nk=Math.min(2,Math.max(0.05,k*f));
x=mx-(mx-x)*(nk/k);y=my-(my-y)*(nk/k);k=nk;}else{x-=e.deltaX;y-=e.deltaY;}apply();},{passive:false});
const zoom=f=>{const r=wall.getBoundingClientRect(),mx=r.width/2,my=r.height/2;
const nk=Math.min(2,Math.max(0.05,k*f));x=mx-(mx-x)*(nk/k);y=my-(my-y)*(nk/k);k=nk;apply();};
wall.querySelector('[data-in]').onclick=()=>zoom(1.25);
wall.querySelector('[data-out]').onclick=()=>zoom(0.8);
wall.querySelector('[data-fit]').onclick=()=>{const b=world.getBoundingClientRect(),r=wall.getBoundingClientRect();
k=Math.min(r.width/(b.width/k||1),r.height/(b.height/k||1))*0.92;x=24;y=24;apply();};
wall.querySelector('[data-100]').onclick=()=>{k=1;x=24;y=24;apply();};}
"""


def bar(counts: dict) -> str:
    total = sum(counts.values()) or 1
    order = [("pass", "var(--ok)"), ("fail", "var(--bad)"), ("skip", "var(--warn)"),
             ("n/a", "var(--mute)"), ("unselected", "var(--carried)"),
             ("open", "var(--open)")]
    return ('<div class="bar">' + "".join(
        f'<i style="width:{counts.get(k, 0) / total * 100:.2f}%;background:{c}"></i>'
        for k, c in order) + "</div>")


# A picture on this page makes two claims: that pixels were captured, and that
# they are of the thing named beneath them. The page used to render the second
# one silently — `alt` came from the label, so a wrong image arrived under a
# right-sounding caption, and a reader had no way to tell an unproved subject
# from a proved one. Every rendered capture now carries its provenance.
PROV_TONE = {"manifest": "ok", "witnessed": "ok", "filename": "bad", "manual": "warn"}
PROV_TEXT = {
    "manifest": "subject recorded at capture",
    "witnessed": "subject judged against its reference",
    "filename": "subject unproved — bound by filename only",
    "manual": "subject not recordable by this channel",
}


def provenance(shot: str, subject: str, manifest: dict, verdicts: dict) -> str:
    """The badge that travels with every published picture."""
    if subject in verdicts:
        v = str(verdicts[subject].get("verdict", "")).lower()
        if v in ("pass", "match", "ok"):
            return "witnessed"
        return "filename" if v else "manifest"
    e = manifest.get(shot) or {}
    if str(e.get("channel", "")).lower() in ("manual", "hand-delivered", "photograph"):
        return "manual"
    return "manifest" if e.get("target") else "filename"


def prov_chip(kind: str) -> str:
    return (f"<span class='chip {PROV_TONE.get(kind, 'mute')}' "
            f"title='{esc(PROV_TEXT.get(kind, kind))}'>{esc(kind)}</span>")


def build(d: Path, out: Path, embed: bool, title: str | None) -> int:
    campaign = load(d, "campaign", {})
    inventory = load(d, "inventory", {"requirement": [], "surface": [], "flow": [], "component": []})
    cases = load(d, "cases", [])

    manifest = {}
    mp = d / "evidence/shots/captures.json"
    if mp.exists():
        try:
            manifest = {str(e.get("path", "")): e for e in json.loads(mp.read_text())}
        except ValueError:
            manifest = {}
    verdicts = {}
    vp = d / "witness-verdicts.json"
    if vp.exists():
        try:
            verdicts = {v.get("subject"): v for v in json.loads(vp.read_text()) if v.get("subject")}
        except ValueError:
            verdicts = {}

    reqs = inventory.get("requirement", [])
    surfaces = inventory.get("surface", [])
    flows = inventory.get("flow", [])
    components = inventory.get("component", [])

    counts = {"pass": 0, "fail": 0, "skip": 0, "n/a": 0, "unselected": 0, "open": 0}
    for c in cases:
        counts[state_of(c.get("status"))] += 1
    armed = sum(1 for c in cases if c.get("armed") and state_of(c.get("status")) == "pass")

    # What the cases actually check. Kept in the same order as the rungs so the
    # mix reads weakest-first, and an unrated case is shown as unrated rather
    # than folded into the nearest rung.
    mix = {r: 0 for r in ORACLE_RUNGS}
    mix["unrated"] = 0
    for c in cases:
        mix[c.get("oracle") if c.get("oracle") in ORACLE_RUNGS else "unrated"] += 1
    effect = sum(mix[r] for r in EFFECT_RUNGS)

    by_flow: dict[str, list[dict]] = {}
    for c in cases:
        by_flow.setdefault(c.get("flow", ""), []).append(c)

    by_surface: dict[str, list[dict]] = {}
    for c in cases:
        by_surface.setdefault(c.get("surface", ""), []).append(c)
    uncovered = [s for s in surfaces if not by_surface.get(s["id"])]

    name = title or campaign.get("project", "Campaign")
    P: list[str] = []
    A = P.append

    A(f"<!doctype html><html lang=en><head><meta charset=utf-8>"
      f"<meta name=viewport content='width=device-width,initial-scale=1'>"
      f"<title>{esc(name)} — evidence</title><style>{CSS}</style></head><body><div class=wrap>")

    # ── rail
    A("<nav><h1>" + esc(name) + "</h1><div class=sub>"
      + esc(", ".join(campaign.get("lanes", []) or ["no lane declared"]))
      + "<br>" + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") + "</div>")
    for anchor, label, n in [("coverage", "Coverage", len(cases)),
                             ("requirements", "Requirements", len(reqs)), ("wall-sec", "The wall", len(surfaces)),
                             ("flows", "Flows", len(flows)), ("surfaces", "Surfaces", len(surfaces)),
                             ("components", "Components", len(components)),
                             ("defects", "Defects", counts["fail"]),
                             ("gaps", "Not covered", counts["open"] + counts["skip"] + len(uncovered)),
                             ("methods", "Methods", 0)]:
        A(f"<a href='#{anchor}'>{esc(label)}<span class=n>{n if n else ''}</span></a>")
    A("</nav><main>")

    # ── coverage
    A("<section id=coverage><h2>Coverage</h2>")
    A("<p class=lede>Every count carries its total. The armed ratio is separate on purpose: "
      "a suite is only known to bite where an assertion was watched to fail with the behaviour "
      "removed.</p>")

    # A selective run says something narrower than a full one, so the page has to
    # say which it was. Rendering a carried result as a pass is the coverage
    # theatre this whole file exists to prevent.
    run = campaign.get("run", {})
    if (run.get("scope") or "full").strip().lower() == "selective":
        A("<p class=lede><b>This is a selective run.</b> "
          f"{len(cases) - counts['unselected']} of {len(cases)} cases ran; "
          f"{counts['unselected']} carry a result from an earlier full run of "
          f"{esc(run.get('lastFullRun') or 'an unrecorded date')}. "
          f"Basis: <code>{esc(run.get('basis') or 'NONE DECLARED')}</code>. "
          "It says what changed passes and the rest is unchanged since that date — "
          "not that the suite passes.</p>")
    elif run.get("lastFullRun"):
        A("<p class=lede><b>Full run</b> — every case in the campaign was run, "
          f"{esc(run.get('lastFullRun'))}.</p>")

    A("<div class=stats>"
      f"<div class=stat><b>{len(reqs)}</b><span>requirements</span></div>"
      f"<div class=stat><b>{len(surfaces)}</b><span>surfaces enumerated</span></div>"
      f"<div class=stat><b>{len(surfaces) - len(uncovered)} of {len(surfaces)}</b><span>surfaces with a case</span></div>"
      f"<div class=stat><b>{len(cases)}</b><span>cases</span></div>"
      f"<div class=stat><b>{counts['pass']}</b><span>pass</span></div>"
      f"<div class=stat><b>{counts['fail']}</b><span>fail</span></div>"
      + (f"<div class=stat><b>{counts['unselected']}</b><span>carried, not re-run</span></div>"
         if counts['unselected'] else "")
      + f"<div class=stat><b>{armed} of {counts['pass']}</b><span>passes armed</span></div>"
      f"<div class=stat><b>{effect} of {len(cases)}</b><span>assert an effect</span></div>"
      f"<div class=stat><b>{len(flows)}</b><span>flows</span></div>"
      f"<div class=stat><b>{len(components)}</b><span>components</span></div>"
      "</div>")
    A(bar(counts))
    if mix:
        A("<p class=lede><b>Oracle mix:</b> "
          + " · ".join(f"{esc(k)} {v}" for k, v in mix.items() if v)
          + ". A case's rung is what it checks, not how hard it looked. Presence and touch "
            "prove a surface rendered; only outcome, metamorphic and visual prove it did "
            "something.</p>")
    if campaign.get("sample"):
        A(f"<p class=lede><b>Declared sample:</b> {esc(campaign['sample'])}</p>")
    A("<input id=q placeholder='Filter by id, surface, state or assertion…'>")
    A("<div class=tw><table><thead><tr><th>Case</th><th>Surface</th><th>State</th><th>Lane</th>"
      "<th>Assertion</th><th>Oracle</th><th>Status</th><th>Why</th><th>Armed</th><th>Evidence</th></tr></thead><tbody>")
    labels = {s["id"]: s.get("label", "") for s in surfaces}
    for c in cases:
        st = state_of(c.get("status"))
        blob = " ".join(str(c.get(k, "")) for k in
                        ("id", "surface", "state", "lane", "assertion", "status", "oracle")).lower()
        blob += " " + labels.get(c.get("surface", ""), "").lower()
        ev = c.get("evidence", [])
        evcell = " ".join(
            f"<a class=id href='{esc(e)}'>{esc(Path(e).name)}</a>" for e in ev) or "<span class=id>—</span>"
        rung = c.get("oracle") if c.get("oracle") in ORACLE_RUNGS else "unrated"
        A(f"<tr id='{esc(c['id'])}' data-search='{esc(blob)}'>"
          f"<td class=id><a href='#{esc(c['id'])}'>{esc(c['id'])}</a></td>"
          f"<td>{esc(c.get('surface', ''))} {esc(labels.get(c.get('surface', ''), ''))}</td>"
          f"<td>{esc(c.get('state', ''))}</td><td>{esc(c.get('lane', ''))}</td>"
          f"<td class=assert>{esc(c.get('assertion', ''))}</td>"
          f"<td><span class='chip {'ok' if rung in EFFECT_RUNGS else 'mute'}'>{esc(rung)}</span></td>"
          f"<td><span class='chip {STATE_TONE[st]}'>{esc(st)}</span></td>"
          f"<td class=why>{esc(c.get('status','') if st in ('skip','n/a') else (c.get('note','') or ''))}</td>"
          f"<td>{'yes' if c.get('armed') else '<span class=id>—</span>'}</td>"
          f"<td>{evcell}</td></tr>")
    if not cases:
        A("<tr><td colspan=10 class=empty>No cases registered yet.</td></tr>")
    A("</tbody></table></div></section>")

    # ── requirements
    by_req: dict[str, list[dict]] = {}
    for c in cases:
        rs = c.get("req")
        for r in ([rs] if isinstance(rs, str) else (rs or [])):
            by_req.setdefault(r, []).append(c)
    A("<section id=requirements><h2>Requirements</h2>"
      "<p class=lede>What the project says it does, and what checked it. A requirement "
      "with no case is the campaign's real gap: something promised that nothing tested. "
      "A deferred one is exempt, and carries its citation.</p>")
    if reqs:
        A("<div class=tw><table><thead><tr><th>Req</th><th>Requirement</th><th>Class</th>"
          "<th>Evidence</th><th>Source</th><th>Cases</th></tr></thead><tbody>")
        for r in reqs:
            cs = by_req.get(r["id"], [])
            deferred = r.get("class") == "deferred"
            tone = "mute" if deferred else ("ok" if cs else "open")
            note = "deferred" if deferred else (f"{len(cs)} case(s)" if cs else "nothing checks this")
            rid = esc(r["id"])
            links = " ".join(
                f"<a class=id href='#{esc(c['id'])}'>{esc(c['id'])}</a>" for c in cs)
            A(f"<tr id='{rid}'><td class=id><a href='#{rid}'>{rid}</a></td>"
              f"<td class=assert>{esc(r.get('text', ''))}</td>"
              f"<td>{esc(r.get('class', ''))}</td>"
              f"<td>{esc(r.get('evidence', ''))}</td>"
              f"<td class=why>{esc(r.get('source', ''))}</td>"
              f"<td><span class='chip {tone}'>{esc(note)}</span> {links}</td></tr>")
        A("</tbody></table></div>")
    else:
        A("<p class=empty>No requirement inventory. Coverage is then measured against what "
          "the application renders rather than what the project promised, and a feature "
          "nobody built cannot be detected. Say so in the report.</p>")
    A("</section>")

    # ── the wall
    A("<section id=wall-sec><h2>The wall</h2>"
      "<p class=lede>Every captured surface on one canvas. Drag to pan, ⌘/ctrl-scroll to zoom "
      "toward the cursor. Each cell carries how its subject was established: "
      "<b>witnessed</b> (judged against its reference), <b>manifest</b> (the channel recorded "
      "what it was pointed at), <b>filename</b> (nothing but the name binds this picture to "
      "this surface).</p>")
    shots = [(s, s.get("shot", "")) for s in surfaces if s.get("shot")]
    if shots:
        COLS, CW, CH, GAP = 5, 420, 300, 46
        A("<div class=wall id=wall><div class=world>")
        for i, (s, shot) in enumerate(shots):
            col, row = i % COLS, i // COLS
            cs = by_surface.get(s["id"], [])
            fails = sum(1 for c in cs if state_of(c.get("status")) == "fail")
            tone = "bad" if fails else ("ok" if cs else "mute")
            A(f"<div class=cellw style='left:{col * (CW + GAP)}px;top:{row * (CH + GAP + 26)}px'>"
              f"<img src='{img_src(d, shot, embed)}' alt='{esc(s.get('label', ''))}' loading=lazy>"
              f"<div class=lab><span class=id>{esc(s['id'])}</span> {esc(s.get('label', ''))}"
              f" <span class='chip {tone}'>{len(cs)} case{'s' if len(cs) != 1 else ''}</span>"
              f" {prov_chip(provenance(shot, s['id'], manifest, verdicts))}</div></div>")
        A("</div><div class=hud><button data-out>−</button><button data-in>+</button>"
          "<button data-fit>Fit</button><button data-100>100%</button></div></div>")
    else:
        A("<p class=empty>No surface captures yet. A surface gains a wall cell when its "
          "inventory entry names a <code>shot</code>.</p>")
    A("</section>")

    # ── flows
    A("<section id=flows><h2>Flows</h2>"
      "<p class=lede>Each step carries what it was supposed to show. An atom that a still "
      "picture cannot answer is marked not observable rather than failed.</p>")
    if flows:
        for f in flows:
            fc = by_flow.get(f["id"], [])
            weak = f.get("critical") and not any(c.get("oracle") in EFFECT_RUNGS for c in fc)
            A(f"<div class=flow id='{esc(f['id'])}'><div><span class=id>"
              f"<a href='#{esc(f['id'])}'>{esc(f['id'])}</a></span> <b>{esc(f.get('label', ''))}</b>"
              + (" <span class='chip bad'>critical · presence only</span>" if weak
                 else " <span class='chip ok'>critical</span>" if f.get("critical") else "")
              + f" <span class=id>{len(f.get('steps', []))} steps</span></div><div class=steps>")
            for j, step in enumerate(f.get("steps", []), 1):
                # The step's OWN id, not one recomputed from the loop index: a
                # reordered or deleted step used to renumber every anchor after
                # it, silently repointing links a reader had already shared.
                sid = step.get("id") or f"{f['id']}.{j:02d}"
                shot = step.get("shot", "")
                A(f"<div class=step id='{esc(sid)}'>")
                if shot:
                    A(f"<img src='{img_src(d, shot, embed)}' alt='{esc(step.get('label', ''))}' loading=lazy>")
                A(f"<div class=cap><span class=id>{esc(sid)}</span> {esc(step.get('label', ''))}"
                  + (f" {prov_chip(provenance(shot, sid, manifest, verdicts))}" if shot else "")
                  + "</div>")
                atoms = step.get("atoms", [])
                if atoms:
                    A("<ul class=atoms>" + "".join(
                        f"<li>{esc(a.get('text', a) if isinstance(a, dict) else a)}"
                        + (f" <span class='chip {STATE_TONE.get(a.get('verdict', 'n/a'), 'mute')}'>"
                           f"{esc(a.get('verdict'))}</span>" if isinstance(a, dict) and a.get("verdict") else "")
                        + "</li>" for a in atoms) + "</ul>")
                A("</div>")
            A("</div></div>")
    else:
        A("<p class=empty>No flows registered.</p>")
    A("</section>")

    # ── surfaces
    A("<section id=surfaces><h2>Surfaces</h2><div class=grid>")
    for s in surfaces:
        cs = by_surface.get(s["id"], [])
        fails = sum(1 for c in cs if state_of(c.get("status")) == "fail")
        tone = "bad" if fails else ("ok" if cs else "open")
        note = f"{len(cs)} case{'s' if len(cs) != 1 else ''}" if cs else "no case — unaudited"
        A(f"<div class=card id='{esc(s['id'])}'>")
        if s.get("shot"):
            A(f"<img src='{img_src(d, s['shot'], embed)}' alt='{esc(s.get('label', ''))}' loading=lazy>")
        A(f"<div class=body><b>{esc(s.get('label', ''))}</b>"
          f"<p><span class=id>{esc(s['id'])}</span> {esc(s.get('route', s.get('lane', '')))}</p>"
          f"<p><span class='chip {tone}'>{esc(note)}</span>"
          + (f" {prov_chip(provenance(s['shot'], s['id'], manifest, verdicts))}"
             if s.get("shot") else "")
          + "</p></div></div>")
    A("</div></section>")

    # ── components
    A("<section id=components><h2>Components</h2>"
      "<p class=lede>The third enumeration. Types nobody opened are not covered, and the "
      "fraction says so.</p><div class=grid>")
    for c in components:
        A(f"<div class=card id='{esc(c['id'])}'>")
        if c.get("shot"):
            A(f"<img src='{img_src(d, c['shot'], embed)}' alt='{esc(c.get('label', ''))}' loading=lazy>")
        A(f"<div class=body><b>{esc(c.get('label', ''))}</b>"
          f"<p><span class=id>{esc(c['id'])}</span> · {esc(c.get('platform', ''))}"
          f" · {esc(c.get('instances', '?'))} instance(s)</p>"
          + (f"<p><span class='chip {'ok' if c.get('opened') else 'open'}'>"
             f"{'opened' if c.get('opened') else 'not opened'}</span></p>")
          + "</div></div>")
    if not components:
        A("<p class=empty>No component inventory captured.</p>")
    A("</div></section>")

    # ── defects
    fails = [c for c in cases if state_of(c.get("status")) == "fail"]
    A("<section id=defects><h2>Defects</h2>")
    if fails:
        A("<div class=tw><table><thead><tr><th>Case</th><th>Surface</th><th>What failed</th>"
          "<th>Note</th><th>Evidence</th></tr></thead><tbody>")
        for c in fails:
            ev = " ".join(f"<a class=id href='{esc(e)}'>{esc(Path(e).name)}</a>"
                          for e in c.get("evidence", [])) or "<span class=id>—</span>"
            A(f"<tr><td class=id><a href='#{esc(c['id'])}'>{esc(c['id'])}</a></td>"
              f"<td>{esc(c.get('surface', ''))}</td><td>{esc(c.get('assertion', ''))}</td>"
              f"<td>{esc(c.get('note', ''))}</td><td>{ev}</td></tr>")
        A("</tbody></table></div>")
    else:
        A("<p class=empty>No failing case. That is a statement about the cases that ran, "
          "not about the application.</p>")
    A("</section>")

    # ── gaps
    A("<section id=gaps><h2>Not covered</h2>"
      "<p class=lede>Rendered rather than omitted. This section is the difference between a "
      "finished campaign and one that looks finished.</p>")
    rows = []
    for r in reqs:
        if r.get("class") != "deferred" and not by_req.get(r["id"]):
            rows.append((r["id"], r.get("text", "")[:70],
                         "no case traces to this requirement", ""))
    for s in uncovered:
        rows.append((s["id"], s.get("label", ""), "no case at all", ""))
    for c in cases:
        st = state_of(c.get("status"))
        if st in ("open", "skip", "n/a"):
            rows.append((c["id"], c.get("surface", ""), st, c.get("status", "")))
    unarmed = [c for c in cases if state_of(c.get("status")) == "pass" and not c.get("armed")]
    if rows or unarmed:
        A("<div class=tw><table><thead><tr><th>Id</th><th>What</th><th>Why it is not covered</th>"
          "</tr></thead><tbody>")
        for i, what, why, detail in rows:
            A(f"<tr><td class=id>{esc(i)}</td><td>{esc(what)}</td>"
              f"<td>{esc(detail or why)}</td></tr>")
        if unarmed:
            A(f"<tr><td class=id>—</td><td>{len(unarmed)} passing case(s)</td>"
              f"<td>Passing but never armed: nobody has watched these fail with the behaviour "
              f"removed, so they are not known to bite.</td></tr>")
        A("</tbody></table></div>")
    else:
        A("<p class=empty>Nothing open, and every pass is armed.</p>")
    A("</section>")

    # ── methods
    A("<section id=methods><h2>Methods</h2><div class=tw><table><tbody>")
    for k, v in [("Project", campaign.get("project", "")),
                 ("Started", campaign.get("startedAt", "")),
                 ("Lanes", ", ".join(campaign.get("lanes", []))),
                 ("Axes varied", ", ".join(campaign.get("axes", [])) or "not declared"),
                 ("Design of record", campaign.get("designOfRecord", "") or "none"),
                 ("Declared sample", campaign.get("sample", "") or "none — full campaign of what is enumerated"),
                 ("Evidence", f"{sum(len(c.get('evidence', [])) for c in cases)} artifacts referenced"),
                 ("Built", datetime.now(timezone.utc).isoformat(timespec="seconds"))]:
        A(f"<tr><th style='width:180px'>{esc(k)}</th><td>{esc(v)}</td></tr>")
    A("</tbody></table></div>")
    for note in campaign.get("laneLimits", []):
        A(f"<p class=lede>· {esc(note)}</p>")
    A("</section>")

    A(f"</main></div><script>{JS}</script></body></html>")

    out.write_text("".join(P))
    print(f"Wrote {out} — {len(surfaces)} surfaces · {len(flows)} flows · "
          f"{len(components)} components · {len(cases)} cases "
          f"({counts['pass']} pass, {counts['fail']} fail, {armed} armed)")
    if uncovered:
        print(f"  {len(uncovered)} surface(s) carry no case and are rendered as gaps: "
              f"{', '.join(s['id'] for s in uncovered)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the living evidence page.")
    ap.add_argument("dir", help="Campaign directory holding campaign/inventory/cases json.")
    ap.add_argument("--out", default=None)
    ap.add_argument("--embed", action="store_true", help="Inline images as data URIs.")
    ap.add_argument("--title")
    args = ap.parse_args()
    d = Path(args.dir).resolve()
    if not (d / "campaign.json").exists():
        sys.exit(f"No campaign.json in {d}. Run campaign.py init first.")
    return build(d, Path(args.out) if args.out else d / "evidence.html", args.embed, args.title)


if __name__ == "__main__":
    sys.exit(main())
