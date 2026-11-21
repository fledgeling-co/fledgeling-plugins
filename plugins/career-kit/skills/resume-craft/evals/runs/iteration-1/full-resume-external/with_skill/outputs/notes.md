# Notes for Hannah

Your résumé for the Lantern Bank Product Owner, Card Disputes role is in `outputs/resume.md`. It uses only the facts you confirmed. It is not ready to send until you have read the first two sections below.

## Requirements in the ad that the résumé does not meet

The ad lists 5 required items. The résumé shows 3 of them: Product Owner in an agile squad, backlog prioritisation using data, and card disputes operations experience.

1. **Experience delivering card scheme mandate changes (Visa or Mastercard): not shown.** You told me you have never owned or delivered one, so the résumé does not claim it. What it does say, twice, is that you worked within Visa and Mastercard chargeback timeframes as an operator. That is true and relevant, but it is not the same thing, and a reader who knows disputes will see the difference. No wording closes this gap. Expect to be asked about it, and decide beforehand how you will answer: what you know about how a mandate change reaches the disputes floor, from the receiving end.
2. **Stakeholder management across operations and risk: partly shown.** Operations is well covered. Nothing you confirmed mentions working with a Risk team, so the résumé says nothing about risk. If you have done this, see question 1 below.

Of the 2 desirable items, Jira and Confluence are on the tools line. You do not hold a product or agile certification. The internal Product Fundamentals course is listed as professional development, which is what it is, and it should not be described as a certification on the application form.

## Questions that would strengthen it

Each of these is something the ad asks about and your facts did not cover. I left them out of the résumé instead of guessing. Answer any that apply and the relevant line can be added.

1. Have you worked with Kestrel's Risk team on a Beacon change, or in operations, for example agreeing a control or getting a change signed off? What was it?
2. Do you accept the squad's work at the end of each sprint? The ad says "accept work each sprint", and you confirmed only that you write the stories and acceptance criteria.
3. Have you run discovery with frontline disputes staff or with customers: interviews, shadowing, workshops? The résumé shows discovery from case data only.
4. In which roles did you work within the Visa and Mastercard chargeback timeframes? I put it in the sentence under the employer heading because I could not tie it to one role. If it was Disputes Officer onwards, it can move to those roles.
5. Did the roster restructure change anything you could describe, even without a number? It currently stands as one line with no result, because none was measured.
6. Is hannah.okoye@example.com a personal address? An external application needs a personal email, not a Kestrel one.

## Things I handled a particular way

- **The $3.2 million chargeback loss figure is not in the résumé**, as you asked. Keep it out of the application form and the interview too.
- **Auto-categorisation is described as in build, with the 30% as a forecast from the business case** and a statement that nothing has been measured. It sits in the paragraph about your current role, not in the bullets, because the bullets are for things that have already happened.
- **The fraud-alert SMS says "supported"** and names your part: the disputes team's process and the training. **User acceptance testing says "coordinated"**, with the QA team running the tests. Use the same verbs in the interview and on LinkedIn.
- **"One of 2 backlogs in the squad"** is stated, so nobody reads the résumé as saying you own the squad's whole backlog.
- **Your line about being tired of working around the tool is in the summary**, close to your own words. It is the sentence that makes the paragraph yours. Say if you would rather it came out.
- **No count of years appears anywhere.** The dates show the tenure. All 5 roles keep their true dates, because Lantern's application form and employment check will collect them.
- **There is no "Education and certifications" section**, because you have no formal qualifications to list and an empty section is worse than none. In its place is a "Professional development" section with one line. The lint warns that this is not a heading every applicant system maps to a field. I kept it because the alternative was to mislabel an internal course.

## Before you apply

- Applications close 5 December 2026, through the Lantern Bank careers site.
- Check that linkedin.com/in/hannah-okoye-example opens your profile, and that the titles and dates there match the résumé exactly.
- The résumé is Markdown and still needs building into a file. Upload a Word (.docx) version to the careers site unless the site asks for something else, named `Hannah-Okoye-Resume-Product-Owner.docx`. After uploading, read the fields the site filled in (employer, title, dates) and correct them by hand. Enter each of the 5 roles as its own employment record.
- If a screening question asks for years of experience as a Product Owner, count from August 2024, not from 2009.
- At 526 words the résumé will run to about one and a half pages. That is within the two-page norm for Australian banking. The answers to the questions above are the right way to fill the space; padding is not.

## Checks run

- `resume_lint.py`: 0 errors, 1 warning (the "Professional development" heading, explained above).
- `facts_lint.py` against `facts.md`: every figure in the résumé traces to a confirmed fact.
