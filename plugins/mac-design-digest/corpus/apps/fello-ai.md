# Fello AI — profile

- **Source:** macapp.supply (marketing cover only — no clean screenshots supplied) · **Surfaces digested:** main chat window (dark), from a marketing composite · **Last updated:** 2026-07-19
- **One-sentence identity:** A ChatGPT-desktop clone wearing a genuine Mac frame — model-switcher-as-hero over a generic dark chat body — think "Raycast AI's aggregator pitch rendered in the Electron-AI-wrapper house style."
- **Cluster:** ai-chat-dark (candidate) — unassigned pending synthesis
- **Lineage:** web-electron (low confidence) — non-native evidence, excluded from macOS canon. See lineage note.
- **Era (chrome):** custom-drawn dark (not Liquid-Glass, not legacy-native; flat opaque graphite)

## Lineage note (why this is contrast evidence only)

This is the diagnostic Catalyst/cross-platform split: a **genuine Mac frame + native-correct source-list sidebar** (real colored traffic lights, inset-rounded selection fill, sentence-case section headers "Today"/"Past 7 days" in secondary grey — the #1 sidebar authenticity tell, passed) wrapping a **web-chat body** built from non-native idioms:

- Circular send button with up-arrow glyph — an iOS/ChatGPT convention, not any stock macOS control.
- Mode / Model pop-ups rendered with a **single** down-chevron (native `NSPopUpButton` value pickers use the **double** up/down chevron) — custom-drawn.
- Outlined "Attach Files" / "Skills" composer chips — a web composer pattern.
- Right-aligned grey rounded user bubble — generic cross-platform chat.
- Body/list text runs ~14px-class with generous ~1.5 leading — heavier than macOS 13pt body.

The custom-drawn controls (not stock UIKit inset-grouped tables or `UISwitch` pills) lean the call toward **web-electron** over strict Catalyst, but the native sidebar keeps confidence **low** — could be cross-platform SwiftUI or well-dressed Catalyst. Either way the body grammar is non-native, so **nothing here feeds macOS canon**. Compounding the uncertainty: the only input is a 1200×630 marketing composite (window is ~742px wide on a gradient backdrop with overlaid provider pills covering the lower sidebar), so all pixel values are `(estimated)` at best and chrome is rendered slightly oversized vs a true logical window.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/content | ~#16181B graphite (estimated)(inferred) | | main chat canvas, dark mode |
| bg/sidebar | ~#202225, faint separation from content (estimated)(inferred) | | source list |
| sel/sidebar-row | ~#34363A inset-rounded fill, ~8px radius, no accent tint (estimated)(inferred) | | native-correct shape; grey (inactive-style) not accent-tinted |
| bubble/user | ~#3A3B3F fill, ~16px radius, right-aligned (estimated)(inferred) | | generic chat bubble |
| accent/brand | gold/amber sparkle ~#F5B301 (estimated)(inferred) | | assistant avatar mark; app uses NO system-blue accent |
| type/title | ~15–16px bold, near-white (estimated)(inferred) | | window title "Fello AI – Your AI Assistant", centered |
| type/body | ~14px regular, lh ~1.5, #F4F4F6 (estimated)(inferred) | | list/answer text — larger than macOS 13pt body |
| type/section-header | ~11px, secondary grey ~#8E8E94, sentence case (estimated)(inferred) | | "Today", "Past 7 days" — native-correct |
| type/timestamp | ~10–11px, tertiary grey ~#6E6E73 (estimated)(inferred) | | de-emphasized dates under chat titles |
| ctrl/send | circular ~28px, light-grey fill, dark up-arrow (estimated)(inferred) | | iOS/ChatGPT send affordance |
| ctrl/composer-chip | outlined pill, ~8px radius, hairline border, icon+label (estimated)(inferred) | | Attach Files / Skills |
| ctrl/model-pill | grouped capsule containing Mode + Model pull-downs, single ⌄ chevron, ~1pt divider (estimated)(inferred) | | container-morph grouping; single chevron = non-native tell |
| chrome/trafficlights | genuine red/yellow/green cluster, focused window (measured-ish)(inferred) | | rendered ~15px dots — slightly large for the window scale |
| radius/family | bubbles ~16 · input ~16–20 · chips ~8 · model-pill ~14 (estimated)(inferred) | | 3–4 radius tiers, roughly disciplined |

## Layout skeletons

**Main chat window (dark):**
- Left **source list sidebar** (~230px at composite scale): header row with "＋ New Chat" text-button aligned to the traffic-light band; "Search chats…" field; unlabeled top group (Bookmarks, "…Money Online", "…secake Recipe"); **"Today"** section header → selected row "Fello AI – Your AI Assistant / 12.10.2026" (inset-rounded grey fill) + "Writing Email to the Boss"; **"Past 7 days"** section. Each row: leading chat glyph, two-line title+timestamp, trailing chevron.
- **Content area:** unified-toolbar-style top with sidebar-toggle glyph (circular button) + centered bold title, trailing grouped **Mode / Model** pop-up pill.
- Conversation column: right-aligned user bubble ("What can you help me with?") → assistant turn led by a gold sparkle glyph + intro line + a 6-item numbered list with **bold lead-ins** (Homework & Studying, Writing Help, Coding Support, Language Practice, Creative Ideas, Productivity Tips).
- **Composer** pinned bottom: multiline input ("Can you chang|"), a row of outlined chips (Attach Files, Skills) at lower-left, circular send button at lower-right.

## Signature moves

- **Model-switcher-as-hero.** The one genuine design decision: the primary chrome control isn't a native action — it's a paired **Mode + Model** pop-up capsule, and the marketing composite amplifies it by ringing the window with nine provider pills (GPT, Claude, Gemini, Grok, Qwen, Deepseek, Perplexity, Nano Banana, GLM). The product's whole promise — one client, every model — is expressed as UI. Hick's-Law-smart in-app (a huge model space compressed to two compact pickers); choice-overload *signaling* in the marketing swarm.
- **Gold sparkle as the sole warm accent** in an otherwise monochrome graphite field — a Von Restorff anchor that marks assistant turns. (But see Defects — it rhymes with the ChatGPT/Gemini sparkle rather than owning a mark.)

## Defects

- **Trade-dress mimicry (persona lookalike constraint, not in the anti-pattern taxonomy).** The app icon is a near-clone of OpenAI's interlocking-knot mark rendered silver-on-graphite, and the assistant avatar is a generic AI sparkle. This borrows authority/trust from OpenAI's visual identity (Cialdini authority-transfer via trade dress) rather than establishing its own — a brand-integrity finding a corpus should flag, not learn from.
- **Non-native controls.** Single-chevron Mode/Model pop-ups (native value-picker = double chevron); circular iOS-style send button on a desktop surface. Records as tells + corrections, not mac taste.
- **Density inflation.** Body/answer text ~14px-class with loose leading vs macOS 13pt body — reads iOS/web, not AppKit.
- **Contrast Dilution (marginal).** Composer-chip and pop-up hairline borders read below ~3:1 against the graphite ground — UI-contrast (#10) is the weakest rubric point; borders should step to a lighter fill on dark.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main chat window (dark, from composite) | 12/14 | #10 UI border contrast (sub-3:1 hairlines on chips/pop-ups); #6 measure borderline (wide content column); #14 focus appearance unverifiable in a static marketing shot |
| — native-tells audit | 6/10 | #1 lineage reads web/custom not AppKit; #5 density too large (~14px body); #6 no system-accent binding (gold brand mark instead of system blue on selection/focus); #9 custom single-chevron pop-ups, non-stock toolbar |
