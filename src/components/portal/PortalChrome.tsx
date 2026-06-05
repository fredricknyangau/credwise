import { useAuth } from "@/lib/store/auth";
import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { BookOpen, Gauge, Home, LogOut, Square, User } from "lucide-react";

const items = [
  { to: "/portal", label: "Home", icon: Home, exact: true },
  { to: "/portal/modules/m1", label: "Learn", icon: BookOpen },
  { to: "/portal/readiness", label: "Score", icon: Gauge },
  { to: "/portal/profile", label: "Profile", icon: User },
];

export function PortalChrome() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const isActive = (to: string, exact?: boolean) =>
    exact
      ? path === to
      : path === to || (to !== "/portal" && path.startsWith(to.split("/").slice(0, 3).join("/")));

  return (
    <>
      {/* Top bar on mobile, full nav on desktop */}
      <header className="sticky top-0 z-40 border-b border-border bg-brand-surface/85 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-3xl items-center justify-between px-4">
          <Link to="/portal" className="flex items-center gap-2">
            <div className="grid size-8 place-items-center rounded-lg bg-brand-primary">
              <Square className="size-4 text-primary-foreground" strokeWidth={2.5} />
            </div>
            <span className="font-display text-lg font-bold text-brand-primary">CredWise</span>
          </Link>
          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-xs font-semibold">{user?.name}</p>
              <p className="text-[10px] text-muted-foreground">Learner</p>
            </div>
            <div className="grid size-9 place-items-center rounded-full bg-brand-secondary text-sm font-bold text-primary-foreground">
              {user?.name?.[0]?.toUpperCase() ?? "?"}
            </div>
            <button
              onClick={() => {
                logout();
                navigate({ to: "/" });
              }}
              className="grid size-9 place-items-center rounded-full text-muted-foreground hover:bg-secondary"
              aria-label="Sign out"
            >
              <LogOut className="size-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Bottom mobile nav */}
      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-border bg-card/95 px-2 pb-[env(safe-area-inset-bottom)] pt-2 backdrop-blur md:hidden">
        <div className="mx-auto flex max-w-md justify-between">
          {items.map((it) => {
            const active = isActive(it.to, it.exact);
            return (
              <Link
                key={it.to}
                to={it.to}
                className={`flex flex-1 flex-col items-center gap-1 rounded-lg py-2 text-[10px] font-bold transition-colors ${
                  active ? "text-brand-primary" : "text-muted-foreground"
                }`}
              >
                <it.icon className={`size-5 ${active ? "stroke-[2.5]" : ""}`} />
                {it.label}
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}
