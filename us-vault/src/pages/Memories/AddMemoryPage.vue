<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'

// ── State ─────────────────────────────────────────────────────────────────────
const title = ref('')
const content = ref('')
const memoryDate = ref(new Date().toISOString())
const mediaFile = ref(null)
const mediaPreviewUrl = ref(null)
const mediaType = ref('')
const videoMuted = ref(true)
const videoRef = ref(null)
const fileInputRef = ref(null)
const isDragging = ref(false)
const mediaError = ref('')
const isSubmitting = ref(false)
const previewOpen = ref(false) // mobile preview panel
const toast = ref({ visible: false, message: '', type: 'success' })

// Live clock
const liveTime = ref(new Date())
let clockInterval = null

// ── Live clock ────────────────────────────────────────────────────────────────
onMounted(() => {
  clockInterval = setInterval(() => {
    liveTime.value = new Date()
    memoryDate.value = liveTime.value.toISOString()
  }, 1000)
})
onUnmounted(() => clearInterval(clockInterval))

// ── Computed ──────────────────────────────────────────────────────────────────
const formattedLiveDate = computed(() =>
  liveTime.value.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })
)
const formattedLiveTime = computed(() =>
  liveTime.value.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
)
const previewDate = computed(() =>
  liveTime.value.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
)

// ── Media ─────────────────────────────────────────────────────────────────────
const MAX_IMAGE_MB = 10
const MAX_VIDEO_MB = 50

const handleFileSelect = (file) => {
  if (!file) return
  mediaError.value = ''
  const isImage = file.type.startsWith('image/')
  const isVideo = file.type.startsWith('video/')
  if (!isImage && !isVideo) { mediaError.value = 'Only images and videos are supported.'; return }
  const sizeMB = file.size / (1024 * 1024)
  if (isImage && sizeMB > MAX_IMAGE_MB) { mediaError.value = `Image exceeds ${MAX_IMAGE_MB}MB.`; return }
  if (isVideo && sizeMB > MAX_VIDEO_MB) { mediaError.value = `Video exceeds ${MAX_VIDEO_MB}MB.`; return }
  mediaFile.value = file
  mediaType.value = isImage ? 'image' : 'video'
  mediaPreviewUrl.value = URL.createObjectURL(file)
  videoMuted.value = true
}
const onFileInputChange = (e) => handleFileSelect(e.target.files[0])
const onDrop = (e) => { e.preventDefault(); isDragging.value = false; handleFileSelect(e.dataTransfer.files[0]) }
const removeMedia = () => {
  mediaFile.value = null; mediaPreviewUrl.value = null; mediaType.value = ''; mediaError.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
}
const toggleVideoMute = () => {
  videoMuted.value = !videoMuted.value
  if (videoRef.value) videoRef.value.muted = videoMuted.value
}

// ── Toast ─────────────────────────────────────────────────────────────────────
const showToast = (message, type = 'success') => {
  toast.value = { visible: true, message, type }
  setTimeout(() => { toast.value.visible = false }, 4000)
}

// ── Submit ────────────────────────────────────────────────────────────────────
const handleSubmit = async () => {
  if (!title.value.trim()) { showToast('Please give your memory a title.', 'error'); return }
  isSubmitting.value = true

  const memoryPayload = { title: title.value, content: content.value, memory_date: memoryDate.value }
  console.log('Creating memory:', memoryPayload)
  await new Promise(r => setTimeout(r, 1100))
  const fakeMemoryId = 'mem_' + Math.random().toString(36).substr(2, 9)
  showToast('✦ Memory captured! Adding media...')

  if (mediaFile.value) {
    const reader = new FileReader()
    reader.onload = (e) => {
      console.log('Uploading media for memory:', fakeMemoryId, '| Type:', mediaFile.value.type, '| Size:', (mediaFile.value.size / 1024 / 1024).toFixed(2) + 'MB')
      console.log('Media payload:', { memory_id: fakeMemoryId, file: '[base64 data]' })
      showToast('✦ Memory saved to your vault.')
    }
    reader.readAsDataURL(mediaFile.value)
  } else {
    showToast('✦ Memory saved to your vault.')
  }

  title.value = ''; content.value = ''; removeMedia()
  isSubmitting.value = false
}
</script>

<template>
  <InactivityOverlay>
        <Sidebar>
      <div class="memory-page min-h-screen relative overflow-x-hidden">

        <!-- Google Fonts -->
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Lato:wght@300;400;700&display=swap');
        </component>

        <!-- ── Toast ──────────────────────────────────────────────── -->
        <Transition name="toast-slide">
          <div v-if="toast.visible"
              :class="['fixed top-6 right-6 z-50 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 max-w-sm',
                        toast.type === 'success' ? 'bg-rose-900 text-white border border-rose-600' : 'bg-red-900 text-white border border-red-600']">
            <span>{{ toast.type === 'success' ? '✦' : '⚠' }}</span>
            <p class="text-sm font-medium mem-body">{{ toast.message }}</p>
          </div>
        </Transition>

        <!-- ── Background Decorations ─────────────────────────────── -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <!-- Warm gradient blobs -->
          <div class="absolute -top-20 -right-20 w-96 h-96 rounded-full opacity-20"
              style="background: radial-gradient(circle, #fecdd3 0%, transparent 70%);"></div>
          <div class="absolute top-1/2 -left-24 w-72 h-72 rounded-full opacity-15"
              style="background: radial-gradient(circle, #fbcfe8 0%, transparent 70%);"></div>
          <div class="absolute -bottom-12 right-1/3 w-80 h-80 rounded-full opacity-10"
              style="background: radial-gradient(circle, #ddd6fe 0%, transparent 70%);"></div>

          <!-- Polaroid-frame lines top-left -->
          <div class="absolute top-8 left-8 opacity-10">
            <div class="w-16 h-20 border-2 border-rose-400 rounded-sm rotate-[-8deg]"></div>
            <div class="w-14 h-18 border-2 border-pink-300 rounded-sm rotate-[4deg] -mt-16 ml-3"></div>
          </div>

          <!-- Ink-stroke swooshes -->
          <svg class="absolute top-0 left-1/4 w-48 opacity-8" viewBox="0 0 200 80" fill="none">
            <path d="M0,60 Q50,10 100,40 Q150,70 200,20" stroke="#f43f5e" stroke-width="1.5" fill="none" stroke-linecap="round"/>
            <path d="M10,70 Q60,20 110,50 Q160,80 200,30" stroke="#fb7185" stroke-width="0.8" fill="none" stroke-linecap="round" opacity="0.5"/>
          </svg>
          <svg class="absolute bottom-32 right-8 w-32 opacity-10" viewBox="0 0 150 60">
            <path d="M0,30 Q37,5 75,30 Q112,55 150,30" stroke="#f43f5e" stroke-width="1.5" fill="none" stroke-linecap="round"/>
          </svg>

          <!-- Floating constellation dots -->
          <div class="star star-1 absolute w-1 h-1 rounded-full bg-rose-300 opacity-60"></div>
          <div class="star star-2 absolute w-1.5 h-1.5 rounded-full bg-pink-400 opacity-40"></div>
          <div class="star star-3 absolute w-1 h-1 rounded-full bg-purple-300 opacity-50"></div>
          <div class="star star-4 absolute w-2 h-2 rounded-full bg-rose-200 opacity-35"></div>
          <div class="star star-5 absolute w-1 h-1 rounded-full bg-fuchsia-300 opacity-45"></div>

          <!-- Corner stamp decoration -->
          <div class="absolute bottom-8 left-8 opacity-8">
            <svg width="60" height="60" viewBox="0 0 60 60">
              <circle cx="30" cy="30" r="28" fill="none" stroke="#f43f5e" stroke-width="1" stroke-dasharray="4 3"/>
              <circle cx="30" cy="30" r="20" fill="none" stroke="#fb7185" stroke-width="0.6"/>
              <text x="30" y="34" text-anchor="middle" font-size="8" fill="#f43f5e" font-family="serif">MEMORY</text>
            </svg>
          </div>
        </div>

        <!-- ── Layout: Form + Preview ──────────────────────────────── -->
        <div class="relative z-10 flex min-h-screen">

          <!-- ── Form Column ─────────────────────────────────────── -->
          <div class="flex-1 max-w-2xl mx-auto px-4 sm:px-8 py-12 lg:mx-0 lg:max-w-none lg:w-0 lg:flex-[0_0_55%] xl:flex-[0_0_52%]">

            <!-- Header -->
            <div class="mb-10">
              <div class="flex items-center gap-3 mb-5">
                <!-- Polaroid icon -->
                <div class="relative w-12 h-14 bg-white rounded-sm shadow-md flex flex-col items-center justify-center border border-gray-100"
                    style="transform: rotate(-5deg); box-shadow: 0 3px 12px rgba(244,63,94,0.12);">
                  <div class="w-8 h-7 rounded-sm bg-gradient-to-br from-rose-100 to-pink-100 mb-1"></div>
                  <div class="w-6 h-0.5 bg-gray-200 rounded"></div>
                </div>
                <div>
                  <h1 class="mem-display text-4xl sm:text-5xl text-gray-900 leading-none">Add a Memory</h1>
                  <p class="mem-body text-rose-400 text-sm tracking-widest uppercase mt-1">Capture this moment</p>
                </div>
              </div>

              <!-- Live timestamp badge -->
              <div class="inline-flex items-center gap-3 px-4 py-3 rounded-2xl border border-rose-100 bg-rose-50">
                <div class="flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></span>
                  <span class="mem-body text-xs text-rose-600 font-semibold uppercase tracking-wider">Live</span>
                </div>
                <div class="w-px h-4 bg-rose-200"></div>
                <div class="mem-body text-sm text-gray-700">
                  <span class="font-semibold">{{ formattedLiveDate }}</span>
                  <span class="text-rose-500 ml-2 font-mono text-xs">{{ formattedLiveTime }}</span>
                </div>
              </div>
              <p class="mem-body text-xs text-gray-400 mt-2 ml-1">Memory time is always now — this moment, preserved as-is.</p>
            </div>

            <!-- ── Form ──────────────────────────────────────────── -->
            <form @submit.prevent="handleSubmit" class="space-y-6">

              <!-- Title -->
              <div>
                <label class="mem-label">Memory Title <span class="text-rose-400">*</span></label>
                <div class="relative">
                  <input v-model="title" type="text" placeholder="What is this moment called?"
                        maxlength="120" required
                        class="mem-input pr-16"
                        style="border-bottom: 2px solid #fecdd3; border-radius: 12px;"/>
                  <span class="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-300 mem-body">{{ title.length }}/120</span>
                </div>
              </div>

              <!-- Content -->
              <div>
                <label class="mem-label">Write it down <span class="text-gray-300 font-normal text-xs">(optional)</span></label>
                <textarea v-model="content"
                          placeholder="Describe what's happening, how you feel, what you want to remember..."
                          rows="6"
                          class="mem-input resize-none leading-relaxed"></textarea>
                <p class="mem-body text-xs text-gray-400 mt-1.5 ml-1">
                  {{ content.length > 0 ? content.length + ' characters' : 'No character limit — write as much as you need.' }}
                </p>
              </div>

              <!-- Media -->
              <div>
                <label class="mem-label">Attach Media <span class="text-gray-300 font-normal text-xs">(optional)</span></label>

                <!-- Limits -->
                <div class="flex gap-4 mb-3">
                  <div class="flex items-center gap-1.5 text-xs text-gray-400 mem-body">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                    Images up to 10 MB
                  </div>
                  <div class="flex items-center gap-1.5 text-xs text-gray-400 mem-body">
                    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                    Videos up to 50 MB
                  </div>
                </div>

                <p v-if="mediaError" class="text-xs text-red-500 mb-2 mem-body flex items-center gap-1">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                  {{ mediaError }}
                </p>

                <!-- Drop zone -->
                <div v-if="!mediaFile"
                    @dragover.prevent="isDragging = true"
                    @dragleave.prevent="isDragging = false"
                    @drop="onDrop"
                    @click="fileInputRef?.click()"
                    :class="['relative border-2 border-dashed rounded-2xl p-9 text-center cursor-pointer transition-all duration-200',
                              isDragging ? 'border-rose-400 bg-rose-50' : 'border-gray-200 hover:border-rose-300 hover:bg-rose-50/40']">
                  <input ref="fileInputRef" type="file" accept="image/*,video/*" class="hidden" @change="onFileInputChange"/>
                  <div class="flex flex-col items-center gap-3 text-gray-400">
                    <!-- Camera icon -->
                    <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-rose-300">
                      <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                      <circle cx="12" cy="13" r="4"/>
                    </svg>
                    <span class="text-sm font-medium text-rose-400 mem-body">Drop a photo or video here</span>
                    <span class="text-xs mem-body">or click to browse</span>
                  </div>
                </div>

                <!-- Preview -->
                <div v-else class="relative rounded-2xl overflow-hidden border border-rose-100 shadow-sm bg-black">
                  <button type="button" @click="removeMedia"
                          class="absolute top-3 left-3 z-20 w-8 h-8 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                  <img v-if="mediaType === 'image'" :src="mediaPreviewUrl" alt="Preview"
                      class="w-full max-h-64 object-contain bg-black"/>
                  <div v-else class="relative">
                    <video ref="videoRef" :src="mediaPreviewUrl" autoplay loop muted playsinline
                          class="w-full max-h-64 object-contain"></video>
                    <button type="button" @click="toggleVideoMute"
                            class="absolute top-3 right-3 z-20 w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition">
                      <svg v-if="videoMuted" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                        <line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/>
                      </svg>
                      <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                        <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                      </svg>
                    </button>
                  </div>
                  <div class="bg-rose-900/90 px-4 py-2 flex items-center justify-between">
                    <span class="text-xs text-rose-200 truncate max-w-[70%] mem-body">{{ mediaFile.name }}</span>
                    <span class="text-xs text-rose-300 mem-body">{{ (mediaFile.size / 1024 / 1024).toFixed(1) }} MB</span>
                  </div>
                </div>
              </div>

              <!-- Submit -->
              <div class="pt-2 pb-8">
                <button type="submit" :disabled="isSubmitting"
                        class="w-full relative overflow-hidden py-4 rounded-2xl font-bold text-white text-base tracking-wide transition-all duration-200 shadow-lg mem-display"
                        style="background: linear-gradient(135deg, #e11d48 0%, #f43f5e 40%, #db2777 100%); letter-spacing: 0.04em;"
                        :style="isSubmitting ? 'opacity:0.7;cursor:not-allowed;' : ''">
                  <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                    Save This Memory
                  </span>
                  <span v-else class="flex items-center justify-center gap-2">
                    <svg class="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                    Saving...
                  </span>
                </button>
                <p class="text-center text-xs text-gray-400 mt-3 mem-body">Both you and your partner will see this memory. </p>
              </div>
            </form>
          </div>

          <!-- ── Preview Column (Desktop) ───────────────────────── -->
          <div class="hidden lg:flex flex-[0_0_42%] xl:flex-[0_0_44%] items-start py-12 px-6 xl:px-10">
            <div class="sticky top-8 w-full">
              <!-- Preview header -->
              <div class="flex items-center gap-2 mb-5">
                <div class="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></div>
                <span class="mem-body text-xs text-gray-400 uppercase tracking-widest">Live Preview</span>
              </div>

              <!-- Memory Card Preview -->
              <div class="memory-preview-card relative bg-white rounded-3xl overflow-hidden"
                  style="box-shadow: 0 20px 60px rgba(244,63,94,0.10), 0 4px 20px rgba(0,0,0,0.06);">

                <!-- Polaroid top bar -->
                <div class="h-1 w-full" style="background: linear-gradient(90deg, #f43f5e, #db2777, #7c3aed);"></div>

                <!-- Media area -->
                <div class="relative bg-gradient-to-br from-rose-50 to-pink-50 flex items-center justify-center overflow-hidden"
                    style="min-height: 200px;">
                  <img v-if="mediaType === 'image' && mediaPreviewUrl" :src="mediaPreviewUrl"
                      class="w-full object-cover" style="max-height: 220px;"/>
                  <video v-else-if="mediaType === 'video' && mediaPreviewUrl"
                        :src="mediaPreviewUrl" autoplay loop muted playsinline
                        class="w-full object-cover" style="max-height: 220px;"></video>
                  <div v-else class="flex flex-col items-center gap-3 py-12 text-rose-200">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                      <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                      <circle cx="12" cy="13" r="4"/>
                    </svg>
                    <span class="text-xs mem-body text-rose-300">Photo or video will appear here</span>
                  </div>

                  <!-- Date stamp overlay -->
                  <div class="absolute bottom-3 right-3 px-2 py-1 rounded-lg bg-black/40 backdrop-blur-sm">
                    <span class="text-white font-mono text-xs">{{ previewDate }}</span>
                  </div>
                </div>

                <!-- Card body -->
                <div class="p-5">
                  <!-- Title -->
                  <h3 class="mem-display text-xl text-gray-900 mb-2 leading-snug"
                      :class="title ? 'text-gray-900' : 'text-gray-300'">
                    {{ title || 'Your memory title...' }}
                  </h3>

                  <!-- Divider with heart -->
                  <div class="flex items-center gap-2 my-3">
                    <div class="flex-1 h-px bg-rose-100"></div>
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="#fca5a5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                    <div class="flex-1 h-px bg-rose-100"></div>
                  </div>

                  <!-- Content -->
                  <p class="mem-body text-sm leading-relaxed"
                    :class="content ? 'text-gray-600' : 'text-gray-300'">
                    {{ content || 'Your note will appear here...' }}
                  </p>

                  <!-- Footer meta -->
                  <div class="mt-4 pt-4 border-t border-gray-50 flex items-center justify-between">
                    <div class="flex items-center gap-1.5">
                      <div class="w-5 h-5 rounded-full bg-gradient-to-br from-rose-400 to-pink-500 flex items-center justify-center">
                        <span class="text-white text-xs font-bold">Y</span>
                      </div>
                      <span class="mem-body text-xs text-gray-400">You</span>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <span v-if="mediaFile"
                            class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs mem-body"
                            :class="mediaType === 'image' ? 'bg-blue-50 text-blue-500' : 'bg-rose-50 text-rose-500'">
                        <svg v-if="mediaType === 'image'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                        <svg v-else width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                        {{ mediaType }}
                      </span>
                      <span class="mem-body text-xs text-gray-400">{{ formattedLiveTime.split(':').slice(0,2).join(':') }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Hint -->
              <p class="text-center text-xs text-gray-300 mt-4 mem-body">This is how your memory will appear in the vault.</p>
            </div>
          </div>
        </div>

        <!-- ── Mobile Preview Drawer ──────────────────────────────── -->
        <div class="lg:hidden fixed right-0 top-1/2 -translate-y-1/2 z-40" style="pointer-events: all;">
          <!-- Pull tab -->
          <button @click="previewOpen = !previewOpen"
                  class="absolute -left-10 top-1/2 -translate-y-1/2 w-10 h-16 bg-white border border-rose-200 rounded-l-2xl shadow-lg flex flex-col items-center justify-center gap-1 transition-all duration-300 hover:bg-rose-50"
                  style="box-shadow: -4px 0 20px rgba(244,63,94,0.1);">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5" stroke-linecap="round"
                :style="previewOpen ? 'transform:rotate(180deg)' : ''" class="transition-transform duration-300">
              <polyline points="15 18 9 12 15 6"/>
            </svg>
            <span class="text-rose-400 text-xs mem-body" style="writing-mode: vertical-rl; transform: rotate(180deg); font-size: 9px; letter-spacing: 0.1em; text-transform: uppercase;">Preview</span>
          </button>

          <!-- Drawer Panel -->
          <Transition name="drawer-slide">
            <div v-if="previewOpen"
                class="w-72 sm:w-80 bg-white/95 backdrop-blur-md rounded-l-3xl shadow-2xl border-l border-t border-b border-rose-100 overflow-y-auto"
                style="max-height: 80vh; box-shadow: -12px 0 40px rgba(244,63,94,0.12);">

              <div class="p-4">
                <div class="flex items-center justify-between mb-4">
                  <span class="mem-body text-xs text-gray-400 uppercase tracking-widest flex items-center gap-1.5">
                    <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                    Live Preview
                  </span>
                  <button @click="previewOpen = false" class="text-gray-400 hover:text-gray-600 transition">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>

                <!-- Mini card -->
                <div class="bg-white rounded-2xl overflow-hidden border border-rose-50"
                    style="box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
                  <div class="h-0.5 w-full" style="background: linear-gradient(90deg, #f43f5e, #db2777, #7c3aed);"></div>
                  <div class="relative bg-gradient-to-br from-rose-50 to-pink-50 flex items-center justify-center overflow-hidden" style="min-height: 140px;">
                    <img v-if="mediaType === 'image' && mediaPreviewUrl" :src="mediaPreviewUrl" class="w-full object-cover" style="max-height:160px;"/>
                    <video v-else-if="mediaType === 'video' && mediaPreviewUrl" :src="mediaPreviewUrl" autoplay loop muted playsinline class="w-full object-cover" style="max-height:160px;"></video>
                    <div v-else class="py-8 text-rose-200 flex flex-col items-center gap-2">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                      <span class="text-xs mem-body text-rose-300">No media yet</span>
                    </div>
                    <div class="absolute bottom-2 right-2 px-1.5 py-0.5 rounded bg-black/40">
                      <span class="text-white font-mono text-xs">{{ previewDate }}</span>
                    </div>
                  </div>
                  <div class="p-4">
                    <h3 class="mem-display text-base text-gray-900 mb-2 leading-snug" :class="!title ? 'text-gray-300' : ''">
                      {{ title || 'Your memory title...' }}
                    </h3>
                    <p class="mem-body text-xs leading-relaxed" :class="content ? 'text-gray-500' : 'text-gray-300'">
                      {{ content ? (content.length > 100 ? content.slice(0, 100) + '…' : content) : 'Your note...' }}
                    </p>
                    <div class="mt-3 pt-3 border-t border-gray-50 flex items-center justify-between">
                      <div class="flex items-center gap-1">
                        <div class="w-4 h-4 rounded-full bg-gradient-to-br from-rose-400 to-pink-500 flex items-center justify-center">
                          <span class="text-white" style="font-size:8px; font-weight:700;">Y</span>
                        </div>
                        <span class="mem-body text-xs text-gray-400">You</span>
                      </div>
                      <span class="mem-body text-xs text-gray-300">{{ formattedLiveTime.split(':').slice(0,2).join(':') }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>

      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
.memory-page {
  background: linear-gradient(160deg, #fff5f6 0%, #ffffff 45%, #fdf4ff 100%);
}

.mem-display {
  font-family: 'Playfair Display', Georgia, serif;
}

.mem-body {
  font-family: 'Lato', sans-serif;
}

.mem-label {
  font-family: 'Lato', sans-serif;
  font-size: 0.8125rem;
  font-weight: 700;
  color: #374151;
  display: block;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.mem-input {
  font-family: 'Lato', sans-serif;
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1.5px solid #fce7f3;
  font-size: 0.9375rem;
  color: #1f2937;
  background: #ffffff;
  transition: all 0.2s ease;
  outline: none;
}

.mem-input:focus {
  border-color: #fb7185;
  box-shadow: 0 0 0 3px rgba(251,113,133,0.1);
}

.mem-input::placeholder {
  color: #d1d5db;
  font-style: italic;
}

/* Constellation stars */
.star { border-radius: 50%; }
.star-1 { top: 18%; left: 18%; }
.star-2 { top: 35%; right: 22%; }
.star-3 { bottom: 40%; left: 30%; }
.star-4 { top: 60%; left: 8%; }
.star-5 { bottom: 25%; right: 15%; }

/* Floating animation for stars */
.star-1 { animation: twinkle 4s ease-in-out infinite; }
.star-2 { animation: twinkle 5s ease-in-out infinite 1s; }
.star-3 { animation: twinkle 3.5s ease-in-out infinite 2s; }
.star-4 { animation: twinkle 6s ease-in-out infinite 0.5s; }
.star-5 { animation: twinkle 4.5s ease-in-out infinite 1.5s; }

@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.4); }
}

/* Preview card hover */
.memory-preview-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.memory-preview-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 28px 70px rgba(244,63,94,0.14), 0 8px 24px rgba(0,0,0,0.07) !important;
}

/* Drawer transition */
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.25s ease;
}
.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* Toast */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-slide-enter-from,
.toast-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.95);
}
</style>