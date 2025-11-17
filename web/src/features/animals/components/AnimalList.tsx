// features/animals/components/AnimalsList.tsx
"use client";

import { useEffect, useMemo, useState } from "react";
import { getMyAnimals } from "@/features/animals/api/api";
import type { AnimalListItemRead, AnimalStatus } from "@/features/animals/types";
import AnimalCard from "./AnimalCard";
import Link from "next/link";

const btnPrimary =
  "inline-flex items-center gap-2 rounded-lg border-2 border-orange-500 " +
  "bg-orange-500 text-white font-bold px-4 py-2 h-11 " +
  "active:bg-white active:text-gray-700 active:border-orange-500 transition-colors";

export default function AnimalsList() {
  const [items, setItems] = useState<AnimalListItemRead[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  const [q, setQ] = useState("");
  const [status, setStatus] = useState<AnimalStatus | "">("");

  const limit = 12;

  async function load(reset = false) {
    setLoading(true);
    try {
      const skip = reset ? 0 : items.length;
      const data = await getMyAnimals({
        skip, limit, name: q || undefined, status: status || null,
      });
      setItems(reset ? data : [...items, ...data]);
      setHasMore(data.length === limit);
    } catch {
      // noop — você pode exibir um toast de erro aqui
    } finally {
      setLoading(false);
    }
  }

  // busca com debounce
  useEffect(() => {
    const id = setTimeout(() => load(true), 300);
    return () => clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q, status]);

  // primeira carga
  useEffect(() => { load(true); /* eslint-disable-next-line */ }, []);

  const empty = useMemo(() => !loading && items.length === 0, [loading, items]);

  return (
    <div className="space-y-6">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            placeholder="Buscar por nome…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="bg-orange-50 border-none rounded-lg h-11 px-4 focus:ring-2 focus:ring-orange-500"
          />
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value as any)}
            className="bg-orange-50 border-none rounded-lg h-11 px-4 focus:ring-2 focus:ring-orange-500"
          >
            <option value="">Todos os status</option>
            <option value="available">Disponível</option>
            <option value="reserved">Reservado</option>
            <option value="in_treatment">Em tratamento</option>
            <option value="adopted">Adotado</option>
            <option value="temporary_home">Em lar temporário</option>
          </select>
        </div>

        <Link href="/animals/register" className={btnPrimary}>➕ Novo animal</Link>
      </div>

      {/* Grid */}
      {empty ? (
        <div className="rounded-xl border bg-white p-8 text-center">
          <p className="text-lg font-semibold">Você ainda não cadastrou animais.</p>
          <p className="text-gray-500 mt-1">Use o botão abaixo para começar.</p>
          <Link href="/animals/register" className={`${btnPrimary} mt-4`}>Cadastrar primeiro animal</Link>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.map((it) => <AnimalCard key={it.id} item={it} />)}
            {loading && Array.from({ length: 3 }).map((_, i) => (
              <div key={`sk-${i}`} className="rounded-xl bg-white border animate-pulse h-72" />
            ))}
          </div>

          {hasMore && (
            <div className="flex justify-center">
              <button onClick={() => load(false)} disabled={loading} className={btnPrimary}>
                {loading ? "Carregando…" : "Carregar mais"}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
