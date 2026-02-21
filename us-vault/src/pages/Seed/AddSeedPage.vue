<script setup>
import { ref, computed } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import { Flower, Flower2 } from 'lucide-vue-next'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'

// ─── Form State ────────────────────────────────────────────────────────────────
const title = ref('')
const content = ref('')
const bloomAt = ref('')
const mediaFile = ref(null)
const mediaPreviewUrl = ref(null)
const mediaType = ref('') // 'image' | 'video'
const videoMuted = ref(true)
const videoRef = ref(null)
const fileInputRef = ref(null)
const isDragging = ref(false)

// ─── Toast State ───────────────────────────────────────────────────────────────
const toast = ref({ visible: false, message: '', type: 'success' })

// ─── Date Picker State ─────────────────────────────────────────────────────────
const showDatePicker = ref(false)
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth())
const selectedDay = ref(null)
const selectedHour = ref(12)
const selectedMinute = ref(0)
const pickerStep = ref('date') // 'date' | 'time'

const monthNames = [
  'January','February','March','April','May','June',
  'July','August','September','October','November','December'
]
const dayNames = ['Su','Mo','Tu','We','Th','Fr','Sa']

const today = new Date()
today.setHours(0, 0, 0, 0)

// ─── Date Picker Computed ──────────────────────────────────────────────────────
const calendarDays = computed(() => {
  const firstDay = new Date(selectedYear.value, selectedMonth.value, 1).getDay()
  const daysInMonth = new Date(selectedYear.value, selectedMonth.value + 1, 0).getDate()
  const cells = []
  for (let i = 0; i < firstDay; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)
  return cells
})

const isDayDisabled = (day) => {
  if (!day) return false
  const d = new Date(selectedYear.value, selectedMonth.value, day)
  d.setHours(0, 0, 0, 0)
  return d <= today
}

const isDaySelected = (day) => day === selectedDay.value

const selectDay = (day) => {
  if (!day || isDayDisabled(day)) return
  selectedDay.value = day
}

const prevMonth = () => {
  if (selectedMonth.value === 0) { selectedMonth.value = 11; selectedYear.value-- }
  else selectedMonth.value--
}

const nextMonth = () => {
  if (selectedMonth.value === 11) { selectedMonth.value = 0; selectedYear.value++ }
  else selectedMonth.value++
}

const confirmDate = () => {
  if (!selectedDay.value) return
  pickerStep.value = 'time'
}

const confirmTime = () => {
  const d = new Date(selectedYear.value, selectedMonth.value, selectedDay.value, selectedHour.value, selectedMinute.value)
  bloomAt.value = d.toISOString()
  showDatePicker.value = false
  pickerStep.value = 'date'
}

const formattedBloomAt = computed(() => {
  if (!bloomAt.value) return ''
  const d = new Date(bloomAt.value)
  return d.toLocaleString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric',
    hour: 'numeric', minute: '2-digit', hour12: true
  })
})

const hoursArr = Array.from({ length: 24 }, (_, i) => i)
const minutesArr = Array.from({ length: 60 }, (_, i) => i)

// ─── Media Handling ────────────────────────────────────────────────────────────
const MAX_IMAGE_MB = 10
const MAX_VIDEO_MB = 50
const mediaError = ref('')

const handleFileSelect = (file) => {
  if (!file) return
  mediaError.value = ''
  const isImage = file.type.startsWith('image/')
  const isVideo = file.type.startsWith('video/')

  if (!isImage && !isVideo) {
    mediaError.value = 'Only images and videos are supported.'
    return
  }

  const sizeMB = file.size / (1024 * 1024)
  if (isImage && sizeMB > MAX_IMAGE_MB) {
    mediaError.value = `Image exceeds ${MAX_IMAGE_MB}MB limit.`
    return
  }
  if (isVideo && sizeMB > MAX_VIDEO_MB) {
    mediaError.value = `Video exceeds ${MAX_VIDEO_MB}MB limit.`
    return
  }

  mediaFile.value = file
  mediaType.value = isImage ? 'image' : 'video'
  mediaPreviewUrl.value = URL.createObjectURL(file)
  videoMuted.value = true
}

const onFileInputChange = (e) => handleFileSelect(e.target.files[0])

const onDrop = (e) => {
  e.preventDefault()
  isDragging.value = false
  handleFileSelect(e.dataTransfer.files[0])
}

const removeMedia = () => {
  mediaFile.value = null
  mediaPreviewUrl.value = null
  mediaType.value = ''
  mediaError.value = ''
  if (fileInputRef.value) fileInputRef.value.value = ''
}

const toggleVideoMute = () => {
  videoMuted.value = !videoMuted.value
  if (videoRef.value) videoRef.value.muted = videoMuted.value
}

// ─── Toast Helper ──────────────────────────────────────────────────────────────
const showToast = (message, type = 'success') => {
  toast.value = { visible: true, message, type }
  setTimeout(() => { toast.value.visible = false }, 4000)
}

// ─── Submit ────────────────────────────────────────────────────────────────────
const isSubmitting = ref(false)

const handleSubmit = async () => {
  if (!title.value.trim() || !bloomAt.value) {
    showToast('Please fill in all required fields.', 'error')
    return
  }

  isSubmitting.value = true

  const seedPayload = {
    title: title.value,
    content: content.value,
    bloom_at: bloomAt.value
  }

  // Step 1: Create Seed
  console.log('Creating seed:', seedPayload)
  await new Promise(resolve => setTimeout(resolve, 1200))
  const fakeSeedId = 'seed_' + Math.random().toString(36).substr(2, 9)
  showToast('🌱 Seed planted! Adding media...')

  // Step 2: Upload Media (if any)
  if (mediaFile.value) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const mediaPayload = {
        seed_id: fakeSeedId,
        file: e.target.result
      }
      console.log('Uploading media for seed:', fakeSeedId, '| File type:', mediaFile.value.type, '| Size:', (mediaFile.value.size / 1024 / 1024).toFixed(2) + 'MB')
      console.log('Media payload (truncated):', { seed_id: mediaPayload.seed_id, file: '[base64 data]' })
      showToast('🌸 Seed fully planted! Your memory will bloom in time.')
    }
    reader.readAsDataURL(mediaFile.value)
  } else {
    showToast('🌸 Seed planted! Your memory will bloom in time.')
  }

  // Reset
  title.value = ''
  content.value = ''
  bloomAt.value = ''
  removeMedia()
  isSubmitting.value = false
}
</script>

<template>
  <InactivityOverlay>
        <Sidebar>
      <div class="add-seed-page min-h-screen relative overflow-x-hidden">

        <!-- Toast -->
        <Transition name="toast-slide">
          <div
            v-if="toast.visible"
            :class="[
              'fixed top-6 right-6 z-50 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 max-w-sm',
              toast.type === 'success' ? 'bg-purple-900 text-white border border-purple-500' : 'bg-red-900 text-white border border-red-500'
            ]"
          >
            <span class="text-lg">{{ toast.type === 'success' ? '✦' : '⚠' }}</span>
            <p class="text-sm font-medium">{{ toast.message }}</p>
          </div>
        </Transition>

        <!-- ── Decorative SVG Flora Layer ─────────────────────────── -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <!-- Large blooming SVG top-right -->
          <svg class="absolute -top-10 -right-16 w-80 opacity-15" viewBox="0 0 300 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(150,150)">
              <ellipse rx="18" ry="60" fill="#a855f7" transform="rotate(0)"/>
              <ellipse rx="18" ry="60" fill="#c084fc" transform="rotate(45)"/>
              <ellipse rx="18" ry="60" fill="#a855f7" transform="rotate(90)"/>
              <ellipse rx="18" ry="60" fill="#c084fc" transform="rotate(135)"/>
              <circle r="22" fill="#fbbf24"/>
            </g>
          </svg>

          <!-- Stem + bud bottom-left -->
          <svg class="absolute bottom-10 -left-8 w-40 opacity-20" viewBox="0 0 120 300" fill="none">
            <path d="M60 300 Q50 200 60 150 Q70 100 60 0" stroke="#7e22ce" stroke-width="3" fill="none"/>
            <ellipse cx="60" cy="80" rx="12" ry="20" fill="#c084fc" transform="rotate(-30 60 80)"/>
            <ellipse cx="60" cy="80" rx="12" ry="20" fill="#a855f7" transform="rotate(30 60 80)"/>
            <circle cx="60" cy="60" r="10" fill="#fde68a"/>
            <ellipse cx="30" cy="160" rx="22" ry="10" fill="#86efac" transform="rotate(-20 30 160)"/>
            <ellipse cx="90" cy="200" rx="22" ry="10" fill="#86efac" transform="rotate(20 90 200)"/>
          </svg>

          <!-- Tiny scattered petals -->
          <svg class="absolute top-1/3 left-8 w-16 opacity-20" viewBox="0 0 80 80">
            <ellipse cx="40" cy="40" rx="8" ry="25" fill="#e879f9" transform="rotate(20 40 40)"/>
            <ellipse cx="40" cy="40" rx="8" ry="25" fill="#c084fc" transform="rotate(80 40 40)"/>
            <circle cx="40" cy="40" r="7" fill="#fbbf24"/>
          </svg>

          <svg class="absolute top-20 left-1/3 w-10 opacity-10" viewBox="0 0 80 80">
            <ellipse cx="40" cy="40" rx="8" ry="25" fill="#e879f9" transform="rotate(50 40 40)"/>
            <ellipse cx="40" cy="40" rx="8" ry="25" fill="#a855f7" transform="rotate(110 40 40)"/>
            <circle cx="40" cy="40" r="6" fill="#fde68a"/>
          </svg>

          <!-- Vine right middle -->
          <svg class="absolute top-1/2 -right-4 w-24 opacity-15" viewBox="0 0 80 300">
            <path d="M40 0 Q20 50 40 100 Q60 150 40 200 Q20 250 40 300" stroke="#7c3aed" stroke-width="2.5" fill="none"/>
            <ellipse cx="25" cy="80" rx="16" ry="8" fill="#86efac" transform="rotate(-25 25 80)"/>
            <ellipse cx="55" cy="160" rx="16" ry="8" fill="#86efac" transform="rotate(25 55 160)"/>
            <ellipse cx="25" cy="240" rx="14" ry="7" fill="#86efac" transform="rotate(-20 25 240)"/>
          </svg>

          <!-- Seed icon top-left area -->
          <svg class="absolute top-32 left-24 w-12 opacity-20" viewBox="0 0 60 60">
            <ellipse cx="30" cy="30" rx="14" ry="22" fill="#a855f7" transform="rotate(-20 30 30)"/>
            <path d="M30 52 Q30 60 35 65" stroke="#7e22ce" stroke-width="2" fill="none"/>
          </svg>

          <!-- Sparkle dots -->
          <div class="absolute top-12 right-1/3 w-2 h-2 rounded-full bg-fuchsia-300 opacity-40"></div>
          <div class="absolute top-40 left-1/4 w-1.5 h-1.5 rounded-full bg-purple-400 opacity-30"></div>
          <div class="absolute bottom-32 right-1/4 w-2 h-2 rounded-full bg-amber-300 opacity-40"></div>
          <div class="absolute bottom-20 left-1/3 w-1 h-1 rounded-full bg-fuchsia-500 opacity-50"></div>
        </div>

        <!-- ── Main Content ─────────────────────────────────────────── -->
        <div class="relative z-10 max-w-3xl mx-auto px-4 sm:px-8 py-12">

          <!-- Header -->
          <div class="mb-12 text-center">
            <div class="inline-flex items-center gap-3 mb-4">
              <!-- Seed icon -->
              <svg width="36" height="36" viewBox="0 0 60 60" class="opacity-80">
                <ellipse cx="30" cy="34" rx="16" ry="22" fill="#7c3aed"/>
                <ellipse cx="30" cy="34" rx="10" ry="16" fill="#a855f7" opacity="0.5"/>
                <path d="M30 56 Q28 62 26 70" stroke="#5b21b6" stroke-width="2.5" fill="none" stroke-linecap="round"/>
              </svg>
              <h1 class="text-4xl font-bold tracking-tight text-gray-900" style="font-family: 'Barlow Semi Condensed', sans-serif; letter-spacing: -0.01em;">
                Plant a Seed
              </h1>
            </div>

            <!-- Explainer card -->
            <div class="relative bg-gradient-to-br from-purple-50 to-fuchsia-50 border border-purple-100 rounded-2xl px-8 py-6 text-left shadow-sm overflow-hidden">
              <div class="absolute top-0 right-0 w-32 h-32 opacity-10">
                <svg viewBox="0 0 100 100"><g transform="translate(50,50)"><ellipse rx="14" ry="44" fill="#7c3aed" transform="rotate(0)"/><ellipse rx="14" ry="44" fill="#a855f7" transform="rotate(60)"/><ellipse rx="14" ry="44" fill="#7c3aed" transform="rotate(120)"/><circle r="14" fill="#fbbf24"/></g></svg>
              </div>
              <div class="flex gap-4 items-start">
                <div class="mt-0.5 w-9 h-9 rounded-xl bg-purple-100 flex items-center justify-center flex-shrink-0">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                </div>
                <div>
                  <p class="text-sm font-semibold text-purple-900 mb-1">What is a Seed?</p>
                  <p class="text-sm text-gray-600 leading-relaxed">
                    A seed is a hidden memory — a message, moment, or feeling you plant today that your partner won't see until it's time to bloom.
                    It stays quietly tucked away, invisible to them, until the bloom date you choose arrives.
                    On that day, it surfaces as a memory — like a letter from your past self, finally ready to be read.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- ── Form ──────────────────────────────────────────────── -->
          <form @submit.prevent="handleSubmit" class="space-y-7">

            <!-- Title -->
            <div class="form-group">
              <label class="seed-label block text-sm font-semibold text-gray-700 mb-2">Seed Title <span class="text-fuchsia-500">*</span></label>
              <div class="relative">
                <input
                  v-model="title"
                  type="text"
                  placeholder="Give your seed a name..."
                  maxlength="120"
                  required
                  class="seed-input"
                />
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400">{{ title.length }}/120</span>
              </div>
            </div>

            <!-- Content -->
            <div class="form-group">
              <label class="seed-label block text-sm font-semibold text-gray-700 mb-2">Message <span class="text-gray-400 font-normal text-xs">(optional)</span></label>
              <textarea
                v-model="content"
                placeholder="Write what you want them to find when it blooms..."
                rows="5"
                class="seed-input resize-none"
              ></textarea>
            </div>

            <!-- Bloom At - Custom Date Picker -->
            <div class="form-group">
              <label class="seed-label block text-sm font-semibold text-gray-700 mb-2">Bloom Date & Time <span class="text-fuchsia-500">*</span></label>
              <p class="text-xs text-gray-400 mb-2">Choose a future date — this seed cannot bloom today.</p>

              <button
                type="button"
                @click="showDatePicker = !showDatePicker"
                class="w-full px-4 py-3 rounded-xl border border-gray-200 text-sm text-gray-800 bg-white transition-all duration-200 outline-none text-left flex items-center justify-between gap-2 cursor-pointer "
              >
                <span :class="bloomAt ? 'text-gray-800' : 'text-gray-400'">
                  {{ bloomAt ? formattedBloomAt : 'Choose when this seed will bloom...' }}
                </span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-purple-400 flex-shrink-0">
                  <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </button>

              <!-- Date Picker Dropdown -->
              <Transition name="picker-drop">
                <div v-if="showDatePicker" class="mt-3 bg-white rounded-2xl shadow-2xl border border-purple-100 overflow-hidden">

                  <!-- Step: Date -->
                  <div v-if="pickerStep === 'date'" class="p-5">
                    <!-- Month Nav -->
                    <div class="flex items-center justify-between mb-5">
                      <button type="button" @click="prevMonth" class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-500 hover:bg-purple-50 hover:text-purple-700 transition-all">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                      </button>
                      <span class="font-semibold text-gray-800 text-sm">{{ monthNames[selectedMonth] }} {{ selectedYear }}</span>
                      <button type="button" @click="nextMonth" class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-500 hover:bg-purple-50 hover:text-purple-700 transition-all">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
                      </button>
                    </div>

                    <!-- Day Headers -->
                    <div class="grid grid-cols-7 mb-2">
                      <div v-for="d in dayNames" :key="d" class="text-center text-xs font-medium text-gray-400 py-1">{{ d }}</div>
                    </div>

                    <!-- Days -->
                    <div class="grid grid-cols-7 gap-1">
                      <div
                        v-for="(day, idx) in calendarDays"
                        :key="idx"
                        @click="selectDay(day)"
                        :class="[
                          'h-9 w-9 mx-auto flex items-center justify-center rounded-xl text-sm transition-all',
                          !day ? '' :
                          isDayDisabled(day) ? 'text-gray-300 cursor-not-allowed' :
                          isDaySelected(day) ? 'bg-purple-700 text-white font-bold cursor-pointer shadow-md' :
                          'text-gray-700 hover:bg-purple-50 cursor-pointer hover:text-purple-800 font-medium'
                        ]"
                      >
                        {{ day || '' }}
                      </div>
                    </div>

                    <button
                      type="button"
                      @click="confirmDate"
                      :disabled="!selectedDay"
                      :class="[
                        'mt-5 w-full py-2.5 rounded-xl text-sm font-semibold transition-all',
                        selectedDay ? 'bg-purple-700 text-white hover:bg-purple-800 shadow' : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      ]"
                    >
                      Set Time →
                    </button>
                  </div>

                  <!-- Step: Time -->
                  <div v-else class="p-5">
                    <div class="flex items-center gap-3 mb-5">
                      <button type="button" @click="pickerStep = 'date'" class=" w-8 h-8 flex items-center justify-center rounded-lg text-gray-500 hover:bg-purple-50 hover:text-purple-700 transition-all">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
                      </button>
                      <span class="font-semibold text-gray-800 text-sm">
                        {{ monthNames[selectedMonth] }} {{ selectedDay }}, {{ selectedYear }}
                      </span>
                    </div>

                    <div class="flex gap-4 justify-center mb-6">
                      <!-- Hour -->
                      <div class="flex flex-col items-center gap-2">
                        <label class="text-xs text-gray-500 font-medium uppercase tracking-wide">Hour</label>
                        <select v-model="selectedHour" class="time-select">
                          <option v-for="h in hoursArr" :key="h" :value="h">{{ String(h).padStart(2,'0') }}</option>
                        </select>
                      </div>
                      <div class="flex items-center text-2xl font-bold text-purple-700 mt-5">:</div>
                      <!-- Minute -->
                      <div class="flex flex-col items-center gap-2">
                        <label class="text-xs text-gray-500 font-medium uppercase tracking-wide">Minute</label>
                        <select v-model="selectedMinute" class="time-select border border-gray-200 rounded-xl px-4 py-2 text-lg font-bold text-purple-800 text-center outline-none cursor-pointer">
                          <option v-for="m in minutesArr" :key="m" :value="m">{{ String(m).padStart(2,'0') }}</option>
                        </select>
                      </div>
                    </div>

                    <button
                      type="button"
                      @click="confirmTime"
                      class="w-full py-2.5 rounded-xl text-sm font-semibold bg-purple-700 text-white hover:bg-purple-800 transition shadow"
                    >
                      Confirm Bloom Time 🌸
                    </button>
                  </div>
                </div>
              </Transition>
            </div>

            <!-- Media Upload -->
            <div class="form-group">
              <label class="seed-label block text-sm font-semibold text-gray-700 mb-2">Attach a Memory <span class="text-gray-400 font-normal text-xs">(optional)</span></label>
              
              <!-- Limits notice -->
              <div class="flex gap-4 mb-3">
                <div class="flex items-center gap-1.5 text-xs text-gray-500">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                  Image: up to 10 MB
                </div>
                <div class="flex items-center gap-1.5 text-xs text-gray-500">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                  Video: up to 50 MB
                </div>
              </div>

              <!-- Error -->
              <p v-if="mediaError" class="text-xs text-red-500 mb-2 flex items-center gap-1">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {{ mediaError }}
              </p>

              <!-- Drop zone (only if no file yet) -->
              <div
                v-if="!mediaFile"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop="onDrop"
                @click="fileInputRef?.click()"
                :class="[
                  'relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200',
                  isDragging ? 'border-purple-500 bg-purple-50' : 'border-gray-200 hover:border-purple-400 hover:bg-purple-50/50'
                ]"
              >
                <input ref="fileInputRef" type="file" accept="image/*,video/*" class="hidden" @change="onFileInputChange"/>
                <div class="flex flex-col items-center gap-3 text-gray-400">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="text-purple-300">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
                  </svg>
                  <span class="text-sm font-medium text-purple-500">Drop your image or video here</span>
                  <span class="text-xs">or click to browse</span>
                </div>
              </div>

              <!-- Preview -->
              <div v-else class="relative rounded-2xl overflow-hidden border border-purple-100 shadow-sm bg-black">
                <!-- Remove button -->
                <button
                  type="button"
                  @click="removeMedia"
                  class="absolute top-3 left-3 z-20 w-8 h-8 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition"
                  title="Remove media"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>

                <!-- Image preview -->
                <img
                  v-if="mediaType === 'image'"
                  :src="mediaPreviewUrl"
                  alt="Preview"
                  class="w-full max-h-72 object-contain bg-black"
                />

                <!-- Video preview -->
                <div v-else class="relative">
                  <video
                    ref="videoRef"
                    :src="mediaPreviewUrl"
                    autoplay
                    loop
                    muted
                    playsinline
                    class="w-full max-h-72 object-contain"
                  ></video>

                  <!-- Mute toggle -->
                  <button
                    type="button"
                    @click="toggleVideoMute"
                    class="absolute top-3 right-3 z-20 w-9 h-9 rounded-full bg-black/60 hover:bg-black/80 flex items-center justify-center text-white transition"
                    :title="videoMuted ? 'Unmute' : 'Mute'"
                  >
                    <!-- Muted icon -->
                    <svg v-if="videoMuted" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                      <line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/>
                    </svg>
                    <!-- Unmuted icon -->
                    <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                      <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
                    </svg>
                  </button>
                </div>

                <!-- File info bar -->
                <div class="bg-purple-900/90 px-4 py-2 flex items-center justify-between">
                  <span class="text-xs text-purple-200 truncate max-w-[70%]">{{ mediaFile.name }}</span>
                  <span class="text-xs text-purple-300">{{ (mediaFile.size / 1024 / 1024).toFixed(1) }} MB</span>
                </div>
              </div>
            </div>

            <!-- Submit -->
            <div class="pt-2">
              <button
                type="submit"
                :disabled="isSubmitting"
                class="w-full relative overflow-hidden py-4 rounded-2xl font-bold text-white text-base tracking-wide transition-all duration-200 shadow-lg"
                style="background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%); font-family: 'Barlow Semi Condensed', sans-serif; letter-spacing: 0.05em;"
                :style="isSubmitting ? 'opacity: 0.7; cursor: not-allowed;' : 'opacity: 1; cursor: pointer;'"
              >
                <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
                  <Flower class="w-5 h-5 text-white animate-pulse" />
                  Plant This Seed
                </span>
                <span v-else class="flex items-center justify-center gap-2">
                  <svg class="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                  Planting...
                </span>
              </button>
              <p class="text-center text-xs text-gray-400 mt-3">
                This memory will remain hidden until it blooms.
              </p>
            </div>
          </form>
        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>

</template>

<!-- <style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Red+Hat+Text:wght@400;500;600;700&display=swap');
</style> -->

<style scoped>
.add-seed-page {
  background: linear-gradient(160deg, #faf5ff 0%, #ffffff 40%, #fdf4ff 100%);
}

.seed-label {
  font-family: 'Red Hat Text', sans-serif;
}

.seed-input {
  font-family: 'Red Hat Text', sans-serif;
}
/* .seed-input:focus {
  @apply border-purple-400 ring-2 ring-purple-100;
}
.seed-input::placeholder {
  @apply text-gray-400;
}
 */

.time-select {
  font-family: 'Red Hat Text', sans-serif;
  background: #faf5ff;
  appearance: none;
  min-width: 72px;
}
/* .time-select:focus {
  @apply border-purple-400 ring-2 ring-purple-100;
} */

/* Transitions */
.toast-slide-enter-active, .toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-slide-enter-from, .toast-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.95);
}

.picker-drop-enter-active, .picker-drop-leave-active {
  transition: all 0.25s ease;
}
.picker-drop-enter-from, .picker-drop-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>