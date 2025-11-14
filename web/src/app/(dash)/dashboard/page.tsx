import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { DashboardCards } from "@/features/dashboard/components/DashboardCards";
import ExpensesByCategory from "@/features/dashboard/components/ExpensesByCategory";
import type { DashboardSummaryRead } from "@/features/dashboard/types";

const btnPress =
  "inline-flex items-center gap-2 rounded-lg border-2 border-orange-500 " +
  "bg-orange-500 text-white font-bold px-5 py-3 " +
  "active:bg-white active:text-gray-700 active:border-orange-500 transition-colors";

export default async function Page() {
  // proteção extra além do middleware
  const actualCookies = await cookies()
  if (!actualCookies.get("access_token")) redirect("/auth/login");

  const cookieHeader = actualCookies
    .getAll()
    .map((c) => `${c.name}=${c.value}`)
    .join("; ");
  
  const res = await fetch(`http://localhost:3000/api/dashboard/summary`, {
    cache: "no-store",
    headers: {
      cookie: cookieHeader,
    },
  }).catch(() => null);
  if (!res || !res.ok) redirect("/auth/login"); // já aproveita pra botar a `/`


  const data = (await res.json()) as DashboardSummaryRead;

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold">Dashboard</h2>
          <p className="text-gray-500 mt-1">Bem-vinda de volta!</p>
        </div>
        <div className="flex flex-wrap gap-2 sm:gap-3">
          <button className={btnPress}>➕ Cadastrar animal</button>
          <button className={btnPress}>🧾 Lançar despesa</button>
          <button className={btnPress}>🗓️ Gerir escala</button>
        </div>
      </div>

      <DashboardCards data={data} />
      <ExpensesByCategory data={data.expenses_by_category} />
    </div>
  );
}
