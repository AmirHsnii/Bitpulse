/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        vazir: ['Vazir', 'sans-serif'],
      },
      colors: {
        primary: '#015845',
        secondary: '#ffc46c',
        background: '#262626',
      },
    },
  },
  plugins: [],
} 