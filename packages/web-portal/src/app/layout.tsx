import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import Image from "next/image";
import Link from "next/link";
import { ApiStatus } from "@/components/ApiStatus";
import "./globals.css";

const ibmSans = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-ibm-sans",
});

const ibmMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-ibm-mono",
});

export const metadata: Metadata = {
  title: "SVIE — Powertrain IP Portal",
  description:
    "Supercritical Vapor-Injection Engine: acquisition-ready physics, specs, demo, and OEM diligence tools",
  icons: {
    icon: "/brand/svie-logo.png",
  },
};

const nav = [
  { href: "/", label: "Overview" },
  { href: "/pitch", label: "Pitch" },
  { href: "/demo", label: "Demo" },
  { href: "/diligence", label: "Diligence" },
  { href: "/package", label: "Package" },
  { href: "/calculators", label: "Calculators" },
  { href: "/lab", label: "Lab" },
  { href: "/specs", label: "Specs" },
  { href: "/architecture", label: "Architecture" },
  { href: "/design", label: "Design" },
  { href: "/hmi", label: "HMI" },
  { href: "/acquisition", label: "Acquire" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${ibmSans.variable} ${ibmMono.variable} antialiased`}>
        <header className="border-b border-[var(--line)] bg-[rgba(18,21,26,0.85)] backdrop-blur-md">
          <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-5 py-4">
            <Link href="/" className="brand-mark group flex items-center gap-3">
              <Image
                src="/brand/svie-logo.png"
                alt="SVIE"
                width={40}
                height={40}
                className="border border-[var(--line)]"
                priority
              />
              <div>
                <div className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-[0.28em] text-[var(--amber)]">
                  SVIE
                </div>
                <div className="mt-0.5 text-sm font-medium text-[var(--ink)] group-hover:text-white">
                  Powertrain Engineering Portal
                </div>
              </div>
            </Link>
            <div className="flex flex-col items-end gap-3 sm:flex-row sm:items-center">
              <ApiStatus />
              <nav className="flex flex-wrap justify-end gap-4">
                {nav.map((item) => (
                  <Link key={item.href} href={item.href} className="nav-link">
                    {item.label}
                  </Link>
                ))}
              </nav>
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-5 py-10">{children}</main>
        <footer className="mx-auto max-w-6xl border-t border-[var(--line)] px-5 py-8 text-sm text-[var(--muted)]">
          <p className="font-[family-name:var(--font-ibm-mono)] text-xs tracking-wider uppercase text-[var(--steel)]">
            SVIE v1.3.1 — Production-ready acquisition package
          </p>
          <p className="mt-2 max-w-2xl">
            Hardware TRL-3 (honest). Package close-ready. Start with /acquisition ·
            /pitch · /hmi · Acquisition.md
          </p>
        </footer>
      </body>
    </html>
  );
}
