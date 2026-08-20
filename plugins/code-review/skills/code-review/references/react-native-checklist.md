# React Native Checklist — Mobile (RN / Expo)

Loads for diffs under the repo's mobile package, plus `*.native.tsx`, React Navigation or Expo
Router files, `app.json` / `app.config.*`, and `metro.config.*`. React component-quality and hook
rules from `frontend-web-checklist.md` §1–3 apply on native too — load both; this file covers only
what differs.

Two facts to take from the Phase 1 profile before applying anything here, because a mobile package
usually gates differently from the web packages beside it: **its own lint, typecheck and test
scripts** (a native package often runs a different linter and a second test runner for component
tests), and **its release path** — a store build, an over-the-air bundle channel, or both. Where an
OTA channel exists, check which fields sit in its update fingerprint: a native build number in the
fingerprint means a bump alone forces a store release rather than an OTA, and a diff that changes it
casually is a release-path finding rather than a code one.

---

## Contents

- [1. Lists & rendering performance](#1-lists--rendering-performance)
- [2. Navigation & screen lifecycle](#2-navigation--screen-lifecycle)
- [3. Platform divergence](#3-platform-divergence)
- [4. Native modules, permissions & config](#4-native-modules-permissions--config)
- [5. Storage, network & offline](#5-storage-network--offline)
- [6. Gestures, animation & UI correctness](#6-gestures-animation--ui-correctness)

---

## 1. Lists & rendering performance

- **`ScrollView` for unbounded data**: mounts every child; anything list-shaped and dynamic needs `FlatList`/`SectionList`/`FlashList`. HIGH when the data source is user content.
- **Broken virtualization**: `FlatList` inside a same-direction `ScrollView`; unstable `keyExtractor`; inline `renderItem` arrow recreating every row on parent render — pair with `memo`ized row components.
- **Anonymous styles/objects per render** in hot lists: inline `style={{...}}` in `renderItem` where `StyleSheet.create` / a memoized object belongs (LOW outside lists, MEDIUM inside).
- **Images**: full-resolution remote images in list rows without resize/caching (repo may use `expo-image`/`FastImage` — cite the repo's pattern); missing dimensions causing layout jumps.

## 2. Navigation & screen lifecycle

- **Screens never unmount by default**: `useEffect` cleanup does not run on `navigate` away (screen stays on the stack). Polling, subscriptions, or intervals started on mount keep running — use `useFocusEffect` / `isFocused` for focus-scoped work. This is the RN-specific bug web reviewers miss most.
- **Params as transport for objects**: non-serializable values (callbacks, class instances, Dates) in navigation params — breaks state persistence and deep links.
- **Deep links unvalidated**: params from a deep link / push notification used without the same validation as any other untrusted input (route auth-adjacent cases to security-checklist).
- **Back-handler leaks**: `BackHandler.addEventListener` without removal; Android hardware back not handled where the screen has unsaved state.

## 3. Platform divergence

- **Single-platform testing assumptions**: shadows (`shadowColor` et al. are iOS-only; Android needs `elevation`), `Platform.select` branches with a missing side, keyboard behavior (`KeyboardAvoidingView` needs different `behavior` per platform).
- **Safe areas**: hardcoded top/bottom padding instead of safe-area insets; new full-screen views ignoring notch/home-indicator.
- **Text input differences**: `keyboardType`, `autoCapitalize`, `textContentType`/`autoComplete` unset on credential or OTP fields (also an autofill/UX-security issue).
- **Touch targets**: pressables below ~44pt without `hitSlop`.

## 4. Native modules, permissions & config

- **Permission flow gaps**: camera/location/notifications used without checking + requesting permission, or without handling the denied path (crash or silent no-op).
- **New native dependency without config-plugin/pod awareness**: a library needing native code added as if it were pure JS (breaks Expo Go / needs a new dev client or prebuild) — flag as needs-info if the build setup isn't visible in the diff.
- **Secrets in app config**: keys in `app.json`/`app.config.*` `extra`, or `EXPO_PUBLIC_`/bundled env vars holding server-side secrets — anything shipped in the JS bundle is extractable from the binary. CRITICAL, route to security-checklist.
- **OTA/versioning hazards**: JS calling a native API added in a newer binary without a runtime-version guard (crashes on older installed binaries).

## 5. Storage, network & offline

- **Sensitive data in AsyncStorage**: tokens, PII, or auth state in plain AsyncStorage where the repo has SecureStore or Keychain available. Where one module owns the token store, a second path that writes a token elsewhere is HIGH on its own — two writers means one of them is missing the clear.
- **A module-level cache holding user-scoped data with no reset on sign-out**: every in-memory cache needs its clear wired into the central sign-out path alongside the query-cache and secure-storage clears, or user A's data survives into user B's session.
- **An authed hook not gated on auth in guest mode**: `enabled: isAuthenticated` on any query hitting a session-scoped endpoint. Without it, guest browsing fires an authed request, takes a 401, and a reactive 401 handler can force-logout a user who never had a token — check that the handler no-ops when no token is stored.
- **No offline/failure path**: fetch-on-mount screens rendering nothing (or crashing) on airplane mode; mutations fired without retry/queue in flows the product treats as offline-capable.
- **Unbounded caches**: image or query caches grown per-session with no eviction on a memory-constrained device.
- **Blocking the JS thread**: JSON-parsing/transforming large payloads synchronously in a render path or gesture handler — jank; move off the interaction path.

## 6. Gestures, animation & UI correctness

- **Animations on the JS thread**: `Animated` without `useNativeDriver: true` (where the props allow it), or setState-per-frame animation where the repo uses Reanimated worklets.
- **Reanimated worklet violations**: worklets capturing non-worklet functions, or reading `.value` during render.
- **Gesture conflicts**: new pan/swipe gestures inside scrollables without `simultaneousHandlers`/`activeOffset` coordination.
- **Keyboard eating the UI**: forms near the bottom without keyboard avoidance; missing `keyboardShouldPersistTaps` on scrollable forms (tap on submit dismisses keyboard instead of submitting).
- **RN a11y**: touchables without `accessibilityRole`/`accessibilityLabel` (icon buttons especially); custom controls without `accessibilityState`; contrast/color-only-meaning rules from frontend-web §4 apply unchanged.
