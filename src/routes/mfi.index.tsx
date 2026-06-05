import { createFileRoute } from "@tanstack/react-router";
import { useDashboard } from "@/lib/api/hooks";
import { useAuth } from "@/lib/store/auth";
import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Pie, PieChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { ArrowUpRight, Activity, Award, BookOpenCheck, Users } from "lucide-react";

export const Route = createFileRoute("/mfi/")({
  head: () => ({ meta: [{ title: "Overview — MFI Dashboard" }] }),
  component: Overview,
});

const COLORS = ["#a7d5c5", "#5ab59a", "#059669", "#065F46"];

function Overview() {
  const { data } = useDashboard();
  const user = useAuth((s) => s.user);

  return (
    <div className="px-6 py-8 md:px-10">
      <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
            {user?.organization ?? "Institution Overview"}
          </p>
          <h1 className="mt-1 font-display text-3xl font-bold">Hello, {user?.name?.split(" ")[0] ?? "there"}.</h1>
          <p className="mt-1 text-muted-foreground">Here's how your community is progressing today.</p>
        </div>
        <div className="rounded-full bg-brand-primary/5 px-3 py-1 text-xs font-semibold text-brand-primary">
          <span className="mr-1.5 inline-block size-1.5 animate-pulse rounded-full bg-brand-secondary align-middle" />
          Live updates
        </div>
      </header>

      {/* KPIs */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi icon={Users} label="Total clients" value={data?.totalClients ?? "—"} trend="+12% this month" tone="brand" />
        <Kpi icon={Activity} label="Active learners" value={data?.activeLearners ?? "—"} trend="68% of total" tone="brand" />
        <Kpi icon={Award} label="Avg readiness" value={data?.averageReadiness ?? "—"} progress={data?.averageReadiness} tone="brand" />
        <Kpi icon={BookOpenCheck} label="Completion rate" value={`${data?.completionRate ?? "—"}%`} trend="High engagement" tone="accent" />
      </div>

      {/* Charts */}
      <div className="mt-6 grid gap-5 lg:grid-cols-3">
        <div className="rounded-2xl border border-border bg-card p-6 shadow-soft lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="font-display text-lg font-bold">Literacy & readiness trend</h2>
              <p className="text-xs text-muted-foreground">Last 8 weeks</p>
            </div>
            <span className="rounded-full bg-brand-secondary/10 px-2.5 py-1 text-xs font-semibold text-brand-secondary">
              <ArrowUpRight className="mr-0.5 inline size-3" /> +14%
            </span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={data?.trend ?? []}>
              <defs>
                <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#059669" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#059669" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="g2" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#065F46" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#065F46" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="week" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip
                contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }}
                cursor={{ stroke: "#059669", strokeWidth: 1, strokeDasharray: "3 3" }}
              />
              <Area type="monotone" dataKey="completion" stroke="#059669" strokeWidth={2} fill="url(#g1)" name="Literacy %" />
              <Area type="monotone" dataKey="readiness" stroke="#065F46" strokeWidth={2} fill="url(#g2)" name="Readiness" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6 shadow-soft">
          <h2 className="font-display text-lg font-bold">Readiness distribution</h2>
          <p className="text-xs text-muted-foreground">By client category</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={data?.distribution ?? []}
                dataKey="value"
                nameKey="name"
                innerRadius={50}
                outerRadius={80}
                paddingAngle={2}
              >
                {(data?.distribution ?? []).map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-2 space-y-1.5">
            {(data?.distribution ?? []).map((d, i) => (
              <div key={d.name} className="flex items-center justify-between text-xs">
                <span className="flex items-center gap-2">
                  <span className="size-2.5 rounded-sm" style={{ background: COLORS[i] }} />
                  {d.name}
                </span>
                <span className="font-mono font-semibold">{d.value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-card p-6 shadow-soft lg:col-span-3">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="font-display text-lg font-bold">Module performance</h2>
              <p className="text-xs text-muted-foreground">Completion rate per module</p>
            </div>
            <span className="text-xs font-medium text-brand-accent">High engagement</span>
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data?.modulePerf ?? []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }} cursor={{ fill: "#059669", fillOpacity: 0.05 }} />
              <Bar dataKey="completion" fill="#059669" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function Kpi({
  icon: Icon, label, value, trend, progress, tone,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: React.ReactNode;
  trend?: string;
  progress?: number;
  tone?: "brand" | "accent";
}) {
  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-soft">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">{label}</p>
        <div className={`grid size-9 place-items-center rounded-lg ${
          tone === "accent" ? "bg-brand-accent/10 text-brand-accent" : "bg-brand-primary/10 text-brand-primary"
        }`}>
          <Icon className="size-4" />
        </div>
      </div>
      <p className="mt-2 font-display text-3xl font-bold">{value}</p>
      {progress !== undefined ? (
        <div className="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-secondary">
          <div className="h-full bg-brand-secondary transition-all" style={{ width: `${progress}%` }} />
        </div>
      ) : (
        trend && (
          <span className="mt-3 inline-flex items-center rounded-full bg-brand-secondary/10 px-2 py-0.5 text-xs font-semibold text-brand-secondary">
            {trend}
          </span>
        )
      )}
    </div>
  );
}
