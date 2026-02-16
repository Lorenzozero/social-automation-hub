"use client";

import { useState } from "react";
import { Plus, Sparkles, Image, Video, Layout, MessageSquare } from "lucide-react";
import Link from "next/link";

type ContentFormat = "post" | "story" | "carousel" | "reel" | "poll" | "giveaway";

interface ContentTemplate {
  id: string;
  name: string;
  format: ContentFormat;
  icon: any;
  description: string;
  platforms: string[];
}

const templates: ContentTemplate[] = [
  {
    id: "post",
    name: "Single Post",
    format: "post",
    icon: Image,
    description: "Photo post con caption",
    platforms: ["instagram", "linkedin", "x"],
  },
  {
    id: "story",
    name: "Story",
    format: "story",
    icon: MessageSquare,
    description: "Storia 24h (Instagram/TikTok)",
    platforms: ["instagram", "tiktok"],
  },
  {
    id: "carousel",
    name: "Carousel",
    format: "carousel",
    icon: Layout,
    description: "Galleria 2-10 immagini swipeable",
    platforms: ["instagram", "linkedin"],
  },
  {
    id: "reel",
    name: "Reel/Video",
    format: "reel",
    icon: Video,
    description: "Video verticale short-form",
    platforms: ["instagram", "tiktok"],
  },
  {
    id: "poll",
    name: "Poll",
    format: "poll",
    icon: MessageSquare,
    description: "Sondaggio interattivo",
    platforms: ["instagram", "x", "linkedin"],
  },
  {
    id: "giveaway",
    name: "Giveaway",
    format: "giveaway",
    icon: Sparkles,
    description: "Contest con regole e premio",
    platforms: ["instagram", "tiktok"],
  },
];

export default function ContentStudioPage() {
  const [selectedFormat, setSelectedFormat] = useState<ContentFormat | null>(null);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <section className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
            Content Studio
          </h1>
          <p className="text-sm text-muted">
            Crea contenuti AI-powered con template ricorrenti per ogni piattaforma
          </p>
        </div>
        <Link href="/content-studio/create" className="btn-primary flex items-center gap-2">
          <Plus size={20} />
          Nuovo Contenuto
        </Link>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold text-foreground">Scegli Formato</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => {
            const Icon = template.icon;
            return (
              <button
                key={template.id}
                onClick={() => setSelectedFormat(template.format)}
                className={`card group text-left hover:scale-[1.02] transition-all duration-200 ${
                  selectedFormat === template.format ? "ring-2 ring-brand-primary" : ""
                }`}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center text-white">
                    <Icon size={24} />
                  </div>
                  {selectedFormat === template.format && (
                    <span className="text-xs bg-brand-primary text-white px-2 py-1 rounded-full">
                      Selezionato
                    </span>
                  )}
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{template.name}</h3>
                <p className="text-sm text-muted mb-3">{template.description}</p>
                <div className="flex gap-2 flex-wrap">
                  {template.platforms.map((platform) => (
                    <span
                      key={platform}
                      className="text-xs bg-surface px-2 py-1 rounded-full text-foreground-secondary capitalize"
                    >
                      {platform}
                    </span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {selectedFormat && (
        <section className="card animate-fade-in">
          <h2 className="text-xl font-semibold text-foreground mb-4">Template Ricorrenti</h2>
          <p className="text-sm text-muted mb-4">
            Crea template salvati per generare contenuti simili velocemente
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-surface border border-muted">
              <h3 className="font-semibold text-foreground mb-2">Quote Monday</h3>
              <p className="text-xs text-muted mb-3">
                Post motivazionale ogni lunedì mattina ore 8:00
              </p>
              <div className="flex gap-2">
                <button className="btn-secondary text-xs">Modifica</button>
                <button className="btn-primary text-xs">Usa Template</button>
              </div>
            </div>
            <div className="p-4 rounded-xl bg-surface border border-muted">
              <h3 className="font-semibold text-foreground mb-2">Product Showcase</h3>
              <p className="text-xs text-muted mb-3">
                Carousel con features prodotto ogni venerdì ore 18:00
              </p>
              <div className="flex gap-2">
                <button className="btn-secondary text-xs">Modifica</button>
                <button className="btn-primary text-xs">Usa Template</button>
              </div>
            </div>
          </div>
          <button className="btn-secondary mt-4 flex items-center gap-2">
            <Plus size={16} />
            Crea Nuovo Template
          </button>
        </section>
      )}

      <section className="card">
        <div className="flex items-center gap-3 mb-4">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-brand-primary to-brand-secondary flex items-center justify-center">
            <Sparkles size={20} className="text-white" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-foreground">AI Content Generator</h2>
            <p className="text-xs text-muted">Genera caption, hashtag e copy adattati per ogni piattaforma</p>
          </div>
        </div>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Brief Contenuto</label>
            <textarea
              className="w-full px-4 py-3 bg-surface border border-muted rounded-xl text-foreground placeholder:text-foreground-secondary focus:outline-none focus:ring-2 focus:ring-brand-primary transition-all duration-200 resize-none"
              rows={4}
              placeholder="Descrivi il contenuto che vuoi creare (es: 'Post su nuovo prodotto eco-friendly, tono friendly, target 25-35 anni')..."
            />
          </div>
          <div className="flex gap-3">
            <button className="btn-primary flex items-center gap-2">
              <Sparkles size={16} />
              Genera con AI
            </button>
            <button className="btn-secondary">Salva come Template</button>
          </div>
        </div>
      </section>
    </div>
  );
}
