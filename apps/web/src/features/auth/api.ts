export interface CurrentUser {
  account_id: string;
  account_kind: "advertiser" | "staff";
  roles: Array<"moderator" | "appeals" | "billing_support" | "security">;
  mfa_verified: boolean;
}

export async function getCurrentUser(apiBaseUrl: string): Promise<CurrentUser | null> {
  const response = await fetch(`${apiBaseUrl}/api/v1/auth/me`, {
    credentials: "include",
    cache: "no-store",
  });
  if (response.status === 401) return null;
  if (!response.ok) throw new Error("Unable to load the current account");
  return (await response.json()) as CurrentUser;
}

export async function logout(apiBaseUrl: string, csrfToken: string): Promise<void> {
  const response = await fetch(`${apiBaseUrl}/api/v1/auth/logout`, {
    method: "POST",
    credentials: "include",
    headers: { "X-CSRF-Token": csrfToken },
  });
  if (!response.ok) throw new Error("Unable to end the session");
}
