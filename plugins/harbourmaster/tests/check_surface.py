#!/usr/bin/env python3
"""Fail when instruction text references a harbourmaster script argument that
does not exist.

The defect class this guards: `berths.py` parses only `--quiet` and silently
ignores everything else, so an instruction like `berths.py claim --weight 4`
spawns a read that exits 0 — no lock taken, nothing recorded, success
reported. Berths are acquired by `governor-run`, which holds the flock around
the child it execs. A phantom argument in a skill or reference is invisible at
runtime by construction, so the only place it can fail loudly is a check like
this one.

Two directions, so the table cannot lie in either:

  1. The declared surface below is verified against each script's source —
     a flag listed here but absent from the source fails the run, so the
     table cannot drift ahead of what the scripts accept.
  2. Every tracked instruction file is scanned for invocations of the five
     uniquely named scripts; a bare-word subcommand (none of them has any)
     or an undeclared flag fails, with file:line and the offending token.

Not checked, deliberately: `ledger.py` — warrant carries a script of the same
name with a different surface, and a filename match cannot tell them apart.
Also not caught: a phantom subcommand named in running prose with no
invocation shape around it ("run berths.py claim before starting"); phantom
flags are validated everywhere, but a bare word counts as a subcommand only
when the name is invoked — at line start, after a path prefix, a quote, a
backtick, or an interpreter word — because in comments and docstrings the
word after a script's name is nearly always English.

Usage: check_surface.py [--root DIR]
  --root defaults to the repository containing this file. Set
  HARBOURMASTER_SCRIPTS_DIR to verify the surface against a different
  scripts directory (the gate test uses this to prove direction 1 fires).

Exit 0 clean, 1 on findings, 2 when the guard itself is misconfigured.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# What each script actually accepts. berths.py and pressure.py parse sys.argv
# by hand, the rest use argparse; either way every flag here must appear as a
# literal in the script's source, and that is asserted before any scanning.
SURFACE: dict[str, dict[str, set[str]]] = {
    "berths.py":    {"flags": {"--quiet"}, "subcommands": set()},
    "pressure.py":  {"flags": {"--max-age", "--fresh", "--no-cache"},
                     "subcommands": set()},
    "governor-run": {"flags": {"--weight", "--project", "--label", "--wait",
                               "--qos", "--dry-run"}, "subcommands": set()},
    "demote.py":    {"flags": {"--apply", "--min-cpu", "--max",
                               "--include-agents", "--restore"},
                     "subcommands": set()},
    "thermal.py":   {"flags": {"--duration", "--check"}, "subcommands": set()},
}
# Accepted everywhere and not required to appear in source.
UNIVERSAL = {"--help", "-h"}

NAME_RE = re.compile(
    r"(?<![A-Za-z0-9_-])(berths\.py|pressure\.py|governor-run|demote\.py|thermal\.py)(?![A-Za-z0-9_-])"
)
SCAN_EXTS = {".md", ".sh", ".zsh", ".bash", ".py", ".mjs", ".js", ".ts",
             ".json", ".txt", ".yaml", ".yml"}
CODE_EXTS = {".sh", ".zsh", ".bash", ".py", ".mjs", ".js", ".ts"}
# Generated or self-referential paths the scan must not read.
EXCLUDE = ("plugins/harbourmaster/tests/", "site/lib/catalogue.json")

STOP_TOKENS = {"|", "#", ";", "&&", "||", "--", ">", ">>", "<", "2>", "1>"}
STRIP = "`'\"),.;:]}"


def verify_surface(scripts_dir: Path) -> list[str]:
    problems = []
    for name, surface in SURFACE.items():
        path = scripts_dir / name
        if not path.is_file():
            problems.append(f"{path}: script missing — surface cannot be verified")
            continue
        source = path.read_text(errors="replace")
        for flag in surface["flags"]:
            if flag not in source:
                problems.append(
                    f"{name}: declared flag {flag} not found in {path} — "
                    "the surface table has drifted from the script")
    return problems


def tracked_files(root: Path) -> list[Path]:
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                             capture_output=True, text=True, check=True)
        rel = [p for p in out.stdout.split("\0") if p]
    except (subprocess.CalledProcessError, OSError):
        rel = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    keep = []
    for r in rel:
        if any(r.startswith(e) or r == e.rstrip("/") for e in EXCLUDE):
            continue
        if Path(r).suffix.lower() in SCAN_EXTS:
            keep.append(root / r)
    return keep


def in_inline_code(line: str, pos: int) -> bool:
    return line[:pos].count("`") % 2 == 1


INTERPRETERS = {"python3", "python", "exec", "sudo", "env", "time",
                "sh", "bash", "zsh", "command"}


def invocation_shaped(line: str, start: int) -> bool:
    """Whether the name at `start` sits where a command would: line start,
    after a path prefix, an opening quote or backtick, or an interpreter."""
    prefix = line[:start].rstrip()
    if not prefix or prefix[-1] in "`'\"/=(":
        return True
    return prefix.split()[-1] in INTERPRETERS


def scan_line(name: str, line: str, name_start: int, name_end: int,
              code_context: bool, md_inline: bool) -> list[tuple[str, str]]:
    """Findings for one occurrence: (kind, token)."""
    rest = line[name_end:]
    subcommand_position = invocation_shaped(line, name_start)
    # A closing quote may sit between the name and its arguments:
    #   "$SKILL_DIR/demote.py" --apply
    # What follows it can equally be prose ("$HM/governor-run" at the weights
    # your skill gives), so past a closing quote only flags are validated.
    if rest[:1] in {'"', "'"}:
        rest = rest[1:]
        subcommand_position = False
    elif rest[:1] == "`":
        # In markdown prose the backtick ends the code span; what follows is
        # English. In fenced or script code it is a template delimiter and the
        # next character decides.
        if md_inline:
            return []
        rest = rest[1:]
        subcommand_position = False
    if rest and rest[0] not in " \t":
        return []  # punctuation directly after the name: not an invocation
    findings = []
    first = True
    for raw in rest.split():
        token = raw.strip(STRIP).lstrip("`'\"([{")
        if not token or token in STOP_TOKENS or token[0] in "|#;<>$":
            break
        if ">" in token or "<" in token:
            break  # a redirection ends the argument run
        if token.startswith("--"):
            flag = token.split("=", 1)[0]
            if flag == "--":
                break
            if flag not in SURFACE[name]["flags"] and flag not in UNIVERSAL:
                findings.append(("phantom flag", flag))
            first = False
            continue
        if token.startswith("-") and len(token) > 1:
            if code_context and token not in UNIVERSAL:
                findings.append(("phantom flag", token))
            first = False
            continue
        if not (token[0].isalnum() or token[0] in "-_"):
            break  # em-dashes, ellipses and the like are prose, not arguments
        # Bare word. Directly after an invoked name it claims to be a
        # subcommand; anywhere else it is English or a flag's value.
        if first and code_context and subcommand_position:
            if token not in SURFACE[name]["subcommands"]:
                findings.append(("phantom subcommand", token))
            first = False
            continue
        if not code_context or (first and not subcommand_position):
            break
        first = False  # a value for the preceding flag; keep walking
    return findings


def scan_file(path: Path) -> list[str]:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return []
    is_md = path.suffix.lower() == ".md"
    is_code_file = path.suffix.lower() in CODE_EXTS
    findings = []
    fenced = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if is_md and line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        for m in NAME_RE.finditer(line):
            name = m.group(1)
            md_inline = is_md and not fenced and in_inline_code(line, m.start())
            code_context = is_code_file or (is_md and (fenced or md_inline))
            for kind, token in scan_line(name, line, m.start(), m.end(),
                                         code_context, md_inline):
                findings.append(
                    f"{path}:{lineno}: `{name} {token}` — {kind}; "
                    f"{name} accepts "
                    f"{sorted(SURFACE[name]['flags']) or 'no flags'} and "
                    f"{'no subcommands' if not SURFACE[name]['subcommands'] else sorted(SURFACE[name]['subcommands'])}")
    return findings


def main() -> int:
    argv = sys.argv[1:]
    root = Path(__file__).resolve().parents[3]
    if "--root" in argv:
        i = argv.index("--root")
        if i + 1 >= len(argv):
            print("check_surface.py: --root needs a value", file=sys.stderr)
            return 2
        root = Path(argv[i + 1]).resolve()
    scripts_dir = Path(os.environ.get(
        "HARBOURMASTER_SCRIPTS_DIR",
        Path(__file__).resolve().parent.parent / "skills/harbourmaster/scripts"))

    problems = verify_surface(scripts_dir)
    if problems:
        print("surface verification failed — fix the table before trusting a scan:",
              file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 2

    findings: list[str] = []
    for path in tracked_files(root):
        findings.extend(scan_file(path))
    if findings:
        print("phantom script arguments in instruction text — these are "
              "silently ignored at runtime and read as success:")
        for f in findings:
            print(f"  {f}")
        return 1
    print(f"clean: no phantom arguments for {sorted(SURFACE)} under {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
