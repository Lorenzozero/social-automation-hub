"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const WORKSPACE_ID = "00000000-0000-0000-0000-000000000001";

interface Automation {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  trigger: any;
  actions: any[];
  consent_required: boolean;
  runs_count?: number;
  last_run?: string;
}

export default function AutomationsPage() {
  const [automations, setAutomations] = useState<Automation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Placeholder: would fetch from API
    setAutomations([]);
    setLoading(false);
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            ⚙️ Automations
          </h1>
          <p className="text-sm text-muted">Create safe, consent-driven workflows</p>
        </div>
        <Link href="/automations/new" className="btn-primary">
          + New Automation
        </Link>
      </section>

      {loading ? (
        <div className="card min-h-[200px] flex items-center justify-center">
          <p className="text-muted animate-pulse">Loading...</p>
        </div>
      ) : automations.length === 0 ? (
        <div className="card text-center py-12">
          <span className="text-6xl mb-4 block">🤖</span>
          <h3 className="text-lg font-semibold text-foreground mb-2">No automations yet</h3>
          <p className="text-sm text-muted mb-6">
            Create your first automation to streamline your workflow
          </p>
          <Link href="/automations/new" className="btn-primary inline-block">
            Create Automation
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {automations.map((automation) => (
            <div key={automation.id} className="card hover:scale-[1.01] transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div
                    className={`h-3 w-3 rounded-full ${
                      automation.enabled ? "bg-green-500 animate-pulse" : "bg-gray-400"
                    }`}
                  />
                  <h3 className="text-base font-semibold text-foreground">{automation.name}</h3>
                  {automation.consent_required && (
                    <span className="text-xs px-2 py-0.5 rounded-md bg-yellow-500/10 text-yellow-600 border border-yellow-500/20">
                      Consent Required
                    </span>
                  )}
                </div>
                <button className="text-sm text-muted hover:text-foreground">⋯</button>
              </div>
              
              <p className="text-sm text-muted mb-4">{automation.description}</p>
              
              <div className="flex items-center gap-4 text-xs text-muted">
                <span>🔥 {automation.runs_count || 0} runs</span>
                {automation.last_run && <span>🕒 Last run: {automation.last_run}</span>}
              </div>
            </div>
          ))}
        </div>
      )}

      <section className="card bg-gradient-to-r from-brand-primary/10 to-brand-secondary/10 border-brand-primary/20">
        <h3 className="text-base font-semibold text-foreground mb-2">💡 Automation Ideas</h3>
        <ul className="space-y-2 text-sm text-muted">
          <li>• <strong>Welcome new followers:</strong> Auto-create thank you story draft when you gain 50+ followers</li>
          <li>• <strong>Engagement spike alert:</strong> Get notified when a post reaches 10K impressions</li>
          <li>• <strong>Content reminder:</strong> Request approval for next week's content every Friday</li>
          <li>• <strong>Unfollower analysis:</strong> Create report when you lose 20+ followers in a day</li>
        </ul>
      </section>
    </div>
  );
}
