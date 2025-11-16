import { cookies } from "next/headers";
import { NextResponse } from "next/server";
const API = "http://api:8000";
export async function GET() {
  const actualCookies = await cookies();
  const token = actualCookies.get("access_token")?.value;
  const r = await fetch(`${API}/animals/species`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store",
  });
  return new NextResponse(await r.text(), {
    status: r.status,
    headers: { "content-type": r.headers.get("content-type") ?? "application/json" },
  });
}
