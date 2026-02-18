"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Calendar, FileText, BarChart3, Inbox, Zap, User, Settings } from "lucide-react";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Calendario", href: "/calendar", icon: Calendar },
  { name: "Contenuti", href: "/content-studio", icon: FileText },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Inbox", href: "/inbox", icon: Inbox },
  { name: "Automazioni", href: "/automations", icon: Zap },
  { name: "Account", href: "/accounts", icon: User },
  { name: "Impostazioni", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-card border-r border-border h-screen fixed left-0 top-0 flex flex-col">
      <div className="p-6 border-b border-border">
        <h1 className="text-xl font-bold bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          Social Hub
        </h1>
        <p className="text-xs text-muted mt-1">Automazione Social</p>
      </div>
      
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? "bg-gradient-to-r from-brand-primary to-brand-secondary text-white shadow-lg shadow-brand-primary/25"
                  : "text-muted hover:text-foreground hover:bg-surface"
              }`}
            >
              <Icon size={20} strokeWidth={2} />
              <span className="font-medium text-sm">{item.name}</span>
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 px-4 py-3 bg-surface rounded-xl">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-white font-bold text-sm">
            L
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-foreground truncate">Lorenzo</p>
            <p className="text-xs text-muted truncate">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
