"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

export default function SettingsPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section className="animate-fade-in">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          {t("settings.title")}
        </h1>
        <p className="text-sm text-muted">{t("settings.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Impostazioni workspace, gestione team, API keys, e preferenze notifiche.
        </p>
      </section>
    </div>
  );
}
