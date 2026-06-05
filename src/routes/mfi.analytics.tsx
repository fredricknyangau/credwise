import { createFileRoute } from "@tanstack/react-router";
import { useClients, useDashboard } from "@/lib/api/hooks";
import {
  Bar, BarChart, CartesianGrid, Cell, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";
import { AlertTriangle } from "lucide-react";

export const Route = createFileRoute("/mfi/analytics")({
  head: () => ({ meta: [{ title: "Analytics — MFI Dashboard" }] }),
  component: Analytics,
});

const RISK_COLORS = ["#dc2626", "#D97706", "#5ab59a", "#059669"];

function Analytics() {
  const { data: dash } = useDashboard();
  const { data: clients = [] } = useClients();

  const highRisk = clients.filter((c) => c.readinessScore < 45);

  return (
    <div className="px-6 py-8 md:px-10">
      <header className="mb-8">
        <h1 className="font-display text-3xl font-bold">Analytics</h1>
        <p className="mt-1 text-muted-foreground">Trends, distribution, and the clients who need outreach.</p>
      </header>

      <div className="grid gap-5 lg:grid-cols-2">
        <Card title="Literacy completion trend" subtitle="Weekly % of clients completing modules">
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={dash?.trend ?? []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="week" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }} />
              <Line type="monotone" dataKey="completion" stroke="#059669" strokeWidth={2.5} dot={{ r: 4, fill: "#059669" }} />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Readiness distribution" subtitle="By category">
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={dash?.distribution ?? []}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
              <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
              <YAxis stroke="#94a3b8" fontSize={12} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }} cursor={{ fill: "#059669", fillOpacity: 0.05 }} />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {(dash?.distribution ?? []).map((_, i) => <Cell key={i} fill={RISK_COLORS[i]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Module performance" subtitle="Completion rate per module" full>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={dash?.modulePerf ?? []} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" horizontal={false} />
              <XAxis type="number" stroke="#94a3b8" fontSize={12} />
              <YAxis type="category" dataKey="name" stroke="#94a3b8" fontSize={12} width={100} />
              <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", fontSize: 12 }} cursor={{ fill: "#059669", fillOpacity: 0.05 }} />
              <Bar dataKey="completion" fill="#065F46" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card title="High-risk clients" subtitle={`${highRisk.length} clients below 45 score`} full>
          <div className="divide-y divide-border">
            {highRisk.slice(0, 8).map((c) => (
              <div key={c.id} className="flex items-center justify-between py-3 text-sm">
                <div className="flex items-center gap-3">
                  <div className="grid size-9 place-items-center rounded-full bg-destructive/10 text-destructive">
                    <AlertTriangle className="size-4" />
                  </div>
                  <div>
                    <p className="font-semibold">{c.name}</p>
                    <p className="text-xs text-muted-foreground">{c.cooperative} · last active {c.lastActive}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-mono font-bold">{c.readinessScore}</p>
                  <p className="text-xs text-muted-foreground">{c.literacyProgress}% literacy</p>
                </div>
              </div>
            ))}
            {!highRisk.length && (
              <p className="py-6 text-center text-sm text-muted-foreground">No high-risk clients right now. 🎉</p>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

function Card({ title, subtitle, children, full }: { title: string; subtitle?: string; children: React.ReactNode; full?: boolean }) {
  return (
    <div className={`rounded-2xl border border-border bg-card p-6 shadow-soft ${full ? "lg:col-span-2" : ""}`}>
      <div className="mb-4">
        <h2 className="font-display text-lg font-bold">{title}</h2>
        {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
      </div>
      {children}
    </div>
  );
}
