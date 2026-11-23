/** Mesma base visual do portal GADHOC Aeroportos (Tailwind 3, tema escuro por classe). */
module.exports = {
  darkMode: 'class',
  content: ['./src/src.html'],
  theme: {
    extend: {
      colors: {
        aero: { 600: '#2a6f9e', 700: '#1d537e', 750: '#174366', 800: '#11324d', 850: '#0b2236', 900: '#071623', 950: '#02070e' },
        slate: { 750: '#283548' }
      },
      fontFamily: {
        sans: ['Saira', '"Segoe UI"', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['"Chakra Petch"', 'Bahnschrift', '"Segoe UI"', 'sans-serif'],
        mono: ['"Share Tech Mono"', 'ui-monospace', 'Menlo', 'Consolas', 'monospace'],
        hud: ['"Share Tech Mono"', 'ui-monospace', 'Menlo', 'Consolas', 'monospace']
      },
      boxShadow: {
        xs: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'glow-cyan': '0 0 20px #3fe0d066',
        'glow-emerald': '0 0 20px #10b98140',
        'glow-sm': '0 0 15px #3fe0d033',
        'glow-amber': '0 0 20px rgba(255,180,64,.35)',
        'hud-hover': '0 12px 35px rgba(0,0,0,.65), 0 0 25px rgba(63,224,208,.25)',
        'hud-panel': '0 8px 30px rgba(7,22,35,.88)'
      },
      spacing: { '0.2': '0.05rem', '1.8': '0.45rem' },
      keyframes: { 'fade-in': { from: { opacity: '0', transform: 'translateY(4px)' }, to: { opacity: '1', transform: 'none' } } },
      animation: { 'fade-in': 'fade-in .25s ease-out both' }
    }
  },
  plugins: []
};
