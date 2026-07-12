import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        rima: {
          DEFAULT: "#2e7d32",
          dark: "#1b5e20",
          light: "#66bb6a",
          accent: "#f9a825",
        },
        risk: {
          low: "#43a047",
          moderate: "#f9a825",
          high: "#e53935",
        },
      },
    },
  },
  plugins: [],
};

export default config;
