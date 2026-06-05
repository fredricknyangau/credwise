/**
 * Generic client-side error reporter.
 *
 * Drop-in replacement for the removed Lovable error bridge.
 * Logs to the console in development. Swap `console.error` for your own
 * error-tracking SDK (e.g. Sentry) when you're ready for production telemetry.
 */

type ErrorContext = Record<string, unknown>;

export function reportError(error: unknown, context: ErrorContext = {}): void {
  if (typeof window === "undefined") return; // SSR guard

  console.error("[ErrorBoundary]", error, context);

  // TODO: integrate your error-tracking SDK here, e.g.:
  // Sentry.captureException(error, { extra: context });
}
