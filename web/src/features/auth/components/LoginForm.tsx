"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/features/auth/api/login";

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    if (!email || !password) { setErr("Informe e-mail e senha."); return; }
    try {
      setLoading(true);
      await login({ email, password });
      router.push("/dashboard");
    } catch {
      setErr("Não foi possível entrar. Verifique suas credenciais.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-4">
      <div className="flex flex-col">
        <label className="pb-2 text-base font-medium">E-mail</label>
        <input
          type="email" value={email} onChange={e=>setEmail(e.target.value)}
          placeholder="Digite seu e-mail"
          className="form-input h-14 rounded-lg border p-4 bg-orange-50/50 focus:ring-2 focus:ring-orange-400"
        />
      </div>

      <div className="flex flex-col">
        <label className="pb-2 text-base font-medium">Senha</label>
        <div className="flex items-stretch rounded-lg">
          <input
            type={show ? "text" : "password"}
            value={password} onChange={e=>setPassword(e.target.value)}
            placeholder="Digite sua senha"
            className="form-input h-14 flex-1 rounded-l-lg border p-4"
          />
          <button
            type="button" onClick={()=>setShow(s=>!s)}
            className="px-4 border rounded-r-lg text-gray-500"
            aria-label={show ? "Ocultar senha" : "Mostrar senha"}
          >
            {show ? "🙈" : "👁️"}
          </button>
        </div>
      </div>

      <button
        type="button"
        className="self-end text-sm text-blue-600 underline opacity-50 cursor-not-allowed"
        title="Em breve"
        disabled
      >
        Esqueci minha senha
      </button>

      {err && <div className="rounded-lg bg-red-50 border border-red-200 text-red-700 p-3 text-sm">{err}</div>}

      <div className="pt-2">
        <button
          type="submit"
          disabled={loading}
          className="h-14 w-full rounded-lg bg-[#FF7A59] text-white font-bold hover:brightness-110 disabled:opacity-50"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </div>
    </form>
  );
}
