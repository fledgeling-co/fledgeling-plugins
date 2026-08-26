#!/usr/bin/env python3
"""
Evaluation and grading harness for improve-skill.
Executes both baseline (original eli5) and improved (explain-craft) arms across eval prompts,
evaluates structural assertions, and prepares anonymized A/B bundles for blind multi-family judging.
"""

import json
import os
import random
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.resolve()
EVALS_JSON = WORKSPACE / "evals.json"

def load_evals():
    with open(EVALS_JSON, "r") as f:
        return json.load(f)["evals"]

def grade_response(eval_item, response_text):
    """
    Grades deterministic structural assertions on a response text.
    """
    results = []
    # Assertion 1: CSP compliance (0 external img tags)
    has_http_img = "<img " in response_text.lower() and ("http://" in response_text.lower() or "https://" in response_text.lower())
    has_inline_svg_or_canvas = "<svg" in response_text.lower() or "<canvas" in response_text.lower()
    csp_pass = (not has_http_img) and has_inline_svg_or_canvas
    results.append({
        "id": "csp_compliance",
        "passed": csp_pass,
        "evidence": "Found <svg>/<canvas> with 0 external http(s) img tags" if csp_pass else f"Failed: has_http_img={has_http_img}, has_inline_svg_or_canvas={has_inline_svg_or_canvas}"
    })

    # Assertion 2: Analogy & boundary limit
    has_analogy = any(w in response_text.lower() for w in ["analogy", "imagine", "like a", "think of", "metaphor", "mental model"])
    has_limit = any(w in response_text.lower() for w in ["limit", "break down", "breaks down", "boundary", "where this fails", "where this departs", "differs from reality", "trade-off", "not quite like"])
    analogy_pass = has_analogy and has_limit
    results.append({
        "id": "analogy_boundary",
        "passed": analogy_pass,
        "evidence": f"Analogy keyword present: {has_analogy}, Explicit analogy boundary/limit present: {has_limit}"
    })

    # Assertion 3: Interactive simulation / explorable control
    has_interactive = any(w in response_text.lower() for w in ["<button", "<input", "addeventlistener", "onclick", "slider", "stepper", "step ", "simulate", "interactive"])
    has_script = "<script" in response_text.lower()
    interactive_pass = has_interactive and has_script
    results.append({
        "id": "interactive_simulation",
        "passed": interactive_pass,
        "evidence": f"Interactive controls present: {has_interactive}, Script present: {has_script}"
    })

    # Assertion 4: Progressive disclosure / abstraction tiers
    has_progressive = any(w in response_text.lower() for w in ["gist", "intuition", "under the hood", "mechanism", "anatomy", "deep dive", "step 1", "overview", "how it works", "why it matters"])
    results.append({
        "id": "progressive_disclosure",
        "passed": has_progressive,
        "evidence": f"Progressive structure markers found: {has_progressive}"
    })

    # Assertion 5: Feynman tone (no baby-talk)
    has_baby_talk = any(w in response_text.lower() for w in ["fairy", "magic wizard", "mommy", "daddy", "little tummy", "magic potion", "boo boo", "kiddy"])
    feynman_pass = not has_baby_talk
    results.append({
        "id": "feynman_tone",
        "passed": feynman_pass,
        "evidence": "Dignified plain English, no patronizing fairy-tale words" if feynman_pass else "Found patronizing baby-talk markers"
    })

    return results

if __name__ == "__main__":
    print("Eval harness initialized.")
