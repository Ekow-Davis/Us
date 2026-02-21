<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, ArrowLeft } from 'lucide-vue-next'

const router = useRouter()

// ── State ──────────────────────────────────────────────────────────────────
const email = ref('')
const isLoading = ref(false)
const error = ref('')
const otpSent = ref(false)
const otp = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const step = ref(1) // 1: Email, 2: OTP, 3: New Password

// ── Methods ────────────────────────────────────────────────────────────────
const handleSendOTP = async () => {
  if (!email.value.trim()) {
    error.value = 'Please enter your email address'
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    error.value = 'Please enter a valid email address'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Mock API call - replace with actual API
    // const response = await fetch('/api/auth/forgot-password', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ email: email.value })
    // })
    
    // if (!response.ok) {
    //   throw new Error('Failed to send OTP')
    // }

    await new Promise(resolve => setTimeout(resolve, 800))
    
    otpSent.value = true
    step.value = 2
  } catch (err) {
    error.value = 'Failed to send OTP. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleVerifyOTP = async () => {
  if (!otp.value.trim()) {
    error.value = 'Please enter the OTP'
    return
  }

  if (otp.value.length !== 6) {
    error.value = 'OTP must be 6 digits'
    return
  }

  // Move to password reset step
  error.value = ''
  step.value = 3
}

const handleResetPassword = async () => {
  if (!newPassword.value.trim()) {
    error.value = 'Please enter a new password'
    return
  }

  if (newPassword.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    // Mock API call - replace with actual API
    // const response = await fetch('/api/auth/reset-password', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({
    //     email: email.value,
    //     otp: otp.value,
    //     new_password: newPassword.value
    //   })
    // })
    
    // if (!response.ok) {
    //   throw new Error('Failed to reset password')
    // }

    await new Promise(resolve => setTimeout(resolve, 800))
    
    // Success - redirect to login
    router.push({
      path: '/login',
      query: { reset: 'success' }
    })
  } catch (err) {
    error.value = 'Failed to reset password. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const goBack = () => {
  if (step.value > 1) {
    step.value--
    error.value = ''
  } else {
    router.push('/login')
  }
}
</script>

<template>
  <div class="forgot-password-page min-h-screen flex items-center justify-center p-4" 
       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Floating particles -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="particle particle-4"></div>
    </div>

    <!-- Card -->
    <div class="relative w-full max-w-md bg-white rounded-3xl shadow-2xl overflow-hidden">
      
      <!-- Top gradient bar -->
      <div class="h-1.5 w-full" style="background: linear-gradient(90deg,#7c3aed,#a855f7,#ec4899);"></div>

      <div class="p-8 md:p-10">
        
        <!-- Back button -->
        <button @click="goBack"
                class="inline-flex items-center gap-2 text-purple-600 hover:text-purple-800 mb-6 text-sm font-semibold transition"
                style="font-family: 'Inter', sans-serif;">
          <ArrowLeft :size="16" />
          {{ step > 1 ? 'Back' : 'Back to Login' }}
        </button>

        <!-- Logo -->
        <div class="flex items-center gap-3 mb-8">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center" 
               style="background: linear-gradient(135deg,#7c3aed,#a855f7);">
            <svg width="24" height="24" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" 
                    fill="white"/>
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-semibold text-slate-900" style="font-family: 'Crimson Pro', Georgia, serif;">
              Forgot Password
            </h1>
            <p class="text-xs text-slate-500" style="font-family: 'Inter', sans-serif;">
              Step {{ step }} of 3
            </p>
          </div>
        </div>

        <!-- Progress bar -->
        <div class="w-full h-1.5 bg-slate-100 rounded-full mb-8 overflow-hidden">
          <div class="h-full bg-gradient-to-r from-purple-600 to-pink-600 transition-all duration-500 rounded-full"
               :style="`width: ${(step / 3) * 100}%`"></div>
        </div>

        <!-- Error message -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
          <p class="text-sm text-red-700" style="font-family: 'Inter', sans-serif;">{{ error }}</p>
        </div>

        <!-- Step 1: Email -->
        <form v-if="step === 1" @submit.prevent="handleSendOTP" class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-slate-900 mb-2" style="font-family: 'Crimson Pro', Georgia, serif;">
              Enter your email
            </h2>
            <p class="text-sm text-slate-600 mb-4" style="font-family: 'Inter', sans-serif;">
              We'll send you a 6-digit OTP to reset your password
            </p>
            
            <div class="relative">
              <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                <Mail :size="20" />
              </div>
              <input 
                v-model="email"
                type="email"
                placeholder="your.email@example.com"
                class="w-full pl-12 pr-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition text-slate-900"
                style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;"
                :disabled="isLoading"
              />
            </div>
          </div>

          <button type="submit"
                  :disabled="isLoading"
                  class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
            {{ isLoading ? 'Sending...' : 'Send OTP' }}
          </button>
        </form>

        <!-- Step 2: OTP -->
        <form v-else-if="step === 2" @submit.prevent="handleVerifyOTP" class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-slate-900 mb-2" style="font-family: 'Crimson Pro', Georgia, serif;">
              Enter OTP
            </h2>
            <p class="text-sm text-slate-600 mb-4" style="font-family: 'Inter', sans-serif;">
              We've sent a 6-digit code to <span class="font-semibold text-purple-600">{{ email }}</span>
            </p>
            
            <input 
              v-model="otp"
              type="text"
              maxlength="6"
              placeholder="000000"
              class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition text-center text-2xl tracking-widest font-semibold text-slate-900"
              style="font-family: 'Inter', sans-serif;"
            />
          </div>

          <button type="submit"
                  class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg"
                  style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
            Verify OTP
          </button>

          <button type="button"
                  @click="handleSendOTP"
                  class="w-full text-sm text-purple-600 hover:text-purple-800 font-semibold"
                  style="font-family: 'Inter', sans-serif;">
            Didn't receive the code? Resend
          </button>
        </form>

        <!-- Step 3: New Password -->
        <form v-else-if="step === 3" @submit.prevent="handleResetPassword" class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-slate-900 mb-2" style="font-family: 'Crimson Pro', Georgia, serif;">
              Create new password
            </h2>
            <p class="text-sm text-slate-600 mb-4" style="font-family: 'Inter', sans-serif;">
              Your new password must be at least 8 characters long
            </p>
            
            <div class="space-y-4">
              <input 
                v-model="newPassword"
                type="password"
                placeholder="New password"
                class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition text-slate-900"
                style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;"
                :disabled="isLoading"
              />
              
              <input 
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm new password"
                class="w-full px-4 py-3.5 rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition text-slate-900"
                style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;"
                :disabled="isLoading"
              />
            </div>
          </div>

          <button type="submit"
                  :disabled="isLoading"
                  class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
            {{ isLoading ? 'Resetting...' : 'Reset Password' }}
          </button>
        </form>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* Particles */
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 20s infinite ease-in-out;
}

.particle-1 { width: 80px; height: 80px; top: 10%; left: 10%; animation-delay: 0s; }
.particle-2 { width: 60px; height: 60px; top: 60%; left: 80%; animation-delay: 5s; }
.particle-3 { width: 100px; height: 100px; top: 80%; left: 20%; animation-delay: 10s; }
.particle-4 { width: 40px; height: 40px; top: 30%; left: 70%; animation-delay: 15s; }

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-30px) translateX(30px); }
  50% { transform: translateY(-60px) translateX(-30px); }
  75% { transform: translateY(-30px) translateX(60px); }
}

/* Remove number input arrows */
input[type="text"]::-webkit-outer-spin-button,
input[type="text"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>