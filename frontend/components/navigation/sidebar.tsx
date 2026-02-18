"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Calendar, FileText, BarChart3, Inbox, Zap, User, Settings } from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  { name: "Calendar", href: "/calendar", icon: Calendar },
  { name: "Content", href: "/content-studio", icon: FileText },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Inbox", href: "/inbox", icon: Inbox },
  { name: "Automations", href: "/automations", icon: Zap },
  { name: "Accounts", href: "/accounts", icon: User },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-card border-r border-border h-screen fixed left-0 top-0 p-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          SocialHub
        </h1>
      </div>
      <nav className="space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? "bg-brand-primary text-white"
                  : "text-foreground hover:bg-surface"
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
