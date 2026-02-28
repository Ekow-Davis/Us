// src/stores/seed.ts
import { defineStore } from "pinia"
import {
  getActiveSeedsApi,
  getAllSeedsApi,
  getMySeedsApi,
  getSeedSummaryApi,
  getSeedDetailsApi,
  createSeedApi,
  bloomSeedApi,
  uploadSeedMediaApi,
  updateSeedApi,
  cancelSeedApi,
  deleteSeedMediaApi
} from "../api/seeds"

export const useSeedStore = defineStore("seed", {
  state: () => ({
    seeds: [] as any[],
    activeSeeds: [] as any[],
    currentSeed: null as any | null,

    summary: {
      total: 0,
      growing: 0,
      ready: 0,
      bloomed: 0
    },

    total: 0,
    page: 1,
    totalPages: 1,

    isLoading: false
  }),

  actions: {

    /* FETCH LISTS */

    async fetchAllSeeds(page = 1, pageSize = 10) {
      this.isLoading = true
      try {
        const res = await getAllSeedsApi(page, pageSize)

        this.seeds = res.data.items
        this.total = res.data.total
        this.page = res.data.page
        this.totalPages = res.data.total_pages
      } finally {
        this.isLoading = false
      }
    },

    async fetchMySeeds(page = 1, pageSize = 10) {
      this.isLoading = true
      try {
        const res = await getMySeedsApi(page, pageSize)

        this.seeds = res.data.items
        this.total = res.data.total
        this.page = res.data.page
        this.totalPages = res.data.total_pages
      } finally {
        this.isLoading = false
      }
    },

    async fetchActiveSeeds() {
      const res = await getActiveSeedsApi()
      this.activeSeeds = res.data
    },

    async fetchSummary() {
      const res = await getSeedSummaryApi()
      this.summary = res.data
    },

    async fetchSeed(seedId: string) {
      const res = await getSeedDetailsApi(seedId)

      // normalize media
      this.currentSeed = {
        ...res.data,
        media: res.data.media ?? []
      }
    },

    /* CREATE */

    async createSeed(data: {
      title: string
      content: string
      bloom_at: string
    }) {
      const res = await createSeedApi(data)

      // optimistic add
      this.seeds.unshift(res.data)

      return res.data
    },

    /* UPDATE */

    async updateSeed(seedId: string, data: any) {
      await updateSeedApi(seedId, data)

      const index = this.seeds.findIndex(s => s.id === seedId)
      if (index !== -1) {
        this.seeds[index] = {
          ...this.seeds[index],
          ...data
        }
      }

      if (this.currentSeed?.id === seedId) {
        this.currentSeed = {
          ...this.currentSeed,
          ...data
        }
      }
    },

    /* BLOOM */

    async bloomSeed(seedId: string) {
      const res = await bloomSeedApi(seedId)

      if (this.currentSeed?.id === seedId) {
        if (res.data.status === "converted_to_memory") {
          this.currentSeed.status = "bloomed"
        }
      }

      return res.data
    },

    /* CANCEL */

    async cancelSeed(seedId: string) {
      await cancelSeedApi(seedId)

      this.seeds = this.seeds.filter(s => s.id !== seedId)

      if (this.currentSeed?.id === seedId) {
        this.currentSeed = null
      }
    },

    /* MEDIA */

    async uploadMedia(seedId: string, file: File) {
      await uploadSeedMediaApi(seedId, file)

      await this.fetchSeed(seedId) // refresh
    },

    async deleteMedia(mediaId: string, seedId: string) {
      await deleteSeedMediaApi(mediaId)

      await this.fetchSeed(seedId)
    }
  }
})