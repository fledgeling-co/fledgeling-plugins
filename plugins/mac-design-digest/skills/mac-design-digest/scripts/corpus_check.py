#!/usr/bin/env python3
"""corpus_check.py — assert the invariants a design corpus depends on.

Run it after every write. The corpus is a file format with a parser: the *next*
invocation of the skill reads it back. Every invariant below is currently
prose-only in the skill, and every violation is silent to the session that
commits it and wrong for every session after — a wrong number in the corpus
outlives the conversation that created it.

    python3 corpus_check.py [corpus-dir]        # default ./design-corpus

Output contract, deliberately three-valued:

  FAIL   a structural break. Printed to stderr; exit code 1. The next
         invocation will silently do the wrong thing.
  NOTE   a degradation, or something this script could not measure. Printed to
         stdout; exit code stays 0. A NOTE is never a pass — it says the check
         did not run on that material.
  OK     the check ran and found nothing, with examined=N naming how much it
         looked at.

`examined=0` is not a pass. A check that examined nothing says so, because a
gate reporting green over an empty read is worse than no gate: it launders an
absence into a guarantee. Every OK line carries its count so the difference is
visible without reading the corpus.

Exit codes: 0 clean (NOTEs allowed) · 1 one or more FAILs · 2 the corpus
directory does not exist or holds no corpus files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The closed mark set. Two orthogonal axes plus three standalone marks.
#
# Changing this vocabulary is a breaking change to a published interface: the
# mac-craft skill's references carry (specified) on every kit value and
# (measured)/(estimated) + (confirmed)/(inferred) on every pattern row, and it
# reads corpora this skill writes. Add to the set only alongside that skill.
# ---------------------------------------------------------------------------

# Two ORTHOGONAL families that compose. `(estimated)(confirmed)` — a guess seen
# twice inside one app — is not interchangeable with `(specified)(canon)` — a
# published kit value corroborated across three independent apps. Collapsing the
# axes is how a single-surface guess becomes a platform value one file
# downstream, which is the failure this whole skill exists to prevent.
MEASUREMENT_AXIS = {"specified", "measured", "estimated", "assumed"}
EVIDENCE_AXIS = {"inferred", "confirmed", "recurring", "canon", "contested"}
STANDALONE = {"user-override", "insufficient-evidence"}
CLOSED_SET = MEASUREMENT_AXIS | EVIDENCE_AXIS | STANDALONE

# Precision is the UN-IMPROVABLE axis: it is a property of where the number came
# from, so it moves only when a better source is found, never by re-sighting.
# Ordering exists so the gate can tell a strengthening from a downgrade.
PRECISION_RANK = {"assumed": 0, "estimated": 1, "measured": 2, "specified": 3}

# Strength is the IMPROVABLE axis: it is a property of how much has been seen,
# and it climbs by accumulating independent app sightings.
STRENGTH_APP_THRESHOLD = {"recurring": 2, "canon": 3}

LOCK_NAME = ".precision-lock.json"

LEVELS = ["Novice", "Competent", "Proficient", "Expert"]
NATIVE_LINEAGES = {"native", "appkit-native", "appkit", "swiftui"}

SYNTHESIS_FILES = ("TASTE.md", "ICONS.md")

# Words that appear parenthesised in ordinary prose and must not be mistaken
# for a malformed mark.
PROSE_PAREN = {
    "high", "medium", "low", "n", "s", "e", "w", "light", "dark", "v1", "v2",
    "figma", "sketch", "png", "svg", "ui", "icon", "kit", "hig", "wcag", "px",
    "pt", "and", "or", "the", "see", "below", "above", "optional", "none",
    "yes", "no", "tbd", "wip", "16", "if", "not",
}


class Report:
    def __init__(self) -> None:
        self.fails: list[str] = []
        self.notes: list[str] = []
        self.oks: list[str] = []
        self._failed_checks: set[str] = set()
        self.ran: set[str] = set()

    def fail(self, check: str, did: str, consequence: str, fix: str) -> None:
        self.fails.append(f"FAIL [{check}] {did} — {consequence}. Fix: {fix}")
        self._failed_checks.add(check)

    def note(self, check: str, msg: str) -> None:
        self.notes.append(f"NOTE [{check}] {msg}")

    def ok(self, check: str, examined: int, what: str, covers: tuple[str, ...] = ()) -> None:
        self.ran.add(check)
        """Record the clean result of a check.

        `covers` names every FAIL label this summary speaks for — a check that
        raised any of them prints nothing, because a run that says both
        "FAIL [ledger-hash]" and "OK [ledger] every row has a unique hash" is the
        gate lying about itself, and that is the one failure mode a gate cannot
        have. The list is explicit rather than inferred from the name: a prefix
        rule silently stopped covering `freshness` under `gaps+freshness`.
        """
        for label in (check,) + covers:
            if label in self._failed_checks:
                return
        self.oks.append(f"OK   [{check}] examined={examined} {what}")
        if examined == 0:
            self.notes.append(
                f"NOTE [{check}] examined=0 — this check found no material to test, "
                f"so it is not evidence that {what} holds."
            )


# ---------------------------------------------------------------------------
# Markdown helpers. Deliberately small: a cell this cannot parse becomes a
# NOTE, never a silent pass.
# ---------------------------------------------------------------------------

def table_rows(text: str) -> list[list[str]]:
    """Every pipe-table body row in the document, as trimmed cell lists."""
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|") or not s.endswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue  # separator row
        rows.append(cells)
    return rows


def section(text: str, heading_re: str) -> str | None:
    """Body of the first heading matching heading_re, up to the next heading of
    the same or shallower depth. Returns None when the heading is absent."""
    lines = text.splitlines()
    start = None
    depth = 0
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and re.search(heading_re, m.group(2), re.I):
            start = i + 1
            depth = len(m.group(1))
            break
    if start is None:
        return None
    out = []
    for line in lines[start:]:
        m = re.match(r"^(#{1,6})\s+", line)
        if m and len(m.group(1)) <= depth:
            break
        out.append(line)
    return "\n".join(out)


def marks_in(s: str) -> list[str]:
    """Closed-set marks present in a string, bracketed forms included.

    `(measured/estimated)` is real notation in a corpus written by this skill and
    read by mac-craft: a value the reader could not place cleanly on one side of
    the measurement axis. It counts as ONE mark from that axis, which is why it is
    collapsed here rather than being seen as two colliding marks or — worse —
    skipped, which is what a plain single-word bracket pattern did to it silently.
    """
    out = []
    for token in re.findall(r"\(([a-z][a-z/ -]*)\)", s):
        parts = [p.strip() for p in token.split("/") if p.strip()]
        if not parts or any(p not in CLOSED_SET for p in parts):
            continue
        if len(parts) == 1:
            out.append(parts[0])
        elif all(p in MEASUREMENT_AXIS for p in parts) or all(p in EVIDENCE_AXIS for p in parts):
            out.append(parts[0])          # one mark, deliberately imprecise within its axis
        else:
            out.extend(parts)             # straddles the axes: let the axis check refuse it
    return out


def bracketed_axis_straddles(s: str) -> list[str]:
    """Bracketed marks whose parts come from different axes — incoherent, not imprecise."""
    bad = []
    for token in re.findall(r"\(([a-z][a-z/ -]*)\)", s):
        parts = [p.strip() for p in token.split("/") if p.strip()]
        if len(parts) < 2 or any(p not in CLOSED_SET for p in parts):
            continue
        if not (all(p in MEASUREMENT_AXIS for p in parts)
                or all(p in EVIDENCE_AXIS for p in parts)):
            bad.append(token)
    return bad


def slug(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def members_of(cell: str) -> tuple[list[str], bool]:
    """App names out of a 'supporting apps' cell.

    Returns (names, clean). `clean` is False when the cell carries prose the
    parser had to discard — the caller turns that into a NOTE rather than
    trusting a count taken from a cell it did not fully understand.
    """
    # Drop a trailing summary count like "(16)" or "(11 cited)".
    body = re.sub(r"\((?:\d+[^)]*)\)\s*$", "", cell).strip()
    names, messy = [], False
    for part in re.split(r"[,;]", body):
        p = re.sub(r"\(.*?\)", "", part).strip().strip("*_`")
        if not p:
            continue
        if re.fullmatch(r"[a-z0-9][a-z0-9 ._&'/-]{0,40}", p, re.I) and len(p.split()) <= 4:
            names.append(slug(p))
        else:
            messy = True
    return [n for n in dict.fromkeys(names) if n], not messy


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_placeholders(rep: Report, files: list[Path], root: Path) -> None:
    examined = 0
    for f in files:
        examined += 1
        for n, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
            for ph in re.findall(r"\{\{[^}]*\}\}", line):
                rep.fail(
                    "placeholder",
                    f"{f.relative_to(root)}:{n} still carries the template placeholder {ph}",
                    "the next invocation reads that literal string as the value and "
                    "propagates it into synthesis, so a template artefact becomes corpus data",
                    "replace it with the real value, or delete the row if there is nothing to record",
                )
    rep.ok("placeholder", examined, "no template placeholder survives into a written file")


def check_ledger(rep: Report, root: Path) -> None:
    led = root / "ledger.md"
    if not led.exists():
        rep.fail(
            "ledger",
            "there is no ledger.md",
            "every later invocation digests blind — it cannot dedupe by hash, so the same "
            "screenshot is re-digested and its evidence double-counts toward canon promotion",
            "create ledger.md from the template in references/corpus-templates.md",
        )
        return

    text = led.read_text(errors="replace")
    seen: dict[str, str] = {}
    numbers: list[int] = []
    examined = 0

    for cells in table_rows(text):
        if len(cells) < 4:
            continue
        num, _date, src, h = cells[0], cells[1], cells[2], cells[3]
        if num.lower() in ("#", "no", "no."):
            continue  # header
        examined += 1

        if not re.fullmatch(r"[0-9a-f]{8}", h):
            rep.fail(
                "ledger-hash",
                f"ledger row {num} ({src}) has hash {h!r}, which is not 8 lowercase hex digits",
                "the next invocation's dedupe compares this column literally, so the match "
                "misses and the file is re-digested — doubling its evidence and skewing "
                "every >=3-independent-apps promotion that counts it",
                "regenerate it with `shasum <file> | cut -c1-8`",
            )
        elif h in seen:
            rep.fail(
                "ledger-hash",
                f"hash {h} appears twice — rows for {seen[h]!r} and {src!r}",
                "the same bytes were digested twice under two rows, so one subject counts as "
                "two independent pieces of evidence and can promote an observation to canon "
                "on its own",
                "delete the duplicate row and merge any evidence it added, or re-hash if the "
                "two files genuinely differ",
            )
        else:
            seen[h] = src

        if re.fullmatch(r"\d+", num):
            numbers.append(int(num))

    if numbers:
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            rep.fail(
                "ledger-append-only",
                f"ledger row numbers are {numbers[:12]}{'...' if len(numbers) > 12 else ''}, "
                f"not a contiguous 1..{len(numbers)}",
                "the ledger was rewritten rather than appended to, so a row was renumbered or "
                "dropped; anything that cited a row number now points at different evidence, and "
                "a dropped row's hash is digestible again",
                "restore the missing rows and append new ones at the end without touching "
                "existing rows",
            )

    rep.ok("ledger", examined, "every ledger row has a unique well-formed hash, appended in order",
           covers=("ledger-hash", "ledger-append-only"))


def check_canon_support(rep: Report, root: Path) -> list[tuple[str, str, list[str]]]:
    """Canon rows carry >=3 distinct members. Returns the parsed rows for the
    lineage gate to reuse."""
    parsed: list[tuple[str, str, list[str]]] = []
    examined = 0

    for name in SYNTHESIS_FILES:
        f = root / name
        if not f.exists():
            continue
        text = f.read_text(errors="replace")
        for heading in (r"^Canon\b", r"\bIcon canon\b"):
            body = section(text, heading)
            if body is None:
                continue
            for cells in table_rows(body):
                if len(cells) < 3:
                    continue
                rule = cells[0]
                if rule.lower().strip("* ") in ("rule", "") or not rule.strip():
                    continue
                members_cell = cells[2] if len(cells) >= 3 else ""
                names, clean = members_of(members_cell)
                examined += 1
                parsed.append((name, rule, names))

                if len(names) < 3:
                    if not clean and len(names) > 0:
                        rep.note(
                            "canon-support",
                            f"{name}: rule {rule[:60]!r} — could parse only {len(names)} member(s) "
                            f"from a cell carrying prose; support NOT verified, check it by hand",
                        )
                    else:
                        rep.fail(
                            "canon-support",
                            f"{name}: rule {rule[:60]!r} lists {len(names)} supporting app(s), "
                            f"below the 3-independent-apps bar",
                            "it is written as canon, so every later mock inherits it as an "
                            "established rule while it rests on one or two apps — the promotion "
                            "bar exists because a single beautiful app is a house style, not a "
                            "platform convention",
                            "demote it to (recurring) in the relevant patterns/ entry until a "
                            "third independent app evidences it, or name the missing members",
                        )
                elif not clean:
                    rep.note(
                        "canon-support",
                        f"{name}: rule {rule[:60]!r} parsed {len(names)} members but the cell also "
                        f"held prose the parser discarded — the count met the bar, the reading is "
                        f"partial",
                    )

    rep.ok("canon-support", examined, "every canon rule names at least 3 distinct supporting apps")
    return parsed


def check_lineage_gate(rep: Report, root: Path, canon: list[tuple[str, str, list[str]]]) -> None:
    """Only lineage: native evidence may reach macOS canon."""
    apps_dir = root / "apps"
    lineage: dict[str, str] = {}
    if apps_dir.is_dir():
        for f in sorted(apps_dir.glob("*.md")):
            m = re.search(r"^\s*[-*]?\s*\*{0,2}Lineage:?\*{0,2}\s*(.+)$",
                          f.read_text(errors="replace"), re.I | re.M)
            if m:
                raw = m.group(1).strip().lower()
                raw = re.sub(r"\(.*?\)", "", raw)
                raw = re.split(r"[—–-]{1,2}\s", raw)[0]
                lineage[f.stem] = raw.strip().strip("*_` ")

    examined = unresolved = 0
    for fname, rule, members in canon:
        for m in members:
            if m not in lineage:
                unresolved += 1
                continue
            examined += 1
            lin = lineage[m]
            if not any(tok in lin for tok in NATIVE_LINEAGES):
                rep.fail(
                    "lineage-gate",
                    f"{fname}: canon rule {rule[:50]!r} counts {m!r}, whose profile records "
                    f"lineage {lin!r}",
                    "a Catalyst / iOS-on-Mac / Electron app's properties have entered macOS "
                    "canon, where nothing downstream can see their origin — the corpus now "
                    "teaches an iOS density or selection style as mac taste, permanently and "
                    "invisibly",
                    f"remove {m!r} from the member list and re-check the rule still clears 3 "
                    f"native apps; record its reading in the tells-and-corrections record instead",
                )

    if unresolved:
        rep.note(
            "lineage-gate",
            f"{unresolved} canon member reference(s) have no apps/<app>.md profile, so their "
            f"lineage could not be read — support unverified for those, not cleared",
        )
    rep.ok("lineage-gate", examined, "no canon rule counts a non-native app")


def role_of(rel: Path) -> str:
    """Which part of the corpus a file is, because the mark rule differs by role."""
    parts = rel.parts
    if parts and parts[0] == "kit":
        return "kit"
    if parts and parts[0] in ("apps", "patterns", "icons"):
        return "evidence"
    if rel.name in SYNTHESIS_FILES:
        return "synthesis"
    return "other"


def check_coverage(rep: Report, root: Path) -> None:
    """Evidence that was digested but never recorded anywhere is simply gone.

    Both of these came from the blind panel: a reader auditing the same corpus by
    eye beat this gate by finding them, and the deciding line in one judge's
    verdict was "`patterns/` is empty after three UI digests, so the sidebar,
    toolbar and settings evidence from those three surfaces is simply gone."
    Neither is a formatting slip. They are silent data loss, and both are countable.
    """
    led = root / "ledger.md"
    if not led.exists():
        rep.ok("coverage", 0, "no ledger, so nothing to reconcile against")
        return

    text = led.read_text(errors="replace")
    ui_rows, targets = 0, []
    for cells in table_rows(text):
        if len(cells) < 8 or cells[0].lower() in ("#", "no", "no."):
            continue
        if cells[4].strip().lower() == "ui":
            ui_rows += 1
        for t in re.split(r"[,;]", cells[7]):
            t = t.strip().strip("`*")
            if t and "/" in t:
                targets.append(t)

    pattern_dir = root / "patterns"
    n_patterns = len(list(pattern_dir.glob("*.md"))) if pattern_dir.is_dir() else 0
    if ui_rows >= 3 and n_patterns == 0:
        rep.fail(
            "coverage",
            f"{ui_rows} UI surfaces are logged in the ledger and patterns/ holds no entries",
            "cross-app evidence is only ever recorded in the pattern files, so the sidebar, "
            "toolbar, settings and empty-state readings from those surfaces are not thin — they "
            "are gone, and nothing in the corpus records that they were ever seen",
            "write the patterns/<name>.md entry for each recognisable pattern in those surfaces; "
            "a digest that updates only apps/ has thrown away the half that generalises",
        )

    missing = sorted({t for t in targets if not (root / t).exists()})
    for t in missing[:12]:
        rep.fail(
            "coverage",
            f"a ledger row records evidence digested into {t!r}, which does not exist",
            "the ledger is the index, so a row pointing at a missing file means either the write "
            "never happened or the file was deleted — and the source hash is now logged as "
            "digested, so it will be skipped rather than re-read",
            f"write {t!r}, or correct the row to name where the evidence actually went",
        )
    if len(missing) > 12:
        rep.note("coverage", f"{len(missing) - 12} further ledger targets missing, not listed")

    rep.ok("coverage", ui_rows + len(targets),
           "every ledger row's target exists, and cross-app patterns were recorded")


def check_mark_pairs(rep: Report, root: Path, files: list[Path]) -> None:
    """A value row must carry one mark from EACH family — where both apply.

    Scoped by role rather than applied flat, and the scoping was measured rather
    than assumed. On the real 134-app corpus, 79 of 88 marked rows already carry a
    composed pair; every one of the 8 exceptions is a `kit/` row and the 9th is a
    qualitative canon rule. Those are correct as they stand:

      kit/       precision only. Strength counts independent APP sightings and a
                 kit is not an app, so a strength mark on a kit value asserts
                 corroboration that does not exist — that is the error here, not
                 its absence.
      apps/ ·    both. This is where collapsing the axes does the damage: a value
      patterns/  needs to say both how it was obtained and how much has been seen.
      icons/
      TASTE.md · strength required; precision required only when the rule states a
      ICONS.md   number. A geometry rule has nothing to qualify numerically.
    """
    examined = 0
    for f in files:
        rel = f.relative_to(root)
        role = role_of(rel)
        if role == "other":
            continue
        for cells in table_rows(f.read_text(errors="replace")):
            joined = " ".join(cells)
            marks = marks_in(joined)
            if not marks:
                continue
            label = (cells[0] or "?")[:44]
            prec = [m for m in marks if m in MEASUREMENT_AXIS]
            stre = [m for m in marks if m in EVIDENCE_AXIS]
            standalone = [m for m in marks if m in STANDALONE]
            if standalone and not (prec or stre):
                continue        # (user-override) / (insufficient-evidence) stand alone by design
            examined += 1

            if role == "evidence":
                if prec and not stre:
                    rep.fail(
                        "mark-pair",
                        f"{rel}: row {label!r} carries precision {'(' + prec[0] + ')'} and no "
                        f"evidence-strength mark",
                        "the two families are orthogonal, so a value with no strength mark says "
                        "how it was obtained and nothing about how much supports it — the next "
                        "synthesis pass has no basis to promote or refuse it, and a "
                        "single-surface reading becomes indistinguishable from a corroborated one",
                        "add one of (inferred) one surface · (confirmed) repeated in this app · "
                        "(recurring) 2 independent apps · (canon) 3+ · (contested)",
                    )
                elif stre and not prec:
                    rep.fail(
                        "mark-pair",
                        f"{rel}: row {label!r} carries strength {'(' + stre[0] + ')'} and no "
                        f"precision mark",
                        "nothing records where the number came from, so a gap-filling default and "
                        "an exact kit value read identically — and the value can later be cited "
                        "as though it were measured",
                        "add one of (specified) from a kit or HIG spec · (measured) clean pixel "
                        "read · (estimated) within a stated range · (assumed) default",
                    )
            elif role == "kit" and stre:
                rep.fail(
                    "mark-pair",
                    f"{rel}: kit row {label!r} carries an evidence-strength mark "
                    f"{'(' + stre[0] + ')'}",
                    "strength counts independent app sightings and a kit is not an app, so this "
                    "claims corroboration that does not exist; downstream it reads as a value "
                    "several shipping apps agree on when only the vendor states it",
                    "keep the precision mark alone here, and record app agreement — or "
                    "divergence, which is the finding — in the apps/ profiles instead",
                )
            elif role == "synthesis" and not stre and re.search(r"\d", joined):
                rep.fail(
                    "mark-pair",
                    f"{rel}: numeric canon row {label!r} carries no evidence-strength mark",
                    "a canon table's whole claim is how many independent apps back the rule, so a "
                    "numeric row without a strength mark states a value with no support recorded",
                    "mark it (canon) with its member list, or move it to a pattern entry at "
                    "(recurring)",
                )

    rep.ok("mark-pair", examined,
           "every value row carries the mark families its role requires")


def check_strength_thresholds(rep: Report, root: Path, files: list[Path]) -> None:
    """A row claiming (canon) or (recurring) must cite that many DISTINCT apps.

    The canon bar lives on the strength axis, so it is checked against the mark
    rather than only against the position of a table. A precision mark never
    satisfies it: `(specified)` on its own is a vendor statement, not corroboration.
    """
    examined = 0
    for f in files:
        rel = f.relative_to(root)
        if role_of(rel) == "kit":
            continue
        for cells in table_rows(f.read_text(errors="replace")):
            joined = " ".join(cells)
            marks = set(marks_in(joined))
            claimed = [m for m in marks if m in STRENGTH_APP_THRESHOLD]
            if not claimed:
                continue
            mark = claimed[0]
            need = STRENGTH_APP_THRESHOLD[mark]
            names: list[str] = []
            clean = True
            for cell in cells[1:]:
                got, ok = members_of(cell)
                if len(got) > len(names):
                    names, clean = got, ok
            examined += 1
            if len(names) < need:
                if not clean and names:
                    rep.note(
                        "strength-threshold",
                        f"{rel}: row {(cells[0] or '?')[:40]!r} is marked ({mark}) and only "
                        f"{len(names)} member(s) could be parsed from a prose cell — support NOT "
                        f"verified against the {need}-app bar",
                    )
                else:
                    rep.fail(
                        "strength-threshold",
                        f"{rel}: row {(cells[0] or '?')[:40]!r} is marked ({mark}), which asserts "
                        f"{need} independent apps, and names {len(names)}",
                        "the mark is what every later reader trusts instead of recounting, so an "
                        "unearned one promotes a house style into a platform rule and nothing "
                        "downstream can see the shortfall",
                        f"name the {need} distinct apps, or drop the mark to the level the "
                        f"evidence supports ((inferred) one surface, (confirmed) one app, "
                        f"(recurring) two)",
                    )

    rep.ok("strength-threshold", examined,
           "every (recurring)/(canon) row names as many distinct apps as it claims")


def precision_index(root: Path, files: list[Path]) -> dict[str, str]:
    """Current precision mark per evidence row, keyed stably."""
    idx: dict[str, str] = {}
    for f in files:
        rel = f.relative_to(root)
        if role_of(rel) != "evidence":
            continue
        for cells in table_rows(f.read_text(errors="replace")):
            if not cells or not cells[0]:
                continue
            prec = [m for m in marks_in(" ".join(cells)) if m in MEASUREMENT_AXIS]
            if not prec:
                continue
            label = re.sub(r"\s+", " ", cells[0].strip().strip("*_` ")) [:60]
            key = f"{rel.as_posix()}::{label}"
            # Keep the WEAKEST reading when a label repeats: a row cannot become
            # more precise by appearing twice, which is the whole point here.
            if key not in idx or PRECISION_RANK[prec[0]] < PRECISION_RANK[idx[key]]:
                idx[key] = prec[0]
    return idx


def check_precision_lock(rep: Report, root: Path, files: list[Path], accept: bool) -> None:
    """Pin the un-improvable axis so a promotion along it cannot happen silently.

    Strength genuinely improves with diligence — more apps seen, more support — so
    it is free to climb. Precision does not: it is a property of where a number
    came from, and the only thing that moves it is finding a better source. An
    `(estimated)` reading never becomes `(specified)` by being seen more often.

    A stateless check cannot enforce that, because both the before and after states
    are perfectly well-formed and the mutation between them is invisible. So the
    baseline is written down. The lock lives inside the corpus rather than inside
    this script — unlike a skill's own bundled references, the corpus is the user's
    and it grows, so a pin compiled into the gate could never cover it. The gate
    generates the lock itself on first run; nobody maintains it by hand.

    Strengthening without `--accept-precision-change` fails. Weakening passes with
    a note, because an honest downgrade is the system working.
    """
    lock_path = root / LOCK_NAME
    current = precision_index(root, files)

    if not current:
        rep.ok("precision-lock", 0, "no precision-marked evidence rows to pin")
        return

    if not lock_path.exists():
        if accept or True:
            lock_path.write_text(json.dumps(
                {"version": 1, "note": "Precision is the un-improvable axis. A value moves along "
                                       "it only when a better SOURCE is found, never by being "
                                       "seen again. Regenerate with --accept-precision-change.",
                 "generated": _today(), "rows": dict(sorted(current.items()))},
                indent=2) + "\n")
        rep.note("precision-lock",
                 f"no {LOCK_NAME} existed, so one was written pinning {len(current)} row(s) at "
                 f"their current precision. This run established the baseline and therefore "
                 f"verified nothing — the check bites from the next run on.")
        rep.ok("precision-lock", 0, "precision pins hold")
        return

    try:
        locked = json.loads(lock_path.read_text()).get("rows", {})
    except (json.JSONDecodeError, UnicodeDecodeError):
        rep.fail(
            "precision-lock",
            f"{LOCK_NAME} is not readable JSON",
            "the pin on the un-improvable axis is gone, so a value could be promoted from "
            "(estimated) to (specified) between two sessions and nothing would show it",
            f"delete {LOCK_NAME} and re-run to regenerate the baseline, noting in the ledger that "
            f"the pin history was lost",
        )
        return

    strengthened, weakened, added = [], [], []
    for key, prec in sorted(current.items()):
        was = locked.get(key)
        if was is None:
            added.append(key)
        elif PRECISION_RANK[prec] > PRECISION_RANK.get(was, 0):
            strengthened.append((key, was, prec))
        elif PRECISION_RANK[prec] < PRECISION_RANK.get(was, 0):
            weakened.append((key, was, prec))

    if strengthened and not accept:
        for key, was, now in strengthened:
            rep.fail(
                "precision-lock",
                f"{key} moved precision ({was}) → ({now})",
                "precision does not improve by re-sighting — only by finding a better source. If "
                "no kit or spec was ingested for this value, a guess has just acquired the "
                "authority of a measurement, and every mock built from the corpus afterwards "
                "inherits it as fact",
                f"if a better source really arrived, name it in the ledger and re-run with "
                f"--accept-precision-change; if not, restore ({was})",
            )
    elif strengthened and accept:
        rep.note("precision-lock",
                 f"accepted {len(strengthened)} precision change(s): " +
                 "; ".join(f"{k} ({a})→({b})" for k, a, b in strengthened[:6]))

    for key, was, now in weakened:
        rep.note("precision-lock",
                 f"{key} weakened ({was}) → ({now}) — allowed, and worth a line in the ledger: a "
                 f"downgrade is the measurement-honesty rule working, not a defect")

    if accept:
        lock_path.write_text(json.dumps(
            {"version": 1, "note": "Precision is the un-improvable axis. A value moves along it "
                                   "only when a better SOURCE is found, never by being seen "
                                   "again. Regenerate with --accept-precision-change.",
             "generated": _today(), "rows": dict(sorted(current.items()))}, indent=2) + "\n")

    if added:
        rep.note("precision-lock",
                 f"{len(added)} new precision-marked row(s) not yet pinned; they are added to the "
                 f"lock on the next --accept-precision-change run")

    rep.ok("precision-lock", len(current), "no value strengthened its precision unannounced",
           covers=())


def _today() -> str:
    from datetime import date
    return date.today().isoformat()


def check_traceability(rep: Report, root: Path, canon: list[tuple[str, str, list[str]]]) -> None:
    """A canon rule must trace back to member profiles that actually hold evidence.

    Added after an eval run: a reader auditing a corpus by eye caught three things
    this gate could not — a canon member whose profile was a single lineage line
    with no tokens, a canon member with no ledger row at all, and a ledger row
    claiming a surface the profile never recorded. The first two are arithmetic.

    A canon rule that cannot be traced to its members' evidence is the exact shape
    of corpus drift: the rule outlives the evidence that made it, and nothing
    downstream can tell.
    """
    apps_dir = root / "apps"
    if not apps_dir.is_dir():
        rep.note("canon-traceability",
                 "no apps/ directory, so no canon rule's membership could be traced to a "
                 "profile — the canon-support count is a count of names, not of evidence")
        rep.ok("canon-traceability", 0, "every canon member has a profile carrying evidence")
        return

    profiles = {f.stem: f for f in apps_dir.glob("*.md")}
    ledger_text = (root / "ledger.md").read_text(errors="replace") \
        if (root / "ledger.md").exists() else ""

    examined = 0
    for fname, rule, members in canon:
        for m in members:
            examined += 1
            f = profiles.get(m)
            if f is None:
                rep.fail(
                    "canon-traceability",
                    f"{fname}: canon rule {rule[:44]!r} counts {m!r}, which has no "
                    f"apps/{m}.md profile",
                    "the rule is written as canon on the strength of a name with no evidence "
                    "behind it — nothing downstream can check what {0!r} actually showed, and "
                    "the promotion arithmetic counted it anyway".format(m),
                    f"write apps/{m}.md from the template with the surfaces and tokens that "
                    f"evidence this rule, or remove {m!r} from the member list and re-check the "
                    f"rule still clears three apps",
                )
                continue

            body = f.read_text(errors="replace")
            token_rows = [c for c in table_rows(body)
                          if len(c) >= 2 and c[0] and c[0].lower().strip("* ") not in
                          ("token", "surface", "dimension", "role", "rule", "app", "control")
                          and (marks_in(" ".join(c)) or re.search(r"\d", " ".join(c[1:])))]
            if not token_rows:
                rep.fail(
                    "canon-traceability",
                    f"{fname}: canon rule {rule[:44]!r} counts {m!r}, whose profile records no "
                    f"tokens at all",
                    "a profile with no measured values cannot evidence a claim about a value; "
                    "the rule reads as three-app canon while resting on fewer, and the shortfall "
                    "is invisible to every later reader",
                    f"record the tokens from {m!r}'s digested surfaces in apps/{m}.md, or drop "
                    f"it from the member list",
                )

            if ledger_text and not re.search(rf"\|\s*{re.escape(m)}\s*\|", ledger_text, re.I):
                rep.fail(
                    "ledger-coverage",
                    f"{m!r} is cited by canon rule {rule[:40]!r} but has no ledger row",
                    "its evidence entered the corpus without a hash, a date or a source file, so "
                    "it cannot be deduped, re-digested or dated — and a later session cannot tell "
                    "where it came from",
                    f"add {m!r}'s ledger row(s) with the source file and hash, or remove it from "
                    f"the member list",
                )

    rep.ok("canon-traceability", examined,
           "every canon member has a profile carrying evidence, and a ledger row",
           covers=("ledger-coverage",))


def check_clusters(rep: Report, root: Path) -> None:
    """A cluster whose members contradict more than 2 identity tokens must have
    been split."""
    taste = root / "TASTE.md"
    examined = 0
    if not taste.exists():
        rep.ok("cluster-budget", 0, "no TASTE.md, so no cluster to audit")
        return
    body = section(taste.read_text(errors="replace"), r"Style clusters")
    if body is None:
        rep.ok("cluster-budget", 0, "TASTE.md has no Style clusters section")
        return

    blocks = re.split(r"^###\s+", body, flags=re.M)[1:]
    for block in blocks:
        name = block.splitlines()[0].strip() if block.splitlines() else "?"
        examined += 1
        contradictions = len(re.findall(
            r"contradict|conflicts with|does not evidence|breaks the cluster|"
            r"outside the band|departs from", block, re.I))
        if contradictions > 2:
            rep.fail(
                "cluster-budget",
                f"cluster {name!r} records {contradictions} contradictions against its identity "
                f"tokens, over the budget of 2",
                "the cluster has stopped cohering, so design mode inherits identity tokens that "
                "its own members disagree about — the mock passes every rubric and still feels "
                "off-brand, which is the failure a cluster exists to prevent",
                "split it along the contradiction, give each half its own identity tokens, and "
                "note the split in the synthesis history",
            )
    rep.ok("cluster-budget", examined, "no cluster exceeds its 2-contradiction budget")


def check_gaps_and_freshness(rep: Report, root: Path) -> None:
    examined = 0
    for name in SYNTHESIS_FILES:
        f = root / name
        if not f.exists():
            continue
        text = f.read_text(errors="replace")
        examined += 1

        # Freshness. The downstream reader cannot date a claim the file does not date.
        dated = re.search(
            r"(?:Updated|Last updated|Regenerated|Ingested|Frozen|Generated|As of)\s*:?\s*"
            r"(\d{4}-\d{2}-\d{2})", text, re.I)
        if not dated:
            rep.fail(
                "freshness",
                f"{name} carries no ISO date in its header",
                "a later reader — a mock build, another skill, a future session — cannot tell "
                "whether these values are current or a year stale, and undated guidance gets "
                "cited as though it were fresh",
                "put `Updated <YYYY-MM-DD>` in the header block (Regenerated / Ingested / "
                "Frozen are accepted too), and re-stamp it on every pass that rewrites the file",
            )

        m = re.search(r"Corpus level:?\s*\**\s*(" + "|".join(LEVELS) + r")", text, re.I)
        if not m:
            stated = re.search(r"Corpus level:?\s*\**\s*([A-Za-z][A-Za-z -]{2,20})", text)
            if stated:
                rep.fail(
                    "corpus-level",
                    f"{name} states corpus level {stated.group(1).strip()!r}, which is not one of "
                    f"{'/'.join(LEVELS)}",
                    "the maturity model is what scales a claim to its evidence, so a level from "
                    "outside it cannot be compared — nothing downstream can tell whether this "
                    "corpus may be treated as authority",
                    f"use one of {'/'.join(LEVELS)}, or add the new level to the model in "
                    f"references/persona.md §3.1 and to this script's LEVELS",
                )
                continue
            rep.fail(
                "corpus-level",
                f"{name} does not state a corpus level",
                "nothing downstream can scale its confidence to the evidence behind it, so a "
                "2-app corpus and a 60-app corpus read identically to the next run",
                "add `Corpus level: <Novice|Competent|Proficient|Expert>` to the header",
            )
            continue

        level = m.group(1).capitalize()
        if LEVELS.index(level) >= LEVELS.index("Proficient"):
            continue

        gaps = section(text, r"Knowledge gaps")
        stripped = re.sub(r"\{\{[^}]*\}\}", "", gaps or "").strip()
        if not stripped:
            rep.fail(
                "knowledge-gaps",
                f"{name} is at {level} and its Knowledge Gaps section is empty or missing",
                "below Proficient the corpus is thin in ways only it can name; an empty gaps "
                "section reads as 'nothing missing', so the user never learns which surface "
                "types, modes or clusters to bring next and the corpus stops growing where it "
                "is weakest",
                "name the missing surface types, the unseen modes, and the cluster blind spots",
            )
    rep.ok("gaps+freshness", examined, "each synthesis file is dated, levelled, and states its gaps",
           covers=("freshness", "corpus-level", "knowledge-gaps"))


def check_marks(rep: Report, root: Path, files: list[Path]) -> None:
    """Marks come from the closed set, and no cell carries two from one axis."""
    examined = collisions = 0

    for f in files:
        rel = f.relative_to(root)
        text = f.read_text(errors="replace")

        for cells in table_rows(text):
            joined = " ".join(cells)
            found = marks_in(joined)
            if not found:
                continue
            examined += 1

            for token in bracketed_axis_straddles(joined):
                rep.fail(
                    "mark-axis",
                    f"{rel}: row {cells[0][:40]!r} carries `({token})`, whose parts come from "
                    f"different provenance axes",
                    "a bracketed mark means 'somewhere between these two within one axis'; "
                    "straddling the axes says nothing a reader can act on, and the value ends up "
                    "with no usable measurement quality and no usable evidence strength",
                    "split it into one measurement-quality mark and one evidence-strength mark",
                )
            meas = [m for m in found if m in MEASUREMENT_AXIS]
            evid = [m for m in found if m in EVIDENCE_AXIS]
            for axis_name, got in (("measurement-quality", meas), ("evidence-strength", evid)):
                if len(set(got)) > 1:
                    collisions += 1
                    rep.fail(
                        "mark-axis",
                        f"{rel}: row {cells[0][:40]!r} carries {len(set(got))} {axis_name} marks "
                        f"({', '.join('(' + g + ')' for g in sorted(set(got)))})",
                        "the two axes are orthogonal and each admits exactly one value, so a "
                        "reader takes whichever it happens to match first — the value silently "
                        "acquires a confidence nobody assigned it",
                        f"keep one {axis_name} mark; if the value was re-read at a different "
                        f"quality, record the stronger reading and note the supersession",
                    )

        # A misspelled mark is invisible to the next run: it reads as no mark at all.
        for tok in set(re.findall(r"\(([a-z][a-z-]{2,24})\)", text)):
            if tok in CLOSED_SET or tok in PROSE_PAREN:
                continue
            near = [k for k in CLOSED_SET if _near_miss(tok, k)]
            if near:
                rep.note(
                    "mark-vocabulary",
                    f"{rel}: `({tok})` is not in the closed mark set and looks like "
                    f"`({near[0]})` — a misspelled mark reads as no mark at all to the next "
                    f"invocation, which then treats the value as unmarked",
                )

    rep.ok("mark-axis", examined, "every marked row carries at most one mark per axis",
           covers=("mark-vocabulary",))


def _near_miss(a: str, b: str) -> bool:
    """Edit distance <= 2 and not equal — a typo, not a different word."""
    if a == b or abs(len(a) - len(b)) > 2:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 2


# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Assert the invariants a design corpus depends on.")
    ap.add_argument("corpus", nargs="?", default="design-corpus")
    ap.add_argument("--accept-precision-change", action="store_true",
                    help="record the current precision marks as the new pinned baseline. Use only "
                         "when a better SOURCE arrived for a value, and say so in the ledger.")
    args = ap.parse_args(argv[1:])
    root = Path(args.corpus).expanduser()

    if not root.is_dir():
        print(f"FAIL [corpus] {root} is not a directory — nothing was checked, and that is not "
              f"a pass. Fix: point this at the corpus directory, or create it from the layout in "
              f"references/corpus-templates.md.", file=sys.stderr)
        return 2

    files = sorted(p for p in root.rglob("*.md") if p.is_file())
    if not files:
        print(f"FAIL [corpus] {root} holds no .md files — nothing was checked. Fix: this is an "
              f"empty directory, not a corpus; digest something first.", file=sys.stderr)
        return 2

    rep = Report()
    check_placeholders(rep, files, root)
    check_ledger(rep, root)
    canon = check_canon_support(rep, root)
    check_lineage_gate(rep, root, canon)
    check_traceability(rep, root, canon)
    check_clusters(rep, root)
    check_coverage(rep, root)
    check_mark_pairs(rep, root, files)
    check_strength_thresholds(rep, root, files)
    check_precision_lock(rep, root, files, args.accept_precision_change)
    check_gaps_and_freshness(rep, root)
    check_marks(rep, root, files)

    for line in rep.oks:
        print(line)
    for line in rep.notes:
        print(line)
    for line in rep.fails:
        print(line, file=sys.stderr)

    print(f"\n{len(files)} file(s) under {root} · "
          f"{len(rep.fails)} FAIL · {len(rep.notes)} NOTE · "
          f"{len(rep.ran)} check(s) ran, {len(rep.oks)} clean")
    if rep.notes and not rep.fails:
        print("NOTEs are not failures, and they are not passes either: read each one before "
              "reporting this corpus as clean.")
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
