#!/usr/bin/env node
/**
 * Fails when the app has lost its iOS scene life cycle, which an iOS 27 SDK build needs to launch.
 *
 *   node scripts/check-scene-lifecycle.mjs        exit 0 ok, 1 regression, with the reason on stderr
 *
 * Built with the iOS 27 SDK, an app with no scene delegate is stopped at launch
 * (_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption). Expo SDK 58 prebuild adopts
 * scenes itself. On SDK 57 the opt-in is expo-build-properties' ios.enableSceneSupport, which needs
 * expo 57.0.23 or later. When ios/ exists this also reads what prebuild generated, because a
 * manifest without the AppDelegate change launches to a black screen: the old window is never
 * attached to the scene.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The app root is this script's parent directory, so it works from any working directory.
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const problems = [];
const read = p => readFileSync(join(root, p), 'utf8');
const readIf = p => (existsSync(join(root, p)) ? read(p) : null);

let expo = null;
try {
  expo = JSON.parse(read('node_modules/expo/package.json')).version;
} catch {
  try {
    expo = (JSON.parse(read('package.json')).dependencies ?? {}).expo?.replace(/^[^\d]*/, '') ?? null;
  } catch {}
}
const [major = 0, minor = 0, patch = 0] = (expo ?? '').split('.').map(n => parseInt(n, 10) || 0);

if (!expo) {
  problems.push('could not read the expo version from node_modules or package.json');
} else if (major < 58) {
  const plugins = JSON.parse(read('app.json')).expo?.plugins ?? [];
  const entry = plugins.find(p => Array.isArray(p) && p[0] === 'expo-build-properties');
  if (!entry?.[1]?.ios?.enableSceneSupport) {
    problems.push('app.json: expo-build-properties is missing { "ios": { "enableSceneSupport": true } }');
  }
  const pkg = JSON.parse(read('package.json'));
  if (!pkg.dependencies?.['expo-build-properties'] && !pkg.devDependencies?.['expo-build-properties']) {
    problems.push('package.json: expo-build-properties is not a dependency (npx expo install expo-build-properties)');
  }
  if (major < 57 || (major === 57 && minor === 0 && patch < 23)) {
    problems.push(`expo ${expo}: scene support needs expo 57.0.23 or later (or SDK 58)`);
  }
}

if (existsSync(join(root, 'ios'))) {
  const target = readdirSync(join(root, 'ios')).find(d => existsSync(join(root, 'ios', d, 'AppDelegate.swift')));
  if (!target) {
    problems.push('ios/: no AppDelegate.swift found');
  } else {
    const plist = readIf(join('ios', target, 'Info.plist')) ?? '';
    const delegate = read(join('ios', target, 'AppDelegate.swift'));
    if (!plist.includes('UIApplicationSceneManifest')) problems.push(`ios/${target}/Info.plist: no UIApplicationSceneManifest`);
    else if (!/UISceneDelegateClassName<\/key>\s*<string>[^<]+<\/string>/.test(plist)) {
      problems.push(`ios/${target}/Info.plist: the scene manifest names no UISceneDelegateClassName`);
    }
    if (/UIWindow\(frame:/.test(delegate)) {
      problems.push(`ios/${target}/AppDelegate.swift still creates its own window (black screen under a scene); re-run expo prebuild --clean`);
    }
    if (!delegate.includes('ExpoReactNativeFactoryProvider')) {
      problems.push(`ios/${target}/AppDelegate.swift does not conform to ExpoReactNativeFactoryProvider`);
    }
  }
}

if (problems.length) {
  for (const p of problems) console.error(`scene life cycle: ${p}`);
  process.exit(1);
}
console.log('scene life cycle: ok');
