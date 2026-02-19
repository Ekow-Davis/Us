<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'

const router = useRouter()
const CURRENT_USER_ID = 'user-001'

// ── Mock API State ──────────────────────────────────────────────────────────
const mySeeds = ref([])
const seedSummary = ref({
  total: 0,
  growing: 0,
  ready: 0,
  bloomed: 0
})
const isLoading = ref(true)

// ── Mock API Calls ──────────────────────────────────────────────────────────
const fetchMySeeds = async (page = 1, pageSize = 6) => {
  // Mock GET /seeds/me
  await new Promise(resolve => setTimeout(resolve, 300))
  
  return {
    items: [
      { id: 'seed-001', vault_id: 'v1', created_by: 'user-001', title: 'A Letter for Our First Year', bloom_at: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), status: 'scheduled', memory_id: null },
      { id: 'seed-003', vault_id: 'v1', created_by: 'user-001', title: 'The Dream I Had About Us', bloom_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(), status: 'bloomed', memory_id: 'mem-003' },
      { id: 'seed-005', vault_id: 'v1', created_by: 'user-001', title: 'Midwinter Note', bloom_at: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), status: 'scheduled', memory_id: null },
      { id: 'seed-007', vault_id: 'v1', created_by: 'user-001', title: 'The Quiet Ones', bloom_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 50 * 24 * 60 * 60 * 1000).toISOString(), status: 'bloomed', memory_id: 'mem-007' },
      { id: 'seed-009', vault_id: 'v1', created_by: 'user-001', title: 'Promise for the Future', bloom_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), status: 'scheduled', memory_id: null },
      { id: 'seed-010', vault_id: 'v1', created_by: 'user-001', title: 'Our First Adventure', bloom_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), status: 'scheduled', memory_id: null },
    ],
    total: 6,
    page: 1,
    page_size: pageSize,
    total_pages: Math.ceil(6 / pageSize)
  }
}

const fetchSeedSummary = async () => {
  // Mock GET /seeds/summary (but filtered for user's seeds)
  await new Promise(resolve => setTimeout(resolve, 150))
  
  return {
    total: 6,
    growing: 3,
    ready: 1,
    bloomed: 2
  }
}

const deleteSeed = async (seedId) => {
  // Mock DELETE /seeds/{seed_id}
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Remove from local state
  mySeeds.value = mySeeds.value.filter(s => s.id !== seedId)
}

// ── Lifecycle Computed ──────────────────────────────────────────────────────
const now = ref(new Date())
setInterval(() => { now.value = new Date() }, 30000) // Update every 30s

const growingSeeds = computed(() => 
  mySeeds.value.filter(s => s.status === 'scheduled' && new Date(s.bloom_at) > now.value)
)

const readySeeds = computed(() => 
  mySeeds.value.filter(s => s.status === 'scheduled' && new Date(s.bloom_at) <= now.value)
)

const bloomedSeeds = computed(() => 
  mySeeds.value.filter(s => s.status === 'bloomed')
)

// ── Pagination ────────────────────────────────────────────────────────────────
const perPage = ref(6)
const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(mySeeds.value.length / perPage.value))
const paginatedSeeds = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return mySeeds.value.slice(start, start + perPage.value)
})
const pageNumbers = computed(() => {
  const pages = [], total = totalPages.value, current = currentPage.value
  if (total <= 7) { for (let i = 1; i <= total; i++) pages.push(i) }
  else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})
watch(perPage, () => { currentPage.value = 1 })
const goToPage = (p) => { if (typeof p === 'number' && p >= 1 && p <= totalPages.value) currentPage.value = p }

// ── Delete Confirmation ─────────────────────────────────────────────────────
const showDeleteModal = ref(false)
const seedToDelete = ref(null)
const isDeleting = ref(false)

const confirmDelete = (seed) => {
  seedToDelete.value = seed
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  seedToDelete.value = null
}

const handleDelete = async () => {
  if (!seedToDelete.value || isDeleting.value) return
  
  isDeleting.value = true
  try {
    await deleteSeed(seedToDelete.value.id)
    showDeleteModal.value = false
    seedToDelete.value = null
  } catch (error) {
    console.error('Failed to delete seed:', error)
  } finally {
    isDeleting.value = false
  }
}

// ── Edit Seed ───────────────────────────────────────────────────────────────
const editSeed = (seedId) => {
  router.push(`/seeds/edit/${seedId}`)
}

// ── Navigate to Memory ──────────────────────────────────────────────────────
const viewMemory = (memoryId) => {
  if (memoryId) {
    router.push(`/memories/${memoryId}`)
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const formatDateTime = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' })

const getLifecycleStatus = (seed) => {
  if (seed.status === 'bloomed') return 'bloomed'
  if (seed.status === 'scheduled' && new Date(seed.bloom_at) <= now.value) return 'ready'
  return 'growing'
}

const timeUntilBloom = (bloomAt) => {
  const diff = new Date(bloomAt) - now.value
  if (diff <= 0) return 'Ready'
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  if (days > 0) return `${days}d ${hours}h`
  return `${hours}h`
}

const bloomProgress = (seed) => {
  const created = new Date(seed.created_at)
  const bloom = new Date(seed.bloom_at)
  const elapsed = now.value - created
  const total = bloom - created
  return Math.max(0, Math.min(100, (elapsed / total) * 100))
}

const canEdit = (seed) => {
  if (seed.status !== 'scheduled') return false
  const editWindowEnd = new Date(seed.created_at).getTime() + (24 * 60 * 60 * 1000)
  const bloomTime = new Date(seed.bloom_at).getTime()
  return now.value.getTime() <= editWindowEnd || now.value.getTime() < bloomTime
}

const canDelete = (seed) => {
  if (seed.status !== 'scheduled') return false
  const createdTime = new Date(seed.created_at).getTime()
  const bloomTime = new Date(seed.bloom_at).getTime()
  const nowTime = now.value.getTime()
  
  const withinCreationWindow = nowTime <= createdTime + (24 * 60 * 60 * 1000)
  const beforeBloomCutoff = nowTime <= bloomTime - (24 * 60 * 60 * 1000)
  
  return withinCreationWindow || beforeBloomCutoff
}

// ── Init ──────────────────────────────────────────────────────────────────────
onMounted(async () => {
  isLoading.value = true
  try {
    const [seedsData, summaryData] = await Promise.all([
      fetchMySeeds(currentPage.value, perPage.value),
      fetchSeedSummary()
    ])
    
    mySeeds.value = seedsData.items
    seedSummary.value = summaryData
  } catch (error) {
    console.error('Failed to load seeds:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <Sidebar>
    <div class="my-seeds-page min-h-screen relative overflow-x-hidden">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
      </component>

      <!-- Ambient BG -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#c7d2fe 0%,transparent 70%);"></div>
        <div class="absolute top-1/2 -left-20 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
        <div class="absolute bottom-0 right-1/4 w-64 h-64 rounded-full opacity-10" style="background: radial-gradient(circle,#fae8ff 0%,transparent 70%);"></div>
        
        <!-- Vine SVG left -->
        <svg class="absolute left-0 top-0 h-full w-16 md:w-20 opacity-[0.05]" viewBox="0 0 80 800" preserveAspectRatio="none" fill="none">
          <path d="M40 0 Q10 100 40 200 Q70 300 40 400 Q10 500 40 600 Q70 700 40 800" stroke="#6366f1" stroke-width="2"/>
          <ellipse cx="22" cy="160" rx="18" ry="8" fill="#6366f1" transform="rotate(-30 22 160)"/>
          <ellipse cx="58" cy="360" rx="18" ry="8" fill="#818cf8" transform="rotate(25 58 360)"/>
          <ellipse cx="22" cy="560" rx="16" ry="7" fill="#6366f1" transform="rotate(-20 22 560)"/>
        </svg>
        
        <!-- Vine SVG right -->
        <svg class="absolute right-0 top-0 h-full w-16 md:w-20 opacity-[0.05]" viewBox="0 0 80 800" preserveAspectRatio="none" fill="none">
          <path d="M40 0 Q70 100 40 200 Q10 300 40 400 Q70 500 40 600 Q10 700 40 800" stroke="#6366f1" stroke-width="2"/>
          <ellipse cx="58" cy="160" rx="18" ry="8" fill="#6366f1" transform="rotate(30 58 160)"/>
          <ellipse cx="22" cy="360" rx="18" ry="8" fill="#818cf8" transform="rotate(-25 22 360)"/>
          <ellipse cx="58" cy="560" rx="16" ry="7" fill="#6366f1" transform="rotate(20 58 560)"/>
        </svg>
      </div>

      <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">

        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center min-h-100">
          <div class="flex flex-col items-center gap-3">
            <div class="flex gap-1">
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.2s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.4s"></span>
            </div>
            <p class="seed-body text-sm text-indigo-400 tracking-wide">Loading your seeds…</p>
          </div>
        </div>

        <template v-else>
          <!-- Header -->
          <div class="mb-8 md:mb-10">
            <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
              <div>
                <p class="seed-sub text-xs text-indigo-500 uppercase tracking-widest mb-1">Your Garden</p>
                <h1 class="seed-display text-4xl md:text-5xl text-slate-900">My Seeds</h1>
                <div class="flex flex-wrap items-center gap-3 mt-2">
                  <p class="seed-body text-sm text-slate-500">{{ seedSummary.total }} seeds planted</p>
                  <span v-if="seedSummary.ready > 0"
                        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body bg-purple-100 text-purple-700 border border-purple-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                    {{ seedSummary.ready }} ready
                  </span>
                  <span v-if="seedSummary.growing > 0"
                        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    {{ seedSummary.growing }} growing
                  </span>
                  <span v-if="seedSummary.bloomed > 0"
                        class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body bg-pink-50 text-pink-700 border border-pink-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-pink-400"></span>
                    {{ seedSummary.bloomed }} bloomed
                  </span>
                </div>
              </div>
              
              <!-- Per page -->
              <div class="flex items-center gap-3 bg-white rounded-xl px-4 py-2.5 border border-indigo-100 shadow-sm self-start sm:self-auto">
                <span class="seed-body text-xs text-slate-500 uppercase tracking-wide">Show</span>
                <div class="flex gap-1">
                  <button v-for="n in [5, 6, 8, 10]" :key="n" @click="perPage = n"
                          :class="['px-3 py-1 rounded-lg text-xs font-semibold transition-all seed-body',
                                   perPage === n ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-500 hover:bg-indigo-50']">{{ n }}</button>
                </div>
              </div>
            </div>
            
            <!-- Divider -->
            <div class="flex items-center gap-3 mt-6">
              <div class="h-px flex-1" style="background: linear-gradient(90deg,#6366f1,#818cf8,transparent);"></div>
              <svg width="12" height="12" viewBox="0 0 60 60" fill="#818cf8"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
              <div class="h-px w-8" style="background:#818cf8;"></div>
            </div>
          </div>

          <!-- Top Pagination -->
          <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
            <p class="seed-body text-xs text-slate-500">Page {{ currentPage }} of {{ totalPages }} · {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, mySeeds.length) }} of {{ mySeeds.length }}</p>
            <div class="flex items-center gap-1">
              <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <template v-for="(p,i) in pageNumbers" :key="i">
                <span v-if="p==='...'" class="px-1 text-slate-400 seed-body text-sm">…</span>
                <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-indigo-600 text-white shadow-sm' : 'hover:bg-indigo-50 hover:text-indigo-600']">{{ p }}</button>
              </template>
              <button @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages" :class="['pag-btn', currentPage===totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>

          <!-- Seeds Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5 mb-8">
            <article v-for="(seed, idx) in paginatedSeeds" :key="seed.id"
                     class="seed-card group relative bg-white rounded-2xl overflow-hidden border border-indigo-50 transition-all duration-300 hover:-translate-y-1"
                     :style="`animation-delay:${idx*60}ms`">

              <!-- Top strip -->
              <div class="h-0.5 w-full" 
                   :style="getLifecycleStatus(seed) === 'bloomed' 
                     ? 'background:linear-gradient(90deg,#6366f1,#818cf8,#ec4899)' 
                     : getLifecycleStatus(seed) === 'ready'
                     ? 'background:linear-gradient(90deg,#6366f1,#c084fc)'
                     : 'background:linear-gradient(90deg,#6366f1,#818cf8)'"></div>

              <!-- Status Icon -->
              <div class="absolute top-3 right-3 z-10 w-9 h-9 flex items-center justify-center">
                <!-- Bloomed -->
                <button v-if="getLifecycleStatus(seed) === 'bloomed'"
                        @click="viewMemory(seed.memory_id)"
                        class="bloom-bud-btn"
                        title="View memory">
                  <svg width="36" height="36" viewBox="0 0 100 100" class="bloom-flower-icon">
                    <g transform="translate(50,50)">
                      <ellipse rx="11" ry="32" fill="#818cf8" opacity="0.85" transform="rotate(0)"/>
                      <ellipse rx="11" ry="32" fill="#6366f1" opacity="0.8" transform="rotate(45)"/>
                      <ellipse rx="11" ry="32" fill="#818cf8" opacity="0.85" transform="rotate(90)"/>
                      <ellipse rx="11" ry="32" fill="#6366f1" opacity="0.8" transform="rotate(135)"/>
                      <circle r="11" fill="#fbbf24"/>
                    </g>
                  </svg>
                </button>
                
                <!-- Ready -->
                <div v-else-if="getLifecycleStatus(seed) === 'ready'" class="ready-pulse" title="Ready to bloom!">
                  <svg width="32" height="40" viewBox="0 0 60 80" class="ready-bud">
                    <ellipse cx="30" cy="36" rx="16" ry="26" fill="#c084fc" opacity="0.8"/>
                    <ellipse cx="30" cy="24" rx="10" ry="16" fill="#a855f7" opacity="0.7"/>
                    <line x1="30" y1="62" x2="30" y2="78" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round"/>
                  </svg>
                </div>
                
                <!-- Growing -->
                <div v-else>
                  <svg width="28" height="36" viewBox="0 0 60 80" class="dormant-bud">
                    <ellipse cx="30" cy="38" rx="14" ry="22" fill="#c7d2fe" opacity="0.7"/>
                    <ellipse cx="30" cy="26" rx="8" ry="12" fill="#a5b4fc" opacity="0.6"/>
                    <line x1="30" y1="60" x2="30" y2="78" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round"/>
                  </svg>
                </div>
              </div>

              <div class="p-4 md:p-5 pr-12 md:pr-14">
                <!-- Status badge -->
                <div class="flex items-center gap-2 mb-3 flex-wrap">
                  <span :class="['inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs seed-body font-semibold',
                                 getLifecycleStatus(seed) === 'bloomed' ? 'bg-pink-100 text-pink-700' 
                                 : getLifecycleStatus(seed) === 'ready' ? 'bg-purple-100 text-purple-700'
                                 : 'bg-slate-100 text-slate-600']">
                    {{ getLifecycleStatus(seed) === 'bloomed' ? '✦ Bloomed' 
                       : getLifecycleStatus(seed) === 'ready' ? '◉ Ready' 
                       : '◌ Growing' }}
                  </span>
                  <span class="seed-body text-xs text-slate-400">
                    Planted {{ formatDate(seed.created_at) }}
                  </span>
                </div>

                <h2 class="seed-display text-lg text-slate-900 leading-snug mb-4 line-clamp-2">{{ seed.title }}</h2>

                <!-- Progress bar (only for growing) -->
                <div v-if="getLifecycleStatus(seed) === 'growing'" class="mb-4">
                  <div class="flex justify-between items-center mb-1">
                    <span class="seed-body text-xs text-slate-400">Growing</span>
                    <span class="seed-body text-xs font-semibold text-indigo-600">{{ timeUntilBloom(seed.bloom_at) }}</span>
                  </div>
                  <div class="w-full h-1.5 bg-indigo-50 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-500" 
                         :style="`width:${bloomProgress(seed)}%; background:linear-gradient(90deg,#6366f1,#818cf8)`"></div>
                  </div>
                </div>

                <!-- Bloom info -->
                <div class="mb-4">
                  <p class="seed-body text-xs text-slate-400 mb-1">
                    {{ getLifecycleStatus(seed) === 'bloomed' ? 'Bloomed' : 'Blooms' }}
                  </p>
                  <p class="seed-body text-sm text-slate-700">{{ formatDateTime(seed.bloom_at) }}</p>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2 pt-3 border-t border-slate-100">
                  <button v-if="getLifecycleStatus(seed) === 'bloomed'"
                          @click="viewMemory(seed.memory_id)"
                          class="flex-1 py-2 px-3 rounded-lg bg-indigo-50 text-indigo-600 hover:bg-indigo-100 text-xs font-semibold seed-body transition-colors flex items-center justify-center gap-1">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    View memory
                  </button>
                  <template v-else>
                    <button v-if="canEdit(seed)"
                            @click="editSeed(seed.id)"
                            class="flex-1 py-2 px-3 rounded-lg bg-slate-50 text-slate-600 hover:bg-slate-100 text-xs font-semibold seed-body transition-colors flex items-center justify-center gap-1">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                      Edit
                    </button>
                    <button v-if="canDelete(seed)"
                            @click="confirmDelete(seed)"
                            class="py-2 px-3 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 text-xs font-semibold seed-body transition-colors flex items-center justify-center gap-1">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                      Delete
                    </button>
                  </template>
                </div>
              </div>
            </article>
          </div>

          <!-- Bottom Pagination -->
          <div class="flex items-center justify-between flex-wrap gap-3 pt-4 border-t border-indigo-50">
            <p class="seed-body text-xs text-slate-500">Showing {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, mySeeds.length) }} of {{ mySeeds.length }} seeds</p>
            <div class="flex items-center gap-1">
              <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <template v-for="(p,i) in pageNumbers" :key="i">
                <span v-if="p==='...'" class="px-1 text-slate-400 seed-body text-sm">…</span>
                <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-indigo-600 text-white shadow-sm' : 'hover:bg-indigo-50 hover:text-indigo-600']">{{ p }}</button>
              </template>
              <button @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages" :class="['pag-btn', currentPage===totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>
        </template>
      </div>

      <!-- ── Delete Confirmation Modal ──────────────────────────────────── -->
      <Transition name="modal-fade">
        <div v-if="showDeleteModal"
             class="fixed inset-0 z-50 flex items-center justify-center p-4"
             style="background: rgba(15,23,42,0.85); backdrop-filter: blur(8px);"
             @click.self="cancelDelete">

          <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div class="h-1 w-full" style="background:linear-gradient(90deg,#ef4444,#dc2626);"></div>
            
            <div class="p-6 md:p-8">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div>
                  <h3 class="seed-display text-xl text-slate-900">Delete Seed?</h3>
                  <p class="seed-body text-sm text-slate-500 mt-0.5">This action cannot be undone</p>
                </div>
              </div>

              <p v-if="seedToDelete" class="seed-body text-sm text-slate-600 mb-6">
                Are you sure you want to delete <strong>"{{ seedToDelete.title }}"</strong>? 
                This seed will be permanently removed.
              </p>

              <div class="flex gap-3">
                <button @click="cancelDelete"
                        class="flex-1 py-2.5 px-4 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold seed-body transition-colors">
                  Cancel
                </button>
                <button @click="handleDelete"
                        :disabled="isDeleting"
                        class="flex-1 py-2.5 px-4 rounded-xl bg-red-600 text-white hover:bg-red-700 font-semibold seed-body transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                  {{ isDeleting ? 'Deleting…' : 'Delete' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>

    </div>
  </Sidebar>
</template>

<style scoped>
.my-seeds-page {
  background: linear-gradient(160deg, #f1f5f9 0%, #ffffff 50%, #f8fafc 100%);
}
.seed-display { font-family: 'Crimson Pro', Georgia, serif; font-weight: 500; }
.seed-body    { font-family: 'Inter', sans-serif; }
.seed-sub     { font-family: 'Inter', sans-serif; }

.pag-btn {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8125rem; font-family: 'Inter', sans-serif; font-weight: 600;
  color: #64748b; transition: all 0.15s ease;
}

.seed-card {
  box-shadow: 0 2px 16px rgba(99,102,241,0.06);
  animation: cardReveal 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.seed-card:hover {
  box-shadow: 0 12px 36px rgba(99,102,241,0.12), 0 4px 12px rgba(0,0,0,0.04);
}
@keyframes cardReveal {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Bloomed flower icon ── */
.bloom-bud-btn { cursor: pointer; transition: transform 0.3s ease; }
.bloom-bud-btn:hover { transform: scale(1.15) rotate(15deg); }
.bloom-flower-icon { filter: drop-shadow(0 0 8px rgba(129,140,248,0.6)); animation: flowerSpin 8s linear infinite; }
@keyframes flowerSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ── Ready pulse ── */
.ready-pulse { animation: readyPulse 2s ease-in-out infinite; }
@keyframes readyPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}
.ready-bud { filter: drop-shadow(0 0 6px rgba(192,132,252,0.5)); }

/* ── Dormant bud ── */
.dormant-bud { animation: budSway 4s ease-in-out infinite; transform-origin: 30px 78px; }
@keyframes budSway {
  0%,100% { transform: rotate(0deg); }
  30%     { transform: rotate(4deg); }
  70%     { transform: rotate(-4deg); }
}

/* ── Loading dots ── */
.loading-dot { animation: dotPulse 1.2s ease-in-out infinite; }
@keyframes dotPulse { 0%,100% { opacity: 0.3; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }

/* ── Modal transitions ── */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.3s cubic-bezier(0.22,1,0.36,1); }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(0.95); }
</style>