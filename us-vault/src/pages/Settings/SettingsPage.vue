<script setup>
import { ref, computed } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { useAuthStore } from '../../stores/auth'
import { changeEmailApi, changePasswordApi } from '../../api/auth'
import { leaveVaultApi, joinVaultApi } from '../../api/vault'
import { useRouter } from 'vue-router'
import { watch } from 'vue'

// ── Active tab ────────────────────────────────────────────────────────────────
const activeTab = ref('general')

const auth = useAuthStore()
const router = useRouter()


const tabs = [
  { id: 'general', label: 'General',  icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 0 0-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 0 0-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 0 0-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 0 0-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 0 0 1.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z' },
  { id: 'vault',   label: 'Vault',    icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' },
  { id: 'profile', label: 'Profile',  icon: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2 M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z' },
  { id: 'privacy', label: 'Privacy',  icon: 'M12 17a2 2 0 1 0 0-4 2 2 0 0 0 0 4z M18 8H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2z M8 8V6a4 4 0 1 1 8 0v2' },
]

// ── General tab state ─────────────────────────────────────────────────────────
const emailForm       = ref({ current: 'john@example.com', new: '', confirm: '' })
const passwordForm    = ref({ current: '', new: '', confirm: '' })
const showEmailPw     = ref(false)
const showCurrentPw   = ref(false)
const showNewPw       = ref(false)
const showConfirmPw   = ref(false)
const notifEmail      = ref(true)
const notifPush       = ref(true)
const notifBlooms     = ref(true)
const notifSignals    = ref(true)
const savingEmail     = ref(false)
const savingPassword  = ref(false)
const successEmail    = ref(false)
const successPassword = ref(false)

const saveEmail = async () => {
  if (!emailForm.value.new || !emailForm.value.password) return

  savingEmail.value = true
  successEmail.value = false

  try {
    await changeEmailApi({
      new_email: emailForm.value.new,
      password: emailForm.value.password
    })

    // Refresh user info
    await auth.fetchUser()

    emailForm.value.current = auth.user.email
    emailForm.value.new = ''
    emailForm.value.password = ''

    successEmail.value = true

  } catch (err) {
    console.error(err?.response?.data?.detail || 'Email change failed')
  } finally {
    savingEmail.value = false
  }
}

const savePassword = async () => {
  if (
    !passwordForm.value.current ||
    !passwordForm.value.new ||
    passwordForm.value.new !== passwordForm.value.confirm
  ) return

  savingPassword.value = true
  successPassword.value = false

  try {
    await changePasswordApi({
      old_password: passwordForm.value.current,
      new_password: passwordForm.value.new
    })

    passwordForm.value = {
      current: '',
      new: '',
      confirm: ''
    }

    successPassword.value = true

  } catch (err) {
    console.error(err?.response?.data?.detail || 'Password change failed')
  } finally {
    savingPassword.value = false
  }
}
 
// ── Vault tab state ───────────────────────────────────────────────────────────
const showLeaveConfirm    = ref(false)
const showSwitchVault     = ref(false)
const switchCode          = ref('')
const switchCodeError     = ref('')
const leavingVault        = ref(false)
const switchingVault      = ref(false)
const leaveSuccess        = ref(false)

const leaveVault = async () => {
  leavingVault.value = true
  leaveSuccess.value = false

  try {
    await leaveVaultApi()

    leaveSuccess.value = true
    showLeaveConfirm.value = false

  } catch (err) {
    console.error(err?.response?.data?.detail || 'Failed to leave vault')
  } finally {
    leavingVault.value = false
  }
}

const switchVault = async () => {
  if (!switchCode.value || switchCode.value.length !== 8) {
    switchCodeError.value = 'Please enter a valid 8-character invitation code.'
    return
  }

  switchCodeError.value = ''
  switchingVault.value = true

  try {
    // Step 1: Leave current vault
    await leaveVaultApi()

    // Step 2: Join new vault
    await joinVaultApi(switchCode.value)

    showSwitchVault.value = false
    switchCode.value = ''

  } catch (err) {
    switchCodeError.value =
      err?.response?.data?.detail || 'Failed to switch vault'
  } finally {
    switchingVault.value = false
  }
}

// ── Profile tab state ─────────────────────────────────────────────────────────
const displayName     = ref('')
const savingName      = ref(false)
const successName     = ref(false)
const showDeleteConfirm = ref(false)
const deleteConfirmText = ref('')
const deletingAccount   = ref(false)

const saveName = async () => {
  savingName.value = true
  await new Promise(r => setTimeout(r, 800))
  savingName.value = false
  successName.value = true
  console.log('Display name updated:', displayName.value)
  setTimeout(() => { successName.value = false }, 3000)
}

const deleteAccount = async () => {
  if (deleteConfirmText.value !== 'DELETE') return
  deletingAccount.value = true
  await new Promise(r => setTimeout(r, 1500))
  console.log('Account deleted')
}

// General for all?
watch(
  () => auth.user,
  (user) => {
    if (user) {
      emailForm.value.current = user.email
      displayName.value = user.display_name
    }
  },
  { immediate: true }
)

// ── Privacy tab state ─────────────────────────────────────────────────────────
const privacyReadReceipts = ref(true)
const privacyActivity     = ref(false)
const privacySignalCount  = ref(true)
// const sessionsExpanded    = ref(false)

// const mockSessions = [
//   { device: 'Chrome · macOS', location: 'Cape Town, ZA', time: 'Active now', current: true },
//   { device: 'Safari · iPhone 15', location: 'Cape Town, ZA', time: '2 hours ago', current: false },
//   { device: 'Firefox · Windows', location: 'Unknown', time: '3 days ago', current: false },
// ]
</script>

<template>
  <InactivityOverlay>
        <Sidebar>
      <div class="settings-page">
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
        </component>

        <!-- ── Background ─────────────────────────────────────────── -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <!-- Hibiscus top-right -->
          <img src="/images/hibiscus_placeholder.png" alt=""
              class="absolute -top-8 -right-8 w-64 opacity-[0.07] rotate-12 select-none pointer-events-none"
              style="filter: hue-rotate(260deg) saturate(0.6);"/>
          <!-- Hibiscus bottom-left -->
          <img src="/images/hibiscus_placeholder.png" alt=""
              class="absolute -bottom-12 -left-10 w-56 opacity-[0.06] -rotate-12 scale-x-[-1] select-none pointer-events-none"
              style="filter: hue-rotate(280deg) saturate(0.5);"/>
          <!-- Ambient orb -->
          <div class="absolute top-0 right-0 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
          <div class="absolute bottom-0 left-0 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#fce7f3 0%,transparent 70%);"></div>
        </div>

        <!-- ── Page header ────────────────────────────────────────── -->
        <div class="relative z-10 px-4 sm:px-8 pt-10 pb-6 max-w-5xl mx-auto">
          <p class="settings-sub">Your account</p>
          <h1 class="settings-display">Settings</h1>
          <div class="flex items-center gap-3 mt-4">
            <div class="h-px flex-1" style="background: linear-gradient(90deg,#7c3aed,#c084fc,transparent);"></div>
            <svg width="10" height="10" viewBox="0 0 60 60" fill="#a855f7"><ellipse cx="30" cy="34" rx="14" ry="20"/></svg>
            <div class="h-px w-8" style="background:#c084fc;"></div>
          </div>
        </div>

        <!-- ── Body: inner sidebar + content ─────────────────────── -->
        <div class="relative z-10 max-w-5xl mx-auto px-4 sm:px-8 pb-20 flex flex-col lg:flex-row gap-6">

          <!-- ── Inner tab sidebar (desktop) ───────────────────────── -->
          <aside class="hidden lg:flex flex-col gap-1 w-52 shrink-0 pt-1">
            <!-- Hibiscus small inside sidebar -->
            <div class="relative mb-4 px-3">
              <img src="/images/hibiscus_placeholder.png" alt=""
                  class="w-10 h-10 opacity-30 mx-auto"
                  style="filter: hue-rotate(260deg) saturate(0.7);"/>
            </div>
            <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
                    :class="['settings-tab-btn', activeTab === tab.id ? 'settings-tab-btn--active' : '']">
              <span class="settings-tab-icon-wrap" :class="activeTab === tab.id ? 'settings-tab-icon-wrap--active' : ''">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path :d="tab.icon"/>
                </svg>
              </span>
              <span>{{ tab.label }}</span>
              <span v-if="activeTab === tab.id" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></span>
            </button>
          </aside>

          <!-- ── Mobile tab scroller ───────────────────────────────── -->
          <div class="lg:hidden w-full overflow-x-auto pb-1 mx-0">
            <div class="flex gap-2 min-w-max px-0.5 py-1">
              <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
                      :class="['mobile-tab-btn', activeTab === tab.id ? 'mobile-tab-btn--active' : '']">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <path :d="tab.icon"/>
                </svg>
                {{ tab.label }}
              </button>
            </div>
          </div>

          <!-- ── Content Panel ──────────────────────────────────────── -->
          <div class="flex-1 min-w-0">
            <Transition name="panel-fade" mode="out-in">

              <!-- ════════════════ GENERAL ════════════════ -->
              <div v-if="activeTab === 'general'" key="general" class="space-y-5">

                <!-- Email -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#f3e8ff;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Email Address</h2>
                      <p class="settings-card-desc">Update your account email</p>
                    </div>
                  </div>
                  <div class="space-y-3 mt-4">
                    <div class="settings-field-group">
                      <label class="settings-label">Current Email</label>
                      <input :value="emailForm.current" disabled class="settings-input settings-input--disabled"/>
                    </div>
                    <div class="settings-field-group">
                      <label class="settings-label">New Email</label>
                      <input v-model="emailForm.new" type="email" placeholder="you@example.com" class="settings-input"/>
                    </div>
                    <div class="settings-field-group">
                      <label class="settings-label">Password</label>
                      <div class="settings-input-wrap">
                        <input v-model="emailForm.password" :type="showEmailPw ? 'text' : 'password'" placeholder="Your Password to Change Email" class="settings-input"/>
                        <button @click="showEmailPw = !showEmailPw" class="settings-eye-btn">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8-4 8-4-8-11-8-4 8-11 8z"/><circle cx="12" cy="12" r="3"/></svg>
                        </button>
                      </div>
                    </div>
                    <div class="flex items-center gap-3 pt-1">
                      <button @click="saveEmail" :disabled="savingEmail" class="settings-btn settings-btn--primary">
                        <svg v-if="savingEmail" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                        {{ savingEmail ? 'Saving…' : 'Update Email' }}
                      </button>
                      <Transition name="success-pop">
                        <span v-if="successEmail" class="settings-success">✦ Updated!</span>
                      </Transition>
                    </div>
                  </div>
                </div>

                <!-- Password -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fdf4ff;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Change Password</h2>
                      <p class="settings-card-desc">Keep your account secure</p>
                    </div>
                  </div>
                  <div class="space-y-3 mt-4">
                    <div class="settings-field-group">
                      <label class="settings-label">Current Password</label>
                      <div class="settings-input-wrap">
                        <input v-model="passwordForm.current" :type="showCurrentPw ? 'text' : 'password'" placeholder="••••••••" class="settings-input"/>
                        <button @click="showCurrentPw = !showCurrentPw" class="settings-eye-btn">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path v-if="!showCurrentPw" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle v-if="!showCurrentPw" cx="12" cy="12" r="3"/><path v-if="showCurrentPw" d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line v-if="showCurrentPw" x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                      </div>
                    </div>
                    <div class="settings-field-group">
                      <label class="settings-label">New Password</label>
                      <div class="settings-input-wrap">
                        <input v-model="passwordForm.new" :type="showNewPw ? 'text' : 'password'" placeholder="Min 8 characters" class="settings-input"/>
                        <button @click="showNewPw = !showNewPw" class="settings-eye-btn">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path v-if="!showNewPw" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle v-if="!showNewPw" cx="12" cy="12" r="3"/><path v-if="showNewPw" d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line v-if="showNewPw" x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                      </div>
                    </div>
                    <div class="settings-field-group">
                      <label class="settings-label">Confirm New Password</label>
                      <div class="settings-input-wrap">
                        <input v-model="passwordForm.confirm" :type="showConfirmPw ? 'text' : 'password'" placeholder="Confirm new password" class="settings-input"/>
                        <button @click="showConfirmPw = !showConfirmPw" class="settings-eye-btn">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path v-if="!showConfirmPw" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle v-if="!showConfirmPw" cx="12" cy="12" r="3"/><path v-if="showConfirmPw" d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line v-if="showConfirmPw" x1="1" y1="1" x2="23" y2="23"/></svg>
                        </button>
                      </div>
                    </div>
                    <div class="flex items-center gap-3 pt-1">
                      <button @click="savePassword" :disabled="savingPassword" class="settings-btn settings-btn--primary">
                        <svg v-if="savingPassword" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                        {{ savingPassword ? 'Saving…' : 'Change Password' }}
                      </button>
                      <Transition name="success-pop">
                        <span v-if="successPassword" class="settings-success">✦ Changed!</span>
                      </Transition>
                    </div>
                  </div>
                </div>

                <!-- Notifications -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fdf2f8;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#db2777" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Notifications</h2>
                      <p class="settings-card-desc">Choose what you hear about</p>
                    </div>
                  </div>
                  <div class="mt-4 space-y-3">
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Email notifications</p>
                        <p class="settings-toggle-desc">Receive updates via email</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': notifEmail }" @click="notifEmail = !notifEmail">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Push notifications</p>
                        <p class="settings-toggle-desc">In-app alerts on your devices</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': notifPush }" @click="notifPush = !notifPush">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Bloom alerts</p>
                        <p class="settings-toggle-desc">Get notified when a seed blooms</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': notifBlooms }" @click="notifBlooms = !notifBlooms">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Signal alerts</p>
                        <p class="settings-toggle-desc">Know when your partner sends you a thought</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': notifSignals }" @click="notifSignals = !notifSignals">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                  </div>
                </div>
              </div>

              <!-- ════════════════ VAULT ════════════════ -->
              <div v-else-if="activeTab === 'vault'" key="vault" class="space-y-5">

                <!-- Current vault info -->
                <div class="settings-card" style="background: linear-gradient(145deg,#1e1530,#2d1b4e); border-color: rgba(124,58,237,0.3);">
                  <div class="flex items-center gap-4">
                    <div class="w-14 h-14 rounded-2xl flex items-center justify-center shrink-0" style="background: linear-gradient(135deg,#7c3aed,#a855f7);">
                      <svg width="24" height="24" viewBox="0 0 48 48" fill="none">
                        <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white"/>
                      </svg>
                    </div>
                    <div>
                      <p class="settings-sub text-purple-400" style="font-size:0.65rem; margin-bottom:2px;">Active Vault</p>
                      <h3 class="settings-display text-white" style="font-size:1.4rem;">Amara & Jordan</h3>
                      <p class="settings-body" style="font-size:0.75rem; color:rgba(167,139,250,0.7);">Member since March 2024 · 24 memories</p>
                    </div>
                  </div>
                </div>

                <!-- Switch Vault -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#f5f0ff;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Switch Vault</h2>
                      <p class="settings-card-desc">Join a different vault with an invitation code</p>
                    </div>
                  </div>

                  <div class="mt-4 p-4 rounded-xl border border-amber-100 bg-amber-50">
                    <div class="flex gap-2.5 items-start">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" class="shrink-0 mt-0.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                      <p class="settings-body text-amber-800" style="font-size:0.78rem; line-height:1.6;">Switching vaults will <strong>permanently remove you</strong> from your current vault. All your added memories stay in the vault, but you'll lose access. This cannot be undone.</p>
                    </div>
                  </div>

                  <div v-if="!showSwitchVault" class="mt-4">
                    <button @click="showSwitchVault = true" class="settings-btn settings-btn--secondary">Enter Invitation Code</button>
                  </div>

                  <Transition name="expand">
                    <div v-if="showSwitchVault" class="mt-4 space-y-3">
                      <div class="settings-field-group">
                        <label class="settings-label">Invitation Code</label>
                        <input v-model="switchCode" type="text" maxlength="8" placeholder="8-character code"
                              class="settings-input font-mono tracking-widest uppercase text-center" style="letter-spacing:0.25em;"/>
                        <p v-if="switchCodeError" class="text-xs text-red-500 mt-1 settings-body">{{ switchCodeError }}</p>
                      </div>
                      <div class="flex gap-2">
                        <button @click="switchVault" :disabled="switchingVault" class="settings-btn settings-btn--primary">
                          <svg v-if="switchingVault" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                          {{ switchingVault ? 'Switching…' : 'Switch Vault' }}
                        </button>
                        <button @click="showSwitchVault = false; switchCode = ''" class="settings-btn settings-btn--ghost">Cancel</button>
                      </div>
                    </div>
                  </Transition>
                </div>

                <!-- Leave Vault -->
                <div class="settings-card settings-card--danger">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fef2f2;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title text-red-600">Leave Vault</h2>
                      <p class="settings-card-desc">Remove yourself from this shared vault</p>
                    </div>
                  </div>

                  <div v-if="!showLeaveConfirm" class="mt-4">
                    <button @click="showLeaveConfirm = true" class="settings-btn settings-btn--danger">Leave this Vault</button>
                  </div>

                  <Transition name="expand">
                    <div v-if="showLeaveConfirm" class="mt-4 p-4 rounded-xl border border-red-100 bg-red-50">
                      <p class="settings-body text-red-700 text-sm mb-4" style="line-height:1.6;">Are you sure? You'll lose access to all shared memories and seeds. Your partner's vault will remain intact.</p>
                      <div class="flex gap-2">
                        <button @click="leaveVault" :disabled="leavingVault" class="settings-btn settings-btn--danger">
                          <svg v-if="leavingVault" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                          {{ leavingVault ? 'Leaving…' : 'Yes, Leave Vault' }}
                        </button>
                        <button @click="showLeaveConfirm = false" class="settings-btn settings-btn--ghost">Cancel</button>
                      </div>
                    </div>
                  </Transition>

                  <Transition name="success-pop">
                    <div v-if="leaveSuccess" class="mt-3 flex items-center gap-2 text-xs settings-body text-green-600">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                      You have left the vault.
                    </div>
                  </Transition>
                </div>
              </div>

              <!-- ════════════════ PROFILE ════════════════ -->
              <div v-else-if="activeTab === 'profile'" key="profile" class="space-y-5">

                <!-- Avatar + display name -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fdf4ff;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Display Name</h2>
                      <p class="settings-card-desc">How you appear to your partner</p>
                    </div>
                  </div>

                  <!-- Avatar preview -->
                  <div class="flex items-center gap-4 mt-5 mb-4">
                    <div class="relative">
                      <div class="w-16 h-16 rounded-2xl flex items-center justify-center text-white text-2xl font-bold"
                          style="background: linear-gradient(135deg,#7c3aed,#ec4899); font-family:'Cormorant Garamond',serif;">
                        {{ displayName?.charAt(0) || 'U' }}
                      </div>
                      <!-- Small hibiscus badge -->
                      <img src="/images/hibiscus_placeholder.png" alt=""
                          class="absolute -bottom-1 -right-1 w-5 h-5 opacity-60"
                          style="filter: hue-rotate(260deg) saturate(0.8);"/>
                    </div>
                    <div>
                      <p class="settings-display" style="font-size:1.1rem; color:#1f2937;">{{ displayName }}</p>
                      <p class="settings-body" style="font-size:0.75rem; color:#9ca3af;">Your vault identity</p>
                    </div>
                  </div>

                  <div class="settings-field-group">
                    <label class="settings-label">Display Name</label>
                    <input v-model="displayName" type="text" placeholder="Your name" class="settings-input"/>
                  </div>
                  <div class="flex items-center gap-3 mt-3">
                    <button @click="saveName" :disabled="savingName" class="settings-btn settings-btn--primary">
                      <svg v-if="savingName" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                      {{ savingName ? 'Saving…' : 'Save Name' }}
                    </button>
                    <Transition name="success-pop">
                      <span v-if="successName" class="settings-success">✦ Saved!</span>
                    </Transition>
                  </div>
                </div>

                <!-- Data export -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#f0fdf4;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Export Your Data</h2>
                      <p class="settings-card-desc">Download a copy of your memories and seeds</p>
                    </div>
                  </div>
                  <div class="mt-4">
                    <button @click="console.log('export data')" class="settings-btn settings-btn--secondary">
                      Request Data Export
                    </button>
                    <p class="settings-body mt-2" style="font-size:0.72rem; color:#9ca3af;">We'll email you a download link within 24 hours.</p>
                  </div>
                </div>

                <!-- Delete account -->
                <div class="settings-card settings-card--danger">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fef2f2;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title text-red-600">Delete Account</h2>
                      <p class="settings-card-desc">Permanently erase your account and all data</p>
                    </div>
                  </div>

                  <div v-if="!showDeleteConfirm" class="mt-4">
                    <button @click="showDeleteConfirm = true" class="settings-btn settings-btn--danger">Delete My Account</button>
                  </div>

                  <Transition name="expand">
                    <div v-if="showDeleteConfirm" class="mt-4 space-y-3">
                      <div class="p-4 rounded-xl border border-red-100 bg-red-50">
                        <p class="settings-body text-red-700 text-sm" style="line-height:1.65;">This will <strong>permanently delete</strong> your account, remove you from your vault, and erase all your personal data. This action <strong>cannot be reversed</strong>.</p>
                      </div>
                      <div class="settings-field-group">
                        <label class="settings-label">Type <span class="font-mono font-bold text-red-500">DELETE</span> to confirm</label>
                        <input v-model="deleteConfirmText" type="text" placeholder="DELETE" class="settings-input"/>
                      </div>
                      <div class="flex gap-2">
                        <button @click="deleteAccount"
                                :disabled="deleteConfirmText !== 'DELETE' || deletingAccount"
                                :class="['settings-btn settings-btn--danger', deleteConfirmText !== 'DELETE' ? 'opacity-40 cursor-not-allowed' : '']">
                          <svg v-if="deletingAccount" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
                          {{ deletingAccount ? 'Deleting…' : 'Permanently Delete' }}
                        </button>
                        <button @click="showDeleteConfirm = false; deleteConfirmText = ''" class="settings-btn settings-btn--ghost">Cancel</button>
                      </div>
                    </div>
                  </Transition>
                </div>
              </div>

              <!-- ════════════════ PRIVACY ════════════════ -->
              <div v-else-if="activeTab === 'privacy'" key="privacy" class="space-y-5">

                <!-- Visibility -->
                <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#f0f9ff;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Visibility</h2>
                      <p class="settings-card-desc">Control what your partner can see</p>
                    </div>
                  </div>
                  <div class="mt-4 space-y-3">
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Read receipts</p>
                        <p class="settings-toggle-desc">Let your partner know when you've seen a memory</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': privacyReadReceipts }" @click="privacyReadReceipts = !privacyReadReceipts">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Activity status</p>
                        <p class="settings-toggle-desc">Show when you were last active in the vault</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': privacyActivity }" @click="privacyActivity = !privacyActivity">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                    <label class="settings-toggle-row">
                      <div>
                        <p class="settings-toggle-title">Signal count</p>
                        <p class="settings-toggle-desc">Let your partner see how many thoughts you've sent today</p>
                      </div>
                      <div class="settings-toggle" :class="{ 'settings-toggle--on': privacySignalCount }" @click="privacySignalCount = !privacySignalCount">
                        <div class="settings-toggle-knob"></div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Active Sessions -->
                <!-- <div class="settings-card">
                  <div class="settings-card-header">
                    <div class="settings-card-icon-wrap" style="background:#fefce8;">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ca8a04" stroke-width="2" stroke-linecap="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                    </div>
                    <div>
                      <h2 class="settings-card-title">Active Sessions</h2>
                      <p class="settings-card-desc">Devices currently signed in</p>
                    </div>
                  </div>
                  <div class="mt-4 space-y-2">
                    <div v-for="session in mockSessions" :key="session.device"
                        class="flex items-center justify-between p-3 rounded-xl border transition-all"
                        :class="session.current ? 'border-purple-100 bg-purple-50' : 'border-gray-100 bg-white hover:border-gray-200'">
                      <div class="flex items-center gap-3">
                        <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', session.current ? 'bg-purple-100' : 'bg-gray-100']">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" :stroke="session.current ? '#7c3aed' : '#9ca3af'" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
                        </div>
                        <div>
                          <p class="settings-body text-gray-800" style="font-size:0.8125rem; font-weight:500;">{{ session.device }}</p>
                          <p class="settings-body text-gray-400" style="font-size:0.7rem;">{{ session.location }} · {{ session.time }}</p>
                        </div>
                      </div>
                      <span v-if="session.current" class="text-xs settings-body text-purple-600 font-semibold px-2 py-0.5 bg-purple-100 rounded-full">This device</span>
                      <button v-else @click="console.log('revoke session')"
                              class="text-xs settings-body text-red-500 hover:text-red-700 transition-colors font-medium">Revoke</button>
                    </div>
                  </div>
                </div> -->
              </div>

            </Transition>
          </div>
        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>

</template>

<style scoped>
.settings-page {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(160deg, #faf5ff 0%, #ffffff 50%, #fdf4ff 100%);
  overflow: hidden;
}

/* ── Typography ──────────────────────────────────────────────────── */
.settings-display { font-family: 'Cormorant Garamond', Georgia, serif; font-weight: 500; }
.settings-body    { font-family: 'DM Sans', sans-serif; }
.settings-sub     { font-family: 'DM Sans', sans-serif; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #a855f7; font-weight: 500; }

/* ── Inner sidebar tabs (desktop) ───────────────────────────────── */
.settings-tab-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.18s ease;
  cursor: pointer;
  border: 1px solid transparent;
  background: transparent;
  text-align: left;
}
.settings-tab-btn:hover {
  background: rgba(124,58,237,0.06);
  color: #7c3aed;
}
.settings-tab-btn--active {
  background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(168,85,247,0.06));
  color: #6d28d9;
  font-weight: 600;
  border-color: rgba(124,58,237,0.15);
  box-shadow: 0 2px 8px rgba(124,58,237,0.08);
}
.settings-tab-icon-wrap {
  width: 28px; height: 28px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  background: #f3f4f6;
  color: #9ca3af;
  flex-shrink: 0;
  transition: all 0.18s ease;
}
.settings-tab-icon-wrap--active {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  box-shadow: 0 2px 8px rgba(124,58,237,0.3);
}

/* ── Mobile tabs ─────────────────────────────────────────────────── */
.mobile-tab-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 500;
  color: #6b7280;
  background: white;
  border: 1.5px solid #f0ebff;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s ease;
}
.mobile-tab-btn--active {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 14px rgba(124,58,237,0.25);
}

/* ── Cards ───────────────────────────────────────────────────────── */
.settings-card {
  background: white;
  border: 1.5px solid #f3e8ff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 2px 16px rgba(124,58,237,0.05);
  animation: cardIn 0.45s cubic-bezier(0.22,1,0.36,1) both;
}
.settings-card--danger {
  border-color: #fee2e2;
}
@keyframes cardIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.settings-card-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.settings-card-icon-wrap {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.settings-card-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.2;
}
.settings-card-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  color: #9ca3af;
  margin-top: 2px;
}

/* ── Form fields ─────────────────────────────────────────────────── */
.settings-field-group { display: flex; flex-direction: column; gap: 5px; }
.settings-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.settings-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1.5px solid #e9d5ff;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.875rem;
  color: #1f2937;
  background: white;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.settings-input:focus {
  border-color: #a855f7;
  box-shadow: 0 0 0 3px rgba(168,85,247,0.1);
}
.settings-input::placeholder { color: #d1d5db; }
.settings-input--disabled {
  background: #faf5ff;
  color: #9ca3af;
  cursor: not-allowed;
}
.settings-input-wrap { position: relative; }
.settings-input-wrap .settings-input { padding-right: 40px; }
.settings-eye-btn {
  position: absolute;
  right: 12px; top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  transition: color 0.15s;
  cursor: pointer;
}
.settings-eye-btn:hover { color: #7c3aed; }

/* ── Buttons ─────────────────────────────────────────────────────── */
.settings-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 18px;
  border-radius: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s ease;
  border: 1.5px solid transparent;
}
.settings-btn--primary {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  box-shadow: 0 4px 14px rgba(124,58,237,0.25);
}
.settings-btn--primary:hover:not(:disabled) {
  box-shadow: 0 6px 20px rgba(124,58,237,0.35);
  transform: translateY(-1px);
}
.settings-btn--primary:disabled { opacity: 0.6; cursor: not-allowed; }
.settings-btn--secondary {
  background: white;
  color: #7c3aed;
  border-color: #e9d5ff;
}
.settings-btn--secondary:hover {
  background: #faf5ff;
  border-color: #c084fc;
}
.settings-btn--danger {
  background: white;
  color: #ef4444;
  border-color: #fecaca;
}
.settings-btn--danger:hover:not(:disabled) {
  background: #fef2f2;
  border-color: #f87171;
}
.settings-btn--ghost {
  background: transparent;
  color: #6b7280;
  border-color: #e5e7eb;
}
.settings-btn--ghost:hover { background: #f9fafb; }

/* ── Success label ────────────────────────────────────────────────── */
.settings-success {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #7c3aed;
  font-weight: 600;
}

/* ── Toggle ──────────────────────────────────────────────────────── */
.settings-toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1.5px solid #f3e8ff;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.settings-toggle-row:hover { background: #faf5ff; border-color: #e9d5ff; }
.settings-toggle-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #374151;
}
.settings-toggle-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: #9ca3af;
  margin-top: 1px;
}
.settings-toggle {
  width: 40px; height: 22px;
  border-radius: 11px;
  background: #e5e7eb;
  position: relative;
  cursor: pointer;
  transition: background 0.25s;
  flex-shrink: 0;
}
.settings-toggle--on {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
}
.settings-toggle-knob {
  position: absolute;
  top: 3px; left: 3px;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
  transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1);
}
.settings-toggle--on .settings-toggle-knob {
  transform: translateX(18px);
}

/* ── Transitions ─────────────────────────────────────────────────── */
.panel-fade-enter-active, .panel-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
}
.panel-fade-enter-from, .panel-fade-leave-to {
  opacity: 0;
  transform: translateX(12px);
}

.expand-enter-active, .expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.expand-enter-from, .expand-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-6px);
}
.expand-enter-to, .expand-leave-from {
  opacity: 1;
  max-height: 400px;
}

.success-pop-enter-active, .success-pop-leave-active {
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.success-pop-enter-from, .success-pop-leave-to {
  opacity: 0;
  transform: scale(0.85) translateY(4px);
}

.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
</style>