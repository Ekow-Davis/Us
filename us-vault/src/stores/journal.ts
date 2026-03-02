import { defineStore } from "pinia"
import {
  createJournalApi,
  updateJournalApi,
  deleteJournalApi,
  convertJournalApi,
  getPrivateJournalsApi,
  getSharedJournalsApi,
  getMyJournalAnalyticsApi,
  getVaultJournalAnalyticsApi
} from "../api/journal"

export interface Journal {
  id: string
  user_id: string
  vault_id: string
  title: string
  content: string
  visibility: "private" | "shared"
  status: string
  created_at: string
  edited_at: string
  memory_id: string | null
  is_deleted: boolean
}

export interface JournalAnalytics {
  total_journals: number
  private_count: number
  shared_count: number
  converted_count: number
}

export const useJournalStore = defineStore("journal", {
  state: () => ({
    privateJournals: [] as Journal[],
    sharedJournals: [] as Journal[],
    currentJournal: null as Journal | null,
    
    // Pagination
    privatePagination: {
      page: 1,
      pageSize: 10,
      total: 0,
      totalPages: 0
    },
    sharedPagination: {
      page: 1,
      pageSize: 10,
      total: 0,
      totalPages: 0
    },
    
    // Analytics
    myAnalytics: null as JournalAnalytics | null,
    vaultAnalytics: null as JournalAnalytics | null,
    
    // Loading states
    isLoading: false,
    isSaving: false,
    error: null as string | null
  }),

  getters: {
    allJournals: (state) => [...state.privateJournals, ...state.sharedJournals],
    
    privateCount: (state) => state.privateJournals.length,
    sharedCount: (state) => state.sharedJournals.length,
  },

  actions: {
    // ── Fetch Private Journals ───────────────────────────────────────
    async fetchPrivateJournals(page = 1, pageSize = 10) {
      this.isLoading = true
      this.error = null
      
      try {
        const res = await getPrivateJournalsApi(page, pageSize)
        
        this.privateJournals = res.data.items
        this.privatePagination = {
          page: res.data.page,
          pageSize: res.data.page_size,
          total: res.data.total,
          totalPages: res.data.total_pages
        }
        
        return res.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to fetch private journals"
        console.error("Failed to fetch private journals:", err)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    // ── Fetch Shared Journals ────────────────────────────────────────
    async fetchSharedJournals(page = 1, pageSize = 10) {
      this.isLoading = true
      this.error = null
      
      try {
        const res = await getSharedJournalsApi(page, pageSize)
        
        this.sharedJournals = res.data.items
        this.sharedPagination = {
          page: res.data.page,
          pageSize: res.data.page_size,
          total: res.data.total,
          totalPages: res.data.total_pages
        }
        
        return res.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to fetch shared journals"
        console.error("Failed to fetch shared journals:", err)
        throw err
      } finally {
        this.isLoading = false
      }
    },

    // ── Create Journal ────────────────────────────────────────────────
    async createJournal(data: {
      title: string
      content: string
      visibility: "private" | "shared"
    }) {
      this.isSaving = true
      this.error = null
      
      try {
        const res = await createJournalApi(data)
        
        // Add to appropriate list
        if (data.visibility === "private") {
          this.privateJournals.unshift(res.data)
        } else {
          this.sharedJournals.unshift(res.data)
        }
        
        return res.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to create journal"
        console.error("Failed to create journal:", err)
        throw err
      } finally {
        this.isSaving = false
      }
    },

    // ── Update Journal ────────────────────────────────────────────────
    async updateJournal(
      journalId: string,
      data: {
        title?: string
        content?: string
        visibility?: "private" | "shared"
      }
    ) {
      this.isSaving = true
      this.error = null
      
      try {
        const res = await updateJournalApi(journalId, data)
        
        // Update in appropriate list
        const privateIdx = this.privateJournals.findIndex(j => j.id === journalId)
        const sharedIdx = this.sharedJournals.findIndex(j => j.id === journalId)
        
        if (privateIdx !== -1) {
          // If visibility changed to shared, move it
          if (data.visibility === "shared") {
            this.privateJournals.splice(privateIdx, 1)
            this.sharedJournals.unshift(res.data)
          } else {
            this.privateJournals[privateIdx] = res.data
          }
        } else if (sharedIdx !== -1) {
          this.sharedJournals[sharedIdx] = res.data
        }
        
        // Update currentJournal if it's the one being edited
        if (this.currentJournal?.id === journalId) {
          this.currentJournal = res.data
        }
        
        return res.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to update journal"
        console.error("Failed to update journal:", err)
        throw err
      } finally {
        this.isSaving = false
      }
    },

    // ── Delete Journal ────────────────────────────────────────────────
    async deleteJournal(journalId: string) {
      this.error = null
      
      try {
        await deleteJournalApi(journalId)
        
        // Remove from lists
        this.privateJournals = this.privateJournals.filter(j => j.id !== journalId)
        this.sharedJournals = this.sharedJournals.filter(j => j.id !== journalId)
        
        // Clear currentJournal if it was deleted
        if (this.currentJournal?.id === journalId) {
          this.currentJournal = null
        }
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to delete journal"
        console.error("Failed to delete journal:", err)
        throw err
      }
    },

    // ── Convert to Memory ─────────────────────────────────────────────
    async convertToMemory(journalId: string) {
      this.error = null
      
      try {
        await convertJournalApi(journalId)
        
        // Optionally refetch to update the journal with memory_id
        // Or you can update locally if the API returns the updated journal
      } catch (err: any) {
        this.error = err.response?.data?.detail || "Failed to convert journal to memory"
        console.error("Failed to convert journal:", err)
        throw err
      }
    },

    // ── Fetch Analytics ───────────────────────────────────────────────
    async fetchMyAnalytics() {
      try {
        const res = await getMyJournalAnalyticsApi()
        this.myAnalytics = res.data
        return res.data
      } catch (err: any) {
        console.error("Failed to fetch my analytics:", err)
        throw err
      }
    },

    async fetchVaultAnalytics() {
      try {
        const res = await getVaultJournalAnalyticsApi()
        this.vaultAnalytics = res.data
        return res.data
      } catch (err: any) {
        console.error("Failed to fetch vault analytics:", err)
        throw err
      }
    },

    // ── Set Current Journal ───────────────────────────────────────────
    setCurrentJournal(journal: Journal | null) {
      this.currentJournal = journal
    },

    // ── Clear Error ───────────────────────────────────────────────────
    clearError() {
      this.error = null
    }
  }
})