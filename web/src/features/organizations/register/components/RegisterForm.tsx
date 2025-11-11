"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { HelpType, OrganizationCreate } from "@/features/organizations/types";
import { registerOrganization } from "@/features/organizations/api/register";
import { useGeocodeAddress } from "../hooks/useGeocode";
import { nominatimAdapter } from "../services/geocoding/nominatim";
import { uploadthingAdapter } from "../services/file-upload/uploadthing";

const UFS = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
             "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
             "RS","RO","RR","SC","SP","SE","TO"];

export default function RegisterForm() {
  const router = useRouter();
  // campos
  const [name, setName] = useState("");
  const [cnpj, setCnpj] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [website, setWebsite] = useState("");
  const [instagram, setInstagram] = useState("");
  const [mission, setMission] = useState("");
  const [password, setPassword] = useState("");
  const [helpTypes, setHelpTypes] = useState<HelpType[]>([]);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [logoUrl, setLogoUrl] = useState<string | null>(null);

  const [submitting, setSubmitting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // geocode automático após preencher endereço + cidade + estado
  const { coords, loading: geocoding } = useGeocodeAddress(address, city, state, nominatimAdapter);

  function toggleHelp(t: HelpType) {
    setHelpTypes((prev) => prev.includes(t) ? prev.filter(x => x !== t) : [...prev, t]);
  }

  async function onSelectFile(file?: File) {
    if (!file) return;
    try {
      setUploading(true);
      const url = await uploadthingAdapter.uploadImage(file);
      setLogoUrl(url);
    } catch {
      setErrorMsg("Falha ao enviar a imagem. Tente novamente.");
    } finally {
      setUploading(false);
    }
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErrorMsg(null);

    if (!acceptTerms) {
      setErrorMsg("Você precisa aceitar os termos para concluir o cadastro.");
      return;
    }
    if (!name || !cnpj || !email || !password) {
      setErrorMsg("Preencha nome, CNPJ, e-mail e senha.");
      return;
    }

    const payload: OrganizationCreate = {
      name,
      cnpj,
      address: address || null,
      city: city || null,
      state: state || null,
      phone: phone || null,
      email,
      website: website || null,
      instagram: instagram || null,
      mission: mission || null,
      help_types: helpTypes,
      logo_url: logoUrl || null,
      accepts_terms: true,
      latitude: coords?.lat ?? null,
      longitude: coords?.lng ?? null,
      password,
    };

    try {
      setSubmitting(true);
      await registerOrganization(payload);
      router.push("/dashboard"); // sucesso
    } catch {
      setErrorMsg("Não foi possível concluir o cadastro agora. Tente novamente em instantes.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-12">
      {/* Título/banner omitidos — seguimos só o form */}
      {/* Sobre a ONG */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Sobre a ONG</h2>
        <div className="grid grid-cols-1 gap-6">
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Nome da ONG</p>
            <input className="form-input rounded-lg border p-4 h-14" value={name} onChange={e=>setName(e.target.value)} placeholder="Digite o nome oficial da organização" />
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">CNPJ</p>
            <input className="form-input rounded-lg border p-4 h-14" value={cnpj} onChange={e=>setCnpj(e.target.value)} placeholder="00.000.000/0000-00" />
          </label>
        </div>
      </section>

      {/* Onde nos encontrar */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Onde nos encontrar</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="flex flex-col md:col-span-2">
            <p className="pb-2 font-medium">Endereço</p>
            <input className="form-input rounded-lg border p-4 h-14" value={address} onChange={e=>setAddress(e.target.value)} placeholder="Rua, Número, Bairro, CEP" />
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Cidade</p>
            <input className="form-input rounded-lg border p-4 h-14" value={city} onChange={e=>setCity(e.target.value)} placeholder="Sua cidade" />
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Estado</p>
            <select className="form-select rounded-lg border p-4 h-14" value={state} onChange={e=>setState(e.target.value)}>
              <option value="">Selecione o estado</option>
              {UFS.map(uf => <option key={uf} value={uf}>{uf}</option>)}
            </select>
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Telefone</p>
            <input className="form-input rounded-lg border p-4 h-14" value={phone} onChange={e=>setPhone(e.target.value)} placeholder="(00) 00000-0000" />
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">E-mail de contato</p>
            <input type="email" className="form-input rounded-lg border p-4 h-14" value={email} onChange={e=>setEmail(e.target.value)} placeholder="contato@suaong.org" />
          </label>
        </div>

        {/* Status da geocodificação */}
        <p className="text-sm text-gray-500">
          {geocoding && "Buscando coordenadas…"}
          {!geocoding && coords && `Localização encontrada: ${coords.lat.toFixed(5)}, ${coords.lng.toFixed(5)}`}
          {!geocoding && !coords && address && city && state && "Não foi possível localizar este endereço."}
        </p>
      </section>

      {/* Web */}
      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Sua ONG na Web</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Site oficial</p>
            <input className="form-input rounded-lg border p-4 h-14" value={website} onChange={e=>setWebsite(e.target.value)} placeholder="https://suaong.org" />
          </label>
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Instagram</p>
            <input className="form-input rounded-lg border p-4 h-14" value={instagram} onChange={e=>setInstagram(e.target.value)} placeholder="@suaong" />
          </label>
        </div>
      </section>

      <section className="space-y-6">
        <h2 className="text-2xl font-bold">Conte-nos mais</h2>

        <label className="flex flex-col">
          <p className="pb-2 font-medium">Missão da ONG</p>
          <textarea className="form-textarea rounded-lg border p-4 min-h-32" value={mission} onChange={e=>setMission(e.target.value)} placeholder="Descreva o propósito e as atividades principais da sua organização." />
        </label>

        <div>
          <p className="pb-3 font-medium">Tipos de ajuda aceita</p>
          <div className="flex flex-col sm:flex-row gap-4">
            {[
              { key: "donation", label: "Doação" },
              { key: "volunteering", label: "Voluntariado" },
              { key: "temporary_home", label: "Lar Temporário" },
            ].map(({ key, label }) => (
              <label key={key} className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={helpTypes.includes(key as HelpType)}
                  onChange={() => toggleHelp(key as HelpType)}
                  className="h-5 w-5 rounded border"
                />
                <span>{label}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <p className="pb-2 font-medium">Logo ou Banner</p>
          <div
            onDragOver={(e)=>e.preventDefault()}
            onDrop={(e)=>{ e.preventDefault(); const f=e.dataTransfer.files?.[0]; if (f) onSelectFile(f); }}
            className="flex items-center justify-center w-full"
          >
            <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer bg-white hover:bg-orange-50">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <span className="text-4xl text-gray-400">⬆️</span>
                <p className="mb-2 text-sm text-gray-600"><span className="font-semibold">Clique para enviar</span> ou arraste e solte</p>
                <p className="text-xs text-gray-500">PNG, JPG ou GIF (máx. 2MB)</p>
                {uploading && <p className="text-xs text-gray-500 mt-2">Enviando…</p>}
                {logoUrl && <p className="text-xs text-green-600 mt-2">Arquivo enviado ✔</p>}
              </div>
              <input
                type="file" accept="image/*" className="hidden"
                onChange={(e)=>onSelectFile(e.target.files?.[0])}
              />
            </label>
          </div>
        </div>
      </section>

      {/* Termos + senha + submit */}
      <section className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <label className="flex flex-col">
            <p className="pb-2 font-medium">Defina uma senha</p>
            <input type="password" className="form-input rounded-lg border p-4 h-14" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Mínimo 8 caracteres" />
          </label>
        </div>

        <div className="flex items-start gap-3">
          <input id="terms" type="checkbox" checked={acceptTerms} onChange={e=>setAcceptTerms(e.target.checked)} className="mt-1 h-5 w-5 rounded border" />
          <label htmlFor="terms" className="text-base">
            Eu li e aceito os <span className="font-semibold underline">Termos de Uso</span> e a <span className="font-semibold underline">Política de Privacidade</span>.
          </label>
        </div>

        {errorMsg && (
          <div className="rounded-xl border border-red-200 bg-red-50 text-red-700 p-3 text-sm">{errorMsg}</div>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="w-full sm:w-auto min-w-[180px] rounded-lg h-14 px-8 bg-orange-500 text-white font-bold hover:bg-orange-600 disabled:opacity-50"
        >
          {submitting ? "Enviando..." : "Finalizar Cadastro"}
        </button>
      </section>
    </form>
  );
}
