<p align="center">
  <img src="assets/banner.png" alt="test-campaign: a porcelain icon of a three-by-three grid of captured frames, one filled vermilion and the ninth cell an empty socket pressed into the tile, beside the wordmark and the line: a test campaign, and a page that shows what it actually proved" width="100%" />
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> test-campaign</h1>

<p align="center"><strong>A test campaign, and a page that shows what it actually proved.</strong><br />
A SWE skill for Claude Code that reads what your project claims to do, tests it across the states and viewports and roles nobody gets to, and leaves one browsable page where the gaps are as visible as the passes.</p>

<p align="center">
  <img alt="Version 0.9.0" src="https://img.shields.io/badge/version-0.9.0-D33C21">
  <img alt="SWE skill: testing" src="https://img.shields.io/badge/SWE_skill-testing-434A55">
  <img alt="Lanes: web, RN, iOS, macOS, Windows, Linux" src="https://img.shields.io/badge/lanes-web_·_RN_·_iOS_·_macOS_·_Windows_·_Linux-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

Here are three test suites. All green, all wrong, and none of them looks it.

The first covered a console with six screens. Five of them were receiving none of the sweeps, because the surface list came from a capture contract that had quietly deduped six screens onto one route. Nothing in the run reported that. The output had exactly the headings a complete run would have had, which is the whole problem.

The second ran 524 assertions across 13 tenants. Every one of those assertions opened `/`, at 1280px or wider, against the reference build. It stayed green for months while every generated tenant shipped with no header, no navigation and no footer.

The third reported **100% checked, 22 armed cases, 59 passing tests** for a macOS app and a Windows app. No GUI process had ever attached to a window server. The Swift half was initialising SwiftUI view structs in memory, and those are value types, so nothing renders; the Windows half was C# that had never been compiled; and the screenshots on the evidence page came from an HTML mock photographed in a browser. Every individual number in that report was true.

What the first two share is a number with no denominator. "524 assertions" reads as breadth. "41 of 52 surfaces, 3 of 8 viewports, 1 of 4 roles" reads as a sample, because that's what it was. The third adds a worse question than *how much did you cover*, which is *did the thing you tested ever run*.

So this skill is built around making the sample say itself out loud, around proving the artifact under test actually existed and was drawn, and around a handful of gates that fail rather than shrug.

## What it does

**It reads the project before it reads the DOM.** Overview, PRD, feature specs, design md, the latest mock UIs. Enumerating routes first gives you DOM-driven coverage, which over-tests trivia and misses requirements; a build can't tell you about a control it never rendered. Requirements come out classed **affordance**, **behaviour**, **honesty-guardrail** or **deferred**, and each one gets a stable id.

**It states the correctness space, then declares its sample.** Surface, state, viewport, theme, role, locale, data shape, input modality, network, and which oracle. Pairwise across the lot as a floor, higher strength on the clusters that actually interact. Sampling is unavoidable; sampling in silence is the bit that hurts.

**It sweeps for what no requirement named.** State matrix, fault injection, interaction integrity, keyboard and the accessibility floor, data-shape stress, security surface, multi-user, refusal honesty, metamorphic relations, freshness, and whether the product acts outside itself at all. Then, for anything with a real window, desktop shell invariants (display scaling, window size limits, popover anchoring, a theme toggled while the app runs, occlusion), and for anything that's more than one process, live IPC chaos: kill the peer, restart it, check the client degrades honestly instead of showing stale telemetry as current. Every sweep prints `examined=41 failures=0`, because `failures=0` on its own is a claim rather than a result.

**It measures the build against its design of record.** Structure, resolved style (longhands only), the vocabulary each screen uses, and quantised box geometry. Not pixels; rendering noise buries the signal, so a pixel diff gets treated as a tripwire and never as a verdict. This is the only phase that can see a control the design specifies and the build simply doesn't have.

**It leaves a page.** Coverage with the oracle mix and the armed ratio, requirements and what checked them, a wall of every capture, user-flow storyboards with per-step atoms, surfaces, the component atlas, defects, **not covered**, and methods. Every row is an anchor: `REQ-004`, `SURF-009`, `FLOW-002.03`, `CASE-0117`, `DEF-006`. A review comment can point at one of those a year later and still land.

## The rule that does the most work

Every case declares which rung of oracle it stands on:

| rung | what it asserts |
|---|---|
| `touch` · `presence` | the step ran; an element exists |
| `structural` | role, accessible name, enabled state |
| `structural-visual` | the labels and hierarchy tokens a render would use exist |
| `outcome` | the promised effect, so data rendered or a record written |
| `metamorphic` | a relation across runs, so undo restores or the count tracks the store |
| `effect-witness` | an effect outside the process, seen by a recorder the product doesn't control |
| `raster-visual` | pixels captured off a display server, against a reference |
| `interactive-glass` | a click, key, or gesture on a live window, then the on-glass state it caused |

A flow you've marked critical that carries no case at `outcome` or above **fails the gate**. Not a model reviewing the suite and offering an opinion; a script exiting non-zero with the flow ids in the output.

That rule is there because of a measurement. Across 214 UI components, behavioural relations were exercised far more often than they were actually checked, validated in only 42.5% to 47.6% of cases. (August 2026 preprint, no independent replication yet, so it's a direction rather than a threshold.) A suite can execute nearly everything and assert almost none of it, and no count of tests will show you that.

The last two rungs used to be one, called `visual`, and that was the hole the third suite fell through. A case asserting that a card's title property equalled `"AGGREGATE CPU"` claimed the visual rung, counted as proof of an effect, was watched to fail, and was completely honest about all of it, while being a data-model check on a struct in memory. Only `raster-visual` buys effect credit now, and it owes an artifact that is a real image, isn't another case's image, and names the channel it came from.

Two more gates in the same spirit. **A pass has to name an evidence artifact on disk**; a verdict you reached by looking isn't a measurement. And **armed and unarmed assertions are counted separately, never summed**. Arming means reverting the behaviour an assertion guards, watching it go red, then restoring it. On one campaign 13 of 225 assertions were armed, and "13 of 225" is the honest number to print.

## It makes you prove the app ran

A lane you name with a `-glass` suffix is claiming the application was running and drawn by a display server, and the gate won't clear until it carries three things: the built artifact as a path that exists, the command that produced it, and what witnessed a process from it reaching a display server. The first of those is the cheapest check in the skill and it's the one that catches a platform whose source was written and never compiled.

When the artifact is not on disk, the next step is the project's documented build, then launch, then `--attached`. `--cannot-attach` is for a structural block that survives that build — `"no Windows host with an interactive desktop is reachable"` is one; `"no signed app is on disk"` is not, and `campaign.py lane` refuses it. A lane silently assumed to have run is the failure; a missing binary recorded as unreachable is the same failure wearing a reason string.

The same discipline runs down to the artifacts. A screenshot that's actually a zero-byte file, an HTML error page saved to a `.png` path, a 1×1 placeholder, or **one screenshot attached to twelve different cases**. All four have shipped, all four are exact to detect from the bytes, and all four now fail the gate. What the skill deliberately doesn't do is score the picture: no density or entropy floor can separate a failed capture from a legitimately sparse screen, because an empty state is mostly background by design. So provenance gates and density only ever annotates.

And there's a fourth thing a case can now say. `inconclusive` means the check was attempted and the instrument couldn't measure. That matters because where an engine returns nothing, `"" === ""` is true and quietly certifies that two layouts are identical. "We do not know" is a weaker claim than "no difference found", so the two get separate rows and the report prints how many observations it actually got.

## And it makes you prove the picture is of the right thing

A screenshot on an evidence page makes two claims. The first — that pixels came off a display server — is the one above. The second is that they're of the surface named underneath them, and until 0.8.0 nothing checked it at all.

A campaign published 20 surface captures and cleared every gate this skill had: every case accounted for, 46 of 49 checked under the strict rule, every glass lane proved and witnessed. The captures were of three unrelated documents — a project status report, the mock browser's own index page, a design accessibility doc. Twenty files held six distinct images. A flow step captioned "Open pairing QR code sheet" showed a questionnaire about Apple developer credentials.

Nothing was broken. Captures were bound to surfaces on a slug of the **filename**, the page rendered each one with alt text taken from the label, and the artifact checks ran over case evidence rather than over the pictures the page actually shows. The gated part of the campaign was sound; the ungated part was the part people look at.

The fix is borrowed wholesale from `warrant`'s oracle plane, which had already solved it one domain over for numbers: a figure without a source reference is the defect that plane exists to find. Substitute *picture* for *figure* and it transfers intact. The capture step now records what each shot depicts and — the load-bearing part — **where the channel was actually pointed**, at capture time, because a manifest written afterwards records what somebody believed. Four passes then run, all exact, none needing a model: a capture with no recorded target, a target that doesn't resolve to its subject's route, two subjects sharing one image, and a capture published without a `be-my-witness` verdict.

That last one ratchets rather than blocks. The other three fail the gate, and the whole ladder is itself watched to fail: `--seed-swap` swaps two subjects and asserts the gate goes red, because a tie check that can't be seen failing is indistinguishable from one that reads nothing.

Worth saying why none of the four asks a model. Run `be-my-witness`'s prescan against the worst capture in that campaign and it returns *is evidence: true, settled: true*, exit 0 — a real, contentful, settled image of entirely the wrong document. Image statistics can't answer the subject question and frontier vision tops out near 40% recall on fine-grained UI diffs. Provenance answers it. Nothing else does.

## And it asks whether the product does the thing at all

Every gate so far assumes the product acts and asks whether the suite watched it. There's a prior question, and until 0.9.0 nothing here asked it.

A campaign closed 230 cases over a CI runner built around zero-trust network isolation, armed 220 of them, cleared every gate this skill had, and recorded "runner communication is outbound pull only over HTTPS/WSS on TCP 443" as **observed**. Somebody on a neighbouring project then read the source. No HTTP client anywhere in the dependency tree. No line of production code that spawns a subprocess. `tart`, `wsl.exe`, `pfctl` and `nft` never executed. No mDNS, so the zero-config discovery in the PRD never happens, and a daemon that only binds loopback, so the multi-device mesh never crosses a machine. The isolation engines are rule generators and state machines. Every network guarantee in that inventory was true because nothing crosses the boundary it describes.

Arming is what should have caught it and structurally cannot. Arming reverts the behaviour an assertion guards and watches the case go red, which mutates the **system** and finds what the suite doesn't cover. Ball & Kupferman named it as one of a pair in 2008: mutating the system finds coverage gaps, and mutating the **specification** finds guarantees that were never exercised at all. This skill had shipped one half of a known pair 220 times and the other half never. The published base rate for vacuity in formal verification is around 20% of formulas, and "trivial validity always points to a real problem".

The rest of the toolkit is blind to it for the same reason. `cargo mutants` mutates code that exists, so a boundary nothing reaches has no mutants to catch. Coverage counts lines the suite executed, and a rule generator's lines all execute. And the whole isolation stack — `pytest --disable-socket`, `WebMock.disable_net_connect!`, `nock.disableNetConnect()` — asserts the *absence* of I/O, which means a suite built on it cannot tell "correctly outbound-only" from "never communicates".

So requirements now carry an **effect class** naming what they make the product do outside its own memory, and a **provider**: the thing in production source that could actually perform it. A requirement claiming an effect with no provider is vacuous before a test runs. A requirement claiming one and recorded `observed` owes a case at `effect-witness` — a recorder the product doesn't control, plus the count it saw. And `vacuous` joins observed / reported / contradicted as a fifth evidence class, because a guarantee over a capability nobody built is a real finding and needs somewhere honest to sit. It clears the gate; the configuration that blocks is `observed` with nothing witnessed.

Two of the six checks cost nothing. One greps for providers. The other scans the test tree for a call that changes state with no read after it, which is the shape that lets a verb report success while doing nothing. On the campaign above it read 164 test functions and found 26 of 32 mutating tests blind — five of them in a file named for the effect it wasn't measuring. That pass immediately surfaced a live defect the 230 cases had passed: `stop_runner` returns `true` twice for the same runner and never removes it, and `restart_runtime` reports success having restarted nothing. The case covering it stood at `outcome`, and the outcome it asserted was the arrival of a sentence.

## The defect class it's named after finding

A GraphQL client configured with `errorPolicy: 'all'` **resolves** an awaited mutation when the response carries errors. So this:

```ts
try { await mutate(); toast('Saved') } catch { /* never runs */ }
```

confirms work the server refused. Four instances of that were live in production across three screens of one console.

It's worth naming because of what it defeats. An element-exists test passes; the element exists. A screenshot looks perfect; it is perfect. A visual judge sees a clean, well laid out screen and says so. Only forcing the server to refuse and then asserting that the interface says so will find it, which is why that's a standard sweep here rather than something you're expected to think of.

## It checks its own instruments first

The skill carries a catalogue of **detector defects**: fourteen measured ways a check lies, each with the fix.

The one that best explains the category: a dead-control sweep compared `document.body.innerHTML.length` before and after clicking each control. Choosing an option writes `aria-pressed="true"` on one control and `"false"` on another, which is length-neutral, so six working presets reported dead on a page where every single control worked.

Same file covers the sweep that writes. Enumerate-and-click on a surface whose controls are save buttons placed a section and set seven theme pairs on a live tenant record, four times in one morning. The answer isn't to skip write-bearing surfaces; it's to refuse the writes locally, so a control wired to a mutation still renders its refusal and still proves it acted, while a control wired to nothing still reports dead.

When a check tells you something surprising, the prior is that the instrument is wrong. It's younger than the application.

## Across platforms, to each lane's ceiling

Web, React Native, iOS, and native macOS, Windows and Linux, planned to what each lane can genuinely observe rather than to what the web lane can.

iOS Simulator exposes no accessibility tree, so there are no elements, no identifiers and no geometry assertions. **No desktop platform exposes a cross-process computed style.** There is no `getComputedStyle` for a foreign native window on macOS, Windows or Linux, so the style vector there is a triangulation rather than a read. Those get marked `n/a` with the structural reason attached, which reads honestly on the page, instead of sitting open forever and looking like neglect.

The desktop rows exist because the alternative is inventing them. A few of the facts that most change a plan:

- On Windows, `SendInput` aimed at an elevated app **fails silently under UIPI**. Microsoft's own reference says it outright: *"neither GetLastError nor the return value will indicate the failure was caused by UIPI blocking."* A standard-user test driver gets no error and no effect.
- Windows has **no per-frame validity signal**, nothing like Apple's `SCFrameStatus`. Minimised windows, windows on an inactive virtual desktop, windows opted out of capture, and hybrid-GPU mismatches all return black without erroring, and from the image alone you cannot tell which.
- Deep UI Automation tree enumeration in WinUI 3 can raise a native `0xc0000005` inside `Microsoft.UI.Xaml.dll`, so a campaign on that lane plans shallow reads or it plans crashes.
- On macOS, a background window emits capture frames **only while the mouse moves on its display**, so an unattended run on a still machine can wait forever.
- Wayland deliberately removed X11's global capture and input injection. Automation goes through a desktop portal that raises a consent dialog, which stops an unattended pipeline dead unless a token was cached beforehand.
- A hosted `windows-latest` runner does give you an interactive desktop, and defaults to **1024×768**: clipping that the runner introduced and the campaign would otherwise blame on the build.

Where a lane's tooling is genuinely absent, that's a blocker to report rather than a licence to eyeball. Windows is thinner than it looks: WinAppDriver has had no stable release since 2020 and can't be forked, White is archived, and Playwright's desktop support is Electron-only.

## What it won't do

Worth saying plainly, since the gaps are the point of the whole thing.

**A model verdict never gates.** As a non-crash oracle the measured ceiling is around 49% of known bugs, with false positives. Judge output is a hypothesis until a deterministic check reproduces it. One real judging pass cost 178 calls, 1.69M input tokens and roughly US$6, and returned 11 pass, 13 fail and 36 inconclusive over 63 surfaces. That inconclusive share isn't a fault in the run; it's what an honest judge says when most of what a flow promises can't be seen in a still picture.

**It doesn't replace a person looking at the thing.** It gets a lot further than a green suite does, and it tells you precisely where it stopped, which is different from finishing.

**Nothing does native visual parity for you.** The commercial visual-testing tools cover web and mobile; none covers a native Mac or Windows window. So comparing a desktop build against its design of record is hand-built here, out of the accessibility tree's structure, vocabulary and geometry, with the style vector marked unmeasurable. And a similarity score is still a tripwire rather than a verdict: imperceptible perturbations have been shown to raise DISTS by up to 34.5%, LPIPS by 36.8% and VIF by 98.0% while human opinion scores stayed flat or fell, so a threshold is a thing an implementation can be tuned toward without getting better.

**Generation is still half redundant.** Mozilla measured LLM-generated QA plans against Firefox's own QA team: 27% valuable and new, 50.5% duplicates, 22.5% invalid or out of scope. That's why the coverage model does the planning and the model does the writing, and why deduplication is treated as most of the value rather than tidying up afterwards.

## Lineage

It's the successor to `acceptance-e2e`. Ten gaps in that skill were each measured during a real multi-day campaign before any of this was designed, and every structural decision here traces back to one of them. `references/evidence.md` carries that trace alongside the research citations, including the four places the research disagrees with itself and the figures dropped when their only source turned out not to exist.

It was called `create-test-suite` until 0.5.0. The name undersold it: the skill sets the strategy, decides what a given run needs to cover, keeps the suite alive across runs, and publishes the evidence. `create-` implied a one-shot generator, and "suite" named the smallest of the things it leaves behind. `campaign` was already the word the code used throughout.

The desktop lanes came out of a fourth research pass in August 2026. Half of it was a sweep of 452 existing research reports for what was already known about macOS; the other half had to be commissioned, because that sweep found **nothing at all** on Windows or Linux: no UI Automation, no capture semantics, no AT-SPI2, no Wayland. Of the new run's 106 citations, 101 resolved, and the two claims left without a source were chased by hand rather than kept on trust: one was withdrawn, and one turned out to be better evidenced than the report had it, straight from the vendor's own API reference.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install test-campaign@fledgeling-plugins
```

Then `/test-campaign`, or just ask Claude to test something properly.
