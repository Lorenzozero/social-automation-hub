"use client";

import { useState } from "react";
import { Plus, Play, Pause, Trash2, Copy, Edit, Zap } from "lucide-react";
import Link from "next/link";

interface AutomationNode {
  id: string;
  type: "trigger" | "condition" | "action";
  label: string;
  config: any;
}

interface Automation {
  id: string;
  name: string;
  enabled: boolean;
  nodes: AutomationNode[];
  lastRun?: string;
  executions: number;
}

const mockAutomations: Automation[] = [
  {
    id: "1",
    name: "Welcome New Followers",
    enabled: true,
    nodes: [
      { id: "t1", type: "trigger", label: "New Follower", config: {} },
      { id: "a1", type: "action", label: "Send DM", config: {} },
    ],
    lastRun: "2026-02-16T10:30:00Z",
    executions: 234,
  },
  {
    id: "2",
    name: "Auto-Publish Monday Motivation",
    enabled: true,
    nodes: [
      { id: "t2", type: "trigger", label: "Schedule: Mon 8:00", config: {} },
      { id: "a2", type: "action", label: "Create Draft", config: {} },
      { id: "a3", type: "action", label: "Request Approval", config: {} },
    ],
    lastRun: "2026-02-16T08:00:00Z",
    executions: 52,
  },
  {
    id: "3",
    name: "Alert Low Engagement",
    enabled: false,
    nodes: [
      { id: "t3", type: "trigger", label: "Engagement < 5%", config: {} },
      { id: "c1", type: "condition", label: "If Last 3 Posts", config: {} },
      { id: "a4", type: "action", label: "Send Notification", config: {} },
    ],
    lastRun: "2026-02-15T18:20:00Z",
    executions: 3,
  },
];

export default function AutomationsPage() {
  const [automations, setAutomations] = useState(mockAutomations);

  const toggleAutomation = (id: string) => {
    setAutomations(
      automations.map((auto) =>
        auto.id === id ? { ...auto, enabled: !auto.enabled } : auto
      )
    );
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            Automations
          </h1>
          <p className="text-sm text-muted">
            Crea workflow automatici con trigger, condizioni e azioni
          </p>
        </div>
        <Link href="/automations/builder" className="btn-primary flex items-center gap-2">
          <Plus size={20} />
          Nuova Automation
        </Link>
      </section>

      <div className="card bg-warning-bg border border-warning">
        <div className="flex items-start gap-3">
          <Zap size={20} className="text-warning mt-0.5" />
          <div>
            <h3 className="text-sm font-semibold text-foreground mb-1">Compliance Note</h3>
            <p className="text-xs text-foreground-secondary">
              Per X (Twitter): tutte le automazioni richiedono{" "}
              <strong>consenso esplicito</strong> dell&apos;utente con opzione opt-out immediata.
              Automazioni &quot;silent&quot; violano le policy e possono causare ban.
            </p>
          </div>
        </div>
      </div>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card">
          <div className="text-center">
            <p className="text-3xl font-bold text-brand-primary">
              {automations.filter((a) => a.enabled).length}
            </p>
            <p className="text-sm text-muted mt-1">Attive</p>
          </div>
        </div>
        <div className="card">
          <div className="text-center">
            <p className="text-3xl font-bold text-foreground">
              {automations.reduce((sum, a) => sum + a.executions, 0)}
            </p>
            <p className="text-sm text-muted mt-1">Esecuzioni Totali</p>
          </div>
        </div>
        <div className="card">
          <div className="text-center">
            <p className="text-3xl font-bold text-muted">
              {automations.filter((a) => !a.enabled).length}
            </p>
            <p className="text-sm text-muted mt-1">Pause</p>
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-foreground">Le Tue Automations</h2>
        {automations.map((automation) => (
          <div
            key={automation.id}
            className="card hover:shadow-lg transition-shadow duration-200"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <button
                  onClick={() => toggleAutomation(automation.id)}
                  className={`h-10 w-10 rounded-xl flex items-center justify-center transition-all duration-200 ${
                    automation.enabled
                      ? "bg-success text-white"
                      : "bg-muted text-foreground-secondary"
                  }`}
                >
                  {automation.enabled ? <Play size={20} /> : <Pause size={20} />}
                </button>
                <div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {automation.name}
                  </h3>
                  <p className="text-xs text-muted">
                    {automation.executions} esecuzioni · Last run:{" "}
                    {automation.lastRun ? formatDate(automation.lastRun) : "Never"}
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="p-2 rounded-lg bg-surface hover:bg-muted transition-colors text-foreground-secondary hover:text-foreground">
                  <Edit size={16} />
                </button>
                <button className="p-2 rounded-lg bg-surface hover:bg-muted transition-colors text-foreground-secondary hover:text-foreground">
                  <Copy size={16} />
                </button>
                <button className="p-2 rounded-lg bg-surface hover:bg-error-bg transition-colors text-foreground-secondary hover:text-error">
                  <Trash2 size={16} />
                </button>
              </div>
            </div>

            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              {automation.nodes.map((node, idx) => (
                <div key={node.id} className="flex items-center gap-2">
                  <div
                    className={`px-4 py-2 rounded-xl text-xs font-medium whitespace-nowrap ${
                      node.type === "trigger"
                        ? "bg-brand-primary text-white"
                        : node.type === "condition"
                        ? "bg-warning text-white"
                        : "bg-brand-secondary text-white"
                    }`}
                  >
                    {node.label}
                  </div>
                  {idx < automation.nodes.length - 1 && (
                    <div className="text-muted">→</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </section>

      <section className="card bg-info-bg border border-info">
        <h3 className="text-lg font-semibold text-foreground mb-3">
          Template Automation Popolari
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button className="p-4 rounded-xl bg-background hover:bg-surface transition-colors text-left border border-muted">
            <h4 className="text-sm font-semibold text-foreground mb-1">
              Auto-Repost Best Performers
            </h4>
            <p className="text-xs text-muted">
              Ripubblica automaticamente contenuti con engagement rate superiore al 10%
            </p>
          </button>
          <button className="p-4 rounded-xl bg-background hover:bg-surface transition-colors text-left border border-muted">
            <h4 className="text-sm font-semibold text-foreground mb-1">
              Content Reminder
            </h4>
            <p className="text-xs text-muted">
              Notifica se non hai pubblicato da 3+ giorni
            </p>
          </button>
          <button className="p-4 rounded-xl bg-background hover:bg-surface transition-colors text-left border border-muted">
            <h4 className="text-sm font-semibold text-foreground mb-1">
              Engagement Boost
            </h4>
            <p className="text-xs text-muted">
              Like automatico a commenti (con consenso esplicito)
            </p>
          </button>
          <button className="p-4 rounded-xl bg-background hover:bg-surface transition-colors text-left border border-muted">
            <h4 className="text-sm font-semibold text-foreground mb-1">
              Giveaway Winner Picker
            </h4>
            <p className="text-xs text-muted">
              Estrai vincitore random da commenti con mention amici
            </p>
          </button>
        </div>
      </section>
    </div>
  );
}
