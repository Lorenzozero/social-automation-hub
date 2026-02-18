"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

export default function AutomationsPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section className="animate-fade-in">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          {t("automations.title")}
        </h1>
        <p className="text-sm text-muted">{t("automations.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Workflow n8n per auto-pubblicazione, riuso contenuti, e automazione engagement.
        </p>
      </section>
    </div>
  );
}
