export type Id = string | number;

export type AnimalSpeciesRead = {
  id: number;
  slug: string;
  label: string;
  description?: string | null;
};

export type AnimalCharacteristicOption = { value: string; label: string };

export type AnimalCharacteristicsRead = {
  temperament_traits: AnimalCharacteristicOption[];
  environment_preferences: AnimalCharacteristicOption[];
  sociable_with: AnimalCharacteristicOption[];
};

export type AnimalPhotoCreate = { url: string; position?: number | null };

export type AnimalCreate = {
  name: string;
  sex: "male" | "female" | "unknown";
  age_years?: number | null;
  weight_kg?: number | null;
  size: "small" | "medium" | "large" | "unknown";
  temperament_traits: string[];
  environment_preferences: string[];
  sociable_with: string[];
  vaccinated: boolean;
  neutered: boolean;
  dewormed: boolean;
  rescue_date?: string | null; // ISO (yyyy-mm-dd)
  microchip?: string | null;
  description?: string | null;
  adoption_requirements?: string | null;
  status: "available" | "in_treatment" | "adopted" | "temporary_home"; // ajuste se o enum do back diferir
  species_id: number;
  photos: AnimalPhotoCreate[];
};

export type AnimalStatus =
  | "available" | "reserved" | "in_treatment" | "adopted" | "temporary_home"
  | (string & {}); 

export type AnimalListItemRead = {
  id: string;
  name: string;
  status: AnimalStatus;
  species: AnimalSpeciesRead;
  photo_url?: string | null;
};
