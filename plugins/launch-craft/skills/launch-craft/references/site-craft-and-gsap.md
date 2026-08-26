# Site Craft, GSAP & Three.js Architecture

This guide defines the standards for crafting high-fidelity, interactive marketing sites with GSAP animations, Three.js 3D hero telemetry, interactive mock UI slices, and 5-platform support badges.

---

## 1. Design & Typography Foundation

In accordance with `/design-craft` and `/ux-craft`:
- **Dark-First Telemetry Ground**: Ground background `#0a0b0e` / `#111318`, elevated card surface `#181b22`, subtle 1px border `#262a36`.
- **Accent Hierarchy**:
  - Primary Warm Accent: `#ff5722` (Ember) / `#e64a19` (Vermilion) for live telemetry alerts, ping spikes, and active CTA buttons.
  - Secondary Signal Colors: `#00e676` (Green / Low Latency), `#00b0ff` (Cyan / Network Packets), `#ffd600` (Amber / Warning).
- **Typography Stack**:
  - Display / Headings: `Geist`, `Space Grotesk`, or `Syne`.
  - Body: `Inter` or `Geist Sans`.
  - Telemetry / Code / Stats: `JetBrains Mono` or `Fira Code`.

---

## 2. Interactive Three.js Hero Canvas

Embed a lightweight, self-contained Three.js particle node mesh in the hero section:
- Dynamic 3D network topology node constellation that rotates smoothly and responds to mouse coordinates.
- Interactive pulsing packets traversing edges between server nodes and client devices.
- Handles `resize` events with clean aspect ratio calculation and caps `devicePixelRatio` at `min(window.devicePixelRatio, 2)`.
- Cleanup on unmount / visibilitychange to ensure 0% CPU consumption when out of view.

---

## 3. GSAP Motion Choreography

Load GSAP and ScrollTrigger via CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

Key Timelines:
1. **Hero Entry Timeline**: Three.js canvas fade-in, headline stagger-up, live latency counter animation (e.g. counting down from `42ms` to `0.8ms`).
2. **Feature Slices Reveal**: ScrollTrigger pins each slice and cross-fades the interactive controls.
3. **Reduced Motion**: Full fallback via `@media (prefers-reduced-motion: reduce)` disabling transform tweens.

---

## 4. Interactive Mock UI Slices

Include at least 3 live, functional interactive mock widgets in the site:

1. **Live Network Telemetry & Packet Filter Slice**:
   - Interactive protocol filter buttons (TCP / UDP / DNS / QUIC).
   - Live stream of synthetic packet rows updating with realistic latency and byte counts.
   - Interactive slider adjusting simulated bufferbloat.

2. **Dual-Model Pricing & ROI Calculator**:
   - Interactive toggle: `Self-Hosted / BYOK ($9.99)` vs `Managed Cloud ($4.99/mo)`.
   - Dynamic feature comparison matrix highlighting storage, relay tunnels, AI key integration, and backup retention.

3. **5-Platform Native Client Explorer**:
   - Tab switcher for **Windows**, **macOS**, **iPadOS**, **iOS**, and **Linux**.
   - Displays native OS mock frame with platform-specific shortcuts, system tray telemetry, and install commands (`winget`, `brew`, App Store, `apt/flatpak`).

---

## 5. 5-Platform Badges

Every launch site must display explicit, accessible platform badges:
- **Windows**: Windows 10/11 (x64, ARM64)
- **macOS**: Universal Binary (Apple Silicon & Intel), macOS 13+
- **iPadOS**: iPadOS 16+, Apple Pencil & Split View support
- **iOS**: iOS 16+, Lock Screen telemetry widgets
- **Linux**: AppImage, Flatpak, `.deb`, `.rpm`, AUR
