import { createFileRoute, Outlet } from "@tanstack/react-router";
import { PortalChrome } from "@/components/portal/PortalChrome";
import { RequireAuth } from "@/components/RequireAuth";

export const Route = createFileRoute("/portal")({
  component: PortalLayout,
});

function PortalLayout() {
  return (
    <RequireAuth role="client">
      <div className="min-h-screen bg-brand-surface pb-24 md:pb-0">
        <PortalChrome />
        <Outlet />
      </div>
    </RequireAuth>
  );
}
