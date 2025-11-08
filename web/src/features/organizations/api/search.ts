import { HelpType, OrganizationSearchRead } from "@/features/organizations/types";

const API = "http://localhost:8010";

export type SearchQuery = {
  skip: number;          // (page-1)*limit
  limit: number;         // 1..100 (vou usar 9 para grid 3x3)
  name?: string;
  helpTypes?: HelpType[];
  latitude: number;      // obrigatório no client
  longitude: number;     // obrigatório no client
  radiusKm: number;      // 3..200 (teu backend aceita até 300)
};

export async function fetchOrganizations(q: SearchQuery, signal?: AbortSignal) {
  const sp = new URLSearchParams();
  sp.set("skip", String(q.skip));
  sp.set("limit", String(q.limit));
  if (q.name?.trim()) sp.set("name", q.name.trim());
  q.helpTypes?.forEach((h) => sp.append("help_type", h));
  sp.set("latitude", String(q.latitude));
  sp.set("longitude", String(q.longitude));
  sp.set("radius_km", String(q.radiusKm));

  const res = await fetch(`${API}/ongs/search?${sp.toString()}`, {
    method: "GET",
    signal,
  });
  if (!res.ok) throw new Error("SEARCH_FAILED");
  const data: OrganizationSearchRead[] = await res.json();
  return data;
}
