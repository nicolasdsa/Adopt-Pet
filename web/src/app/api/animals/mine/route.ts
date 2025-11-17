import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

const API = "http://api:8000";

export async function GET(req: NextRequest) {
  const actualCookies = await cookies();
  const token = actualCookies.get("access_token")?.value;
  if (!token) return NextResponse.json({ message: "unauthorized" }, { status: 401 });

  const { search } = new URL(req.url);
  const upstream = await fetch(`${API}/animals/mine${search}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  const text = await upstream.text();
  return new NextResponse(text, {
    status: upstream.status,
    headers: { "content-type": upstream.headers.get("content-type") ?? "application/json" },
  });
}
