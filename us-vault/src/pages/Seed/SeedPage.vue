<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { useSeedStore } from '../../stores/seed'

const router = useRouter()
const seedStore = useSeedStore()
const CURRENT_USER_ID = 'user-001'

const seedDetails = ref(null)

// ── Mock API State ──────────────────────────────────────────────────────────
const allSeeds = computed(() => seedStore.seeds)

const seedSummary = computed(() => seedStore.summary)
const isLoading = computed(() => seedStore.isLoading)


// ── Lifecycle Computed ──────────────────────────────────────────────────────
const now = ref(new Date())
setInterval(() => { now.value = new Date() }, 30000) // Update every 30s

const growingSeeds = computed(() => 
  allSeeds.value.filter(s => s.status === 'scheduled' && new Date(s.bloom_at) > now.value)
)

const readySeeds = computed(() => 
  allSeeds.value.filter(s => s.status === 'scheduled' && new Date(s.bloom_at) <= now.value)
)

const bloomedSeeds = computed(() => 
  allSeeds.value.filter(s => s.status === 'bloomed')
)

// ── Pagination ────────────────────────────────────────────────────────────────
const perPage = ref(6)
const currentPage = ref(1)
const totalPages = computed(() => seedStore.totalPages)
const paginatedSeeds = computed(() => allSeeds.paginatedSeeds)
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
const goToPage = async (p) => {
  if (typeof p === 'number' && p >= 1 && p <= totalPages.value) {
    currentPage.value = p
    await seedStore.fetchSeeds(p, perPage.value)
  }
}

// ── Ready Bloom Modal ───────────────────────────────────────────────────────
const showReadyBloomModal = ref(false)
const currentReadySeedIndex = ref(0)
const isViewing = ref(false)
const hasBloomedCurrent = ref(false) // Track if current seed has been bloomed

const currentReadySeed = computed(() => readySeeds.value[currentReadySeedIndex.value] || null)

const openReadyBloom = async (seed) => {
  try {
    seedDetails.value = await seedStore.fetchSeed(seed.id)

    const idx = readySeeds.value.findIndex(s => s.id === seed.id)
    currentReadySeedIndex.value = idx >= 0 ? idx : 0

    hasBloomedCurrent.value = false
    showReadyBloomModal.value = true
  } catch (err) {
    console.error('Failed to load seed details')
  }
}

const closeReadyBloom = () => {
  showReadyBloomModal.value = false
  hasBloomedCurrent.value = false
}

const handleViewSeed = async () => {
  if (!currentReadySeed.value || isViewing.value) return

  isViewing.value = true
  try {
    const res = await seedStore.bloomSeed(currentReadySeed.value.id)

    hasBloomedCurrent.value = true

    // Refresh everything after bloom
    await Promise.all([
      seedStore.fetchAllSeeds(currentPage.value, perPage.value),
      seedStore.fetchActiveSeeds(),
      seedStore.fetchSummary()
    ])
  } catch (err) {
    alert(err?.response?.data?.detail || 'Failed to bloom seed')
  } finally {
    isViewing.value = false
  }
}

const nextReadySeed = () => {
  if (currentReadySeedIndex.value < readySeeds.value.length - 1) {
    currentReadySeedIndex.value++
    hasBloomedCurrent.value = false // Reset for next seed
  }
}

const prevReadySeed = () => {
  if (currentReadySeedIndex.value > 0) {
    currentReadySeedIndex.value--
    hasBloomedCurrent.value = false // Reset for previous seed
  }
}

// ── Navigate to Memory ──────────────────────────────────────────────────────
const viewMemory = (memoryId) => {
  if (memoryId) {
    router.push(`/memories/${memoryId}`)
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const truncate = (text, max = 100) => !text ? '' : text.length > max ? text.slice(0, max) + '…' : text
const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const isOwn = (seed) => seed.created_by === CURRENT_USER_ID

const getLifecycleStatus = (seed) => {
  if (seed.status === 'bloomed') return 'bloomed'
  if (seed.status === 'scheduled' && new Date(seed.bloom_at) <= now.value) return 'ready'
  return 'growing'
}

const timeUntilBloom = (bloomAt) => {
  const diff = new Date(bloomAt) - now.value
  if (diff <= 0) return 'Ready to bloom'
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

// ── Init ──────────────────────────────────────────────────────────────────────
onMounted(async () => {
  isLoading.value = true
  try {
    await Promise.all([
      seedStore.fetchAllSeeds(currentPage.value, perPage.value),
      seedStore.fetchActiveSeeds(),
      seedStore.fetchSummary()
    ])
  } catch (error) {
    console.error('Failed to load seeds:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <InactivityOverlay>
    <Sidebar>
      <div class="seeds-page min-h-screen relative overflow-x-hidden">
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
              <p class="seed-body text-sm text-indigo-400 tracking-wide">Loading seeds…</p>
            </div>
          </div>

          <template v-else>
            <!-- Header -->
            <div class="mb-8 md:mb-10">
              <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
                <div>
                  <p class="seed-sub text-xs text-indigo-500 uppercase tracking-widest mb-1">Shared Vault</p>
                  <h1 class="seed-display text-4xl md:text-5xl text-slate-900">Seeds</h1>
                  <div class="flex flex-wrap items-center gap-3 mt-2">
                    <p class="seed-body text-sm text-slate-500">{{ seedSummary.total }} seeds planted</p>
                    <span v-if="seedSummary.ready > 0"
                          class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body bg-indigo-600 text-white animate-pulse-soft cursor-pointer hover:bg-indigo-700 transition-colors"
                          @click="readySeeds.length > 0 && openReadyBloom(readySeeds[0])">
                      <span class="w-1.5 h-1.5 rounded-full bg-pink-300"></span>
                      {{ seedSummary.ready }} ready to bloom
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
              <p class="seed-body text-xs text-slate-500">Page {{ currentPage }} of {{ totalPages }} · {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allSeeds.length) }} of {{ allSeeds.length }}</p>
              <div class="flex items-center gap-1">
                <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                </button>
                <div v-for="(p,i) in pageNumbers" :key="i">
                  <span v-if="p==='...'" class="px-1 text-slate-400 seed-body text-sm">…</span>
                  <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-indigo-600 text-white shadow-sm' : 'hover:bg-indigo-50 hover:text-indigo-600']">{{ p }}</button>
                </div>
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
                  <button v-else-if="getLifecycleStatus(seed) === 'ready'"
                          @click="openReadyBloom(seed)"
                          class="ready-pulse"
                          title="Ready to bloom!">
                    <svg width="32" height="40" viewBox="0 0 60 80" class="ready-bud">
                      <ellipse cx="30" cy="36" rx="16" ry="26" fill="#c084fc" opacity="0.8"/>
                      <ellipse cx="30" cy="24" rx="10" ry="16" fill="#a855f7" opacity="0.7"/>
                      <line x1="30" y1="62" x2="30" y2="78" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                  </button>
                  
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
                  <!-- Author + status -->
                  <div class="flex items-center gap-2 mb-3 flex-wrap">
                    <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body border',
                                  isOwn(seed) ? 'bg-indigo-50 text-indigo-600 border-indigo-100' : 'bg-pink-50 text-pink-600 border-pink-100']">
                      <span :class="['w-1.5 h-1.5 rounded-full', isOwn(seed) ? 'bg-indigo-400' : 'bg-pink-400']"></span>
                      {{ isOwn(seed) ? 'You' : 'Partner' }}
                    </span>
                    <span :class="['inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs seed-body font-semibold',
                                  getLifecycleStatus(seed) === 'bloomed' ? 'bg-pink-100 text-pink-700' 
                                  : getLifecycleStatus(seed) === 'ready' ? 'bg-purple-100 text-purple-700'
                                  : 'bg-slate-100 text-slate-600']">
                      {{ getLifecycleStatus(seed) === 'bloomed' ? '✦ Bloomed' 
                        : getLifecycleStatus(seed) === 'ready' ? '◉ Ready' 
                        : '◌ Growing' }}
                    </span>
                  </div>

                  <h2 class="seed-display text-lg text-slate-900 leading-snug mb-2 line-clamp-2">{{ seed.title }}</h2>
                  
                  <!-- Content display logic -->
                  <p v-if="getLifecycleStatus(seed) === 'bloomed'" 
                    class="seed-body text-sm text-slate-600 leading-relaxed mb-4">
                    {{ truncate(seed.content, 90) }}
                  </p>
                  <p v-else-if="getLifecycleStatus(seed) === 'ready'" 
                    class="seed-body text-sm text-slate-400 italic leading-relaxed mb-4">
                    Ready to bloom — open to reveal
                  </p>
                  <p v-else 
                    class="seed-body text-sm text-slate-400 italic leading-relaxed mb-4">
                    Surprise for later…
                  </p>

                  <!-- Progress bar (only for growing) -->
                  <div v-if="getLifecycleStatus(seed) === 'growing'" class="mb-3">
                    <div class="flex justify-between items-center mb-1">
                      <span class="seed-body text-xs text-slate-400">Growing</span>
                      <span class="seed-body text-xs font-semibold text-indigo-600">{{ timeUntilBloom(seed.bloom_at) }}</span>
                    </div>
                    <div class="w-full h-1.5 bg-indigo-50 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-500" 
                          :style="`width:${bloomProgress(seed)}%; background:linear-gradient(90deg,#6366f1,#818cf8)`"></div>
                    </div>
                  </div>

                  <div class="flex items-center justify-between">
                    <span class="seed-body text-xs text-slate-400">
                      {{ getLifecycleStatus(seed) === 'bloomed' ? 'Bloomed' : 'Blooms' }} {{ formatDate(seed.bloom_at) }}
                    </span>
                    <div>
                      <button v-if="getLifecycleStatus(seed) === 'bloomed'"
                              @click="viewMemory(seed.memory_id)"
                              class="seed-body text-xs text-indigo-600 hover:text-indigo-800 font-semibold flex items-center gap-1 transition-colors">
                        View memory
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                      </button>
                      <button v-else-if="getLifecycleStatus(seed) === 'ready'"
                              @click="openReadyBloom(seed)"
                              class="seed-body text-xs text-purple-600 hover:text-purple-800 font-semibold flex items-center gap-1 transition-colors">
                        Open bloom
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                      </button>
                    </div>
                  </div>
                </div>
              </article>
            </div>

            <!-- Bottom Pagination -->
            <div class="flex items-center justify-between flex-wrap gap-3 pt-4 border-t border-indigo-50">
              <p class="seed-body text-xs text-slate-500">Showing {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allSeeds.length) }} of {{ allSeeds.length }} seeds</p>
              <div class="flex items-center gap-1">
                <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                </button>
                <div v-for="(p,i) in pageNumbers" :key="i">
                  <span v-if="p==='...'" class="px-1 text-slate-400 seed-body text-sm">…</span>
                  <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-indigo-600 text-white shadow-sm' : 'hover:bg-indigo-50 hover:text-indigo-600']">{{ p }}</button>
                </div>
                <button @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages" :class="['pag-btn', currentPage===totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-indigo-50 hover:text-indigo-600']">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                </button>
              </div>
            </div>
          </template>
        </div>

        <!-- ── Ready Bloom Modal ──────────────────────────────────────────── -->
        <Transition name="bloom-modal">
          <div v-if="showReadyBloomModal && currentReadySeed"
              class="fixed inset-0 z-50 flex items-center justify-center p-4"
              style="background: rgba(15,23,42,0.94); backdrop-filter: blur(12px);"
              @click.self="closeReadyBloom">

            <!-- Close -->
            <button @click="closeReadyBloom"
                    class="absolute top-4 md:top-5 right-4 md:right-5 z-20 w-10 h-10 rounded-full border border-indigo-600 bg-indigo-900/60 flex items-center justify-center text-indigo-300 hover:text-white hover:bg-indigo-800 transition">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <!-- Counter -->
            <div class="absolute top-4 md:top-5 left-1/2 -translate-x-1/2 seed-body text-xs text-indigo-400 tracking-widest uppercase">
              Bloom {{ currentReadySeedIndex + 1 }} of {{ readySeeds.length }}
            </div>

            <div class="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div class="bloom-content-card relative rounded-2xl md:rounded-3xl overflow-hidden"
                  style="background: linear-gradient(145deg,#1e293b,#334155); box-shadow: 0 20px 60px rgba(99,102,241,0.3);">

                <!-- Top gradient bar -->
                <div class="h-1 w-full" style="background:linear-gradient(90deg,#6366f1,#818cf8,#c084fc);"></div>

                <!-- Content -->
                <div class="p-6 md:p-8">
                  <!-- Author -->
                  <div class="flex items-center gap-2 mb-4">
                    <span :class="['inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold seed-body',
                                  currentReadySeed.created_by === CURRENT_USER_ID ? 'bg-indigo-800 text-indigo-200' : 'bg-pink-900/60 text-pink-300']">
                      <span class="w-1.5 h-1.5 rounded-full bg-pink-400 animate-pulse"></span>
                      {{ currentReadySeed.created_by === CURRENT_USER_ID ? 'From You' : 'From Your Partner' }}
                    </span>
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold seed-body bg-purple-900/60 text-purple-300">
                      <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                      Ready to bloom
                    </span>
                  </div>

                  <h2 class="seed-display text-2xl md:text-3xl text-white leading-tight mb-6">{{ currentReadySeed.title }}</h2>

                  <!-- Before Bloom: Show CTA -->
                  <div v-if="!hasBloomedCurrent" class="text-center py-8 md:py-12">
                    <div class="mb-6">
                      <svg width="80" height="100" viewBox="0 0 60 80" class="mx-auto ready-bud-large">
                        <ellipse cx="30" cy="36" rx="18" ry="30" fill="#c084fc" opacity="0.8"/>
                        <ellipse cx="30" cy="24" rx="12" ry="20" fill="#a855f7" opacity="0.7"/>
                        <line x1="30" y1="66" x2="30" y2="78" stroke="#818cf8" stroke-width="3" stroke-linecap="round"/>
                      </svg>
                    </div>
                    <p class="seed-body text-indigo-200 mb-6 text-sm md:text-base">This seed is ready to bloom. Once you view it, it will transform into a memory.</p>
                    <button @click="handleViewSeed"
                            :disabled="isViewing"
                            class="px-8 py-3 rounded-xl bg-linear-to-r from-indigo-600 to-purple-600 text-white font-semibold seed-body hover:from-indigo-500 hover:to-purple-500 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed">
                      {{ isViewing ? 'Blooming…' : 'Bloom Now' }}
                    </button>
                  </div>

                  <!-- After Bloom: Show Content -->
                  <div v-else class="bloom-reveal">
                    <!-- Bloomed flower animation -->
                    <div class="flex justify-center mb-6">
                      <svg width="100" height="100" viewBox="0 0 100 100" class="bloom-flower-reveal">
                        <g transform="translate(50,50)">
                          <ellipse rx="11" ry="32" fill="#818cf8" opacity="0.85" transform="rotate(0)"/>
                          <ellipse rx="11" ry="32" fill="#6366f1" opacity="0.8" transform="rotate(45)"/>
                          <ellipse rx="11" ry="32" fill="#818cf8" opacity="0.85" transform="rotate(90)"/>
                          <ellipse rx="11" ry="32" fill="#6366f1" opacity="0.8" transform="rotate(135)"/>
                          <circle r="11" fill="#fbbf24"/>
                        </g>
                      </svg>
                    </div>

                    <!-- Content -->
                    <div class="space-y-4">
                      <p class="seed-body text-indigo-100 text-base md:text-lg leading-relaxed whitespace-pre-wrap">{{ seedDetails?.content }}</p>

                      <!-- Media -->
                      <div v-if="seedDetails?.media && seedDetails?.media.length > 0" class="grid grid-cols-1 gap-3 mt-6">
                        <div v-for="media in seedDetails?.media" :key="media.id" 
                            class="rounded-xl overflow-hidden border border-indigo-700/50">
                          <img v-if="media.file_type.startsWith('image/')" 
                              :src="media.file_url" 
                              class="w-full h-auto"
                              alt="Seed media" />
                          <video v-else
                                :src="media.file_url"
                                controls
                                class="w-full h-auto"></video>
                        </div>
                      </div>
                    </div>

                    <!-- View Memory CTA -->
                    <div class="mt-8 text-center">
                      <p class="seed-body text-indigo-300 text-sm mb-4">This seed has bloomed into a memory</p>
                      <button @click="viewMemory(currentReadySeed.memory_id || `mem-${currentReadySeed.id}`)"
                              class="px-6 py-2.5 rounded-xl bg-linear-to-r from-pink-600 to-rose-600 text-white font-semibold seed-body hover:from-pink-500 hover:to-rose-500 transition-all shadow-lg">
                        View in Memories
                      </button>
                    </div>
                  </div>

                  <!-- Nav -->
                  <div v-if="readySeeds.length > 1" class="flex items-center justify-between pt-6 border-t border-slate-700/50 gap-4 mt-6">
                    <button @click="prevReadySeed" :disabled="currentReadySeedIndex === 0"
                            :class="['flex items-center gap-2 px-4 py-2 rounded-xl text-sm seed-body font-semibold transition-all',
                                    currentReadySeedIndex === 0 ? 'opacity-30 cursor-not-allowed text-indigo-600' : 'text-indigo-300 hover:bg-indigo-800 hover:text-white']">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                      <span class="hidden sm:inline">Previous</span>
                    </button>
                    <span class="seed-body text-xs text-indigo-600 tracking-wide">{{ currentReadySeedIndex + 1 }} / {{ readySeeds.length }}</span>
                    <button @click="nextReadySeed" :disabled="currentReadySeedIndex === readySeeds.length - 1"
                            :class="['flex items-center gap-2 px-4 py-2 rounded-xl text-sm seed-body font-semibold transition-all',
                                    currentReadySeedIndex === readySeeds.length - 1 ? 'opacity-30 cursor-not-allowed text-indigo-600' : 'text-indigo-300 hover:bg-indigo-800 hover:text-white']">
                      <span class="hidden sm:inline">Next</span>
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
.seeds-page {
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
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── Bloomed flower icon ── */
.bloom-bud-btn { cursor: pointer; transition: transform 0.3s ease; }
.bloom-bud-btn:hover { transform: scale(1.15) rotate(15deg); }
.bloom-flower-icon { filter: drop-shadow(0 0 8px rgba(129,140,248,0.6)); animation: flowerSpin 8s linear infinite; }
@keyframes flowerSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ── Bloom reveal animation ── */
.bloom-reveal {
  animation: bloomFadeIn 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
@keyframes bloomFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.bloom-flower-reveal {
  filter: drop-shadow(0 0 16px rgba(129,140,248,0.8));
  animation: flowerBloom 1.2s cubic-bezier(0.22,1,0.36,1) both, flowerSpin 8s linear 1.2s infinite;
}
@keyframes flowerBloom {
  from { transform: scale(0.3) rotate(0deg); opacity: 0; }
  to { transform: scale(1) rotate(180deg); opacity: 1; }
}

/* ── Ready pulse ── */
.ready-pulse { cursor: pointer; animation: readyPulse 2s ease-in-out infinite; }
@keyframes readyPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
}
.ready-bud { filter: drop-shadow(0 0 6px rgba(192,132,252,0.5)); }

/* ── Ready bud large ── */
.ready-bud-large { 
  filter: drop-shadow(0 0 12px rgba(168,85,247,0.6)); 
  animation: budGlow 2.5s ease-in-out infinite;
}
@keyframes budGlow {
  0%, 100% { filter: drop-shadow(0 0 12px rgba(168,85,247,0.6)); }
  50% { filter: drop-shadow(0 0 20px rgba(192,132,252,0.8)); }
}

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

/* ── Pulse soft ── */
@keyframes pulseSoft {
  0%,100% { opacity: 1; }
  50%     { opacity: 0.7; }
}
.animate-pulse-soft { animation: pulseSoft 2.5s ease-in-out infinite; }

/* ── Modal transitions ── */
.bloom-modal-enter-active, .bloom-modal-leave-active { transition: all 0.4s cubic-bezier(0.22,1,0.36,1); }
.bloom-modal-enter-from, .bloom-modal-leave-to       { opacity: 0; }
</style>