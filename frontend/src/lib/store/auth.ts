import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { User, UserRole } from "../types";

interface AuthState {
  user: User | null;
  token: string | null;
  hydrated: boolean;
  login: (email: string, role: UserRole, name?: string, organization?: string) => void;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  setHydrated: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      hydrated: false,
      login: (email, role, name, organization) =>
        set({
          user: {
            id: crypto.randomUUID(),
            name: name ?? email.split("@")[0],
            email,
            role,
            organization,
          },
          token: "mock-jwt-" + Math.random().toString(36).slice(2),
        }),
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
      setHydrated: () => set({ hydrated: true }),
    }),
    {
      name: "CredWise-auth",
      storage: createJSONStorage(() =>
        typeof window !== "undefined" ? window.localStorage : (undefined as never),
      ),
      onRehydrateStorage: () => (state) => state?.setHydrated(),
    },
  ),
);
