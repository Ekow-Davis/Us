import api from "./axios"

/* CREATE  */

export const createJournalApi = (data: {
  title: string
  content: string
  visibility: "private" | "shared"
}) => {
  return api.post("/journals/", data)
}

export const convertJournalApi = (journalId: string) => {
  return api.post(`/journals/${journalId}/convert`)
}

/* GET LISTS  */

export const getPrivateJournalsApi = (
  page = 1,
  page_size = 10
) => {
  return api.get("/journals/private", {
    params: { page, page_size }
  })
}

export const getSharedJournalsApi = (
  page = 1,
  page_size = 10
) => {
  return api.get("/journals/shared", {
    params: { page, page_size }
  })
}

/* ANALYTICS  */

export const getMyJournalAnalyticsApi = () => {
  return api.get("/journals/analytics/me")
}

export const getVaultJournalAnalyticsApi = () => {
  return api.get("/journals/analytics/vault")
}

/* UPDATE  */

export const updateJournalApi = (
  journalId: string,
  data: {
    title?: string
    content?: string
    visibility?: "private" | "shared"
  }
) => {
  return api.put(`/journals/${journalId}`, data)
}

/* DELETE  */

export const deleteJournalApi = (journalId: string) => {
  return api.delete(`/journals/${journalId}`)
}