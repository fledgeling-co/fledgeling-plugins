#!/usr/bin/env python3
"""
run_synthesis.py - Inventories conventional project source paths; does not run synthesis.
"""

import os
import sys
import glob
import argparse

def scan_project(root_dir):
    briefs = glob.glob(os.path.join(root_dir, "docs/features-to-triage/*.md"))
    plans = glob.glob(os.path.join(root_dir, "docs/plans/*.md"))
    specs = glob.glob(os.path.join(root_dir, "docs/specs/*.md"))
    mocks = glob.glob(os.path.join(root_dir, "design/mocks/html/*.html")) + glob.glob(os.path.join(root_dir, "mocks/*.html"))
    
    summary = {
        "briefs": len(briefs),
        "plans": len(plans),
        "specs": len(specs),
        "mocks": len(mocks),
        "brief_files": briefs,
        "plan_files": plans,
        "spec_files": specs,
        "mock_files": mocks
    }
    return summary

def main():
    parser = argparse.ArgumentParser(description="Inventory conventional source paths for a later synthesis task; no model is invoked.")
    parser.add_argument("--root", default=".", help="Root directory of the project")
    parser.add_argument("--output-dir", default=".", help="Reserved compatibility option; this inventory helper writes no documents")
    parser.add_argument("--dry-run", action="store_true", help="Print the inventory; this helper never calls a model")
    args = parser.parse_args()

    project_info = scan_project(args.root)
    print(f"Scanned project at {args.root}:")
    print(f"  - Briefs: {project_info['briefs']}")
    print(f"  - Plans: {project_info['plans']}")
    print(f"  - Specs: {project_info['specs']}")
    print(f"  - Mocks: {project_info['mocks']}")

    for category in ("brief_files", "plan_files", "spec_files", "mock_files"):
        for source_path in sorted(project_info[category]):
            print(f"  {category}: {source_path}")
    print("\nInventory only: no file contents read, model invoked or documents generated. "
          "Read these paths and discover any additional project-specific sources before synthesis.")

if __name__ == "__main__":
    main()
