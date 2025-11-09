"use client";

type Props = {
  page: number;
  hasNext: boolean;
  onPrev: () => void;
  onNext: () => void;
};

export default function Pagination({ page, hasNext, onPrev, onNext }: Props) {
  return (
    <div className="flex items-center justify-center gap-3 mt-6">
      <button
        className="px-3 py-1 rounded-full border disabled:opacity-40"
        onClick={onPrev}
        disabled={page <= 1}
      >
        {"<"} Anterior
      </button>
      <span className="text-sm text-gray-600">Página {page}</span>
      <button
        className="px-3 py-1 rounded-full border disabled:opacity-40"
        onClick={onNext}
        disabled={!hasNext}
      >
        Próxima {">"}
      </button>
    </div>
  );
}
