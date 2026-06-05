import { PublicNav } from "@/components/PublicNav";
import { useAuth } from "@/lib/store/auth";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { toast } from "sonner";
import { api, USE_MOCKS } from "@/lib/api/client";

export const Route = createFileRoute("/auth/register-learner")({
  head: () => ({ meta: [{ title: "Sign up as a Learner - CredWise" }] }),
  component: RegisterLearner,
});

function RegisterLearner() {
  const navigate = useNavigate();
  const login = useAuth((s) => s.login);
  const setAuth = useAuth((s) => s.setAuth);
  const [form, setForm] = useState({
    name: "",
    phone: "",
    password: "",
  });

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.password || !form.name || !form.phone) {
      toast.error("Please fill in all required fields.");
      return;
    }

    if (USE_MOCKS) {
      login(form.phone, "client", form.name);
      toast.success(`Welcome to CredWise, ${form.name}!`);
      navigate({ to: "/portal" });
    } else {
      try {
        const regRes = await api.post("/auth/register-learner", {
          full_name: form.name,
          phone_number: form.phone,
          password: form.password,
        });

        // The endpoint automatically logs the user in and returns the TokenResponse
        const { access_token } = regRes.data.data;

        // Set token
        api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

        const profileRes = await api.get("/users/me");
        const p = profileRes.data.data;

        setAuth(
          {
            id: p.id,
            name: p.full_name,
            email: p.phone_number,
            role: "client",
            organization: p.institution_id || undefined,
          },
          access_token
        );

        toast.success(`Welcome to CredWise, ${form.name}!`);
        navigate({ to: "/portal" });
      } catch (err: any) {
        toast.error(
          err.response?.data?.message ||
            "Registration failed. Make sure your phone number is unique and password is strong."
        );
      }
    }
  };

  return (
    <div className="min-h-screen bg-brand-surface">
      <PublicNav />
      <main className="mx-auto grid max-w-lg gap-6 px-4 py-16">
        <div>
          <span className="text-xs font-bold uppercase tracking-widest text-brand-secondary">
            For Learners
          </span>
          <h1 className="mt-2 font-display text-3xl font-bold">Create your account</h1>
          <p className="mt-2 text-muted-foreground">
            Start learning and track your financial readiness in minutes.
          </p>
        </div>
        <form
          onSubmit={handleSubmit}
          className="space-y-4 rounded-2xl border border-border bg-card p-6 shadow-soft"
        >
          <Field
            label="Full name"
            value={form.name}
            onChange={set("name")}
            placeholder="John Doe"
          />
          <Field
            label="Phone Number"
            value={form.phone}
            onChange={set("phone")}
            placeholder="+254711223344"
          />
          <Field
            label="Password"
            type="password"
            value={form.password}
            onChange={set("password")}
            placeholder="••••••••"
          />
          <button className="w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary">
            Sign up
          </button>
          <p className="text-center text-sm text-muted-foreground">
            Already registered?{" "}
            <Link
              to="/auth/login"
              search={{ role: "client" }}
              className="font-semibold text-brand-primary hover:underline"
            >
              Sign in
            </Link>
          </p>
        </form>
      </main>
    </div>
  );
}

function Field({
  label,
  value,
  onChange,
  placeholder,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium">{label}</span>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm outline-none ring-brand-secondary focus:ring-2"
      />
    </label>
  );
}
