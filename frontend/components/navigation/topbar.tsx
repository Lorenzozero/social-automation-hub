"use client";

import { Bell, Search, Moon, Sun } from "lucide-react";
import { usePreferences } from "@/store/preferences";

export function Topbar() {
  const { theme, setTheme } = usePreferences();

  return (
    <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex-1 max-w-xl">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" size={18} />
          <input
            type="text"
            placeholder="Cerca..."
            className="w-full pl-10 pr-4 py-2 bg-surface border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-primary text-sm text-foreground placeholder:text-muted"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-2 ml-6">
        <button className="relative p-2 hover:bg-surface rounded-xl transition-colors">
          <Bell size={20} className="text-muted" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full" />
        </button>
        
        <button
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          className="p-2 hover:bg-surface rounded-xl transition-colors"
        >
          {theme === 'dark' ? (
            <Moon size={20} className="text-muted" />
          ) : (
            <Sun size={20} className="text-muted" />
          )}
        </button>
      </div>
    </header>
  );
}

export default Topbar;
