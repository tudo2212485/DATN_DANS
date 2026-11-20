import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "#F8FAF9",
        surface: {
          DEFAULT: "#FFFFFF",
          subtle: "#F1F5F3",
          hover: "#F8FAF9",
          dark: "#1E293B",
        },
        sidebar: "#FFFFFF",
        sidebarItem: "#F0F7F4",
        card: "#FFFFFF",
        border: {
          subtle: "#E5E7EB",
          DEFAULT: "#E5E7EB",
          strong: "#CBD5E1",
        },
        brand: {
          DEFAULT: "#2F6F4E",
          hover: "#24583D",
          dark: "#1B432E",
          light: "#F0F7F4",
          badge: "#D1FAE5",
        },
        primary: {
          text: "#1E293B",
        },
        secondary: {
          text: "#334155",
          light: "#64748B",
          muted: "#94A3B8",
        },
        accent: {
          emerald: "#15803D",
          emeraldLight: "#F0FDF4",
          blue: "#2563EB",
          blueLight: "#EFF6FF",
          purple: "#7C3AED",
          purpleLight: "#F5F3FF",
          rose: "#DC2626",
          roseLight: "#FEF2F2",
          amber: "#D97706",
          amberLight: "#FEF3C7",
          cyan: "#0891B2",
          cyanLight: "#ECFEFF",
        },
      },
      fontFamily: {
        sans: [
          "var(--font-sans)",
          '"Be Vietnam Pro"',
          '"Segoe UI"',
          "Roboto",
          "-apple-system",
          "BlinkMacSystemFont",
          "Arial",
          "sans-serif",
        ],
        mono: [
          "var(--font-sans)",
          '"Be Vietnam Pro"',
          '"JetBrains Mono"',
          "Consolas",
          "monospace",
        ],
      },
      boxShadow: {
        card: "0 1px 2px 0 rgba(30, 41, 59, 0.03), 0 2px 8px -2px rgba(30, 41, 59, 0.04)",
        hover: "0 6px 16px -3px rgba(47, 111, 78, 0.10), 0 2px 6px -2px rgba(30, 41, 59, 0.04)",
      },
      borderRadius: {
        lg: "0.5rem",
        xl: "0.75rem",
        "2xl": "0.875rem",
      },
    },
  },
  plugins: [],
};
export default config;
