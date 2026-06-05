import { createFileRoute, Outlet } from "@tanstack/react-router";
import { PortalChrome } from "@/components/portal/PortalChrome";
import { RequireAuth } from "@/components/RequireAuth";

export const Route = createFileRoute("/portal")({
  component: PortalLayout,
});

function PortalLayout() {
  return (
    <RequireAuth role="client">
      <div className="mx-auto flex min-h-screen w-full max-w-md flex-col overflow-hidden bg-brand-surface shadow-2xl ring-1 ring-border sm:my-8 sm:h-[850px] sm:min-h-[850px] sm:rounded-[2.5rem]">
        <PortalChrome />
        <div className="flex-1 overflow-y-auto pb-24">
          <Outlet />
        </div>
      </div>
    </RequireAuth>
  );
}
