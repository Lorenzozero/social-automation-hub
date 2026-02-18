"use client";

export const dynamic = 'force-dynamic';

export default function LoginPage() {
  return (
    <main className="h-full flex items-center justify-center px-4">
      <div className="w-full max-w-md rounded-2xl border border-slate-800/70 bg-slate-950/60 p-6 space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-brand-secondary/70 mb-1">
            Social Automation Hub
          </p>
          <h1 className="text-xl font-semibold">Accedi al tuo workspace</h1>
          <p className="text-sm text-slate-400">
            L&apos;autenticazione reale (Supabase/Firebase/Auth esterno) verrà configurata
            in base all&apos;ambiente. Qui non ci sono credenziali hardcodate.
          </p>
        </div>
        <button className="w-full rounded-full bg-brand-primary px-4 py-2.5 text-sm font-medium shadow-lg shadow-brand-primary/40 hover:bg-brand-primary/90 transition">
          Continua con provider
        </button>
      </div>
    </main>
  );
}
