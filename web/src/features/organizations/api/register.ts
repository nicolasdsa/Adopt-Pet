import type { OrganizationCreate, OrganizationRead } from "@/features/organizations/types";

const API = "http://localhost:8010";

export async function registerOrganization(
  payload: OrganizationCreate,
  signal?: AbortSignal
): Promise<OrganizationRead> {
  const res = await fetch(`${API}/organizations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    signal,
  });
  if (!res.ok) throw new Error("REGISTER_FAILED");
  return res.json();
}
