"use client";

export const dynamic = 'force-dynamic';

import { useSearchParams } from "next/navigation";
import { useState, useEffect } from "react";
import Link from "next/link";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

interface FollowerChange {
  id: string;
  user_id: string;
  username: string;
  profile_pic_url?: string;
  verified: boolean;
  follower_count?: number;
  timestamp: string;
}

export default function FollowersPage() {
  const searchParams = useSearchParams();
  const type = searchParams?.get("type") || "new";
  const accountId = searchParams?.get("account");
  
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!accountId) return;
    fetchFollowerChanges();
  }, [accountId, type]);

  const fetchFollowerChanges = async () => {
    setLoading(true);
    try {
      const changeType = type === "new" ? "new_follower" : "unfollower";
      const res = await fetch(`${BACKEND_URL}/api/oauth/analytics/follower-changes/${accountId}?type=${changeType}&limit=100`);
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (error) {
      console.error("Failed to fetch follower changes:", error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  if (!accountId) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <p className="text-muted text-center">Select an account from dashboard to view follower changes.</p>
          <Link href="/dashboard" className="btn-primary mt-4 mx-auto block w-fit">
            Go to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            {type === "new" ? "New Followers" : "Unfollowers"}
          </h1>
          {data && (
            <p className="text-sm text-muted">
              @{data.handle} · {data.total} total {type === "new" ? "new followers" : "unfollowers"}
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <Link
            href={`/analytics/followers?type=new&account=${accountId}`}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
              type === "new" ? "bg-brand-primary text-white" : "bg-surface text-muted hover:bg-muted"
            }`}
          >
            👋 New
          </Link>
          <Link
            href={`/analytics/followers?type=unfollowers&account=${accountId}`}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
              type === "unfollowers" ? "bg-brand-primary text-white" : "bg-surface text-muted hover:bg-muted"
            }`}
          >
            👎 Unfollowers
          </Link>
        </div>
      </section>

      {loading ? (
        <div className="card min-h-[200px] flex items-center justify-center">
          <p className="text-muted animate-pulse">Loading...</p>
        </div>
      ) : !data || data.results.length === 0 ? (
        <div className="card">
          <p className="text-muted text-center">No {type === "new" ? "new followers" : "unfollowers"} yet.</p>
        </div>
      ) : (
        <div className="card space-y-3">
          {data.results.map((change: FollowerChange) => (
            <div
              key={change.id}
              className="flex items-center justify-between p-3 rounded-xl bg-surface hover:bg-muted transition-all duration-200"
            >
              <div className="flex items-center gap-3">
                <div className="h-12 w-12 rounded-full bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-white font-bold">
                  {change.username[0]?.toUpperCase() || "?"}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-semibold text-foreground">@{change.username}</p>
                    {change.verified && <span className="text-blue-500">✓</span>}
                  </div>
                  <p className="text-xs text-muted">
                    {change.follower_count ? `${change.follower_count.toLocaleString()} followers` : "Unknown followers"} · {formatDate(change.timestamp)}
                  </p>
                </div>
              </div>
              <a
                href={`https://instagram.com/${change.username}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary text-xs px-3 py-1.5"
              >
                View Profile
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
