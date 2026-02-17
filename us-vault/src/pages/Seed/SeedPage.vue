<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'

const router = useRouter()
const CURRENT_USER_ID = 'user-001'

// ── Mock Seeds Data ──────────────────────────────────────────────────────────
const allSeeds = ref([
  { id: 'seed-001', vault_id: 'v1', created_by: 'user-001', title: 'A Letter for Our First Year', content: 'There are things I want to tell you a year from now, when we\'ve grown into something neither of us can fully predict yet. I want you to read this and know that even before I knew how it would go, I was already sure about you.', bloom_at: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: false, media: [] },
  { id: 'seed-002', vault_id: 'v1', created_by: 'user-002', title: 'What I Noticed First', content: 'I\'ve been keeping this for a while. When the time comes, I hope you smile reading it.', bloom_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: false, media: [] },
  { id: 'seed-003', vault_id: 'v1', created_by: 'user-001', title: 'The Dream I Had About Us', content: 'I wrote this the morning after I had the most vivid dream. I want you to have it when the time is right.', bloom_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: true, media: [{ id: 'sm1', file_url: 'https://picsum.photos/seed/dream/800/500', file_type: 'image/jpeg' }] },
  { id: 'seed-004', vault_id: 'v1', created_by: 'user-002', title: 'Something I Never Said Out Loud', content: 'Words I\'ve been holding onto, waiting for the right moment. That moment is now.', bloom_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: true, media: [] },
  { id: 'seed-005', vault_id: 'v1', created_by: 'user-001', title: 'Midwinter Note', content: 'Planted this on the coldest day of the year. Wanted something warm waiting for you on the other side of winter.', bloom_at: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: false, media: [] },
  { id: 'seed-006', vault_id: 'v1', created_by: 'user-002', title: 'For a Rainy Day', content: 'This is for whenever you need it. I hope it finds you well, and I hope by then you remember this day fondly.', bloom_at: new Date(Date.now() + 21 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: false, media: [] },
  { id: 'seed-007', vault_id: 'v1', created_by: 'user-001', title: 'The Quiet Ones', content: 'Sometimes the best memories are the quiet ones. I\'ve been saving this for when we need a reminder.', bloom_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), created_at: new Date(Date.now() - 50 * 24 * 60 * 60 * 1000).toISOString(), is_seed: true, has_bloomed: true, media: [{ id: 'sm7', file_url: 'https://picsum.photos/seed/quiet/800/500', file_type: 'image/jpeg' }] },
])

// Active blooms (seeds that have bloomed)
const activeBlooms = computed(() => allSeeds.value.filter(s => s.has_bloomed))

// ── Pagination ────────────────────────────────────────────────────────────────
const perPage = ref(6)
const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(allSeeds.value.length / perPage.value))
const paginatedSeeds = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return allSeeds.value.slice(start, start + perPage.value)
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

// ── Bloom Modal ───────────────────────────────────────────────────────────────
const showBloomModal = ref(false)
const bloomAnimationDone = ref(false)
const currentBloomIndex = ref(0)
const currentBloom = computed(() => activeBlooms.value[currentBloomIndex.value] || null)

const openBloom = (seed) => {
  const idx = activeBlooms.value.findIndex(b => b.id === seed.id)
  currentBloomIndex.value = idx >= 0 ? idx : 0
  bloomAnimationDone.value = false
  showBloomModal.value = true
  setTimeout(() => { bloomAnimationDone.value = true }, 3200)
}

const closeBloom = () => { showBloomModal.value = false; bloomAnimationDone.value = false }

const nextBloom = () => {
  if (currentBloomIndex.value < activeBlooms.value.length - 1) {
    currentBloomIndex.value++
    bloomAnimationDone.value = false
    setTimeout(() => { bloomAnimationDone.value = true }, 3200)
  }
}
const prevBloom = () => {
  if (currentBloomIndex.value > 0) {
    currentBloomIndex.value--
    bloomAnimationDone.value = false
    setTimeout(() => { bloomAnimationDone.value = true }, 3200)
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const truncate = (text, max = 100) => !text ? '' : text.length > max ? text.slice(0, max) + '…' : text
const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const isOwn = (seed) => seed.created_by === CURRENT_USER_ID
const timeUntilBloom = (bloomAt) => {
  const diff = new Date(bloomAt) - new Date()
  if (diff <= 0) return 'Bloomed'
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  if (days > 0) return `${days}d ${hours}h`
  return `${hours}h`
}
const bloomProgress = (seed) => {
  const created = new Date(seed.created_at)
  const bloom = new Date(seed.bloom_at)
  const now = new Date()
  const total = bloom - created
  const elapsed = now - created
  return Math.max(0, Math.min(100, (elapsed / total) * 100))
}
</script>

<template>
  <Sidebar>
    <div class="seeds-page min-h-screen relative overflow-x-hidden">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
      </component>

      <!-- Ambient BG -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
        <div class="absolute top-1/2 -left-20 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#f3e8ff 0%,transparent 70%);"></div>
        <div class="absolute bottom-0 right-1/4 w-64 h-64 rounded-full opacity-10" style="background: radial-gradient(circle,#fce7f3 0%,transparent 70%);"></div>
        <!-- Vine SVG left -->
        <svg class="absolute left-0 top-0 h-full w-20 opacity-[0.06]" viewBox="0 0 80 800" preserveAspectRatio="none" fill="none">
          <path d="M40 0 Q10 100 40 200 Q70 300 40 400 Q10 500 40 600 Q70 700 40 800" stroke="#7c3aed" stroke-width="2"/>
          <ellipse cx="22" cy="160" rx="18" ry="8" fill="#7c3aed" transform="rotate(-30 22 160)"/>
          <ellipse cx="58" cy="360" rx="18" ry="8" fill="#a855f7" transform="rotate(25 58 360)"/>
          <ellipse cx="22" cy="560" rx="16" ry="7" fill="#7c3aed" transform="rotate(-20 22 560)"/>
        </svg>
        <!-- Vine SVG right -->
        <svg class="absolute right-0 top-0 h-full w-20 opacity-[0.06]" viewBox="0 0 80 800" preserveAspectRatio="none" fill="none">
          <path d="M40 0 Q70 100 40 200 Q10 300 40 400 Q70 500 40 600 Q10 700 40 800" stroke="#7c3aed" stroke-width="2"/>
          <ellipse cx="58" cy="160" rx="18" ry="8" fill="#7c3aed" transform="rotate(30 58 160)"/>
          <ellipse cx="22" cy="360" rx="18" ry="8" fill="#a855f7" transform="rotate(-25 22 360)"/>
          <ellipse cx="58" cy="560" rx="16" ry="7" fill="#7c3aed" transform="rotate(20 58 560)"/>
        </svg>
      </div>

      <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        <!-- Header -->
        <div class="mb-10">
          <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
            <div>
              <p class="seed-sub text-xs text-purple-400 uppercase tracking-widest mb-1">Your Vault</p>
              <h1 class="seed-display text-5xl text-gray-900">Seeds</h1>
              <div class="flex items-center gap-4 mt-2">
                <p class="seed-body text-sm text-gray-400">{{ allSeeds.length }} seeds planted</p>
                <span v-if="activeBlooms.length > 0"
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body bg-purple-700 text-white animate-pulse-soft">
                  <span class="w-1.5 h-1.5 rounded-full bg-fuchsia-300"></span>
                  {{ activeBlooms.length }} bloom{{ activeBlooms.length !== 1 ? 's' : '' }} ready
                </span>
              </div>
            </div>
            <!-- Per page -->
            <div class="flex items-center gap-3 bg-white rounded-xl px-4 py-2.5 border border-purple-100 shadow-sm self-start sm:self-auto">
              <span class="seed-body text-xs text-gray-400 uppercase tracking-wide">Show</span>
              <div class="flex gap-1">
                <button v-for="n in [5, 6, 8, 10]" :key="n" @click="perPage = n"
                        :class="['px-3 py-1 rounded-lg text-xs font-semibold transition-all seed-body',
                                 perPage === n ? 'bg-purple-700 text-white shadow-sm' : 'text-gray-500 hover:bg-purple-50']">{{ n }}</button>
              </div>
            </div>
          </div>
          <!-- Divider -->
          <div class="flex items-center gap-3 mt-6">
            <div class="h-px flex-1" style="background: linear-gradient(90deg,#7c3aed,#c084fc,transparent);"></div>
            <svg width="12" height="12" viewBox="0 0 60 60" fill="#a855f7"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
            <div class="h-px w-8" style="background:#c084fc;"></div>
          </div>
        </div>

        <!-- Top Pagination -->
        <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
          <p class="seed-body text-xs text-gray-400">Page {{ currentPage }} of {{ totalPages }} · {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allSeeds.length) }} of {{ allSeeds.length }}</p>
          <div class="flex items-center gap-1">
            <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-purple-50 hover:text-purple-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <template v-for="(p,i) in pageNumbers" :key="i">
              <span v-if="p==='...'" class="px-1 text-gray-400 seed-body text-sm">…</span>
              <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-purple-700 text-white shadow-sm' : 'hover:bg-purple-50 hover:text-purple-600']">{{ p }}</button>
            </template>
            <button @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages" :class="['pag-btn', currentPage===totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-purple-50 hover:text-purple-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>

        <!-- Seeds Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-8">
          <article v-for="(seed, idx) in paginatedSeeds" :key="seed.id"
                   class="seed-card group relative bg-white rounded-2xl overflow-hidden border border-purple-50 transition-all duration-300 hover:-translate-y-1.5"
                   :style="`animation-delay:${idx*60}ms`">

            <!-- Top strip -->
            <div class="h-0.5 w-full" :style="seed.has_bloomed ? 'background:linear-gradient(90deg,#7c3aed,#c084fc,#ec4899)' : 'background:linear-gradient(90deg,#7c3aed,#a855f7)'"></div>

            <!-- Bloom trigger (right side floating bud) -->
            <button v-if="seed.has_bloomed"
                    @click="openBloom(seed)"
                    class="absolute top-3 right-3 z-10 bloom-bud-btn"
                    title="This seed has bloomed — click to open">
              <!-- Animated bloomed flower -->
              <svg width="36" height="36" viewBox="0 0 100 100" class="bloom-flower-icon">
                <g transform="translate(50,50)">
                  <ellipse rx="11" ry="32" fill="#c084fc" opacity="0.85" transform="rotate(0)"/>
                  <ellipse rx="11" ry="32" fill="#a855f7" opacity="0.8" transform="rotate(45)"/>
                  <ellipse rx="11" ry="32" fill="#c084fc" opacity="0.85" transform="rotate(90)"/>
                  <ellipse rx="11" ry="32" fill="#a855f7" opacity="0.8" transform="rotate(135)"/>
                  <circle r="11" fill="#fbbf24"/>
                </g>
              </svg>
            </button>

            <!-- Dormant bud (not bloomed yet) -->
            <div v-else class="absolute top-3 right-3 z-10 w-9 h-9 flex items-center justify-center">
              <svg width="28" height="36" viewBox="0 0 60 80" class="dormant-bud">
                <ellipse cx="30" cy="38" rx="14" ry="22" fill="#ddd6fe" opacity="0.7"/>
                <ellipse cx="30" cy="26" rx="8" ry="12" fill="#c4b5fd" opacity="0.6"/>
                <line x1="30" y1="60" x2="30" y2="78" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
            </div>

            <div class="p-5 pr-14">
              <!-- Author + status -->
              <div class="flex items-center gap-2 mb-3">
                <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold seed-body border',
                               isOwn(seed) ? 'bg-purple-50 text-purple-600 border-purple-100' : 'bg-fuchsia-50 text-fuchsia-600 border-fuchsia-100']">
                  <span :class="['w-1.5 h-1.5 rounded-full', isOwn(seed) ? 'bg-purple-400' : 'bg-fuchsia-400']"></span>
                  {{ isOwn(seed) ? 'You' : 'Partner' }}
                </span>
                <span :class="['inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs seed-body font-semibold',
                               seed.has_bloomed ? 'bg-fuchsia-100 text-fuchsia-700' : 'bg-gray-100 text-gray-500']">
                  {{ seed.has_bloomed ? '✦ Bloomed' : '◌ Dormant' }}
                </span>
              </div>

              <h2 class="seed-display text-lg text-gray-900 leading-snug mb-2 line-clamp-2">{{ seed.title }}</h2>
              <p class="seed-body text-sm text-gray-500 leading-relaxed mb-4">{{ truncate(seed.content, 90) }}</p>

              <!-- Progress bar (only for non-bloomed) -->
              <div v-if="!seed.has_bloomed" class="mb-3">
                <div class="flex justify-between items-center mb-1">
                  <span class="seed-body text-xs text-gray-400">Growing</span>
                  <span class="seed-body text-xs font-semibold text-purple-600">Blooms in {{ timeUntilBloom(seed.bloom_at) }}</span>
                </div>
                <div class="w-full h-1.5 bg-purple-50 rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-500" :style="`width:${bloomProgress(seed)}%; background:linear-gradient(90deg,#7c3aed,#c084fc)`"></div>
                </div>
              </div>

              <div class="flex items-center justify-between">
                <span class="seed-body text-xs text-gray-400">Blooms {{ formatDate(seed.bloom_at) }}</span>
                <div v-if="seed.has_bloomed">
                  <button @click="openBloom(seed)"
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
        <div class="flex items-center justify-between flex-wrap gap-3 pt-4 border-t border-purple-50">
          <p class="seed-body text-xs text-gray-400">Showing {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allSeeds.length) }} of {{ allSeeds.length }} seeds</p>
          <div class="flex items-center gap-1">
            <button @click="goToPage(currentPage-1)" :disabled="currentPage===1" :class="['pag-btn', currentPage===1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-purple-50 hover:text-purple-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <template v-for="(p,i) in pageNumbers" :key="i">
              <span v-if="p==='...'" class="px-1 text-gray-400 seed-body text-sm">…</span>
              <button v-else @click="goToPage(p)" :class="['pag-btn', currentPage===p ? 'bg-purple-700 text-white shadow-sm' : 'hover:bg-purple-50 hover:text-purple-600']">{{ p }}</button>
            </template>
            <button @click="goToPage(currentPage+1)" :disabled="currentPage===totalPages" :class="['pag-btn', currentPage===totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-purple-50 hover:text-purple-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- ── Bloom Modal ──────────────────────────────────────────── -->
      <Transition name="bloom-modal">
        <div v-if="showBloomModal"
             class="fixed inset-0 z-50 flex items-center justify-center"
             style="background: rgba(10,5,25,0.92); backdrop-filter: blur(12px);"
             @click.self="closeBloom">

          <!-- Close -->
          <button @click="closeBloom"
                  class="absolute top-5 right-5 z-20 w-10 h-10 rounded-full border border-purple-700 bg-purple-900/60 flex items-center justify-center text-purple-300 hover:text-white hover:bg-purple-800 transition">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>

          <!-- Bloom counter -->
          <div class="absolute top-5 left-1/2 -translate-x-1/2 seed-body text-xs text-purple-400 tracking-widest uppercase">
            Bloom {{ currentBloomIndex + 1 }} of {{ activeBlooms.length }}
          </div>

          <div class="relative w-full max-w-5xl mx-4 flex flex-col lg:flex-row items-center gap-0 min-h-[70vh]">

            <!-- LEFT: Flower animation -->
            <div class="hidden lg:flex flex-[0_0_40%] items-center justify-center relative h-full min-h-[500px]">
              <div class="flower-animation-container">
                <!-- Animated SVG Flower built purely in SVG/CSS -->
                <svg viewBox="0 0 300 420" width="280" height="420" class="bloom-svg" :class="{ 'bloom-svg--ready': !bloomAnimationDone }">
                  <!-- Stem -->
                  <line x1="150" y1="420" x2="150" y2="240" stroke="#7c3aed" stroke-width="4" stroke-linecap="round" class="bloom-stem"/>
                  <!-- Left leaf -->
                  <ellipse cx="118" cy="320" rx="28" ry="12" fill="#a855f7" opacity="0.6" transform="rotate(-35 118 320)" class="bloom-leaf bloom-leaf-1"/>
                  <!-- Right leaf -->
                  <ellipse cx="182" cy="290" rx="28" ry="12" fill="#8b5cf6" opacity="0.6" transform="rotate(35 182 290)" class="bloom-leaf bloom-leaf-2"/>
                  <!-- Petal group (8 petals) -->
                  <g transform="translate(150,200)" class="bloom-petals">
                    <ellipse rx="14" ry="52" fill="#c084fc" opacity="0.85" transform="rotate(0)   translate(0,-18)" class="petal p0"/>
                    <ellipse rx="14" ry="52" fill="#a855f7" opacity="0.80" transform="rotate(45)  translate(0,-18)" class="petal p1"/>
                    <ellipse rx="14" ry="52" fill="#c084fc" opacity="0.85" transform="rotate(90)  translate(0,-18)" class="petal p2"/>
                    <ellipse rx="14" ry="52" fill="#a855f7" opacity="0.80" transform="rotate(135) translate(0,-18)" class="petal p3"/>
                    <ellipse rx="14" ry="52" fill="#d8b4fe" opacity="0.85" transform="rotate(180) translate(0,-18)" class="petal p4"/>
                    <ellipse rx="14" ry="52" fill="#a855f7" opacity="0.80" transform="rotate(225) translate(0,-18)" class="petal p5"/>
                    <ellipse rx="14" ry="52" fill="#c084fc" opacity="0.85" transform="rotate(270) translate(0,-18)" class="petal p6"/>
                    <ellipse rx="14" ry="52" fill="#a855f7" opacity="0.80" transform="rotate(315) translate(0,-18)" class="petal p7"/>
                    <!-- Center -->
                    <circle r="18" fill="#fbbf24" class="bloom-center"/>
                    <circle r="10" fill="#fde68a" class="bloom-center-inner"/>
                  </g>
                  <!-- Sparkle dots -->
                  <circle cx="80"  cy="160" r="3" fill="#e879f9" class="sparkle sp1"/>
                  <circle cx="220" cy="140" r="2.5" fill="#c084fc" class="sparkle sp2"/>
                  <circle cx="60"  cy="230" r="2" fill="#fbbf24" class="sparkle sp3"/>
                  <circle cx="240" cy="200" r="3" fill="#e879f9" class="sparkle sp4"/>
                  <circle cx="150" cy="120" r="2" fill="#c084fc" class="sparkle sp5"/>
                </svg>

                <!-- Loading state shown during animation -->
                <div v-if="!bloomAnimationDone" class="absolute inset-0 flex flex-col items-center justify-end pb-8">
                  <div class="flex gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-purple-400 loading-dot" style="animation-delay:0s"></span>
                    <span class="w-1.5 h-1.5 rounded-full bg-purple-400 loading-dot" style="animation-delay:0.2s"></span>
                    <span class="w-1.5 h-1.5 rounded-full bg-purple-400 loading-dot" style="animation-delay:0.4s"></span>
                  </div>
                  <p class="seed-body text-xs text-purple-400 tracking-widest uppercase mt-2">Blooming…</p>
                </div>
              </div>
            </div>

            <!-- RIGHT: Bloom Content -->
            <Transition name="content-reveal">
              <div v-if="bloomAnimationDone && currentBloom"
                   class="flex-1 relative">
                <div class="bloom-content-card relative rounded-3xl overflow-hidden"
                     style="background: linear-gradient(145deg,#1e1530,#2d1b4e); box-shadow: 0 30px 80px rgba(124,58,237,0.3);">

                  <!-- Top gradient bar -->
                  <div class="h-1 w-full" style="background:linear-gradient(90deg,#7c3aed,#c084fc,#ec4899);"></div>

                  <!-- Media -->
                  <div v-if="currentBloom.media.length > 0" class="relative overflow-hidden" style="height:220px;">
                    <img v-if="currentBloom.media[0].file_type.startsWith('image/')"
                         :src="currentBloom.media[0].file_url" :alt="currentBloom.title"
                         class="w-full h-full object-cover"/>
                    <!-- Date stamp -->
                    <div class="absolute bottom-3 right-3 px-2 py-1 rounded-lg bg-black/50 backdrop-blur-sm">
                      <span class="text-white font-mono text-xs">{{ formatDate(currentBloom.bloom_at) }}</span>
                    </div>
                    <!-- Bloom badge -->
                    <div class="absolute top-3 left-3 flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-700/80 backdrop-blur-sm">
                      <svg width="8" height="8" viewBox="0 0 60 60" fill="#fbbf24"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
                      <span class="text-white text-xs seed-body font-semibold">Bloomed</span>
                    </div>
                  </div>

                  <!-- Content -->
                  <div class="p-7">
                    <!-- Author -->
                    <div class="flex items-center gap-2 mb-4">
                      <span :class="['inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold seed-body',
                                     currentBloom.created_by === CURRENT_USER_ID ? 'bg-purple-800 text-purple-200' : 'bg-fuchsia-900/60 text-fuchsia-300']">
                        <span class="w-1.5 h-1.5 rounded-full bg-fuchsia-400 animate-pulse"></span>
                        {{ currentBloom.created_by === CURRENT_USER_ID ? 'From You' : 'From Your Partner' }}
                      </span>
                    </div>

                    <h2 class="seed-display text-3xl text-white leading-tight mb-4">{{ currentBloom.title }}</h2>

                    <div class="text-4xl text-purple-800 seed-display leading-none mb-2 select-none">"</div>
                    <p class="seed-body text-purple-200 leading-loose text-base">{{ currentBloom.content }}</p>
                    <div class="text-4xl text-purple-800 seed-display text-right mt-2 select-none">"</div>

                    <!-- Planted date -->
                    <div class="mt-5 pt-5 border-t border-purple-800/50 flex items-center justify-between">
                      <div>
                        <p class="seed-body text-xs text-purple-500 uppercase tracking-widest mb-1">Planted</p>
                        <p class="seed-body text-sm text-purple-300">{{ formatDate(currentBloom.created_at) }}</p>
                      </div>
                      <div class="text-right">
                        <p class="seed-body text-xs text-purple-500 uppercase tracking-widest mb-1">Bloomed</p>
                        <p class="seed-body text-sm text-purple-300">{{ formatDate(currentBloom.bloom_at) }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Prev / Next bloom nav -->
                  <div class="flex items-center justify-between px-7 pb-6 gap-4">
                    <button @click="prevBloom" :disabled="currentBloomIndex === 0"
                            :class="['flex items-center gap-2 px-4 py-2 rounded-xl text-sm seed-body font-semibold transition-all',
                                     currentBloomIndex === 0 ? 'opacity-30 cursor-not-allowed text-purple-600' : 'text-purple-300 hover:bg-purple-800 hover:text-white']">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                      Previous
                    </button>
                    <span class="seed-body text-xs text-purple-600 tracking-wide">{{ currentBloomIndex + 1 }} / {{ activeBlooms.length }}</span>
                    <button @click="nextBloom" :disabled="currentBloomIndex === activeBlooms.length - 1"
                            :class="['flex items-center gap-2 px-4 py-2 rounded-xl text-sm seed-body font-semibold transition-all',
                                     currentBloomIndex === activeBlooms.length - 1 ? 'opacity-30 cursor-not-allowed text-purple-600' : 'text-purple-300 hover:bg-purple-800 hover:text-white']">
                      Next
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                    </button>
                  </div>
                </div>
              </div>
            </Transition>

            <!-- Mobile bloom content -->
            <Transition name="content-reveal">
              <div v-if="bloomAnimationDone && currentBloom" class="lg:hidden w-full">
                <div class="bloom-content-card rounded-3xl overflow-hidden"
                     style="background:linear-gradient(145deg,#1e1530,#2d1b4e); box-shadow:0 20px 60px rgba(124,58,237,0.3);">
                  <div class="h-1 w-full" style="background:linear-gradient(90deg,#7c3aed,#c084fc,#ec4899);"></div>
                  <div v-if="currentBloom.media.length > 0" class="relative overflow-hidden" style="height:180px;">
                    <img v-if="currentBloom.media[0].file_type.startsWith('image/')"
                         :src="currentBloom.media[0].file_url" :alt="currentBloom.title" class="w-full h-full object-cover"/>
                  </div>
                  <div class="p-5">
                    <span :class="['inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold seed-body mb-3',
                                   currentBloom.created_by === CURRENT_USER_ID ? 'bg-purple-800 text-purple-200' : 'bg-fuchsia-900/60 text-fuchsia-300']">
                      <span class="w-1.5 h-1.5 rounded-full bg-fuchsia-400 animate-pulse"></span>
                      {{ currentBloom.created_by === CURRENT_USER_ID ? 'From You' : 'From Your Partner' }}
                    </span>
                    <h2 class="seed-display text-2xl text-white mb-3">{{ currentBloom.title }}</h2>
                    <p class="seed-body text-purple-200 text-sm leading-loose">{{ currentBloom.content }}</p>
                    <div class="flex items-center justify-between mt-4 pt-4 border-t border-purple-800/40">
                      <button @click="prevBloom" :disabled="currentBloomIndex===0"
                              :class="['text-sm seed-body flex items-center gap-1', currentBloomIndex===0 ? 'opacity-30 text-purple-600' : 'text-purple-300']">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                        Prev
                      </button>
                      <span class="seed-body text-xs text-purple-600">{{ currentBloomIndex+1 }} / {{ activeBlooms.length }}</span>
                      <button @click="nextBloom" :disabled="currentBloomIndex===activeBlooms.length-1"
                              :class="['text-sm seed-body flex items-center gap-1', currentBloomIndex===activeBlooms.length-1 ? 'opacity-30 text-purple-600' : 'text-purple-300']">
                        Next
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </Transition>

          </div>
        </div>
      </Transition>

    </div>
  </Sidebar>
</template>

<style scoped>
.seeds-page {
  background: linear-gradient(160deg, #faf5ff 0%, #ffffff 50%, #f5f3ff 100%);
}
.seed-display { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; }
.seed-body    { font-family: 'DM Sans', sans-serif; }
.seed-sub     { font-family: 'DM Sans', sans-serif; }

.pag-btn {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8125rem; font-family: 'DM Sans', sans-serif; font-weight: 600;
  color: #848b9a; transition: all 0.15s ease;
}

.seed-card {
  box-shadow: 0 2px 16px rgba(124,58,237,0.07);
  animation: cardReveal 0.5s cubic-bezier(0.22,1,0.36,1) both;
}
.seed-card:hover {
  box-shadow: 0 12px 36px rgba(124,58,237,0.14), 0 4px 12px rgba(0,0,0,0.04);
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

/* ── Bloomed flower icon on card ── */
.bloom-bud-btn { cursor: pointer; transition: transform 0.3s ease; }
.bloom-bud-btn:hover { transform: scale(1.15) rotate(15deg); }
.bloom-flower-icon { filter: drop-shadow(0 0 8px rgba(192,132,252,0.6)); animation: flowerSpin 8s linear infinite; }
@keyframes flowerSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.dormant-bud { animation: budSway 4s ease-in-out infinite; transform-origin: 30px 78px; }
@keyframes budSway {
  0%,100% { transform: rotate(0deg); }
  30%     { transform: rotate(4deg); }
  70%     { transform: rotate(-4deg); }
}

/* ── Bloom SVG animation ── */
.bloom-svg .bloom-stem {
  stroke-dasharray: 200; stroke-dashoffset: 200;
  animation: drawStem 1s ease-out 0.2s forwards;
}
@keyframes drawStem { to { stroke-dashoffset: 0; } }

.bloom-svg .bloom-leaf   { transform-box: fill-box; transform-origin: center; scale: 0; animation: growLeaf 0.6s ease-out forwards; }
.bloom-svg .bloom-leaf-1 { animation-delay: 0.8s; }
.bloom-svg .bloom-leaf-2 { animation-delay: 1.0s; }
@keyframes growLeaf { from { scale: 0; } to { scale: 1; } }

.bloom-svg .petal { transform-box: fill-box; transform-origin: center; scale: 0; animation: bloomPetal 0.5s cubic-bezier(0.34,1.56,0.64,1) forwards; }
.bloom-svg .p0 { animation-delay: 1.3s; }
.bloom-svg .p1 { animation-delay: 1.45s; }
.bloom-svg .p2 { animation-delay: 1.6s; }
.bloom-svg .p3 { animation-delay: 1.75s; }
.bloom-svg .p4 { animation-delay: 1.9s; }
.bloom-svg .p5 { animation-delay: 2.05s; }
.bloom-svg .p6 { animation-delay: 2.2s; }
.bloom-svg .p7 { animation-delay: 2.35s; }
@keyframes bloomPetal { from { scale: 0; opacity: 0; } to { scale: 1; opacity: 1; } }

.bloom-svg .bloom-center       { transform-box: fill-box; transform-origin: center; scale: 0; animation: popCenter 0.4s cubic-bezier(0.34,1.56,0.64,1) 2.5s forwards; }
.bloom-svg .bloom-center-inner { transform-box: fill-box; transform-origin: center; scale: 0; animation: popCenter 0.4s cubic-bezier(0.34,1.56,0.64,1) 2.65s forwards; }
@keyframes popCenter { from { scale: 0; } to { scale: 1; } }

.bloom-svg .sparkle { scale: 0; opacity: 0; animation: sparklePop 0.5s ease-out forwards; }
.bloom-svg .sp1 { animation-delay: 2.8s; }
.bloom-svg .sp2 { animation-delay: 2.9s; }
.bloom-svg .sp3 { animation-delay: 3.0s; }
.bloom-svg .sp4 { animation-delay: 3.1s; }
.bloom-svg .sp5 { animation-delay: 3.2s; }
@keyframes sparklePop { from { scale: 0; opacity: 0; } to { scale: 1; opacity: 1; } }

/* After bloom is done, gently sway the whole flower */
.bloom-svg .bloom-petals { animation: gentleSway 5s ease-in-out 3.5s infinite; transform-origin: 50% 80%; }
@keyframes gentleSway {
  0%,100% { transform: rotate(0deg); }
  25%     { transform: rotate(3deg); }
  75%     { transform: rotate(-3deg); }
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

.content-reveal-enter-active { transition: all 0.6s cubic-bezier(0.22,1,0.36,1); }
.content-reveal-enter-from   { opacity: 0; transform: translateY(20px); }
</style>