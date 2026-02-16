export function Topbar() {
  return (
    <header className="h-14 flex items-center justify-between px-4 border-b border-slate-800/70 bg-slate-950/60 backdrop-blur">
      <div>
        <p className="text-xs text-slate-400">Workspace attivo</p>
        <p className="text-sm font-medium">Da selezionare dal backend reale</p>
      </div>
      <div className="flex items-center gap-3">
        <span className="h-8 w-8 rounded-full bg-gradient-to-br from-brand.primary to-brand.secondary" aria-hidden />
      </div>
    </header>
  );
}
