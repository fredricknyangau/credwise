import { PublicNav } from "@/components/PublicNav";
import { useAuth } from "@/lib/store/auth";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { toast } from "sonner";

export const Route = createFileRoute("/auth/register")({
  head: () => ({ meta: [{ title: "Register your MFI - CredWise" }] }),
  component: Register,
});

import { api, USE_MOCKS } from "@/lib/api/client";

function Register() {
  const navigate = useNavigate();
  const login = useAuth((s) => s.login);
  const setAuth = useAuth((s) => s.setAuth);
  const [form, setForm] = useState({
    org: "",
    name: "",
    email: "",
    phone: "",
    location: "Nairobi, Kenya",
    password: "",
  });

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.org || !form.email || !form.password || !form.name || !form.phone) {
      toast.error("Please fill in all required fields.");
      return;
    }

    if (USE_MOCKS) {
      login(form.email, "mfi_admin", form.name, form.org);
      toast.success(`${form.org} is now on CredWise`);
      navigate({ to: "/mfi" });
    } else {
      try {
        const regRes = await api.post("/auth/register-mfi", {
          institution_name: form.org,
          institution_email: form.email,
          institution_phone: form.phone,
          institution_location: form.location,
          admin_full_name: form.name,
          admin_phone: form.phone, // using the same phone for simplicity
          admin_password: form.password,
        });

        // Registration returns { success, data: { access_token, user: { ... } } }
        // Let's check: actually backend register_mfi returns:
        // MFIRegistrationResponse: id, name, email, phone, location, admin_id, admin_name, admin_phone, role
        // Then we can immediately log them in!
        const loginRes = await api.post("/auth/login", {
          phone_number: form.phone,
          password: form.password,
        });
        const { access_token } = loginRes.data.data;

        // Set token
        api.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;

        const profileRes = await api.get("/users/me");
        const p = profileRes.data.data;

        setAuth(
          {
            id: p.id,
            name: p.full_name,
            email: p.phone_number,
            role: "mfi_admin",
            organization: p.institution_id || undefined,
          },
          access_token
        );

        toast.success(`Welcome to CredWise, ${form.name}!`);
        navigate({ to: "/mfi" });
      } catch (err: any) {
        toast.error(
          err.response?.data?.message ||
            "Registration failed. Make sure phone/email is unique and password is strong."
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
            For Institutions
          </span>
          <h1 className="mt-2 font-display text-3xl font-bold">Register your MFI</h1>
          <p className="mt-2 text-muted-foreground">
            Set up your institution dashboard in under a minute.
          </p>
        </div>
        <form
          onSubmit={handleSubmit}
          className="space-y-4 rounded-2xl border border-border bg-card p-6 shadow-soft"
        >
          <Field
            label="Institution name"
            value={form.org}
            onChange={set("org")}
            placeholder="Kilimo Cooperative Union"
          />
          <Field
            label="Your name"
            value={form.name}
            onChange={set("name")}
            placeholder="Jane Kamau"
          />
          <Field
            label="Work email"
            type="email"
            value={form.email}
            onChange={set("email")}
            placeholder="jane@kilimocoop.co.ke"
          />
          <Field
            label="Admin Phone Number"
            value={form.phone}
            onChange={set("phone")}
            placeholder="+254711100001"
          />
          <Field
            label="Location"
            value={form.location}
            onChange={set("location")}
            placeholder="Nairobi, Kenya"
          />
          <Field
            label="Password"
            type="password"
            value={form.password}
            onChange={set("password")}
            placeholder="••••••••"
          />
          <button className="w-full rounded-xl bg-brand-primary py-3 font-bold text-primary-foreground shadow-brand transition-colors hover:bg-brand-secondary">
            Create institution account
          </button>
          <p className="text-center text-sm text-muted-foreground">
            Already registered?{" "}
            <Link
              to="/auth/login"
              search={{ role: "mfi_admin" }}
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
