#!/usr/bin/env node
// The quality gate (BP §19). One script for both entry points:
//   pnpm gate                       → node scripts/gate.mjs --all
//   .husky/pre-push                 → node scripts/gate.mjs --pre-push  (refs on stdin)
// Add --dry-run to either to print what would run and stop.
//
// Path-aware: a push runs the checks for the workspace packages it touched.
// Shared code (packages/**, lockfile, workspace or TS base config, this script)
// revalidates everything, and so does any range that can't be computed (a new
// branch, a shallow clone). Skipping is only ever for a change proven out of
// scope. GATE_FULL=1 forces the whole suite. SKIP_VERCEL_BUILD=1 skips only the
// `vercel build` step.
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

// Node 24 is the runtime (BP §1, .nvmrc). Below 24.9 Jest can't require() the
// ESM packages NestJS 12 ships, and the failure reads as a broken test, so say so.
const [major, minor] = process.versions.node.split('.').map(Number);
if (major < 24 || (major === 24 && minor < 9)) {
  console.error(`gate: Node ${process.versions.node} is too old; this repo runs on Node 24.9+ (.nvmrc). Run \`nvm use\` and push again.`);
  process.exit(1);
}

const ZERO = /^0+$/;
const root = process.cwd();

function run(label, cmd, args, opts = {}) {
  process.stdout.write(`\ngate: ${label}\n`);
  const r = spawnSync(cmd, args, { stdio: 'inherit', ...opts });
  if (r.status !== 0) {
    process.stdout.write(`\ngate: FAIL at "${label}" (exit ${r.status ?? r.signal})\n`);
    process.exit(r.status ?? 1);
  }
}

function has(cmd) {
  return spawnSync('sh', ['-c', `command -v ${cmd}`], { stdio: 'ignore' }).status === 0;
}

/** Every workspace package with a package.json: { name, dir, scripts, next }. */
function workspacePackages() {
  const out = [];
  for (const group of ['apps', 'packages']) {
    if (!existsSync(group)) continue;
    for (const d of readdirSync(group)) {
      const pj = join(group, d, 'package.json');
      if (!existsSync(pj)) continue;
      const json = JSON.parse(readFileSync(pj, 'utf8'));
      const deps = { ...json.dependencies, ...json.devDependencies };
      out.push({ name: json.name, dir: join(group, d), scripts: json.scripts ?? {}, next: 'next' in deps });
    }
  }
  return out;
}

/** Files changed by the refs git hands a pre-push hook, or null when unknowable. */
function changedFilesFromStdin() {
  const input = readFileSync(0, 'utf8').trim();
  if (!input) return [];
  const files = new Set();
  for (const line of input.split('\n')) {
    const [, localSha, , remoteSha] = line.trim().split(/\s+/);
    if (!localSha || ZERO.test(localSha)) continue; // a branch deletion changes no files
    if (!remoteSha || ZERO.test(remoteSha)) return null; // new branch: no base to diff
    const r = spawnSync('git', ['diff', '--name-only', `${remoteSha}..${localSha}`], { encoding: 'utf8' });
    if (r.status !== 0) return null; // shallow clone or unknown object
    for (const f of r.stdout.split('\n')) if (f) files.add(f);
  }
  return [...files];
}

const SHARED = [/^packages\//, /^pnpm-lock\.yaml$/, /^pnpm-workspace\.yaml$/, /^package\.json$/,
  /^tsconfig\.base\.json$/, /^turbo\.json$/, /^scripts\/gate\.mjs$/, /^scripts\/check-env\.mjs$/, /^\.husky\//];
// Paths no JS check reads. Anything else outside a package is treated as shared.
const OUT_OF_SCOPE = [/^docs\//, /^design\//, /^[^/]+\.md$/, /^Caddyfile$/, /^docker-compose[^/]*\.ya?ml$/,
  /^\.slipway\//, /^\.claude\//, /^\.watchmanconfig$/, /^\.prettierrc$/, /^\.gitignore$/,
  /^crates\//, /^Cargo\.(toml|lock)$/, /^apps\/(macos|ios)\//, /^scripts\/[^/]+\.sh$/];

function plan(files, pkgs) {
  if (files === null) return { full: true, reason: 'range not computable' };
  const touched = new Set();
  let rust = false;
  let swift = false;
  for (const f of files) {
    if (/^(crates\/|Cargo\.(toml|lock)$)/.test(f)) rust = true;
    if (f.startsWith('apps/macos/')) swift = true;
    if (SHARED.some((re) => re.test(f))) return { full: true, reason: `shared file ${f}` };
    const pkg = pkgs.find((p) => f.startsWith(`${p.dir}/`));
    if (pkg) { touched.add(pkg.name); continue; }
    if (OUT_OF_SCOPE.some((re) => re.test(f))) continue;
    return { full: true, reason: `unclassified path ${f}` };
  }
  return { full: false, packages: [...touched], rust, swift };
}

const args = new Set(process.argv.slice(2));
const pkgs = workspacePackages();
let p;
if (args.has('--all') || process.env.GATE_FULL === '1') p = { full: true, reason: 'full run requested' };
else if (args.has('--pre-push')) p = plan(changedFilesFromStdin(), pkgs);
else { console.error('usage: gate.mjs --all | --pre-push [--dry-run]'); process.exit(2); }

const selected = p.full ? pkgs : pkgs.filter((x) => p.packages.includes(x.name));
const rust = p.full ? existsSync('Cargo.toml') : p.rust;
const swift = p.full ? existsSync('apps/macos/Package.swift') : p.swift;
const scope = [...selected.map((x) => x.name), ...(rust ? ['crates (cargo)'] : []), ...(swift ? ['apps/macos (swift)'] : [])];
process.stdout.write(`gate: ${p.full ? `full (${p.reason})` : `scoped to ${scope.join(', ') || 'nothing'}`}\n`);
if (args.has('--dry-run')) process.exit(0); // print the plan, run nothing

if (selected.length > 0) {
  const filters = p.full ? [] : selected.map((x) => `--filter=${x.name}`);
  const linked = selected.filter((x) => x.next && existsSync(join(x.dir, '.vercel', 'project.json')));
  const vercelBuild = process.env.SKIP_VERCEL_BUILD !== '1' && linked.length > 0;

  run('env parity', 'node', ['scripts/check-env.mjs']);
  run('lint + typecheck + test', 'pnpm', ['turbo', 'run', 'lint', 'typecheck', 'test', ...filters, '--output-logs=errors-only']);

  // A linked Next app builds with `vercel build`, which runs the framework build
  // in place and catches standalone, CSP-nonce and build-time-env bugs a plain
  // next build misses. Everything else builds through turbo.
  const viaVercel = vercelBuild ? new Set(linked.map((x) => x.name)) : new Set();
  const turboBuild = selected.filter((x) => !viaVercel.has(x.name)).map((x) => `--filter=${x.name}`);
  if (turboBuild.length > 0) run('build', 'pnpm', ['turbo', 'run', 'build', ...turboBuild, '--output-logs=errors-only']);
  for (const x of linked) {
    if (!vercelBuild) break;
    if (!has('vercel')) { console.error('gate: vercel CLI not installed (npm i -g vercel); linked apps need it'); process.exit(1); }
    run(`vercel build (${x.name})`, 'vercel', ['build'], { cwd: join(root, x.dir) });
  }
  for (const x of selected.filter((s) => s.next && !existsSync(join(s.dir, '.vercel', 'project.json')))) {
    process.stdout.write(`gate: note: ${x.name} is not linked to Vercel, so next build stood in for vercel build. Run \`vercel link && vercel pull\` in ${x.dir} for build parity.\n`);
  }

  for (const x of selected.filter((s) => s.scripts['test:e2e:smoke'])) {
    run(`e2e smoke (${x.name})`, 'pnpm', ['--filter', x.name, 'test:e2e:smoke']);
  }
}
if (rust) {
  if (has('cargo')) run('cargo test', 'cargo', ['test', '-q']);
  else process.stdout.write('gate: note: crates/ changed but cargo is not installed; rust tests did not run\n');
}
if (swift) {
  if (has('swift')) run('swift test (apps/macos)', 'swift', ['test'], { cwd: join(root, 'apps/macos') });
  else process.stdout.write('gate: note: apps/macos changed but swift is not installed; AppCore tests did not run\n');
}
process.stdout.write('\ngate: PASS\n');
