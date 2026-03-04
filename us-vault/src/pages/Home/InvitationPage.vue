<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, Lock, Eye, EyeOff } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { joinVaultApi } from '../../api/vault'

const router = useRouter()
const auth = useAuthStore()

// ── State ──────────────────────────────────────────────────────────────────
const step = ref<'login' | 'code'>('login')
const showPassword = ref(false)

// Login fields
const email = ref('')
const password = ref('')

// 8-digit invitation code
const codeDigits = ref(['', '', '', '', '', '', '', ''])
const codeInputs = ref<HTMLInputElement[]>([])

// Loading & error states
const isLoggingIn = ref(false)
const isJoining = ref(false)
const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

// ── Methods ────────────────────────────────────────────────────────────────
const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = 'Please enter both email and password'
    return
  }

  try {
    errorMessage.value = null
    isLoggingIn.value = true

    await auth.login({
      email: email.value,
      password: password.value
    })

    // Move to code entry step after successful login
    step.value = 'code'
    
    // Focus first input after a short delay
    await nextTick()
    setTimeout(() => {
      codeInputs.value[0]?.focus()
    }, 100)

  } catch (err: any) {
    errorMessage.value = err?.response?.data?.detail || 'Login failed. Please check your credentials.'
  } finally {
    isLoggingIn.value = false
  }
}

const handleCodeInput = (index: number, event: Event) => {
  const input = event.target as HTMLInputElement
  const value = input.value

  // Only allow single digit
  if (value.length > 1) {
    input.value = value.slice(-1)
  }

  // Update the code array
  codeDigits.value[index] = input.value

  // Auto-focus next input
  if (input.value && index < 7) {
    codeInputs.value[index + 1]?.focus()
  }

  // Clear error when user types
  errorMessage.value = null
}

const handleCodeKeydown = (index: number, event: KeyboardEvent) => {
  // Handle backspace
  if (event.key === 'Backspace' && !codeDigits.value[index] && index > 0) {
    codeInputs.value[index - 1]?.focus()
  }

  // Handle paste
  if (event.key === 'v' && (event.ctrlKey || event.metaKey)) {
    event.preventDefault()
    handlePaste(event as any)
  }
}

const handlePaste = async (event: ClipboardEvent) => {
  event.preventDefault()
  const pastedText = event.clipboardData?.getData('text') || ''
  const digits = pastedText.replace(/\D/g, '').slice(0, 8).split('')

  digits.forEach((digit, index) => {
    if (index < 8) {
      codeDigits.value[index] = digit
      if (codeInputs.value[index]) {
        codeInputs.value[index].value = digit
      }
    }
  })

  // Focus the next empty input or the last one
  const nextEmptyIndex = codeDigits.value.findIndex(d => !d)
  if (nextEmptyIndex >= 0) {
    codeInputs.value[nextEmptyIndex]?.focus()
  } else {
    codeInputs.value[7]?.focus()
  }
}

const handleJoinVault = async () => {
  const inviteCode = codeDigits.value.join('')

  if (inviteCode.length !== 8) {
    errorMessage.value = 'Please enter all 8 digits of the invitation code'
    return
  }

  try {
    errorMessage.value = null
    successMessage.value = null
    isJoining.value = true

    await joinVaultApi(inviteCode)

    // Show success message
    successMessage.value = 'Successfully joined vault! Redirecting...'

    // Wait a moment then redirect
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)

  } catch (err: any) {
    errorMessage.value = err?.response?.data?.detail || 'Invalid invitation code. Please try again.'
  } finally {
    isJoining.value = false
  }
}

const goBackToLogin = () => {
  step.value = 'login'
  codeDigits.value = ['', '', '', '', '', '', '', '']
  errorMessage.value = null
  successMessage.value = null
}
</script>

<template>
  <div class="invitation-page min-h-screen flex items-center justify-center p-4">
    
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Animated background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="particle particle-4"></div>
      <div class="particle particle-5"></div>
    </div>

    <!-- Main Card -->
    <div class="relative w-full max-w-md">
      <div class="bg-white rounded-3xl shadow-2xl overflow-hidden">
        
        <!-- Top gradient bar -->
        <div class="h-1.5 w-full" style="background: linear-gradient(90deg,#7c3aed,#a855f7,#ec4899);"></div>

        <!-- Content -->
        <div class="p-8 md:p-10">

          <!-- Logo/Icon -->
          <div class="flex justify-center mb-6">
            <div class="w-20 h-20 rounded-2xl flex items-center justify-center" 
                 style="background: linear-gradient(135deg,#7c3aed,#a855f7);">
              <svg width="40" height="40" viewBox="0 0 48 48" fill="none">
                <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" 
                      fill="white"/>
              </svg>
            </div>
          </div>

          <!-- Title -->
          <h1 class="text-center text-3xl font-semibold text-slate-900 mb-2" 
              style="font-family: 'Crimson Pro', Georgia, serif;">
            {{ step === 'login' ? 'Welcome Back' : 'Enter Invitation Code' }}
          </h1>
          <p class="text-center text-slate-600 mb-8" 
             style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
            {{ step === 'login' ? 'Sign in to join your vault' : 'Enter the 8-digit code to join the vault' }}
          </p>

          <!-- Success Message -->
          <div v-if="successMessage" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl animate-fade-in">
            <p class="text-sm text-emerald-700 text-center" style="font-family: 'Inter', sans-serif;">
              {{ successMessage }}
            </p>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
            <p class="text-sm text-red-700 text-center" style="font-family: 'Inter', sans-serif;">
              {{ errorMessage }}
            </p>
          </div>

          <!-- LOGIN FORM -->
          <form v-if="step === 'login'" @submit.prevent="handleLogin" class="space-y-6">
            
            <!-- Email -->
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-2" 
                     style="font-family: 'Inter', sans-serif;">
                Email
              </label>
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
                  :disabled="isLoggingIn"
                  required
                />
              </div>
            </div>

            <!-- Password -->
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-2" 
                     style="font-family: 'Inter', sans-serif;">
                Password
              </label>
              <div class="relative">
                <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                  <Lock :size="20" />
                </div>
                <input 
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full pl-12 pr-12 py-3.5 rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition text-slate-900"
                  style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;"
                  :disabled="isLoggingIn"
                  required
                />
                <button type="button"
                        @click="togglePassword"
                        class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition">
                  <Eye v-if="!showPassword" :size="20" />
                  <EyeOff v-else :size="20" />
                </button>
              </div>
            </div>

            <!-- Submit -->
            <button type="submit"
                    :disabled="isLoggingIn"
                    class="w-full py-3.5 rounded-xl bg-linear-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
              {{ isLoggingIn ? 'Signing in...' : 'Continue to Code Entry' }}
            </button>

            <!-- Back to regular login -->
            <div class="text-center pt-4">
              <router-link to="/login" 
                           class="text-sm text-purple-600 hover:text-purple-800 font-semibold transition"
                           style="font-family: 'Inter', sans-serif;">
                ← Back to Login
              </router-link>
            </div>
          </form>

          <!-- CODE ENTRY FORM -->
          <form v-else @submit.prevent="handleJoinVault" class="space-y-6">
            
            <!-- 8-Digit Code Input -->
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-4 text-center" 
                     style="font-family: 'Inter', sans-serif;">
                Invitation Code
              </label>
              
              <div class="flex justify-center gap-2 mb-6">
                <input
                  v-for="(digit, index) in codeDigits"
                  :key="index"
                  :ref="el => { if (el) codeInputs[index] = el as HTMLInputElement }"
                  v-model="codeDigits[index]"
                  type="text"
                  inputmode="numeric"
                  maxlength="1"
                  @input="handleCodeInput(index, $event)"
                  @keydown="handleCodeKeydown(index, $event)"
                  @paste="handlePaste"
                  class="w-12 h-14 text-center text-xl font-bold rounded-xl border-2 border-slate-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition"
                  :class="{
                    'border-purple-500 bg-purple-50': codeDigits[index],
                    'border-red-300 bg-red-50': errorMessage && !codeDigits[index]
                  }"
                  style="font-family: 'Inter', sans-serif;"
                  :disabled="isJoining || !!successMessage"
                />
              </div>

              <p class="text-xs text-slate-500 text-center" style="font-family: 'Inter', sans-serif;">
                You can paste all 8 digits at once
              </p>
            </div>

            <!-- Submit -->
            <button type="submit"
                    :disabled="isJoining || !!successMessage"
                    class="w-full py-3.5 rounded-xl bg-linear-to-r from-purple-600 to-pink-600 text-white font-semibold hover:from-purple-500 hover:to-pink-500 transition shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                    style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
              <span v-if="successMessage">✓ Joined Successfully!</span>
              <span v-else-if="isJoining">Joining Vault...</span>
              <span v-else>Join Vault</span>
            </button>

            <!-- Back button -->
            <button type="button"
                    @click="goBackToLogin"
                    :disabled="isJoining || !!successMessage"
                    class="w-full py-3 rounded-xl border-2 border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
                    style="font-family: 'Inter', sans-serif; font-size: 0.9375rem;">
              ← Back to Login
            </button>
          </form>

        </div>
      </div>

      <!-- Footer text -->
      <p class="text-center text-sm text-slate-400 mt-6" style="font-family: 'Inter', sans-serif;">
        Don't have an account? 
        <router-link to="/login" class="text-purple-600 hover:text-purple-800 font-semibold transition">
          Register here
        </router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.invitation-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

/* Animated particles */
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
.particle-5 { width: 70px; height: 70px; top: 50%; left: 40%; animation-delay: 7s; }

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-30px) translateX(30px); }
  50% { transform: translateY(-60px) translateX(-30px); }
  75% { transform: translateY(-30px) translateX(60px); }
}

/* Fade in animation */
.animate-fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Remove number input arrows */
input[type="text"]::-webkit-outer-spin-button,
input[type="text"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Code input focus animation */
input[type="text"]:focus {
  transform: scale(1.05);
}
</style>