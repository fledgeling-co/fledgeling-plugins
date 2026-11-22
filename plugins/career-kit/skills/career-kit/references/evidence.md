# Evidence — where each rule in this skill comes from

Every structural choice traces to something observed. The source is one engagement on 20 and
21 November 2026 that produced a complete application kit for one person: research, a review
page, a résumé (first as five role-targeted versions, then as one), a personal website,
LinkedIn copy and an interview guide. No claim here is a general finding about résumés; they
are failures that happened once, to one run, and were fixed. The rules about the words
themselves are evidenced in `../../resume-craft/references/evidence.md`.

| Rule | What happened |
| --- | --- |
| Never invent a fact; a gap goes back to the person as a question | Worked examples offered in chat for one question came back as the person's answer almost word for word. The relay confirmed they were accurate, but the agent could not tell that from the answer alone. |
| An unchanged example is a real answer | Fifteen second-round answers came back as the form's example text. They were recorded as unverified; the person's relay said she had selected them because they were accurate, and all fifteen were applied. |
| State scope exactly | Review panels caught, on separate rounds, "shipped" where the truth was "supported", "runs" where it was "coordinates", "led" where it was "coordinated", and a summary implying ownership of a squad's whole backlog where the person owned one backlog in it. |
| One résumé per role from one source of facts | The first draft was a single generic résumé. The instruction was that it had to target the named roles; a panel separately said twice that one document cannot serve a product role and a delivery role. Later reversed by the same person, who asked for one résumé written by hand after five assembled versions had passed review and read badly; the skill now asks which the person wants |
| Ask which figures may appear publicly, keep a softened copy | Three figures were fine on internal applications and not on a public page. The public résumé, the site and the LinkedIn text each needed a softened version. |
| One set of facts across every document; check them all when one changes | Five résumés, a website, a LinkedIn document and an interview guide shared the same dates and figures, and outputs edited separately began to disagree. A build script was the first remedy; it was later limited to rendering, after documents it assembled from fragments passed review and read badly. On the second day a corrected fact was still wrong in another document three times: a claim about promotions on the website, a role attribution in the interview guide, and a withdrawn statement in the LinkedIn copy |
| Pages break automatically; no fixed-height container | `.sheet { height: 297mm; overflow: hidden }` with a manual page split silently cut bullets from page one of all five variants. Nothing errored; the page count was still correct. |
| Check fonts actually embedded | `pdffonts` showed Helvetica and Arial where the CSS specified Aptos and Calibri, neither of which was installed. The PDF and the Word file had diverged invisibly. |
| Check rendered output in a real browser, and say what you did not look at | Chrome's `--screenshot` captures scroll 0 only, so a scroll-driven site reported as fine. A CDP driver that eases to each position was written to see the rest. Nobody saw the site on a real phone or in Safari, and the notes say so. |
| Panel briefs on disk, reversed option order, failed lane ≠ verdict | One lane returned an empty file after a headless permission denial. Order reversal was done by hand for two decisions. Every brief and answer was copied into `decisions/`. |
| The person's rules outrank reviewers | A panel's majority chose a hero image concept; the person chose a different one and a combination the panel had not considered. Two panel recommendations were declined because the person had ruled the wording out. |
| Check the project files after a panel | A file was found changed that nobody in the session had edited; the likeliest cause was a panel lane with write tools that had been given the project path. |
| Call the router directly when the session's MCP link drops | The session's connection failed with "session belongs to another process" while the router itself was healthy. One deliverable had already shipped saying the reference and image tools were unavailable; they were not. |
| An unlisted deployed page is still public | A private practice page was deployed with a `noindex` header and no password, returning 200 with three restricted figures in it, and its footer mentioned a password that was never set. |
| Keep chat replies short and route output to files | The session ran long enough to be restored to an earlier point at least once and to need its auto-compact window raised. |
| Research: reconcile lanes, verify directly | Four research lanes disagreed about which applicant tracking systems the target employers run. A `curl` against each careers site settled it, and found that the internal and external paths used different systems. |
| Research: write the hand-off prompt yourself | The research tool's own auto-generated prompt came out as a legal-research template, with "legal team" framing and laws-in-force tags, for a résumé question. |
| Expect rounds, and say so | Three question forms were needed. The third, of fifteen questions, came from a panel reading résumés that had already been called finished, and it was answered within the hour because eight of its questions quoted earlier answers back. |
| A panel reviews copy after any change | The résumés were reviewed and corrected twice. A third panel of five lanes still found a forecast ("would be") printed as a result, a count of users printed as staff, one piece of work counted in three bullets, and a line no answer supported. |
| A quiet lane is not a failed lane; results are interim until all lanes settle | One lane stopped after a one-line preamble, was recorded as failed and retried, and both runs then returned complete answers. The synthesis was corrected twice, vote fractions restated, and the question count derived from it went nine, thirteen, fifteen. |
| Give reviewers the whole fact base | A lane proposed deleting a figure as unsourced; it was confirmed in notes the lane had not been given. |
| Review is not apply | The request was to review the résumé content. Findings and wording were reported and no source was edited until the answers came back and the instruction to incorporate was given. |
| Count questions looked at, not questions holding a value | The third form pre-selected every suggested default and read "15 of 15 answered" before it was opened. |
| Ask when the tick and the text disagree | One answer ticked the option to drop a claim and wrote a note supporting it. The agent chose a reading and flagged it for the relay. |
| The research's lengths are limits; a requirement the person holds appears in the ad's words | Five summaries ran 113 to 157 words against a researched 60 to 100, and five of five lanes said trim. One ad's required phrase appeared only hyphenated and its synonym not at all. |
| Preview an effect before building it; review tools never deploy | One hero image took six iterations, including seven selectable shader effects and a water simulation, and ended as a single image that grows on hover. The effect chooser was kept local and removed. |
| Check funds, registrant, owner and email before offering to buy a domain | Buying one took four turns: short balance, no registrant details, no tool to read the contact on other domains, and a contact email the owner did not expect, changed afterwards. The registrar's old parking records were still being served minutes after the new ones were written. |
| Name every file a subagent must read | A subagent told to extract "across the session" ran over its own context until given the transcript paths and the render command. |
| Keep a list of what is waiting on whom | A caption wording, registrant details and whether to apply a review's findings were all open at once across a long conversation, alongside four changes of direction to one image. |
| Read the document as a reader, and ask reviewers for a cold read first | A panel asked whether tense and person were consistent passed summaries that read "Lead discovery… Took the backlog…". The person pointed out that "Lead" reads as a command or a misspelt "Led". |
| Do not hand the panel your own style rule as settled | "No first person" was written into a review brief. A lane proposed first-person summaries twice and was overruled by it; the person then asked for first person. |
| Write each document whole; scripts render and check | Five résumés were assembled from fragments by a build script. The person asked for one résumé written out by hand, and the faults became visible on the first full read. |
| Define each section's job before drafting | "Epics, features and stories" sat in Key skills because it was true and matched an ad. Four other items in that section were also things, not abilities. |
| Use the whole career, not only form answers | The summary gave "coordinated 5 to 10 change workstreams" as the whole of eighteen years, because it had a confirmed number and an ad's word. The old résumé and profile described far more and had been used only for dates. |
| Read the reviewers' reasons before rewriting | Four then five lanes stumbled on one sentence. It was rewritten from a summary of their answers, for the wrong fault, and "teams of 5 and about 15" survived until the person read it. |
| Distrust wording that has survived many drafts | That phrase was written in the first hour as shorthand and passed every fact check after. |
| Do not cut to a word count | A cut to 800 to 850 words left page two 40% empty and removed the one sentence in the summary with a person in it. |
| Give reviewers the original documents | Lanes flagged four true statements as unsourced; each was in the old résumé. |
| Answer before acting | A sentence was changed and redeployed while the person's message asking why it had been missed was in transit. |
| Check the built page, not the page count | Raising the type size pushed "· Employer" onto its own line on three roles in every résumé; the page count was unchanged. |
| Generate the end state and reverse the clip | A hero video of beads settling into rows was made by animating the settled still coming apart and reversing it. A first, busier concept was rejected for what it resembled. |
| Missing information is a red placeholder where the answer will go | The person asked for gaps to be shown in the draft as red text in angle brackets. An earlier instruction had objected to a draft with many highlighted gaps; they now preferred to see exactly where an answer was wanted |
| A few questions go in the conversation; many go in a form | Five gaps were asked as multiple-choice questions with a free-text option in chat, at the person's request, and all five were answered in free text within minutes |
| A document that will be judged against the research abides by it | The person said the résumé would later be judged against the research digest. The current role then had a 53-word scope paragraph and six bullets against the research's scope line and three to five |
| The person's standing decisions are checked after every revision | An audit found a term the person had asked for by name, and several required phrases, dropped while unrelated feedback was being applied |
| Put your recommendation to the panel and ask for the case against each verdict | On a structural question three lanes took the writer's recommendation and two took no change; both dissenters named the same narrower option as the strongest case against themselves, and it became the decision |
| Settle placement, edges, the resting frame and the beats before generating a video hero | A character hero took 11 billed clips for a cut that uses three. Four came from a tool that could not make clips join. The rest include a return clip added because the sequence ended on an empty frame, an exit and a return made again because mirroring the clip for the layout turned the exit toward the text, and a dance the person replaced with another action |
| Read the video tool's parameters before planning a sequence | The tool sent a prompt and a first frame only, so four clips chained from each other's last frames restarted at every join and came back at 720p. The person said they did not go together. Adding last-frame, resolution and audio inputs to the tool gave 1920x1080 clips that ended on the frame supplied |
| Join on a held pose, and measure a skip | The person reported frame skips while the character was thinking. Frame-to-frame difference across the join was 1.41 against 0.4 to 0.5 either side: the first clip was still moving when it reached its last frame and the second started from rest |
| Fit the length in the script, never in the edit | A 20-second sequence was cut to 14 by speeding it up 1.35 times, cutting inside two clips and cross-fading one join. The person described each of those as a skip |
| A contact sheet is not a viewing | Every clip was checked from tiled frames and reported as correct. The person, watching, found the rushed pace, the skips and the missing pause after the wave |
| Check your reading of free-text feedback before rewriting | On 22 November 2026 the person sent about fourteen notes. A page of 25 questions, each quoting a note with the readings as options and nothing pre-selected, came back with every question answered. Two of her answers chose a reading the drafts had not considered: work split into the part she supported and the part that was hers |
| Put the rules you drew back to the person | Seven rules drawn from her notes were offered as a tick list; she ticked four. The other three stayed the skill's defaults, and her own answers on two verbs went the other way from one of them |
| Offer an old document's lines back as a tick list | Her note said "review original resume copy"; offered its four lines for one role, she took three back |
| An unchanged example is often the floor | A selected example about missed service levels stood for two rounds; her own words described a red-to-green turnaround over a six-month plan |
| After corrections, ask which other lines do not represent the work, and offer research-backed wording | The person asked for this step herself, and chose it for the lines she had flagged |

## What this skill changed from the session

The session hand-edited some outputs, kept scripts in `/tmp`, and did not have a mechanical
check on figures. This skill moves the scripts into the package, adds `facts_lint.py` as the
gate the session enforced by review alone, and generalises every name and path.

## Not carried forward

The session's Google Doc output was requested and never built. The step is designed in
`references/documents.md` and marked as unproven there.
