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
    4  vocabulary violation — an input this tool cannot classify, reported as a
       finding that names the input and how many rows carried it. It is not
       resolved by a default in either direction: over-reporting announces
       itself and gets looked at, while under-reporting prints a clean count
       over a quietly smaller population and nothing about it asks to be
       checked.
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
WAIVED_DECLARED = ("waived", "deferred", "wontfix", "won't fix", "declined", "out of scope", "retired", "completed", "consumed", "scaffolded", "historical")

# A case status that means no verdict was reached. Each has a different remedy
# — blocked needs access, inconclusive needs a better instrument, unoracled
# needs an oracle, unselected needs re-running — but they share a class,
# because to a reader of a remaining-work list they are the same thing: an
# answer nobody has.
UNMEASURED_STATUS = ("blocked", "inconclusive", "unoracled", "unselected", "open")

# Defect statuses. A defect row records its own repair, and reading that record
# is the difference between "110 things are broken here" and "10 are". A case
# whose status is `pass` already retires with no further corroboration; a
# defect whose status is `fixed` is the same registry speaking about the same
# run, so it is read the same way.
#
# These four tuples are a partition over the words this tool has a rule for, and
# a word outside all four is NOT resolved by a default. It lands `broken`,
# because guessing done is the error here that cannot be recovered from, AND it
# is reported as a finding naming the word and its row count, because the
# fail-closed placement is a decision this tool took rather than a reading of
# the registry. Measured in a sibling project: a register holding `fixed 55,
# open 11, partially-fixed 3, characterised 2, resolved 1, not-a-defect 1,
# inconclusive 1, vacuous 1` put six rows in `broken` against an adjudicated
# true queue of nine, and fifteen where nine is the truth reads as a backlog
# rather than as a bug.
DEFECT_FIXED = ("fixed", "resolved", "closed", "done", "verified", "answered")

# Qualifiers that survive a fix verb and negate it. A defect recorded
# `answered · F191 · not re-measured` is a repair CLAIM, not a repair: somebody
# wired a feature to it and nobody looked again. Seven project transcripts
# proposed folding `answered` straight into the fixed set, which would have
# retired exactly the defects nobody re-measured — the failure this tool exists
# to prevent, arriving through its own vocabulary.
#
# Same shape as the closure matcher's negation guard: a bare substring over a fix
# verb once read "Not repaired here" as repaired.
FIX_UNMEASURED_QUALIFIERS = ("not re-measured", "not remeasured", "unverified",
                             "not verified", "not re-tested", "not retested",
                             "unconfirmed", "not confirmed")


def defect_status_parts(raw: str) -> tuple[str, str]:
    """Split a compound defect status into its leading verb and the whole string.

    Registries write `answered · F191 · not re-measured`, `resolved · v2.3`, and
    plain `fixed`. Exact-equality matching sees none of the first two, so a
    genuinely repaired defect arrived `unclassified` and a genuinely unmeasured
    one did too — indistinguishable, and both landing wherever the default sent
    them.
    """
    low = (raw or "").strip().lower()
    lead = re.split(r"\s*[·|,;]\s*", low)[0].strip() if low else ""
    return lead, low
DEFECT_OPEN = ("open", "new", "confirmed", "reopened", "regressed", "in progress", "recorded", "standing")
DEFECT_WAIVED = ("wontfix", "won't fix", "will not fix", "deferred", "declined",
                 "duplicate", "n/a", "not a bug")

# Words that mean the row owes nothing without meaning anybody repaired it: a
# ruling about whether the defect was ever a defect, or is still one. They class
# `waived` rather than `verified-done` — not remaining work, and not done
# either, kept visible because the reason for the ruling can stop being true. A
# `cannot reproduce` is the clearest case: it is one reproduction away from
# being work again.
DEFECT_NOT_OWING = ("by design", "by-design", "invalid", "obsolete", "superseded",
                    "cannot reproduce", "cannot-reproduce", "not-a-defect",
                    "not a defect", "vacuous")

# `partially-fixed` is deliberately NOT in the set above, and this is the one
# place in this file where the fail-closed direction is chosen against a word
# that sounds like a closure. A half still broken owes a reproduction for that
# half; in the sibling register measured above, none of the three
# partially-fixed rows had one. Retiring it would make this tool under-report
# for the first time.
DEFECT_PARTIAL = ("partially-fixed", "partially fixed", "part-fixed")

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

# The plane the evidence came from, weakest first. test-campaign records this per
# case; reckon reads it to decide whether a brief's intent has actually been met.
#
# Measured across seven projects in one week, each reporting its backlog
# implemented and verified: every one had retired stated intent on evidence from a
# weaker plane than the intent lived on. An API compiler suite standing for a
# desktop app. A mock Drive peer standing for live sync. Unit tests standing for
# buttons that ran empty closures. In each case the case was honest and the
# retirement was not.
EVIDENCE_PLANES = ("in-tree", "hermetic", "live-glass", "live-external")
PLANE_RANK = {p: i for i, p in enumerate(EVIDENCE_PLANES)}

# What a brief's own words say its intent spans. A brief naming a shipped
# application, a device, a user's account or a live service is not satisfied by a
# double, however green. Deliberately generous on the trigger and conservative on
# the consequence: a match holds the brief open rather than closing it, so a false
# positive costs a re-read and a false negative costs the failure above.
OUTER_INTENT = (
    "on device", "on-device", "physical", "hardware", "real account",
    "live service", "production", "end to end", "end-to-end", "on glass",
    "on-glass", "desktop app", "native app", "menu bar", "finder",
    "live sync", "real api", "third-party", "third party",
)
EVIDENCE_SELF_REPORTED = ("reported", "unknown", "built-unwatched")
EVIDENCE_DISPUTED = ("contradicted", "vacuous")
EVIDENCE_CIRCULAR = ("source",)

# The three registry vocabularies this tool reads, each closed. Every word a
# registry can put in these fields is either in one of these sets — in which
# case the class it supports is written down — or it is a finding. There is no
# third outcome and no default: `unclassified_inputs` names the word and counts
# the rows, and the gate refuses on it.
#
# `EVIDENCE_VOCABULARY` is test-campaign's own `REQ_EVIDENCE` — observed,
# reported, contradicted, unknown, vacuous — reached through the three tuples
# above rather than re-spelled, so the two cannot drift apart silently. A
# registry writing a sixth word is writing one its own schema rejects, and this
# repository has one: REQ-072 carries `inconclusive`, which took the
# self-reported branch and was explained to the reader as "the project's own
# account of itself" when it is a stated ceiling.
CASE_VOCABULARY = ADJUDICATED + WAIVED_STATUS + UNMEASURED_STATUS
DEFECT_VOCABULARY = (DEFECT_FIXED + DEFECT_OPEN + DEFECT_WAIVED + DEFECT_NOT_OWING
                     + DEFECT_PARTIAL)
EVIDENCE_VOCABULARY = EVIDENCE_OBSERVED + EVIDENCE_SELF_REPORTED + EVIDENCE_DISPUTED + EVIDENCE_CIRCULAR

# The classes. Every entity lands in exactly one.
CLASSES = (
    "unbuilt",       # named, and nothing in the registry answers to it
    "unjoined",      # named, and the join could not reach the registry at all
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
    "unjoined": "decision-work",
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

# The same gate for defects. A defect is the one entity that carries its own
# repair, so its status may only ever produce the class that status supports.
DEFECT_LEGAL_CLASS = {}
for _st in DEFECT_FIXED:
    DEFECT_LEGAL_CLASS[_st] = {"verified-done"}
for _st in DEFECT_OPEN:
    DEFECT_LEGAL_CLASS[_st] = {"broken"}
for _st in DEFECT_WAIVED:
    DEFECT_LEGAL_CLASS[_st] = {"waived"}
for _st in DEFECT_NOT_OWING:
    DEFECT_LEGAL_CLASS[_st] = {"waived"}
for _st in DEFECT_PARTIAL:
    DEFECT_LEGAL_CLASS[_st] = {"broken"}

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
    "source": "obtain independent evidence — citing the source declaration is circular, not an observation",
}

# `unjoined` is a class rather than a status, so its remedy sits apart from the
# table above rather than mixing two vocabularies in one dict.
UNJOINED_REMEDY = ("read the brief against the registry and rule — the join is a guess and it "
                   "returned nothing, so nothing here is a finding about the product yet")

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

    for root, dirs, files in os.walk(briefs_dir):
        dirs.sort()
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            if name in ignore or name.upper().startswith(("BRIEF-TEMPLATE", "README", "00-INDEX", "LEDGER")):
                continue
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, briefs_dir)
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
                raw = meta.get("reckon-sources") or meta.get("sources") or meta.get("source") or ""
                source_ids = [s.strip() for s in raw.strip("[]").split(",") if s.strip()]
                body = body[m.end():]

            title = ""
            for line in body.splitlines():
                if line.startswith("#"):
                    title = line.lstrip("#").strip()
                    break

            status = (meta.get("status") or "").lower()
            rel_parts = [p.lower() for p in rel_path.split(os.sep)[:-1]]
            if not status and ("consumed" in rel_parts or "archive" in rel_parts or "archived" in rel_parts):
                status = "consumed"

            slug = os.path.splitext(name)[0]
            briefs.append({
                "id": "BRIEF-" + slug,
                "file": rel_path if rel_path != name else name,
                "path": path,
                "title": title or slug.replace("-", " "),
                "text": body,
                "status": status,
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

# A fenced block, an HTML comment and a struck-through span are the three places
# a markdown document SHOWS a token rather than uses one. A scanner that reads a
# whole document for an id cannot tell a citation from a mention of one, and the
# mention wins at confidence 1.0 — a brief whose only id-shaped token was
# `CASE-9999` inside an example command was classed `unbuilt` and product-work,
# on the reasoning that the registry holds none of the ids it cites.
#
# Excluding them is not the whole repair. An id-shaped token this scanner cannot
# place is a third outcome rather than a quiet drop: `scan_ids` returns it under
# `unclassifiable`, `classify` refuses to let it carry `unbuilt`, and the gate
# names it with its count.
#
# Zero briefs in the repository this was written against use a fenced id, and
# that is a fact about one repository's idiom rather than about the risk. A
# repository whose convention is *the brief names the defects it closes* has the
# opposite prior, and one does: there a brief discussing a neighbouring defect is
# textually identical to one that owns it.
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?(?:^\1?\2[^\n]*\n|\Z)", re.M | re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
STRIKETHROUGH_RE = re.compile(r"~~[^\n]+?~~")

# An id of three or more digits, all 9 or all 0, is the shape every worked example
# uses. It is not treated as "not a citation" — that would be the same guess in
# the other direction — but as an id this tool cannot place, which is a finding.
#
# Three digits rather than one, because `9+` also matches `REQ-9`: an
# out-of-family review of this change pointed out that a repository numbering its
# queue without padding has a real ninth item, and it would have been read as a
# worked example. A repository large enough to hold a real `CASE-999` still gets
# a finding rather than a lost citation, which is the direction this whole
# mechanism is built to fail in.
PLACEHOLDER_ID_RE = re.compile(r"\A(?:REQ|CASE|DEF|SURF|FLOW|COMP)-(?:9{3,}|0{3,})\Z")

EXCLUSION_KINDS = (("fenced", FENCE_RE), ("comment", HTML_COMMENT_RE),
                   ("struck", STRIKETHROUGH_RE))


def _blank(text):
    """Replace every character except newlines, so offsets and line counts hold."""
    return re.sub(r"[^\n]", " ", text)


def citable_text(text):
    """(text with the three shown-not-used regions blanked, {kind: [ids in it]}).

    Blanked rather than deleted: a fence removed outright joins the line above it
    to the line below, and a `**Brief:**`-style line anchored to a line start
    would then match text that was never at one.
    """
    shown, out = {}, text or ""
    for kind, rx in EXCLUSION_KINDS:
        found = []

        def take(m, _found=found):
            _found.extend(ID_RE.findall(m.group(0)))
            return _blank(m.group(0))

        out = rx.sub(take, out)
        if found:
            shown[kind] = sorted(set(found))
    return out, shown


def scan_ids(text):
    """Every id-shaped token in a document, each placed in exactly one class.

    `cited`          — used in prose: a citation somebody wrote on purpose
    `shown`          — inside a fence, an HTML comment or a struck-through span,
                       per kind, so a fixture can prove one exclusion at a time
    `shown_only`     — shown somewhere and used nowhere: explicitly not a citation
    `unclassifiable` — placeholder-shaped and in prose: this tool cannot tell
                       whether it is a citation, and says so rather than guessing
    """
    body, shown = citable_text(text)
    found = set(ID_RE.findall(body))
    unclassifiable = sorted(i for i in found if PLACEHOLDER_ID_RE.match(i))
    shown_all = {i for ids in shown.values() for i in ids}
    return {"cited": sorted(found - set(unclassifiable)),
            "shown": shown, "shown_only": sorted(shown_all - found),
            "unclassifiable": unclassifiable}


def brief_scan(brief):
    """`scan_ids` for one brief, computed once and cached on the brief itself.

    Read through a helper rather than required as a key, so a caller that builds
    a brief dict by hand — every fixture in `selftest.py` does — keeps working.
    """
    scan = brief.get("id_scan")
    if scan is None:
        scan = scan_ids(brief.get("text") or "")
        brief["id_scan"] = scan
    return scan


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


PROJECT_ID_RE = re.compile(r"\A([A-Za-z]{2,}-\d{2,})\b")


def project_id_in(filename):
    """The project id a brief filename opens with, or None.

    The reverse-citation scan exists for `SCR-0075-dead-credential.md`, where a
    registry note reading "DEF-0015 / SCR-0075" is a link somebody wrote on
    purpose. Taking the first two hyphen-separated fields instead turns
    `03-menu-bar-key-equivalents.md` into the token `03-menu` — a position in a
    directory listing, matched against free prose, and then labelled a citation
    at confidence 1.0. A guess that can carry a retirement is worse than no
    edge at all, so the token has to look like an id: letters, then digits.

    Measured on the campaign this was written against, the scan contributed 0
    of 92 cited edges, so requiring the shape costs nothing there."""
    m = PROJECT_ID_RE.match(os.path.splitext(os.path.basename(filename or ""))[0])
    return m.group(1) if m else None


def registry_tokens(campaign):
    """(id, kind, tokens) for every registry entity a brief could match.

    Shared by the join and by the near-miss report, so the candidate a reader
    is shown for an unjoined brief is the same candidate the join considered
    and rejected, rather than a second opinion computed a different way."""
    registry = []
    for r in campaign["requirements"]:
        registry.append((r.get("id"), "requirement", tokens(r.get("text", "")) | tokens(r.get("note", ""))))
    for d in campaign["defects"]:
        registry.append((d.get("id"), "defect", tokens(d.get("title", "")) | tokens(d.get("evidence", ""))))
    for s in campaign["surfaces"]:
        registry.append((s.get("id"), "surface", tokens(s.get("title", "")) | tokens(s.get("slug", ""))))
    return registry


def build_join(briefs, campaign, threshold=0.18):
    """Return edges brief→registry-id, each with a method and a confidence.

    Two mechanisms, and they are not equal. An explicit id written into a
    brief or a registry note is a citation somebody made on purpose; token
    overlap is a guess. They are labelled differently so a reader can discount
    the second, and so the gate can refuse to retire a brief on a guess."""
    edges = []
    registry = registry_tokens(campaign)

    # Registry notes frequently cite a brief by its own project id (SCR-0075).
    # Harvest those first: they are the strongest edges available.
    reverse_cites = defaultdict(set)
    for coll, kind in (("requirements", "requirement"), ("defects", "defect"), ("cases", "case")):
        for item in campaign[coll]:
            blob = " ".join(str(item.get(k, "")) for k in ("note", "title", "text", "evidence", "status", "source"))
            for brief in briefs:
                token = project_id_in(brief["file"])
                brief_file_base = os.path.splitext(brief["file"])[0]
                matched = False
                if token and item.get("id") and re.search(r"\b" + re.escape(token) + r"\b", blob, re.I):
                    matched = True
                elif item.get("id") and item.get("source") and (
                    brief["file"] in str(item["source"])
                    or brief_file_base in str(item["source"])
                    or brief["id"] in str(item["source"])
                ):
                    matched = True
                if matched:
                    reverse_cites[brief["id"]].add(item["id"])

    for brief in briefs:
        btok = tokens(brief["title"]) | tokens(brief["text"][:4000])
        scan = brief_scan(brief)
        cited = set(scan["cited"]) | set(brief["source_ids"]) | reverse_cites.get(brief["id"], set())
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
            "total_cases": total_cases,
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
        known = st in CASE_VOCABULARY
        rows.append({
            "id": c.get("id"), "entity": "case", "class": cls, "kind": KIND_OF[cls],
            "title": "%s · %s" % (c.get("surface", "?"), c.get("state", "?")),
            "status": st, "oracle": c.get("oracle"), "armed": c.get("armed"),
            "note": c.get("status") if ":" in str(c.get("status", "")) else c.get("note"),
            "surface": c.get("surface"), "lane": c.get("lane"),
            "is_work_item": False,
            "remedy": REMEDY.get(st) if cls == "unmeasured" else None,
            "rolls_up_to": cited_defects or None,
            "why": ("a measurement, not a task: status %r may only be %s. It rolls up to %s."
                    % (st, "/".join(sorted(LEGAL_CLASS.get(st, {cls}))),
                       ", ".join(cited_defects) if cited_defects
                       else ("a blocker cluster" if cls == "unmeasured" else "its surface"))
                   if known else
                   ("status %r is not a word this tool classifies, so this case is held "
                    "`unmeasured` — the class an unread answer takes — and the word is reported "
                    "as a finding with its row count rather than resolved by that default." % st)),
        })
        if c.get("surface"):
            case_by_surface[c["surface"]].append((st, c.get("oracle")))

    # --- requirements ------------------------------------------------------
    #
    # What backs each requirement, computed from the cases rather than from the
    # requirement's own account of itself. `evidence` is a word in a registry a
    # person can edit; `backed_by` is the set of cases that cite this id and
    # reached a verdict. The ratchet needs the second, because a requirement can
    # be moved from `unmeasured` to `observed` by typing, and one campaign moved
    # eight of them in a single session with no case having run in between.
    backing: dict[str, list[str]] = defaultdict(list)
    for c in campaign["cases"]:
        if state_of(c.get("status")) != "pass":
            continue
        cited = c.get("req")
        for rid in ([cited] if isinstance(cited, str) else (cited or [])):
            if rid:
                backing[rid].append(c.get("id"))

    for r in campaign["requirements"]:
        ev = (r.get("evidence") or "unknown").lower()
        if ev in EVIDENCE_DISPUTED:
            cls = "undecided"
            why = "requirement evidence %r is a disagreement between the documents and the build; a person rules on it, an instrument cannot" % ev
        elif ev in EVIDENCE_CIRCULAR:
            cls = "unmeasured"
            why = "requirement evidence %r is circular: citing the source declaration restates intent rather than measuring execution" % ev
        elif ev in EVIDENCE_OBSERVED:
            planes = [p for p in (r.get("planes") or []) if p in EVIDENCE_PLANES]
            reached = [p for p in (r.get("planesReached") or []) if p in EVIDENCE_PLANES]
            short = [p for p in planes if p not in reached]
            if short:
                cls = "undecided"
                why = ("requirement is recorded observed, but its stated intent spans %s and "
                       "no passing case reached %s. Evidence from one plane does not retire "
                       "intent on another." % (", ".join(planes), ", ".join(short)))
            else:
                cls = "verified-done"
                why = "requirement observed"
        elif ev in EVIDENCE_SELF_REPORTED:
            cls = "unmeasured"
            why = "requirement evidence %r is the project's own account of itself, not an observation" % ev
        else:
            # Reaching this branch used to tell the reader the row was a
            # self-report, which is a claim about a word this tool had never
            # heard of. REQ-072 here carries `inconclusive` — a stated ceiling,
            # recorded deliberately — and was explained to every reader as the
            # project talking about itself.
            cls = "unmeasured"
            why = ("requirement evidence %r is not a word this tool classifies, and not one "
                   "test-campaign's own schema permits either. It stays unmeasured because an "
                   "unreadable claim is not an observation, and the word is reported as a finding "
                   "with its row count rather than resolved by that default." % ev)
        rows.append({
            "id": r.get("id"), "entity": "requirement", "class": cls, "kind": KIND_OF[cls],
            "title": (r.get("text") or "")[:200], "evidence": ev,
            "note": r.get("note"), "provider": r.get("provider"),
            "backed_by": sorted(backing.get(r.get("id"), [])) or None,
            "remedy": REMEDY.get(ev) if cls == "unmeasured" else None,
            "is_work_item": cls not in ("verified-done", "waived"), "why": why,
        })

    # --- defects -----------------------------------------------------------
    #
    # A defect is the one entity that carries its own repair. Classing every
    # row `broken` without reading `status` is how a campaign that had fixed
    # 100 of its 110 defects reported all 110 as remaining product work — an
    # entity absent from the failing set treated as an entity that failed,
    # which is this tool's own target failure arriving from the other side.
    defect_class = {}
    for d in campaign["defects"]:
        st = state_of(d.get("status")) if d.get("status") else ""
        st = st.lower()
        lead, whole = defect_status_parts(st)
        # A fix verb carrying a negated-measurement qualifier is a claim about a
        # repair, not a repair. It goes to `unmeasured`, which is the class whose
        # remedy is "go and look".
        claimed_unmeasured = (lead in DEFECT_FIXED
                              and any(q in whole for q in FIX_UNMEASURED_QUALIFIERS))
        if lead in DEFECT_FIXED or lead in DEFECT_OPEN:
            st = lead if not claimed_unmeasured else st
        if claimed_unmeasured:
            cls = "unmeasured"
            why = ("the registry records this defect as %r — a repair claimed and not "
                   "re-measured. A fix nobody looked at again is a claim, so this needs an "
                   "observation rather than a closure." % st)
        elif st in DEFECT_FIXED:
            cls = "verified-done"
            why = ("the registry records this defect as %r. That is the same registry, speaking "
                   "about the same run, as the `pass` that retires a case." % st)
        elif st in DEFECT_PARTIAL:
            cls = "broken"
            why = ("the registry records this defect as %r, which stays in the owing set. A half "
                   "still broken owes a reproduction for that half, and retiring it here would "
                   "make this tool under-report for the first time." % st)
        elif st in DEFECT_NOT_OWING:
            cls = "waived"
            why = ("the registry records this defect as %r — a ruling that the row owes nothing, "
                   "rather than a record of anybody repairing it. It stays on the ledger because "
                   "the ruling can stop being true." % st)
        elif st in DEFECT_WAIVED:
            cls = "waived"
            why = ("the registry records this defect as %r — a decision, not a measurement. It "
                   "stays on the ledger because the reason for it may stop being true." % st)
        elif st in DEFECT_OPEN:
            cls = "broken"
            why = ("a defect is a measured negative result — the unit of product work behind every "
                   "failing case that cites it")
        else:
            cls = "broken"
            why = (("this defect's status is %r, which is not a word this tool classifies. It "
                    "stays broken because guessing done is the one error here that cannot be "
                    "recovered from, and the word is reported as a finding with its row count "
                    "because that placement is this tool's decision rather than the registry's."
                    % st) if st else
                   "this defect row carries no status, so it stays broken — a repair nobody "
                   "recorded is not a repair this tool can read")
        defect_class[d.get("id")] = cls
        rows.append({
            "id": d.get("id"), "entity": "defect", "class": cls, "kind": KIND_OF[cls],
            "title": (d.get("title") or "")[:200], "severity": d.get("severity"),
            "status": st or None,
            "surface": d.get("surface"), "note": (d.get("evidence") or d.get("note") or d.get("fix") or "")[:400],
            "is_work_item": cls == "broken",
            "why": why,
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
    #
    # Three outcomes where there used to be one, because "the registry answered
    # and said no" and "the join reached nothing" are opposite conclusions
    # about the same brief. 75 of 91 briefs landed in `unbuilt` on a 17.6%
    # join, and every one of them named an item that had shipped.
    #
    #   resolvable support   -> classed on the evidence, as before
    #   cited ids the registry does not hold -> `unbuilt`. Somebody wrote down
    #                                           what should exist and it is not
    #                                           there: evidence of absence, and
    #                                           the only thing that keeps
    #                                           `unbuilt` a live predicate.
    #   nothing at all       -> `unjoined`. Decision work: a person reads it.
    known_ids = {x.get("id") for coll in ("requirements", "defects", "surfaces", "cases",
                                          "flows", "components")
                 for x in campaign.get(coll, []) if x.get("id")}
    near_registry = None

    for b in briefs:
        my_edges = edges_by_brief.get(b["id"], [])
        scan = brief_scan(b)
        cited = [e for e in my_edges if e["method"] == "cited"]
        # Prefer the citations, but do not let a dangling one discard a usable
        # overlap edge: what matters is support that actually reaches a row.
        support = ([e for e in cited if e["target"] in known_ids]
                   or [e for e in my_edges if e["target"] in known_ids])
        near_misses = None

        best_cls, best_why = "unjoined", (
            "the join could not tie this brief to anything in the registry. That is not evidence "
            "that it was never built — it is the inferential step of this pipeline returning "
            "nothing, and a person has to read the brief and rule"
            if campaign.get("present") else
            "there is no registry in this run, so nothing could have answered to this brief. "
            "`unbuilt` would be a claim that the registry was asked; it was not")
        if b["status"] in WAIVED_DECLARED:
            best_cls = "waived"
            best_why = ("the brief declares status %r — a decision, not a measurement. It stays on the "
                        "ledger because the reason for it may stop being true." % b["status"])
        elif support:
            targets = {e["target"] for e in support}
            req_ev = [(r.get("evidence") or "unknown").lower()
                      for r in campaign["requirements"] if r.get("id") in targets]
            # Only a defect that is still broken makes the brief broken. Once a
            # repaired defect stops being a measured negative, a brief joined
            # to it must stop being one too, or the fault moves one hop out and
            # reports the same repaired work as remaining.
            hit_defect = any(defect_class.get(t) == "broken" for t in targets if t.startswith("DEF-"))
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
        elif cited and campaign.get("present"):
            best_cls = "unbuilt"
            best_why = ("this brief cites %s, and the registry holds none of them. A citation is a "
                        "link somebody wrote on purpose, so its target being absent is evidence of "
                        "absence rather than a join that missed"
                        % ", ".join(sorted({e["target"] for e in cited})[:6]))
        else:
            # An unjoined row that says only "I could not tell" sends its
            # reader to grep. The join already scored every candidate and threw
            # the best one away below threshold; hand it over instead.
            if near_registry is None:
                near_registry = registry_tokens(campaign)
            btok = tokens(b["title"]) | tokens(b["text"][:4000])
            scored = sorted(((jaccard(btok, rtok), rid, kind) for rid, kind, rtok in near_registry
                             if rid), reverse=True)
            near_misses = [{"target": rid, "kind": kind, "score": round(sc, 3)}
                           for sc, rid, kind in scored[:3] if sc > 0]
            # An id-shaped token this scan refused to read as a citation is the
            # difference between "the join found nothing" and "the join was
            # handed something it could not place". Both land `unjoined`; only
            # one of them tells the reader where to look.
            placed = []
            if scan["unclassifiable"]:
                placed.append("%d placeholder-shaped id(s) in prose (%s) — this tool cannot tell a "
                              "citation from a worked example, so neither reading was taken"
                              % (len(scan["unclassifiable"]), ", ".join(scan["unclassifiable"])))
            for kind, ids in sorted(scan["shown"].items()):
                only = [i for i in ids if i in scan["shown_only"]]
                if only:
                    placed.append("%d id(s) shown in a %s region and used nowhere (%s)"
                                  % (len(only), kind, ", ".join(only)))
            if placed:
                best_why += ". It was handed " + "; and ".join(placed)

        rows.append({
            "id": b["id"], "entity": "brief", "class": best_cls, "kind": KIND_OF[best_cls],
            "title": b["title"][:200], "file": b["file"], "declared_status": b["status"],
            "generated_by": b["generated_by"],
            "is_work_item": best_cls not in ("verified-done", "waived"),
            "edges": [{"target": e["target"], "method": e["method"], "confidence": e["confidence"]}
                      for e in my_edges],
            "near_misses": near_misses,
            "id_scan": {"cited": scan["cited"], "shown": scan["shown"],
                        "shown_only": scan["shown_only"]},
            "unclassifiable_ids": scan["unclassifiable"] or None,
            "remedy": UNJOINED_REMEDY if best_cls == "unjoined" else None,
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
# Inputs this tool cannot classify
#
# The repair for an unrecognised input is not a longer list. A longer list
# extends the set of inputs the instrument guesses correctly about and leaves it
# guessing, so the next word past the end of the list fails exactly as the last
# one did. What closes it is a third outcome: every input is in a vocabulary
# whose class is written down, or it is a finding that names the input and the
# rows carrying it.
#
# Computed from the ledger's rows rather than recorded at build time, so a
# ledger built by an older copy of this tool is still gated on it, and so the
# check can be armed against a hand-written ledger.
# ---------------------------------------------------------------------------

FIELD_VOCABULARY = (("case", "status", "case status", CASE_VOCABULARY),
                    ("defect", "status", "defect status", DEFECT_VOCABULARY),
                    ("requirement", "evidence", "requirement evidence", EVIDENCE_VOCABULARY))


def unclassified_inputs(rows):
    """[{field, value, count, ids, placed_in}] — one entry per unclassifiable input.

    An absent field is not one of these. A defect row carrying no status at all
    is classified: nothing recorded is not a repair, and the row says so. What is
    reported here is a value that was written down and that no rule covers.
    """
    found = defaultdict(list)
    placed = {}
    for r in rows:
        for entity, key, label, vocabulary in FIELD_VOCABULARY:
            if r.get("entity") != entity:
                continue
            value = (r.get(key) or "")
            value = value.lower() if isinstance(value, str) else value
            # A compound defect status (`answered · F191 · not re-measured`) is
            # classified on its leading verb, so it is a word this tool reads
            # rather than one it could not. Reporting it as unclassified after
            # deliberately classifying it sends a reader looking for a decision
            # that was already made.
            if entity == "defect" and value:
                lead, _ = defect_status_parts(value)
                if lead in vocabulary:
                    continue
            if value and value not in vocabulary:
                found[(label, value)].append(r.get("id"))
                placed[(label, value)] = r.get("class")
        for pid in r.get("unclassifiable_ids") or []:
            found[("id-shaped token", pid)].append(r.get("id"))
            placed[("id-shaped token", pid)] = r.get("class")
    return [{"field": field, "value": value, "count": len(ids),
             "ids": sorted(str(i) for i in ids), "placed_in": placed[(field, value)]}
            for (field, value), ids in sorted(found.items())]


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
        if r["entity"] == "defect":
            # A status this tool does not recognise, or none at all, supports
            # exactly one class: the fail-closed one the classifier assigns it.
            # Leaving it unconstrained would make the gate unable to fire on
            # the very rows whose evidence is weakest.
            legal = DEFECT_LEGAL_CLASS.get((r.get("status") or "").lower(), {"broken"})
            if r["class"] not in legal:
                violations.append(("placement",
                                   "%s has status %r but class %r — %r may only be %s. A defect "
                                   "carries its own repair; classing it against that record is how "
                                   "a repaired defect reads as remaining work, or a live one as done."
                                   % (r["id"], r.get("status"), r["class"], r.get("status"),
                                      "/".join(sorted(legal)))))
        if r["entity"] == "requirement":
            if (r.get("evidence") in EVIDENCE_SELF_REPORTED or r.get("evidence") in EVIDENCE_CIRCULAR) and r["class"] in ("verified-done", "retirable"):
                violations.append(("placement",
                                   "%s rests on %r evidence but is classed %r — circular or self-reported evidence "
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
        joined_n = ledger["denominators"]["briefs_joined"]["n"]
        joined_of = ledger["denominators"]["briefs_joined"]["of"]
        warnings.append("only %d/%d (%.1f%%) of briefs could be joined to the registry at all. The join is the "
                        "inferential step in this pipeline; below half, retirement claims are withheld "
                        "and every brief stays in its documentary class." % (joined_n, joined_of, ratio))

    d = ledger["denominators"]
    for key in ("cases_adjudicated", "decisions_taken", "requirements_observed",
                "surfaces_spoken_for", "briefs_joined"):
        if key not in d:
            violations.append(("disclosure", "denominator %r is absent; a remaining-work list without a "
                                             "denominator reads as though it covered everything" % key))

    for u in unclassified_inputs(rows):
        violations.append((
            "vocabulary",
            "%s %r is not a word this tool classifies — %d row(s) carry it (%s), and each was "
            "placed in %r by this tool's fail-closed default rather than by the registry. Give the "
            "word a rule or correct the rows; a longer list would only move the edge."
            % (u["field"], u["value"], u["count"], ", ".join(u["ids"][:8]), u["placed_in"])))

    counts = Counter(r["class"] for r in rows)
    stated = ledger.get("summary", {}).get("counts")
    if stated and stated != dict(counts):
        violations.append(("disclosure", "the ledger's own summary disagrees with its rows: summary says "
                                         "%r, rows say %r" % (stated, dict(counts))))

    return violations, warnings


def verdict(violations):
    """The most structural failure present decides the code.

    `vocabulary` sits between the two: a ledger whose placements rest on a
    default this tool chose is not unsound in the way a duplicated id is, and it
    is a stronger objection than an absent denominator, because every count in
    the ledger is computed over rows it placed by guessing.
    """
    kinds = {k for k, _ in violations}
    if kinds & {"conservation", "placement"}:
        return 1
    if "vocabulary" in kinds:
        return 4
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
            # `observed` releases a requirement from `unmeasured`, and until now
            # the word alone did it. Measured 24 Aug 2026: a campaign moved eight
            # requirements from unmeasured to observed inside one session, with
            # no case having run in between and the ratchet exiting 0 — the same
            # session in which the join was carried from 6% to 100% by writing
            # citations into 81 briefs. A registry a person edits cannot also be
            # the witness that the edit was earned.
            #
            # `backed_by` is computed from the cases, so it is the one thing on
            # this row the requirement does not say about itself. A ledger built
            # before this field existed carries None rather than an empty list,
            # and is let through: refusing there would fail every first
            # comparison against an older ledger, which is a fact about the
            # ledger's age rather than about the project.
            backed = crow.get("backed_by")
            if backed is None or backed:
                continue
            bad.append("%s moved from unmeasured to observed with no passing case citing it — "
                       "the evidence word changed and nothing else did, which is a re-label "
                       "rather than a measurement" % rid)
            continue
        if crow["entity"] == "surface" and crow["class"] == "verified-done":
            continue
        if crow["entity"] == "brief":
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
        "unjoined": "named in a brief; the join reached nothing, so its state is unknown either way",
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
            tot = b.get("total_cases") or d.get("cases_adjudicated", {}).get("of")
            cov = ("+%d/%d (+%.1f pts)" % (b["unblocks"], tot, b["coverage_gain_pct"])) if tot else ("+%.1f pts" % b["coverage_gain_pct"])
            A("| `%s` | %d | %s | %s |" % (b["id"], b["unblocks"], cov,
                                          b["summary"][:150].replace("|", "／")))
        A("")

    for cls in ("broken", "unbuilt", "unjoined", "undecided", "unnamed", "retirable"):
        items = [r for r in ledger["rows"] if r["class"] == cls and r.get("is_work_item")]
        if not items:
            continue
        A("## %s (%d)" % (cls.capitalize(), len(items)))
        A("")
        for r in sorted(items, key=lambda r: str(r.get("severity") or "") + str(r["id"]))[:40]:
            A("- **%s** — %s" % (r["id"], (r.get("title") or "")[:140]))
            A("  - %s" % r["why"])
            if r.get("near_misses"):
                A("  - nearest the join considered: %s"
                  % ", ".join("%s (%.2f)" % (n["target"], n["score"]) for n in r["near_misses"]))
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

    unclassified = ledger.get("unclassified") or unclassified_inputs(ledger["rows"])
    if unclassified:
        A("## Inputs this reckoning could not classify (%d)" % len(unclassified))
        A("")
        A("Each of these was written into the registry or a brief and no rule here covers it. The "
          "rows were still placed, because the partition has to be total — but they were placed by "
          "this tool's fail-closed default rather than by anything the registry said, so the class "
          "is this tool's opinion and is reported as one. An unrecognised input fails in both "
          "directions and only over-reporting announces itself.")
        A("")
        A("| Input | Value | Rows | Placed in | Which rows |")
        A("|---|---|---:|---|---|")
        for u in unclassified:
            A("| %s | `%s` | %d | `%s` | %s |"
              % (u["field"], u["value"], u["count"], u["placed_in"], ", ".join(u["ids"][:8])))
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
    cases_pct = "—" if adj["pct"] is None else "%d/%d (%.0f%%)" % (adj["n"], adj["of"], adj["pct"])
    reqs_pct = "—" if dens["requirements_observed"]["pct"] is None else "%d/%d (%.0f%%)" % (
        dens["requirements_observed"]["n"], dens["requirements_observed"]["of"], dens["requirements_observed"]["pct"])
    headline = (
        "%d piece(s) of work remain — %d product, %d evidence, %d decision — across %d ledger rows. "
        "This reckoning speaks for %s of the campaign's designed cases and %s of its stated "
        "requirements; the rest is not known to be done, it is simply not known."
        % (work_total, kind_counts.get("product-work", 0), kind_counts.get("evidence-work", 0),
           kind_counts.get("decision-work", 0), len(rows),
           cases_pct, reqs_pct))

    unclassified = unclassified_inputs(rows)
    if unclassified:
        headline += (" %d input(s) could not be classified — %s — and each is named with its row "
                     "count rather than counted as work or as done."
                     % (len(unclassified),
                        "; ".join("%s %r on %d row(s)" % (u["field"], u["value"], u["count"])
                                  for u in unclassified[:4])))

    unjoined = counts.get("unjoined", 0)
    if unjoined:
        headline += (" %d brief(s) could not be tied to the registry at all; they are listed as "
                     "`unjoined` and counted as decision work, rather than assumed unbuilt."
                     % unjoined)

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
        "unclassified": unclassified,
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
