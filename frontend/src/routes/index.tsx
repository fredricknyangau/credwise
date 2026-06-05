import heroImg from "@/assets/hero-illustration.jpg";
import { PublicNav } from "@/components/PublicNav";
import { createFileRoute, Link } from "@tanstack/react-router";
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  LineChart,
  ShieldCheck,
  Sparkles,
  Users,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "CredWise - Ethical credit readiness for the unbanked" },
      {
        name: "description",
        content:
          "A financial literacy and credit-readiness platform for microfinance institutions and unbanked users.",
      },
      { property: "og:title", content: "CredWise" },
      { property: "og:description", content: "Ethical credit readiness for the unbanked." },
    ],
  }),
  component: Landing,
});

function Landing() {
  return (
    <div className="min-h-screen bg-brand-surface text-foreground">
      <PublicNav />

      {/* Hero */}
      <header className="relative overflow-hidden px-4 py-16 md:py-24">
        <div className="mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-2">
          <div>
            <span className="mb-6 inline-block rounded-full bg-brand-primary/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-brand-primary">
              Empowering the Unbanked
            </span>
            <h1 className="mb-6 font-display text-5xl font-extrabold leading-[1.05] tracking-tight md:text-6xl">
              Financial readiness through{" "}
              <span className="text-brand-secondary">ethical learning.</span>
            </h1>
            <p className="mb-8 max-w-xl text-lg text-muted-foreground">
              CredWise bridges microfinance institutions and their clients with transparent,
              module-based credit preparation. Build trust on behavior - not just history.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/auth/register"
                className="inline-flex items-center gap-2 rounded-xl bg-brand-primary px-7 py-4 font-bold text-primary-foreground shadow-brand transition-all hover:-translate-y-0.5 hover:bg-brand-secondary"
              >
                For Institutions <ArrowRight className="size-4" />
              </Link>
              <Link
                to="/auth/register-learner"
                className="rounded-xl border border-border bg-card px-7 py-4 font-bold text-foreground transition-all hover:bg-secondary"
              >
                Start Learning
              </Link>
            </div>
            <div className="mt-10 flex items-center gap-6 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Users className="size-4 text-brand-secondary" /> 40+ MFIs
              </div>
              <div className="flex items-center gap-2">
                <ShieldCheck className="size-4 text-brand-secondary" /> Transparent scoring
              </div>
            </div>
          </div>
          <div className="relative">
            <div className="absolute -inset-6 -z-10 rounded-[2.5rem] bg-gradient-to-br from-brand-secondary/15 to-brand-accent/10 blur-2xl" />
            <img
              src={heroImg}
              alt="CredWise mobile app showing credit readiness gauge"
              width={1280}
              height={960}
              className="aspect-[4/3] w-full rounded-3xl bg-card object-cover shadow-lift outline-1 -outline-offset-1 outline-brand-primary/10"
            />
          </div>
        </div>
      </header>

      {/* How it works */}
      <section className="border-y border-border bg-card/50 px-4 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="mx-auto mb-12 max-w-2xl text-center">
            <span className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
              How it works
            </span>
            <h2 className="mt-3 font-display text-3xl font-bold md:text-4xl">
              Three steps to credit readiness
            </h2>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                icon: BookOpen,
                title: "1. Learn",
                desc: "Bite-sized literacy modules on saving, interest, and cash flow - designed for low-bandwidth devices.",
              },
              {
                icon: Sparkles,
                title: "2. Build your profile",
                desc: "Share income patterns, business type, and cooperative ties. We compute an ethical readiness score.",
              },
              {
                icon: CheckCircle2,
                title: "3. Get ready for credit",
                desc: "Transparent scoring with explanations. MFIs see verified, prepared borrowers ready to grow.",
              },
            ].map((s) => (
              <div
                key={s.title}
                className="rounded-2xl border border-border bg-card p-8 shadow-soft transition-all hover:-translate-y-1 hover:shadow-lift"
              >
                <div className="mb-5 grid size-12 place-items-center rounded-xl bg-brand-primary/10 text-brand-primary">
                  <s.icon className="size-6" />
                </div>
                <h3 className="mb-2 font-display text-xl font-bold">{s.title}</h3>
                <p className="text-sm leading-relaxed text-muted-foreground">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="px-4 py-20">
        <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-2">
          <BenefitCard
            tone="primary"
            label="For institutions"
            title="Lower default risk. Better-prepared borrowers."
            items={[
              "Real-time readiness scores across your portfolio",
              "Filter clients by literacy progress and risk",
              "Module performance analytics by cooperative",
              "Transparent, ethical scoring - defensible to regulators",
            ]}
            cta={{ to: "/auth/register", label: "Register your MFI" }}
          />
          <BenefitCard
            tone="accent"
            label="For users"
            title="Learn at your pace. Build credit on your terms."
            items={[
              "Mobile-first lessons under 20 minutes each",
              "Quizzes with instant feedback",
              "See exactly why your score is what it is",
              "Concrete next steps to improve it",
            ]}
            cta={{ to: "/auth/register-learner", label: "Start learning" }}
          />
        </div>
      </section>

      {/* Testimonials */}
      <section className="border-y border-border bg-brand-primary/5 px-4 py-20">
        <div className="mx-auto max-w-5xl">
          <h2 className="mb-12 text-center font-display text-3xl font-bold">
            Trusted by mission-driven lenders
          </h2>
          <div className="grid gap-6 md:grid-cols-2">
            {[
              {
                quote:
                  "CredWise cut our pre-loan vetting time by 60% and our defaults are down two quarters in a row.",
                who: "Adaeze N., Risk Lead - Lagos Microcredit Union",
              },
              {
                quote:
                  "For the first time, our clients understand the score. That changes the whole conversation.",
                who: "Thabo M., Field Officer - Cape Cooperative",
              },
            ].map((t) => (
              <figure
                key={t.who}
                className="rounded-2xl border border-border bg-card p-8 shadow-soft"
              >
                <blockquote className="font-display text-lg italic leading-relaxed">
                  "{t.quote}"
                </blockquote>
                <figcaption className="mt-4 text-sm font-medium text-muted-foreground">
                  - {t.who}
                </figcaption>
              </figure>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="px-4 py-20">
        <div className="mx-auto max-w-5xl overflow-hidden rounded-[2.5rem] bg-ink p-10 text-background md:p-16">
          <div className="grid items-center gap-10 md:grid-cols-2">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
                Get started
              </span>
              <h2 className="mt-3 font-display text-3xl font-bold md:text-4xl">
                Bridge the financial gap, ethically.
              </h2>
              <p className="mt-4 text-muted-foreground">
                Open a demo dashboard or jump into the learning portal - no setup required.
              </p>
            </div>
            <div className="flex flex-col gap-3">
              <Link
                to="/mfi"
                className="inline-flex items-center justify-between rounded-xl bg-brand-secondary px-6 py-4 font-bold text-primary-foreground transition-all hover:bg-brand-primary"
              >
                <span className="flex items-center gap-3">
                  <LineChart className="size-5" /> Explore MFI Dashboard
                </span>
                <ArrowRight className="size-5" />
              </Link>
              <Link
                to="/portal"
                className="inline-flex items-center justify-between rounded-xl border border-white/15 bg-white/5 px-6 py-4 font-bold text-background transition-all hover:bg-white/10"
              >
                <span className="flex items-center gap-3">
                  <BookOpen className="size-5" /> Open Learning Portal
                </span>
                <ArrowRight className="size-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-border px-4 py-10 text-center text-sm text-muted-foreground">
        © 2026 CredWise - Ethical credit infrastructure
      </footer>
    </div>
  );
}

function BenefitCard({
  tone,
  label,
  title,
  items,
  cta,
}: {
  tone: "primary" | "accent";
  label: string;
  title: string;
  items: string[];
  cta: { to: string; label: string };
}) {
  const isPrimary = tone === "primary";
  return (
    <div
      className={`rounded-3xl border p-8 md:p-10 ${
        isPrimary
          ? "border-brand-primary/15 bg-brand-primary/5"
          : "border-brand-accent/20 bg-brand-accent/5"
      }`}
    >
      <span
        className={`text-xs font-bold uppercase tracking-widest ${
          isPrimary ? "text-brand-primary" : "text-brand-accent"
        }`}
      >
        {label}
      </span>
      <h3 className="mt-2 font-display text-2xl font-bold md:text-3xl">{title}</h3>
      <ul className="mt-6 space-y-3">
        {items.map((it) => (
          <li key={it} className="flex items-start gap-3 text-sm">
            <CheckCircle2
              className={`mt-0.5 size-5 shrink-0 ${isPrimary ? "text-brand-primary" : "text-brand-accent"}`}
            />
            <span>{it}</span>
          </li>
        ))}
      </ul>
      <Link
        to={cta.to as never}
        className={`mt-8 inline-flex items-center gap-2 rounded-xl px-5 py-3 text-sm font-bold ${
          isPrimary
            ? "bg-brand-primary text-primary-foreground hover:bg-brand-secondary"
            : "bg-brand-accent text-white hover:opacity-90"
        }`}
      >
        {cta.label} <ArrowRight className="size-4" />
      </Link>
    </div>
  );
}
