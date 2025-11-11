export interface FileUploadPort {
  uploadImage(file: File): Promise<string>; 
}
