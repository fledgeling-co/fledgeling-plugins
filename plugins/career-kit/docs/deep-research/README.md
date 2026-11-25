# Research corpus: how Australian banks screen résumés, November 2026

Six reports on one brief, about a generic candidate with twenty-plus years at one large
Australian financial-services employer. `skills/resume-craft/references/evidence.md` cites them
by the letter below. No report contains a real person's details.

| Letter | File | Produced by | Sources | Notes |
| --- | --- | --- | --- | --- |
| C | `codex-local-au-bank-cv-2026.md` | Codex CLI through Dossier's free lane (runs `dr_2ad454d07e9275f1` and `dr_c46b6b7fb38a3bdd`, the same text) | 57 to 63 | 11-ad sample; the most careful about what is unproven |
| A | `openai-au-bank-cv-2026.md` | OpenAI deep research through Dossier (`dr_223cc71819f7674a`), about $9 | 79 | 13-ad sample; cut-off 19 November 2026 |
| P | `perplexity-au-bank-cv-2026.md` | Perplexity through Dossier (`dr_b4ddbff57607da36`), about $4 | 19 | Mostly inference; sampled no ads; its bank table is superseded |
| O | `claude-opus-au-bank-cv-2026.md` | Headless Claude Opus run | 76 | 16-ad sample; vendor documentation for the ranking tools |
| G | `gemini-au-bank-cv-2026.md` | Gemini Deep Research in the Gemini app | 142 | Embedded chart images removed; several figures arrive through CV-vendor blogs |

All six runs were read in full before the skill was written. Citations inside the reports were
not re-opened for this skill; the careers-site checks recorded in `au-banking-2026.md` were made
directly on 20 November 2026 during the source engagement.

## Layout and typography, 25 November 2026

Two more reports on a second brief: the layout, structure, type, size, line spacing and margins
of a résumé for the corporate Australian market in 2026, and whether there is one accepted layout
or several. `resume-craft/references/evidence.md` cites them as LG and LP.

| Letter | File | Produced by | Sources | Notes |
| --- | --- | --- | --- | --- |
| LG | `gemini-au-resume-layout-2026.md` | Gemini Deep Research in a signed-in Chrome, started through Dossier | 31 | Text read from the page's accessibility tree, because copy and export were unavailable; line breaks are approximate and citation chips appear as fragments. Marks its exact spacing values as its own inference |
| LP | `perplexity-au-resume-layout-2026.md` (+ `.sources.md`) | Perplexity Sonar Deep Research through Dossier (`dr_8007ed40c67f61d3`), about $4 | 20 | Strongest on government guidance and the legibility research; leans on one employer's own CV guide |

Both found three accepted layouts rather than one: corporate through a hiring system, public
sector, and a two-column first page only for a PDF sent straight to a person. Neither found an
Australian source that gives a number for line spacing or margins.

Every page cited for a layout claim was then opened and its own example checked against the
claim. Two did not match: SEEK's ATS-tips page links three "ATS-optimised" templates, two of which
build a sidebar from Word tables (measured: Arial 11pt, 12.7 mm margins, 16 to 18pt headings), and
SEEK's formatting article recommends two columns on page one. One employer's own published CV
guide said "a CV can be 3-4 pages long" and asked for "plenty of white space"; read the target
employer's own guide where it has one.
