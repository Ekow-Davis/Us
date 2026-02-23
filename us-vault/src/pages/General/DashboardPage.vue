<script setup>
import { ref, onMounted } from "vue"
import FlowerFieldOverlay from "./FlowerFieldOverlay.vue"

import Sidebar from "../../components/layout/Sidebar.vue"
import DashboardContent from "./DashboardContent.vue"

const showFlowers = ref(false)
const signalCount = ref(0)

onMounted(() => {
  // Simulate API call delay
  setTimeout(() => {
    // This would come from your API response
    signalCount.value = 13
    console.log(`Checking signal count: ${signalCount.value}`)
    
    if (signalCount.value > 0) {
      showFlowers.value = true
      console.log("Flowers will bloom!")
    }
  }, 1200)
})
</script>

<template>
  <Sidebar>
    <div class="dashboard">
    <DashboardContent />

    <FlowerFieldOverlay 
      v-if="showFlowers" 
      :signal-count="signalCount" 
    />
  </div>
  </Sidebar>
  
</template>

<style scoped>

</style>