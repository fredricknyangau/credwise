import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useAuth } from "@/lib/store/auth";
import { PublicNav } from "@/components/PublicNav";
import { toast } from "sonner";

export const Route = createFileRoute("/auth/register")({
  head: () => ({ meta: [{ title: "Register your MFI — CrediPath" }] }),
  component: Register,
});

function Register() {
  const navigate = useNavigate();
  const login = useAuth((s) => s.login);
  const [form, setForm] = useState({ org: "", name: "", email: "", password: "" });

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!form.org || !form.email || !form.password || !form.name) {
      toast.error("All fields are required.");
      return;
    }
    login(form.email, "mfi_admin", form.name, form.org);
    toast.success(`${form.org} is now on CrediPath`);
    navigate({ to: "/mfi" });
  };

  return (
    <div className="min-h-screen bg-brand-surface">
      <PublicNav />
      <main className="mx-auto grid max-w-lg gap-6 px-4 py-16">
        <div>
          <span className="text-xs font-bold uppercase tracking-widest text-brand-secondary">For Institutions</span>
          <h1 className="mt-2 font-display text-3xl font-bold">Register your MFI</h1>
          <p className="mt-2 text-muted-foreground">
            Set up your institution dashboard in under a minute.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-border bg-card p-6 shadow-soft">
          <Field label="Institution name" value={form.org} onChange={set("org")} placeholder="Dakar Cooperative Union" />
          <Field label="Your name" value={form.name} onChange={set("name")} placeholder="Adaeze N." />
          <Field label="Work email" type="email" value={form.email} onChange={set("email")} placeholder="you@coop.org" />
          <Field label="Password" type="password" value={form.password} onChange={set("password")} placeholder="••••••••" />
          <button className="w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary">
            Create institution account
          </button>
          <p className="text-center text-sm text-muted-foreground">
            Already registered?{" "}
            <Link to="/auth/login" search={{ role: "mfi_admin" }} className="font-semibold text-brand-primary hover:underline">
              Sign in
            </Link>
          </p>
        </form>
      </main>
    </div>
  );
}

function Field({
  label, value, onChange, placeholder, type = "text",
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
