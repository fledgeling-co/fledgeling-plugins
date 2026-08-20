---
title: "Australian R&D Tax Incentive Eligibility for Software and SaaS Expenses"
run_id: dr_e1a4cc95de48cc8b
question: "Which software and SaaS operating expenses of a small Australian software company qualify as eligible R&D expenditure under the Australian R&D Tax Incentive (R&DTI)?\n\nCover in depth:\n1. The statutory test for core R&D activities vs supporting R&D activities under Division 355 of ITAA 1997, and how the \"dominant purpose\" test applies to supporting activities.\n2. How the \"directly related\" / nexus test is applied to recurring software subscriptions and cloud services, and what AusIndustry and the ATO have actually said about it.\n3. Eligibility, on a category-by-category basis, of: cloud compute and hosting (Azure, AWS, Vercel, Fly.io); observability, logging and error monitoring (Sentry, Axiom); managed databases (Redis Cloud); AI and LLM API usage and AI assistant subscriptions (Anthropic Claude, ElevenLabs, xAI/Grok); developer tooling and issue tracking (Linear, Ref.tools, Tailscale, Supermemory); source control and CI (GitHub); app store developer registration (Google Play); domain registration; email, collaboration and productivity subscriptions (Google Workspace, Slack); and training or education subscriptions.\n4. Apportionment where a tool serves both R&D and ordinary business use — the accepted methodologies, and what evidence substantiates an apportionment percentage.\n5. The excluded activities list and expenditure that cannot be notionally deducted.\n6. Record-keeping and substantiation requirements, including contemporaneous records and the nexus between expenditure and registered activities.\n7. The refundable and non-refundable offset rates from 2021-22 onwards, the $20m aggregated turnover threshold, the $150m expenditure cap, and the minimum $20,000 notional deduction.\n8. Treatment of expenditure paid to overseas suppliers, the Overseas Finding requirement, and where an overseas-supplied cloud service sits relative to that requirement.\n9. GST treatment — whether notional deductions are GST-inclusive or exclusive for a GST-registered entity.\n10. Common ATO and AusIndustry review and audit triggers for software R&D claims, and documented cases or guidance where software subscription claims were denied."
provider: gemini
model: deep-research-max-preview-04-2026
tier: max
archetype: regulatory
sources: 44
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 7.00
completed: 2026-08-19T23:57:06.958Z
---
# Australian R&D Tax Incentive: Classification of Software and SaaS Operating Expenses

This research report provides a decisive, jurisdictional analysis of software and Software-as-a-Service (SaaS) operating expenses to determine their eligibility under the Australian Research & Development Tax Incentive (R&DTI). It is designed to empower legal and accounting teams to accurately classify a concrete 79-line expense schedule for a small Australian software company spanning the 2025–2026 income year. This report is for informational purposes only and does not constitute professional tax, financial, or legal advice; confirm all enacted obligations with qualified counsel.

*   The statutory framework strictly bifurcates R&D into "core" and "supporting" activities, rejecting "whole of project" software claims.
*   Recurring SaaS and cloud compute costs must demonstrate a direct nexus to registered experiments; ordinary business and commercialisation expenses are aggressively targeted by regulators.
*   The deployment of advanced tools (e.g., AI assistants, managed databases) requires granular apportionment, as blanket deductions routinely trigger compliance reviews.
*   Notional deductions must be calculated exclusive of GST input tax credits, and overseas-procured SaaS inputs generally bypass complex "Overseas Finding" requirements provided the actual experimental activity occurs in Australia.

## Executive Summary

*   **(High Confidence)** Core vs. Supporting Activities: Eligible expenditure must map directly to registered `<ENACTED>` core R&D activities (experimental, unknown outcomes) or supporting R&D activities under Division 355 of the *Income Tax Assessment Act 1997* (ITAA 1997). Supporting activities must pass a "dominant purpose" test if they relate to production or excluded activities.
*   **(High Confidence)** The Nexus Requirement: Expenditure on SaaS and software subscriptions is only deductible to the extent it is "directly related" to conducting eligible R&D. The Australian Taxation Office (ATO) explicitly rejects claiming 100% of tools used for both business-as-usual (BAU) and R&D.
*   **(High Confidence)** Apportionment Methodologies: Where tools serve dual purposes, the ATO mandates a "reasonable basis of apportionment." Accepted methodologies include Headcount/Time Ratios (for per-seat licenses based on logged R&D hours) and Resource/Usage Tracking (for consumption-based SaaS using environment tags or distinct API keys).
*   **(High Confidence)** Record-Keeping and Substantiation: The burden of proof strictly requires contemporaneous records. Claims must be substantiated by documents created at the time the work was performed (e.g., Git commit histories, Jira/Linear tickets, and Slack transcripts) to prove technical uncertainty and the nexus of the expense.
*   **(High Confidence)** Financial Thresholds and Caps: For the 2025–2026 income year, companies with an aggregated turnover under $20 million receive a refundable offset at their corporate tax rate plus an 18.5% premium (typically a 43.5% total offset). A minimum of $20,000 in notional deductions must be incurred to claim the offset. Eligible expenditure is capped at $150 million, above which the offset drops to the standard corporate rate.
*   **(Medium Confidence)** Category Eligibility: Developer tooling, Continuous Integration / Continuous Deployment (CI/CD), and dev-environment cloud hosting (AWS/Azure) are highly defensible when apportioned correctly. Conversely, app store registrations, domain hosting, and generic productivity suites (Google Workspace) face high regulatory resistance unless an extraordinary dominant R&D purpose is documented.
*   **(High Confidence)** Audit Triggers (TA 2017/5 & TA 2023/4): The ATO and AusIndustry aggressively audit software claims that exhibit "whole-of-project" claiming, classify routine bug/beta testing as core R&D, rely on non-specific retrospective documentation, or improperly claim expenses incurred by associated foreign entities. 
*   **(High Confidence)** GST Treatment: R&D notional deductions must be calculated on a GST-exclusive basis for GST-registered entities, explicitly removing input tax credits before applying the R&D offset premium.
*   **(Medium Confidence)** Overseas SaaS Inputs: Purchasing cloud infrastructure or Application Programming Interfaces (APIs) from foreign vendors (e.g., AWS, OpenAI) does not typically trigger the requirement for an "Overseas Finding," provided the actual development activity (the human experimentation) is conducted by personnel physically located in Australia. 

## R&D Tax Incentive Claim Schedule (Aug 2025 - Jun 2026)

This schedule directly classifies the requested software categories for the ~A$6,600 expense claim.

| Tool / Service | Functional Scope & Real-World Context | Eligible (TRUE / FALSE) | Statutory Explanation & Accountant Check |
| :--- | :--- | :--- | :--- |
| **Azure / AWS** | General cloud infrastructure used for computing, storage, and networking. | **TRUE** (Apportioned) | Eligible *only* for the proportion mapped to isolated R&D sandbox/testing environments. Commercial hosting is excluded. Requires AWS/Azure billing tags for substantiation. |
| **Vercel / Fly.io** | Edge-compute networks and global application deployment platforms. | **TRUE** (Apportioned) | Edge networks deploy code globally. If used to test edge-caching latency hypotheses, it is eligible. If used to serve the live commercial app, FALSE. |
| **Sentry / Axiom** | Observability, logging, and error monitoring tools for tracking code failures. | **TRUE** (Apportioned) | Eligible if deployed in a staging environment to observe the failure states of an experimental algorithm (satisfying "observation and evaluation"). FALSE if monitoring live commercial user crashes (routine bug tracking). |
| **Redis Cloud** | Managed, in-memory database used for caching and high-speed data retrieval. | **TRUE** (Apportioned) | TRUE if storing test data for an experiment. If it handles mixed dev/production data, strict mathematical apportionment is required. |
| **Anthropic Claude / ElevenLabs / xAI (Grok)** | Large Language Models (LLMs) and generative AI API suites. | **TRUE** (Apportioned) | FALSE if used as a generic code-completion or writing assistant (business overhead). TRUE if the APIs are the subject of the experiment itself (e.g., testing novel prompt-chaining latency limits). |
| **Linear** | Developer tooling and issue tracking platform. | **TRUE** (Apportioned) | Eligible as supporting R&D to manage the technical struggle. Must be apportioned based on the time/headcount of developers engaged in registered R&D. |
| **Ref.tools** | ModelContextProtocol (MCP) server providing AI coding agents access to API documentation. | **TRUE** (Apportioned) | Eligible if used to build or train an agent within a registered core software experiment. Must be apportioned against general business coding use. |
| **Tailscale** | Zero-trust VPN and secure networking software. | **TRUE** (Apportioned) | Eligible to the extent it secures isolated R&D testing environments. Must be apportioned based on R&D staff headcount ratios. |
| **Supermemory** | Open-source AI memory API and platform for storing/indexing user-specific context for LLMs. | **TRUE** (Apportioned) | If deployed as infrastructure within an experimental AI product build, eligible. If used purely as a personal productivity "second brain" by staff, FALSE. |
| **GitHub** | Source control, repository management, and Continuous Integration (CI/CD) pipelines. | **TRUE** (Apportioned) | Highly defensible as the primary environment for executing technical hypotheses. Claimable based on developer R&D time ratios. |
| **Google Play** | App store developer registration and distribution portal. | **FALSE** | Strictly a commercialisation and marketing expense. Excluded from generating new technical knowledge. |
| **Domain Registration** | Purchasing and registering web domains (e.g., .com, .com.au). | **FALSE** | Marketing/branding expense. Fails the dominant purpose test for supporting R&D. |
| **Google Workspace / Slack** | Email, collaboration, and general team productivity suites. | **TRUE** (Heavily Apportioned) | Classic overhead. Viewed with high skepticism by the ATO. Must be strictly apportioned (e.g., R&D staff headcount ratios) and documented thoroughly. |
| **Training / Education** | Subscriptions for developer upskilling or courses. | **FALSE** | Standard business capacity building. Excluded from R&DTI; should be claimed under general tax deduction provisions. |

## Detailed Findings

### 1. The Statutory Test: Core R&D vs. Supporting R&D (Division 355, ITAA 1997)

To classify any line item on an expense schedule, one must first apply the statutory definitions governing the R&DTI, codified in `<ENACTED>` Division 355 of the *Income Tax Assessment Act 1997* (ITAA 1997) [cite: 1, 2]. The Australian regime demands that expenditure be incurred on specific activities, not general projects [cite: 3].

**Core R&D Activities (Section 355-25):** 
Core activities are defined as experimental activities whose outcome cannot be known or determined in advance based on current knowledge, information, or experience. They must proceed via a systematic progression of work (hypothesis, experiment, observation, and evaluation) conducted for the purpose of generating new knowledge [cite: 1, 2]. In the context of software, applying existing logic to build a standard database does not qualify; designing a novel, untested data-caching architecture to solve a concurrency failure does [cite: 4]. 

**Supporting R&D Activities (Section 355-30):**
Supporting activities are those "directly related" to core R&D activities [cite: 1, 5]. However, a critical statutory threshold applies: the **Dominant Purpose Test**. If a supporting activity produces goods/services, or falls under the statutory list of excluded activities (such as internal administration software), it can only qualify if it was conducted for the *dominant purpose* of supporting the core R&D [cite: 1, 5, 6]. 

*Synthesis:* For the accounting team reviewing the 79-line claim, an expense cannot merely be labelled "R&D." It must be mapped to a specific, AusIndustry-registered core experiment or a supporting activity. If a software subscription was purchased to support an activity that *also* serves a commercial production purpose, the legal team must demonstrate that its dominant purpose (the primary, prevailing reason for the activity) was R&D, not commercial deployment [cite: 6, 7].

### 2. The Nexus Test for Recurring Software Subscriptions and Cloud Services

The ATO mandates that expenditure is only eligible if there is a clear nexus—meaning the expense was incurred *on* one or more registered R&D activities [cite: 8]. This is the "directly related" test. 

According to `<GUIDANCE>` provided by the ATO and AusIndustry, general overheads and broad project costs do not automatically meet this threshold [cite: 3, 9]. The ATO has explicitly warned against "apportionment of overheads between eligible and non-eligible R&D activities in an unreasonable manner" [cite: 9, 10]. 

When applying this to SaaS and cloud services, the nexus test requires the claimant to prove that the subscription was actively consumed in the execution of the experiment. `<INFERENCE from="[cite: 4, 9, 11]">A cloud server used to host a commercial beta test fails the nexus test for core R&D because its primary function is commercial delivery, whereas a cloud instance spun up specifically to run a load-testing experiment on a novel algorithm satisfies the nexus test.</INFERENCE>`

### 3. Category-by-Category Eligibility Analysis

The "Sandwich Method" below contextualizes how specific modern developer tools align with the statutory requirements. These classifications assume the company has valid, registered core R&D activities.

**Infrastructure, Compute, and Databases**
*   **Cloud Compute (AWS, Azure):** Eligible, but strictly bounded. AusIndustry guidance dictates that cloud costs incurred specifically for testing, staging, and development environments tied to the core experiment are claimable [cite: 4]. Hosting for live commercial products is categorically excluded [cite: 4].
*   **Edge Compute (Vercel, Fly.io):** These modern deployment platforms push application rendering and edge-functions globally. While fundamentally similar to AWS in statutory treatment, the operational constraint is that edge-compute is intrinsically designed to serve live user traffic. `<INFERENCE from="[cite: 4, 11]">To claim Vercel or Fly.io, the company must explicitly prove the environments spun up were preview/staging links strictly accessed by developers for hypothesis testing (e.g., measuring edge-caching latency), not commercial traffic routing.</INFERENCE>`
*   **Managed Databases (Redis Cloud):** Eligible if the database is utilized to store test data for the experiment. If the database serves mixed dev/production data, strict apportionment is required. 

**Monitoring and Observability**
*   **Logging and Error Monitoring (Sentry, Axiom):** `<CONFIDENCE:MEDIUM>These tools straddle the boundary of eligibility.</CONFIDENCE:MEDIUM>` If Sentry or Axiom (which ingest high volumes of telemetry and error logs) are deployed in a staging environment to observe the failure states of an experimental algorithm (satisfying the "observation and evaluation" phase of core R&D), they are directly related [cite: 1]. If they are deployed in production to monitor commercial user crashes (routine bug tracking), they are explicitly excluded under `<GUIDANCE>` TA 2017/5 [cite: 11, 12].

**AI and Developer Tooling**
*   **AI/Large Language Model (LLM) APIs and Assistants (Anthropic Claude, ElevenLabs, xAI/Grok):** `<MISSING_DATA>The ATO has not published binding rulings specifically naming LLM API subscriptions.</MISSING_DATA>` However, applying the statutory principles: `<INFERENCE from="[cite: 13, 14]">Using Claude as a generic code-completion tool is an overhead/productivity expense subject to general apportionment. However, if the core R&D involves experimenting with LLM architecture (e.g., passing data to ElevenLabs/Grok to test novel prompt-chaining latency limits), the Application Programming Interface (API) usage cost is a direct core R&D expense.</INFERENCE>`
*   **Dev Tooling and Issue Tracking (Linear, Ref.tools, Tailscale, Supermemory):** Eligible as supporting R&D to the extent they are used to manage, secure, and document the R&D process. 
    *   *Linear* is accepted as a project management tool provided it contains the contemporaneous records proving the technical struggle [cite: 4]. 
    *   *Ref.tools* functions as a ModelContextProtocol (MCP) server for giving AI coding tools access to API documentation [cite: 15]. If the AI coding tool is being leveraged strictly to iterate on a core R&D software problem, its use is eligible.
    *   *Tailscale* provides zero-trust secure networking. Claiming this relies on proving it secured the specific R&D development environments or servers.
    *   *Supermemory* is an open-source AI memory API providing RAG, user profiles, and context for AI agents [cite: 16, 17]. If integrated into an experimental software architecture, its hosting/API costs are highly eligible; if used merely as a developer's personal "second brain" for bookmarking, it is generic overhead.
*   **Source Control (GitHub):** Highly eligible. Repositories and Continuous Integration / Continuous Deployment (CI/CD) pipelines are the primary environments where technical hypotheses are tested, code is rolled back, and experiments are executed [cite: 4]. 

**Administrative and Commercial Overhead**
*   **App Store Registration (Google Play) & Domain Registration:** Not eligible. These are commercialisation and marketing expenses, which do not meet the definition of generating new technical knowledge [cite: 6, 18].
*   **Email, Collaboration, and Productivity (Google Workspace, Slack):** Generally viewed with deep skepticism by the ATO if claimed entirely. They are classic "overhead" expenses [cite: 19]. They can only be claimed via a strict, defensible apportionment methodology (e.g., based on R&D staff headcount ratios) [cite: 9].
*   **Training or Education Subscriptions:** Excluded from R&DTI. Upskilling developers reflects standard business capacity building, not experimental R&D [cite: 20]. These should be claimed under general tax deduction provisions.

*Synthesis:* The accounting team must annotate the 79-line claim by separating "Productivity/Commercial" (Google Workspace, Play Store, Domains)—which require heavy apportionment or exclusion—from "Direct Technical Sandbox" tools (GitHub, AWS Dev instances), which carry a much higher defensibility.



### 4. Apportionment Methodologies and Evidence

Where a software tool serves both R&D and ordinary business use, the expenditure must be apportioned. The ATO mandates that companies must use a "reasonable basis of apportionment" [cite: 9]. 

**Accepted Methodologies:**
*   **Headcount/Time Ratio:** For tools licensed per-seat (e.g., GitHub, Slack, Linear), the most defensible method is applying the ratio of time spent on R&D by the staff using the tool. If three developers spend 60% of their logged time on R&D, 60% of their specific seat licenses can be claimed [cite: 4, 9].
*   **Resource/Usage Tracking:** For consumption-based SaaS (e.g., AWS, Azure), companies should use resource tagging (e.g., AWS tagging environments as `env:rnd`) to isolate exact R&D expenditure from production expenditure.
*   **API Token Apportionment:** For consumption-based AI APIs (e.g., Anthropic Claude or OpenAI charging per million tokens), apportionment cannot rely on headcount. `<INFERENCE from="[cite: 4, 9]">Developers must utilize distinct API keys, workspace endpoints, or project tags for the R&D testing suite versus the commercial application. This enables exact mathematical apportionment of token costs on the monthly invoice, directly linking the token burn to the registered experiment.</INFERENCE>`

**Substantiating Evidence:**
Claiming 100% of a mixed-use subscription routinely triggers ATO audits [cite: 21]. The legal team must ensure the accountant has access to timesheets, AWS billing tags, Git commit logs, or API dashboard exports that mathematically justify the applied percentage [cite: 4, 22]. 

### 5. Excluded Activities and Expenditure

The `<ENACTED>` legislation explicitly prevents certain activities and expenses from being claimed.

**Excluded Activities (Subsection 355-25(2)):**
*   Market research, sales promotion, and management studies [cite: 6, 18].
*   Developing, modifying, or customising computer software for the dominant purpose of use for internal administration (e.g., building a bespoke HR or payroll system) [cite: 3, 23].
*   `<PENDING>` Activities relating to gambling or tobacco (unless strictly for harm minimisation), applicable to income years starting on or after 1 July 2025 [cite: 5, 18].

**Non-Deductible Expenditure:**
*   Expenditure not "at risk" (e.g., guaranteed returns or indemnified costs) [cite: 8, 9].
*   Expenditure incurred in acquiring, or acquiring the right to use, core technology (e.g., purchasing a patented algorithm off-the-shelf) [cite: 2, 3, 8].

### 6. Record-Keeping and Substantiation Requirements

The burden of proof in the self-assessment regime lies entirely with the taxpayer. The ATO and AusIndustry have escalated compliance requirements, insisting on **contemporaneous records**—documents created at the time the work was performed, not retroactively generated for tax purposes [cite: 24, 25].

For software claims, standard project management artifacts must be repurposed to prove technical uncertainty:
*   **Git Commit History:** Used to demonstrate the "struggle." Commits showing reverts, failed attempts, and algorithm optimization fixes prove experimentation [cite: 4].
*   **Jira/Linear Tickets:** Establish the timeline, linking the human effort (and by extension, the SaaS tools used) to specific technical hypotheses [cite: 4].
*   **Development Logs & Slack transcripts:** Providing they demonstrate technical barriers that could not be solved by standard documentation (e.g., Stack Overflow) [cite: 4, 24].

### 7. Offset Rates, Thresholds, and Financial Caps (2021–2026)

For the timeline in question (Aug 2025 - Jun 2026), the financial mechanics of the R&DTI are critical for calculating the net benefit of the 79-line claim.

*   **Turnover Threshold and Rates:** For companies with an aggregated turnover of less than $20 million, the `<ENACTED>` R&DTI provides a refundable tax offset equal to the corporate tax rate plus an 18.5% premium (typically resulting in a 43.5% total refundable offset) [cite: 1, 2, 26, 27]. Companies above $20 million receive a non-refundable, tiered offset [cite: 26].
*   **Minimum Expenditure:** The company must incur a minimum of $20,000 in notional deductions to be eligible to claim (unless using a registered Research Service Provider) `<ENACTED>` [cite: 2, 8, 28]. The ~$A6,600 claim presented by the user *must* be aggregated with salaries and other R&D expenses to breach this $20,000 threshold.
*   **Expenditure Cap:** The maximum eligible expenditure is currently capped at $150 million [cite: 26, 27, 29]. For R&D expenditure beyond $150 million, the tax offset drops to the prevailing corporate tax rate [cite: 2]. `<PROPOSED>` The 2026–27 Federal Budget announced intentions to raise this cap to $200 million and raise the minimum threshold to $50,000, effective 1 July 2028 [cite: 30, 31, 32, 33, 34].

### 8. Overseas Suppliers and the Overseas Finding Requirement

A major jurisdictional risk arises when software companies use foreign-supplied tools (e.g., US-based AWS or OpenAI). Under `<ENACTED>` Section 28D of the *Industry Research and Development Act 1986*, R&D activities conducted outside Australia are only eligible if the company obtains a positive "Overseas Finding" from AusIndustry prior to claiming the expense [cite: 8, 35]. 

However, a crucial distinction exists between an *overseas activity* and an *overseas input* to an Australian activity.
`<INFERENCE from="[cite: 4, 25, 36]">An Overseas Finding is required when the R&D activity itself (e.g., the human labour, the offshore development team) is located outside Australia. If Australian-based developers purchase a software subscription or cloud infrastructure from a foreign supplier (like AWS or Vercel) to conduct experiments locally, this is classified as an eligible Australian R&D expense, not an overseas activity. Therefore, paying an offshore SaaS vendor does not trigger the Overseas Finding requirement, provided the physical testing and development occur within Australia.</INFERENCE>`

If the company utilizes offshore contractors for development, an Overseas Finding is strictly required [cite: 4, 25]. Furthermore, `<GUIDANCE>` TA 2023/5 emphasizes severe ATO scrutiny on arrangements where Australian entities claim the offset for activities conducted overseas on behalf of foreign-related entities without fulfilling strict statutory conditions [cite: 37, 38, 39].

### 9. GST Treatment of Notional Deductions

When a small Australian company reimburses a personal expense claim for software subscriptions, the legal team must determine the exact numerical value of the notional deduction. 

Under `<ENACTED>` Australian taxation law, the R&D notional deduction must be calculated on a **GST-exclusive** basis if the entity is registered for GST and entitled to an input tax credit [cite: 40, 41, 42]. 

*Synthesis:* If a subscription to Sentry costs $110 (inclusive of 10% GST), the company claims a $10 GST input tax credit on its Business Activity Statement (BAS). The remaining $100 is the GST-exclusive expense that forms the basis of the R&DTI notional deduction [cite: 41, 42]. If a subscription is purchased from an overseas vendor that does not charge Australian GST, the entire converted AUD amount is used.

### 10. Audit Triggers and Documented Denials (TA 2017/5 & TA 2023/4)

Software R&D claims are subjected to the highest level of scrutiny by the ATO and AusIndustry. `<GUIDANCE>` Taxpayer Alert TA 2017/5 ("Claiming the R&D Tax Incentive for software development activities") remains the definitive enforcement posture [cite: 3, 9, 12].

**Primary Audit Triggers:**
1.  **"Whole of Project" Claims:** Registering the entirety of a commercial software build as R&D, rather than isolating specific technical experiments [cite: 3, 11, 12].
2.  **Routine Testing:** Asserting that routine bug testing, beta testing, User Acceptance Testing (UAT), or system testing are core R&D activities. TA 2017/5 Addendum explicitly states these are ineligible unless they are part of a specific experiment to resolve a technical hypothesis [cite: 11, 12].
3.  **Broad Descriptions:** Using non-specific language in registrations that fails to distinguish the R&D from ordinary business activities [cite: 3, 11].
4.  **Related/Associate Entity Discrepancies:** `<GUIDANCE>` TA 2023/4 and TA 2023/5 target claims where expenses are paid to associated entities without being truly "at risk", where the R&D entity has not genuinely incurred the expenditure, or where the IP is held offshore to the benefit of a foreign entity [cite: 9, 37, 38, 43, 44].

If an accountant submits a schedule claiming 100% of Jira, AWS, and Slack across the entire financial year without timesheet-backed apportionment or specific mapping to registered experiments, the ATO views this as a high-risk indicator of TA 2017/5 behaviours [cite: 10, 11].

## Knowledge Gaps

*   **Specific SaaS Tool Rulings:** `<MISSING_DATA>The ATO and AusIndustry do not maintain a publicly available "whitelist" or "blacklist" of specific software tools (e.g., Vercel, Slack, Sentry, Claude). Eligibility must be derived via legal inference applying statutory definitions to the specific use-case of the tool by the taxpayer.</MISSING_DATA>`
*   **Safe Harbor Apportionment Percentages:** `<INSUFFICIENT_EVIDENCE>There is no statutory safe harbor or flat percentage approved by the ATO for apportioning mixed-use software (e.g., "claim 50% of Jira"). Taxpayers must calculate actual, defensible metrics per claim.</INSUFFICIENT_EVIDENCE>`
*   **LLM API Treatment:** `<MISSING_DATA>No primary regulatory guidance currently exists addressing the specific treatment of generative AI APIs (e.g., OpenAI, Anthropic). It is unclear if regulators view AI hallucinations as "technical uncertainty" under Div 355.</MISSING_DATA>`

## Recommended Next Steps

1.  **Enforce Headcount-to-Time Apportionment:** The accounting team must request developer timesheets. If the timesheets show 40% of dev time was spent on registered R&D, apply a baseline 40% claim rate to per-seat mixed-use subscriptions (Linear, GitHub, Slack) to preempt ATO audit algorithms.
2.  **Audit the Cloud Architecture Topology:** Mandate the engineering team to provide a cloud architecture diagram separating `Production`, `Staging`, and `R&D Sandbox`. Only claim the invoices mapped to the R&D Sandbox to ensure compliance with TA 2017/5.
3.  **Verify the Minimum $20,000 Threshold:** Because the current SaaS schedule is only ~$A6,600, immediately cross-reference developer payroll and contractor expenses. If total R&D expenditure does not exceed $20,000 for the year, discard the SaaS schedule as the claim will be statutorily barred (unless using an RSP).
4.  **Implement API Token Tagging:** Instruct the developers to immediately split API keys (e.g., Anthropic, Redis) into separate "Dev/R&D" and "Production" keys so that future invoices are natively apportioned.
5.  **Tag "Excluded" Commercial Line Items:** Instruct the legal team to immediately red-line Google Play registrations, domain hosting, and generic marketing SaaS from the 79-line claim, as these cannot pass the dominant purpose test.

<REGULATORY_MAPPING_ONLY>This is a factual map, not legal advice. Confirm all enacted obligations with qualified counsel in each jurisdiction before acting.</REGULATORY_MAPPING_ONLY>

**Sources:**
1. [viridianlawyers.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE0CKe6oCKaUaiPna4yG_zCeBKUTUtuhCMwmP94v7AMXnabLW8G68FzWSXyUMb0Akgi8KYhR4G1ssFQ0_haUA-IcefbgHtEMwD22RBjDP25GbPsiyCTfg8SCAEq6HnIf6ko9xAyK_lTJ6_u3sIrkc8Z2g==)
2. [oecd.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgbOY-_uvu_mqUauU6DkIbVyqK2Zok_lDttannSP0uvfDCbRmwKyE-8_aKRWjAk2pAc3sLSpNlBZm2BqSDYmF_vRkSdt9fZJGqX8t_Ik-KEx1BzY3tnEriX2Exvgv8gW0-LFg=)
3. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFeED5x1450ZBaLs574YbqWrqvQGYMq-mMINKSXtMkdI0kxgl5fVimP-twqaw1m6VIT8LdXcIKVQR2hAZoaDBTSEe6_yTZBl0kw4UC8rne2PCvYPA9TP4erOd9vOO7Agb4HSHYAq5jXOfHPDrlPp_flyNbdcWwqgH4t1ywQLDOANsY6-u-RRzOuhQcL2bAEEy6)
4. [bulletpoint.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHEaA2kWHXBgqQHu1iqunWAJqHnbtVXBRz0ExlI9tH6_4ftnY24E5Lumb71tIl_2DV52X5MbHw1YsfHLmClMLm_RwryO-u76E0DJPrvloHIEwYUzRej9QEe1C9ak3eGHP3YeodugpLoTrk3mezed3vuxt0M0EG1IUtrHc0=)
5. [business.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGaeWq2k91a96vkM5zZdfjOdKEq9zaIyAFlchpj7Qchiusv6iuaHWAXsjk6mGBlHsZ-6QCjaH6N4Z2rPHOBzDRLVPQnEm2IpghSRlVUvHK8F6OWOAR2qR2terr3K2ZO6cPhT8LNxbXeyV5gaMcXtdqJkoON-u-nFSsMNeGddLWbH73vkg4PRTQr3Lkf2dTCQPxp5vEr-4l3ZvjUMfnMWKqlDEqeOOSKwd5IiyOHEnBmC8NThTpe5JqYzp-bHQ2dnQ==)
6. [pattens.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGoRoQxuM_kHyg3mjHGrykkDcL2enfcfSi5oSj6HydiOoQ-3gWX44ZxZcglbHTEAIYTj8r6cn2yt12svPtJr7meg-J3HbQf2OskdUF-AEe5vd31bG5l-FRjTYRo)
7. [business.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHh2msWM8lmHFO1vkEoIE2CLOthktwZSvWwamHh2G0j6ws-P7XGUlFeVt1nRJ70ZpMS3HZUG8AQMVBp5PGuWltdTkkiAJvn1cUc7RuNr0NA549X3sSkcxPwRoE2crvzQthOUFLm8Ep7DX69fg83PRMx3XiQaJXxPQn3ssNfvzJsojeo2pwEVqxjQxLG9o2piR0_bwcnJSQVM9JwQr7JnoXNmOjPBYz_tRQyZGS-TqaspacTcoyVg48EWYdd2a-TdDiALUegdjQAdAVpOqcpArAyzYY3eBrEeA==)
8. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG-MskoVCBep6AkQlnNPwjtc6435RsoCGQ8lAdDHyONbYSUrOtaDtydZYWrUAPMcJj2BXpk8gDVgK3YuRu38l_3dTLiiFX9R06Anj5OFF-Mi144f3v61pLc1n0wUbjTDTZCLCPR7DgxZlhkefcHeP31Sff_u4trhFUTU--q7UewfUNIm-7sZ1JKnNwl-zirUkPz6PAIU_YO_TPl7Ss7_DX1zv4hVpU8KKo2nO5Fo5sCkNu9YnrbCcpLOr6ky43qRR5vEk2zlGr-4pJoe8y5UnJzwEt7Qge4YltLMqVgup3UFczjz6xI6fanQn_SntpcPEaxI7FY)
9. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFE3BEGI3C-grX4FoLQ9iVDOCA7Stik_1s4x6P0y_z4fzXjgkmoc8PiMClbmchUaOn2KBq60yO8dD0akfDHaJtSYxFYzUlak9RlYNThly2A2N58oa-fGdT-T1OCcZFxweVhM80XdYxA9v7T9B1R_mNpzMSSvx-sGHAtiK4ZaWzLZqTJAffrPf4RYIELSVXfWob86rwP2vODtlEX5FNjQohqTtWln55RStiscp7ZZ6JcpuWqHo7MLGQ7R66sPKZ1laXOFD0lVY1yj1ES7UnEtvURrvWDwUmhH7ZKDKL5nJaSiQeJZCDJALLjlnXyOmBtOA==)
10. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG6sVBa3WMt3so3pVCZQfhwEjW_UYXC-U9z5P7PA8CJzugnNjT-M1nO7R-caJHofWpa1EP_QLVXQPixbdB9B1Yi18WLsVUi3_pP1xzIzmHN9Nd0qnk0UoNTe0INVVvyiUaopCTJzmoQ9zDuA6Ges-HQT6fQi0PaZftwUV3KOzuCrD_2H9k4zgFZCeIaXZpChfQiqbDEG1JSrxurA-O5fkRl8OXHBTlgFH232MbTIdtm42rmZ6PCjbX59Ltn8burRASVxbp7O0OLPmXzkNQOysSBgbWFBjillNO3_X6-4x_m-kzwhu7_JbIvlerHyH33Q0NeuK9n46_eI5DOdTztt5B89nKMhO0rVk0=)
11. [hlb.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHliWFYT2ODDsW8j9HAf9Nbv295D3iqBzDO1HgA_0zTIPdofxKj4yZB6wBup89V_l39i4PtcLdwGeyXYV47oN0P809p0cMa8449xBR1yCWzDNlUA5jTtwbJCzsRwgMX6GgYfS9BfJZ8gtnvesDBCNIZEhYCLf32)
12. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH-22n4EckU42wqGWVVEACTDVHgv5jrd5F-Lz1Uq-b_iOZ1IBbRycEDRPWU1S95mbmeauUaVQ6LJCaSSCe6Hy0QBStpNKicjc4pON62R6Y4igtkPHfRZxPDfSvMLpE0tUDXFCA5CjbUgth2bvVYUdNZaj-4CNLvWrd2oK2Zng3dNwZWKKXBY_Tq_EKz8DyHDBs60A==)
13. [gibsonpromotions.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGfLlpGAVBCKElfeKcd0BgRSDa2wCiKQaN4uq--V7n-kwF-3819q12Y8g9jsDpjFEzZFXMVQAdPlWyL-5ruU29QWSOjpf6RmS53weEDt12RbCHo1wVvN1C0xlcLwhXlStqE94iSDpsTKVeGHvoJnkarAswX4dd9R_BKudAaHa1kaQLTgM2DeQ==)
14. [vistra.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGZ-Kj1O40nvdgXOqFoLvSHYNPVgcig2s1_k6STGhaw8WX7MFVUZU-BlMBhxty1N2yH-sDqtu6H0GMxfjqwSOrt3UwgHPCfx6-zt92731cEu5mi7uzMIZHMG0dvt_WwcOFUAGO9pwdwrS69NyOxDxJid8vdylHVlJnaZ0jflYSyaeFGuFy0vaNBzYJBLOG3OUtbEJdE6LUzlWyXMsB5yN5egJiy9sBglw==)
15. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFJVkH0F7-4kjVcGauCrwKyzUgeuVsGe_sHcni7UGHfFtCl7WmoFU575tiuPqBAnREfFx-AbU1BnIlUcKnJPJJk_oskDhWYOkjPTc7gACWJ69z63zGz-wIOiHcs3mYv32g=)
16. [opensourcealternatives.to](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5PBUxOAbpZSOBcHP5356cCh7YaWsLQK_UL2ooXquHUmsskFC9keJbAGRT2ageJ5fcmd8-VcKQahY5N1r5SKohzUFD9meF94wn1JTs9sFDh6c02R3tk5jqNCl1L3IKPVlqpwIQeelYyFiQU24=)
17. [supermemory.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG0ivNzuqxhMikPjTPcUBVWz4mVyBqHmUmMlQC6B8DJLC3giR3B1UidHyVP8LUiHzdvrcrKT7iTo_BNchNx0yjlWCiqhcaxlLZ4EZ2ZNg==)
18. [aph.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG2LGTaxMQb8NWVCwkiapyybK387o50vyHR4iSf2yfwA08BsKCCDOI1L57DxtnoFdOs29K3kbqGDAbjrsKOK8OqSZ8JekYLKe2OGm_GKw9RqFbR4bowJ5B6TEHgo9BpdNEMfGjKVja9qq59bmaoX6Dr2LUFAEO9pOYADgqndRfIaSKUCANE0Qc=)
19. [randadvisory.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhI3qCBfPwO8V2JWzc0HAW7Y0oZwjAUphFIRcNU-U3ieQ1fvB622ywu2A2kNfC3ckCC8VDPwdAEgW6go-05JxOp4V0Az1Q3mOcMEukjDpvueV_daculP4ZrfoqUgEewwH18M3PhEds_8sfTjH5ehGWaeijnGqqDHw=)
20. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlWWJNQTMmuCSw0oc0v5EG7fbFq20i43PmTk_zpgp6P4Lbz_GRxTI4K6xMUfRybdeZOs0vbqx3qNcKi5Hmb6ZFRkcxJ3F9-QlaOvdg_TCezGsx5LbYew5vXuxI1imoPYcGW-yOs1E0FyTd9MZ-9iiQQBdCkhgT3WdBr5T3nnlaQ8j8L7E8HCRcV_Gcp4uyq-vBYRmVIPBJGymB5Px8NdHh1wc-Qp7jPhAiCPX53bhHJVuq9-b1moNdGVinnJ0GXuAfAiU6wLvHyktyj29Ip1QL9atANg4iz1SJPgkfBQCIVJrVjQ==)
21. [wisemanaccountants.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGeSi7bAlnyOTDDvDei5CQBXIj1iNcZ7ICNJZSVXzTEBF7B6u29aAu0Au6C5bSglFLf0xVMYH5wJVjzCWK7ysrQI_TP6QBODLKWMnQxMK-A1KUyTRP2mAgPO2MZiUGdZ3tPQ6yCfgWdwynFPwpOsXSnCE5t8E1a0RgChnalM7p2R35qlXSKJrAJjvwmtR5vF4zO9QKw1iTBPcKBEZBHeTh59oD_zcr5jW-gisRstJ4U1n3ZTbSxDs5Bt9sBX1zdQFHvFQMqQVK8KA==)
22. [claimkit.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH357Sc1iRMCwbfmNswfXayldafdOCbg8PLJnOJdNnzrZMcNjr_4x_aioGfi0MZq_8q_KjHEKi1dlxCBFxDvawhi5NAc7z50DIKdegHYNoZ5v1552PoNe8ugODpKUye7b-O6Cej7HgSbH3PTxuGCgE=)
23. [business.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpMLP-voBpfB7uHCzE0cnA705rXiBkIsaJLHaeKYix7jk4EtTpqkVMxAilXv5SZszIr6qdGuNH3xKvIJascZA6J8s_TI6_tR7cNo0sDIKqAbxjNJZDeFcpS-2nre8MY-CjbGW2_EkPU8LCgSpB6W7gGzHZjLycO99Gxz65bVByFKUzvH2etKauE8XHONX3pjIHUffsoU5KspAfWDLGzP-oY6RVO2cGFd3eeMUMOD2CtQ0pwY0K0WLAxtUsz14gDU5ByLr_s-NwUfcNnSd21_mzWg==)
24. [thegildgroup.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGjapVAksTDebgIuyPgiKXTUUoguDDXk3yp0kyp_in4ui-4HpCiCDWda3H0L6u6fzadsk_DXDiUajhMqAt3pEuSl__ZZiak485NdAMQQf-9mTsJ6ZuLzsA6HQrKRALv_wmxrNViAKnURNfl7r485A==)
25. [segueadvisorygroup.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGdCvEjS_YPlHuay_gJKeeGfcyMjCvoS1HFiCgqTRi9_E7Bh1yPTqCQsl79a9A3_4PvQG7lwGjBlXzz4neI_bXAn1P5ZEa8nLxhkSTMHFNeUybPFA5q8W65V21HFo4GJ-kpEadgab3wn8LUsbu6YMogCmAQ9vFEZcLB1_zNMvxxdZZ3KveiChiLkYLylpI=)
26. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHe8z4sziVxd1sMCeHgEnmRujHyezfCYexdVH-EKK1kT5do_irnvGXNcypWF5p5SZDCCg6wa7Olbc2nBzaW5Pu3ZDvj0TsJSRePU21y34bGUP-rAStWlFTiN1a4dfXqx2aoQXm4NCRDmk90RAnCranFEaXQWrcTjAQqBLMgX4XA-rETovBkXHDM5tq7hd522bdPSEBoSbMtk4nd9Gwnmo0bSQczlIoG0F_57fkykPsRzII0uTMcc9DGHlrvN-mlxouoO9esiGDv1ovm-YVp1dTCsye7TFKxN3qIaWqKA6cRNkdvFJCYVDfgC7Oti3o-SCtfhQ==)
27. [business.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE4nzLLcjJiUemC9WZXVbb3fkv3wXXjeKmB1b9dnXXB620v2YJ8HpJYRTXwAM0tuK__EC-h62i71-P5EIMos6JlZ4K_2XavFKQFqLPyGCNvEVnfdT1yllZBpcqnjN8PvZeRvs9t8Eub5jOeqPkMBb6w6lA_LVqvIoJ49L-EaX0zl652QdhO3aua-qSLKJojKbZaA80EvAtqVaA2qHYdUaQ-QEoAU1Y=)
28. [rndassist.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF3mSiXt-9Np38QSyVGRUjU_ffnYhWAM45eKQO90y7shlu2LB0EG9oICBdlRYL7WKTUNH7_fujLImLiDmGC905R-PSJdyvzdLUmvmuHIb0dIrEFYrWY3AtjW8o0HweU3HPFEe9wIaeSYXp4XK2uXHtlFY-ktDj9Ul1L1p6Q1DZhZtpNmw==)
29. [ignitionresearch.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFaqZ2L_uoBeqTy4okodTmQFepgjHTT8QYOuxh5TsMuU_wTN-3I1kT_4ekzU3qHAYbUI4HYjcJ5F6TWa7k5Dib1uqyiDBV4uq_8GfmrzibrYzTjEa9bDYRpYmhql5OdOy3FKsSm_Qu0TovLVBI=)
30. [davidsons.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEaSre4xuz5yBzmu6qKQWVcHWkqRf_0ZU3zKH4Abe5PmDZ_JR4163OZQT4R5cRvUfIWoT5kQX-6n1mdtPNwr_jVveHKSpkGAEKJQEwk2gMjleAmdtj9fwLZpOcM9SSnadwljJ7cIpIqIj9OyyKBeFRlyhm0H3IwV27RjLiAaSFlWG_Z1cKLGvqxai14AV7x9xv0mhAjMPFABY8p9yJS)
31. [fortisap.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGFMhodsUrdZrrrHr64NeSxM6XqwHccjI2a0qtwQ7hDPgQ2ZiWZlOULJVg22pRL7M13jTJzhrbwcU20aBWfBYY3Kft0o6cbSoIRuWDvkE_Kg4PJBskelfnl4KVwsou8HxefyJpEMdY6WjS5ezmXsJscl3inHXtU58yrLU9RAYr2D-zzkmQgV5tgmRV0e8xHR_ZF2gzjTdC2yAO_6_HwYQ==)
32. [obrienaccountants.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHgkGShTgFXD4v2_I7CW5g2H-Kbgchl7OiDMIIA7kTtEwFKcbE-mp6B_ie8gRI7NJEOpgyZkQDQtI0Ywv1mQe0aLhS3Vvti804SuQ_wO3xsuCN_xe5-QEYuNaGmQ7o=)
33. [bakermckenzie.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGaWEqqhjjPyC9x2sBpkayQOxReLiW9hpJBYZ_CFQYQhz2l1kaidduARsmouzVbMwdghAXJNW14d-d9M0f-feIXXayAjCfv1b_iUlFzP3n0r4LgIWkcJtVpb-6Qli4p_VnbYtuQg5drZ24OQYlwAr2eFN-hnfnt54Wdu2lee-M75TFhqYnW-aNEpj45fWmC3cWqt9spGBCzN-SdUg==)
34. [pwc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE2LgTHiOaeEmXTSAMJdTTp2Nyu-bfyHzg1zktV-2HQBrWQxe1cWuhaXR9GgAPGNYHgqTqgi3Ok8IXxSS-9Ly0vIzQeaisBCnzdpHH364zWeGx5Q5cz6iTRaeMpiq6DZBs7FIy3AXvuKUTQjWBB98qnGZnlttMLvnL4SFBETnkGlBM=)
35. [business.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuDoLVxFO9QGMMaIYLUqcDEYUwptr_0EsAaYTquMMMZT43diZpSKvx7mgFzwsRdUnbDLEFyF-CEl2TkzADrvEhlxh4FaZ6TMoyyFKLK_61IURpRf_7XeFAjaidBb7n0gGqDpEYDgUWpb5gDlaeKzDBHu-RVvXY-ug1BCJvSw48xrTEOjU7bw5qW0L-8VrVdlMHpbotUN4lgzlXkaEWqOV3aVnf3wiD)
36. [rsfconsulting.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG39WjuREQZk19IakmCvVcAKhQZJW-7IHtbw1w8liKDCCSEb4LhwnWD2wwjEyoQb_eebi1u0_2IaYoLzMFSGHKAWLTON1wFD8NrGjtFgzjmM9dh8vvZh6s2)
37. [fbrice.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhZ5lvrfraiNWvN67FHR3dU_QTW6z1cPNeo8XT2rML3PidRSNrwvCbOSjeIEHgoqx-TrWFwyJy22pPJt6CdyWmxTkxFuzNftrqZWe6cM_OKkG5LqxX742jDt3seyJlVmzCEiGxeW6UXooZYLQEVRJpesDozqh_-_vsU2FVP20kC_pJC0YAbQnKEZL0ZdDaoKHZPCocQSnZUwYJ5w5sHw==)
38. [taxathand.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFN2DaIUW5rw1k0M2MyBMtImPfeuhfP_S4_eNYKup5QyVMgI5l7x06T7MStPy0Q0yiNfDHVXyb6QnEgpw_SdZTdgwnjyiIPshV-32JwRZ3zTMHeUsVc_tNaA8xvUwezECpSo1-Z6EM6Pbu-2FTyoPEIBQyF-h6PXuqSTVSo7V2S7o4YKSzroCJhbscsqLq_Aw==)
39. [guests.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFaQ62OagInfR-kxhhpoIdJilqu8s8-cJk_S7Eivx7SEsevMkzsb4XLqeGMoA9pSnQ71YHFXhZkrHpARPitO-cEm-RI7PV0gcv7SqAsfVWL9SYdg3nVET8UZFiKXNc1yFzXNd_yV0V7sdtQWIrK_5k94lH5z21FvN84cpvrbA_02FP8PWZOakrdmYtavUrNwrkdm0R-Sjm-KNE=)
40. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHoGZFdZS0GDWJFXrZPEHr_2mafhztB7KjYX4ew41oIdu_0Zrn34Op7V-lM-RIxHG5lVylDWlMT8u-FIlkz2VGzzbSvRPQJ9g_nxz-6tslNM65L7ba71FF_1M1dU6PzzDFODKlt9RDWyL5kmDBaSryxxtYkkcGxLsb-0FqzJXyMfSSfI9wG6v_hH3A1xycN2jw2WDLadbHom6wlYQVyshrdDg7v7kto6MFnzjJkQHCWMnUFxA==)
41. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFl7jxfmTjRGt8LPuNNjEzqL7Ce4ci0B2xAwdAHXMdmWTPd-ctrkREeK2y7mUGBLb4WkqvJxLPtIKy8ljFyKVoTAfVjd51EXSSKRgWPx5j_scBUrZLZGCic5IqW6umWXqkGLsE8q70M4zIs-G6faWH1jJ-os2rWcJ2Geubs8aiv7W14h68HcC9Fz0HedmS_7xBWMT4rTZMLo2GZVW4WO8H48-a7njNnsNg6jxzcNMNSe7B9Gg6Kx9PpUo9KBROSshYCIg8uFNgwva-DO0XnFNNBwN-peas9oA-I1IrCSwTPd_UjKLIP)
42. [ato.gov.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_YuGQ_VsZXIhqUjRtIDcxSmI3lYoZEeYPjG3_o_RDB9DLF-0gkvSi7SljgKwSwoNAnjWcszNv-wE211o4VQinLh-I6uArr90zK7Eza7s5YZbVECILPlc4iRHxOyWxWvFAepuN4oazl6IkZ7T6mlO6ydgJtPwE4t96UmwrP1Q9BaXlcRznNA==)
43. [pwc.com.au](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFVQDNaBykw8JUUGDuo2K3ed7MK677f3cW9OdOTNFqikI7LvIkX5BYSdOzxBiLDROu8q3sDMnky0FZuhKYuZmbSukBViRRo4O3uETU6JbAi2nN4XAH5_rsMYv77DspC8BuT31LTQzFneVrRg3orOWlrotxwLqCvijrXXIKxKsD5R8Xpa2yQ49E7kjNA-zmSNBIqGuCBXhI0tR7wPLUkYwe4zlo=)
44. [incorp.asia](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHc7OHIcSW0TZxtafIkoSL5QrH0b0OjquEL17V3nVPKi-TcKgjhp0BJzfB9PPNkV2LHMhOhfHAfavCT7XlHVwA260lDloUAC2ZFTYkyiCSfZgFw2k1C-7DAVOh68RWqJe6-Sw==)
