import { isAllowedFile } from "./allowed";

export async function compressImageToWebp(file: File, maxDim = 1600, quality = 0.85): Promise<File> {
  if (!isAllowedFile(file)) throw new Error("INVALID_TYPE"); 
  const img = await createImageBitmap(file);
  const scale = Math.min(1, maxDim / Math.max(img.width, img.height));
  const w = Math.max(1, Math.round(img.width * scale));
  const h = Math.max(1, Math.round(img.height * scale));

  const canvas = document.createElement("canvas");
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext("2d")!;
  ctx.drawImage(img, 0, 0, w, h);

  const blob: Blob = await new Promise((resolve) =>
    canvas.toBlob((b) => resolve(b as Blob), "image/webp", quality)
  );
  return new File([blob], file.name.replace(/\.\w+$/, ".webp"), { type: "image/webp" });
}
