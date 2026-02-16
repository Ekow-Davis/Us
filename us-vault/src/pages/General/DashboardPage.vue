<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})


</script>

<template>
  <div>

    <p>
        Dashboard page
    </p>
    <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
