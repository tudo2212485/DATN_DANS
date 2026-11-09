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
        canvas: "#F8FAFC",      // Slate 50: Nền siêu sạch, chuẩn Modern SaaS/Fintech
        surface: {
          DEFAULT: "#FFFFFF",
          subtle: "#F1F5F9",   // Slate 100
          hover: "#F8FAFC",
          dark: "#0F172A",     // Slate 900
        },
        sidebar: "#0F172A",    // Slate 900: Thanh bên phong cách Terminal đẳng cấp
        sidebarItem: "#1E293B",
        card: "#FFFFFF",       // Card trắng tinh tế trên nền slate nhẹ
        border: {
          subtle: "#F1F5F9",
          DEFAULT: "#E2E8F0",  // Slate 200
          strong: "#CBD5E1",   // Slate 300
        },
        brand: {
          DEFAULT: "#059669",  // Emerald 600: Xanh ngọc lục bảo công nghệ cao
          hover: "#047857",    // Emerald 700
          dark: "#064E3B",     // Emerald 900
          light: "#ECFDF5",    // Emerald 50
          badge: "#D1FAE5",    // Emerald 100
        },
        primary: {
          text: "#0F172A",     // Slate 900: Đen than chì sắc nét, dễ đọc tối đa
        },
        secondary: {
          text: "#475569",     // Slate 600: Nâu xám hiện đại
          light: "#64748B",    // Slate 500
          muted: "#94A3B8",    // Slate 400
        },
        accent: {
          emerald: "#10B981",
          emeraldLight: "#ECFDF5",
          blue: "#2563EB",
          blueLight: "#EFF6FF",
          purple: "#7C3AED",
          purpleLight: "#F5F3FF",
          rose: "#E11D48",
          roseLight: "#FFF1F2",
          amber: "#D97706",
          amberLight: "#FEF3C7",
          cyan: "#0891B2",
          cyanLight: "#ECFEFF",
        },
      },
      fontFamily: {
        sans: [
          '"Plus Jakarta Sans"',
          '"Segoe UI"',
          'Roboto',
          '-apple-system',
          'BlinkMacSystemFont',
          'Arial',
          'sans-serif',
        ],
        mono: [
          '"JetBrains Mono"',
          'Consolas',
          'Menlo',
          'Monaco',
          'ui-monospace',
          'monospace',
        ],
      },
      boxShadow: {
        card: "0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 4px 16px -2px rgba(15, 23, 42, 0.06)",
        hover: "0 10px 25px -3px rgba(5, 150, 105, 0.12), 0 4px 6px -2px rgba(15, 23, 42, 0.04)",
        glow: "0 0 20px -2px rgba(16, 185, 129, 0.35)",
        glowBlue: "0 0 20px -2px rgba(37, 99, 235, 0.35)",
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
    },
  },
  plugins: [],
};
export default config;
