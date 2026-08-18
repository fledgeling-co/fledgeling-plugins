# Intent Conformance: Did the Build Become the Thing That Was Chosen?

Every other stage in this pipeline asks whether the surface is internally sound. This one asks whether it is the **right surface** — whether the build matches the direction, mock, or design system it was told to implement, whether its shared chrome was reviewed as a component rather than as background, and whether output that was supposed to vary between instances actually does.

The three checks here exist because of three reviews that came back clean and were then contradicted by the person who commissioned them:

> *"The web app looks terrible, was it visually verified? It looks like a mashup of the original and the new chosen design instead of like the new chosen design."*

> *"Every portal header also has a broken layout. … `/design-review` has clearly missed the header issue."*

> *"The leadership page looks almost identical for every company paid portal. Find the root cause given that I asked for many sections, components and pages to be created so that each portal could look unique."*

All three are invisible to a review that looks at one surface at a time and judges it on its own terms. A mashup is internally consistent. A broken header is consistent across every page that shares it. Fourteen identical portals each pass their own review. **Self-consistency is not conformance**, and the gap between them is where these defects live.

## 1 — Direction conformance

Find the intended target before judging the result. It is one of:

- a committed direction block (`:root` tokens plus posture bullets) from `design-craft`'s `frontend-aesthetic-direction`
- a chosen mock — `design/mocks/html/*.html`, a Figma export, a screenshot the user approved
- a `DESIGN.md` / `tokens.css` / `design.md` the build was supposed to obey
- a named concept the user picked from a set ("go with concept 5", "the Scale Ladder one")

If none exists, record `n/a: no stated target` and move on — this check has nothing to measure and inventing a target is worse than skipping it.

When one does exist, **diff the render against it**, not against your memory of it. Open the target and the build side by side.

| Axis | What a mashup looks like |
|---|---|
| Palette | Both palettes present. The new accent appears, and so does the old surface colour or the old neutral temperature. Count distinct backgrounds and named hues in the render; compare the set to the target's. |
| Type | The new display face on headings, the old face still on body, controls, or one stranded component. Enumerate every distinct `fontFamily` in the computed styles — a two-family target showing four families is the finding. |
| Radius / border / shadow | The single most reliable tell. Old components keep their old radius, so a 4px system and a 12px system coexist. Collect the distinct `borderRadius` values; a target committing to one or two showing five means the old system survived. |
| Density and rhythm | The new spacing scale applied to new sections, old margins retained in untouched ones. |
| Structure | The target's band order versus the build's. A section that only exists in the build, or one the target dropped that is still there. |

`parity-oracle.md` carries the mechanics when the target is itself a rendered surface: token diff, band skeleton, ~40 landmarks × ~20 computed properties. Use it — this is exactly the job it was built for, and "did the build implement the mock" is the same measurement as "did the port preserve the original", pointed the other way.

**Report unconverted regions by name, not as a global verdict.** "Doesn't match the direction" is unactionable. "The settings pane and the table header still carry the pre-redesign 4px radius and `#F5F5F5` ground; every other surface converted" is a fix list.

**Refinement and redesign are scored differently.** On a refinement, surviving old identity is correct and only the named scope should have moved. On a redesign, surviving old identity is the defect. Establish which the brief asked for at stage 0; scoring a refinement as a failed redesign is a wrong-advice failure, and it is the more embarrassing direction to get wrong.

## 2 — Shared chrome, reviewed once and deliberately

The header, primary nav, sidebar, and footer appear on every surface in the worklist, which is exactly why they get missed. Per-surface review treats them as the frame around the thing being reviewed, and attention goes to the content. A defect that repeats on all fourteen surfaces reads as the background rather than as fourteen instances of a bug.

So give shared chrome its own row in the ledger and review it as a component:

1. **Identify it.** The elements present on every, or nearly every, surface — usually `header`, `nav`, `[role=banner]`, `aside`, `footer`, and any persistent toolbar.
2. **Review it at every breakpoint on its own**, not embedded in a page capture. Crop to the chrome at 375 / 768 / 1280 / 1920 and read those crops. A header failure is most often a wrap, a collapse, an overlap with the content beneath, or a nav that loses items — all of which a full-page thumbnail renders as a slightly odd strip.
3. **Drive its states.** Scrolled versus at rest (sticky headers change height and shadow, and that transition is where they break), menu open, logged out versus in, the longest real title, the longest real user name, an active item at each end of the nav.
4. **Check it against the intent target too** — chrome is the component most likely to survive a redesign unconverted, because it is often the one file nobody touched.

A chrome finding is reported **once**, with its surface count: *"header nav wraps to two rows below 1100px — all 14 surfaces"*. Reporting it fourteen times buries the rest of the report; reporting it zero times is the failure this section exists to prevent.

## 3 — Cross-instance differentiation

Applies when the surfaces under review are **generated instances of one system**: multi-tenant portals, per-customer sites, templated pages driven from a CMS, anything where the brief promised that each one would look like itself.

Every other check in this pipeline rewards consistency. This one is the inverse, and running the usual lens here produces a clean report on the exact defect: fourteen portals that are identical score perfectly on cross-page drift.

Capture the same route across 3–5 instances and measure what actually differs:

```js
// per instance, on the same route
(() => {
  // Custom properties declared on :root, read back resolved. The earlier version
  // of this snippet was `Object.fromEntries([...document.styleSheets].flatMap(() => []))`,
  // which always evaluates to {} — so a reviewer following it measured zero tokens
  // on every instance and landed on this section's expected conclusion through a
  // dead instrument. Exactly the defect this file exists to catch, in this file.
  const root = getComputedStyle(document.documentElement);
  const names = new Set();
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch { continue; }   // cross-origin
    if (!rules) continue;
    for (const r of rules) {
      const text = String(r.cssText || '');
      for (const m of text.matchAll(/(--[\w-]+)\s*:/g)) names.add(m[1]);
    }
  }
  return {
    tokens: Object.fromEntries([...names].sort()
      .map(n => [n, root.getPropertyValue(n).trim()])
      .filter(([, v]) => v)),
    bands:  [...document.querySelectorAll('main > section')].map(s => s.className),
    fonts:  [...new Set([...document.querySelectorAll('h1,h2,body,p')]
              .map(e => getComputedStyle(e).fontFamily))],
    hero:   document.querySelector('h1')?.textContent?.trim(),
  };
})()
```

Two caveats on the output, both measured. A cross-origin stylesheet throws on `cssRules` and is skipped, so `tokens` is a floor rather than a census — count the skips if the number matters. And `fonts` records what the CSS asked for: web fonts never load on this engine, so a font set that differs across instances is a real difference while an *identical* one is not evidence the rendered type matches.

Then ask what varies: **only the content**, or the structure and the system too? Content-only variation with an identical band skeleton, identical token values and identical section order means the generator is a template with slots, whatever the brief promised. That is a High finding against the brief, and the root cause is upstream in the generator — name it there rather than filing fourteen cosmetic findings.

State the differentiation budget as a number in the report: *"across 5 tenants: 1 token differs (accent hue), 0 of 9 band skeletons differ, 0 layout variants observed. The brief asked for per-tenant uniqueness; the system delivers per-tenant recolouring."*

## What this stage cannot settle

Into Needs verification, every time:

- **Whether the chosen direction was the right choice.** This measures conformance to it, never its merit.
- **Whether an unconverted region was left deliberately.** Phased migrations are legitimate. Report the divergence and ask; do not assume abandonment.
- **Whether the differentiation that exists is enough.** The count is measurable, the sufficiency is the commissioner's call.
