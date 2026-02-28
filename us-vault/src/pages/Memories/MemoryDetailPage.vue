<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { Edit2, Save, X, Plus, Trash2 } from 'lucide-vue-next'
import { getMemoryApi, updateMemoryApi, deleteMemoryApi } from '../../api/memories'
import { uploadMemoryMediaApi, deleteMemoryMediaApi } from '../../api/media'
// import { useAuthStore } from '../../stores/authStore'
// import { useVaultStore } from '../../stores/vaultStore'

const route = useRoute()
const router = useRouter()

// ── Stores (mock for now) ──────────────────────────────────────────────────
// const authStore = useAuthStore()
// const vaultStore = useVaultStore()
// const CURRENT_USER_ID = authStore.user?.id || 'user-001'
// const PARTNER_NAME = vaultStore.partner_name || 'Partner'

const CURRENT_USER_ID = 'user-001' // Mock
const PARTNER_NAME = 'Alex' // Mock

// ── Mock Data Store ────────────────────────────────────────────────────────
const ALL_MEMORIES = ref([
  { id: 'mem-001', vault_id: 'v1', created_by: 'user-001', title: 'The Night We Got Caught in the Rain', content: 'We ran from the café to the car and you were laughing so hard you couldn\'t even open the door. Your hair was soaked and you looked absolutely unreal.', memory_date: '2025-02-10T19:30:00Z', created_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(), is_seed: false, media: [{ id: 'm1', file_url: 'https://picsum.photos/seed/rain/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-002', vault_id: 'v1', created_by: 'user-002', title: 'Sunday Morning Pancakes', content: 'Made them from scratch for the first time. Burned the first three. The fourth one came out perfect.', memory_date: '2025-01-28T10:15:00Z', created_at: '2025-01-28T10:15:00Z', is_seed: false, media: [{ id: 'm2', file_url: 'https://picsum.photos/seed/pancake/1200/700', file_type: 'image/jpeg' }] },
  { id: 'mem-003', vault_id: 'v1', created_by: 'user-001', title: 'Museum Afternoon', content: 'You stood in front of that painting for eleven minutes. I timed it.', memory_date: '2025-01-15T14:00:00Z', created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), is_seed: false, media: [] },
  { id: 'mem-004', vault_id: 'v1', created_by: 'user-002', title: 'First Grocery Run Together', content: 'We spent 40 minutes arguing about which pasta sauce to buy.', memory_date: '2025-01-03T16:45:00Z', created_at: '2025-01-03T16:45:00Z', is_seed: false, media: [] },
])

// ── State ──────────────────────────────────────────────────────────────────
const memory = ref(null)
const isLoading = ref(true)
const isEditing = ref(false)
const isSaving = ref(false)
const error = ref('')

// Edit form
const editForm = ref({
  title: '',
  content: '',
  media: []
})

// Media
const mediaInput = ref(null)
const isUploadingMedia = ref(false)
const videoRef = ref(null)
const videoMuted = ref(false)

// ── Computed ───────────────────────────────────────────────────────────────
const isOwn = computed(() => memory.value?.created_by === CURRENT_USER_ID)
const authorLabel = computed(() => isOwn.value ? 'You' : PARTNER_NAME)

const canEdit = computed(() => {
  if (!memory.value || !isOwn.value) return false

  const createdAt = new Date(memory.value.created_at)
  const now = new Date()

  const hoursDiff = (now.getTime() - createdAt.getTime()) / (1000 * 60 * 60)

  return hoursDiff <= 8
})

const hasChanges = computed(() => {
  if (!memory.value) return false
  return (
    editForm.value.title !== memory.value.title ||
    editForm.value.content !== memory.value.content ||
    editForm.value.media.length !== memory.value.media.length
  )
})

// Author color scheme
const authorColorClass = computed(() => {
  return isOwn.value 
    ? 'bg-rose-50 text-rose-600 border-rose-200' 
    : 'bg-purple-50 text-purple-600 border-purple-200'
})

const authorDotClass = computed(() => {
  return isOwn.value ? 'bg-rose-400' : 'bg-purple-400'
})

const images = computed(() => {
  const mediaList = isEditing.value ? editForm.value.media : (memory.value?.media || [])
  return mediaList.filter(m => m.file_type.startsWith('image/'))
})

const videos = computed(() => {
  const mediaList = isEditing.value ? editForm.value.media : (memory.value?.media || [])
  return mediaList.filter(m => m.file_type.startsWith('video/'))
})

// ── Navigation ─────────────────────────────────────────────────────────────
const currentIndex = computed(() => 
  ALL_MEMORIES.value.findIndex(m => m.id === route.params.id)
)

const prevMemory = computed(() => 
  currentIndex.value > 0 ? ALL_MEMORIES.value[currentIndex.value - 1] : null
)

const nextMemory = computed(() => 
  currentIndex.value < ALL_MEMORIES.value.length - 1 
    ? ALL_MEMORIES.value[currentIndex.value + 1] 
    : null
)

// ── Methods ────────────────────────────────────────────────────────────────
const initializeEditForm = () => {
  if (memory.value) {
    editForm.value = {
      title: memory.value.title,
      content: memory.value.content,
      media: [...memory.value.media]
    }
  }
}

const startEditing = () => {
  if (!canEdit.value) return
  initializeEditForm()
  isEditing.value = true
}

const cancelEditing = () => {
  if (hasChanges.value) {
    if (!confirm('You have unsaved changes. Are you sure you want to cancel?')) {
      return
    }
  }
  isEditing.value = false
  error.value = ''
}

const handleSave = async () => {
  if (!editForm.value.title.trim()) {
    error.value = 'Title is required'
    return
  }

  if (!editForm.value.content.trim()) {
    error.value = 'Content is required'
    return
  }

  isSaving.value = true
  error.value = ''

  try {
    const res = await updateMemoryApi(memory.value.id, {
      title: editForm.value.title,
      content: editForm.value.content
    })

    memory.value = res.data

    isEditing.value = false

    showToast('Memory updated successfully')

  } catch (err) {
    error.value = err?.response?.data?.detail || 'Editing window is closed.'
  } finally {
    isSaving.value = false
  }
}

const handleMediaSelect = async (event) => {
  const files = Array.from(event.target.files)
  if (!files.length) return

  isUploadingMedia.value = true
  error.value = ''

  try {
    for (const file of files) {
      await uploadMemoryMediaApi(memory.value.id, file)
    }

    // reload memory to get fresh media
    await loadMemory(memory.value.id)

    showToast('Media uploaded')

  } catch (err) {
    error.value = err?.response?.data?.detail || 'Upload failed'
  } finally {
    isUploadingMedia.value = false
  }
}

const removeMedia = async (mediaId) => {
  try {
    await deleteMemoryMediaApi(mediaId)

    await loadMemory(memory.value.id)

    showToast('Media removed')

  } catch (err) {
    error.value = err?.response?.data?.detail || 'Cannot delete media'
  }
}

const handleDelete = async () => {
  if (!confirm('This will permanently withdraw this memory. Continue?')) {
    return
  }

  try {
    await deleteMemoryApi(memory.value.id)

    showToast('Memory withdrawn')

    router.push('/my-memories')

  } catch (err) {
    error.value = err?.response?.data?.detail || 'Delete window expired'
  }
}

const toggleMute = () => {
  videoMuted.value = !videoMuted.value
  if (videoRef.value) videoRef.value.muted = videoMuted.value
}

const downloadMedia = (url, filename) => {
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.target = '_blank'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

const toast = ref({
  visible: false,
  message: '',
  type: 'success'
})

const showToast = (message, type = 'success') => {
  toast.value = { visible: true, message, type }
  setTimeout(() => toast.value.visible = false, 4000)
}

const formatFull = (iso) => new Date(iso).toLocaleDateString('en-US', {
  weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
})

const formatTime = (iso) => new Date(iso).toLocaleTimeString('en-US', {
  hour: '2-digit', minute: '2-digit', hour12: true
})

const loadMemory = async (memoryId) => {
  isLoading.value = true
  isEditing.value = false
  error.value = ''

  try {
    const res = await getMemoryApi(memoryId)
    memory.value = res.data
  } catch (err) {
    console.error(err)
    memory.value = null
  } finally {
    isLoading.value = false
  }
}

// ── Watch for route changes ────────────────────────────────────────────────
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      loadMemory(newId)
    }
  }
)

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
  loadMemory(route.params.id)
})
</script>

<template>
  <InactivityOverlay>
    <Sidebar>
      <div class="detail-page min-h-screen relative">
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Nunito:wght@300;400;600;700&display=swap');
        </component>

        <!-- Bg blobs -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <div class="absolute -top-10 right-0 w-72 h-72 rounded-full opacity-20" 
               :style="`background: radial-gradient(circle, ${isOwn ? '#fce7f3' : '#ede9fe'} 0%, transparent 70%);`"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 rounded-full opacity-10" 
               :style="`background: radial-gradient(circle, ${isOwn ? '#fce7f3' : '#ede9fe'} 0%, transparent 70%);`"></div>
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

          <!-- Back + nav + edit -->
          <div class="flex items-center justify-between mb-8 gap-4">
            <button @click="router.push(isOwn ? '/my-memories' : '/memories')"
                    class="flex items-center gap-2 text-sm text-gray-400 hover:text-rose-500 transition-colors detail-body group">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transition-transform group-hover:-translate-x-0.5">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              {{ isOwn ? 'My Memories' : 'All Memories' }}
            </button>

            <div class="flex items-center gap-2">
              <!-- Edit button -->
              <button 
                v-if="canEdit && !isEditing"
                @click="startEditing"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white hover:bg-emerald-600 transition detail-body text-sm font-semibold">
                <Edit2 :size="14" />
                Edit
              </button>

              <!-- Navigation -->
              <div class="flex items-center gap-1">
                <button @click="prevMemory && router.push(`/memories/${prevMemory.id}`)"
                        :disabled="!prevMemory"
                        :class="['pag-btn-sm', !prevMemory ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-500']">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="15 18 9 12 15 6"/>
                  </svg>
                </button>
                <span class="detail-body text-xs text-gray-400 px-2">
                  {{ currentIndex + 1 }} / {{ ALL_MEMORIES.length }}
                </span>
                <button @click="nextMemory && router.push(`/memories/${nextMemory.id}`)"
                        :disabled="!nextMemory"
                        :class="['pag-btn-sm', !nextMemory ? 'opacity-30 cursor-not-allowed' : 'hover:bg-rose-50 hover:text-rose-500']">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="9 18 15 12 9 6"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Edit Mode Banner -->
          <div v-if="isEditing" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between">
            <div class="flex items-center gap-3">
              <Edit2 :size="18" class="text-emerald-600" />
              <div>
                <p class="detail-body text-sm font-semibold text-emerald-900">Editing Mode</p>
                <p class="detail-body text-xs text-emerald-700">Make changes to your memory below</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button @click="cancelEditing"
                      class="flex items-center gap-1.5 px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-100 transition detail-body text-sm font-semibold">
                <X :size="14" />
                Cancel
              </button>
              <button 
                v-if="canEdit"
                @click="handleDelete"
                class="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 transition detail-body text-sm font-semibold">
                <Trash2 :size="14" />
                Delete
              </button>
              <button @click="handleSave"
                      :disabled="!hasChanges || isSaving"
                      class="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition detail-body text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed">
                <Save :size="14" />
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
            <p class="detail-body text-sm text-red-700">{{ error }}</p>
          </div>

          <!-- Author badge -->
          <div class="flex items-center gap-3 mb-5">
            <span :class="['inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold detail-body border', authorColorClass]">
              <span :class="['w-2 h-2 rounded-full', authorDotClass]"></span>
              {{ authorLabel }}
            </span>
            <span v-if="memory.is_seed" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold detail-body bg-violet-50 text-violet-600 border border-violet-200">
              <svg width="9" height="9" viewBox="0 0 60 60" fill="#7c3aed">
                <ellipse cx="30" cy="34" rx="14" ry="20"/>
              </svg>
              From a Bloom
            </span>
          </div>

          <!-- Title (editable) -->
          <div v-if="isEditing" class="mb-4">
            <label class="detail-body text-sm font-semibold text-slate-700 mb-2 block">Title</label>
            <input 
              v-model="editForm.title"
              type="text"
              class="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-rose-300 focus:ring-2 focus:ring-rose-100 transition detail-display text-2xl"
              placeholder="Memory title..."
            />
          </div>
          <h1 v-else class="detail-display text-4xl sm:text-5xl text-gray-900 leading-tight mb-4">
            {{ memory.title }}
          </h1>

          <!-- Date & time -->
          <div class="flex items-center gap-2 mb-8">
            <div class="h-px w-6" :class="isOwn ? 'bg-rose-200' : 'bg-purple-200'"></div>
            <p class="detail-body text-sm text-gray-400">
              {{ formatFull(memory.memory_date) }}
              <span :class="['font-mono ml-2', isOwn ? 'text-rose-400' : 'text-purple-400']">
                {{ formatTime(memory.memory_date) }}
              </span>
            </p>
          </div>

          <!-- Media Section -->
          <div class="mb-8">
            <!-- Add Media (Edit Mode) -->
            <div v-if="isEditing" class="mb-4">
              <div class="flex items-center justify-between mb-3">
                <label class="detail-body text-sm font-semibold text-slate-700">
                  Media ({{ editForm.media.length }})
                </label>
                <button 
                  @click="mediaInput?.click()"
                  :disabled="isUploadingMedia"
                  class="flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-50 text-rose-600 hover:bg-rose-100 detail-body text-sm font-semibold transition disabled:opacity-50">
                  <Plus :size="16" />
                  {{ isUploadingMedia ? 'Uploading...' : 'Add Media' }}
                </button>
                <input 
                  ref="mediaInput"
                  type="file"
                  accept="image/*,video/*"
                  multiple
                  class="hidden"
                  @change="handleMediaSelect"
                />
              </div>
            </div>

            <!-- Images Display/Edit -->
            <div v-if="images.length > 0" class="mb-4 rounded-2xl overflow-hidden" style="box-shadow: 0 12px 40px rgba(0,0,0,0.1);">
              <div class="relative">
                <img :src="images[0].file_url" :alt="memory.title" class="w-full object-cover" style="max-height: 480px;"/>
                
                <!-- Remove button (Edit Mode) -->
                <button v-if="isEditing"
                        @click="removeMedia(images[0].id)"
                        class="absolute top-3 right-3 w-9 h-9 rounded-full bg-red-500 hover:bg-red-600 flex items-center justify-center text-white transition">
                  <Trash2 :size="14" />
                </button>
                
                <!-- Download button (View Mode) -->
                <button v-else
                        @click="downloadMedia(images[0].file_url, `memory-${memory.id}.jpg`)"
                        class="absolute top-3 right-3 w-9 h-9 rounded-full bg-black/50 hover:bg-black/70 flex items-center justify-center text-white transition backdrop-blur-sm">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                </button>
              </div>

              <!-- Additional images -->
              <div v-if="images.length > 1" class="grid grid-cols-3 gap-0.5 mt-0.5">
                <div v-for="img in images.slice(1)" :key="img.id" class="relative aspect-square overflow-hidden">
                  <img :src="img.file_url" :alt="memory.title" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"/>
                  
                  <button v-if="isEditing"
                          @click="removeMedia(img.id)"
                          class="absolute top-2 right-2 w-7 h-7 rounded-full bg-red-500 hover:bg-red-600 flex items-center justify-center text-white transition">
                    <Trash2 :size="12" />
                  </button>
                  
                  <button v-else
                          @click="downloadMedia(img.file_url, `memory-${memory.id}-extra.jpg`)"
                          class="absolute top-2 right-2 w-7 h-7 rounded-full bg-black/50 flex items-center justify-center text-white opacity-0 hover:opacity-100 transition">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Videos -->
            <div v-if="videos.length > 0" class="space-y-4">
              <div v-for="vid in videos" :key="vid.id" class="relative rounded-2xl overflow-hidden bg-black" style="box-shadow: 0 8px 30px rgba(0,0,0,0.12);">
                <video ref="videoRef" :src="vid.file_url" controls playsinline class="w-full" style="max-height: 440px;"></video>
                
                <div class="absolute top-3 right-3 flex gap-2">
                  <!-- Remove (Edit Mode) -->
                  <button v-if="isEditing"
                          @click="removeMedia(vid.id)"
                          class="w-9 h-9 rounded-full bg-red-500 hover:bg-red-600 flex items-center justify-center text-white transition">
                    <Trash2 :size="14" />
                  </button>
                  
                  <template v-else>
                    <!-- Mute toggle -->
                    <button @click="toggleMute"
                            class="w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition backdrop-blur-sm">
                      <svg v-if="videoMuted" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                        <line x1="23" y1="9" x2="17" y2="15"/>
                        <line x1="17" y1="9" x2="23" y2="15"/>
                      </svg>
                      <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
                        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                      </svg>
                    </button>
                    <!-- Download -->
                    <button @click="downloadMedia(vid.file_url, `memory-${memory.id}.mp4`)"
                            class="w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition backdrop-blur-sm">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </button>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <!-- Content (editable) -->
          <div class="mb-12">
            <div v-if="isEditing">
              <label class="detail-body text-sm font-semibold text-slate-700 mb-2 block">Content</label>
              <textarea 
                v-model="editForm.content"
                rows="10"
                class="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-rose-300 focus:ring-2 focus:ring-rose-100 transition detail-body text-lg resize-none"
                placeholder="Write your memory..."></textarea>
            </div>
            <div v-else-if="memory.content">
              <div class="text-6xl leading-none text-rose-100 detail-display mb-2 select-none" aria-hidden="true">"</div>
              <p class="detail-body text-lg text-gray-700 leading-loose whitespace-pre-wrap">{{ memory.content }}</p>
              <div class="text-6xl leading-none text-rose-100 detail-display text-right mt-2 select-none" aria-hidden="true">"</div>
            </div>
          </div>

          <!-- Divider -->
          <div class="flex items-center gap-4 my-8">
            <div class="flex-1 h-px" :style="`background: linear-gradient(90deg, transparent, ${isOwn ? '#fca5a5' : '#c4b5fd'});`"></div>
            <svg width="14" height="14" viewBox="0 0 24 24" :fill="isOwn ? '#fca5a5' : '#c4b5fd'">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
            <div class="flex-1 h-px" :style="`background: linear-gradient(90deg, ${isOwn ? '#fca5a5' : '#c4b5fd'}, transparent);`"></div>
          </div>

          <!-- Meta footer -->
          <div class="rounded-2xl border border-gray-100 bg-white p-5 mb-10" style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
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
                <p class="detail-body text-gray-700 font-semibold">
                  {{ memory.media.length === 0 ? 'None' : `${images.length} image${images.length !== 1 ? 's' : ''}${videos.length > 0 ? `, ${videos.length} video${videos.length !== 1 ? 's' : ''}` : ''}` }}
                </p>
              </div>
            </div>
          </div>

          <!-- Prev / Next nav -->
          <div class="flex items-center justify-between gap-4">
            <button v-if="prevMemory" @click="router.push(`/memories/${prevMemory.id}`)"
                    class="flex-1 flex items-center gap-3 p-4 rounded-xl border border-gray-100 bg-white hover:border-rose-200 hover:shadow-md transition-all group text-left"
                    style="max-width: 260px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5" class="shrink-0 transition-transform group-hover:-translate-x-0.5">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
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
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5" class="shrink-0 transition-transform group-hover:translate-x-0.5">
                <polyline points="9 18 15 12 9 6"/>
              </svg>
            </button>
          </div>

        </div>
      </div>
      
      <div v-if="toast.visible"
          class="fixed bottom-6 right-6 px-6 py-3 rounded-xl shadow-lg text-white text-sm z-50"
          :class="toast.type === 'error' ? 'bg-red-500' : 'bg-emerald-500'">
        {{ toast.message }}
      </div>
    </Sidebar>
    
  </InactivityOverlay>
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