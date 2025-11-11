export type LatLng = { lat: number; lng: number };

export interface GeocodingPort {
  geocodeOne(query: string): Promise<LatLng | null>;
}
