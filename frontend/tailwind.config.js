/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        midnight: {
          950: '#020408', // Deepest background (Main)
          900: '#090b10', // Panels / Cards
          800: '#151923', // Hover states
          700: '#1e2433', // Borders (Subtle)
        },
        accent: {
          blue: '#3b82f6', // Primary Action
          gold: '#d97706', // Warnings / Macros
          teal: '#10b981', // Growth / Success
          rose: '#e11d48', // Risk / Critical
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
      boxShadow: {
        'glow': '0 0 20px -5px rgba(59, 130, 246, 0.15)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
      }
    },
  },
  plugins: [],
}