<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'

import { useMemoryStore } from '../../stores/memories'
import { useAuthStore } from '../../stores/auth'
import { useVaultStore } from '../../stores/vault'

const router = useRouter()

const memoryStore = useMemoryStore()
const auth = useAuthStore()
const vault = useVaultStore()

/* Pagination (Backend-driven) */

const perPage = ref(6)
const currentPage = ref(1)

watch(currentPage, async (page) => {
  await memoryStore.fetchMemories(page)
})

onMounted(async () => {
  await memoryStore.fetchMemories(currentPage.value)
})

const paginatedMemories = computed(() => memoryStore.memories)
const totalPages = computed(() => memoryStore.totalPages)

/* Helpers */

const truncate = (text, max = 100) => {
  if (!text) return ''
  return text.length > max ? text.slice(0, max) + '…' : text
}

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })

const isOwn = (memory) =>
  memory.created_by === auth.user?.id

const authorLabel = (memory) => {
  if (isOwn(memory)) return 'You'
  return vault.partnerName || 'Partner'
}

const primaryImage = (memory) =>
  memory.media?.find((m) =>
    m.file_type?.startsWith('image/')
  )

const goToPage = (p) => {
  if (p >= 1 && p <= totalPages.value) {
    currentPage.value = p
  }
}

</script>

<template>
  <InactivityOverlay>
    <Sidebar>
      <div class="memories-page min-h-screen relative overflow-x-hidden">
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Nunito:wght@300;400;600;700&display=swap');
        </component>

        <!-- Background -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <div class="absolute -top-16 -right-16 w-80 h-80 rounded-full opacity-20" style="background: radial-gradient(circle, #fce7f3 0%, transparent 70%);"></div>
          <div class="absolute top-1/3 -left-20 w-64 h-64 rounded-full opacity-15" style="background: radial-gradient(circle, #ede9fe 0%, transparent 70%);"></div>
          <!-- Thread lines -->
          <svg class="absolute top-0 right-0 w-full h-full opacity-5" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice">
            <line x1="0" y1="150" x2="800" y2="180" stroke="#7c3aed" stroke-width="0.5"/>
            <line x1="0" y1="300" x2="800" y2="320" stroke="#f43f5e" stroke-width="0.5"/>
            <line x1="0" y1="450" x2="800" y2="460" stroke="#7c3aed" stroke-width="0.5"/>
          </svg>
        </div>

        <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

          <!-- Header -->
          <div class="mb-10">
            <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
              <div>
                <p class="mem-sub text-xs text-rose-400 uppercase tracking-widest mb-1">Your Vault</p>
                <h1 class="mem-display text-5xl text-gray-900">Memories</h1>
                <p class="mem-body text-sm text-gray-400 mt-2">{{ memoryStore.total || 0 }} moments preserved</p>
              </div>

              <!-- Per page selector -->
              <div class="flex items-center gap-3 bg-white rounded-xl px-4 py-2.5 border border-gray-100 shadow-sm self-start sm:self-auto">
                <span class="mem-body text-xs text-gray-400 uppercase tracking-wide">Show</span>
                <div class="flex gap-1">
                  <button v-for="n in [5, 6, 8, 10]" :key="n"
                          @click="perPage = n"
                          :class="['px-3 py-1 rounded-lg text-xs font-semibold transition-all duration-200 mem-body',
                                  perPage === n ? 'bg-rose-500 text-white shadow-sm' : 'text-gray-500 hover:bg-gray-100']">
                    {{ n }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Decorative divider -->
            <div class="flex items-center gap-3 mt-6">
              <div class="h-px flex-1" style="background: linear-gradient(90deg, #f43f5e, #c084fc, transparent);"></div>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="#fca5a5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              <div class="h-px w-8" style="background: #fca5a5;"></div>
            </div>
          </div>

          <!-- Top Pagination -->
          <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
            <p class="mem-body text-xs text-gray-400">
              Page {{ currentPage }} of {{ totalPages }} &nbsp;·&nbsp; {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, memoryStore.total || 0) }} of {{ memoryStore.total || 0 }} memories
            </p>
            <div class="flex items-center gap-1">
              <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                      :class="['pag-btn', currentPage === 1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <template v-for="(p, i) in pageNumbers">
                <span v-if="p === '...'"  :key="'ellipsis-' + i" class="px-1 text-gray-400 mem-body text-sm">…</span>
                <button v-else @click="goToPage(p)"
                        :class="['pag-btn', currentPage === p ? 'bg-rose-500 text-white shadow-sm' : 'hover:bg-rose-50 hover:text-rose-600']"
                        :key="'page-' + p"
                        >
                  {{ p }}
                </button>
              </template>
              <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
                      :class="['pag-btn', currentPage === totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>

          <!-- Memory Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
            <article v-for="(memory, idx) in paginatedMemories" :key="memory.id"
                    @click="router.push(`/memories/${memory.id}`)"
                    class="memory-card group relative bg-white rounded-2xl overflow-hidden cursor-pointer border border-gray-100 transition-all duration-300 hover:-translate-y-1.5"
                    :style="`animation-delay: ${idx * 60}ms`">

              <!-- Gradient top strip -->
              <div class="h-0.5 w-full" :style="isOwn(memory) ? 'background: linear-gradient(90deg,#f43f5e,#fb7185)' : 'background: linear-gradient(90deg,#7c3aed,#a855f7)'"></div>

              <!-- Media -->
              <div v-if="primaryImage(memory)" class="relative overflow-hidden bg-gray-50" style="height: 180px;">
                <img :src="primaryImage(memory).file_url" :alt="memory.title"
                    class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"/>
                <!-- Date overlay -->
                <div class="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/50 backdrop-blur-sm">
                  <span class="text-white font-mono text-xs">{{ formatDate(memory.memory_date) }}</span>
                </div>
                <!-- Bloom badge -->
                <div v-if="memory.is_seed" class="absolute top-2 left-2 px-2 py-0.5 rounded-full bg-purple-700/80 backdrop-blur-sm flex items-center gap-1">
                  <svg width="8" height="8" viewBox="0 0 60 60" fill="white"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
                  <span class="text-white text-xs mem-body">From a Bloom</span>
                </div>
              </div>

              <!-- Card Body -->
              <div class="p-4 flex flex-col gap-2">
                <!-- Author badge -->
                <div class="flex items-center justify-between">
                  <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold mem-body border',
                                isOwn(memory) ? 'bg-rose-50 text-rose-600 border-rose-100' : 'bg-purple-50 text-purple-600 border-purple-100']">
                    <span :class="['w-1.5 h-1.5 rounded-full', isOwn(memory) ? 'bg-rose-400' : 'bg-purple-400']"></span>
                    {{ isOwn(memory) ? 'You' : 'Partner' }}
                  </span>
                  <span v-if="!primaryImage(memory)" class="mem-body text-xs text-gray-400">{{ formatDate(memory.memory_date) }}</span>
                </div>

                <h2 class="mem-display text-base text-gray-900 leading-snug group-hover:text-rose-600 transition-colors line-clamp-2">
                  {{ memory.title }}
                </h2>

                <p v-if="memory.content" class="mem-body text-sm text-gray-500 leading-relaxed">
                  {{ truncate(memory.content, 100) }}
                </p>

                <!-- Media indicator chips -->
                <div v-if="memory.media.length > 0 && !primaryImage(memory)" class="flex gap-1.5 mt-1">
                  <span v-for="m in memory.media" :key="m.id"
                        class="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 rounded-full text-xs text-gray-500 mem-body">
                    <svg v-if="m.file_type.startsWith('video')" width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                    <svg v-else width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                    {{ m.file_type.startsWith('video') ? 'Video' : 'Image' }}
                  </span>
                </div>

                <!-- Read more cue -->
                <div class="flex items-center gap-1 mt-1 text-xs text-gray-300 group-hover:text-rose-400 transition-colors mem-body">
                  <span>Open memory</span>
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                </div>
              </div>
            </article>
          </div>

          <!-- Bottom Pagination -->
          <div class="flex items-center justify-between flex-wrap gap-3 pt-4 border-t border-gray-100">
            <p class="mem-body text-xs text-gray-400">
              Showing {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, memoryStore.total || 0) }} of {{ memoryStore.total || 0 }} memories memories
            </p>
            <div class="flex items-center gap-1">
              <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                      :class="['pag-btn', currentPage === 1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <div v-for="(p, i) in pageNumbers" :key="i">
                <span v-if="p === '...'" class="px-1 text-gray-400 mem-body text-sm">…</span>
                <button v-else @click="goToPage(p)"
                        :class="['pag-btn', currentPage === p ? 'bg-rose-500 text-white shadow-sm' : 'hover:bg-rose-50 hover:text-rose-600']">
                  {{ p }}
                </button>
              </div>
              <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
                      :class="['pag-btn', currentPage === totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>

        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>

</template>

<style scoped>
.memories-page {
  background: linear-gradient(155deg, #fff8f8 0%, #ffffff 50%, #f9f5ff 100%);
}
.mem-display { font-family: 'Libre Baskerville', Georgia, serif; }
.mem-body    { font-family: 'Nunito', sans-serif; }
.mem-sub     { font-family: 'Nunito', sans-serif; }

.pag-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8125rem;
  font-family: 'Nunito', sans-serif;
  font-weight: 600;
  color: #6b7280;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.memory-card {
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  animation: cardReveal 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.memory-card:hover {
  box-shadow: 0 12px 32px rgba(244,63,94,0.12), 0 4px 12px rgba(0,0,0,0.06);
}

@keyframes cardReveal {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.line-clamp-2 {
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>