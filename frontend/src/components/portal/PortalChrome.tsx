import { useAuth } from "@/lib/store/auth";
import { useModules } from "@/lib/api/hooks";
import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { BookOpen, Gauge, Home, LogOut, Square, User } from "lucide-react";

export function PortalChrome() {
  const path = useRouterState({ select: (r) => r.location.pathname });
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { data: modules = [] } = useModules();
  
  const currentModule = modules.find((m: any) => m.progress > 0 && m.progress < 100) ?? modules[0];
  const learnPath = currentModule ? `/portal/modules/${currentModule.id}` : "/portal";

  const items = [
    { to: "/portal", label: "Home", icon: Home, exact: true },
    { to: learnPath, label: "Learn", icon: BookOpen },
    { to: "/portal/readiness", label: "Score", icon: Gauge },
    { to: "/portal/profile", label: "Profile", icon: User },
  ];

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

      {/* Bottom mobile nav - Always visible to enforce mobile-first testing */}
      <nav className="fixed bottom-0 left-1/2 z-40 w-full max-w-md -translate-x-1/2 border-x border-t border-border bg-card/95 px-2 pb-[env(safe-area-inset-bottom)] pt-2 backdrop-blur sm:bottom-8 sm:rounded-b-[2.5rem]">
        <div className="mx-auto flex justify-between">
          {items.map((it) => {
            const active = isActive(it.to, it.exact);
            return (
              <Link
                key={it.label}
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
