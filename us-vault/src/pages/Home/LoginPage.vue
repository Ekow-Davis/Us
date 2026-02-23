<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, Lock, User, Eye, EyeOff } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { registerApi } from '../../api/auth'

const router = useRouter()
const auth = useAuthStore()

const isSignUpMode = ref(false)
const showPassword = ref(false)

const loginEmail = ref('')
const loginPassword = ref('')

const registerForm = ref({
  display_name: '',
  email: '',
  password: ''
})

const isLoggingIn = ref(false)
const isRegistering = ref(false)
const errorMessage = ref<string | null>(null)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  if (!loginEmail.value || !loginPassword.value) return

  try {
    errorMessage.value = null
    isLoggingIn.value = true

    await auth.login({
      email: loginEmail.value,
      password: loginPassword.value
    })

    router.push('/dashboard')

  } catch (err: any) {
    errorMessage.value = err?.response?.data?.detail || "Login failed"
  } finally {
    isLoggingIn.value = false
  }
}

const handleRegister = async () => {
  const { email, password, display_name } = registerForm.value
  if (!email || !password || !display_name) return

  try {
    errorMessage.value = null
    isRegistering.value = true

    // Register
    await registerApi({
      email,
      password,
      display_name
    })

    // Auto-login after successful registration
    await auth.login({
      email,
      password
    })

    router.push('/registration-transfer')

  } catch (err: any) {
    errorMessage.value = err?.response?.data?.detail || "Registration failed"
  } finally {
    isRegistering.value = false
  }
}
</script>

<template>
  <div :class="['container', { 'sign-up-mode': isSignUpMode }]">
    <div class="forms-container">
      <div class="signin-signup">
        
        <!-- SIGN IN -->
        <form @submit.prevent="handleLogin" class="sign-in-form">
          <h2 class="title">Login</h2>
          <p v-if="errorMessage" style="color:#ff4d4f;font-size:14px;margin-bottom:10px;">
            {{ errorMessage }}
          </p>

          <div class="input-field">
            <Mail class="lucide-icon" />
            <input
              type="email"
              placeholder="Email"
              v-model="loginEmail"
              required
            />
          </div>

          <div class="input-field">
            <Lock class="lucide-icon" />
            <input
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password"
              v-model="loginPassword"
              required
            />
            <span class="toggle-eye" @click="togglePassword">
              <component :is="showPassword ? EyeOff : Eye" />
            </span>
          </div>

          <button class="btn-pink" type="submit" :disabled="isLoggingIn">
            <span v-if="isLoggingIn">Loading...</span>
            <span v-else>Login</span>
          </button>

          <p>
            <router-link to="/forgot-password" class="m-2 text-blue-400 underline">Forgot your password?</router-link>
          </p>
        </form>

        <!-- REGISTER -->
        <form @submit.prevent="handleRegister" class="sign-up-form">
          <h2 class="title">Register</h2>

          <div class="input-field">
            <User class="lucide-icon" />
            <input
              type="text"
              placeholder="Display Name"
              v-model="registerForm.display_name"
              required
            />
          </div>

          <div class="input-field">
            <Mail class="lucide-icon" />
            <input
              type="email"
              placeholder="Email"
              v-model="registerForm.email"
              required
            />
          </div>

          <div class="input-field">
            <Lock class="lucide-icon" />
            <input
              :type="showPassword ? 'text' : 'password'"
              placeholder="Password"
              v-model="registerForm.password"
              required
            />
            <span class="toggle-eye" @click="togglePassword">
              <component :is="showPassword ? EyeOff : Eye" />
            </span>
          </div>

          <button class="btn" type="submit" :disabled="isRegistering">
            <span v-if="isRegistering">Creating...</span>
            <span v-else>Register</span>
          </button>
        </form>

      </div>
    </div>

    <!-- PANELS -->
    <div class="panels-container">
      <!-- Login PANEL -->
      <div class="panel left-panel">
        <div class="content">
          <h3>New here?</h3>
          <p>Register now to get started.</p>
          <button class="btn transparent" @click="isSignUpMode = true">
            Sign Up
          </button>
        </div>
        <img src="/images/undraw_spread-love_0ekp.svg" class="image" />
      </div>

      <!-- Register PANEL -->
      <div class="panel right-panel">
        <div class="content">
          <h3>Already a member?</h3>
          <p>Sign in to access your dashboard.</p>
          <button class="btn transparent" @click="isSignUpMode = false">
            Sign In
          </button>
        </div>
        <img src="/images/undraw_intense-feeling_4i8u.svg" class="image" />
      </div>
    </div>
  </div>
</template>



<style scoped>
@import './signinup.css';

/* icon adjustments so CSS grid still works */
.lucide-icon {
  width: 20px;
  height: 20px;
  color: #acacac;
  align-self: center;
  justify-self: center;
}

.toggle-eye {
  position: absolute;
  right: 18px;
  top: 16px;
  cursor: pointer;
}
</style>
