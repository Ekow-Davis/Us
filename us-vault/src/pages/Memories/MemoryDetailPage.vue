<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'

const route  = useRoute()
const router = useRouter()
const CURRENT_USER_ID = 'user-001'

// ── Mock store (same data, in real app would be an API call) ──────────────────
const ALL_MEMORIES = [
  { id: 'mem-001', vault_id: 'v1', created_by: 'user-001', title: 'The Night We Got Caught in the Rain', content: 'We ran from the café to the car and you were laughing so hard you couldn\'t even open the door. Your hair was soaked and you looked absolutely unreal. I don\'t think I\'ve ever loved a moment more than that one. The rain on the roof sounded like applause. We sat there for twenty minutes just listening to it, fogging up the windows, neither of us wanting to be the first to drive away. Some moments you know you\'ll remember forever before they\'re even finished.', memory_date: '2025-02-10T19:30:00Z', created_at: '2025-02-10T19:30:00Z', edited_at: '2025-02-10T19:30:00Z', is_seed: false, media: [{ id: 'm1', file_url: 'https://picsum.photos/seed/rain/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-002', vault_id: 'v1', created_by: 'user-002', title: 'Sunday Morning Pancakes', content: 'Made them from scratch for the first time. Burned the first three. The fourth one came out perfect. You ate two of the burned ones without saying a word and I knew then. Knew what? I\'m still not sure I can say it exactly. But I knew something. Maybe that this was safe. That you were the kind of person who eats the burned pancakes and asks for more. That\'s everything, really.', memory_date: '2025-01-28T10:15:00Z', created_at: '2025-01-28T10:15:00Z', edited_at: '2025-01-28T10:15:00Z', is_seed: false, media: [{ id: 'm2', file_url: 'https://picsum.photos/seed/pancake/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-003', vault_id: 'v1', created_by: 'user-001', title: 'Museum Afternoon', content: 'You stood in front of that painting for eleven minutes. I timed it. When you finally turned around your eyes were wet and you just said "let\'s go get food" like nothing happened. I still think about what you were thinking. What it was that held you there that long. You\'ve never told me and I\'ve never asked. Some things are yours to keep.', memory_date: '2025-01-15T14:00:00Z', created_at: '2025-01-15T14:00:00Z', edited_at: '2025-01-15T14:00:00Z', is_seed: false, media: [] },
  { id: 'mem-004', vault_id: 'v1', created_by: 'user-002', title: 'First Grocery Run Together', content: 'We spent 40 minutes arguing about which pasta sauce to buy. You won. It was actually better. I haven\'t admitted that out loud until now. There\'s something quietly significant about doing the ordinary things with someone. Grocery lists and car parks and checkout lines. That\'s where love actually lives, I think.', memory_date: '2025-01-03T16:45:00Z', created_at: '2025-01-03T16:45:00Z', edited_at: '2025-01-03T16:45:00Z', is_seed: false, media: [] },
  { id: 'mem-005', vault_id: 'v1', created_by: 'user-001', title: 'New Year\'s at Home', content: 'We missed the countdown because we were watching that documentary. By the time we noticed it was 12:04. You kissed me anyway and said "still counts." It really did. More than any countdown I\'ve ever watched. Because it was ours and it was late and it was quiet and it was enough.', memory_date: '2025-01-01T00:04:00Z', created_at: '2025-01-01T00:04:00Z', edited_at: '2025-01-01T00:04:00Z', is_seed: false, media: [{ id: 'm5', file_url: 'https://picsum.photos/seed/newyear/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-006', vault_id: 'v1', created_by: 'user-002', title: 'The Long Drive Back', content: 'Six hours, your playlist, and that diner we stopped at somewhere in the middle. You ordered pie. I ordered pie. The waitress said we looked like we\'d been together forever. You didn\'t correct her. Neither did I.', memory_date: '2024-12-28T20:00:00Z', created_at: '2024-12-28T20:00:00Z', edited_at: '2024-12-28T20:00:00Z', is_seed: false, media: [{ id: 'm6', file_url: 'https://picsum.photos/seed/drive/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-007', vault_id: 'v1', created_by: 'user-001', title: 'Learning to Make Your Grandmother\'s Recipe', content: 'You dictated it from memory. I wrote every word down. It took us three hours and two phone calls to your mom. We still didn\'t get it exactly right but it was ours. There\'s a version of it now that belongs to us and I think that\'s better than getting it perfect.', memory_date: '2024-12-20T18:30:00Z', created_at: '2024-12-20T18:30:00Z', edited_at: '2024-12-20T18:30:00Z', is_seed: false, media: [] },
  { id: 'mem-008', vault_id: 'v1', created_by: 'user-002', title: 'Afternoon Nap in the Garden', content: 'You fell asleep reading. The light was coming through the leaves. I didn\'t want to wake you. I just sat there for a while, watching the afternoon pass. Time felt different. Slower. I want more afternoons like that.', memory_date: '2024-12-12T15:00:00Z', created_at: '2024-12-12T15:00:00Z', edited_at: '2024-12-12T15:00:00Z', is_seed: false, media: [{ id: 'm8', file_url: 'https://picsum.photos/seed/garden/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-009', vault_id: 'v1', created_by: 'user-001', title: 'Your First Work Presentation', content: 'You practiced it four times in front of me. The night before you couldn\'t sleep. The day after you called me laughing because they loved it. I already knew they would. I\'ve known what you\'re capable of since before you did.', memory_date: '2024-11-30T09:00:00Z', created_at: '2024-11-30T09:00:00Z', edited_at: '2024-11-30T09:00:00Z', is_seed: false, media: [] },
  { id: 'mem-010', vault_id: 'v1', created_by: 'user-002', title: 'Bookshop on a Rainy Tuesday', content: 'We weren\'t planning to go anywhere. You grabbed your jacket and just said "come on." We came home with nine books and a candle that smelled like cedar. It rained all the way home. We didn\'t mind.', memory_date: '2024-11-18T13:30:00Z', created_at: '2024-11-18T13:30:00Z', edited_at: '2024-11-18T13:30:00Z', is_seed: false, media: [{ id: 'm10', file_url: 'https://picsum.photos/seed/books/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-011', vault_id: 'v1', created_by: 'user-001', title: 'Late Night Conversations', content: 'We talked until 3am about everything. Childhood things. Future things. The kind of conversation that only happens when the rest of the world goes quiet. You told me things you said you\'d never said to anyone. I believed you. I still do.', memory_date: '2024-11-05T03:00:00Z', created_at: '2024-11-05T03:00:00Z', edited_at: '2024-11-05T03:00:00Z', is_seed: true, media: [] },
  { id: 'mem-012', vault_id: 'v1', created_by: 'user-002', title: 'Morning Coffee Without Saying Anything', content: 'Sometimes the best moments aren\'t about what was said. Just the two of us, the steam from the cups, and the light through the kitchen window. We didn\'t need to fill the silence. We never do.', memory_date: '2024-10-22T08:00:00Z', created_at: '2024-10-22T08:00:00Z', edited_at: '2024-10-22T08:00:00Z', is_seed: false, media: [{ id: 'm12', file_url: 'https://picsum.photos/seed/coffee/1200/700', file_type: 'image/jpeg' }] },
]

// ── State ─────────────────────────────────────────────────────────────────────
const memory   = ref(null)
const isLoading = ref(true)
const videoRef  = ref(null)
const videoMuted = ref(false)

// ── Load ──────────────────────────────────────────────────────────────────────
onMounted(() => {
  setTimeout(() => {
    const found = ALL_MEMORIES.find(m => m.id === route.params.id)
    memory.value = found || null
    isLoading.value = false
  }, 400)
})

// ── Computed ──────────────────────────────────────────────────────────────────
const isOwn = computed(() => memory.value?.created_by === CURRENT_USER_ID)
const authorLabel = computed(() => isOwn.value ? 'You' : 'Partner')

const formatFull = (iso) => new Date(iso).toLocaleDateString('en-US', {
  weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
})
const formatTime = (iso) => new Date(iso).toLocaleTimeString('en-US', {
  hour: '2-digit', minute: '2-digit', hour12: true
})

const images = computed(() => memory.value?.media.filter(m => m.file_type.startsWith('image/')) || [])
const videos = computed(() => memory.value?.media.filter(m => m.file_type.startsWith('video/')) || [])

// ── Navigation ────────────────────────────────────────────────────────────────
const currentIndex = computed(() => ALL_MEMORIES.findIndex(m => m.id === route.params.id))
const prevMemory = computed(() => currentIndex.value > 0 ? ALL_MEMORIES[currentIndex.value - 1] : null)
const nextMemory = computed(() => currentIndex.value < ALL_MEMORIES.length - 1 ? ALL_MEMORIES[currentIndex.value + 1] : null)

const toggleMute = () => {
  videoMuted.value = !videoMuted.value
  if (videoRef.value) videoRef.value.muted = videoMuted.value
}

// ── Download ──────────────────────────────────────────────────────────────────
const downloadMedia = (url, filename) => {
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.target = '_blank'
  document.body.appendChild(a); a.click(); document.body.removeChild(a)
}
</script>

<template>
  <Sidebar>
    <div class="detail-page min-h-screen relative">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Nunito:wght@300;400;600;700&display=swap');
      </component>

      <!-- Bg blobs -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute -top-10 right-0 w-72 h-72 rounded-full opacity-20" style="background: radial-gradient(circle, #fce7f3 0%, transparent 70%);"></div>
        <div class="absolute bottom-0 left-0 w-64 h-64 rounded-full opacity-10" style="background: radial-gradient(circle, #ede9fe 0%, transparent 70%);"></div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="relative z-10 flex items-center justify-center min-h-[80vh]">
        <div class="flex flex-col items-center gap-4">
          <div class="w-12 h-12 rounded-full border-2 border-rose-200 border-t-rose-500 animate-spin"></div>
          <p class="detail-body text-sm text-gray-400 tracking-widest uppercase">Opening memory…</p>
        </div>
      </div>

      <!-- Not found -->
      <div v-else-if="!memory" class="relative z-10 flex items-center justify-center min-h-[80vh]">
        <div class="text-center">
          <p class="detail-display text-3xl text-gray-300 mb-4">Memory not found</p>
          <button @click="router.push('/memories')"
                  class="detail-body text-sm text-rose-500 hover:text-rose-700 underline underline-offset-4">
            Back to Memories
          </button>
        </div>
      </div>

      <!-- Content -->
      <div v-else class="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 py-10 detail-fade-in">

        <!-- Back + nav -->
        <div class="flex items-center justify-between mb-8">
          <button @click="router.push('/memories')"
                  class="flex items-center gap-2 text-sm text-gray-400 hover:text-rose-500 transition-colors detail-body group">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transition-transform group-hover:-translate-x-0.5"><polyline points="15 18 9 12 15 6"/></svg>
            All Memories
          </button>
          <div class="flex items-center gap-1">
            <button @click="prevMemory && router.push(`/memories/${prevMemory.id}`)"
                    :disabled="!prevMemory"
                    :class="['pag-btn-sm', !prevMemory ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-500']">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            </button>
            <span class="detail-body text-xs text-gray-400 px-2">{{ currentIndex + 1 }} / {{ ALL_MEMORIES.length }}</span>
            <button @click="nextMemory && router.push(`/memories/${nextMemory.id}`)"
                    :disabled="!nextMemory"
                    :class="['pag-btn-sm', !nextMemory ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-500']">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>
        </div>

        <!-- Author badge -->
        <div class="flex items-center gap-3 mb-5">
          <span :class="['inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold detail-body border',
                         isOwn ? 'bg-rose-50 text-rose-600 border-rose-200' : 'bg-purple-50 text-purple-600 border-purple-200']">
            <span :class="['w-2 h-2 rounded-full', isOwn ? 'bg-rose-400' : 'bg-purple-400']"></span>
            {{ authorLabel }}
          </span>
          <span v-if="memory.is_seed" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold detail-body bg-violet-50 text-violet-600 border border-violet-200">
            <svg width="9" height="9" viewBox="0 0 60 60" fill="#7c3aed"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
            From a Bloom
          </span>
        </div>

        <!-- Title -->
        <h1 class="detail-display text-4xl sm:text-5xl text-gray-900 leading-tight mb-4">
          {{ memory.title }}
        </h1>

        <!-- Date & time -->
        <div class="flex items-center gap-2 mb-8">
          <div class="h-px w-6 bg-rose-200"></div>
          <p class="detail-body text-sm text-gray-400">
            {{ formatFull(memory.memory_date) }}
            <span class="text-rose-400 font-mono ml-2">{{ formatTime(memory.memory_date) }}</span>
          </p>
        </div>

        <!-- Hero image -->
        <div v-if="images.length > 0" class="mb-8 rounded-2xl overflow-hidden" style="box-shadow: 0 12px 40px rgba(0,0,0,0.1);">
          <div class="relative">
            <img :src="images[0].file_url" :alt="memory.title" class="w-full object-cover" style="max-height: 480px;"/>
            <!-- Download button -->
            <button @click="downloadMedia(images[0].file_url, `memory-${memory.id}.jpg`)"
                    class="absolute top-3 right-3 w-9 h-9 rounded-full bg-black/50 hover:bg-black/70 flex items-center justify-center text-white transition backdrop-blur-sm"
                    title="Download image">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            </button>
          </div>
          <!-- Additional images -->
          <div v-if="images.length > 1" class="grid grid-cols-3 gap-0.5 mt-0.5">
            <div v-for="img in images.slice(1)" :key="img.id" class="relative aspect-square overflow-hidden">
              <img :src="img.file_url" :alt="memory.title" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"/>
              <button @click="downloadMedia(img.file_url, `memory-${memory.id}-extra.jpg`)"
                      class="absolute top-2 right-2 w-7 h-7 rounded-full bg-black/50 flex items-center justify-center text-white opacity-0 hover:opacity-100 transition">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Videos -->
        <div v-if="videos.length > 0" class="mb-8 space-y-4">
          <div v-for="vid in videos" :key="vid.id" class="relative rounded-2xl overflow-hidden bg-black" style="box-shadow: 0 8px 30px rgba(0,0,0,0.12);">
            <video ref="videoRef" :src="vid.file_url" controls playsinline
                   class="w-full" style="max-height: 440px;"></video>
            <div class="absolute top-3 right-3 flex gap-2">
              <!-- Mute toggle -->
              <button @click="toggleMute"
                      class="w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition backdrop-blur-sm">
                <svg v-if="videoMuted" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>
                <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
              </button>
              <!-- Download -->
              <button @click="downloadMedia(vid.file_url, `memory-${memory.id}.mp4`)"
                      class="w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition backdrop-blur-sm">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div v-if="memory.content" class="mb-12">
          <!-- Decorative quote mark -->
          <div class="text-6xl leading-none text-rose-100 detail-display mb-2 select-none" aria-hidden="true">"</div>
          <p class="detail-body text-lg text-gray-700 leading-loose">
            {{ memory.content }}
          </p>
          <div class="text-6xl leading-none text-rose-100 detail-display text-right mt-2 select-none" aria-hidden="true">"</div>
        </div>

        <!-- Divider -->
        <div class="flex items-center gap-4 my-8">
          <div class="flex-1 h-px" style="background: linear-gradient(90deg, transparent, #fca5a5);"></div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="#fca5a5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          <div class="flex-1 h-px" style="background: linear-gradient(90deg, #fca5a5, transparent);"></div>
        </div>

        <!-- Meta footer -->
        <div class="rounded-2xl border border-gray-100 bg-white p-5" style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 text-sm">
            <div>
              <p class="detail-body text-xs text-gray-400 uppercase tracking-wide mb-1">Memory Date</p>
              <p class="detail-body text-gray-700 font-semibold">{{ formatFull(memory.memory_date) }}</p>
            </div>
            <div>
              <p class="detail-body text-xs text-gray-400 uppercase tracking-wide mb-1">Added by</p>
              <p class="detail-body text-gray-700 font-semibold">{{ authorLabel }}</p>
            </div>
            <div>
              <p class="detail-body text-xs text-gray-400 uppercase tracking-wide mb-1">Media</p>
              <p class="detail-body text-gray-700 font-semibold">{{ memory.media.length === 0 ? 'None' : `${images.length} image${images.length !== 1 ? 's' : ''}${videos.length > 0 ? `, ${videos.length} video${videos.length !== 1 ? 's' : ''}` : ''}` }}</p>
            </div>
          </div>
        </div>

        <!-- Prev / Next nav at bottom -->
        <div class="flex items-center justify-between mt-10 gap-4">
          <button v-if="prevMemory" @click="router.push(`/memories/${prevMemory.id}`)"
                  class="flex-1 flex items-center gap-3 p-4 rounded-xl border border-gray-100 bg-white hover:border-rose-200 hover:shadow-md transition-all group text-left"
                  style="max-width: 260px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5" class="flex-shrink-0 transition-transform group-hover:-translate-x-0.5"><polyline points="15 18 9 12 15 6"/></svg>
            <div class="min-w-0">
              <p class="detail-body text-xs text-gray-400 uppercase tracking-wide">Previous</p>
              <p class="detail-body text-sm text-gray-700 font-semibold truncate">{{ prevMemory.title }}</p>
            </div>
          </button>
          <div v-else class="flex-1" style="max-width: 260px;"></div>

          <button v-if="nextMemory" @click="router.push(`/memories/${nextMemory.id}`)"
                  class="flex-1 flex items-center justify-end gap-3 p-4 rounded-xl border border-gray-100 bg-white hover:border-rose-200 hover:shadow-md transition-all group text-right ml-auto"
                  style="max-width: 260px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div class="min-w-0">
              <p class="detail-body text-xs text-gray-400 uppercase tracking-wide">Next</p>
              <p class="detail-body text-sm text-gray-700 font-semibold truncate">{{ nextMemory.title }}</p>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5" class="flex-shrink-0 transition-transform group-hover:translate-x-0.5"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
        </div>

        <div class="h-16"></div>
      </div>
    </div>
  </Sidebar>
</template>

<style scoped>
.detail-page {
  background: linear-gradient(160deg, #fff8f8 0%, #ffffff 60%, #f9f5ff 100%);
}
.detail-display { font-family: 'Libre Baskerville', Georgia, serif; }
.detail-body    { font-family: 'Nunito', sans-serif; }

.pag-btn-sm {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: all 0.15s ease;
}

.detail-fade-in {
  animation: detailReveal 0.55s cubic-bezier(0.22,1,0.36,1) both;
}

@keyframes detailReveal {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>