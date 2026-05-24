/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: '#000000',
        'canvas-soft': '#000000',
        'canvas-card': '#000000',
        'canvas-mid': '#363a3f',
        hairline: '#ffffff',
        ink: '#ffffff',
        'ink-hover': '#fafaf7',
        body: '#dadbdf',
        'body-mid': '#7d8187',
        mute: '#7d8187',
        accent: {
          sunset: '#ff7a17',
          'sunset-soft': '#ffc285',
          dusk: '#7c3aed',
          twilight: '#c4b5fd',
          breeze: '#a0c3ec',
          midnight: '#0d1726',
        },
      },
      fontFamily: {
        sans: ['Courier Prime', 'JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Courier New', 'monospace'],
        mono: ['Courier Prime', 'JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Courier New', 'monospace'],
      },
      fontSize: {
        'display-xl': ['96px', { lineHeight: '96px', letterSpacing: '-2.4px', fontWeight: '400' }],
        'display-lg': ['72px', { lineHeight: '72px', letterSpacing: '-1.8px', fontWeight: '400' }],
        'display-md': ['48px', { lineHeight: '48px', letterSpacing: '-1.2px', fontWeight: '400' }],
        'display-sm': ['32px', { lineHeight: '36px', letterSpacing: '-0.6px', fontWeight: '400' }],
        'display-xs': ['20px', { lineHeight: '28px', fontWeight: '400' }],
      },
      borderRadius: {
        card: '8px',
        pill: '9999px',
      },
      spacing: {
        'section': '64px',
      },
    },
  },
  plugins: [],
}
