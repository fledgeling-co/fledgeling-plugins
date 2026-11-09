#!/usr/bin/env node
// Env-key parity (CP §6.8): every app's .env.example lists exactly the keys its
// code reads. A key the code reads that the example omits breaks the next
// deploy; a key the example lists that nothing reads is a dead variable that
// someone will dutifully set forever.
//
// "Read" means `process.env.KEY`, `process.env['KEY']`, a destructure from
// process.env, or a lib/env.ts accessor
// (`requireEnv('KEY')`, `requireSecret('KEY')`, `optionalEnv('KEY', …)`) in the
// app's source. A key a repo script under scripts/ consumes (env-pull.sh reads
// OP_ACCOUNT) may be listed without being read by code.
// Platform-injected keys are exempt.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname } from 'node:path';

const EXEMPT = /^(NODE_ENV|NEXT_RUNTIME|NEXT_PHASE|CI|PORT|HOSTNAME|VERCEL|VERCEL_[A-Z_]+|E2E_[A-Z_]+)$/;
const SOURCE_EXT = new Set(['.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs']);
const SKIP_DIRS = new Set(['node_modules', '.next', 'dist', '.turbo', 'coverage', 'test-results', 'playwright-report', '.vercel']);

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (SOURCE_EXT.has(extname(name))) out.push(p);
  }
  return out;
}

function keysRead(appDir) {
  const keys = new Set();
  const re = /process\.env(?:\.([A-Z][A-Z0-9_]*)|\[['"]([A-Z][A-Z0-9_]*)['"]\])|(?:requireEnv|requireSecret|optionalEnv)\(\s*['"]([A-Z][A-Z0-9_]*)['"]/g;
  for (const file of walk(appDir)) {
    if (/\.(test|spec)\.[cm]?[jt]sx?$/.test(file)) continue; // tests may set any key
    const text = readFileSync(file, 'utf8');
    for (const m of text.matchAll(re)) keys.add(m[1] ?? m[2] ?? m[3]);
    // const { A, B: alias } = process.env
    for (const m of text.matchAll(/\{([^{}]*)\}\s*=\s*process\.env\b/g)) {
      for (const part of (m[1] ?? '').split(',')) {
        const name = part.split(':')[0]?.trim();
        if (name && /^[A-Z][A-Z0-9_]*$/.test(name)) keys.add(name);
      }
    }
  }
  return keys;
}

// Keys a repo shell script consumes from an env file. They justify a listing
// (not dead) but never demand one, since a script may serve only one app.
function keysReadByScripts() {
  const keys = new Set();
  if (!existsSync('scripts')) return keys;
  for (const name of readdirSync('scripts').filter((n) => n.endsWith('.sh'))) {
    for (const m of readFileSync(join('scripts', name), 'utf8').matchAll(/\^([A-Z][A-Z0-9_]+)=/g)) keys.add(m[1]);
  }
  return keys;
}

function keysListed(example) {
  return new Set(
    readFileSync(example, 'utf8')
      .split('\n')
      .map((l) => l.trim())
      .filter((l) => l && !l.startsWith('#') && l.includes('='))
      .map((l) => l.slice(0, l.indexOf('='))),
  );
}

const scriptKeys = keysReadByScripts();
let failed = false;
for (const group of ['apps', 'packages']) {
  if (!existsSync(group)) continue;
  for (const d of readdirSync(group)) {
    const dir = join(group, d);
    const example = join(dir, '.env.example');
    if (!existsSync(example)) continue;
    const read = keysRead(dir);
    const listed = keysListed(example);
    const missing = [...read].filter((k) => !EXEMPT.test(k) && !listed.has(k));
    const dead = [...listed].filter((k) => !read.has(k) && !scriptKeys.has(k));
    if (missing.length) { failed = true; console.error(`${example}: read by code but not listed: ${missing.join(', ')}`); }
    if (dead.length) { failed = true; console.error(`${example}: listed but never read: ${dead.join(', ')}`); }
  }
}
if (failed) process.exit(1);
console.log('env parity: every .env.example matches the keys its app reads');
