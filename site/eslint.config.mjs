import { defineConfig } from "eslint/config";
import next from "eslint-config-next";

/**
 * eslint-config-next ships a flat-config ARRAY in this version, not a
 * `{ configs: { … } }` object — spreading it directly is the shape that works.
 */
export default defineConfig([
  { ignores: [".next/**", "node_modules/**", "public/**", "lib/catalogue.json"] },
  ...next,
]);
