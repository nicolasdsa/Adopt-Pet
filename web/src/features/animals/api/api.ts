import type {
  AnimalCharacteristicOption,
  AnimalCharacteristicsRead,
  AnimalCreate,
  AnimalListItemRead,
  AnimalSpeciesRead,
  AnimalStatus,
} from "../types";

export async function getSpecies(): Promise<AnimalSpeciesRead[]> {
  const r = await fetch("/api/animals/species", { cache: "no-store" });
  if (!r.ok) throw new Error("SPECIES_FAILED");
  return r.json();
}

export async function getCharacteristics(): Promise<AnimalCharacteristicsRead> {
  const r = await fetch("/api/animals/characteristics", { cache: "no-store" });
  if (!r.ok) throw new Error("CHAR_FAILED");
  return r.json();
}

export async function createAnimal(p: AnimalCreate) {
  const r = await fetch("/api/animals", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(p),
  });
  if (!r.ok) throw new Error("CREATE_FAILED");
  return r.json();
}

export async function getMyAnimals(params: {
  skip?: number; limit?: number; name?: string; status?: AnimalStatus | null;
}): Promise<AnimalListItemRead[]> {
  const sp = new URLSearchParams();
  if (params.skip) sp.set("skip", String(params.skip));
  if (params.limit) sp.set("limit", String(params.limit));
  if (params.name) sp.set("name", params.name);
  if (params.status) sp.set("status", params.status);
  const r = await fetch(`/api/animals/mine?${sp.toString()}`, { cache: "no-store" });
  if (!r.ok) throw new Error("LIST_FAILED");
  return r.json();
}
