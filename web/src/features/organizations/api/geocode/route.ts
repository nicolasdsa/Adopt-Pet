import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const q = new URL(req.url).searchParams.get("q") ?? "";
  const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=br&q=${encodeURIComponent(q)}`;

  const upstream = await fetch(url, {
    // Bons modos com OSM: identifique seu app/contato
    headers: { "User-Agent": "ONG-Platform/1.0 (contato@sua-plataforma.com)" }
  });

  const data = await upstream.json();
  return NextResponse.json(data);
}
