import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import AnimalsList from "@/features/animals/components/AnimalList";

export default async function Page() {
  const actualCookies = await cookies()
  if (!actualCookies.get("access_token")) redirect("/auth/login"); // reforço além do middleware

  return (
    <div className="max-w-6xl">
      <h2 className="text-3xl font-bold mb-1">Animais</h2>
      <p className="text-gray-500 mb-6">Visualize e gerencie os animais da sua ONG.</p>
      <AnimalsList />
    </div>
  );
}
