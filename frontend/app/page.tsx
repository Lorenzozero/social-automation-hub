import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center px-4">
      <div className="text-center space-y-8 max-w-3xl animate-slide-up">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-brand-primary text-xs font-semibold uppercase tracking-wider animate-fade-in">
          <span>🚀</span>
          <span>Open-source multi-social platform</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-black bg-gradient-to-r from-brand-primary via-brand-secondary to-brand-primary bg-clip-text text-transparent animate-fade-in stagger-1">
          Social Automation Hub
        </h1>
        
        <p className="text-lg md:text-xl text-muted max-w-2xl mx-auto leading-relaxed animate-fade-in stagger-2">
          Unified dashboard for influencers, creators, and agencies. Monitor, publish, and automate across
          Instagram, TikTok, LinkedIn, and X with real data and professional compliance.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in stagger-3">
          <Link href="/onboarding" className="btn-primary w-full sm:w-auto">
            Start Guide
          </Link>
          <Link href="/dashboard" className="btn-secondary w-full sm:w-auto">
            Go to Dashboard
          </Link>
          <a
            href="https://github.com/Lorenzozero/social-automation-hub"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary w-full sm:w-auto flex items-center justify-center gap-2"
          >
            <span>📦</span>
            <span>View on GitHub</span>
          </a>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8 animate-fade-in stagger-3">
          <div className="card text-center">
            <p className="text-3xl mb-2">📸</p>
            <p className="text-xs text-muted">Instagram</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl mb-2">🎵</p>
            <p className="text-xs text-muted">TikTok</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl mb-2">💼</p>
            <p className="text-xs text-muted">LinkedIn</p>
          </div>
          <div className="card text-center">
            <p className="text-3xl mb-2">𝕏</p>
            <p className="text-xs text-muted">X (Twitter)</p>
          </div>
        </div>
      </div>
    </main>
  );
}
