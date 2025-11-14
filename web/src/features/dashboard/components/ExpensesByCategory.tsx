"use client";
import type { ExpensesByCategoryRead } from "@/features/dashboard/types";

export default function ExpensesByCategory({ data }: { data: ExpensesByCategoryRead[] }) {
  const total = data.reduce((s, c) => s + Number(c.total), 0) || 1;

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm">
      <h3 className="text-lg font-bold">Despesas por categoria</h3>
      <p className="text-3xl font-bold mt-4">
        {Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(total)}
      </p>
      <p className="text-sm text-gray-500">Mês atual</p>

      <div className="space-y-4 mt-6">
        {data.map((c) => {
          const pct = Math.max(2, Math.round((Number(c.total) / total) * 100)); // sempre visível
          return (
            <div key={c.category_id}>
              <div className="flex justify-between text-sm font-semibold text-gray-500 mb-1">
                <span>{c.category_name}</span>
                <span>{Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(c.total))}</span>
              </div>
              <div className="h-2 bg-orange-100 rounded-full">
                <div className="h-2 bg-orange-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
