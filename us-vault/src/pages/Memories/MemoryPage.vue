<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'

const router = useRouter()

// ── Mock Data ────────────────────────────────────────────────────────────────
const CURRENT_USER_ID = 'user-001'

const allMemories = ref([
  { id: 'mem-001', vault_id: 'v1', created_by: 'user-001', title: 'The Night We Got Caught in the Rain', content: 'We ran from the café to the car and you were laughing so hard you couldn\'t even open the door. Your hair was soaked and you looked absolutely unreal. I don\'t think I\'ve ever loved a moment more than that one.', memory_date: '2025-02-10T19:30:00Z', created_at: '2025-02-10T19:30:00Z', edited_at: '2025-02-10T19:30:00Z', is_seed: false, media: [{ id: 'm1', file_url: 'https://picsum.photos/seed/rain/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-002', vault_id: 'v1', created_by: 'user-002', title: 'Sunday Morning Pancakes', content: 'Made them from scratch for the first time. Burned the first three. The fourth one came out perfect. You ate two of the burned ones without saying a word and I knew then.', memory_date: '2025-01-28T10:15:00Z', created_at: '2025-01-28T10:15:00Z', edited_at: '2025-01-28T10:15:00Z', is_seed: false, media: [{ id: 'm2', file_url: 'https://picsum.photos/seed/pancake/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-003', vault_id: 'v1', created_by: 'user-001', title: 'Museum Afternoon', content: 'You stood in front of that painting for eleven minutes. I timed it. When you finally turned around your eyes were wet and you just said "let\'s go get food" like nothing happened. I still think about what you were thinking.', memory_date: '2025-01-15T14:00:00Z', created_at: '2025-01-15T14:00:00Z', edited_at: '2025-01-15T14:00:00Z', is_seed: false, media: [] },
  { id: 'mem-004', vault_id: 'v1', created_by: 'user-002', title: 'First Grocery Run Together', content: 'We spent 40 minutes arguing about which pasta sauce to buy. You won. It was actually better. I haven\'t admitted that out loud until now.', memory_date: '2025-01-03T16:45:00Z', created_at: '2025-01-03T16:45:00Z', edited_at: '2025-01-03T16:45:00Z', is_seed: false, media: [] },
  { id: 'mem-005', vault_id: 'v1', created_by: 'user-001', title: 'New Year\'s at Home', content: 'We missed the countdown because we were watching that documentary. By the time we noticed it was 12:04. You kissed me anyway and said "still counts." It really did.', memory_date: '2025-01-01T00:04:00Z', created_at: '2025-01-01T00:04:00Z', edited_at: '2025-01-01T00:04:00Z', is_seed: false, media: [{ id: 'm5', file_url: 'https://picsum.photos/seed/newyear/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-006', vault_id: 'v1', created_by: 'user-002', title: 'The Long Drive Back', content: 'Six hours, your playlist, and that diner we stopped at somewhere in the middle. You ordered pie. I ordered pie. The waitress said we looked like we\'d been together forever.', memory_date: '2024-12-28T20:00:00Z', created_at: '2024-12-28T20:00:00Z', edited_at: '2024-12-28T20:00:00Z', is_seed: false, media: [{ id: 'm6', file_url: 'https://picsum.photos/seed/drive/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-007', vault_id: 'v1', created_by: 'user-001', title: 'Learning to Make Your Grandmother\'s Recipe', content: 'You dictated it from memory. I wrote every word down. It took us three hours and two phone calls to your mom. We still didn\'t get it exactly right but it was ours.', memory_date: '2024-12-20T18:30:00Z', created_at: '2024-12-20T18:30:00Z', edited_at: '2024-12-20T18:30:00Z', is_seed: false, media: [] },
  { id: 'mem-008', vault_id: 'v1', created_by: 'user-002', title: 'Afternoon Nap in the Garden', content: 'You fell asleep reading. The light was coming through the leaves. I didn\'t want to wake you. I just sat there for a while, watching the afternoon pass.', memory_date: '2024-12-12T15:00:00Z', created_at: '2024-12-12T15:00:00Z', edited_at: '2024-12-12T15:00:00Z', is_seed: false, media: [{ id: 'm8', file_url: 'https://picsum.photos/seed/garden/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-009', vault_id: 'v1', created_by: 'user-001', title: 'Your First Work Presentation', content: 'You practiced it four times in front of me. The night before you couldn\'t sleep. The day after you called me laughing because they loved it. I already knew they would.', memory_date: '2024-11-30T09:00:00Z', created_at: '2024-11-30T09:00:00Z', edited_at: '2024-11-30T09:00:00Z', is_seed: false, media: [] },
  { id: 'mem-010', vault_id: 'v1', created_by: 'user-002', title: 'Bookshop on a Rainy Tuesday', content: 'We weren\'t planning to go anywhere. You grabbed your jacket and just said "come on." We came home with nine books and a candle that smelled like cedar.', memory_date: '2024-11-18T13:30:00Z', created_at: '2024-11-18T13:30:00Z', edited_at: '2024-11-18T13:30:00Z', is_seed: false, media: [{ id: 'm10', file_url: 'https://picsum.photos/seed/books/800/500', file_type: 'image/jpeg' }] },
  { id: 'mem-011', vault_id: 'v1', created_by: 'user-001', title: 'Late Night Conversations', content: 'We talked until 3am about everything. Childhood things. Future things. The kind of conversation that only happens when the rest of the world goes quiet.', memory_date: '2024-11-05T03:00:00Z', created_at: '2024-11-05T03:00:00Z', edited_at: '2024-11-05T03:00:00Z', is_seed: true, media: [] },
  { id: 'mem-012', vault_id: 'v1', created_by: 'user-002', title: 'Morning Coffee Without Saying Anything', content: 'Sometimes the best moments aren\'t about what was said. Just the two of us, the steam from the cups, and the light through the kitchen window.', memory_date: '2024-10-22T08:00:00Z', created_at: '2024-10-22T08:00:00Z', edited_at: '2024-10-22T08:00:00Z', is_seed: false, media: [{ id: 'm12', file_url: 'https://picsum.photos/seed/coffee/800/500', file_type: 'image/jpeg' }] },
])

// ── Pagination ────────────────────────────────────────────────────────────────
const perPage = ref(6)
const currentPage = ref(1)

const totalPages = computed(() => Math.ceil(allMemories.value.length / perPage.value))

const paginatedMemories = computed(() => {
  const start = (currentPage.value - 1) * perPage.value
  return allMemories.value.slice(start, start + perPage.value)
})

const pageNumbers = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    pages.push(1)
    if (current > 3) pages.push('...')
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) pages.push(i)
    if (current < total - 2) pages.push('...')
    pages.push(total)
  }
  return pages
})

watch(perPage, () => { currentPage.value = 1 })

const goToPage = (p) => {
  if (typeof p === 'number' && p >= 1 && p <= totalPages.value) currentPage.value = p
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const truncate = (text, max = 100) => {
  if (!text) return ''
  return text.length > max ? text.slice(0, max) + '…' : text
}
const formatDate = (iso) => new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
const isOwn = (memory) => memory.created_by === CURRENT_USER_ID
const primaryImage = (memory) => memory.media.find(m => m.file_type.startsWith('image/'))
</script>

<template>
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
              <p class="mem-body text-sm text-gray-400 mt-2">{{ allMemories.length }} moments preserved</p>
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
            Page {{ currentPage }} of {{ totalPages }} &nbsp;·&nbsp; {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allMemories.length) }} of {{ allMemories.length }}
          </p>
          <div class="flex items-center gap-1">
            <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                    :class="['pag-btn', currentPage === 1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <template v-for="(p, i) in pageNumbers" :key="i">
              <span v-if="p === '...'" class="px-1 text-gray-400 mem-body text-sm">…</span>
              <button v-else @click="goToPage(p)"
                      :class="['pag-btn', currentPage === p ? 'bg-rose-500 text-white shadow-sm' : 'hover:bg-rose-50 hover:text-rose-600']">
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
            Showing {{ (currentPage-1)*perPage+1 }}–{{ Math.min(currentPage*perPage, allMemories.length) }} of {{ allMemories.length }} memories
          </p>
          <div class="flex items-center gap-1">
            <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
                    :class="['pag-btn', currentPage === 1 ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <template v-for="(p, i) in pageNumbers" :key="i">
              <span v-if="p === '...'" class="px-1 text-gray-400 mem-body text-sm">…</span>
              <button v-else @click="goToPage(p)"
                      :class="['pag-btn', currentPage === p ? 'bg-rose-500 text-white shadow-sm' : 'hover:bg-rose-50 hover:text-rose-600']">
                {{ p }}
              </button>
            </template>
            <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
                    :class="['pag-btn', currentPage === totalPages ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-600']">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>

      </div>
    </div>
  </Sidebar>
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
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>