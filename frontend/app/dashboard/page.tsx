"use client";

import { StatCard } from "@/components/common/stat-card";
import { useTranslations } from "@/lib/i18n";
import { EmptyState } from "@/components/common/empty-state";
import { useState, useEffect } from "react";
import Link from "next/link";

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
    <div className="space-y-6 max-w-7xl mx-auto">
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
          <p className="text-muted animate-pulse">Loading metrics...</p>
        </div>
      ) : !metrics || metrics.accounts.length === 0 ? (
        <EmptyState
          icon="📊"
          title="No data yet"
          description="Connect your first social account to start seeing metrics."
          action={
            <Link href="/accounts" className="btn-primary mt-4">
              Connect Account
            </Link>
          }
        />
      ) : (
        <>
          <section className="grid grid-cols-1 md:grid-cols-4 gap-6 animate-fade-in stagger-1">
            <StatCard
              label="Total Followers"
              value={formatNumber(metrics.totals.followers)}
              hint={`${metrics.accounts.length} account${metrics.accounts.length !== 1 ? "s" : ""}`}
              trend="neutral"
            />
            <StatCard
              label={`Reach (${timeframe})`}
              value={formatNumber(metrics.totals.reach)}
              hint="Unique accounts reached"
              trend="up"
            />
            <StatCard
              label={`Impressions (${timeframe})`}
              value={formatNumber(metrics.totals.impressions)}
              hint="Total views"
              trend="up"
            />
            <StatCard
              label={`Engagement (${timeframe})`}
              value={formatNumber(metrics.totals.engagement)}
              hint="Likes + comments + shares"
              trend="up"
            />
          </section>

          <section className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in stagger-2">
            <Link href="/analytics/followers?type=new" className="card group hover:scale-[1.02] transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-foreground">New Followers</h3>
                <span className="text-2xl group-hover:scale-110 transition-transform">👋</span>
              </div>
              <p className="text-3xl font-bold text-green-500">
                +{metrics.follower_changes.new_followers}
              </p>
              <p className="text-xs text-muted mt-2">Last {timeframe}</p>
            </Link>

            <Link href="/analytics/followers?type=unfollowers" className="card group hover:scale-[1.02] transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-foreground">Unfollowers</h3>
                <span className="text-2xl group-hover:scale-110 transition-transform">👎</span>
              </div>
              <p className="text-3xl font-bold text-red-500">
                -{metrics.follower_changes.unfollowers}
              </p>
              <p className="text-xs text-muted mt-2">Last {timeframe}</p>
            </Link>

            <div className="card">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-foreground">Net Change</h3>
                <span className="text-2xl">📈</span>
              </div>
              <p className={`text-3xl font-bold ${metrics.follower_changes.net_change >= 0 ? "text-green-500" : "text-red-500"}`}>
                {metrics.follower_changes.net_change >= 0 ? "+" : ""}{metrics.follower_changes.net_change}
              </p>
              <p className="text-xs text-muted mt-2">Last {timeframe}</p>
            </div>
          </section>

          <section className="space-y-4 animate-fade-in stagger-3">
            <h3 className="text-lg font-semibold text-foreground">Connected Accounts</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {metrics.accounts.map((account) => (
                <Link
                  key={account.account_id}
                  href={`/analytics/account/${account.account_id}`}
                  className="card group hover:scale-[1.02] transition-all duration-200"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-xl">
                        {account.platform === "instagram" && "📸"}
                        {account.platform === "tiktok" && "🎵"}
                        {account.platform === "linkedin" && "💼"}
                        {account.platform === "x" && "𝕏"}
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-foreground">@{account.handle}</p>
                        <p className="text-xs text-muted capitalize">{account.platform}</p>
                      </div>
                    </div>
                    <span className="text-lg group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div>
                      <p className="text-xs text-muted">Followers</p>
                      <p className="text-sm font-bold text-foreground">{formatNumber(account.followers)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted">Reach</p>
                      <p className="text-sm font-bold text-foreground">{formatNumber(account.reach)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted">Engagement</p>
                      <p className="text-sm font-bold text-foreground">{formatNumber(account.engagement)}</p>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
