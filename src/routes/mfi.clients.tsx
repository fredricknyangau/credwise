import { createFileRoute } from "@tanstack/react-router";
import { useClients } from "@/lib/api/hooks";
import { useMemo, useState } from "react";
import { Search, Plus, ChevronRight } from "lucide-react";
import type { Client, ReadinessCategory } from "@/lib/types";

export const Route = createFileRoute("/mfi/clients")({
  head: () => ({ meta: [{ title: "Clients - MFI Dashboard" }] }),
  component: Clients,
});

const catColor: Record<ReadinessCategory, string> = {
  Strong: "bg-brand-primary/10 text-brand-primary",
  Ready: "bg-brand-secondary/15 text-brand-secondary",
  Developing: "bg-brand-accent/15 text-brand-accent",
  Building: "bg-secondary text-muted-foreground",
};

function Clients() {
  const { data, isLoading } = useClients();
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<"all" | ReadinessCategory>("all");
  const [open, setOpen] = useState<Client | null>(null);

  const filtered = useMemo(() => {
    const list = data ?? [];
    return list.filter((c) => {
      const matchesQ =
        c.name.toLowerCase().includes(q.toLowerCase()) ||
        c.cooperative.toLowerCase().includes(q.toLowerCase());
      const matchesF = filter === "all" || c.category === filter;
      return matchesQ && matchesF;
    });
  }, [data, q, filter]);

  return (
    <div className="px-6 py-8 md:px-10">
      <header className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold">Clients</h1>
          <p className="mt-1 text-muted-foreground">
            Track, filter, and review every client in your portfolio.
          </p>
        </div>
        <button className="inline-flex items-center gap-2 rounded-xl bg-brand-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary">
          <Plus className="size-4" /> Add client
        </button>
      </header>

      <div className="mb-4 flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-64">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search by name or cooperative…"
            className="w-full rounded-lg border border-input bg-card py-2.5 pl-9 pr-3 text-sm outline-none ring-brand-secondary focus:ring-2"
          />
        </div>
        <div className="flex flex-wrap gap-1.5 rounded-lg bg-secondary p-1">
          {(["all", "Strong", "Ready", "Developing", "Building"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`rounded-md px-3 py-1.5 text-xs font-semibold capitalize transition-colors ${
                filter === f ? "bg-card text-foreground shadow-soft" : "text-muted-foreground"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-soft">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-border bg-secondary/50 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
            <tr>
              <th className="px-5 py-3">Client</th>
              <th className="px-5 py-3 hidden md:table-cell">Cooperative</th>
              <th className="px-5 py-3">Progress</th>
              <th className="px-5 py-3 hidden sm:table-cell">Readiness</th>
              <th className="px-5 py-3">Status</th>
              <th className="px-5 py-3 hidden lg:table-cell">Last active</th>
              <th className="px-5 py-3 w-10"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {isLoading && (
              <tr>
                <td colSpan={7} className="px-5 py-10 text-center text-muted-foreground">
                  Loading clients…
                </td>
              </tr>
            )}
            {filtered.map((c) => (
              <tr
                key={c.id}
                onClick={() => setOpen(c)}
                className="cursor-pointer transition-colors hover:bg-secondary/40"
              >
                <td className="px-5 py-4">
                  <div className="flex items-center gap-3">
                    <div className="grid size-9 place-items-center rounded-full bg-brand-secondary/15 text-sm font-bold text-brand-primary">
                      {c.name[0]}
                    </div>
                    <div>
                      <p className="font-semibold">{c.name}</p>
                      <p className="text-xs text-muted-foreground">{c.phone}</p>
                    </div>
                  </div>
                </td>
                <td className="px-5 py-4 hidden md:table-cell text-muted-foreground">
                  {c.cooperative}
                </td>
                <td className="px-5 py-4">
                  <div className="flex items-center gap-2.5">
                    <span className="w-9 font-mono text-xs">{c.literacyProgress}%</span>
                    <div className="h-1.5 w-24 overflow-hidden rounded-full bg-secondary">
                      <div
                        className="h-full bg-brand-secondary"
                        style={{ width: `${c.literacyProgress}%` }}
                      />
                    </div>
                  </div>
                </td>
                <td className="px-5 py-4 hidden sm:table-cell font-mono text-sm font-semibold">
                  {c.readinessScore}
                </td>
                <td className="px-5 py-4">
                  <span
                    className={`rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider ${catColor[c.category]}`}
                  >
                    {c.category}
                  </span>
                </td>
                <td className="px-5 py-4 hidden lg:table-cell text-xs text-muted-foreground">
                  {c.lastActive}
                </td>
                <td className="px-5 py-4 text-right text-muted-foreground">
                  <ChevronRight className="inline size-4" />
                </td>
              </tr>
            ))}
            {!isLoading && !filtered.length && (
              <tr>
                <td colSpan={7} className="px-5 py-10 text-center text-muted-foreground">
                  No clients match those filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Detail drawer */}
      {open && (
        <div
          className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm"
          onClick={() => setOpen(null)}
        >
          <div
            className="absolute right-0 top-0 h-full w-full max-w-md overflow-y-auto bg-card p-8 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-6 flex items-center gap-4">
              <div className="grid size-14 place-items-center rounded-full bg-brand-primary text-xl font-bold text-primary-foreground">
                {open.name[0]}
              </div>
              <div>
                <h3 className="font-display text-xl font-bold">{open.name}</h3>
                <p className="text-sm text-muted-foreground">
                  {open.cooperative} · {open.phone}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Stat label="Readiness" value={open.readinessScore} />
              <Stat label="Literacy" value={`${open.literacyProgress}%`} />
            </div>
            <div className="mt-5 rounded-xl bg-secondary/50 p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Category
              </p>
              <p className="mt-1 font-display text-2xl font-bold">{open.category}</p>
              <p className="mt-2 text-sm text-muted-foreground">
                {open.category === "Strong" &&
                  "Eligible for highest loan tier. Recommend periodic literacy refreshers."}
                {open.category === "Ready" &&
                  "Eligible for standard credit. Encourage savings consistency."}
                {open.category === "Developing" &&
                  "Promising but needs to complete more modules and build savings history."}
                {open.category === "Building" &&
                  "Early-stage learner. Focus on basics of savings and weekly check-ins."}
              </p>
            </div>
            <div className="mt-5 space-y-2">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Recent activity
              </p>
              {[
                "Completed lesson: Setting a savings goal",
                "Quiz passed: Basics of Savings (90%)",
                "Profile updated: business type",
              ].map((a) => (
                <div key={a} className="flex items-start gap-2 text-sm">
                  <span className="mt-1.5 size-1.5 rounded-full bg-brand-secondary" /> {a}
                </div>
              ))}
            </div>
            <button
              onClick={() => setOpen(null)}
              className="mt-8 w-full rounded-xl border border-border bg-card py-3 text-sm font-semibold hover:bg-secondary"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border p-4">
      <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {label}
      </p>
      <p className="mt-1 font-display text-2xl font-bold">{value}</p>
    </div>
  );
}
