# React Native targets — how to measure the rendered tree (not the source)

A React Native app has **no DOM**, so `getComputedStyle` doesn't exist and `getBoundingClientRect` doesn't apply. Under the New Architecture (RN 0.85+, Fabric), JS hands the view tree to the Fabric renderer, Yoga computes layout in C++, and native `UIView`s are instantiated — by the time anything is on screen, the per-component style props you care about have been *flattened away*. This is why the web playbook doesn't transfer, and why the old shortcuts fail:

- **Appium / XCUITest** read the native accessibility tree — great for geometry, text, and roles, but **blind to style**. `getCssValue` is documented as webview-only; on a native context it errors. You cannot get a colour, font-weight, or border-radius this way.
- **Reading the `StyleSheet` source** tells you what a component *declares*, not what *rendered*. It can't see a component that never mounted, a prop that didn't reach the node, a relocated control, or a cell the data left empty. **It is not a measurement** and must never, on its own, justify a ✓ (this is the trap the whole skill was rebuilt to kill).

So measure the running app in **two layers**, and write each to a `*.json` artifact:

| Layer | What it gives you | Tool |
|---|---|---|
| **Structure** | hierarchy, geometry, text content, accessibility labels → catches *missing elements, wrong text, relocated controls* | `axe describe-ui`, or the Maestro view hierarchy |
| **Resolved style** | the actual applied colours / spacing / radii / borders / fonts → catches *style drift* | the live React component tree over the **Metro CDP** connection (rozenite / agent-cdp) |

> Tool names and CLIs in this space move fast. What's load-bearing is the *capability* (a structural tree dump + a resolved-style read from the running app), not a specific binary. Before relying on one, confirm it's installed and check its current command surface; if the named tool is gone, find the current equivalent that provides the same capability. If neither layer is obtainable in this environment, that's a **blocker to report — not a cue to fall back to eyeballing** (see "When a layer can't run").

## 1. Structure layer — `axe describe-ui` (or Maestro hierarchy)

`axe describe-ui` (the cameroncooke/AXe simulator CLI) emits a deterministic JSON dump of the iOS accessibility tree for the foreground app: nodes, roles, exact frames (x/y/w/h), and text. Maestro's view hierarchy gives a similar structural tree. Either becomes `target.structure.json`.

The **present/divergent/absent ledger and the structural diff come from here** — compare this tree against the parsed mock DOM (`ref.structure.json`). Because it's node-and-text matching, not pixels, the missing-element and wrong-text calls are deterministic with near-zero false positives — exactly the class a screenshot or a code-read misses.

Pairing caveat: the mock uses `div`/`span`/`h2`; RN surfaces as `View`/`Text`/accessibility roles. **Pair nodes by text content, accessibility label, and sibling order — never by tag name.** A small custom normalizer that strips both sides to `{role-ish, text, children[]}` before diffing is worth writing once; it's the one genuinely custom piece of this pipeline.

Maestro quirk: it *merges* some composite views (a toggle initialised with a label can collapse into one node), so a control can look absent when it's folded into a parent. When the structure tree looks surprisingly flat, cross-check with `axe describe-ui` before recording an "absent".

## 2. Resolved-style layer — Metro CDP (rozenite / agent-cdp)

RN 0.85 added support for multiple simultaneous Chrome DevTools Protocol connections to Metro (default port 8081). Tools like Callstack's **rozenite** / **agent-cdp** attach over that connection and read the **live React component tree**, exposing the resolved style props applied to each node *before* Yoga flattens them. This is the only way to get true applied colours/spacing/radii on native iOS without react-native-web. Write it to `target.styles.json` and diff it property-by-property against the mock's `getComputedStyle` (`ref.styles.json`).

Setup is moderate (the app must be running on the simulator with Metro up; you add the inspector middleware/connection). It currently can contend with the standard RN DevTools browser connection — expect to use one at a time.

**Reality check — the CDP path is often gated.** On RN's New-Architecture "Fusebox" inspector, a plain external CDP client frequently can't drive the runtime: the device-level `/json/list` URL 401s, and the real `/json` target (`…&page=1`) accepts the socket but **never answers `Runtime.evaluate`** because Fusebox expects a client-identification handshake that rozenite implements only for its *own* browser frontend, not for your script. rozenite is also a DevTools-*panel* framework with **no headless/file egress** — its data lands in a browser panel a human reads, so it cannot feed a file-based audit even when connected. When you hit this, don't fight the handshake or install rozenite; use the in-app harness below, which needs none of it.

## 2.5 In-app instrumentation harness — the reliable extractor (and it MUST carry structure + geometry)

The dependable way to extract the rendered app — no CDP, no Fusebox, no panel — is a **dev-only module that runs inside the app**, walks the fiber tree via `global.__REACT_DEVTOOLS_GLOBAL_HOOK__.getFiberRoots(...)`, and **POSTs to a tiny local collector** (`fetch('http://localhost:<port>/dump', …)`; the iOS sim shares the host network). Add it dev-only (`if (__DEV__) require('./.audit/measure')` in the root, gitignored, removed at the end). Tag each node with its native screen container (`RNSScreen`/`RNSTabsScreenIOS`, increment a seq) so you can isolate the **foreground** screen — RN keeps tabs and pushed screens mounted, so a raw walk returns every mounted screen merged.

**The lesson that makes this section exist:** a harness that emits a flat list of `{type, text, style}` per node is a *style* extractor, and it is **layout-blind** — it cannot tell a `row` card from a `column` card, a present divider from an absent one, or a 2-up grid from a stack. Per node, the harness MUST also emit:

- **containment** — the parent chain or a `path`/`depth` so you can rebuild the *ordered nested tree*, not just a bag of nodes;
- **layout** — `flexDirection` (and `alignItems`/`justifyContent`) from the flattened style, so "icon above vs beside the label" is a diffable fact;
- **geometry** — `measureInWindow` (or the Fabric `getBoundingClientRect`) → `x/y/w/h` per node, so relative position, ordering, and "is there a 12px gap (divider) between rows" are measurable.

Then the structural diff (skill Phase 3B) runs on the containment + flex + geometry, and the style diff (3C) on the flattened styles — from the *same* artifact. Skipping containment/geometry is exactly how a passing-looking audit ships a screen whose every colour matches and whose entire layout is wrong.

**Don't write this harness from scratch — drop in the bundled one.** `assets/rn-harness/` ships a complete, generic version (`measure.js` + `collector.js` + `README.md`) with 4-step setup. Beyond containment/geometry it already captures, per node: `owner` component, sub-pixel `rect` (via `nativeFabricUIManager.measureInWindow(stateNode.node)` — on Fabric `stateNode = {node, canonical}`, so it's NOT on `stateNode`), effective **inherited** text style + `fontLoaded` (declared-vs-loaded), `effOpacity`, `placeholderTextColor`, **icon `name`+`iconColor`**, image `source`/`resizeMode`, **SVG `fill`/`stroke`/`d` internals**, `gradient` stops, **native nav/tab `cfg`** (the JS-controlled `RNSScreenStackHeaderConfig`/`RNSTabs*` props — title, `largeTitle`, tint, tab label/icon/badge), a11y state, and `press`. Composite-only props (onPress, icon name/colour, gradient) are threaded down from composite fibers to host nodes.

**Its honest blind spots** (README has the full list) — cover these with a targeted screenshot or an extra dump, never by pretending: the final native **pixel** render (system blur/glass, native title/tab font metrics); non-SVG canvas/Skia/GL internals; animation timing; interaction states / dark mode / data variants / below-fold (re-dump after triggering); release builds (no DevTools hook). A harness captures *resolved style + geometry* (intent + layout), not pixels — where declared ≠ rendered, the screenshot is the evidence.

## 3. Navigate the sim — DEEP-LINK FIRST (the single biggest speedup)

Before reaching for Maestro to *navigate*, use deep links. **Why it matters:** every
`maestro test` spins up a fresh XCUITest driver (`xcodebuild test-without-building` →
connect to the sim) costing **~15-20s before the flow even runs**. Agents call Maestro
once per action (tab tap, scroll-to-element, assert), so a single screen pays that tax
8-9×. In a measured audit, **Maestro navigation was ~70% of all wall-clock**; the actual
fidelity work (differ, edit, git) was <3%. Per-call: **Maestro ~18s vs deep link ~0.5s vs
idb tap ~0.3s.**

expo-router (and most file-based RN routers) **map route files to `<scheme>://` URLs out
of the box** — route GROUPS in parens (`(tabs)`, `(screens)`) are stripped from the URL.
So deep-linking replaces almost all navigation:

- **Tabs / screens:** `xcrun simctl openurl <SIM> "<scheme>:///<route>"` (e.g. `myapp:///home`,
  `myapp:///documents`, `myapp:///analysis-new?kind=disclosure`). Read the `scheme` from
  `app.json`; routes are the file paths minus the group parens.
- **Detail screens (`[id]` routes):** you rarely need a real id — deep-link the LIST then
  **idb-tap the first row** (~5× faster than a Maestro row-tap, no id discovery).
- **Routeless affordances** (a custom header control a router can't address, a sheet/popover):
  idb coordinate tap, or — only if nothing else works — ONE batched Maestro flow with
  several `tapOn`s so the ~15-20s startup is paid once, not per tap.
- **Never** Maestro-tap a tab or a list row that a deep link / idb can reach.

`assets/rn-harness/nav.sh` is a drop-in helper (`nav.sh tab|open|detail|tap|prime`), each
call polling the harness dump to settle (no blind `sleep`s). Set `MF_SIM/MF_DUMP/MF_SCHEME/MF_BUNDLE`.

Three caveats this navigation hits:

- **First deep link per device raises a native "Open in <app>?" confirmation** — a UIKit
  alert the RN harness dump can NEVER see, so a deep link can silently STALL behind it. Run
  `nav.sh prime` ONCE per device at session start (openurls + Maestro-taps Open/Allow);
  `settle` also auto-taps it on a stall.
- **RN keeps ALL tabs/screens mounted**, so the dump is a MERGE of every mounted screen — an
  anchor that lives on tab X reads `true` even when tab Y is foreground. The deep link DOES
  switch the foreground (confirm with a screenshot), but you can't *prove* the switch from
  the dump alone; rely on the differ's `--anchor` to scope the merged dump, and screenshot.
- **A wedged/stale Maestro driver causes silent false-negative taps** — a `tapOn` reports
  FAILED (or no-ops) though the element is plainly visible, sometimes even after the tap
  actually landed. Recover with `pkill -9 -f maestro`. (Multi-sim Maestro *does* work; driver
  contention just makes stale drivers more likely — kill-and-retry, don't conclude "no multi-sim".)
- **If dev-login / data silently hangs, check the BACKEND first** — a paused Docker / down BFF
  makes every login + fetch time out, which looks like a nav or sim bug but isn't. Confirm the
  backend answers (`curl`) before debugging the app.

## 3a. Maestro — last-resort UI driver + supplementary screenshots

When a surface genuinely needs UI driving (a routeless sheet, text input, an assertion),
Maestro is still the tool — and it captures the `*.png` you keep *alongside* the artifacts
(supplementary, for the spatial/overlap fallback — not the evidence). Batch its taps into one
flow to amortize the driver startup. **Pick an iOS runtime Maestro can drive:** on iOS-26 the
Liquid-Glass native tab-bar labels are not reliably text-tappable; a consistent **iOS 18.x**
sim taps them fine — keep every sim in a parallel run on ONE runtime (and deep-link/idb where
native chrome won't tap).

- Flows are YAML (`appId`, then `tapOn`/`inputText`/`assertVisible`/`takeScreenshot: /abs/path`). The simulator is a **serial resource** — one screen at a time; the orchestrator drives navigation, sub-agents read the resulting artifacts and edit disjoint files in parallel.
- **Dev-client reconnect fatigue:** each `launchApp` reloads the JS bundle on a dev build; many flows back-to-back can hang a later launch. Run flows individually or restart Metro between batches; a release build with an embedded bundle is stable for batches. macOS has no `timeout` — guard a flow with a backgrounded kill-after-N-seconds if you need a ceiling.
- Raw capture without Maestro: `xcrun simctl io <udid> screenshot out.png` (3× on retina, so 1px ≈ 0.33pt). A dev client connects to whatever Metro is at the host/port — if two apps share a Metro port you can load the wrong bundle; use a **separate simulator + its own Metro port** when another app holds the default.
- **An `accessibilityLabel` on a pressable shadows its inner text.** `<Pressable accessibilityLabel="Generate AI brief"><Text>Generate</Text></Pressable>` is ONE accessibility element labelled "Generate AI brief" — the inner "Generate" is gone from the tree, so `tapOn: { text: "Generate" }` **fails**. Tap the label: `tapOn: { text: "Generate AI brief" }`. (`tapOn: { id: ... }` matches `testID`/accessibilityIdentifier, **not** the label, so it also misses.) This is the general rule behind "tap a card CTA by its accessibilityLabel, not its inner text".
- **`launchApp` restores the LAST route, not the tab root.** A flow that assumes it lands on a tab home must tap the tab first (`tapOn: "Discover"`) — otherwise it's still on whatever screen the previous run left mounted.
- **Submitting a field: prefer the keyboard send key over tapping the send button.** A composer/search/revise field with `onSubmitEditing` + `returnKeyType:"send"` submits reliably via `- pressKey: Enter`. Tapping the send button can no-op when the button is `disabled` until `draft.trim()` and the typed text hasn't committed to React state yet (an autocorrect suggestion still pending in the keyboard bar is the tell).
- **Streaming / AI-generation screens need a real wait.** The harness re-dumps every ~1.5 s, but an AI stream takes several seconds — wait ~8–12 s and re-screenshot so you measure the **settled** result, not a mid-stream frame or an empty loading state. Re-dump only after the body stops growing.

## 4. Fallback A — react-native-web (only if it boots)

`react-native-web` renders RN components to real DOM, so `getComputedStyle` works like the reference. It's a *fallback* for the style layer, not the method: RNW only *approximates* native rendering (it maps RN styles to CSS; native shadows, blur/glass, fonts, and the native tab bar differ), so a clean RNW diff still needs a sanity check against a real device screenshot.

Boot is iterative — **native-only modules crash it one at a time**. Stub them in the metro web resolver, gated on `platform === 'web'` so native builds are untouched:

```js
// metro.config.js — inside config.resolver.resolveRequest, before the default return:
const WEB_STUBS = {
  'react-native-branch': path.resolve(__dirname, 'web-stubs/noop.js'),
  'react-native-maps': path.resolve(__dirname, 'web-stubs/maps.js'),
  'expo-secure-store': path.resolve(__dirname, 'web-stubs/secure-store.js'), // localStorage shim so auth can persist on web
  'expo-glass-effect': path.resolve(__dirname, 'web-stubs/glass.js'),        // passthrough View
  '@react-native-firebase/app': NOOP, '@react-native-firebase/messaging': NOOP,
  'expo-notifications': NOOP,
};
if (platform === 'web' && WEB_STUBS[moduleName]) {
  return { type: 'sourceFile', filePath: WEB_STUBS[moduleName] };
}
```

Stub shapes: a no-op is a `Proxy` whose every property is a no-op function; a native UI component (`react-native-maps`) stubs to a `View` passthrough; `expo-secure-store` stubs to a `localStorage`-backed `getItemAsync/setItemAsync/deleteItemAsync` so the login token persists and you reach authenticated screens. Set the viewport to the mock's frame (e.g. 393×852). Clear the metro cache after a resolver change and hard-reload past stale error overlays.

**Know when to stop.** Apps built on **native-only primitives** — e.g. `@expo/ui/swift-ui` (`Host`, `VStack`, `BottomSheet`) for an iOS-native look — have *no web rendering by design* and are architecturally unbootable under RNW. That's a *finding* (it's why native chrome wins), not a wall to push through; drop to the CDP style layer instead. Don't sink hours into a web boot that can't happen.

## 5. Fallback B — source-resolved StyleSheet (intent only, never a ✓)

RN has no CSS cascade: a component's declared style is its `StyleSheet` object resolved against literal token constants — no inheritance (beyond a few text props), no specificity, no `calc`. That makes source-resolution *exact for what's declared*, which is genuinely useful for **two narrow jobs**: (a) confirming token *intent* (is the mock's `#1F3FA6` even in the app's token set?), and (b) locating **where to fix** once a real extraction has already flagged a divergence.

What it **cannot** do — and why it never closes a ledger row by itself: it can't tell you the component mounted, that the prop reached the node, that the element isn't covered/empty/relocated, or that a conditional didn't render a different branch. A screen "verified" by reading its StyleSheet is **unaudited**. Use this only after the structure + style artifacts exist, to explain a diff and target the edit.

Watch for **systematic token offsets** (every radius 2px tighter, every spacing step shifted): that's one decision in the generated token source, not a per-screen bug — flag it for the user rather than hand-editing a shared/generated token to chase one mock.

## 6. When a layer can't run

No simulator, no Metro/CDP, RNW won't boot, AXe not installed — any of these removes a measurement layer. **Report it as a blocker and stop on the affected screens; do not substitute a screenshot-and-reasoning ledger.** State precisely which layer is missing and what would restore it (boot the sim, start Metro, install the CLI). Partial coverage is fine *if labelled* — "structure measured via AXe; style layer unavailable (no CDP), N rows pending" is honest; silently grading those rows ✓ from screenshots is the exact failure this skill exists to prevent.

## 7. Native chrome wins — for chrome, not content

When the implementation deliberately uses native components — a native bottom tab bar (`expo-router` `NativeTabs`), native nav headers with the OS back chevron and bar-button items, native sheets/modals, native blur/glass — those are the intended look; do **not** recreate the mock's hand-drawn versions. Record the chrome boundary once (Phase 1) and don't refight it per screen.

Two guardrails:
- This applies to **chrome**, never **content** — "native wins" must not become a blanket excuse to skip auditing the screen body (the native-chrome-as-excuse anti-pattern).
- A real defect can still live *in* the chrome: a self-drawn title overlapping the status bar (missing safe-area inset), a custom circular back button where the native chevron belongs, a tab badge shown when it shouldn't be. "Use native chrome" also means *prefer the native affordance over a custom one* — flag custom-drawn back/nav buttons where a native header button is intended.

## 8. Common RN defects this pass surfaces

Invisible in source, only show at render — which is the whole point of extracting the rendered tree:
- **Raw/unformatted numbers** — a market cap printed `56252638047.35` instead of `56.25B` (a value sent through a price formatter instead of a compact one). The structure artifact shows the literal text; grep the formatter at that cell.
- **Duplicate React keys** — a `.map()` whose `key` is built from non-unique fields throws "two children with the same key" on duplicate data (corporate-action feeds). Fix by appending the index; audit every `.map()` in a changed file.
- **Status-bar / Dynamic-Island overlap** — a `headerShown:false` screen drawing its own large title with a fixed `paddingTop` instead of `insets.top + n` (`useSafeAreaInsets`). The structure artifact's top-frame y reveals it.
- **Cosmetic feature affordances** — an "AI" badge / mic / "Ask in plain English" that renders but does nothing, while the real search/interpretation isn't wired. Present in the structure tree, absent in behaviour → these belong in the **functional-gaps document**.
- **Streaming-generation abort race** (when you *build* a screen that streams real content) — a `generate` callback that depends on the `streaming` state is recreated the instant streaming flips true; if a `useEffect` that kicks off generation lists `generate` in its deps, the dep change re-runs the effect and its **cleanup aborts the in-flight stream** (symptom: every generation dies with "stopped before it finished"). Guard concurrency with a `useRef` (so `generate` stays referentially stable, deps `[id]` only) and put the abort in a separate **unmount-only** effect (`useEffect(() => () => abortRef.current?.abort(), [])`). Also strip stray model markdown (`**`, `---`, `*`) when rendering an LLM's free-text into a structured layout.
