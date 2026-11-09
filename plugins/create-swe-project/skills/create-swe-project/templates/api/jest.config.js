// Plain .js config on purpose: a jest.config.ts silently drags ts-node into the
// workspace. The transform is @swc/jest, never ts-jest, with decorator metadata
// or Nest DI silently fails to resolve (BP §15, CP §2).
//
// NestJS 12 ships ESM. Jest loads it through native require(esm) only on Node
// 24.9+ AND with --experimental-vm-modules (it needs vm.SourceTextModule), which
// is why the test script sets NODE_OPTIONS. Without the flag every suite fails
// with "Must use import to load ES Module".
const isCI = Boolean(process.env.CI);

module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/test'],
  transform: {
    '^.+\\.ts$': [
      '@swc/jest',
      {
        jsc: {
          target: 'es2022',
          parser: { syntax: 'typescript', decorators: true },
          transform: { legacyDecorator: true, decoratorMetadata: true },
          keepClassNames: true,
        },
        module: { type: 'commonjs' },
      },
    ],
  },
  // @swc/jest doesn't instrument, so v8 avoids a second Babel pass (CP §2).
  coverageProvider: 'v8',
  collectCoverage: isCI,
  // Jest 30 opt-ins: release test globals, recycle ballooning workers, and keep
  // interactive runs lean on a many-core machine.
  testEnvironmentOptions: { globalsCleanup: 'on' },
  workerIdleMemoryLimit: '1GB',
  maxWorkers: isCI ? '50%' : 4,
};
