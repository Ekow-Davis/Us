import api from "./axios"

/* MEMORY MEDIA */

export const uploadMemoryMediaApi = (
  memoryId: string,
  file: File
) => {
  const formData = new FormData()
  formData.append("file", file)

  return api.post(`/media/${memoryId}`, formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

export const deleteMemoryMediaApi = (mediaId: string) => {
  return api.delete(`/media/${mediaId}`)
}