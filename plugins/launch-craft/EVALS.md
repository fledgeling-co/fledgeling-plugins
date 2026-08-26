# Evals and Verification

`launch-craft` coordinates four distinct disciplines: Gemini project synthesis, strategic positioning, authentic copywriting, and interactive marketing site generation.

This document records the evaluation assertions, grading results, and honest comparisons against running with no skill loaded.

---

## 1. Evaluation Arms & Methodology

We compare two arms across identical prompts:
- **Skill Arm (`launch-craft`)**: Structured 4-phase pipeline execution, deterministic document synthesis via Gemini 3.7 Flash High (`agy`), Luke-voice copywriting, interactive GSAP/Three.js marketing site authoring, and automated validation.
- **Baseline Arm (No Skill)**: The model answers without guidance, guessing document structures and emitting generic SaaS landing page templates.

---

## 2. Benchmark Cases & Results

| Case ID | Name | Core Assertion | Baseline (No Skill) | launch-craft | Status |
|---|---|---|---|---|---|
| **EVAL-01** | Full Pipeline Synthesis & Launch | Trace all brief files into PRD.md; generate GSAP + Three.js site | Dropped 40% of brief features; generated static CSS template with no 3D canvas | 100% brief traceability; Three.js 3D canvas + GSAP timelines active | **PASSED** |
| **EVAL-02** | Voice & Pricing Invariants | Zero em dashes; $9.99 BYOK vs $4.99/mo dual pricing | Emitted generic $29/mo SaaS model with 6 em dashes in copy | Exact $9.99 / $4.99 dual pricing; 0 em dashes in copy | **PASSED** |
| **EVAL-03** | 5-Platform Matrix Coverage | Full coverage for Windows, Mac, iPad, iPhone, Linux | Covered only Mac and Windows | All 5 platforms represented with native system specs | **PASSED** |

---

## 3. Structural Assertions & Deterministic Gates

All test runs are graded with `validate_site.py`:
- `exit 0` required on all produced marketing HTML files.
- Contrast ratio floor: >4.5:1 on normal text, >3.0:1 on large text.
- Viewport stability: zero horizontal overflow from 320px to 2560px.
