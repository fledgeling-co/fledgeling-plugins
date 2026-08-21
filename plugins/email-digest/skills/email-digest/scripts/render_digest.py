#!/usr/bin/env python3
"""render_digest.py - compile a tiered digest email from a JSON payload.

Emits a table-based HTML part and a plain-text part. Everything it does is a
consequence of a rule in references/evidence.md; the ones that shape the output
most are worth naming here because they are the ones a reader will want to
argue with:

  * There is no item cap. The tiers absorb volume instead. MailerLite's 317,000
    campaigns put the 21+ link bucket at the highest click-to-open rate in the
    dataset, and the choice-overload meta-analysis pools to roughly zero, so
    truncating the list fixes a defect nobody has measured while removing
    content somebody asked for.
  * Three tiers, and the split is not arbitrary. Kong et al. is the only causal
    evidence in the corpus: featuring relevant items raised their detail-reading
    from 13% to 22%, while reordering everything below the featured block did
    nothing significant. So prominence is worth spending on and ranking the tail
    is not, which is exactly a small featured set over a compressed remainder.
  * The summary is three highlights and category counts, linking outward. Not a
    contents list, which recreates the flat list, and never anchored, because
    anchors do not act on iOS and Apple is 62.26% of opens. A highlight may be
    several parts, so one line can name the work in plain text and still send
    the reader to each destination it mentions.
  * Every headline is a text node beside its image, never inside it.

Usage:
    python3 render_digest.py payload.json --out-html mail.html --out-text mail.txt

Payload shape: see references/payload.md, or run with --example to print one.
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import sys

# Near-black and near-white rather than pure values: Outlook.com's partial
# inversion targets #000000 and #FFFFFF specifically rather than reacting to
# lightness, so these sidestep it. Overridable per brand.
DEFAULT_PALETTE = {
    "paper":   "#F5F3EF",
    "surface": "#FBFAF8",
    "ink":     "#24221E",
    "muted":   "#5C574E",
    "hairline": "#E0DBD2",
    "accent":  "#A44E20",
    "codebg":  "#EDEAE3",
}

# Every stack ends web-safe, because Outlook falls back to Times New Roman
# rather than to the next font in the stack.
#
# The named face at the head of each is the project's own, linked from Google
# Fonts in the head. It loads in Apple Mail and iOS Mail, which is 62.26% of
# opens; Gmail ignores the link and takes the fallback, which is why the
# fallback has to be a face somebody chose rather than whatever came next.
# Override the whole set through brand.fonts when the project's are different.
#
# Single quotes inside every stack, and that is load-bearing rather than a
# style preference: these end up in a `style="..."` attribute, so one double
# quote inside a family name closes the attribute and silently discards every
# declaration after it. It cost this renderer a version - the whole email fell
# back to Times, and `fonts:fallback` still passed because it read the raw
# text rather than the parsed attribute. `css:quoted-family` gates it now.
DEFAULT_FONTS = {
    "sans":  ("'Instrument Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', "
              "Roboto, Helvetica, Arial, sans-serif"),
    "serif": "Newsreader, Georgia, 'Times New Roman', Times, serif",
    "mono":  ("'IBM Plex Mono', ui-monospace, 'SF Mono', Menlo, Consolas, "
              "'Courier New', monospace"),
    # Hidden from Outlook by a downlevel-revealed comment: the Word engine
    # cannot use a linked web font and has been observed to mis-handle the tag.
    "link": ("https://fonts.googleapis.com/css2?family=Newsreader:wght@400;600"
             "&family=Instrument+Sans:wght@400;500;600"
             "&family=IBM+Plex+Mono:wght@400;500&display=swap"),
}
SANS = DEFAULT_FONTS["sans"]
SERIF = DEFAULT_FONTS["serif"]
MONO = DEFAULT_FONTS["mono"]

WIDTH = 600


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def assign_tiers(items: list[dict], featured: int = 2, spotlight: int = 3) -> list[dict]:
    """Explicit tier wins; otherwise fall to position.

    Featuring is the only lever with causal evidence, and that evidence is
    conditional on the featured items being *relevant*. Position is a proxy for
    relevance and a weak one, so a caller that knows better should say so by
    setting `tier` on the item."""
    out = []
    auto = [i for i in items if not i.get("tier")]
    n_f = sum(1 for i in items if i.get("tier") == "featured")
    for item in items:
        t = item.get("tier")
        if not t:
            if n_f < featured:
                t, n_f = "featured", n_f + 1
            elif sum(1 for o in out if o["tier"] == "spotlight") < spotlight:
                t = "spotlight"
            else:
                t = "oneline"
        out.append({**item, "tier": t})
    return out


def cell(content: str, pad: str = "0 32px", tier: str = "") -> str:
    """The tier marker is emitted for the gate to read, not for styling.

    Without it lint_email.py cannot see the tiers at all, and every tier rule
    plus the prose-intro rule silently measures nothing while still printing a
    verdict. That failure mode is the reason the marker is data rather than a
    class somebody could rename during a restyle."""
    t = f' data-tier="{tier}"' if tier else ""
    return (f'<tr{t}><td align="left" style="padding:{pad};font-family:{SANS};'
            f'text-align:left;">{content}</td></tr>')


def render_featured(it: dict, p: dict) -> str:
    """Large treatment: headline, then banner, then the claim.

    The headline leads rather than following the banner. Under the banner it sat
    a full image-height away from the section heading that introduced it, and
    with images blocked it moved again, so the reader met the artwork before
    they met the thing it was for. Above it, the headline is the first text in
    the card in both states.

    It is a text node either way, never the image's alt: the banner's failure
    modes (blocked, broken, alt clipped to the image width, alt unstylable in
    Outlook) all land on the same element and take the AI-generated inbox
    summary with them."""
    banner = ""
    if it.get("bannerUrl"):
        # Deliberately not wrapped in a link. Its only content would be an
        # alt="" image, which gives the link no accessible name, and the
        # headline above and the button below already point at the same URL. A
        # redundant link with no name is worse than no link.
        banner = (
            f'<img src="{esc(it["bannerUrl"])}" width="{WIDTH - 64}" '
            f'height="{int((WIDTH - 64) * 0.325)}" alt="" class="banner" '
            f'style="display:block;width:100%;max-width:{WIDTH - 64}px;border:0;'
            f'border-radius:8px;" />'
            f'<div style="height:18px;line-height:18px;">&nbsp;</div>')
    inst = it.get("install")
    # A command string still renders as a code block above the actions, because
    # it is a thing to copy rather than a thing to press.
    command = ""
    if inst and not isinstance(inst, dict):
        command = (
            f'<div style="margin:0 0 14px;padding:11px 13px;background:{p["codebg"]};'
            f'border-radius:7px;font-family:{MONO};font-size:13px;line-height:1.5;'
            f'color:{p["ink"]};word-break:break-word;">{esc(inst)}</div>')
    return cell(
        f'<h2 style="margin:0 0 13px;font-family:{SERIF};font-size:23px;line-height:1.28;'
        f'font-weight:700;color:{p["ink"]};mso-line-height-rule:exactly;">'
        f'<a href="{esc(it["url"])}" style="color:{p["ink"]};text-decoration:none;">'
        f'{esc(it.get("headline") or it["title"])}</a></h2>'
        f'{banner}'
        f'<p style="margin:0 0 14px;font-size:16px;line-height:1.6;color:{p["ink"]};">'
        f'{esc(it.get("body",""))}</p>'
        f'{command}'
        f'{actions(it, p)}',
        pad="0 32px 30px", tier="featured")

def actions(it: dict, p: dict) -> str:
    """One primary action, one subordinate, on a single row.

    Two calls to action stacked as separate rows read as a list of two similar
    choices, which is the shape one-primary-action exists to prevent. The reader
    of a digest is deciding whether this is worth their attention, not deciding
    to install: the skill's own page is the primary and the install route is the
    secondary, and the difference is carried by fill rather than by order.

    The accent appears once per card as a result. A second accent-coloured link
    beside a filled accent button is two claims on the same emphasis, so the
    secondary demotes to the muted foreground with an underline, which is what a
    link looks like when a button already has the accent.

    Side by side means a two-cell table here: Outlook has no flex, and
    `display:inline-block` on the second element is not reliable enough in the
    Word engine to hang a layout on. Under 620px the second cell becomes a block
    so the pair stacks rather than colliding at 375px."""
    primary = (
        f'<a href="{esc(it["url"])}" style="display:inline-block;background:{p["accent"]};'
        f'color:#FDFBF8;font-size:15px;font-weight:600;line-height:16px;padding:14px 20px;'
        f'border-radius:7px;text-decoration:none;">Read what {esc(it["title"])} does &rarr;</a>')
    inst = it.get("install")
    if not (isinstance(inst, dict) and inst.get("label")):
        return primary
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
        f'<td class="act" valign="middle" style="font-family:{SANS};">{primary}</td>'
        f'<td class="act" valign="middle" style="padding-left:18px;font-family:{SANS};'
        f'font-size:14px;line-height:1.5;">'
        f'<a href="{esc(inst.get("url",""))}" style="color:{p["muted"]};'
        f'text-decoration:underline;">{esc(inst["label"])}</a></td>'
        f'</tr></table>')


SPOT_COL = 168      # 3 x 168 + 2 x 16 gutter = 536, the card's inner width
SPOT_GUTTER = 16
SPOT_ICON = 112

def render_spotlight_row(items: list[dict], p: dict) -> str:
    """The middle tier, three across in one row, each led by a large icon.

    An icon rather than a banner here, and the reason is the column: a banner is
    a wide crop, and a wide crop at 168px is a strip of colour with an
    illegible wordmark inside it. An icon is drawn to survive being small, so at
    112px it still reads as the thing it depicts. The banner keeps the featured
    tier, where the column is wide enough for it to mean something.

    Each column carries its own `data-tier`, because the gate counts tier
    markers rather than rows; one marker on the row would report a three-item
    tier as one and every count below it would be wrong.

    A real table with pixel widths rather than anything modern: Outlook renders
    through the Word engine, which has no flex and no grid but lays a table out
    correctly. The media query collapses the columns to full width on a narrow
    screen, and the clients that ignore it are the desktop ones with the room."""
    cols = []
    for n, it in enumerate(items):
        icon = ""
        if it.get("iconUrl"):
            icon = (
                f'<img src="{esc(it["iconUrl"])}" width="{SPOT_ICON}" '
                f'height="{SPOT_ICON}" alt="" class="spot-icon" '
                f'style="display:block;width:{SPOT_ICON}px;height:{SPOT_ICON}px;'
                f'max-width:100%;border:0;" />'
                f'<div style="height:12px;line-height:12px;">&nbsp;</div>')
        cols.append(
            f'<td class="col" data-tier="spotlight" width="{SPOT_COL}" valign="top" '
            f'style="width:{SPOT_COL}px;font-family:{SANS};text-align:left;">'
            f'{icon}'
            f'<h3 style="margin:0 0 4px;font-family:{SERIF};font-size:17px;line-height:1.28;'
            f'font-weight:600;color:{p["ink"]};mso-line-height-rule:exactly;">'
            f'<a href="{esc(it["url"])}" style="color:{p["ink"]};text-decoration:none;">'
            f'{esc(it["title"])}</a></h3>'
            f'<p style="margin:0;font-size:13px;line-height:1.5;color:{p["muted"]};">'
            f'{esc(it.get("headline") or it.get("body",""))[:110]}</p>'
            f'</td>')
        if n < len(items) - 1:
            cols.append(f'<td class="gut" width="{SPOT_GUTTER}" '
                        f'style="width:{SPOT_GUTTER}px;font-size:0;line-height:0;">&nbsp;</td>')
    return cell(
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'width="100%"><tr>{"".join(cols)}</tr></table>',
        pad="0 32px 26px")

RESEARCH_COL = 260      # 2 x 260 + 16 gutter = 536, the card's inner width
RESEARCH_GUTTER = 16
RESEARCH_IMG_H = 110

# A dark inset by default, because this tier is a different class of thing from
# the items around it and the quickest way to say so is to stop matching them.
# Override it with `research.palette` to whatever the research actually looks
# like where it is published; a tile that does not resemble the page it leads to
# is a worse tile than a plain one.
DEFAULT_RESEARCH_PALETTE = {
    "ground": "#0E1013",
    "ink":    "#E9E7E2",
    "muted":  "#A8ADB4",
    "meta":   "#767D86",
    "accent": "#3EBBAE",
}

def render_research_row(block: dict, p: dict) -> str:
    """Long-form background reading, two tiles across, on their own ground.

    Two rather than three. The tile has to carry a headline and a sentence of
    what was found, and at the three-across width of 168px that sentence sets
    to four or five words a line. Two columns of 260px is the widest this card
    goes without dropping to one, and one tile reads as an orphan rather than a
    section.

    The ground colour sits on the cell, never on the image. A tile whose dark
    field arrives as artwork turns into light-on-paper the moment images are
    blocked, which is a meaningful share of Outlook and every reader who has not
    tapped "load images" yet. Everything textual here is live text for the same
    reason: with the image gone the tile still says what the research found.

    The image is decorative and carries `alt=""`. The title beneath it is the
    accessible name, and it is a link rather than a caption because the whole
    point of the tier is to send the reader somewhere longer."""
    rp = {**DEFAULT_RESEARCH_PALETTE, **(block.get("palette") or {})}
    cols = []
    items = block.get("items", [])
    for n, it in enumerate(items):
        img = ""
        if it.get("imageUrl"):
            img = (
                f'<tr><td style="font-size:0;line-height:0;">'
                f'<img src="{esc(it["imageUrl"])}" width="{RESEARCH_COL}" '
                f'height="{RESEARCH_IMG_H}" alt="" '
                f'style="display:block;width:{RESEARCH_COL}px;'
                f'height:{RESEARCH_IMG_H}px;max-width:100%;border:0;" />'
                f'</td></tr>')
        slug = (f'<p style="margin:0 0 7px;font-family:{MONO};font-size:11px;'
                f'line-height:1.4;letter-spacing:0.04em;color:{rp["accent"]};">'
                f'{esc(it["slug"])}</p>') if it.get("slug") else ""
        meta = (f'<p style="margin:0;font-family:{MONO};font-size:11px;'
                f'line-height:1.5;color:{rp["meta"]};">{esc(it["meta"])}</p>'
                ) if it.get("meta") else ""
        cols.append(
            f'<td class="col" width="{RESEARCH_COL}" valign="top" '
            f'style="width:{RESEARCH_COL}px;font-family:{SANS};text-align:left;">'
            f'<table role="presentation" data-block="research" cellpadding="0" '
            f'cellspacing="0" border="0" width="100%" bgcolor="{rp["ground"]}" '
            f'style="width:100%;background-color:{rp["ground"]};'
            f'border-top:3px solid {rp["accent"]};border-radius:0 0 10px 10px;">'
            f'{img}'
            f'<tr><td valign="top" style="padding:15px 17px 17px;'
            f'font-family:{SANS};text-align:left;">'
            f'{slug}'
            f'<h3 style="margin:0 0 8px;font-family:{SERIF};font-size:17px;'
            f'line-height:1.3;font-weight:600;color:{rp["ink"]};'
            f'mso-line-height-rule:exactly;">'
            f'<a href="{esc(it["url"])}" style="color:{rp["ink"]};'
            f'text-decoration:none;">{esc(it["title"])}</a></h3>'
            f'<p style="margin:0 0 12px;font-size:13px;line-height:1.55;'
            f'color:{rp["muted"]};">{esc(it.get("summary",""))}</p>'
            f'{meta}'
            f'</td></tr></table></td>')
        if n < len(items) - 1:
            cols.append(f'<td class="gut" width="{RESEARCH_GUTTER}" '
                        f'style="width:{RESEARCH_GUTTER}px;font-size:0;'
                        f'line-height:0;">&nbsp;</td>')
    return cell(
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'width="100%"><tr>{"".join(cols)}</tr></table>',
        pad="0 32px 26px")

TAIL_ICON = 24

def render_oneline(items: list[dict], p: dict) -> str:
    """Title plus a short tag, an icon per row, grouped under category headings.

    Primary links sit left: Kumar and Salo's peer-reviewed analysis found
    newsletter click-through follows a U-pattern with left-region links
    outperforming right, which is the one position finding measured in email
    rather than borrowed from the web.

    The icon is decorative and carries `alt=""`. It is a two-cell row rather
    than a floated image because the Word engine does not float reliably, and
    the text cell has to hold its own left edge when the title wraps. Point it
    at a small derivative: a tail of eighteen rows aimed at 256px card icons
    costs the recipient most of a megabyte to render a 24px square."""
    groups: dict[str, list[dict]] = {}
    for it in items:
        groups.setdefault(it.get("group") or "More", []).append(it)
    out = []
    for name, rows in groups.items():
        out.append(
            f'<h3 style="margin:0 0 10px;font-family:{MONO};font-size:11px;'
            f'letter-spacing:0.12em;text-transform:uppercase;font-weight:400;'
            f'color:{p["muted"]};mso-line-height-rule:exactly;">{esc(name)}</h3>')
        lis = ""
        for r in rows:
            icon = (f'<img src="{esc(r["iconUrl"])}" width="{TAIL_ICON}" '
                    f'height="{TAIL_ICON}" alt="" '
                    f'style="display:block;width:{TAIL_ICON}px;height:{TAIL_ICON}px;'
                    f'border:0;" />') if r.get("iconUrl") else "&nbsp;"
            # Non-breaking spaces around the separator: a plain space after an
            # inline link collapses against the link box in several clients and
            # the dot ends up welded to the title.
            tag = (f'<span style="color:{p["muted"]};">&nbsp;&middot;&nbsp;'
                   f'{esc(r.get("oneline") or "")}</span>') if r.get("oneline") else ""
            lis += (
                f'<tr>'
                f'<td width="{TAIL_ICON}" valign="top" '
                f'style="width:{TAIL_ICON}px;padding:0 12px 11px 0;font-size:0;'
                f'line-height:0;">{icon}</td>'
                f'<td valign="top" style="padding:0 0 11px;font-family:{SANS};'
                f'font-size:15px;line-height:1.5;color:{p["ink"]};">'
                f'<a href="{esc(r["url"])}" style="color:{p["ink"]};'
                f'text-decoration:underline;">{esc(r["title"])}</a>{tag}</td>'
                f'</tr>')
        out.append(f'<table role="presentation" cellpadding="0" cellspacing="0" '
                   f'border="0" width="100%">{lis}</table>'
                   f'<div style="height:14px;line-height:14px;">&nbsp;</div>')
    return cell("".join(out), pad="0 32px 12px", tier="oneline")


def render(payload: dict) -> tuple[str, str]:
    p = {**DEFAULT_PALETTE, **(payload.get("brand", {}).get("palette") or {})}
    brand = payload.get("brand", {})
    fonts = {**DEFAULT_FONTS, **(brand.get("fonts") or {})}
    global SANS, SERIF, MONO
    SANS, SERIF, MONO = fonts["sans"], fonts["serif"], fonts["mono"]
    issue = payload.get("issue", {})
    items = assign_tiers(payload["items"],
                         featured=payload.get("featured", 2),
                         spotlight=payload.get("spotlight", 3))
    fe = [i for i in items if i["tier"] == "featured"]
    co = [i for i in items if i["tier"] == "spotlight"]
    ol = [i for i in items if i["tier"] == "oneline"]

    research = payload.get("research") or {}
    rs = research.get("items") or []

    summary = payload.get("summary", {})
    highlights = (summary.get("highlights") or [])[:3]
    def hl_body(h: dict) -> str:
        """A highlight is one link, or several parts of which some are links.

        The multi-part form exists so a line can name the thing that was worked
        on in plain text and still send the reader somewhere real. Every link
        points outward at its own destination; none of them is an anchor, which
        would not act at all on the platform holding 62.26% of opens."""
        parts = h.get("parts") or [h]
        out = []
        for part in parts:
            t = esc(part.get("text", ""))
            # The linked name carries the weight, so a reader scanning the block
            # lands on the destination rather than on the sentence around it.
            out.append(f'<a href="{esc(part["url"])}" style="color:{p["ink"]};'
                       f'font-weight:600;">{t}</a>' if part.get("url") else t)
        return "".join(out)

    # No bullet glyphs. A bulleted trio reads as three items to work through;
    # the same three lines set as statements on a tinted ground read as one
    # summary the reader can take in and move past, which is the job.
    #
    # What it must not become is a prose paragraph. NN/g measured 67% of readers
    # with zero fixations on a three-line intro, and that finding indicts prose
    # specifically: separate short lines are the object the same heatmaps show
    # people reading. So this changes the register and keeps the shape.
    hl = "".join(
        f'<tr><td class="summary" style="padding:0 0 9px;font-family:{SANS};'
        f'font-size:15px;line-height:1.5;color:{p["ink"]};text-align:left;">'
        f'{hl_body(h)}</td></tr>' for h in highlights)
    counts = (f'<p style="margin:14px 0 0;padding-top:13px;'
              f'border-top:1px solid {p["hairline"]};font-family:{MONO};'
              f'font-size:12px;line-height:1.5;color:{p["muted"]};">'
              f'{esc(summary.get("counts",""))}</p>'
              if summary.get("counts") else "")

    # The mark reads as a favicon at 28px and as a masthead at 44. Nothing about
    # a digest is cramped for vertical room at the top, and the first thing the
    # reader identifies should be who it is from.
    logo = ""
    if brand.get("logoUrl"):
        logo = (f'<img src="{esc(brand["logoUrl"])}" width="44" height="44" '
                f'alt="" style="display:block;width:44px;height:44px;border:0;'
                f'border-radius:10px;" />')

    # Built the way the site builds it rather than as one monospace string:
    # the name in the display face, a hairline separator, the section in mono
    # caps. A wordmark that does not match the site is the first thing a reader
    # already familiar with it notices.
    name, _, section = str(brand.get("wordmark", "")).partition("\u00b7")
    wordmark = (
        f'<span style="font-family:{SERIF};font-size:19px;font-weight:600;'
        f'letter-spacing:-0.01em;color:{p["ink"]};">{esc(name.strip())}</span>')
    if section.strip():
        wordmark += (
            f'<span style="font-family:{SERIF};font-size:17px;color:{p["hairline"]};'
            f'padding-left:8px;padding-right:8px;">/</span>'
            f'<span style="font-family:{MONO};font-size:12px;font-weight:500;'
            f'letter-spacing:0.1em;text-transform:uppercase;color:{p["muted"]};">'
            f'{esc(section.strip())}</span>')

    sections = []
    if fe:
        sections.append(cell(
            f'<h2 style="margin:0 0 26px;font-family:{SERIF};font-size:28px;'
            f'line-height:1.22;font-weight:700;letter-spacing:-0.01em;'
            f'color:{p["ink"]};mso-line-height-rule:exactly;">Worth your time</h2>',
            pad="0 32px 4px"))
        sections.extend(render_featured(i, p) for i in fe)
    if co:
        sections.append(cell(
            f'<hr style="border:0;border-top:1px solid {p["hairline"]};margin:0 0 24px;" />'
            f'<h2 style="margin:0 0 22px;font-family:{SERIF};font-size:28px;'
            f'line-height:1.22;font-weight:700;letter-spacing:-0.01em;'
            f'color:{p["ink"]};mso-line-height-rule:exactly;">Also worth a look</h2>',
            pad="0 32px 4px"))
        sections.append(render_spotlight_row(co, p))
    # Between the middle tier and the tail, which is where a second class of
    # thing belongs: the reader has been through the items that were chosen for
    # them, and the long list is still ahead. Kong et al. found that ordering
    # the tail changes nothing, so this is the last position in the email where
    # placement is still worth anything.
    if rs:
        sections.append(cell(
            f'<hr style="border:0;border-top:1px solid {p["hairline"]};margin:0 0 24px;" />'
            f'<h2 style="margin:0 0 22px;font-family:{SERIF};font-size:28px;'
            f'line-height:1.22;font-weight:700;letter-spacing:-0.01em;'
            f'color:{p["ink"]};mso-line-height-rule:exactly;">'
            f'{esc(research.get("heading", "The research behind them"))}</h2>',
            pad="0 32px 4px"))
        sections.append(render_research_row(research, p))
    if ol:
        sections.append(cell(
            f'<hr style="border:0;border-top:1px solid {p["hairline"]};margin:0 0 24px;" />'
            f'<h2 style="margin:0 0 22px;font-family:{SERIF};font-size:28px;'
            f'line-height:1.22;font-weight:700;letter-spacing:-0.01em;'
            f'color:{p["ink"]};mso-line-height-rule:exactly;">Also shipped</h2>', pad="0 32px 4px"))
        sections.append(render_oneline(ol, p))

    doc = f"""<!DOCTYPE html>
<html lang="{esc(payload.get('lang','en'))}" dir="ltr" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(payload.get('subject',''))}</title>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
<!--[if !mso]><!--><link href="{esc(fonts['link'])}" rel="stylesheet"><!--<![endif]-->
<style>
@media (prefers-color-scheme: dark){{
  .bg{{background:#1A1C20 !important}}
  .card{{background:#22252B !important}}
  .t{{color:#E9E7E0 !important}}
  .tm{{color:#A8A399 !important}}
}}
@media only screen and (max-width:620px){{
  .card{{width:100% !important}}
  .pad{{padding-left:20px !important;padding-right:20px !important}}
  .col{{display:block !important;width:100% !important;padding-bottom:22px !important}}
  .gut{{display:none !important}}
  .act{{display:block !important;width:100% !important;padding-left:0 !important}}
  .act + .act{{padding-top:14px !important}}
}}
</style>
</head>
<body class="bg" style="margin:0;padding:0;background:{p['paper']};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">{esc(payload.get('preheader',''))}</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" class="bg" style="background:{p['paper']};">
<tr><td align="center" style="padding:28px 12px 40px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="{WIDTH}" class="card" style="width:{WIDTH}px;max-width:{WIDTH}px;background:{p['surface']};border-radius:14px;text-align:left;">

<tr><td align="left" style="padding:28px 32px 18px;font-family:{SANS};text-align:left;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
    <td style="padding-right:13px;">{logo}</td>
    <td valign="middle" class="tm">{wordmark}</td>
  </tr></table>
</td></tr>

<tr><td align="left" style="padding:0 32px 30px;font-family:{SANS};text-align:left;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:{p['paper']};border-radius:11px;">
  <tr><td align="left" style="padding:20px 22px;font-family:{SANS};text-align:left;">
    <h1 class="t" style="margin:0 0 12px;font-family:{SANS};font-size:14px;line-height:1.4;font-weight:600;letter-spacing:0.005em;color:{p['ink']};mso-line-height-rule:exactly;">{esc(payload.get('heading',''))}</h1>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{hl}</table>
    {counts}
  </td></tr>
  </table>
</td></tr>

{''.join(sections)}

<tr><td align="left" style="padding:26px 32px 30px;font-family:{SANS};text-align:left;border-top:1px solid {p['hairline']};">
  <p class="tm" style="margin:0 0 10px;font-size:13px;line-height:1.7;color:{p['muted']};">
    <a href="{esc(issue.get('webUrl',''))}" style="color:{p['muted']};">Read this issue on the web</a>
  </p>
  <p class="tm" style="margin:0;font-size:13px;line-height:1.7;color:{p['muted']};">
    You are receiving this because you subscribed at
    <a href="{esc(brand.get('siteUrl',''))}" style="color:{p['muted']};">{esc(brand.get('siteUrl','').replace('https://',''))}</a>.<br>
    <a href="{esc(issue.get('preferencesUrl',''))}" style="color:{p['muted']};">Change what you receive</a>
    &nbsp;&middot;&nbsp;
    <a href="{esc(issue.get('unsubscribeUrl',''))}" style="color:{p['muted']};">Unsubscribe from these emails</a>
  </p>
</td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""

    # ── plain-text part ──────────────────────────────────────────────────────
    lines = [payload.get("heading", ""), ""]
    if highlights:
        lines += ["".join(part.get("text", "")
                          for part in (h.get("parts") or [h]))
                  for h in highlights] + [""]
    if summary.get("counts"):
        lines += [summary["counts"], ""]
    lines.append("-" * 58)
    for i in fe:
        lines += ["", i["title"].upper(), i.get("headline", ""), "",
                  i.get("body", ""), ""]
        inst = i.get("install")
        if isinstance(inst, dict) and inst.get("label"):
            lines += [f"  {inst['label']}: {inst.get('url','')}", ""]
        elif inst:
            lines += ["  " + inst, ""]
        lines += [i["url"], "", "-" * 58]
    if co:
        lines += ["", "ALSO WORTH A LOOK", ""]
        for i in co:
            lines += [f"{i['title']} - {i.get('headline','')}", f"  {i['url']}", ""]
    if rs:
        lines += ["-" * 58, "",
                  research.get("heading", "The research behind them").upper(), ""]
        for r in rs:
            lines += [r["title"], f"  {r.get('summary','')}"]
            if r.get("meta"):
                lines += [f"  {r['meta']}"]
            lines += [f"  {r['url']}", ""]
    if ol:
        lines += ["-" * 58, "", "ALSO SHIPPED", ""]
        for i in ol:
            tail = f" - {i['oneline']}" if i.get("oneline") else ""
            lines += [f"{i['title']}{tail}", f"  {i['url']}", ""]
    lines += ["-" * 58, "",
              f"Read on the web: {issue.get('webUrl','')}",
              f"Change what you receive: {issue.get('preferencesUrl','')}",
              f"Unsubscribe: {issue.get('unsubscribeUrl','')}"]
    return doc, "\n".join(lines)


EXAMPLE = {
    "subject": "Review that reports its blind spots, plus 23 more",
    "preheader": "Top additions: a diff review with a coverage ledger, an OTA release skill, and a spend tracer.",
    "heading": "Twenty-four skills shipped this fortnight",
    "lang": "en",
    "brand": {"wordmark": "Fledgeling · Skills", "siteUrl": "https://skills.fledgeling.app",
              "logoUrl": "https://skills.fledgeling.app/brand/mark-56.png"},
    "issue": {"webUrl": "https://skills.fledgeling.app/digest/18",
              "preferencesUrl": "https://skills.fledgeling.app/preferences/TOKEN",
              "unsubscribeUrl": "https://skills.fledgeling.app/api/unsubscribe?token=TOKEN"},
    "summary": {
        "counts": "9 making · 6 orchestration · 5 long-runs · 4 research",
        "highlights": [
            {"text": "code-review closes every run with a ledger of what it could not check",
             "url": "https://skills.fledgeling.app/skills/code-review"},
            {"text": "atlas-publish decides over-the-air against store release from the fingerprint",
             "url": "https://skills.fledgeling.app/skills/atlas-publish"},
            {"text": "vouch traces a claimed charge back to the invoice line behind it",
             "url": "https://skills.fledgeling.app/skills/vouch"},
        ]},
    # Optional, and a block rather than a tier: longer-lived than the issue and
    # read for a different reason. The ground goes on the cell, so pass a
    # palette matching wherever the research is actually published.
    "research": {
        "heading": "The research behind them",
        "palette": {"ground": "#0E1013", "ink": "#E9E7E2", "muted": "#A8ADB4",
                    "meta": "#767D86", "accent": "#3EBBAE"},
        "items": [
            {"slug": "uniform", "title": "The item count was never the defect",
             "url": "https://dossier.example/uniform",
             "summary": "Twenty four items read as unreadable, and three of four backends said cut the list. The two best sourced found no ceiling exists.",
             "meta": "182 sources · 4 backends · 21 Aug",
             "imageUrl": "https://skills.fledgeling.app/research/uniform.png"},
            {"slug": "deputy", "title": "You can delegate the decision, not the signature",
             "url": "https://dossier.example/deputy",
             "summary": "A hundred and ninety four finished items wait on a person to sign off. Nobody has handed that signature to a model, and accuracy is not why.",
             "meta": "22 sources · 4 backends · ~$20",
             "imageUrl": "https://skills.fledgeling.app/research/deputy.png"},
        ]},
    "items": [
        {"title": "code-review", "headline": "A diff review that reports its own blind spots",
         "body": "Fourteen angles that are forbidden from suppressing each other, three verdicts so a realistic-but-unproven bug survives as PLAUSIBLE, and a coverage ledger naming every angle and gate that never ran.",
         # Either a command line, or {"label": ..., "url": ...} for a named
         # route. The second is the better default where one exists: a phone
         # cannot act on a shell line at all.
         "install": {"label": "Install with MCP Router",
                     "url": "https://mcp-router.fledgeling.app"},
         "url": "https://skills.fledgeling.app/skills/code-review",
         "bannerUrl": "https://skills.fledgeling.app/banners/code-review-1072.png",
         "group": "Making"},
    ],
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload", nargs="?", type=pathlib.Path)
    ap.add_argument("--out-html", type=pathlib.Path)
    ap.add_argument("--out-text", type=pathlib.Path)
    ap.add_argument("--example", action="store_true")
    a = ap.parse_args()

    if a.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if not a.payload:
        ap.error("a payload path is required (or --example)")

    payload = json.loads(a.payload.read_text(encoding="utf-8"))
    doc, text = render(payload)
    if a.out_html:
        a.out_html.write_text(doc, encoding="utf-8")
    if a.out_text:
        a.out_text.write_text(text, encoding="utf-8")
    if not a.out_html and not a.out_text:
        sys.stdout.write(doc)
    n = len(doc.encode("utf-8"))
    print(f"rendered {len(payload['items'])} item(s), {n/1024:.1f}KB HTML",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
