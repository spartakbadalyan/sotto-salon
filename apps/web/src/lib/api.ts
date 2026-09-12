// Thin API client. The base URL is configured per environment; it defaults to the
// local API published by the compose stack.
import type { components } from "@sotto-salon/contracts";

export type Meta = components["schemas"]["MetaResponse"];

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function fetchMeta(signal?: AbortSignal): Promise<Meta> {
  const res = await fetch(`${API_BASE_URL}/api/v1/meta`, {
    signal,
    headers: { accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`meta request failed: ${res.status}`);
  }
  return (await res.json()) as Meta;
}
