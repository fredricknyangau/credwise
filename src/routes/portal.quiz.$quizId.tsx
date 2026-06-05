import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuiz } from "@/lib/api/hooks";
import { useState } from "react";
import { ArrowLeft, Check, X } from "lucide-react";

export const Route = createFileRoute("/portal/quiz/$quizId")({
  head: () => ({ meta: [{ title: "Quiz — CrediPath" }] }),
  component: QuizView,
});

function QuizView() {
  const { quizId } = Route.useParams();
  const { data: quiz, isLoading } = useQuiz(quizId);
  const [step, setStep] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [done, setDone] = useState(false);

  if (isLoading) return <div className="grid place-items-center py-20 text-muted-foreground">Loading quiz…</div>;
  if (!quiz) return null;

  const q = quiz.questions[step];
  const correct = picked !== null && picked === q.correctIndex;
  const score = answers.reduce((acc, a, i) => acc + (a === quiz.questions[i].correctIndex ? 1 : 0), 0);

  if (done) {
    const pct = Math.round((score / quiz.questions.length) * 100);
    return (
      <main className="mx-auto max-w-md px-4 py-12 text-center">
        <div className="rounded-3xl border border-border bg-card p-8 shadow-soft">
          <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">Quiz complete</p>
          <h1 className="mt-2 font-display text-5xl font-black">{pct}%</h1>
          <p className="mt-2 text-muted-foreground">{score} of {quiz.questions.length} correct</p>
          <p className="mt-6 text-sm">
            {pct >= 80
              ? "Excellent — you've added 8 points to your readiness score."
              : pct >= 60
              ? "Good work. Review the module to push your score higher."
              : "Keep going — try the lessons again and retake the quiz."}
          </p>
          <Link to="/portal" className="mt-8 block w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground hover:bg-brand-secondary">
            Back to learning
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl px-4 py-6">
      <Link to="/portal" className="mb-4 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground">
        <ArrowLeft className="size-4" /> Exit quiz
      </Link>

      <div className="mb-6 flex items-center gap-4">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-secondary">
          <div className="h-full rounded-full bg-brand-secondary transition-all" style={{ width: `${((step + 1) / quiz.questions.length) * 100}%` }} />
        </div>
        <span className="font-mono text-xs text-muted-foreground">{step + 1} / {quiz.questions.length}</span>
      </div>

      <div className="rounded-3xl border border-border bg-card p-6 shadow-soft md:p-8">
        <span className="rounded-full bg-brand-accent/15 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-brand-accent">
          Question
        </span>
        <h2 className="mt-4 font-display text-2xl font-bold leading-tight">{q.prompt}</h2>
        <div className="mt-6 space-y-3">
          {q.options.map((opt, i) => {
            const isPicked = picked === i;
            const showFeedback = picked !== null;
            const isCorrect = i === q.correctIndex;
            return (
              <button
                key={i}
                disabled={picked !== null}
                onClick={() => setPicked(i)}
                className={`flex w-full items-center justify-between rounded-xl border-2 px-5 py-4 text-left text-sm font-medium transition-all ${
                  showFeedback
                    ? isCorrect
                      ? "border-brand-secondary bg-brand-secondary/10"
                      : isPicked
                      ? "border-destructive bg-destructive/10"
                      : "border-border opacity-60"
                    : "border-border hover:border-brand-primary hover:bg-brand-primary/5"
                }`}
              >
                {opt}
                {showFeedback && isCorrect && <Check className="size-5 text-brand-secondary" />}
                {showFeedback && isPicked && !isCorrect && <X className="size-5 text-destructive" />}
              </button>
            );
          })}
        </div>

        {picked !== null && (
          <div className={`mt-5 rounded-xl p-4 text-sm ${correct ? "bg-brand-secondary/10 text-brand-secondary" : "bg-secondary text-foreground"}`}>
            <p className="font-bold">{correct ? "Correct!" : "Not quite."}</p>
            <p className="mt-1 text-foreground/80">{q.explanation}</p>
          </div>
        )}

        <button
          disabled={picked === null}
          onClick={() => {
            const next = [...answers, picked!];
            setAnswers(next);
            setPicked(null);
            if (step + 1 >= quiz.questions.length) setDone(true);
            else setStep((s) => s + 1);
          }}
          className="mt-6 w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground transition-colors hover:bg-brand-secondary disabled:opacity-40"
        >
          {step + 1 >= quiz.questions.length ? "Finish quiz" : "Next question"}
        </button>
      </div>
    </main>
  );
}
