# Gemini Deep Research prompt architecture

The framework for the two prompts this skill emits. (If the `deep-research-prompt-creator` skill is installed you may invoke it to draft/refine each prompt; this reference keeps the skill self-contained.) Both prompts are the **competitive / market** archetype.

## Why pseudo-XML
Gemini's attention uses the tags to separate instruction from context and they survive the plan-compression step better than markdown headings. Use them verbatim.

## The skeleton (fill every applicable section)

```
<role>You are a senior [market-intelligence / positioning] analyst conducting a Deep Research investigation for [stakeholder]. Your output will directly inform [the specific decision/artefact].</role>

<context>[2–4 sentences, <150 words: who needs it, why, what decision it informs, domain constraints — product, audience, geography, stage. Tight; context bloat degrades the run.]</context>

<core_directive>[ONE sentence stating the single question the research must answer. The anti-drift anchor — repeated verbatim at the very end.]</core_directive>

<research_questions>
Primary:
1. [Restates the core_directive as a question.]
Secondary:
2.–n. [3–7 total. More than ~8 triggers context rot.]
</research_questions>

<scope_and_boundaries>
<include>[segments, competitor set, geographies, time window]</include>
<exclude>[what to keep out — enterprise buyers, generic trend listicles, off-topic adjacencies]</exclude>
<time_horizon>[e.g. "Jan 2024–present, with a 12-month forward outlook"]</time_horizon>
<geography>[primary + secondary markets; note divergences]</geography>
</scope_and_boundaries>

<source_discipline>
<prioritise>[organic customer-sentiment platforms (Reddit, HN, Indie Hackers, Product Hunt, G2/Capterra reviews), competitor pricing/positioning pages read in context, filed financials/funding, search + AI-search signal, the actual rendered competitor sites]</prioritise>
<deprioritise>[SEO "top N" listicles, vendor comparison pages, marketing blogs — label "[SECONDARY: promotional]" and corroborate from a primary source]</deprioritise>
<criteria_match_validator>For each source used, justify why it met the criteria; discard the rest during synthesis.</criteria_match_validator>
</source_discipline>

<depth_requirements>
For each question: factual findings with quantitative data where available; contrasting/disconfirming evidence; named sources (author/org, date, URL); a confidence qualifier (High/Medium/Low) on every non-trivial claim.
Load-bearing — pain-point / language mining: extract the exact words buyers use, with quotes, and contrast them with vendor positioning; name the gap.
</depth_requirements>

<analysis_lens>[3–6 frames telling Gemini HOW to weigh findings — e.g. discriminating evidence for/against each candidate position; the Dunford 10-second category test; blue-ocean defensibility over 12 months; beachhead scoring; positioning→aesthetic/attribute mapping. This section is the highest-leverage part — invest here.]</analysis_lens>

<epistemic_bounding>
Use inline tags; do not estimate or paper over gaps:
<MISSING_DATA>…</MISSING_DATA> · <INSUFFICIENT_EVIDENCE>…</INSUFFICIENT_EVIDENCE> · <CONFLICTING_EVIDENCE>…</CONFLICTING_EVIDENCE> · <CONFIDENCE:LOW>…</CONFIDENCE:LOW> · <INFERENCE>…(show the chain)</INFERENCE>
Do not present extrapolated numbers as empirical findings.
</epistemic_bounding>

<citation_protocol>Inline <cite url="..."> at the point of every quantitative claim, quote, and attributed statement — never deferred to a bibliography. Use <cite url="UNVERIFIED" note="…"> if a URL can't be verified rather than omitting or inventing one.</citation_protocol>

<output_format>[A fixed section structure with tables — exec summary (confidence-led bullets), detailed findings per question, the decision-grade tables (a scorecard, a competitor table, a beachhead table, a category/language table), an evidence table, knowledge gaps, recommended next steps. Specify it; a fixed skeleton prevents a wall of prose.]</output_format>

<constraints>[no fabricated citations/quotes/dates; present both sides of conflicts; cite inline; keep prose dense; preserve any multi-product/segment distinctions]</constraints>

<core_directive>[REPEAT the core_directive verbatim — re-anchors synthesis after the long run.]</core_directive>
```

## Rules that matter most
- **Positive framing** — tell Gemini what to do, not what to avoid (except the SEO/aggregator exclusion, which is a load-bearing negative).
- **Rigid macroscopic skeleton, loose microscopic prose** — specify headings/tables/tags; don't micromanage word counts (over-specification degrades output).
- **Name the candidate positions explicitly** in Prompt A so Gemini tests/discriminates between them rather than re-describing the audience.
- **Confidence qualifiers and inline citations are non-negotiable.**

## Operator notes to give the user (after the launcher)
- **Pause at Gemini's Plan Review** and prune/inject branches before it runs autonomously — the single highest-leverage intervention.
- **Attach the user's own docs** (product brief, positioning of record) as authoritative context so Gemini doesn't re-derive the product wrong.
- **Decompose** if scope is large (run the two prompts separately — which this skill already does).
- **Adversarial audit** — for high-stakes runs, have a second model red-team the scorecard and every demand-signal claim against its citation (the most hallucination-prone outputs).
