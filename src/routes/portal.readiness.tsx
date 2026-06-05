import { createFileRoute, Link } from "@tanstack/react-router";
import { useReadiness } from "@/lib/api/hooks";
import { ArrowLeft, CheckCircle2, Circle, Clock, Lightbulb } from "lucide-react";

export const Route = createFileRoute("/portal/readiness")({
  head: () => ({ meta: [{ title: "Credit readiness — CrediPath" }] }),
  component: Readiness,
});

function Readiness() {
  const { data } = useReadiness();
  if (!data) return <div className="grid place-items-center py-20 text-muted-foreground">Loading…</div>;

  const circumference = 2 * Math.PI * 80;
  const dash = circumference * (data.score / 100);

  return (
    <main className="mx-auto max-w-3xl px-4 py-6">
      <Link to="/portal" className="mb-4 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground">
        <ArrowLeft className="size-4" /> Back
      </Link>

      <section className="overflow-hidden rounded-[2rem] bg-ink p-8 text-background md:p-10">
        <div className="relative z-10 grid gap-8 md:grid-cols-2 md:items-center">
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">Ethical credit readiness</p>
            <h1 className="mt-2 font-display text-3xl font-bold">Your score, explained</h1>
            <p className="mt-3 text-sm text-muted-foreground">
              Calculated from financial behavior, literacy progress, and community ties — not income alone.
            </p>
            <div className="mt-6 space-y-3">
              {data.factors.map((f) => (
                <div key={f.label} className="flex items-start gap-3">
                  <span className={`mt-1 inline-block size-2.5 shrink-0 rounded-full ${
                    f.status === "active" ? "bg-brand-secondary" :
                    f.status === "partial" ? "bg-brand-accent" : "bg-muted-foreground/40"
                  }`} />
                  <div>
                    <p className="text-sm font-medium text-background">{f.label}</p>
                    <p className="text-xs text-muted-foreground">{f.detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="flex flex-col items-center justify-center">
            <div className="relative size-56">
              <svg className="size-56 -rotate-90" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="16" />
                <circle
                  cx="100" cy="100" r="80" fill="none" stroke="#059669" strokeWidth="16"
                  strokeLinecap="round"
                  strokeDasharray={`${dash} ${circumference}`}
                  style={{ transition: "stroke-dasharray 800ms cubic-bezier(0.16,1,0.3,1)" }}
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-display text-6xl font-black">{data.score}</span>
                <span className="text-xs font-bold uppercase tracking-widest text-brand-secondary">{data.category}</span>
              </div>
            </div>
            <p className="mt-6 text-center text-sm text-muted-foreground">
              You are <span className="font-bold text-background underline decoration-brand-secondary decoration-2 underline-offset-4">Ready for Credit</span>
            </p>
          </div>
        </div>
      </section>

      <section className="mt-8">
        <div className="mb-3 flex items-center gap-2">
          <Lightbulb className="size-5 text-brand-accent" />
          <h2 className="font-display text-xl font-bold">How to improve</h2>
        </div>
        <div className="space-y-2">
          {data.suggestions.map((s, i) => (
            <div key={s} className="flex items-start gap-3 rounded-2xl border border-border bg-card p-4">
              <div className="grid size-7 shrink-0 place-items-center rounded-full bg-brand-accent/15 text-xs font-bold text-brand-accent">
                {i + 1}
              </div>
              <p className="text-sm">{s}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mt-8 rounded-2xl border border-border bg-brand-primary/5 p-6">
        <h3 className="font-display text-lg font-bold">Why we score this way</h3>
        <p className="mt-2 text-sm text-muted-foreground">
          Traditional credit scoring excludes most unbanked people because they lack formal history.
          CrediPath replaces that with verifiable behavior — savings consistency, financial literacy,
          and cooperative participation. Every factor that affects your score is shown above and can be
          improved through your own actions. No hidden inputs.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 text-xs">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-secondary/15 px-3 py-1 font-semibold text-brand-secondary">
            <CheckCircle2 className="size-3" /> Transparent
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-primary/10 px-3 py-1 font-semibold text-brand-primary">
            <Circle className="size-3" /> Behavior-based
          </span>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-accent/15 px-3 py-1 font-semibold text-brand-accent">
            <Clock className="size-3" /> Updated weekly
          </span>
        </div>
      </section>
    </main>
  );
}
