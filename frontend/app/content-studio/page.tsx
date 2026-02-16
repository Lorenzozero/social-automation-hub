"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const WORKSPACE_ID = "00000000-0000-0000-0000-000000000001";

interface ContentVariant {
  id: string;
  platform: string;
  caption: string;
  hashtags: string[];
}

export default function ContentStudioPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [variants, setVariants] = useState<ContentVariant[]>([]);

  const [brief, setBrief] = useState({
    topic: "",
    goal: "",
    tone: "casual",
    target_audience: "",
    keywords: "",
    target_platforms: ["instagram"] as string[],
    ai_model: "anthropic",
    variants_per_platform: 3,
  });

  const handleGenerate = async () => {
    if (!brief.topic || !brief.goal) {
      alert("Please fill in topic and goal");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/content-studio/briefs/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          workspace_id: WORKSPACE_ID,
          ...brief,
          keywords: brief.keywords.split(",").map((k) => k.trim()).filter(Boolean),
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setVariants(data.variants);
      } else {
        alert("Failed to generate content");
      }
    } catch (error) {
      console.error("Generation error:", error);
      alert("Error generating content");
    } finally {
      setLoading(false);
    }
  };

  const togglePlatform = (platform: string) => {
    setBrief((prev) => ({
      ...prev,
      target_platforms: prev.target_platforms.includes(platform)
        ? prev.target_platforms.filter((p) => p !== platform)
        : [...prev.target_platforms, platform],
    }));
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <section>
        <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-brand-primary to-brand-secondary bg-clip-text text-transparent">
          ✨ Content Studio
        </h1>
        <p className="text-sm text-muted">AI-powered content generation for all your platforms</p>
      </section>

      <div className="card space-y-6">
        <h2 className="text-lg font-semibold text-foreground">Create Brief</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Topic *</label>
            <input
              type="text"
              value={brief.topic}
              onChange={(e) => setBrief({ ...brief, topic: e.target.value })}
              placeholder="e.g., New product launch, Behind-the-scenes, Tips & tricks"
              className="input w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Goal *</label>
            <textarea
              value={brief.goal}
              onChange={(e) => setBrief({ ...brief, goal: e.target.value })}
              placeholder="What do you want to achieve? (e.g., Increase engagement, Drive traffic, Build awareness)"
              className="input w-full min-h-[100px]"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Tone</label>
              <select
                value={brief.tone}
                onChange={(e) => setBrief({ ...brief, tone: e.target.value })}
                className="input w-full"
              >
                <option value="casual">Casual</option>
                <option value="professional">Professional</option>
                <option value="funny">Funny</option>
                <option value="inspiring">Inspiring</option>
                <option value="educational">Educational</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Target Audience</label>
              <input
                type="text"
                value={brief.target_audience}
                onChange={(e) => setBrief({ ...brief, target_audience: e.target.value })}
                placeholder="e.g., Young professionals, Fitness enthusiasts"
                className="input w-full"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Keywords (comma-separated)</label>
            <input
              type="text"
              value={brief.keywords}
              onChange={(e) => setBrief({ ...brief, keywords: e.target.value })}
              placeholder="e.g., innovation, technology, future"
              className="input w-full"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Target Platforms</label>
            <div className="flex flex-wrap gap-2">
              {["instagram", "tiktok", "linkedin", "x"].map((platform) => (
                <button
                  key={platform}
                  onClick={() => togglePlatform(platform)}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                    brief.target_platforms.includes(platform)
                      ? "bg-brand-primary text-white"
                      : "bg-surface text-muted hover:bg-muted"
                  }`}
                >
                  {platform === "instagram" && "📸"}
                  {platform === "tiktok" && "🎵"}
                  {platform === "linkedin" && "💼"}
                  {platform === "x" && "𝕏"}
                  {" "}
                  {platform.charAt(0).toUpperCase() + platform.slice(1)}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">AI Model</label>
              <select
                value={brief.ai_model}
                onChange={(e) => setBrief({ ...brief, ai_model: e.target.value })}
                className="input w-full"
              >
                <option value="anthropic">Claude 3.5 Sonnet (Anthropic)</option>
                <option value="openai">GPT-4 Turbo (OpenAI)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">Variants per Platform</label>
              <input
                type="number"
                value={brief.variants_per_platform}
                onChange={(e) => setBrief({ ...brief, variants_per_platform: parseInt(e.target.value) || 3 })}
                min={1}
                max={5}
                className="input w-full"
              />
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !brief.topic || !brief.goal}
            className="btn-primary w-full py-3 text-base font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Generating..." : "✨ Generate Content"}
          </button>
        </div>
      </div>

      {variants.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-foreground">🎨 Generated Variants</h2>
          <div className="grid grid-cols-1 gap-4">
            {variants.map((variant) => (
              <div key={variant.id} className="card space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">
                      {variant.platform === "instagram" && "📸"}
                      {variant.platform === "tiktok" && "🎵"}
                      {variant.platform === "linkedin" && "💼"}
                      {variant.platform === "x" && "𝕏"}
                    </span>
                    <span className="text-sm font-semibold text-foreground capitalize">{variant.platform}</span>
                  </div>
                  <button className="btn-secondary text-sm px-3 py-1.5">Approve</button>
                </div>
                <p className="text-sm text-foreground whitespace-pre-wrap">{variant.caption}</p>
                <div className="flex flex-wrap gap-2">
                  {variant.hashtags.map((tag, i) => (
                    <span key={i} className="text-xs px-2 py-1 rounded-lg bg-brand-primary/10 text-brand-primary">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
