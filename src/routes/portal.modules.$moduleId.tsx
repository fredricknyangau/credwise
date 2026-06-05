import { useModule, useQuizByModule } from "@/lib/api/hooks";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ArrowLeft, CheckCircle2, ChevronRight, Circle } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/portal/modules/$moduleId")({
  head: () => ({ meta: [{ title: "Lesson - CredWise" }] }),
  component: ModuleView,
});

function ModuleView() {
  const { moduleId } = Route.useParams();
  const { data: module, isLoading } = useModule(moduleId);
  const { data: quiz } = useQuizByModule(moduleId);
  const navigate = useNavigate();
  const [selected, setSelected] = useState(0);

  if (isLoading) return <Loading />;
  if (!module) return <NotFound />;

  const lesson = module.lessons[selected];

  return (
    <main className="mx-auto max-w-3xl px-4 py-6">
      <Link
        to="/portal"
        className="mb-4 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> Back to learning
      </Link>

      <header className="mb-6">
        <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
          {module.category}
        </p>
        <h1 className="mt-1 font-display text-3xl font-bold">{module.title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">{module.description}</p>
        <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div
            className="h-full rounded-full bg-brand-secondary"
            style={{ width: `${module.progress}%` }}
          />
        </div>
      </header>

      <div className="grid gap-6 md:grid-cols-[200px_1fr]">
        {/* Lesson list */}
        <aside className="space-y-1.5">
          {module.lessons.map((l, i) => (
            <button
              key={l.id}
              onClick={() => setSelected(i)}
              className={`flex w-full items-center gap-2.5 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
                selected === i ? "bg-brand-primary text-primary-foreground" : "hover:bg-secondary"
              }`}
            >
              {l.completed ? (
                <CheckCircle2
                  className={`size-4 shrink-0 ${selected === i ? "text-background" : "text-brand-secondary"}`}
                />
              ) : (
                <Circle className="size-4 shrink-0" />
              )}
              <span className="line-clamp-2 font-medium">{l.title}</span>
            </button>
          ))}
        </aside>

        {/* Lesson body */}
        <article className="rounded-2xl border border-border bg-card p-6 shadow-soft md:p-8">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Lesson {selected + 1} of {module.lessons.length}
          </p>
          <h2 className="mt-1 font-display text-2xl font-bold">{lesson.title}</h2>
          <p className="mt-4 leading-relaxed text-foreground/85">{lesson.body}</p>

          <div className="mt-8 flex items-center justify-between border-t border-border pt-6">
            <button
              disabled={selected === 0}
              onClick={() => setSelected((s) => Math.max(0, s - 1))}
              className="rounded-lg px-4 py-2 text-sm font-semibold text-muted-foreground disabled:opacity-40 hover:bg-secondary"
            >
              Previous
            </button>
            {selected < module.lessons.length - 1 ? (
              <button
                onClick={() => setSelected((s) => s + 1)}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-primary px-5 py-2.5 text-sm font-bold text-primary-foreground hover:bg-brand-secondary"
              >
                Next lesson <ChevronRight className="size-4" />
              </button>
            ) : quiz ? (
              <button
                onClick={() =>
                  navigate({ to: "/portal/quiz/$quizId", params: { quizId: quiz.id } })
                }
                className="inline-flex items-center gap-2 rounded-xl bg-brand-accent px-5 py-2.5 text-sm font-bold text-white hover:opacity-90"
              >
                Take the quiz <ChevronRight className="size-4" />
              </button>
            ) : (
              <span className="text-sm font-semibold text-brand-secondary">Module complete ✓</span>
            )}
          </div>
        </article>
      </div>
    </main>
  );
}

function Loading() {
  return <div className="grid place-items-center py-20 text-muted-foreground">Loading module…</div>;
}
function NotFound() {
  return (
    <div className="mx-auto max-w-md px-4 py-20 text-center">
      <h2 className="font-display text-2xl font-bold">Module not found</h2>
      <Link to="/portal" className="mt-4 inline-block font-semibold text-brand-primary">
        Back to learning
      </Link>
    </div>
  );
}
