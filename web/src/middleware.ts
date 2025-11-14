import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

const PROTECTED = ["/dashboard", "/animals", "/expenses", "/voluntarios"];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  const needsAuth = PROTECTED.some((p) => pathname === p || pathname.startsWith(p + "/"));
  if (!needsAuth) return NextResponse.next();

  const token = req.cookies.get("access_token")?.value;
  if (!token) {
    const url = req.nextUrl.clone();
    url.pathname = "/auth/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/animals/:path*", "/expenses/:path*", "/voluntarios/:path*"],
};
