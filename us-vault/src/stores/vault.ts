// src/stores/vault.ts
import { defineStore } from "pinia"
import { getVaultDetailsApi } from "../api/vault"

export const useVaultStore = defineStore("vault", {
  state: () => ({
    vaultId: null as string | null,
    partnerName: null as string | null,
    status: null as string | null,
    createdAt: null as string | null,
    createdBy: null as string | null,
    stats: null as any,
    isLoading: false,
    isInitialized: false
  }),

  getters: {
    hasVault: (state) => !!state.vaultId,
    isActive: (state) => state.status === "active",
  },

  actions: {

    async fetchVault() {
      this.isLoading = true
      try {
        const res = await getVaultDetailsApi()

        const data = res.data

        this.vaultId = data.vault_id
        this.partnerName = data.partner_name
        this.status = data.status
        this.createdAt = data.created_at
        this.createdBy = data.created_by
        this.stats = data.stats

      } catch (err) {
        // Not in vault
        this.resetVault()
      } finally {
        this.isLoading = false
        this.isInitialized = true
      }
    },

    resetVault() {
      this.vaultId = null
      this.partnerName = null
      this.status = null
      this.createdAt = null
      this.createdBy = null
      this.stats = null
    }
  }
})