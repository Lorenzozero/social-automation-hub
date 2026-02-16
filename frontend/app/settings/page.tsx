"use client";

import { useTranslations } from "@/lib/i18n";
import { usePreferences } from "@/store/preferences";

export default function SettingsPage() {
  const t = useTranslations();
  const { theme, locale, setTheme, setLocale } = usePreferences();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("settings.title")}</h1>
        <p className="text-sm text-muted">{t("settings.subtitle")}</p>
      </section>

      <section className="card space-y-6">
        <div>
          <h2 className="text-lg font-medium mb-3">{t("settings.appearance")}</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">{t("settings.theme")}</label>
              <div className="flex gap-2">
                {["light", "dark", "system"].map((th) => (
                  <button
                    key={th}
                    onClick={() => setTheme(th as any)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                      theme === th
                        ? "bg-brand-primary text-white shadow-lg shadow-brand-primary/40"
                        : "bg-surface border border-border text-foreground hover:bg-muted"
                    }`}
                  >
                    {t(`settings.${th}` as any)}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">{t("settings.language")}</label>
              <div className="flex gap-2">
                {["en", "it"].map((loc) => (
                  <button
                    key={loc}
                    onClick={() => setLocale(loc as any)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                      locale === loc
                        ? "bg-brand-primary text-white shadow-lg shadow-brand-primary/40"
                        : "bg-surface border border-border text-foreground hover:bg-muted"
                    }`}
                  >
                    {loc.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
