import { LoginRequest, TokenResponse } from "../types";

export async function login(req: LoginRequest): Promise<TokenResponse> {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error("LOGIN_FAILED");
  return res.json();
}
