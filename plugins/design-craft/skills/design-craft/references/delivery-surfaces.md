# Delivery Surfaces: What Ships, and What the Surface Silently Refuses

One deliverable, three destinations, and they do not agree about what a page is allowed
to do. **Every failure below is silent** — the page renders, nothing errors, and the
missing half is invisible to the machine that built it. Read this before reaching for a
CDN, a font host, `localStorage`, or a download link.

| | Served locally / on a host you control | Published as an **Artifact** | Installable (added to a phone's home screen) |
|---|---|---|---|
| External `<script>` | yes, pinned with SRI | **blocked, no error** | yes, but offline it is gone |
| External stylesheet | yes | **blocked, no error** | yes |
| Google Fonts `<link>` | yes | **yes — the only permitted origin** | yes |
| Any other font host | yes | **blocked** — use a `@font-face` `data:` URI | yes |
| `fetch` / XHR / WebSocket | yes | **`connect-src 'self'` only** | yes |
| `eval`, WASM, Babel-in-page | yes | **yes — `'unsafe-eval'` is allowed** | yes |
| `localStorage` | yes | unreliable across views — use a **`sessionStorage`** stash | yes |
| `<a download>` / script-driven save | yes | **inert for viewers**, data: and blob: included | yes |
| Total page weight | your budget | **16 MB rendered**, and `data:` URIs count | keep it small; it is a phone |

## The artifact CSP, stated once

A published Artifact runs inside a sandboxed iframe whose CSP allows network egress only
to the artifact's own origin. Anthropic's own design skill states the policy directly, and
this is the quotation the rest of this file rests on:

> "**The iframe has no network egress beyond its own origin, Google Fonts aside.** The
> CSP's `connect-src 'self'` permits fetches only to the artifact's own serving origin …
> every other destination — CDNs, APIs — is blocked … The single carve-out is typographic:
> stylesheets from `https://fonts.googleapis.com` and the font files they pull from
> `https://fonts.gstatic.com` load through `<link>`/`@import`, never `fetch()`; no other
> font host does. … `'unsafe-eval'` IS allowed, so eval and WASM work."
> — `design` SKILL.md, Foundation (read 18 Aug 2026)

**One technical correction to that quotation, because the wrong inference from it is expensive.**
`connect-src 'self'` governs **script-initiated** connections — `fetch`, XHR, WebSocket,
EventSource, Beacon — and **not** `<script src>` loading, which is `script-src`; fonts are
`font-src` and stylesheets are `style-src`. The observable behaviour is exactly as the quote
describes (CDNs are blocked), but do not reason from it that a CDN script is *allowed* because
`connect-src` permits self. Different directive, same outcome.

Three consequences this skill got wrong before that quotation was read, all of them worth
carrying as concrete facts rather than as a general caution:

1. **`gsap-motion.md`'s three `cdn.jsdelivr.net` tags, `make-a-prototype.md`'s three
   `unpkg.com` tags, and `ai-slop-check.md`'s `cdn.simpleicons.org` logo wall all fail in a
   published artifact with no error.** The GSAP page ships motionless, the React prototype
   ships blank, the logo wall ships broken images. Each of those pages passes every static
   check and every look on the machine that built it, because on that machine the CDN
   resolves.
2. **Google Fonts via `<link>` is *permitted*, so a lint that condemns every external
   resource condemns the one sanctioned external.** `scripts/design-lint.py` carves out
   `fonts.googleapis.com` and `fonts.gstatic.com`, and downgrades a pinned-with-integrity
   script to a warning rather than a blocker, because the same tag is correct for served
   delivery and wrong for a published artifact.
3. **`'unsafe-eval'` being allowed makes inlining Babel a real option.** A JSX prototype
   destined for an artifact is not a dead end: inline `@babel/standalone` (it is ~1.5 MB
   minified, which fits inside 16 MB with room to spare) and the `text/babel` path works.
   The blocker was always the *load*, never the *eval*.

## Reading the console is part of the check, not part of debugging

**Browsers fail quietly here.** There is no dialog, no visual warning, and nothing server-side: a
blocked resource simply does not arrive, and the page renders a plausible degraded version of
itself — fallback typography, an inert control, an empty widget, a motionless hero. A
screenshot-only check passes it.

So collect the console on every load and treat any of these as a **failure**, not a note:

```
Refused to load the script …                       (script-src)
Refused to apply inline style / load the stylesheet …   (style-src)
Refused to evaluate a string as JavaScript …       (script-src, no 'unsafe-eval')
Content Security Policy: A violation occurred
```

**And know the second-order failure, which is the expensive one.** With the console unread, the
agent sees a page whose JavaScript "did not work" and starts rewriting logic that was never
broken — a loop of edits against functional code, driven by an infrastructure block it never
looked for. One console read costs a single call and ends it. The same applies to fonts:
`document.fonts.ready` then `document.fonts.check('16px "Your Face"')` tells you whether the face
actually loaded, where a screenshot only tells you that *something* rendered.

## Choosing, before you build

Ask the delivery question in the kickoff round, because retrofitting is a rebuild:

- **"Where will you open this?"** A local file the user opens themselves, a page you will
  publish for them, or something they will pin to a phone's home screen.
- Default to **served HTML** when nobody says. It is the least constrained surface and it
  is what this skill's procedures assume.
- The moment "share this with the team" or "publish it" enters the brief, the artifact
  column becomes binding — and the artifact-shaped rules below are not optional polish,
  they are what makes the page work at all.

## Building for the artifact surface

design-craft targets **served HTML files**. When a deliverable is going out as an
Artifact, the format, theme, naming and capability contract belong to the **`artifact-design`
skill** — load it, and treat the rules below as the design-side subset you must honour
whichever skill writes the wrapper.

- **No `<!DOCTYPE>`, `<html>`, `<head>` or `<body>` tags of your own.** The page content is
  wrapped at publish time. Write the content directly, plus a `<title>` and a `<style>`.
- **The `<title>` is the artifact's name** in the tab and the gallery, and only the first
  8 KB of the file is scanned for it — so it goes at the top. Name it from the content: a
  short noun phrase, two to four words, distinctive enough to pick out of a gallery. Never
  the format, never a name-plus-explainer. Keep it stable across redeploys. (SKILL.md §18
  and the lint's `missing-title` / `generic-title` checks are the same rule.)
- **Theme is a three-state contract, and getting it wrong is the most common artifact bug.**
  An explicit viewer choice stamps `data-theme="dark"` or `data-theme="light"` on the root
  element; the default "system" setting stamps *nothing*, so only `prefers-color-scheme`
  separates light from dark. Define the complete light palette as tokens on **bare `:root`**;
  redefine only the changed tokens under `@media (prefers-color-scheme: dark)` guarded as
  `:root:not([data-theme="light"])`; then redefine them again under `:root[data-theme="dark"]`
  so an explicit toggle wins in both directions. **Never give a colour its only definition
  inside a media or `[data-theme]` block**, and give `body` an explicit token background —
  a transparent body borrows the host's ground and the page reads as half-themed. A design
  that deliberately commits to one look may skip the dark blocks, and still paints
  background and colours explicitly.
- **Nothing the page starts itself can download.** `<a download>`, `data:`/`blob:` hrefs and
  script-driven saves are all inert for viewers. So never offer a file through a plain link:
  render the content on the page, or hand the user the file another way.
- **Wide content scrolls inside its own `overflow-x: auto` container** — tables, diagrams,
  code blocks. The page body must never scroll horizontally.
- **16 MB rendered, `data:` URIs included.** That is the real budget for inlined fonts,
  base64 imagery and an inlined library; a generated hero at ~200 KB and a woff2 at ~40 KB
  are cheap, an uncompressed PNG field is not.
- **Mermaid renders natively** (a ```mermaid fence in Markdown, `<pre class="mermaid">` in
  HTML) with no library. Reach for it for a genuine diagram rather than importing one.
- **Runtime capabilities** (live data, shared state, assets, self-update) exist but are
  declared, not assumed: load the `artifact-capabilities` skill before writing any
  `window.claude.*` code or passing a `capabilities` field.

## Building for served HTML (the default)

- **Serve over HTTP, never `file://`** — one `python3 -m http.server` per project
  directory. Module scripts, `fetch`, and some fonts fail silently from the filesystem, and
  a multi-file React prototype opens as a blank page with nothing useful in the console.
- **Pin every external tag and keep the integrity hash.** `curl -sf <url> | openssl dgst
  -sha384 -binary | openssl base64 -A` when you need a hash the reference doesn't carry.
  An unpinned `react@18` is a page whose behaviour changes without a commit.
- **Self-containment is still the better default**, for a reason that has nothing to do with
  CSP: a page that `<link>`s a webfont opens in a different typeface offline, and offline is
  one of the three places a shipped artifact is most often actually read. Inline what you
  can; pin what you cannot.

## Building an installable

Covered in full by `make-a-prototype.md` § *Installable mobile prototypes* — the head tags,
the `icon.png`, `env(safe-area-inset-*)`, and the rule that matters most: **no fake chrome**.
The real status bar and keyboard render on top of your layout, so a painted one doubles up.

## Persisting state

- **Served or installable:** `localStorage`, keyed to the artifact (`design.tweaks`,
  `deck.slide`). Refreshing during iterative design is one of the most common user actions,
  and state that doesn't survive reload makes a prototype feel broken.
- **Published artifact:** a **`sessionStorage` stash** is the mechanism the platform's own
  editor uses — edits accumulate locally and the stash survives a reload of the tab. Treat
  `localStorage` as unreliable there rather than as unavailable, and never make a feature
  depend on it silently.

## What this file does not decide

Whether the piece *should* be an artifact at all. That is the user's call and it belongs in
the kickoff round, because the answer changes what you build rather than how you deliver
it — a scroll-driven GSAP page and a CSP-bound artifact are two different commissions, and
discovering that at handover costs the whole build.
