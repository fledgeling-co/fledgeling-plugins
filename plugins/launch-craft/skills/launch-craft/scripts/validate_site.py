#!/usr/bin/env python3
"""Check explicit source-text requirements in a standalone launch HTML file.

This does not render the page or establish accessibility, support claims,
dependency loading, or interaction behavior.
"""

import argparse
from pathlib import Path
import sys


def validate_html(file_path, required_text=(), forbid_em_dash=False):
    path = Path(file_path)
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Source check FAILED: {error}", file=sys.stderr)
        return 1

    errors = []
    if not content.strip():
        errors.append("The HTML source is empty.")
    if forbid_em_dash and "—" in content:
        lines = [i + 1 for i, line in enumerate(content.splitlines()) if "—" in line]
        errors.append(f"Em dash found on lines: {lines[:5]}")
    for value in required_text:
        if not value.strip():
            errors.append("A required-text value is empty; provide approved copy.")
        elif value not in content:
            errors.append(f"Required source text absent: {value!r}")

    if errors:
        print(f"Source check FAILED for {path}:", file=sys.stderr)
        for error in errors:
            print(f"  [ERROR] {error}", file=sys.stderr)
        return 1

    print(f"Source check PASSED for {path}: readable nonempty source, "
          f"{len(required_text)} required text values, em-dash rule "
          f"{'enabled' if forbid_em_dash else 'not requested'}.")
    print("Not checked: rendered content, WCAG, layout, dependencies, interactions, "
          "or the truth of product, pricing and platform claims.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", help="Standalone HTML source to inspect")
    parser.add_argument("--require-text", action="append", default=[],
                        help="Approved source text that must be present; repeat as needed")
    parser.add_argument("--forbid-em-dash", action="store_true",
                        help="Apply when the selected copy voice forbids em dashes")
    args = parser.parse_args()
    return validate_html(args.html, args.require_text, args.forbid_em_dash)


if __name__ == "__main__":
    sys.exit(main())
