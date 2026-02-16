import "@/styles/globals.css";
import type { ReactNode } from "react";
import { Inter } from "next/font/google";
import { Shell } from "@/components/layout/shell";
import { ThemeProvider } from "@/components/providers/theme-provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Social Automation Hub",
  description: "Multi-social dashboard for creators and agencies",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <ThemeProvider>
          <Shell>{children}</Shell>
        </ThemeProvider>
      </body>
    </html>
  );
}
