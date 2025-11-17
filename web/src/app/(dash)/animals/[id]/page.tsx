import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import Link from "next/link";

export default async function AnimalDetailPage({ params }: { params: { id: string } }) {
  // proteção extra além do middleware
  const actualCookies = await cookies()
  if (!actualCookies.get("access_token")) redirect("/auth/login"); // reforço além do middleware

  return (
    <div className="max-w-4xl">
      <Link href="/animals" className="text-sm text-gray-600 hover:underline">
        ← Voltar para Animais
      </Link>

      <h1 className="text-3xl font-bold mt-2">Animal</h1>
      <p className="text-gray-500">
        Página de detalhes do animal <span className="font-mono">{params.id}</span> — em breve.
      </p>

      {/* Quando formos implementar de verdade:
          - buscar /api/animals/{id} com Bearer do cookie (proxy)
          - exibir carrossel de fotos, chips, histórico, etc. */}
    </div>
  );
}
