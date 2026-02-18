'use client';

import { ReactNode, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface ShellProps {
  children: ReactNode;
}

export function Shell({ children }: ShellProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Calendar', href: '/calendar', icon: '📅' },
    { name: 'Content Studio', href: '/content-studio', icon: '✨' },
    { name: 'Analytics', href: '/analytics', icon: '📈' },
    { name: 'Inbox', href: '/inbox', icon: '💬' },
    { name: 'Automations', href: '/automations', icon: '⚙️' },
    { name: 'Accounts', href: '/accounts', icon: '🔗' },
    { name: 'Settings', href: '/settings', icon: '⚡' },
  ];

  // Hide navigation on landing/login/onboarding pages
  const hideNav = ['/', '/login', '/onboarding'].some(path => pathname?.startsWith(path));

  if (hideNav) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile Header */}
      <header className="lg:hidden fixed top-0 left-0 right-0 z-50 bg-card border-b border-border backdrop-blur-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <Link href="/dashboard" className="font-bold text-lg">
            🎭 Social Hub
          </Link>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 hover:bg-surface rounded-lg transition-colors"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Mobile Sidebar */}
      <aside
        className={`lg:hidden fixed top-[57px] left-0 bottom-0 z-40 w-64 bg-card border-r border-border transform transition-transform duration-300 ease-in-out ${
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <nav className="p-4 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-brand-primary text-white font-medium'
                    : 'hover:bg-surface text-foreground'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Desktop Sidebar */}
      <aside className="hidden lg:block fixed top-0 left-0 bottom-0 w-64 bg-card border-r border-border">
        <div className="p-6">
          <Link href="/dashboard" className="font-bold text-xl flex items-center gap-2">
            <span>🎭</span>
            <span>Social Hub</span>
          </Link>
        </div>
        <nav className="px-4 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-brand-primary text-white font-medium'
                    : 'hover:bg-surface text-foreground'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 pt-[57px] lg:pt-0">
        <div className="p-4 md:p-6 lg:p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
