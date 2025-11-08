"use client";

import { useEffect, useRef, useState } from "react";
import { HelpType, OrganizationSearchRead } from "@/features/organizations/types";
import { fetchOrganizations } from "@/features/organizations/api/search";

const SP_FALLBACK = { lat: -23.55052, lng: -46.633308 };

export type SearchState = {
  name: string;
  radiusKm: number;      // 3..200
  helpTypes: HelpType[]; // multiseleção
  page: number;          // 1..n
  limit: number;         // 9
};

export function useOrganizationsSearch(s: SearchState) {
  const [coords, setCoords] = useState<{lat:number; lng:number} | null>(null);
  const [items, setItems] = useState<OrganizationSearchRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<null | "SEARCH_FAILED">(null);
  const [hasNext, setHasNext] = useState(false);
  const ctrlRef = useRef<AbortController | null>(null);

  // geolocalização
  useEffect(() => {
    let mounted = true;
    navigator.geolocation.getCurrentPosition(
      (pos) => mounted && setCoords({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      () => mounted && setCoords(SP_FALLBACK),
      { timeout: 5000, maximumAge: 60000 }
    );
    return () => { mounted = false; };
  }, []);

  // busca
  useEffect(() => {
    if (!coords) return;
    ctrlRef.current?.abort();
    const ctrl = new AbortController(); ctrlRef.current = ctrl;

    setLoading(true); setError(null);

    const skip = (s.page - 1) * s.limit;

    fetchOrganizations({
      skip,
      limit: s.limit,
      name: s.name || undefined,
      helpTypes: s.helpTypes.length ? s.helpTypes : undefined,
      latitude: coords.lat,
      longitude: coords.lng,
      radiusKm: s.radiusKm,
    }, ctrl.signal)
      .then((list) => {
        setItems(list);
        setHasNext(list.length === s.limit);
      })
      .catch(() => setError("SEARCH_FAILED"))
      .finally(() => setLoading(false));

    return () => ctrl.abort();
  }, [coords, s.name, s.radiusKm, s.helpTypes, s.page, s.limit]);

  return { items, loading, error, coordsReady: !!coords, hasNext };
}
