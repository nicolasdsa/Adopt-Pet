"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import ChipsGroup from "./ChipsGroup";
import { createAnimal, getCharacteristics, getSpecies } from "@/features/animals/api/api";
import type {
  AnimalCharacteristicsRead, AnimalCreate, AnimalSpeciesRead,
} from "@/features/animals/types";
import { uploadthingAdapter } from "@/features/organizations/register/services/file-upload/uploadthing";
import { compressImageToWebp } from "@/features/organizations/register/services/file-upload/compress";
import { isAllowedFile } from "@/features/organizations/register/services/file-upload/allowed";

const ring = "focus:ring-2 focus:ring-orange-500";

export default function AnimalForm() {
  const router = useRouter();

  // selects e chips
  const [species, setSpecies] = useState<AnimalSpeciesRead[]>([]);
  const [char, setChar] = useState<AnimalCharacteristicsRead | null>(null);

  // campos
  const [name, setName] = useState("");
  const [speciesId, setSpeciesId] = useState<number | "">("");
  const [sex, setSex] = useState<"male" | "female" | "unknown">("unknown");
  const [size, setSize] = useState<"small" | "medium" | "large" | "unknown">("unknown");
  const [age, setAge] = useState<number | "">("");
  const [weight, setWeight] = useState<number | "">("");
  const [temper, setTemper] = useState<string[]>([]);
  const [sociable, setSociable] = useState<string[]>([]);
  const [env, setEnv] = useState<string[]>([]);
  const [vaccinated, setVaccinated] = useState(false);
  const [neutered, setNeutered] = useState(false);
  const [dewormed, setDewormed] = useState(false);
  const [rescueDate, setRescueDate] = useState<string>("");
  const [microchip, setMicrochip] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] =
    useState<"available" | "in_treatment" | "adopted" | "temporary_home">("available");

  // fotos
  const [photos, setPhotos] = useState<{ url: string }[]>([]);
  const [uploading, setUploading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [okMsg, setOkMsg] = useState<string | null>(null);

  useEffect(() => {
    getSpecies().then(setSpecies).catch(() => setErr("Falha ao carregar espécies."));
    getCharacteristics().then(setChar).catch(() => setErr("Falha ao carregar características."));
  }, []);

  function toggle(list: string[], v: string, set: (v: string[]) => void) {
    set(list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);
  }

  async function onChooseFiles(files?: FileList | null) {
    if (!files?.length) return;
    setErr(null); setOkMsg(null);
    const toProcess = Array.from(files).slice(0, 10); // limite razoável
    try {
      setUploading(true);
      const uploaded: string[] = [];
      for (const f of toProcess) {
        if (!isAllowedFile(f)) {
          setErr("Formato não permitido. Use PNG, JPEG ou WebP.");
          continue;
        }
        const optimized = await compressImageToWebp(f, 1600, 0.85);
        const url = await uploadthingAdapter.uploadImage(optimized);
        uploaded.push(url);
      }
      if (uploaded.length) {
        setPhotos((prev) => [...prev, ...uploaded.map((url) => ({ url }))]);
        setOkMsg("Imagens otimizadas e enviadas com sucesso ✔");
      }
    } catch {
      setErr("Falha ao enviar imagens. Tente novamente.");
    } finally {
      setUploading(false);
    }
  }

  function removePhoto(i: number) {
    setPhotos((p) => p.filter((_, idx) => idx !== i));
  }

  const payload = useMemo<AnimalCreate>(() => ({
    name,
    sex,
    age_years: age === "" ? null : Number(age),
    weight_kg: weight === "" ? null : Number(weight),
    size,
    temperament_traits: temper,
    environment_preferences: env,
    sociable_with: sociable,
    vaccinated, neutered, dewormed,
    rescue_date: rescueDate || null,
    microchip: microchip || null,
    description: description || null,
    adoption_requirements: null,
    status,
    species_id: Number(speciesId),
    photos: photos.map((p, i) => ({ url: p.url, position: i })),
  }), [
    name, sex, age, weight, size, temper, env, sociable, vaccinated, neutered, dewormed,
    rescueDate, microchip, description, status, speciesId, photos,
  ]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null); setOkMsg(null);
    if (!name || !speciesId) { setErr("Preencha pelo menos nome e espécie."); return; }
    try {
      await createAnimal(payload);
      setOkMsg("Animal cadastrado com sucesso! 🎉");
      // opcional: ir para a listagem
      // router.push("/animais");
    } catch {
      setErr("Não foi possível publicar o animal agora.");
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-8">
      {/* linha 1 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium mb-1">Nome</label>
          <input value={name} onChange={(e)=>setName(e.target.value)}
            placeholder="Nome do animal"
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 placeholder:text-gray-400 ${ring}`} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Espécie</label>
          <select value={speciesId} onChange={(e)=>setSpeciesId(Number(e.target.value))}
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`}>
            <option value="">Selecione a espécie</option>
            {species.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Sexo</label>
          <select value={sex} onChange={(e)=>setSex(e.target.value as any)}
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`}>
            <option value="unknown">Selecione o sexo</option>
            <option value="male">Macho</option>
            <option value="female">Fêmea</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Idade (anos)</label>
          <input type="number" value={age} onChange={(e)=>setAge(e.target.value === "" ? "" : Number(e.target.value))}
            placeholder="Idade aproximada"
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Porte</label>
          <select value={size} onChange={(e)=>setSize(e.target.value as any)}
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`}>
            <option value="unknown">Selecione o porte</option>
            <option value="small">Pequeno</option>
            <option value="medium">Médio</option>
            <option value="large">Grande</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Peso (kg)</label>
          <input type="number" value={weight} onChange={(e)=>setWeight(e.target.value === "" ? "" : Number(e.target.value))}
            placeholder="Peso aproximado"
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`} />
        </div>
      </div>

      {/* chips */}
      {char && (
        <>
          <ChipsGroup
            label="Temperamento"
            options={char.temperament_traits}
            values={temper}
            onToggle={(v)=>toggle(temper, v, setTemper)}
          />
          <ChipsGroup
            label="Compatibilidades"
            options={char.sociable_with}
            values={sociable}
            onToggle={(v)=>toggle(sociable, v, setSociable)}
          />
          <ChipsGroup
            label="Requisitos do Lar"
            options={char.environment_preferences}
            values={env}
            onToggle={(v)=>toggle(env, v, setEnv)}
          />
        </>
      )}

      {/* saúde */}
      <div>
        <h3 className="text-lg font-bold mb-3">Estado de Saúde</h3>
        <div className="space-y-3">
          <label className="flex items-center gap-3">
            <input type="checkbox" checked={vaccinated} onChange={()=>setVaccinated(v=>!v)}
              className={`h-5 w-5 rounded border-2 text-orange-600 ${ring}`} />
            <span>Vacinado</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" checked={neutered} onChange={()=>setNeutered(v=>!v)}
              className={`h-5 w-5 rounded border-2 text-orange-600 ${ring}`} />
            <span>Castrado</span>
          </label>
          <label className="flex items-center gap-3">
            <input type="checkbox" checked={dewormed} onChange={()=>setDewormed(v=>!v)}
              className={`h-5 w-5 rounded border-2 text-orange-600 ${ring}`} />
            <span>Vermifugado</span>
          </label>
        </div>
      </div>

      {/* data & microchip */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium mb-1">Data de Resgate</label>
          <input type="date" value={rescueDate} onChange={(e)=>setRescueDate(e.target.value)}
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`} />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Microchip</label>
          <input value={microchip} onChange={(e)=>setMicrochip(e.target.value)} placeholder="Número do microchip"
            className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`} />
        </div>
      </div>

      {/* fotos */}
      <div>
        <h3 className="text-lg font-bold mb-3">Fotos</h3>
        <div
          onDragOver={(e)=>e.preventDefault()}
          onDrop={(e)=>{ e.preventDefault(); onChooseFiles(e.dataTransfer.files); }}
          className="rounded-lg border-2 border-dashed border-orange-200 px-6 py-10 text-center"
        >
          <p className="font-semibold">Arraste e solte ou clique para adicionar fotos</p>
          <p className="text-sm text-gray-500">PNG, JPG ou WebP (recomendado) • até 10MB</p>
          <label className="inline-block mt-3">
            <input type="file" className="hidden"
              accept="image/png,image/jpeg,image/webp" multiple
              onChange={(e)=>onChooseFiles(e.target.files)} />
            <span className="cursor-pointer inline-flex items-center px-5 py-2 rounded-full bg-orange-100 text-orange-700 font-semibold">
              Escolher arquivos
            </span>
          </label>

          {!!photos.length && (
            <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {photos.map((p, i) => (
                <div key={i} className="relative group">
                  <img src={p.url} alt={`foto ${i+1}`} className="h-28 w-full object-cover rounded-lg" />
                  <button type="button" onClick={()=>removePhoto(i)}
                    className="absolute top-1 right-1 hidden group-hover:inline-flex bg-white/90 border rounded px-2 py-0.5 text-xs">
                    remover
                  </button>
                </div>
              ))}
            </div>
          )}

          {uploading && <p className="mt-3 text-sm text-gray-500">Enviando imagens…</p>}
        </div>
      </div>

      {/* descrição e status */}
      <div>
        <label className="block text-sm font-medium mb-1">Descrição</label>
        <textarea rows={4} value={description} onChange={(e)=>setDescription(e.target.value)}
          placeholder="Conte a história do animal, suas características e personalidade."
          className={`w-full bg-orange-50 border-none rounded-lg p-4 ${ring}`} />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Status</label>
        <select value={status} onChange={(e)=>setStatus(e.target.value as any)}
          className={`w-full bg-orange-50 border-none rounded-lg h-12 px-4 ${ring}`}>
          <option value="available">Disponível</option>
          <option value="in_treatment">Em tratamento</option>
          <option value="adopted">Adotado</option>
          <option value="temporary_home">Em lar temporário</option>
        </select>
      </div>

      {/* mensagens */}
      {err && <div className="rounded-lg bg-red-50 border border-red-200 p-3 text-red-700">{err}</div>}
      {okMsg && <div className="rounded-lg bg-green-50 border border-green-200 p-3 text-green-700">{okMsg}</div>}

      {/* ações */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 border-t pt-6">
        <div className="flex gap-2">
          <button type="button" className="h-12 px-6 rounded-full bg-orange-50 text-gray-800 font-bold">Marcar como Adotado</button>
          <button type="button" className="h-12 px-6 rounded-full bg-orange-50 text-gray-800 font-bold">Vincular Despesas</button>
        </div>
        <div className="flex gap-2">
          <button type="button" className="h-12 px-6 rounded-full bg-orange-50 text-gray-800 font-bold">Salvar Rascunho</button>
          <button type="submit" className="h-12 px-6 rounded-full bg-orange-500 text-white font-bold active:bg-white active:text-gray-700 active:border-2 active:border-orange-500">
            Publicar Animal
          </button>
        </div>
      </div>
    </form>
  );
}
