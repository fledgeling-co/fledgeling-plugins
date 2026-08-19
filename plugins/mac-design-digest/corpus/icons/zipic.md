# Icon: Zipic

- **Era:** Big Sur unified (3D-rendered skeuomorphic-object variant; not yet Liquid Glass) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 512×512, SHA-1 `aa17c980`) — likely a downscaled web render of a 1024 master; fine gauge detail already slightly soft in source.
- **Subject the icon must communicate:** native image compression/conversion utility (tagline: "Native, private image compression and conversion for macOS").

| Dimension | Reading |
|---|---|
| Background | scene — a rendered charcoal machine body *is* the squircle; matte-plastic ramp #626262 (top) → #3D3D3D (bottom), corners vignette to ~#242424 (measured) |
| Glyph | object — a physical "compression device": LEVEL dial/gauge (0–10) top, output slot dispensing a stack of glossy photo prints bottom. Photo shows a blue landscape (#8FA0DD→#5066B2) + gold sun (#E6CA0B) on white stack (#F0F0F0/#E4E4E4/#C0C0C0). Two focal masses on the vertical axis (dial upper-third, photo lower-half) |
| Overlay device | none — no diagonal tool crossing the plane; all devices are integral to the depicted object |
| Light model | single soft top-down studio light: body highlight at top decaying to shadow at bottom; short soft baked micro-shadows under the photo stack, inside the slot, and under the knob; matte finish, no specular glass highlights |
| Layer stack | charcoal body (back) → recessed gauge panel + knurled knob + LED (inset) → recessed output slot → stack of photo prints emerging (front), top print carrying the landscape |
| Palette economy | 1 neutral ground (charcoal) + 2 chromatic families (indigo-blue landscape, gold-yellow); accent saturation reserved for the LED and the photo. Gold appears twice (LED + sun) — an intentional "set the level → this comes out" rhyme |

## Signature devices
- **[GOLDEN-NUGGET] Feature-as-machine skeuomorphism.** The app's core control — compression *level* — is literalised as a physical `LEVEL 0–10` dial with a knurled knob and a gauge arc. The icon is a didactic diagram of what the app does: dial a level, images come out. This is committed subject-mining, not a generic glyph-on-gradient.
- **Photos physically dispensing from a slot** as a stacked ream — the "output" of compression made tangible; strongest surviving cue at small sizes.
- **LED status light** (bright yellow #FDE623) top-right — quotes real appliance hardware and ties chromatically to the sun in the output print.
- **Matte soft-3D render register** (Blender/C4D studio-light look) rather than flat vector — places it in the Big Sur "rendered object" indie tradition.

## Failures
- **#4 16px squint — FAIL.** Verified by downscale: at 16px the dial, `LEVEL` text, numerals, and tick marks fully smear into a gray blob; the icon reads only as "dark box with a blue+white photo strip," and the *compression* idea is lost. Marginal at 32px (device+photo legible, dial still a blob). The icon is built for hero/large display, not Dock/Spotlight/menu-bar duty.
- **#12 no-text — FAIL.** Baked text present: `LEVEL` plus gauge numerals `0 / 5 / 10`. Words/numbers in icons are the classic small-size liability and directly feed the #4 smear.

## Soft passes / flags
- **#3 silhouette (soft).** Filled solid black the outer shape is a plain squircle — the subject is not nameable from silhouette alone; legibility rides entirely on internal figure-ground (dial circle, photo rectangle). Inherent to full-bleed object icons, but a real robustness cost.
- **#10 variant robustness (soft, era-conditional).** Not authored in Icon Composer; the composition depends on the charcoal ground and would not gracefully yield tinted / clear / mono renders under macOS 26 Liquid Glass. Fine for its Big Sur era; a re-author would be needed to survive current-era appearance modes.
- **#7 figure-ground (soft).** Photo-on-body contrast is excellent (>7:1); dial-face-on-body is only ~2:1 — the dial leans on shadow/inset, not tone, to separate.
- **HIG note:** a soft outer drop shadow is baked into the PNG (alpha bbox 26–486 vs solid squircle 50–461). Apple asks that the system apply the shadow; baked shadow is common on macapp.supply renders and on Big Sur-era third-party icons.

## Rubric ledger
| # | Check | Verdict |
|---|---|---|
| 1 | Mask discipline | pass — body fills the squircle, no corner-radius fight |
| 2 | Grid adherence | pass (soft) — balanced two-mass vertical composition, full-bleed |
| 3 | Silhouette | pass (soft) — generic squircle solid; relies on internal contrast |
| 4 | 16px squint | **FAIL** — dial/text/ticks smear; compression idea lost |
| 5 | Single light model | pass — one coherent top-down studio light |
| 6 | Palette economy | pass — neutral + 2 hue families, accent reserved |
| 7 | Figure-ground | pass (soft) — photo pops; dial-on-body only ~2:1 |
| 8 | Depth coherence | pass — sensible inset→emerging stack; shadows track the light |
| 9 | Era coherence | pass — all devices in one matte soft-3D register |
| 10 | Variant robustness | pass (era-exempt) — would fail Liquid Glass tinted/mono |
| 11 | Personality | pass (strong) — feature-as-machine, multiple named devices |
| 12 | No-text | **FAIL** — `LEVEL`, `0/5/10` baked in |

**Score: 10/12** (fails #4, #12 — both small-size/text liabilities on an otherwise characterful hero icon.)

## Full-bleed / grid measurements
- Solid squircle: 50→461 px = **411 px of 512 (80.3%)** each axis — proper Big Sur full-bleed squircle proportion (~822/1024 scaled), not a floating centred glyph.
- Body ramp (left edge, top→bottom): #626262 · #5F5F5F · #5B5B5B · #555555 · #4F4F4F · #474747 · #3F3F3F · #3D3D3D (measured) — subtle, short-range top-lit gradient.

## Brand coherence (vs cover.png)
The cover reuses the icon's exact triad: charcoal card grounds, periwinkle-blue section headings, and gold accents (`90%+`, `One-Time Purchase`). Icon and marketing share the **charcoal + indigo-blue + gold** palette — coherent brand system, not an orphan icon.

## Rhymes with
- Big Sur-era **"app-as-appliance" rendered-object icons** — utilities depicted as physical gadgets/machines under soft studio light (the compression-as-press/printer metaphor family), rather than the flat-gradient-glyph family or the Apple diagonal-tool family (TextEdit/Preview). *(Hint only — needs ≥3 independent icons before any cluster is promoted.)*
