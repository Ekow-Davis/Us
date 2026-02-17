<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { Heart, Sparkles, Calendar, Clock } from 'lucide-vue-next';
import FlowerFieldOverlay from './FlowerFieldOverlay.vue';

// State
const upcomingBlooms = ref([]);
const recentMemories = ref([]);
const signalCount = ref(0);
const showFlowers = ref(false);
const currentTime = ref(new Date());

// Countdown state
const days = ref(0);
const hours = ref(0);
const minutes = ref(0);
const seconds = ref(0);

// Previous values for flip animation
const prevDays = ref(0);
const prevHours = ref(0);
const prevMinutes = ref(0);
const prevSeconds = ref(0);

// Flip animation triggers
const flipDays = ref(false);
const flipHours = ref(false);
const flipMinutes = ref(false);
const flipSeconds = ref(false);

// Mock data - replace with actual API calls
const loadDashboardData = () => {
  // Simulate API delay
  setTimeout(() => {
    // Mock blooms data (same structure as memories but with is_seed: true and bloom_date)
    upcomingBlooms.value = [
      {
        id: "bloom-001",
        vault_id: "vault-001",
        created_by: "user-001",
        title: "Birthday Surprise Gift",
        content: "A special moment we've been waiting for",
        memory_date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000 + 4 * 60 * 60 * 1000).toISOString(),
        bloom_date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000 + 4 * 60 * 60 * 1000).toISOString(),
        created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: true,
        media: []
      },
      {
        id: "bloom-002",
        vault_id: "vault-001",
        created_by: "user-001",
        title: "Summer Memory Lane",
        content: "Revisiting our favorite summer moments",
        memory_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        bloom_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: true,
        media: []
      },
      {
        id: "bloom-003",
        vault_id: "vault-001",
        created_by: "user-001",
        title: "Birthday Wishes",
        content: "A special birthday message",
        memory_date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
        bloom_date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
        created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: true,
        media: []
      }
    ];

    // Mock memories data
    recentMemories.value = [
      {
        id: "mem-001",
        vault_id: "vault-001",
        created_by: "user-001",
        title: "Our First Date at the Beach",
        content: "The sunset was beautiful that evening...",
        memory_date: "2024-01-15T18:30:00Z",
        created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: true,
        media: [
          {
            id: "media-001",
            file_url: "https://example.com/photo.jpg",
            file_type: "image/jpeg"
          }
        ]
      },
      {
        id: "mem-002",
        vault_id: "vault-001",
        created_by: "user-002",
        title: "Late Night Conversations",
        content: "We talked for hours about everything and nothing...",
        memory_date: "2024-01-08T23:45:00Z",
        created_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: true,
        media: []
      },
      {
        id: "mem-003",
        vault_id: "vault-001",
        created_by: "user-001",
        title: "Morning Coffee Together",
        content: "Started the day with your favorite brew",
        memory_date: "2024-01-01T08:00:00Z",
        created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
        edited_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(),
        is_seed: false,
        media: []
      }
    ];

    // Check for signals
    signalCount.value = 0; // Change to test flower overlay
  }, 800);
};

// Computed
const primaryBloom = computed(() => upcomingBlooms.value[0] || null);
const secondaryBlooms = computed(() => upcomingBlooms.value.slice(1, 3));

const updateCountdown = () => {
  if (!primaryBloom.value) {
    days.value = 0;
    hours.value = 0;
    minutes.value = 0;
    seconds.value = 0;
    return;
  }

  const now = new Date();
  const bloomDate = new Date(primaryBloom.value.bloom_date);
  const diff = bloomDate - now;

  if (diff <= 0) {
    days.value = 0;
    hours.value = 0;
    minutes.value = 0;
    seconds.value = 0;
    return;
  }

  const newDays = Math.floor(diff / (1000 * 60 * 60 * 24));
  const newHours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const newMinutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const newSeconds = Math.floor((diff % (1000 * 60)) / 1000);

  // Trigger flip animations
  if (newDays !== days.value) {
    prevDays.value = days.value;
    flipDays.value = true;
    setTimeout(() => { flipDays.value = false; }, 600);
  }
  if (newHours !== hours.value) {
    prevHours.value = hours.value;
    flipHours.value = true;
    setTimeout(() => { flipHours.value = false; }, 600);
  }
  if (newMinutes !== minutes.value) {
    prevMinutes.value = minutes.value;
    flipMinutes.value = true;
    setTimeout(() => { flipMinutes.value = false; }, 600);
  }
  if (newSeconds !== seconds.value) {
    prevSeconds.value = seconds.value;
    flipSeconds.value = true;
    setTimeout(() => { flipSeconds.value = false; }, 600);
  }

  days.value = newDays;
  hours.value = newHours;
  minutes.value = newMinutes;
  seconds.value = newSeconds;
};

const getCountdown = (bloomDateStr) => {
  const now = currentTime.value;
  const bloomDate = new Date(bloomDateStr);
  const diff = bloomDate - now;
  
  if (diff <= 0) return "Blooming now";
  
  const d = Math.floor(diff / (1000 * 60 * 60 * 24));
  const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  
  if (d > 0) {
    return `${d} day${d !== 1 ? 's' : ''} ${h} hour${h !== 1 ? 's' : ''}`;
  } else if (h > 0) {
    return `${h} hour${h !== 1 ? 's' : ''} ${m} minute${m !== 1 ? 's' : ''}`;
  } else {
    return `${m} minute${m !== 1 ? 's' : ''}`;
  }
};

const getBloomProgress = (bloomDateStr) => {
  const now = currentTime.value;
  const bloomDate = new Date(bloomDateStr);
  const diff = bloomDate - now;
  
  const maxTime = 30 * 24 * 60 * 60 * 1000;
  const progress = Math.max(0, Math.min(100, ((maxTime - diff) / maxTime) * 100));
  return progress;
};

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const options = { month: 'short', day: 'numeric', year: 'numeric' };
  return date.toLocaleDateString('en-US', options);
};

const formatMemoryDate = (dateStr) => {
  const date = new Date(dateStr);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) !== 1 ? 's' : ''} ago`;
  return formatDate(dateStr);
};

const padZero = (num) => {
  return String(num).padStart(2, '0');
};

const navigateToMemory = (memoryId) => {
  console.log('Navigate to memory:', memoryId);
};

let countdownInterval = null;

// Lifecycle
onMounted(() => {
  loadDashboardData();
  
  // Update countdown every second
  countdownInterval = setInterval(() => {
    currentTime.value = new Date();
    updateCountdown();
  }, 1000);
  
  // Initial countdown
  setTimeout(() => {
    updateCountdown();
  }, 1000);
  
  // Check for signals after data loads
  setTimeout(() => {
    if (signalCount.value > 0) {
      showFlowers.value = true;
    }
  }, 1200);
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});
</script>

<template>
  <div class="min-h-screen">
    <!-- Flower Field Overlay (only shows if signals exist) -->
    <FlowerFieldOverlay v-if="showFlowers" :signal-count="signalCount" />

    <!-- Countdown Timer Section -->
    <div class="countdown-section py-16 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="countdown-title mb-12">
          {{ primaryBloom ? primaryBloom.title : 'WE\'RE LAUNCHING SOON' }}
        </h1>
        
        <div v-if="primaryBloom" class="countdown-container">
          <!-- Days -->
          <div class="flip-card-wrapper">
            <div class="flip-card" :class="{ flipping: flipDays }">
              <div class="flip-card-top">
                <span>{{ padZero(days) }}</span>
              </div>
              <div class="flip-card-bottom" data-value="10">
                <span>{{ padZero(days) }}</span>
              </div>
              <div class="flip-card-back" data-value="10">
                <span>{{ padZero(prevDays) }}</span>
              </div>
              <div class="flip-card-back-bottom" data-value="10">
                <span>{{ padZero(prevDays) }}</span>
              </div>
            </div>
            <div class="flip-label">DAYS</div>
          </div>

          <!-- Hours -->
          <div class="flip-card-wrapper">
            <div class="flip-card" :class="{ flipping: flipHours }">
              <div class="flip-card-top">
                <span>{{ padZero(hours) }}</span>
              </div>
              <div class="flip-card-bottom">
                <span>{{ padZero(hours) }}</span>
              </div>
              <div class="flip-card-back">
                <span>{{ padZero(prevHours) }}</span>
              </div>
              <div class="flip-card-back-bottom">
                <span>{{ padZero(prevHours) }}</span>
              </div>
            </div>
            <div class="flip-label">HOURS</div>
          </div>

          <!-- Minutes -->
          <div class="flip-card-wrapper">
            <div class="flip-card" :class="{ flipping: flipMinutes }">
              <div class="flip-card-top">
                <span>{{ padZero(minutes) }}</span>
              </div>
              <div class="flip-card-bottom">
                <span>{{ padZero(minutes) }}</span>
              </div>
              <div class="flip-card-back">
                <span>{{ padZero(prevMinutes) }}</span>
              </div>
              <div class="flip-card-back-bottom">
                <span>{{ padZero(prevMinutes) }}</span>
              </div>
            </div>
            <div class="flip-label">MINUTES</div>
          </div>

          <!-- Seconds -->
          <div class="flip-card-wrapper">
            <div class="flip-card" :class="{ flipping: flipSeconds }">
              <div class="flip-card-top">
                <span>{{ padZero(seconds) }}</span>
              </div>
              <div class="flip-card-bottom">
                <span>{{ padZero(seconds) }}</span>
              </div>
              <div class="flip-card-back">
                <span>{{ padZero(prevSeconds) }}</span>
              </div>
              <div class="flip-card-back-bottom">
                <span>{{ padZero(prevSeconds) }}</span>
              </div>
            </div>
            <div class="flip-label">SECONDS</div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-8">
          <p class="text-gray-400 text-lg">No bloom to count down to</p>
        </div>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left Column: Upcoming Blooms -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Next Bloom Card -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-sm font-semibold text-purple-600 uppercase tracking-wide">Next Bloom</h2>
                <Calendar :size="18" class="text-purple-400" />
              </div>

              <div v-if="primaryBloom">
                <div class="flex items-start justify-between mb-6">
                  <div class="flex-1">
                    <h3 class="text-2xl font-semibold text-gray-900 mb-2">{{ primaryBloom.title }}</h3>
                    <p class="text-sm text-gray-500">{{ formatDate(primaryBloom.bloom_date) }}</p>
                  </div>
                  
                  <!-- Heart Loading Animation -->
                  <div class="relative w-24 h-24 flex-shrink-0">
                    <svg viewBox="0 0 100 100" class="w-full h-full">
                      <defs>
                        <clipPath id="heartClip">
                          <path d="M50,90 C50,90 10,60 10,40 C10,25 20,15 30,15 C40,15 45,20 50,30 C55,20 60,15 70,15 C80,15 90,25 90,40 C90,60 50,90 50,90 Z" />
                        </clipPath>
                      </defs>
                      
                      <path 
                        d="M50,90 C50,90 10,60 10,40 C10,25 20,15 30,15 C40,15 45,20 50,30 C55,20 60,15 70,15 C80,15 90,25 90,40 C90,60 50,90 50,90 Z" 
                        fill="none" 
                        stroke="#e9d5ff" 
                        stroke-width="2"
                      />
                      
                      <g clip-path="url(#heartClip)">
                        <rect 
                          x="0" 
                          :y="100 - getBloomProgress(primaryBloom.bloom_date)" 
                          width="100" 
                          :height="getBloomProgress(primaryBloom.bloom_date)" 
                          fill="url(#heartGradient)"
                        />
                      </g>
                      
                      <defs>
                        <linearGradient id="heartGradient" x1="0%" y1="100%" x2="0%" y2="0%">
                          <stop offset="0%" style="stop-color:#e879f9;stop-opacity:1" />
                          <stop offset="100%" style="stop-color:#9333ea;stop-opacity:1" />
                        </linearGradient>
                      </defs>
                    </svg>
                    
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="text-xs font-bold text-purple-700">{{ Math.round(getBloomProgress(primaryBloom.bloom_date)) }}%</span>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-100">
                  <div class="flex items-center gap-2">
                    <Clock :size="16" class="text-purple-600" />
                    <span class="text-sm font-medium text-purple-900">Blooms in {{ getCountdown(primaryBloom.bloom_date) }}</span>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-12">
                <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-50 flex items-center justify-center">
                  <Sparkles :size="24" class="text-purple-400" />
                </div>
                <p class="text-gray-600 mb-2">No blooms scheduled yet.</p>
                <p class="text-sm text-gray-400">Plant a seed to create your next moment.</p>
              </div>
            </div>
          </div>

          <!-- Upcoming Blooms List -->
          <div v-if="secondaryBlooms.length > 0" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 class="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-4">Upcoming</h3>
            <div class="space-y-3">
              <div 
                v-for="bloom in secondaryBlooms" 
                :key="bloom.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
              >
                <span class="text-sm font-medium text-gray-700">{{ bloom.title }}</span>
                <span class="text-xs text-gray-500">{{ formatDate(bloom.bloom_date) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Recent Memories + Signals -->
        <div class="lg:col-span-1 space-y-6">
          
          <div v-if="signalCount > 0" class="bg-gradient-to-br from-indigo-900 to-purple-900 rounded-2xl shadow-lg p-6 text-white">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                <Sparkles :size="20" class="text-yellow-300 animate-pulse" />
              </div>
              <div>
                <p class="text-sm font-medium opacity-90">New Signals</p>
                <p class="text-lg font-semibold">{{ signalCount }} thinking of you</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 class="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-4">Recent Memories</h3>
            
            <div v-if="recentMemories.length > 0" class="space-y-3">
              <div
                v-for="memory in recentMemories"
                :key="memory.id"
                @click="navigateToMemory(memory.id)"
                class="group p-4 bg-white border border-gray-200 rounded-xl hover:shadow-md hover:-translate-y-1 transition-all duration-200 cursor-pointer"
              >
                <h4 class="font-semibold text-gray-900 mb-2 group-hover:text-purple-700 transition-colors">
                  {{ memory.title }}
                </h4>
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-500">{{ formatMemoryDate(memory.created_at) }}</span>
                  <span v-if="memory.is_seed" class="inline-flex items-center gap-1 px-2 py-1 bg-pink-50 text-pink-600 rounded-full text-xs font-medium">
                    <Heart :size="10" class="fill-current" />
                    Bloom
                  </span>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-gray-100 flex items-center justify-center">
                <Heart :size="20" class="text-gray-400" />
              </div>
              <p class="text-sm text-gray-600 mb-1">No memories yet.</p>
              <p class="text-xs text-gray-400">Your shared moments will appear here.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Red+Hat+Text:wght@400;500;600;700&display=swap');
</style>

<style scoped>
/* Countdown Section */
.countdown-section {
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  margin-left: 2rem;
  margin-right: 2rem;
  border-bottom-left-radius: 2rem;
  border-bottom-right-radius: 2rem;
  border-top-right-radius: 2rem;
  border-top-left-radius: 2rem;
}

.countdown-section::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.countdown-title {
  font-family: 'Barlow Semi Condensed', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  position: relative;
  z-index: 1;
}

.countdown-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.flip-card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.flip-card {
  position: relative;
  width: 110px;
  height: 120px;
  font-family: 'Red Hat Text', sans-serif;
  font-size: 3.5rem;
  font-weight: 700;
  color: #ffffff;
  perspective: 1000px;
}

.flip-card > div {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: linear-gradient(145deg, #312e81, #4c1d95);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -2px 6px rgba(0,0,0,0.3),
    0 8px 20px rgba(0,0,0,0.3);
}

.flip-card span {
  text-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

.flip-card-top {
  top: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}



.flip-card-bottom {
  bottom: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.flip-card-back,
.flip-card-back-bottom {
  z-index: 1;
  opacity: 0;
}

.flip-card-back {
  top: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
  transform-origin: bottom;
}

.flip-card-top span,
.flip-card-bottom span,
.flip-card-back span,
.flip-card-back-bottom span {
  transform: none;
}


.flip-card-back-bottom {
  bottom: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  transform-origin: top;
}



/* Flip Animation */
.flip-card.flipping .flip-card-back {
  animation: flipTop 0.6s ease-in;
}

.flip-card.flipping .flip-card-back-bottom {
  animation: flipBottom 0.6s ease-out 0.3s;
}

@keyframes flipTop {
  0% {
    opacity: 1;
    transform: rotateX(0deg);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 1;
    transform: rotateX(-90deg);
  }
}

@keyframes flipBottom {
  0% {
    opacity: 1;
    transform: rotateX(90deg);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 1;
    transform: rotateX(0deg);
  }
}

.flip-label {
  font-family: 'Red Hat Text', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: #c4b5fd;
  text-transform: uppercase;
  letter-spacing: 0.25em;
}


/* Responsive */
@media (max-width: 640px) {
  .countdown-title {
    font-size: 1.5rem;
  }

  .countdown-container {
    gap: 1rem;
  }

  .flip-card {
    width: 70px;
    height: 80px;
    font-size: 2.5rem;
  }

  .flip-label {
    font-size: 0.65rem;
  }
}

@media (max-width: 768px) {
  .flip-card {
    width: 80px;
    height: 95px;
    font-size: 2.5rem;
  }
}

</style>

