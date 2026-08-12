#!/usr/bin/env python3
"""validate_model.py — check meta/items/questions before a page is built.

    python3 validate_model.py <dir>

Exit 0 clean, 1 on any error. Warnings never block.

Everything checked here is a property of the model, not of taste, and each rule
traces to a row in `references/evidence.md`. The four that matter most, because
each one is a defect the research says ships silently:

  * `stage` is a required enum, and `built` is not `deployed`. All five research
    members converged on this; DORA defines "deployed" from deployment automation
    and never defines "done".
  * a work item blocked on a decision that is not on the page, or a decision that
    releases nothing. The two halves drifting apart is the failure the combined
    page exists to prevent, so it is an error rather than a warning.
  * a pre-selected recommendation on a question that is the reader's taste, cost
    or risk appetite. Defaults carry d = 0.68 and are read as endorsement, so
    pre-selecting one there is answering the question while appearing to ask it.
  * a `plain` line that is not plain. It is the whole report for a reader who has
    never opened the repo, and a line carrying a path or an identifier has
    quietly stopped being one.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ITEM_FIELDS = ["id", "group", "urgency", "plain", "stage", "state", "live", "owner", "from_you", "remaining"]
URGENCIES = {"urgent", "high", "medium", "low"}
OWNERS = {"you", "agent", "someone-else"}
KINDS = {"single", "multi", "text"}

# Built is not deployed, and deployed is not accepted. Keeping these as separate
# states is the one encoding in which "90% done" cannot be expressed.
STAGES = {"not-started", "in-progress", "built", "tested", "deployed", "accepted", "blocked", "unknown"}

# How much a decision actually releases. Without this, a page claims a decision
# "unblocks four items" when three of them stay blocked for other reasons.
EFFECTS = {"fully-releases", "removes-one-blocker", "enables-planning"}

# recommended = one option pre-selected, with its reason.
# none        = nothing pre-selected; the choice is the reader's alone.
# forced      = nothing pre-selected and the page says it cannot be left undecided.
POLICIES = {"recommended", "none", "forced"}

JARGON = [
    (re.compile(r"[\w/]+\.(ts|tsx|js|jsx|py|json|yml|yaml|toml|md|sql|go|rs|swift)\b"), "a file name"),
    (re.compile(r"(?<![`\w])(?:src|lib|app|packages|config|dist)/"), "a directory path"),
    (re.compile(r"(?<![`\w#])[a-z]+[A-Z][a-zA-Z]*(?![\w])"), "a camelCase identifier"),
    (re.compile(r"\b[A-Z][A-Z0-9]{3,}(?:_[A-Z0-9]+)+\b"), "a CONSTANT_NAME"),
]

PLAIN_MAX_WORDS = 40
STRAIGHT_QUOTE = re.compile(r"(?<=\w)'(?=\w)|(?<![=\w])\"(?=\w)|(?<=\w)\"(?![\w=])")
PERCENT_DONE = re.compile(r"\b(\d{1,3})\s?%\s*(?:done|complete)", re.I)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def typography(text, where: str, r: Report) -> None:
    if not isinstance(text, str):
        return
    if STRAIGHT_QUOTE.search(text):
        r.warn(f"{where}: straight quote or apostrophe — use ’ and “ ”")
    if re.search(r"\w\s-\s\w", text):
        r.warn(f"{where}: hyphen used as a dash — use an em dash")
    m = PERCENT_DONE.search(text)
    if m:
        r.err(f"{where}: says {m.group(0)!r} — percent-complete is the carrier for the 90%-done failure; "
              f"say which stage it reached and what is genuinely live instead")


def load(path: pathlib.Path, r: Report):
    if not path.exists():
        r.err(f"{path.name} is missing")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        r.err(f"{path.name} is not valid JSON: {exc}")
        return None


def check_items(items, r: Report) -> set[str]:
    ids: set[str] = set()
    if not isinstance(items, list):
        r.err("items.json must be a list")
        return ids
    if not items:
        r.err("items.json is empty — a status page with no items has nothing to say")
    for i, it in enumerate(items):
        where = f"item[{i}]"
        if not isinstance(it, dict):
            r.err(f"{where} is not an object")
            continue
        iid = it.get("id")
        where = f"item {iid!r}" if iid else where
        for f in ITEM_FIELDS:
            if f not in it or it[f] in (None, ""):
                r.err(f"{where} is missing `{f}`")
        if iid:
            if iid in ids:
                r.err(f"duplicate item id {iid!r}")
            ids.add(iid)
        if it.get("urgency") not in URGENCIES:
            r.err(f"{where} has urgency {it.get('urgency')!r}, expected one of {sorted(URGENCIES)}")
        if it.get("owner") not in OWNERS:
            r.err(f"{where} has owner {it.get('owner')!r}, expected one of {sorted(OWNERS)}")
        if it.get("stage") not in STAGES:
            r.err(f"{where} has stage {it.get('stage')!r}, expected one of {sorted(STAGES)}")

        for f in ("plain", "state", "live", "from_you", "remaining", "title"):
            typography(it.get(f), f"{where}.{f}", r)

        plain = it.get("plain") or ""
        if plain:
            words = len(plain.split())
            if words > PLAIN_MAX_WORDS:
                r.err(f"{where}: `plain` is {words} words — it is a one-line summary, keep it under {PLAIN_MAX_WORDS}")
            for pat, what in JARGON:
                m = pat.search(plain)
                if m:
                    r.err(f"{where}: `plain` contains {what} ({m.group(0)!r}) — the reader has never opened the repo")
                    break

        # A claim about the running system that nothing can back is the failure the
        # `unknown` stage exists to make visible rather than hide.
        if it.get("stage") in {"deployed", "accepted"} and not (it.get("evidence") or "").strip():
            r.err(f"{where} claims stage {it['stage']!r} with no `evidence` — a completion claim needs a locator, "
                  f"or the stage is `unknown`")

        if it.get("owner") == "you" and not it.get("blocked_by"):
            r.warn(f"{where} is the reader's to move but links to no question — they cannot act on it here")
        if isinstance(it.get("live"), str) and it["live"].strip().lower() in {"yes", "no", "n/a", "live", "not live"}:
            r.warn(f"{where}: `live` is a single word — it exists to say what is genuinely true in the running system")
    return ids


def check_questions(questions, item_ids: set[str], r: Report) -> set[str]:
    ids: set[str] = set()
    if not isinstance(questions, list):
        r.err("questions.json must be a list")
        return ids
    for i, q in enumerate(questions):
        where = f"question[{i}]"
        if not isinstance(q, dict):
            r.err(f"{where} is not an object")
            continue
        qid = q.get("id")
        where = f"question {qid!r}" if qid else where
        for f in ("id", "title", "why", "kind"):
            if not q.get(f):
                r.err(f"{where} is missing `{f}`")
        if qid:
            if qid in ids:
                r.err(f"duplicate question id {qid!r}")
            ids.add(qid)

        for f in ("title", "why"):
            typography(q.get(f), f"{where}.{f}", r)

        kind = q.get("kind")
        if kind not in KINDS:
            r.err(f"{where} has kind {kind!r}, expected one of {sorted(KINDS)}")

        policy = q.get("default_policy", "recommended" if kind != "text" else "none")
        if policy not in POLICIES:
            r.err(f"{where} has default_policy {policy!r}, expected one of {sorted(POLICIES)}")

        opts = q.get("options") or []
        if kind in ("single", "multi"):
            if len(opts) < 2:
                r.err(f"{where} has {len(opts)} option(s) — a choice needs at least two")
            if len(opts) > 4:
                r.warn(f"{where} has {len(opts)} options — reading cost climbs past four")
            recs = [o for o in opts if o.get("recommended")]
            if policy in ("none", "forced") and recs:
                r.err(f"{where} has default_policy {policy!r} but marks {len(recs)} option(s) recommended — "
                      f"nothing is pre-selected on a question that is the reader's alone")
            if policy == "recommended":
                if kind == "single" and len(recs) != 1:
                    r.err(f"{where} marks {len(recs)} recommended options — exactly one, or set default_policy")
                if kind == "multi" and not recs:
                    r.err(f"{where} recommends nothing — recommend at least one, or set default_policy")
                for o in recs:
                    if not (o.get("because") or "").strip():
                        r.err(f"{where}: the recommended option has no `because` — 'Recommended' without a reason "
                              f"is a preference, and the reader cannot reject a reason they were not given")
            for j, o in enumerate(opts):
                if not o.get("value") or not o.get("label"):
                    r.err(f"{where} option[{j}] needs both `value` and `label`")
                if not o.get("consequence"):
                    r.err(f"{where} option[{j}] has no `consequence` — the export carries consequences, not labels, "
                          f"so that acting on the answer cannot widen it")
                typography(o.get("label"), f"{where} option[{j}].label", r)
                typography(o.get("consequence"), f"{where} option[{j}].consequence", r)
                if len((o.get("label") or "").split()) > 8:
                    r.warn(f"{where} option[{j}] label is long; it is a label, not a sentence")
            vals = [o.get("value") for o in opts]
            if len(vals) != len(set(vals)):
                r.err(f"{where} has duplicate option values")
        elif kind == "text" and opts:
            r.err(f"{where} is kind `text` but carries options")

        for u in q.get("unblocks") or []:
            if isinstance(u, str):
                r.err(f"{where}: unblocks entries need an `effect` — write "
                      f'{{"item": "{u}", "effect": "fully-releases"}}')
                continue
            if u.get("item") not in item_ids:
                r.err(f"{where} says it unblocks {u.get('item')!r}, which is not an item")
            if u.get("effect") not in EFFECTS:
                r.err(f"{where} unblocks {u.get('item')!r} with effect {u.get('effect')!r}, "
                      f"expected one of {sorted(EFFECTS)}")
        if not (q.get("unblocks") or []) and kind != "text":
            r.warn(f"{where} releases nothing — check it belongs on a page about what is holding the work up")
    return ids


def check_links(items, question_ids: set[str], r: Report, free_text: set[str] | None = None) -> None:
    blocked_refs: set[str] = set()
    for it in items if isinstance(items, list) else []:
        if not isinstance(it, dict):
            continue
        b = it.get("blocked_by")
        if not b:
            continue
        for qid in (b if isinstance(b, list) else [b]):
            blocked_refs.add(qid)
            if qid not in question_ids:
                r.err(f"item {it.get('id')!r} is blocked by {qid!r}, which is not a question on this page")
    for qid in question_ids - blocked_refs - (free_text or set()):
        r.warn(f"question {qid!r} is not named by any item's `blocked_by`")


def check_ordering(questions, r: Report) -> None:
    """Position is an endorsement the reader did not consent to.

    Marking a recommendation with a badge and *also* always putting it first
    stacks the two signals, so a reader cannot tell whether they agreed with the
    reasoning or simply took the top row. Order options by their consequence —
    cheapest-to-costliest, safest-to-riskiest — and let the badge carry the
    endorsement on its own.
    """
    picks = [q for q in questions
             if isinstance(q, dict) and q.get("kind") == "single"
             and q.get("default_policy", "recommended") == "recommended"
             and q.get("options")]
    if len(picks) < 3:
        return
    firsts = sum(1 for q in picks if (q["options"][0] or {}).get("recommended"))
    if firsts == len(picks):
        r.warn(f"the recommended option is first in all {len(picks)} pick-one questions — order options by "
               f"consequence and let the badge do the endorsing, or position and badge stack into one signal")


def check_meta(meta, r: Report) -> None:
    if not isinstance(meta, dict):
        r.err("meta.json must be an object")
        return
    for f in ("slug", "project", "title", "generatedAt", "standfirst", "methods"):
        if not meta.get(f):
            r.err(f"meta is missing `{f}`")
    if not meta.get("completionContract"):
        r.err("meta has no `completionContract` — the page claims what is left before the whole thing is done, "
              "so it has to say what done means before it counts anything against it")
    if not meta.get("unknowns"):
        r.warn("meta lists no `unknowns` — a survey of a real project that could check everything is unusual, "
               "and an empty list reads as a claim rather than an absence")
    typography(meta.get("standfirst"), "meta.standfirst", r)
    typography(meta.get("lead"), "meta.lead", r)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    d = pathlib.Path(sys.argv[1])
    r = Report()

    meta = load(d / "meta.json", r)
    items = load(d / "items.json", r)
    questions = load(d / "questions.json", r)
    if items is None or questions is None or meta is None:
        _emit(r)
        return 1

    check_meta(meta, r)
    item_ids = check_items(items, r)
    q_ids = check_questions(questions, item_ids, r)
    free_text = {q.get("id") for q in questions if isinstance(q, dict) and q.get("kind") == "text"}
    check_links(items, q_ids, r, free_text)
    check_ordering(questions, r)

    _emit(r)
    return 1 if r.errors else 0


def _emit(r: Report) -> None:
    for w in r.warnings:
        print(f"warn  {w}")
    for e in r.errors:
        print(f"ERROR {e}")
    print(f"\n{len(r.errors)} error(s), {len(r.warnings)} warning(s)")


if __name__ == "__main__":
    raise SystemExit(main())
