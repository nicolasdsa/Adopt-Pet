import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
const API = "http://api:8000";
export async function POST(req: NextRequest) {
  const actualCookies = await cookies();
  const token = actualCookies.get("access_token")?.value;
  if (!token) return NextResponse.json({ message: "unauthorized" }, { status: 401 });
  const body = await req.text();
  const r = await fetch(`${API}/animals`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body,
  });
  return new NextResponse(await r.text(), {
    status: r.status,
    headers: { "content-type": r.headers.get("content-type") ?? "application/json" },
  });
}
