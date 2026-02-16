"use client";

import Link from "next/link";
import { useState } from "react";

export default function OnboardingGuidePage() {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    {
      title: "Welcome to Social Automation Hub",
      description: "Your all-in-one platform for multi-social orchestration, built for professionals.",
      icon: "👋",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted leading-relaxed">
            Social Automation Hub is an open-source platform designed for influencers, creators, and agencies
            to manage Instagram, TikTok, LinkedIn, and X from a unified dashboard.
          </p>
          <ul className="space-y-2 text-sm text-muted">
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">✓</span>
              <span>Real-time KPIs and analytics across all platforms</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">✓</span>
              <span>AI-powered content creation with approval workflows</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">✓</span>
              <span>Safe automations with consent and audit trails</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">✓</span>
              <span>No mock data – only real integrations</span>
            </li>
          </ul>
        </div>
      ),
    },
    {
      title: "Connect Your First Account",
      description: "Link Instagram, TikTok, LinkedIn, or X to start monitoring.",
      icon: "🔗",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted leading-relaxed">
            Navigate to <strong className="text-foreground">Accounts</strong> from the sidebar and click
            <strong className="text-foreground"> Connect Account</strong>. You'll be guided through the OAuth flow
            for each platform.
          </p>
          <div className="rounded-xl border border-border bg-surface p-4 space-y-3">
            <div className="flex items-center gap-3">
              <span className="text-2xl">📸</span>
              <div>
                <p className="text-sm font-semibold text-foreground">Instagram</p>
                <p className="text-xs text-muted">Professional accounts only, 100 posts/24h via API</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">🎵</span>
              <div>
                <p className="text-sm font-semibold text-foreground">TikTok</p>
                <p className="text-xs text-muted">Creator info + content posting with UX consent</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">💼</span>
              <div>
                <p className="text-sm font-semibold text-foreground">LinkedIn</p>
                <p className="text-xs text-muted">UGC posts + member/org social permissions</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-2xl">𝕏</span>
              <div>
                <p className="text-sm font-semibold text-foreground">X (Twitter)</p>
                <p className="text-xs text-muted">POST /2/tweets with transparent automation rules</p>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: "Explore the Dashboard",
      description: "Monitor KPIs, schedule posts, and manage automations.",
      icon: "📊",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted leading-relaxed">
            Once accounts are connected, your dashboard will populate with real-time metrics:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="rounded-xl border border-border bg-surface p-4">
              <p className="text-sm font-semibold text-foreground mb-1">📊 Dashboard</p>
              <p className="text-xs text-muted">Reach, impressions, followers delta in real-time</p>
            </div>
            <div className="rounded-xl border border-border bg-surface p-4">
              <p className="text-sm font-semibold text-foreground mb-1">📅 Calendar</p>
              <p className="text-xs text-muted">Schedule posts with drag&drop across platforms</p>
            </div>
            <div className="rounded-xl border border-border bg-surface p-4">
              <p className="text-sm font-semibold text-foreground mb-1">✨ Content Studio</p>
              <p className="text-xs text-muted">AI-powered multi-variant content with approval</p>
            </div>
            <div className="rounded-xl border border-border bg-surface p-4">
              <p className="text-sm font-semibold text-foreground mb-1">💬 Inbox</p>
              <p className="text-xs text-muted">Unified comments/DM management with AI priority</p>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: "Set Up Safe Automations",
      description: "Create workflows with consent, opt-out, and full audit trails.",
      icon: "⚙️",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted leading-relaxed">
            Navigate to <strong className="text-foreground">Automations</strong> to build trigger-based workflows.
            All automations are transparent and comply with platform policies (especially X's automation rules).
          </p>
          <div className="rounded-xl border border-brand-primary/20 bg-brand-primary/5 p-4">
            <p className="text-sm font-semibold text-brand-primary mb-2">⚠️ Compliance First</p>
            <p className="text-xs text-muted leading-relaxed">
              For X: explicit consent required, immediate opt-out, no silent posting.
              For Instagram: 100 posts/24h limit via API.
              For TikTok: UX consent + creator nickname display.
            </p>
          </div>
        </div>
      ),
    },
    {
      title: "You're All Set!",
      description: "Start creating, scheduling, and analyzing your social presence.",
      icon: "🎉",
      content: (
        <div className="space-y-4">
          <p className="text-sm text-muted leading-relaxed">
            You're ready to use Social Automation Hub professionally. Remember:
          </p>
          <ul className="space-y-2 text-sm text-muted">
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">→</span>
              <span>All data is real – no mock numbers or fake insights</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">→</span>
              <span>Automations require approval and consent</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">→</span>
              <span>Full audit logs for compliance and transparency</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-brand-primary">→</span>
              <span>Open-source and community-driven</span>
            </li>
          </ul>
          <div className="flex gap-3 mt-6">
            <Link href="/dashboard" className="btn-primary flex-1 text-center">
              Go to Dashboard
            </Link>
            <Link href="/accounts" className="btn-secondary flex-1 text-center">
              Connect Account
            </Link>
          </div>
        </div>
      ),
    },
  ];

  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-3xl">
        <div className="card space-y-6 animate-slide-up">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-2xl shadow-lg shadow-brand-primary/30">
                {steps[currentStep].icon}
              </div>
              <div>
                <p className="text-xs text-muted font-medium">Step {currentStep + 1} of {steps.length}</p>
                <h2 className="text-xl font-bold text-foreground">{steps[currentStep].title}</h2>
              </div>
            </div>
          </div>

          <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-brand-primary to-brand-secondary transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>

          <p className="text-sm text-muted">{steps[currentStep].description}</p>

          <div className="min-h-[280px]">{steps[currentStep].content}</div>

          <div className="flex items-center justify-between pt-4">
            <button
              onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
              disabled={currentStep === 0}
              className="btn-secondary disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            {currentStep < steps.length - 1 ? (
              <button onClick={() => setCurrentStep(currentStep + 1)} className="btn-primary">
                Next Step
              </button>
            ) : (
              <Link href="/dashboard" className="btn-primary">
                Get Started
              </Link>
            )}
          </div>
        </div>

        <div className="mt-6 text-center">
          <Link href="/dashboard" className="text-xs text-muted hover:text-foreground transition-colors duration-200">
            Skip guide and go to dashboard →
          </Link>
        </div>
      </div>
    </div>
  );
}
