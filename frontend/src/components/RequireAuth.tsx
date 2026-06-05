import { useEffect, type ReactNode } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/lib/store/auth";
import type { UserRole } from "@/lib/types";

interface Props {
  role: UserRole;
  children: ReactNode;
}

/**
 * Component-level auth gate. Renders nothing during SSR / pre-hydration,
 * redirects to /auth/login if no user or wrong role.
 */
export function RequireAuth({ role, children }: Props) {
  const navigate = useNavigate();
  const { user, hydrated } = useAuth();

  useEffect(() => {
    if (!hydrated) return;
    if (!user) navigate({ to: "/auth/login", search: { role } });
    else if (user.role !== role) navigate({ to: user.role === "mfi_admin" ? "/mfi" : "/portal" });
  }, [hydrated, user, role, navigate]);

  if (!hydrated) {
    return (
      <div className="grid min-h-screen place-items-center bg-brand-surface">
        <div className="size-8 animate-spin rounded-full border-2 border-brand-primary border-t-transparent" />
      </div>
    );
  }

  if (!user || user.role !== role) {
    return (
      <div className="grid min-h-screen place-items-center bg-brand-surface px-4 text-center">
        <div>
          <h2 className="text-xl font-bold text-foreground">Access Denied</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            You do not have permission to view this page. 
            (Current role: {user?.role || "none"}, Required: {role})
          </p>
          <button
            onClick={() => {
              useAuth.getState().logout();
              navigate({ to: "/auth/login" });
            }}
            className="mt-6 rounded-full bg-brand-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-brand-secondary"
          >
            Sign out
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
