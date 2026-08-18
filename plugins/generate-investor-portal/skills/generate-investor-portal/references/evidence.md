# Evidence

Where the rules in this skill come from when they come from outside it. Everything here was read in
full from a four-backend Dossier deep-research panel run on 2026-08-18; the complete reports are in
`docs/deep-research/` in this plugin, with their source registries, so every claim below can be
walked back to the page it came from.

**Citation verification, run on all four reports.** Two passed clean (Perplexity 20/20, xAI 15/15,
zero fabricated). Two came back ATTENTION: the OpenAI report had 4 of 80 citations dead, and the
Gemini report 1 of 40 malformed plus five claims resting on sources that did not resolve. The dead
ones are named in the "Where the evidence is thin" section below rather than quietly dropped, and
where a claim was recoverable by hand it says so.

**This is a factual map, not legal advice.** Every regulatory source here carries that caveat from
its own author, and so does this file. Confirm any enacted obligation with counsel before treating
it as a compliance basis.

---

## E1 — A portal is a secondary view, and it must not go first

ASX Listing Rule 15.7 prevents a listed entity releasing information intended for the market to any
person before ASX has released it. Listing Rule 3.1 requires immediate disclosure of information a
reasonable person would expect to have a material effect on price or value, where "immediately"
means promptly and without delay.

**What it changes here.** A portal may mirror a released announcement, only after that control
point. A record must not carry market-sensitive material that has not been lodged. ASX's stated
enforcement tools include rejecting announcements, requiring retractions or corrections, and
suspending trading under LR 17.3.2.

*Source:* ASX Listing Rules Chapter 15 · ASX Guidance Note 8 · First Advisers, "ASX Compliance —
Avoiding the Tendentious and Intemperate". OpenAI report §1.1; Perplexity report §"Continuous
disclosure obligations".
*Confidence:* High. `<ENACTED>`.

## E2 — Website disclosure has conditions, and they are close to this skill's own shape

ASIC Regulatory Guide 198 permits an unlisted disclosing entity to satisfy s675 through website
disclosure, subject to good-practice conditions: all material information located in a **single
place** on the website with a prominent home-page link; every item present there even where it is
also disclosed elsewhere; published as soon as practicable; **a clear indication of when each item
was first published**; and records kept to demonstrate compliance.

**What it changes here.** The disclosure index is not a nice-to-have surface, and "when this was
first published" is a required field rather than a courtesy. It is also the strongest external
argument for the levy treatment of the disclosure index.

*Source:* ASIC RG 198, via the Perplexity report §"Continuous disclosure obligations and the role of
websites and portals".
*Confidence:* High. `<ENACTED>`.

## E3 — "If not, why not" is why a mandated surface cannot simply be absent

ASX Listing Rule 4.10.3 requires an annual corporate-governance statement. Where an entity has not
followed a recommendation for any part of the reporting period it must **identify the
recommendation and the period, explain why, and state the alternative governance practice
adopted**. ASX Guidance Note 9 carries the detail.

**What it changes here.** This is the external basis for the levy rule. An absent governance surface
is not a neutral omission — the regime's whole design is that a departure is *stated*, not silent.
It also means the portal must surface the issuer's actual explanation, never infer compliance.

*Source:* ASX GN 9 · ASX LR 4.10.3. OpenAI report §1.1; Gemini report §1.
*Confidence:* High. `<ENACTED>`.

## E4 — Prominence is a compliance surface, not a design choice

ASX Guidance Note 8 requires announcements to be accurate, complete and not misleading, where
"complete" means not omitting material information, and a materially inaccurate one may create a
further correction obligation. It warns specifically against unbalanced "spin", **including a
heading that highlights a small positive point while concealing essentially negative
information**. ASX has also stated that a cautionary statement accompanying an estimate or target
must be given **equal prominence and appear in the same font type, size and colour on the same
page**.

**What it changes here.** Two things. The H1 rule is not only an editorial preference — a headline
is a disclosure surface. And the emphasis budget acquires a hard floor: an allocation mechanism that
can quieten a cautionary statement is a compliance defect. ESMA's parallel expectation for
Alternative Performance Measures is the same shape: define them, reconcile them to IFRS, and do not
give them undue prominence over the IFRS metric.

*Source:* ASX GN 8 · First Advisers on ASX presentation compliance · ESMA financial reporting /
APM guidelines. OpenAI report §1.2; Perplexity report §§"Continuous disclosure", "Plain-language".
*Confidence:* High for GN 8 `<ENACTED>` / `<GUIDANCE>`; High for the ESMA APM expectation.

## E5 — The accessibility floors, and the one that applies to the placeholder itself

WCAG 2.2: normal-size text needs **4.5:1** contrast (1.4.3); large-scale text and non-text
graphical objects need **3:1** (1.4.3, 1.4.11). In a financial table, body figures, negative signs,
footnotes, period labels and column headers are **normal text** unless they meet the large-scale
definition. Under 1.4.1, where colour communicates a state — red for loss, green for profit, amber
for estimate, grey for unavailable — the same information must be available through text, symbol,
sign or pattern.

Two findings beyond the floors:

- **`Unavailable` must be readable text, not a pale blank or a colour-only marker.** This is the
  external confirmation that `ABN ᴹ` — a label, a space, and a lone superscript marker — is an
  accessibility failure and not merely ugly.
- **Complex tables need `id` and `headers`, not `scope`.** W3C technique H63 (`scope`) is
  sufficient for a simple table; for the multi-level and irregular headers that capital tables and
  multi-year summaries actually use, H43 requires each `<th>` to carry a unique `id` and each
  `<td>` a `headers` attribute listing them. A model emitting markdown tables cannot express that,
  so it has to be a deterministic rendering step. That is the renderer's job rather than the
  record's, and it belongs on the renderer-side gate this skill's Known limits already names.

**Held loosely.** No universal securities-law rule was found making WCAG 2.2 AA binding on every
private investor portal; the binding status depends on entity type, jurisdiction, service status
and contract. Both the OpenAI and Perplexity reports mark this explicitly as insufficient evidence.
Treat the floors as the engineering baseline, not as a proven legal obligation.

*Source:* W3C WCAG 2.2 · W3C WAI Tables Tutorial · W3C techniques H43 / H63 · Understanding SC
1.4.1. All four reports; the "readable text" formulation is OpenAI §1.3.
*Confidence:* High for the technical criteria `<GUIDANCE>`; Low for universal legal applicability.

## E6 — Models produce wrong numbers from tables they can see

A masked-span study over real financial tables from S&P 500 companies' 2024 10-K reports masked
numeric spans that had a unique, consistent ground truth answerable from the provided context, then
asked models to recover them. Models showed significant intrinsic hallucination rates, worsening
with reasoning complexity across four categories — Direct Lookup, Comparative Calculation,
Bivariate Calculation, Multivariate Calculation — and **even Direct Lookup produced numbers
inconsistent with the source table**.

**What it changes here.** This is why "do not derive figures" is a refusal rather than a caution: if
direct lookup is unreliable, a derivation over two looked-up values is worse. Market capitalisation
from price × shares is arithmetic, not data.

*Source:* "A Framework for Assessing Intrinsic Tabular Hallucinations", arXiv 2508.05201.
Perplexity report §"Empirical hallucination patterns".
*Confidence:* High. `<GUIDANCE>` (peer-reviewed / preprint).

## E7 — The cases where the model is most likely to be right are where it is most likely to be wrong

A study of more than 197,000 questions about revenue values for US listed companies, against
Compustat-IQ ground truth spanning 1980–2022, defined hallucination as an absolute percentage error
above 10%. Models answered more accurately for larger companies, more recent years, and firms with
more attention and more readable filings — **and were also more likely to hallucinate for larger
firms and more recent years**, with measured log-odds of hallucinating revenue rising with market
capitalisation.

**What it changes here.** Apparent plausibility carries no signal. A figure about a well-known
company, in a recent period, from a model that has clearly seen the filings, is exactly the figure
that gets waved through — and it is not safer than any other. It has to be marked or absent.

Two further results in the same family, held at lower weight. A widely-cited benchmark reports a
GPT-4-Turbo-plus-retrieval failure rate of **81%** on complex financial questions; a peer-reviewed
multilingual/multimodal financial benchmark reports **46.01%** overall for GPT-4o. Treat both as
directional: they measure question-answering over filings, not record emission from a supplied
overview, and the OpenAI report's own framing is the more careful one — the defensible conclusion is
not that models always fabricate, it is that **fluent output and cited output are insufficient
reliability indicators**.

*Source:* "Where Large Language Models Fall Short on Financial Knowledge", arXiv 2504.00042 ·
Patronus AI FinanceBench · MultiFinBen, ACL 2026. Perplexity §"Empirical hallucination patterns";
Gemini §3; OpenAI §1.4.
*Confidence:* High for the 197k-question study; Medium for the benchmark headline rates.

## E8 — The crawl is an attack surface, and prose is not the control

NIST AI 600-1, the Generative AI Profile of the AI Risk Management Framework (published 26 July
2024), defines **confabulation** as a system confidently producing erroneous or false content, and
notes expressly that confabulated output can include **citations that purport to justify an
answer**. It defines **indirect prompt injection** as an attack in which an adversary places prompts
into data that an LLM-integrated application is likely to retrieve, potentially causing unintended
behaviour or access to proprietary data. Its suggested actions include reviewing and verifying
sources and citations, verifying retrieval-data provenance and grounding, deploying fact-checking,
monitoring provenance deviations, and human moderation.

The engineering shape that follows, as prescribed across the panel: treat crawled text as untrusted
data and never as instruction; keep fixed system instructions **outside** the retrieved corpus;
wrap fetched bodies in explicit machine-readable delimiters with a treat-as-data preamble, and
**neutralise forged fence tags inside the fetched body** so a payload cannot plant text outside the
fence; permit read-only retrieval during drafting; and have a **separate deterministic service**
write validated facts — **the generation agent should not hold direct production-database write
authority**.

**What it changes here.** The verbatim fence sentence at the top of SKILL.md, repeated into
`references/imagery.md` where crawled copy becomes image-prompt context. And the reading of
`record-gate.mjs` plus `seed-portal.mjs` as the separation of drafting from writing rather than as
a convenience.

**Provenance note, because this citation failed verification.** The panel cited NIST AI 600-1 at
`nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`, which returns 404, and three claims rested on it
alone. Checked by hand on 2026-08-18: the document is real, published 26 July 2024, DOI
**10.6028/NIST.AI.600-1**, listed at
`nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence`
with a working PDF at `tsapps.nist.gov/publication/get_pdf.cfm?pub_id=958388`. Cite the DOI. The
URL was stale, not invented.

*Source:* NIST AI 600-1 (DOI 10.6028/NIST.AI.600-1). OpenAI report §1.4; Gemini report §3C.
*Confidence:* High for the document and its definitions; Medium for the specific wording of the
fence-tag-neutralisation recipe, which the Gemini report sourced to a single project changelog.

## E9 — Duplicate generation, and corrections that supersede rather than overwrite

Two controls the panel prescribes independently of each other:

- **Before crawl or paid generation, check the canonical release index and the content hash**, and
  return the canonical record if it is already present. Re-scraping and re-summarising figures that
  are already available as tagged structured data adds cost and an opportunity for
  misrepresentation without adding value.
- **A correction workflow that supersedes, rather than silently overwrites, a public version**, as
  the last step of a release pipeline that also publishes an immutable version.

**What it changes here.** The first is the reason the republish check moved to the top of SKILL.md
and gained a content-hash clause. The second is the external confirmation of this skill's own
re-entrancy finding — `$set: { record }` over a published portal replacing its entire body while
`status` stays `published` — and it names the fix this skill does not yet have: an immutable version
plus a supersede path. Until that exists, `--republish` is the whole of the control.

*Source:* OpenAI report §1.1 and §1.5, drawing on ASX LR 15.7, the SEC EDGAR validation model and
ASX correction principles; Perplexity §"Refusal before crawl or paid generation".
*Confidence:* High as design guidance; `<INFERENCE>` in both reports rather than a quoted rule.

## E10 — One `unavailable` state is not enough

Regulators penalise inventing a substitute for missing information — including improvised custom
responses in place of the prescribed one. But the panel is equally clear in the other direction: a
visible unavailable state **does not cure a legal omission where the item is mandatory**. The
distinctions that have to be expressible are *not required* / *not prepared* / *not lodged* / *not
held by portal* / *awaiting approval* / *source conflict*, and for a governance item the model is
tri-state: held, not held, not applicable.

For a mandatory current governance statement, the prescribed handling is a **publication block plus
legal escalation**, not an honest surface.

**The disagreement, left in.** This skill's own levy rule says a mandated surface with no evidence
renders an honest `unavailable` rather than vanishing, and that remains right as against silence.
The research says that is not sufficient where the item is legally mandatory. Both can hold: the
`unavailable` surface is the correct *rendering*, and for a mandatory item it should also be a
*publish blocker* that a human clears. The skill states both; the gate currently enforces the
surface and not the block, because deciding which items are mandatory for a given entity needs the
entity classification the record does not carry. That is a named gap, not a resolved one.

**Provenance note.** The FinCEN guidance the Gemini report leaned on for the "custom responses pose
as real data" formulation did not resolve (timeout, so plausible but unconfirmed), and it was that
claim's only source. The ASIC and ASX material behind the rest of this entry resolved.

*Source:* OpenAI report §"Conflict over 'not held'" and §1.1, on ASIC small-proprietary reporting
status and ASX governance disclosure; Perplexity §"Honest 'not held' surfaces"; Gemini §1 for the
FinCEN formulation.
*Confidence:* High for the taxonomy as design guidance; Medium for the mandatory-item block, which
is an inference in the source rather than a quoted rule; Low for the FinCEN wording.

## E11 — Selective quotation has a documented mechanism

A US district court noted that selective quotation obscures legal holdings, a risk explicitly tied
to the use of AI tools for case summarisation and document review; a Ninth Circuit case raised the
same concern about the mutation of meaning through selective quotation. Extracting isolated
statements without their surrounding context creates a material misrepresentation even where every
quoted word is accurate.

**What it changes here.** It is the external support for the contract's outright refusal of
`announcementExcerpt`. The mechanism is not that the excerpt is inaccurate; it is that the reader
receives the fragment the portal chose in place of the document the company lodged.

*Source:* Linet Americas, Inc. v. Hill-Rom Holdings, Inc. (July 2024) · Chicken Ranch Rancheria v.
State of California (9th Cir. 2022). Gemini report §4.
*Confidence:* Medium. Both citations were bot-blocked at verification (403 on law.justia.com), so
existence is plausible but unconfirmed from here, and the AI-summarisation link is the report's
characterisation rather than a quoted holding.

## E12 — Enforcement exists for AI claims, and not yet for AI-generated figures

Documented actions, in ascending relevance and descending certainty:

- **SEC v. Delphia (USA) Inc. and Global Predictions Inc.**, 18 March 2024. False and misleading
  statements about AI use in SEC filings, a press release, a website and social media; censure,
  cease-and-desist, **US$400,000** in total civil penalties (US$225,000 and US$175,000). This is
  the best-sourced item here.
- **SEC v. Presto Automation Inc.**, January 2025 — reported as the first AI-washing settlement
  against a public company, over autonomous-AI claims in 8-K, 10-K and S-4 filings where a human
  agent entered orders much of the time.
- **FCA public censure of Carillion plc** for announcements that did not accurately or fully
  disclose true financial performance. No automation involved; it is evidence of the consequence of
  incomplete and selectively positive disclosure.
- **Deloitte Australia / DEWR assurance review.** A report reportedly containing a fabricated
  judicial quote and non-existent academic references was replaced by a corrected version, with a
  reported partial refund. Closest documented incident of AI-assisted citation fabrication in a
  paid professional deliverable — but a government assurance report, not an investor disclosure.
- **ASIC Report 798**, "Beware the gap", October 2024. A review of 624 AI use cases across 23
  licensees found nearly half lacked policies considering consumer fairness or bias, and fewer
  still governed disclosure of AI use.

**And the honest negative, which three of four reports state independently:** no primary enforcement
action was found, across ASIC, ASX, SEC and FCA materials, establishing that an issuer's
investor-facing financial document was LLM-generated and contained a fabricated numerical fact.
Public enforcement summaries describe the false statement and the remedy, not the drafting
technology, so absence of a documented case is weak evidence of absence of the failure. Do not cite
this as reassurance.

*Source:* SEC Release 2024-36 · FCA Primary Markets enforcement outcomes · ASIC REP 798 ·
DEWR / AP reporting. OpenAI §"Documented incidents"; Gemini §4; Perplexity §"SEC enforcement".
*Confidence:* High for Delphia/Global Predictions and Carillion; Medium for Presto and Deloitte
(both cited to secondary sources that did not resolve); High for the negative finding, which three
backends reached separately.

---

## Where the evidence is thin

Carried forward rather than resolved.

| Gap | Why it matters here |
|---|---|
| No enforcement case for a fabricated figure in an AI-generated investor document | The strongest argument for these gates is the mechanism, not a precedent. Do not present a precedent that does not exist. |
| No universal securities-law WCAG mandate for investor portals | The contrast floors are an engineering baseline. Saying they are legally required would be the same class of overclaim this skill exists to prevent. |
| Australia has no XBRL-equivalent structured-data mandate for portals | The traceability argument for `asAt` and `source` is a control argument here, not a compliance one, unlike the US and EU. |
| Which items are mandatory for a given entity | The gate cannot turn a levy into a publication block without the entity classification, and the record does not carry it. E10's stronger control is therefore unimplemented and named as a limit. |
| Machine-checkable gate efficacy versus human review for selective quotation | Every report says this is human-detectable and none quantifies it. The Known limits section says so rather than implying the gate covers it. |
| "Fine-tuning degrades abstention by 24%" | Cited by one backend to a HuggingFace search-results URL, which is not a source. **Not used.** Recorded so nobody re-imports it from the report. |
