# Review: Hannah Okoye's résumé against the Lantern Bank Product Owner, Card Disputes ad

Reviewed 21 November 2026. Files: `old-resume.md`, `facts.md`, `ad.md`. This is a review only:
nothing in the résumé has been changed. Every proposed line uses facts from `facts.md` and
nothing else. Gaps are written as `[questions in square brackets]`.

**The short version.** Do not send this résumé as it stands. Four of its eight bullets claim
more than Hannah confirmed, one prints a figure she has said must not leave Kestrel Bank (and
states it as a saving, which it is not), and the layout tells a reader she has been a Product
Owner since 2009. Her real case for this job is strong and mostly absent from the page: she
owns a card disputes backlog, she has a prioritisation decision backed by data with a measured
result, and she ran the operation the product serves. She meets 3 of the ad's 5 required items,
partly meets 1, and does not meet 1 (card scheme mandate changes), which no wording can fix.

The defaults applied here come from research on Australian bank hiring in late 2026, which is
the market this ad is in.

## 1. Cold read

Read once, as the hiring manager at Lantern Bank would, before checking any rule. These are the
lines I stumbled on.

| Line | Why it stops a reader |
| --- | --- |
| "Hannah Okoye — Curriculum Vitae" | The label adds nothing and can be parsed as part of her name. |
| "DOB: 14 June 1986 \| Married" | No employer needs either. Both invite a judgement the résumé should not prompt. |
| "Results-driven operations and product professional with 15+ years of experience seeking a challenging Product Owner role where I can leverage my skills." | It could sit on anyone's résumé. It says what she wants, where a reader wants to know what she is. "15+ years" beside "product professional" suggests 15 years in product; she moved into product in August 2024. |
| "Stakeholders, Agile, Jira, Risk, Backlogs, Chargebacks, Leadership, Communication" | Eight nouns. None says what she can do, and nothing below shows "Risk" or "Communication" happening. |
| "Kestrel Bank \| 2009 – Present" followed by "Product Owner / Operations Manager / Team Leader" | Which title is current, and when did each start? As written it reads as one job held for 17 years. I cannot tell which bullets belong to which role. |
| "Lead the disputes squad and own the squad backlog." | "Lead" beside past-tense bullets reads as a typo for "Led" or as an instruction. It is also the line a Lantern interviewer will test first, and it is not what she does (section 3). |
| "Delivered the fraud-alert SMS rollout for the bank." | A big claim with no detail: what was her part? |
| "Reduced manual triage by 30% through auto-categorisation." and "Reduced handling time from 18 minutes to 14 minutes." | Two results with no account of what she did to cause either. The second is real and is her best story; here it has no cause attached. |
| "Responsible for managing a team of 31 staff." | A duty, and I cannot tell whether she manages 31 people now, as a Product Owner. |
| "Restructured rosters, improving efficiency significantly." | "Significantly" with no number reads as a result nobody measured. |
| "Saved the bank $3.2 million a year in chargeback losses." | The largest claim on the page, with nothing about how. A reader either disbelieves it or asks about it at interview. |
| "## Education" with nothing under it | An empty heading draws attention to what is not there. |
| "Jo Example, Head of Payments Product, Kestrel Bank, 0400 111 222" | A named referee at her current employer, with a mobile number, on an application to another bank. |

After the cold read I know she works in disputes at Kestrel Bank and wants a Product Owner job.
I do not know what she owns, what makes her different from another Product Owner, or which
claims I could rely on.

## 2. Section by section

### Name and contact line

**Job:** how to reach her and her right to work. **Test:** is every item plain text, and is
anything personal there that no employer needs? **Fails.** It carries a street address, a date
of birth and marital status, and it omits the two things worth having: her LinkedIn address and
"Australian citizen", which bank application systems filter on.

Proposed:

```
# HANNAH OKOYE

Brisbane, QLD | 0400 000 000 | hannah.okoye@example.com | linkedin.com/in/hannah-okoye-example | Australian citizen
```

Check that the LinkedIn address resolves before it goes on the page, and that the titles and
dates on the profile match the résumé.

### Professional summary

**Job:** who she is in the target role's terms, what makes her different, proof she delivers
now. **Test:** could it sit on someone else's résumé? **Fails.** There is no summary; there is a
career objective, which states what she wants. It also contains a count of years and
"results-driven", both of which the lint rejects.

Proposed (100 words), replacing the "Career objective" section:

> As a Product Owner at Kestrel Bank I own the backlog for Beacon, the case-management tool for
> card payment disputes that about 140 staff use. I came to product from disputes operations,
> where I managed a 31-person team handling about 2,400 disputes a month. I moved because I was
> tired of working around the tool and wanted to fix it. I put a change that auto-fills merchant
> details ahead of a dashboard managers wanted, after case data showed staff retyping them on
> about 70% of cases. Average handling time fell from 18 minutes to 14 in the quarter after
> release.

Each statement is carried by a role below. The third sentence is her own words and is the line
that makes the paragraph hers, so it should survive any later cut. The first person is this
skill's default; if Hannah prefers an implied subject throughout, that is her call.

### Key skills

**Job:** things she can do. **Test:** is each item an ability, and which line below shows it?
**Fails.** All eight items are nouns in one unlabelled line. "Risk" and "Communication" have
nothing behind them. Confluence and Power BI, both of which she uses and one of which the ad
names, are missing.

Proposed:

```
Product ownership: prioritising a backlog using case data; writing user stories and acceptance criteria; coordinating user acceptance testing across releases
Card disputes operations: managing disputes teams across 2 sites; working within Visa and Mastercard chargeback timeframes; cutting ageing disputes with daily reporting
People: leading team leaders and frontline staff; coaching disputes officers into team leader roles; writing process and training for 140 staff
Tools: Jira, Confluence, Power BI
```

Every item is shown by a line in the experience section proposed below. "Risk" is left off
until there is a fact behind it (see question 2 in section 7).

### Professional experience: employer heading

**Job:** where she has worked and how she moved. **Test:** are the start date and each move true
and visible? **Fails.** "2009 – Present" hides the month, and three titles joined by slashes
hide two promotions and the move into product. Two of her five roles are missing altogether.
The heading "Employment" is not one a parser reliably maps to a field; use "Professional
experience".

Proposed:

```
## Professional experience

### Kestrel Bank, Brisbane | Feb 2009 – Present
```

> I started as a customer service officer, moved into disputes in 2012 and was promoted twice,
> to team leader and then to operations manager. I moved into product in 2024 because I was
> tired of working around the disputes tool and wanted to fix it.

### Current role

**Job:** exactly what she owns, how the work runs, and what happened because of her. **Test:**
is each bullet one thing that happened, with a detail only she would know? **Fails.** There is
no separate current role. Of the bullets that belong to it, one overstates her scope, two
overstate her part, one states a forecast as a result, and the one true result has no cause.

Proposed:

```
#### Product Owner, Disputes Workflow | Kestrel Bank | Aug 2024 – Present
```

> I own the backlog for Beacon, Kestrel's internal case-management tool for card payment
> disputes, which about 140 staff use. It is one of 2 backlogs in a 10-person agile squad that
> works in 2-week sprints, and I report to the Head of Payments Product. I write the user
> stories and acceptance criteria.

- Moved a change that auto-fills merchant details ahead of a dashboard that managers had asked
  for, after case data showed staff were retyping merchant details on about 70% of cases.
  Average handling time fell from 18 minutes to 14 minutes in the quarter after release.
- Supported the bank's rollout of a new fraud-alert SMS by writing the disputes team's process
  and the training for 140 staff.
- Coordinated user acceptance testing for 4 releases, which the QA team ran.
- `[What was your part in auto-categorisation of new disputes: is it on the Beacon backlog, and did you write the business case or the stories?]`

The first bullet is the strongest thing she has for this ad: a prioritisation decision, the
data behind it, who she said no to, and a measured result. It goes first. If the answer to the
bracketed question gives her a part in auto-categorisation, the bullet has to say the work is
in build and the 30% is the business case's forecast, for example: "…now in build; the business
case forecasts a 30% cut in manual triage." If she had no part in it, the bullet comes out.

### Roles in the last 10 to 12 years

**Job:** the depth the summary claims. **Test:** does this role show something the summary says?
**Fails.** Operations Manager and Team Leader exist only as words in a slashed title, with
their bullets mixed into the Product Owner's. The ageing-disputes result and the coaching are
not on the page at all.

Proposed:

```
#### Operations Manager, Payments Disputes | Kestrel Bank | Mar 2020 – Aug 2024
```

> I managed payments disputes operations across 2 sites. 3 team leaders reported to me and the
> team was 31 staff in total, handling about 2,400 card disputes a month within Visa and
> Mastercard chargeback timeframes.

- Introduced a daily report of ageing disputes. Disputes older than 45 days fell from about 310
  to about 90 over 6 months.
- Restructured rosters across the 2 sites.

```
#### Team Leader, Disputes Operations | Kestrel Bank | Sep 2015 – Mar 2020
```

> I led a disputes operations team of 9 direct reports.

- Coached 2 disputes officers into team leader roles.

The rosters bullet carries scope and no result, because none was measured. The chargeback
timeframes clause is placed in the Operations Manager role on the assumption that it applies
there; question 4 in section 7 checks that.

### Earlier roles

**Job:** that the ladder exists. **Test:** would a reader miss this line if it were cut?
**Fails by omission.** Disputes Officer and Customer Service Officer are not on the résumé,
though the heading's 2009 start date implies them. The Disputes Officer role is 3 years of
hands-on card disputes work, which the ad requires.

Proposed, a title line each with no description:

```
#### Disputes Officer | Kestrel Bank | Jun 2012 – Sep 2015

#### Customer Service Officer | Kestrel Bank | Feb 2009 – Jun 2012
```

### Education and certifications

**Job:** qualifications actually held. **Test:** is there something to list? **Fails.** The
heading is empty. Hannah has no formal qualifications, so the Education heading comes out. She
does have dated learning from the last 3 years that this role cares about, which earns one line
under its own heading:

```
## Professional development

Product Fundamentals, Kestrel Bank internal course, completed 2025
```

It is an internal course and should be described as one. It is not a certification, and the ad
lists a certification as desirable, not required. The lint warns that "Professional
development" is not a standard parser heading; I would accept that warning, because filing an
internal course under "Education and certifications" suggests something she does not hold.

### Sections to remove

- **Career objective.** Replaced by the summary above.
- **Referees.** Remove the section and Jo's details. Australian bank applications do not print
  referees; they are supplied when asked for. Printing a current Kestrel manager's mobile on an
  external application also gives Lantern a way to call her employer before she has told them
  she is looking.

## 3. Overclaim check

Each line of the old résumé against `facts.md`. The first is the most serious.

| Résumé says | Hannah confirmed | Kind of problem | Fix |
| --- | --- | --- | --- |
| "Saved the bank $3.2 million a year in chargeback losses." | Card disputes **cost** Kestrel about $3.2 million a year in chargeback losses. The figure is internal only and she does not want it on anything that leaves Kestrel. | A figure whose noun changed (a cost written as a saving), and a confidential figure on an external document. | Delete the bullet. No saving was confirmed, so nothing replaces it. |
| "Lead the disputes squad and own the squad backlog." | She owns the Beacon backlog, one of 2 in a 10-person squad. She does not own the other backlog or the squad. | Scope: one backlog written as the squad's, and ownership of a backlog written as leading the squad. | "I own the backlog for Beacon… one of 2 backlogs in a 10-person agile squad." |
| "Delivered the fraud-alert SMS rollout for the bank." | She supported the rollout. Her part was the disputes team's process and the training for 140 staff. She did not lead or deliver it. | A stronger verb than confirmed. | "Supported the bank's rollout of a new fraud-alert SMS by writing the disputes team's process and the training for 140 staff." |
| "Reduced manual triage by 30% through auto-categorisation." | Auto-categorisation is in build and unreleased. The 30% is the business case's forecast. Nothing has been measured. | An expected outcome written as achieved. | Remove until her part is confirmed; then state it as in build and forecast. |
| "Managed user acceptance testing for 4 releases." | She coordinated it. The QA team ran the tests. | A stronger verb than confirmed. | "Coordinated user acceptance testing for 4 releases, which the QA team ran." |
| "Restructured rosters, improving efficiency significantly." | She restructured rosters across the 2 sites. No result was measured. | A result that was never measured. | "Restructured rosters across the 2 sites." |
| "Reduced handling time from 18 minutes to 14 minutes." | True figures: average handling time fell from 18 to 14 minutes in the quarter after the auto-fill change was released. | Not an overclaim, but it has lost its cause, its measure ("average") and its period. | The first bullet of the proposed current role. |
| "Responsible for managing a team of 31 staff." | 3 team leaders reported to her; 31 staff in total across 2 sites, as Operations Manager from March 2020 to August 2024. | Direct reports and total team merged; undated, so it reads as current. | The proposed Operations Manager scope paragraph. |
| "Kestrel Bank \| 2009 – Present" with "Product Owner / Operations Manager / Team Leader" | 5 roles, each with its own dates. Product Owner since August 2024. | The whole tenure presented as one role; a parser will record 17 years as a Product Owner. | One employer heading with each role dated beneath it. |
| "operations and product professional with 15+ years of experience" | At Kestrel since February 2009; in product since August 2024. | True in total, misleading beside "product". | No count of years. The dates show the tenure. |
| Skills: "Risk" | No fact about work with a risk team or on controls. | A term with no evidence behind it. | Leave it off unless question 2 produces a fact. |

Nothing is counted twice. The street address, the date of birth, the marital status and the
referee's details are not in `facts.md`, so I have not checked them; they come off regardless.

## 4. What is missing

Confirmed facts about her career that the résumé leaves out, most useful for this ad first.

1. **The prioritisation decision.** She put the merchant auto-fill change ahead of a dashboard
   managers had asked for, because case data showed retyping on about 70% of cases. The résumé
   has only its result. This is the ad's "backlog prioritisation using data" requirement, shown.
2. **What she owns.** Beacon, what it is, and that about 140 staff use it.
3. **How the work runs.** A 10-person squad, 2-week sprints, user stories and acceptance
   criteria written by her, reporting to the Head of Payments Product. The ad asks for most of
   these in so many words.
4. **The ageing-disputes result.** A daily report she introduced; disputes older than 45 days
   fell from about 310 to about 90 over 6 months.
5. **The scale of the operation.** About 2,400 disputes a month, 2 sites, 3 team leaders.
6. **Card scheme experience.** She worked within Visa and Mastercard chargeback timeframes.
7. **Two promotions and the move into product,** with her reason for it in her own words.
8. **Coaching.** 2 disputes officers coached into team leader roles; 9 direct reports as Team
   Leader.
9. **Two roles.** Disputes Officer (June 2012 to September 2015) and Customer Service Officer
   (February 2009 to June 2012).
10. **Tools and learning.** Confluence, Power BI, and the 2025 Product Fundamentals course.
11. **Contact items.** LinkedIn address and Australian citizenship.

## 5. Against the Lantern Bank ad

| Ad item | Status | Evidence, and where the ad's phrase goes |
| --- | --- | --- |
| Required: experience as a Product Owner in an agile squad | **Shown** | Product Owner since August 2024 in a 10-person squad on 2-week sprints. "Product Owner" in the summary; "agile squad" in the current role's scope paragraph. Lantern's role owns the squad's backlog; hers is one of 2, and the résumé should say so plainly. |
| Required: backlog prioritisation using data | **Shown** | The auto-fill decision and the 70% of cases. In the summary, the skills and the first bullet. |
| Required: card disputes or chargeback operations experience | **Shown**, and her strongest item | Disputes roles since June 2012, ending with a 31-person operation handling about 2,400 disputes a month. |
| Required: experience delivering card scheme mandate changes (Visa or Mastercard) | **Not shown** | She has never owned or delivered one. Leave it out entirely. Working within Visa and Mastercard chargeback timeframes is true and is on the page as operations experience; it must not be worded to suggest mandate delivery. |
| Required: stakeholder management across operations and risk | **Partly shown** | Operations: she turned down a dashboard managers asked for, and wrote process and training for 140 staff. Risk: no fact. See question 2. |
| Desirable: a product or agile certification | **Not held** | The internal Product Fundamentals course is listed as a course. |
| Desirable: Jira and Confluence | **Shown** | Both on the Tools line. The old résumé omits Confluence. |
| Duty: lead discovery with frontline disputes staff and customers | **Not shown** | The case data is evidence of discovery from data. No fact covers discovery sessions with staff or with customers. See question 3. |
| Duty: accept work each sprint | **Not shown** | She writes the acceptance criteria; whether she accepts the work is not confirmed. See question 3. |

Hannah should know before applying that the résumé will not meet the mandate-changes
requirement. One documented ranking tool grades on whether every required item is met, so she
may be ranked below candidates who meet all five. It is still worth applying: the other four
are met or partly met from recent roles, and her operations background is unusual for a Product
Owner.

Practical points for this application:

- The ad says to apply through Lantern's careers site, so upload a Word file unless the site
  says otherwise, then read the fields it fills in and correct them by hand. I have no research
  on which system Lantern runs.
- Enter each of the 5 roles as its own record on the form. If a screening question asks for
  years as a Product Owner, the answer counts from August 2024, not from 2009.
- Applications close 5 December 2026.
- The proposed wording comes to 529 words, which fits 2 pages with room to spare. That
  leaves space for the answers to the questions below.

## 6. Lint output

`python3 scripts/resume_lint.py old-resume.md`, exit code 1:

```
ERROR street-address: the contact line carries a street address; city and state are enough
ERROR section-not-wanted: line 5: section 'Career objective' does not belong on the résumé
ERROR referee-details: line 30: referee contact details are supplied on request, not printed
ERROR section-missing: no summary section
ERROR section-missing: no experience section
ERROR education-empty: the education section is empty; leave it out when there is nothing to list
ERROR personal-detail: line 3: date of birth does not belong on the résumé
ERROR personal-detail: line 3: marital status does not belong on the résumé
ERROR years-count: line 7: '15+ years' counts years; the dates already show the tenure
ERROR generic-register: line 7: 'results-driven' reads as generic; say what happened instead
WARN  section-name: line 13: 'Employment' is not a standard heading a parser maps to a field
WARN  skills-lines: key skills has 1 line(s); the default is 2 to 4 labelled lines plus a tools line
WARN  skills-label: 1 skills line(s) have no 'Label: ' opening
WARN  skills-tools: no Tools line; tools are a list and get their own line
info  142 words, 0 bullets
RESULT: 10 error(s), 4 warning(s)
```

The lint checks structure and voice only. It found none of the overclaims in section 3, and it
reports "0 bullets" because it found no experience section to read them from.

I also ran the lint with `--allow-gaps` over the wording proposed above, assembled in a scratch
file that is not part of this review. It returned 0 errors and 3 warnings: the non-standard
"Professional development" heading, and 2 for the bracketed question, which clear when Hannah
answers it. The summary measured 100 words and the whole document 529. `facts_lint.py`, which
checks figures, has not been run; I checked each figure against `facts.md` by hand.

## 7. Questions for Hannah

1. **Auto-categorisation:** what was your part in it? Is it on the Beacon backlog, and did you
   write the business case or the stories?
2. **Risk:** have you worked with Kestrel's Risk team on a Beacon change or a disputes process,
   for example agreeing a control? If so, what was it? This is the missing half of a required
   item.
3. **Discovery and acceptance:** have you run discovery with frontline disputes staff or with
   customers, beyond the case data? Do you accept the squad's work on the Beacon backlog each
   sprint?
4. **Chargeback timeframes:** in which roles did you work within Visa and Mastercard chargeback
   timeframes? The proposal puts it in the Operations Manager role.
5. **Figures leaving Kestrel:** you have ruled out the $3.2 million. Are the others cleared for
   an external résumé: 140 staff on Beacon, 2,400 disputes a month, 31 staff, 310 to 90 ageing
   disputes, 18 to 14 minutes?
6. **Jo:** does your manager know you are applying? Either way, the referee details come off.
7. **First person:** the proposal writes paragraphs as "I own…". Do you want that, or an implied
   subject throughout?
8. **One résumé or several:** is this the only role you are applying for, or do you want a
   second version for operations leadership roles?

Say which findings to apply and I will make the changes.
