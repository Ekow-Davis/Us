<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Props ──────────────────────────────────────────────────────────────────
const props = defineProps({
  inactivityTimeout: {
    type: Number,
    default: 10 * 60 * 1000 // 10 minutes in milliseconds
  }
})

// ── State ──────────────────────────────────────────────────────────────────
const showInactivityModal = ref(false)
const isRefreshing = ref(false)
let inactivityTimer = null
let lastActivity = Date.now()

// ── Methods ────────────────────────────────────────────────────────────────
const resetInactivityTimer = () => {
  lastActivity = Date.now()
  
  // Clear existing timer
  if (inactivityTimer) {
    clearTimeout(inactivityTimer)
  }
  
  // Set new timer
  inactivityTimer = setTimeout(() => {
    showInactivityModal.value = true
  }, props.inactivityTimeout)
}

const handleStillHere = async () => {
  isRefreshing.value = true
  
  try {
    // Call refresh token API
    // const response = await fetch('/api/auth/refresh', {
    //   method: 'POST',
    //   credentials: 'include' // Important for sending cookies
    // })
    
    // if (!response.ok) {
    //   throw new Error('Failed to refresh token')
    // }
    
    // const data = await response.json()
    // localStorage.setItem('token', data.access_token)
    
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 500))
    console.log('Token refreshed successfully')
    
    // Close modal and reset timer
    showInactivityModal.value = false
    resetInactivityTimer()
  } catch (error) {
    console.error('Failed to refresh token:', error)
    // If refresh fails, log out
    handleLogout()
  } finally {
    isRefreshing.value = false
  }
}

const handleLogout = () => {
  // Clear auth state
  localStorage.removeItem('token')
  
  // Optional: Call logout API
  // fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
  
  // Close modal
  showInactivityModal.value = false
  
  // Redirect to home
  router.push('/')
}

// Track user activity
const trackActivity = () => {
  resetInactivityTimer()
}

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
  // Start the inactivity timer
  resetInactivityTimer()
  
  // Listen for user activity
  const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click']
  events.forEach(event => {
    window.addEventListener(event, trackActivity, { passive: true })
  })
})

onUnmounted(() => {
  // Clear timer
  if (inactivityTimer) {
    clearTimeout(inactivityTimer)
  }
  
  // Remove event listeners
  const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click']
  events.forEach(event => {
    window.removeEventListener(event, trackActivity)
  })
})
</script>

<template>
  <div class="inactivity-wrapper">
    <!-- Main content -->
    <slot></slot>

    <!-- Inactivity Modal Overlay -->
    <Transition name="inactivity-modal">
      <div v-if="showInactivityModal"
           class="fixed inset-0 z-9999 flex items-start justify-center pt-20 px-4"
           style="background: rgba(15,23,42,0.75); backdrop-filter: blur(8px);">
        
        <div class="inactivity-modal-card relative bg-white rounded-2xl shadow-2xl overflow-hidden max-w-md w-full"
             style="animation: slideDown 0.4s cubic-bezier(0.22,1,0.36,1) both;">
          
          <!-- Top accent -->
          <div class="h-1 w-full" style="background: linear-gradient(90deg,#7c3aed,#a855f7,#ec4899);"></div>

          <div class="p-6 md:p-8">
            <!-- Icon -->
            <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-linear-to-br from-purple-100 to-pink-100 flex items-center justify-center">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>

            <!-- Title -->
            <h2 class="text-center text-xl md:text-2xl font-semibold text-slate-900 mb-2" 
                style="font-family: 'Crimson Pro', Georgia, serif;">
              Are you still there?
            </h2>

            <!-- Message -->
            <p class="text-center text-sm text-slate-600 mb-6" style="font-family: 'Inter', sans-serif;">
              We've detected prolonged inactivity. Would you like to continue your session?
            </p>

            <!-- Actions -->
            <div class="flex flex-col sm:flex-row gap-3">
              <button @click="handleLogout"
                      :disabled="isRefreshing"
                      class="flex-1 px-6 py-3 rounded-xl border-2 border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
                      style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
                No, Log Out
              </button>
              <button @click="handleStillHere"
                      :disabled="isRefreshing"
                      class="flex-1 px-6 py-3 rounded-xl bg-linear-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                      style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
                {{ isRefreshing ? 'Refreshing...' : 'Yes, I\'m Here' }}
              </button>
            </div>

            <!-- Info text -->
            <p class="text-center text-xs text-slate-400 mt-4" style="font-family: 'Inter', sans-serif;">
              Your session will be refreshed if you choose to continue
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

/* Modal transitions */
.inactivity-modal-enter-active,
.inactivity-modal-leave-active {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.inactivity-modal-enter-from,
.inactivity-modal-leave-to {
  opacity: 0;
}

.inactivity-modal-enter-from .inactivity-modal-card {
  transform: translateY(-20px);
  opacity: 0;
}

/* Slide down animation */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>