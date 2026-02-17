<script setup>
import { ref, onMounted } from "vue"
import FlowerFieldOverlay from "./FlowerFieldOverlay.vue"

const showFlowers = ref(false)
const signalCount = ref(0)

onMounted(() => {
  // Simulate API call delay
  setTimeout(() => {
    // This would come from your API response
    signalCount.value = 2
    console.log(`Checking signal count: ${signalCount.value}`)
    
    if (signalCount.value > 0) {
      showFlowers.value = true
      console.log("Flowers will bloom!")
    }
  }, 1200)
})
</script>

<template>
  <div class="dashboard">
    <h1>This is the dashboard</h1>
    <p>Welcome to your dashboard. Your content goes here.</p>

    <FlowerFieldOverlay 
      v-if="showFlowers" 
      :signal-count="signalCount" 
    />
  </div>
</template>

<style scoped>
.dashboard {
  padding: 3rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.dashboard p {
  color: #666;
  font-size: 1.1rem;
}
</style>