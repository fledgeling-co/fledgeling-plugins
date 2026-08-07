// SINGLE source of design tokens (BP §22). Every downstream copy (tokens.css,
// native token structs) is GENERATED from this file — never hand-edit those.
// Replace these placeholder values when the DESIGN.md lands.
export const tokens = {
  color: {
    bg: '#ffffff',
    fg: '#111114',
    muted: '#6b6b76',
    accent: '#2f6fed',
    'accent-fg': '#ffffff',
  },
  space: { xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '40px' },
  radius: { sm: '6px', md: '10px', lg: '16px' },
  font: {
    sans: "system-ui, -apple-system, sans-serif",
    mono: "ui-monospace, 'SF Mono', monospace",
  },
};
