import Link from "next/link";
import { clsx } from "clsx";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/calendar", label: "Calendario" },
  { href: "/automations", label: "Automazioni" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex md:flex-col w-64 border-r border-slate-800/70 bg-slate-950/80 backdrop-blur-sm">
      <div className="px-4 py-4 border-b border-slate-800/70">
        <p className="text-xs uppercase tracking-[0.25em] text-brand-secondary/70 mb-1">
          Creator Hub
        </p>
        <p className="font-semibold">Social Automation Hub</p>
      </div>
      <nav className="flex-1 py-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "mx-2 flex items-center rounded-full px-3 py-2 text-sm text-slate-300 hover:bg-slate-900/70 transition", 
              pathname?.startsWith(item.href) && "bg-slate-900 text-slate-50"
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
