"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

export default function InboxPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">{t("inbox.title")}</h1>
        <p className="text-sm text-muted">{t("inbox.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Unified inbox for comments, DMs, and mentions from all connected social accounts.
        </p>
      </section>
    </div>
  );
}
