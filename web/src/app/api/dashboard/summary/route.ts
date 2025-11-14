import { cookies } from "next/headers";
import { NextResponse } from "next/server";

const API = "http://api:8000";

export async function GET() {
  const actualCookies = await cookies();
  const token = actualCookies.get("access_token")?.value;
  console.log("Cookies no summary:", actualCookies);
  console.log("Token no summary:", token);
  if (!token) return NextResponse.json({ message: "unauthorized" }, { status: 401 });

  console.log("Passou do token");

  const r = await fetch(`${API}/dashboard`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  const text = await r.text();
  return new NextResponse(text, {
    status: r.status,
    headers: { "content-type": r.headers.get("content-type") ?? "application/json" },
  });
}
