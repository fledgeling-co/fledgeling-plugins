---
title: "Evidence-based question design for software coding agents"
run_id: dr_735b0dce7a358c3e
question: "What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly? Cover: (1) requirements-elicitation research in software engineering on ambiguity detection, unstated assumptions, and the measured cost of building the wrong thing from an under-specified brief; (2) survey and questionnaire methodology on question wording — question length and verbosity effects on response accuracy, jargon and readability effects on comprehension, satisficing and response-order effects, the measured cost of vague or double-barrelled questions; (3) judgment and decision-making research on choice architecture — choice overload and the optimal number of options, anchoring and default effects when a recommendation is presented first, whether recommending an option improves or degrades decision quality, and how offering a free-text escape hatch changes response behaviour; (4) human-computer interaction research on interruption cost — when interrupting someone is worth it, how question batching versus serial prompting affects total cost and answer quality, and how attention and context-switching costs are measured; (5) plain-language and readability research on the measured effect of simplifying wording on comprehension, response rate and error rate, including any measured word-count thresholds; (6) recent work on conversational AI and LLM agents asking clarifying questions — measured benefits and harms, over-asking versus under-asking, ambiguity detection before asking, and any benchmarks or evaluations of clarification quality in agentic systems."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: academic
sources: 60
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-09T08:21:23.623Z
---
## Executive Summary

- **(High Confidence)** Ask only about **consequential ambiguity**, not every missing detail. The governing test should be expected value of information: ask when two or more plausible interpretations lead to materially different implementations and the expected loss from choosing a default exceeds interruption and delay costs. Requirements surveys show that incomplete/hidden requirements and customer–team communication failures are common, but case studies also show many textual ambiguities never cause defects. [doi.org](https://doi.org/10.1007/s10664-016-9451-7) [doi.org](https://doi.org/10.1016/j.scico.2020.102472) ([researchgate.net](https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requirements_Engineering))  
  <INFERENCE from="NaPiRE prevalence of consequential requirements problems; Ribeiro and Berry's evidence that many persistent ambiguities were harmless; HCI interruption costs">**Rule:** ask only if the ambiguity is consequential, cannot be resolved from repository evidence, and one answer is likely to change the implementation. Otherwise use the safest reversible default and state the assumption.</INFERENCE>

- **(Medium Confidence)** Use **one decision question by default; batch at most three tightly related blocking questions** if all are already known. There is no controlled study establishing an optimal batch size for coding agents. HCI evidence supports reducing interruption episodes, while survey research shows that task difficulty and accumulated burden increase satisficing. [doi.org](https://doi.org/10.1145/1314683.1314689) [web.stanford.edu](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2009/2009_handbook_krosnick.pdf) ([doi.org](https://doi.org/10.1145/1314683.1314689))  
  <INFERENCE from="interruption costs plus survey satisficing evidence">**Rule:** one question normally; two or three only when answering them together avoids later drip-feed interruptions.</INFERENCE>

- **(Medium Confidence)** Present **two to four total options; default to three**, including any “Other” option. There is no universal empirically optimal option count: a meta-analysis of 63 conditions and 5,036 participants found the average choice-overload effect virtually zero, while a later meta-analysis of 99 observations and 7,202 participants found overload under high task difficulty, preference uncertainty and option complexity. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([ideas.repec.org](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html))  
  <INFERENCE from="conditional rather than universal choice-overload evidence">**Rule:** show only the options that produce materially different code, normally the recommended path, the principal alternative, and “Other.”</INFERENCE>

- **(High Confidence)** A marked recommendation is useful **only when the agent has a defensible, preference-aligned reason**. Defaults and initial advice strongly influence choices: a default-effects meta-analysis estimated \(d=0.68\), 95% CI \(0.53\)–\(0.83\), while advice experiments show adjustment toward advice can occur independently of its quality. [doi.org](https://doi.org/10.1017/bpp.2018.43) [doi.org](https://doi.org/10.1027/1618-3169/a000361) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html))  
  <INFERENCE from="default-effect magnitude and advice anchoring">**Rule:** put **“Recommended” first** when repository evidence or explicit constraints make it superior, give one short reason, and do not preselect it. When eliciting a subjective preference, use neutral ordering and no recommendation.</INFERENCE>

- **(High Confidence for simplicity; Low Confidence for the exact count)** Use concrete, familiar words; one issue per question; active syntax; explicit scope and time period. Eye-tracking experiments found that low-frequency words, vague terms, ambiguous noun phrases, complex syntax and complex logical structures increased rereading and fixation time, with partial \(\eta^2\) values from approximately .12 to .40. [doi.org](https://doi.org/10.1093/ijpor/edq053) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension))  
  <CONFIDENCE:LOW><INFERENCE from="psycholinguistic burden evidence, questionnaire-length evidence, and absence of a validated word threshold">**Operational target:** 30–60 words for a complete one-question block; question stem no more than about 20 words; each option no more than about 12 words. These are implementation targets, not empirically established thresholds.</INFERENCE></CONFIDENCE:LOW>

- **(Medium Confidence)** Offer a free-text escape hatch, but make it **optional and secondary to the choice**. Open-ended prompts capture unanticipated cases but have substantially higher nonresponse: Pew analyses found median nonresponse of 12% for one-word or short-sentence prompts and 17% for prompts requesting multiple sentences, compared with roughly 1%–2% for typical closed questions in the same panel. [pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/) [pewresearch.org](https://www.pewresearch.org/decoded/2021/10/14/why-do-some-open-ended-survey-questions-result-in-higher-item-nonresponse-rates-than-others/) ([pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/))  
  <INFERENCE from="open-ended nonresponse and option-exhaustiveness evidence">**Rule:** include “Other — add a note (optional)” when the option set may be incomplete or rationale could change implementation; never require an explanation after a valid selection.</INFERENCE>

- **(High Confidence)** Asking badly fails in predictable ways: vague wording produces idiosyncratic interpretations; double-barrelled questions produce answers that cannot be mapped reliably to either issue; long or complex wording increases rereading and neutral/non-substantive answers; leading recommendations anchor choices; excessive options worsen difficult and preference-uncertain decisions; serial interruptions add resumption costs; mandatory free text raises nonresponse; and never asking causes code to be generated against the wrong interpretation. [doi.org](https://doi.org/10.2478/jos-2020-0041) [doi.org](https://doi.org/10.1145/3660810) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.2478/jos-2020-0041))

---

## Detailed Findings

### 1. Answer this decisively: What does the evidence say about how to ask a person a decision question well — so they answer accurately, quickly, and without decision fatigue — and what are the documented failure modes of asking badly?

#### Decision specification for the coding-agent skill

| Parameter | Recommended rule | Evidence status and rationale | Confidence |
|---|---|---|---|
| **When to ask** | <INFERENCE from="requirements-risk findings, harmless-ambiguity case studies, clarification gains and interruption costs">Ask only when at least two plausible interpretations remain, they imply materially different implementations, local evidence cannot distinguish them, and the answer is likely to change the action.</INFERENCE> | Selective clarification addresses consequential uncertainty without treating every linguistic ambiguity as a blocker. | High |
| **Ask/default test** | <INFERENCE from="value-of-information logic and interruption-cost evidence">Ask when \(E[L(\text{best current default})]-E[L(\text{best action after answer})] > C_{\text{interruption}}+C_{\text{delay}}\). Otherwise default and disclose the assumption.</INFERENCE> | No validated universal dollar, minute or probability threshold exists. | High for the test; Low for any fixed threshold |
| **Questions per batch** | <INFERENCE from="interruption and satisficing evidence">One by default; maximum three, provided they are independent, already known blockers and can be answered in one short turn.</INFERENCE> | No direct factorial study of coding-agent batch size was found. | Medium |
| **Options per question** | <INFERENCE from="conditional choice-overload and response-order evidence">Two to four total; default three. Do not list variations that lead to essentially the same implementation.</INFERENCE> | There is no universal optimum; difficulty and option similarity matter more than count alone. | Medium |
| **Recommendation** | <INFERENCE from="default meta-analysis and advice-anchoring research">Lead with “Recommended” only when constraints or repository evidence justify it. Add a reason of roughly one clause and do not preselect it.</INFERENCE> | Recommendations reduce search effort but anchor responses; quality depends on alignment. | High |
| **Wording** | <CONFIDENCE:LOW><INFERENCE from="eye-tracking and questionnaire burden studies">Target 30–60 words total, a stem of approximately 20 words or fewer, and option labels of approximately 12 words or fewer.</INFERENCE></CONFIDENCE:LOW> | Simplicity is well supported; the exact word counts are product heuristics, not established cut-offs. | High for plain wording; Low for count |
| **Free-text note** | <INFERENCE from="open-ended nonresponse and non-exhaustive-option evidence">Offer “Other/add a note” when needed, optional and after the fixed options. Do not demand justification.</INFERENCE> | Likely to discover edge cases, but introduces burden, missingness and coding costs. | Medium |
| **Ordering** | Recommended first when seeking consent to an evidence-backed implementation; neutral or randomized ordering when eliciting preference. | Initial options and defaults alter choice. | High |
| **Answer format** | Ask for a letter or option label; permit a short correction. | Lowers response-production burden while preserving an escape hatch. | Medium |

**Proposed gate for the agent**

<INFERENCE from="the evidence summarized in the six domains below">The agent should ask only if all five gates pass:</INFERENCE>

1. **Ambiguity:** At least two interpretations are reasonably consistent with the request.
2. **Divergence:** Those interpretations produce different externally observable behavior, API/schema choices, dependency choices, security properties or substantial rework.
3. **No local resolution:** Repository conventions, tests, documentation, issue history and existing code do not resolve it.
4. **Answerability:** A user can resolve it with one short selection or note.
5. **Positive value:** Expected avoided error or rework exceeds the cost of interruption and waiting.

<INFERENCE from="asymmetric-loss decision theory">For destructive, difficult-to-reverse or safety-sensitive actions, use a lower uncertainty threshold; for reversible internal details, use a higher threshold and default more readily.</INFERENCE>

A suitable output template is:

> **Which authentication model should I implement?**  
> **A. Recommended — existing session middleware:** matches the current application.  
> **B. JWT:** better for stateless external clients.  
> **C. Other:** add a short note.  
>  
> Reply A, B or C.

This template asks one thing, exposes the implementation consequence of each option, marks but does not preselect the recommendation, and retains an optional escape hatch.

---

#### 1.1 Requirements elicitation: ambiguity, assumptions and the cost of building the wrong thing

**(High Confidence)** In the NaPiRE cross-company survey, 228 organizations in ten countries reported incomplete or hidden requirements in 109 cases (48%), customer–team communication flaws in 93 (41%), moving targets in 76 (33%) and requirements that were too abstract in 76 (33%). These were practitioner rankings and causal narratives, not randomized or archival estimates of the dollar cost of a particular ambiguity. [doi.org](https://doi.org/10.1007/s10664-016-9451-7) ([researchgate.net](https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requirements_Engineering))

**(Medium Confidence)** A focused NaPiRE replication covered 14 Austrian and 74 Brazilian organizations and again found incomplete/hidden requirements among the most critical requirements-engineering problems. Its value is cross-context replication; its limitations are self-report, organizational sampling and absence of measured project-level counterfactuals. [arxiv.org](https://arxiv.org/abs/1612.00163) ([arxiv.org](https://arxiv.org/abs/1612.00163))

**(Medium Confidence)** Chari and Agrawal analyzed archival records from 49 waterfall MIS projects completed in 2008–2009 at one CMMI Level 5 organization; four observations with missing data reduced the regression sample to 45. New-requirement change requests were associated with more injected defects, coefficient \(0.23\), \(p<.01\), and greater logged effort, coefficient \(0.06\), \(p<.10\). Incorrect-requirement changes predicted additional new requirements, coefficient \(0.26\), \(p<.05\), while the incomplete-requirement coefficient for defects was \(0.003\) and not significant. External validity is restricted by the single highly mature organization, dated waterfall setting, small sample and subjective defect categorization. [doi.org](https://doi.org/10.1007/s10664-017-9506-4) ([researchgate.net](https://www.researchgate.net/publication/316362583_Impact_of_incorrect_and_new_requirements_on_waterfall_software_project_outcomes))

**(High Confidence)** The popular claim that defects become exponentially—often tens or hundreds of times—more expensive merely because they are found later is not a safe general rule. Menzies and colleagues analyzed 47,376 defect logs from 171 Team Software Process projects conducted from 2006 to 2014; median team size was seven and median increment duration was 46 days. Most injection/removal-phase comparisons were statistically indistinguishable, and the only reported significant scale-up was about threefold, far below classic exponential claims. Limitations include selection into TSP, pre-release rather than post-deployment data, variable defect definitions and self-recorded time. [arxiv.org](https://arxiv.org/abs/1609.04886) ([arxiv.org](https://arxiv.org/abs/1609.04886))

**(Medium Confidence)** Not every textual ambiguity warrants clarification. Ribeiro and Berry examined persistent ambiguities in three completed systems and asked chief requirements engineers whether the ambiguities had caused or could cause serious defects; they failed to falsify earlier findings that sampled persistent ambiguities had not caused serious problems. The study warns against paying to remove all ambiguity, but its case-study design could miss rare catastrophic ambiguities. [doi.org](https://doi.org/10.1016/j.scico.2020.102472) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0167642320300824))

**(High Confidence)** The ambiguity-detection literature contains far more proposals than strong evaluations. A systematic mapping identified 174 studies from 1995–2015 but only 28 empirically evaluated studies. This limits claims that a particular lexical “smell” reliably predicts costly misunderstanding. [doi.org](https://doi.org/10.1109/EmpiRE.2015.7431303) ([doi.org](https://doi.org/10.1109/EmpiRE.2015.7431303))

<CONFLICTING_EVIDENCE>The requirements literature agrees that incomplete, incorrect and changing requirements are common risks, but it does not support treating every linguistic ambiguity as economically important. NaPiRE and Chari–Agrawal show substantial requirements risk; Ribeiro–Berry show that many persistent ambiguities can be harmless; Menzies et al. reject a universal exponential late-fix multiplier.</CONFLICTING_EVIDENCE>

<INSUFFICIENT_EVIDENCE>No credible, modern primary study establishes a universal percentage of software budgets lost specifically by “building the wrong thing from an under-specified brief.” Frequently repeated 40%–80% rework or 100× late-fix numbers should not be used as general empirical constants.</INSUFFICIENT_EVIDENCE>

<INFERENCE from="NaPiRE prevalence; Chari and Agrawal's differentiated effects; Ribeiro and Berry's harmless ambiguities">**Authoring rule:** the agent should identify *decision ambiguity*, not merely linguistic ambiguity: “Would choosing interpretation A rather than B change what I build?”</INFERENCE>

##### Methodological Comparison — requirements ambiguity and cost

| Study | Method and sample | Main result | Statistical detail | Stated or material limitations |
|---|---|---|---|---|
| Méndez Fernández et al., NaPiRE | Cross-company practitioner survey; 228 organizations in ten countries | Incomplete/hidden requirements 48%; customer communication flaws 41%; underspecification 33%. [doi.org](https://doi.org/10.1007/s10664-016-9451-7) ([researchgate.net](https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requirements_Engineering)) | Descriptive rankings; no causal effect size | Self-report, sampling and ranking effects; no objective rework measure |
| Kalinowski et al. | Replicated surveys; 14 Austrian and 74 Brazilian organizations | Incomplete/hidden requirements rated highly critical. [arxiv.org](https://arxiv.org/abs/1612.00163) ([arxiv.org](https://arxiv.org/abs/1612.00163)) | Descriptive and qualitative causal analysis | Small Austrian sample; country and respondent selection |
| Chari & Agrawal | Archival regression; 49 projects, regression \(n=45\) | New requirements predicted defects and, marginally, effort; incomplete requirements had no measurable effect. [doi.org](https://doi.org/10.1007/s10664-017-9506-4) ([researchgate.net](https://www.researchgate.net/publication/316362583_Impact_of_incorrect_and_new_requirements_on_waterfall_software_project_outcomes)) | New requirements→defects \(b=.23,p<.01\); →effort \(b=.06,p<.10\) | One CMMI-5 organization; waterfall; older MIS projects |
| Menzies et al. | 171 TSP projects; 47,376 logged defects | No consistent exponential delayed-fix effect. [arxiv.org](https://arxiv.org/abs/1609.04886) ([arxiv.org](https://arxiv.org/abs/1609.04886)) | Most Scott–Knott comparisons nonsignificant; largest significant example ≈3× | TSP selection, pre-release scope, self-recorded times |
| Ribeiro & Berry | Three retrospective case studies | Sampled persistent ambiguities were not judged to cause serious defects. [doi.org](https://doi.org/10.1016/j.scico.2020.102472) ([sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0167642320300824)) | Primarily expert assessment; exact ambiguity counts unavailable in retrieved extract | Low power for rare severe cases; retrospective judgment |

---

#### 1.2 Survey methodology: wording, jargon, satisficing and response order

**(High Confidence)** Survey answering requires comprehension, retrieval, judgment and response mapping. Greater task difficulty, lower respondent ability and lower motivation increase the probability of “satisficing”—performing these steps superficially or omitting some. Standard survey guidance therefore recommends familiar words, simple syntax, concrete terms, mutually exclusive and exhaustive options, and one construct per question. [web.stanford.edu](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2009/2009_handbook_krosnick.pdf) ([web.stanford.edu](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2009/2009_handbook_krosnick.pdf))

**(High Confidence)** Lenzner, Kaczmirek and Galesic randomly assigned 44 German participants—22 per condition—to questions containing or avoiding seven problematic text features. Six features increased fixation time, fixation count or both. Effects on word/phrase fixation included low-frequency words, \(F(1,41)=21.25,p=.0001,\eta_p^2=.34\); vague relative terms, \(F=14.19,p=.001,\eta_p^2=.26\); ambiguous noun phrases, \(F=8.60,p=.005,\eta_p^2=.17\); complex syntax, \(F=8.42,p=.006,\eta_p^2=.17\); complex logical structures, \(F=14.90,p=.0001,\eta_p^2=.27\); and low syntactic redundancy, \(F=8.40,p=.006,\eta_p^2=.17\). Similar effects occurred for attitudinal, factual and behavioral questions. Participants were young, highly educated and German-speaking, limiting generalization. [doi.org](https://doi.org/10.1093/ijpor/edq053) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension))

**(Medium Confidence)** A separate web experiment by Lenzner found that less-comprehensible questions produced more breakoff, nonsubstantive answers, neutral answers and lower over-time consistency, with interactions involving verbal ability and motivation. <MISSING_DATA>[The accessible article extract did not expose the experiment’s exact sample size, coefficients or p-values; full publisher tables are required.]</MISSING_DATA> [doi.org](https://doi.org/10.1177/1525822X12448166) ([journals.sagepub.com](https://journals.sagepub.com/doi/abs/10.1177/1525822x12448166))

**(High Confidence)** Double-barrelled questions do not merely feel awkward: they change the construct being measured. Menold conducted two randomized experiments comparing double-stimulus items with single-stimulus versions. Metric and scalar measurement invariance did not hold across versions, and at least one single-stimulus version had higher validity. Response times were not consistently longer for the double-barrelled forms, supporting the failure mode in which respondents silently answer only one barrel rather than visibly struggle. <MISSING_DATA>[Exact sample sizes and all model coefficients were not present in the retrieved extract.]</MISSING_DATA> [doi.org](https://doi.org/10.2478/jos-2020-0041) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.2478/jos-2020-0041))

**(High Confidence)** Option order affects visually presented choices. Malhotra randomized option order for five unipolar scales and six four-option categorical questions in a nationally representative web sample of 397 US adults. Low-education respondents who completed the questionnaire fastest were most susceptible to primacy effects on unipolar scales. The study demonstrates an interaction among burden, respondent ability and option order rather than a universal fixed bias. [doi.org](https://doi.org/10.1093/poq/nfn050) ([academic.oup.com](https://academic.oup.com/poq/article/72/5/914/1832496))

**(Medium Confidence)** A 2024 Public Opinion Quarterly study of complex policy questions found an overall response-order effect of 2.8 percentage points, with larger effects associated with question length and lower respondent knowledge. <MISSING_DATA>[The retrieved extract did not expose sample size, confidence intervals or full model coefficients.]</MISSING_DATA> [doi.org](https://doi.org/10.1093/poq/nfae050) ([academic.oup.com](https://academic.oup.com/poq/article/88/4/1249/8005355))

**(Medium Confidence)** Clarification improves accuracy but consumes time. In a laboratory study using Census Bureau interviewers, fictional scenarios and factual government-survey questions, three forms of partially conversational interviewing all produced reliably greater accuracy than strict standardization, but longer interviews; fully conversational interviewing was more accurate again and still slower. Respondents often failed to request help even when help would have improved their answers. <MISSING_DATA>[Exact sample sizes and inferential statistics were not available on the accessible BLS summary page.]</MISSING_DATA> [bls.gov](https://www.bls.gov/osmr/research-papers/1999/st990270.htm) ([bls.gov](https://www.bls.gov/osmr/research-papers/1999/st990270.htm))

<INFERENCE from="Lenzner eye tracking; Menold double-barrel experiments; Malhotra order experiment">**Authoring rules:**</INFERENCE>

- Ask about **one decision dimension at a time**. “Should I use PostgreSQL and deploy on AWS?” must become two questions.
- Replace “fast,” “recent,” “scalable,” “standard” and “secure enough” with an explicit condition, range or example.
- Describe options by their consequences: “shared across processes,” not merely “Redis.”
- Make options mutually exclusive at the decision level.
- Put the likely sufficient option set in view at once so the respondent need not remember earlier alternatives.
- Treat rapid selection of the first acceptable option as a predictable response mode, not proof of a true preference.

##### Methodological Comparison — question wording and response quality

| Study | Method and sample | Outcome | Statistical detail | Limitations |
|---|---|---|---|---|
| Lenzner et al., 2011 | Randomized eye-tracking experiment, \(n=44\) | Six of seven difficult-language features increased processing burden. [doi.org](https://doi.org/10.1093/ijpor/edq053) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension)) | \(p=.021\) to \(p<.0001\); \(\eta_p^2\approx.12\)–.40 | Young, highly educated German sample |
| Lenzner, 2012 | Web experiment | Harder questions increased multiple indicators of low response quality. [doi.org](https://doi.org/10.1177/1525822X12448166) ([journals.sagepub.com](https://journals.sagepub.com/doi/abs/10.1177/1525822x12448166)) | Exact statistics unavailable in retrieved extract | Paywalled tables; web-survey transfer |
| Menold, 2020 | Two randomized experiments | Double-barrelled and single-barrel versions lacked measurement invariance. [doi.org](https://doi.org/10.2478/jos-2020-0041) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.2478/jos-2020-0041)) | Latency did not reliably reveal the validity problem | Exact sample details unavailable in extract; scale-specific |
| Malhotra, 2008 | Randomized option order, \(n=397\) US adults | Fast, lower-education respondents showed stronger visual primacy. [doi.org](https://doi.org/10.1093/poq/nfn050) ([academic.oup.com](https://academic.oup.com/poq/article/72/5/914/1832496)) | Moderated effects; exact coefficients omitted here | Political survey; total completion time is imperfect attention proxy |
| Schober et al., 1999 | Laboratory factual interviews with fictional records | Conversational clarification increased accuracy and duration. [bls.gov](https://www.bls.gov/osmr/research-papers/1999/st990270.htm) ([bls.gov](https://www.bls.gov/osmr/research-papers/1999/st990270.htm)) | Summary reports reliable differences; exact values unavailable | Artificial scenarios; interviewer-mediated |
| Sen et al., 2024/2025 | Complex-policy survey analysis | Overall response-order effect 2.8 percentage points. [doi.org](https://doi.org/10.1093/poq/nfae050) ([academic.oup.com](https://academic.oup.com/poq/article/88/4/1249/8005355)) | Heterogeneous by length and knowledge | Policy questions may be harder than coding decisions about one’s own work |

---

#### 1.3 Choice architecture: option count, recommendations, defaults and free text

**(High Confidence)** There is no evidence-based universal optimum such as “always offer three choices.” Scheibehenne, Greifeneder and Todd’s meta-analysis combined 63 conditions from 50 published and unpublished experiments, \(N=5,036\), and found a mean choice-overload effect virtually equal to zero but substantial between-study variance. [doi.org](https://doi.org/10.1086/651235) ([ideas.repec.org](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html))

**(High Confidence)** Chernev, Böckenholt and Goodman’s theory-based meta-analysis combined 99 observations, \(N=7,202\), and found that overload is more likely when option sets are difficult to compare, the decision itself is difficult, preferences are uncertain, and the decision maker is trying to minimize effort. Thus, ten clearly dominated technical variants may be easier than four finely balanced preference choices. [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([researchgate.net](https://www.researchgate.net/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-Analysis))

<INFERENCE from="both choice-overload meta-analyses">For coding-agent questions, option count should be determined by the number of materially distinct implementation paths, with a small display cap to suppress near-duplicate alternatives. **Two to four total options, default three, is a conservative interface rule rather than a discovered psychological optimum.**</INFERENCE>

**(High Confidence)** Defaults exert a substantial aggregate effect. Jachimowicz and colleagues’ meta-analysis estimated a default effect of \(d=0.68\), 95% CI \(0.53\)–\(0.83\), while also finding marked heterogeneity and some null or negative results. Defaults work through multiple mechanisms, including implied endorsement, effort reduction and reference dependence. [doi.org](https://doi.org/10.1017/bpp.2018.43) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html))

**(Medium Confidence)** Recommendations can improve decisions when the adviser has superior information and aligned objectives, but their position and apparent authority can anchor judgments even when the advice is poor. Experiments in the judge–advisor paradigm found adjustment toward advice independent of advice quality, indicating that users cannot be expected to discount an unjustified “recommended” label perfectly. [doi.org](https://doi.org/10.1027/1618-3169/a000361) ([doi.org](https://doi.org/10.1027%2F1618-3169%2Fa000361))

<INFERENCE from="default meta-analysis and advice-quality findings">Use a recommendation to reduce search effort only when the agent can name its basis: existing project convention, explicit requirement, compatibility constraint, lower reversibility cost or dominant security property. A recommendation based merely on model preference should not be shown.</INFERENCE>

**(Medium Confidence)** A recommendation should be **marked but not preselected**. This retains informational value while avoiding the stronger manipulation produced by an opt-out default. The literature does not directly compare these two exact formats in coding-agent clarification.  
<INSUFFICIENT_EVIDENCE>There is no coding-agent RCT showing that a first-position “Recommended” option improves final software quality compared with neutral ordering.</INSUFFICIENT_EVIDENCE>

**(Medium Confidence)** Optional free text can reveal an omitted category or a constraint the author did not anticipate, but open response is expensive for respondents and selective in who supplies it. Pew’s analysis found median nonresponse of 12% for one-word or short-sentence prompts and 17% for prompts asking for multiple sentences; typical closed items on the same panel averaged about 1%–2% nonresponse. Education, age and device also predicted open-answer participation and length. [pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/) [pewresearch.org](https://www.pewresearch.org/decoded/2021/10/14/why-do-some-open-ended-survey-questions-result-in-higher-item-nonresponse-rates-than-others/) ([pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/))

<INSUFFICIENT_EVIDENCE>No located experiment directly tests whether placing an optional free-text note beside a selected coding option improves implementation accuracy.</INSUFFICIENT_EVIDENCE>

<INFERENCE from="open-ended missingness and the need for exhaustive fixed options">Use free text as an escape hatch, not the primary response channel: “Other — add a note (optional).” Do not impose a word minimum and do not ask every user to justify a fixed-option answer.</INFERENCE>

##### Methodological Comparison — choice architecture

| Study | Evidence | Main finding | Relevance and limitation |
|---|---|---|---|
| Scheibehenne et al., 2010 | Meta-analysis, 63 conditions, \(N=5,036\) | Overall choice-overload effect virtually zero. [doi.org](https://doi.org/10.1086/651235) ([ideas.repec.org](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html)) | Rejects a universal option-count rule; domains were heterogeneous and often consumer-facing |
| Chernev et al., 2015 | Meta-analysis, 99 observations, \(N=7,202\) | Overload depends on complexity, difficulty, uncertain preferences and effort-minimization. [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([researchgate.net](https://www.researchgate.net/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-Analysis)) | Supports reducing confusable alternatives rather than chasing a magic count |
| Jachimowicz et al., 2019 | Meta-analysis of defaults | Aggregate effect \(d=.68\), 95% CI .53–.83. [doi.org](https://doi.org/10.1017/bpp.2018.43) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)) | Shows influence, not automatically improved decision quality |
| Pütter et al., 2017 | Judge–advisor experiments | Adjustment toward advice was not adequately sensitive to advice quality. [doi.org](https://doi.org/10.1027/1618-3169/a000361) ([doi.org](https://doi.org/10.1027%2F1618-3169%2Fa000361)) | Supports warning against unjustified “recommended” labels |
| Pew Research Center, 2021/2023 | Large-panel archival analyses | Open questions had materially higher and demographically patterned nonresponse. [pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/) ([pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/)) | Authoritative methodological evidence, but not a randomized coding study |

---

#### 1.4 HCI interruption cost: when asking is worth it and whether to batch

**(High Confidence)** Interruption costs are measured through at least four distinct outcomes: **resumption lag**, primary-task completion time, post-interruption error rate, and subjective or physiological workload. Pupil dilation has been used to locate lower-workload task boundaries, and interruptions delivered at those boundaries are less disruptive than those delivered during high workload. [doi.org](https://doi.org/10.1145/1314683.1314689) ([doi.org](https://doi.org/10.1145/1314683.1314689))

**(Medium Confidence)** Iqbal and Bailey interrupted users at different boundaries in interactive tasks and measured resumption lag, showing that task structure predicts interruption cost. <MISSING_DATA>[The retrieved primary-source summary did not expose participant count, confidence intervals or the complete resumption-lag table.]</MISSING_DATA> [doi.org](https://doi.org/10.1145/1124772.1124812) ([experts.illinois.edu](https://experts.illinois.edu/en/publications/leveraging-characteristics-of-task-structure-to-predict-the-cost-))

**(Medium Confidence)** Mark, Gudith and Klocke’s laboratory study of 48 participants found that interrupted participants compensated by working faster but reported more stress, frustration, effort and time pressure. Faster completion therefore does not imply zero interruption cost. <MISSING_DATA>[Exact condition-level means and p-values require the full ACM tables.]</MISSING_DATA> [doi.org](https://doi.org/10.1145/1357054.1357072)

**(Medium Confidence)** In a sequence-execution experiment, interruptions averaging approximately 2.8 seconds doubled sequence errors and interruptions averaging 4.4 seconds tripled them. The important result is that even very brief interruptions can disrupt a maintained action state. <MISSING_DATA>[Exact experiment-level sample sizes and inferential statistics were unavailable in the retrieved materials.]</MISSING_DATA> [doi.org](https://doi.org/10.1037/a0030986)

**(High Confidence)** The HCI evidence supports asking at a **natural boundary**—before implementation begins, before a destructive action or when planning cannot proceed—not after the agent has begun a long coherent edit. It does not establish that a batch of three questions is superior to one or five in conversational coding.

<INSUFFICIENT_EVIDENCE>No direct controlled study was found comparing serial versus batched clarification questions in an AI coding workflow while jointly measuring software correctness, user response quality, latency and fatigue.</INSUFFICIENT_EVIDENCE>

<INFERENCE from="resumption-lag findings; workload-sensitive timing; survey satisficing">If several blockers are already visible, asking them in one numbered batch should reduce repeated context switches. The batch should remain small because each additional decision increases reading, comparison and response-mapping work. This supports **one by default, maximum three**, but the numeric cap requires product validation.</INFERENCE>

**Ask-versus-default decision**

<INFERENCE from="interruption cost plus value of avoided requirements error">A question is worth interrupting for when its expected information value exceeds: (a) the time to read and answer it, (b) the cognitive cost of leaving the user’s current task, and (c) waiting latency. A reversible default with low expected regret normally fails this test; a decision that changes public behavior or causes costly rework is more likely to pass.</INFERENCE>

---

#### 1.5 Plain language, readability and word-count thresholds

**(High Confidence)** The strongest finding is about **linguistic features**, not raw word count. Rare words, abstraction, vague relative terms, ambiguous references, passive or nominalized syntax and complex logical structure increase processing burden. A short but cryptic question can therefore be worse than a slightly longer concrete one. [doi.org](https://doi.org/10.1093/ijpor/edq053) [gesis.org](https://www.gesis.org/fileadmin/admin/Dateikatalog/pdf/guidelines/question_wording_lenzner_menold_2016.pdf) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension))

**(Medium Confidence)** Plain-language rewriting does not invariably improve all survey outcomes. Bauer, Kunz and Gummer’s between-subjects web experiment found no general plain-language advantage in questionnaire evaluation or data quality, but found less item nonresponse and more response differentiation among respondents who spoke a language other than German at home. <MISSING_DATA>[Exact sample size and coefficients were not exposed in the accessible publisher extract.]</MISSING_DATA> [doi.org](https://doi.org/10.1080/13645579.2023.2294880) ([eric.ed.gov](https://eric.ed.gov/?id=EJ1458540&q=source%3A%22International+Journal+of+Social+Research+Methodology%22))

**(Medium Confidence)** A 2026 experiment by Kunz, Gummer and Neuert randomly assigned 3,256 German online-panel respondents to standard- or plain-language versions of a 16-item scale. Plain language produced greater response differentiation, fewer midpoint responses and shorter response times, with mostly comparable factor structure and slightly higher internal consistency; however, several item and scale means shifted, meaning that simplification can alter the construct or pragmatic force rather than merely remove noise. The authors note the nonprobability panel and single-scale design as limitations. [doi.org](https://doi.org/10.1177/1525822X251322031) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.1177/1525822X251322031))

**(High Confidence)** Overall questionnaire length affects participation, though heterogeneous study definitions prevent an optimal count. A systematic review of randomized health-survey trials found that shorter questionnaires increased response, pooled OR \(1.35\), 95% CI \(1.19\)–\(1.54\), \(p<.00001\), averaging a nine-percentage-point improvement. “Short” ranged from seven to 47 questions and “long” from 36 to 123, so this does not identify a sharp threshold. [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC1421421/) ([pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC1421421/))

**(High Confidence)** In a quasi-randomized trial of 847 women aged 70 or over, response was 49% for four- and five-page questionnaires but 40% for a seven-page version; the nine-point short-versus-long difference had a 95% CI of 0.3–16.6 percentage points. Item completion near the beginning did not differ. [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/11184958/) ([pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/11184958/))

<INSUFFICIENT_EVIDENCE>No robust experimental literature establishes that a decision-question stem becomes inaccurate at exactly 20, 25 or any other number of words. “Under 20 words” is a conventional design rule, not a demonstrated universal breakpoint.</INSUFFICIENT_EVIDENCE>

<CONFIDENCE:LOW><INFERENCE from="psycholinguistic feature effects, questionnaire-length response effects and the need to fit several concise options">For an agent UI, target **30–60 words total** for one question and its options. Treat 60 words as a review trigger, not an absolute prohibition: technical identifiers, necessary risk explanations and mutually exclusive consequences may justify more.</INFERENCE></CONFIDENCE:LOW>

**Plain-language authoring test**

- Can a user understand the decision without rereading?
- Does every option state a consequence rather than only a technology name?
- Are vague quantifiers replaced by an observable criterion?
- Is there only one decision dimension?
- Can each option be selected without reading hidden documentation?
- Has every sentence that merely explains the agent’s thought process been removed?

---

#### 1.6 Conversational AI and coding agents asking clarifying questions

**(High Confidence)** ClarifyGPT is the strongest peer-reviewed coding-specific evidence located. It first generates multiple candidate programs, uses inconsistency among them as a signal of ambiguous requirements, generates targeted clarification questions, incorporates the answers into a refined requirement, and regenerates code. In a human evaluation with ten participants on MBPP-sanitized and MBPP-ET, GPT-4 Pass@1 on MBPP-sanitized increased from 70.96% to 80.80%. In simulated-user evaluations across four benchmarks, average GPT-4 performance rose from 68.02% to 75.75%, and ChatGPT performance from 58.55% to 67.22%. Limitations include only ten human participants, short benchmark programs, dependence on simulated answers for scale, and uncertainty about transfer to long-running repository tasks. [doi.org](https://doi.org/10.1145/3660810) ([arxiv.org](https://arxiv.org/abs/2310.10996))

**(Medium Confidence)** Kim and colleagues framed asking as a selective classification problem in a large commercial conversational system: asking for every ambiguity would itself harm user experience. They evaluated decisions across five ambiguity types using real commercial-agent data and reported improvement over baseline approaches. <MISSING_DATA>[The public summary does not provide sample size, absolute metric values, confidence intervals or per-ambiguity results.]</MISSING_DATA> [amazon.science](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding) ([amazon.science](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding))

**(Medium Confidence)** A 2025 preprint, *Curiosity by Design*, combined a query classifier for unclear programming questions with a fine-tuned clarification-question generator. Its evaluation reported better clarification usefulness than zero-shot prompting and a user-study preference for its questions, but the retrieved abstract did not provide participant counts or effect sizes. It remains preliminary. [arxiv.org](https://arxiv.org/abs/2507.21285) ([arxiv.org](https://arxiv.org/abs/2507.21285))

**(Medium Confidence, preprint)** The March 2026 preprint *Ask or Assume?* reported a 69.40% task-resolution rate for an uncertainty-aware multi-agent OpenHands system using Claude Sonnet 4.5, compared with 61.20% for a standard single-agent setup on underspecified software-development tasks. <MISSING_DATA>[The retrieved paper summary did not expose task count, confidence intervals, statistical tests or intervention cost.]</MISSING_DATA> [arxiv.org](https://arxiv.org/abs/2603.26233) ([huggingface.co](https://huggingface.co/papers/2603.26233))

**(Low-to-Medium Confidence, very recent preprint)** *ClarifyCodeBench*, posted in July 2026, evaluates ambiguity identification, clarification-question generation and code generation on manually annotated real-world programming tasks. Its reported qualitative findings are that strong static code-generation performance does not guarantee strong clarification, additional reasoning produces only limited gains in ambiguity identification, and clarification degrades as multiple ambiguities accumulate. The available abstract contained unresolved placeholders for some benchmark statistics, so numerical claims are not usable. [arxiv.org](https://arxiv.org/abs/2607.00711) ([arxiv.org](https://arxiv.org/abs/2607.00711))

**(Medium Confidence)** ACL Findings 2026 introduced ClarifyBench for tool-using agents, with a user simulator and ambiguity categories spanning areas such as API, file-system, vehicle-control, travel-document and stock tasks. This reflects the field’s shift from evaluating answer quality alone toward evaluating whether the agent asks at the right time. <MISSING_DATA>[The retrieved proceedings extract did not expose all benchmark counts and result tables.]</MISSING_DATA> [aclanthology.org](https://aclanthology.org/2026.findings-acl.2028.pdf) ([aclanthology.org](https://aclanthology.org/2026.findings-acl.2028.pdf))

<CONFLICTING_EVIDENCE>Recent work consistently finds that clarification can improve task success on deliberately underspecified tasks, but it also treats indiscriminate questioning as a user-experience failure. Evidence is much stronger for “clarification can help” than for exact policies governing question count, wording, recommendation order or stopping.</CONFLICTING_EVIDENCE>

<INFERENCE from="ClarifyGPT's consistency detector; commercial-agent selective asking; uncertainty-aware agent results">The most defensible architecture is **detect → estimate consequence → inspect local context → ask selectively → integrate answer**, not “always ask before coding” and not “always infer.”</INFERENCE>

##### Methodological Comparison — AI clarification systems

| Work | Status and method | Sample/evaluation | Main result | Key limitation |
|---|---|---|---|---|
| Kim et al., 2021 | Commercial spoken-language system; classifier decides whether to clarify | Five ambiguity types; exact \(N\) unavailable | Selective asking beat baselines; asking for every ambiguity was treated as harmful. [amazon.science](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding) ([amazon.science](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding)) | Non-coding domain; incomplete public statistics |
| ClarifyGPT, 2024 | Peer-reviewed FSE framework; code-consistency ambiguity detector | Ten human participants plus simulated users; four benchmarks | GPT-4 MBPP-sanitized Pass@1 70.96%→80.80%; four-benchmark average 68.02%→75.75%. [doi.org](https://doi.org/10.1145/3660810) ([arxiv.org](https://arxiv.org/abs/2310.10996)) | Small human study; short programs; simulated responses |
| Curiosity by Design, 2025 | `[PREPRINT]` classifier plus fine-tuned question generator | User study; exact \(N\) unavailable | Questions preferred over zero-shot baseline. [arxiv.org](https://arxiv.org/abs/2507.21285) ([arxiv.org](https://arxiv.org/abs/2507.21285)) | Preliminary; insufficient numerical reporting in abstract |
| Ask or Assume?, 2026 | `[PREPRINT]` uncertainty-aware OpenHands multi-agent system | Underspecified development tasks; task count unavailable | Resolve rate 69.40% versus 61.20%. [arxiv.org](https://arxiv.org/abs/2603.26233) ([huggingface.co](https://huggingface.co/papers/2603.26233)) | No exposed CI/significance/cost data |
| ClarifyCodeBench, 2026 | `[PREPRINT]` manually annotated interactive coding benchmark | Real-world programming tasks; some counts unresolved in available abstract | Clarification and code-generation abilities decouple; multi-ambiguity performance deteriorates. [arxiv.org](https://arxiv.org/abs/2607.00711) ([arxiv.org](https://arxiv.org/abs/2607.00711)) | Very recent; placeholder statistics; no longitudinal field test |
| ClarifyBench, 2026 | Peer-reviewed ACL Findings benchmark for tool agents | User simulator and multiple tool domains | Formalizes when-to-ask evaluation across ambiguity sources. [aclanthology.org](https://aclanthology.org/2026.findings-acl.2028.pdf) ([aclanthology.org](https://aclanthology.org/2026.findings-acl.2028.pdf)) | Simulated users; incomplete transfer evidence to developers |

---

#### Documented failure modes of a bad decision question

| Failure mode | What happens | Evidence and confidence |
|---|---|---|
| **Asking every time information is absent** | Users become the agent’s external planner; interruption and latency exceed information value. | **High:** interruption cost is real; **Medium:** direct coding-agent burden studies are sparse. |
| **Never asking** | The agent silently commits to one interpretation and may optimize the wrong program. | **High:** ClarifyGPT and 2026 agent studies show gains from resolving deliberate underspecification. [doi.org](https://doi.org/10.1145/3660810) ([doi.org](https://doi.org/10.1145/3660810)) |
| **Vague terms** | Different users apply different thresholds or time periods; some choose neutral/skip rather than expose confusion. | **High:** eye-tracking and web-survey experiments. [doi.org](https://doi.org/10.1093/ijpor/edq053) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension)) |
| **Double-barrelled question** | The answer may apply to either issue, an average of both, or only the easier issue; measurement invariance fails. | **High:** two randomized Menold experiments. [doi.org](https://doi.org/10.2478/jos-2020-0041) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.2478/jos-2020-0041)) |
| **Long, syntactically dense wording** | More fixation, rereading and working-memory demand; greater satisficing risk. | **High:** psycholinguistic experiments; no sharp word threshold. |
| **Too many confusable options** | Search and comparison burden increases, particularly when preferences are uncertain. | **High:** moderated choice-overload meta-analysis. [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([researchgate.net](https://www.researchgate.net/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-Analysis)) |
| **Unjustified recommendation first** | The recommendation acts as an anchor or implied endorsement. | **High:** defaults strongly influence choice; **Medium:** direct software-quality effect unknown. |
| **Preselected recommendation** | The user may accept through inertia rather than agreement. | **High:** default effect; decision-quality consequences are context dependent. |
| **Serial drip-feed** | Repeated task reorientation and waiting; later questions may reveal that earlier work was premature. | **Medium:** strong indirect HCI evidence; direct coding comparison missing. |
| **Large batch** | Users skim, satisfice or answer only easy items; dependencies among questions may be missed. | **Medium:** survey literature supports burden effects; exact batch threshold missing. |
| **Mandatory explanation** | Higher nonresponse and low-quality filler text; differential burden by education and device. | **High:** open-response analyses. [pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/) ([pewresearch.org](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/)) |
| **No “Other/none” where options are incomplete** | Users choose a least-wrong answer, creating false certainty. | **Medium:** supported by option-exhaustiveness methodology; direct coding estimate missing. |
| **Removing all ambiguity before acting** | Time is spent resolving distinctions that would not change implementation. | **Medium:** requirements case studies found many persistent ambiguities harmless. |

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The mature evidence supports five propositions:

1. **Comprehension difficulty is measurable and avoidable.** Randomized psycholinguistic studies directly observe rereading and fixation costs from vague, rare and syntactically complex wording, with medium-to-large partial-\(\eta^2\) effects in a controlled sample. [doi.org](https://doi.org/10.1093/ijpor/edq053) ([researchgate.net](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension))
2. **Double-barrelled questions corrupt interpretation rather than merely adding time.** Randomized experiments found failure of measurement invariance even when response latency did not reveal difficulty. [doi.org](https://doi.org/10.2478/jos-2020-0041) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.2478/jos-2020-0041))
3. **Defaults and recommendation-like anchors materially change choice.** The default-effects meta-analysis provides the strongest quantitative evidence, \(d=.68\), 95% CI .53–.83. [doi.org](https://doi.org/10.1017/bpp.2018.43) ([ideas.repec.org](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html))
4. **There is no universal optimal option count.** The two principal choice-overload meta-analyses agree that the effect is heterogeneous and conditional. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([ideas.repec.org](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html))
5. **Selective clarification can improve code generation.** ClarifyGPT’s peer-reviewed benchmark results are the strongest coding-specific evidence, but its ten-person human evaluation and simulated-user scaling mean it is not yet a field-standard policy study. [doi.org](https://doi.org/10.1145/3660810) ([doi.org](https://doi.org/10.1145/3660810))

**(Medium Confidence)** The current best design is therefore not a universally inquisitive agent. It is a **calibrated selective-clarification agent** that searches available context, detects implementation-divergent uncertainty, estimates its cost, and asks a small, structured question only if the answer has positive expected value.

<INFERENCE from="the five propositions above">The defensible initial product setting is: **one question, three options, recommendation conditional, 30–60 words total, optional note, and a value-of-information gate.** Only “plain, single-issue, selective and non-coercive” is strongly established; the exact counts require experimentation.</INFERENCE>

---

### 3. What are the contrasting viewpoints or competing evidence?

**(High Confidence)** **Requirements ambiguity:** practitioner surveys consistently rate incomplete and underspecified requirements as serious, but retrospective case studies found many persistent ambiguities harmless. The correct distinction is consequential versus inconsequential ambiguity, not ambiguous versus unambiguous prose. [doi.org](https://doi.org/10.1007/s10664-016-9451-7) [doi.org](https://doi.org/10.1016/j.scico.2020.102472) ([researchgate.net](https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requirements_Engineering))

**(High Confidence)** **Late correction costs:** older cost-escalation curves are still widely repeated, but the 171-project TSP analysis found no consistent exponential increase during development. Project architecture, process, post-deployment exposure and defect type probably moderate cost. [arxiv.org](https://arxiv.org/abs/1609.04886) ([arxiv.org](https://arxiv.org/abs/1609.04886))

**(High Confidence)** **Choice overload:** famous individual experiments imply that fewer options are better, while the broad 2010 meta-analysis found a near-zero average. The 2015 meta-analysis reconciles these positions by identifying boundary conditions: overload occurs especially when comparison is difficult and preferences are unclear. [doi.org](https://doi.org/10.1086/651235) [doi.org](https://doi.org/10.1016/j.jcps.2014.08.002) ([ideas.repec.org](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html))

**(High Confidence)** **Recommendations:** a well-informed recommendation can reduce search costs and communicate expertise, but the same mechanism can create anchoring and default acceptance. There is no contradiction if decision quality and choice influence are separated: a recommendation can increase both influence and quality when aligned, or influence while decreasing quality when wrong.

**(Medium Confidence)** **Plain language:** psycholinguistic evidence strongly favors familiar, concrete and syntactically simple wording, yet complete “plain-language” rewrites show mixed aggregate effects and can change response means. Simplification is not automatically meaning-preserving. [doi.org](https://doi.org/10.1080/13645579.2023.2294880) [doi.org](https://doi.org/10.1177/1525822X251322031) ([tandfonline.com](https://www.tandfonline.com/doi/abs/10.1080/13645579.2023.2294880))

**(Medium Confidence)** **Clarification by AI:** under-asking increases wrong-intent execution, but over-asking adds latency, transfers planning work to the user and can make the system appear incompetent. Current results favor selective detection, but the field lacks a validated calibration curve connecting uncertainty, question cost and downstream code quality.

---

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** Between 2023 and August 2026, research moved from the general claim that LLMs “should ask clarifying questions” toward three concrete technical problems:

1. **Ambiguity detection before asking.** ClarifyGPT uses disagreement among generated programs; newer systems use query classifiers or structured uncertainty. [doi.org](https://doi.org/10.1145/3660810) [arxiv.org](https://arxiv.org/abs/2603.26233) ([doi.org](https://doi.org/10.1145/3660810))
2. **Interactive evaluation.** Benchmarks increasingly include a user or user simulator rather than treating the original prompt as immutable. ClarifyCodeBench and ClarifyBench are 2026 examples. [arxiv.org](https://arxiv.org/abs/2607.00711) [aclanthology.org](https://aclanthology.org/2026.findings-acl.2028.pdf) ([arxiv.org](https://arxiv.org/abs/2607.00711))
3. **Separating coding ability from elicitation ability.** Very recent work reports that a model can be a strong code generator but a weak ambiguity detector, and that multiple simultaneous ambiguities remain difficult. [arxiv.org](https://arxiv.org/abs/2607.00711) ([arxiv.org](https://arxiv.org/abs/2607.00711))

**(Medium Confidence)** The likely trajectory is toward agents that maintain explicit uncertainty over requirements, inspect repository evidence before interrupting, estimate the expected benefit of a question, and learn a user-specific interruption threshold from outcomes.

<INFERENCE from="2024 ClarifyGPT, 2025 classifier-based assistants, and 2026 uncertainty-aware benchmarks">The next research bottleneck is no longer demonstrating that clarification sometimes helps. It is calibrating **when to ask, what single question has highest information value, and whether the resulting gain justifies the human turn.**</INFERENCE>

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| **(High)** Incomplete/hidden requirements and communication failures are frequently reported RE problems. | Méndez Fernández et al., NaPiRE | 2017 | Peer-reviewed cross-company survey; primary and directly relevant | https://doi.org/10.1007/s10664-016-9451-7 |
| **(Medium)** The criticality of incomplete/hidden requirements replicated in Austria and Brazil. | Kalinowski et al. | 2016 | Peer-reviewed replicated organizational survey; primary | https://arxiv.org/abs/1612.00163 |
| **(Medium)** New and incorrect requirements have differentiated associations with effort and defects. | Chari & Agrawal | 2018 | Peer-reviewed archival project analysis; primary | https://doi.org/10.1007/s10664-017-9506-4 |
| **(High)** A universal exponential late-fix cost multiplier is unsupported. | Menzies, Nichols, Shull & Layman | 2016 | Large reproducible project-log analysis; primary | https://arxiv.org/abs/1609.04886 |
| **(Medium)** Many persistent textual ambiguities may be harmless. | Ribeiro & Berry | 2020 | Peer-reviewed multi-case retrospective study; primary | https://doi.org/10.1016/j.scico.2020.102472 |
| **(High)** Empirical evaluation of requirements-ambiguity tools is sparse. | Yang et al. | 2015 | Systematic mapping of 174 publications; peer-reviewed secondary synthesis | https://doi.org/10.1109/EmpiRE.2015.7431303 |
| **(High)** Rare, vague, abstract and syntactically complex wording increases processing burden. | Lenzner, Kaczmirek & Galesic | 2011 | Randomized eye-tracking experiment; primary | https://doi.org/10.1093/ijpor/edq053 |
| **(Medium)** Less-comprehensible questions reduce multiple response-quality indicators. | Lenzner | 2012 | Peer-reviewed web experiment; primary | https://doi.org/10.1177/1525822X12448166 |
| **(High)** Double-barrelled questions alter measurement and can fail invariance tests. | Menold | 2020 | Two randomized experiments; peer-reviewed primary study | https://doi.org/10.2478/jos-2020-0041 |
| **(High)** Rapid, lower-education respondents are vulnerable to visual primacy effects. | Malhotra | 2008 | Randomized nationally representative web experiment; primary | https://doi.org/10.1093/poq/nfn050 |
| **(Medium)** Conversational clarification improves factual response accuracy but takes longer. | Schober, Conrad & Fricker | 1999 | Government laboratory experiment; authoritative primary source | https://www.bls.gov/osmr/research-papers/1999/st990270.htm |
| **(Medium)** Complex questions exhibit measurable option-order effects. | Sen et al. | 2024/2025 | Peer-reviewed survey analysis; primary | https://doi.org/10.1093/poq/nfae050 |
| **(High)** Choice overload has a near-zero overall mean but high heterogeneity. | Scheibehenne, Greifeneder & Todd | 2010 | Meta-analysis of published and unpublished experiments | https://doi.org/10.1086/651235 |
| **(High)** Choice overload is moderated by task difficulty, option complexity and preference uncertainty. | Chernev, Böckenholt & Goodman | 2015 | Theory-based meta-analysis, 99 observations | https://doi.org/10.1016/j.jcps.2014.08.002 |
| **(High)** Defaults exert a substantial aggregate influence on choice. | Jachimowicz et al. | 2019 | Peer-reviewed meta-analysis | https://doi.org/10.1017/bpp.2018.43 |
| **(Medium)** Advice can anchor decisions independently of advice quality. | Pütter et al. | 2017 | Peer-reviewed judge–advisor experiments; primary | https://doi.org/10.1027/1618-3169/a000361 |
| **(Medium)** Open-ended prompts have higher and demographically patterned nonresponse. | Pew Research Center | 2021, 2023 | Authoritative primary panel-data analysis; not peer reviewed | https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/ |
| **(High)** Interruption cost varies with task workload and timing. | Iqbal & Bailey | 2008 | Peer-reviewed controlled HCI experiment using pupillometry | https://doi.org/10.1145/1314683.1314689 |
| **(Medium)** Interrupted workers compensate with speed but report greater stress and effort. | Mark, Gudith & Klocke | 2008 | Peer-reviewed laboratory HCI experiment | https://doi.org/10.1145/1357054.1357072 |
| **(Medium)** Even brief interruptions can sharply increase sequence errors. | Altmann, Trafton & Hambrick | 2014 | Peer-reviewed cognitive experiment | https://doi.org/10.1037/a0030986 |
| **(High)** Shorter questionnaires improve response on average, but no universal item threshold exists. | Nakash et al. | 2006 | Systematic review and meta-analysis of randomized trials | https://pmc.ncbi.nlm.nih.gov/articles/PMC1421421/ |
| **(High)** Seven pages reduced response versus four or five pages in older women. | Iglesias & Torgerson | 2000 | Quasi-randomized trial, \(n=847\) | https://pubmed.ncbi.nlm.nih.gov/11184958/ |
| **(Medium)** Plain-language questionnaires do not universally improve data quality but may help vulnerable subgroups. | Bauer, Kunz & Gummer | 2025 | Peer-reviewed between-subjects web experiment | https://doi.org/10.1080/13645579.2023.2294880 |
| **(Medium)** Plain language can increase differentiation and speed while shifting response means. | Kunz, Gummer & Neuert | 2026 | Peer-reviewed randomized web experiment, \(n=3,256\) | https://doi.org/10.1177/1525822X251322031 |
| **(High)** Clarification improved benchmark code generation. | Mu et al., ClarifyGPT | 2024 | Peer-reviewed FSE framework; human and simulated-user evaluation | https://doi.org/10.1145/3660810 |
| **(Medium)** Whether to clarify should be modeled selectively rather than asking on every ambiguity. | Kim et al. | 2021 | Commercial conversational-agent evaluation; authoritative primary source | https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding |
| **(Medium, PREPRINT)** Uncertainty-aware clarification improved coding-agent resolve rate. | Ask or Assume? | 2026 | Recent preprint; agent benchmark | https://arxiv.org/abs/2603.26233 |
| **(Low-to-Medium, PREPRINT)** Clarification ability is distinct from code-generation ability and declines with multiple ambiguities. | ClarifyCodeBench | 2026 | Very recent manually annotated benchmark preprint | https://arxiv.org/abs/2607.00711 |
| **(Medium)** ClarifyBench formalizes clarification evaluation for tool-using agents. | ACL Findings ClarifyBench paper | 2026 | Peer-reviewed benchmark paper | https://aclanthology.org/2026.findings-acl.2028.pdf |

---

## Knowledge Gaps

### Direct transfer to coding-agent workflows

- <MISSING_DATA>[A field experiment with professional developers comparing selective asking, always asking and never asking on real repository tasks, measuring task correctness, rework, latency and satisfaction.]</MISSING_DATA>
- <MISSING_DATA>[Evidence on whether expert users answering questions about their own code are less susceptible to option order and anchoring than general survey respondents.]</MISSING_DATA>
- <MISSING_DATA>[Longitudinal evidence on whether users abandon or disable agents that ask too often.]</MISSING_DATA>

### Exact design parameters

- <INSUFFICIENT_EVIDENCE>No empirical optimum was found for questions per batch. “One, maximum three” is a defensible starting heuristic, not a discovered optimum.</INSUFFICIENT_EVIDENCE>
- <INSUFFICIENT_EVIDENCE>No universal optimal number of options exists. “Two to four, default three” is conditional on low option complexity and clear distinctions.</INSUFFICIENT_EVIDENCE>
- <INSUFFICIENT_EVIDENCE>No validated word-count threshold was found. Evidence concerns vocabulary, syntax, abstraction and total burden more strongly than raw words.</INSUFFICIENT_EVIDENCE>
- <MISSING_DATA>[A direct comparison of marked-first recommendation, marked-last recommendation, neutral ordering and preselection in coding decisions.]</MISSING_DATA>

### Free-text escape hatch

- <MISSING_DATA>[A randomized test of fixed options alone versus fixed options plus an optional adjacent note, with downstream implementation accuracy as the outcome.]</MISSING_DATA>
- <INSUFFICIENT_EVIDENCE>Existing open-question evidence establishes higher burden and selective nonresponse but does not quantify how often an optional coding note discovers a consequential missing constraint.</INSUFFICIENT_EVIDENCE>

### Requirements cost

- <INSUFFICIENT_EVIDENCE>There is no trustworthy universal rework multiplier attributable specifically to under-specified briefs.</INSUFFICIENT_EVIDENCE>
- <MISSING_DATA>[Prospective project telemetry linking the exact ambiguity, clarification timing, resulting code divergence and person-hours of avoided rework.]</MISSING_DATA>

### AI benchmark maturity

- <MISSING_DATA>[Benchmarks with real users, multi-file repositories, delayed responses, conflicting stakeholders and costly or irreversible actions.]</MISSING_DATA>
- <MISSING_DATA>[Calibrated ambiguity probabilities and expected-loss estimates, rather than binary ambiguous/unambiguous labels.]</MISSING_DATA>
- <MISSING_DATA>[Standard metrics for question quality that jointly capture information gain, user burden, answerability, anchoring and final task success.]</MISSING_DATA>

### Reporting and accessibility

- <MISSING_DATA>[Several primary-study full tables were inaccessible in the retrieved sources, preventing extraction of every requested sample size, coefficient, confidence interval and p-value. Full publisher access or author manuscripts would be needed.]</MISSING_DATA>

---

## Recommended Next Steps

1. **Run a preregistered factorial experiment inside a coding-agent benchmark.**  
   Compare: ask policy (`always`, `VOI-gated`, `never`) × batch size (`1`, `3`) × recommendation (`none`, `marked-first`) × note (`absent`, `optional`). Measure exact task success, incorrect assumptions, response time, number of turns, rework tokens, human time and subjective interruption.  
   **Rationale:** This directly estimates the parameters the existing cross-domain literature cannot supply.

2. **Build a real-ticket ambiguity corpus.**  
   Sample underspecified issues and feature requests; have maintainers identify plausible interpretations, the implementation consequence of each, questions they would ask and whether a safe reversible default existed.  
   **Rationale:** Current coding benchmarks overrepresent short, deliberately ambiguous algorithm tasks and underrepresent repository conventions and tacit context.

3. **Calibrate an expected-regret asking model from replay data.**  
   For historical agent runs, estimate whether alternative interpretations would have changed externally visible behavior and the cost of correcting the selected default. Train the asking policy on avoided regret minus interruption cost, not merely an ambiguity label.  
   **Rationale:** Ribeiro–Berry and ClarifyCodeBench both imply that detecting ambiguity alone is insufficient.

4. **Conduct a wording and option-count study with professional developers.**  
   Test total blocks near 30, 60 and 120 words; two, three and five options; jargon versus consequence-based labels; and single versus double-barrelled questions. Include comprehension checks and actual implementation choices rather than preference ratings alone.  
   **Rationale:** The proposed word and option targets presently rely on cross-domain inference.

5. **Audit recommendation-induced anchoring.**  
   Seed the agent with correct, weak and intentionally wrong recommendations, then measure acceptance, correction and final code quality under marked-first, marked-last, neutral and preselected formats.  
   **Rationale:** Default and advice research shows strong influence, but current coding-agent work has not established when that influence improves rather than degrades decisions.

## Sources

- [https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requireme...](https://www.researchgate.net/publication/318121417_On_Evidence-Based_Risk_Management_in_Requirements_Engineering)
- [https://doi.org/10.1145/1314683.1314689](https://doi.org/10.1145/1314683.1314689)
- [https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html](https://ideas.repec.org/a/oup/jconrs/v37y2010i3p409-425.html)
- [https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html](https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html)
- [https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_E...](https://www.researchgate.net/publication/235875570_Seeing_Through_the_Eyes_of_the_Respondent_An_Eye-Tracking_Study_on_Survey_Question_Comprehension)
- [https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-v...](https://www.pewresearch.org/decoded/2023/03/07/nonresponse-rates-on-open-ended-survey-questions-vary-by-demographic-group-other-factors/)
- [https://journals.sagepub.com/doi/10.2478/jos-2020-0041](https://journals.sagepub.com/doi/10.2478/jos-2020-0041)
- [https://arxiv.org/abs/1612.00163](https://arxiv.org/abs/1612.00163)
- [https://www.researchgate.net/publication/316362583_Impact_of_incorrect_and_new_requirements_on_wa...](https://www.researchgate.net/publication/316362583_Impact_of_incorrect_and_new_requirements_on_waterfall_software_project_outcomes)
- [https://arxiv.org/abs/1609.04886](https://arxiv.org/abs/1609.04886)
- [https://www.sciencedirect.com/science/article/pii/S0167642320300824](https://www.sciencedirect.com/science/article/pii/S0167642320300824)
- [https://doi.org/10.1109/EmpiRE.2015.7431303](https://doi.org/10.1109/EmpiRE.2015.7431303)
- [https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2009/2009_handbook_krosnick.pdf](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/2009/2009_handbook_krosnick.pdf)
- [https://journals.sagepub.com/doi/abs/10.1177/1525822x12448166](https://journals.sagepub.com/doi/abs/10.1177/1525822x12448166)
- [https://academic.oup.com/poq/article/72/5/914/1832496](https://academic.oup.com/poq/article/72/5/914/1832496)
- [https://academic.oup.com/poq/article/88/4/1249/8005355](https://academic.oup.com/poq/article/88/4/1249/8005355)
- [https://www.bls.gov/osmr/research-papers/1999/st990270.htm](https://www.bls.gov/osmr/research-papers/1999/st990270.htm)
- [https://www.researchgate.net/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-A...](https://www.researchgate.net/publication/265170803_Choice_Overload_A_Conceptual_Review_and_Meta-Analysis)
- [https://doi.org/10.1027%2F1618-3169%2Fa000361](https://doi.org/10.1027%2F1618-3169%2Fa000361)
- [https://experts.illinois.edu/en/publications/leveraging-characteristics-of-task-structure-to-pred...](https://experts.illinois.edu/en/publications/leveraging-characteristics-of-task-structure-to-predict-the-cost-)
- [https://eric.ed.gov/?id=EJ1458540&q=source%3A%22International+Journal+of+Social+Research+Methodol...](https://eric.ed.gov/?id=EJ1458540&q=source%3A%22International+Journal+of+Social+Research+Methodology%22)
- [https://journals.sagepub.com/doi/10.1177/1525822X251322031](https://journals.sagepub.com/doi/10.1177/1525822X251322031)
- [https://pmc.ncbi.nlm.nih.gov/articles/PMC1421421/](https://pmc.ncbi.nlm.nih.gov/articles/PMC1421421/)
- [https://pubmed.ncbi.nlm.nih.gov/11184958/](https://pubmed.ncbi.nlm.nih.gov/11184958/)
- [https://arxiv.org/abs/2310.10996](https://arxiv.org/abs/2310.10996)
- [https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-sca...](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding)
- [https://arxiv.org/abs/2507.21285](https://arxiv.org/abs/2507.21285)
- [https://huggingface.co/papers/2603.26233](https://huggingface.co/papers/2603.26233)
- [https://arxiv.org/abs/2607.00711](https://arxiv.org/abs/2607.00711)
- [https://aclanthology.org/2026.findings-acl.2028.pdf](https://aclanthology.org/2026.findings-acl.2028.pdf)
- [https://doi.org/10.1145/3660810](https://doi.org/10.1145/3660810)
- [https://www.tandfonline.com/doi/abs/10.1080/13645579.2023.2294880](https://www.tandfonline.com/doi/abs/10.1080/13645579.2023.2294880)
