import nextCoreWebVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';

// Flat config. core-web-vitals wires in @next/next + react-hooks + jsx-a11y,
// the plugins a hollow lint gate would skip (CP §6.9).
const config = [
  { ignores: ['.next/**', 'node_modules/**', 'next-env.d.ts'] },
  ...nextCoreWebVitals,
  ...nextTypescript,
  // lib/logger.ts is the one sanctioned console writer (CP §5).
  { rules: { 'no-console': 'error' } },
  { files: ['lib/logger.ts', '**/*.test.ts'], rules: { 'no-console': 'off' } },
];

export default config;
