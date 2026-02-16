"use client";

import { useTranslations } from "@/lib/i18n";

export default function AccountsPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("accounts.title")}</h1>
        <p className="text-sm text-muted">{t("accounts.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Lista account collegati con stato OAuth, scope, rate-limit info, pulsanti connetti/scollega.
          Nessun account di esempio, solo veri collegati.
        </p>
      </section>
    </div>
  );
}
