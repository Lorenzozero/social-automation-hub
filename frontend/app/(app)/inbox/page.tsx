"use client";

import { useTranslations } from "@/lib/i18n";

export const dynamic = 'force-dynamic';

export default function InboxPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <section className="animate-fade-in">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          {t("inbox.title")}
        </h1>
        <p className="text-sm text-muted">{t("inbox.subtitle")}</p>
      </section>

      <section className="card min-h-[400px] flex items-center justify-center">
        <p className="text-sm text-muted max-w-md text-center">
          Inbox unificata per commenti, DM, e menzioni da tutti gli account social collegati.
        </p>
      </section>
    </div>
  );
}
