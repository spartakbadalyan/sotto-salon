import { FlatCompat } from "@eslint/eslintrc";

// Flat-config bridge for Next.js's shareable ESLint config (ESLint 9). Running
// `npm run lint` (`eslint .`) performs a reproducible, non-interactive check.
const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

const config = [
  { ignores: [".next/**", "node_modules/**", "next-env.d.ts"] },
  ...compat.extends("next/core-web-vitals"),
];

export default config;
