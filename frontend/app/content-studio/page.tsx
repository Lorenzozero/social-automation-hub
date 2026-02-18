"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

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
          Editor visuale per post multi-piattaforma con preview in tempo reale, AI suggestions, e scheduling.
        </p>
      </section>
    </div>
  );
}
