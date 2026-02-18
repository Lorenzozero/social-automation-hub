"use client";

import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: LucideIcon;
}

export function StatCard({ title, value, change, changeType = 'neutral', icon: Icon }: StatCardProps) {
  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted mb-1">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
          {change && (
            <p
              className={`text-xs mt-2 ${
                changeType === 'positive'
                  ? 'text-success'
                  : changeType === 'negative'
                  ? 'text-error'
                  : 'text-muted'
              }`}
            >
              {change}
            </p>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-brand-primary/10 rounded-lg">
            <Icon size={24} className="text-brand-primary" />
          </div>
        )}
      </div>
    </div>
  );
}

export default StatCard;
