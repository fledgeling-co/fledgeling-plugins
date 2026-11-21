# Getting through screening at Australian banks in late 2026: CV, LinkedIn and Seek strategy for an internal-first Product Owner, Delivery Lead or People Leader move

*Research cut-off: 20 November 2026. All "live" job-ad observations were made on 18–20 November 2026 unless stated otherwise.*

**Method note.** I worked from four kinds of source:

- **Bank careers sites.** I identified each bank's applicant tracking system (ATS) by reading its careers-site domains, page markup and apply links.
- **Live job ads.** I pulled 16 full-text ads for the target roles directly from the CBA (Workday), ANZ (SAP SuccessFactors) and ING (Workday) feeds, and read partial text of about 12 more for Westpac, NAB, Macquarie, Bendigo and Revolut through aggregator mirrors.
- **Vendor documentation.** Workday/HiredScore, SAP, Oracle Taleo, Eightfold, PageUp, Seek and LinkedIn.
- **Australian survey and regulatory material.** AHRI/AHRC, ABA, APRA, ACCC, Hays, Robert Walters and people2people.

Seek blocked automated access (HTTP 403), so the listing sample comes from bank-owned feeds rather than Seek. The keyword counts are therefore a **small, bank-direct sample, not a market census**.

---

## 1. Executive summary

- **There is no single "bank ATS", and the platform differs at every bank she is targeting.** CBA and ING Australia run Workday. ANZ and Bendigo run SAP SuccessFactors. Westpac runs Oracle Taleo. NAB's Australian roles run on PageUp, with Eightfold AI for its international roles. AMP runs Oracle Recruiting Cloud. Macquarie appears to run Avature. One CV file has to parse cleanly in all of them, so formatting discipline matters more than designing for any one system. *(Confidence: High for CBA, ANZ, Westpac, NAB, ING, Bendigo and AMP; Medium for Macquarie; Low–Medium for Judo, Revolut and Beem.)*
- **The ranking engines now read meaning, not just keywords, but they still score against the ad's stated requirements.**
  - Workday's HiredScore grades applicants A–D. "B" means the resume meets every required qualification; "C" means it meets most but not all.
  - Eightfold (NAB's international site) scores 0–5 using skill embeddings, title trajectory and "recent-role" skills. NAB's configuration marks 4.0 as a "strong match".
  - Practical consequence: every *required* item in an ad needs a visible, literal counterpart on the CV, and the most recent roles carry extra weight. *(High for how the vendors document it; Medium on whether a particular bank has switched these features on.)*
- **Use DOCX by default for bank portals and keep a text-based PDF for people.** SAP's own help page lists DOCX, but not PDF, among the formats SuccessFactors sends to its parser, and SuccessFactors is the system at ANZ and Bendigo. Workday, Eightfold, PageUp and Avature all accept both formats. *(Medium–High.)*
- **The CV for Australian bank roles in 2026 runs two to three pages, with no photo, no date of birth and no full address, and referees "available on request".**
  - Hays says about two pages. SEEK (updated 30 September 2026) allows two to five pages for extensive experience, and says to leave out the photo, the full address and anything that reveals age.
  - For 20+ years across several roles I recommend **two pages for external applications, with three as a hard ceiling**, and making page 1 carry the whole case. *(High for the conventions; Medium for the length recommendation, because the sources disagree.)*
- **Twenty years at one employer should read as a promotion ladder, not as one long job.**
  - Use a single employer heading with each role nested under it, each with month–year dates.
  - Describe the last 10–12 years in full and compress earlier roles into one "Earlier roles" line.
  - Leave graduation years off.
  - Keep the true employer start year: Workday and SuccessFactors application forms ask for role dates anyway, and a CV that disagrees with the form costs more than tenure does. *(Medium; partly my inference.)*
- **Age bias is real in Australian hiring and has moved younger.** In the 2025 AHRI/AHRC survey, 24% of HR respondents called workers aged 51–55 "older", up from 10% in 2023. 56% were open "to a large extent" to hiring people aged 50–64, against 80% for those aged 25–34. The LLM-screening research is mixed rather than uniformly anti-older. Remove proxies such as graduation years and "30 years' experience"; do not hide facts. *(High for the survey; Low–Medium for the LLM effect.)*
- **The vocabulary that recurs in current bank ads is outcomes, stakeholders, risk, customer, delivery, prioritisation, dependencies and governance, much more than certifications.**
  - Across 16 full-text target-role ads, "stakeholder", "outcome(s)", "customer", "risk" and "delivery" appeared in all 16. "Prioritise/prioritisation" and "financial services/banking" appeared in 11, and "dependencies" in 9.
  - Only 2 of 16 mentioned any certification, and both called it "advantageous" or "viewed favourably".
  - No ad named CPS 230 explicitly. Westpac's product ads consistently use SAFe language ("Release Train"); CBA's use "domain / crew / Product Lead". *(Medium: small sample.)*
- **AI-written CVs are not detected by the ATS. Generic writing is penalised by people.** No Australian employer surveyed by AHRI (September 2025) auto-rejected AI-written applications; it describes AI checkers as "far from foolproof". Recruiters do report rejecting applications that read as generic, over-polished or unspecific. Write with numbers, names of real systems and real decisions. *(Medium–High.)*
- **For the internal move, the internal portal is mandatory, not optional.**
  - CBA states that existing employees "need to apply through Sidekick to submit a valid application". Bendigo routes staff through People Hub. Westpac has a separate internal Taleo career section and a new Internal Careers site (FY25). NAB's PageUp signs employees in automatically.
  - The internal market is tight after 2025–26 restructures (ANZ alone cut about 3,500 roles). Tell the current manager before applying. *(High for the portals; Medium for the etiquette.)*
- **On LinkedIn, set Open to Work to "Recruiters only" or hold off until the internal search is done; LinkedIn's own help page says it "can't guarantee complete privacy" from recruiters at her current employer. On Seek, the visibility setting is the main lever.**
  - Hiring Assistant has been generally available in Australia since about October 2025, and Hiring Assistant 2 rolls out from November 2026.
  - Seek's "Public" setting shows name, role title and most recent company to anyone, even people who are not signed in. *(High.)*

---

## 2. Detailed findings

### 2.1 Screening technology: which tools the banks use and how they parse and rank

#### 2.1.1 What each bank actually runs (evidence-based)

| Bank | Platform found | Evidence | Confidence |
|---|---|---|---|
| **CBA** (incl. Bankwest, x15ventures) | **Workday Recruiting** | Live ads at `cba.wd3.myworkdayjobs.com/CommBank_Careers`, e.g. *Product Manager, Deposits* (REQ268169, posted 19 Nov 2026, closes 29 Nov 2026) and *Technology Product Owner – Database & DevSecOps* (REQ267762, 18 Nov 2026). Every ad carries the line: "If you're already part of the Commonwealth Bank Group… you'll need to apply through Sidekick to submit a valid application." (CBA Workday feed, accessed 20 Nov 2026, https://cba.wd3.myworkdayjobs.com/CommBank_Careers) | High |
| **Westpac** (incl. St.George group) | **Oracle Taleo** (Australia); Workday for Westpac NZ | An internal career section exists at `westpac.taleo.net/careersection/group_internal/` and links to the Westpac and St.George intranet "employee-central/careers"; its build string reads "2026PRD", which suggests a live 2026 deployment (Westpac Taleo, accessed 20 Nov 2026, https://westpac.taleo.net/careersection/group_internal/jobsearch.ftl). The Taleo sign-in page tells staff their username is "AU + salary number" (search snapshot, https://westpac.taleo.net/careersection/iam/accessmanagement/login.jsf). Westpac NZ uses `westpacnz.wd105.myworkdayjobs.com` (https://westpacnz.wd105.myworkdayjobs.com/en-US/Westpac_Careers). | High for Taleo internally; Medium that external Australian applications still go through Taleo rather than a newer system |
| **NAB** | **PageUp** (Australian roles) behind a branded front end at `careers.nab.com.au`; **Eightfold AI** for international and BNZ roles | The PageUp sign-in "Applicant sign in – National Australia Bank" (client 410) says: "Current NAB employees – please click Next to sign in automatically" (https://secure.dc2.pageuppeople.com/apply/410/aaw/applicationform/default.asp, accessed 20 Nov 2026). NAB's careers page sends overseas candidates to `nab.eightfold.ai` (https://www.nab.com.au/about-us/careers). The Eightfold site's configuration shows `strongMatchThreshold: 4.0`, profile-match sorting switched on, and Workday-style "JR" requisition IDs (https://nab.eightfold.ai/careers). | High for PageUp and Eightfold; vendor of the `careers.nab.com.au` front end not identified |
| **ANZ** | **SAP SuccessFactors Recruiting** (Recruiting Marketing career site) | `careers.anz.com` links to `career10.successfactors.com … company=anzbanking` and uses the `rmkcdn.successfactors.com` assets (accessed 20 Nov 2026, https://careers.anz.com/go/ANZ-Jobs-List/4739210/). An older ANZ guide shows ANZ previously ran Taleo (https://www.anz.com/resources/f/e/fe6e420047cc7d3bb57db7e47d444d82/Quick-Reference-Guide.pdf, undated, older). | High |
| **Macquarie** | **Avature** (inferred) | Avature URL patterns (`/en_US/careers/JobDetail/…`, `/ApplicationMethods?jobId=`) on `recruitment.macquarie.com`, plus a Macquarie talent-community page hosted on `sandboxmgl.avature.net`. The registration page accepts a resume in "PDF or Word format… less than 20MB" (https://recruitment.macquarie.com/en_US/careers/RegistrationMethods). | Medium |
| **AMP / AMP Bank** | **Oracle Recruiting Cloud** (Oracle HCM Candidate Experience) | AMP's careers page links to `fa-esow-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1` (https://www.amp.com.au/about-amp/careers, accessed 20 Nov 2026). | Medium–High |
| **ING Australia** | **Workday** (site `ICSGBLCOR`) behind a Radancy/TalentBrew front end at careers.ing.com | Live Sydney ads in the Workday feed: *Product Owner – Onboarding and Engagement* (REQ-10124137) and two *Senior Customer Journey Expert / Product Manager* roles (https://ing.wd3.myworkdayjobs.com/en-US/ICSGBLCOR). | High |
| **Bendigo & Adelaide Bank** | **SAP SuccessFactors** | `careers.bendigobank.com.au` loads `career10.successfactors.com` and `rmkcdn.successfactors.com` assets (accessed 20 Nov 2026, https://careers.bendigobank.com.au/). Staff apply via "People Hub" (aggregator snapshot of the Bendigo careers search). | High for SuccessFactors; Medium for People Hub |
| **Up** | Ferocia careers page; ATS **not confirmed** | "Up is built by Ferocia"; roles are listed on Ferocia's careers page (https://up.com.au/careers/). | n/a |
| **Judo Bank** | **SmartRecruiters** (third-party claim) | An aggregator states that Judo uses SmartRecruiters (https://scoutify.com/companies/judo-bank/). Not verified on judo.bank. | Low–Medium |
| **Revolut Australia** | In-house careers site; ATS **not confirmed** | Revolut says it uses no third-party recruitment platforms and that genuine email comes only from @revolut.com (search snapshot of revolut.com/careers). | n/a |
| **Beem (AP+)** | Australian Payments Plus careers site, possibly **Workable** | Beem hires through its parent, AP+; one tracker lists `apply.workable.com/auspayplus` (search results; https://www.auspayplus.com.au). | Low |

**What could not be confirmed.**

- I found no public evidence that CBA, ING or Westpac NZ have switched on Workday's paid HiredScore grading.
- I found no evidence on whether Westpac's Taleo uses any AI ranking layer.
- I found no evidence on whether ANZ uses SAP's AI-assisted matching.
- HireVue at ANZ is documented only by a graduate-focused third-party prep site (GraduatesFirst, 2026, https://www.graduatesfirst.com/anz-job-interviews; low-grade).
- Westpac says only that "some roles" start with "a recorded video interview or a phone interview", and that First Advantage runs background checks (Westpac, undated, accessed 20 Nov 2026, https://www.westpac.com.au/about-westpac/careers/how-to-apply/recruitment-process/).

#### 2.1.2 How the ranking layers work, per vendor documentation

**Workday HiredScore (CBA and ING, if enabled).** Workday's own reference page defines the grades (Workday, "Reference: Candidate Grades", accessed 20 Nov 2026, https://doc.workday.com/hiredscore/en-us/workday-hiredscore/recruiter-productivity-/reference--candidate-grades.html):

- **A:** "meets all basic (required) qualifications, most preferred qualifications" and "has an average qualification match above a defined threshold".
- **B:** "meets all basic qualifications".
- **C:** "meets most but not all basic qualifications".
- **D:** "does not meet most basic qualifications".

Grades are based on "how well their resumes match the skills and qualifications specified in the job description". Workday's published bias audit covers September 2025 to February 2026, finished testing on 20 March 2026, and describes Spotlight as comparing "stated qualifications" with job requirements (Workday, "Responsible AI and Bias Mitigation for HiredScore Spotlight", 2026, https://www.workday.com/en-us/legal/responsible-ai-and-bias-mitigation.html). *Confidence: High that this is how it works; Unknown whether CBA or ING use it.*

*Implication (my inference):* the jump from C to B is binary on **required** qualifications. If an ad requires "experience in a regulated financial services environment" and "agile delivery", the CV must say both in words a matcher can align, ideally in the summary and in the most recent role.

**Eightfold (NAB international; also used by many global firms).** Eightfold's engineering blog (13 August 2025, https://eightfold.ai/engineering-blog/ai-powered-talent-matching-the-tech-behind-smarter-and-fairer-hiring/) describes its matching:

- Semantic embeddings of resumes and job descriptions.
- Skill similarity computed twice, once on all skills and once **on skills from recent roles only**, which it calls a "freshness" signal.
- Title-trajectory models that predict the candidate's likely next title.
- Employer-similarity embeddings.
- A calibrated 0–5 score, shown as stars.

NAB's live configuration sets 4.0 as "strong match". *Confidence: High.* *Implication:* skills that appear only under a 2008 role count for less than skills in the 2023–2026 roles. Put the target vocabulary in the current and previous role.

**SAP SuccessFactors (ANZ, Bendigo).**

- SAP's help page says resumes can be uploaded "with DOCX, PPT, and TXT format" for parsing, and that SuccessFactors uses Textkernel as its parser. PDF does not appear on that parsing list, although PDF is an accepted upload type for the Candidate Profile. (SAP Help Portal, "Working with Resume Parsing" and "Candidate Profile in SAP SuccessFactors", accessed via search 20 Nov 2026, https://help.sap.com/docs/successfactors-recruiting/setting-up-and-maintaining-sap-successfactors-recruiting/working-with-resume-parsing.) I could not render the SAP page directly; the wording comes from the indexed text.
- Textkernel itself parses PDF (Textkernel developer specs, https://developer.textkernel.com/tx-platform/v10/resume-parser/overview/specs/).

*Confidence: Medium–High.* *Implication:* for ANZ and Bendigo, upload **DOCX**.

**Oracle Taleo (Westpac).**

- Oracle documents three recruiter keyword-search modes: "Exact Terms", "Related Terms" and "Conceptual". Conceptual mode broadens the search across "documents or attachments with relevant ideas and concepts" (Oracle, Taleo Enterprise 21B, "Searching for Candidates", https://docs.oracle.com/en/cloud/saas/taleo-enterprise/21b/otfru/searching-for-candidates.html).
- Resume parsing populates profile fields (Oracle, Taleo 21B "Candidate Management", https://docs.oracle.com/en/cloud/saas/taleo-enterprise/21b/otrec/candidate-management.html).

*Implication:* Westpac recruiters searching Taleo can still run exact-term searches, so literal terms ("Product Owner", "Release Train", "SAFe", "Jira", "backlog") matter more here than at an Eightfold or HiredScore bank. *Confidence: Medium.*

**PageUp (NAB Australia).** In August–September 2025 PageUp launched "AI Resume Summarization", "Transparent AI Skills Matching" and the Paige co-pilot (PageUp, 16 September 2025, https://www.pageuppeople.com/news/paige-ai-launch/). In August 2026 it announced Sapia.ai text-based AI interviewing that "screens 100% of applicants" (GlobeNewswire, 26 August 2026, https://www.globenewswire.com/news-release/2026/08/26/3351491/0/en/pageup-and-sapia-ai-embed-intelligent-ai-interviewing-directly-into-enterprise-hiring-workflows.html). Whether NAB has switched these on is **not confirmed**. *Implication:* an AI summary of her CV may be the first thing a NAB recruiter reads. A CV whose first third states role, scale and outcomes plainly will summarise well.

**Seek and LinkedIn.**

- Seek's employer side offers Talent Search over profile fields: work history, education, qualifications and right to work. A free "Basic Talent Search" tier has terms updated 20 July 2026, and a seekAi-powered Premium tier was flagged for 2026 (Seek, https://au.employer.seek.com/products/talentsearch; https://au.employer.seek.com/support/talentsearchofferterms; https://au.employer.seek.com/products/article/enhanced-discovery-for-candidates).
- Employers can add up to eight screening questions, including right to work (search snapshot of au.employer.seek.com hiring advice).
- LinkedIn's Hiring Assistant became generally available in English, including Australia, around late September to 1 October 2025 (HR Brew, 3 September 2025; Tech Business News, 1 October 2025, via search snippets).
- Hiring Assistant 2 was announced on 29 September 2026, adds "fit signals" and voice pre-screening, and rolls out free to English-language customers from November 2026. Its Workday integration is listed as "coming soon" (DHRmap and others, September–October 2026, https://www.dhrmap.com/news/linkedin-launches-hiring-assistant-2).

*Confidence: Medium. LinkedIn's own announcement page was not directly opened.*

#### 2.1.3 Formatting: where sources agree and disagree

| Issue | Evidence | Recommendation |
|---|---|---|
| **DOCX vs PDF** | SAP lists DOCX, not PDF, for parsing (above). Workday accepts DOC, DOCX, PDF and others; community reports say DOCX autofills more reliably, which is anecdotal (third-party Workday guides, 2026; low-grade). Macquarie accepts PDF or Word. NAB Eightfold accepts pdf, doc, docx, txt, rtf and ppt(x). | **DOCX for every bank portal.** Text-based PDF for emailing a human, the LinkedIn "Featured" section and internal hiring managers. Never an image-PDF. *Medium–High.* |
| **Columns, tables, text boxes** | No vendor publishes column-handling rules. Oracle's own example warns that keyword searches over unstructured text mis-hit ("Harvard" the town versus the university), which shows how parsers lose context. | Single column. No tables for experience, no text boxes, no skill bars or graphics. *Medium (inference from parser behaviour).* |
| **Headers and footers** | Not documented by vendors; widely reported by low-grade sources as being skipped by parsers. | Keep name and contact details in the body, not the Word header. Page numbers in the footer are fine. *Low–Medium.* |
| **Section headings** | Parsers map standard headings to fields. | Use conventional headings: "Career Summary", "Key Skills", "Professional Experience", "Education & Certifications". *Medium.* |
| **Dates** | Hays: list work history "in reverse chronological order" with "months as well as years" (Hays, undated, accessed 20 Nov 2026, https://www.hays.com.au/career-advice/resumes-cover-letters/how-to-write-a-resume). Workday and SuccessFactors forms ask for start and end dates per role. | "Mar 2021 – Present" format, consistent throughout. *High.* |
| **Keyword vs semantic** | HiredScore matches against stated qualifications. Eightfold uses embeddings plus recency. Taleo supports exact-term search. | Use the ad's literal phrases **and** concrete context, once each in the summary and skills and again inside achievements. No keyword stuffing. *Medium–High.* |
| **Knockout questions** | Seek screening questions (up to eight, including right to work). Westpac: "answer some questions as part of your application". | Answer knockout questions consistently with the CV; state citizenship or work rights on the CV. *High.* |

### 2.2 Australian conventions for 2026

**Length.** The authorities disagree:

- **Hays:** "Your resume should be approximately two pages long" (Hays, accessed 20 Nov 2026).
- **SEEK (updated 30 September 2026):** a resume "can be two to five pages long if you have extensive experience and are looking for senior positions"; its FAQ says three to five pages (https://au.seek.com/career-advice/article/how-to-make-a-resume). SEEK's separate article says "typically one to two pages" (https://au.seek.com/career-advice/article/how-long-should-a-resume-be, mid-2026).
- **DEWR's résumé tips:** "no more than 2 pages" (DEWR PDF via search snippet, undated; https://www.dewr.gov.au/download/8284/resume-tips-and-example-resume/12432/resume-tips-and-example-resume/pdf).
- **UQ:** 2–4 pages for professionals (UQ Employability, undated).

*My recommendation:* **two pages for external applications and three as a ceiling**, with page 1 complete on its own (summary, skills and the most recent two or three roles). ATS and LLM screeners do not penalise length, but recruiters faced with Robert Walters' "600 applications in the first 24 hours" skim (AHRI, 3 September 2025, https://www.ahri.com.au/articles/responding-to-ai-generated-applications). An internal version can run to three pages if the hiring manager wants role-by-role detail. *Confidence: Medium.*

**Personal details.** SEEK says to "leave out your photo – it's not standard in Australian resumés – and your complete address", and to leave out "any mention of your age, unless the position has age-related requirements" (SEEK, 30 September 2026). The Queensland Human Rights Commission says employers generally should not ask for age or date of birth at application stage (QHRC, https://www.qhrc.qld.gov.au/your-rights/discrimination-law/age). Hays recommends name, phone, professional email and LinkedIn URL. *Recommendation:* name, suburb and state (e.g. "Parramatta NSW"), mobile, email, LinkedIn URL, and a work-rights line. No photo, no date of birth, no marital status, no street address. *High.*

**Referees.** Hays: referee details "are rarely included"; "References are available upon request" is common, and the most valued referees are "those people you reported to directly". SEEK agrees that most employers ask after interview. DEWR's older guidance says to list two. *Recommendation:* use "Referees available on request" externally. **Internally,** be ready to name the current manager plus one previous manager or senior stakeholder from another division. *High.*

**Career summary.** SEEK: "ideally just one to three sentences". Hays: 50–150 words, tailored, stating what you offer. *Recommendation:* 60–100 words, rewritten per role family (PO/PM versus Delivery Lead versus People Leader). *High.*

**Spelling.** Australian bank ads use Australian spelling ("prioritise", "organisation", "programme" occasionally, "behaviour"), as observed across all 16 sampled ads. Use Australian spelling throughout. Semantic matchers handle the variants, but exact-term Taleo searches may not. *Medium.*

**Work rights and citizenship.** Seek employers can filter on right to work, and Seek profiles carry a right-to-work field verifiable through SEEK Pass (Seek profile privacy, https://au.seek.com/profile-privacy; Talent Search pages). *Recommendation:* add "Australian citizen" to the CV contact line and complete and verify the right-to-work field in Seek. *High.*

**Background and conduct checks: how banks treat them and what to show.**

- The ABA's Industry Protocol – Conduct Background Check (Version 14.0) applies to prospective employees for any role based in Australia, apart from the advice-specific carve-outs. It covers a request period of "up to 5 years", requires the candidate's consent using standard wording, and asks former employers fact-based questions about dismissal or resignation for misconduct (ABA, file dated 30 September 2025, hosted March 2026, https://www.ausbanking.org.au/wp-content/uploads/2026/03/Final-ABA-Industry-Protocol-Conduct_Background_Check-250930.pdf).
- Westpac uses First Advantage for "a range of third-party background checks", timed by role risk profile and overseas history (Westpac recruitment process page).

*Recommendation:* do not put a "police check" line on the CV. An optional, honest line under Additional Information ("Eligible for standard financial-services background and conduct checks") is acceptable but adds little. A 20-year clean record at one ADI is itself the strongest signal; the protocol means the next bank will ask her current employer anyway. *Medium.*

### 2.3 Twenty-plus years at one employer: structure, depth, age signals

**Structure.** Sources and parsers point the same way: one employer block containing separate, dated role entries.

- Hays wants reverse-chronological order with months.
- Workday and SuccessFactors autofill create one "experience" record per role.

A single 20-year entry would collapse into one record and hide the promotions. *My inference:* to avoid a parser merging nested roles, repeat a short employer name on each role line ("Senior Product Owner | [Employer] | Jul 2022 – Present"). This costs nothing for a human reader. *Medium–Low; vendors do not document nested-role handling.*

**Depth.**

- Last 10–12 years: full achievement bullets. Three to five for the current role, two to four for the one before, one to three for older ones.
- Before that: one line titled "Earlier roles", listing titles such as Team Leader, Senior Analyst and Customer Service Manager, with an optional single highlight.

This puts the target vocabulary where Eightfold's "freshness" weighting and human reading time both concentrate. *Medium–High.*

**Age and "stagnation" signals: what to remove and what to keep.**

The evidence that age bias exists in Australian hiring:

- AHRI/AHRC 2025 (n=148 HR professionals; https://www.ahri.com.au/wp-content/uploads/Older-Younger-Workers-Report-2025-FINAL.pdf): 24% consider 51–55 "older" (10% in 2023, 17% in 2021). 56% are open to hiring people aged 50–64 "to a large extent", against 80% for ages 25–34 and 78% for 35–49. On the positive side, 57% report no age above which they are reluctant to recruit, and "exclude date of birth from application forms" is among the age-inclusive practices tracked. *High.*
- Sheard (University of Melbourne) found that AI hiring systems used by Australian employers "may solidify traditional forms of hiring discrimination", mainly through how recruiters configure them (Journal of Law and Society, 2025, https://onlinelibrary.wiley.com/doi/10.1111/jols.12535). *Medium.*

The LLM research is mixed:

- A 2026 audit that used graduation year as the age proxy found most of the apparent age effect was really experience. Under a naturalistic prompt it found *older* cohorts scored slightly higher (MDPI *Analytics*, 2026, https://www.mdpi.com/2813-2203/5/3/30).
- A Springer study of ChatGPT, Claude and DeepSeek found under-selection of older candidates in some conditions (https://link.springer.com/chapter/10.1007/978-3-032-16764-4_13).

*Confidence: Low–Medium that LLM screeners penalise age; High that graduation year is the main age proxy machines read.*

Recommendations:

| Do | Don't |
|---|---|
| Remove graduation years and school-leaving details | Delete or shift dates of roles you list in full |
| Write "Earlier roles" without years if you list them as titles only, but keep the employer's true start year in the heading | Write "30 years' experience" or "over two decades" in the summary. Say "extensive" plus the specific scope instead. |
| Show recency: current tools (Jira, Confluence, Miro, Power BI, GenAI copilots the organisation has approved), current frameworks, 2024–2026 outcomes | List obsolete tools (Lotus Notes, legacy mainframe screen names) unless the ad asks |
| Make each promotion visible as a separate dated role, and name a cross-division move as a move ("moved from Retail Operations to Digital to…") | Collapse 20 years into "Various roles" |

Keeping the start year honest matters for three reasons. Application forms collect role dates. The ABA conduct check and referee calls go to her employer. And a CV whose dates disagree with the form looks worse than tenure does. *Medium (my judgement, grounded in the form design and the conduct protocol).*

**Turning tenure into breadth.** Each role line should carry its *reason for being there*, such as "promoted", "selected for", "seconded to" or "moved to lead". Use the summary to name the span: "across operations, digital and change", "led teams of up to [N]", "through [core platform migration / regulatory programme]". CBA's own careers material frames internal moves, secondments and short-term contracts as growth (CBA, "Career pathways at CommBank", c. 2021, older, https://www.commbank.com.au/articles/careers/career-pathways-at-commbank.html). Bank hiring managers are used to internal mobility and read it as institutional knowledge when it is framed that way. *Medium.*

### 2.4 Product Owner and people leadership: what the ads actually ask for

**Sample.** The full-text sample is 16 target-role ads:

- **CBA (6):** Senior Product Manager – Working Capital; Product Manager Commercial Cards; Product Manager CommSec; Technology Product Owner – Database & DevSecOps; Product Lead – Home Buying Verification Capability; Product Manager, Deposits.
- **ANZ (6):** Agile Delivery Lead (two); Change Lead; Senior Lead – Enterprise Change; Senior Project Manager; Senior Product Manager (Consumer Cards).
- **ING (4):** Product Owner – Onboarding and Engagement; two Senior Customer Journey Expert / PM roles; an EOI for Product Managers.

These were supplemented with partial text from seven Westpac PO/Lead PO ads (aggregator mirrors, November 2026), Macquarie's Engineering Product Owner (posted 4 November 2026), Bendigo Technical Product Owner ads (August–October 2026) and NAB Product Owner Deposits (October 2026). I counted presence per ad (does the ad contain the term at least once?).

| Term / theme | Ads containing it (of 16) | Notes |
|---|---|---|
| stakeholder(s) | 16 | Often "senior / executive stakeholders" (7) |
| outcome(s) | 16 | "customer and business outcomes", "measurable outcomes" |
| customer | 16 | |
| risk | 16 | Substantive, not boilerplate: "risks, controls and emerging priorities" (CBA Deposits); "risk remediation and operational resilience" (CBA Tech PO) |
| deliver / delivery | 16 | |
| data | 11 | "data-led decision making" is a CBA capability heading |
| prioritise / prioritisation | 11 | |
| financial services / banking experience | 11 | Usually "ideally within financial services… or another complex regulated environment" |
| end-to-end | 10 | |
| commercial / P&L | 9 | Strong in PM roles |
| dependencies | 9 | Delivery and PO roles |
| compliance / regulatory / governance | 8 each | |
| roadmap | 7 | |
| customer outcomes / conduct / vulnerability | 7 | |
| NPS / customer experience | 7 | |
| crew | 6 | All CBA ads: CBA's "domain → crew → squad / chapter" model |
| discovery | 6 | "continuous discovery, experimentation and adaptive delivery" (CBA) |
| coach / mentor | 6 | |
| agile / backlog / squad | 5 each | Low here because CBA PM ads describe agile practice without the word; Westpac PO ads (outside the count) all use squad, backlog and Release Train |
| metrics / KPIs, continuous improvement | 5 each | Delivery Lead ads name "velocity, cycle time and health checks" |
| change management / adoption | 4 | |
| Jira | 2 | Both ANZ Agile Delivery Lead ads ("Jira standards") |
| AI | 2–3 | "agentic AI verification" (CBA Home Buying); "AI literacy – … responsible use of role-appropriate AI tools" (CBA capability list); "AI-enabled products… welcomed, but not essential" |
| certification | 2 | "Agile delivery, Scrum or scaled agile certification is advantageous" (ANZ); "viewed favourably" |
| Scrum | 1 | |
| SAFe / Release Train | 1 in sample; **all 7** Westpac PO snippets | Westpac: "DU and Release Train priorities", "within agreed RT guardrails", "Definition of Done", "coaching other Product Owners" (freehire mirrors, November 2026) |
| CPS 230 / CPS 234 | 0 | Appears in no sampled ad |
| Kanban / Confluence / tribe | 0 | "Tribe" appears in ASB (NZ) ads, not CBA |

*Confidence: Medium. This is a small, bank-direct sample from three banks, plus qualitative reads of four others.*

**Bank-specific operating-model vocabulary to mirror (observed in the ads):**

- **CBA:** "domain", "crew", "Product Lead", "Product Stream Lead", "chapter", plus a published capability list: Product discovery and problem definition; Product roadmap and prioritisation; Product lifecycle management; Data-led decision making; Customer and user experience; Cross-functional collaboration; Commercial and market analysis; Risk management ("A risk mindset"); AI literacy; Ways of working.
- **Westpac:** "squad", "Release Train" / "RT", "CPO" (Chief Product Owner), "DU", "acceptance criteria", "Definition of Done", "embedding risk and regulatory obligations into product decisions". Westpac's UNITE technology-simplification programme runs to mid-2029 under a "3-in-a-box" Business/Technology/Data model (Westpac UNITE update, 26 March 2026, https://www.westpac.com.au/content/dam/public/wbc/documents/pdf/aw/ic/wbc-UNITE-presentation-2026.pdf).
- **ANZ:** "Agile Delivery Lead Practice", "squads", "value streams", "showcases", "psychological safety", "production readiness", "ANZ 2030 Strategy".
- **ING:** "Customer Journey Expert", cross-functional marketing, analytics and digital work, "basic SQL".
- **Macquarie:** builder-oriented: APIs, event-driven architecture, "AI agents or LLM-powered workflows", "rather than solely managing product roadmaps".
- **Revolut:** its Product Owner (Technical) ad states that "Product Owners at Revolut directly manage Engineering, Operations, and Design team members", which suits a candidate with both PO and people-management experience (Revolut careers, search snapshot, 2026).

**Certifications.** I found no Australian count of how often CSPO, PSPO or SAFe POPM is requested. The only data is a US LinkedIn figure from a training vendor (ThinkLouder, 2026; low-grade). In my sample, certifications were "advantageous" at most. *Recommendation:*

- If she holds one, list it, with its full name and acronym, in Education & Certifications and in LinkedIn Licences.
- If she is choosing one for Westpac (SAFe Release Trains), **SAFe POPM** is the closest fit.
- For the broader market, PSPO I (exam-based, no expiry) or CSPO.

Do not expect a certificate to compensate for missing outcome evidence. *Medium.*

**Regulatory themes and how to use them.**

- **CPS 230** has been in force since 1 July 2025. It requires ADIs to identify critical operations (payments, deposit-taking and others by default), set Board-approved tolerance levels, and manage material service providers (APRA CPS 230, https://www.apra.gov.au/system/files/2023-07/Prudential%20Standard%20CPS%20230%20Operational%20Risk%20Management%20-%20clean.pdf).
- The **Scams Prevention Framework** became law on 20 February 2025. Banks had to join AFCA by 1 September 2026, and most obligations apply from 31 March 2027 (ACCC, https://www.accc.gov.au/about-us/scams-prevention-framework).

No sampled ad named CPS 230, but "risk", "controls", "regulatory change", "compliance obligations" and "operational resilience" recur. *Recommendation:* name CPS 230, scams or DDO work only where she actually did it, and put it inside an achievement ("Owned the backlog for CPS 230 critical-operation mapping across [N] processes…") rather than in a keyword list. DDO and CPS 234 are background knowledge here; I did not source them in this run. *Medium.*

**Quantifying outcomes.** Use the CAR shape (Context, Action, Result) with a number in the result. Typical bank metrics, taken from the ads:

- NPS and complaints
- straight-through processing and turnaround times (CBA Home Buying)
- digital sales targets (NAB PO Deposits)
- velocity, cycle time and health checks (ANZ Delivery Lead)
- P&L drivers such as balances, spend and account growth (ANZ Senior PM)
- controls and remediation items closed
- team engagement scores and attrition
- people promoted

Rewrites are in Section 6.

### 2.5 AI-written CVs: detection, penalties and voice

**Usage in Australia.**

- people2people (16 September 2025): 25% of Australians have used AI to help write CVs or cover letters (Gen X highest at 33%), and 90% believe AI makes it easier to mislead (IT Brief, https://itbrief.com.au/story/ai-use-grows-in-australian-job-hunting-but-honesty-concerns-rise).
- Hays quotes Capterra's 73% of Australian job seekers using AI tools for CVs and cover letters (Hays, "Recruitment battle of the bots", c. 2025, https://www.hays.com.au/blog/insights/battle-of-bots).

The spread from 25% to 73% reflects different questions and samples. *Confidence: Medium.*

**Do tools detect it?** I found no evidence that any of the ATSs above flag AI authorship. AHRI's September 2025 review of Australian practice found:

- no featured employer auto-rejects AI-written applications;
- one firm tags suspected AI text "for further review";
- AI checkers are "far from foolproof";
- employers are adding skills tasks, short video introductions and referrals instead (AHRI, 3 September 2025).

*Confidence: Medium–High.*

**Do people penalise it?**

- people2people's NSW MD says over-polished applications "can raise red flags" and that trust is "the currency of recruitment" (HRD Australia, 10 September 2025, https://www.hcamag.com/au/specialisation/recruitment/recruiters-grapple-with-rise-of-ai-written-cvs/549105).
- Robert Walters UK found 73% of hiring managers claim they can spot AI-assisted CVs, citing "impersonal language and perfect formatting" (May 2025, UK, not Australian).
- Hays lists the tells as "flawless grammar, overly elaborate vocabulary, a perfectly uniform tone, and generic content with no specific examples".

*Confidence: Medium.*

**How to stay keyword-rich and human (recommendations):**

1. Draft from her own notes of real projects, numbers and decisions. Use AI, if at all, for compression and spelling, then re-insert the specifics.
2. Each bullet needs one fact only she could know: a system name, a volume, a regulator, a trade-off she made.
3. Ban the generic register: "spearheaded", "leveraged", "dynamic", "passionate", "results-driven", "proven track record", "in today's fast-paced".
4. Vary sentence length and keep some plain verbs ("ran", "cut", "fixed", "hired").
5. Mirror the ad's required phrases **once** in the summary or skills section and **once** in context. More than that reads as stuffing to people and adds nothing for semantic matchers.
6. Never invent a metric. The ABA check, the referee calls and the internal-HR record will test it.

### 2.6 Internal transfers at large Australian banks

**The mechanics.**

| Bank | Internal channel | Evidence |
|---|---|---|
| CBA | Sidekick (Career Hub). Applying through the external Workday site is not a "valid application" for staff | Every sampled CBA ad, November 2026. CBA's graduate page names the "Career Hub on Sidekick" (search snapshot) |
| Westpac | Separate Taleo career section `group_internal`, linked from the intranet "employee-central/careers"; a new Internal Careers site plus the Westpac Talent Community (FY25); job-matching tools for redeployed staff | Westpac Taleo (2026 build); Westpac 2025 Annual Report: "a second consecutive year of improvement in internal talent mobility, which is up 5% from FY23" (SEC filing, https://www.sec.gov/Archives/edgar/data/719245/000110465925105894/webnf-20250930xex15d3.htm) |
| NAB | Same PageUp instance; employees "sign in automatically". Source options include "NAB Intranet" and "Current Colleague" | PageUp sign-in page; Eightfold configuration |
| ANZ | **Not confirmed.** SuccessFactors usually runs an internal career site off the same requisitions (my inference). Some ANZ ads are internal secondments, e.g. "Role Type: Secondment – 12 Months" (ANZ Agile Delivery Lead) | ANZ ads, November 2026 |
| Bendigo | People Hub | Aggregator snapshot of Bendigo careers |

**Is internal screening different?** The ATS is the same system or tenant, so the same parsing and any grading layer apply. *(High for CBA, NAB and Westpac; Medium elsewhere.)* What differs is the people side:

- the internal HR record (performance ratings, tenure, conduct) is visible to the hiring side, in my inference;
- hiring managers often know the candidate's work, or can phone her manager;
- many internal roles are filled through networks or expressions of interest before or alongside advertising.

I found no 2025–26 bank-published internal-fill rate. Westpac reports only the 5% trend. *Confidence: Medium.*

**Market conditions.** ANZ announced about 3,500 role reductions plus about 1,000 contractors by September 2026, with branches and call centres largely excluded (ABC News, 9 September 2025, https://www.abc.net.au/news/2025-09-09/anz-to-cut-jobs-3500-to-go-by-sept-2026/105751484). NAB and Bendigo cut technology roles in 2025 (ACS Information Age, 2025, https://ia.acs.org.au/article/2025/tech-workers-face-job-cuts-at-anz--nab.html), and Westpac flagged about 250 cuts in October 2026 (search snapshot). *Implication:* internal roles are contested, sometimes by people in redeployment, and transformation and delivery roles are where cuts landed. A CV that connects her work to cost, simplification, risk reduction or customer outcomes is better aligned with the current mandate than one that leads with "managed a team of 12". *Medium.*

**What the internal CV should do differently.**

- **Lead with the target role's language, not the current department's.** Internal jargon (programme code names, team acronyms) is fine for an internal reader, but gloss it once: "Project Phoenix (core lending platform migration)". Keep a de-jargoned external version.
- **Use internal proof points the external version can't:** performance ratings ("rated Exceeds in FY24 and FY25", only if that is accurate and the culture allows it), internal awards, named executive sponsors, and transformation programmes the hiring manager will recognise.
- **Anticipate "why move?"** A one-line summary clause should frame it as wanting breadth or scope, not escape.
- **Internal referees:** her current manager (expect the hiring manager to call them anyway) plus a senior stakeholder from another division, which evidences cross-functional reputation.
- **Length:** three pages is acceptable internally if the hiring manager wants depth. Two is still safer for the portal.

**Etiquette.** Generic career sources agree: tell the current manager before or at the time of applying, and frame it as growth, because most internal processes involve the current manager at some point (Indeed UK; Job200; CareerBuilder; low-to-medium-grade generic sources). Bank policies on notifying managers are not public. Check the intranet policy. *Medium.*

### 2.7 LinkedIn and Seek in 2026

**LinkedIn.**

- **Open to Work.** The options are "All LinkedIn Members" (adds the #OpenToWork frame), "Recruiters only" (people using LinkedIn Recruiter) and "Visible only to you". LinkedIn "takes steps" to hide the signal from Recruiter users at the current employer but "can't guarantee complete privacy" (LinkedIn Help, updated about November 2026, https://www.linkedin.com/help/linkedin/answer/a507508/let-recruiters-know-you-re-open-to-work). **Recommendation:** "Recruiters only" during the internal phase, or off entirely if discretion matters most. Never the public frame while pursuing an internal move. *High.*
- **How recruiters find people.**
  - LinkedIn's Recruiter help page says its AI-assisted messages draw on job title, company, Open to Work status, skills, location and past-applicant status (LinkedIn Help, https://www.linkedin.com/help/recruiter/answer/a1445743).
  - AI-assisted search, which replaced Boolean search as the default, weighs titles, skills, experience and career trajectory, according to third-party vendor guides (Pin, HeroHunt, 2026; Medium–Low).
  - Hiring Assistant 2 (from November 2026) adds "fit signals" and voice or text pre-screening.

  *Implication:* headline and current-role title carry the most weight. Skills must be listed explicitly. Activity and recency signals matter.
- **Profile recommendations:**
  - **Headline (220 characters):** target title plus domain plus proof. For example: "Senior Product Owner | Agile delivery & people leadership in banking | Payments, lending & regulatory change | Jira, SAFe, discovery." Avoid "Experienced professional seeking…".
  - **About (about 1,200–2,000 characters):** first person, four short paragraphs: what she does; two or three quantified outcomes; how she leads people; what she wants next (phrased neutrally if the search is confidential). Unlike the CV, it can carry personality.
  - **Experience:** mirror the CV's nested roles under one company entry, using LinkedIn's multiple-positions-under-one-company feature, so promotions show as a ladder. Give two or three bullets per recent role. Don't paste the CV wholesale.
  - **Skills:** fill the section with the exact strings from Section 4 (Product Ownership, Agile Methodologies, Scrum, SAFe, Backlog Management, Product Roadmapping, Stakeholder Management, Risk Management, People Leadership, Change Management, Jira) and pin the top three. *Medium.*
  - **Licences & Certifications:** full names with acronyms.
  - **Easy Apply:** fine for Revolut, fintechs and AP+. For the big banks, apply on the bank's own portal where possible, because the ad directs you there and the ATS record is what's screened. *Medium (inference).*

**Seek.**

- **Visibility settings** (Seek, https://au.seek.com/profile-privacy):
  - **Public:** anyone, including users not signed in, sees "name, location, role title and most recent company".
  - **Standard:** signed-in employers can search and see the full profile, verified information and resume.
  - **Limited:** employers can email her via Seek but can't see her resume.
  - **Hidden ("Applications only"):** visible only to employers she applies to.

  Partner recruitment software can see full profiles on Public or Standard. Seek's People Search lets "anyone on SEEK, including other candidates, referrers, hiring managers and recruiters" find public profiles (Seek employer site, 2025/26). I found **no Seek feature that blocks her current employer**. *Recommendation:* **Limited or Standard** during the internal phase, since Public exposes her name and current employer to anyone. Move to Standard once she starts the external search. *High for the facts; the setting itself is her trade-off between discretion and discoverability.*
- **Right to work:** complete the field and verify it via SEEK Pass, because employers can filter on it.
- **Profile content:** Seek Talent Search shows work history, education, qualifications and right to work. Use the same role titles and dates as the CV. Keep a short "Personal summary" (the CV summary, lightly shortened). Add skills using Seek's suggested terms that match Section 4. Upload the DOCX as the default resume.
- **Consistency rule:** titles, employers and dates must match exactly across the CV, LinkedIn and Seek, because recruiters and Hiring Assistant cross-check. Wording should differ: CV bullets are evidence-dense, LinkedIn's About is voice and narrative, and Seek's summary is a short pitch.

---

## 3. Bank-by-bank table

| Bank | ATS / screening tool (evidence) | Application channel | Notable culture and keyword signals (from current ads) |
|---|---|---|---|
| **CBA** | Workday Recruiting, `cba.wd3.myworkdayjobs.com/CommBank_Careers` (live REQ268169, REQ267762 and others, November 2026). HiredScore not confirmed. | External: Workday. **Internal: Sidekick / Career Hub (mandatory)**. Seek and LinkedIn mirrors. | Domain / crew / squad / chapter; "Product Lead", "Product Stream Lead"; capability list including "AI literacy", "A risk mindset", "continuous discovery, experimentation and adaptive delivery"; "complex regulated environment". |
| **Westpac** | Oracle Taleo (`westpac.taleo.net`, internal section `group_internal`, 2026 build); Westpac NZ on Workday. Background checks by First Advantage. Possible recorded video or phone interview. | External careers portal (Taleo). **Internal: `group_internal` section / Internal Careers site**. Talent Community. | SAFe vocabulary: "Release Train", "RT guardrails", "CPO", "squad", "acceptance criteria", "Definition of Done", "coaching other Product Owners", "embedding risk and regulatory obligations"; UNITE simplification programme to 2029. |
| **NAB** | PageUp (client 410) behind `careers.nab.com.au`; Eightfold (`nab.eightfold.ai`) for international roles, strong match ≥ 4.0. | External: careers.nab.com.au. **Internal: same PageUp, employee auto sign-in**. | Product Owner ads (e.g. Deposits; Home Owners & General Insurance, October 2026): "digital roadmap", "digital sales targets"; role grades like "Senior Consultant, Product Owner". |
| **ANZ** | SAP SuccessFactors (`career10.successfactors.com`, company `anzbanking`). Historic Taleo. HireVue reported for graduates (third-party). | careers.anz.com. Internal channel not confirmed (some roles posted as 12-month secondments). | "Agile Delivery Lead Practice", "Jira standards", "velocity, cycle time and health checks", "psychological safety", "showcases", "production readiness", "ANZ 2030 Strategy", P&L drivers. |
| **Macquarie** | Avature (inferred: URL patterns plus `sandboxmgl.avature.net`). PDF or Word < 20 MB. | recruitment.macquarie.com | Builder PO: APIs, event-driven architecture, automation, "AI agents or LLM-powered workflows"; "rather than solely managing product roadmaps". |
| **AMP / AMP Bank** | Oracle Recruiting Cloud (Oracle HCM Candidate Experience link on careers page). | amp.com.au/about-amp/careers → Oracle | Digital bank build (AMP Bank GO); AI Product Owner roles advertised (Glassdoor/Indeed, 2026). |
| **ING Australia** | Workday (`ing.wd3.myworkdayjobs.com/ICSGBLCOR`) behind Radancy careers.ing.com. | careers.ing.com → Workday | "Customer Journey Expert / Product Manager"; "Agile delivery", "basic SQL", cross-functional marketing and analytics. |
| **Bendigo & Adelaide** | SAP SuccessFactors (careers.bendigobank.com.au). | External: SuccessFactors. Internal: People Hub. | Technical PO roles: "Agile principles, backlog management, and roadmap development"; AML/CTF, KYC, sanctions platforms; security. |
| **Up** | Not confirmed (Ferocia careers page). | up.com.au/careers → Ferocia | Tech-company culture; small number of roles. |
| **Judo** | SmartRecruiters (third-party claim, Low). | Judo careers, Seek, LinkedIn | Business-banking specialist. |
| **Revolut Australia** | In-house; ATS not confirmed. Official channels only. | revolut.com/careers | PO roles "directly manage Engineering, Operations, and Design team members"; multi-stage interviews including problem-solving and product-sense cases (Glassdoor, candidate-reported). |
| **Beem (AP+)** | Possibly Workable (tracker, Low). | auspayplus.com.au careers; Seek; LinkedIn | Payments (eftpos, BPAY, NPP); AP+ often "not partnering with recruitment agencies". |

---

## 4. Keyword bank

Frequency marks: **[A]** appeared in 75% or more of the 16 full-text ads; **[B]** 40–74%; **[C]** 15–39%; **[D]** under 15% or only in supplementary ads; **[W]** recurring in Westpac partial ads. Use only the terms she can evidence.

**Product Owner / Product Manager**

- **[A]** stakeholder management; customer outcomes; business outcomes; delivery; risk (risks and controls)
- **[B]** prioritisation; data-led / data-driven decisions; financial services / banking; end-to-end; commercial (P&L drivers, business case); dependencies
- **[B/C]** product roadmap; product strategy; product discovery; customer experience / NPS; compliance; regulatory change; governance
- **[C]** product backlog; backlog management; agile; squad; crew (CBA); continuous improvement; metrics / KPIs / OKRs; experimentation / test-and-learn
- **[W]** Release Train; Chief Product Owner; acceptance criteria; Definition of Done; epics, features and stories; sprint; value-based prioritisation; "embedding risk and regulatory obligations"
- **[D]** Jira; Scrum; SAFe; AI literacy / responsible AI; agentic AI; open banking; straight-through processing; SQL; APIs; product lifecycle management; pricing; CSPO / PSPO / SAFe POPM

**People Leader / Team Manager**

- **[B/C]** coach and mentor; capability development; high-performing team; psychological safety / culture; executive stakeholder engagement
- **[D]** people leadership; direct reports; performance management; engagement; recruitment and onboarding; wellbeing; inclusion; workforce planning; succession

*(People-leadership vocabulary was thin in the sample because few people-manager-only roles were open in the bank feeds that week. Treat it as Low-confidence frequency and take terms from each specific ad.)*

**Delivery Lead / Project / Change Manager**

- **[A]** delivery; stakeholders; risk
- **[B]** dependencies; governance; end-to-end; prioritisation
- **[C]** agile frameworks; delivery plans and milestones; risks, issues and dependencies (RAID); change management / adoption; continuous improvement; coaching delivery teams
- **[D]** Jira standards; velocity; cycle time; health checks; showcases; ceremonies; production readiness; deployment planning; scaled agile; value streams; certification in Change / Project / Agile (e.g. Prosci, PMP, PRINCE2, SAFe)

**Banking context terms (use only where true)**

- Operational resilience; critical operations; CPS 230; service-provider management
- Scams and fraud; financial crime; AML/CTF; KYC
- Customer outcomes; vulnerable customers; DDO / target market determinations
- Regulatory remediation; controls testing; complaints reduction; AI adoption / responsible AI

---

## 5. Recommended CV template

### 5.1 Section-by-section skeleton (plain text)

```
[FULL NAME]
[Suburb, State] | [Mobile] | [Email] | linkedin.com/in/[handle] | Australian citizen
(Body text, not the Word header. Single column. 10.5–11pt standard font. DOCX.)

CAREER SUMMARY   (60–100 words; rewrite per role family)
- Line 1: target identity + domain. ("Senior Product Owner and people leader with
  deep retail-banking experience across [payments / lending / operations].")
- Line 2: scope proof. (teams led, squads/backlogs owned, programmes, budgets)
- Line 3: two headline outcomes with numbers.
- Line 4: what you bring next, in the ad's language. No "years of experience" count.

KEY SKILLS   (12–18 items, 2–3 lines, comma- or pipe-separated, no graphics)
- Mirror the ad's required items literally (e.g. "Product backlog management",
  "Agile / Scrum / SAFe", "Stakeholder management", "Risk & controls",
  "People leadership", "Jira & Confluence", "Discovery & roadmapping").

PROFESSIONAL EXPERIENCE   (about 75% of the document)
[EMPLOYER NAME], [City] | [Mon YYYY] – Present
One-line framing: "[N] roles across [divisions]; promoted [N] times;
selected for [programme/secondment]."

  [Current Title] | [Employer short name] | [Mon YYYY] – Present
  Context line (1 sentence): team/crew/train, product, scale, regulatory context.
  • 3–5 achievement bullets (CAR, number in each, target keywords in context)

  [Previous Title] | [Employer short name] | [Mon YYYY] – [Mon YYYY]
  • 2–4 bullets

  [Older Title] | [Employer short name] | [Mon YYYY] – [Mon YYYY]
  • 1–3 bullets

  Earlier roles: [Title], [Title], [Title] (one line; optional single highlight;
  years optional — keep the employer start year in the heading above)

EDUCATION & CERTIFICATIONS   (no graduation years)
- [Degree], [Institution]
- [Certification full name (ACRONYM)], [Issuer], [year obtained optional — recent
  years help; old ones can be omitted]

PROFESSIONAL DEVELOPMENT / AI & TOOLS   (optional, 1–2 lines; shows recency)
- e.g. "Responsible AI for product teams (2025)", "Jira Align", approved GenAI tools

ADDITIONAL   (optional, 1 line)
- Industry memberships, internal awards, volunteering relevant to leadership

Referees available on request
```

**Length guide.** Page 1 covers the summary, skills and the current role plus most of the previous one. Page 2 covers the remaining detailed roles, earlier roles and education. A third page is internal-only or for senior roles where the ad asks for depth.

### 5.2 Worked example: laying out 20+ years at one employer

*All employer details, figures and programme names below are placeholders to be replaced with true values.*

```
PROFESSIONAL EXPERIENCE

[MAJOR AUSTRALIAN BANK], Sydney | Feb 2004 – Present
Seven roles across Retail Operations, Digital and Enterprise Change; promoted three
times; selected for the [Core Banking Modernisation] program in 2021.

Senior Product Owner, Home Lending Origination | [Bank] | Jul 2022 – Present
Own the backlog and roadmap for a 9-person cross-functional squad within a
SAFe Release Train delivering broker and digital lending journeys.
• Cut median time-to-conditional-approval from [8] to [3] days by re-prioritising
  the backlog around straight-through processing; [X]% of applications now
  auto-decisioned.
• Embedded CPS 230 critical-operation and control requirements into feature
  acceptance criteria, closing [N] audit actions with no rework at release.
• Led discovery with [N] brokers and lenders; shipped [feature] that lifted
  digital completion from [X]% to [Y]% in two quarters.
• Coach two Product Owners; chair quarterly PI planning inputs for the train.

Team Manager, Lending Operations | [Bank] | Mar 2018 – Jun 2022   (promoted)
Led 3 team leaders and [24] staff processing [N] applications per month.
• Reduced backlog-driven SLA breaches by [X]% through Kanban-style work
  visualisation and daily stand-ups, adopted across [N] teams.
• Raised engagement from [X] to [Y] (annual survey); [N] team members promoted.
• Business lead for UAT and change adoption on [platform] migration
  ([N] users, [N] processes).

Project Manager, Customer Remediation | [Bank] | Jan 2015 – Feb 2018   (secondment, then permanent)
• Delivered remediation for [N] customers ($[X]m) to ASIC-agreed timelines.

Earlier roles (2004–2014): Team Leader, Contact Centre; Senior Analyst, Process
Improvement; Customer Service Officer.
```

Why this layout works:

- Each role is a separate dated record that parsers and autofill can map.
- "(promoted)" and "(secondment, then permanent)" make the moves legible.
- The current and previous roles carry the PO, agile, risk and people-leader vocabulary where recency-weighted matchers look.
- The employer start year stays truthful.
- The earlier roles prove the ladder without spending space or emphasising age.

---

## 6. Before/after bullet rewrites

*Numbers in brackets are placeholders. Use real figures or an honest range ("about", "more than").*

1. **PO backlog**
   - *Before:* "Responsible for managing the product backlog and working with the development team."
   - *After:* "Owned the prioritised backlog for a [9]-person squad delivering [digital deposits onboarding]; re-sequenced [40] epics around customer value and risk, lifting release predictability from [60]% to [90]% of committed features over four PIs."
2. **Stakeholders and roadmap**
   - *Before:* "Liaised with stakeholders to define requirements."
   - *After:* "Aligned Risk, Legal, Operations and Technology on a 12-month roadmap for [business transaction accounts], securing executive sign-off in [3] weeks and avoiding [an estimated $X] of duplicated build across two crews."
3. **Regulatory and risk delivery**
   - *Before:* "Worked on regulatory projects."
   - *After:* "Translated [CPS 230 / scams-prevention / DDO] obligations into [N] backlog features with control-linked acceptance criteria; delivered on the regulatory date with zero high-rated audit findings."
4. **Customer outcome**
   - *Before:* "Improved customer experience."
   - *After:* "Led discovery with [30] customers and frontline staff; simplified the [hardship] journey from [7] to [3] steps, cutting related complaints [X]% and lifting journey NPS from [+5] to [+21] in six months."
5. **People leadership**
   - *Before:* "Managed a team of staff and conducted performance reviews."
   - *After:* "Led [3] team leaders and [24] staff; rebuilt the coaching cadence and capability plan, raising engagement from [62] to [78] and promoting [5] people internally in two years."
6. **Delivery Lead and dependencies**
   - *Before:* "Coordinated project delivery across teams."
   - *After:* "Ran delivery across [4] squads and [2] vendors for [platform migration]; introduced a shared RAID and dependency board in Jira, cutting blocked work items [X]% and landing go-live [2] weeks early."
7. **Change management**
   - *Before:* "Supported change management activities."
   - *After:* "Planned and led adoption of [new origination system] for [600] users across [N] sites; [95]% trained before cut-over and processing productivity back to baseline within [3] weeks."
8. **Efficiency and AI adoption**
   - *Before:* "Helped implement automation."
   - *After:* "Product-owned an approved GenAI summarisation pilot for [complaints case notes] with Risk and Privacy sign-off; reduced handling time [X]% for [N] agents and wrote the controls pattern reused by [2] other teams."

---

## 7. Checklists

### (a) ATS- and AI-safe formatting

- [ ] DOCX for every bank portal (essential for ANZ and Bendigo on SuccessFactors); text-based PDF only for human email or LinkedIn
- [ ] Single column; no tables, text boxes, icons, photos, skill bars or charts
- [ ] Name and contact details in the body, not the Word header
- [ ] Standard headings: Career Summary, Key Skills, Professional Experience, Education & Certifications
- [ ] Every role as its own line: Title | Employer | Mon YYYY – Mon YYYY, in reverse-chronological order
- [ ] Standard fonts (Calibri, Arial or Aptos), 10.5–11pt; bullets as simple round characters
- [ ] Each *required* qualification in the ad appears literally at least once, ideally in the summary or skills and again in a recent role
- [ ] Australian spelling throughout; acronyms spelled out once (e.g. "Scaled Agile Framework (SAFe)")
- [ ] File name: `Firstname-Lastname-CV-Senior-Product-Owner.docx`
- [ ] Dates and titles identical to the form fields you fill in Workday, Taleo or SuccessFactors
- [ ] No graduation years; no date of birth; no photo; no full street address
- [ ] Read it aloud once: cut any sentence that could appear in anyone's CV

### (b) Internal-application version

- [ ] Apply through the **internal** portal (CBA: Sidekick; Westpac: internal careers / `group_internal`; NAB: PageUp employee sign-in; Bendigo: People Hub)
- [ ] Tell the current manager before or when applying; frame it as wanting breadth or scope
- [ ] Use the target team's vocabulary (e.g. CBA "crew / Product Lead"; Westpac "Release Train / CPO"); gloss programme code names once
- [ ] Include internal proof points: programme names, executive sponsors, awards, ratings if accurate and culturally acceptable
- [ ] Line up internal referees: current manager plus a senior stakeholder from another division
- [ ] Message or meet the hiring manager (a short note with two or three relevant outcomes) where policy allows
- [ ] Three pages is acceptable if useful; page 1 must still stand alone
- [ ] Keep LinkedIn Open to Work at "Recruiters only" or off; Seek on Limited or Standard

### (c) External-application version

- [ ] Two pages (three as a hard ceiling); remove internal jargon or translate it into market terms
- [ ] Tailor the summary and skills to each ad's required qualifications; reorder bullets so the matching evidence sits in the current role
- [ ] Apply on the bank's own portal where the ad points there; use Easy Apply mainly for fintechs
- [ ] "Australian citizen" in the contact line; knockout answers match the CV
- [ ] "Referees available on request"; prepare two former-manager referees and expect ABA conduct-check consent at offer stage
- [ ] Short cover letter only where requested: three paragraphs, specific to the bank's strategy (e.g. Westpac UNITE, ANZ 2030, CBA's domain model)
- [ ] For Revolut and fintechs, emphasise hands-on product decisions and direct management of cross-functional staff

### (d) LinkedIn and Seek alignment

- [ ] Same titles, employer name and dates on the CV, LinkedIn and Seek
- [ ] LinkedIn headline: target title, banking domain, two proof themes and tools; no "seeking" language
- [ ] LinkedIn About in first person, 4 short paragraphs, 2–3 quantified outcomes, human voice (different words from the CV)
- [ ] LinkedIn Experience: multiple positions under one company entry; 2–3 bullets for recent roles
- [ ] LinkedIn Skills: Section 4 terms, top three pinned; certifications with full names
- [ ] Open to Work: "Recruiters only" (internal phase); add target titles, locations and work type
- [ ] Seek: visibility Limited or Standard while searching internally; Standard when going external; Public only if discretion no longer matters
- [ ] Seek: right-to-work field completed and verified via SEEK Pass; DOCX uploaded as the default resume; skills match the CV; short personal summary
- [ ] Recent activity: a few considered posts or comments on product, agile or banking topics improve recency signals (low-cost; Low confidence on ranking effect)

---

## 8. Knowledge gaps and what could not be verified

1. **AI ranking layers per bank.** I could confirm which ATS each bank runs, but not whether CBA or ING have HiredScore switched on, whether NAB uses PageUp's AI Skills Matching or summaries, whether ANZ or Bendigo use SAP's AI matching, or whether Westpac's Taleo has any AI layer. Vendor capabilities are documented; bank configurations are not public.
2. **Westpac's external Australian portal.** The internal Taleo section is current (2026 build) and Westpac NZ is on Workday. I did not directly confirm whether external Australian applications still go through Taleo or a newer system. Westpac ads in my sample came through aggregators.
3. **The `careers.nab.com.au` front end.** It sits in front of PageUp, but I could not identify the vendor.
4. **Macquarie (Avature), Judo (SmartRecruiters) and Beem/AP+ (Workable)** are inferred from URL patterns or third-party trackers. Revolut's and Up's systems are unknown.
5. **The Seek listing sample was blocked** (HTTP 403 to automated access), so I could not sample Seek listings directly. Keyword frequencies come from 16 bank-direct ads at CBA, ANZ and ING, plus partial text for Westpac, NAB, Macquarie and Bendigo. People-manager-only roles were under-represented that week. A manual Seek review of 20–30 current ads would strengthen Section 4.
6. **Certification demand in Australia.** No Australian data quantifies CSPO, PSPO or POPM requests. The two mentions in my sample were "advantageous" only.
7. **Internal-fill rates.** No 2025–26 figure from any big-four bank. Westpac reports only "up 5% from FY23". CBA's internal-mobility article dates from about 2021.
8. **Internal application screening specifics** (whether internal applicants are graded the same way, whether managers must approve applications, notice-period rules) are intranet-only.
9. **AI-CV detection.** No Australian survey of recruiters measured detection accuracy. The most-cited "can spot AI" figures are UK and US. I found no evidence of any ATS flagging AI authorship.
10. **Effect of LLM screening on older candidates.** The studies conflict, and none is Australian-bank-specific.
11. **Primary-source rendering failures.** SAP's help page on parsing formats, the DEWR résumé PDF, the Robert Walters AU blog and LinkedIn's Hiring Assistant news pages were relied on through indexed text or secondary reports because direct fetches failed. Wording is as indexed; the confidence levels above reflect this.
12. **Undated pages.** The Hays resume guidance, Westpac's recruitment-process page and AMP's careers page carry no publication date. CBA's career-pathways article (about 2021) and ANZ's Taleo guide pre-date the January 2025 window and are flagged where used.

---

## Sources

1. "Search for Jobs – CommBank Careers" (Workday feed incl. REQ268169, REQ267762, REQ268819, REQ268478, REQ267853), Commonwealth Bank, accessed 20 Nov 2026, https://cba.wd3.myworkdayjobs.com/CommBank_Careers
2. "Career pathways at CommBank", Commonwealth Bank, c. 2021 (older), https://www.commbank.com.au/articles/careers/career-pathways-at-commbank.html
3. "Our Graduate and Intern Programs" (Sidekick Career Hub), Commonwealth Bank, 2026 (search snapshot), https://www.commbank.com.au/about-us/careers/graduate-intern-programs.html
4. "What to expect from the recruitment process", Westpac, undated, accessed 20 Nov 2026, https://www.westpac.com.au/about-westpac/careers/how-to-apply/recruitment-process/
5. "Careers@WestpacGroup – Job Search (group_internal)", Westpac / Oracle Taleo, 2026 build, https://westpac.taleo.net/careersection/group_internal/jobsearch.ftl
6. "Login – User Sign In", Westpac / Oracle Taleo, search snapshot 2026, https://westpac.taleo.net/careersection/iam/accessmanagement/login.jsf
7. "Westpac Careers" (NZ Workday), Westpac New Zealand, 2026, https://westpacnz.wd105.myworkdayjobs.com/en-US/Westpac_Careers
8. Westpac Banking Corporation 2025 Annual Report (Form 6-K exhibit), Westpac / SEC, Nov 2025, https://www.sec.gov/Archives/edgar/data/719245/000110465925105894/webnf-20250930xex15d3.htm
9. "UNITE Update", Westpac, 26 Mar 2026, https://www.westpac.com.au/content/dam/public/wbc/documents/pdf/aw/ic/wbc-UNITE-presentation-2026.pdf
10. "Product Owner, Pricing Experience — Westpac Group", freehire (aggregator), 12 Nov 2026, https://freehire.me/jobs/product-owner-pricing-experience-westpac-group-wpz42zij
11. "Lead Product Owner — Westpac Group", freehire (aggregator), Nov 2026, https://freehire.me/jobs/lead-product-owner-westpac-group-w7hjhdc3
12. "Product Owner — Westpac Group", freehire (aggregator), Nov 2026, https://freehire.me/jobs/product-owner-westpac-group-yf6ucvbi
13. "Careers", National Australia Bank, accessed 20 Nov 2026, https://www.nab.com.au/about-us/careers
14. "NAB Careers – Jobs listing", National Australia Bank, accessed 20 Nov 2026, https://careers.nab.com.au/en/listing/
15. "Applicant sign in – National Australia Bank", PageUp, accessed 20 Nov 2026, https://secure.dc2.pageuppeople.com/apply/410/aaw/applicationform/default.asp
16. "NAB – Recent Jobs", PageUp, search snapshot 2026, https://careers.pageuppeople.com/410/fb/en
17. "Careers at National Australia Bank" (Eightfold site and API), NAB / Eightfold AI, accessed 20 Nov 2026, https://nab.eightfold.ai/careers
18. "Product Owner Deposits – VIC – Melbourne CBD" (Job 809364), NAB, Oct 2026 (search snapshot), https://careers.nab.com.au/jobs/product-owner-deposits-vic-melbourne-cbd-vic-australia
19. "ANZ Jobs List" (and job ads: Agile Delivery Lead ×2, Change Lead, Senior Lead – Enterprise Change, Senior Project Manager, Senior Product Manager), ANZ / SAP SuccessFactors, 15–19 Nov 2026, https://careers.anz.com/go/ANZ-Jobs-List/4739210/
20. "Quick Reference Guide" (Taleo, historical), ANZ, undated (older), https://www.anz.com/resources/f/e/fe6e420047cc7d3bb57db7e47d444d82/Quick-Reference-Guide.pdf
21. "How to Pass the ANZ Digital Interview 2026/27", GraduatesFirst (low-grade), 2026, https://www.graduatesfirst.com/anz-job-interviews
22. "Engineering Product Owner – Digital Channels" (21456), Macquarie Group, 4 Nov 2026, https://recruitment.macquarie.com/en_US/careers/JobDetail/Engineering-Product-Owner-Digital-Channels/21456
23. "Registering to" (resume PDF/Word < 20 MB), Macquarie Group, 2026 (search snapshot), https://recruitment.macquarie.com/en_US/careers/RegistrationMethods
24. "Join the Macquarie Talent Community", Avature sandbox, 2026, https://sandboxmgl.avature.net/internal2/wizard
25. "Careers", AMP, accessed 20 Nov 2026, https://www.amp.com.au/about-amp/careers
26. "ASIC Reference Checking and Information Sharing Protocol", AMP, accessed 20 Nov 2026, https://www.amp.com.au/about-amp/careers/asic-reference-checking-and-information-sharing-protocol
27. "ING Careers" (Workday ICSGBLCOR; Product Owner – Onboarding and Engagement REQ-10124137 and others), ING, 20 Nov 2026, https://ing.wd3.myworkdayjobs.com/en-US/ICSGBLCOR
28. "Product Owner – Onboarding and Engagement", ING (careers.ing.com / Radancy), Nov 2026, https://careers.ing.com/en/job/sydney/product-owner-onboarding-and-engagement/3121/46810241728
29. "Careers – Bendigo and Adelaide Bank", Bendigo Bank / SAP SuccessFactors, accessed 20 Nov 2026, https://careers.bendigobank.com.au/
30. "Careers at Up", Up / Ferocia, 2026, https://up.com.au/careers/
31. "Judo Bank Careers: 22 Open Jobs (Nov 2026)", Scoutify (aggregator, low-grade), Nov 2026, https://scoutify.com/companies/judo-bank/
32. "Product Owner (Technical)", Revolut, 2026 (search snapshot), https://www.revolut.com/en-US/careers/position/product-owner-technical-5beb1f80-446c-41b8-b59c-c34bd557bc7b/
33. "Beem" company page (AP+ careers pointer), LinkedIn, 2026, https://www.linkedin.com/company/beemit/
34. "Reference: Candidate Grades", Workday HiredScore documentation, accessed 20 Nov 2026, https://doc.workday.com/hiredscore/en-us/workday-hiredscore/recruiter-productivity-/reference--candidate-grades.html
35. "Responsible AI and Bias Mitigation for HiredScore Spotlight", Workday, 2026, https://www.workday.com/en-us/legal/responsible-ai-and-bias-mitigation.html
36. "Working with Resume Parsing", SAP Help Portal, accessed via index 20 Nov 2026, https://help.sap.com/docs/successfactors-recruiting/setting-up-and-maintaining-sap-successfactors-recruiting/working-with-resume-parsing
37. "Candidate Profile in SAP SuccessFactors", SAP Help Portal, accessed via index 20 Nov 2026, https://help.sap.com/docs/successfactors-recruiting/setting-up-and-maintaining-sap-successfactors-recruiting/candidate-profile-in-sap-successfactors
38. "Resume Parser – Technical Specifications", Textkernel, 2026, https://developer.textkernel.com/tx-platform/v10/resume-parser/overview/specs/
39. "Searching for Candidates" (Taleo Enterprise 21B), Oracle, https://docs.oracle.com/en/cloud/saas/taleo-enterprise/21b/otfru/searching-for-candidates.html
40. "Candidate Management" (Taleo Enterprise 21B), Oracle, https://docs.oracle.com/en/cloud/saas/taleo-enterprise/21b/otrec/candidate-management.html
41. "AI-powered talent matching: The tech behind smarter and fairer hiring", Eightfold AI, 13 Aug 2025, https://eightfold.ai/engineering-blog/ai-powered-talent-matching-the-tech-behind-smarter-and-fairer-hiring/
42. "PageUp Unveils New AI Suite", PageUp, 16 Sep 2025, https://www.pageuppeople.com/news/paige-ai-launch/
43. "PageUp and Sapia.ai embed intelligent AI interviewing…", GlobeNewswire, 26 Aug 2026, https://www.globenewswire.com/news-release/2026/08/26/3351491/0/en/pageup-and-sapia-ai-embed-intelligent-ai-interviewing-directly-into-enterprise-hiring-workflows.html
44. "Find the right talent with AI-powered search and match", SEEK Employer, 2026, https://au.employer.seek.com/products/article/right-talent-with-ai-powered-search-and-match
45. "Enhanced discovery for candidates", SEEK Employer, c. 2025, https://au.employer.seek.com/products/article/enhanced-discovery-for-candidates
46. "Talent Search", SEEK Employer, 2026, https://au.employer.seek.com/products/talentsearch
47. "Candidate Matches, Basic Talent Search & Premium Talent Search Terms", SEEK, updated 20 Jul 2026, https://au.employer.seek.com/support/talentsearchofferterms
48. "Profile Visibility", SEEK, accessed 20 Nov 2026, https://au.seek.com/profile-privacy
49. "How to make a resumé: Step-by-step guide with examples", SEEK, updated 30 Sep 2026, https://au.seek.com/career-advice/article/how-to-make-a-resume
50. "How long should a resumé be?", SEEK, mid-2026, https://au.seek.com/career-advice/article/how-long-should-a-resume-be
51. "Let recruiters know you're Open to Work", LinkedIn Help, updated about Nov 2026, https://www.linkedin.com/help/linkedin/answer/a507508/let-recruiters-know-you-re-open-to-work
52. "AI-Assisted Messages in Recruiter", LinkedIn Help, 2025–26, https://www.linkedin.com/help/recruiter/answer/a1445743
53. "LinkedIn's first agent, Hiring Assistant, expands availability globally after first year", HR Brew, 3 Sep 2025, https://www.hr-brew.com/stories/2025/09/03/linkedin-s-first-agent-hiring-assistant-expands-availability-globally-after-first-year
54. "LinkedIn Launches First-Ever AI Agent For Recruiters… Across Australia", Tech Business News, 1 Oct 2025, https://www.techbusinessnews.com.au/news/linkedin-launches-first-ever-ai-agent-for-recruiters-to-enhance-hiring-across-australia/
55. "LinkedIn Launches Hiring Assistant 2…", DHRmap, Sep–Oct 2026, https://www.dhrmap.com/news/linkedin-launches-hiring-assistant-2
56. "LinkedIn Launches AI Job Search Tool For Premium Users First", Forbes, 2 Jun 2025, https://www.forbes.com/sites/torconstantino/2025/06/02/linkedin-launches-ai-job-search-tool-for-premium-users/
57. "How to Write a Resume Australia – Template & Tips", Hays Australia, undated, accessed 20 Nov 2026, https://www.hays.com.au/career-advice/resumes-cover-letters/how-to-write-a-resume
58. "Recruitment battle of the bots", Hays Australia, c. 2025, https://www.hays.com.au/blog/insights/battle-of-bots
59. "5 ways businesses are responding to the rise of AI-generated job applications", Australian HR Institute, 3 Sep 2025, https://www.ahri.com.au/articles/responding-to-ai-generated-applications
60. "AI use grows in Australian job hunting but honesty concerns rise", IT Brief Australia (people2people survey), 16 Sep 2025, https://itbrief.com.au/story/ai-use-grows-in-australian-job-hunting-but-honesty-concerns-rise
61. "Recruiters grapple with rise of AI-written CVs", HRD Australia, 10 Sep 2025, https://www.hcamag.com/au/specialisation/recruitment/recruiters-grapple-with-rise-of-ai-written-cvs/549105
62. "How to stand out in job applications in the age of AI", Robert Walters Australia, 7 Aug 2025 (via index), https://www.robertwalters.com.au/insights/career-advice/blog/how-to-stand-out-in-age-of-ai.html
63. "Older and Younger Workers: What Do Employers Think?", Australian HR Institute & Australian Human Rights Commission, Jul 2025, https://www.ahri.com.au/wp-content/uploads/Older-Younger-Workers-Report-2025-FINAL.pdf
64. "Algorithm-facilitated discrimination: a socio-legal study of the use by employers of AI hiring systems", N. Sheard, Journal of Law and Society 52(2), 2025, https://onlinelibrary.wiley.com/doi/10.1111/jols.12535
65. "Minimal but Conditional: Auditing Demographic Bias in LLM Résumé Evaluation", Analytics (MDPI), 2026, https://www.mdpi.com/2813-2203/5/3/30
66. "LLMs Resistance to Discrimination: A Study of Prompt Influence in AI-Based Resume Screening", Springer, c. 2026, https://link.springer.com/chapter/10.1007/978-3-032-16764-4_13
67. "Age" (discrimination law), Queensland Human Rights Commission, current, https://www.qhrc.qld.gov.au/your-rights/discrimination-law/age
68. "Industry Protocol – Conduct Background Check" v14.0, Australian Banking Association, 30 Sep 2025 (hosted Mar 2026), https://www.ausbanking.org.au/wp-content/uploads/2026/03/Final-ABA-Industry-Protocol-Conduct_Background_Check-250930.pdf
69. "Prudential Standard CPS 230 Operational Risk Management", APRA, effective 1 Jul 2025, https://www.apra.gov.au/system/files/2023-07/Prudential%20Standard%20CPS%20230%20Operational%20Risk%20Management%20-%20clean.pdf
70. "Scams Prevention Framework", ACCC, 2026, https://www.accc.gov.au/about-us/scams-prevention-framework
71. "ANZ Bank reveals plans to cut about 3,500 jobs by next September", ABC News, 9 Sep 2025, https://www.abc.net.au/news/2025-09-09/anz-to-cut-jobs-3500-to-go-by-sept-2026/105751484
72. "Tech workers face job cuts at ANZ, NAB, Bendigo Bank", ACS Information Age, 2025, https://ia.acs.org.au/article/2025/tech-workers-face-job-cuts-at-anz--nab.html
73. "Résumé Tips and Example Résumé", Department of Employment and Workplace Relations, undated (via index), https://www.dewr.gov.au/download/8284/resume-tips-and-example-resume/12432/resume-tips-and-example-resume/pdf
74. "Résumé guide and checklist", University of Queensland Employability, undated, https://employability.uq.edu.au/files/176803/Resume%20Fact%20Sheet%20&%20Example.pdf
75. "Product Owner Certifications to Consider", Indeed Australia (low-grade), 2025–26, https://au.indeed.com/career-advice/career-development/product-owner-certifications
76. "Executive Manager Operations Technology — Commonwealth Bank" (crew/squad/chapter wording), freehire (aggregator), 2026, https://freehire.me/jobs/executive-manager-operations-technology-commonwealth-bank-aog2rlyy
