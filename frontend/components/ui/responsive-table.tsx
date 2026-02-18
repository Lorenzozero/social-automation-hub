'use client';

import { ReactNode } from 'react';

interface Column<T> {
  key: keyof T | string;
  label: string;
  render?: (item: T) => ReactNode;
  className?: string;
  mobileHidden?: boolean; // Hide on mobile
}

interface ResponsiveTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (item: T) => void;
  loading?: boolean;
  emptyMessage?: string;
}

export function ResponsiveTable<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
  loading,
  emptyMessage = 'No data available'
}: ResponsiveTableProps<T>) {
  if (loading) {
    return (
      <div className="animate-pulse space-y-2">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-surface rounded-lg" />
        ))}
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="text-center py-12 text-muted">
        <p className="text-lg">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <>
      {/* Desktop Table */}
      <div className="hidden md:block overflow-x-auto rounded-lg border border-border">
        <table className="w-full">
          <thead className="bg-surface">
            <tr>
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  className={`px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider ${
                    col.className || ''
                  }`}
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {data.map((item, rowIdx) => (
              <tr
                key={rowIdx}
                onClick={() => onRowClick?.(item)}
                className={onRowClick ? 'cursor-pointer hover:bg-surface transition-colors' : ''}
              >
                {columns.map((col, colIdx) => (
                  <td key={colIdx} className={`px-6 py-4 whitespace-nowrap ${col.className || ''}`}>
                    {col.render ? col.render(item) : (item[col.key as keyof T] as ReactNode)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Cards */}
      <div className="md:hidden space-y-4">
        {data.map((item, idx) => (
          <div
            key={idx}
            onClick={() => onRowClick?.(item)}
            className={`bg-card border border-border rounded-lg p-4 space-y-3 ${
              onRowClick ? 'cursor-pointer active:scale-[0.98] transition-transform' : ''
            }`}
          >
            {columns
              .filter(col => !col.mobileHidden)
              .map((col, colIdx) => (
                <div key={colIdx} className="flex justify-between items-start gap-4">
                  <span className="text-xs font-medium text-muted uppercase">{col.label}</span>
                  <span className={`text-sm text-foreground text-right ${col.className || ''}`}>
                    {col.render ? col.render(item) : (item[col.key as keyof T] as ReactNode)}
                  </span>
                </div>
              ))}
          </div>
        ))}
      </div>
    </>
  );
}
