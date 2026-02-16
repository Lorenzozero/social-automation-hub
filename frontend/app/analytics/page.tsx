"use client";

import { useTranslations } from "@/lib/i18n";

export default function AnalyticsPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("analytics.title")}</h1>
        <p className="text-sm text-muted">{t("analytics.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Grafici interattivi con trend temporali, breakdown per piattaforma e KPI custom.
          Solo metriche da API reali (IG, TikTok, LinkedIn, X).
        </p>
      </section>
    </div>
  );
}
