import { createFileRoute, Outlet } from "@tanstack/react-router";
import { MfiSidebar } from "@/components/mfi/MfiSidebar";
import { RequireAuth } from "@/components/RequireAuth";

export const Route = createFileRoute("/mfi")({
  component: MfiLayout,
});

function MfiLayout() {
  return (
    <RequireAuth role="mfi_admin">
      <div className="flex min-h-screen bg-brand-surface">
        <MfiSidebar />
        <main className="flex-1 overflow-x-hidden">
          <Outlet />
        </main>
      </div>
    </RequireAuth>
  );
}
