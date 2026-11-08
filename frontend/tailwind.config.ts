import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        torob: {
          red: "#D73948",
          redHover: "#BE123C",
          softBg: "#FFF1F2",
          canvas: "#F8F9FA",
          liveGreen: "#10B981",
          staleAmber: "#F59E0B",
          realPurple: "#7C3AED"
        }
      },
      fontFamily: {
        sans: ["Vazirmatn", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};
export default config;
