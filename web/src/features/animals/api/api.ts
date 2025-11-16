import type {
  AnimalCharacteristicOption,
  AnimalCharacteristicsRead,
  AnimalCreate,
  AnimalSpeciesRead,
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
