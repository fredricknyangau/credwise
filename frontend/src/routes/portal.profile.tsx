import type { FinancialProfile } from "@/lib/types";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ArrowLeft, ArrowRight, Check } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/portal/profile")({
  head: () => ({ meta: [{ title: "Financial profile - CredWise" }] }),
  component: ProfileForm,
});

const steps = [
  {
    key: "incomeRange" as const,
    title: "Roughly, what is your weekly income?",
    options: ["Under $20", "$20 – $50", "$50 – $150", "$150 – $400", "Over $400"],
  },
  {
    key: "savingsHabit" as const,
    title: "How often do you save?",
    options: ["Daily", "Weekly", "Monthly", "Rarely", "Not yet"],
  },
  {
    key: "businessType" as const,
    title: "What best describes your work?",
    options: [
      "Market trader",
      "Tailoring / textiles",
      "Farming",
      "Food vendor",
      "Services",
      "Other",
    ],
  },
  {
    key: "cooperative" as const,
    title: "Are you part of a cooperative or savings group?",
    options: ["Yes, very active", "Yes, occasionally", "Yes, but inactive", "No, not yet"],
  },
];

function ProfileForm() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [profile, setProfile] = useState<Partial<FinancialProfile>>({});

  const current = steps[step];
  const pick = (val: string) => {
    setProfile((p) => ({ ...p, [current.key]: val }));
    if (step + 1 < steps.length) {
      setTimeout(() => setStep((s) => s + 1), 200);
    } else {
      setTimeout(() => {
        toast.success("Profile saved - +6 to your readiness score");
        navigate({ to: "/portal/readiness" });
      }, 250);
    }
  };

  return (
    <main className="mx-auto max-w-xl px-4 py-6">
      <button
        onClick={() => (step === 0 ? navigate({ to: "/portal" }) : setStep((s) => s - 1))}
        className="mb-4 inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> Back
      </button>

      <header className="mb-6">
        <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
          Financial profile
        </p>
        <h1 className="mt-1 font-display text-2xl font-bold">Help us understand you better</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          A few questions so we can tailor your readiness path.
        </p>
      </header>

      <div className="mb-6 flex items-center gap-2">
        {steps.map((_, i) => (
          <div
            key={i}
            className={`h-1.5 flex-1 rounded-full transition-all ${i <= step ? "bg-brand-secondary" : "bg-secondary"}`}
          />
        ))}
      </div>

      <div className="rounded-3xl border border-border bg-card p-6 shadow-soft md:p-8">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Step {step + 1} of {steps.length}
        </p>
        <h2 className="mt-2 font-display text-xl font-bold">{current.title}</h2>
        <div className="mt-6 space-y-3">
          {current.options.map((opt) => {
            const selected = profile[current.key] === opt;
            return (
              <button
                key={opt}
                onClick={() => pick(opt)}
                className={`flex w-full items-center justify-between rounded-xl border-2 px-5 py-4 text-left text-sm font-medium transition-all ${
                  selected
                    ? "border-brand-primary bg-brand-primary/5"
                    : "border-border hover:border-brand-primary/40"
                }`}
              >
                {opt}
                {selected ? (
                  <Check className="size-5 text-brand-primary" />
                ) : (
                  <ArrowRight className="size-4 text-muted-foreground" />
                )}
              </button>
            );
          })}
        </div>
      </div>
    </main>
  );
}
