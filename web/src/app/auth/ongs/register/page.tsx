"use client";
import RegisterForm from "@/features/organizations/register/components/RegisterForm";

export default function Page() {
  return (
    <main className="w-full max-w-3xl mx-auto px-4">
      <div className="rounded-2xl border bg-white/90 shadow-lg p-6 sm:p-10">
        <h1 className="text-3xl font-bold mb-6">Cadastre sua ONG</h1>
        <RegisterForm />
      </div>
    </main>
  );
}
