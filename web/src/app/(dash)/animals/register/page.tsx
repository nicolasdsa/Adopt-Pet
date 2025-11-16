import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import AnimalForm from "@/features/animals/components/AnimalForm";

export default async function Page() {
  const actualCookies = await cookies()
  if (!actualCookies.get("access_token")) redirect("/auth/login"); // reforço ao middleware
  return (
    <div className="max-w-4xl">
      <h2 className="text-3xl font-bold mb-1">Cadastro de Animal</h2>
      <p className="text-gray-500 mb-6">Preencha os dados do animal para disponibilizá-lo para adoção.</p>
      <AnimalForm />
    </div>
  );
}
