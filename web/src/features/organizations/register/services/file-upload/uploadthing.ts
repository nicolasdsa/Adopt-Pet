"use client";
import { genUploader } from "uploadthing/client";
import type { FileUploadPort } from "./port";
import type { OurFileRouter } from "../../../api/uploadthing/core";

const { uploadFiles } = genUploader<OurFileRouter>();

export const uploadthingAdapter: FileUploadPort = {
  async uploadImage(file: File) {
    const res = await uploadFiles("orgLogo", { files: [file] });
    if (!res?.[0]?.url) throw new Error("UPLOAD_FAILED");
    return res[0].url;
  },
};
