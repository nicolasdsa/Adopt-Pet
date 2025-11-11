import { NextRequest, NextResponse } from "next/server";

const API = "http://localhost:8010";

export async function POST(req: NextRequest) {
  const body = await req.json();

  const upstream = await fetch(`${API}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const text = await upstream.text();
  if (!upstream.ok) {
    return new NextResponse(text || "Unauthorized", { status: upstream.status });
  }

  const data = JSON.parse(text) as {
    access_token: string; token_type: string; expires_in: number;
  };

  const res = NextResponse.json(data, { status: 200 });

  // grava cookie httpOnly com expiração
  const expires = new Date(Date.now() + data.expires_in * 1000);
  res.cookies.set("access_token", data.access_token, {
    httpOnly: true, sameSite: "lax", secure: process.env.NODE_ENV === "production",
    expires,
    path: "/",
  });
  res.cookies.set("token_type", data.token_type, { httpOnly: true, sameSite: "lax", secure: process.env.NODE_ENV === "production", expires, path: "/" });
  return res;
}
