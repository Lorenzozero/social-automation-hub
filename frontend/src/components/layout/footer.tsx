"use client";

import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-border bg-surface/40 backdrop-blur-xl mt-auto">
      <div className="px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="h-8 w-8 rounded-xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-sm shadow-md">
                🚀
              </div>
              <p className="font-bold text-foreground">Social Automation Hub</p>
            </div>
            <p className="text-xs text-muted leading-relaxed">
              Open-source multi-social orchestration platform for influencers, creators, and agencies.
            </p>
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground mb-3">Resources</p>
            <ul className="space-y-2 text-xs text-muted">
              <li>
                <Link href="/docs" className="hover:text-foreground transition-colors duration-200">
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="/api" className="hover:text-foreground transition-colors duration-200">
                  API Reference
                </Link>
              </li>
              <li>
                <a
                  href="https://github.com/Lorenzozero/social-automation-hub"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors duration-200"
                >
                  GitHub Repository
                </a>
              </li>
            </ul>
          </div>
          <div>
            <p className="text-sm font-semibold text-foreground mb-3">Legal</p>
            <ul className="space-y-2 text-xs text-muted">
              <li>
                <Link href="/privacy" className="hover:text-foreground transition-colors duration-200">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-foreground transition-colors duration-200">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/compliance" className="hover:text-foreground transition-colors duration-200">
                  Platform Compliance
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-6 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted">© 2026 Social Automation Hub. MIT License.</p>
          <div className="flex items-center gap-4">
            <a href="https://github.com/Lorenzozero/social-automation-hub" target="_blank" rel="noopener noreferrer" className="text-muted hover:text-foreground transition-colors duration-200">
              <span className="text-lg">📦</span>
            </a>
            <a href="#" className="text-muted hover:text-foreground transition-colors duration-200">
              <span className="text-lg">🐦</span>
            </a>
            <a href="#" className="text-muted hover:text-foreground transition-colors duration-200">
              <span className="text-lg">💼</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
