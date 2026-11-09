import nextCoreWebVitals from 'eslint-config-next/core-web-vitals';
import nextTypescript from 'eslint-config-next/typescript';

// Flat config. core-web-vitals wires in @next/next + react-hooks + jsx-a11y,
// the plugins a hollow lint gate would skip (CP §6.9).
const config = [
  { ignores: ['.next/**', 'node_modules/**', 'next-env.d.ts', 'playwright-report/**', 'test-results/**'] },
  ...nextCoreWebVitals,
  ...nextTypescript,
  {
    rules: {
      // lib/logger.ts is the one sanctioned console writer (CP §5).
      'no-console': 'error',
      // The browser calls only this app's route handlers (BP §24): no direct
      // backend client, no public backend URL.
      'no-restricted-imports': ['error', { paths: [{ name: 'axios', message: 'Use fetch through a route handler (BFF rule, BP §24).' }] }],
      'no-restricted-syntax': [
        'error',
        {
          selector: "MemberExpression[object.object.name='process'][object.property.name='env'][property.name='NEXT_PUBLIC_API_URL']",
          message: 'The browser never calls the backend directly; go through a route handler (BP §24).',
        },
      ],
    },
  },
  { files: ['lib/logger.ts', 'scripts/**', 'e2e/**', '**/*.test.ts', '**/*.test.tsx'], rules: { 'no-console': 'off' } },
];

export default config;
