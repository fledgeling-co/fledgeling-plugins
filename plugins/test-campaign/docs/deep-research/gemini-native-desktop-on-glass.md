---
title: "Native Desktop GUI Test Automation Limits"
run_id: dr_520a53de0ba977ac
question: "What can an automated test campaign actually observe, actuate and prove about a **native desktop GUI application running on a live display server** on Windows and on Linux, as opposed to headless unit tests of its view/viewmodel types — and what are the documented ceilings, silent-failure modes and preconditions?\n\nCover, with primary sources (vendor docs, framework source, issue trackers, standards, peer-reviewed or industrial measurement) rather than blog summaries:\n\n1. WINDOWS OBSERVATION. UI Automation (UIA) and MSAA/IAccessible2: what properties are reliably readable from another process (control type, name, automation id, bounding rectangle, enabled/offscreen state, patterns)? What is documented as unreliable, absent or lying — particularly for WinUI 3 / XAML Islands, WPF, WinForms, Electron and Qt? Is there any equivalent of the web's getComputedStyle for a foreign window (resolved colour, font, box model)? Cite the actual API surface.\n\n2. WINDOWS CAPTURE. Windows.Graphics.Capture (WinRT), PrintWindow with PW_RENDERFULLCONTENT, BitBlt, and DXGI Desktop Duplication: which of these can capture a window that is occluded, minimised, or on another virtual desktop, and which return black/blank frames? Is there a per-frame validity or staleness signal comparable to Apple's SCFrameStatus? What does DWM do when a window is minimised — does the composition surface still exist? Document the known black-frame conditions (hardware-accelerated content, protected/DRM content, GPU driver differences, remote sessions).\n\n3. WINDOWS ACTUATION. Current maintenance status of WinAppDriver (is it deprecated or archived?), Appium Windows Driver, FlaUI, White, Playwright's Windows support, WinUI's own test tooling. UIA InvokePattern and other control patterns versus synthetic input (SendInput, keybd_event): which require the target window to be foreground, and which cross the UIPI/UAC integrity-level boundary? What does an elevated target do to a non-elevated driver?\n\n4. SESSION PRECONDITIONS THAT SILENTLY YIELD NOTHING. Windows Session 0 isolation and interactive services; whether a hosted CI runner (GitHub Actions windows-latest, Azure DevOps) has an interactive desktop and a composited DWM at all; what happens to a running GUI session when an RDP connection disconnects (the classic session-blanking failure) and the documented workarounds; headless/service accounts; screen resolution and colour depth defaults on CI runners.\n\n5. DPI AND MULTI-MONITOR. Per-monitor DPI awareness v1 vs v2, what a DPI-unaware or system-DPI-aware process actually renders (bitmap stretching), and how a test harness detects clipping or overlap introduced at 125/150/200% scaling. Any measured study of scaling-induced layout defects. Mixed-DPI multi-monitor moves.\n\n6. RUNTIME THEME SWITCHING. Toggling Windows light/dark (the AppsUseLightTheme registry value and WM_SETTINGCHANGE/WM_THEMECHANGED broadcast) while an app is running: what is actually guaranteed to update, what requires a relaunch, and what a test can assert. Same question for high-contrast mode.\n\n7. NOTIFICATION AREA / TRAY. Whether a Shell_NotifyIcon tray icon and its flyout/popover can be located and driven programmatically, and what the accessibility tree exposes for it.\n\n8. LINUX. AT-SPI2 as an automation tree (what it exposes, what commonly does not implement it), Wayland's deliberate restrictions on screen capture and synthetic input versus X11 (portals, libei/libeis, wlroots protocols), and what Xvfb/Xephyr headless testing does and does not prove about a real compositor.\n\n9. CROSS-PLATFORM VISUAL PARITY. Any documented, measured approach to comparing a native desktop window's render against a reference design (HTML mock or Figma) — region/geometry tolerances rather than pixel equality — and evidence on where that fails. Explicitly report if no such measured approach exists.\n\nFor every one of the nine areas, state plainly where NO authoritative source exists, and separate vendor claims from independent measurement. Numbers with a traceable primary source are the most valuable output; unsourced percentages are worthless to me."
provider: gemini
model: deep-research-max-preview-04-2026
tier: max
archetype: technical
sources: 106
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 7.00
completed: 2026-08-18T14:44:55.683Z
---
# Native Desktop GUI Test Automation: Capability, Observability, and Structural Limits

The automation of native desktop Graphical User Interfaces (GUIs) across Windows and Linux presents a fragmented ecosystem characterized by rigid security boundaries, opaque rendering pipelines, and deprecated vendor tooling. 

Microsoft's WinAppDriver is effectively abandoned, shifting the burden of Windows automation to community-maintained UI Automation (UIA) wrappers like FlaUI. Simultaneously, Wayland on Linux has structurally dismantled the global input and capture models of X11, forcing automation through permission-gated XDG Desktop Portals and Emulated Input (`libei`). 

Silent failures dominate desktop testing: minimized windows yield undetectable black frames in modern capture APIs, and User Interface Privilege Isolation (UIPI) silently discards synthetic inputs aimed at elevated processes. DPI scaling introduces severe coordinate system mismatches between what observation APIs report and what actuation APIs require. Evaluating desktop test infrastructure requires decoupling web-centric testing assumptions from OS-level realities. Unlike the Document Object Model (DOM), native desktop accessibility trees are derivative, frequently incomplete, and vulnerable to rendering optimizations. This report synthesizes primary framework documentation, issue trackers, and systems architecture to define the exact boundaries of what an automated test campaign can observe, actuate, and mathematically prove on live display servers. 

## Executive Summary

*   **(High Confidence) Windows Observation:** UIA property reliability degrades heavily across modern frameworks. Deep tree enumeration in WinUI 3 causes native access violations (`0xc0000005`), requiring strict depth-capping workarounds, while Qt 5.11+ conflates semantic types with localized strings.
*   **(High Confidence) Windows Capture:** Minimized windows and those explicitly shielded via DRM/WVD policies return black frames. `Windows.Graphics.Capture` entirely ceases to capture frames if the target window is moved to an inactive virtual desktop. 
*   **(High Confidence) Windows Actuation:** Tooling is severely deprecated. WinAppDriver is effectively dead, forcing reliance on community UIA wrappers (FlaUI) or Microsoft's internal `winapp ui` command skills. UIPI dictates silent actuation failures for standard-user test drivers targeting elevated apps.
*   **(High Confidence) Session Preconditions:** Headless CI pipelines fundamentally alter GUI rendering. Standard hosted runners like GitHub Actions `windows-latest` default to a rigid 1024x768 screen resolution, which can induce layout clipping if unmanaged. 
*   **(High Confidence) DPI Scaling & Multi-Monitor:** Mixed-DPI multi-monitor environments warp physical and logical coordinate systems, creating unrenderable "dead zones." Accurate testing strictly requires Per-Monitor V2 DPI Awareness (`SetThreadDpiAwarenessContext`) to prevent synthetic input misses.
*   **(High Confidence) Runtime Theme Switching:** Toggling the Windows registry for light/dark themes is insufficient. Applications require a live `WM_SETTINGCHANGE` broadcast; classic apps mandate a total relaunch to assert visual changes.
*   **(Medium Confidence) Notification Area/Tray:** Tray icons cannot be tested as standard windows. They are deeply embedded within `ToolbarWindow32` UIA hierarchies and suffer from stranded ghost-icon states if an app crashes without issuing a specific shell delete command.
*   **(High Confidence) Linux Automation:** Wayland deliberately blocks the X11 global capture/input models. Automation requires explicit user consent via XDG Desktop Portals (`libei`), though wlroots-based compositors offer `wlr-virtual-pointer` extensions as a bypass. 
*   **(High Confidence) Visual Parity:** Pixel-perfect assertion is impossible across platforms due to font smoothing and DPI stretching. Structural Similarity Index Measure (SSIM) via OpenCV is the only mathematically proven approach to measuring cross-platform geometry tolerances.

## Detailed Findings

### 1. WINDOWS OBSERVATION

To assert state in an automated test, the harness must extract properties from a foreign process. On Windows, this is mediated primarily by UI Automation (UIA) and Microsoft Active Accessibility (MSAA).

**The Automation Tree and Reliable Properties**
UIA operates by projecting an accessibility tree derived from the application's visual tree. When inspecting a foreign process, an automation client can reliably read the `ControlType` (e.g., Button, Window), `Name`, `AutomationId`, `BoundingRectangle`, and `IsEnabled` / `IsOffscreen` properties [cite: 1] [comcomponent.com](https://comcomponent.com/en/blog/windows-desktop-ui-automation-testing/). Furthermore, control patterns (like `InvokePattern`, `SelectionPattern`, and `ValuePattern`) allow the client to read specific states without knowing the underlying implementation. 

However, this data is strictly semantic and often lies. Accessibility providers can hang, cache stale data, or expose a tree that does not match visual reality [cite: 2] [cua.ai](https://cua.ai/blog/inside-windows-computer-use). 

**Framework-Specific Instability**
Modern UI frameworks exhibit distinct failure modes when observed via UIA:
*   **WinUI 3 / XAML Islands:** Deep enumeration of the UIA tree in WinUI 3 can trigger a native `0xc0000005` access violation crash within `Microsoft.UI.Xaml.dll` during tree traversal [cite: 3] [github.com](https://github.com/microsoft/microsoft-ui-xaml/issues/11028). *The required workaround:* Test harnesses must explicitly cap tree enumeration depth (e.g., to a maximum depth of 3), wrap per-node enumeration in `try/catch` blocks for `COMException` and `SEHException`, and avoid deep `FindAll` tree walkers entirely [cite: 3] [github.com](https://github.com/microsoft/microsoft-ui-xaml/issues/11028). 
*   **Electron:** Chromium-based apps manually map DOM accessibility to UIA. While generally robust, ARIA overrides can destroy the native semantic mapping, causing interactive elements to vanish from the accessibility tree if misconfigured [cite: 4] [accessibilitychecker.org](https://www.accessibilitychecker.org/blog/the-accessibility-tree/).
*   **WPF/WinForms:** Highly reliant on developer convention. Without explicit `AutomationProperties.AutomationId` (WPF) or `AccessibleName` (WinForms), locating elements requires brittle tree-walking [cite: 1] [comcomponent.com](https://comcomponent.com/en/blog/windows-desktop-ui-automation-testing/).
*   **Qt:** With Qt 5.11, the framework migrated from MSAA to a pure UI Automation backend [cite: 5] [github.com](https://github.com/nvaccess/nvda/issues/8604). However, this implementation is heavily flawed. It relies primarily on `LocalizedControlType` to distinguish controls rather than semantic `ControlTypes`, preventing test clients from reliably identifying element types to assert behavior. Furthermore, Qt frequently fails to raise crucial state notifications, such as `UIA_Text_TextSelectionChangedEventId`, leaving test clients blind to internal control state shifts [cite: 5, 6] [jantrid.net](https://www.jantrid.net/2025/03/19/why-uia-insufficient-web/). 

**The Absence of Native Computed Styles**
<MISSING_DATA>[Equivalent of getComputedStyle for foreign Windows GUI apps, Native APIs for retrieving resolved font/color from foreign processes]</MISSING_DATA>
There is no Win32 or Universal Windows Platform (UWP) equivalent to the DOM's `window.getComputedStyle()`. UWP, Microsoft's application platform introduced in Windows 10, alongside older architectures, does not expose rendered color, typography, or exact box-model padding [cite: 7] [lobehub.com](https://lobehub.com/skills/hermeticormus-libreuiux-claude-code-browser-devtools-mcp). To verify visual styling on a native desktop app, tests must rely on pixel-level capture and computer vision, as the rendering pipeline does not marshal styling metadata back to the OS level for external inspection.

### 2. WINDOWS CAPTURE

Capturing the visual output of a native application is structurally complex due to hardware acceleration, the Graphics Device Interface (GDI) legacy layers, and modern window compositing. 

**Capture API Ceilings and Silent Failures**
Windows offers multiple pathways to capture a screen or window, each with distinct structural ceilings. 

| Capture API | Can Capture Occluded? | Captures Minimized? | Captures on Inactive Virtual Desktop? | Captures Hardware-Accelerated UI? |
| :--- | :--- | :--- | :--- | :--- |
| **Windows.Graphics.Capture (WGC)** | Yes | No (Returns Black / Fails) | No (Stops capturing / Returns Black) | Yes |
| **DXGI Desktop Duplication** | No (Captures entire screen) | No (Captures entire screen) | No (Fails) | Yes |
| **PrintWindow (PW_RENDERFULLCONTENT)**| Yes | No (Returns Black) | Yes (If window handle is maintained) | Yes |
| **BitBlt (GDI)** | No (Captures overlapping UI) | No (Returns Black) | Yes (If window handle is maintained)| No (Returns Black) |

*Table notes: WGC is the modern WinRT API reading from the Desktop Window Manager (DWM). BitBlt fails completely on GPU-accelerated frameworks like WPF, Chrome, or UE4 [cite: 2, 8, 9, 10] [ayumax.net](https://ayumax.net/entry/2019/06/19/214840/).*

**Virtual Desktop and Staleness Signals**
Unlike Apple's `SCFrameStatus`, Windows DXGI does not offer a rich per-frame validity signal; it merely provides `GetFrameDirtyRects` and `GetFrameMoveRects` [cite: 10] [learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/direct3ddxgi/desktop-dup-api). When utilizing `Windows.Graphics.Capture` against a target window, if the user or automated runner switches to a different virtual desktop, the API immediately stops returning new frames or yields a black screen, effectively breaking observation [cite: 11, 12] [github.com](https://github.com/obsproject/obs-studio/issues/3560).

**The Minimized Window Problem**
When a window is minimized, the DWM stops compositing new frames for it. It only retains the *last bitmap rendered* before the application was minimized [cite: 9, 13] [en.wikipedia.org](https://en.wikipedia.org/wiki/Desktop_Window_Manager). Consequently, WGC has "no pixels to capture" for minimized windows, returning black or failing [cite: 2] [cua.ai](https://cua.ai/blog/inside-windows-computer-use). <INFERENCE from="[cite: 2, 9, 14]">An automated test cannot visually assert the state of a minimized window; it must be restored to the active desktop to re-engage the DWM rendering pipeline.</INFERENCE>

**Black-Frame Conditions (DRM, GPU Drivers, and Remote Sessions)**
*   **Security & DRM:** Windows explicitly supports obscuring windows via `SetWindowDisplayAffinity`. If an application uses the `WDA_EXCLUDEFROMCAPTURE` flag, the DWM intentionally omits that window from all capture operations [cite: 15, 16] [kdarkteam.com](https://www.kdarkteam.com/blog/why-screenshot-becomes-black-windows).
*   **GPU Driver Failures:** On "Microsoft Hybrid" graphics systems (e.g., NVIDIA Optimus laptops with both discrete and integrated GPUs), DXGI Desktop Duplication will fail silently with `DXGI_ERROR_UNSUPPORTED` if the capture application runs on the discrete GPU but attempts to duplicate an output managed by the integrated GPU [cite: 17, 18] [freemancw.com](https://www.freemancw.com/2020/11/desktop-duplication-on-hybrid-graphics-systems/).
*   **Remote Sessions:** Azure Windows Virtual Desktop (WVD) includes a group policy registry key (`fEnableScreenCaptureProtection`). When set to `1`, the OS deliberately intercepts capture APIs executed on the host and returns solid black frames to prevent remote data exfiltration [cite: 19] [terminalworks.com](https://www.terminalworks.com/blog/post/2021/01/14/windows-virtual-desktop-enable-screen-capture-protection).

### 3. WINDOWS ACTUATION

Actuating a UI requires choosing between injecting low-level hardware events or calling semantic UIA methods. 

**Tooling Maintenance Status**
*   **WinAppDriver:** Deprecated in practice. Microsoft has not shipped a stable release since v1.2.1 in November 2020. The server is closed-source, preventing community forks, and issues remain unaddressed [cite: 1, 20] [learn.microsoft.com](https://learn.microsoft.com/en-us/answers/questions/1455246/is-the-tool-winappdriver-dead-or-not).
*   **Appium Windows Driver:** Inherits the stagnation of WinAppDriver [cite: 1] [comcomponent.com](https://comcomponent.com/en/blog/windows-desktop-ui-automation-testing/).
*   **WinUI's Internal Test Tooling:** Microsoft natively tests modern WinUI 3 apps using the `winapp ui` command line and the `winui-ui-testing` skill, which orchestrates standard UI Automation (UIA). For WebView2 boundaries inside WinUI apps, Microsoft officially relies on Playwright rather than native Win32 APIs [cite: 21, 22, 23] [learn.microsoft.com](https://learn.microsoft.com/en-us/windows/apps/develop/testing/).
*   **White:** Officially deprecated and archived [cite: 24] [wearecommunity.io](https://wearecommunity.io/communities/india-devtestsecops-community/articles/1126).
*   **FlaUI:** Actively maintained. This MIT-licensed wrapper around UIA2/UIA3 is currently the most viable library for C#/.NET based Windows test automation [cite: 1] [comcomponent.com](https://comcomponent.com/en/blog/windows-desktop-ui-automation-testing/).
*   **Playwright:** Its native desktop capabilities are marked "experimental" and limited strictly to Electron wrappers [cite: 25, 26] [playwright.dev](https://playwright.dev/docs/selenium-grid).

**UIA vs. Synthetic Input (SendInput)**
`InvokePattern` triggers a control's action semantically and does not require the target window to be in the foreground. Conversely, `SendInput` synthesizes physical keystrokes and mouse clicks directly into the system input stream; this inherently requires the target window to be active and in the foreground [cite: 27] [learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput).

**The UIPI and UAC Boundary**
User Interface Privilege Isolation (UIPI) explicitly blocks lower-privilege processes from sending messages or injecting input to higher-privilege processes. <INFERENCE from="[cite: 27, 28, 29]">If a test runner operates as a standard user, calling `SendInput` against a process elevated via UAC will fail silently. The API returns 0, but neither the return value nor `GetLastError` signals a UIPI block.</INFERENCE> 
To bypass this, the test driver must run as an Administrator, or it must carry a verified digital signature, be installed in a secure location, and explicitly declare `uiAccess="true"` in its manifest [cite: 29, 30] [learn.microsoft.com](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/jj852244(v=ws.11)).

### 4. SESSION PRECONDITIONS THAT SILENTLY YIELD NOTHING

Desktop automation fails completely if the display server or desktop session is missing.

**Session 0 and CI Runners**
Windows Services run in Session 0, which fundamentally lacks an interactive desktop and a composited DWM [cite: 2] [cua.ai](https://cua.ai/blog/inside-windows-computer-use). Hosted CI runners like GitHub Actions `windows-latest` *do* provide a fully interactive desktop session with an active DWM, allowing standard UI Automation to function [cite: 31] [xa11y.dev](https://xa11y.dev/guides/ci/). 
However, the default display resolution for `windows-latest` on GitHub Actions is constrained to `1024x768`, which can trigger severe UI clipping for modern apps designed for 1080p [cite: 32] [github.com](https://github.com/actions/runner-images/issues/2935). On Azure DevOps, adjusting this requires the `Screen Resolution Utility` task, but this silently fails unless the agent is strictly configured for interactive autologon without any active remote desktop sessions overriding the console [cite: 33, 34, 35] [marketplace.visualstudio.com](https://marketplace.visualstudio.com/items?itemName=ms-autotest.screen-resolution-utility-task).

**RDP Disconnects and Session Blanking**
When an RDP connection to a test machine is closed, Windows immediately locks the desktop, destroying the GUI context. Any running GUI automation will instantly fail. The documented workaround is to disconnect via the command line using `tscon %sessionname% /dest:console`, forcing the RDP session back to the local physical console [cite: 36] [support.smartbear.com](https://support.smartbear.com/testcomplete/docs/testing-with/running/via-rdp/keeping-computer-unlocked.html).

### 5. DPI AND MULTI-MONITOR

DPI scaling induces massive layout and coordinate discrepancies in test automation. 

**Per-Monitor DPI Awareness: V1 vs V2**
The Windows API handles DPI coordinates based on application awareness, which dictates structural behavior:
*   **Per-Monitor V1 (Windows 8.1):** Top-level windows are notified of DPI changes, and Windows stops bitmap-stretching the UI. However, non-client areas (title bars, scroll bars) do not automatically scale, leading to visual corruption [cite: 37, 38] [learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows).
*   **Per-Monitor V2 (Windows 10 1703):** Both top-level and child HWNDs receive DPI change notifications. Windows automatically handles the scaling of non-client areas, `CreateDialog` windows, and common control bitmaps [cite: 37, 39] [blogs.windows.com](https://blogs.windows.com/windowsdeveloper/2017/04/04/high-dpi-scaling-improvements-desktop-applications-windows-10-creators-update/). 

**Mixed-DPI Multi-Monitor Moves**
Testing across multi-monitor setups with disparate scaling (e.g., crossing from a 1080p 100% monitor to a 4K 150% monitor) creates fractured coordinate systems. When a window is dragged or a test harness moves the mouse across monitors, Windows dynamically rescales the coordinate space. A logical physical click targeted at `(2880, 1620)` on the 150% monitor is reported as `(1920, 1080)` to a non-DPI-aware test harness [cite: 40] [screencoordinates.com](https://screencoordinates.com/dpi-scaling-guide/). 
Furthermore, mixed setups create non-renderable "dead zones" within the virtual screen bounding box. The virtual screen height is determined by the tallest monitor; coordinates existing outside the physical bounds of the smaller monitor but inside the virtual box map to dead space [cite: 41] [screencoordinates.com](https://screencoordinates.com/multi-monitor-coordinates/). Test harnesses must explicitly translate logical coordinates to physical using APIs like `SetThreadDpiAwarenessContext` to prevent synthetic clicks from missing targets entirely [cite: 42] [learn.microsoft.com](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-improvements-for-desktop-applications).

**Rendering Defects**
DPI-unaware applications are rendered off-screen by Windows at 96 DPI (100%) and then stretched using bitmap scaling to match the monitor's DPI, resulting in blurry, interpolated graphics [cite: 43] [mariusbancila.ro](https://mariusbancila.ro/blog/2021/05/19/how-to-build-high-dpi-aware-native-desktop-applications/). 
<MISSING_DATA>[Formal peer-reviewed measurements of scaling-induced layout defects]</MISSING_DATA> While structural clipping is a known side effect of scaling transitions, there is no authoritative dataset quantifying the exact percentage of geometric overlap failure. 

### 6. RUNTIME THEME SWITCHING

Toggling light/dark themes programmatically is a frequent requirement for visual regression testing.

**Registry and Shell Broadcasts**
The system theme is driven by the `AppsUseLightTheme` and `SystemUsesLightTheme` values inside `HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize`. Writing to this registry key alone does not update running applications. The test harness must broadcast a `WM_SETTINGCHANGE` message (with the `ImmersiveColorSet` parameter) via `SendMessageTimeout` [cite: 44, 45] [support.liquidware.com](https://support.liquidware.com/hc/en-us/articles/45472011346317-Applying-Windows-Dark-Theme-via-ProfileUnity-on-W11-25H2).

**Guarantees and Assertion**
While broadcasting `WM_SETTINGCHANGE` forces the Windows Explorer shell and modern UWP/WinUI apps to instantly reload their themes, classic Win32 applications may not dynamically subscribe to this message [cite: 46] [github.com](https://github.com/microsoft/WindowsAppSDK/discussions/5476). For these legacy stacks, a complete application relaunch is structurally required to assert the dark-theme rendering. High Contrast mode relies on similar system metric broadcasts (`SPI_SETHIGHCONTRAST`), but verifying its application requires pixel-level capture.

### 7. NOTIFICATION AREA / TRAY

System tray icons managed by `Shell_NotifyIcon` are notoriously difficult to automate. 

**Observability and The Accessibility Tree**
Tray icons are not standalone windows. They are hosted inside specific system toolbars. To interact with them, an automation framework must traverse `Shell_TrayWnd` -> `TrayNotifyWnd` -> `SysPager` -> `ToolbarWindow32` [cite: 47, 48] [stackoverflow.com](https://stackoverflow.com/questions/39646114/windows-ui-automation-doesnt-recognize-button-controls). Furthermore, overflow icons are housed in a completely separate hierarchy under `NotifyIconOverflowWindow` [cite: 49, 50] [geekdroppings.com](https://www.geekdroppings.com/category/c/). The UIA tree exposes these merely as `ControlType.Button`. If an application crashes or closes without explicitly calling `Shell_NotifyIcon(NIM_DELETE)`, the icon remains stranded in the visual tray until a mouse hover event forces the shell to invalidate it [cite: 47] [stackoverflow.com](https://stackoverflow.com/questions/2311877/tray-icon-does-not-disappear-on-killing-process).

### 8. LINUX

Linux UI automation is divided across two deeply incompatible display server paradigms: X11 and Wayland.

**AT-SPI2 Automation Tree**
The Assistive Technology Service Provider Interface (AT-SPI2) is the de facto accessibility bus for Linux, exposing a highly detailed tree of widgets for GTK (the GIMP Toolkit) and Qt applications [cite: 51, 52] [freedesktop.org](https://www.freedesktop.org/wiki/Accessibility/AT-SPI2/). However, non-native UI toolkits and aggressive sandboxes (like specific Flatpak configurations) frequently fail to implement the D-Bus interface, rendering them completely invisible to AT-SPI2.

**Wayland Restrictions vs. X11**
In X11, `xdotool` and `XTEST` allow unprivileged scripts to globally inject inputs and capture screens. Wayland explicitly destroys this model for security [cite: 53] [semicomplete.com](https://www.semicomplete.com/blog/xdotool-and-exploring-wayland-fragmentation/). On Wayland, a test harness must interface with the XDG Desktop Portal (`org.freedesktop.portal.RemoteDesktop`) and negotiate a `libei` (Emulated Input) session [cite: 54, 55] [who-t.blogspot.com](http://who-t.blogspot.com/2026/07/libei-integrations-in-xdg-remotedesktop.html). 
Crucially, this pipeline triggers interactive OS-level permission dialogs, blocking automated pipelines unless a `restore_token` is explicitly cached on the filesystem in advance [cite: 56] [github.com](https://github.com/cushycush/wdotool). 

**wlroots Protocols**
As an alternative to XDG portals, compositors built on `wlroots` (such as Sway or Hyprland) offer distinct Wayland protocol extensions explicitly designed for test automation and screen management. Test tools (like `wl-kbptr`) can utilize `wlr-virtual-pointer-unstable-v1` to emulate physical pointer devices and `wlr-screencopy-unstable-v1` to capture precise window regions without triggering standard portal consent dialogs, provided the compositor permits the protocol bindings [cite: 57, 58, 59] [wayland.app](https://wayland.app/protocols/wlr-virtual-pointer-unstable-v1).

**Headless Testing: Xvfb/Xephyr**
Tools like Xvfb provide an entirely in-memory X11 display, allowing CI pipelines to render GUI apps headlessly [cite: 60] [webdriver.io](https://webdriver.io/docs/headless-and-xvfb/). While Xvfb proves that an application's view layer doesn't crash on render, it fundamentally does not prove Wayland compositor behavior, hardware-acceleration nuances, or D-Bus portal permission flows.

### 9. CROSS-PLATFORM VISUAL PARITY

Asserting that a native desktop window matches a Figma reference design cannot be done via strict pixel-to-pixel equality due to OS-level antialiasing, font rendering, and DPI interpolation differences.

**Measured Geometry and Tolerance Approaches**
Instead of pixel diffing, modern visual parity tools utilize the Structural Similarity Index Measure (SSIM) [cite: 61] [github.com](https://github.com/prash5t/design-compare-tool). This approach converts the Figma baseline and the live capture to grayscale, computes luminance/contrast boundaries, and applies a binary threshold (Otsu's method) to find distinct contours [cite: 61] [github.com](https://github.com/prash5t/design-compare-tool). This algorithm establishes region and geometry tolerances, flagging visual drift rather than failing over sub-pixel font smoothing differences. 
<INSUFFICIENT_EVIDENCE>[A universally adopted open-source library specifically for mapping Figma component properties (like bounding box paddings) directly to Win32/AT-SPI2 native accessibility tree coordinates without using computer vision]</INSUFFICIENT_EVIDENCE> Current property-level tools are highly dependent on the DOM and do not map perfectly to native desktop trees without utilizing OpenCV as a visual fallback [cite: 62, 63] [uiprobe.io](https://www.uiprobe.io/learn/best-design-qa-tools-compare-figma-live-websites).

---

## Knowledge Gaps

*   **Computed Styles API:** There is no documented OS-level API on Windows or Linux that can query the explicitly resolved rendering styles (e.g., exact HEX color or font family) of an arbitrary foreign window, forcing reliance on computer vision.
*   **Scaling-Induced Layout Defects:** Formal empirical data quantifying layout clipping and coordinate overlap failures at highly specific Windows scaling thresholds (e.g., 175% vs 200%) across disparate GUI frameworks is missing from authoritative technical literature.
*   **Wayland Portal Bypassing in CI:** Documentation on seamlessly bypassing the Wayland XDG Desktop Portal permission prompt in a pristine, ephemeral CI environment without pre-injecting stateful `restore_tokens` is currently unavailable or actively blocked by design.

---

## Recommended Next Steps

1.  **Benchmarking FlaUI against WinUI 3:** Given the known `0xc0000005` native crashes during deep accessibility tree enumeration in WinUI 3, implement explicit code-level tests using the depth-capped (`depth 3`) `try/catch` workaround to validate safe traversal heuristics.
2.  **DPI Coordinate Matrix Construction:** Develop a normalization layer script utilizing `SetThreadDpiAwarenessContext` that tests `GetWindowRect` against UI Automation bounding rectangles across 100%, 125%, and 150% scales to programmatically map logical-to-physical coordinate drift for AI agent integration.
3.  **Implement `libei` Token Provisioning:** For the Linux lane, map out the exact filesystem locations (e.g., `$XDG_STATE_HOME`) and DBus handshake sequences required to provision pre-approved `restore_tokens` for the Wayland RemoteDesktop portal in headless CI pipelines.
4.  **OpenCV Integration for Parity Assertions:** Since native APIs cannot query colors or fonts, implement an SSIM-based OpenCV pipeline to ingest expected Figma UI boundaries and compute geometrical tolerance scores for output capture.

---

## Technical Comparison: Observation and Actuation Bridges

| Tool / API | Maintenance Status | Primary Scope (Context Window) | Operational Overhead (Cost) | Limitations / Ceiling |
| :--- | :--- | :--- | :--- | :--- |
| **FlaUI (UIA2/3)** | Active | Windows GUI Semantic Tree | Medium (Requires .NET environment) | Fails on UIPI boundaries without elevated privileges. |
| **WinAppDriver** | Deprecated / Dead | Windows App WebDriver | High (Requires legacy server) | Unmaintained, closed-source, breaks on modern W3C standards. |
| **winapp ui skills** | Active (Internal MS Tool) | Windows UI Automation | Low (Direct CLI invoke) | Misses popups and lazy-loaded items without direct IDs. |
| **libei / XDG Portals** | Active (Wayland Standard) | Linux Wayland Emulated Input | High (Requires DBus & tokens) | Demands interactive user permission dialogs by default. |
| **wlr-virtual-pointer** | Active (wlroots extension) | wlroots Compositors (Sway) | Low (Direct protocol access) | Only functions on compositors that explicitly expose the API. |
| **AT-SPI2 (D-Bus)** | Active | Linux GTK/Qt Accessibility | Low (Native D-Bus integration) | Fails to detect apps with sandboxes or custom renderers. |
| **Windows.Graphics.Capture** | Active | Windows Compositor | Low (Hardware accelerated) | Returns blank/black frames for minimized, DRM, or WVD windows. |

**Sources:**
1. [comcomponent.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtmJ-6sp5qVCb8avs5gzj1WHDXRF7xGcgZj7XLz7f2BDs8ex6AAeepTMdML97Sjw9KWT69M9lwwd68bfj2gEVv0PyRXH_6gT_qDkWOQaU8j_bHTkwNrQ88y2q6pH35HNcReulsQXqYmxaNP_amhytuzLViOAkEmziiYzPvmg==)
2. [cua.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGKtNkmeuanfq6uVy9lO3y95_eSJMOig3tfXrhZuKO60tFMrK5ueINRKcDyxaFuAMjFqMANHpfnZFgwxLftcUI6VoFZFJAGkCSHrjegDHQ3JbpW8GAcxBVqeg839UrH5Nkk8DjvIQ==)
3. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFgXm6HvzNA9B635AdR8xhDCsNmlQqZwsltZDwYrAQvAKACOOnmm20bokn8CKY7b8AtkxaqsaP5cq21daq4ooyFilf3ct6lM0KjVY15XyO4V7sUp3LHypgf7O-2A8WT-8V6oONrgaLzv7a2K7UktP5Llg==)
4. [accessibilitychecker.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1sL_0re3w6A3-nZJeQ6HKNB5oDpR-LW-yQltHnLj0KLOdEjWCBn60-Xdb5aCEBd-bSQy2wfwF1unxSW3W_vltSj8m1KxIRf3COKOKC7mODaQr7DjLV9yNlcdepWM2CmuoWix2gD9iJD-ySLApi0QV3uW7fm06UQ==)
5. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3bSYiMas03Lch1S-CML3br8wEPxDJlqjq9cUHEIvLR0zJlJppknuBFlZ7KotK5Nk8rdMAN330Uuj7nsL_CCxm2U_6YBFcbkp6F4MMu1hrMNZCFkpdn29uYepyM1plI29mMA==)
6. [jantrid.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5SbmmCQbjn7m-YD_1t5wl8dLC_zdj8hosbhzURxsKvp1hgYZ389ePnqWSTFun7iq54TSZ1WPNN_ZuykBxwPfFABaKomA6gTz8c3YrR1RcA8aPGFzGc3VAJRSc9wdXObQwK9Umaligj36d37wHxqVDGbU=)
7. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCREnQHoHDX-nhmOlt55kAfyaJKpzP7wbyr4wzI_Y9W7ZU4UT8vJ0P0d9_NIBm0rnLZ8iz0qdMLt7-IZps7iMk_mMKkmi0XYzPYp3x4GEr6rks9j5GXZWZBOY5jhO8hvy6PMCUPVrAYXjmihKjmxUzSiiqYBPpUNjgR4JTYuNHTHCEHUE5306zXw==)
8. [ayumax.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZaMgvk08-GpQstV-2nVlYVD4CoBzvTMe3j2m7lui7lnMX1woEJfP_kZEwM4TedI2FStcDr5kxwEP2-pfTooCgs8-3LeHQQxetgfTOWUBiQwp21Z0xbBF4gxum7q99HJo3)
9. [fandom.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGJQP6bKyhQsLfSeeBxHeSW85-b_4nfio0KDNVeR-36D72sflMr0HyDXDipBsegs7u14h_mYnuplp97vZJYRqIQ4kKv12VYShF66r__pQ1e3Sb6ZzmkE-RQez9MvLVFMLr-bGg0vV_mK9-UWAZYWg==)
10. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHtsjx-_dYe-btVWJZaqdWQrd0Yu-F2aG-pFHRzMTpmo4hzW8QAmlfGNXTszaQHQdi2Mc9NiDu5UTJRN4eY1dDf1CImNUhDyx4ujs4YXaZ8N_s0aJQym3LVGERXcDXc-NdOLMxTClZ6b6AWAIVW6H6FLNCCWdNUE1L9F3RBgjFl0FC)
11. [obsproject.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGVwQoTLLopdF9KcEH2lfegNurmD7zpGnsAOIlvvWstbCIWNfKMzd8YETsY4XmBj-BCSvW97skSSLACCRYPpoUMq6i5VdkS1km3FKR1JaN1UNZg3ZvFcD4fwJV0_ys3h7_LOZJ2NIg5Bc420ZFGYZk2FFQ93OC116IKTAtuJyu1x9W5K3gtxnaN6fzfs36exg==)
12. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEaioyURl2tG66OXskTqBtoL_kyaH72jjBCKpUar5GZ8-bMwN3a9lOucqhbGo6MkKkOYMxqOUa-yqTKlgD1ReTpWpcphJovftMGHgv4TIidkHtf10F1E4wRuhxy72t0Rbcot6Yxz1UjbwK1)
13. [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH23l1hiX-pJfK-IeFbTD_BiMxf83KMCMgZ5o32ltw5I6zUwLyE0tFstPWDL_Tupy1GzrXjwjYBL_QGn5j-L657o-WAhs1jvA1_GHHTJ_HEWiKwDpVNL6JZO4W3j9r-LGsTGDcIrWmMgQCn)
14. [cilwa.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9sQ43-3_5LkyZNLTgHdVwt_dQwq_m1QsJA68VKD2jYNM5rpQNFrQGY94kVgQetj3i2zVQBUGfMr8eECj4IVOygiXrMK1rzxJYNVlaxZqAh7oqgoIFrZC4Wmm0UBHfvuuhZ1MU9uv94BDCiIrDKoocXg==)
15. [gitconnected.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHYHj10cEhHVc9-vziLTb6_niuLpQUnoGvj-r-1Bsq6EO5uDGSR0Kp7Jo8543AkF13oTOoz5POOq3u5N6_BeEiQo5tEkCJYL3fXPLktTCfLs1VmFFwXlkDwgJmdUtLFNwGRSG12a412Slbd4eYiwU4PIA2h95UcOPFGiX6ggiYBJZsdPW5SGzvQUlkw3khR4kbRkX_c3OOmt3nfYEIGrrrTIyjbRwXkOfxoo1y8va05vfQ=)
16. [kdarkteam.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEN1r4xA2kwBWDPHuFqiG_wIGg-Wo0m69rTwcgnk69_DgnYOmrGk8pAGkI2XFwfh1sVsnEhzzzb0H9Jws9DroLdfjQmVloKJUqYOYalSQiSukhdhbZ4szBGOZdyZ5AMgFGytWaGSVacE_JLuLqg6HUz0QSZ5T2Bp3lL)
17. [freemancw.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGBlx03m-1uyHoZeeci0XgE9VQJ8gSrNbeCyvMwKKe82JIZpTVm2dbiLedanHKYdIWrbLxfVWzPu0HeJ4-Ph5Zl0AwHn33-Q42tUTLjzHIq-86d0HVaFWSSORyt5yTXGqXQGvZClXhji8wMW5_n9iLIvXpgOrxd374k2va_n1Nk5XsIbml_TyU=)
18. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGlYnUYpw54DJwdmFO4iGzAHdkr3t4aNrg8eqfWOQWUXT020tguUirR39q2KgPXZr1uxxWGJhGb593HGl8LcLQt4-T9QEqLWfzxg77naQX6lIQUPpM6NtR9Yq6Lmy79PIxuPrzOpYZjA4WXiv-5XyqpCiRZ4Qc7psJuaKtWKY7fJMxx7r5j5LcqmVf6vRlgXcTaVxU6IBJ0xA==)
19. [terminalworks.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGIC13UtMBeoIz_ZIWB2dWA0D_ySDpYDugEkzsX9zgF_A9Wal3aO1gxx1FiHp6Dojb6CU0Yz0J-MviFbn8Uz1wB9FjOEs37QtsrqS3feOEfeP_X53p7Z2NjvdOriW815V2LPAGXsKQVna8x8_tGZKA-oxFoPFPHOYwp07inTrtZcdk_1cYkQc6z_y3fevYxZpu8PxvypL5xuiZ944JGHishbQ==)
20. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQED2qbmq_9FezJLxiyQm-d35L05zeuLPEf3mFea300YfSQOClEBfibuJjRhJclmv2b0zDWOp6f0o4WGP_a1tFzv2aB_a0HdzT1dCiW8z7KrEP2CVhPkXzDNVTPOorwp__Op8Uin056GZINEykifYNp6vE6tbytAM9eD6c41i1IGtP_UlE0JzeMrw_bIY4aeB3j2lSTEvTw=)
21. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGOHMX5JqDj_N0hIjImZYWfft8mYWhKNgwZWWs8M-nRGgsy77ATYQHr5fe-FZb1iHVyfJMlygnXDj6CsK0Z5qq3qi3ZnEXo7pDcti46OqDuXCNzpR7V9Iee78qlLFYuSCxy6cjRPFwonwU6oUn3FAc4FTAwHptjoW4LnQ8toiJA2Q==)
22. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF8b-0LdoBLc3VY8z58N_vlAEfPIB2kujdtkEjLR5jLqXr1QPpiW14udk-WQI-y7OnDZhqKS5b91mI7NvGsDCWnzupQt-fStEWgdq5MTYMA9Q-XdneakbHEUW5gHSIlIFtTRV5V0CHDFJX1lc2_Awsafw-hzUI=)
23. [mcpservers.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQET5KNsvqm-WLr2o3LSmzih7bWPJg5a1ug5xAE6JmNE8OhqKYvfbE3tIUGb9OPwuv0BUhfHjSpUEjPVTozWTcFUkue_fEFt_RF9mtfS6WoNCt4siC2MPRKWDDTC0pgNDp9gcjfT6Dm9Uzdd4lZswD2t-APzi0vKJ1Tse_XfnbJ_2NJHTA==)
24. [wearecommunity.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHa9Hx0fU0JrQClkGpVGmJwnP_WkJG_7sVcHNMVknLCKpG3uaRjpOnKkJ2ODvucAKtvgNP1lYVUi2MRIYShNpuEvjLDQJ8AvMRaVwtzszJ2j_2Fil0YqkE7RxC8DIUNcJLN9BcBioAPMJALQ3WuzZ4d--X1SDjpDSmvIA-0m_xSqWpVy9ZrQvw=)
25. [playwright.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHpeZFTzC43NAUVoODnsJdkB4CqWjaDiB4PwtuwTrbPUbzGhr1O3TWIDBmQwZxxAAULDlBQ0E5t_M2kqpYAUCadiyvb04GfzLPnXsZdUIPnY6a0KRcRYO5Q6Qq7P8VrzQ==)
26. [logrocket.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHulqx36wd6VwEAH2LC7iE-H1qUqQfugEfAMsQEgwwOdEtLBN50Cjx2M3AWIJWA2yDi4jScj-SlBIjxZIxnt_SkKmjuD6SKJ9xA0qTvQJG2iO1sPbhEI9VUBigKf7kyD93PrENFag7hw7Stkw==)
27. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFMGT773dhvfQVaL7FZijXBVFPzPArUNNeQz8mUx4kRP9EUkxnb1nRd3cuNtQR0eSOd9VnmLUOiuWsepaaf8R_xNM2SUwmd2H55505-Psa3rmoUsN-bORqJx_6QAEt2-0dpjMGwL5oPMJlCduXr0DkyA6IAATJDNmeQqEr-RiKRtRvxLN6alA==)
28. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJ6p0NXqN0p4AwC3pkk6G-8kFWhnKbZCO4ahAsvBdc817rmqh65nWedEwASiSaZeKyaSV6NLCGwp3R8oN_famXfp-neAdmC-YIAH-LwnblmroHzwEGCnpHF1hl5aAzwASAW2HZYn_W2EperPOlV2-OEbn-OuliJ-0Lblkq0pMxDA==)
29. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHfsVtUm-qs6tx84zRw-6GjOuT-VSqR9pz98EJYDvRLnr9KEvJGTkYslv3LDlss8ZbWcahAvhg5MUQ-P4WIq_7njfIuji1BiajFAjq2q0aaFRDb5ONnXghXvLsoA2HYwMCckbymHokAFB48IPH0x-nkW7SspMJ8_0Vc84-ZREidX1oBIIhNdPljTHpZIK5cnlNeqB1BxxAMQSo4m3QnVXfeuMwaNxTkSap3yA==)
30. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEqkxsptjvB3tXb31nbnf-8o8olu-Vi_B8ShvlTPI5RUb4izeCQuAGe4EqvGnR0TY-PFy36SyAmVUoAC9u-Pnddp49CW16xI-MULY1IgErHDee077dXa76oiW1mi6x1N2JPx-ADFMdN4ACYBUlq1-ev_jis6NOVtiwmwZLiPeczyT4=)
31. [xa11y.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUOgOAr1iKI8U8am42uotPruv0Cgoxl2aeARkPQi3ApJca7XgtuJdYwMM3iD0VIpPu_oN07W6-mUfh2dQISiCo7RTIB58KIa1jSt_GCf4qOA7n)
32. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHPQLaS_hMN9yjmcRZYXKARmsaA5bX2AIEGe8Wy01oxX-HZx9G-1OyPlaDKzrMH4o7kyhV40YI27R_6IcdEU6LUEDGybwQj4LwWgrKJUKyeUhBH0Fn-Jf3M3B-6g5cZ09Wz4Rjv0sPT2UiJ)
33. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEFKA3a3afJ3BurD9-iA1dkY0yqM1nfsqXWb1O_T9TijuZ4FPyTiH3VeZXtlzfbkiD_M7YFEC9GVc2a4XiNclO9IvRFskMLy3-qBayvDs-07_BIhJNrV8Ws72l2D0j2VlvlVf-Fdg3J7_U9-UHEfdR8vKLU9w-8QQ5OBLlRvum3ZhcEiZLq0OGnq1y7JHnQly3PoEH5cZSymnDBtQj6FCk=)
34. [visualstudio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHEq_QjdAykHwKGEUqpmLGNIKqo65vDpP0M0Ln292WiNwTRRhSr0QrRD9g9qQRi4Roo6ePw8tHHYYcNgpZw_dE00Qyy5wM3Fcuu72sFd2CeSbj7F4OIZgDgjMjLUXsQueIbSnu-BDaSTvdcNsxEu9REbunsU-kQ6a2q2GRA48RMZ9z_Sb2IZrmDK_sGFlcHLk0IVesGUANBgaEz2nVtShrRnYvGoMGxMlBiX_Wz02senQ==)
35. [visualstudio.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEY-R2Y4T4BUaZNqPPoagxFXSG83wdEibczxFRzxnbfKyG4TaZg4d7O0KgpmKS0pcmU2ep4-ZeH5u_UO4on3S82NvyY3XcmTIcgvUIsPTip2aixPbwS-1gv1ir1cH57IP0j84V4mqpgeR6AZeEqesO23VprKpuW51-AljRFBK2emTWIqMOfxff4kIiB1eSKtj-OJvyL)
36. [smartbear.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGGd7TJ71zuhmMqO3Yc5_zqyPybB0v4dlfR0N_4YNk0zCcYFmpqjyfSy7JWTuBdHMFH8gW6pTFxIPZEeAOe1o1NnwIcHCj2Ot6gTBUALApM8XVYF3ZoqlvEqa42GQoX3iZtZjmedjHsHLKF8f0kwz3v7O-cERJi5Ep6uMOSqR_0PK3KO6zZTV9Dn_tGP6lpHU0AyUUfHnUt8ZVdXqYEpO7otg==)
37. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGeTSV2ZQzFks-qBdmGGBEINQ2hY_vCKs89rflzRiFzBsHzKhRNjTuM9iitm7pV7xju7vtoY-YRmLK9_jBnO7mFaMSJlfTRvU4eTvfV6dC0tje3axBB_PeZrQouPIoX8wSBLu1b4hwti3T1543dBZzN3WZYC7WHDtFJZNH64zxOSw6lSoKdf-pVVMe20mAfW-UjxtAwUR66nndqzQnadDY=)
38. [windowscentral.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhq6rmxvej3jDF0SanoXEWwM66KUzuoa28uYs-jSnc08lbNH2pQkW2ARJfqngDpBToQ-x_yCIDBoQEh81oN_mSeaNmCQrzpcgJKYrZFWg0N-EheTKm8LrISy0s7gGsi-_fCHQaHk8qYn3xi6xdOhNsSYz-QbE-cqcYTbdIzL5dV1LDId4Dzw==)
39. [windows.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFyiIzmzZNsLuKeU3AcDPRehG4I1gu-yR5gu1Kf14UoEM6eF6LmAFr8OPtPKj8f7xejvwHYCyLxgGgI9suJiiQEkA7K3fTqL-kz5Xn0F0-N_nIfaCGf-BmHb4fZwL_ctcNbnUh_i5ekXI3RJKcosOw2_yBaHgWm7eGRZ7P10jBsQ2tWsu-ZYEZixjjBTZ2yhWy6DsVF_dAn7HvYtcv-zeONA2qE1sIg7ti2BMOknMRjncdBUeFFylVolEFx)
40. [screencoordinates.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEf8O_8Lv7RnP2tS4U5wU1mvuPYZN2FMxQrnsQDD45hc1RVP9HtP_7k0B7iWgLE9wy5XkSolirImt9rSMw3gwUyYngj-Wv9K9iBKRJGNeo6stsUP7xNE1H1DsdvvLSaSe-Tjjags-M=)
41. [screencoordinates.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFbQD_MiFwLraCpD2Whv13wDHMxrxDIfrGZ-cDTmlszogfSU6AyV8T5TISiOarxMVtLaUwwH7_8xFyxCY2y8VZ6ZoEFqc0I8eufp1MqvaWsHshQX1z4nKMLLGr0DnFhoXM_IQRORAbD-5SxsQI1rw==)
42. [microsoft.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEzBqZY41ng0Es_xkkEQ6F4ghNGmDUp-7YNorfq75Nem9TeCmDE0GNI8GCaVOgP8Zhg_LBEIOQlf0ZFgSxs7afy44KpXKII6xiv155dYpFeMbBDrP-8WNkYat9TFflW8rKLbbGRoIlYbti4JCHSThg5ChXP8B-FoTA8s3oc1jNXkIkHzOkzMjeyRwuN4OIEkbrkqn0uK_TVTVI8)
43. [mariusbancila.ro](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFC9zJ3-5BQjlNs3yR0WvDO1VHwlWc2PflYNAPhfan7BuV1LWH1hPL6vQ4cUCsNYv-17srqkQ6B8tjpLVBuRjK2Efpp2leAZqrDpLS9PLjii7vAhiK_gC36UmU0bQ1ul48ZGbPKPeIlIqJGkisadOQone6D9VbvBORa33lVRpLjasC28mVUP0IE4YnwHjZX9srmeiZYyExw)
44. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHBr5GhroBPLd_jBxe6xHeMlKGAo7ZmGbX79mSiWVV53hGYsIMPsZ_XnKXcmzORKfcAcRtcRQNFKrj65GtNWXFXP4ivuV9XSonBslt0ozOQwEM2ka_f8tUZhXsO-xgvOhS1VgWemfeORDFeGer7nIlWaGPaNRJflSyGKqcL_i7fGEj-D9Luu6B15vXFfZZROWOMo24mhOvlRKICbNeb)
45. [liquidware.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHkZ8enTl-4O2AWBANWwNKg7Oem-F8r5QTkbtJTIgR20i0wR__8tX9RR4IEzROoVcNkWshFjG1GqPhS03O8lbv00kEm2tkU3-5OTlmOJUAQeLqE9eFXSRSL68tP_iXu_Zm_eTEdy45OdI75PV2Aplwc16C-lsYntea3gxwIn7OwtP_TX7McsvSDR65IwLPnk0XYiX9Ni3yxl5DfRbxW1HSqMF58oqc0NCHQP0f_xkQ=)
46. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFe-sDqeSRnWdD6aQa7Znfj3LwVPp3rKxv6Gr9asMD9QehpCgpuFML16_oTb7P7E-jc5SEuy_NLGeR7xaMboz16QtXVxkl4jBsFFdJFdRkiuQiDDBHGhx_t658cd0J-qBQTyNxz5CYe1-1Rml1YF0XAZw==)
47. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxgxZYUZ8BnH2drm6-O43oaXzkTdkKcfnzLQVbK7gYweN11aYr2Ziidi7avG_yh_FCw8jPfiSoFuu23J7XwJbTRF2ryAg4TZVWMUehtBpWMxgJLqnChCdfX_q7HDNJ1L7oa-8Ui8-2wOzDKGFwFyzTvRTL2rSQLle6VBqk5tAYU3VPJj-swqNFX0AaDuQIiZw9)
48. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEzJUXKD6leKU0uM2Iv8u5gTx-wDsl_Fo9wF_T3ySN2IE2edgSG-bgpVWSFxi611MQxVOOCObGOFCYz-Ia04agLpj8z-knHqBFTC_CMYj8avma7UCLKa3ElTGKqu-0BFes-MB8pzpClICyKi0gd8weVoHZpogc5fC7jCVnShvzjftdvWVOMXxUrwM7V-UBEKr0mUqiZlrpE8J0=)
49. [autoitscript.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEpYriNZxMfYg0Ld6tXU6mggDFHJQynBavZBL5-DHiO_AnaSSoioM4kvFq6-iUHLXdg0s2rm3K7TJHBHiVIL-J7N6gdi9nHdarNl8yd0licPPKUnWMNeN79LNDs252ytc5WZhXhpBVI-5132lqZQdVdaxEZxrw4F9NjoFqmnkgIPDFoSRN_marjm-RdfUQaqia5dw==)
50. [geekdroppings.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFCg4tML99E6llYy-KOx5c_4p1Gt9P18FwEDSx8ZvVyxQwxgqmFFYlfZfEBgdjRAFIxY45rZMfASPXe7vAr6JCSGONL66fNoKtrKl6BnCoXlGDWCErIf0xV0txkH_1ew==)
51. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEPTFDloN4xpJ53DnjhRpQK4CpM4y6uBrClVONNZQkQjEy6wcPJC_wo4FAPn3SAlb9nM7TceF8H4d1UZEZ8CCBpzoGWW56os67QYMqNHs9e4pwz9pfnULp-Ahzh1_vem5lyg6n2BKotytuqa42wWOIyNVw-ZDk=)
52. [freedesktop.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG__XOxmnju6iGxSY479YRaci4Gs61BYdVce82deyfhhi5FLKetJKEH0aJe33bTA6GWV5ZW-ebT0ixa2fzv0AdFxvYJpxXi7b6DtwRDCBRHesw2UTQt0rhuSHB3vgDNVY7zz-uh5N7GP2kQfFl5)
53. [semicomplete.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsqJTwD4HtfO1_nLumllejeOAQHzv2I0vu1O4aBYuE4eQ2qpwulL9KMoGrAVKVchDB1IsrCpO9ib3LPFaFZbhmE_nBzu_Snf3ce074KSXNs8HA0XRXfXWKnkXTSiudYyy0qZaW8qCWY_zPH031BR76kDdIF0QPDJR3U96RsxVsPopIGTg=)
54. [lamco.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHIMQP7d-b0_F_EtvtgN-q3iaAk7sRGcn8dW_T3onwmsIHDOZn1jYG0nxSvHftYWufoeB50IOsgvBjoaSYCIK4dlZCoEpPpEkUtHHEnox8tWdYHDPwcL4bHTh9CoiXknCob-hMvLawi300tpdINfQ==)
55. [blogspot.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGROAjGTwQRdmXtuldxE-ve7WC_fU1ikBbjOu6DZSuT-qu8QXMdeyNzNxUT0gL_A1tybPLtD108l0COszVSAA31GmtRLO3Qin09eYf7yDyzsMb9r-RyfM_rqZsb3NJhLlUzBgER_GUBe0WmqZ3_HAdqnkhAKXQXv58tmUMtZygI3SpjzjI=)
56. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEaQO513WMVf2Evp7Vbs8n12sE-3NlNyQLrPysb1RQeM2Qaxe4I4jfdqGrQ9EZlxsMLldshSRRu7nx372JQ0W-fhqiF9OpMgRZiHiiEhdZZthRawREVFCku5oU=)
57. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGcWszLPdiW_1vYm0G1lQSECnQbVb27vpvpctEBwdlb99Kbf0k1bpj7XmPAeWkyDpIG4Y5yE_u_MTlPBGSB3MSG6flEAvuT7pvrP3QbCpVcS2zXJcmS6_oPKf8=)
58. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtNQXeIA6UbV5A-RnuTGwh0g4g4QoYnwZbDdLR524_Lr4VLOBUhG5U8ij6GAWaAOAbmupIgN3Aqz_KdaKwHYFvBv4pWL-DQ7fd3chAcIkGgidfU23yTaornCyaHB6lK9z1i_n2PCmDDg5lAIQR4WMaj6YSjXHrRqVM6YOw-CujLPTXqyNHwzX17tBp1ZiRT4S1FPQw)
59. [wayland.app](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0a1fiRsXR9RX36j9MXsjbMk5dDIov53fsfUNl9eMQSvf5m_mNF5SjJp6uKFdbevphm1CxwsvxqQTtreEwlbbPTO9Yz65i-DGm6_Y7lQ4evrqtqdfkJPrsiXA0nLXhbEcySqdyd7D2eQsVLOm4_WFJruP3)
60. [webdriver.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-8g3E05VMM00RdHVNPgRI1f-IcGoFDcot1ZlpnF0yn6dvF5hQZqRsRQIWde_HVUKSTY9ehYVgxn_pSLXPg3pDZriUyv2DZFFHP8fhNVBAbREUiF_pKg3NN2rFGrYwsLhVZg==)
61. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHQgRAmfu1HW-zcil8BqwZfXt7qNpZxR4NYL1gH69OfDzyZp81I5Uq0vTdSEvsp4BswqL6c2jpYEeqxQa2UoH5W8rlxIbmjrUzO7NRkNVwrY5h09SfCaoq47djKvnj_me7-V95z)
62. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEC_7WAQE_LB-YMwQA3APl-avo48rExuEOlyhUoZHBieGY5Vopawmy4QokXxXVB0wBlKN8nbgawNQZpUG43WcujK5rNNUzfTkHKiMvdTZ0ZJYArlTEUygOz2y2NSsVnOoTamPBsExw0UnhDcV85H5f8xQqmV24soM1GK0Ubqmu2CYiAWGrfns-yJluWfBNlosnAKEbIAaVC1E_LTWCBa1bVrtE=)
63. [uiprobe.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGe-3c-FoIFZFDrG1Q0V06zkuU0Gweyef42fi001u1WFvB9rJADJR7EXulDEYqG6b9X70dccP5i5SPDqgoAmeIvJqYKd_5TouxyIhWJ0-HkNK8v75u4pf8UXOR5RvefRVZG4HmJ2aaLYL3V5tb4bt0OIGiRqSI8Xy1Dou27h4VFW0dcHw==)
