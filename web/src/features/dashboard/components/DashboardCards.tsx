"use client";
import type { DashboardSummaryRead } from "@/features/dashboard/types";

export function DashboardCards({ data }: { data: DashboardSummaryRead }) {
  const v = data.expenses.variation_percentage;
  const good = v < 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card icon="🐾" title="Nº animais ativos" value={data.active_animals} />
      <Card icon="❤️" title="Adoções no mês" value={data.adoptions.current_month_total} />
      <Card icon="👥" title="Voluntários ativos" value={data.volunteers_active} />
      <div className="bg-white p-6 rounded-xl shadow-sm">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center">🧾</div>
            <div>
              <p className="text-sm text-gray-500">Despesas</p>
              <p className="text-2xl font-bold">
                {Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" })
                  .format(Number(data.expenses.current_month_total))}
              </p>
              <p className="text-xs text-gray-500">
                vs {Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" })
                  .format(Number(data.expenses.previous_month_total))} mês ant.
              </p>
            </div>
          </div>
          <div className={`text-sm font-bold ${good ? "text-green-600" : "text-red-600"}`}>
            {good ? "⬇" : "⬆"} {Math.abs(v).toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  );
}

function Card({ icon, title, value }: { icon: string; title: string; value: number }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center">{icon}</div>
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
        </div>
      </div>
    </div>
  );
}
