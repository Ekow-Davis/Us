<script setup>
import FlowerFieldOverlay from "./FlowerFieldOverlay.vue"

import Sidebar from "../../components/layout/Sidebar.vue"
import DashboardContent from "./DashboardContent.vue"

import { onMounted } from "vue"
import { useSignalStore } from "../../stores/signal"

const signal = useSignalStore()

onMounted(() => {
  signal.fetchUnreadCount()
})
</script>

<template>
  <Sidebar>
    <div class="dashboard">
    <DashboardContent />

    <FlowerFieldOverlay 
      v-if="signal.unreadCount > 0" 
      :signal-count="signal.unreadCount" 
    />
  </div>
  </Sidebar>
  
</template>

<style scoped>

</style>