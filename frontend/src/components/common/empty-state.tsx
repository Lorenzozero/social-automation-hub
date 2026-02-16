"use client";

import type { ReactNode } from "react";

type EmptyStateProps = {
  icon: string;
  title: string;
  description: string;
  action?: ReactNode;
  compact?: boolean;
};

export function EmptyState({ icon, title, description, action, compact = false }: EmptyStateProps) {
  return (
    <div className={`flex flex-col items-center justify-center text-center ${compact ? 'py-8' : 'py-12'}`}>
      <div className={`${compact ? 'text-4xl' : 'text-6xl'} mb-4 opacity-40 animate-pulse`}>
        {icon}
      </div>
      <h3 className={`${compact ? 'text-base' : 'text-lg'} font-semibold text-foreground mb-2`}>
        {title}
      </h3>
      <p className={`${compact ? 'text-xs' : 'text-sm'} text-muted max-w-md`}>
        {description}
      </p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
