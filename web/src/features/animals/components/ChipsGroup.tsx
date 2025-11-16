"use client";
type Opt = { value: string; label: string };
export default function ChipsGroup({
  label, options, values, onToggle,
}: {
  label: string;
  options: Opt[];
  values: string[];
  onToggle: (v: string) => void;
}) {
  return (
    <div>
      <p className="block text-sm font-medium mb-2">{label}</p>
      <div className="flex flex-wrap gap-2">
        {options.map((o) => {
          const active = values.includes(o.value);
          return (
            <button
              type="button"
              key={o.value}
              onClick={() => onToggle(o.value)}
              className={`rounded-full border px-4 py-2 text-sm transition
                ${active
                  ? "bg-orange-500 border-orange-500 text-white"
                  : "bg-orange-50 border-orange-100 text-gray-800 hover:border-orange-300 focus:ring-2 focus:ring-orange-500"}`}
            >
              {o.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}
