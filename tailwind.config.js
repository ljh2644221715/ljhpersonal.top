/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "Segoe UI", "PingFang SC", "Microsoft YaHei", "sans-serif"],
      },
      colors: {
        ink: "#020617",
        aurora: {
          50: "#ebfffd",
          100: "#c4fff8",
          200: "#8effef",
          300: "#51f1e0",
          400: "#22d3ee",
          500: "#14b8a6",
          600: "#0d9488",
          700: "#0f766e",
        },
        surface: {
          DEFAULT: "rgba(255,255,255,0.04)",
          hover: "rgba(255,255,255,0.08)",
        },
      },
      boxShadow: {
        soft: "0 24px 80px rgba(15, 23, 42, 0.45)",
        glow: "0 0 0 1px rgba(34, 211, 238, 0.2), 0 20px 60px rgba(20, 184, 166, 0.16)",
        card: "0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)",
      },
      backgroundImage: {
        "hero-grid":
          "linear-gradient(rgba(148,163,184,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.08) 1px, transparent 1px)",
        "aurora-radial":
          "radial-gradient(circle at top, rgba(34, 211, 238, 0.16), transparent 42%), radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.16), transparent 30%)",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        pulseLine: {
          "0%, 100%": { opacity: "0.55" },
          "50%": { opacity: "1" },
        },
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        float: "float 7s ease-in-out infinite",
        "pulse-line": "pulseLine 3.5s ease-in-out infinite",
        "fade-in": "fadeIn 0.5s ease-out",
      },
    },
  },
  plugins: [],
};
