import { defineConfig } from 'vitest/config';

// Node-env tests over the PURE lib/ helpers only (BP §18): modules with no
// runtime react-native or expo import (use `import type`), no asset require().
// Anything touching the RN runtime is covered by Maestro on a device instead.
export default defineConfig({
  test: { environment: 'node', include: ['lib/**/*.test.ts'], passWithNoTests: true },
});
