#!/usr/bin/env python3
"""Gate for the injected block and the provenance registry.

Prose that says "a test asserts X" is worse than prose asking for X, because it reads as covered.
This is that test. It runs with no dependencies on any python3, and it owns every failure mode in
this skill that is otherwise silent:

  * a literal edited without bumping the version, which re-mints every warm prefix at full price
  * a retired literal deleted or tidied, which re-mints every conversation still pinned to it
  * a figure added to the prose with no provenance tier, which borrows the measured numbers' credit
  * an assumed figure stated outside an honesty section, which is the same borrowing one step later
  * a claim about a living third-party document with no date on it, which cannot be falsified

Usage:
    python3 scripts/block-check.py            # gate the tree this script lives in
    python3 scripts/block-check.py --verbose  # also print what passed
    python3 scripts/block-check.py <dir>      # gate another copy (for a before/after comparison)

Exit 0 means every hard check passed. Warnings go to stderr and do not fail the build; anything on
stderr is a warning to read. Check the exit code rather than the output: piping this through grep
makes $? grep's status and not the gate's.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import re
import sys
from pathlib import Path

# --- Pins -------------------------------------------------------------------------------------
#
# Mirrored here on purpose. Editing a literal means editing this file in the same commit, which is
# the smallest mechanism that makes the cost of a wording change visible before it ships.

BLOCK_PINS = [
    # (version, stripped UTF-8 bytes, sha256 of the unwrapped literal, first 16 hex)
    ("v4", 881, "a4f1ff0d16fdb4c7"),
    ("v3", 736, "3f4d1e004323b4ae"),
    ("v1", 1029, "232e2c558a5ae1d8"),
]

# The ceiling, as a number rather than an assertion that a ceiling exists.
#
# The target is 150-300 tokens (see SKILL.md § Sizing, and the PRISM persona result behind it).
# At the ~4 bytes/token this block's register actually measures, 300 tokens is ~1,200 bytes. That is
# the ceiling. v4 sits at 881, so there are 319 bytes of headroom — about two clauses' worth.
#
# A pin is not a ceiling. Pinning 881 makes every proposed addition fail, which is why the previous
# wording served nobody: the section's job is to make cost visible, not to refuse all change.
BLOCK_CEILING_BYTES = 1200
BLOCK_FLOOR_BYTES = 600

# Provenance is TWO orthogonal families that compose as `independence+verification`, not one flat list.
#
# Flattening them is a real defect: it makes a promotion along one axis look like a promotion along the
# other. Independence is a property of the SOURCE and is not improvable by reading harder; verification
# is a property of OUR diligence and is. So `self-report+results-read` — a competitor's README read in
# full — is a legitimate, permanent state, and no amount of re-reading may turn it into `independent`.
# Under a single flat axis that row read as "not verified", and a reader fixing the verification half
# would have appeared licensed to promote the independence half. See provenance.md.
INDEPENDENCE = {"first-party", "independent", "vendor-doc", "self-report", "anecdote", "assumed"}
VERIFICATION = {"results-read", "summarised", "second-hand", "unlocated", "none"}

# `assumed` means there is no source, so there is nothing to verify; the pairing is exclusive both ways.
EXCLUSIVE_PAIR = ("assumed", "none")

# Independence marks naming a living, external document: an undated claim about one is unfalsifiable.
INDEPENDENCE_REQUIRING_DATE = {"independent", "vendor-doc", "self-report", "anecdote"}

# --- The promotion guard ----------------------------------------------------------------------
#
# Promotion runs along the VERIFICATION axis only. Reading a paper's results section moves
# `second-hand` -> `results-read`; it never moves `self-report` -> `independent`. But both
# `self-report+results-read` and `independent+results-read` are individually well-formed, so no amount
# of shape-checking can see a row that quietly changed families — a stateless gate has no history.
#
# So the independence mark is PINNED per row, the same way the block literals are pinned above.
# Changing one now requires editing this file in the same commit, which makes a promotion deliberate
# and reviewable instead of silent. That is the whole mechanism: not that it cannot be done, but that
# it cannot be done quietly.
INDEPENDENCE_PINS = {
    "swe-bench-caveman": "first-party",
    "swe-bench-tasklength": "first-party",
    "register-compliance": "first-party",
    "swe-bench-v4": "first-party",
    "blind-panel": "first-party",
    "effort-sweep": "first-party",
    "block-size": "first-party",
    "jetbrains": "independent",
    "cost-anatomy": "independent",
    "caveman-readme": "self-report",  # fully read; a stake in its own numbers. Never promotes.
    "prism-persona": "independent",
    "giskard-aggregate": "independent",
    "giskard-permodel": "independent",
    "renze-guven": "independent",
    "nayab-budgets": "independent",
    "brevity-counterevidence": "independent",
    "tool-definitions-anthropic": "vendor-doc",
    "tool-definitions-practitioner": "independent",
    "lever-hierarchy": "self-report",  # a vendor benchmarking its own feature.
    "cache-economics": "vendor-doc",
    "tokenizer-change": "vendor-doc",
    "reused-input-anecdote": "anecdote",
    "output-share": "assumed",
    "perch-enrollment": "first-party",
}

# Register: the block is a set of statements about how the session works, not a set of demands.
BANNED_REGISTER = ["CRITICAL", "YOU MUST", "ALWAYS ", "NEVER FORGET", "DO NOT EVER", "IMPORTANT:"]

# The five the quality floor has to name, because these five are exactly what a token metric
# rewards dropping.
QUALITY_FLOOR_SURVIVORS = [
    "uncertainty",
    "caveat",
    "security warning",
    "destructive-action confirmation",
    "required verification",
]

# v1's clause 4 shape. It contradicted a mandatory review gate, and skipping the gate improves every
# token metric, so the regression is invisible on any dashboard.
VERIFICATION_PROHIBITION = [
    "no trailing verification",
    "skip verification",
    "skip the verification",
    "do not verify",
    "don't verify",
    "no second pass",
    "one artifact, once",
]

# A block that asks the model to confirm it followed the block spends output tokens auditing
# compliance with an instruction whose whole purpose was spending fewer output tokens.
SELF_AUDIT = [
    "confirm you are following",
    "confirm that you followed",
    "report that you followed",
    "verify you followed",
    "state that you have followed",
    "acknowledge these rules",
]

# Anything that makes the literal vary turns a preamble into a cache-miss generator.
VOLATILE = [
    (r"\{\{", "a template placeholder"),
    (r"\$\{", "a shell/JS interpolation"),
    (r"%[sd]\b", "a printf placeholder"),
    (r"\b20\d\d-\d\d-\d\d\b", "an ISO date"),
    (r"\bv\d+\.\d+", "a version string the model can see"),
    (r"\bsession[ _-]?id\b", "a session id"),
]

HONESTY_HEADINGS = (
    "honesty about the numbers",
    "honest limits",
    "what is not yet measured",
    "open questions",
    "what this measurement does not establish",
    "what this registry cannot do",
)


class Gate:
    def __init__(self, root: Path, verbose: bool = False):
        self.root = root
        self.verbose = verbose
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def fail(self, check: str, msg: str) -> None:
        self.failures.append(f"{check}: {msg}")

    def warn(self, check: str, msg: str) -> None:
        self.warnings.append(f"{check}: {msg}")

    def ok(self, check: str, msg: str = "") -> None:
        self.passes.append(f"{check}{': ' + msg if msg else ''}")

    # --- helpers ---------------------------------------------------------------------------
    def read(self, rel: str) -> str | None:
        p = self.root / rel
        if not p.exists():
            return None
        # Normalise CRLF: a Windows checkout must not change what gets counted, or the byte pin
        # fails for a reason that has nothing to do with the block.
        return p.read_text(encoding="utf-8").replace("\r\n", "\n")

    @staticmethod
    def unwrap(literal: str) -> str:
        """Collapse the markdown hard-wrap so the literal compares on content, not on line breaks."""
        paras = [" ".join(p.split()) for p in literal.strip().split("\n\n")]
        return "\n\n".join(paras)

    # --- checks ----------------------------------------------------------------------------
    def check_blocks(self) -> str | None:
        src = self.read("skills/discipline/references/injected-block.md")
        if src is None:
            self.fail("block/present", "references/injected-block.md is missing — the literal IS the "
                                      "deliverable; without it the skill ships prose about a block "
                                      "nobody can inject. Restore the file.")
            return None

        fences = re.findall(r"```text\n(.*?)```", src, re.S)
        if not fences:
            self.fail("block/present", "injected-block.md contains no ```text fence — the literal is "
                                      "what gets injected; prose about it is not a substitute.")
            return None

        if len(fences) != len(BLOCK_PINS):
            self.fail(
                "block/retention",
                f"found {len(fences)} fenced literals, expected {len(BLOCK_PINS)} "
                f"({', '.join(v for v, _, _ in BLOCK_PINS)}). A conversation is pinned to the "
                "version it opened with and replays those exact bytes, so deleting or tidying a "
                "retired literal re-mints every conversation still naming it at full price. Add the "
                "outgoing literal here before overwriting it; rows only ever get added.",
            )
        else:
            self.ok("block/retention", f"{len(fences)} literals retained")

        # Score every fence we can identify, rather than bailing on a count mismatch: a tree with a
        # missing retained literal still has a current block whose floors and register can be checked,
        # and short-circuiting there hides every other defect behind the first one.
        by_digest = {d: (v, b) for v, b, d in BLOCK_PINS}
        for idx, literal in enumerate(fences):
            unwrapped = self.unwrap(literal)
            got_bytes = len(unwrapped.encode("utf-8"))
            got_digest = hashlib.sha256(unwrapped.encode("utf-8")).hexdigest()[:16]

            if got_digest in by_digest:
                version, want_bytes = by_digest[got_digest]
                if got_bytes != want_bytes:
                    self.fail(f"block/{version}/bytes", f"{got_bytes} bytes, pinned at {want_bytes}.")
                else:
                    self.ok(f"block/{version}", f"{got_bytes} bytes, digest {got_digest}")
            else:
                match_by_size = [v for v, b, _ in BLOCK_PINS if b == got_bytes]
                if match_by_size:
                    self.fail(
                        f"block/{match_by_size[0]}/digest",
                        f"literal {idx} is {got_bytes} bytes — the pinned size for "
                        f"{match_by_size[0]} — but its content differs (sha256 {got_digest}, pinned "
                        f"{[d for v, b, d in BLOCK_PINS if v == match_by_size[0]][0]}). A same-length "
                        "edit is the one change no byte count catches, and it silently rewrites the "
                        "front of every warm prefix naming this version. Bump the version rather than "
                        "editing in place.",
                    )
                else:
                    self.fail(
                        "block/unknown-literal",
                        f"literal {idx} ({got_bytes} bytes, sha256 {got_digest}) matches no pin in "
                        "BLOCK_PINS. Either it was edited without updating the gate, or a literal was "
                        "added without being pinned — both ship a cost change quietly. Add its pin.",
                    )

        # The current block is the first fence: both this file and its predecessor put the live
        # literal above the retained ones.
        return self.unwrap(fences[0])

    def check_ceiling(self, block: str) -> None:
        n = len(block.encode("utf-8"))
        if n > BLOCK_CEILING_BYTES:
            self.fail(
                "block/ceiling",
                f"{n} bytes, over the {BLOCK_CEILING_BYTES}-byte ceiling (~300 tokens). Persona and "
                "style prompts carry an accuracy cost that scales with length, and coding was the "
                "worst-hit category in the study behind that target. Cut a clause rather than "
                "raising the ceiling.",
            )
        elif n < BLOCK_FLOOR_BYTES:
            self.warn(
                "block/floor",
                f"{n} bytes, under the {BLOCK_FLOOR_BYTES}-byte floor (~150 tokens). Not an error, "
                "but check a clause was not lost in an edit.",
            )
        else:
            head = BLOCK_CEILING_BYTES - n
            self.ok("block/ceiling", f"{n} of {BLOCK_CEILING_BYTES} bytes, {head} bytes of headroom")

    def check_literal_purity(self, block: str) -> None:
        for pattern, what in VOLATILE:
            if re.search(pattern, block, re.I):
                self.fail(
                    "block/literal",
                    f"contains {what}. The prompt cache matches an exact byte prefix, so anything "
                    "that varies stops being a preamble and becomes a cache-miss generator — the "
                    "most expensive thing this feature can do is edit itself. Remove it; the proxy "
                    "already logs the version for free.",
                )
                return
        self.ok("block/literal", "no interpolation, clock, id or model-visible version")

    def check_register(self, block: str) -> None:
        up = block.upper()
        hits = [b for b in BANNED_REGISTER if b in up]
        if hits:
            self.fail(
                "block/register",
                f"uses {', '.join(repr(h.strip()) for h in hits)}. Current models over-trigger on "
                "that register, and a block whose job is to be a default rather than a demand gets "
                "over-complied with instead of followed. Restate it as how the session already "
                "works, with an escape hatch.",
            )
        else:
            self.ok("block/register", "declarative throughout")

    def check_floors(self, block: str) -> None:
        low = block.lower()

        missing = [s for s in QUALITY_FLOOR_SURVIVORS if s not in low]
        if missing:
            self.fail(
                "block/quality-floor",
                f"the quality floor no longer names: {', '.join(missing)}. Told only to be brief, a "
                "model prunes caveats and reasoning first — cheapest to cut, hardest absence to "
                "notice, and invisible in every per-turn metric. These are named because they are "
                "exactly what a token metric rewards dropping.",
            )
        else:
            self.ok("block/quality-floor", "all five survivors named")

        if not ("never how much you do" in low or "not how much you do" in low):
            self.fail(
                "block/work-floor",
                "clause 6 is gone. Without it, 'spend fewer tokens' is satisfied most cheaply by "
                "investigating less — measured at -32.7% steps for -7.6 points of task score. It is "
                "the only clause here whose job is to prevent a saving; every other clause can be "
                "satisfied by doing less work.",
            )
        else:
            self.ok("block/work-floor", "present")

        for phrase in VERIFICATION_PROHIBITION:
            if phrase in low:
                self.fail(
                    "block/no-verification-ban",
                    f"contains {phrase!r}. v1 did this and it contradicted a mandatory self-review "
                    "gate. Skipping is cheaper, so every token metric improves when the security "
                    "gate stops running — a regression no dashboard can see. Remove your own "
                    "verification instructions instead of adding a prohibition.",
                )
                return
        self.ok("block/no-verification-ban", "does not re-acquire v1's clause 4 shape")

        for phrase in SELF_AUDIT:
            if phrase in low:
                self.fail(
                    "block/no-self-audit",
                    f"contains {phrase!r}. The savings would fund their own audit: output tokens "
                    "spent confirming compliance with an instruction about spending fewer output "
                    "tokens. The proxy already logs the version.",
                )
                return
        self.ok("block/no-self-audit", "never asks the model to confirm compliance")

    # --- provenance ------------------------------------------------------------------------
    def parse_registry(self) -> list[dict] | None:
        src = self.read("skills/discipline/references/provenance.md")
        if src is None:
            self.fail(
                "provenance/present",
                "references/provenance.md is missing. Without it no figure in this skill has a "
                "declared tier, and the measured numbers lend their credibility to the assumed ones "
                "— which is the one thing this skill's own closing rule forbids.",
            )
            return None

        rows = []
        for line in src.split("\n"):
            if not line.startswith("| "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 7 or cells[0] in ("id", "Tier", "Mark") or set(cells[0]) <= {"-"}:
                continue
            rows.append(
                {
                    "id": cells[0],
                    "figures": [f.strip() for f in cells[1].split(";") if f.strip()],
                    "provenance": cells[2],
                    "scope": cells[3],
                    "appears_in": [a.strip() for a in cells[4].split(";") if a.strip()],
                    "observed": cells[5],
                    "source": cells[6],
                }
            )
        if not rows:
            self.fail("provenance/parse", "provenance.md has no parseable registry rows — the gate "
                                         "reads a 6-column pipe table. Nothing is being checked.")
            return None
        return rows

    FILE_MAP = {
        "SKILL.md": "skills/discipline/SKILL.md",
        "evidence.md": "skills/discipline/references/evidence.md",
        "injected-block.md": "skills/discipline/references/injected-block.md",
        "provenance.md": "skills/discipline/references/provenance.md",
        "README.md": "README.md",
        "EVALS.md": "EVALS.md",
    }

    @staticmethod
    def numbers_in(text: str) -> set[float]:
        """Every credibility-bearing figure: a number carrying %, $, pp, or 'points'."""
        out = set()
        for m in re.finditer(
            r"(?:\$\s*)?(\d[\d,]*(?:\.\d+)?)\s*(?:%|pp\b|points?\b|percentage points)|"
            r"\$\s*(\d[\d,]*(?:\.\d+)?)",
            text,
        ):
            raw = m.group(1) or m.group(2)
            try:
                out.add(float(raw.replace(",", "")))
            except ValueError:
                pass
        return out

    @staticmethod
    def as_float(s: str) -> float | None:
        try:
            return float(s.replace(",", ""))
        except ValueError:
            return None

    def check_provenance(self, rows: list[dict]) -> None:
        today = _dt.date.today()

        # (a) two closed families, composed as one pair per row
        marked_ok = 0
        for r in rows:
            raw = r["provenance"]
            parts = [p.strip() for p in raw.split("+") if p.strip()]
            if len(parts) != 2:
                self.fail(
                    "provenance/mark",
                    f"row {r['id']!r} has mark {raw!r}. A mark is a composed PAIR, "
                    "`independence+verification` — a single mark is incomplete, not valid. "
                    f"Independence: {', '.join(sorted(INDEPENDENCE))}. "
                    f"Verification: {', '.join(sorted(VERIFICATION))}.",
                )
                continue
            a, b = parts
            a_ok, b_ok = a in INDEPENDENCE, b in VERIFICATION
            if a_ok and b_ok:
                if (a == EXCLUSIVE_PAIR[0]) != (b == EXCLUSIVE_PAIR[1]):
                    self.fail(
                        "provenance/mark",
                        f"row {r['id']!r} pairs {a!r} with {b!r}. `assumed` means there is no source, "
                        "so it pairs only with `none`, and `none` only with `assumed`. Anything else "
                        "claims a verification state for a figure that has nothing to verify.",
                    )
                else:
                    marked_ok += 1
                continue
            if a in VERIFICATION and b in INDEPENDENCE:
                self.fail(
                    "provenance/mark",
                    f"row {r['id']!r} has mark {raw!r} — the families are the wrong way round. "
                    "Write independence first: it is the property of the source, and putting it "
                    "second is how a verification upgrade gets mistaken for an independence one.",
                )
            elif a in INDEPENDENCE and b in INDEPENDENCE:
                self.fail(
                    "provenance/mark",
                    f"row {r['id']!r} carries two independence marks ({a}, {b}), which is malformed. "
                    "One from each family, never two from one.",
                )
            elif a in VERIFICATION and b in VERIFICATION:
                self.fail(
                    "provenance/mark",
                    f"row {r['id']!r} carries two verification marks ({a}, {b}), which is malformed. "
                    "One from each family, never two from one.",
                )
            else:
                bad = a if not a_ok else b
                self.fail(
                    "provenance/mark",
                    f"row {r['id']!r} uses {bad!r}, which is in neither closed set. An invented mark "
                    "is how a self-report gets filed as a measurement.",
                )
        if marked_ok == len(rows):
            self.ok("provenance/mark", f"{len(rows)} rows, every mark a valid composed pair")

        # (a2) the promotion guard: independence is pinned, so a family change cannot be silent
        drifted, unpinned = [], []
        for r in rows:
            a = r["provenance"].split("+")[0].strip()
            want = INDEPENDENCE_PINS.get(r["id"])
            if want is None:
                unpinned.append(r["id"])
            elif a != want:
                drifted.append(f"{r['id']}: {want} -> {a}")
        if drifted:
            self.fail(
                "provenance/promotion",
                "independence changed on " + ", ".join(drifted) + ". Promotion runs along the "
                "verification axis only — reading a source more carefully never makes its author "
                "disinterested. If this change is genuinely correct (the figure was re-sourced to an "
                "independent party, not merely re-read), update INDEPENDENCE_PINS in this script in "
                "the same commit and say in the message what re-sourced it.",
            )
        if unpinned:
            self.fail(
                "provenance/promotion",
                f"rows {', '.join(unpinned)} have no entry in INDEPENDENCE_PINS. A new row must pin its "
                "independence mark so a later change to it is visible. Add it to this script.",
            )
        if not drifted and not unpinned:
            self.ok("provenance/promotion", f"{len(rows)} independence marks match their pins")

        # (b) a dated claim about a living, external document
        undated = [            r["id"]
            for r in rows
            if r["provenance"].split("+")[0].strip() in INDEPENDENCE_REQUIRING_DATE
            and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["observed"])
        ]
        if undated:
            self.fail(
                "provenance/observed",
                f"rows {', '.join(undated)} cite a living external document with no observed date. A "
                "claim about what a third-party page 'currently says' is unfalsifiable without one, and "
                "will become false without anyone noticing — which is exactly what happened to the "
                "caveman-readme row. Add the date you read it.",
            )
        else:
            self.ok("provenance/observed", "every living-source row carries a read date")

        future = []
        for r in rows:
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["observed"]):
                d = _dt.date.fromisoformat(r["observed"])
                if d > today:
                    future.append(r["id"])
        if future:
            self.fail("provenance/observed", f"rows {', '.join(future)} are dated in the future.")

        # (c) registry has not drifted out of the prose
        drift = []
        for r in rows:
            targets = [self.FILE_MAP.get(a) for a in r["appears_in"]]
            corpus = "\n".join(filter(None, (self.read(t) for t in targets if t)))
            if not corpus:
                continue
            present = self.numbers_in(corpus) | {
                v for v in (self.as_float(x) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", corpus)) if v is not None
            }
            for fig in r["figures"]:
                v = self.as_float(fig)
                if v is None:
                    continue
                if v not in present:
                    drift.append(f"{r['id']}:{fig}")
        if drift:
            self.fail(
                "provenance/drift",
                f"registered figures no longer in the prose they claim: {', '.join(drift)}. A stale "
                "registry is worse than none — it reads as coverage. Remove the row or fix the "
                "appears_in column.",
            )
        else:
            self.ok("provenance/drift", "every registered figure still occurs where it claims to")

        # (d) coverage: no untiered figure in SKILL.md
        registered: set[float] = set()
        for r in rows:
            for fig in r["figures"]:
                v = self.as_float(fig)
                if v is not None:
                    registered.add(v)

        skill = self.read("skills/discipline/SKILL.md") or ""
        unregistered = sorted(self.numbers_in(skill) - registered)
        if unregistered:
            self.fail(
                "provenance/coverage",
                f"SKILL.md states figures with no registry row: {', '.join(str(u) for u in unregistered)}. "
                "An untiered number borrows the measured numbers' credibility for free, which the "
                "skill's own closing rule forbids. Add a row with its tier and source, or cut it.",
            )
        else:
            self.ok("provenance/coverage", f"all {len(self.numbers_in(skill))} figures in SKILL.md are tiered")

        # (e) an assumed figure may appear only inside an honesty section
        assumed: set[float] = set()
        for r in rows:
            if r["provenance"].split("+")[0].strip() == "assumed":
                for fig in r["figures"]:
                    v = self.as_float(fig)
                    if v is not None:
                        assumed.add(v)

        for label in ("SKILL.md", "README.md", "EVALS.md"):
            text = self.read(self.FILE_MAP[label])
            if not text:
                continue
            leaked = []
            in_honesty = False
            for line in text.split("\n"):
                if line.startswith("#"):
                    in_honesty = any(h in line.lower() for h in HONESTY_HEADINGS)
                if in_honesty:
                    continue
                for v in self.numbers_in(line):
                    if v in assumed:
                        leaked.append(f"{v} in {line.strip()[:60]!r}")
            if leaked:
                self.fail(
                    "provenance/assumed-containment",
                    f"{label} states an assumed figure outside an honesty section: {leaked[0]}"
                    + (f" (+{len(leaked)-1} more)" if len(leaked) > 1 else "")
                    + ". An unmeasured number placed in the argument reads as a finding. Move it "
                      "under the limits section, or qualify it in place as an assumption.",
                )
            else:
                self.ok(f"provenance/assumed-containment/{label}", "no assumed figure in the argument")

    # --- references ------------------------------------------------------------------------
    def check_references(self) -> None:
        missing = set()
        for label, rel in self.FILE_MAP.items():
            text = self.read(rel)
            if not text:
                continue
            for m in re.finditer(r"`?references/([A-Za-z0-9._-]+\.md)`?", text):
                target = self.root / "skills/discipline/references" / m.group(1)
                if not target.exists():
                    missing.add(f"{label} -> references/{m.group(1)}")
        if missing:
            self.fail(
                "references/exist",
                f"pointers to files that are not there: {', '.join(sorted(missing))}. A dead "
                "reference renders as a plain path and nothing warns; the reader concludes the "
                "depth was never written.",
            )
        else:
            self.ok("references/exist", "every referenced file resolves")

    def run(self) -> int:
        block = self.check_blocks()
        if block:
            self.check_ceiling(block)
            self.check_literal_purity(block)
            self.check_register(block)
            self.check_floors(block)
        rows = self.parse_registry()
        if rows:
            self.check_provenance(rows)
        self.check_references()

        if self.verbose:
            for p in self.passes:
                print(f"  ok    {p}")
        for w in self.warnings:
            print(f"  warn  {w}", file=sys.stderr)
        for f in self.failures:
            print(f"  FAIL  {f}")

        n_ok, n_fail = len(self.passes), len(self.failures)
        print(f"\n{self.root}: {n_ok} passed, {n_fail} failed, {len(self.warnings)} warning(s)")
        return 1 if n_fail else 0


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv or "-v" in argv
    positional = [a for a in argv[1:] if not a.startswith("-")]
    root = Path(positional[0]).resolve() if positional else Path(__file__).resolve().parents[3]
    if not (root / "skills").is_dir():
        print(f"{root} does not look like the plugin root (no skills/ directory)", file=sys.stderr)
        return 2
    return Gate(root, verbose).run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
