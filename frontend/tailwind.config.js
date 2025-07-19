/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        corporate: {
          light: '#e0f2ff',
          DEFAULT: '#0077ff',
          dark: '#004799'
        }
      }
    }
  },
  plugins: []
};
