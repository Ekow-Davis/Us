<template>
  <div class="min-h-screen p-4">
    <h1 class="text-3xl font-bold mb-6">Memory Details</h1>
    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-semibold mb-4">{{ memory.title }}</h2>
      <p class="text-gray-700 mb-4">{{ memory.content }}</p>
      <p class="text-sm text-gray-500">Memory Date: {{ new Date(memory.memory_date).toLocaleDateString() }}</p>
      <p class="text-sm text-gray-500">Bloom Date: {{ new Date(memory.bloom_date).toLocaleDateString() }}</p>
    </div>
  </div>
</template>

<script>

</script>

<style>

</style>