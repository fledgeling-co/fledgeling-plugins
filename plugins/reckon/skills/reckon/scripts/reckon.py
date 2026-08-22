#!/usr/bin/env python3
"""reckon — reconcile stated intent against verification evidence.

Reads a repo's feature-brief queue (and PRD, if named) alongside a
test-campaign registry, and resolves every entity on both sides into exactly
one class of a partition. The partition is the point: an entity that was never
measured cannot fall out of the ledger, because there is nowhere for it to
fall to except `unmeasured`.

Subcommands
    build   read the inputs, write ledger.json
    check   re-read a ledger and gate it; exit code is the verdict
    ratchet compare two ledgers and refuse silent transitions out of unmeasured

Exit codes (check, ratchet)
    0  clean
    1  conservation or placement violation — the ledger is structurally unsound
    2  disclosure violation — a headline number the ledger does not support
    3  ratchet violation — an item left `unmeasured` with no evidence for it
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# The vocabulary, and why each word is separate from its neighbour.
#
# These names are test-campaign's, deliberately. Re-spelling them here would
# create a second vocabulary that drifts from the registry it reads, and the
# drift would be silent because both halves would still parse.
# ---------------------------------------------------------------------------

# A case status that means the instrument returned a verdict about the product.
# `n/a` and `skip` are deliberately absent: those are decisions somebody made,
# not measurements an instrument returned, and regulated verification regimes
# keep them in a separate register for exactly that reason. Folding a waiver
# into the numerator is how a campaign closed by decision reads as a campaign
# closed by evidence. (ECSS-E-ST-10-02C's VCD; FAA AC 20-189.)
ADJUDICATED = ("pass", "fail")

# Decisions. Not remaining work, and not done either — a third thing, which
# stays visible because the reason it was taken may stop being true.
WAIVED_STATUS = ("n/a", "skip")

# Frontmatter statuses on a brief that amount to the same decision.
WAIVED_DECLARED = ("waived", "deferred", "wontfix", "won't fix", "declined", "out of scope")

# A case status that means no verdict was reached. Each has a different remedy
# — blocked needs access, inconclusive needs a better instrument, unoracled
# needs an oracle, unselected needs re-running — but they share a class,
# because to a reader of a remaining-work list they are the same thing: an
# answer nobody has.
UNMEASURED_STATUS = ("blocked", "inconclusive", "unoracled", "unselected", "open")

# The oracle ladder, weakest first. A rung is not a quality score; it is what
# the check was able to observe. `presence` proves a thing exists on screen,
# which is compatible with it doing nothing at all.
ORACLE_RUNGS = ("presence", "structural", "outcome", "effect-witness", "interactive-glass")

# Retiring a brief means deleting somebody's stated intent. Doing that on
# `presence` retires intent on the weakest evidence the ladder has, so the
# floor sits above it.
RETIREMENT_RUNG = "outcome"

# Requirement evidence vocabulary.
EVIDENCE_OBSERVED = ("observed",)
EVIDENCE_SELF_REPORTED = ("reported", "unknown")
EVIDENCE_DISPUTED = ("contradicted", "vacuous")

# The classes. Every entity lands in exactly one.
CLASSES = (
    "unbuilt",       # named, and nothing in the registry answers to it
    "broken",        # measured, and the answer was no
    "unmeasured",    # nobody found out
    "unnamed",       # the registry found it; no brief or requirement claims it
    "undecided",     # the documents and the evidence disagree; needs a ruling
    "retirable",     # measured done at a rung that can carry the claim
    "waived",        # somebody decided not to; an exception, never a pass
    "verified-done", # measured done; not remaining, kept for the denominator
)

# What kind of work each class is. Executors filter on this: evidence-work must
# never reach a feature backlog, because building a feature does not answer a
# question about whether another feature works.
KIND_OF = {
    "unbuilt": "product-work",
    "broken": "product-work",
    "unmeasured": "evidence-work",
    "unnamed": "decision-work",
    "undecided": "decision-work",
    "retirable": "bookkeeping",
    "waived": "exception",
    "verified-done": "none",
}

# Which classes a given piece of evidence may legally support. This table is
# the gate: a status on the left may only ever produce a class on the right.
LEGAL_CLASS = {
    "blocked": {"unmeasured"},
    "inconclusive": {"unmeasured"},
    "unoracled": {"unmeasured"},
    "unselected": {"unmeasured"},
    "open": {"unmeasured"},
    "fail": {"broken"},
    "pass": {"verified-done", "retirable"},
    "n/a": {"waived"},
    "skip": {"waived"},
}

# What each kind of not-knowing actually costs to fix. The remedies are
# different jobs for different people, and a single "test this properly" item
# sends all five to the wrong place.
REMEDY = {
    "blocked": "reach the state — credentials, a non-destructive route, or a hook that forces it",
    "inconclusive": "add observability — the instrument ran and could not read the answer",
    "unoracled": "build an oracle — nothing here decides what a pass would look like",
    "unselected": "re-run — this verdict is carried from an older run, against older code",
    "open": "run it — the case exists and was never attempted",
    "skip": "revisit the decision to skip",
    "reported": "obtain independent evidence — this is the project's own account of itself",
    "unknown": "obtain any evidence at all",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is",
    "are", "be", "it", "its", "that", "this", "as", "at", "by", "from", "not",
    "no", "can", "cannot", "does", "do", "has", "have", "was", "were", "when",
    "which", "what", "so", "but", "if", "then", "than", "into", "over", "per",
}


# ---------------------------------------------------------------------------
# Reading the inputs
# ---------------------------------------------------------------------------

def _load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_campaign(campaign_dir):
    """Read a test-campaign registry. Every part is optional except that at
    least one must be present, because a reckoning with no evidence at all is
    a different and much weaker claim, and the caller is told which it got."""
    if not campaign_dir:
        return {"present": False, "cases": [], "requirements": [], "surfaces": [],
                "defects": [], "flows": [], "components": [], "header": {}}

    header = _load_json(os.path.join(campaign_dir, "campaign.json"), {}) or {}
    cases = _load_json(os.path.join(campaign_dir, "cases.json"), []) or []
    inv = _load_json(os.path.join(campaign_dir, "inventory.json"), {}) or {}
    if isinstance(cases, dict):
        cases = cases.get("case", cases.get("cases", []))

    return {
        "present": bool(header or cases or inv),
        "header": header,
        "cases": cases,
        "requirements": inv.get("requirement", []),
        "surfaces": inv.get("surface", []),
        "defects": inv.get("defect", []),
        "flows": inv.get("flow", []),
        "components": inv.get("component", []),
    }


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def read_briefs(briefs_dir, ignore=()):
    """Read the feature-brief queue. A brief is one markdown file; its id is
    its slug. Frontmatter is parsed shallowly — enough to find a status and to
    recognise this tool's own emissions, which must not be counted as fresh
    intent on the next run or the queue inflates itself."""
    briefs = []
    if not briefs_dir or not os.path.isdir(briefs_dir):
        return briefs

    for name in sorted(os.listdir(briefs_dir)):
        if not name.endswith(".md"):
            continue
        if name in ignore or name.upper().startswith(("BRIEF-TEMPLATE", "README", "00-INDEX", "LEDGER")):
            continue
        path = os.path.join(briefs_dir, name)
        try:
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
        except (OSError, UnicodeDecodeError):
            continue

        meta, generated_by, source_ids = {}, None, []
        m = FRONTMATTER_RE.match(body)
        if m:
            for line in m.group(1).splitlines():
                if ":" not in line:
                    continue
                k, _, v = line.partition(":")
                meta[k.strip().lower()] = v.strip().strip("\"'")
            generated_by = meta.get("generated-by")
            raw = meta.get("reckon-sources", "")
            source_ids = [s.strip() for s in raw.strip("[]").split(",") if s.strip()]
            body = body[m.end():]

        title = ""
        for line in body.splitlines():
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                break

        briefs.append({
            "id": "BRIEF-" + os.path.splitext(name)[0],
            "file": name,
            "path": path,
            "title": title or os.path.splitext(name)[0].replace("-", " "),
            "text": body,
            "status": (meta.get("status") or "").lower(),
            "generated_by": generated_by,
            "source_ids": source_ids,
        })
    return briefs


# ---------------------------------------------------------------------------
# The join — brief ↔ requirement ↔ case
#
# This is the weak point of the whole method and it is treated as such. Briefs
# do not share ids with requirements, so matching them is the one inferential
# step in an otherwise mechanical pipeline. A reconciliation gate sitting on
# top of a bad join is theatre, so every edge carries how it was made, and the
# unmatched count is published rather than absorbed.
# ---------------------------------------------------------------------------

ID_RE = re.compile(r"\b(?:REQ|CASE|DEF|SURF|FLOW|COMP)-\d+\b")


def flatten_text(value):
    """Every registry field reaching `tokens` is free-form JSON, so it is not
    reliably a string.

    Measured on one real campaign's `inventory.json`: of 52 defect rows the
    `evidence` field was `None` on 31, a string on 16 and a **list on 5** — and
    `(text or "").lower()` raised `AttributeError: 'list' object has no
    attribute 'lower'` on the first list, so `build` crashed outright rather
    than producing a weaker join. The same field is free-form on requirements
    (`note`) and surfaces (`slug`), so fixing the one call site would only move
    the crash.

    A list is flattened rather than dropped. Dropping is the fail-closed
    direction and it is the wrong one here: `tokens` feeds the JOIN, which is
    already labelled a guess and already refuses to retire a brief on one, so
    silently shrinking it loses real signal while making the join look weaker
    than the evidence is. Nothing downstream trusts a token edge on its own."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(flatten_text(v) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(flatten_text(v) for v in value)
    return str(value)


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", flatten_text(text).lower())
            if len(w) > 2 and w not in STOPWORDS}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def build_join(briefs, campaign, threshold=0.18):
    """Return edges brief→registry-id, each with a method and a confidence.

    Two mechanisms, and they are not equal. An explicit id written into a
    brief or a registry note is a citation somebody made on purpose; token
    overlap is a guess. They are labelled differently so a reader can discount
    the second, and so the gate can refuse to retire a brief on a guess."""
    edges = []
    registry = []
    for r in campaign["requirements"]:
        registry.append((r.get("id"), "requirement", tokens(r.get("text", "")) | tokens(r.get("note", ""))))
    for d in campaign["defects"]:
        registry.append((d.get("id"), "defect", tokens(d.get("title", "")) | tokens(d.get("evidence", ""))))
    for s in campaign["surfaces"]:
        registry.append((s.get("id"), "surface", tokens(s.get("title", "")) | tokens(s.get("slug", ""))))

    # Registry notes frequently cite a brief by its own project id (SCR-0075).
    # Harvest those first: they are the strongest edges available.
    reverse_cites = defaultdict(set)
    for coll, kind in (("requirements", "requirement"), ("defects", "defect"), ("cases", "case")):
        for item in campaign[coll]:
            blob = " ".join(str(item.get(k, "")) for k in ("note", "title", "text", "evidence", "status"))
            for brief in briefs:
                stem = os.path.splitext(brief["file"])[0]
                key = stem.split("-")[0:2]
                token = "-".join(key)
                if len(token) > 4 and re.search(r"\b" + re.escape(token) + r"\b", blob, re.I):
                    reverse_cites[brief["id"]].add(item.get("id"))

    for brief in briefs:
        btok = tokens(brief["title"]) | tokens(brief["text"][:4000])
        cited = set(ID_RE.findall(brief["text"])) | set(brief["source_ids"]) | reverse_cites.get(brief["id"], set())
        for rid in sorted(x for x in cited if x):
            edges.append({"brief": brief["id"], "target": rid, "method": "cited", "confidence": 1.0})
        if cited:
            continue
        best, best_score, best_kind = None, 0.0, None
        for rid, kind, rtok in registry:
            score = jaccard(btok, rtok)
            if score > best_score:
                best, best_score, best_kind = rid, score, kind
        if best and best_score >= threshold:
            edges.append({"brief": brief["id"], "target": best, "method": "overlap",
                          "confidence": round(best_score, 3), "target_kind": best_kind})
    return edges


# ---------------------------------------------------------------------------
# Blocker clustering
#
# Twenty blocked cases are rarely twenty problems. In the campaign this was
# written against, one dead OAuth credential accounted for ten of them. The
# useful unit of remaining evidence-work is therefore the blocker, not the
# case, and the number worth ranking on is how much coverage resolving it
# would return.
# ---------------------------------------------------------------------------

NOISE_RE = re.compile(r"\b(case|cases|the|this|that|it|its)\b", re.I)


def blocker_tokens(note):
    """Reduce a blocker note to the words that identify its cause.

    The registry writes these as free prose, and the shape is consistent: a
    leading clause naming the cause, then a trailing clause about the one
    surface this case wanted. Ten cases blocked on one dead credential share
    the first and differ in the second, so weight the opening.
    """
    text = (note or "").split(":", 1)[-1].strip().lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    parts = re.split(r"(?<=[.;])\s+", text)
    head = " ".join(parts[:2])
    return tokens(NOISE_RE.sub(" ", head))


def cluster_blockers(unmeasured_rows, total_cases, threshold=0.30):
    """Group blocked cases by the cause behind them.

    Twenty blocked cases are rarely twenty problems. In the campaign this was
    written against, one dead OAuth credential accounted for ten of them, and
    a list of twenty separate line items would have hidden the single thing
    worth doing first. Exact-match keys do not find that — the notes differ in
    their tails — so this is single-link agglomeration on token overlap.

    The clustering is lossy on purpose and the ledger keeps every original
    note, so a reader who disagrees with a grouping can regroup it without
    having lost anything.
    """
    cases = [r for r in unmeasured_rows if r["entity"] == "case"]
    feats = [(r, blocker_tokens(r.get("note"))) for r in cases]

    clusters = []  # each: {"rows": [...], "tok": set}
    for row, tok in feats:
        if not tok:
            tok = {"unattributed"}
        best, best_score = None, 0.0
        for cl in clusters:
            score = jaccard(tok, cl["tok"])
            if score > best_score:
                best, best_score = cl, score
        if best is not None and best_score >= threshold:
            best["rows"].append(row)
            best["tok"] |= tok
        else:
            clusters.append({"rows": [row], "tok": set(tok)})

    out = []
    for cl in clusters:
        rows = cl["rows"]
        # The shortest note is usually the cause without one case's tail on it.
        notes = sorted((r.get("note") or "" for r in rows), key=len)
        out.append({
            "id": "BLOCK-0000",
            "summary": (notes[0] if notes else "")[:400],
            "cases": sorted(r["id"] for r in rows),
            "unblocks": len(rows),
            "coverage_gain_pct": round(100.0 * len(rows) / total_cases, 1) if total_cases else 0.0,
            "kind": "evidence-work",
        })
    out.sort(key=lambda g: (-g["unblocks"], g["summary"][:60]))
    for i, g in enumerate(out, 1):
        g["id"] = "BLOCK-%04d" % i
    return out


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def rung_index(oracle):
    try:
        return ORACLE_RUNGS.index(oracle)
    except ValueError:
        return -1


def state_of(status):
    """Campaign statuses carry their reason inline ('blocked: the credential
    is dead'). Split the verdict from the prose."""
    return (status or "open").split(":", 1)[0].strip()


def classify(briefs, campaign, edges, join_is_weak):
    rows = []
    matched_targets = {e["target"] for e in edges}
    edges_by_brief = defaultdict(list)
    for e in edges:
        edges_by_brief[e["brief"]].append(e)

    # --- cases -------------------------------------------------------------
    #
    # A case is a measurement, not a task. It still gets a row, because the
    # partition has to be total or the gate proves nothing — but it is marked
    # as corroborating rather than as work. Counting a failing case *and* the
    # defect it evidences as two remaining items is how a remaining-work list
    # doubles itself and stops being believed.
    case_by_surface = defaultdict(list)
    for c in campaign["cases"]:
        st = state_of(c.get("status"))
        cls = "unmeasured"
        if st == "fail":
            cls = "broken"
        elif st == "pass":
            cls = "verified-done"
        elif st in WAIVED_STATUS:
            cls = "waived"
        elif st in UNMEASURED_STATUS:
            cls = "unmeasured"
        blob = "%s %s" % (c.get("note") or "", c.get("status") or "")
        cited_defects = sorted(set(re.findall(r"\bDEF-\d+\b", blob)))
        rows.append({
            "id": c.get("id"), "entity": "case", "class": cls, "kind": KIND_OF[cls],
            "title": "%s · %s" % (c.get("surface", "?"), c.get("state", "?")),
            "status": st, "oracle": c.get("oracle"), "armed": c.get("armed"),
            "note": c.get("status") if ":" in str(c.get("status", "")) else c.get("note"),
            "surface": c.get("surface"), "lane": c.get("lane"),
            "is_work_item": False,
            "remedy": REMEDY.get(st) if cls == "unmeasured" else None,
            "rolls_up_to": cited_defects or None,
            "why": "a measurement, not a task: status %r may only be %s. It rolls up to %s."
                   % (st, "/".join(sorted(LEGAL_CLASS.get(st, {cls}))),
                      ", ".join(cited_defects) if cited_defects
                      else ("a blocker cluster" if cls == "unmeasured" else "its surface")),
        })
        if c.get("surface"):
            case_by_surface[c["surface"]].append((st, c.get("oracle")))

    # --- requirements ------------------------------------------------------
    for r in campaign["requirements"]:
        ev = (r.get("evidence") or "unknown").lower()
        if ev in EVIDENCE_DISPUTED:
            cls = "undecided"
            why = "requirement evidence %r is a disagreement between the documents and the build; a person rules on it, an instrument cannot" % ev
        elif ev in EVIDENCE_OBSERVED:
            cls = "verified-done"
            why = "requirement observed"
        else:
            cls = "unmeasured"
            why = "requirement evidence %r is the project's own account of itself, not an observation" % ev
        rows.append({
            "id": r.get("id"), "entity": "requirement", "class": cls, "kind": KIND_OF[cls],
            "title": (r.get("text") or "")[:200], "evidence": ev,
            "note": r.get("note"), "provider": r.get("provider"),
            "remedy": REMEDY.get(ev) if cls == "unmeasured" else None,
            "is_work_item": cls not in ("verified-done", "waived"), "why": why,
        })

    # --- defects -----------------------------------------------------------
    for d in campaign["defects"]:
        rows.append({
            "id": d.get("id"), "entity": "defect", "class": "broken", "kind": "product-work",
            "title": (d.get("title") or "")[:200], "severity": d.get("severity"),
            "surface": d.get("surface"), "note": (d.get("evidence") or "")[:400],
            "is_work_item": True,
            "why": "a defect is a measured negative result — the unit of product work behind every "
                   "failing case that cites it",
        })

    # --- surfaces ----------------------------------------------------------
    #
    # A surface is a location, not a task. It becomes work in exactly one
    # situation: nothing in the documents claims it, which makes it a decision
    # about whether it should exist at all.
    for s in campaign["surfaces"]:
        sid = s.get("id")
        seen = case_by_surface.get(sid, [])
        adjudicated = [x for x in seen if x[0] in ADJUDICATED]
        if adjudicated:
            cls = "verified-done"
            why = ("%d case(s) here reached a verdict, so the campaign can speak for this surface. "
                   "Whether those verdicts were good is carried by the cases and defects themselves."
                   % len(adjudicated))
        elif sid in matched_targets or seen:
            cls = "unmeasured"
            why = ("this surface is claimed but no case on it reached a verdict"
                   if sid in matched_targets else
                   "this surface has cases, none of which reached a verdict")
        else:
            cls = "unnamed"
            why = "the campaign found this surface; no brief and no requirement claims it"
        rows.append({
            "id": sid, "entity": "surface", "class": cls, "kind": KIND_OF[cls],
            "title": s.get("title") or s.get("slug") or "", "reachability": s.get("reachability"),
            "note": s.get("note"), "is_work_item": cls == "unnamed", "why": why,
        })

    # --- briefs ------------------------------------------------------------
    for b in briefs:
        my_edges = edges_by_brief.get(b["id"], [])
        cited = [e for e in my_edges if e["method"] == "cited"]
        support = cited or my_edges

        best_cls, best_why = "unbuilt", "no requirement, defect or case in the registry answers to this brief"
        if b["status"] in WAIVED_DECLARED:
            best_cls = "waived"
            best_why = ("the brief declares status %r — a decision, not a measurement. It stays on the "
                        "ledger because the reason for it may stop being true." % b["status"])
        elif support:
            targets = {e["target"] for e in support}
            req_ev = [(r.get("evidence") or "unknown").lower()
                      for r in campaign["requirements"] if r.get("id") in targets]
            hit_defect = any(t.startswith("DEF-") for t in targets)
            surf_cases = []
            for t in targets:
                surf_cases.extend(case_by_surface.get(t, []))

            best_rung = max([rung_index(o) for _, o in surf_cases] or [-1])
            any_fail = any(st == "fail" for st, _ in surf_cases)
            any_pass = any(st == "pass" for st, _ in surf_cases)

            if hit_defect or any_fail:
                best_cls = "broken"
                best_why = "the registry records a defect or a failing case against this brief's subject"
            elif any(e in EVIDENCE_DISPUTED for e in req_ev):
                best_cls = "undecided"
                best_why = "the requirement this brief maps to is contradicted or vacuous; the document and the build disagree"
            elif any(e in EVIDENCE_OBSERVED for e in req_ev) or any_pass:
                if best_rung >= rung_index(RETIREMENT_RUNG) and cited and not join_is_weak:
                    best_cls = "retirable"
                    best_why = ("observed at rung %r, at or above the %r floor, on a cited join — "
                                "the work this brief asks for appears already done"
                                % (ORACLE_RUNGS[best_rung] if best_rung >= 0 else "?", RETIREMENT_RUNG))
                else:
                    best_cls = "undecided"
                    reason = []
                    if best_rung < rung_index(RETIREMENT_RUNG):
                        reason.append("the strongest oracle behind it is %r, below the %r floor for retiring intent"
                                      % (ORACLE_RUNGS[best_rung] if best_rung >= 0 else "none", RETIREMENT_RUNG))
                    if not cited:
                        reason.append("the join to the registry is a token-overlap guess, not a citation")
                    if join_is_weak:
                        reason.append("the join as a whole is too weak to carry a retirement claim")
                    best_why = "looks done, but " + "; and ".join(reason) + " — route to spec-validation before retiring"
            else:
                best_cls = "unmeasured"
                best_why = "this brief maps to the registry only through self-reported evidence; nothing observed it"

        rows.append({
            "id": b["id"], "entity": "brief", "class": best_cls, "kind": KIND_OF[best_cls],
            "title": b["title"][:200], "file": b["file"], "declared_status": b["status"],
            "generated_by": b["generated_by"],
            "is_work_item": best_cls not in ("verified-done", "waived"),
            "edges": [{"target": e["target"], "method": e["method"], "confidence": e["confidence"]}
                      for e in my_edges],
            "why": best_why,
        })

    return rows


# ---------------------------------------------------------------------------
# Denominators
#
# Reported per axis and never blended, because the axes disagree and a single
# blended figure hides which one is weak. Every figure is a floor: an `unnamed`
# finding is proof that the intent space is larger than the documents describe,
# so the denominator itself is only a lower bound on the real one.
# ---------------------------------------------------------------------------

def denominators(rows, campaign):
    def count(entity, pred):
        items = [r for r in rows if r["entity"] == entity]
        return sum(1 for r in items if pred(r)), len(items)

    adj_cases, tot_cases = count("case", lambda r: r["status"] in ADJUDICATED)
    waived_cases, _ = count("case", lambda r: r["class"] == "waived")
    obs_reqs, tot_reqs = count("requirement", lambda r: r.get("evidence") in EVIDENCE_OBSERVED)
    spoken_surf, tot_surf = count("surface", lambda r: r["class"] == "verified-done")
    joined_briefs, tot_briefs = count("brief", lambda r: bool(r.get("edges")))

    def pct(n, d):
        return round(100.0 * n / d, 1) if d else None

    return {
        "cases_adjudicated": {"n": adj_cases, "of": tot_cases, "pct": pct(adj_cases, tot_cases),
                              "means": "an instrument returned a verdict on the product — pass or fail. "
                                       "A fail is knowledge; this is not a pass rate."},
        "decisions_taken": {"n": waived_cases, "of": tot_cases, "pct": pct(waived_cases, tot_cases),
                            "means": "somebody ruled the cell out of scope or not applicable. A decision, "
                                     "not a measurement, and it is kept out of the line above on purpose."},
        "requirements_observed": {"n": obs_reqs, "of": tot_reqs, "pct": pct(obs_reqs, tot_reqs),
                                  "means": "somebody watched it happen, rather than the project reporting it of itself."},
        "surfaces_spoken_for": {"n": spoken_surf, "of": tot_surf, "pct": pct(spoken_surf, tot_surf),
                                "means": "at least one case on this surface reached a verdict."},
        "briefs_joined": {"n": joined_briefs, "of": tot_briefs, "pct": pct(joined_briefs, tot_briefs),
                          "means": "the brief could be tied to something in the registry at all."},
        "is_floor": True,
        "floor_note": ("Each figure is a lower bound. Every `unnamed` row is a surface the documents "
                       "never described, which means the true denominator is larger than the one the "
                       "documents can supply."),
        "scope": (campaign.get("header") or {}).get("run", {}).get("scope"),
        "sample": (campaign.get("header") or {}).get("sample"),
    }


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def gate(ledger, weak_join_ratio=0.5):
    violations, warnings = [], []
    rows = ledger["rows"]

    seen = Counter(r["id"] for r in rows)
    dupes = [i for i, n in seen.items() if n > 1]
    if dupes:
        violations.append(("conservation", "%d id(s) appear in more than one ledger row: %s"
                           % (len(dupes), ", ".join(sorted(map(str, dupes))[:8]))))

    missing_id = [r for r in rows if not r.get("id")]
    if missing_id:
        violations.append(("conservation", "%d row(s) carry no id, so they cannot be reconciled"
                           % len(missing_id)))

    for r in rows:
        if r["class"] not in CLASSES:
            violations.append(("placement", "%s has class %r, which is not one of the partition"
                               % (r["id"], r["class"])))
        if r["entity"] == "case":
            legal = LEGAL_CLASS.get(r.get("status"), set(CLASSES))
            if r["class"] not in legal:
                violations.append(("placement",
                                   "%s has status %r but class %r — %r may only be %s. This is the "
                                   "silent-done failure: an unmeasured case presenting as settled."
                                   % (r["id"], r["status"], r["class"], r["status"], "/".join(sorted(legal)))))
        if r["entity"] == "requirement":
            if r.get("evidence") in EVIDENCE_SELF_REPORTED and r["class"] in ("verified-done", "retirable"):
                violations.append(("placement",
                                   "%s rests on %r evidence but is classed %r — self-reported evidence "
                                   "cannot retire a requirement" % (r["id"], r.get("evidence"), r["class"])))

    for r in rows:
        if r["class"] == "retirable":
            if not any(e.get("method") == "cited" for e in r.get("edges", [])):
                violations.append(("placement",
                                   "%s is marked retirable on a token-overlap join. Retiring intent on a "
                                   "guess is how stated work disappears." % r["id"]))

    for r in rows:
        if r["class"] == "waived" and not (r.get("note") or r.get("declared_status") or r.get("status")):
            violations.append(("placement",
                               "%s is waived with no recorded reason. A waiver names who decided and "
                               "why, or it is an omission wearing a decision's clothes." % r["id"]))

    ratio = ledger["denominators"]["briefs_joined"]["pct"]
    if ratio is not None and ratio < (100 * (1 - weak_join_ratio)):
        warnings.append("only %.1f%% of briefs could be joined to the registry at all. The join is the "
                        "inferential step in this pipeline; below half, retirement claims are withheld "
                        "and every brief stays in its documentary class." % ratio)

    d = ledger["denominators"]
    for key in ("cases_adjudicated", "decisions_taken", "requirements_observed",
                "surfaces_spoken_for", "briefs_joined"):
        if key not in d:
            violations.append(("disclosure", "denominator %r is absent; a remaining-work list without a "
                                             "denominator reads as though it covered everything" % key))

    counts = Counter(r["class"] for r in rows)
    stated = ledger.get("summary", {}).get("counts")
    if stated and stated != dict(counts):
        violations.append(("disclosure", "the ledger's own summary disagrees with its rows: summary says "
                                         "%r, rows say %r" % (stated, dict(counts))))

    return violations, warnings


def verdict(violations):
    kinds = {k for k, _ in violations}
    if kinds & {"conservation", "placement"}:
        return 1
    if "disclosure" in kinds:
        return 2
    return 0


# ---------------------------------------------------------------------------
# Ratchet
# ---------------------------------------------------------------------------

EVIDENCE_BEARING = ("case-adjudicated", "requirement-observed", "spec-validation", "defect-closed")


def ratchet(prev, cur):
    """An item may leave `unmeasured` only by being measured. Compare two
    ledgers and refuse any transition that has no evidence behind it.

    Snapshot gates catch a bad run. This catches the slow version: an item
    quietly reclassified across runs until nothing remembers it was never
    checked."""
    prev_rows = {r["id"]: r for r in prev["rows"]}
    cur_rows = {r["id"]: r for r in cur["rows"]}
    bad = []

    for rid, prow in prev_rows.items():
        if prow["class"] != "unmeasured":
            continue
        crow = cur_rows.get(rid)
        if crow is None:
            bad.append("%s was unmeasured and is absent from the new ledger entirely — it did not "
                       "become done, it stopped being counted" % rid)
            continue
        if crow["class"] == "unmeasured":
            continue
        if crow["entity"] == "case" and crow.get("status") in ADJUDICATED:
            continue
        if crow["entity"] == "requirement" and crow.get("evidence") in EVIDENCE_OBSERVED:
            continue
        if crow.get("evidence_event") in EVIDENCE_BEARING:
            continue
        bad.append("%s moved from unmeasured to %r with no evidence-bearing event (status %r, evidence %r)"
                   % (rid, crow["class"], crow.get("status"), crow.get("evidence")))
    return bad


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def render(ledger):
    d = ledger["denominators"]
    counts = Counter(r["class"] for r in ledger["rows"])
    L = []
    A = L.append

    A("# Reckoning — %s" % ledger["project"])
    A("")
    A("%s" % ledger["headline"])
    A("")
    A("## What it can speak for")
    A("")
    A("| Axis | Measured | Of | % | What the number means |")
    A("|---|---:|---:|---:|---|")
    for key, label in (("cases_adjudicated", "Cases adjudicated"),
                       ("decisions_taken", "Cases ruled out by decision"),
                       ("requirements_observed", "Requirements observed"),
                       ("surfaces_spoken_for", "Surfaces spoken for"),
                       ("briefs_joined", "Briefs joined to evidence")):
        v = d[key]
        A("| %s | %s | %s | %s | %s |" % (label, v["n"], v["of"],
                                          "—" if v["pct"] is None else "%.1f%%" % v["pct"], v["means"]))
    A("")
    A("_%s_" % d["floor_note"])
    A("")

    A("## What remains")
    A("")
    A("Two counts, because they answer different questions. **Rows** is every entity on both sides, "
      "and it is total by construction — that is what makes the gate meaningful. **Work** is what "
      "somebody would actually schedule: a failing case and the defect it evidences are one job, and "
      "blocked cases are counted as the blockers behind them rather than one by one.")
    A("")
    A("| Class | Work | Rows | Kind | What it is |")
    A("|---|---:|---:|---|---|")
    blurb = {
        "unbuilt": "named in a brief; nothing in the registry answers to it",
        "broken": "measured, and the answer was no",
        "unmeasured": "nobody found out — the work here is becoming able to tell",
        "unnamed": "the campaign found it; no document claims it",
        "undecided": "the documents and the evidence disagree; needs a person",
        "retirable": "already done to a standard that can carry the claim — close it",
        "waived": "somebody decided not to — an exception, and it stays visible",
        "verified-done": "not remaining; kept so the denominator is honest",
    }
    work_counts = Counter(r["class"] for r in ledger["rows"] if r.get("is_work_item"))
    for cls in CLASSES:
        if counts.get(cls):
            w = work_counts.get(cls, 0)
            if cls == "unmeasured" and ledger["blockers"]:
                w = "%d + %d blockers" % (w, len(ledger["blockers"]))
            A("| `%s` | %s | %d | %s | %s |" % (cls, w, counts[cls], KIND_OF[cls], blurb[cls]))
    A("")

    if ledger["blockers"]:
        A("## What unblocks the most")
        A("")
        A("Blocked cases cluster: a handful of causes usually account for most of them. "
          "Resolving these in order returns the most measurement per unit of work.")
        A("")
        A("| Blocker | Cases it unblocks | Coverage returned | Cause |")
        A("|---|---:|---:|---|")
        for b in ledger["blockers"][:10]:
            A("| `%s` | %d | +%.1f pts | %s |" % (b["id"], b["unblocks"], b["coverage_gain_pct"],
                                                  b["summary"][:150].replace("|", "／")))
        A("")

    for cls in ("broken", "unbuilt", "undecided", "unnamed", "retirable"):
        items = [r for r in ledger["rows"] if r["class"] == cls and r.get("is_work_item")]
        if not items:
            continue
        A("## %s (%d)" % (cls.capitalize(), len(items)))
        A("")
        for r in sorted(items, key=lambda r: str(r.get("severity") or "") + str(r["id"]))[:40]:
            A("- **%s** — %s" % (r["id"], (r.get("title") or "")[:140]))
            A("  - %s" % r["why"])
        if len(items) > 40:
            A("- _…and %d more in ledger.json_" % (len(items) - 40))
        A("")

    waived = [r for r in ledger["rows"] if r["class"] == "waived"]
    if waived:
        A("## Decisions on the record (%d)" % len(waived))
        A("")
        A("Not remaining work, and not done either. Each of these was ruled out by somebody, and the "
          "reason it was ruled out can stop being true — a state that had no hook may get one, an "
          "account that could not be reached may become reachable. They stay on the ledger so that "
          "when the reason expires, the item is still there.")
        A("")
        for r in waived[:25]:
            A("- **%s** — %s" % (r["id"], (r.get("title") or "")[:120]))
            A("  - %s" % ((r.get("note") or r.get("why") or "")[:220]))
        A("")

    reqs = [r for r in ledger["rows"] if r["entity"] == "requirement" and r["class"] == "unmeasured"]
    if reqs:
        A("## Requirements standing on the project's own word (%d)" % len(reqs))
        A("")
        A("These are not failures. Each is a claim the project makes about itself that nothing "
          "independent has confirmed, which is a different thing from a claim that has been checked "
          "and held.")
        A("")
        for r in reqs[:25]:
            A("- **%s** (`%s`) — %s" % (r["id"], r.get("evidence"), (r.get("title") or "")[:140]))
            if r.get("remedy"):
                A("  - %s" % r["remedy"])
        A("")

    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_build(args):
    campaign = read_campaign(args.campaign)
    briefs = read_briefs(args.briefs)

    edges = build_join(briefs, campaign, threshold=args.join_threshold)
    joined = {e["brief"] for e in edges}
    join_pct = (100.0 * len(joined) / len(briefs)) if briefs else 100.0
    join_is_weak = join_pct < 50.0

    rows = classify(briefs, campaign, edges, join_is_weak)
    dens = denominators(rows, campaign)
    counts = Counter(r["class"] for r in rows)

    total_cases = sum(1 for r in rows if r["entity"] == "case")
    blockers = cluster_blockers([r for r in rows if r["class"] == "unmeasured"], total_cases,
                                threshold=args.blocker_threshold)

    # Two different counts, and conflating them is what makes a remaining-work
    # list untrustworthy. Every row is accounted for — that is the gate's job.
    # But a failing case and the defect it evidences are one piece of work, and
    # twenty blocked cases behind one dead credential are one piece of work
    # too. What a person schedules is the second number.
    work = [r for r in rows if r.get("is_work_item")]
    work_counts = Counter(r["class"] for r in work)
    kind_counts = Counter(r["kind"] for r in work)
    kind_counts["evidence-work"] += len(blockers)
    work_total = len(work) + len(blockers)

    adj = dens["cases_adjudicated"]
    headline = (
        "%d piece(s) of work remain — %d product, %d evidence, %d decision — across %d ledger rows. "
        "This reckoning speaks for %s of the campaign's designed cases and %s of its stated "
        "requirements; the rest is not known to be done, it is simply not known."
        % (work_total, kind_counts.get("product-work", 0), kind_counts.get("evidence-work", 0),
           kind_counts.get("decision-work", 0), len(rows),
           "—" if adj["pct"] is None else "%.0f%%" % adj["pct"],
           "—" if dens["requirements_observed"]["pct"] is None
           else "%.0f%%" % dens["requirements_observed"]["pct"]))

    ledger = {
        "tool": "reckon", "version": 1,
        "project": (campaign["header"] or {}).get("project") or os.path.basename(os.path.abspath(args.briefs or ".")),
        "campaign_present": campaign["present"],
        "campaign_dir": args.campaign,
        "briefs_dir": args.briefs,
        "headline": headline,
        "summary": {"counts": dict(counts), "work_items": work_total,
                    "work_by_class": dict(work_counts), "work_by_kind": dict(kind_counts),
                    "rows": len(rows)},
        "denominators": dens,
        "join": {"edges": edges, "briefs_joined": len(joined), "briefs_total": len(briefs),
                 "pct": round(join_pct, 1), "weak": join_is_weak,
                 "note": "cited edges are citations somebody wrote; overlap edges are guesses and cannot retire a brief"},
        "blockers": blockers,
        "rows": rows,
    }

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "ledger.json"), "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(args.out, "reckoning.md"), "w", encoding="utf-8") as fh:
        fh.write(render(ledger))

    v, w = gate(ledger, weak_join_ratio=args.weak_join)
    for kind, msg in v:
        print("VIOLATION [%s] %s" % (kind, msg), file=sys.stderr)
    for msg in w:
        print("warning: %s" % msg, file=sys.stderr)
    print("%s · %d rows · %s" % (ledger["project"], len(rows), headline))
    print("wrote %s" % os.path.join(args.out, "ledger.json"))
    return verdict(v)


def cmd_check(args):
    ledger = _load_json(args.ledger)
    if ledger is None:
        print("no ledger at %s" % args.ledger, file=sys.stderr)
        return 1
    v, w = gate(ledger, weak_join_ratio=args.weak_join)
    for kind, msg in v:
        print("VIOLATION [%s] %s" % (kind, msg), file=sys.stderr)
    for msg in w:
        print("warning: %s" % msg, file=sys.stderr)
    counts = Counter(r["class"] for r in ledger["rows"])
    print("%d rows · %s" % (len(ledger["rows"]),
                            " · ".join("%s %d" % (c, counts[c]) for c in CLASSES if counts.get(c))))
    code = verdict(v)
    print("gate: %s" % ("clean" if code == 0 else "FAILED (exit %d)" % code))
    return code


def cmd_ratchet(args):
    prev, cur = _load_json(args.previous), _load_json(args.current)
    if prev is None or cur is None:
        print("need two ledgers", file=sys.stderr)
        return 1
    bad = ratchet(prev, cur)
    for msg in bad:
        print("RATCHET %s" % msg, file=sys.stderr)
    print("ratchet: %s" % ("clean" if not bad else "%d silent transition(s)" % len(bad)))
    return 3 if bad else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="reconcile briefs + campaign into a ledger")
    b.add_argument("--briefs", required=True, help="the feature-brief directory")
    b.add_argument("--campaign", help="a test-campaign run directory")
    b.add_argument("--out", required=True)
    b.add_argument("--join-threshold", type=float, default=0.18)
    b.add_argument("--weak-join", type=float, default=0.5)
    b.add_argument("--blocker-threshold", type=float, default=0.30,
                   help="token overlap at which two blocked cases are treated as one cause")
    b.set_defaults(fn=cmd_build)

    c = sub.add_parser("check", help="gate an existing ledger")
    c.add_argument("ledger")
    c.add_argument("--weak-join", type=float, default=0.5)
    c.set_defaults(fn=cmd_check)

    r = sub.add_parser("ratchet", help="refuse silent transitions out of unmeasured")
    r.add_argument("previous")
    r.add_argument("current")
    r.set_defaults(fn=cmd_ratchet)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
