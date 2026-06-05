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

  if (!hydrated || !user || user.role !== role) {
    return (
      <div className="grid min-h-screen place-items-center bg-brand-surface">
        <div className="size-8 animate-spin rounded-full border-2 border-brand-primary border-t-transparent" />
      </div>
    );
  }
  return <>{children}</>;
}
