import { PublicNav } from "@/components/PublicNav";
import { useAuth } from "@/lib/store/auth";
import type { UserRole } from "@/lib/types";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/auth/login")({
  validateSearch: (s: Record<string, unknown>) => ({
    role: (s.role === "mfi_admin" || s.role === "client" ? s.role : "client") as UserRole,
  }),
  head: () => ({ meta: [{ title: "Sign in - CredWise" }] }),
  component: Login,
});

import { api, USE_MOCKS } from "@/lib/api/client";

function Login() {
  const navigate = useNavigate();
  const search = Route.useSearch();
  const login = useAuth((s) => s.login);
  const setAuth = useAuth((s) => s.setAuth);
  const [role, setRole] = useState<UserRole>(search.role);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error("Please fill in both fields.");
      return;
    }

    if (USE_MOCKS) {
      login(email, role);
      toast.success(`Welcome back to CredWise`);
      navigate({ to: role === "mfi_admin" ? "/mfi" : "/portal" });
    } else {
      try {
        const loginRes = await api.post("/auth/login", {
          phone_number: email,
          password: password,
        });
        const { access_token } = loginRes.data.data;

        // Set token for this request
        api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

        const profileRes = await api.get("/users/me");
        const p = profileRes.data.data;

        setAuth(
          {
            id: p.id,
            name: p.full_name,
            email: p.phone_number,
            role: p.role as UserRole,
            organization: p.institution_id || undefined,
          },
          access_token,
        );

        toast.success(`Welcome back, ${p.full_name}`);
        navigate({ to: p.role === "mfi_admin" ? "/mfi" : "/portal" });
      } catch (err: any) {
        toast.error(
          err.response?.data?.message ||
            "Authentication failed. Please verify your phone number and password.",
        );
      }
    }
  };

  return (
    <div className="min-h-screen bg-brand-surface">
      <PublicNav />
      <main className="mx-auto grid max-w-md gap-6 px-4 py-16">
        <div>
          <h1 className="font-display text-3xl font-bold">Welcome back</h1>
          <p className="mt-2 text-muted-foreground">Sign in to continue your CredWise journey.</p>
        </div>

        <div className="grid grid-cols-2 gap-2 rounded-xl bg-secondary p-1">
          {(["client", "mfi_admin"] as const).map((r) => (
            <button
              key={r}
              onClick={() => setRole(r)}
              className={`rounded-lg py-2 text-sm font-semibold transition-colors ${
                role === r ? "bg-card text-brand-primary shadow-soft" : "text-muted-foreground"
              }`}
            >
              {r === "client" ? "I'm a Learner" : "MFI Admin"}
            </button>
          ))}
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-4 rounded-2xl border border-border bg-card p-6 shadow-soft"
        >
          <label className="block text-sm">
            <span className="mb-1 block font-medium">{USE_MOCKS ? "Email" : "Phone Number"}</span>
            <input
              type={USE_MOCKS ? "email" : "text"}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm outline-none ring-brand-secondary focus:ring-2"
              placeholder={
                USE_MOCKS
                  ? role === "mfi_admin"
                    ? "admin@coop.org"
                    : "you@example.com"
                  : role === "mfi_admin"
                    ? "+254711100001"
                    : "+254722000001"
              }
            />
          </label>
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Password</span>
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm outline-none ring-brand-secondary focus:ring-2"
              placeholder="••••••••"
            />
          </label>
          <button
            type="submit"
            className="w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary"
          >
            Sign in
          </button>
          <p className="text-center text-xs text-muted-foreground"></p>
        </form>

        {role === "mfi_admin" ? (
          <p className="text-center text-sm text-muted-foreground">
            New institution?{" "}
            <Link to="/auth/register" className="font-semibold text-brand-primary hover:underline">
              Register your MFI
            </Link>
          </p>
        ) : (
          <p className="text-center text-sm text-muted-foreground">
            New to CredWise?{" "}
            <Link
              to="/auth/register-learner"
              className="font-semibold text-brand-primary hover:underline"
            >
              Sign up as a Learner
            </Link>
          </p>
        )}
      </main>
    </div>
  );
}
