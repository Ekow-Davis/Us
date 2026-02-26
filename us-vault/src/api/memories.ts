// src/api/memories.ts
import api from "./axios"

/*  MEMORY CRUD  */

export const createMemoryApi = (data: {
  title: string
  content: string
  memory_date: string
}) => {
  return api.post("/memories", data)
}

export const listMemoriesApi = (page = 1, page_size = 10) => {
  return api.get("/memories", {
    params: { page, page_size }
  })
}

export const getMyMemoriesApi = (page = 1, page_size = 10) => {
  return api.get("/memories/me", {
    params: { page, page_size }
  })
}

export const getMemoryApi = (memoryId: string) => {
  return api.get(`/memories/${memoryId}`)
}

export const updateMemoryApi = (
  memoryId: string,
  data: {
    title?: string
    content?: string
  }
) => {
  return api.put(`/memories/${memoryId}`, data)
}

export const deleteMemoryApi = (memoryId: string) => {
  return api.delete(`/memories/${memoryId}`)
}