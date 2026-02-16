"use client";

import { StatCard } from "@/components/common/stat-card";
import { useTranslations } from "@/lib/i18n";

export default function DashboardPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("dashboard.title")}</h1>
        <p className="text-sm text-muted">{t("dashboard.subtitle")}</p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard label={t("dashboard.reach_24h")} value="–" hint={t("dashboard.no_data")} />
        <StatCard label={t("dashboard.impressions_7d")} value="–" hint={t("dashboard.connect_account")} />
        <StatCard label={t("dashboard.followers_delta")} value="–" hint={t("dashboard.shows_variation")} />
      </section>

      <section className="card min-h-[220px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          {t("dashboard.subtitle")}
        </p>
      </section>
    </div>
  );
}
