import nextCoreWebVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';

// Flat config — eslint-config-next 16 exports flat-config arrays directly.
// core-web-vitals wires in @next/next + react-hooks + jsx-a11y — the plugins a
// hollow lint gate would skip (CP §6.9).
const config = [
  { ignores: ['.next/**', 'node_modules/**', 'next-env.d.ts'] },
  ...nextCoreWebVitals,
  ...nextTypescript,
];

export default config;
