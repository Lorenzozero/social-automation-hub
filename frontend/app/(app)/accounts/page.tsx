"use client";

export const dynamic = 'force-dynamic';

import { useTranslations } from "@/lib/i18n";
import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const WORKSPACE_ID = "00000000-0000-0000-0000-000000000001";

type Platform = "instagram" | "tiktok" | "linkedin" | "x";

interface PlatformConfig {
  name: string;
  icon: string;
  color: string;
  description: string;
}

const platforms: Record<Platform, PlatformConfig> = {
  instagram: {
    name: "Instagram",
    icon: "📸",
    color: "from-pink-500 to-purple-500",
    description: "Account professionali, 100 post/24h via API",
  },
  tiktok: {
    name: "TikTok",
    icon: "🎵",
    color: "from-cyan-400 to-pink-600",
    description: "Info creatore + pubblicazione con consenso UX",
  },
  linkedin: {
    name: "LinkedIn",
    icon: "💼",
    color: "from-blue-600 to-blue-800",
    description: "Post UGC + permessi social membro/org",
  },
  x: {
    name: "X (Twitter)",
    icon: "𝕏",
    color: "from-slate-700 to-slate-900",
    description: "POST /2/tweets con automazione trasparente",
  },
};

function AccountsContent() {
  const t = useTranslations();
  const searchParams = useSearchParams();
  const [notification, setNotification] = useState<{ type: "success" | "error"; message: string } | null>(null);

  useEffect(() => {
    const success = searchParams?.get("success");
    const error = searchParams?.get("error");

    if (success) {
      const platform = success.replace("_connected", "");
      setNotification({
        type: "success",
        message: `${platform.charAt(0).toUpperCase() + platform.slice(1)} collegato con successo!`,
      });
      setTimeout(() => setNotification(null), 5000);
    } else if (error) {
      setNotification({
        type: "error",
        message: `Connessione fallita: ${error.replace(/_/g, " ")}`,
      });
      setTimeout(() => setNotification(null), 5000);
    }
  }, [searchParams]);

  const handleConnect = (platform: Platform) => {
    const authorizeUrl = `${BACKEND_URL}/api/oauth/${platform}/authorize?workspace_id=${WORKSPACE_ID}`;
    window.location.href = authorizeUrl;
  };

  return (
    <div className="space-y-6">
      {notification && (
        <div
          className={`card animate-slide-up ${
            notification.type === "success"
              ? "bg-green-500/10 border-green-500/30"
              : "bg-red-500/10 border-red-500/30"
          }`}
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">{notification.type === "success" ? "✅" : "❌"}</span>
            <p className="text-sm font-medium text-foreground">{notification.message}</p>
          </div>
        </div>
      )}

      <section className="animate-fade-in">
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          {t("accounts.title")}
        </h1>
        <p className="text-sm text-muted">{t("accounts.subtitle")}</p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
        {(Object.keys(platforms) as Platform[]).map((platform) => {
          const config = platforms[platform];
          return (
            <div
              key={platform}
              className="card group hover:scale-[1.02] transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div
                    className={`h-14 w-14 rounded-2xl bg-gradient-to-br ${config.color} flex items-center justify-center text-2xl shadow-lg transition-transform duration-200 group-hover:scale-110`}
                  >
                    {config.icon}
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-foreground">{config.name}</h3>
                    <p className="text-xs text-muted">Non collegato</p>
                  </div>
                </div>
              </div>

              <p className="text-sm text-muted mb-4 leading-relaxed">{config.description}</p>

              <button
                onClick={() => handleConnect(platform)}
                className="w-full btn-primary flex items-center justify-center gap-2"
              >
                <span>🔗</span>
                <span>Collega {config.name}</span>
              </button>
            </div>
          );
        })}
      </section>
    </div>
  );
}

export default function AccountsPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><p className="text-muted">Caricamento...</p></div>}>
      <AccountsContent />
    </Suspense>
  );
}
