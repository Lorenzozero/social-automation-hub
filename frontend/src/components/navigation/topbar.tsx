"use client";

import { useTranslations } from "@/lib/i18n";
import { usePreferences } from "@/store/preferences";

export function Topbar() {
  const t = useTranslations();
  const { theme, setTheme } = usePreferences();

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-border bg-surface/60 backdrop-blur-xl sticky top-0 z-50 animate-fade-in">
      <div className="flex items-center gap-4">
        <div>
          <p className="text-xs text-muted font-medium">Active Workspace</p>
          <p className="text-sm font-semibold text-foreground">My Creator Space</p>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="h-10 w-10 rounded-xl bg-muted hover:bg-muted/70 flex items-center justify-center transition-all duration-200 hover:scale-110 active:scale-95"
          aria-label="Toggle theme"
        >
          <span className="text-lg">{theme === "dark" ? "🌙" : "☀️"}</span>
        </button>
        <button className="h-10 w-10 rounded-xl bg-muted hover:bg-muted/70 flex items-center justify-center transition-all duration-200 hover:scale-110 active:scale-95">
          <span className="text-lg">🔔</span>
        </button>
        <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center font-bold text-white shadow-lg shadow-brand-primary/30 cursor-pointer transition-all duration-200 hover:scale-110 active:scale-95">
          LZ
        </div>
      </div>
    </header>
  );
}
