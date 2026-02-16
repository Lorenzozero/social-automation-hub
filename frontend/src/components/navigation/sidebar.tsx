"use client";

import Link from "next/link";
import { clsx } from "clsx";
import { usePathname } from "next/navigation";
import { useTranslations } from "@/lib/i18n";

const navItems = [
  { href: "/dashboard", key: "dashboard" },
  { href: "/calendar", key: "calendar" },
  { href: "/content-studio", key: "content_studio" },
  { href: "/inbox", key: "inbox" },
  { href: "/analytics", key: "analytics" },
  { href: "/automations", key: "automations" },
  { href: "/accounts", key: "accounts" },
  { href: "/settings", key: "settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const t = useTranslations();

  return (
    <aside className="hidden md:flex md:flex-col w-64 border-r border-border bg-surface/80 backdrop-blur-sm">
      <div className="px-4 py-4 border-b border-border">
        <p className="text-xs uppercase tracking-[0.25em] text-brand-secondary/70 mb-1">
          Creator Hub
        </p>
        <p className="font-semibold text-foreground">Social Automation Hub</p>
      </div>
      <nav className="flex-1 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "mx-2 flex items-center rounded-full px-3 py-2 text-sm text-muted hover:bg-muted transition",
              pathname?.startsWith(item.href) && "bg-muted/70 text-foreground font-medium"
            )}
          >
            {t(`nav.${item.key}` as any)}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
