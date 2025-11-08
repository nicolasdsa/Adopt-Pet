"use client";

import { useEffect, useState } from "react";
import FiltersBar from "@/features/organizations/components/FiltersBar";
import OrgCard from "@/features/organizations/components/OrgCard";
import Pagination from "@/features/organizations/components/Pagination";
import { useOrganizationsSearch } from "@/features/organizations/hooks/useOrganizationsSearch";
import { HelpType } from "@/features/organizations/types";

export default function OrganizationsPage() {
  const [name, setName] = useState("");
  const [radiusKm, setRadiusKm] = useState(25);
  const [radiusSliderValue, setRadiusSliderValue] = useState(radiusKm);
  const [helpTypes, setHelpTypes] = useState<HelpType[]>([]);
  const [page, setPage] = useState(1);
  const limit = 9;

  useEffect(() => {
    setRadiusSliderValue(radiusKm);
  }, [radiusKm]);

  const { items, loading, error, coordsReady, hasNext } = useOrganizationsSearch({
    name, radiusKm, helpTypes, page, limit,
  });

  function toggleHelp(k: HelpType) {
    setPage(1);
    setHelpTypes((prev) => prev.includes(k) ? prev.filter(x => x !== k) : [...prev, k]);
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <section className="max-w-6xl mx-auto px-4 py-10">
        <h1 className="text-3xl font-semibold text-center">Encontre ONGs</h1>
        <p className="text-center text-gray-500 mt-2">
          Descubra e conecte-se com ONGs de proteção animal próximas a você.
        </p>

        <div className="mt-6">
          <FiltersBar
            name={name}
            onNameChange={(v) => { setPage(1); setName(v); }}
            radiusValue={radiusSliderValue}
            onRadiusInput={(n) => setRadiusSliderValue(n)}
            onRadiusCommit={(n) => {
              setRadiusSliderValue(n);
              if (n !== radiusKm) {
                setPage(1);
                setRadiusKm(n);
              }
            }}
            helpTypes={helpTypes}
            onToggleHelp={toggleHelp}
          />
        </div>

        {!coordsReady && (
          <div className="text-center text-gray-500 mt-10">Obtendo sua localização…</div>
        )}

        {error && (
          <div className="mt-10 rounded-xl border border-red-200 bg-red-50 text-red-700 p-4 text-center">
            Ocorreu um erro ao buscar as ONGs. Tente novamente mais tarde.
          </div>
        )}

        {loading && !error && (
          <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-48 rounded-2xl bg-white animate-pulse" />
            ))}
          </div>
        )}

        {!loading && !error && items.length === 0 && coordsReady && (
          <div className="mt-10 rounded-xl border bg-white p-6 text-center">
            <p className="text-gray-700">
              Não encontramos ONGs para a região selecionada.
            </p>
            <p className="text-gray-500 text-sm mt-1">
              Fique à vontade para continuar usando o sistema — novas ONGs chegam com frequência!
            </p>
          </div>
        )}

        {!loading && !error && items.length > 0 && (
          <>
            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {items.map((org) => <OrgCard key={org.id} org={org} />)}
            </div>

            <Pagination
              page={page}
              hasNext={hasNext}
              onPrev={() => setPage((p) => Math.max(1, p - 1))}
              onNext={() => setPage((p) => (hasNext ? p + 1 : p))}
            />
          </>
        )}
      </section>
    </main>
  );
}
