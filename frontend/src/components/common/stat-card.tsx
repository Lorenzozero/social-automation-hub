"use client";

type StatCardProps = {
  label: string;
  value: string;
  hint?: string;
  trend?: "up" | "down" | "neutral";
};

export function StatCard({ label, value, hint, trend = "neutral" }: StatCardProps) {
  const trendColors = {
    up: "text-green-500",
    down: "text-red-500",
    neutral: "text-muted",
  };

  const trendIcons = {
    up: "↗",
    down: "↘",
    neutral: "→",
  };

  return (
    <div className="card space-y-3 group">
      <div className="flex items-center justify-between">
        <p className="text-xs text-muted uppercase tracking-wide font-semibold">{label}</p>
        <span className={`text-xl ${trendColors[trend]} transition-transform duration-200 group-hover:scale-125`}>
          {trendIcons[trend]}
        </span>
      </div>
      <p className="text-3xl font-bold text-foreground">{value}</p>
      {hint && <p className="text-xs text-muted">{hint}</p>}
    </div>
  );
}
