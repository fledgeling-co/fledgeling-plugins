// Generates tokens.css from src/tokens.mjs. `--check` regenerates in memory and
// fails on drift — wired into the turbo gate so a hand-edit can't survive a push.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tokens } from './src/tokens.mjs';

const lines = [':root {'];
for (const [group, values] of Object.entries(tokens)) {
  for (const [name, value] of Object.entries(values)) {
    lines.push(`  --${group}-${name}: ${value};`);
  }
}
lines.push('}', '');
const css = `/* GENERATED from src/tokens.mjs — do not hand-edit (BP §22). */\n${lines.join('\n')}`;

if (process.argv.includes('--check')) {
  const current = existsSync('tokens.css') ? readFileSync('tokens.css', 'utf8') : '';
  if (current !== css) {
    console.error('tokens.css is out of date with src/tokens.mjs — run: pnpm --filter design-tokens build');
    process.exit(1);
  }
  console.log('tokens.css is in sync');
} else {
  writeFileSync('tokens.css', css);
  console.log('wrote tokens.css');
}
