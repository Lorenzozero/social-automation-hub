"use client";

import { useTranslations } from "@/lib/i18n";

export default function CalendarPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("calendar.title")}</h1>
        <p className="text-sm text-muted">{t("calendar.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Calendario editoriale con drag&drop sarà disponibile qui.
          Nessun post fittizio, solo contenuti schedulati da backend reale.
        </p>
      </section>
    </div>
  );
}
