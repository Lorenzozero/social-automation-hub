import "@/styles/globals.css";
import type { ReactNode } from "react";
import { Inter } from "next/font/google";
import { Shell } from "@/components/layout/shell";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Social Automation Hub",
  description: "Dashboard multi-social per creator e agency",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body className="bg-brand-background text-slate-100">
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
