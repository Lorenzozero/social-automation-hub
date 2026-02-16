# Design Guidelines

## Overview

Social Automation Hub is designed for **creators, influencers, and agencies** who need a professional yet approachable tool for managing their social media presence. The design balances **vibrant energy** (appealing to creators) with **professional credibility** (trusted by brands).

## Design Principles

### 1. Creator-First
- **Personality**: Friendly, energetic, empowering
- **Tone**: Professional but never corporate or cold
- **Goal**: Make social media management feel less like work, more like creative expression

### 2. Visual Hierarchy
- **Most important**: Current metrics and actionable insights
- **Secondary**: Historical trends and detailed breakdowns
- **Tertiary**: Settings and configuration

### 3. Speed & Efficiency
- **Loading states**: Always show skeleton loaders, never blank screens
- **Transitions**: Smooth (200-300ms) but never slow (avoid >500ms)
- **Interactions**: Immediate feedback (hover states, click animations)

### 4. Data Density
- **Dashboard**: High-level overview, scannable in 5 seconds
- **Analytics**: Detailed drill-down, support exploratory analysis
- **Balance**: Don't overwhelm with data, but don't hide important info

### 5. Mobile-Responsive
- **Desktop-first design** (primary use case: content creators at desks)
- **Mobile-optimized** (secondary: check metrics on-the-go)
- **Breakpoints**: Tailwind default (sm: 640px, md: 768px, lg: 1024px, xl: 1280px)

## Color Palette

### Primary Colors

```css
/* Brand Primary (Violet) - Main CTAs, active states */
--brand-primary: #8b5cf6;        /* violet-500 */
--brand-primary-dark: #7c3aed;   /* violet-600 - hover state */
--brand-primary-light: #a78bfa;  /* violet-400 - disabled state */

/* Brand Secondary (Coral) - Accents, highlights, secondary CTAs */
--brand-secondary: #f97316;       /* orange-500 */
--brand-secondary-dark: #ea580c;  /* orange-600 */
--brand-secondary-light: #fb923c; /* orange-400 */
```

### Semantic Colors

```css
/* Success - Positive metrics, completed actions */
--success: #10b981;        /* green-500 */
--success-bg: #d1fae5;     /* green-100 */

/* Error - Errors, failed actions, alerts */
--error: #ef4444;          /* red-500 */
--error-bg: #fee2e2;       /* red-100 */

/* Warning - Warnings, pending actions */
--warning: #f59e0b;        /* amber-500 */
--warning-bg: #fef3c7;     /* amber-100 */

/* Info - Neutral information, hints */
--info: #3b82f6;           /* blue-500 */
--info-bg: #dbeafe;        /* blue-100 */
```

### Neutral Colors

```css
/* Light Mode */
--background: #ffffff;       /* Pure white background */
--surface: #f9fafb;          /* gray-50 - Cards, inputs */
--muted: #f3f4f6;            /* gray-100 - Disabled, secondary elements */
--foreground: #111827;       /* gray-900 - Primary text */
--foreground-secondary: #6b7280; /* gray-500 - Secondary text */

/* Dark Mode */
--background-dark: #0f172a;       /* slate-900 */
--surface-dark: #1e293b;          /* slate-800 */
--muted-dark: #334155;            /* slate-700 */
--foreground-dark: #f8fafc;       /* slate-50 */
--foreground-secondary-dark: #94a3b8; /* slate-400 */
```

## Typography

### Font Family

```css
/* Primary: Inter (modern, highly legible, professional) */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Why Inter?**
- Excellent legibility at all sizes (8px to 72px)
- Wide language support (Latin, Cyrillic, Greek)
- Designed for screens (optimized hinting)
- Free and open-source

### Font Scale

```css
/* Headings */
--text-4xl: 2.25rem;  /* 36px - Page titles */
--text-3xl: 1.875rem; /* 30px - Section headings */
--text-2xl: 1.5rem;   /* 24px - Card headings */
--text-xl: 1.25rem;   /* 20px - Subheadings */
--text-lg: 1.125rem;  /* 18px - Large body */

/* Body */
--text-base: 1rem;    /* 16px - Default body */
--text-sm: 0.875rem;  /* 14px - Small text, labels */
--text-xs: 0.75rem;   /* 12px - Captions, hints */
```

### Font Weights

```css
--font-regular: 400;   /* Body text */
--font-medium: 500;    /* Emphasized text */
--font-semibold: 600;  /* Headings, buttons */
--font-bold: 700;      /* Strong emphasis, numbers */
```

### Line Heights

```css
--leading-tight: 1.25;   /* Headings */
--leading-normal: 1.5;   /* Body text */
--leading-relaxed: 1.75; /* Long-form content */
```

## Spacing Scale

Follow Tailwind's spacing scale (based on 0.25rem = 4px):

```css
/* Common spacings */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

**Usage**:
- Between cards: `space-6` (24px)
- Inside cards (padding): `space-6` (24px)
- Between sections: `space-12` (48px)
- Page margins: `space-8` (32px) on mobile, `space-12` (48px) on desktop

## Components

### Buttons

**Primary Button** (main CTAs):
```tsx
className="
  px-6 py-3 
  bg-brand-primary hover:bg-brand-primary-dark 
  text-white font-semibold 
  rounded-xl 
  transition-all duration-200 
  hover:scale-105 active:scale-95
  shadow-lg hover:shadow-xl
"
```

**Secondary Button** (less prominent actions):
```tsx
className="
  px-6 py-3 
  bg-surface hover:bg-muted 
  text-foreground font-semibold 
  rounded-xl 
  transition-all duration-200 
  border border-muted
"
```

**Ghost Button** (tertiary actions):
```tsx
className="
  px-4 py-2 
  text-foreground-secondary hover:text-foreground 
  font-medium 
  rounded-lg 
  transition-colors duration-200
"
```

### Cards

**Standard Card**:
```tsx
className="
  bg-surface 
  rounded-2xl 
  p-6 
  shadow-sm 
  hover:shadow-md 
  transition-shadow duration-200 
  border border-muted
"
```

**Stat Card** (KPI metrics):
```tsx
className="
  bg-gradient-to-br from-brand-primary to-brand-secondary 
  text-white 
  rounded-2xl 
  p-6 
  shadow-lg
"
```

**Interactive Card** (clickable):
```tsx
className="
  bg-surface 
  rounded-2xl 
  p-6 
  shadow-sm 
  hover:shadow-lg hover:scale-[1.02] 
  transition-all duration-200 
  cursor-pointer 
  border border-muted
"
```

### Inputs

**Text Input**:
```tsx
className="
  w-full 
  px-4 py-3 
  bg-surface 
  border border-muted 
  rounded-xl 
  text-foreground 
  placeholder:text-foreground-secondary 
  focus:outline-none 
  focus:ring-2 focus:ring-brand-primary 
  transition-all duration-200
"
```

**Select Dropdown**:
```tsx
className="
  w-full 
  px-4 py-3 
  bg-surface 
  border border-muted 
  rounded-xl 
  text-foreground 
  focus:outline-none 
  focus:ring-2 focus:ring-brand-primary 
  appearance-none 
  cursor-pointer
"
```

### Badges

**Status Badge**:
```tsx
// Success
className="px-3 py-1 bg-success-bg text-success rounded-full text-xs font-medium"

// Error
className="px-3 py-1 bg-error-bg text-error rounded-full text-xs font-medium"

// Warning
className="px-3 py-1 bg-warning-bg text-warning rounded-full text-xs font-medium"
```

### Loading States

**Skeleton Loader**:
```tsx
className="
  animate-pulse 
  bg-muted 
  rounded-xl 
  h-24 w-full
"
```

**Spinner** (for inline loading):
```tsx
<div className="animate-spin rounded-full h-8 w-8 border-4 border-muted border-t-brand-primary" />
```

## Layout Patterns

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│ Header (Sidebar collapsed: logo + breadcrumb + user menu)  │
├───────────┬─────────────────────────────────────────────────┤
│           │                                                 │
│  Sidebar  │                Main Content                     │
│           │  ┌─────────────────────────────────────────┐   │
│  - Dash   │  │ Page Title + Actions                    │   │
│  - Cal    │  ├─────────────────────────────────────────┤   │
│  - Studio │  │                                         │   │
│  - Inbox  │  │  Grid of Cards (4 columns on desktop,   │   │
│  - Analyt │  │  2 on tablet, 1 on mobile)              │   │
│  - Auto   │  │                                         │   │
│  - Acc    │  │                                         │   │
│  - Set    │  └─────────────────────────────────────────┘   │
│           │                                                 │
└───────────┴─────────────────────────────────────────────────┘
```

**Responsive Behavior**:
- **Desktop (lg+)**: Sidebar always visible (240px width)
- **Tablet (md)**: Sidebar collapsible (hamburger menu)
- **Mobile (sm)**: Sidebar drawer (overlay)

### Content Width

```css
/* Maximum content width for readability */
max-width: 1280px; /* Tailwind: max-w-7xl */
margin: 0 auto;
padding: 0 2rem; /* space-8 */
```

## Animations

### Micro-Interactions

**Hover Scale** (buttons, cards):
```css
transition: transform 200ms ease-in-out;
&:hover { transform: scale(1.05); }
```

**Fade In** (page load, modals):
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 300ms ease-out;
}
```

**Stagger Animation** (list items):
```css
.stagger-1 { animation-delay: 100ms; }
.stagger-2 { animation-delay: 200ms; }
.stagger-3 { animation-delay: 300ms; }
```

### Performance

- Prefer `transform` and `opacity` (GPU-accelerated)
- Avoid animating `width`, `height`, `top`, `left` (layout thrashing)
- Use `will-change` sparingly (only for known animations)

## Icons

**Iconography System**: Lucide React (consistent, open-source)

**Sizes**:
- `size={16}` - Inline with text (text-sm)
- `size={20}` - Default buttons, navigation
- `size={24}` - Section headers, primary actions
- `size={32}` - Feature highlights, empty states

**Colors**:
- Match text color (inherit `currentColor`)
- Use semantic colors for status icons (green checkmark, red X)

## Accessibility

### Color Contrast

- **WCAG AA**: Minimum contrast ratio 4.5:1 for normal text, 3:1 for large text
- **WCAG AAA**: Minimum contrast ratio 7:1 for normal text, 4.5:1 for large text
- **Check**: Use WebAIM Contrast Checker

### Focus States

All interactive elements must have visible focus indicator:

```css
focus:outline-none 
focus:ring-2 focus:ring-brand-primary focus:ring-offset-2
```

### Screen Readers

- Use semantic HTML (`<nav>`, `<main>`, `<article>`)
- Add `aria-label` for icon-only buttons
- Use `sr-only` class for screen-reader-only text

```tsx
<button aria-label="Close modal">
  <X size={20} />
  <span className="sr-only">Close</span>
</button>
```

### Keyboard Navigation

- All features accessible via keyboard
- Logical tab order
- Support arrow keys for navigation (lists, calendars)
- Escape key to close modals/dropdowns

## Dark Mode

**Implementation**: CSS variables swap on `dark` class (root level)

```tsx
// Zustand store toggle
const toggleTheme = () => {
  const newTheme = theme === 'light' ? 'dark' : 'light';
  document.documentElement.classList.toggle('dark', newTheme === 'dark');
  setTheme(newTheme);
};
```

**CSS Variables**:
```css
:root {
  --background: #ffffff;
  --foreground: #111827;
  /* ... other light mode colors */
}

.dark {
  --background: #0f172a;
  --foreground: #f8fafc;
  /* ... other dark mode colors */
}
```

**Considerations**:
- Test all components in both modes
- Shadows less prominent in dark mode
- Reduce contrast in dark mode (pure white text is harsh)

## Internationalization (i18n)

**Supported Languages**: English (en), Italian (it)

**Implementation**:
```tsx
import { useTranslations } from '@/lib/i18n';

const t = useTranslations();
<h1>{t('dashboard.title')}</h1> // "Dashboard" or "Pannello di controllo"
```

**Best Practices**:
- Keep translation keys semantic (`page.section.element`)
- Avoid hardcoded strings in components
- Use placeholders for dynamic content: `t('greeting', { name: 'John' })`
- Test RTL languages (future: Arabic, Hebrew)

## Platform-Specific Branding

**Instagram**: Gradient violet-pink, camera icon 📸
**TikTok**: Gradient cyan-pink, music icon 🎵
**LinkedIn**: Blue professional, briefcase icon 💼
**X (Twitter)**: Black/white minimal, 𝕏 icon

**Use Cases**:
- Account connection cards (platform icon + gradient background)
- Analytics drill-down (platform color accent)
- Publishing preview (platform-specific mockups)

## Design Tokens (Tailwind Config)

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#8b5cf6',
          secondary: '#f97316',
        },
        // ... other colors
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
    },
  },
};
```

## Resources

- **Color Tool**: [coolors.co](https://coolors.co/) - Generate palettes
- **Contrast Checker**: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Icons**: [Lucide Icons](https://lucide.dev/)
- **Font**: [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
- **Inspiration**: [Dribbble - SaaS Dashboards](https://dribbble.com/tags/saas-dashboard)

---

**Design is never done. Iterate based on user feedback and analytics.**
