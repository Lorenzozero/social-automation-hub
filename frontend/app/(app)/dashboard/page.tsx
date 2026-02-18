"use client";

import { StatCard } from "@/components/common/stat-card";
import { useTranslations } from "@/lib/i18n";
import { EmptyState } from "@/components/common/empty-state";
import { useState, useEffect } from "react";
import Link from "next/link";
import { BarChart3 } from "lucide-react";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const WORKSPACE_ID = "00000000-0000-0000-0000-000000000001";

interface DashboardMetrics {
  totals: {
    followers: number;
    reach: number;
    impressions: number;
    engagement: number;
  };
  follower_changes: {
    new_followers: number;
    unfollowers: number;
    net_change: number;
  };
  accounts: Array<{
    account_id: string;
    platform: string;
    handle: string;
    followers: number;
    reach: number;
    impressions: number;
    engagement: number;
  }>;
}

export default function DashboardPage() {
  const t = useTranslations();
  const [timeframe, setTimeframe] = useState("24h");
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, [timeframe]);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/oauth/analytics/dashboard/${WORKSPACE_ID}?timeframe=${timeframe}`);
      if (res.ok) {
        const data = await res.json();
        setMetrics(data);
      }
    } catch (error) {
      console.error("Failed to fetch metrics:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="space-y-6">
      <section className="animate-fade-in flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            {t("dashboard.title")}
          </h1>
          <p className="text-sm text-muted">{t("dashboard.subtitle")}</p>
        </div>
        <div className="flex gap-2">
          {["24h", "7d", "30d", "90d"].map((tf) => (
            <button
              key={tf}
              onClick={() => setTimeframe(tf)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                timeframe === tf
                  ? "bg-brand-primary text-white shadow-lg"
                  : "bg-surface text-muted hover:bg-muted"
              }`}
            >
              {tf.toUpperCase()}
            </button>
          ))}
        </div>
      </section>

      {loading ? (
        <div className="card min-h-[200px] flex items-center justify-center">
          <p className="text-muted animate-pulse">Caricamento metriche...</p>
        </div>
      ) : !metrics || metrics.accounts.length === 0 ? (
        <EmptyState
          icon={BarChart3}
          title="Nessun dato disponibile"
          description="Collega il tuo primo account social per iniziare a vedere le metriche."
        />
      ) : (
        <>
          <section className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-fade-in">
            <StatCard
              title="Follower Totali"
              value={formatNumber(metrics.totals.followers)}
              change={`${metrics.accounts.length} account`}
            />
            <StatCard
              title={`Reach (${timeframe})`}
              value={formatNumber(metrics.totals.reach)}
              change="Account unici raggiunti"
            />
            <StatCard
              title={`Impressioni (${timeframe})`}
              value={formatNumber(metrics.totals.impressions)}
              change="Visualizzazioni totali"
            />
            <StatCard
              title={`Engagement (${timeframe})`}
              value={formatNumber(metrics.totals.engagement)}
              change="Like + commenti + condivisioni"
            />
          </section>
        </>
      )}
    </div>
  );
}
