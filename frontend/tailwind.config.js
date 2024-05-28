/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: ({ defaultTheme }) =>  ({
      fontFamily: {
        sans: ['IBM Plex Sans', 'sans-serif'],
      },
    }),
  },
  plugins: [],
}
