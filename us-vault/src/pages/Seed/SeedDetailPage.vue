<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'

const route = useRoute()
const router = useRouter()
const seedId = route.params.id

// ── State ──────────────────────────────────────────────────────────────────
const seed = ref(null)
const isLoading = ref(true)
const isSaving = ref(false)
const error = ref(null)
const successMessage = ref(null)

// Form data
const editForm = ref({
  title: '',
  content: '',
  media: []
})

// Media upload
const mediaInput = ref(null)
const isUploadingMedia = ref(false)

// ── Mock API Calls ─────────────────────────────────────────────────────────
const fetchSeed = async (id) => {
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock seed data
  const mockSeeds = {
    'seed-001': {
      id: 'seed-001',
      vault_id: 'v1',
      created_by: 'user-001',
      title: 'A Letter for Our First Year',
      content: 'There are things I want to tell you a year from now, when we\'ve grown into something neither of us can fully predict yet. This is my message to future us, a reminder of how I felt today.',
      bloom_at: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
      status: 'scheduled',
      media: []
    },
    'seed-002': {
      id: 'seed-002',
      vault_id: 'v1',
      created_by: 'user-001',
      title: 'What I Noticed First',
      content: 'I\'ve been keeping this for a while. When the time comes, I hope you smile reading it. It\'s about all the small things that made me realize this was special.',
      bloom_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
      status: 'scheduled',
      media: [
        { id: 'sm1', file_url: 'https://picsum.photos/seed/first/800/500', file_type: 'image/jpeg' }
      ]
    }
  }
  
  return mockSeeds[id] || null
}

const updateSeed = async (id, data) => {
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // Check if seed is within 24 hours of blooming
  const bloomDate = new Date(seed.value.bloom_at)
  const hoursUntilBloom = (bloomDate - new Date()) / (1000 * 60 * 60)
  
  if (hoursUntilBloom < 24 && hoursUntilBloom > 0) {
    throw new Error('Cannot edit seed within 24 hours of blooming')
  }
  
  // Mock successful update
  return {
    ...seed.value,
    ...data,
    updated_at: new Date().toISOString()
  }
}

const uploadMedia = async (file) => {
  await new Promise(resolve => setTimeout(resolve, 800))
  
  // Mock media upload
  return {
    id: `media-${Date.now()}`,
    file_url: URL.createObjectURL(file),
    file_type: file.type,
    file_name: file.name
  }
}

// ── Computed ───────────────────────────────────────────────────────────────
const hasChanges = computed(() => {
  if (!seed.value) return false
  return (
    editForm.value.title !== seed.value.title ||
    editForm.value.content !== seed.value.content ||
    editForm.value.media.length !== seed.value.media.length
  )
})

const bloomDate = computed(() => {
  if (!seed.value) return null
  return new Date(seed.value.bloom_at)
})

const hoursUntilBloom = computed(() => {
  if (!bloomDate.value) return null
  const diff = bloomDate.value - new Date()
  return Math.max(0, diff / (1000 * 60 * 60))
})

const canEdit = computed(() => {
  return hoursUntilBloom.value === null || hoursUntilBloom.value >= 24
})

const formatDate = (iso) => {
  return new Date(iso).toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

// ── Methods ────────────────────────────────────────────────────────────────
const initializeForm = () => {
  if (seed.value) {
    editForm.value = {
      title: seed.value.title,
      content: seed.value.content,
      media: [...seed.value.media]
    }
  }
}

const handleMediaSelect = async (event) => {
  const files = Array.from(event.target.files)
  if (files.length === 0) return
  
  isUploadingMedia.value = true
  error.value = null
  
  try {
    for (const file of files) {
      // Validate file type
      if (!file.type.startsWith('image/') && !file.type.startsWith('video/')) {
        throw new Error('Only image and video files are allowed')
      }
      
      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        throw new Error('File size must be less than 10MB')
      }
      
      const uploadedMedia = await uploadMedia(file)
      editForm.value.media.push(uploadedMedia)
    }
  } catch (err) {
    error.value = err.message
  } finally {
    isUploadingMedia.value = false
    if (mediaInput.value) {
      mediaInput.value.value = ''
    }
  }
}

const removeMedia = (mediaId) => {
  editForm.value.media = editForm.value.media.filter(m => m.id !== mediaId)
}

const handleSave = async () => {
  if (!canEdit.value) {
    error.value = 'Cannot edit seed within 24 hours of blooming'
    return
  }
  
  if (!editForm.value.title.trim()) {
    error.value = 'Title is required'
    return
  }
  
  if (!editForm.value.content.trim()) {
    error.value = 'Content is required'
    return
  }
  
  isSaving.value = true
  error.value = null
  successMessage.value = null
  
  try {
    await updateSeed(seedId, {
      title: editForm.value.title,
      content: editForm.value.content,
      media: editForm.value.media
    })
    
    successMessage.value = 'Seed updated successfully!'
    
    // Navigate back after a short delay
    setTimeout(() => {
      router.push('/my-seeds')
    }, 1500)
  } catch (err) {
    error.value = err.message
    
    // If can't edit due to bloom time, redirect after showing error
    if (err.message.includes('24 hours')) {
      setTimeout(() => {
        router.push('/my-seeds')
      }, 2500)
    }
  } finally {
    isSaving.value = false
  }
}

const handleCancel = () => {
  if (hasChanges.value) {
    if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
      router.push('/my-seeds')
    }
  } else {
    router.push('/my-seeds')
  }
}

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const data = await fetchSeed(seedId)
    
    if (!data) {
      error.value = 'Seed not found'
      return
    }
    
    seed.value = data
    initializeForm()
  } catch (err) {
    error.value = 'Failed to load seed'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <Sidebar>
    <div class="seed-detail-page min-h-screen relative overflow-x-hidden">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
      </component>

      <!-- Ambient BG -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#c7d2fe 0%,transparent 70%);"></div>
        <div class="absolute top-1/2 -left-20 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">

        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center min-h-100">
          <div class="flex flex-col items-center gap-3">
            <div class="flex gap-1">
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.2s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.4s"></span>
            </div>
            <p class="seed-body text-sm text-indigo-400 tracking-wide">Loading seed…</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error && !seed" class="flex flex-col items-center justify-center min-h-100 gap-4">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <p class="seed-body text-red-600 text-lg">{{ error }}</p>
          <button @click="router.push('/my-seeds')" 
                  class="px-6 py-2 rounded-xl bg-indigo-600 text-white seed-body font-semibold hover:bg-indigo-700 transition">
            Back to My Seeds
          </button>
        </div>

        <!-- Main Content -->
        <template v-else-if="seed">
          <!-- Header -->
          <div class="mb-8">
            <button @click="handleCancel" 
                    class="inline-flex items-center gap-2 text-indigo-600 hover:text-indigo-800 seed-body text-sm font-semibold mb-4 transition">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="15 18 9 12 15 6"/>
              </svg>
              Back to My Seeds
            </button>

            <div class="flex items-start justify-between gap-4 flex-wrap">
              <div>
                <p class="seed-sub text-xs text-indigo-500 uppercase tracking-widest mb-1">Edit Seed</p>
                <h1 class="seed-display text-3xl md:text-4xl text-slate-900">{{ seed.title }}</h1>
                <p class="seed-body text-sm text-slate-500 mt-2">
                  Blooms {{ formatDate(seed.bloom_at) }}
                </p>
              </div>
              
              <!-- Status Badge -->
              <div class="flex flex-col items-end gap-2">
                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold seed-body bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  Growing
                </span>
                <p v-if="!canEdit" class="seed-body text-xs text-amber-600 font-semibold">
                  ⚠ Within 24h of bloom - editing disabled
                </p>
              </div>
            </div>
          </div>

          <!-- Alerts -->
          <div v-if="error" class="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 flex items-start gap-3">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" class="shrink-0 mt-0.5">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <p class="seed-body text-sm text-red-700 flex-1">{{ error }}</p>
          </div>

          <div v-if="successMessage" class="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-start gap-3">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" class="shrink-0 mt-0.5">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            <p class="seed-body text-sm text-emerald-700 flex-1">{{ successMessage }}</p>
          </div>

          <!-- Edit Form -->
          <div class="bg-white rounded-2xl border border-indigo-100 shadow-sm overflow-hidden">
            <div class="p-6 md:p-8 space-y-6">
              
              <!-- Title -->
              <div>
                <label class="seed-body text-sm font-semibold text-slate-700 mb-2 block">
                  Title
                </label>
                <input 
                  v-model="editForm.title"
                  type="text"
                  :disabled="!canEdit"
                  class="w-full px-4 py-3 rounded-xl border border-indigo-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition seed-body disabled:bg-slate-50 disabled:text-slate-500"
                  placeholder="Give your seed a meaningful title..."
                />
              </div>

              <!-- Content -->
              <div>
                <label class="seed-body text-sm font-semibold text-slate-700 mb-2 block">
                  Message
                </label>
                <textarea 
                  v-model="editForm.content"
                  :disabled="!canEdit"
                  rows="8"
                  class="w-full px-4 py-3 rounded-xl border border-indigo-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition seed-body resize-none disabled:bg-slate-50 disabled:text-slate-500"
                  placeholder="Write your message that will bloom in the future..."
                ></textarea>
              </div>

              <!-- Media -->
              <div>
                <div class="flex items-center justify-between mb-3">
                  <label class="seed-body text-sm font-semibold text-slate-700">
                    Media ({{ editForm.media.length }})
                  </label>
                  <button 
                    v-if="canEdit"
                    @click="mediaInput?.click()"
                    :disabled="isUploadingMedia"
                    class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-50 text-indigo-600 hover:bg-indigo-100 seed-body text-sm font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="12" y1="5" x2="12" y2="19"/>
                      <line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
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

                <!-- Media Grid -->
                <div v-if="editForm.media.length > 0" class="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div v-for="media in editForm.media" :key="media.id" 
                       class="relative group aspect-video rounded-lg overflow-hidden bg-slate-100 border border-slate-200">
                    <img v-if="media.file_type.startsWith('image/')" 
                         :src="media.file_url" 
                         class="w-full h-full object-cover"
                         :alt="media.file_name || 'Media'" />
                    <video v-else
                           :src="media.file_url"
                           class="w-full h-full object-cover"></video>
                    
                    <button v-if="canEdit"
                            @click="removeMedia(media.id)"
                            class="absolute top-2 right-2 w-7 h-7 rounded-full bg-red-500 text-white opacity-0 group-hover:opacity-100 transition flex items-center justify-center hover:bg-red-600">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </button>
                  </div>
                </div>

                <p v-else class="seed-body text-sm text-slate-400 text-center py-8 border-2 border-dashed border-slate-200 rounded-xl">
                  No media attached. Add photos or videos to make your seed more memorable.
                </p>
              </div>

            </div>

            <!-- Footer Actions -->
            <div class="px-6 md:px-8 py-5 bg-slate-50 border-t border-slate-200 flex items-center justify-between gap-4 flex-wrap">
              <p v-if="hasChanges && canEdit" class="seed-body text-sm text-amber-600 font-semibold">
                You have unsaved changes
              </p>
              <p v-else class="seed-body text-sm text-slate-500">
                {{ canEdit ? 'No changes made' : 'Editing disabled - too close to bloom time' }}
              </p>

              <div class="flex items-center gap-3">
                <button @click="handleCancel"
                        class="px-6 py-2.5 rounded-xl border border-slate-300 text-slate-700 seed-body font-semibold hover:bg-slate-100 transition">
                  Cancel
                </button>
                <button @click="handleSave"
                        :disabled="!hasChanges || !canEdit || isSaving"
                        class="px-6 py-2.5 rounded-xl bg-indigo-600 text-white seed-body font-semibold hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed">
                  {{ isSaving ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </div>
          </div>
        </template>

      </div>
    </div>
  </Sidebar>
</template>

<style scoped>
.seed-detail-page {
  background: linear-gradient(160deg, #f1f5f9 0%, #ffffff 50%, #f8fafc 100%);
}
.seed-display { font-family: 'Crimson Pro', Georgia, serif; font-weight: 500; }
.seed-body    { font-family: 'Inter', sans-serif; }
.seed-sub     { font-family: 'Inter', sans-serif; }

.loading-dot { 
  animation: dotPulse 1.2s ease-in-out infinite; 
}
@keyframes dotPulse { 
  0%,100% { opacity: 0.3; transform: scale(0.8); } 
  50% { opacity: 1; transform: scale(1.2); } 
}
</style>