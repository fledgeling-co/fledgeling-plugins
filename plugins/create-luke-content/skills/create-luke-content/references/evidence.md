# Copywriting Craft: Empirical Evidence Base

Distilled from a five-backend Dossier deep-research panel (2026-08-27, 232k characters, 208 cited sources across OpenAI gpt-5.6-sol, Perplexity Sonar Deep Research, Google Gemini Deep Research, and Claude Code).

This reference provides the empirical evidence base for the **marketing route** of the `create-luke-content` skill. It separates replicated findings from direct-response folklore so no rule is encoded on the strength of a famous name.

---

## 1. Load-Bearing Replicated Findings

### 1.1 Message Hierarchy and Outcome-Mechanism Pairing
- **(High) Connect outcomes to mechanisms; do not enforce "benefit-before-feature" ordering.** A controlled advertising experiment (Meeds & Farnall, 2018) found the highest attitude scores when benefit and feature sentences were combined (mean 4.64), significantly outperforming benefit-only copy (4.27), while feature-only was not significantly worse than combined (4.50). For technical readers, mechanism-anchored copy validates architectural feasibility and unlocks rational consideration (CXL / Nielsen Norman Group).
- **(High) Causal mechanisms improve evaluability when directionally aligned.** Consumers chose products with directionally consistent mechanisms at 60.18% vs 42.30% when mechanism and effect directions matched (OR=2.21, Journal of Consumer Research 2024). Analytically inclined evaluators ("explanation fiends") demand causal depth; superficial benefit claims invite skepticism (Fernbach et al., 2013).
- **(High) Headline-to-CTA message continuity drives conversion.** Repeating the headline promise verbatim on the action button increased conversion by >10 percentage points in a 956-visitor field experiment (PMC, 2024). Coordinating ad and landing-page copy reduced cost per action by 37% in a B2B semiconductor field experiment (Kim & Kalyanam, 2025).

### 1.2 Specificity, Proof, and Limitations
- **(High) Concrete language outperforms abstract adjectival copy.** Across field text analysis of 1,000+ interactions and controlled experiments, linguistic concreteness increased customer satisfaction, purchase intention, and downstream purchasing (Packard & Berger, JCR 2020).
- **(High) Numerical precision signals measurement on unfamiliar attributes.** Precise numbers increased purchase willingness for unfamiliar technology attributes from 3.28 to 4.36 on a 7-point scale (Park, JCP 2022). Unsubstantiated or manufactured precision backfires; round numbers signal stability or natural approximation when precise telemetry does not exist.
- **(High) Voluntary disclosure of limitations ("two-sided messages") lifts credibility.** Meta-analysis of 217 effects shows two-sided messages have a positive effect (r = .068), driven by source credibility (Eisend, IJRM 2006). Disclosing operational boundaries, unsupported configurations, or known rough edges builds trust with technical buyers auditing career risk.

### 1.3 Professional B2B Risk Calculus vs Consumer Psychology
- **(High) B2B copy must reduce career and operational risk, not merely stoke desire.** Perceived risk correlates negatively with purchase intention (r = -.362 across 13,779 participants, JCIS 2019). Technical buyers evaluate against downside risk ("will this break production or breach disclosure rules?"). Stated preference for guaranteed B2B service showed a 50% premium (IMM, 2019).
- **(High) The Expertise Reversal Effect: do not dumb down domain vocabulary.** Cognitive load research (Kalyuga et al., 2003) proves that aggressive simplification that helps novices actively hinders domain experts. Jargon avoidance does not reduce perceived expertise (Learning & Instruction, 2025), but stripping recognized domain terms (e.g., continuous disclosure, AST pruning, idempotency) degrades perceived enterprise readiness.

---

## 2. Direct-Response Canon: Replicated vs Folklore

| Canonical claim | Proponent | Evidence status | Decision in this skill |
|---|---|---|---|
| Specific facts beat generalities | Ogilvy / Hopkins | **Replicated (High)**: Concrete numbers and named mechanisms outperform adjectives | Enforce concrete claims; ban unsupported superlatives |
| Test alternatives systematically | Caples | **Replicated (High)**: Large variation across headline variants in field experiments | Support variation; do not encode a single rigid formula |
| "Lead with benefits, not features" | Traditional Canon | **Falsified as a universal rule (High)**: Combined benefit + mechanism outperforms benefit-only | Require outcome AND mechanism in top message unit |
| "Long copy always outsells short" | Hopkins / Direct Mail | **Context-dependent / Unreplicated in B2B (Low)**: Information need dictates length, not word count | Match length to artifact schema; omit padding |
| "Slippery slide" narrative loops | Sugarman | **Unreplicated for B2B (Low)**: B2B buyers scan non-linearly (F-pattern) | Use scannable structure and clear headers, not narrative traps |
| Manufactured urgency / countdowns | Halbert | **Falsified in B2B (Backfires)**: Destroys credibility and negotiation trust | Ban fake urgency; allow only verified operational deadlines |
| Universal 5th-grade reading level | General CRO | **Falsified for technical buyers (High)**: Expertise Reversal Effect | Plain structure and short sentences, but preserve domain terminology |

---

## 3. Ranked Failure Modes to Ban

1. **Unsubstantiated outcome, security, or comparative claims**: Claims lacking a verifiable baseline, denominator, or timeframe trigger skepticism and regulatory risk.
2. **Unsupported superlative stacking**: Multiple praise adjectives ("revolutionary, seamless, best-in-class") trigger cognitive discounting.
3. **Manufactured urgency or artificial scarcity**: Fake countdowns, arbitrary deadlines, or fake seat limits destroy enterprise trust.
4. **Jargon as a credibility costume**: Buzzwords substituting for mechanism descriptions increase cognitive friction.
5. **Feature dumps without outcome or consequence**: Unstructured lists of capabilities without user impact fail to communicate value.
6. **Consumer-app hype substituted for decision information**: Emotional excitement ("We're thrilled to announce!") replaces evaluability.

---

## 4. Artifact-Specific Schemas

- **Product announcement**: What changed → Who it is for → Prior problem → Named mechanism → Concrete evidence/demo → Known limitations/migration impact → One next action.
- **Landing page copy**: Headline (outcome + buyer/use case) → Subhead (mechanism + proof cue) → Mechanism/architecture proof → Objection handling & risk treatment → Repeated semantically matched CTA.
- **Release notes**: Version/date → Affected users → Breaking changes first → What changed & what it means → Exact configuration paths/settings → Known limitations.
- **Campaign email**: Specific unhyped subject line → Opening line stating relevance/capability in first 15 words → Single focused topic → One semantic CTA.
