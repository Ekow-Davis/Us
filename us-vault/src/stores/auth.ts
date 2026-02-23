import { defineStore } from "pinia"
import {
  loginApi,
  refreshApi,
  getMeApi,
  logoutApi
} from "../api/auth"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: null as string | null,
    user: null as any,
    isInitialized: false,
  }),

  actions: {
    async login(credentials: { email: string; password: string }) {
      const res = await loginApi(credentials)
      this.accessToken = res.data.access_token

      await this.fetchUser()
    },

    async fetchUser() {
      const res = await getMeApi()
      this.user = res.data
    },

    async refresh() {
      try {
        const res = await refreshApi()
        this.accessToken = res.data.access_token
        return true
      } catch {
        this.accessToken = null
        this.user = null
        return false
      }
    },

    async logout() {
      await logoutApi()
      this.accessToken = null
      this.user = null
    },

    async initialize() {
      try {
        const res = await refreshApi()
        this.accessToken = res.data.access_token
        await this.fetchUser()
      } catch {
        // silent fail — user not logged in
      } finally {
        this.isInitialized = true
      }
    }
  }
})