'use client';

import { ReactNode, useEffect, useState } from 'react';

interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load theme from localStorage or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const theme = savedTheme || systemTheme;
    
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, []);

  // Prevent flash of unstyled content
  if (!mounted) {
    return <div className="opacity-0">{children}</div>;
  }

  return <>{children}</>;
}
