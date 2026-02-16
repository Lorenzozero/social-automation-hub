"use client";

import { StatCard } from "@/components/common/stat-card";
import { useTranslations } from "@/lib/i18n";
import { EmptyState } from "@/components/common/empty-state";

export default function DashboardPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <section className="animate-fade-in">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          {t("dashboard.title")}
        </h1>
        <p className="text-sm text-muted">{t("dashboard.subtitle")}</p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in stagger-1">
        <StatCard label={t("dashboard.reach_24h")} value="–" hint={t("dashboard.no_data")} trend="neutral" />
        <StatCard label={t("dashboard.impressions_7d")} value="–" hint={t("dashboard.connect_account")} trend="neutral" />
        <StatCard label={t("dashboard.followers_delta")} value="–" hint={t("dashboard.shows_variation")} trend="neutral" />
      </section>

      <section className="card min-h-[320px] animate-fade-in stagger-2">
        <EmptyState
          icon="📊"
          title="Analytics Dashboard"
          description="Charts and insights will appear here once you connect your social accounts and start collecting real data from Instagram, TikTok, LinkedIn, and X."
          action={
            <button className="btn-primary mt-4">
              Connect First Account
            </button>
          }
        />
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in stagger-3">
        <div className="card">
          <h3 className="text-sm font-semibold text-foreground mb-4 flex items-center gap-2">
            <span>📅</span> Recent Activity
          </h3>
          <EmptyState
            icon="⏳"
            title="No activity yet"
            description="Your recent posts, automations, and engagement will be tracked here."
            compact
          />
        </div>
        <div className="card">
          <h3 className="text-sm font-semibold text-foreground mb-4 flex items-center gap-2">
            <span>🎯</span> Quick Actions
          </h3>
          <div className="space-y-3">
            <button className="w-full btn-secondary justify-start flex items-center gap-3">
              <span>✨</span>
              <span>Create Content</span>
            </button>
            <button className="w-full btn-secondary justify-start flex items-center gap-3">
              <span>📅</span>
              <span>Schedule Post</span>
            </button>
            <button className="w-full btn-secondary justify-start flex items-center gap-3">
              <span>🔗</span>
              <span>Connect Account</span>
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
