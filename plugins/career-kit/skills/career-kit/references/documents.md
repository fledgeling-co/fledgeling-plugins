# The documents: one set of facts, built to PDF and Word

`career-kit:resume-craft` decides the words: what each section is for, the voice, how to suit
the document to a role. This file covers the source format, the builds and the checks on the
built pages.

## The Markdown source

```markdown
# JANE DOE

Sydney, NSW | 0400 000 000 | jane@example.com | linkedin.com/in/jane-doe | Australian citizen

## Professional summary

One first-person paragraph.

## Key skills

Label: an ability; another ability
Tools: Jira, Power BI

## Professional experience

### Example Employer, Sydney | Aug 2005 – Present

One or two sentences on how they moved.

#### Current Title | Example Employer | May 2025 – Present

A scope line.

- One thing that happened, ending on what it changed.

#### Earlier Title | Example Employer | Jun 2008 – Dec 2013
```

**Missing information is a placeholder in angle brackets**, named for what is missing and put
where the answer will go: `<what the award recognised>`. The builders print it in red in the
PDF and the Word file. A document with a placeholder goes to the person and never to an
employer. Square brackets still render as a yellow highlight, for drafts written to the
earlier convention.

## One résumé, or one per role family

Ask the person. Write whichever they choose out whole, by hand, and build it with
`build_resume.py` and `make_docx.py`.

Where there are several, they share every title, date and figure and differ in three places:
the summary, which skills appear, and which bullets appear and in what order.
`make_variants.py` produces a draft of each from one facts file and a variant spec. Read and
rewrite each draft as a document; text assembled from fragments has not been read by anyone.

A public copy drops the phone number and email and softens any figure the person has
restricted. Write it from the finished internal copy in the same sitting, and check its
extracted text for every restricted figure and contact detail before it goes anywhere.

## Building

```bash
python3 -m http.server 8942 --bind 127.0.0.1 --directory rewrite &
python3 scripts/build_resume.py resume.md resume.html "Footer title"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --no-pdf-header-footer --print-to-pdf=resume.pdf http://127.0.0.1:8942/resume.html
python3 -m venv /tmp/dv && /tmp/dv/bin/pip install python-docx     # once
/tmp/dv/bin/python scripts/make_docx.py resume.md resume.docx
```

The local server is needed because Chrome's `--print-to-pdf` loads the page over HTTP.
Without `python-docx` the Word step falls back to an unstyled conversion that is readable and
does not match the PDF.

## Pages break, containers do not

The sheet has `min-height` and no `height`, and no `overflow: hidden`. A fixed height with a
manual page split once cut the last bullets off page one of several documents with no error
anywhere and a correct page count. The CSS that does the work:

```css
@page { size: A4; margin: 18mm }
h2, h3 { break-after: avoid }
li, h3 + p { break-inside: avoid }
```

Because a list item does not break, a bullet too long for the space left on a page moves whole
to the next page and leaves the space empty. In the source session a merged 100-word bullet left
three empty lines at the foot of page one and pushed the document to three pages; moving it up
the role, to where it fitted whole, brought it back to two pages without cutting a word. Reorder
before cutting.

When cutting, find the lines that cost most first. `pdftotext -layout resume.pdf - | awk 'NF>0
&& NF<=4'` lists lines of four words or fewer, and a few words cut from that paragraph saves the
whole line. A cut that does not remove a whole line changes nothing, so check where the last
line of the final page sits (`pdftotext -bbox`) after each one. Cut words the person did not
give, such as a repeated noun or an article, before any phrase they confirmed, and list every
trim in the reply.

Resolve an overflow by cutting ranked content, never by shrinking type or margins. Take the
type sizes and margins from the research for the person's market and set them in both
builders together.

## Type and spacing

The builders' defaults sit in the middle of the Australian research's ranges and of typesetting
guidance for reading: Arial 10.5pt on exact 13pt lines (1.24 times the type), 4.5pt between
bullets, 6pt after paragraphs, 13pt section headings with 14pt above, and margins of 20 mm at the
sides and 18 mm at top and bottom. The research gives Arial, Calibri or Aptos at 10.5 to 11pt,
13 to 14pt headings, Word line spacing of 1.05 to 1.15 and margins of 1.8 to 2.2 cm; typesetting
guidance gives a line height of 1.2 to 1.45 times the type. For another market, take the ranges
from that market's research and choose from their middle.

Choose the middle of each range, not the end that fits more words. In the source session every
value had drifted to its dense end, each one defensible alone: lines 1.15 times the type, 3pt
between bullets, margins at the floor, both pages full to the margin. Together they made a page a
skimming reader struggles with, and the person helping asked about density only after the layout
had been through seven rounds. Moving every value to the middle cost about a tenth of the lines,
which came out of the drafter's words first; at 11pt the same spacing would have cost a quarter.
At 10.5pt a line across 170 mm holds about 95 characters, above the 90 that reading guidance
allows; inside the research's size and margin ranges it cannot get lower, so leave it and say so.

Set line spacing in points, the same number in both builders. Word's "1.15" multiple is about
1.32 times the type size for Arial, while CSS's 1.15 is 1.15 times, so one number gave the Word
file lines 16% taller than the PDF's, and it opened in Word at three pages while the PDF held two.
Word also adds one paragraph's space-after to the next one's space-before where CSS collapses the
two margins, so `make_docx.py` sets each space-before as the CSS gap less the usual space-after.

Check the Word file's page count in Word, or in LibreOffice where Word is absent; the PDF says
nothing about how Word lays the same text out, and a python-docx file records no page count of its
own. Word's sandbox on macOS opens files inside its container without a permission prompt:

```bash
C=~/Library/Containers/com.microsoft.Word/Data/check && mkdir -p $C && cp resume.docx $C/
osascript -e 'tell application "Microsoft Word"' -e "open POSIX file \"$C/resume.docx\"" \
  -e "save as active document file name \"$C/resume.pdf\" file format format PDF" \
  -e 'quit saving no' -e 'end tell'
pdfinfo $C/resume.pdf | grep Pages                 # then delete $C
soffice --headless --convert-to pdf resume.docx    # LibreOffice, where Word is absent
```

## Reading the built page

```bash
pdftoppm -r 60 -png resume.pdf /tmp/page       # then look at the images
pdffonts resume.pdf                            # what actually embedded
pdftotext resume.pdf - | head                  # the order a parser will read
```

A page count of two says nothing about these, so check each on the images:

- a last line that ends mid-sentence, or a second page that is half empty;
- a role line where the employer or the date has dropped to its own line;
- a contact line that has wrapped untidily;
- a font named in the CSS and absent from the machine, which falls back silently and leaves the
  PDF and the Word file different for a reason invisible in the source;
- a red placeholder still in a copy meant for an employer.

## Word and Google Doc

Upload the Word file to application portals, which parse it, and send the PDF to people.

A Google Doc version has no prior run behind it in this skill. Check what the runtime offers,
`anthropic-skills:google-workspace` where it is installed or a Google Drive MCP server, create
the document from the same Markdown so the facts cannot diverge, and say which route you used.

## After any edit

1. Run `../resume-craft/scripts/resume_lint.py --keep keep.txt resume.md`, and
   `scripts/facts_lint.py` for figures.
2. Rebuild the PDF and the Word file together, and check both page counts, the Word file's in Word.
3. Look at the page images.
4. Check the other documents for the fact you changed.
