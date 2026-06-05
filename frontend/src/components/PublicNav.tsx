import { useAuth } from "@/lib/store/auth";
import { Link } from "@tanstack/react-router";
import { Square } from "lucide-react";

export function PublicNav() {
  const user = useAuth((s) => s.user);
  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2">
          <div className="grid size-8 place-items-center rounded-lg bg-brand-primary">
            <Square className="size-4 text-primary-foreground" strokeWidth={2.5} />
          </div>
          <span className="font-display text-xl font-bold tracking-tight text-brand-primary">
            CredWise
          </span>
        </Link>
        <div className="hidden items-center gap-8 md:flex">
          <Link
            to="/mfi"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-brand-primary"
          >
            MFI Dashboard
          </Link>
          <Link
            to="/portal"
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-brand-primary"
          >
            Learning Portal
          </Link>
          {user ? (
            <Link
              to={user.role === "mfi_admin" ? "/mfi" : "/portal"}
              className="rounded-full bg-brand-primary px-5 py-2 text-sm font-semibold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary"
            >
              Open {user.role === "mfi_admin" ? "Dashboard" : "Portal"}
            </Link>
          ) : (
            <Link
              to="/auth/login"
              className="rounded-full bg-brand-primary px-5 py-2 text-sm font-semibold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary"
            >
              Get Started
            </Link>
          )}
        </div>
        <Link
          to="/auth/login"
          className="rounded-full bg-brand-primary px-4 py-2 text-xs font-semibold text-primary-foreground md:hidden"
        >
          Sign in
        </Link>
      </div>
    </nav>
  );
}
