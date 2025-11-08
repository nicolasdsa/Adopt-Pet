export type HelpType = "donation" | "volunteering" | "temporary_home";

export type OrganizationSearchRead = {
  id: string;
  created_at: string;
  updated_at: string;

  name: string;
  cnpj: string;
  address?: string | null;
  city?: string | null;
  state?: string | null;     // "SP", "RJ", etc.
  phone?: string | null;
  email: string;
  website?: string | null;
  instagram?: string | null;
  mission?: string | null;
  help_types: HelpType[];
  logo_url?: string | null;

  latitude?: number | null;
  longitude?: number | null;

  distance_km?: number | null;
  dogs_count: number;        // inteiro >= 0
  cats_count: number;        // inteiro >= 0
};
