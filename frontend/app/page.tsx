import Link from "next/link";

export default function HomePage() {
  return (
    <main className="h-full flex items-center justify-center">
      <div className="text-center space-y-6 max-w-xl">
        <p className="text-sm uppercase tracking-[0.25em] text-brand-secondary/80">
          Open-source multi-social
        </p>
        <h1 className="text-4xl md:text-5xl font-semibold">
          Pannello unico per i tuoi social.
        </h1>
        <p className="text-slate-300">
          Monitoraggio, publishing e automazioni safe per influencer, creator e agency.
          Nessun dato finto: solo ciò che arriva davvero dalle tue integrazioni.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="rounded-full bg-brand.primary px-6 py-3 text-sm font-medium shadow-lg shadow-brand-primary/40 hover:bg-brand.primary/90 transition"
          >
            Vai alla dashboard
          </Link>
          <Link
            href="/login"
            className="rounded-full border border-slate-600 px-6 py-3 text-sm font-medium text-slate-100 hover:bg-slate-900/40 transition"
          >
            Accedi
          </Link>
        </div>
      </div>
    </main>
  );
}
