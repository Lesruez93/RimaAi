import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette sampled from the RimaAI badge logo.
        rima: {
          DEFAULT: "#18532E", // deep badge green
          dark: "#0E3D21",
          light: "#2E8B4E",
          leaf: "#73A64B", // maize-leaf green
          gold: "#C5A763", // badge ring
          blue: "#136A90", // badge blue half
          "blue-dark": "#0E5375",
          cream: "#F4F6F1",
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
