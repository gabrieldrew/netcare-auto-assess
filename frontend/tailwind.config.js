module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        netcare: {
          navy: '#1B4B5A',
          primary: '#1D3443',
          gold: '#D3B380',
          cyan: '#3DA9D1',
          light: '#D0E9F3',
          white: '#FFFFFF',
        }
      },
      fontFamily: {
        'sans': ['Inter', 'Open Sans', 'Arial', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'fade-in-up': 'fadeInUp 0.6s ease-out forwards',
        'scale-in': 'scaleIn 0.3s ease-out forwards',
        'slide-in': 'slideIn 0.4s ease-out forwards',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          'from': {
            opacity: '0',
            transform: 'translateY(10px)'
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        fadeInUp: {
          'from': {
            opacity: '0',
            transform: 'translateY(20px)'
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0)'
          }
        },
        scaleIn: {
          'from': {
            opacity: '0',
            transform: 'scale(0.95)'
          },
          'to': {
            opacity: '1',
            transform: 'scale(1)'
          }
        },
        slideIn: {
          'from': {
            opacity: '0',
            transform: 'translateX(-20px)'
          },
          'to': {
            opacity: '1',
            transform: 'translateX(0)'
          }
        }
      },
      boxShadow: {
        'glow': '0 0 30px rgba(61, 169, 209, 0.15)',
        'glow-lg': '0 0 50px rgba(61, 169, 209, 0.2)',
        'netcare': '0 10px 25px -3px rgba(29, 52, 67, 0.1), 0 4px 6px -2px rgba(29, 52, 67, 0.05)',
        'netcare-lg': '0 20px 25px -5px rgba(29, 52, 67, 0.1), 0 10px 10px -5px rgba(29, 52, 67, 0.04)',
      },
      backgroundImage: {
        'netcare-gradient': 'linear-gradient(135deg, #D0E9F3 0%, #B8E1F0 50%, #A0D6ED 100%)',
        'netcare-card': 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.8) 100%)',
        'glass-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      maxWidth: {
        '8xl': '88rem',
        '9xl': '96rem',
      },
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      }
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        '.glass-effect': {
          'background': 'rgba(255, 255, 255, 0.8)',
          'backdrop-filter': 'blur(10px)',
          'border': '1px solid rgba(255, 255, 255, 0.2)',
        },
        '.gradient-text': {
          'background': 'linear-gradient(135deg, #1D3443 0%, #3DA9D1 100%)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text',
        },
        '.border-gradient': {
          'border': '1px solid transparent',
          'background': 'linear-gradient(white, white) padding-box, linear-gradient(135deg, #3DA9D1, #1D3443) border-box',
        },
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none'
          }
        }
      }
      addUtilities(newUtilities)
    }
  ],
};