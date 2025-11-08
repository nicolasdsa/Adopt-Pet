"use client";
import { HelpType } from "@/features/organizations/types";

type Props = {
  name: string;
  onNameChange: (v: string) => void;
  radiusValue: number;
  onRadiusInput: (n: number) => void;
  onRadiusCommit: (n: number) => void;
  helpTypes: HelpType[];
  onToggleHelp: (v: HelpType) => void;
};

const HELP: { key: HelpType; label: string }[] = [
  { key: "donation",        label: "Doação" },
  { key: "volunteering",    label: "Voluntariado" },
  { key: "temporary_home",  label: "Lar temporário" },
];

export default function FiltersBar(p: Props) {
  return (
    <div className="rounded-2xl bg-white shadow-sm p-4 md:p-6 space-y-4">
      <input
        value={p.name}
        onChange={(e) => p.onNameChange(e.target.value)}
        placeholder="Buscar por nome ou cidade"
        className="w-full rounded-xl border px-4 py-2 outline-none focus:ring focus:ring-orange-200"
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
        <div className="flex items-center justify-between gap-3">
          <span className="text-sm text-gray-600">Raio ({p.radiusValue}km)</span>
          <input
            type="range"
            min={3}
            max={200}
            value={p.radiusValue}
            onChange={(e) => p.onRadiusInput(Number(e.target.value))}
            onPointerUp={(e) => p.onRadiusCommit(Number(e.currentTarget.value))}
            onBlur={(e) => p.onRadiusCommit(Number(e.currentTarget.value))}
            onKeyUp={(e) => {
              if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].includes(e.key)) {
                p.onRadiusCommit(Number(e.currentTarget.value));
              }
            }}
            className="w-56"
          />
        </div>

        <div className="md:col-span-2 flex flex-wrap gap-2">
          {HELP.map(h => {
            const active = p.helpTypes.includes(h.key);
            return (
              <button
                key={h.key}
                onClick={() => p.onToggleHelp(h.key)}
                className={`rounded-full border px-3 py-1 text-sm
                ${active ? "bg-orange-500 text-white border-orange-500" : "bg-white text-gray-700"}`}
                aria-pressed={active}
              >
                {h.label}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
