import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark" | "system";
type Locale = "en" | "it";

type PreferencesStore = {
  theme: Theme;
  locale: Locale;
  setTheme: (theme: Theme) => void;
  setLocale: (locale: Locale) => void;
};

export const usePreferences = create<PreferencesStore>()(
  persist(
    (set) => ({
      theme: "dark",
      locale: "it",
      setTheme: (theme) => set({ theme }),
      setLocale: (locale) => set({ locale }),
    }),
    {
      name: "preferences-storage",
    }
  )
);
