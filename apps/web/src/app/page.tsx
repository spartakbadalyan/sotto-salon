"use client";

import { useEffect, useState } from "react";

import { API_BASE_URL, fetchMeta, type Meta } from "@/lib/api";

type Status =
  | { kind: "loading" }
  | { kind: "ok"; meta: Meta }
  | { kind: "error"; message: string };

export default function Home() {
  const [status, setStatus] = useState<Status>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    fetchMeta(controller.signal)
      .then((meta) => setStatus({ kind: "ok", meta }))
      .catch((err: unknown) =>
        setStatus({
          kind: "error",
          message: err instanceof Error ? err.message : "unknown error",
        }),
      );
    return () => controller.abort();
  }, []);

  return (
    <main style={{ maxWidth: 640 }}>
      <h1>Sotto Salon</h1>
      <p>
        Synthetic-only foundation (SAL-007). This page verifies the web app can reach the
        API at <code>{API_BASE_URL}</code>.
      </p>
      <section
        aria-live="polite"
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: "1rem",
          marginTop: "1rem",
        }}
      >
        {status.kind === "loading" && <p>Contacting API…</p>}
        {status.kind === "error" && (
          <p>
            API unavailable: <strong>{status.message}</strong>. Start the backend and the
            compose stack (see <code>docs/development.md</code>).
          </p>
        )}
        {status.kind === "ok" && (
          <dl style={{ margin: 0 }}>
            <dt>Service</dt>
            <dd>
              {status.meta.name} v{status.meta.version}
            </dd>
            <dt>Environment</dt>
            <dd>{status.meta.environment}</dd>
            <dt>Verification adapter</dt>
            <dd>{status.meta.verification_adapter}</dd>
            <dt>Payment adapter</dt>
            <dd>{status.meta.payment_adapter}</dd>
          </dl>
        )}
      </section>
    </main>
  );
}
