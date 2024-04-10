/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors:{
        "primary": "#567BFF",
        "segundary": "#A1A1AA"
      }
    },
  },
  plugins: [],
}