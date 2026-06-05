import { useModules, useReadiness } from "@/lib/api/hooks";
import { useAuth } from "@/lib/store/auth";
import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, CheckCircle2, Clock, Play, Sparkles } from "lucide-react";

export const Route = createFileRoute("/portal/")({
  head: () => ({ meta: [{ title: "Your learning path - CredWise" }] }),
  component: LearnHome,
});

function LearnHome() {
  const user = useAuth((s) => s.user);
  const { data: modules = [] } = useModules();
  const { data: readiness } = useReadiness();

  const current = modules.find((m) => m.progress > 0 && m.progress < 100) ?? modules[0];

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <section className="mb-8">
        <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
          Welcome back
        </p>
        <h1 className="mt-1 font-display text-3xl font-bold">
          Good to see you, {user?.name?.split(" ")[0] ?? "friend"}.
        </h1>
        <p className="mt-1 text-muted-foreground">
          You're {readiness?.score ?? 0} points into your readiness journey.
        </p>
      </section>

      {/* Readiness snapshot */}
      <Link
        to="/portal/readiness"
        className="mb-6 flex items-center justify-between rounded-3xl bg-ink p-6 text-background transition-all hover:-translate-y-0.5"
      >
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-brand-secondary">
            Your score
          </p>
          <p className="mt-2 font-display text-5xl font-black">{readiness?.score ?? "-"}</p>
          <p className="text-sm text-muted-foreground">
            {readiness?.category} - tap to view details
          </p>
        </div>
        <div className="relative grid size-24 place-items-center">
          <svg className="size-24 -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="42"
              fill="none"
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="8"
            />
            <circle
              cx="50"
              cy="50"
              r="42"
              fill="none"
              stroke="#059669"
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 42 * ((readiness?.score ?? 0) / 100)} ${2 * Math.PI * 42}`}
            />
          </svg>
          <ArrowRight className="absolute size-5 text-brand-secondary" />
        </div>
      </Link>

      {/* Current module */}
      {current && (
        <Link
          to="/portal/modules/$moduleId"
          params={{ moduleId: current.id }}
          className="mb-6 block rounded-3xl border-2 border-brand-primary/15 bg-card p-6 shadow-lift transition-all hover:-translate-y-0.5"
        >
          <div className="flex gap-5">
            <div className="grid size-16 shrink-0 place-items-center rounded-2xl bg-brand-primary/10 text-brand-primary">
              <Play className="size-6" fill="currentColor" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-semibold uppercase tracking-wider text-brand-secondary">
                Continue learning
              </p>
              <h3 className="mt-1 font-display text-xl font-bold">{current.title}</h3>
              <p className="text-xs text-muted-foreground">
                Module · {current.durationMin} min · {current.progress}% done
              </p>
              <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-secondary">
                <div
                  className="h-full rounded-full bg-brand-secondary transition-all"
                  style={{ width: `${current.progress}%` }}
                />
              </div>
            </div>
          </div>
        </Link>
      )}

      {/* Profile prompt */}
      <Link
        to="/portal/profile"
        className="mb-8 flex items-center justify-between rounded-2xl border border-brand-accent/25 bg-brand-accent/5 p-5"
      >
        <div className="flex items-center gap-4">
          <div className="grid size-11 place-items-center rounded-full bg-brand-accent/15 text-brand-accent">
            <Sparkles className="size-5" />
          </div>
          <div>
            <h4 className="font-bold">Complete your profile</h4>
            <p className="text-xs text-muted-foreground">Add 5 details to boost your score</p>
          </div>
        </div>
        <ArrowRight className="size-5 text-brand-accent" />
      </Link>

      <section>
        <h2 className="mb-4 font-display text-xl font-bold">All modules</h2>
        <div className="space-y-3">
          {modules.map((m) => (
            <Link
              key={m.id}
              to="/portal/modules/$moduleId"
              params={{ moduleId: m.id }}
              className="flex items-center gap-4 rounded-2xl border border-border bg-card p-4 transition-colors hover:bg-secondary/30"
            >
              <div
                className={`grid size-12 shrink-0 place-items-center rounded-xl ${
                  m.progress === 100
                    ? "bg-brand-secondary/15 text-brand-secondary"
                    : m.progress > 0
                      ? "bg-brand-primary/10 text-brand-primary"
                      : "bg-secondary text-muted-foreground"
                }`}
              >
                {m.progress === 100 ? (
                  <CheckCircle2 className="size-5" />
                ) : (
                  <Clock className="size-5" />
                )}
              </div>
              <div className="min-w-0 flex-1">
                <p className="font-semibold">{m.title}</p>
                <p className="truncate text-xs text-muted-foreground">{m.description}</p>
                <div className="mt-2 h-1 w-full overflow-hidden rounded-full bg-secondary">
                  <div
                    className="h-full rounded-full bg-brand-secondary"
                    style={{ width: `${m.progress}%` }}
                  />
                </div>
              </div>
              <ArrowRight className="size-4 text-muted-foreground" />
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
