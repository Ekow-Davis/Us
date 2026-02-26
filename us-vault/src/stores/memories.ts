// src/stores/memory.ts
import { defineStore } from "pinia"
import {
  createMemoryApi,
  listMemoriesApi,
  getMyMemoriesApi,
  getMemoryApi,
  updateMemoryApi,
  deleteMemoryApi
} from "../api/memories"

import {
  uploadMemoryMediaApi,
  deleteMemoryMediaApi
} from "../api/media"

export const useMemoryStore = defineStore("memory", {
  state: () => ({
    memories: [] as any[],
    currentMemory: null as any | null,
    total: 0,
    page: 1,
    totalPages: 1,
    isLoading: false
  }),

  actions: {

    /* FETCH */

    async fetchMemories(page = 1) {
      this.isLoading = true
      try {
        const res = await listMemoriesApi(page)
        this.memories = res.data.items
        this.total = res.data.total
        this.page = res.data.page
        this.totalPages = res.data.total_pages
      } finally {
        this.isLoading = false
      }
    },

    async fetchMyMemories(page = 1) {
      this.isLoading = true
      try {
        const res = await getMyMemoriesApi(page)
        this.memories = res.data.items
        this.total = res.data.total
        this.page = res.data.page
        this.totalPages = res.data.total_pages
      } finally {
        this.isLoading = false
      }
    },

    async fetchMemory(memoryId: string) {
      const res = await getMemoryApi(memoryId)
      this.currentMemory = res.data
    },

    /* CREATE */

    async createMemory(data: {
      title: string
      content: string
      memory_date: string
    }) {
      const res = await createMemoryApi(data)

      this.memories.unshift(res.data)

      return res.data
    },

    /* UPDATE */

    async updateMemory(memoryId: string, data: any) {
      const res = await updateMemoryApi(memoryId, data)

      const index = this.memories.findIndex(m => m.id === memoryId)
      if (index !== -1) {
        this.memories[index] = res.data
      }

      if (this.currentMemory?.id === memoryId) {
        this.currentMemory = res.data
      }
    },

    /* DELETE */

    async deleteMemory(memoryId: string) {
      await deleteMemoryApi(memoryId)
      this.memories = this.memories.filter(m => m.id !== memoryId)
    },

    /* MEDIA */

    async uploadMedia(memoryId: string, file: File) {
      await uploadMemoryMediaApi(memoryId, file)
      await this.fetchMemory(memoryId) // refresh media list
    },

    async deleteMedia(mediaId: string, memoryId: string) {
      await deleteMemoryMediaApi(mediaId)
      await this.fetchMemory(memoryId)
    }
  }
})