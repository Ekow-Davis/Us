<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, Lock, User, Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()

const isSignUpMode = ref(false)
const showPassword = ref(false)

const loginEmail = ref('')
const loginPassword = ref('')

const registerForm = ref({
  display_name: '',
  email: '',
  password: ''
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// Fake login handler (no API)
const handleLogin = () => {
  if (!loginEmail.value || !loginPassword.value) return
  router.push('/dashboard')
}

// Fake register handler (no API)
const handleRegister = () => {
  if (!registerForm.value.email ||
      !registerForm.value.password ||
      !registerForm.value.display_name) return

  router.push('/registration-transfer')
}
</script>

<template>
  <div :class="['container', { 'sign-up-mode': isSignUpMode }]">
    <div class="forms-container">
      <div class="signin-signup">
        
        <!-- SIGN IN -->
        <form @submit.prevent="handleLogin" class="sign-in-form">
          <h2 class="title">Login</h2>

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

          <button class="btn-pink" type="submit">
            Login
          </button>
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

          <button class="btn" type="submit">
            Register
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
        <img src="../../../public/images/undraw_spread-love_0ekp.svg" class="image" />
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
        <img src="../../../public/images/undraw_intense-feeling_4i8u.svg" class="image" />
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
