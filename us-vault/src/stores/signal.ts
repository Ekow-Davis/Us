import { defineStore } from "pinia"
import {
  getUnreadSignalCountApi,
  markSignalsSeenApi,
} from "../api/signals"

export const useSignalStore = defineStore("signal", {
  state: () => ({
    unreadCount: 0,
    displayCount: 0, // Separate count for display (won't change during animation)
    isLoading: false,
    hasSeenAnimation: false, // Track if animation has been viewed
  }),
  actions: {
    async fetchUnreadCount() {
      try {
        const res = await getUnreadSignalCountApi()
        this.unreadCount = res.data.unread_count
        this.displayCount = res.data.unread_count // Set display count
        
        // DON'T mark as seen immediately - let the animation play
        // The FlowerFieldOverlay component will call markAsSeen() when it closes
      } catch (err) {
        console.error("Failed to fetch signal count", err)
      }
    },
    
    async markAsSeen() {
      try {
        await markSignalsSeenApi()
        this.unreadCount = 0
        this.displayCount = 0
        this.hasSeenAnimation = true
      } catch (err) {
        console.error("Failed to mark signals as seen", err)
      }
    },
    
    // Reset the animation state (useful for testing or when new signals arrive)
    resetAnimationState() {
      this.hasSeenAnimation = false
    }
  }
})