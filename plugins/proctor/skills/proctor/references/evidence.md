# Evidence

Every load-bearing rule in `SKILL.md`, `tools.md` and `methodology.md`, mapped
to what it rests on. `Direct` means a source states it. `Inference` means the
sources support it but none states it; those are marked so a reader can
discount them independently.

The corpus is a five-backend research panel compiled 12 August 2026, plus
first-party inspection of one machine. Four members produced reports: Claude
local (64 sources), OpenAI gpt-5.6 (50), Gemini Deep Research max (52),
Perplexity Sonar Deep Research (20). Where members disagreed, the disagreement
is carried below rather than resolved.

---

## The two planes

| Rule | Type | Source | URL |
|---|---|---|---|
| Accessibility actions are IPC to the target process rather than events in the shared input stream, so they reach non-frontmost windows without stealing focus | Direct | `axcli` documents the two strategies explicitly: `--strategy ax` is "AXPress (no event posting)", `--strategy cg` is a global click that "brings app to front" | https://github.com/andelf/axcli |
| The same property is observable in shipping software — parallel operation on background apps without foregrounding them | Direct | MacStories (Viticci), first-hand testing | https://www.macstories.net/notes/openais-new-codex-app-has-the-best-computer-use-feature-ive-ever-tested/ |
| A binary can hold the full `AXUIElementPerformAction` / `AXUIElementSetAttributeValue` surface and import zero synthetic-event APIs, which is what makes non-foregrounding actuation architecturally possible | Direct | First-party import inspection of `SkyComputerUseService`; corroborated by all four panel members | internal: capability inspection 2026-08-12 |
| No framework promises that an accessibility action avoids activation — the contract is "perform this action", not "perform it invisibly" | Direct | OpenAI gpt-5.6 panel report, per-toolkit analysis | internal: docs/deep-research/openai-gpt56.md |
| Menu interaction generally needs the app raised; a single `AXPress` on a deep menu item does not reliably work standalone | Direct | `axcli` implementation replays `AXPress` on each ancestor to open nested submenus | https://github.com/andelf/axcli |
| Hover-gated UI cannot be triggered process-directed; the mitigation moves the real cursor and breaks the no-foreground property | Direct | `axcli` `--hover` flag and its documented consequence | https://github.com/andelf/axcli |
| `CGEventPostToPid` changes the delivery target but does not create an independent keyboard-focus universe; intra-app focus still needs an accessibility write | Direct | OpenAI gpt-5.6 panel report; `axcli`'s separate `--strategy pid` path | https://github.com/andelf/axcli |

## Secure Event Input

| Rule | Type | Source | URL |
|---|---|---|---|
| Secure Event Input is aimed at preventing interception of keyboard input; it disrupts event taps, global hotkeys and key observation | Direct | Apple Technical Note TN2150 | https://developer.apple.com/library/archive/technotes/tn2150/_index.html |
| Accessibility and Apple Events are separate IPC planes and are not globally disabled because Secure Event Input is active | Direct | OpenAI gpt-5.6 panel report | internal: docs/deep-research/openai-gpt56.md |
| Corroborating observation: with Secure Input actively held (`kCGSSessionSecureInputPID=400`), AppleScript still drove Chrome successfully | Direct | openai/codex issue #26743, first-party logs | https://github.com/openai/codex/issues/26743 |
| Secure Input is chronically stuck-on, and the I/O Registry method third-party apps use to identify the holder is "best effort" with situations where it is inaccurate | Direct | Apple DTS (Quinn), Developer Forums 726353 | https://developer.apple.com/forums/thread/726353 |
| Secure text fields redact their value and may expose no writable accessibility value — the transport survives, the element's semantics are deliberately restricted | Direct | OpenAI gpt-5.6 panel report | internal: docs/deep-research/openai-gpt56.md |

`SKILL.md` states that Secure Event Input "blocks [synthetic events] outright".
The evidence supports the weaker "event injection unreliable and observation
blocked" — see the disagreement below.

## Element references and Spaces

| Rule | Type | Source | URL |
|---|---|---|---|
| A retained `AXUIElementRef` to a window that moves to another Space remains valid and readable, while a fresh `AXUIElementCreateApplication` enumeration will not find it | Direct | Apple Developer Forums 121114; AltTab commit 3f5ea25 | https://developer.apple.com/forums/thread/121114 · https://github.com/lwouis/alt-tab-macos/commit/3f5ea25 |
| Therefore an agent that re-enumerates per step loses windows a reference-caching agent keeps; build for `AXWindowCreated` observation and caching | Inference | Claude local panel report, from the two sources above | internal: docs/deep-research/claude-local.md |
| A minimised window stays in `AXWindows` and reports `AXMinimized`; `AXWindowDeminiaturized` fires | Direct | Same forum thread and commit | https://developer.apple.com/forums/thread/121114 |

## The negotiated accessibility tree

| Rule | Type | Source | URL |
|---|---|---|---|
| Chromium enables accessibility support based on whether a client sets `AXEnhancedUserInterface` on the main application window | Direct | Chromium accessibility design docs | https://www.chromium.org/developers/design-documents/accessibility/ |
| Electron added `AXManualAccessibility` because `AXEnhancedUserInterface` is reserved by VoiceOver | Direct | electron/electron PR #10305 | https://github.com/electron/electron/pull/10305 |
| The tree materialises lazily: the first walk often returns empty and subsequent walks work — a pipeline that bails on the first miss falls back to OCR | Direct | screenpipe issue #3002, with reproduction | https://github.com/screenpipe/screenpipe/issues/3002 |
| Set both flags on the **application** element, not a renderer helper; the focused-app PID is frequently a helper and returns nothing | Direct | screenpipe #3002 | https://github.com/screenpipe/screenpipe/issues/3002 |
| Some apps still refuse until VoiceOver or Accessibility Inspector actually launches | Direct | Apple Developer Forums 756895 | https://developer.apple.com/forums/thread/756895 |
| The flag is detectable by the app: Electron exposes `app.setAccessibilitySupportEnabled` and reports assistive-technology presence to app code | Direct | Electron accessibility docs | https://www.electronjs.org/docs/tutorial/accessibility |
| Setting `AXEnhancedUserInterface` changes app behaviour measurably — it breaks and slows window positioning with window managers | Direct | vimac issue #78 | https://github.com/nchudleigh/vimac/issues/78 |
| Therefore an accessibility-driven suite measures the app in its assistive-technology configuration, not the one a human runs — a validity threat to disclose | Direct | Unanimous across all four panel members | internal: claims.json c13 |

## Capture and freshness

| Rule | Type | Source | URL |
|---|---|---|---|
| `CGWindowListCreateImage` is obsoleted in the macOS 15 SDK — a hard compile error, not a deprecation warning | Direct | MacPorts ticket #71136 (compiler transcript); JUCE issue #1414 | https://trac.macports.org/ticket/71136 · https://github.com/juce-framework/JUCE/issues/1414 |
| `CGWindowListCopyWindowInfo` was not deprecated and remains the enumeration path | Direct | Nonstrict, ScreenCaptureKit on Sonoma | https://nonstrict.eu/blog/2023/a-look-at-screencapturekit-on-macos-sonoma/ |
| `SCFrameStatus.idle` means the system generated no new frame because the display did not change; treat it as "no new pixels", never as an error | Direct | Apple, `SCFrameStatus.idle` | https://developer.apple.com/documentation/screencapturekit/scframestatus/idle |
| Apple's own sample guards on `status != .complete` and returns nil | Direct | Apple, Capturing screen content in macOS | https://developer.apple.com/documentation/ScreenCaptureKit/capturing-screen-content-in-macos |
| Dirty rectangles identify regions redrawn or moved in the captured output — they do not indicate pending application work | Direct | Apple, `SCStreamFrameInfo.dirtyRects` | https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects |
| A `.complete` frame does not prove the application freshly rendered it in response to recent state | Direct | OpenAI gpt-5.6 panel report, reading Apple's dirtyRects documentation | https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects |
| Off-screen windows emit completed frames only when there is mouse movement on the display containing the window, and only with pointer capture configured | Direct | Apple Developer Forums, ScreenCaptureKit tag | https://developer.apple.com/forums/tags/screencapturekit |
| An unchanged image hash alone cannot distinguish a static UI from a stale surface | Direct | OpenAI gpt-5.6 panel report | internal: docs/deep-research/openai-gpt56.md |
| Occluded windows, screensaver-active apps and apps on a non-active Space are all "hidden" by Apple's definition and are expected to halt drawing | Direct | Apple Energy Efficiency Guide | https://developer.apple.com/library/archive/documentation/Performance/Conceptual/power_efficiency_guidelines_osx/WorkWhenVisible.html |
| There is no supported API that forces an arbitrary third-party application to keep a minimised or hidden window rendering | Direct | OpenAI gpt-5.6 and Claude local panel reports, concurring | internal: docs/deep-research/openai-gpt56.md |
| The strongest available freshness assertion is three-way agreement between semantic state, compositor frame metadata and an app-owned render revision | Inference | Both best-sourced members reach it independently | internal: claims.json c15 |
| The ScreenCaptureKit window set and the `CGWindowListCopyWindowInfo` set legitimately differ, because SCK filters per-window privacy flags before frames reach you | Direct | Claude local panel report | internal: docs/deep-research/claude-local.md |

## Computed styles

| Rule | Type | Source | URL |
|---|---|---|---|
| macOS has no public cross-process object combining hierarchy, resolved theme, typography and paint the way browser DevTools does | Direct | Unanimous across all four panel members, with per-mechanism analysis | internal: claims.json c9 |
| Every richer mechanism requires code injection into the target: the View Debugger needs `DYLD_INSERT_LIBRARIES` of `libViewDebuggerSupport.dylib` plus LLDB expression evaluation | Direct | Adam Bell, reverse-engineering write-up | https://blog.adambell.ca/posts/20190724-Visualizing-Xcode's-View-Debugger/ |
| `MTLCaptureManager` is per-process self-capture, gated on `MetalCaptureEnabled` in the target | Direct | Catnip codes; `MTLCaptureManager.h` | https://alia-traces.github.io/metal/tools/xcode/2020/07/18/adding-framecapture-outside-of-xcode.html |
| Hardened runtime plus Library Validation is what blocks injection into notarised third-party apps — and it is already rejecting a first-party vendor's own signed helper | Direct | openai/codex issue #24013: "mapping process is a platform binary, but mapped file is not" | https://github.com/openai/codex/issues/24013 |
| So for an app you do not own, the ceiling is the accessibility tree plus pixels | Direct | Unanimous | internal: claims.json c9 |
| The durable answer for an app you own is a debug-only in-process reflector serialising the view and layer hierarchy with resolved colours, fonts, radii, constraints and Core Animation model/presentation values | Inference | The two best-sourced members independently recommend it as the build | internal: claims.json c10 |
| Model and presentation layer values differ exactly while an animation is in flight | Direct | Cameron Little, SwiftUI and Core Animation | https://camlittle.com/posts/2024-11-14-swiftui-core-animation/ |
| The accessibility projection of web content yields role, name, value, state and geometry — never the cascade | Direct | Claude local panel report; Texture issue #1954 on WKWebView out-of-process bridging | https://github.com/TextureGroup/Texture/issues/1954 |

## Settling and determinism

| Rule | Type | Source | URL |
|---|---|---|---|
| There is no native macOS analogue to CDP's `Emulation.setVirtualTimePolicy`; Core Animation timing runs in the out-of-process render server on the system clock with no supported hook to a test clock | Direct | Unanimous across all four members | internal: claims.json c12 |
| Even the CDP command is marked Experimental and carries known budget-never-expires hangs | Direct | Chrome DevTools Protocol, Emulation domain; chrome-headless-render-pdf issue #29 | https://chromedevtools.github.io/devtools-protocol/tot/Emulation/ · https://github.com/Szpadel/chrome-headless-render-pdf/issues/29 |
| `CALayer.speed` / `timeOffset` control is in-process only, so it is available for apps you own and not for foreign ones | Direct | Claude local panel report | https://camlittle.com/posts/2024-11-14-swiftui-core-animation/ |
| There is no universal native "UI quiescent" signal; the most defensible settle rule is a conjunction of several consecutive complete frames with no meaningful dirty rects, no relevant accessibility notifications, no pending app-owned work where available, and an upper timeout | Inference | OpenAI gpt-5.6, from the limitations of each individual signal; Claude local reaches the same shape | internal: claims.json c12 |
| Accessibility notifications are the least honest of the available signals: registration fails intermittently with `-25204`, some notifications do not fire for mouse selection, and observers die silently on element invalidation | Direct | Apple Developer Forums 741013; Apple, `AXObserverAddNotification` | https://developer.apple.com/forums/thread/741013 · https://developer.apple.com/documentation/applicationservices/1462089-axobserveraddnotification |
| Treat notifications as hints that trigger a re-read rather than as state; register on `kCFRunLoopCommonModes` or lose events during menu tracking and window resize | Direct | Claude local panel report, from the forum thread above | internal: docs/deep-research/claude-local.md |
| Per-step canonical hashing over a normalised tree with volatile fields masked, plus first-divergence and a 0–1 per-step instability score, is the buildable determinism metric | Inference | Both best-sourced members propose it independently; gpt-5.6 gives the formulae. No public tool or paper was found doing this on macOS | internal: docs/deep-research/openai-gpt56.md · claude-local.md |

## Parallelism

| Rule | Type | Source | URL |
|---|---|---|---|
| Apple silicon caps concurrent macOS guests at two per host, enforced in the kernel via `hv_apple_isa_vm_quota`, returning `VZErrorVirtualMachineLimitExceeded` (code 6) on the third | Direct | Independent web check; Eclectic Light | https://khronokernel.com/macos/2023/08/08/AS-VM.html · https://eclecticlight.co/2022/08/04/virtualisation-on-apple-silicon-macs-8-how-apple-limits-vms/ |
| The bypass requires disabling SIP and a boot argument | Direct | khronokernel | https://khronokernel.com/macos/2023/08/08/AS-VM.html |
| Virtualization save/restore is suspend/resume, not multi-snapshot — the framework deletes the save file after restore | Direct | Apple, Virtualization framework | https://developer.apple.com/documentation/virtualization |
| So real parallelism past two guests is a hardware purchase; within one session it comes from driving many windows process-directed, which does not contend for focus | Inference | Claude local panel report, from the kernel cap plus the single-session nature of WindowServer | internal: claims.json c16 |

## Grants, TCC and fleet policy

| Rule | Type | Source | URL |
|---|---|---|---|
| The accessibility API cannot be used from a sandboxed app, and will not work even if the user manually grants permission | Direct | Apple DTS, Developer Forums 749494 | https://developer.apple.com/forums/thread/749494 |
| Screen Recording cannot be silently granted by configuration profile by Apple's design; it is user-toggled | Direct | Hexnode PPPC deployment documentation | https://www.hexnode.com/mobile-device-management/help/automate-macos-tcc-pppc-permissions-deployment/ |
| A signed binary holding `com.apple.security.automation.apple-events` with its own TCC record is the standard configuration for having the Automation prompt attributed to itself rather than to its parent host — the responsible-process question | Direct | Scripting OS X, on avoiding AppleScript privacy prompts; corroborated by first-party TCC inspection | https://scriptingosx.com/2020/09/avoiding-applescript-security-and-privacy-requests/ |
| PPPC's ability to grant Accessibility was deprecated in macOS 26.2 and removed in 27, replaced by declarative App Settings supplying a managed default through a consolidated consent prompt | Direct | OpenAI gpt-5.6 panel report, citing Apple's WWDC26 app-management updates and the App Settings privacy object | https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web · https://developer.apple.com/documentation/devicemanagement/appsettingsappdictionaryobject |
| Apple's macOS 27 device-management documentation is explicitly pre-release and subject to change | Direct | Same Apple deployment page | https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web |
| Pre-seeding TCC grants in a VM guest works only with SIP disabled | Direct | jonnyzzz/tart-skills, documenting direct `TCC.db` writes at image build | https://github.com/jonnyzzz/tart-skills |

## Declared contracts

| Rule | Type | Source | URL |
|---|---|---|---|
| App Intents has no third-party programmatic invocation API; the sanctioned callers are Shortcuts, Spotlight and Siri | Direct | Apple WWDC25 Session 275; corroborated by all four members | https://developer.apple.com/videos/play/wwdc2025/275/ |
| No public API lets an arbitrary process enumerate installed apps' intents and invoke them by bundle id | Direct | OpenAI gpt-5.6 panel report | internal: docs/deep-research/openai-gpt56.md |
| `AppIntentsTesting` in macOS 27 invokes an app's **own** intents in isolation; it is a testing framework, not a cross-app broker | Direct | Apple WWDC26 session 240 | https://developer.apple.com/videos/play/wwdc2026/240/ |
| The `shortcuts` CLI is the practical escape hatch, and every call needs a timeout wrapper because a shortcut that prompts pauses forever; each shortcut's permission prompts must be pre-authorised interactively before unattended use | Direct | Crosley, Shortcuts reference; Apple Shortcuts user guide for the CLI itself | https://blakecrosley.com/guides/shortcuts · https://support.apple.com/guide/shortcuts-mac/run-shortcuts-from-the-command-line-apd455c82f02/mac |
| AppleScript `sdef` coverage is declining and inconsistent; URL schemes are write-only; NSServices are selection-scoped | Direct | All four members; Spotify's shipped-broken `sdef` as the worked example | https://community.spotify.com/t5/Desktop-Mac/Please-bring-back-AppleScript-support/td-p/1066196 |
| So the accessibility tree remains the only broad cross-application semantic surface | Direct | Unanimous | internal: claims.json c17 |

## The accessibility rubric

These are outside the research corpus — the panel studied observation and
control, not audit criteria — so each is cited to its own primary source.

| Rule | Type | Source | URL |
|---|---|---|---|
| `accessibilityIdentifier` exists to identify an element for UI tests without affecting the accessibility or UI experience | Direct | Apple WWDC23 session 10035, "Perform accessibility audits for your app" | https://developer.apple.com/videos/play/wwdc2023/10035/ |
| The AppKit surface is `setAccessibilityIdentifier(_:)` on `NSAccessibilityProtocol` | Direct | Apple Developer Documentation | https://developer.apple.com/documentation/appkit/nsaccessibilityprotocol/setaccessibilityidentifier(_:) |
| Putting a machine-readable string in the accessibility **label** so tests can find it is the named anti-pattern; the fix is to move it to the identifier | Direct | Apple WWDC23 session 10035 | https://developer.apple.com/videos/play/wwdc2023/10035/ |
| Identifiers are excluded from XLIFF localisation output, which is what makes them survive translation | Direct | Apple engineer statement, Developer Forums | https://developer.apple.com/forums/thread/108327 |
| The audit categories a platform audit uses are contrast, hit region, sufficient element description, dynamic type, element detection and clipped text | Direct | Apple, `XCUIAccessibilityAuditType` | https://developer.apple.com/documentation/xcuiautomation/xcuiaccessibilityaudittype |
| Apple recommends a minimum 4.5:1 contrast ratio between foreground text and background, citing the W3C formula rather than defining its own | Direct | Apple HIG, Accessibility; App Store Connect sufficient-contrast criteria | https://developer.apple.com/design/human-interface-guidelines/accessibility · https://developer.apple.com/help/app-store-connect/manage-app-accessibility/sufficient-contrast-evaluation-criteria/ |
| 4.5:1 for body text, 3:1 for large text, with exemptions for incidental text, inactive components, logotypes and pure decoration | Direct | WCAG 2.2 SC 1.4.3 Contrast (Minimum), Level AA | https://www.w3.org/TR/WCAG22/ |
| 3:1 is the commonly recommended minimum for non-text contrast, including a control's checked-versus-unchecked distinction | Direct | Apple HIG, Accessibility | https://developer.apple.com/design/human-interface-guidelines/accessibility |
| Apple advises checking contrast in both light and dark, and testing dark together with Increase Contrast | Direct | Apple HIG, Accessibility and Color | https://developer.apple.com/design/human-interface-guidelines/accessibility |
| The pointer hit-target floor is 24 × 24 units (Level AA), with a spacing exception for undersized targets | Direct | WCAG 2.2 SC 2.5.8 Target Size (Minimum) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html |
| 44 × 44 is the enhanced bar, recommended for important controls | Direct | WCAG 2.2 SC 2.5.5 Target Size (Enhanced) | https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html |
| Focus order must preserve meaning and operability — the criterion behind comparing tab traversal against visual order | Direct | WCAG 2.2 SC 2.4.3 Focus Order | https://www.w3.org/TR/WCAG22/ |

## The fidelity ledger

| Rule | Type | Source | URL |
|---|---|---|---|
| Breadth before depth (present / divergent / absent for every reference element, filled before any property is measured), the inverted burden of proof, and the requirement that a citation be external and pre-existing | Direct | The `mockup-fidelity:mockup-fidelity` skill, whose method this reuses | `/Users/lukerhodes/Dev/diolog-plugins/plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md` |
| Enumerating build-side extras, not only reference-side absences | Direct | Same skill, its sixth blocking-gate rule | Same path |

---

## Where the corpus disagreed

Carried at the strength the evidence supports, not resolved.

**Whether Electron and Chromium honour accessibility actions on unfocused
windows.** Gemini reported that they frequently discard `AXPress` and `AXClick`
when out of focus and require activation, citing a third-party write-up. Claude
local and OpenAI gpt-5.6 reported that they honour them after tree activation,
citing `axcli` and screenpipe. The likely confound is lazy tree
materialisation — an unactivated tree looks exactly like a refusal. The
practical answer is toolkit- and activation-dependent, and a campaign against an
Electron app should read the step's `plane` and `ok` rather than assume either.
(`claims.json` c14, confidence medium.)

**The strength of Secure Event Input against synthetic events.** Gemini
described all `CGEventPost` injection as "aggressively blocked at the kernel
level". OpenAI gpt-5.6 was explicit that Apple does not publicly promise every
posted event is rejected, and recommended modelling Secure Event Input as "event
injection unreliable and observation blocked" rather than as a documented
universal firewall. The weaker reading is the better-sourced one. Both agree the
accessibility and Apple Events planes are unaffected.

**Whether the two-VM cap holds on macOS 26/27.** Claude local and Gemini
asserted it. OpenAI gpt-5.6 declined to confirm the number for 26/27 from public
API documentation. An independent web check naming the kernel counter and the
error code, with a WWDC26 Virtualization session in the macOS 27 cycle, resolves
it toward two. (`claims.json` c16.)

**What a locked session permits.** Perplexity inferred that a lock-screen
authorization plugin operates *through* the lock by reading the lock-screen UI
with accessibility. The better-evidenced reading, from first-party logs, is
unlock-act-relock: while genuinely locked, every real application returns
`cgWindowNotFound` and only `loginwindow` is reachable. This matters to Proctor
only as a boundary — a locked session is not a testable session.
(`claims.json` c3.)

**Which capture API is in use in shipping software.** Gemini attributed
`CGWindowListCreateImage` to a current agent, sourced to a blog. Claude local
established with a compiler transcript that the call is obsoleted in the macOS
15 SDK and that the surviving pair is ScreenCaptureKit for pixels plus
`CGWindowListCopyWindowInfo` for enumeration. Gemini appears to have conflated
the two calls; the compiler transcript wins.

---

## No public data

Named rather than sourced to something weaker.

- **Accessibility actions on background windows for SwiftUI, Qt, Java/Swing and
  Mac Catalyst.** No source directly tests any of them. SwiftUI is
  AppKit-backed on macOS and is reasonably expected to behave like AppKit;
  the other three are unestablished, and gpt-5.6's toolkit table rates them at
  medium to medium-low confidence on reasoning rather than testing.
- **Whether Secure Event Input degrades accessibility *reads and actions* as
  distinct from event taps.** Sources say "accessibility-related tasks" without
  disambiguating. The locked-session evidence hints they are separable. This
  needs measurement, not literature.
- **ScreenCaptureKit behaviour with the display asleep, disentangled from the
  session being locked.** Every public source conflates the two states.
- **Any dataset measuring declared-contract coverage across a typical installed
  Mac application base.** None exists; the corpus offers a qualitative curve
  only.
- **An Apple-published pointer hit-target minimum for macOS.** Apple's 44 × 44
  figure is touch-platform guidance. The WCAG 2.2 numbers cited above are the
  defensible thresholds for a pointer-driven platform, and are cited as WCAG
  rather than as Apple guidance.
- **Whether Apple intends to close the Library Validation path that blocks
  injection deliberately, or whether the observed rejection is a regression.**
  Structurally unknowable from public sources, and it determines how much of
  this stays true on macOS 27.
