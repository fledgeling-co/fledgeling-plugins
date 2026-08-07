// Monorepo-aware Metro (BP §18): watch the workspace root and resolve from both
// the app's and the root node_modules — Metro does not handle a pnpm layout
// without this (the root .npmrc also sets node-linker=hoisted).
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);
config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = config;
