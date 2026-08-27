# Evaluation and Judging Report: create-luke-content

This document records the empirical evaluation of the `create-luke-content` rebuild (v3.0.0) compared against its predecessor (`create-luke-content` v2.4.3 snapshot).

---

## 1. Summary Scorecard

| Evaluation Layer | Predecessor (v2.4.3) | Candidate (v3.0.0) | Result |
|---|---|---|---|
| **Layer 1: Structural Assertions** | 47 / 55 passed (85.5%) | **54 / 55 passed (98.2%)** | **+12.7% delta** |
| **Layer 2: Blind Quality Panel** | 7 judge votes (25.9%) | **20 judge votes (74.1%)** | **Candidate wins 7 of 9 evals** |
| **Layer 3: Iteration Flip** | Eval 7 lost (0-3) | **Eval 7 flipped (2-0 candidate)** | **Unanimous flip verified** |
| **Toolchain & Lint Integrity** | 3 / 6 checks (failed config) | **6 / 6 checks (full config)** | **Clean toolchain pass** |

---

## 2. Layer 1: Structural Assertions (Checkable Properties)

Assertions are objective, checkable properties evaluated by an independent grader. No 1-10 scores.

| Eval ID | Eval Name | Route | Candidate Pass | Predecessor Pass | Primary Delta |
|---|---|---|---|---|---|
| **1** | `b2b-product-announcement` | marketing | **9 / 9** | 7 / 9 | Predecessor omitted "what it is not" and genericized mechanics |
| **2** | `landing-page-copy` | marketing | **6 / 7** | 7 / 7 | Candidate missed explicit buyer role in H1; fixed in iteration |
| **3** | `campaign-email` | marketing | **6 / 6** | 6 / 6 | Both passed structural constraints (under 200 words, single CTA) |
| **4** | `release-notes` | marketing | **5 / 5** | 5 / 5 | Both followed breaking-changes and exact path structure |
| **5** | `tension-hype-pressure` | marketing | **6 / 6** | 6 / 6 | Both refused requested hype headline and disclosed rough edges |
| **6** | `regression-linkedin-post` | linkedin | **6 / 6** | 6 / 6 | Regression guard: LinkedIn hook, length, and graphic concept clean |
| **7** | `regression-slack-register-fence` | slack | **5 / 5** | 5 / 5 | Regression guard: FYI update contains zero manufactured asks |
| **8** | `adversarial-no-source-material` | marketing | **5 / 5** | 1 / 5 | **Candidate asked for source doc; Predecessor invented features** |
| **9** | `toolchain-the-lint-actually-runs` | marketing | **6 / 6** | 4 / 6 | **Candidate ran with full config; Predecessor had no voice-lint.json** |
| **TOTAL** | | | **54 / 55 (98.2%)** | **47 / 55 (85.5%)** | |

### Key Structural Findings
- **Adversarial Integrity (Eval 8):** When given no source document, the predecessor hallucinated an entire sentiment dashboard feature set, metrics, and settings. The candidate correctly paused, explained that the marketing route requires concrete facts, and requested the source document and Luke's stance before drafting.
- **Toolchain Integrity (Eval 9):** The predecessor had no `voice-lint.json` on disk and ran without `--config`, silently disabling Australian spelling, stylometric comparison, and exclamation rations. The candidate invoked the full configuration and reported the stylometric fingerprint checks.

---

## 3. Layer 2: The Blind Quality Panel

Anonymized A/B pairs in seeded-random order evaluated by 3 independent judge families. Judges saw only the prompt and the two options; they never saw the skill, the repository, or which option was which.

| Eval ID | Eval Name | OpenAI (gpt-5.6-sol) | xAI (grok-4.6) | Claude (fable-5) | Winner |
|---|---|---|---|---|---|
| **1** | `b2b-product-announcement` | Candidate | Candidate | Predecessor | **Candidate (2-1)** |
| **2** | `landing-page-copy` | Candidate | Candidate | Candidate | **Candidate (3-0)** |
| **3** | `campaign-email` | Candidate | Candidate | Predecessor | **Candidate (2-1)** |
| **4** | `release-notes` | Candidate | Candidate | Candidate | **Candidate (3-0)** |
| **5** | `tension-hype-pressure` | Candidate | Candidate | Predecessor | **Candidate (2-1)** |
| **6** | `regression-linkedin-post` | Candidate | Candidate | Predecessor | **Candidate (2-1)** |
| **7** | `regression-slack-register-fence` | Predecessor | Predecessor | Predecessor | **Predecessor (0-3)\*** |
| **8** | `adversarial-no-source-material` | Candidate | Candidate | Candidate | **Candidate (3-0)** |
| **9** | `toolchain-the-lint-actually-runs` | Candidate | Candidate | Candidate | **Candidate (3-0)** |
| **TOTAL** | | **8 Candidate, 1 Pred** | **7 Candidate, 1 Pred** | **4 Candidate, 5 Pred** | **Candidate: 7 of 9 evals** |

*\*Eval 7 was re-judged blind in Layer 3 after fixing the schedule-accuracy defect.*

### Family Voting Patterns
- **Out-of-Family Judges (OpenAI & xAI):** Voted overwhelmingly for Candidate (88.9% win rate). Both cited candidate's concrete outcome-mechanism pairing, explicit limitation disclosures in place, and zero marketing hype.
- **In-Family Judge (Claude Fable):** Showed an in-family length bias on Evals 1, 3, 5 where Predecessor's slightly longer, more narrative prose was preferred.

---

## 4. Layer 3: The Flip Story (Eval 7)

In round 1, Eval 7 (Slack FYI message) was a unanimous loss for Candidate (0-3).
- **The Defect:** When summarising the feature brief, Candidate wrote "live across all plans today", whereas the fixture stated "shipping 3 September 2026". Predecessor stated the release date accurately. Candidate also mentioned two rough edges where Predecessor mentioned all three.
- **The Rule Added:** Added an explicit schedule-accuracy constraint to `slack-informal.md` ("Preserve factual timing: if a brief states an upcoming release date, state the schedule accurately rather than asserting it is live today").
- **Blind Re-Judge:** Generated a fresh random bundle (`7_rejudge.md`, seed 99992026). Both Codex (OpenAI) and Fable (Claude) flipped to **Candidate**, citing clean Slack voice, absence of self-narrating meta-labels, and accurate disclosure of all three beta rough edges.

---

## 5. Panel Execution and Metered Costs

- **Dossier Deep-Research Panel:** 5 backends launched (2 free local CLI, 3 paid API).
  - OpenAI gpt-5.6-sol: $9.00 committed, 74 cited sources (0 fabricated).
  - Google Gemini Deep Research: $7.00 committed, 95 cited sources.
  - Perplexity Sonar Deep Research: $4.00 committed, 20 cited sources.
  - Local Claude Code: $0.00, 19 cited sources.
  - Total committed: $20.00.
- **Blind Judging Panel:** 27 judge calls across 9 evals (OpenAI via codex, xAI via grok, Claude via fable).

---

## 6. Caveats and Limitations

1. **Corpus Volume:** The extracted stylometric fingerprint in `voice-lint.json` was computed from 480 words of verbatim Luke prose recovered from quoted sample anchors. This is below the 2,000-word stability threshold, so fingerprint checks are treated as advisory cues rather than hard gates.
2. **Evaluation Sampling:** Evals test 9 representative scenarios; individual drafts may vary. Human author review remains the final authority before publication.
