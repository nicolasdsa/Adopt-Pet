// features/animals/components/AnimalCard.tsx
"use client";
import type { AnimalListItemRead, AnimalStatus } from "@/features/animals/types";
import Link from "next/link";

export default function AnimalCard({ item }: { item: AnimalListItemRead }) {
  const badge = {
    available: "bg-green-100 text-green-700",
    adopted: "bg-blue-100 text-blue-700",
    in_treatment: "bg-yellow-100 text-yellow-800",
    temporary_home: "bg-violet-100 text-violet-700",
    reserved: "bg-orange-100 text-orange-700",
  } as const satisfies Record<AnimalStatus, string>;

  const badgeClass = badge[item.status as keyof typeof badge] ?? "bg-gray-100 text-gray-700";

  return (
    <Link
      href={`/animals/${item.id}`}
      className="group block rounded-xl bg-white border hover:border-orange-300 shadow-sm hover:shadow-md
                 focus:outline-none focus:ring-2 focus:ring-orange-500 transition"
    >
      <div className="aspect-[4/3] w-full overflow-hidden rounded-t-xl bg-orange-50">
        <img
          src={item.photo_url || "https://placehold.co/600x450?text=Sem+foto"}
          alt={item.name}
          className="h-full w-full object-cover group-hover:scale-[1.02] transition-transform"
        />
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-base font-bold">{item.name}</p>
            <p className="text-sm text-gray-500">{item.species.label}</p>
          </div>
          <span className={`px-2 py-1 text-xs rounded-full ${badgeClass}`}>
            {item.status.replaceAll("_", " ")}
          </span>
        </div>

        <span className="mt-3 inline-flex items-center gap-1 text-sm text-orange-600 group-hover:underline">
          Ver detalhes →
        </span>
      </div>
    </Link>
  );
}
