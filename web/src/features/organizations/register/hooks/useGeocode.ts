"use client";
import { useEffect, useState } from "react";
import type { GeocodingPort, LatLng } from "../services/geocoding/port";

export function useGeocodeAddress(
  address: string, city: string, state: string,
  geocoder: GeocodingPort,
  delay = 600
) {
  const [coords, setCoords] = useState<LatLng | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const filled = address.trim() && city.trim() && state.trim();
    if (!filled) { setCoords(null); return; }

    const q = `${address}, ${city} - ${state}, Brasil`;
    const t = setTimeout(async () => {
      setLoading(true);
      const c = await geocoder.geocodeOne(q).catch(() => null);
      setCoords(c);
      setLoading(false);
    }, delay);
    return () => clearTimeout(t);
  }, [address, city, state, geocoder, delay]);

  return { coords, loading };
}
