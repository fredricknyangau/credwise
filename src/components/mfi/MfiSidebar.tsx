import { useAuth } from "@/lib/store/auth";
import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { BarChart3, LayoutDashboard, LogOut, Square, Users } from "lucide-react";

const items = [
  { to: "/mfi", label: "Overview", icon: LayoutDashboard, exact: true },
  { to: "/mfi/clients", label: "Clients", icon: Users },
  { to: "/mfi/analytics", label: "Analytics", icon: BarChart3 },
];

export function MfiSidebar() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const isActive = (to: string, exact?: boolean) =>
    exact ? path === to : path === to || path.startsWith(to + "/");

  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-border bg-sidebar md:flex">
      <Link to="/" className="flex h-16 items-center gap-2 border-b border-border px-6">
        <div className="grid size-8 place-items-center rounded-lg bg-brand-primary">
          <Square className="size-4 text-primary-foreground" strokeWidth={2.5} />
        </div>
        <span className="font-display text-xl font-bold tracking-tight text-brand-primary">
          CredWise
        </span>
      </Link>
      <div className="px-4 py-5">
        <p className="px-3 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          {user?.organization ?? "Institution"}
        </p>
      </div>
      <nav className="flex-1 space-y-1 px-3">
        {items.map((it) => {
          const active = isActive(it.to, it.exact);
          return (
            <Link
              key={it.to}
              to={it.to}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                active
                  ? "bg-brand-primary text-primary-foreground shadow-soft"
                  : "text-foreground hover:bg-sidebar-accent"
              }`}
            >
              <it.icon className="size-4" />
              {it.label}
            </Link>
          );
        })}
      </nav>
      <div className="border-t border-border p-4">
        <div className="mb-3 flex items-center gap-3">
          <div className="grid size-9 place-items-center rounded-full bg-brand-secondary text-sm font-bold text-primary-foreground">
            {user?.name?.[0]?.toUpperCase() ?? "?"}
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold">{user?.name}</p>
            <p className="truncate text-xs text-muted-foreground">{user?.email}</p>
          </div>
        </div>
        <button
          onClick={() => {
            logout();
            navigate({ to: "/" });
          }}
          className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-secondary"
        >
          <LogOut className="size-4" /> Sign out
        </button>
      </div>
    </aside>
  );
}
