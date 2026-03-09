/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        colombian: {
          yellow: '#FCD116',
          blue: '#003893',
          red: '#CE1126',
        }
      }
    },
  },
  plugins: [],
}
