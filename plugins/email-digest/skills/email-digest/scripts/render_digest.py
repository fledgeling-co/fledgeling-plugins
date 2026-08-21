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
    anchors do not act on iOS and Apple is 62.26% of opens.
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

# Ends web-safe, because Outlook falls back to Times New Roman rather than to
# the next font in the stack.
SANS = ('-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, '
        "Arial, sans-serif")
SERIF = 'Georgia, "Times New Roman", Times, serif'
MONO = 'ui-monospace, "SF Mono", Menlo, Consolas, "Courier New", monospace'

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
    """Large treatment. The banner may carry mood; the headline is a text node
    beside it, because the banner's failure modes (blocked, broken, alt clipped
    to the image width, alt unstylable in Outlook) all land on the same element
    and take the AI-generated inbox summary with them."""
    banner = ""
    if it.get("bannerUrl"):
        # Deliberately not wrapped in a link. Its only content would be an
        # alt="" image, which gives the link no accessible name, and the
        # headline and the button below already point at the same URL. A
        # redundant link with no name is worse than no link.
        banner = (
            f'<img src="{esc(it["bannerUrl"])}" width="{WIDTH - 64}" '
            f'height="{int((WIDTH - 64) * 0.325)}" alt="" class="banner" '
            f'style="display:block;width:100%;max-width:{WIDTH - 64}px;border:0;'
            f'border-radius:8px;" />'
            f'<div style="height:16px;line-height:16px;">&nbsp;</div>')
    install = ""
    if it.get("install"):
        install = (
            f'<div style="margin:0 0 14px;padding:11px 13px;background:{p["codebg"]};'
            f'border-radius:7px;font-family:{MONO};font-size:13px;line-height:1.5;'
            f'color:{p["ink"]};word-break:break-word;">{esc(it["install"])}</div>')
    return cell(
        f'{banner}'
        f'<h2 style="margin:0 0 9px;font-family:{SERIF};font-size:23px;line-height:1.28;'
        f'font-weight:700;color:{p["ink"]};mso-line-height-rule:exactly;">'
        f'<a href="{esc(it["url"])}" style="color:{p["ink"]};text-decoration:none;">'
        f'{esc(it.get("headline") or it["title"])}</a></h2>'
        f'<p style="margin:0 0 14px;font-size:16px;line-height:1.6;color:{p["ink"]};">'
        f'{esc(it.get("body",""))}</p>'
        f'{install}'
        f'<a href="{esc(it["url"])}" style="display:inline-block;background:{p["accent"]};'
        f'color:#FDFBF8;font-size:15px;font-weight:600;line-height:16px;padding:14px 20px;'
        f'border-radius:7px;text-decoration:none;">Read what {esc(it["title"])} does &rarr;</a>',
        pad="0 32px 30px", tier="featured")


def render_spotlight(it: dict, p: dict) -> str:
    """A banner at reduced width, then the headline as text beside nothing.

    This tier is the middle of three and its imagery is deliberately narrower
    rather than square. NN/g's finding is about *thumbnails* being rated less
    valuable than full-width photography, and a 360px banner is neither: it is
    the same wide crop at less prominence, which is what a second tier is for.
    The headline is still a text node outside the image, for the same reason it
    is in the featured tier."""
    banner = ""
    if it.get("bannerUrl"):
        w = 360
        banner = (
            f'<img src="{esc(it["bannerUrl"])}" width="{w}" '
            f'height="{int(w * 0.325)}" alt="" class="banner" '
            f'style="display:block;width:{w}px;max-width:100%;border:0;'
            f'border-radius:7px;" />'
            f'<div style="height:12px;line-height:12px;">&nbsp;</div>')
    return cell(
        f'{banner}'
        f'<h3 style="margin:0 0 5px;font-family:{SERIF};font-size:19px;line-height:1.3;'
        f'font-weight:700;color:{p["ink"]};mso-line-height-rule:exactly;">'
        f'<a href="{esc(it["url"])}" style="color:{p["ink"]};text-decoration:none;">'
        f'{esc(it["title"])}</a></h3>'
        f'<p style="margin:0;font-size:15px;line-height:1.55;color:{p["muted"]};">'
        f'{esc(it.get("headline") or it.get("body",""))[:160]}</p>',
        pad="0 32px 26px", tier="spotlight")


def render_oneline(items: list[dict], p: dict) -> str:
    """Title plus a short tag, grouped under category headings where they exist.

    Primary links sit left: Kumar and Salo's peer-reviewed analysis found
    newsletter click-through follows a U-pattern with left-region links
    outperforming right, which is the one position finding measured in email
    rather than borrowed from the web."""
    groups: dict[str, list[dict]] = {}
    for it in items:
        groups.setdefault(it.get("group") or "More", []).append(it)
    out = []
    for name, rows in groups.items():
        out.append(
            f'<h3 style="margin:0 0 10px;font-family:{MONO};font-size:11px;'
            f'letter-spacing:0.12em;text-transform:uppercase;font-weight:400;'
            f'color:{p["muted"]};mso-line-height-rule:exactly;">{esc(name)}</h3>')
        lis = "".join(
            f'<tr><td style="padding:0 0 9px;font-family:{SANS};font-size:15px;'
            f'line-height:1.5;color:{p["ink"]};">'
            f'<a href="{esc(r["url"])}" style="color:{p["ink"]};text-decoration:underline;">'
            f'{esc(r["title"])}</a>'
            + (f'<span style="color:{p["muted"]};"> &mdash; {esc(r.get("oneline") or "")}</span>'
               if r.get("oneline") else "")
            + '</td></tr>'
            for r in rows)
        out.append(f'<table role="presentation" cellpadding="0" cellspacing="0" '
                   f'border="0" width="100%">{lis}</table>'
                   f'<div style="height:14px;line-height:14px;">&nbsp;</div>')
    return cell("".join(out), pad="0 32px 12px", tier="oneline")


def render(payload: dict) -> tuple[str, str]:
    p = {**DEFAULT_PALETTE, **(payload.get("brand", {}).get("palette") or {})}
    brand = payload.get("brand", {})
    issue = payload.get("issue", {})
    items = assign_tiers(payload["items"],
                         featured=payload.get("featured", 2),
                         spotlight=payload.get("spotlight", 3))
    fe = [i for i in items if i["tier"] == "featured"]
    co = [i for i in items if i["tier"] == "spotlight"]
    ol = [i for i in items if i["tier"] == "oneline"]

    summary = payload.get("summary", {})
    highlights = (summary.get("highlights") or [])[:3]
    hl = "".join(
        f'<tr><td class="summary" style="padding:0 0 7px;font-family:{SANS};'
        f'font-size:15px;line-height:1.5;color:{p["ink"]};">&bull;&nbsp; '
        f'<a href="{esc(h["url"])}" style="color:{p["ink"]};">{esc(h["text"])}</a>'
        f'</td></tr>' for h in highlights)
    counts = (f'<p style="margin:8px 0 0;font-family:{MONO};font-size:12px;'
              f'color:{p["muted"]};">{esc(summary.get("counts",""))}</p>'
              if summary.get("counts") else "")

    logo = ""
    if brand.get("logoUrl"):
        logo = (f'<img src="{esc(brand["logoUrl"])}" width="28" height="28" '
                f'alt="" style="display:block;border:0;border-radius:7px;" />')

    sections = []
    if fe:
        sections.append(cell(
            f'<h2 style="margin:0 0 18px;font-family:{MONO};font-size:11px;'
            f'letter-spacing:0.14em;text-transform:uppercase;font-weight:400;'
            f'color:{p["muted"]};mso-line-height-rule:exactly;">Worth your time</h2>',
            pad="0 32px 4px"))
        sections.extend(render_featured(i, p) for i in fe)
    if co:
        sections.append(cell(
            f'<hr style="border:0;border-top:1px solid {p["hairline"]};margin:0 0 24px;" />'
            f'<h2 style="margin:0 0 16px;font-family:{MONO};font-size:11px;'
            f'letter-spacing:0.14em;text-transform:uppercase;font-weight:400;'
            f'color:{p["muted"]};mso-line-height-rule:exactly;">Also worth a look</h2>',
            pad="0 32px 4px"))
        sections.extend(render_spotlight(i, p) for i in co)
    if ol:
        sections.append(cell(
            f'<hr style="border:0;border-top:1px solid {p["hairline"]};margin:0 0 24px;" />'
            f'<h2 style="margin:0 0 16px;font-family:{MONO};font-size:11px;'
            f'letter-spacing:0.14em;text-transform:uppercase;font-weight:400;'
            f'color:{p["muted"]};mso-line-height-rule:exactly;">Also shipped</h2>', pad="0 32px 4px"))
        sections.append(render_oneline(ol, p))

    doc = f"""<!DOCTYPE html>
<html lang="{esc(payload.get('lang','en'))}" dir="ltr" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(payload.get('subject',''))}</title>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->
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
    <td style="padding-right:10px;">{logo}</td>
    <td style="font-family:{MONO};font-size:12px;letter-spacing:0.12em;text-transform:uppercase;color:{p['muted']};" class="tm">{esc(brand.get('wordmark',''))}</td>
  </tr></table>
</td></tr>

<tr><td align="left" style="padding:0 32px 6px;font-family:{SANS};text-align:left;">
  <h1 class="t" style="margin:0 0 10px;font-family:{SERIF};font-size:28px;line-height:1.22;font-weight:700;color:{p['ink']};mso-line-height-rule:exactly;">{esc(payload.get('heading',''))}</h1>
</td></tr>

<tr><td align="left" style="padding:0 32px 26px;font-family:{SANS};text-align:left;">
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{hl}</table>
  {counts}
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
        lines += [h["text"] for h in highlights] + [""]
    if summary.get("counts"):
        lines += [summary["counts"], ""]
    lines.append("-" * 58)
    for i in fe:
        lines += ["", i["title"].upper(), i.get("headline", ""), "",
                  i.get("body", ""), ""]
        if i.get("install"):
            lines += ["  " + i["install"], ""]
        lines += [i["url"], "", "-" * 58]
    if co:
        lines += ["", "ALSO WORTH A LOOK", ""]
        for i in co:
            lines += [f"{i['title']} - {i.get('headline','')}", f"  {i['url']}", ""]
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
    "items": [
        {"title": "code-review", "headline": "A diff review that reports its own blind spots",
         "body": "Fourteen angles that are forbidden from suppressing each other, three verdicts so a realistic-but-unproven bug survives as PLAUSIBLE, and a coverage ledger naming every angle and gate that never ran.",
         "install": "/plugin install code-review@fledgeling-plugins",
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
