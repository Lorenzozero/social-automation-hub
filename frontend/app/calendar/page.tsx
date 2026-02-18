"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

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
          Monthly calendar view with scheduled posts, drag-and-drop rescheduling, and AI timing recommendations.
        </p>
      </section>
    </div>
  );
}
