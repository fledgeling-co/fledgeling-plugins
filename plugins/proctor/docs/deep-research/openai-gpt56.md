---
title: "Analysis of OpenAI Codex macOS Computer Use architecture"
run_id: dr_3470278e48e4dc65
question: "How does OpenAI's Codex/ChatGPT macOS \"computer use\" agent actually observe and control the Mac — including operating a locked machine and acting on background windows without foregrounding them — and what are the best available and best buildable methods for AI agents to capture screenshots and read UI layout hierarchy and computed styles on macOS 26/27, for agentic UI/UX and end-to-end user-flow testing?\n\nALREADY ESTABLISHED BY FIRST-PARTY INSPECTION OF THE MACHINE — do not re-derive, but do corroborate, explain, contextualise and assess the implications of each:\n- Codex ships a separate sandboxed service, \"Codex Computer Use.app\" / SkyComputerUseService (bundle com.openai.sky.CUAService, Team ID 2DC432GLL2), installed under ~/.codex/ rather than /Applications.\n- That service statically imports the full AXUIElement read AND write surface (AXUIElementPerformAction, AXUIElementSetAttributeValue, AXUIElementCreateSystemWide, AXUIElementCreateApplication), ScreenCaptureKit (SCStream, SCShareableContent, SCContentFilter), and CGWindowListCopyWindowInfo — and imports ZERO synthetic-event APIs (no CGEventPost, no CGEventCreateMouseEvent, no IOHIDPostEvent). It holds com.apple.security.automation.apple-events. TCC shows kTCCServiceAppleEvents=2 for com.openai.codex.\n- A root-installed SecurityAgent authorization plugin, /Library/Security/SecurityAgentPlugins/CodexComputerUseAuthorizationPlugin.bundle, exists, and the system.login.screensaver authorizationdb rule has been rewritten from Apple's default \"authenticate-session-owner-or-admin\" to [\"com.openai.sky.CUAService.AuthorizationPlugin.remote\", \"use-login-window-ui\"]. Swift classes LockScreenAutoUnlockCoordinator, SystemLockScreenAXInteractor, LockScreenLoginAuthorizationBroker, LockScreenLoginAuthorizationSocketServer, SystemLockScreenOverlayPresenter, SystemLockScreenPhysicalInputMonitor, LockScreenGuardianCoordinator communicate over a world-writable unix socket /tmp/com.openai.sky.CUAService/LockScreenLoginAuthorization.sock.\n- No OpenAI DriverKit system extension and no HID entitlement are present, so virtual-HID injection is NOT the mechanism.\n- The Electron app hosts a server-delivered-JavaScript runtime: Resources/cua_node/bin/node_repl, codex-code-mode-host, \"codex --features code_mode_host=true\", an objc-js Objective-C bridge, and node running kernel.js from a temp directory. A separate codex_chronicle binary links ScreenCaptureKit, Vision, CoreML and Metal.\n\nALSO ALREADY COVERED BY PRIOR RESEARCH — explicitly EXCLUDE and do not spend search budget on: the general agentic UI-testing tooling landscape (Playwright, Playwright MCP, Stagehand, browser-use, Appium, Maestro, XCUITest, Peekaboo, XcodeBuildMCP), VLM-as-a-judge screenshot evaluation, and generic UI-test flakiness advice. Assume the reader already knows all of it.\n\nAnswer these ten numbered subtopics:\n1. SecurityAgent authorization plugins as an agent capability: what an authorization mechanism plugin can legitimately do inside the SecurityAgent/loginwindow context on macOS 26/27; how rewriting system.login.screensaver changes the unlock path; how a remote/socket-brokered mechanism supplies credentials; documented precedent for third-party software doing this; and the security and fleet-management consequences, including which MDM/PPPC or configuration-profile controls actually constrain it and whether removing the app reverts the rule.\n2. The server-delivered-JavaScript capability model (code_mode_host, a bundled Node runtime, an Objective-C bridge): what is publicly documented about this architecture, comparable designs in other shipping agents, and the auditability problem created when a client's native capability set is defined by the server at runtime rather than by its binary.\n3. A session-state capability matrix for macOS 26/27: for each of display-asleep, screensaver-active, session-locked, fast-user-switched-away, no-display/headless, window-occluded, window-minimised and window-on-another-Space — which of AX attribute reads, AXUIElementPerformAction, AXObserver notification delivery, Apple Events, SCStream (window-scoped and display-scoped), CGWindowListCreateImage and CGEventPost still function, degrade, or fail.\n4. The two control planes: process-directed actuation (AXUIElementPerformAction, AXUIElementSetAttributeValue, Apple Events) versus event-stream injection (CGEventPost, CGEventPostToPid). Which mainstream toolkits — AppKit, SwiftUI, Mac Catalyst, Electron/Chromium, Qt, Java — honour AX actions on non-frontmost windows without self-activating; whether keyboard focus is a per-WindowServer singleton that CGEventPostToPid genuinely escapes; and how EnableSecureEventInput affects each plane.\n5. Whether background and occluded window capture returns live or stale pixels: NSWindowOcclusionState, App Nap, CoreAnimation suspension of offscreen surfaces, WindowServer backing-store purge, and the supported ways to keep a non-visible window rendering at a known cadence; plus how to detect a stale frame in-band.\n6. The native equivalent of getComputedStyle on macOS. Assess and compare: the CoreAnimation layer and presentation tree; Xcode's View Debugger transport (DTX/LLDB injection, _ViewDebug, libViewDebuggerSupport) driven headlessly; MTLCaptureManager GPU command-stream capture; CoreText glyph-submission interposition; and re-rendering into a PDF/vector context to recover a display list. For each: what it yields, whether it works on third-party apps versus only your own signed debug builds, and what hardened runtime, SIP and notarisation permit on 26/27.\n7. The accessibility tree as negotiated rather than fixed state: AXManualAccessibility and AXEnhancedUserInterface, per-toolkit lazy-tree activation, the performance cost, whether the target app can detect that it is being agent-driven (an observer effect and validity threat for e2e suites), and what the AX projection of web content in WKWebView and Electron exposes compared with CDP computed styles.\n8. Determinism primitives: CDP Emulation.setVirtualTimePolicy and whether any native macOS analogue exists for controlling an app's clock and animation timing; quiescence and settle signals (ScreenCaptureKit dirty rects, CoreAnimation commit counters, AXObserver notifications, run-loop idleness) and how honest each is; and per-step state hashing to measure first-divergence and quantify nondeterminism as a number.\n9. Isolation and parallelism: the entitlement and availability status of CGVirtualDisplay on macOS 26/27 and whether ScreenCaptureKit binds a virtual display as an SCDisplay; Virtualization.framework macOS-guest save/restore support, latency and GPU/display fidelity; TCC behaviour inside a guest and whether grants can be pre-seeded at image build; and what the real ceiling on concurrent agent-driven UI sessions is on Apple silicon.\n10. Declared automation contracts as a pixel-free action surface: App Intents and Assistant Schemas on macOS 26/27, AppleScript sdef dictionaries, NSServices, URL schemes and Shortcuts; whether a third-party non-Shortcuts process can invoke intents and query entities programmatically; the coverage curve across a typical installed app base; and whether there is evidence Codex routes through declared intents before falling back to AX.\n\nFor each subtopic give evidence-backed findings AND documented failure modes. Prioritise Apple developer documentation, WWDC sessions, open-source implementations, security research and Apple platform-security documentation over blog posts and vendor marketing. Where sources disagree, say so explicitly rather than resolving it. State clearly what could not be established from public sources."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 50
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-12T12:56:58.807Z
---
## Executive Summary

- **(High Confidence)** OpenAI’s Codex/ChatGPT macOS Computer Use implementation is best understood as a **process-directed automation system**, not a virtual mouse and keyboard. Accepting the machine inspection supplied in scope, observation is primarily ScreenCaptureKit plus WindowServer metadata, while control is primarily writable Accessibility (`AXUIElementPerformAction` and `AXUIElementSetAttributeValue`) and Apple Events. The absence of CGEvent/HID imports materially supports that conclusion. OpenAI publicly documents only the required Screen Recording and Accessibility permissions, not this internal routing. [OpenAI Help Center, current](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) ([help.openai.com](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex))

- **(High Confidence)** “Locked Computer Use” does **not** appear to mean continuously manipulating the protected desktop while it remains locked. It appears to mean: participate in the `system.login.screensaver` authorization decision through a root-installed SecurityAgent plug-in, temporarily authorize/unlock the existing session, conceal or guard physical output, perform AX/SCK work in the unlocked user session, and relock afterward. A public report in OpenAI’s Codex repository independently records the plug-in path, authorization-database rule, and expected unlock/overlay/relock behavior. [OpenAI Codex issue #24086, empirical corroboration](https://github.com/openai/codex/issues/24086) ([github.com](https://github.com/openai/codex/issues/24086))

- **(High Confidence)** Background-window operation follows naturally from this design. AX actions and Apple Events are sent to an application or element rather than synthesized into the single WindowServer input stream; many standard controls can therefore be pressed, toggled, or assigned values while their window is occluded or non-frontmost. ScreenCaptureKit’s `desktopIndependentWindow` filter provides the matching window-directed observation surface. [Apple ScreenCaptureKit documentation](https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init(desktopindependentwindow:)) ([developer.apple.com](https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init%28desktopindependentwindow%3A%29))

- **(High Confidence)** The best production-safe observation stack for arbitrary third-party Mac apps is **AX hierarchy + ScreenCaptureKit window streams + CGWindow metadata**. It supplies semantics, geometry and pixels, but **not native computed styles**. `CGWindowListCreateImage` should be treated only as a legacy fallback; it is deprecated and has weaker behavior around minimized, locked and nonresident surfaces. ScreenCaptureKit provides frame status, timestamps and dirty rectangles, but these indicate compositor activity—not whether the target application’s internal state is quiescent. [Apple ScreenCaptureKit frame metadata](https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects) ([developer.apple.com](https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects?changes=_7))

- **(High Confidence)** There is **no public, cross-process macOS equivalent of DOM/CSS `getComputedStyle`**. Core Animation’s model and presentation trees, AppKit view properties, constraints, CoreText runs and Metal captures each expose only one rendering layer and ordinarily require in-process code or an attachable debug build. Xcode View Debugger’s transport is not a supported headless API, and hardened runtime, library validation, `get-task-allow` and SIP prevent treating debugger injection as a general third-party-app technique.

- **(High Confidence)** For your own portfolio, the strongest build is an **in-app UI observability contract**, not reverse-engineered debugger injection: serialize the native view/control hierarchy, constraints, semantic design tokens, effective appearance, text layout, Core Animation model/presentation values and a monotonic render revision; pair it with AX and ScreenCaptureKit externally. For WKWebView/Electron content, use CDP or injected `getComputedStyle` when you own the web surface.

- **(High Confidence)** Do not make a SecurityAgent authorization plug-in the default architecture for a UI-testing product. It is a legitimate Apple extension point, with established precedents such as Duo and Jamf Connect, but it creates a root/loginwindow trust path and an authorization-database persistence problem. Deleting the user app does not inherently remove the plug-in or restore `system.login.screensaver`; an explicit, privileged uninstaller must do so. macOS 27 strengthens fleet-side binary control while simultaneously changing Accessibility-consent management. [Apple authorization plug-in documentation](https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins) [Apple WWDC26 device-management updates](https://support.apple.com/guide/deployment/device-management-updates-depd638aa061/web) ([developer.apple.com](https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins))

- **(Medium Confidence)** The durable actuation priority for a new toolchain should be: **declared domain contract—App Intent or Apple Event—then AX semantics, then synthetic events only as a foreground, isolated-session fallback**. No public evidence establishes that Codex probes or invokes App Intents before AX. Its inspected Apple Events and AX capabilities support those planes; intent-first routing remains uncorroborated.

### Build decision matrix

| Requirement | Best available for arbitrary apps | Best buildable for owned apps | Public/private status | Principal limitation | Recommendation |
|---|---|---|---|---|---|
| Screenshot capture | `[H]` ScreenCaptureKit window-scoped stream | `[H]` SCK plus app-generated IOSurface/render stream | Public | Minimized/offscreen surfaces may be stale or absent | **Build** |
| UI hierarchy | `[H]` AX tree | `[H]` Native test telemetry plus AX | Public | AX is negotiated, lossy and observer-sensitive | **Build** |
| Computed/native styling | `[H]` No general solution | `[H]` In-process resolved-style and design-token endpoint | Public if implemented by you | Cannot be recovered reliably from third-party releases | **Build into owned apps** |
| Background actions | `[H]` AX actions and Apple Events | `[H]` App Intents/Apple Events plus direct test contract | Public | Custom controls and focus-dependent editing vary | **Prefer over events** |
| Drag, canvas and raw text composition | `[M]` Foreground CGEvent fallback | `[H]` Add semantic test actions to app | Public, TCC-controlled | Global focus, coordinates, secure input | **Use sparingly** |
| Locked-machine operation | `[M]` SecurityAgent authorization plug-in | `[H]` Dedicated unlocked VM/test account | Plug-in API public; policy details partly private | Root trust path; cannot unlock FileVault preboot | **Prefer VM/test appliance** |
| Parallel sessions | `[H]` Separate macOS VMs | `[H]` VM snapshots plus guest MDM/TCC | Public | RAM/GPU cost; current concurrency ceiling undocumented | **VM per independent session** |
| Headless View Debugger | `[L]` Unsupported/private transport | `[M]` LLDB tooling for owned debug builds only | Private/unsupported headless interface | Hardened runtime and version fragility | **Do not productize** |

---

## Detailed Findings

### 1. SecurityAgent authorization plugins as an agent capability

#### Finding

`[H]` Apple explicitly supports authorization plug-ins for changing system authorization policies. The authorization engine loads plug-in mechanisms in dedicated host processes: one runs as an anonymous user and can display UI, while another may run with root privileges but must not connect to WindowServer. Mechanisms can exchange hints and context—including authentication information—and return allow, deny, cancel or undefined results. Plug-ins are installed in `/Library/Security/SecurityAgentPlugins`, and authorization rules are modified to reference their mechanisms. [Apple, “Extending authorization services with plug-ins”](https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins) ([developer.apple.com](https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins))

`[H]` Apple’s `SetContextValue` API permits a mechanism to store a user name and other authentication context for later mechanisms; sensitive values such as passwords are not exposed back to the ordinary authorization client. This makes a brokered flow technically legitimate: one component obtains or validates credentials, communicates the result to the mechanism, and the mechanism populates authorization context or returns an authorization result. [Apple AuthorizationCallbacks documentation](https://developer.apple.com/documentation/security/authorizationcallbacks/1543148-setcontextvalue) ([developer.apple.com](https://developer.apple.com/documentation/security/authorizationcallbacks/1543148-setcontextvalue))

`[H]` Replacing `system.login.screensaver` changes which authorization rule chain decides whether a locked session may resume. It does not merely add an app-level permission. It inserts third-party code or a third-party-defined rule into a security-sensitive decision normally handled by Apple’s session-owner/admin authentication path.

`[M]` <INFERENCE from="supplied authorizationdb rule; Apple plug-in context/result APIs; supplied broker and socket class names">The OpenAI “remote” rule most plausibly allows SkyComputerUseService to request an authorization attempt, provide a session-bound credential or authorization assertion over the local socket, and have the plug-in either populate the authorization context or return a successful result before the standard login-window UI is needed.</INFERENCE> The exact socket messages, credential origin and authorization-result logic were not established from public material.

`[H]` The plug-in cannot unlock FileVault before the macOS system volume and user data volume are available. `system.login.screensaver` covers a running session’s lock path; it is not equivalent to FileVault preboot authentication after shutdown or restart. Apple’s own macOS 27 Platform SSO documentation treats FileVault, Lock Screen and login-window authentication as distinct integration points. [Apple Platform SSO for macOS, published June 12, 2026](https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web) ([support.apple.com](https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web))

#### Precedent

`[H]` Cisco Duo ships a macOS authorization plug-in that protects console login and, on current releases, screen unlock and wake-from-sleep. Its documentation warns that incompatible mechanisms can prevent login and supplies distinct restore and uninstall packages. [Cisco Duo, updated July 21, 2026](https://duo.com/docs/macos) ([duo.com](https://duo.com/docs/macos))

`[H]` Jamf Connect’s `authchanger` explicitly manipulates the authorization database used by `loginwindow`, controls mechanism ordering, and offers a root-only reset-to-default operation. Its open-source implementation includes examples that overwrite `system.login.screensaver`. [Jamf Connect authchanger documentation](https://learn.jamf.com/r/en-US/jamf-connect-documentation-current/authchanger) [Jamf authchanger source](https://github.com/jamf/authchanger) ([learn.jamf.com](https://learn.jamf.com/r/en-US/jamf-connect-documentation-current/authchanger))

#### Fleet and policy consequences

| Control | macOS 26 | macOS 27 status as of August 12, 2026 | Effect on Codex-like design |
|---|---|---|---|
| Accessibility TCC | `[H]` PPPC can manage allow/deny | `[H]` Legacy PPPC ability to grant Accessibility was deprecated in 26.2 and removed in 27; new declarative App Settings supplies a managed default through a consolidated user-consent prompt | Can prevent AX control; 27 makes silent fleet grant less straightforward |
| Apple Events TCC | `[H]` PPPC can constrain sender/receiver pairs | `[M]` Legacy PPPC schema is marked deprecated, but the new App Settings privacy object publicly lists Accessibility and common sensors—not Apple Events | Can block the Apple Events plane; transition details are incompletely documented |
| Post Event TCC | `[H]` PPPC has a `PostEvent` service | `[M]` Legacy schema deprecation creates the same migration uncertainty | Irrelevant to inspected Codex imports, but constrains CGEvent-based competitors |
| Screen Capture TCC | `[H]` A profile can deny capture but cannot silently grant it | `[M]` No new declarative silent-grant surface was found | Can break SCK observation; user consent remains central |
| `allowScreenShot` restriction | `[H]` Can disable screenshots/screen recording system-wide | `[H]` Still documented | Broad fleet kill switch for capture |
| Binary execution policy | Limited built-in granularity | `[H]` New declarative `AllowedBinaries`/`DeniedBinaries` can match CD hash, Team ID, signing ID and optionally path/state | Can block the CUA service, plug-in helper or interpreter before execution |
| Login Window profile | `[H]` Controls UI and login options | `[H]` Does not expose an authorization-plug-in allow/deny list | Does not directly restore `system.login.screensaver` |
| Package removal tracking | Ordinary uninstaller logic | `[H]` New package removal can delete tracked installed files, but Apple says post-install script changes are not tracked | Removing files still does not inherently undo `authorizationdb` writes |

Apple’s macOS 27 documentation remains explicitly pre-release and subject to change. [Apple WWDC26 app-management updates, June 8, 2026](https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web) [Apple App Settings privacy object](https://developer.apple.com/documentation/devicemanagement/appsettingsappdictionaryobject) ([support.apple.com](https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web))

`[H]` <INFERENCE from="authorization database is separate from app files; Jamf requires explicit reset; Apple says package removal does not track post-install changes">Deleting Codex.app or `~/.codex` does not, by itself, restore the authorization rule or remove a root plug-in under `/Library`. Only an OpenAI-provided uninstaller or another privileged remediation that explicitly restores the rule can do so.</INFERENCE>

`<MISSING_DATA>[Public documentation for the current Codex uninstaller, including whether it removes CodexComputerUseAuthorizationPlugin.bundle and restores system.login.screensaver, was not found.]</MISSING_DATA>`

#### Security failure modes

- `[H]` A broken or incompatible mechanism can prevent unlock or login; Duo explicitly warns that incompatible plug-ins may make login impossible. ([duo.com](https://duo.com/docs/macos))
- `[H]` An authorization rule can survive ordinary app deletion.
- `[H]` A plug-in executing in the authorization path materially expands the trusted computing base.
- `[M]` A world-writable socket is not automatically exploitable if the server authenticates peers using audit tokens, effective UID, code requirements, nonces and session binding.
- `<INSUFFICIENT_EVIDENCE>[No public source established whether the OpenAI socket authenticates its peer, cryptographically binds messages to the active Computer Use turn, prevents replay, rate-limits attempts, or zeroizes credential material.]</INSUFFICIENT_EVIDENCE>`
- `[H]` The design cannot recover from FileVault preboot, a powered-off Mac, or a session whose local password is unavailable.

---

### 2. The server-delivered-JavaScript capability model

#### Publicly documented portion

`[H]` OpenAI publicly states that Codex workflows can run locally, that Computer Use processes screenshots, and that the desktop experience uses the permissions available to it. OpenAI also characterizes Codex as being based on the premise that “everything is controlled by code,” but it does not document the CUA service’s Node/Objective-C bridge or downloaded `kernel.js`. [OpenAI, February 2, 2026](https://openai.com/index/introducing-the-codex-app/) [OpenAI Help Center](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) ([openai.com](https://openai.com/index/introducing-the-codex-app/))

`[H]` OpenAI’s public Codex repository confirms that release packages include a separately signed `codex-code-mode-host` and that the Darwin build path uses a Codex-built V8 distribution. That corroborates a code-host architecture, but not the inspected Computer Use Node REPL or Objective-C bridge. [OpenAI Codex package README](https://github.com/openai/codex/blob/main/scripts/codex_package/README.md) ([github.com](https://github.com/openai/codex/blob/main/scripts/codex_package/README.md))

`<INSUFFICIENT_EVIDENCE>[OpenAI has not publicly documented the provenance, signing, version pinning, selector allowlist, retention or audit logging of the inspected server-delivered kernel.js.]</INSUFFICIENT_EVIDENCE>`

#### Capability interpretation

`[H]` Downloaded JavaScript cannot grant itself additional entitlements. The static upper bound remains the native host’s sandbox, TCC grants, entitlements, IPC endpoints and selector/function allowlist.

`[H]` <INFERENCE from="bundled interpreter; Objective-C bridge; server-delivered program">The binary defines the maximum capability envelope, while the server-delivered program selects the actual sequence of native operations at runtime. Therefore, import-table and entitlement analysis can establish what the client could do, but cannot establish what a particular Computer Use turn did.</INFERENCE>

This is comparable in broad shape—not necessarily trust model—to systems with an extension host or embedded automation interpreter:

- `[M]` VS Code executes separately packaged JavaScript extensions in extension-host processes.
- `[M]` JavaScript for Automation provides a JavaScript-to-Objective-C and Apple Events bridge.
- `[M]` Electron applications routinely place a policy/IPC boundary between a JavaScript renderer and privileged native code.

The crucial auditability difference is whether the executable program is a durable, content-addressed package with a version and signature, or transient code selected by a service.

#### Audit requirements for a buildable equivalent

A defensible implementation should record, for every turn:

1. `[H]` SHA-256 or stronger content hash of the executed code bundle.
2. `[H]` Server signature and signing-key identifier.
3. `[H]` Capability-manifest version and exact native selector/function allowlist.
4. `[H]` Host binary version, entitlements and code-signing requirement.
5. `[H]` TCC decision snapshot.
6. `[H]` Every native bridge call with arguments redacted according to policy.
7. `[H]` Code expiry, revocation and replay-prevention metadata.
8. `[H]` A policy decision explaining why each bridge call was allowed.

`[H]` <INFERENCE from="dynamic program selection and static native envelope">Without these artifacts, a static SBOM or notarization ticket proves the identity of the interpreter but cannot reproduce or attest the behavior chosen by the server for a historical turn.</INFERENCE>

#### Documented or foreseeable failure modes

- Server and client capability-manifest skew.
- A broad Objective-C bridge accidentally exposing selectors beyond the reviewed API.
- Non-reproducible behavior after server code changes.
- Temporary scripts escaping endpoint monitoring that keys only on Mach-O hashes.
- Interpreter or bridge compromise becoming equivalent to compromise of all granted Accessibility, Screen Capture and Apple Events privileges.
- Notarization of the native host being mistaken for review or notarization of downloaded program logic.

---

### 3. Session-state capability matrix for macOS 26/27

**Legend:** ✅ generally functional; ⚠️ conditional/degraded; ❌ unavailable or targets the wrong session. Confidence is shown per cell.

Apple documents window-directed ScreenCaptureKit filters, frame status and dirty rectangles, but it does not provide a normative matrix for every lock, Space, minimization and fast-user-switching combination. [Apple ScreenCaptureKit window filter](https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init(desktopindependentwindow:)) [Apple capture sample](https://developer.apple.com/documentation/screencapturekit/capturing-screen-content-in-macos) ([developer.apple.com](https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init%28desktopindependentwindow%3A%29))

| Session/window state | AX reads | AX actions / value writes | AXObserver | Apple Events | SCK window-scoped | SCK display-scoped | `CGWindowListCreateImage` | `CGEventPost` |
|---|---|---|---|---|---|---|---|---|
| Display asleep, session unlocked | ✅ `[H]` | ✅/⚠️ `[M]` | ✅/⚠️ `[M]` | ✅ `[H]` | ⚠️ `[M]` stream may become idle/suspended; app may nap | ⚠️ `[M]` blank/idle or wake-dependent | ⚠️ `[L]` stale/blank possible | ⚠️ `[M]` usually wakes display and uses current focus |
| Screensaver active but not locked | ✅ `[M]` | ✅ `[M]` | ✅ `[M]` | ✅ `[H]` | ✅/⚠️ `[M]` target surface permitting | ✅ `[H]` but captures screensaver, not unobscured desktop | ⚠️ `[L]` | ⚠️ `[H]` input normally dismisses screensaver |
| Session locked | ⚠️ `[L]` underlying processes may remain reachable, but not a supported automation state | ⚠️ `[L]` may alter a running app, but cannot operate the secure UI as an ordinary user process | ⚠️ `[L]` | ⚠️ `[M]` transport can work if target remains responsive | ⚠️/❌ `[L]` surfaces may disappear; public Codex report observed `cgWindowNotFound` | ⚠️ `[M]` lock/blank output; never a safe view of underlying session | ❌/⚠️ `[L]` | ⚠️ `[H]` reaches lock/current secure session, not arbitrary underlying window |
| Fast-user-switched away | ❌ from another user’s agent `[H]`; local resident agent uncertain | ❌/⚠️ `[L]` | ⚠️ `[L]` | ⚠️ `[M]` if same-session target process remains responsive | ❌/⚠️ `[L]` usually suspended or unavailable | ❌ `[H]` active console session differs | ❌/⚠️ `[L]` | ❌ `[H]` global events route to active console session |
| Logged-in GUI session with no display | ✅ `[M]` | ✅ `[M]` | ✅ `[M]` | ✅ `[H]` | ⚠️ `[M]` if a window/surface exists | ❌ `[H]` without an enumerated `SCDisplay` | ⚠️ `[L]` | ⚠️ `[L]` mouse geometry and active focus may be undefined |
| Window fully occluded | ✅ `[H]` | ✅ `[H]` for semantic actions | ✅ `[H]` | ✅ `[H]` | ✅ `[H]` using desktop-independent window capture | ✅ `[H]` but pixels show occluders | ⚠️ `[M]` legacy backing-store behavior | ❌ `[H]` for coordinate click unless target is exposed/activated |
| Window minimized | ✅/⚠️ `[M]` tree usually remains | ✅/⚠️ `[M]` | ✅/⚠️ `[M]` | ✅ `[H]` | ⚠️/❌ `[L]` surface may be stale, absent or no longer shareable | ❌ `[H]` target is not displayed | ❌/⚠️ `[M]` | ❌ `[H]` cannot click minimized content |
| Window on another Space | ✅ `[H]` | ✅/⚠️ `[M]` | ✅/⚠️ `[M]` | ✅ `[H]` | ✅/⚠️ `[M]` desktop-independent filter is the intended route | ❌ `[H]` active display stream shows the current Space | ⚠️ `[L]` | ❌ `[H]` global event hits active Space/focus |

`[H]` The operationally safe interpretation is:

- Lock state is **not** an ordinary background-window state.
- A minimized window is materially less reliable than an occluded, non-minimized window.
- Another Space is compatible with process-directed AX and window-directed SCK, but not with display screenshots or global clicks.
- Fast User Switching is not an isolation primitive for concurrent event-driven agents.
- A headless Mac needs an actual or supported virtual display if display-scoped rendering is required.

`<CONFLICTING_EVIDENCE>[ScreenCaptureKit’s desktop-independent window abstraction suggests capture independent of desktop placement, while field reports—including the Codex cgWindowNotFound report—show that lock/minimization/display transitions can remove or suspend the underlying shareable surface. Apple does not specify the complete lifecycle contract.]</CONFLICTING_EVIDENCE>`

`<MISSING_DATA>[A reproducible macOS 26.6 versus macOS 27-beta conformance run across all eight states, APIs and target toolkits is required before treating low-confidence cells as contractual behavior.]</MISSING_DATA>`

---

### 4. Process-directed actuation versus event-stream injection

#### The two planes

| Plane | APIs | Routing model | Background suitability | Primary failure class |
|---|---|---|---|---|
| Process-directed | AX actions, AX writable attributes, Apple Events, declared intents | Message or semantic command to target process/element | `[H]` Strong | Missing semantic action, app bug, nonwritable attribute |
| Event-stream | `CGEventPost`, `CGEventPostToPid` | Keyboard/mouse event interpreted through AppKit/WindowServer focus and responder state | `[H]` Weak for global post; `[M]` improved but not isolated for PID post | Wrong focus/window/Space, coordinates, secure input |

`[H]` AX `Press`, `Increment`, `Decrement`, `Confirm`, menu actions and writable value attributes do not inherently require a physical pointer hit-test. An app may nonetheless activate itself, expose an action by simulating an internal click, or reject an action while disabled.

`[M]` `CGEventPostToPid` changes the process-delivery target but does not create an independent keyboard-focus universe. Inside an AppKit process, key events still traverse that process’s key-window and first-responder state. It therefore does not supply simultaneous per-window keyboard focus and does not solve cross-process modal or secure-input ownership.

#### Toolkit behavior

| Toolkit | Standard AX press/value action on non-frontmost window | Likely self-activation cases | Documented failure modes | Confidence |
|---|---|---|---|---|
| AppKit | Usually yes | Focus, text editing, menu presentation, app-authored activation | Custom `NSView` lacking accessibility actions; disabled controls; modal sheets | High |
| SwiftUI | Usually yes for `Button`, `Toggle`, exposed accessibility actions | Focus state, text fields, custom gestures | Accessibility projection is synthesized; custom drawing/gestures may expose no actionable node | Medium |
| Mac Catalyst | Often for standard UIKit controls | Scene activation, text input and UIKit lifecycle assumptions | Incomplete Mac accessibility adaptation; custom UIKit controls | Medium |
| Electron/Chromium | Usually for semantic HTML controls after accessibility is enabled | Focus, selection, popup/menu and browser activation paths | Lazy AX tree; custom canvas; ARIA errors; renderer accessibility overhead | Medium-High |
| Qt | Usually for standard widgets implementing `QAccessibleActionInterface` | Focus and popup paths | Custom QML/widgets without accessibility interfaces | Medium |
| Java AWT/Swing | Often for controls exposing `AccessibleAction` | Native text/focus and bridge-specific paths | Java Accessibility bridge gaps, custom components, latency | Medium-Low |

Primary toolkit contracts include Electron’s accessibility-support switch, Qt’s `QAccessibleActionInterface`, and Java’s `AccessibleAction`. [Electron API](https://www.electronjs.org/docs/latest/api/app#appsetaccessibilitysupportenabledenabled-macos-windows) [Qt documentation](https://doc.qt.io/qt-6/qaccessibleactioninterface.html) [Oracle Java Accessibility API](https://docs.oracle.com/en/java/javase/21/docs/api/java.desktop/javax/accessibility/AccessibleAction.html)

`[H]` None of these frameworks provides a general promise that every accessibility action will avoid activation. The contract is semantic—“perform this accessibility action”—not “perform it invisibly without changing application activation.”

#### Secure Event Input

`[H]` Secure Event Input is aimed principally at preventing other processes from intercepting keyboard input while sensitive entry is occurring. It disrupts event taps, global hotkeys and key observation. [Apple Technical Note TN2150](https://developer.apple.com/library/archive/technotes/tn2150/_index.html)

`[H]` AX and Apple Events are separate IPC/control planes and are not globally disabled merely because Secure Event Input is active.

`[H]` Secure text fields generally redact their value and may not expose a writable AX value. Thus the transport survives, while the sensitive element’s semantics are deliberately restricted.

`[M]` Apple does not publicly promise that every posted CGEvent is rejected during Secure Event Input. Posted events still face the current secure-input owner, focus and target application’s validation. Therefore, Secure Event Input should be modeled as “event injection unreliable and observation blocked,” not as a documented universal CGEvent firewall.

#### Recommendation

`[H]` Use process-directed actions for buttons, menus, selection, toggles, value assignment and application commands. Reserve event injection for:

- drag paths,
- canvas interactions lacking AX semantics,
- hover-only states,
- native text-composition/IME testing,
- keyboard shortcut behavior itself,
- testing focus and hit-testing as user-visible behaviors.

Run those cases in a dedicated foreground session.

---

### 5. Live versus stale background-window capture

`[H]` Window visibility and pixel freshness are different properties. `NSWindow.occlusionState` reports whether a window is considered visible, and an application may use that signal to reduce work. App Nap can further throttle applications with no visible, user-relevant activity. [Apple NSWindow occlusion state](https://developer.apple.com/documentation/appkit/nswindow/occlusionstate) [Apple App Nap guidance](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/power_efficiency_guidelines_osx/AppNap.html)

`[H]` ScreenCaptureKit’s `SCFrameStatus.complete` means the sample contains a valid complete frame. It does **not** prove that the target application freshly rendered that frame in response to recent state. Dirty rectangles identify regions redrawn or moved in the captured output, not pending application work. ([developer.apple.com](https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects?changes=_7))

| Window condition | Typical capture result | Freshness confidence |
|---|---|---|
| Visible and updating | Live frames | High |
| Fully occluded but non-minimized | Usually live if app continues committing | Medium-High |
| On another Space | Window stream may remain live; app may throttle | Medium |
| Minimized | Last frame, blank frame, absent surface or failed enumeration | Low |
| Hidden/offscreen by app | Framework- and app-dependent | Low |
| App Napped | Valid but slowly changing or stale surface | Medium-Low |
| Display asleep | Idle/suspended stream or retained last frame | Medium-Low |
| Locked session | Lock/blank content or missing target surface | Low |

`[M]` WindowServer and Core Animation may retain the most recently committed IOSurface after the application stops updating. That explains how capture can return visually valid but old pixels. Public APIs do not guarantee how long such backing stores remain resident.

#### Supported ways to keep content rendering

**For your own apps:**

- `[H]` Render the testable scene into an IOSurface, Metal texture or offscreen Core Animation tree independent of a minimized `NSWindow`.
- `[H]` Drive it from an explicit deterministic cadence rather than assuming WindowServer will request redraws.
- `[H]` Use `ProcessInfo.beginActivity` only for justified test activity; it is not a substitute for an explicit renderer.
- `[H]` Publish a render revision, presentation timestamp and “last model mutation included” revision.
- `[H]` Keep capture and rendering lifecycle separate from user window visibility.

**For third-party apps:**

- `[H]` There is no supported API that forces an arbitrary application to keep a minimized or hidden window rendering.
- `[M]` The least-bad operational workaround is a non-minimized window kept visible on a dedicated Space, display or VM.
- `[M]` Preventing system/display sleep does not prevent App Nap or application-specific offscreen throttling.

#### In-band stale-frame detection

Use all of the following:

1. SCK frame status must be complete.
2. `displayTime` must advance.
3. Dirty rectangles or tile hashes should reflect an expected visual change after a mutating action.
4. AX state should agree with the intended mutation.
5. The app-owned render revision should advance when available.
6. For owned apps, include a test-only visual heartbeat or render counter outside production captures.

`[H]` An unchanged image hash alone cannot distinguish a legitimately static UI from a stale surface.

`[H]` <INFERENCE from="SCK metadata limitations; AX semantic state; controllable own-app telemetry">The strongest freshness assertion is a three-way agreement between semantic state, compositor frame metadata and an app-owned render revision.</INFERENCE>

---

### 6. The native equivalent of `getComputedStyle`

#### Bottom line

`[H]` macOS has no public cross-process object that combines view hierarchy, resolved theme, constraints, typography, animation state, drawing commands and composited pixels in the way browser DevTools combines DOM, layout, CSS and paint information.

| Method | What it yields | Arbitrary third-party release apps | Owned signed debug builds | Hardened runtime/SIP implications | Product verdict |
|---|---|---|---|---|---|
| AX tree | Role, name, value, state, bounds, relationships, actions | Yes, with TCC | Yes | Public and durable | **Core production layer, but not style** |
| Core Animation model tree | Configured layer geometry, color, opacity, transform, contents | No cross-process public access | Yes, in process | Injection/attach blocked by target hardening | **Instrument owned apps** |
| Core Animation presentation tree | Current interpolated animatable values | No | Yes, while presentation exists | Same attach limits | **Best source of current animation geometry** |
| Xcode View Debugger | View hierarchy, frames, constraints and selected properties | Only if debugger attachment is permitted; not a product API | Yes | Hardened targets generally need debug entitlement; SIP protects system processes | **Developer-only** |
| Headless DTX/`_ViewDebug`/`libViewDebuggerSupport` | Potentially View Debugger snapshots | Unsupported/private | Technically possible but version-fragile | Private transport/injection; poor notarization durability | **Do not ship** |
| `MTLCaptureManager` | Metal command buffers, resources, shaders and render passes | No practical semantic access | Yes, with capture support | Target must be capturable/attachable | **GPU diagnosis, not style** |
| CoreText interposition | Submitted glyphs, fonts, runs and positions | Requires unsupported injection | Possible in owned test builds | Library validation/SIP block broad deployment | **Niche diagnostic only** |
| PDF/vector re-render | Vector paths, text, fonts and some colors produced by AppKit drawing | No public arbitrary-view API | Yes, in process | Public when invoked by owning app | **Useful supplemental display list** |
| App-owned telemetry | Whatever resolved properties and semantic tokens you choose | No, unless app adopts SDK | Yes | Fully compatible with hardened runtime | **Best buildable answer** |

Core Animation exposes a view’s backing layer, while its presentation layer supplies current interpolated values. It does not encode Auto Layout intent, SwiftUI modifier provenance, theme-token names or application business semantics. [Apple NSView layer documentation](https://developer.apple.com/documentation/appkit/nsview/layer) [Apple CALayer presentation tree](https://developer.apple.com/documentation/quartzcore/calayer/presentation()) ([developer.apple.com](https://developer.apple.com/documentation/appkit/nsview/layer))

#### Xcode View Debugger

`[H]` Xcode View Debugger is appropriate for apps you own and can attach to with debugging enabled.

`[H]` There is no supported command-line API promising headless View Debugger capture of arbitrary Mac apps.

`[M]` DTX, `_ViewDebug` and `libViewDebuggerSupport` are implementation details identified through reverse engineering and debugger behavior, not stable application APIs.

`[H]` Hardened runtime and library validation prevent arbitrary library injection. A production target normally has no `com.apple.security.get-task-allow`; SIP imposes additional restrictions on Apple/system processes. [Apple Hardened Runtime documentation](https://developer.apple.com/documentation/security/hardened-runtime) [Apple get-task-allow entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.get-task-allow)

`<INSUFFICIENT_EVIDENCE>[Apple does not publicly specify the current macOS 26/27 View Debugger wire protocol or commit to compatibility for headless DTX clients.]</INSUFFICIENT_EVIDENCE>`

#### Metal capture

`[H]` `MTLCaptureManager` records GPU command activity and resources. It can reveal render-pass order, textures, pipeline state and shaders, but it cannot tell an agent that a rectangle is a “destructive primary button” or that its fill came from a semantic design token. [Apple Metal documentation](https://developer.apple.com/documentation/metal/mtlcapturemanager)

#### CoreText interposition

`[M]` Interposing CoreText or Quartz text calls can recover fonts, glyph identifiers, positions and some colors for text drawn through those paths.

Failure modes:

- Metal/custom text rendering bypasses the intercepted path.
- Glyph submission does not reconstruct source strings reliably in all shaping cases.
- It does not recover controls, constraints or theme semantics.
- Injection into hardened third-party apps is not a supported distribution technique.

#### PDF/vector re-rendering

`[H]` `NSView.dataWithPDF(inside:)` or related AppKit drawing APIs can recover a vector-like rendering of owned AppKit content, including text and paths where the drawing implementation supports it. [Apple NSView PDF API](https://developer.apple.com/documentation/appkit/nsview/datawithpdf(inside:))

Failure modes include Metal layers, video, remote surfaces, effects that rasterize, and components that draw differently in a print/PDF context.

#### Recommended owned-app schema

Expose a test-only, authenticated endpoint returning:

```text
Window
  stableWindowID
  frame/screen/Space
  key/main/occlusion/minimized state
  renderRevision
  lastPresentedModelRevision

ViewNode
  stableTestID
  nativeClass / semanticComponentType
  parent / children / zOrder
  frame in local/window/screen coordinates
  hidden / alpha / enabled / focused
  constraints and intrinsicContentSize
  effectiveAppearance / controlSize
  semantic design tokens
  resolved font / colors / border / corner radius
  CALayer model values
  CALayer presentation values
  text runs and glyph bounds where owned
  accessibility projection
```

`[H]` This is more durable and semantically useful than attempting to reconstruct style by attaching Xcode’s private debugger machinery.

---

### 7. Accessibility as negotiated rather than fixed state

`[H]` Accessibility trees are often created lazily. Electron publicly exposes `app.setAccessibilitySupportEnabled`, and warns that enabling accessibility support can affect performance. Chromium and WebKit similarly maintain accessibility-specific caches and projections rather than treating the AX tree as an always-materialized mirror of the DOM or native view tree. [Electron app accessibility API](https://www.electronjs.org/docs/latest/api/app#appsetaccessibilitysupportenabledenabled-macos-windows)

`[M]` `AXManualAccessibility` is used in practice to force accessibility support in applications such as Chromium/Electron, but it is not a suitably documented, durable Apple contract on which to base a macOS 27 product.

`[M]` `AXEnhancedUserInterface` is an accessibility attribute through which assistive technologies can request a richer or modified interface projection. Frameworks may create more nodes, disable virtualization or alter control behavior in response.

#### Observer effect

`[H]` An application can detect accessibility activation indirectly or directly:

- Electron reports changes in accessibility-support state.
- A toolkit receives requests to enable/manualize its AX projection.
- AX object caches and renderer accessibility modes become active.
- Application code can check VoiceOver/accessibility state or respond to richer-interface requests.

`[H]` <INFERENCE from="lazy AX activation; toolkit-visible accessibility state; documented performance impact">An AX-driven E2E suite can change the target’s timing, memory use, tree materialization and occasionally layout or virtualization behavior. This is a genuine observer effect and should be treated as a validity threat.</INFERENCE>

Mitigation:

1. Run a baseline visual/performance pass without AX where possible.
2. Record whether and when AX activation was forced.
3. Compare AX-enabled and AX-disabled screenshots and timing.
4. Avoid using accessibility activation as an invisible global fixture for tests intended to measure cold-start or first-use behavior.
5. Keep AX tree acquisition bounded and incremental.

#### Web content projection

| Surface | AX exposes | AX does not expose |
|---|---|---|
| WKWebView | Semantic web roles, names, values, headings, links, controls, state, bounds, selected text and relationships where WebKit maps them | CSS cascade, full computed style set, pseudo-element styles, layout fragments, paint order, stacking-context detail |
| Electron/Chromium | Chromium accessibility-tree projection of semantic DOM and ARIA | Full DOM, CSSOM, computed styles and exact paint/layout internals |
| CDP | DOM nodes, box models, computed CSS, layout snapshots, network/runtime state | Native host UI outside Chromium |

CDP’s `CSS.getComputedStyleForNode` and `DOMSnapshot` are strictly richer for web layout/style inspection than AX. [Chrome DevTools Protocol CSS domain](https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-getComputedStyleForNode) [Chrome DevTools Protocol DOMSnapshot domain](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/)

`[H]` For a WKWebView you own, injected JavaScript calling `getComputedStyle` is the public, accurate style route. An external process cannot generically obtain that information from an arbitrary third-party WKWebView.

---

### 8. Determinism primitives

#### Clock and animation control

`[H]` CDP provides `Emulation.setVirtualTimePolicy`, allowing browser virtual time to pause or advance independently of wall-clock progression. [Chrome DevTools Protocol Emulation domain](https://chromedevtools.github.io/devtools-protocol/tot/Emulation/#method-setVirtualTimePolicy)

`[H]` Native macOS has no system-wide analogue that virtualizes time for an arbitrary third-party AppKit, SwiftUI, Electron, Qt or Java process.

Owned-app alternatives are narrower:

- dependency-injected clocks,
- test network schedulers,
- controlled `CALayer.speed`, `timeOffset` and `beginTime`,
- disabling `NSAnimationContext`/SwiftUI animations,
- deterministic test launch arguments,
- explicit “advance test clock” and “drain work queue” endpoints.

#### Honesty of settle signals

| Signal | What it honestly proves | What it does not prove | Confidence |
|---|---|---|---|
| SCK dirty rectangles | Captured compositor regions changed or moved | No network work, model work or uncommitted rendering remains | High |
| SCK complete frame | Frame sample is complete and usable | Target app freshly rendered it | High |
| Core Animation transaction completion | An in-process CA transaction committed/completed its callback path | All GPU, network or other-thread work is finished | High |
| AXObserver quiet period | No subscribed AX notifications arrived | UI is idle; provider emitted every relevant notification | High |
| Main run-loop idle | That run loop had no immediately runnable source at that instant | Other threads, actors, GPU or network are idle | High |
| App-owned idle endpoint | Conditions included by your implementation are idle | Conditions omitted by the implementation | High |

`[H]` There is no universal native “UI quiescent” signal.

`[H]` <INFERENCE from="limitations of each individual settle signal">The most defensible generic settle rule is a conjunction: several consecutive complete SCK frames with no meaningful dirty rectangles, no relevant AX notifications, no pending app-owned work when available, and an upper timeout. It remains a heuristic for third-party apps.</INFERENCE>

#### Per-step state hashing

For repeated run `r` and step `i`, define:

```text
H[r,i] = hash(
  canonicalAXTree,
  normalizedWindowState,
  stableVisualTileHashes,
  appContractState,
  relevantEnvironmentState
)
```

Canonicalization should remove volatile PIDs, object addresses, timestamps, antialiasing noise and nondeterministic child ordering.

Proposed numerical measures:

```text
first_divergence(r, reference) =
  min i where H[r,i] != H[reference,i]

step_instability(i) =
  1 - max_h count(H[r,i] == h) / number_of_runs

run_pair_divergence_rate =
  divergent_run_pairs / all_run_pairs
```

For visual state, report both exact tile-hash mismatches and a fixed perceptual-distance threshold.

`[H]` <INFERENCE from="canonical per-step hashes across repeated runs">`step_instability(i)` turns nondeterminism into a value from 0 to 1: 0 means every run reached the same canonical state at that step; values approaching 1 mean no single state dominates.</INFERENCE>

These are proposed engineering metrics, not empirical macOS benchmarks.

---

### 9. Isolation and parallelism

#### `CGVirtualDisplay`

`[H]` No public Apple developer documentation was found exposing `CGVirtualDisplay` as an application API for third-party developers on macOS 26 or the macOS 27 beta.

`[H]` ScreenCaptureKit documents `SCDisplay` as representing a physical display obtained from `SCShareableContent`. [Apple SCDisplay documentation](https://developer.apple.com/documentation/screencapturekit/scdisplay) ([developer.apple.com](https://developer.apple.com/documentation/screencapturekit/scdisplay?changes=_5))

`<INSUFFICIENT_EVIDENCE>[It could not be established from public Apple sources whether a display created through private CGVirtualDisplay SPI is guaranteed to appear as an SCDisplay. Any observed enumeration would be implementation behavior, not a public contract.]</INSUFFICIENT_EVIDENCE>`

`[H]` Even if a private virtual display works, it remains in the same user session and shares activation, keyboard focus, menus, pasteboard and many process-global resources. It isolates pixels better than it isolates agents.

#### Virtualization.framework

`[H]` Apple supports installing and running macOS guests on Apple silicon through Virtualization.framework. The framework supplies a virtual Mac graphics device and `VZVirtualMachineView` for display and input. [Apple macOS VM sample](https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-apple-silicon) ([developer.apple.com](https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-apple-silicon?changes=_4%2C_4))

`[H]` Save/restore is public. A stopped VM can restore a state saved through `saveMachineStateTo`, after which it enters the paused state and may be resumed. Apple notes that not every configuration is saveable and provides `validateSaveRestoreSupport`. [Apple VZVirtualMachine restore API](https://developer.apple.com/documentation/virtualization/vzvirtualmachine/restoremachinestatefrom(url:completionhandler:)) [Apple save/restore validation API](https://developer.apple.com/documentation/virtualization/vzvirtualmachineconfiguration/validatesaverestoresupport()) ([developer.apple.com](https://developer.apple.com/documentation/virtualization/vzvirtualmachine/restoremachinestatefrom%28url%3Acompletionhandler%3A%29))

Advantages for UI agents:

- Independent WindowServer/session focus.
- Independent loginwindow, pasteboard and Spaces.
- Independent TCC database and user accounts.
- Snapshot-based rollback.
- Ability to hold each agent in a stable display resolution and locale.

Limitations:

- No authoritative Apple latency numbers for save, restore or boot.
- VM snapshots include RAM-scale state and therefore have storage/I/O costs.
- Virtual display/GPU behavior is not guaranteed to match HDR, ProMotion, color management or every physical-monitor path.
- Hardware-dependent UI behavior—Touch ID, some cameras, display hot-plug and physical input—needs separate coverage.

`<MISSING_DATA>[Published macOS 26/27 benchmarks for VM restore latency, ScreenCaptureKit throughput inside guests, GPU animation fidelity and maximum sustainable concurrent macOS guests were not found.]</MISSING_DATA>`

#### TCC inside guests

`[H]` A macOS guest is a separate OS installation and maintains its own TCC state.

`[H]` The supportable method for preconfiguration is to enroll/configure the guest through MDM and deploy the applicable privacy policies. Directly editing or transplanting `TCC.db` is unsupported and brittle because grants are tied to code requirements and protected system state.

`[H]` A golden image may include installed management profiles and applications, but screen capture still requires the permission flow Apple permits for that OS release. On macOS 27, Accessibility management moves toward the declarative App Settings consent model described earlier.

#### Concurrency ceiling

`[H]` The public Virtualization.framework API documentation does not specify a fixed maximum number of concurrent macOS guests.

`<MISSING_DATA>[The current macOS 26/27 software-license limit for additional virtualized macOS instances and any independently enforced Virtualization.framework cap need verification against the exact SLA shipped with the host OS.]</MISSING_DATA>`

`[H]` The engineering ceiling is the first of:

- software-license allowance,
- available RAM,
- GPU/compositor load,
- storage IOPS,
- ScreenCaptureKit encoding/copy bandwidth,
- model inference budget,
- test application backend capacity.

`[H]` For genuinely independent agent sessions, one VM per concurrent agent is the durable architecture. Multiple agents in one host session can parallelize AX/Apple Events against separate processes, but they are not isolated from global focus, menus, pasteboard, alerts, Spaces and system dialogs.

---

### 10. Declared automation contracts as a pixel-free action surface

#### App Intents and App Schemas

`[H]` On macOS 26, App Intents actions are available through Shortcuts and increasingly through Spotlight. Apple’s HIG says App Shortcuts themselves are not supported on macOS, but actions defined with App Intents can be used to build custom shortcuts on Mac. [Apple HIG, updated June 8, 2026](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/260/))

`[H]` In the 27 releases, Apple is expanding “Assistant Schemas” into the broader App Schemas model. Schemas allow the system to interpret intents and entities as well-known domain actions such as creating an email draft or sending a message. Apple’s documentation and WWDC26 material describe Siri and Apple Intelligence as the system-level invokers. [Apple App schema domains](https://developer.apple.com/documentation/appintents/app-schema-domains) [WWDC26, “Build intelligent Siri experiences with App Schemas”](https://developer.apple.com/videos/play/wwdc2026/240/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/240/))

`[H]` App Intents can expose actions without requiring visual UI manipulation, making them excellent semantic contracts when an app adopts them correctly.

#### Can another third-party process invoke arbitrary intents?

`[H]` No generic public API was identified that lets an arbitrary non-system process enumerate every installed app’s intents and invoke them directly by bundle ID and intent identifier.

`[H]` The supported brokers are system experiences such as Shortcuts, Siri and Spotlight. A process can run an existing user-created Shortcut through the `shortcuts` command-line tool, but that is not equivalent to direct arbitrary-intent dispatch. [Apple Shortcuts User Guide](https://support.apple.com/guide/shortcuts-mac/run-shortcuts-from-the-command-line-apd455c82f02/mac)

`[H]` AppIntentsTesting in macOS 27 lets developers invoke and validate **their own** intents in isolation; it is a testing framework, not a general cross-app automation broker. Apple explicitly presents it as the first testing layer before Shortcuts, Spotlight and Siri. ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/240/))

`[M]` New entity-transfer mechanisms such as `IntentValueRepresentation` make system-brokered cross-app flows richer, but do not create an unrestricted entity-enumeration API for arbitrary processes.

#### Other declared surfaces

| Contract | Invocation path | Background capable | Discoverability | Failure modes |
|---|---|---|---|---|
| AppleScript `sdef` | Apple Events/OSA/ScriptingBridge | Usually | Dictionary can be queried | TCC, incomplete dictionaries, app-specific bugs |
| App Intents | Shortcuts/Siri/Spotlight/system brokers | Often | System metadata | Adoption is sparse; confirmations and UI may be required |
| Shortcuts | Shortcuts app or `shortcuts run` | Often | Named user workflows | Workflow must exist; prompts and UI actions may interrupt |
| NSServices | Registered service with pasteboard data | Sometimes | Services registration | Narrow data model; service names collide/change |
| URL scheme/universal link | `NSWorkspace.open` | Usually activates app | Declared schemes/links | Often launches/foregrounds; weak result/error channel |
| CLI/local IPC | App-specific | Yes | App-specific | No ecosystem-wide standard |

#### Coverage

`<MISSING_DATA>[No authoritative dataset measures the percentage of a typical 2026 Mac application portfolio exposing App Intents, complete AppleScript dictionaries, NSServices, actionable URL schemes or queryable entities.]</MISSING_DATA>`

A qualitative—not numerical—coverage curve is:

- `[M]` Apple first-party and automation-oriented productivity apps: strongest declared-contract coverage.
- `[M]` Long-lived professional Mac apps: often stronger AppleScript than App Intents.
- `[M]` New Swift/SwiftUI apps: growing App Intents adoption, but often only a small subset of UI behavior.
- `[M]` Electron, Qt and Java ports: commonly expose URL schemes or custom APIs, but relatively rarely comprehensive native intents or `sdef` dictionaries.
- `[H]` AX remains the only broadly cross-application semantic surface, despite its inconsistencies.

#### Does Codex use intents first?

`<INSUFFICIENT_EVIDENCE>[No OpenAI document, trace, binary evidence supplied in scope, or public issue establishes an intent-first routing policy.]</INSUFFICIENT_EVIDENCE>`

`[M]` <INFERENCE from="inspected AX read/write imports; inspected Apple Events entitlement and grant; no established App Intents evidence">The strongest supported conclusion is that Codex has AX and Apple Events as native process-directed surfaces and may choose between them at runtime. An App Intents-first strategy is possible through a dynamic bridge but has not been demonstrated.</INFERENCE>

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Codex Computer Use uses Screen Recording and Accessibility permissions | OpenAI Help Center | Current; retrieved August 12, 2026 | Official vendor documentation; primary for declared permissions | https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex |
| Codex local workflows process screenshots on-device | OpenAI Help Center | Current; retrieved August 12, 2026 | Official vendor documentation | https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan |
| Codex packages a signed `codex-code-mode-host` and uses V8 on Darwin | OpenAI Codex repository | Current; retrieved August 12, 2026 | First-party open-source packaging implementation | https://github.com/openai/codex/blob/main/scripts/codex_package/README.md |
| Codex authorization plug-in path and locked-use unlock/overlay expectation | OpenAI Codex issue #24086 | 2026; exact issue date not captured | Secondary empirical report in first-party repository; used only as corroboration | https://github.com/openai/codex/issues/24086 |
| Authorization plug-ins run in dedicated anonymous/UI and root hosts | Apple Security documentation | n.d.; current | Official platform API documentation | https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins |
| Authorization mechanisms can store authentication context | Apple `SetContextValue` documentation | n.d.; current | Official API documentation | https://developer.apple.com/documentation/security/authorizationcallbacks/1543148-setcontextvalue |
| Third-party authorization-plug-in precedent | Cisco Duo for macOS | July 21, 2026 | Current vendor implementation documentation | https://duo.com/docs/macos |
| Authorization database can be modified and explicitly reset | Jamf Connect `authchanger` | n.d.; current | Current vendor documentation and open-source implementation | https://learn.jamf.com/r/en-US/jamf-connect-documentation-current/authchanger |
| `system.login.screensaver` can be overwritten by a custom rule | Jamf `authchanger` source | Current | Open-source implementation | https://github.com/jamf/authchanger |
| macOS 27 removes legacy PPPC Accessibility granting | Apple WWDC26 app-management update | June 8, 2026 | Official deployment documentation; pre-release | https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web |
| macOS 27 adds declarative binary execution controls | Apple WWDC26 device-management session | June 2026 | Official WWDC platform documentation | https://developer.apple.com/videos/play/wwdc2026/206/ |
| SCK can capture a desktop-independent window | Apple ScreenCaptureKit documentation | n.d.; current | Official API documentation | https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init(desktopindependentwindow:) |
| SCK frames expose dirty rectangles and status | Apple ScreenCaptureKit documentation | n.d.; current | Official API documentation | https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects |
| A complete SCK frame is validated using `SCFrameStatus.complete` | Apple ScreenCaptureKit sample | n.d.; current | Official sample code | https://developer.apple.com/documentation/screencapturekit/capturing-screen-content-in-macos |
| `SCDisplay` is documented as a physical display | Apple ScreenCaptureKit documentation | n.d.; current | Official API documentation | https://developer.apple.com/documentation/screencapturekit/scdisplay |
| Virtualization.framework supports macOS guests on Apple silicon | Apple Virtualization sample | Current | Official API/sample implementation | https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-apple-silicon |
| VM machine state can be saved and restored | Apple `VZVirtualMachine` documentation | Current; API available since macOS 14 | Official API documentation | https://developer.apple.com/documentation/virtualization/vzvirtualmachine/restoremachinestatefrom(url:completionhandler:) |
| App Intents actions are usable in Shortcuts on Mac | Apple WWDC25 and HIG | June 2025; HIG updated June 8, 2026 | Official platform guidance | https://developer.apple.com/videos/play/wwdc2025/260/ |
| macOS does not support App Shortcuts as such | Apple HIG | Updated June 8, 2026 | Official design/platform documentation | https://developer.apple.com/design/human-interface-guidelines/app-shortcuts |
| App Schemas make well-known actions executable by Siri/system experiences | Apple App Intents documentation and WWDC26 | June 2026 | Official API and WWDC documentation | https://developer.apple.com/documentation/appintents/app-schema-domains |
| Platform SSO separately integrates FileVault, Lock Screen and login window | Apple Platform SSO deployment guide | June 12, 2026 | Official deployment/security documentation; macOS 27 portions pre-release | https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web |

---

## Knowledge Gaps

### OpenAI-proprietary implementation

- `<MISSING_DATA>[The CUA socket protocol, peer-authentication logic, credential source, replay protection and credential lifetime.]</MISSING_DATA>`
- `<MISSING_DATA>[Whether OpenAI’s uninstaller restores system.login.screensaver and removes every privileged artifact.]</MISSING_DATA>`
- `<MISSING_DATA>[The server-delivered kernel.js signing, pinning, retention and per-turn audit model.]</MISSING_DATA>`
- `<MISSING_DATA>[The runtime decision policy among AX, Apple Events, OCR/Vision and any declared intents.]</MISSING_DATA>`

### Undocumented macOS behavior

- `<MISSING_DATA>[Normative AX, SCK, CGWindow and event-posting behavior across lock, minimization, Spaces, display sleep and inactive user sessions.]</MISSING_DATA>`
- `<MISSING_DATA>[WindowServer backing-store retention and purge rules for nonvisible windows.]</MISSING_DATA>`
- `<MISSING_DATA>[Whether private virtual displays are consistently enumerated by ScreenCaptureKit.]</MISSING_DATA>`

### Private/debugging mechanisms

- `<MISSING_DATA>[Current macOS 26/27 View Debugger DTX protocol and headless invocation contract.]</MISSING_DATA>`
- `<MISSING_DATA>[Any notarization-safe entitlement for third parties to create independent CoreGraphics virtual displays.]</MISSING_DATA>`

### Quantitative performance

- `<MISSING_DATA>[VM boot/restore latency, SCK frame latency under load, AX tree activation cost by toolkit, and the concurrency ceiling on current M-series hardware.]</MISSING_DATA>`
- `<MISSING_DATA>[A representative installed-app dataset measuring App Intents, AppleScript, URL-scheme and AX action coverage.]</MISSING_DATA>`

### Pre-release uncertainty

- `[H]` macOS 27 remains pre-release as of August 12, 2026. Apple explicitly warns that Platform SSO, privacy-management and App Schema details may change before final release. ([support.apple.com](https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web))

---

## Recommended Next Steps

1. **Build an automated session-state conformance laboratory.**  
   Test all eight states in the requested matrix on the latest macOS 26 release and every macOS 27 seed, against small reference apps in AppKit, SwiftUI, Catalyst, Electron, Qt and Java. Record AX calls/results, notifications, SCK status/dirty rectangles, window metadata, event routing and frame hashes.  
   **Rationale:** Most low-confidence matrix cells are undocumented implementation behavior and are too important to infer.

2. **Perform a focused security review of the Codex authorization path.**  
   Reverse and fuzz only the local socket protocol; verify socket mode, peer audit-token/code-signature checks, nonce and turn binding, failed-attempt handling, credential storage and uninstaller rollback. Test whether an unprivileged local process can invoke or replay any broker message.  
   **Rationale:** The world-writable socket and loginwindow authorization path are the highest-impact trust boundary in the inspected design.

3. **Build a portfolio-wide native UI observability SDK.**  
   Add an authenticated test endpoint exposing stable view IDs, hierarchy, constraints, semantic design tokens, effective typography/colors, CA model/presentation state, text runs, render revision, app quiescence and a deterministic clock. Keep AX and SCK as external validation layers.  
   **Rationale:** This is the only durable route to native “computed style,” strong stale-frame detection and deterministic settling.

4. **Prototype VM-backed execution before investing in virtual-display SPI.**  
   Produce a macOS guest image pipeline with MDM-managed permissions, fixed display/locale settings, VM save/restore, per-test clones and measured capture/input latency.  
   **Rationale:** VMs provide real WindowServer, focus, TCC and login isolation; virtual displays do not, and `CGVirtualDisplay` lacks a public contract.

5. **Trace Codex’s action routing and measure declared-contract coverage.**  
   Instrument a controlled Mac with AX/Apple Events logging, unified logs and application-side probes; offer the same task through App Intents, AppleScript and AX and observe which path Codex selects. Separately inventory the actual application portfolio for `sdef`, App Intents metadata, Services and URL schemes.  
   **Rationale:** There is presently no evidence for intent-first Codex routing and no defensible ecosystem coverage percentage.

## Sources

- [https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex)
- [https://github.com/openai/codex/issues/24086](https://github.com/openai/codex/issues/24086)
- [https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init%28desktopindepend...](https://developer.apple.com/documentation/screencapturekit/sccontentfilter/init%28desktopindependentwindow%3A%29)
- [https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects?changes=_7](https://developer.apple.com/documentation/screencapturekit/scstreamframeinfo/dirtyrects?changes=_7)
- [https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins](https://developer.apple.com/documentation/security/extending-authorization-services-with-plug-ins)
- [https://developer.apple.com/documentation/security/authorizationcallbacks/1543148-setcontextvalue](https://developer.apple.com/documentation/security/authorizationcallbacks/1543148-setcontextvalue)
- [https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web](https://support.apple.com/guide/deployment/platform-sso-for-macos-dep7bbb05313/web)
- [https://duo.com/docs/macos](https://duo.com/docs/macos)
- [https://learn.jamf.com/r/en-US/jamf-connect-documentation-current/authchanger](https://learn.jamf.com/r/en-US/jamf-connect-documentation-current/authchanger)
- [https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web](https://support.apple.com/id-id/guide/deployment/depd567c9ffa/web)
- [https://openai.com/index/introducing-the-codex-app/](https://openai.com/index/introducing-the-codex-app/)
- [https://github.com/openai/codex/blob/main/scripts/codex_package/README.md](https://github.com/openai/codex/blob/main/scripts/codex_package/README.md)
- [https://developer.apple.com/documentation/appkit/nsview/layer](https://developer.apple.com/documentation/appkit/nsview/layer)
- [https://developer.apple.com/documentation/screencapturekit/scdisplay?changes=_5](https://developer.apple.com/documentation/screencapturekit/scdisplay?changes=_5)
- [https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-ap...](https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-apple-silicon?changes=_4%2C_4)
- [https://developer.apple.com/documentation/virtualization/vzvirtualmachine/restoremachinestatefrom...](https://developer.apple.com/documentation/virtualization/vzvirtualmachine/restoremachinestatefrom%28url%3Acompletionhandler%3A%29)
- [https://developer.apple.com/videos/play/wwdc2025/260/](https://developer.apple.com/videos/play/wwdc2025/260/)
- [https://developer.apple.com/videos/play/wwdc2026/240/](https://developer.apple.com/videos/play/wwdc2026/240/)
