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
        canvas: "#F9F6F2",
        sidebar: "#FAF8F5",
        card: "#FFFFFF",
        border: {
          subtle: "#EFECE6",
          DEFAULT: "#E5E0D8",
          strong: "#D4CEBE",
        },
        brand: {
          DEFAULT: "#4E7152",
          dark: "#3B573F",
          light: "#E8EFE9",
          badge: "#EBF3EB",
        },
        primary: {
          text: "#2D231E",
        },
        secondary: {
          text: "#8D7B68",
          light: "#A89A8B",
        },
        accent: {
          green: "#4E7152",
          coral: "#D97757",
          coralLight: "#FDECE8",
          brown: "#9C6644",
          blue: "#4A69BD",
          blueLight: "#EBF0FA",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "Inter", "Be Vietnam Pro", "-apple-system", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(45, 35, 30, 0.03), 0 4px 12px rgba(45, 35, 30, 0.02)",
        hover: "0 4px 20px rgba(78, 113, 82, 0.08)",
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.25rem',
      },
    },
  },
  plugins: [],
};
export default config;
