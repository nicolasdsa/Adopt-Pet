"use client";
import Link from "next/link";
import LoginForm from "@/features/auth/components/LoginForm";

export default function Page() {
  return (
    <main className="w-full max-w-md mx-auto px-4">
      <div className="rounded-2xl border bg-white/90 shadow-lg p-6 sm:p-8">
        <h1 className="text-3xl font-bold text-center mb-6">Acesse sua conta</h1>
        <LoginForm />
      </div>

      <div className="mt-8 text-center">
        <p className="text-gray-700">Sua ONG ainda não faz parte da nossa comunidade?</p>
        <Link
          href="/ongs/cadastrar"
          className="mt-4 inline-block w-full rounded-lg border-2 border-[#FF7A59] px-5 py-3.5 font-bold text-[#FF7A59] hover:bg-[#FF7A59] hover:text-white transition"
        >
          Cadastrar minha ONG
        </Link>
      </div>
    </main>
  );
}
