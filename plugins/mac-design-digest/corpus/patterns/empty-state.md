# Pattern: empty-state

Cross-app synthesis of empty / ready / completion states — the surface a utility shows before content exists or after a job finishes. Native-lineage evidence only. Kit floor: `kit/macos-27.md` — hero figures at LargeTitle/Title1 (22–26pt); one filled primary; capsule bezel; primary text 85% black light / #FFFFFF dark.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Purge | completion card (dark) | centred stack: circled checkmark → **`2.98 GB` display figure** → "moved to Trash" (secondary bold) → **tangible-equivalents chips** ("🖼 710 photos / ♪ 355 songs", capsules) → "⚡ done in 0.3 seconds" → tertiary footnote → **full-width white "Done" capsule**; reversibility written into copy | (estimated)(confirmed) |
| Mole | Clean "ready" hero (dark) | centred vertical hero over navy-dusk sky: photoreal 3D Earth globe → **`86.4 GB` bold figure** → dimmed mono caption → single blue-tinted capsule primary "Return to Earth"; reads as a reclaimable-space ready state | (estimated)(inferred) |
| Viaduct | single-example ready state (dark) | centred: app name + one-line subtitle → **content card with a real example** (Dark Reader icon + name + green ✓ "Installed in Safari" capsule pill) → full-width teal CTA "Open extension"; Hick's Law at its floor | (estimated)(inferred) |
| Open Timer | idle timer (dark) | oversized tabular time hero + 7-bar session sparkline (glanceable "how has today gone"); single accent action | (estimated)(inferred) |
| Cachesweep | reclaimable hero (dark glass) | **giant `120.3 MB` hero metric ~36pt** answering the one question + one full-width capsule "Clean Selected" | (estimated)(inferred) |
| Satu | no-task popover (light) | collapses the task-header to one grey full-width pill ("Stop chilling") — the minimal ready/empty state | (estimated)(confirmed) |
| macUSB | welcome screen (dark) | USB icon + wordmark + "Download. Flash. Boot." tagline + one blue "Start →" capsule + footer | (estimated)(confirmed) |

## Converged rules

- **Centred vertical stack: hero visual/figure → short primary line → optional secondary line → one filled primary action** — apps: Purge, Mole, Viaduct, Cachesweep, macUSB — **(canon)**. The empty/ready state is a single-column, single-decision surface.
- **A dominant hero figure or icon carries the state; value outranks label by scale** — apps: Purge (`2.98 GB`), Mole (`86.4 GB`), Cachesweep (`120.3 MB` ~36pt), Open Timer (oversized time) — **(canon)**. Scale-as-hierarchy answers "what now / what happened" pre-attentively.
- **Exactly one filled primary CTA; Hick's Law taken to its floor (one obvious next step)** — apps: Purge (Done), Mole (Return to Earth), Viaduct (Open extension), Cachesweep (Clean Selected), macUSB (Start →) — **(canon)**.
- **Warmth/reassurance is spent here more than anywhere: completion copy, tangible equivalents, thematic imagery** — apps: Purge (photos/songs equivalents + "moved to Trash" reversibility), Mole (Earth globe + "Return to Earth"), Cachesweep (live green ▲ deltas) — **(recurring→canon)**; a category people distrust (cleaners) reframed as calm/forgiving.

## Divergences

- **Completion vs pre-content vs ready-to-run.** *Completion* (Purge result card, after a job) vs *ready-to-run* hero (Mole Clean, Cachesweep, Open Timer — content exists, awaiting the action) vs *single-example onboarding-empty* (Viaduct, macUSB welcome). All share the centred-stack + one-CTA shape; they differ in whether the hero shows a result, a reclaimable total, or a first-run example.
- **Illustration vs pure typography.** Thematic imagery (Mole's 3D Earth, Satu's mascot art on adjacent surfaces) vs a clean numeric/glyph hero (Purge checkmark, Cachesweep metric). The illustration route tracks the warm-consumer clusters; the numeric route tracks the graphite/telemetry utilities.
- **CTA colour.** System-accent / system-blue (macUSB, Mole) vs **brand hue** (Viaduct teal) — the brand-hue CTA is a flagged accent-binding tell where present, but the *one-CTA* rule holds regardless.

## Generation guidance

- **Layout:** a centred single column. Top-to-bottom: **hero** (a large figure ~34–48pt for a metric/result, or a thematic illustration/icon), a **short primary line** (what this is / what happened), an optional **secondary line** (context, dimmed), then **one filled primary CTA**.
- **Hero:** make the number or icon the dominant element (value outranks its label by scale). For a result state, pair a success glyph + the figure + a plain-language line ("moved to Trash", not "deleted").
- **One action only:** a single filled capsule primary bound to the system accent. Do not add a competing second primary. Secondary/dismiss actions stay quiet (plain text or the neutral white capsule Purge uses).
- **Spend the warmth budget here:** completion copy, tangible equivalents ("710 photos"), or thematic imagery are appropriate exactly on this surface (they close the description-experience gap); keep the rest of the app quiet by contrast.
- **Contrast watch:** the tertiary footnote that carries reassurance is the most-often-diluted element (Purge's ~25% white footnote, Mole's dim mono caption) — keep any load-bearing reassurance at the secondary (~55% white) tier, not tertiary.
- **Reversibility:** if the state follows a destructive action, state the undo path in the copy (Purge's "Empty your Trash to reclaim this space") — forgiveness written into the layout.
