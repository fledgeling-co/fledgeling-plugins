#!/usr/bin/env python3
"""Check a résumé's structure and voice against the defaults in resume-craft.

    python3 resume_lint.py resume.md                 # exit 0 clean, 1 on any error
    python3 resume_lint.py --allow-gaps draft.md     # a draft that still carries [gaps]
    python3 resume_lint.py --voice implied resume.md # the person chose no "I" in paragraphs
    python3 resume_lint.py --self-test               # run the bundled fixtures

It reads the Markdown subset that career-kit's build_resume.py renders:

    # Name / contact line / ## Section / ### Employer | dates /
    #### Title | Employer | dates / paragraphs / "- " bullets

What it checks is mechanical: section order and names, summary length, a count of years,
personal details, date format, role-line shape, bare present-tense openers, the generic
register, bullet counts, an empty education section, and [gap] markers. It cannot tell
whether a summary could sit on someone else's résumé, whether a skill is shown below, or
whether a verb is stronger than the person confirmed. Those are read by a person or a
reviewer; facts_lint.py in career-kit checks that each figure was confirmed.

ERROR lines fail the run. WARN lines are questions: read each one and decide.
"""
import argparse
import datetime
import os
import re
import sys

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
DATE_RANGE = re.compile(
    rf"\b(?:{MONTHS}) \d{{4}} [–-] (?:(?:{MONTHS}) \d{{4}}|Present|present)\b")
FULL_MONTH = re.compile(
    r"\b(January|February|March|April|June|July|August|September|October|November|December) \d{4}\b")

SECTION_ALIASES = {
    "summary": {"professional summary", "career summary", "summary", "profile",
                "professional profile"},
    "skills": {"key skills", "skills", "core capabilities", "core skills", "key capabilities"},
    "experience": {"professional experience", "experience", "career history",
                   "employment history", "work experience"},
    "education": {"education and certifications", "education & certifications", "education",
                  "qualifications", "qualifications and certifications",
                  "education and qualifications", "certifications"},
    "development": {"professional development", "training", "recent professional development"},
}
ORDER = ["summary", "skills", "experience", "education", "development"]
BANNED_SECTIONS = {"objective", "career objective", "personal details", "personal information",
                   "hobbies", "interests"}

# The register recruiters read as generic or machine-written. Sources: references/evidence.md.
CLICHES = [
    "results-driven", "results driven", "results-oriented", "results oriented",
    "proven track record", "passionate", "dynamic", "spearheaded", "spearhead",
    "leveraged", "leveraging", "leverage", "synergy", "synergies", "synergised",
    "seasoned", "visionary", "operational excellence", "fast-paced", "fast paced",
    "detail-oriented", "detail oriented", "team player", "self-starter", "self starter",
    "highly motivated", "thought leader", "best-in-class", "best in class", "world-class",
    "world class", "cutting-edge", "cutting edge", "strong communication skills",
    "excellent communication skills", "go-getter", "hard-working", "hardworking",
]
DUTY_OPENERS = re.compile(r"^(responsible for|duties includ|tasked with|in charge of)", re.I)

# Verbs that, opening a line in their bare form, read as a command or a misspelt past tense.
BARE_PRESENT = {
    "lead", "own", "manage", "drive", "deliver", "coordinate", "run", "build", "develop",
    "support", "oversee", "work", "write", "coach", "ensure", "partner", "collaborate",
    "prioritise", "prioritize", "create", "define", "maintain", "provide", "design", "plan",
    "prepare", "review", "report", "liaise", "facilitate", "implement", "identify", "analyse",
    "analyze", "monitor", "track", "mentor", "train", "negotiate", "present", "translate",
    "champion", "act", "serve", "take", "bring", "help", "handle", "execute", "engage",
    "shape", "set", "establish", "improve", "accept", "embed", "orchestrate", "administer",
}
# Items nearly every résumé for a role carries. They read as the job ad, not as the person.
SKILL_GENERIC = {"leading teams", "leadership", "stakeholder management", "communication",
                 "teamwork", "problem solving", "problem-solving", "time management",
                 "attention to detail", "managing stakeholders", "team leadership",
                 "project management", "people management", "strategic thinking",
                 "collaboration", "relationship management"}

# "use X to draft …, and validate …": the second verb attaches to the tool.
SECOND_VERB = re.compile(
    r"\b(?:use|used|using)\b[^.;]{3,80}?\bto \w+[^.;]{3,120}?,? and "
    r"(?:validate|check|review|approve|confirm|verify|edit|correct|publish|send|sign off)\b")

# A widely known product or method followed by a few words saying what it is.
KNOWN_GLOSS = re.compile(
    r"\b(?:Microsoft Copilot|Copilot|ChatGPT|Jira|Confluence|Excel|Power BI|Tableau|Salesforce|"
    r"Slack|Microsoft Teams|GitHub|Scrum|Kanban|SQL|Python|Word|PowerPoint|SharePoint|Trello|"
    r"Asana|ServiceNow|Workday|SAP|Figma|Miro)(?:,| \() ?(?:an?|the) [A-Za-z][A-Za-z -]{1,40}?"
    r"(?:tool|assistant|platform|system|software|application|app|framework|methodology|method|"
    r"language|product|suite)\b")

VAGUE_RANGE = re.compile(r"\b\d{1,3} (?:to|or) \d{1,3} (?!per cent|percent|%)[a-z]+")

LIST_IN_BULLET = re.compile(r"(?:(?!and\b)[\w'-]+(?: (?!and\b)[\w'-]+){0,2}, ){2,}"
                            r"(?!and\b)[\w'-]+(?: (?!and\b)[\w'-]+){0,2},? and ")

EMPTY_SELL = re.compile(r"\b(?:successfully|significant(?:ly)?|key (?:role|stakeholder|contributor)|"
                        r"instrumental|pivotal|world-class|best-in-class|robust|seamless(?:ly)?)\b", re.I)
ADMIN_END = re.compile(r"(?:tracked|logged|recorded|documented|raised|filed) (?:it|them|this) "
                       r"in (?:Jira|Confluence|a ticket|the register|the log)\.?$", re.I)

AWARD = re.compile(r"\b(?:[Aa]ward|[Pp]rize)\b")

# Capitalised words that are methods or standard terms, not this employer's product or system.
SKILL_PROPER_OK = {"Definition", "Done", "Scrum", "Agile", "Kanban", "Lean", "Release", "Train",
                   "Chief", "Product", "Owner", "English", "Australian"}

# A sentence that describes something near the person instead of what they answer for.
LABEL_OPENER = re.compile(
    r"^I(?: am|'m|\u2019m) (?:the |a |an )?(?:[A-Z][\w-]+ ){0,3}"
    r"(?:Owner|Manager|Lead|Leader|Engineer|Analyst|Director|Head|Consultant|Specialist|"
    r"Officer|Designer|Developer|Architect|Coordinator|Advisor|Adviser|Partner|Executive)\b")
FIGURE_ON_OBJECT = re.compile(
    r"\b(?:which|that) (?:has|have|serves|serve|supports|support)\b[^.]*\d|\bused by (?:about |around |over )?\d")
FIRST_PERSON = re.compile(r"\b(?:I|my|me|I'm|I\u2019m|I've|I\u2019ve|our|we|us)\b", re.I)

# A first-person sentence that reports a single decision or event. The summary is standing:
# what the person does and how they judge it. One occasion is evidence and goes in a bullet.
SUMMARY_EVENT = re.compile(
    r"^I (?:put|moved|fixed|cut|closed|deferred|chose|rebuilt|rewrote|added|removed|shipped|"
    r"launched|introduced|prioritised|prioritized|redesigned|stopped|delayed)\b(?! into)"
    r".*\b(?:ahead of|first|when|after|because|instead of|before)\b", re.I)

IRREGULAR_PAST = {
    "led", "ran", "built", "cut", "took", "brought", "wrote", "won", "grew", "held", "set",
    "made", "gave", "got", "kept", "drove", "chose", "taught", "sold", "spoke", "began",
    "oversaw", "rebuilt", "put", "found", "saw", "met", "paid", "sent", "spent", "stood",
    "told", "withdrew", "rewrote", "undertook", "dealt", "drew", "rose", "split", "spread",
    "struck", "became", "came", "did", "went", "left", "lent", "lost", "read", "rethought",
    "shrank", "sought", "thought", "understood", "overcame", "underwent", "upheld", "hit",
    "let", "bid", "broke", "caught", "fought", "flew", "forecast", "heard", "knew", "laid",
    "learnt", "meant", "outgrew", "overhauled", "reset", "shut", "stuck", "swept", "wound",
    "was", "were", "had",
}

YEARS_COUNT = [
    re.compile(r"\b\d{1,2}\s*\+\s*years?\b", re.I),
    re.compile(r"\b(?:\d{1,2}|ten|fifteen|twenty|twenty-five|thirty)\s+years?['’]?\s+(?:of\s+)?"
               r"(?:experience|service|tenure|expertise|in the|in banking|in financial|"
               r"with the|at the|leading|managing)", re.I),
    re.compile(r"\b(?:over|more than|nearly|almost)\s+(?:a|one|two|three|\d)\s+decades?\b", re.I),
    re.compile(r"\bdecades?\s+of\s+(?:experience|service)\b", re.I),
]
PERSONAL = [
    (re.compile(r"\b(date of birth|d\.?o\.?b\.?)\b", re.I), "date of birth"),
    (re.compile(r"\bborn\s+(?:on\s+|in\s+)?\d", re.I), "birth date"),
    (re.compile(r"\bmarital status\b|\b(married|single|divorced)\b\s*(\||$)", re.I),
     "marital status"),
    (re.compile(r"\bage\s*:\s*\d", re.I), "age"),
    (re.compile(r"\bnationality\s*:", re.I), "nationality"),
    (re.compile(r"\b(gender|religion)\s*:", re.I), "gender or religion"),
    (re.compile(r"!\[[^\]]*\]\("), "an image (a photo does not belong on the résumé)"),
]
CLEARED = re.compile(r"\b(security cleared|probity cleared|police check(ed)?|apra approved|"
                     r"eligible for (all )?(banking|background) checks)\b", re.I)
# Gap markers: [old style], <Missing Thing>, and ==suggested text== the person has not confirmed.
GAP = re.compile(r"\[[^\]\n]{2,}\](?!\()|<[^<>\n/!][^<>\n]{1,70}>|==[^=\n]+==")


def words(text):
    return re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'’.,/-]*", text)


class Report:
    def __init__(self):
        self.errors, self.warns, self.infos = [], [], []

    def error(self, code, msg):
        self.errors.append(f"ERROR {code}: {msg}")

    def warn(self, code, msg):
        self.warns.append(f"WARN  {code}: {msg}")

    def info(self, msg):
        self.infos.append(f"info  {msg}")

    def codes(self):
        return {ln.split()[1].rstrip(":") for ln in self.errors + self.warns}


def canonical(heading):
    h = heading.strip().lower()
    for key, names in SECTION_ALIASES.items():
        if h in names:
            return key
    return None


def parse(text):
    """Split the document into the name, the contact line and a list of sections."""
    lines = text.splitlines()
    doc = {"name": "", "contact": "", "sections": [], "lines": lines}
    cur = None
    seen_h1 = False
    for i, ln in enumerate(lines, 1):
        s = ln.rstrip()
        if s.startswith("# ") and not seen_h1:
            doc["name"], seen_h1 = s[2:].strip(), True
            continue
        if s.startswith("## "):
            cur = {"title": s[3:].strip(), "line": i, "body": []}
            doc["sections"].append(cur)
            continue
        if cur is None:
            if seen_h1 and s.strip() and not doc["contact"]:
                doc["contact"] = s.strip()
            continue
        cur["body"].append((i, s))
    return doc


def roles_of(section):
    """Group an experience section's body into employer headings and roles."""
    roles, cur, employer_intro = [], None, []
    in_employer = False
    for i, s in section["body"]:
        if s.startswith("#### "):
            cur = {"line": i, "head": s[5:].strip(), "paras": [], "bullets": []}
            roles.append(cur)
            in_employer = False
        elif s.startswith("### "):
            roles.append({"line": i, "head": s[4:].strip(), "employer": True,
                          "paras": [], "bullets": []})
            cur = roles[-1]
            in_employer = True
        elif cur is not None and s.startswith("- "):
            cur["bullets"].append((i, s[2:].strip()))
        elif cur is not None and s.strip():
            cur["paras"].append((i, s.strip()))
            if in_employer:
                employer_intro.append(s.strip())
    return roles


def lint(text, voice="first", summary_range=(60, 90), allow_gaps=False, year=None, keep=()):
    r = Report()
    year = year or datetime.date.today().year
    doc = parse(text)
    body_text = "\n".join(doc["lines"])

    # --- name and contact line
    if not doc["name"]:
        r.error("no-name", "the first line should be '# Full Name'")
    if not doc["contact"]:
        r.error("no-contact-line", "no contact line under the name")
    elif re.search(r"\b\d{1,4}\s+[A-Z][a-z]+\s+(Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|"
                   r"Place|Crescent|Parade)\b", doc["contact"]):
        r.error("street-address", "the contact line carries a street address; city and state "
                                  "are enough")

    # --- sections: names and order
    found = []
    for sec in doc["sections"]:
        key = canonical(sec["title"])
        low = sec["title"].strip().lower()
        if low in BANNED_SECTIONS:
            r.error("section-not-wanted", f"line {sec['line']}: section '{sec['title']}' "
                                          "does not belong on the résumé")
        elif low in {"referees", "references"}:
            body = " ".join(s for _, s in sec["body"])
            if re.search(r"\b0\d[\d ]{7,}\b|@", body):
                r.error("referee-details", f"line {sec['line']}: referee contact details are "
                                           "supplied on request, not printed")
        elif key is None:
            r.warn("section-name", f"line {sec['line']}: '{sec['title']}' is not a standard "
                                   "heading a parser maps to a field")
        else:
            found.append((key, sec))
    keys = [k for k, _ in found]
    for need in ("summary", "skills", "experience"):
        if need not in keys:
            r.error("section-missing", f"no {need} section")
    ordered = [k for k in ORDER if k in keys]
    if keys != ordered:
        r.error("section-order", "sections should run summary, key skills, experience, "
                                 f"education; found {', '.join(keys)}")
    sec_of = dict(found)

    # --- summary
    if "summary" in sec_of:
        paras = [s for _, s in sec_of["summary"]["body"] if s.strip()]
        text_s = " ".join(paras)
        n = len(words(text_s))
        lo, hi = summary_range
        if n < lo - 20 or n > hi + 20:
            r.error("summary-length", f"summary is {n} words; the default is {lo} to {hi}")
        elif n < lo or n > hi:
            r.warn("summary-length", f"summary is {n} words; the default is {lo} to {hi}")
        if any(s.startswith("- ") for s in paras):
            r.warn("summary-bullets", "the summary is one paragraph of prose, not bullets")
        if voice == "first" and not re.search(r"\b(I|my|me)\b", text_s):
            r.warn("summary-person", "the summary has no 'I' or 'my'; paragraphs default to "
                                     "the first person (use --voice implied if the person "
                                     "chose otherwise)")
        r.info(f"summary: {n} words")

    # --- key skills
    if "skills" in sec_of:
        lines = [s for _, s in sec_of["skills"]["body"] if s.strip()]
        n = len(lines)
        if n < 2 or n > 5:
            r.warn("skills-lines", f"key skills has {n} line(s); the default is 2 to 4 "
                                   "labelled lines plus a tools line")
        unlabelled = [s for s in lines if not re.match(r"^(- )?[A-Z][A-Za-z ,&/-]{1,40}: ", s)]
        if unlabelled:
            r.warn("skills-label", f"{len(unlabelled)} skills line(s) have no 'Label: ' "
                                   "opening")
        if not any(re.match(r"^(- )?(Tools|Technology|Systems|Tools and systems)", s)
                   for s in lines):
            r.warn("skills-tools", "no Tools line; tools are a list and get their own line")
        for line in lines:
            if re.match(r"^(- )?(Tools|Technology|Systems|Tools and systems)", line):
                continue
            for item in line.split(":", 1)[-1].split(";"):
                toks = item.split()
                if " ".join(toks).lower().strip(" .") in SKILL_GENERIC:
                    r.warn("skill-generic", f"skill '{' '.join(toks)}' is what anyone with the "
                                            "title would list; lead with what this person is "
                                            "unusually good at")
                if len(toks) > 10:
                    r.warn("skill-long", f"skill '{' '.join(toks[:6])}…' is {len(toks)} words; a "
                                         "skill names an ability that carries to another role, "
                                         "and the instance goes in a bullet")
                proper = [t.strip(",.()") for t in toks[1:]
                          if re.match(r"^[A-Z][a-z]{2,}", t) and t.strip(",.()") not in SKILL_PROPER_OK]
                if proper:
                    r.warn("skill-specific", f"skill '{' '.join(toks[:6])}…' names "
                                             f"{', '.join(proper)}; leave out where the ability "
                                             "was used")
        if re.search(r"[█▓▒░●○★☆]|\b\d/5\b|\b\d{1,3}\s?%", " ".join(lines)):
            r.error("skills-ratings", "rating bars, stars or percentages in key skills")

    # --- experience
    all_bullets = []
    if "experience" in sec_of:
        roles = roles_of(sec_of["experience"])
        real_roles = [x for x in roles if not x.get("employer")]
        if not real_roles:
            r.error("no-roles", "no '#### Title | Employer | dates' role lines")
        for x in roles:
            head, line = x["head"], x["line"]
            parts = [p.strip() for p in head.split("|")]
            if not DATE_RANGE.search(head):
                if FULL_MONTH.search(head):
                    r.error("date-format", f"line {line}: write months as three letters, "
                                           "'Mon YYYY – Mon YYYY'")
                else:
                    r.error("date-format", f"line {line}: '{head}' needs dates as "
                                           "'Mon YYYY – Mon YYYY' or '– Present'")
            if not x.get("employer"):
                if len(parts) < 3:
                    r.warn("role-line", f"line {line}: role lines read 'Title | Employer | "
                                        "dates'; repeat the employer on each role")
                if re.search(r"\((promoted|promotion|secondment)[^)]*\)", head, re.I):
                    r.warn("role-line-note", f"line {line}: keep '(promoted)' out of the "
                                             "role line; say it in the employer sentences")
            all_bullets.extend(x["bullets"])
        for idx, x in enumerate(real_roles):
            nb = len(x["bullets"])
            if idx == 0:
                if nb and (nb < 3 or nb > 5):
                    r.warn("bullet-count", f"line {x['line']}: the current role has {nb} "
                                           "bullet(s); the default is 3 to 5")
                if not x["paras"]:
                    r.warn("no-scope", f"line {x['line']}: the current role has no scope "
                                       "paragraph before its bullets")
                scope = " ".join(p for _, p in x["paras"])
                if len(words(scope)) > 45:
                    r.warn("scope-length", f"line {x['line']}: the scope paragraph is "
                                           f"{len(words(scope))} words; the default is under "
                                           "about 35, with the detail in bullets")
            elif nb > 4:
                r.warn("bullet-count", f"line {x['line']}: an earlier role has {nb} bullets; "
                                       "the default is 1 to 4")
        dated = [x for x in real_roles if re.search(r"Present", x["head"])]
        if len(real_roles) == 1 and dated:
            m = re.search(r"(\d{4}) [–-] Present", real_roles[0]["head"])
            if m and year - int(m.group(1)) >= 8:
                r.warn("one-long-role", f"line {real_roles[0]['line']}: one role covering "
                                        f"{year - int(m.group(1))} years; date each role "
                                        "separately")

        # openers: bullets and paragraphs
        for i, b in all_bullets:
            first = re.sub(r"[^A-Za-z'-]", "", b.split()[0]) if b.split() else ""
            low = first.lower()
            if DUTY_OPENERS.match(b):
                r.warn("duty-opener", f"line {i}: '{' '.join(b.split()[:3])}…' describes a "
                                      "duty; a bullet is one thing that happened")
            elif low in BARE_PRESENT and low not in IRREGULAR_PAST - {"set", "cut", "put",
                                                                       "read", "split",
                                                                       "spread", "forecast",
                                                                       "reset", "shut",
                                                                       "hit", "let", "bid"}:
                r.error("bare-present", f"line {i}: bullet opens with the bare verb "
                                        f"'{first}', which reads as a command or a misspelt "
                                        "past tense")
            elif low == "i":
                r.warn("bullet-subject", f"line {i}: bullets open with a past-tense verb, "
                                         "without 'I'")
            elif not (low.endswith("ed") or low in IRREGULAR_PAST):
                r.warn("bullet-opener", f"line {i}: bullet opens with '{first}'; bullets "
                                        "open with a past-tense verb")
            vr = VAGUE_RANGE.search(b)
            if vr:
                r.warn("vague-range", f"line {i}: '{vr.group(0)}' is a range; it reads as few and "
                                      "as unsure. Say the thing without the count, or give the "
                                      "one figure that is impressive")
            if EMPTY_SELL.search(b):
                r.warn("empty-sell", f"line {i}: '{EMPTY_SELL.search(b).group(0)}' sells with an "
                                     "adjective; say what was at stake or what changed instead")
            if ADMIN_END.search(b.strip()):
                r.warn("admin-ending", f"line {i}: the bullet ends on the admin ('"
                                       f"{' '.join(b.strip().split()[-5:])}'); end on what it "
                                       "changed, or ask the person what happened next")
            if len(words(b)) < 14 and not re.search(r"\d", b):
                r.warn("bullet-no-result", f"line {i}: '{' '.join(b.split()[:6])}…' stops at the "
                                           "action; ask the person what was different "
                                           "afterwards, or give the scale of the work")
            if len(words(b)) > 60:
                r.warn("bullet-length", f"line {i}: bullet is {len(words(b))} words; one "
                                        "headline and one supporting fact")
            first_sent = re.split(r"(?<=[.!?])\s+", b.strip())[0]
            if len(first_sent.split()) > 34:
                r.warn("headline-long", f"line {i}: the bullet's first sentence is "
                                        f"{len(first_sent.split())} words; put the point in "
                                        "about 30 and move the rest down or out")
            if len(LIST_IN_BULLET.findall(b)) >= 2:
                r.warn("bullet-lists", f"line {i}: the bullet carries two or more lists; rank "
                                       "the detail and keep the one that matters")
        for x in roles:
            for i, p in x["paras"]:
                if voice == "first":
                    for sent in re.split(r"(?<=[.!?])\s+", p.strip()):
                        if len(sent.split()) > 4 and not FIRST_PERSON.search(sent):
                            r.warn("impersonal-prose", f"line {i}: '{' '.join(sent.split()[:6])}…' "
                                                       "has no 'I', 'my' or 'our'; say it as the "
                                                       "person would, or fold it into a sentence "
                                                       "that is about them")
                first = re.sub(r"[^A-Za-z'-]", "", p.split()[0]).lower() if p.split() else ""
                if first in BARE_PRESENT and len(p.split()) > 3:
                    r.error("bare-present", f"line {i}: paragraph opens with the bare verb "
                                            f"'{p.split()[0]}'; write 'I {first}…' or recast")
    if "summary" in sec_of:
        for i, p in sec_of["summary"]["body"]:
            for sent in re.split(r"(?<=[.!?])\s+", p.strip()):
                if not sent:
                    continue
                first = re.sub(r"[^A-Za-z'-]", "", sent.split()[0]).lower()
                if first in BARE_PRESENT and len(sent.split()) > 3:
                    r.error("bare-present", f"line {i}: a summary sentence opens with the "
                                            f"bare verb '{sent.split()[0]}'")
                    break
                if LABEL_OPENER.search(sent):
                    r.warn("label-opener", f"line {i}: '{' '.join(sent.split()[:6])}…' opens with a "
                                           "title; say what the person is responsible for")
                if FIGURE_ON_OBJECT.search(sent):
                    r.warn("figure-on-object", f"line {i}: a figure describes the product or team "
                                               "('which has…', 'used by…'); attach it to what the "
                                               "person is responsible for")
                if not FIRST_PERSON.search(sent) and len(sent.split()) > 4:
                    r.warn("not-about-person", f"line {i}: '{' '.join(sent.split()[:6])}…' has no "
                                               "'I' or 'my'; a summary sentence is about the person")
                if SUMMARY_EVENT.search(sent):
                    r.warn("summary-event", f"line {i}: a summary sentence reports one occasion "
                                            f"('{' '.join(sent.split()[:6])}…'); say what the work "
                                            "turns on and leave the occasion to a bullet")

    # --- the same story told in full twice
    if "summary" in sec_of and "experience" in sec_of:
        sw = [w.lower().strip(".,;:") for _, s_ in sec_of["summary"]["body"] for w in s_.split()]
        ex = " ".join(w.lower().strip(".,;:") for _, s_ in sec_of["experience"]["body"]
                      for w in s_.split())
        # A required term named in the summary and shown in a role shares words by design, so
        # only a long run counts as the same story told twice.
        for k in range(len(sw) - 11):
            run = " ".join(sw[k:k + 12])
            if run in ex:
                r.warn("told-twice", f"the summary and the experience share the words '{run}'; "
                                     "tell it once, in the experience")
                break

    # --- education
    if "education" in sec_of:
        lines = [(i, s) for i, s in sec_of["education"]["body"] if s.strip()]
        if not lines:
            r.error("education-empty", "the education section is empty; leave it out when "
                                       "there is nothing to list")
        for i, s in lines:
            if re.search(r"\b(Bachelor|Master|Diploma|Degree|BA|BSc|BCom|MBA|Graduate "
                         r"Certificate)\b", s):
                for y in re.findall(r"\b(19\d{2}|20\d{2})\b", s):
                    if year - int(y) > 10:
                        r.warn("graduation-year", f"line {i}: a graduation year of {y} is "
                                                  "an age signal; leave it off")

    # --- whole-document checks
    for i, ln in enumerate(doc["lines"], 1):
        for rx in YEARS_COUNT:
            m = rx.search(ln)
            if m:
                r.error("years-count", f"line {i}: '{m.group(0)}' counts years; the dates "
                                       "already show the tenure")
                break
        for rx, what in PERSONAL:
            if rx.search(ln):
                r.error("personal-detail", f"line {i}: {what} does not belong on the résumé")
        if SECOND_VERB.search(ln):
            r.warn("two-readings", f"line {i}: after 'use … to …', a second verb joined by 'and' "
                                   "reads as the tool doing it; say who does it and when "
                                   "('then … myself')")
        g = KNOWN_GLOSS.search(ln)
        if g:
            r.warn("gloss-known", f"line {i}: '{g.group(0).strip()}' explains something the "
                                  "reader already knows; name it and move on")
        if AWARD.search(ln):
            for sent in re.split(r"(?<=[.!?])\s+", ln):
                if AWARD.search(sent) and not re.search(r"\bfor\b", sent.split("ward", 1)[-1]):
                    r.warn("award-bare", f"line {i}: an award is named without what it was for; "
                                         "ask the person what it recognised and what they did "
                                         "towards it")
                    break
        m = CLEARED.search(ln)
        if m:
            r.warn("cleared-claim", f"line {i}: '{m.group(0)}'; employers run their own "
                                    "checks, so this claims nothing")
        if re.match(r"^\s*\|.*\|\s*$", ln) and not ln.lstrip().startswith("#"):
            if re.search(r"\|\s*:?-{3,}", ln) or ln.count("|") >= 3 and i > 3:
                r.error("table", f"line {i}: a table; parsers lose text in tables")
        low = ln.lower()
        for c in CLICHES:
            if re.search(rf"(?<![a-z-]){re.escape(c)}(?![a-z-])", low):
                r.error("generic-register", f"line {i}: '{c}' reads as generic; say what "
                                            "happened instead")
                break
        if not ln.startswith("#") and FULL_MONTH.search(ln) and DATE_RANGE.search(ln) is None \
                and re.search(r"[–-]\s*(Present|\w+ \d{4})", ln):
            r.warn("date-format", f"line {i}: use three-letter months in date ranges")

    gaps = [(i, m.group(0)) for i, ln in enumerate(doc["lines"], 1) for m in GAP.finditer(ln)]
    if gaps:
        msg = f"{len(gaps)} gap marker(s), first at line {gaps[0][0]}: {gaps[0][1][:60]}"
        if allow_gaps:
            r.warn("gaps", msg + "; a document with gaps goes to the person, not an employer")
        else:
            r.error("gaps", msg + "; resolve them, or pass --allow-gaps for a draft")

    total = len(words(re.sub(r"^#+ ", "", body_text, flags=re.M)))
    r.info(f"{total} words, {len(all_bullets)} bullets")
    if total > 1100:
        r.warn("length", f"{total} words is more than two pages usually hold at 11pt")
    low_text = re.sub(r"\s+", " ", text.lower())
    for term in keep:
        if term.lower() not in low_text:
            r.error("kept-term-missing", f"'{term}' is on the keep list and is not in the "
                                         "résumé; the person asked for it or the ad requires "
                                         "it, so a later edit should not have removed it")

    return r


def run_self_test():
    here = os.path.dirname(os.path.abspath(__file__))
    tests = os.path.join(here, "..", "tests")
    good = open(os.path.join(tests, "good.md"), encoding="utf-8").read()
    bad = open(os.path.join(tests, "bad.md"), encoding="utf-8").read()
    ok = True
    rg = lint(good, year=2026)
    if rg.errors:
        ok = False
        print("FAIL good.md should have no errors:")
        print("\n".join(rg.errors))
    else:
        print(f"ok   good.md: 0 errors, {len(rg.warns)} warning(s)")
    rb = lint(bad, year=2026)
    expected = {"years-count", "personal-detail", "bare-present", "generic-register",
                "date-format", "section-not-wanted", "education-empty", "gaps",
                "summary-length", "section-order", "referee-details", "duty-opener",
                "role-line", "skills-ratings", "table", "street-address"}
    missing = expected - rb.codes()
    if missing:
        ok = False
        print("FAIL bad.md did not raise: " + ", ".join(sorted(missing)))
    else:
        print(f"ok   bad.md: all {len(expected)} expected checks fired "
              f"({len(rb.errors)} errors, {len(rb.warns)} warnings)")
    spec = "finding what customers are stuck on from call and claims data in the Harbour claims system"
    r_sk = lint(good.replace("finding where customers get stuck, from data and frontline staff", spec, 1), year=2026)
    r_gen = lint(good.replace("coaching frontline staff into senior roles", "leading teams", 1), year=2026)
    if "skill-generic" not in r_gen.codes() or "skill-generic" in rg.codes():
        ok = False
        print("FAIL skill-generic: should fire on an item anyone with the title would list")
    else:
        print("ok   skill-generic fires on an item anyone with the title would list")
    want_sk = {"skill-long", "skill-specific"}
    if not want_sk <= r_sk.codes() or want_sk & rg.codes():
        ok = False
        print("FAIL skill-long/skill-specific: should fire on a skill that describes one job only")
    else:
        print("ok   skill-long and skill-specific fire on a skill that describes one job only")
    lab = "I am the Product Owner for the claims lodgement journey, used by about 9,000 customers a month."
    r_lab = lint(good.replace("As Product Owner for claims lodgement at Harbour Mutual, I am responsible for how about 9,000 customers a month lodge a claim.", lab, 1), year=2026)
    want = {"label-opener", "figure-on-object"}
    if not want <= r_lab.codes() or want & rg.codes():
        ok = False
        print("FAIL label-opener/figure-on-object: should fire on a title-and-statistic opening only")
    else:
        print("ok   label-opener and figure-on-object fire on a title-and-statistic opening only")
    ph = good.replace("was promoted twice", "was promoted twice for <what the promotions recognised>", 1)
    if "gaps" in lint(ph, year=2026).codes() and not lint(ph, year=2026, allow_gaps=True).errors:
        print("ok   an angle-bracket placeholder is an error, and a warning with --allow-gaps")
    else:
        ok = False
        print("FAIL gaps: <placeholder> should fail the lint unless --allow-gaps is given")
    sg = good.replace("was promoted twice", "was promoted ==twice==", 1)
    if "gaps" in lint(sg, year=2026).codes() and not lint(sg, year=2026, allow_gaps=True).errors:
        print("ok   an unconfirmed ==suggestion== is an error, and a warning with --allow-gaps")
    else:
        ok = False
        print("FAIL gaps: ==suggestion== should fail the lint unless --allow-gaps is given")
    vg = good.replace("- Coached 3 assessors into senior roles.", "- Coordinated 5 to 10 changes to the claims process for 12 assessors.", 1)
    if "vague-range" in lint(vg, year=2026).codes() and "vague-range" not in rg.codes():
        print("ok   vague-range fires on '5 to 10 changes', and not on good.md")
    else:
        ok = False
        print("FAIL vague-range: should fire on a range in a bullet only")
    li = good.replace("- Coached 3 assessors into senior roles.", "- Coordinated changes to access, onboarding, processes and transitions, managing milestones, dependencies, risks and issues for 3 teams.", 1)
    if "bullet-lists" in lint(li, year=2026).codes() and "bullet-lists" not in rg.codes():
        print("ok   bullet-lists fires on a bullet carrying two lists, and not on good.md")
    else:
        ok = False
        print("FAIL bullet-lists: should fire on two lists in one bullet only")
    ad = good.replace("- Coached 3 assessors into senior roles.", "- Successfully brought 3 teams together, agreed who owned what and tracked it in Jira.", 1)
    if {"empty-sell", "admin-ending"} <= lint(ad, year=2026).codes() and not ({"empty-sell", "admin-ending"} & rg.codes()):
        print("ok   empty-sell and admin-ending fire on an adjective and an admin ending only")
    else:
        ok = False
        print("FAIL empty-sell/admin-ending: should fire on the mutated bullet and not on good.md")
    nr = good.replace("- Coached 3 assessors into senior roles.", "- Brought the two teams under one way of working.", 1)
    if "bullet-no-result" in lint(nr, year=2026).codes() and "bullet-no-result" not in rg.codes():
        print("ok   bullet-no-result fires on a bullet that stops at the action, and not on good.md")
    else:
        ok = False
        print("FAIL bullet-no-result: should fire on a short bullet with no figure only")
    tw = "I started as a claims assessor. I use Jira to draft the release notes, and check them before release."
    r_tw = lint(good.replace("I started as a claims assessor", tw, 1), year=2026)
    r_tw2 = lint(good.replace("I started as a claims assessor", tw.replace(", and check them", ", then check them myself"), 1), year=2026)
    if "two-readings" in r_tw.codes() and "two-readings" not in r_tw2.codes():
        print("ok   two-readings fires on 'use X to draft …, and check …' and not on the 'then' form")
    else:
        ok = False
        print("FAIL two-readings: should fire on the 'and' form only")
    gl = "I started as a claims assessor. I track work in Jira, a ticketing tool, each week."
    r_gl = lint(good.replace("I started as a claims assessor", gl, 1), year=2026)
    if "gloss-known" in r_gl.codes() and "gloss-known" not in rg.codes():
        print("ok   gloss-known fires on a gloss of a widely known product, and not on good.md")
    else:
        ok = False
        print("FAIL gloss-known: should fire on 'Jira, a ticketing tool' and not on good.md")
    aw = "I started as a claims assessor. I am proud that our team received the 2025 Service Award."
    r_aw = lint(good.replace("I started as a claims assessor", aw, 1), year=2026)
    aw2 = aw.replace("Award.", "Award for cutting duplicate claims.")
    r_aw2 = lint(good.replace("I started as a claims assessor", aw2, 1), year=2026)
    if "award-bare" in r_aw.codes() and "award-bare" not in r_aw2.codes():
        print("ok   award-bare fires on an award with no 'for', and not once it says what for")
    else:
        ok = False
        print("FAIL award-bare: should fire only when the award line does not say what it was for")
    imp = "I started as a claims assessor. The lodgement project received the 2025 team award."
    r_imp = lint(good.replace("I started as a claims assessor", imp, 1), year=2026)
    if "impersonal-prose" in r_imp.codes() and "impersonal-prose" not in rg.codes():
        print("ok   impersonal-prose fires on a record-style sentence in a prose paragraph only")
    else:
        ok = False
        print("FAIL impersonal-prose: should fire on a record-style sentence, and not on good.md")
    r_keep = lint(good, year=2026, keep=["acceptance criteria", "a term that is not there"])
    if r_keep.codes() & {"kept-term-missing"} and len([e for e in r_keep.errors if "kept-term" in e]) == 1:
        print("ok   --keep reports a missing term and accepts a present one")
    else:
        ok = False
        print("FAIL --keep: should report exactly the one missing term")
    ev = "I put a duplicate-claims fix first when call data showed lodgements made twice."
    r_ev = lint(good.replace("Most of my work is deciding which customer problem gets fixed first, from what the call data shows.", ev, 1), year=2026)
    if "summary-event" not in r_ev.codes() or "summary-event" in rg.codes():
        ok = False
        print("FAIL summary-event: should fire on one occasion in the summary, and only then")
    else:
        print("ok   summary-event fires on one occasion in the summary and not on good.md")
    r3 = lint(good.replace("I am the", "Am the", 1) + "\n", voice="implied", year=2026)
    print("ok   --voice implied accepted" if "summary-person" not in r3.codes()
          else "FAIL --voice implied still warns")
    ok = ok and "summary-person" not in r3.codes()
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--voice", choices=["first", "implied"], default="first",
                    help="person used in paragraphs (default: first)")
    ap.add_argument("--summary-words", default="60-90",
                    help="accepted summary length as min-max (default 60-90)")
    ap.add_argument("--allow-gaps", action="store_true",
                    help="report <placeholder>, ==suggestion== and [gap] markers as warnings, for a draft going to the person")
    ap.add_argument("--keep", metavar="FILE",
                    help="a file of terms that must stay in the résumé, one per line: words "
                         "the person asked for and the ad's required phrases they hold")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(run_self_test())
    if not a.files:
        ap.error("give a résumé file, or --self-test")
    lo, hi = (int(x) for x in a.summary_words.split("-"))
    keep = []
    if a.keep:
        keep = [ln.strip() for ln in open(a.keep, encoding="utf-8")
                if ln.strip() and not ln.startswith("#")]
    status = 0
    for path in a.files:
        text = open(path, encoding="utf-8").read()
        r = lint(text, voice=a.voice, summary_range=(lo, hi), allow_gaps=a.allow_gaps, keep=keep)
        print(f"== {path}")
        for ln in r.errors + r.warns + r.infos:
            print(ln)
        print(f"RESULT: {len(r.errors)} error(s), {len(r.warns)} warning(s)")
        if r.warns:
            print("A warning is a prompt to read the line against its section's job. Change the "
                  "line only if it fails that job; do not edit to clear the warning.")
        if r.errors:
            status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
