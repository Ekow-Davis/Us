<script setup>
import FlowerFieldOverlay from "./FlowerFieldOverlay.vue"
import Sidebar from "../../components/layout/Sidebar.vue"
import InactivityOverlay from "../../components/layout/InactivityOverlay.vue"
import DashboardContent from "./DashboardContent.vue"
import { onMounted } from "vue"
import { useSignalStore } from "../../stores/signal"

const signalStore = useSignalStore()

onMounted(() => {
  signalStore.fetchUnreadCount()
})
</script>

<template>
  <InactivityOverlay>
    <Sidebar>
      <div class="dashboard">
        <DashboardContent />
        
        <!-- Use displayCount instead of unreadCount so it doesn't disappear during animation -->
        <FlowerFieldOverlay 
          v-if="signalStore.displayCount > 0" 
          :signal-count="signalStore.displayCount" 
        />
      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
.dashboard {
  position: relative;
  min-height: 100vh;
}
</style>