#!/usr/bin/env python3
"""Mutation survival: measure the suite's fault sensitivity before trusting it.

Every downstream verdict inherits the suite's ability to notice a fault, and a
green suite can have very little of it -- more than half of over 15,000 generated
mutants survived a rigorous unit, integration and system suite that was passing.
Nobody has measured this for browser suites at all, which is why it is measured
here rather than assumed.

The mutation set is small and deterministic on purpose: comparison-operator
flips, boolean-literal flips, arithmetic-operator swaps, off-by-one on integer
literals, and removal of an await. No randomness, so two runs on one tree give
one answer.

Three properties worth knowing before reading the score:

- Nothing is ever mutated in the working tree. A sandbox is built beside it and
  the test command runs there. In the default sparse mode the sandbox is a
  symlink mirror with real directories only along the path to each target, so a
  large monorepo costs a few symlinks rather than a copy; --copy-mode full
  copies instead, minus the usual build and dependency directories.
- Strings and comments are masked before any mutation is generated, because a
  flipped operator inside a comment is not a fault and a suite that fails to
  notice it is not insensitive. Operators are also only mutated where the
  surrounding whitespace makes their meaning unambiguous, which keeps TypeScript
  generics and regex literals out of the set: a mutant that merely fails to
  compile reads as killed and inflates the score.
- The baseline is run first. A suite that is already red would score every
  mutant as killed while looking excellent, so a red baseline is a refusal to
  measure (exit 1) rather than a result.

The score is ratcheted in .warrant/suite-health.json: it may rise, and a drop
below the recorded high-water mark exits 2.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Iterable

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402

MASKED = "\x00"
DEFAULT_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py")
SKIP_DIRS = frozenset((".git", "node_modules", ".next", "dist", "build", "coverage",
                       ".warrant", "__pycache__", ".venv", "venv"))
COPY_IGNORE = shutil.ignore_patterns(*SKIP_DIRS)

# Longest first: === must be seen before ==, or the mutant is generated twice.
_COMPARISONS: tuple[tuple[str, str], ...] = (
    ("===", "!=="), ("!==", "==="), ("==", "!="), ("!=", "=="),
    ("<=", ">"), (">=", "<"), ("<", ">="), (">", "<="),
)
_BOOLEANS = {"true": "false", "false": "true", "True": "False", "False": "True"}
_ARITHMETIC = {"+": "-", "-": "+", "*": "/", "/": "*"}

_BOOL_RE = re.compile(r"(?<![\w$.])(true|false|True|False)(?![\w$])")
_INT_RE = re.compile(r"(?<![\w$.])(\d+)(?![\w$.])")
_AWAIT_RE = re.compile(r"(?<![\w$])await\s+")


# -- masking ------------------------------------------------------------------

def _regex_end(text: str, start: int) -> int:
    """End of a regex literal starting at start, or -1 if it is not one.

    A regex body may contain quotes, backticks and unbalanced parentheses, so
    leaving them unmasked is not a cosmetic problem: one .replace(/[#>*`_]/g, ' ')
    convinced the masker it had entered a template literal and masked the whole
    rest of the file, which read as a spec with no assertions in it.
    """
    i = start + 1
    in_class = False
    while i < len(text):
        char = text[i]
        if char == "\\":
            i += 2
            continue
        if char == "\n":
            return -1                            # regex literals do not span lines
        if in_class:
            if char == "]":
                in_class = False
        elif char == "[":
            in_class = True
        elif char == "/":
            i += 1
            while i < len(text) and text[i].isalpha():
                i += 1                           # flags
            return i
        i += 1
    return -1


def mask_noncode(text: str, ext: str = ".ts") -> str:
    """Return text with comment, string and regex bodies replaced by NULs.

    Same length as the input and newlines preserved, so an offset into the mask
    is an offset into the original and line numbers still work. Shared with
    cannotfail_scan.py, which needs the same distinction for the same reason.
    """
    py = ext == ".py"
    out = list(text)
    n = len(text)

    def blank(start: int, stop: int) -> None:
        for k in range(start, min(stop, n)):
            if out[k] != "\n":
                out[k] = MASKED

    i = 0
    while i < n:
        two, three = text[i:i + 2], text[i:i + 3]
        if py and text[i] == "#":
            j = text.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
            continue
        if not py and two == "//":
            j = text.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
            continue
        if not py and two == "/*":
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(i, j)
            i = j
            continue
        if py and three in ('"""', "'''"):
            j = text.find(three, i + 3)
            j = n if j < 0 else j + 3
            blank(i, j)
            i = j
            continue
        if not py and text[i] == "/":
            # A slash is a regex only where a value cannot have just ended;
            # after an identifier, a closing bracket or a masked literal it is
            # division. A masked char counts as a value because it was one.
            prev = next((out[k] for k in range(i - 1, -1, -1) if not text[k].isspace()), "")
            if not (prev.isalnum() or prev in "_$)]" or prev == MASKED):
                j = _regex_end(text, i)
                if j > 0:
                    blank(i, j)
                    i = j
                    continue
        if text[i] in ("'", '"') or (not py and text[i] == "`"):
            quote, j = text[i], i + 1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                if text[j] == "\n" and quote != "`":
                    break                        # unterminated; do not eat the file
                j += 1
            blank(i, j)
            i = j
            continue
        i += 1
    return "".join(out)


# -- mutation generation ------------------------------------------------------

def _spaced(mask: str, start: int, length: int) -> bool:
    """True when both neighbours are whitespace.

    The guard that keeps TypeScript generics (Array<string>), arrows (=>),
    increments (i++) and regex literals (/ab/g) out of the mutation set. Those
    mutants would not compile, and a mutant that cannot compile reads as killed
    however blind the suite is.
    """
    before = mask[start - 1] if start > 0 else " "
    after = mask[start + length] if start + length < len(mask) else " "
    return before in " \t" and after in " \t"


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _mutant(kind: str, path: str, text: str, offset: int, length: int,
            replacement: str) -> dict[str, Any]:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    line_end = len(text) if line_end < 0 else line_end
    return {
        "kind": kind,
        "file": path,
        "line": _line_of(text, offset),
        "offset": offset,
        "length": length,
        "before": text[offset:offset + length],
        "after": replacement,
        "context": text[line_start:line_end].strip()[:120],
    }


def generate(text: str, path: str, ext: str = ".ts") -> list[dict[str, Any]]:
    """Every mutation this harness knows how to make in one file, in file order."""
    mask = mask_noncode(text, ext)
    mutants: list[dict[str, Any]] = []

    i = 0
    while i < len(mask):
        for op, replacement in _COMPARISONS:
            if not mask.startswith(op, i):
                continue
            if len(op) == 1 and not _spaced(mask, i, 1):
                break                            # ambiguous single char; leave it alone
            if len(op) == 1 and mask[i - 1:i + 1] in ("=>", "<<", ">>"):
                break
            mutants.append(_mutant("comparison", path, text, i, len(op), replacement))
            i += len(op) - 1
            break
        i += 1

    for match in _BOOL_RE.finditer(mask):
        mutants.append(_mutant("boolean", path, text, match.start(),
                               len(match.group(1)), _BOOLEANS[match.group(1)]))

    for index, char in enumerate(mask):
        if char not in _ARITHMETIC or not _spaced(mask, index, 1):
            continue
        if char == "/":
            # Only where a division can be: after something an expression can end
            # with. A regex literal never follows one of those.
            prev = mask[:index].rstrip()
            if not prev or not (prev[-1].isalnum() or prev[-1] in "_)]"):
                continue
        mutants.append(_mutant("arithmetic", path, text, index, 1, _ARITHMETIC[char]))

    for match in _INT_RE.finditer(mask):
        mutants.append(_mutant("offbyone", path, text, match.start(),
                               len(match.group(1)), str(int(match.group(1)) + 1)))

    for match in _AWAIT_RE.finditer(mask):
        mutants.append(_mutant("await_removal", path, text, match.start(),
                               match.end() - match.start(), ""))

    mutants.sort(key=lambda m: (m["file"], m["offset"], m["kind"]))
    return mutants


def apply_mutation(text: str, mutant: dict[str, Any]) -> str:
    return text[:mutant["offset"]] + mutant["after"] + text[mutant["offset"] + mutant["length"]:]


def sample(mutants: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Round-robin across kinds so a cap cannot silence a whole mutation kind."""
    if limit <= 0 or len(mutants) <= limit:
        return list(mutants)
    buckets: dict[str, list[dict[str, Any]]] = {}
    for mutant in mutants:
        buckets.setdefault(mutant["kind"], []).append(mutant)
    order = sorted(buckets)
    chosen: list[dict[str, Any]] = []
    index = 0
    while len(chosen) < limit:
        progressed = False
        for kind in order:
            if index < len(buckets[kind]) and len(chosen) < limit:
                chosen.append(buckets[kind][index])
                progressed = True
        if not progressed:
            break
        index += 1
    chosen.sort(key=lambda m: (m["file"], m["offset"], m["kind"]))
    return chosen


# -- targets and sandbox ------------------------------------------------------

def resolve_targets(values: Iterable[str], root: pathlib.Path,
                    exts: tuple[str, ...]) -> list[pathlib.Path]:
    """Each --targets value: a source file, a directory to walk, or a list file."""
    found: list[pathlib.Path] = []
    for value in values:
        path = pathlib.Path(value).expanduser()
        if not path.is_absolute():
            path = (root / path)
        path = path.resolve()
        if not path.exists():
            raise _state.Absent(str(path))
        if path.is_dir():
            found.extend(p.resolve() for p in sorted(path.rglob("*"))
                         if p.is_file() and p.suffix in exts and not (SKIP_DIRS & set(p.parts)))
        elif path.suffix in (".txt", ".list", ".lst"):
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                listed = (root / line).resolve() if not pathlib.Path(line).is_absolute() \
                    else pathlib.Path(line).resolve()
                if not listed.exists():
                    raise _state.Absent(str(listed))
                found.append(listed)
        else:
            found.append(path)
    # Stable, de-duplicated.
    return sorted(dict.fromkeys(found))


def build_sandbox(root: pathlib.Path, targets: list[pathlib.Path],
                  sandbox: pathlib.Path, mode: str) -> None:
    """Materialise a tree the test command can run in without touching the tree."""
    root = root.resolve()
    targets = [t.resolve() for t in targets]
    if mode == "full":
        shutil.copytree(root, sandbox, ignore=COPY_IGNORE, symlinks=True, dirs_exist_ok=True)
        return

    relatives = [t.relative_to(root) for t in targets]
    real_dirs = {pathlib.PurePath(".")}
    for rel in relatives:
        for parent in rel.parents:
            real_dirs.add(parent)

    def mirror(src: pathlib.Path, dst: pathlib.Path) -> None:
        dst.mkdir(parents=True, exist_ok=True)
        for entry in sorted(src.iterdir()):
            rel = entry.relative_to(root)
            if entry.is_dir() and pathlib.PurePath(rel) in real_dirs:
                mirror(entry, dst / entry.name)
            elif rel in relatives:
                shutil.copyfile(entry, dst / entry.name)      # the file that gets mutated
            else:
                # Everything else, directories included, is borrowed rather than
                # copied: the sandbox needs to resolve it, not own it.
                (dst / entry.name).symlink_to(entry)

    mirror(root, sandbox)


def run_command(command: str, cwd: pathlib.Path, timeout: float,
                use_shell: bool) -> tuple[int | None, str, str]:
    try:
        completed = subprocess.run(
            command if use_shell else shlex.split(command),
            cwd=str(cwd), shell=use_shell, timeout=timeout,
            capture_output=True, text=True, check=False)
    except subprocess.TimeoutExpired:
        return None, "", f"timed out after {timeout}s"
    return completed.returncode, completed.stdout[-400:], completed.stderr[-400:]


# -- the harness --------------------------------------------------------------

def measure(root: pathlib.Path, targets: list[pathlib.Path], test_cmd: str,
            limit: int, timeout: float, copy_mode: str,
            use_shell: bool) -> dict[str, Any]:
    """Build a sandbox, run the baseline, then one mutant at a time."""
    root = root.resolve()
    targets = [t.resolve() for t in targets]
    originals = {t: t.read_text() for t in targets}
    generated: list[dict[str, Any]] = []
    for target in targets:
        generated.extend(generate(originals[target], str(target.relative_to(root)),
                                  target.suffix))
    chosen = sample(generated, limit)

    with tempfile.TemporaryDirectory(prefix="warrant-mutate-") as tmp:
        sandbox = pathlib.Path(tmp) / "sandbox"
        build_sandbox(root, targets, sandbox, copy_mode)

        code, out, err = run_command(test_cmd, sandbox, timeout, use_shell)
        if code != 0:
            return {
                "baseline": {"exit_code": code, "stdout_tail": out, "stderr_tail": err},
                "baseline_green": False,
                "generated": len(generated),
                "run": 0, "killed": 0, "survived": 0, "timed_out": 0,
                "score": None, "by_mutation_kind": {}, "mutants": [],
                "sandbox_mode": copy_mode,
            }

        results: list[dict[str, Any]] = []
        for mutant in chosen:
            path = sandbox / mutant["file"]
            source = originals[root / mutant["file"]]
            path.write_text(apply_mutation(source, mutant))
            code, out, err = run_command(test_cmd, sandbox, timeout, use_shell)
            path.write_text(source)
            status = "timeout" if code is None else ("survived" if code == 0 else "killed")
            results.append({**mutant, "status": status, "exit_code": code,
                            "stdout_tail": out, "stderr_tail": err})

    killed = sum(1 for r in results if r["status"] in ("killed", "timeout"))
    timed_out = sum(1 for r in results if r["status"] == "timeout")
    survived = sum(1 for r in results if r["status"] == "survived")
    by_kind: dict[str, dict[str, Any]] = {}
    for result in results:
        bucket = by_kind.setdefault(result["kind"], {"run": 0, "killed": 0, "survived": 0})
        bucket["run"] += 1
        bucket["killed" if result["status"] in ("killed", "timeout") else "survived"] += 1
    for bucket in by_kind.values():
        bucket["score"] = round(bucket["killed"] / bucket["run"], 4) if bucket["run"] else None

    return {
        "baseline_green": True,
        "generated": len(generated),
        "run": len(results),
        "killed": killed,
        "survived": survived,
        "timed_out": timed_out,
        "score": round(killed / len(results), 4) if results else None,
        "by_mutation_kind": by_kind,
        "mutants": results,
        "sandbox_mode": copy_mode,
    }


def apply_ratchet(path: pathlib.Path, score: float | None, stamp: str,
                  tolerance: float, killed: int = 0, run: int = 0) -> tuple[dict[str, Any], str, bool]:
    """Judge the score against the recorded mark and return the record to write."""
    health = _state.read_json(path, default={}) if path.exists() else {}
    previous = health.get("mutation", {})
    high_water = previous.get("high_water")
    verdict, regressed = "recorded", False

    if score is None:
        verdict = "no score to record"
    elif high_water is None:
        high_water, verdict = score, "first mark set"
    elif score > high_water:
        high_water, verdict = score, "mark raised"
    elif score < high_water - tolerance:
        verdict, regressed = "below the recorded mark", True
    else:
        verdict = "mark held"

    mutation = {
        "score": score,
        # Both parts of the score travel with it: a rate whose population is
        # elsewhere is a rate a later reader will misread.
        "killed": killed,
        "run": run,
        "high_water": high_water,
        "high_water_at": stamp if verdict in ("first mark set", "mark raised")
        else previous.get("high_water_at", stamp),
        "run_at": stamp,
        "verdict": verdict,
    }
    history = list(previous.get("history", []))
    history.append({"at": stamp, "score": score, "high_water": high_water})
    mutation["history"] = history
    # Merge: other planes write their own keys into this file.
    return {**health, "mutation": mutation}, verdict, regressed


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    if not args.targets or not args.test_cmd:
        _cli.say(args, "--targets and --test-cmd are both required")
        return _cli.ERROR

    exts = tuple(e if e.startswith(".") else f".{e}" for e in args.ext.split(","))
    targets = resolve_targets(args.targets, root, exts)
    targets = [t for t in targets if root in t.parents or t.parent == root
               or str(t).startswith(str(root))]
    if not targets:
        _cli.say(args, "no target files resolved under --root")
        return _cli.MISSING

    result = measure(root, targets, args.test_cmd, args.max_mutants,
                     args.timeout, args.copy_mode, args.shell)
    result["targets"] = [str(t.relative_to(root)) for t in targets]
    result["generated_at"] = _cli.now(args).isoformat()

    if not result["baseline_green"]:
        _cli.say(args, "the suite fails before any mutation is applied, so every mutant "
                       "would read as killed; fix the baseline before measuring")
        _cli.say(args, f"  baseline exit {result['baseline']['exit_code']}: "
                       f"{result['baseline']['stderr_tail'].strip()[:200]}")
        _cli.emit(args, result)
        return _cli.ERROR

    stamp = _cli.now(args).isoformat()
    regressed = False
    if args.no_write:
        result["ratchet"] = "not recorded (--no-write)"
    else:
        # The state directory is created only on the writing path, so a dry run
        # leaves nothing behind.
        out = _state.state_dir(root, create=True) / "suite-health.json"
        health, verdict, regressed = apply_ratchet(out, result["score"], stamp, args.tolerance,
                                                   result["killed"], result["run"])
        result["ratchet"] = verdict
        result["high_water"] = health["mutation"]["high_water"]
        try:
            _state.write_json(out, health)
            result["written_to"] = str(out)
        except OSError as exc:
            # The mutants have already been run; losing the record is reportable,
            # not raisable, because a retry would spend the whole run again.
            result["written_to"] = None
            result["write_error"] = f"{type(exc).__name__}: {exc}"
            _cli.say(args, f"could not write {out}: {exc}")

    _cli.say(args, f"{result['generated']} mutant(s) generated from {len(targets)} target(s), "
                   f"{result['run']} run in a {args.copy_mode} sandbox")
    _cli.say(args, "killed: " + _cli.rate(result["killed"], result["run"], "mutants run")
                   + (f", {result['timed_out']} by timeout" if result["timed_out"] else ""))
    for kind, bucket in sorted(result["by_mutation_kind"].items()):
        _cli.say(args, f"  {kind}: " + _cli.rate(bucket["killed"], bucket["run"], "killed"))
    for mutant in result["mutants"]:
        if mutant["status"] == "survived":
            _cli.say(args, f"  SURVIVED {mutant['kind']} {mutant['file']}:{mutant['line']} "
                           f"{mutant['before']!r} -> {mutant['after']!r}  [{mutant['context']}]")
    _cli.say(args, f"ratchet: {result['ratchet']}"
                   + (f" (mark {result.get('high_water')})" if not args.no_write else ""))
    _cli.emit(args, result)
    return _cli.FAILED if regressed else _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--targets", action="append", default=[],
                   help="a source file, a directory to walk, or a .txt/.list of paths "
                        "(repeatable)")
    p.add_argument("--test-cmd", help="command run inside the sandbox; nonzero means killed")
    p.add_argument("--ext", default=",".join(DEFAULT_EXTS),
                   help="extensions to mutate when a target is a directory")
    p.add_argument("--max-mutants", type=int, default=25,
                   help="cap on mutants run, sampled round-robin across kinds (0 = no cap)")
    p.add_argument("--timeout", type=float, default=300.0,
                   help="per-mutant seconds; a timeout counts as killed and is reported apart")
    p.add_argument("--copy-mode", choices=("sparse", "full"), default="sparse",
                   help="sparse symlink mirror (default) or a full copy of --root")
    p.add_argument("--shell", action="store_true",
                   help="run --test-cmd through a shell instead of argv-splitting it")
    p.add_argument("--tolerance", type=float, default=0.0,
                   help="how far below the high-water mark is tolerated before exit 2")
    p.add_argument("--no-write", action="store_true",
                   help="measure without touching .warrant/suite-health.json")


def selftest() -> list[tuple[str, bool]]:
    """Generation observed both firing and correctly declining, then real runs."""
    import contextlib
    import io
    import json

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay" / "mutate")
    spans = (fx / "spans.ts").read_text()
    mutants = generate(spans, "spans.ts", ".ts")
    kinds = {m["kind"] for m in mutants}

    cases.append(("every mutation kind is generated where the pattern is present",
                  kinds == {"comparison", "boolean", "arithmetic", "offbyone", "await_removal"}))
    cases.append(("a comparison flip is generated on real code",
                  any(m["kind"] == "comparison" and m["before"] == "===" for m in mutants)))
    cases.append(("an await removal is generated",
                  any(m["kind"] == "await_removal" for m in mutants)))
    cases.append(("an integer literal is incremented",
                  any(m["kind"] == "offbyone" and m["before"] == "3" and m["after"] == "4"
                      for m in mutants)))
    cases.append(("a boolean literal is flipped",
                  any(m["kind"] == "boolean" and m["before"] == "true" for m in mutants)))

    # The same tokens inside the comment and the string must yield nothing.
    mask = mask_noncode(spans, ".ts")
    cases.append(("no mutation offset lands in a masked region",
                  all(MASKED not in mask[m["offset"]:m["offset"] + max(m["length"], 1)]
                      for m in mutants)))
    comment_line = next(i for i, line in enumerate(spans.splitlines(), 1)
                        if "The comment below is the trap" in line)
    string_line = next(i for i, line in enumerate(spans.splitlines(), 1)
                       if "const label" in line)
    cases.append(("nothing is mutated inside a comment",
                  not any(m["line"] == comment_line for m in mutants)))
    cases.append(("nothing is mutated inside a string literal",
                  not any(m["line"] == string_line for m in mutants)))

    # The ambiguity guards, each seen declining and seen allowing.
    generics = generate("const xs: Array<string> = []; const n = a < b;", "g.ts", ".ts")
    cases.append(("a generic bracket is not read as a comparison",
                  [m["before"] for m in generics if m["kind"] == "comparison"] == ["<"]))
    arrows = generate("items.map((x) => x); const ok = a >= b;", "g.ts", ".ts")
    cases.append(("an arrow is not read as a comparison",
                  [m["before"] for m in arrows if m["kind"] == "comparison"] == [">="]))
    regexes = generate("const re = /ab/g; const half = total / 2;", "g.ts", ".ts")
    cases.append(("a regex literal is not read as division",
                  [m["before"] for m in regexes if m["kind"] == "arithmetic"] == ["/"]))
    increments = generate("i++; const n = a + b;", "g.ts", ".ts")
    cases.append(("an increment is not read as addition",
                  [m["before"] for m in increments if m["kind"] == "arithmetic"] == ["+"]))
    decimals = generate("const rate = 1.5; const n = 7;", "g.ts", ".ts")
    cases.append(("a decimal is not split into an off-by-one",
                  [m["before"] for m in decimals if m["kind"] == "offbyone"] == ["7"]))
    cases.append(("python comments and booleans are handled by extension",
                  {m["before"] for m in generate("# true\nflag = True\n", "g.py", ".py")}
                  == {"True"}))

    # Regex literals are masked; division is not.
    inside = generate("if (/a+b/.test(s)) { const n = 1; }", "g.ts", ".ts")
    cases.append(("nothing inside a regex literal is mutated",
                  all(m["kind"] != "arithmetic" for m in inside)))
    cases.append(("a division beside a regex is still mutated",
                  any(m["kind"] == "arithmetic" and m["before"] == "/"
                      for m in generate("const r = /a/g; const half = total / 2;", "g.ts", ".ts"))))
    swallower = "const s = x.replace(/[#>*`_]/g, ' ');\nconst ok = a === b;\n"
    cases.append(("a regex holding a backtick does not swallow the rest of the file",
                  any(m["kind"] == "comparison" for m in generate(swallower, "g.ts", ".ts"))))

    text = "const ok = a === b;"
    one = generate(text, "g.ts", ".ts")[0]
    cases.append(("applying a mutation changes exactly the matched span",
                  apply_mutation(text, one) == "const ok = a !== b;" and text == "const ok = a === b;"))

    capped = sample(mutants, 3)
    cases.append(("a cap samples across kinds rather than truncating",
                  len(capped) == 3 and len({m['kind'] for m in capped}) == 3))
    cases.append(("no cap keeps everything", len(sample(mutants, 0)) == len(mutants)))

    # -- real runs against the fixture project
    project = fx / "project"
    calc = project / "src" / "calc.py"
    before_bytes = calc.read_bytes()
    result = measure(project, [calc], "python3 -B run_tests.py", 0, 60.0, "sparse", False)
    cases.append(("the baseline is checked and green", result["baseline_green"] is True))
    cases.append(("mutants are killed", result["killed"] > 0))
    cases.append(("mutants survive where no test looks", result["survived"] > 0))
    cases.append(("the score is killed over run",
                  result["score"] == round(result["killed"] / result["run"], 4)))
    cases.append(("by_mutation_kind carries both parts of its rate",
                  all(b["killed"] + b["survived"] == b["run"]
                      for b in result["by_mutation_kind"].values())))
    # calc.py: total() is lines 10-15 and every test exercises it; forecast() is
    # lines 18-21 and nothing calls it.
    covered = [m for m in result["mutants"] if m["line"] <= 15]
    uncovered = [m for m in result["mutants"] if m["line"] >= 18]
    cases.append(("every mutant in the covered function is killed",
                  bool(covered) and all(m["status"] == "killed" for m in covered)))
    cases.append(("every mutant in the untested function survives",
                  bool(uncovered) and all(m["status"] == "survived" for m in uncovered)))
    cases.append(("the working tree file is untouched", calc.read_bytes() == before_bytes))
    cases.append(("the suite ran against the sandbox copy, not the fixture",
                  all("warrant-mutate-" in m["stdout_tail"] for m in result["mutants"])))

    # A red baseline is a refusal to measure, not a perfect score.
    with tempfile.TemporaryDirectory() as tmp:
        broken = pathlib.Path(tmp) / "project"
        shutil.copytree(project, broken)
        (broken / "run_tests.py").write_text("import sys\nsys.exit(1)\n")
        red = measure(broken, [broken / "src" / "calc.py"], "python3 -B run_tests.py",
                      2, 60.0, "sparse", False)
        cases.append(("a red baseline refuses to score",
                      red["baseline_green"] is False and red["score"] is None))

    # -- the ratchet, both directions, and the merge with other planes' keys
    with tempfile.TemporaryDirectory() as tmp:
        health = pathlib.Path(tmp) / "suite-health.json"
        merged, verdict, regressed = apply_ratchet(health, 0.5, "T0", 0.0, 2, 4)
        cases.append(("a first score sets the mark",
                      verdict == "first mark set" and merged["mutation"]["high_water"] == 0.5
                      and not regressed))
        cases.append(("the recorded score carries its population",
                      merged["mutation"]["killed"] == 2 and merged["mutation"]["run"] == 4))
        _state.write_json(health, {**merged, "cannotfail": {"count": 7}})
        merged, verdict, regressed = apply_ratchet(health, 0.75, "T1", 0.0)
        cases.append(("a higher score raises the mark",
                      verdict == "mark raised" and merged["mutation"]["high_water"] == 0.75))
        cases.append(("another plane's key survives the merge",
                      merged.get("cannotfail") == {"count": 7}))
        _state.write_json(health, merged)
        _, verdict, regressed = apply_ratchet(health, 0.75, "T2", 0.0)
        cases.append(("an equal score holds the mark",
                      verdict == "mark held" and not regressed))
        _, verdict, regressed = apply_ratchet(health, 0.6, "T3", 0.0)
        cases.append(("a lower score is a regression",
                      regressed and verdict == "below the recorded mark"))
        _, _, tolerated = apply_ratchet(health, 0.6, "T4", 0.2)
        cases.append(("--tolerance absorbs a small drop", not tolerated))
        cases.append(("history keeps every run",
                      len(apply_ratchet(health, 0.6, "T5", 0.2)[0]["mutation"]["history"]) == 3))

    # -- through main(), including the exit code the ratchet decides
    def run(argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = _cli.entry("selftest", main, None, _extra, argv)
        return rc, out.getvalue(), err.getvalue()

    with tempfile.TemporaryDirectory() as tmp:
        sandbox_root = pathlib.Path(tmp) / "project"
        shutil.copytree(project, sandbox_root)
        base = ["--root", str(sandbox_root), "--targets", "src/calc.py",
                "--test-cmd", "python3 -B run_tests.py", "--max-mutants", "4", "--json"]
        rc, out, err = run(base)
        payload = json.loads(out)
        cases.append(("a first run exits 0 and records a mark",
                      rc == _cli.OK and payload["high_water"] == payload["score"]))
        cases.append(("the human summary names the surviving mutants",
                      "SURVIVED" in err))
        health = sandbox_root / ".warrant" / "suite-health.json"
        cases.append(("suite-health.json is written", health.exists()))

        # Force a regression: raise the recorded mark above anything achievable.
        stored = json.loads(health.read_text())
        stored["mutation"]["high_water"] = 1.0
        _state.write_json(health, stored)
        rc, _, err = run(base)
        cases.append(("a score below the mark exits 2", rc == _cli.FAILED))
        cases.append(("the failing run says the mark was missed",
                      "below the recorded mark" in err))

        rc, _, _ = run(["--root", str(sandbox_root), "--targets", "src/nope.py",
                        "--test-cmd", "true", "--json"])
        cases.append(("an absent target exits 3", rc == _cli.MISSING))
        rc, _, _ = run(["--root", str(sandbox_root), "--json"])
        cases.append(("missing arguments exit 1, not 2", rc == _cli.ERROR))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
