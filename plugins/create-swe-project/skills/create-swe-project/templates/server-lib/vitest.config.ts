import { defineConfig } from 'vitest/config';
import { fileURLToPath } from 'node:url';

const here = (p: string) => fileURLToPath(new URL(p, import.meta.url));

// Two projects (BP §15). `unit` is hermetic and is what `pnpm test` and the gate
// run; it never needs Docker. `integration` runs black-box against a seeded
// server and stays out of the gate (its script passes --passWithNoTests until
// the first integration test exists).
export default defineConfig({
  // Next's tsconfig says jsx: preserve; tests need the automatic runtime.
  oxc: { jsx: { runtime: 'automatic' } },
  resolve: {
    alias: [
      { find: 'server-only', replacement: here('./test/server-only-stub.ts') },
      { find: /^@\//, replacement: here('./') },
    ],
  },
  test: {
    projects: [
      {
        extends: true,
        test: {
          name: 'unit',
          environment: 'node',
          include: ['**/*.test.{ts,tsx}'],
          exclude: ['node_modules/**', '.next/**', 'e2e/**', 'tests/integration/**'],
        },
      },
      {
        extends: true,
        test: {
          name: 'integration',
          environment: 'node',
          include: ['tests/integration/**/*.test.ts'],
        },
      },
    ],
  },
});
