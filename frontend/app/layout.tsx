import "@/styles/globals.css";
import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";
import { Inter } from "next/font/google";
import { Shell } from "@/components/layout/shell";
import { ThemeProvider } from "@/components/providers/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Social Automation Hub - Multi-Platform Management",
  description: "Professional social media management for Instagram, TikTok, LinkedIn, and X. Open-source, self-hosted, compliant automation.",
  keywords: ["social media", "automation", "instagram", "tiktok", "linkedin", "twitter", "analytics"],
  authors: [{ name: "Lorenzo", url: "https://github.com/Lorenzozero" }],
  openGraph: {
    title: "Social Automation Hub",
    description: "Multi-platform social media management tool",
    type: "website",
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0a' },
  ],
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={inter.className} suppressHydrationWarning>
      <body className="antialiased">
        <ThemeProvider>
          <Shell>{children}</Shell>
        </ThemeProvider>
      </body>
    </html>
  );
}
