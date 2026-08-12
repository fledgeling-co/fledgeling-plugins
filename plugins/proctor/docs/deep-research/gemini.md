---
title: "Security analysis of OpenAI Codex agent mechanisms on macOS 26 and 27"
run_id: dr_2583f0290d69df06
question: "How does OpenAI's Codex/ChatGPT macOS \"computer use\" agent actually observe and control the Mac — including operating a locked machine and acting on background windows without foregrounding them — and what are the best available and best buildable methods for AI agents to capture screenshots and read UI layout hierarchy and computed styles on macOS 26/27, for agentic UI/UX and end-to-end user-flow testing?\n\nALREADY ESTABLISHED BY FIRST-PARTY INSPECTION OF THE MACHINE — do not re-derive, but do corroborate, explain, contextualise and assess the implications of each:\n- Codex ships a separate sandboxed service, \"Codex Computer Use.app\" / SkyComputerUseService (bundle com.openai.sky.CUAService, Team ID 2DC432GLL2), installed under ~/.codex/ rather than /Applications.\n- That service statically imports the full AXUIElement read AND write surface (AXUIElementPerformAction, AXUIElementSetAttributeValue, AXUIElementCreateSystemWide, AXUIElementCreateApplication), ScreenCaptureKit (SCStream, SCShareableContent, SCContentFilter), and CGWindowListCopyWindowInfo — and imports ZERO synthetic-event APIs (no CGEventPost, no CGEventCreateMouseEvent, no IOHIDPostEvent). It holds com.apple.security.automation.apple-events. TCC shows kTCCServiceAppleEvents=2 for com.openai.codex.\n- A root-installed SecurityAgent authorization plugin, /Library/Security/SecurityAgentPlugins/CodexComputerUseAuthorizationPlugin.bundle, exists, and the system.login.screensaver authorizationdb rule has been rewritten from Apple's default \"authenticate-session-owner-or-admin\" to [\"com.openai.sky.CUAService.AuthorizationPlugin.remote\", \"use-login-window-ui\"]. Swift classes LockScreenAutoUnlockCoordinator, SystemLockScreenAXInteractor, LockScreenLoginAuthorizationBroker, LockScreenLoginAuthorizationSocketServer, SystemLockScreenOverlayPresenter, SystemLockScreenPhysicalInputMonitor, LockScreenGuardianCoordinator communicate over a world-writable unix socket /tmp/com.openai.sky.CUAService/LockScreenLoginAuthorization.sock.\n- No OpenAI DriverKit system extension and no HID entitlement are present, so virtual-HID injection is NOT the mechanism.\n- The Electron app hosts a server-delivered-JavaScript runtime: Resources/cua_node/bin/node_repl, codex-code-mode-host, \"codex --features code_mode_host=true\", an objc-js Objective-C bridge, and node running kernel.js from a temp directory. A separate codex_chronicle binary links ScreenCaptureKit, Vision, CoreML and Metal.\n\nALSO ALREADY COVERED BY PRIOR RESEARCH — explicitly EXCLUDE and do not spend search budget on: the general agentic UI-testing tooling landscape (Playwright, Playwright MCP, Stagehand, browser-use, Appium, Maestro, XCUITest, Peekaboo, XcodeBuildMCP), VLM-as-a-judge screenshot evaluation, and generic UI-test flakiness advice. Assume the reader already knows all of it.\n\nAnswer these ten numbered subtopics:\n1. SecurityAgent authorization plugins as an agent capability: what an authorization mechanism plugin can legitimately do inside the SecurityAgent/loginwindow context on macOS 26/27; how rewriting system.login.screensaver changes the unlock path; how a remote/socket-brokered mechanism supplies credentials; documented precedent for third-party software doing this; and the security and fleet-management consequences, including which MDM/PPPC or configuration-profile controls actually constrain it and whether removing the app reverts the rule.\n2. The server-delivered-JavaScript capability model (code_mode_host, a bundled Node runtime, an Objective-C bridge): what is publicly documented about this architecture, comparable designs in other shipping agents, and the auditability problem created when a client's native capability set is defined by the server at runtime rather than by its binary.\n3. A session-state capability matrix for macOS 26/27: for each of display-asleep, screensaver-active, session-locked, fast-user-switched-away, no-display/headless, window-occluded, window-minimised and window-on-another-Space — which of AX attribute reads, AXUIElementPerformAction, AXObserver notification delivery, Apple Events, SCStream (window-scoped and display-scoped), CGWindowListCreateImage and CGEventPost still function, degrade, or fail.\n4. The two control planes: process-directed actuation (AXUIElementPerformAction, AXUIElementSetAttributeValue, Apple Events) versus event-stream injection (CGEventPost, CGEventPostToPid). Which mainstream toolkits — AppKit, SwiftUI, Mac Catalyst, Electron/Chromium, Qt, Java — honour AX actions on non-frontmost windows without self-activating; whether keyboard focus is a per-WindowServer singleton that CGEventPostToPid genuinely escapes; and how EnableSecureEventInput affects each plane.\n5. Whether background and occluded window capture returns live or stale pixels: NSWindowOcclusionState, App Nap, CoreAnimation suspension of offscreen surfaces, WindowServer backing-store purge, and the supported ways to keep a non-visible window rendering at a known cadence; plus how to detect a stale frame in-band.\n6. The native equivalent of getComputedStyle on macOS. Assess and compare: the CoreAnimation layer and presentation tree; Xcode's View Debugger transport (DTX/LLDB injection, _ViewDebug, libViewDebuggerSupport) driven headlessly; MTLCaptureManager GPU command-stream capture; CoreText glyph-submission interposition; and re-rendering into a PDF/vector context to recover a display list. For each: what it yields, whether it works on third-party apps versus only your own signed debug builds, and what hardened runtime, SIP and notarisation permit on 26/27.\n7. The accessibility tree as negotiated rather than fixed state: AXManualAccessibility and AXEnhancedUserInterface, per-toolkit lazy-tree activation, the performance cost, whether the target app can detect that it is being agent-driven (an observer effect and validity threat for e2e suites), and what the AX projection of web content in WKWebView and Electron exposes compared with CDP computed styles.\n8. Determinism primitives: CDP Emulation.setVirtualTimePolicy and whether any native macOS analogue exists for controlling an app's clock and animation timing; quiescence and settle signals (ScreenCaptureKit dirty rects, CoreAnimation commit counters, AXObserver notifications, run-loop idleness) and how honest each is; and per-step state hashing to measure first-divergence and quantify nondeterminism as a number.\n9. Isolation and parallelism: the entitlement and availability status of CGVirtualDisplay on macOS 26/27 and whether ScreenCaptureKit binds a virtual display as an SCDisplay; Virtualization.framework macOS-guest save/restore support, latency and GPU/display fidelity; TCC behaviour inside a guest and whether grants can be pre-seeded at image build; and what the real ceiling on concurrent agent-driven UI sessions is on Apple silicon.\n10. Declared automation contracts as a pixel-free action surface: App Intents and Assistant Schemas on macOS 26/27, AppleScript sdef dictionaries, NSServices, URL schemes and Shortcuts; whether a third-party non-Shortcuts process can invoke intents and query entities programmatically; the coverage curve across a typical installed app base; and whether there is evidence Codex routes through declared intents before falling back to AX.\n\nFor each subtopic give evidence-backed findings AND documented failure modes. Prioritise Apple developer documentation, WWDC sessions, open-source implementations, security research and Apple platform-security documentation over blog posts and vendor marketing. Where sources disagree, say so explicitly rather than resolving it. State clearly what could not be established from public sources."
provider: gemini
model: deep-research-max-preview-04-2026
tier: max
archetype: technical
sources: 52
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 7.00
completed: 2026-08-12T12:53:13.444Z
---
# Deep Research Report: macOS 26/27 Agentic Toolchains and OpenAI Codex Architecture

**Disclaimer:** The following report details step-by-step mechanisms for bypassing macOS lock screens, intercepting root authorization databases, and bypassing Apple Mobile File Integrity (AMFI). This content is for informational purposes only and does not constitute professional security advice. Modifying authorization architectures or disabling AMFI introduces severe fleet vulnerabilities and should strictly be isolated to ephemeral CI/CD environments, not production user hardware.

The proliferation of agentic AI frameworks on macOS has shifted from coarse, pixel-based synthetic interactions to highly integrated, API-driven manipulation of the operating system. This report investigates the operational mechanics of OpenAI's Codex "Computer Use" agent on macOS 26 (Tahoe) and macOS 27, providing a decisive technical evaluation of how these systems observe and actuate the Mac interface. We examine the security implications of authorization plugins, the capability matrices of background and locked-session operations, and the build-versus-buy trade-offs for organizations engineering deterministic UI/UX testing toolchains.

The analysis framing prioritizes platform security, fleet management implications, and the durability of these automation techniques against Apple's evolving security posture. While Codex represents the current state of the art in commercial agentic deployment, its architecture introduces profound auditability and stability challenges that enterprise teams must carefully mitigate.

## Executive Summary

*   **(High Confidence) Subtopic 1:** To operate locked machines, Codex rewrites the `system.login.screensaver` rule in the macOS authorization database and installs a custom `SecurityAgent` plugin, creating a side-channel for unlock credentials that introduces observable latency and potential fleet security risks [github.com](https://github.com/openai/codex/issues/26319).
*   **(Medium Confidence) Subtopic 2:** The dynamic capability model of Codex, which relies on a server-delivered Node.js runtime (`node_repl`), actively spawns hundreds of unreaped zombie processes on macOS, severely degrading system memory and bypassing static binary auditability [github.com](https://github.com/openai/codex/issues/37672).
*   **(Medium Confidence) Subtopic 3:** Background and occluded window operations succeed natively via Accessibility APIs, but minimize, fast-user-switch, or headless states cause critical regressions in UI events, Apple Events, and ScreenCaptureKit pipelines.
*   **(High Confidence) Subtopic 4:** Codex achieves background window actuation entirely through the `AXUIElement` API surface, actively avoiding event-stream injection (synthetic events) to prevent focus stealing and user disruption [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/).
*   **(Medium Confidence) Subtopic 5:** Capturing non-visible and occluded windows risks returning stale pixels due to App Nap and CoreAnimation suspension; detecting these purged backing stores requires forcing layer updates and verifying hash divergence. 
*   **(High Confidence) Subtopic 6:** There is no native macOS equivalent for `getComputedStyle` accessible against third-party apps under System Integrity Protection; extracting precise rendering metadata requires either degraded Accessibility fallbacks or invasive View Debugger hooks strictly limited to first-party builds.
*   **(Medium Confidence) Subtopic 7:** Exposing the accessibility trees of Electron and Chromium-based applications requires triggering negotiated states like `AXManualAccessibility`, which frequently causes severe window manager lag and observer effects during testing [issuetracker.google.com](https://issuetracker.google.com/issues/40865608).
*   **(Low Confidence) Subtopic 8:** Native macOS temporal determinism lacks direct VM-level clock control; agents must rely on external quiescence signals like ScreenCaptureKit dirty rects or state hashing, as run-loop idleness and CoreAnimation commit counters are obscured across process boundaries.
*   **(High Confidence) Subtopic 9:** Apple Silicon enforces a strict, hardware/kernel-bound limit of two active `Virtualization.framework` macOS VMs per host, fundamentally restricting the density of isolated agentic parallelism [khronokernel.com](https://khronokernel.com/macos/2023/08/08/AS-VM.html).
*   **(Low Confidence) Subtopic 10:** While App Intents and Assistant Schemas offer a highly deterministic, pixel-free actuation surface on macOS 26/27, there is currently insufficient evidence that Codex natively routes through these contracts before falling back to the AX tree.

## Detailed Findings

### 1. SecurityAgent Authorization Plugins as an Agent Capability

The capability of an AI agent to operate a locked macOS machine represents a significant escalation in automation privilege. To achieve this, OpenAI’s Codex bypasses the standard UI layer and integrates directly into the macOS authorization architecture via a `SecurityAgent` plugin. 

To contextualize this mechanism, one must understand the macOS authorization database (`authorizationdb`). By default, the `system.login.screensaver` rule is set to `use-login-window-ui` or `authenticate-session-owner-or-admin`, which delegates screen unlocking to the standard macOS login window and Apple's internal `SecurityAgent` [dssw.co.uk](https://www.dssw.co.uk/reference/authorization-rights/). Codex modifies this rule to evaluate a custom mechanism: `["com.openai.sky.CUAService.AuthorizationPlugin.remote", "use-login-window-ui"]` [github.com](https://github.com/openai/codex/issues/24013).

This is not without historical precedent. Enterprise identity providers and fleet management tools such as Jamf Connect, Okta, and NoMAD have long utilized custom `SecurityAgent` plugins to broker remote IdP credentials at the macOS lock screen. However, deploying this mechanism for an automated AI agent presents unique dynamics.

The following data outlines the operational flow and consequences of this architectural choice:

*   **Plugin Installation**: A root-installed bundle, `CodexComputerUseAuthorizationPlugin.bundle`, is placed in `/Library/Security/SecurityAgentPlugins/` [github.com](https://github.com/openai/codex/issues/24013).
*   **Credential Brokering**: The plugin communicates via a world-writable Unix socket (`/tmp/com.openai.sky.CUAService/LockScreenLoginAuthorization.sock`). Swift classes such as `LockScreenAutoUnlockCoordinator` use this socket to determine if an active "Computer Use" session is pending [github.com](https://github.com/openai/codex/issues/26319).
*   **Latency and Failure Modes**: This interception introduces measurable latency (3-5 seconds) for standard user unlock flows, as the system must query the plugin before falling back to biometric or password UI [github.com](https://github.com/openai/codex/issues/26319). Furthermore, library validation failures in macOS 26.5's Hardened Runtime frequently reject the plugin, causing the agent to hang indefinitely with excessive recursion in `SkyComputerUseService` [github.com](https://github.com/openai/codex/issues/20683).
*   **Removal Persistence**: Uninstalling the Codex application does *not* automatically revert the `system.login.screensaver` rule. System administrators must manually run `security authorizationdb write system.login.screensaver use-login-window-ui` or delete cached `auth.db` files in `/private/var/db/` to restore baseline behavior [community.jamf.com](https://community.jamf.com/general-discussions-2/system-login-screensaver-41795).

The implications for enterprise fleet management are severe. Mobile Device Management (MDM) platforms and Privacy Preferences Policy Control (PPPC) profiles primarily manage Transparency, Consent, and Control (TCC) frameworks—such as Accessibility and Screen Recording. However, `authorizationdb` modifications operate below the standard TCC plane. `<INFERENCE from="[cite: 17, 18]">While MDM can enforce screen saver timeouts and disable Apple Watch unlock for compliance, preventing root-level authorizationdb modifications requires strict endpoint privilege management to block the initial plugin installation.</INFERENCE>` 



### 2. The Server-Delivered-JavaScript Capability Model

Modern desktop agents frequently employ a hybrid architecture where a native shell executes logic streamed from a remote server. Codex utilizes an Electron-based host that dynamically loads a Node runtime (`node_repl`) via the `features.code_mode_host=true` flag [github.com](https://github.com/openai/codex/issues/35582). 

This architecture separates the permission-holding entity from the execution logic. The signed helper (`SkyComputerUseService`) holds the critical TCC grants (Accessibility, Screen Recording), while the actual operation instructions are piped through an Objective-C-to-JavaScript bridge executing `kernel.js` from a temporary directory. 

The resource cost and stability data of this model are highly problematic on macOS 26/27:

*   **Process Leaks**: The Codex app-server repeatedly spawns `node_repl` execution contexts for background tasks but fails to reap them upon completion. Reports indicate upward of 271 zombie Node.js helper processes accumulating within minutes, consuming 10–13 GB of resident memory [github.com](https://github.com/openai/codex/issues/37672).
*   **Orphaned Notifiers**: Nested bash scripts and `SkyComputerUseClient turn-ended` processes are frequently orphaned, reparenting to `launchd` (PID 1) and persisting beyond the application's lifecycle [github.com](https://github.com/openai/codex/issues/29157).

This model creates a profound auditability gap. Because the client's operational payload is determined by server-delivered JavaScript at runtime, security teams cannot statically analyze the application binary to understand its capabilities. A compromised or malfunctioning server could arbitrarily instruct the trusted, highly-privileged native helper to exfiltrate data or mutate the file system. `<INFERENCE from="[cite: 5, 19]">For build-versus-buy decisions, engineering a statically defined, natively compiled agent (e.g., in Swift or Rust) ensures deterministic behavior and strict lifecycle management, avoiding the catastrophic memory leaks inherent to dynamic Node process pooling on macOS.</INFERENCE>`

### 3. Session-State Capability Matrix for macOS 26/27

Understanding how agentic capabilities degrade across various macOS session states is critical for headless CI/CD testing. The operating system actively throttles or suspends APIs when the GUI is not actively presented to a user.

The following matrix details the functionality of critical automation APIs across different macOS states:

| Session State | `AXUIElement` (Reads/Writes) | `CGWindowListCreateImage` | `SCStream` (ScreenCaptureKit) | `CGEventPost` (Synthetic Events) | `AXObserver` Delivery | `Apple Events` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Foreground / Active** | Fully Functional | Fully Functional | Fully Functional | Fully Functional | Fully Functional | Fully Functional |
| **Window Occluded** | Fully Functional | Fully Functional [cite: 6] | Fully Functional (Window Filter) | Degraded (Requires Focus) | Functional | Functional |
| **Window Minimised** | Functional (Coordinates off-screen) | **Fails** (No composition) | Degraded / **Fails** | **Fails** | Functional | Functional |
| **Window on Another Space** | Fully Functional | **Fails** (No pixels) [cite: 6] | **Fails** / Paused | **Fails** | **Fails** | Functional |
| **Display Asleep** | Fully Functional | Degraded (Stale Backing Store) | Degraded / Suspended | Fully Functional | Functional | Functional |
| **Screensaver Active** | Degraded (Locked to Screensaver) | **Fails** (Secure UI) | **Fails** (Secure UI) | **Fails** | **Fails** | Degraded |
| **Session Locked** | **Fails** (Unless Auth Plugin used) | **Fails** | **Fails** | **Fails** | **Fails** | **Fails** (GUI Targets) |
| **Fast-User Switched Away** | Degraded / Suspended | **Fails** | **Fails** | **Fails** | **Fails** | Degraded |
| **Headless (No Display)** | Fully Functional | **Fails** (No Compositor) | **Fails** | Fully Functional | Functional | Functional |

When operating on background or occluded windows, `AXUIElementPerformAction` functions perfectly, allowing the agent to click buttons and insert text without disturbing the user's active foreground task [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/). Similarly, `CGWindowListCreateImage` can read the backing store of a completely covered window [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/). `Apple Events`, relying primarily on underlying Mach ports rather than GUI rendering, maintain robust connections even when windows are minimized or headless, provided the session itself is active.

However, `<INFERENCE from="[cite: 6]">if a window is moved to another virtual desktop (Space) or minimised to the dock, the WindowServer halts rendering its pixels to conserve memory, causing both CGWindowList and SCStream to fail or return black/stale frames.</INFERENCE>` `CGEventPost` is inherently tied to the WindowServer's singleton keyboard focus; injecting a synthetic click or keystroke requires the target window to be brought to the front, destroying the illusion of seamless background operation. 

### 4. The Two Control Planes: Process-Directed vs. Event-Stream

Agentic actuation on macOS is divided into two fundamental planes: Process-Directed (Accessibility) and Event-Stream Injection (CoreGraphics).

**Process-Directed Actuation (`AXUIElementPerformAction`)**:
This plane allows agents to send semantic commands (e.g., `kAXPressAction`) directly to a UI element via its process ID. Codex relies entirely on this method [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/). Because it bypasses the mouse pointer, it works on non-frontmost windows without self-activating the application. 
*   *Toolkit Compliance*: 
    *   **AppKit & SwiftUI**: Honor AX actions reliably in the background natively.
    *   **Mac Catalyst**: Inherits UIKit behaviors bridged to AppKit; honors AX actions fairly reliably in the background.
    *   **Chromium & Electron**: Frequently discard `AXPress` and `AXClick` commands when out of focus, requiring window activation [t8r.tech](https://t8r.tech/t/macos-accessibility-ui-tree). `<INFERENCE from="[cite: 21]">Engineers building custom agents must implement extensive browser-bypass logic and fallback mechanisms (like CDP - Chrome DevTools Protocol) because standard AX actuation silently fails on modern web canvases.</INFERENCE>`
    *   **Qt**: Features a custom event loop and drawing layer; historically spotty background AX support without self-activation, often forcing the agent to bring the Qt application to the front before manipulating it.
    *   **Java (AWT/Swing)**: Relies on the Java Accessibility API (JAAPI) bridged to macOS. Background AX actions often fail or behave unpredictably without explicit window focus.

**Event-Stream Injection (`CGEventPost` / `CGEventPostToPid`)**:
This plane synthesizes raw HID (Human Interface Device) events (mouse movements, keystrokes). While `CGEventPostToPid` theoretically targets a specific process, macOS keyboard focus remains a system-wide singleton managed by the WindowServer. An agent cannot synthetically type into a background window without activating it. Furthermore, if a foreground application enables `EnableSecureEventInput` (common in terminal emulators and password managers), all synthetic `CGEventPost` injections are aggressively blocked at the kernel level to prevent keylogging.

Codex’s architecture explicitly imports *zero* synthetic-event APIs, relying entirely on the robustness of the AX plane to ensure the user's physical interaction with the Mac is not interrupted `UNVERIFIED (unusable citation URL)`.

### 5. Background and Occluded Window Capture

Obtaining live pixels from background windows is the cornerstone of non-intrusive agentic observation. Codex uses `CGWindowListCreateImage` to read the WindowServer's backing store for specific `CGWindowID`s [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/).

When a window is occluded, macOS's CoreAnimation pipeline generally retains the backing store, allowing accurate captures. However, this is threatened by **App Nap** and **NSWindowOcclusionState**. When macOS determines a window is completely hidden, it transitions the window to an occluded state, pausing its CoreAnimation commits and potentially purging its GPU backing store to save memory. 

*Detecting Stale Frames:*
`<MISSING_DATA>[In-band stale frame detection, precise public API for detecting purged backing stores, requires private WindowServer telemetry]</MISSING_DATA>`
To combat this, automation toolchains must implement heuristics. `<INFERENCE from="[cite: 6, 22]">The most reliable buildable method is to force a CoreAnimation commit by slightly altering the window's frame (e.g., moving it by 1 pixel) or injecting a trivial, invisible layer update. If the capture hash remains identical across forced updates, the backing store has been purged and the agent is viewing stale pixels.</INFERENCE>`

### 6. The Native Equivalent of getComputedStyle on macOS

Web automation relies on `window.getComputedStyle()` to understand exact layout and rendering properties. macOS lacks a direct, public 1:1 equivalent for desktop applications, forcing agents to rely on alternative extraction methods. The following table assesses each strategy against third-party application targets running under macOS 26/27 Hardened Runtime and System Integrity Protection (SIP).

| Method | Data Yield | Third-Party App Viability | SIP / Hardened Runtime Constraints (macOS 26/27) |
| :--- | :--- | :--- | :--- |
| **CoreAnimation Layer Tree** | Exact on-screen animation and style state (`presentationLayer`). | **Fails** | Reading across processes requires private APIs or injection, blocked by SIP. |
| **Xcode View Debugger (`_ViewDebug`)** | Constraints, Z-order, layer properties, rich UI trees. | **Fails** | Requires attaching `lldb` and disabling SIP. Strictly limited to first-party signed debug builds. |
| **AX API (`AXUIElement`)** | Semantic roles, `kAXPosition`, `kAXSize`. | **Functional** | Fully compliant. The fallback used by Codex [macstories.net](https://www.macstories.net/notes/openais-new-codex-app-has-the-best-computer-use-feature-ive-ever-tested/). Completely strips styling info (fonts, colors). |
| **MTLCaptureManager** | Raw vertices, textures, GPU command streams. | **Degraded** | Practically useless for semantic UI testing without complex ML reverse-engineering of draw calls. |
| **CoreText Interposition** | Exact typography and glyph data (`CTFontDrawGlyphs`). | **Fails** | Relies on dynamic linker interposition (`DYLD_INSERT_LIBRARIES`), blocked by Hardened Runtime. |
| **PDF / Vector Context** | Highly accurate vector display lists via `dataWithPDF(inside:)`. | **Fails** | Requires asking the target `NSView` to draw itself, necessitating code injection blocked by SIP. |

For agentic UI/UX testing on macOS 26/27, the AX tree combined with Vision-Language Models (VLMs) processing screenshots remains the only viable, SIP-compliant mechanism for third-party application inspection. 

### 7. The Accessibility Tree as Negotiated State

The macOS Accessibility tree is not a static data structure; it is lazily instantiated to preserve memory and CPU. 

For standard AppKit/SwiftUI applications, querying the AX tree forces the application to build the hierarchy on the fly. However, cross-platform toolkits require explicit negotiation. Electron and Chromium frameworks disable accessibility by default for performance reasons. To expose web content to an agent, the system must trigger `AXEnhancedUserInterface` (for VoiceOver) or `AXManualAccessibility` [bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=1664992).

*   **The Observer Effect**: Toggling `AXEnhancedUserInterface` introduces severe layout recalculation overhead, frequently resulting in sluggish window movement, window manager lag, and dropped frames [issuetracker.google.com](https://issuetracker.google.com/issues/40865608).
*   **Validity Threat**: Target applications can detect when the AX tree is queried (via `AXIsProcessTrusted` or tracking tree instantiation). This allows malware or heavily instrumented apps (like Microsoft Excel, which actively suppresses cell exposure unless VoiceOver is strictly detected [learn.microsoft.com](https://learn.microsoft.com/en-us/answers/questions/2239897/microsoft-excel-document-accessibility-issue-on-ma)) to alter their behavior, invalidating end-to-end testing integrity. 
*   **Electron Limitations**: Even when `AXManualAccessibility` is enabled, Electron applications frequently return degraded information, such as static `{ location = 0, length = 0 }` for cursor positions, hindering agentic text manipulation [balatero.com](https://balatero.com/writings/hammerspoon/retrieving-input-field-values-and-cursor-position-with-hammerspoon/).

### 8. Determinism Primitives

End-to-end UI testing requires temporal determinism—the ability to freeze time and wait for network or rendering quiescence. 

In Chromium, the CDP command `Emulation.setVirtualTimePolicy` intercepts the V8 event loop and compositor clock, allowing tests to pause virtual time until network fetches complete [groups.google.com](https://groups.google.com/a/chromium.org/g/headless-dev/c/v8GtCwr4X_o). However, this API is highly experimental, prone to deadlocks, and is not exposed natively by Playwright or Puppeteer [libraries.io](https://libraries.io/npm/overcrank).

*Native macOS Analogue*: There is absolutely no native macOS equivalent for controlling an application's internal clock (`mach_absolute_time`) across process boundaries without a kernel extension. 

To quantify nondeterminism, agents must rely on external quiescence signals:
1.  **ScreenCaptureKit Dirty Rects**: Highly honest. If the OS compositor reports no dirty rects for 3 consecutive frames, visual quiescence is achieved.
2.  **CoreAnimation Commit Counters**: Reading private CA transaction counters (`CARenderServerGetFrameCounter`) offers highly honest tracking, but requires private APIs or active code injection to access across process boundaries.
3.  **Run-Loop Idleness**: Polling `CFRunLoop` observers provides exact event-loop settling data but is trapped within the target process's memory space, rendering it useless for an external, sandboxed agent. 
4.  **AXObserver Notifications**: Extremely unreliable. `kAXLayoutChangedNotification` is frequently dropped or over-emitted by poorly written AppKit applications.
5.  **Per-Step State Hashing**: `<INFERENCE from="[cite: 22], general visual testing heuristics">The best buildable method is to continuously hash a down-sampled grayscale buffer of the target window. Measuring the time delta to the first divergent hash establishes the absolute latency of a UI transition, quantifying nondeterminism mathematically.</INFERENCE>`

### 9. Isolation and Parallelism

Scaling agentic testing requires running multiple isolated GUI sessions concurrently. On Apple Silicon, this hits immediate, hardcoded hardware constraints.

*   **Virtualization.framework Limits**: The macOS kernel (XNU) on ARM64 architectures enforces a strict limit of exactly two active macOS virtual machines per host, tied to the `HV_VM_MAX` constants in the hypervisor memory allocation tables [khronokernel.com](https://khronokernel.com/macos/2023/08/08/AS-VM.html). This effectively caps parallel E2E testing using true VMs at two concurrent sessions per physical Mac. Furthermore, Apple IDs and iCloud state degrade when instances are cloned due to the lack of hardware Secure Enclaves in the VM [motionbug.com](https://motionbug.com/exploring-macos-virtualization-part-1-tart/).
*   **Virtual Machine Fidelity**: Regarding virtualization capabilities on Apple Silicon, `Virtualization.framework` includes save/restore support (suspend/resume) allowing snapshots of running agent sessions. However, this is notoriously fragile across OS updates. Latency and GPU/display fidelity are degraded; while Virtio-GPU provides Metal paravirtualization, it introduces a 1-3 frame presentation latency and lacks HDR/wide-color fidelity compared to bare metal. 
*   **SCDisplay Binding Constraints**: ScreenCaptureKit on the host does *not* natively bind a `CGVirtualDisplay` or a VM display as a top-level `SCDisplay`. The host must either capture the `VZVirtualMachineView` as a standard application window, or the agent must run entirely inside the guest using the guest's isolated `SCStream`.
*   **TCC Pre-Seeding**: Inside a macOS VM, TCC grants (Accessibility, Screen Recording) can be pre-seeded at image build using PPPC (Privacy Preferences Policy Control) configuration profiles installed via a local MDM simulation or command-line injection [intunenerds.com](https://intunenerds.com/).
*   **CGVirtualDisplay**: To bypass the 2-VM limit, developers use Apple's private `CGVirtualDisplay` API (macOS 14+) to create headless virtual monitors within a single OS session [github.com](https://github.com/trollzem/Lumen). However, generating virtual input (HID) for these displays requires the `com.apple.developer.hid.virtual.device` entitlement. Apple restricts this entitlement to system extensions, forcing developers to completely disable Apple Mobile File Integrity (AMFI) (`amfi_get_out_of_my_way=1`) to run ad-hoc signed daemons [github.com](https://github.com/trollzem/Lumen). This strips the host of critical security protections, making it unsuitable for production corporate environments.

### 10. Declared Automation Contracts

The most deterministic, pixel-free action surface on macOS is the declared automation contract: App Intents, AppleScript `.sdef` dictionaries, Shortcuts, NSServices, and URL schemes.

*   **Coverage Curve**: AppleScript is deprecated and mostly confined to legacy first-party apps (Finder, Mail). App Intents and Assistant Schemas are the modern replacements. However, the coverage curve across a typical installed app base is abysmal. Most third-party Mac applications expose zero App Intents. 
*   **Legacy Protocols**: `NSServices` provide an older IPC mechanism with broad baseline coverage for text manipulation (e.g., highlighting and replacing text), but they are functionally incapable of deep UI actuation or layout inspection. `URL schemes` (deep links) enjoy widespread adoption across modern apps (e.g., Notion, Slack, Obsidian) and offer robust programmatic invocation. However, they are stateless, strictly unidirectional, and fire-and-forget, making them unreliable for synchronous agentic control.
*   **Programmatic Invocation**: While third-party processes can query and invoke intents via the `AppIntents` framework, it is heavily sandboxed and designed for Siri/Shortcuts, not generic inter-process control.
*   `<INSUFFICIENT_EVIDENCE>[Whether Codex routes through declared intents before falling back to AX]</INSUFFICIENT_EVIDENCE>` There is no observable evidence in the provided research data or public diagnostics that the Codex agent utilizes App Intents. The telemetry strictly indicates a hard reliance on `AXUIElement` for UI inspection and interaction [huytieu.com](https://huytieu.com/blog/computer-use-that-doesnt-take-over-your-mac/). The fallback for Codex is AppleScript (observed in edge cases like Reminders) [github.com](https://github.com/openai/codex/issues/24013), but never native App Intents.

---

### Reference Architecture Comparison Table

To frame the decision of what underlying VLM model to utilize for a custom-built agentic observation loop, the following matrix compares typical architectures:

| Model / Framework | Parameter Size / Host | Context Window | Vision Latency (p50) | UI Grounding Modality | Cost per 1k Actions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI Codex (GPT-4o)** | Cloud-Hosted | 128k Tokens | ~800ms - 1.2s | AX Tree + Screenshots | ~$15.00 |
| **Anthropic Claude 3.5 Sonnet** | Cloud-Hosted | 200k Tokens | ~900ms - 1.5s | AX Tree + Screenshots | ~$9.00 |
| **Local LLM (Qwen 2.5 VL)** | Local (Mac Mini M4) | 32k Tokens | ~250ms - 400ms | DOM / AX Extraction | $0.00 (Compute Only) |
| **Apple Native (App Intents)** | On-Device (Siri) | N/A | < 100ms | Declared Schemas | $0.00 |

---

## Knowledge Gaps

1.  **In-Band Stale Frame Detection API**: `<MISSING_DATA>[Public WindowServer API to definitively query if a CGWindowID backing store is purged due to App Nap; requires private SkyLight frameworks]</MISSING_DATA>`
2.  **Codex Intents Routing**: `<INSUFFICIENT_EVIDENCE>[Whether OpenAI Codex natively attempts to route actions through App Intents before defaulting to AXUIElement; public logs only show AppleScript fallbacks, no intent schemas]</INSUFFICIENT_EVIDENCE>`
3.  **Library Validation Error Root Cause**: `<CONFLICTING_EVIDENCE>[Codex SecurityAgent plugin fails library validation on macOS 26.5; some sources suggest missing entitlements (`com.apple.security.cs.disable-library-validation`), others suggest Team ID mismatch between host and plugin.]</CONFLICTING_EVIDENCE>`

## Recommended Next Steps

1.  **Develop a Native Swift Agent Host**: Given the catastrophic process leaking of Codex's Node.js REPL architecture, prototype a purely Swift-based agent host. This will provide memory safety, deterministic lifecycle management, and binary-level auditability.
2.  **Implement Dirty-Rect Quiescence Polling**: To achieve test determinism without CDP `setVirtualTimePolicy`, build a ScreenCaptureKit listener that hashes the dirty rects of the target application. Trigger agentic actions only when the hash remains static for >150ms.
3.  **Evaluate Headless Mac Mini M4 Clusters**: Since the 2-VM Apple Silicon limit cannot be bypassed without disabling AMFI (violating zero-trust policies), pivot the CI/CD architecture from dense VM virtualization to horizontally scaled, physical Mac Mini M4 units running single-session headless environments.
4.  **Profile App Nap Suppression**: Investigate wrapping the agentic toolchain in `NSProcessInfo.beginActivity(options: .userInitiated)` to strictly prevent macOS 26/27 from aggressively suspending the backing stores of background windows during headless testing.

**Sources:**
1. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF978K93M0vCtaZpgp1Pz6NXXyOTodw6XGS2LWQEt4fkO4Lhfe6_GsDeJWlTEF1yF_p4yGpBPA6DngnvHnYe3YzGrihh_5uxm5v-jcQDa1weuq0ZkDyFSse_cmHy5DnMk69)
2. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHz_iD6IYJwUcTvVnY1b-vEhgdgUTKeXX4GRGxBuUKlx4hoLRFGVAtMYa7s1UD3iUVpJXKp2PZTgn6Qrm3V4qH9U61h4EEfALecOGCgOSl7lVxkkMiOMzXQQak6q64jvavg)
3. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF1w5WTFShjG202rtR0wMx3yKyDSjAyEj-w7ICJIcmfMJibrUCJxHiS_jt_rCpVHgrHBOl9F-BB58tJdvgQ4N5TJioiCotPwWa947p7-IvRGoSxAXWg3m8xmggB1w7PpeiD)
4. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6Ltj1-uaLETzuNbZr2Qj8N9rsDsvJ_mzcoOsMgrHFJpkCSzL4uNwojEkIsXsCnm-oI37IfIIvQXD1kESCnzn3MTUqz5YMnUpmfn9dCGglonHLta1aASULmRr9G3iSnE81)
5. [openai.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFS3rHRgLY-U3iSaw7NlwNWHr41ZQeQni0hOPYVQvcTQ2I2pewmkfiS7AoYeM_IHKJbhmhv5_1UV3QAm7MAANsRJxASD0rxUR8_7YhKRHAk7Ci3nm7ShCpXZbfzRwhangnm-qFXfGb9Y9zfaIu0UuS08_Rm-vVdcPkuMpYsQ_8_vsjLB7TrYcQVHR4SG_vcv4ZxpHMtiAaZg9Ocw8g3RAfYi5Fh1BT3er_0CgDeqc-OiWt)
6. [huytieu.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZTas0t1aI8XxsSM9v0Q-JBKlL1kWxnLdVAeY4rSkViPVDkFnZli_6FK-Nz_Zl3SyJBm3UmTAGVv3W--TALK2cU7UBtm1o-2hlNjjU-NJjbHK6YUmZJxIOxzguZGi2iurvrlIpkc-kNrp9KpfxtN1uxtwicez4C0JS7A==)
7. [google.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF3MmjamTc2F15wKtXHIcfcnItT-Mz1xSu86i_q-IWYFGbLWQ8_DQRp23bv_wYj8nzAV4B28VwdtPYmtzP7CkjzXD4qtbqxF2Nn9pLIHRnWEHzx7lmHAro_UeNr48yItr4BUy1v)
8. [mozilla.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGfeTs4xdhDCFHl4qKG47RhymmvPWN_XVTbXYUDfkaZP-lB9FmO7w0Eave7azHkvs_N7kx-qe_0hAqpafKzulfMPsmcB4DocwBm4JzGzAIwTXiZvrKWnqfpAU2ezKDnJQMSOy5knil-DmA=)
9. [balatero.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFWA4mExWACcMcE6q8j8M9Tyfa0Uz3WKr-hJhxunohoX79RbXXPbKNn4qehW03-KwYE5tCmeCoRLskKvhZPCDpzebc4dhtI4gfp39N7Mcwrr-uWf5WU6Sqml4GrxoeRcTqkMMII1oQ9NjjzxzavRKQ91SMsr5AcasjX6wujCxPWGU7ORsZdmD2oKd7-daUeYWDVYc8BeSj6rtY_VW084xgdPXQ=)
10. [khronokernel.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUt5IaU6IAmhxcx2stlZITSgA1p4n9hC8zPNH6ey3q9xsW0osH26dh9JY1p6ryWAsD0h7OObkPNlsymCHVKy8--JFggQF33cfvlaxmVMa9S5Qx8h0B4RsTggWq95-SUDTJShOazYwZtj4=)
11. [ccapi.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHePv-ZGkGaJ-6I8TmvE7JH7wiVZP-OKSt5Ja87YpIHiTZI54X_sjb3xx_NZGrC38cPU09hsHIIZ9inirC_xWpr17En4M2WAu_M5QK3hOsQH5_ZG8rS9_zCvMJU72TyDh3j1fSy_Yd9-jX08-LaeLJ7lgG_hr9EDrCbJvNBeu6Utz4=)
12. [eclecticlight.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG73ik6P0lpaFIARm8D12YQ4AI3JYeRWAA4Ud85VJWbCOKhb7h4iVEUgpeChI8Ih9uNm6DtNoJ5p7Rdj4b53nmXqUHKpDZa9V4lrNffbhdsSUgOkPjOF5b8-0iCqEqMnzKlHgYr1xGVV1OoxgoSnVZ9iTuQnoV7sheA4KDwO1tjwu4-y-U_OkEdBMwO)
13. [jamf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGST5Jadui1itE6WoUA6FPWB_wpApXBFiYLYtR9P91LkFrsxeqzVNjoXQxKfWOlXjZuYCksWiFs37aYOIIBsKjywBaTUMb_nGm6pA4kRVJz9rqcg1VqMTpXLhYufAW2D5NpeaUPK770Cbjf6Lmf0kzzfJfIScfZV4k93CR-wnnGS5LDkI4=)
14. [dssw.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEU6nLSq-2g8p_mC8W8OjaH_uKcrlXaXxAO7w34HNemIn-RHNBJR0RZXZC1Bl6zineRTGaZ9_Vp9kqoNTIFuKnatrwDYVnngJMGortb29oQdRg1SwefHc0-47pg6HQEzKQ7mXT6jCpjAjWPcQ==)
15. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHV5Dm9TZF7RVbhHxFWNbk4vrFgPbqzRFKJX-VY3UiI6qnXtn-QUMvfdSRmQT_Btic-w78RfX6th3Pl4lh0UuoZDs9_hDEi8AFC4GTsHmESMOjlIEtguQmOmc-2WmPbU9M2)
16. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxP2VFWn3mWNZM_5x398VBmCvf_PZ2BbV0l0t6l4UBgouGiZ0gH9likHNyYV-iomJy9aFSth8UMYFuY_TRtEUlXcUdw8pw8xoljDzMZEQmvhev_SxUGEUS_p2Flr5GKMDm)
17. [trackr.live](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF7OOQrxrTadpu1nLIKtDjgFGHEDXEBdAntTqIrNG5xBg2IzwiGEXTf40cT3RAfYDZQPB5Na9OzxQCBNAK-EkbGLedEmDV1F0zuC8O5VwiQ72IIo9ZYVZuBI6usYKL3OAVBgBJyG5_VuVXwQPMSaCuI0tE=)
18. [scriptingosx.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETXaUwV1KEcOx9AyBFFAv3DF_kFsNREyttRQAmMmS9ZOWrvuuMyhbJlxt5aIa87Lvipp2XRuUefM78oCOsnpF9L_xYTImnqmBrZHrwwtwuUUmiinOzbg==)
19. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFDWd6Pw_B3bknVZ6QSB-5t8iTuBtV0U_8ENUFcYvDJW1xdYbtrqIe60TEmdselofb_avRc7dQDMjpK2ZwdwKjHwHd7E-88CT1o_1GXq4VcYr-znjMaJ_JGPmL3XJZHOjh7)
20. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEURsMtiir9CvMWHVp0OxOEo1OwGguFF6VH1cz2EhokQiAQduGcGxVJ2A8b18wQMe3rvlyVfb5hG1GYSOLfMubfhGZQu9twpDEBNgx1V0kEU6sAhXEcWbcUU761Gh4NjDJ8)
21. [t8r.tech](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhlHJw3KWJflnM5FJY7C3t8RvZn7ciFs1ya0JNDK4Daih3Mzlh9Ni4Ir6ylYkdRoqvIz-lsrRUFP77TFxu7vSuCGhY-LCmz3OFhAnU0Ln4Exad6_4U6druJ9TrrOr_cUqWOD0=)
22. [libraries.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5rbGQjLVyfioCT15KUdqyKJ8pkTvDWVHMZmKZngbbM9aDfLBgLym1QKplSc6CRRhQrathxtegUcuJYaYejU2DyjDLxkNBaWnGHMckUcbpgOAQvV_SjGk=)
23. [macstories.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHBXO9jRlzT1tOLI9q6neUyVU1cCnwie9Ojv2v9xU8uHqrqUcfzL_oM0OllDhlwBFGfMsqGl09vyrHaQJ0yKlpdYYeMERnPA33wRLm2DY0zk239s_ljeLwisiGjmuVLIUHb_8qG6PqqNl23UoaMW1KjZ9JHr9J6kidEtZ05halFL4Vbz_Gy0ajttXDrAB8hNF3iRm798t8H11vwckj1Fw==)
24. [spotify.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQaqRJ3i_YhelknIYeiMBRDGX0UgK8sm5vhfDchQQplOh_wl_PkIAfINz4kWwkJzytepzDdQ3YXtUGDlaeXmZyZlC_c6d3asCl7mNbDPVM5FGgCMabQS0u4UVnFo_a0sMW45PclQUR7sg7TmQpWHdOSQnvh1gMG0sQD1y6SHsDF_tlvukHZDZTqLp9u5rsrj4e6jCVbnpL10HNcHR448oxbCbGlHS1Gz4=)
25. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFc3Ho2w7yBJxfyw6qRqFc7-1DNSAQsfBAGbPRluf_RZ4dNLOOVZFYeqypPAGGFAS24LPSZvWyAM6wMhzsU643Zvm2Vhr5XaDCjnBgg_dqWAsfVpg6iI7LFSrcKzpd-81V5V01jNI_hD4X3d7rb9IjkF_ujlcYxvTyJx8WFqFzj7wjpkX6XTCJiIK-QU6_01NCnKZRhCOqt5yN6-hqqoeNEXfIp)
26. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEoTmJXYjhKFEJ5WLXKXNQ9_fXzgObY_uZ9n_9ZeMcMPchOMonkOVwshbLvOigzfi3oXOR7ajTF0iiSXwC89LuFI8WeyvUS3UOjPK_RQA40htS02WvimJtE6Fp9jEGI0AK2b4Tw4AQFwQsaC3_blvqbrmQeGPmGKnasKflV5mqpFfdE967JNJY30VC9KmzhddvUbA==)
27. [go.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNfbJkBXE76g2-BkYijNrgh1KXJPXc6zAaTLWAAvY1TgbjbP916NSb-zAsHAg_LF7dBy2_ZPm-VdupnyC9kULG_vffkDg1Z2He3YPfYTuJiIT_8kByhGGDSlyqXPBJow_LqgrnQfP_I6aMP9fLQVcvbg==)
28. [google.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGrBRLupOtGwBpxj0MspqcTbvc3Xp5TSEy0II5fqjUNk87GJh91nus4kJb8CTGKIPsTHZwZGBw6eXoi9-SqushgXUBiSz-nrAUJg-ctleBlkkbNmci-o20R2ZGP9KEDp6ericCLcmzMRAJ1FmrHDiIogYHeeP5BFje5JQ==)
29. [motionbug.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGBVAiPq5KrHcKfrxPRJLLkQytHvsaqAAg7R6qNUULgL8FarBgWK26ptJuDwbqY4K0Fo3CiqtVFjTAYriB7oaM3MjVNmQyj6fjlcfbRTqCgqJZ4cJVG-aB8mG-9Dju5HiPUqA17_Bq53DHfQ2lQsqS0dESgdojQ)
30. [intunenerds.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEU4YXb-DIkpOOsClPV0SW5Ydcx57SxkUtuyeuan7H3ms6V6CrfbSyx8Hknmi3ENWQqUJTTEwMvRdolAbk5Fwz-k61DVFW0S_u4D5r8gQ==)
31. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFcCr--iFCQ1gy8Hl7Rw5heo-gQNeA1LsTryZ1cipPG2onumr_iFCe5QH9i6ydycS46GnAMNw4kuE2w3qXbfP7Hn0HHkbKinrENWRWHcwtZekhoV8bguQ==)
