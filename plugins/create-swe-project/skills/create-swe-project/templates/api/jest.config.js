// Plain .js config on purpose: a jest.config.ts silently drags ts-node into the
// workspace (BP §15). Transform is @swc/jest — never ts-jest — with decorator
// metadata or Nest DI silently fails to resolve.
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
  coverageProvider: 'v8',
  testEnvironmentOptions: { globalsCleanup: 'on' },
};
