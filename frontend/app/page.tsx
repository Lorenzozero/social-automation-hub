"use client";

import Link from "next/link";
import { ArrowRight, Zap, Shield, TrendingUp } from "lucide-react";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center space-y-6 mb-16 animate-fade-in">
          <h1 className="text-6xl font-bold tracking-tight">
            <span className="bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
              Social Hub
            </span>
          </h1>
          <p className="text-xl text-muted max-w-2xl mx-auto">
            Automatizza la gestione dei tuoi social media con intelligenza artificiale.
            Pubblica, analizza e cresci su tutte le piattaforme.
          </p>
          <div className="flex gap-4 justify-center pt-6">
            <Link href="/dashboard" className="btn-primary inline-flex items-center gap-2">
              Inizia Ora
              <ArrowRight size={20} />
            </Link>
            <Link href="/accounts" className="btn-secondary inline-flex items-center gap-2">
              Collega Account
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mt-20">
          <div className="card text-center space-y-4 hover:scale-105 transition-transform duration-200">
            <div className="w-12 h-12 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-xl flex items-center justify-center mx-auto">
              <Zap className="text-white" size={24} />
            </div>
            <h3 className="text-lg font-semibold">Automazione Completa</h3>
            <p className="text-sm text-muted">
              Pianifica e pubblica contenuti su Instagram, TikTok, LinkedIn e X contemporaneamente.
            </p>
          </div>

          <div className="card text-center space-y-4 hover:scale-105 transition-transform duration-200">
            <div className="w-12 h-12 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-xl flex items-center justify-center mx-auto">
              <TrendingUp className="text-white" size={24} />
            </div>
            <h3 className="text-lg font-semibold">Analytics Avanzate</h3>
            <p className="text-sm text-muted">
              Monitora crescita, engagement e metriche dettagliate in tempo reale.
            </p>
          </div>

          <div className="card text-center space-y-4 hover:scale-105 transition-transform duration-200">
            <div className="w-12 h-12 bg-gradient-to-br from-brand-primary to-brand-secondary rounded-xl flex items-center justify-center mx-auto">
              <Shield className="text-white" size={24} />
            </div>
            <h3 className="text-lg font-semibold">Sicurezza Totale</h3>
            <p className="text-sm text-muted">
              Token OAuth crittografati e conformità alle policy delle piattaforme.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
