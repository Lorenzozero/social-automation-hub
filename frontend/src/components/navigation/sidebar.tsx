"use client";

import Link from "next/link";
import { clsx } from "clsx";
import { usePathname } from "next/navigation";
import { useTranslations } from "@/lib/i18n";

const navItems = [
  { href: "/dashboard", key: "dashboard", icon: "📊" },
  { href: "/calendar", key: "calendar", icon: "📅" },
  { href: "/content-studio", key: "content_studio", icon: "✨" },
  { href: "/inbox", key: "inbox", icon: "💬" },
  { href: "/analytics", key: "analytics", icon: "📈" },
  { href: "/automations", key: "automations", icon: "⚙️" },
  { href: "/accounts", key: "accounts", icon: "🔗" },
  { href: "/settings", key: "settings", icon: "⚡" },
];

export function Sidebar() {
  const pathname = usePathname();
  const t = useTranslations();

  return (
    <aside className="hidden md:flex md:flex-col w-72 border-r border-border bg-surface/80 backdrop-blur-xl animate-slide-in">
      <div className="px-6 py-6 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-xl shadow-lg shadow-brand-primary/30">
            🚀
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-brand-secondary/70 font-semibold">
              Creator Hub
            </p>
            <p className="font-bold text-foreground text-lg">Social Hub</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 py-6 space-y-2 overflow-y-auto px-3">
        {navItems.map((item, idx) => (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-all duration-200",
              pathname?.startsWith(item.href)
                ? "bg-gradient-to-r from-brand-primary/20 to-brand-secondary/10 text-foreground shadow-sm border border-brand-primary/20"
                : "text-muted hover:bg-muted hover:text-foreground hover:scale-[1.02]"
            )}
            style={{ animationDelay: `${idx * 50}ms` }}
          >
            <span className="text-xl transition-transform duration-200 group-hover:scale-110">{item.icon}</span>
            <span>{t(`nav.${item.key}` as any)}</span>
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-border">
        <div className="rounded-2xl bg-gradient-to-br from-brand-primary/10 to-brand-secondary/10 p-4 border border-brand-primary/20">
          <p className="text-xs font-semibold text-brand-primary mb-1">💡 Pro Tip</p>
          <p className="text-xs text-muted leading-relaxed">
            Connect your first social account to start seeing real-time insights.
          </p>
        </div>
      </div>
    </aside>
  );
}
