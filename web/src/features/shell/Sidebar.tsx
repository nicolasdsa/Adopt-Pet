"use client";
import Link from "next/link";
import { useState } from "react";
import { usePathname } from "next/navigation";

const items = [
  { href: "/dashboard",   label: "Dashboard",   icon: "📊" },
  { href: "/animals",     label: "Animais",     icon: "🐾" },
  { href: "/expenses",    label: "Despesas",    icon: "🧾" },
  { href: "/voluntarios", label: "Voluntários", icon: "👥" },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);        // retrátil
  const pathname = usePathname();

  return (
    <>
      {/* mobile overlay */}
      <button
        className="lg:hidden fixed top-4 left-4 z-50 rounded-md p-2 bg-white/80 shadow"
        onClick={() => setOpen((o) => !o)}
        aria-label="Abrir menu"
      >☰</button>

      <aside
        className={`fixed z-40 top-0 left-0 h-full bg-white border-r transition-[width,transform]
                    ${open ? "translate-x-0 w-64" : "-translate-x-full w-64"} lg:translate-x-0
                    lg:w-64`}
      >
        <div className="h-16 flex items-center justify-between px-4 border-b">
          <span className="font-bold">Pet Sanctuary</span>
          <button className="hidden lg:inline-block text-sm text-gray-500" onClick={() => setOpen((o)=>!o)}>
            {open ? "«" : "»"}
          </button>
        </div>

        <nav className="p-3">
          <ul className="space-y-2">
            {items.map((it) => {
              const active = pathname.startsWith(it.href);
              return (
                <li key={it.href}>
                  <Link
                    href={it.href}
                    className={`flex items-center gap-3 rounded-lg px-4 py-2
                      ${active ? "bg-orange-100 text-orange-600 font-semibold"
                               : "text-gray-600 hover:bg-orange-50 hover:text-orange-600"}`}
                    onClick={() => setOpen(false)} // fecha no mobile
                  >
                    <span className="text-lg">{it.icon}</span>
                    <span className="truncate">{it.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>

      {/* espaço lateral em telas grandes */}
      <div className="hidden lg:block w-64 shrink-0" />
    </>
  );
}
