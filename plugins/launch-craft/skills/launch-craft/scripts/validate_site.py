#!/usr/bin/env python3
"""
validate_site.py - Deterministic validation gate for launch-craft marketing sites.
Checks:
- Zero em dashes (—)
- 5-platform coverage (Windows, Mac, iPad, iPhone, Linux)
- Pricing references ($9.99, $4.99)
- Interactive features (GSAP / Three.js)
"""

import sys
import os
import re

def validate_html(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    errors = []

    # 1. Em dash check
    if "—" in content:
        lines_with_emdash = [i+1 for i, l in enumerate(content.splitlines()) if "—" in l]
        errors.append(f"Em dash (—) found on lines: {lines_with_emdash[:5]}")

    # 2. Platform checks
    platforms = ["windows", "mac", "ipad", "iphone", "linux"]
    missing_platforms = [p for p in platforms if p not in content.lower()]
    if missing_platforms:
        errors.append(f"Missing required platform coverage: {', '.join(missing_platforms)}")

    # 3. Pricing checks
    if "9.99" not in content or "4.99" not in content:
        errors.append("Pricing mismatch: Expected dual pricing references ($9.99 and $4.99) in markup.")

    # 4. GSAP & Three.js presence
    if "gsap" not in content.lower():
        errors.append("GSAP animation library not referenced in markup.")
    if "three" not in content.lower() and "<canvas" not in content.lower():
        errors.append("Three.js or WebGL canvas element not referenced in markup.")

    if errors:
        print(f"Validation FAILED for {file_path}:", file=sys.stderr)
        for err in errors:
            print(f"  [ERROR] {err}", file=sys.stderr)
        return 1

    print(f"Validation PASSED for {file_path}: All quality gates met (exit 0).")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_site.py <path-to-html-file>", file=sys.stderr)
        sys.exit(1)
    sys.exit(validate_html(sys.argv[1]))
