import { useQuiz } from "@/lib/api/hooks";
import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowLeft, Check, X } from "lucide-react";
import { useState } from "react";
import { api, USE_MOCKS } from "@/lib/api/client";
import { toast } from "sonner";

export const Route = createFileRoute("/portal/quiz/$quizId")({
  head: () => ({ meta: [{ title: "Quiz - CredWise" }] }),
  component: QuizView,
});

function QuizView() {
  const { quizId } = Route.useParams();
  const { data: quiz, isLoading } = useQuiz(quizId);
  const [step, setStep] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [done, setDone] = useState(false);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [finalPct, setFinalPct] = useState<number | null>(null);
  const [correctCount, setCorrectCount] = useState(0);

  if (isLoading)
    return <div className="grid place-items-center py-20 text-muted-foreground">Loading quiz…</div>;
  if (!quiz) return null;

  const q = quiz.questions[step];
  const correct = picked !== null && picked === q.correctIndex;

  const handleFinish = async (nextAnswers: number[]) => {
    setIsSubmitting(true);
    if (USE_MOCKS) {
      const calculatedScore = nextAnswers.reduce(
        (acc, a, i) => acc + (a === quiz.questions[i].correctIndex ? 1 : 0),
        0,
      );
      setCorrectCount(calculatedScore);
      setFinalPct(Math.round((calculatedScore / quiz.questions.length) * 100));
      setDone(true);
      setIsSubmitting(false);
    } else {
      try {
        const answersDict: Record<string, string> = {};
        quiz.questions.forEach((qn: any, i: number) => {
          const pickedIndex = nextAnswers[i];
          answersDict[qn.id] = qn.options[pickedIndex];
        });

        const res = await api.post(`/quizzes/${quiz.id}/submit`, {
          answers: answersDict,
        });
        const attempt = res.data.data;

        // Instantly generate new credit readiness score based on new quiz score!
        await api.post("/credit-scores/generate");

        setCorrectCount(attempt.correct);
        setFinalPct(Math.round((attempt.correct / attempt.total_questions) * 100));
        setDone(true);
      } catch (err: any) {
        toast.error(
          err.response?.data?.message || "Failed to submit quiz results. Please try again."
        );
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  if (done) {
    const pct = finalPct ?? 0;
    return (
      <main className="mx-auto max-w-md px-4 py-12 text-center">
        <div className="rounded-3xl border border-border bg-card p-8 shadow-soft">
          <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
            Quiz complete
          </p>
          <h1 className="mt-2 font-display text-5xl font-black">{pct}%</h1>
          <p className="mt-2 text-muted-foreground">
            {correctCount} of {quiz.questions.length} correct
          </p>
          <p className="mt-6 text-sm">
            {pct >= 80
              ? "Excellent - you've added 8 points to your readiness score."
              : pct >= 60
                ? "Good work. Review the module to push your score higher."
                : "Keep going - try the lessons again and retake the quiz."}
          </p>
          <Link
            to="/portal"
            className="mt-8 block w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground hover:bg-brand-secondary"
          >
            Back to learning
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-2xl px-4 py-6">
      <Link
        to="/portal"
        className="mb-4 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> Exit quiz
      </Link>

      <div className="mb-6 flex items-center gap-4">
        <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-secondary">
          <div
            className="h-full rounded-full bg-brand-secondary transition-all"
            style={{ width: `${((step + 1) / quiz.questions.length) * 100}%` }}
          />
        </div>
        <span className="font-mono text-xs text-muted-foreground">
          {step + 1} / {quiz.questions.length}
        </span>
      </div>

      <div className="rounded-3xl border border-border bg-card p-6 shadow-soft md:p-8">
        <span className="rounded-full bg-brand-accent/15 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-brand-accent">
          Question
        </span>
        <h2 className="mt-4 font-display text-2xl font-bold leading-tight">{q.prompt}</h2>
        <div className="mt-6 space-y-3">
          {q.options.map((opt: string, i: number) => {
            const isPicked = picked === i;
            const showFeedback = picked !== null;
            const isCorrect = i === q.correctIndex;
            return (
              <button
                key={i}
                disabled={picked !== null}
                onClick={() => setPicked(i)}
                className={`flex w-full items-center justify-between rounded-xl border-2 px-5 py-4 text-left text-sm font-medium transition-all ${
                  picked !== null
                    ? isPicked
                      ? "border-brand-primary bg-brand-primary/10"
                      : "border-border opacity-60"
                    : "border-border hover:border-brand-primary hover:bg-brand-primary/5"
                }`}
              >
                {opt}
                {isPicked && <Check className="size-5 text-brand-primary" />}
              </button>
            );
          })}
        </div>

        {picked !== null && (
          <div
            className={`mt-5 rounded-xl p-4 text-sm ${correct ? "bg-brand-secondary/10 text-brand-secondary" : "bg-secondary text-foreground"}`}
          >
            <p className="font-bold">{correct ? "Correct!" : "Not quite."}</p>
            <p className="mt-1 text-foreground/80">{q.explanation}</p>
          </div>
        )}

        <button
          disabled={picked === null || isSubmitting}
          onClick={() => {
            const next = [...answers, picked!];
            setAnswers(next);
            setPicked(null);
            if (step + 1 >= quiz.questions.length) {
              handleFinish(next);
            } else {
              setStep((s) => s + 1);
            }
          }}
          className="mt-6 w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground transition-colors hover:bg-brand-secondary disabled:opacity-40"
        >
          {isSubmitting
            ? "Submitting..."
            : step + 1 >= quiz.questions.length
              ? "Finish quiz"
              : "Next question"}
        </button>
      </div>
    </main>
  );
}
