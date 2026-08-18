#!/usr/bin/env python3
"""Every flag a SKILL.md or reference shows must exist on the script it shows it for.

This gate exists because a skill that documents a flag the script does not have
fails at runtime for everyone who installs it, and no amount of reading the prose
catches it. On this plugin's first build it found thirteen mismatches across five
skills, every one of which would have handed the reader a usage error.

Run from the plugin root:  python3 evals/check_doc_flags.py
Exit 0 when the documentation and the scripts agree.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

COMMON = {"--help", "--root", "--json", "--now", "--selftest"}


def flags_of(script: pathlib.Path) -> set[str]:
    out = subprocess.run([sys.executable, str(script), "--help"],
                         capture_output=True, text=True).stdout
    return set(re.findall(r"--[a-z][a-z0-9-]*", out))


def takes_positional(script: pathlib.Path) -> bool:
    out = subprocess.run([sys.executable, str(script), "--help"],
                         capture_output=True, text=True).stdout
    # argparse prints a "positional arguments:" section only when there are some
    return "positional arguments:" in out.lower()


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    docs = sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("references/*.md"))
    findings: list[str] = []
    checked = 0

    for md in docs:
        for m in re.finditer(r"python3 scripts/([a-z_]+)\.py([^\n`]*)", md.read_text()):
            name, tail = m.group(1), m.group(2)
            script = root / "scripts" / f"{name}.py"
            rel = md.relative_to(root)
            if not script.exists():
                findings.append(f"{rel}: names scripts/{name}.py, which does not exist")
                continue
            checked += 1
            real = flags_of(script)
            for flag in sorted(set(re.findall(r"--[a-z][a-z0-9-]*", tail))):
                if flag not in real:
                    findings.append(f"{rel}: {name}.py has no {flag}")
            # A <placeholder> counts as positional only when no flag precedes it on
            # the line; `--input <x.html>` is a flag's value, not a positional.
            for tok in re.finditer(r"(?:^|\s)(<[a-z][a-z0-9.<>-]*>)", tail):
                before = tail[:tok.start()].rstrip()
                if re.search(r"--[a-z][a-z0-9-]*$", before):
                    continue                      # it is a flag's value, not a positional
                if not takes_positional(script):
                    findings.append(f"{rel}: {name}.py shown with the positional "
                                    f"{tok.group(1)}; it takes flags only")

    for f in sorted(set(findings)):
        print(f"  {f}")
    uniq = len(set(findings))
    print(f"{checked} documented invocation(s) checked, {uniq} mismatch(es)")
    return 1 if uniq else 0


if __name__ == "__main__":
    raise SystemExit(main())
