// src/api/seeds.ts
import api from "./axios" 

/* GET */

// Active seeds (ready to bloom)
export const getActiveSeedsApi = () =>
  api.get("/seeds/active")

// All seeds (paginated)
export const getAllSeedsApi = (page = 1, pageSize = 10) =>
  api.get("/seeds", {
    params: { page, page_size: pageSize }
  })

// My seeds
export const getMySeedsApi = (page = 1, pageSize = 10) =>
  api.get("/seeds/me", {
    params: { page, page_size: pageSize }
  })

// Summary
export const getSeedSummaryApi = () =>
  api.get("/seeds/summary")

// Single seed details
export const getSeedDetailsApi = (seedId: string) =>
  api.get(`/seeds/${seedId}`)


/* POST */

// Create seed
export const createSeedApi = (data: {
  title: string
  content: string
  bloom_at: string
}) =>
  api.post("/seeds", data)

// Bloom seed
export const bloomSeedApi = (seedId: string) =>
  api.post(`/seeds/${seedId}/bloom`)

// Upload seed media
export const uploadSeedMediaApi = (seedId: string, file: File) => {
  const formData = new FormData()
  formData.append("file", file)

  return api.post(`/seeds/${seedId}/media`, formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}


/* PUT */

export const updateSeedApi = (
  seedId: string,
  data: {
    title: string
    content: string
    bloom_at: string
  }
) =>
  api.put(`/seeds/${seedId}`, data)


/* DELETE */

// Cancel seed
export const cancelSeedApi = (seedId: string) =>
  api.delete(`/seeds/${seedId}`)

// Delete seed media
export const deleteSeedMediaApi = (mediaId: string) =>
  api.delete(`/seeds/media/${mediaId}`)