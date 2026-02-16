"use client";

import type { ReactNode } from "react";
import { Footer } from "@/components/layout/footer";

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col text-foreground">
      <div className="flex-1">{children}</div>
      <Footer />
    </div>
  );
}
