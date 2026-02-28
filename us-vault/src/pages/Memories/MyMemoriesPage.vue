<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { getMyMemoriesApi } from '../../api/memories'
// import { useAuthStore } from '../../stores/authStore'
// import { useVaultStore } from '../../stores/vaultStore'

const router = useRouter()

// ── Store (mock for now) ───────────────────────────────────────────────────
// const authStore = useAuthStore()
// const vaultStore = useVaultStore()
// const CURRENT_USER_ID = authStore.user?.id || 'user-001'
const CURRENT_USER_ID = 'user-001' // Mock

// ── State ──────────────────────────────────────────────────────────────────
const myMemories = ref([])
const isLoading = ref(true)
const searchQuery = ref('')
const sortBy = ref('newest') // newest, oldest, title

// Pagination
const currentPage = ref(1)
const perPage = ref(9)
const totalPages = ref(1)

// Stop looking here
const fetchMyMemories = async () => {
  isLoading.value = true

  try {
    const response = await getMyMemoriesApi(
      currentPage.value,
      perPage.value
    )

    myMemories.value = response.data.items
    totalPages.value = response.data.total_pages

  } catch (error) {
    console.error('Failed to load memories:', error)
  } finally {
    isLoading.value = false
  }
}

// ── Computed ─-
const filteredMemories = computed(() => {
  let result = [...myMemories.value]
  
  // Search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(m => 
      m.title.toLowerCase().includes(query) || 
      m.content.toLowerCase().includes(query)
    )
  }
  
  // Sort
  switch (sortBy.value) {
    case 'oldest':
      result.sort((a, b) => new Date(a.memory_date) - new Date(b.memory_date))
      break
    case 'title':
      result.sort((a, b) => a.title.localeCompare(b.title))
      break
    case 'newest':
    default:
      result.sort((a, b) => new Date(b.memory_date) - new Date(a.memory_date))
  }
  
  return result
})

const paginatedMemories = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return filteredMemories.value.slice(start, start + perPage.value)
})

const totalPagesComputed = computed(() => 
  Math.ceil(filteredMemories.value.length / perPage.value)
)

const pageNumbers = computed(() => {
  const pages = []
  const total = totalPagesComputed.value
  const current = currentPage.value
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i)
    }
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  
  return pages
})

// ── Methods ────────────────────────────────────────────────────────────────
const canEdit = (memory) => {
  const createdAt = new Date(memory.created_at)
  const now = new Date()

  const hoursDiff = (now.getTime() - createdAt.getTime()) / (1000 * 60 * 60)

  return hoursDiff <= 8
}

const goToPage = (page) => {
  if (typeof page === 'number' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchMyMemories()
  }
}

const truncate = (text, max = 120) => {
  if (!text) return ''
  return text.length > max ? text.slice(0, max) + '…' : text
}

const formatDate = (iso) => {
  return new Date(iso).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

// ── Lifecycle ──────────────
onMounted(() => {
  fetchMyMemories()
})
</script>

<template>
  <InactivityOverlay>
    <Sidebar>
      <div class="my-memories-page min-h-screen relative overflow-x-hidden">
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
        </component>

        <!-- Ambient BG -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#fce7f3 0%,transparent 70%);"></div>
          <div class="absolute top-1/2 -left-20 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#fce7f3 0%,transparent 70%);"></div>
        </div>

        <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">

          <!-- Loading -->
          <div v-if="isLoading" class="flex items-center justify-center min-h-100">
            <div class="flex flex-col items-center gap-3">
              <div class="flex gap-1">
                <span class="w-2 h-2 rounded-full bg-rose-400 loading-dot" style="animation-delay:0s"></span>
                <span class="w-2 h-2 rounded-full bg-rose-400 loading-dot" style="animation-delay:0.2s"></span>
                <span class="w-2 h-2 rounded-full bg-rose-400 loading-dot" style="animation-delay:0.4s"></span>
              </div>
              <p class="mem-body text-sm text-rose-400 tracking-wide">Loading memories…</p>
            </div>
          </div>

          <template v-else>
            <!-- Header -->
            <div class="mb-8 md:mb-10">
              <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-6">
                <div>
                  <p class="mem-sub text-xs text-rose-500 uppercase tracking-widest mb-1">Your Collection</p>
                  <h1 class="mem-display text-4xl md:text-5xl text-slate-900">My Memories</h1>
                  <p class="mem-body text-sm text-slate-500 mt-2">
                    {{ myMemories.length }} {{ myMemories.length === 1 ? 'memory' : 'memories' }} you've created
                  </p>
                </div>
              </div>

              <!-- Search & Sort -->
              <div class="flex flex-col sm:flex-row gap-3 mb-6">
                <!-- Search -->
                <div class="flex-1">
                  <input 
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search your memories..."
                    class="w-full px-4 py-2.5 rounded-xl border border-rose-100 focus:border-rose-300 focus:ring-2 focus:ring-rose-100 transition mem-body text-sm"
                  />
                </div>

                <!-- Sort -->
                <div class="flex items-center gap-2">
                  <span class="mem-body text-xs text-slate-500 uppercase tracking-wide">Sort:</span>
                  <div class="flex gap-1">
                    <button 
                      v-for="option in [
                        { value: 'newest', label: 'Newest' },
                        { value: 'oldest', label: 'Oldest' },
                        { value: 'title', label: 'Title' }
                      ]" 
                      :key="option.value"
                      @click="sortBy = option.value"
                      :class="[
                        'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all mem-body',
                        sortBy === option.value 
                          ? 'bg-rose-500 text-white shadow-sm' 
                          : 'text-slate-500 hover:bg-rose-50'
                      ]">
                      {{ option.label }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Divider -->
              <div class="flex items-center gap-3">
                <div class="h-px flex-1" style="background: linear-gradient(90deg,#fb7185,#fda4af,transparent);"></div>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="#fb7185">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
                <div class="h-px w-8" style="background:#fda4af;"></div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredMemories.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
              <div class="w-20 h-20 rounded-full bg-rose-50 flex items-center justify-center mb-4">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="2">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </div>
              <h3 class="mem-display text-xl text-slate-700 mb-2">
                {{ searchQuery ? 'No memories found' : 'No memories yet' }}
              </h3>
              <p class="mem-body text-sm text-slate-500 text-center max-w-sm">
                {{ searchQuery ? 'Try adjusting your search query' : 'Start creating memories to see them here' }}
              </p>
            </div>

            <!-- Memories Grid -->
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
              <article 
                v-for="(memory, idx) in paginatedMemories" 
                :key="memory.id"
                @click="router.push(`/memories/${memory.id}`)"
                class="memory-card group relative bg-white rounded-2xl overflow-hidden border border-rose-50 hover:border-rose-200 transition-all duration-300 cursor-pointer"
                :style="`animation-delay:${idx*60}ms`">

                <!-- Top accent -->
                <div class="h-1 w-full" style="background: linear-gradient(90deg,#fb7185,#fda4af,#fecdd3);"></div>

                <!-- Edit badge -->
                <div v-if="canEdit(memory)" 
                     class="absolute top-3 right-3 z-10 px-2.5 py-1 rounded-full bg-emerald-500 text-white text-xs font-bold mem-body">
                  Editable
                </div>

                <!-- Image -->
                <div v-if="(memory.media || []).length > 0 && memory.media[0].file_type.startsWith('image/')" 
                     class="aspect-video overflow-hidden bg-slate-100">
                  <img 
                    :src="memory.media[0].file_url" 
                    :alt="memory.title"
                    class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <div v-else class="aspect-video bg-linear-to-br from-rose-50 to-pink-50 flex items-center justify-center">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="1.5" opacity="0.3">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                  </svg>
                </div>

                <!-- Content -->
                <div class="p-5">
                  <!-- Badges -->
                  <div class="flex items-center gap-2 mb-3">
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold mem-body bg-rose-50 text-rose-600 border border-rose-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                      You
                    </span>
                    <span v-if="memory.is_seed" class="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs mem-body font-semibold bg-violet-100 text-violet-700">
                      🌱 From Bloom
                    </span>
                  </div>

                  <!-- Title -->
                  <h2 class="mem-display text-lg text-slate-900 leading-snug mb-2 line-clamp-2">
                    {{ memory.title }}
                  </h2>

                  <!-- Content preview -->
                  <p class="mem-body text-sm text-slate-600 leading-relaxed mb-4 line-clamp-3">
                    {{ truncate(memory.content, 100) }}
                  </p>

                  <!-- Footer -->
                  <div class="flex items-center justify-between">
                    <span class="mem-body text-xs text-slate-400">
                      {{ formatDate(memory.memory_date) }}
                    </span>
                    <button class="mem-body text-xs text-rose-600 hover:text-rose-800 font-semibold flex items-center gap-1 transition-colors">
                      {{ canEdit(memory) ? 'Edit' : 'View' }}
                      <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="9 18 15 12 9 6"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </article>
            </div>

            <!-- Pagination -->
            <div v-if="totalPagesComputed > 1" class="flex items-center justify-center gap-2 pt-6 border-t border-rose-50">
              <button 
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-4 py-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed mem-body text-sm font-semibold transition">
                Previous
              </button>
              
              <div v-for="(page, i) in pageNumbers" :key="i">
                <span v-if="page === '...'" class="px-2 text-slate-400 mem-body text-sm">…</span>
                <button 
                  v-else
                  @click="goToPage(page)"
                  :class="[
                    'px-4 py-2 rounded-lg mem-body text-sm font-semibold transition',
                    currentPage === page 
                      ? 'bg-rose-500 text-white shadow-sm' 
                      : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                  ]">
                  {{ page }}
                </button>
              </div>
              
              <button 
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPagesComputed"
                class="px-4 py-2 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed mem-body text-sm font-semibold transition">
                Next
              </button>
            </div>

          </template>
        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
.my-memories-page {
  background: linear-gradient(160deg, #fff1f2 0%, #ffffff 50%, #fef2f2 100%);
}
.mem-display { font-family: 'Crimson Pro', Georgia, serif; font-weight: 500; }
.mem-body    { font-family: 'Inter', sans-serif; }
.mem-sub     { font-family: 'Inter', sans-serif; }

.memory-card {
  box-shadow: 0 2px 16px rgba(251,113,133,0.08);
  animation: cardReveal 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.memory-card:hover {
  box-shadow: 0 12px 36px rgba(251,113,133,0.15), 0 4px 12px rgba(0,0,0,0.04);
  transform: translateY(-4px);
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

.line-clamp-3 {
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.loading-dot { 
  animation: dotPulse 1.2s ease-in-out infinite; 
}
@keyframes dotPulse { 
  0%,100% { opacity: 0.3; transform: scale(0.8); } 
  50% { opacity: 1; transform: scale(1.2); } 
}
</style>