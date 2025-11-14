import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const q = new URL(req.url).searchParams.get("q") ?? "";
  const KEY = process.env.LOCATIONIQ_KEY; 
  if (!KEY) return NextResponse.json({ error: "missing key" }, { status: 500 });

  const url = `https://us1.locationiq.com/v1/search?key=${KEY}&q=${encodeURIComponent(q)}&format=json&limit=1&countrycodes=br`;

  const upstream = await fetch(url, {
    headers: { "User-Agent": "ONG-Platform/1.0 (contato@exemplo.org)" },
    cache: "no-store",
  });

  const data = await upstream.json();
  return NextResponse.json(data, { status: upstream.status });
}
