/** @type {import('tailwindcss').Config} */
module.exports = {
  // Support both .dark class and [data-theme="dark"] attribute
  darkMode: ['class', '[data-theme="dark"]'],
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./static/**/*.css"
  ],
  theme: {
    extend: {
      colors: {
        // Studio Obsidian Noir (Dark Theme) Tokens
        obsidian: {
          base: '#0E0F12',
          dim: '#121316',
          surface: '#16181F',
          card: '#1A1D27',
          bright: '#292A2D',
          border: 'rgba(255, 255, 255, 0.08)',
        },
        // Clean Gallery Editorial (Light Theme) Tokens
        gallery: {
          bone: '#FAF9F6',
          canvas: '#F9F8F5',
          surface: '#FFFFFF',
          container: '#EFEEEB',
          subtle: '#F4F3F0',
          hairline: '#E6E3DD',
        },
        // Primary Brand Accents
        terracotta: {
          DEFAULT: '#D96B43',
          hover: '#BD5630',
          dark: '#9D3E1A',
          light: '#FFB59C',
          container: '#FFDBCF',
        },
        amber: {
          DEFAULT: '#E5A93C',
          gold: '#F59E0B',
          light: '#FFDEAD',
          bright: '#FFC665',
        },
        gold: {
          DEFAULT: '#C58B2E',
          ochre: '#825500',
          light: '#FFDDB2',
          dim: '#FCBB59',
        },
        // Editorial Typography Inks
        charcoal: {
          DEFAULT: '#1A1A1E',
          deep: '#1A1C1A',
          muted: '#56423C',
          slate: '#64748B',
        },
        // Digital Highlights & Tools
        violet: {
          DEFAULT: '#8B5CF6',
          container: '#7C3AED',
          light: '#D0BCFF',
        },
        cyan: {
          DEFAULT: '#06B6D4',
          bright: '#59E0FF',
          container: '#2EC4E2',
        },
        // Workflow Status Indicators
        status: {
          revision: '#EF4444',
          'revision-bg': '#FFDAD6',
          pending: '#F59E0B',
          'pending-bg': '#FFBD5C',
          delivery: '#10B981',
          'delivery-bg': '#C8FAD6',
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'Outfit', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['"Playfair Display"', 'serif'],
        body: ['"Plus Jakarta Sans"', 'sans-serif'],
      },
      fontSize: {
        'display-lg': ['64px', { lineHeight: '72px', letterSpacing: '-0.02em' }],
        'headline-lg': ['40px', { lineHeight: '48px', letterSpacing: '-0.015em' }],
        'headline-md': ['28px', { lineHeight: '36px', letterSpacing: '0' }],
        'title-lg': ['20px', { lineHeight: '28px', letterSpacing: '0' }],
        'body-lg': ['18px', { lineHeight: '28px', letterSpacing: '0.01em' }],
        'body-md': ['16px', { lineHeight: '24px', letterSpacing: '0' }],
        'label-md': ['14px', { lineHeight: '20px', letterSpacing: '0.05em' }],
        'label-sm': ['12px', { lineHeight: '16px', letterSpacing: '0.08em' }],
        'currency-inr': ['18px', { lineHeight: '24px', letterSpacing: '0.02em' }],
      },
      borderRadius: {
        sm: '4px',
        DEFAULT: '8px',
        md: '8px',
        lg: '16px',
        xl: '24px',
        full: '9999px',
      },
      spacing: {
        gutter: '24px',
        'section-gap': '80px',
        'desktop-margin': '64px',
        'mobile-margin': '20px',
        'stack-sm': '8px',
        'stack-md': '16px',
        'stack-lg': '32px',
      },
      maxWidth: {
        'container-canvas': '1440px',
      },
      boxShadow: {
        'glass-level1': '0 8px 32px 0 rgba(0, 0, 0, 0.15)',
        'elevated-dark': '0 24px 64px -12px rgba(0, 0, 0, 0.6)',
        'elevated-light': '0 20px 48px -8px rgba(26, 26, 30, 0.12)',
        'amber-glow': '0 0 20px rgba(229, 169, 60, 0.28)',
        'terracotta-focus': '0 0 0 3px rgba(217, 107, 67, 0.15)',
      },
      backdropBlur: {
        vitrine: '16px',
        modal: '40px',
      }
    },
  },
  plugins: [],
};
