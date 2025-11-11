import { createUploadthing, type FileRouter } from "uploadthing/next";

const f = createUploadthing();

export const ourFileRouter = {
  orgLogo: f({ image: { maxFileSize: "2MB" } }) // PNG/JPG/GIF
    .onUploadComplete(async ({ file }) => {
      // Você pode persistir no DB se quiser; aqui só repasso a URL
      return { url: file.url };
    }),
} satisfies FileRouter;

export type OurFileRouter = typeof ourFileRouter;
