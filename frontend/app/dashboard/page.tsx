import { StatCard } from "@/components/common/stat-card";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-2xl font-semibold mb-1">Overview</h1>
        <p className="text-sm text-slate-400">
          KPI multi-social in tempo reale non appena colleghi i tuoi account.
        </p>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard label="Reach totale (24h)" value="–" hint="In attesa di dati reali" />
        <StatCard label="Impressions (7 giorni)" value="–" hint="Collega almeno un account" />
        <StatCard label="Followers delta" value="–" hint="Mostra la variazione, non stime" />
      </section>

      <section className="rounded-2xl border border-slate-800/60 bg-slate-950/40 p-4 min-h-[220px] flex items-center justify-center">
        <p className="text-sm text-slate-400 max-w-md text-center">
          Qui compariranno grafici e insight solo a partire da metriche
          effettivamente lette via API (Instagram, TikTok, LinkedIn, X).
          Nessun numero inventato, nessun dato demo.
        </p>
      </section>
    </div>
  );
}
