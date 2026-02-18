import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Theme = 'light' | 'dark' | 'system';
export type Language = 'en' | 'it' | 'es' | 'fr' | 'de';

interface PreferencesState {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  language: Language;
  setLanguage: (language: Language) => void;
  notificationsEnabled: boolean;
  setNotificationsEnabled: (enabled: boolean) => void;
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  refreshInterval: number;
  setRefreshInterval: (interval: number) => void;
}

export const usePreferences = create<PreferencesState>()(persist(
  (set) => ({
    theme: 'system',
    setTheme: (theme) => set({ theme }),
    language: 'en',
    setLanguage: (language) => set({ language }),
    notificationsEnabled: true,
    setNotificationsEnabled: (enabled) => set({ notificationsEnabled: enabled }),
    sidebarCollapsed: false,
    toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
    setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
    refreshInterval: 300,
    setRefreshInterval: (interval) => set({ refreshInterval: interval }),
  }),
  {
    name: 'user-preferences',
  }
));
