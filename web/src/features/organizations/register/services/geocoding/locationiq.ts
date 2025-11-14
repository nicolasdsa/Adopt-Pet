"use client";
import type { GeocodingPort, LatLng } from "./port";

export const locationIqAdapter: GeocodingPort = {
  async geocodeOne(query: string): Promise<LatLng | null> {
    const res = await fetch(`/api/geocode?q=${encodeURIComponent(query)}`);
    if (!res.ok) return null;
    const data = await res.json();
    if (Array.isArray(data) && data[0]?.lat && data[0]?.lon) {
      return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
    }
    return null;
  },
};
