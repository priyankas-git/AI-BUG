/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0b0c10",
        darkCard: "#1f2833",
        darkBorder: "#2d3748",
        accentBlue: "#66fcf1",
        accentBlueHover: "#45a29e",
        severityCritical: "#ef4444",
        severityHigh: "#f97316",
        severityMedium: "#eab308",
        severityLow: "#22c55e"
      }
    },
  },
  plugins: [],
}
