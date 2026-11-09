// Expo configures Metro for monorepos itself since SDK 52 (BP §18). Hand-written
// watchFolders / resolver.nodeModulesPaths / extraNodeModules /
// disableHierarchicalLookup now fight those defaults, so this stays the default.
const { getDefaultConfig } = require('expo/metro-config');

module.exports = getDefaultConfig(__dirname);
