"use client";
import { OrganizationSearchRead } from "@/features/organizations/types";

export default function OrgCard({ org }: { org: OrganizationSearchRead }) {
  return (
    <div className="rounded-2xl bg-white shadow-sm p-6 flex flex-col items-center gap-3">
      <div className="h-16 w-16 rounded-full ring-1 ring-gray-200 overflow-hidden flex items-center justify-center">
        {org.logo_url
          ? <img src={org.logo_url} alt={org.name} className="h-full w-full object-cover" />
          : <span className="text-sm text-gray-400">Logo</span>}
      </div>

      <div className="text-center">
        <h3 className="font-medium">{org.name}</h3>
        <p className="text-xs text-gray-500">
          {org.city ?? "—"}, {org.state ?? "—"}
          {typeof org.distance_km === "number" && (
            <span className="text-gray-400"> • {org.distance_km.toFixed(1)} km</span>
          )}
        </p>
      </div>

      <div className="flex gap-2 text-[11px]">
        <span className="rounded-full bg-orange-50 text-orange-600 px-2 py-0.5">
          {org.dogs_count} Cães
        </span>
        <span className="rounded-full bg-orange-50 text-orange-600 px-2 py-0.5">
          {org.cats_count} Gatos
        </span>
      </div>

      <button className="mt-2 w-full rounded-full bg-orange-500 text-white py-2 text-sm hover:bg-orange-600">
        Ver ONG
      </button>
    </div>
  );
}
