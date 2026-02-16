"use client";

import { useTranslations } from "@/lib/i18n";

export default function ContentStudioPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("content_studio.title")}</h1>
        <p className="text-sm text-muted">{t("content_studio.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Brief → AI multi-variante per copy + adattamento per piattaforma (IG, TikTok, LinkedIn, X).
          L'utente approva prima del publish.
        </p>
      </section>
    </div>
  );
}
