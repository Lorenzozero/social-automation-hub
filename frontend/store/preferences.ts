import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Theme = 'light' | 'dark' | 'system';
export type Language = 'en' | 'it' | 'es' | 'fr' | 'de';

interface PreferencesState {
  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;
  
  // Language
  language: Language;
  setLanguage: (language: Language) => void;
  
  // Notifications
  notificationsEnabled: boolean;
  setNotificationsEnabled: (enabled: boolean) => void;
  
  // Sidebar
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  
  // Data refresh interval (seconds)
  refreshInterval: number;
  setRefreshInterval: (interval: number) => void;
}

export const usePreferences = create<PreferencesState>()(persist(
  (set) => ({
    // Theme defaults
    theme: 'system',
    setTheme: (theme) => set({ theme }),
    
    // Language defaults
    language: 'en',
    setLanguage: (language) => set({ language }),
    
    // Notifications defaults
    notificationsEnabled: true,
    setNotificationsEnabled: (enabled) => set({ notificationsEnabled: enabled }),
    
    // Sidebar defaults
    sidebarCollapsed: false,
    toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
    setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    
    // Refresh interval defaults (5 minutes)
    refreshInterval: 300,
    setRefreshInterval: (interval) => set({ refreshInterval: interval }),
  }),
  {
    name: 'user-preferences',
  }
));
