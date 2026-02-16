"use client";

import { useTranslations } from "@/lib/i18n";

export default function AutomationsPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("automations.title")}</h1>
        <p className="text-sm text-muted">{t("automations.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Builder per automazioni safe (trigger, azioni, consensi) con policy X e audit log.
          Nessun workflow fittizio, solo configurazioni reali.
        </p>
      </section>
    </div>
  );
}
