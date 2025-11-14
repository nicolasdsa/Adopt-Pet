export const ALLOWED_MIMES = new Set(["image/png","image/jpeg","image/webp"]);

export function isAllowedFile(file: File): boolean {
  if (file.type) return ALLOWED_MIMES.has(file.type);
  const ext = file.name.split(".").pop()?.toLowerCase();
  return ext === "png" || ext === "jpg" || ext === "jpeg" || ext === "webp";
}
