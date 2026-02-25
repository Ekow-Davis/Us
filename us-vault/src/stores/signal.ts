import { defineStore } from "pinia"
import {
  getUnreadSignalCountApi,
  markSignalsSeenApi,
} from "../api/signals"

export const useSignalStore = defineStore("signal", {
  state: () => ({
    unreadCount: 0,
    isLoading: false,
  }),

  actions: {
    async fetchUnreadCount() {
      try {
        const res = await getUnreadSignalCountApi()
        this.unreadCount = res.data.unread_count

        // If there are unread signals, mark them as seen
        if (this.unreadCount > 0) {
          await this.markAsSeen()
        }

      } catch (err) {
        console.error("Failed to fetch signal count", err)
      }
    },

    async markAsSeen() {
      try {
        await markSignalsSeenApi()
        this.unreadCount = 0
      } catch (err) {
        console.error("Failed to mark signals as seen", err)
      }
    }
  }
})