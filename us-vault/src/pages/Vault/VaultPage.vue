<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { getVaultDetailsApi } from '../../api/vault'
import { useAuthStore } from '../../stores/auth'

// ── Data ─────────────────────────────────────────────────────────────────────
const vault = ref(null)
const isLoading = ref(true)

const auth = useAuthStore()
const user = computed(() => auth.user)

const creatorName = computed(() => vault.value?.created_by || '')
const partnerName = computed(() => vault.value?.partner_name || '')

const otherPerson = computed(() => {
  if (!vault.value || !user.value) return ''

  // If logged in user is creator → other is partner
  if (user.value.display_name === creatorName.value) {
    return partnerName.value
  }

  // Otherwise logged in user is partner → other is creator
  return creatorName.value
})

const loadVaultDetails = async () => {
  try {
    isLoading.value = true

    const res = await getVaultDetailsApi()
    vault.value = res.data

  } catch (err) {
    console.error("Failed to load vault details")
    vault.value = null
  } finally {
    isLoading.value = false
  }
}

// ── Computed ──────────────────────────────────────────────────────────────────
const formattedDate = (iso) => {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'long', day: 'numeric', year: 'numeric'
  })
}

const vaultAge = computed(() => {
  if (!vault.value) return ''
  const start = new Date(vault.value.created_at)
  const now = new Date()
  const months = (now.getFullYear() - start.getFullYear()) * 12 + (now.getMonth() - start.getMonth())
  if (months < 1) return 'Less than a month'
  if (months === 1) return '1 month'
  if (months < 12) return `${months} months`
  const years = Math.floor(months / 12)
  const rem = months % 12
  return rem === 0 ? `${years} year${years > 1 ? 's' : ''}` : `${years}y ${rem}m`
})

const statusConfig = computed(() => {
  const s = vault.value?.status
  if (s === 'active') return { label: 'Active', dot: '#22c55e', text: 'text-green-700', bg: 'bg-green-50', border: 'border-green-200' }
  if (s === 'paused') return { label: 'Paused', dot: '#f59e0b', text: 'text-amber-700', bg: 'bg-amber-50', border: 'border-amber-200' }
  return { label: 'Closed', dot: '#ef4444', text: 'text-red-700', bg: 'bg-red-50', border: 'border-red-200' }
})

const initials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(loadVaultDetails)
</script>

<template>
  <InactivityOverlay>
        <Sidebar>
      <div class="vault-page min-h-screen relative overflow-x-hidden">

        <!-- Google Fonts -->
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');
        </component>

        <!-- ── Decorative Background ──────────────────────────────────── -->
        <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
          <!-- Ambient glow blobs -->
          <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full opacity-20"
              style="background: radial-gradient(circle, #ddd6fe 0%, transparent 70%);"></div>
          <div class="absolute top-1/3 -right-32 w-80 h-80 rounded-full opacity-15"
              style="background: radial-gradient(circle, #fbcfe8 0%, transparent 70%);"></div>
          <div class="absolute -bottom-16 left-1/3 w-64 h-64 rounded-full opacity-10"
              style="background: radial-gradient(circle, #c4b5fd 0%, transparent 70%);"></div>

          <!-- Thin decorative lines -->
          <svg class="absolute top-0 right-0 w-64 h-64 opacity-10" viewBox="0 0 200 200">
            <circle cx="200" cy="0" r="120" fill="none" stroke="#7c3aed" stroke-width="0.8"/>
            <circle cx="200" cy="0" r="80" fill="none" stroke="#a855f7" stroke-width="0.5"/>
            <circle cx="200" cy="0" r="40" fill="none" stroke="#c084fc" stroke-width="0.4"/>
          </svg>

          <svg class="absolute bottom-0 left-0 w-48 h-48 opacity-10" viewBox="0 0 200 200">
            <circle cx="0" cy="200" r="120" fill="none" stroke="#7c3aed" stroke-width="0.8"/>
            <circle cx="0" cy="200" r="80" fill="none" stroke="#a855f7" stroke-width="0.5"/>
          </svg>

          <!-- Locket chain motif top -->
          <div class="absolute top-0 left-1/2 -translate-x-1/2 flex flex-col items-center gap-0">
            <div v-for="i in 6" :key="i"
                class="w-0.5 bg-linear-to-b from-purple-200 to-transparent"
                :style="`height: ${14 + i * 4}px; opacity: ${0.6 - i * 0.08};`"></div>
          </div>

          <!-- Floating petals (CSS animated) -->
          <svg class="petal petal-1 absolute w-8 opacity-25" viewBox="0 0 40 60">
            <ellipse cx="20" cy="30" rx="12" ry="26" fill="#c084fc"/>
          </svg>
          <svg class="petal petal-2 absolute w-6 opacity-20" viewBox="0 0 40 60">
            <ellipse cx="20" cy="30" rx="10" ry="22" fill="#f0abfc"/>
          </svg>
          <svg class="petal petal-3 absolute w-5 opacity-15" viewBox="0 0 40 60">
            <ellipse cx="20" cy="30" rx="9" ry="20" fill="#a855f7"/>
          </svg>
          <svg class="petal petal-4 absolute w-7 opacity-20" viewBox="0 0 40 60">
            <ellipse cx="20" cy="30" rx="11" ry="24" fill="#e879f9"/>
          </svg>
        </div>

        <!-- ── Loading ──────────────────────────────────────────────── -->
        <div v-if="isLoading" class="relative z-10 flex flex-col items-center justify-center min-h-[80vh] gap-6">
          <div class="locket-spinner">
            <svg width="64" height="64" viewBox="0 0 64 64" class="animate-spin-slow">
              <circle cx="32" cy="32" r="28" fill="none" stroke="#e9d5ff" stroke-width="2"/>
              <circle cx="32" cy="32" r="28" fill="none" stroke="#7c3aed" stroke-width="2"
                      stroke-dasharray="44 132" stroke-linecap="round"/>
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
                      fill="#c084fc" stroke="#7c3aed" stroke-width="1.5"/>
              </svg>
            </div>
          </div>
          <p class="vault-body text-sm text-purple-400 tracking-widest uppercase">Opening your vault…</p>
        </div>

        <!-- ── Main Content ────────────────────────────────────────── -->
        <div v-else-if="vault" class="relative z-10 max-w-4xl mx-auto px-4 sm:px-8 py-12 fade-in">

          <!-- ── Hero Header ─────────────────────────────────────── -->
          <div class="text-center mb-14 relative">
            <!-- Locket icon -->
            <div class="inline-flex flex-col items-center mb-6">
              <div class="relative">
                <!-- Outer ring -->
                <div class="w-28 h-28 rounded-full border-2 border-purple-200 flex items-center justify-center"
                    style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); box-shadow: 0 8px 32px rgba(124,58,237,0.12), inset 0 1px 0 rgba(255,255,255,0.8);">
                  <!-- Inner locket face -->
                  <div class="w-20 h-20 rounded-full flex items-center justify-center border border-purple-100"
                      style="background: linear-gradient(145deg, #ede9fe, #fdf4ff);">
                    <svg width="38" height="38" viewBox="0 0 48 48" fill="none">
                      <!-- Heart inside locket -->
                      <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z"
                            fill="url(#locketGrad)" stroke="#7c3aed" stroke-width="1"/>
                      <defs>
                        <linearGradient id="locketGrad" x1="6" y1="6" x2="42" y2="40" gradientUnits="userSpaceOnUse">
                          <stop offset="0%" stop-color="#c084fc"/>
                          <stop offset="100%" stop-color="#7c3aed"/>
                        </linearGradient>
                      </defs>
                    </svg>
                  </div>
                </div>
                <!-- Status dot -->
                <span class="absolute bottom-1 right-1 w-4 h-4 rounded-full border-2 border-white"
                      :style="`background-color: ${statusConfig.dot};`"></span>
              </div>
            </div>

            <!-- Names -->
            <h1 class="vault-display text-4xl sm:text-5xl text-gray-900 mb-2">
              {{ creatorName }}
              <span class="text-purple-400 mx-3 text-3xl">✦</span>
              {{ otherPerson }}
            </h1>
            <p class="vault-body text-gray-500 text-sm tracking-widest uppercase mb-5">Our Shared Vault</p>

            <!-- Status badge -->
            <span :class="`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold border ${statusConfig.bg} ${statusConfig.text} ${statusConfig.border}`">
              <span class="w-1.5 h-1.5 rounded-full animate-pulse" :style="`background: ${statusConfig.dot}`"></span>
              {{ statusConfig.label }}
            </span>
          </div>

          <!-- ── Partners Card ───────────────────────────────────── -->
          <div class="relative rounded-3xl p-8 mb-8 overflow-hidden"
              style="background: linear-gradient(135deg, #1e1b2e 0%, #2d1b4e 50%, #1a0a2e 100%); box-shadow: 0 20px 60px rgba(124,58,237,0.2);">

            <!-- Inner shimmer -->
            <div class="absolute inset-0 rounded-3xl opacity-10"
                style="background: repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.03) 20px, rgba(255,255,255,0.03) 40px);"></div>

            <!-- Corner flourishes -->
            <div class="absolute top-4 left-4 text-purple-700 opacity-40 text-2xl select-none">✦</div>
            <div class="absolute top-4 right-4 text-purple-700 opacity-40 text-2xl select-none">✦</div>
            <div class="absolute bottom-4 left-4 text-purple-700 opacity-30 text-lg select-none">◆</div>
            <div class="absolute bottom-4 right-4 text-purple-700 opacity-30 text-lg select-none">◆</div>

            <div class="relative flex flex-col sm:flex-row items-center gap-8 justify-center">
              <!-- Person A -->
              <div class="flex flex-col items-center gap-3">
                <div class="w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-bold"
                    style="background: linear-gradient(135deg, #7c3aed, #a855f7); box-shadow: 0 4px 20px rgba(124,58,237,0.4);">
                  {{ initials(vault.created_by) }}
                </div>
                <div class="text-center">
                  <p class="vault-display text-white text-lg">{{ creatorName }}</p>
                  <p class="vault-body text-purple-400 text-xs tracking-widest uppercase">Created by</p>
                </div>
              </div>

              <!-- Divider -->
              <div class="flex flex-col items-center gap-2 text-purple-600">
                <div class="w-px h-8 bg-linear-to-b from-transparent via-purple-600 to-transparent hidden sm:block"></div>
                <svg width="28" height="28" viewBox="0 0 48 48" fill="none" class="opacity-60">
                  <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z"
                        fill="#7c3aed"/>
                </svg>
                <div class="w-px h-8 bg-linear-to-b from-transparent via-purple-600 to-transparent hidden sm:block"></div>
              </div>

              <!-- Person B -->
              <div class="flex flex-col items-center gap-3">
                <div class="w-16 h-16 rounded-full flex items-center justify-center text-white text-xl font-bold"
                    style="background: linear-gradient(135deg, #db2777, #ec4899); box-shadow: 0 4px 20px rgba(219,39,119,0.35);">
                  {{ initials(otherPerson) }}
                </div>
                <div class="text-center">
                  <p class="vault-display text-white text-lg">
                    {{ otherPerson }}
                  </p>
                  <p class="vault-body text-pink-400 text-xs tracking-widest uppercase">Partner</p>
                </div>
              </div>
            </div>

            <!-- Together since -->
            <div class="relative mt-8 pt-6 border-t border-white/10 text-center">
              <p class="vault-body text-purple-300 text-xs tracking-widest uppercase mb-1">Vault opened</p>
              <p class="vault-display text-white text-xl">{{ formattedDate(vault.created_at) }}</p>
              <p class="vault-body text-purple-400 text-sm mt-1">{{ vaultAge }} of shared moments</p>
            </div>
          </div>

          <!-- ── Stats Grid ──────────────────────────────────────── -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-8">

            <!-- Stat Card component inline -->
            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-purple-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="absolute top-0 right-0 w-16 h-16 opacity-5">
                <svg viewBox="0 0 64 64"><circle cx="64" cy="0" r="48" fill="#7c3aed"/></svg>
              </div>
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #f3e8ff;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_memories }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Memories</p>
            </div>

            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-purple-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="absolute top-0 right-0 w-16 h-16 opacity-5">
                <svg viewBox="0 0 64 64"><circle cx="64" cy="0" r="48" fill="#7c3aed"/></svg>
              </div>
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #fdf4ff;">
                <svg width="18" height="18" viewBox="0 0 60 60" fill="none">
                  <ellipse cx="30" cy="34" rx="14" ry="20" fill="#a855f7"/>
                  <ellipse cx="30" cy="22" rx="8" ry="10" fill="#c084fc" opacity="0.7"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_seeds }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Seeds</p>
            </div>

            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-pink-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="absolute top-0 right-0 w-16 h-16 opacity-5">
                <svg viewBox="0 0 64 64"><circle cx="64" cy="0" r="48" fill="#db2777"/></svg>
              </div>
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #fdf2f8;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#db2777" stroke-width="2" stroke-linecap="round">
                  <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                  <polyline points="13 2 13 9 20 9"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_signals }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Signals</p>
            </div>

            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-blue-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #eff6ff;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round">
                  <rect x="3" y="3" width="18" height="18" rx="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21 15 16 10 5 21"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_images }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Images</p>
            </div>

            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-rose-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #fff1f2;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round">
                  <polygon points="23 7 16 12 23 17 23 7"/>
                  <rect x="1" y="5" width="15" height="14" rx="2"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_videos }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Videos</p>
            </div>

            <!-- Media total combined -->
            <div class="stat-card group relative rounded-2xl p-5 bg-white border border-gray-100 hover:border-amber-200 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg overflow-hidden"
                style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
              <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style="background: #fffbeb;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <p class="vault-display text-3xl text-gray-900 mb-1">{{ vault.stats.total_images + vault.stats.total_videos }}</p>
              <p class="vault-body text-xs text-gray-500 tracking-wide uppercase">Total Media</p>
            </div>
          </div>

          <!-- ── Timeline Card ───────────────────────────────────── -->
          <div class="rounded-2xl bg-white border border-gray-100 p-6 mb-8"
              style="box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
            <h3 class="vault-display text-lg text-gray-800 mb-5 flex items-center gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2" stroke-linecap="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              Timeline
            </h3>

            <div class="relative pl-6">
              <!-- Vertical line -->
              <div class="absolute left-2 top-2 bottom-2 w-px"
                  style="background: linear-gradient(to bottom, #7c3aed, #c084fc, transparent);"></div>

              <!-- First memory -->
              <div class="relative mb-6">
                <div class="absolute -left-4 top-0.5 w-3 h-3 rounded-full border-2 border-white"
                    style="background: #7c3aed; box-shadow: 0 0 0 3px #ede9fe;"></div>
                <p class="vault-body text-xs text-purple-500 uppercase tracking-widest mb-0.5">First Memory</p>
                <p class="vault-display text-gray-800 text-base">{{ formattedDate(vault.stats.first_memory_date) }}</p>
              </div>

              <!-- Last activity -->
              <div class="relative mb-6">
                <div class="absolute -left-4 top-0.5 w-3 h-3 rounded-full border-2 border-white"
                    style="background: #a855f7; box-shadow: 0 0 0 3px #f3e8ff;"></div>
                <p class="vault-body text-xs text-purple-400 uppercase tracking-widest mb-0.5">Last Activity</p>
                <p class="vault-display text-gray-800 text-base">{{ formattedDate(vault.stats.last_activity_date) }}</p>
              </div>

              <!-- Today marker -->
              <div class="relative">
                <div class="absolute -left-4 top-0.5 w-3 h-3 rounded-full border-2 border-white animate-pulse"
                    style="background: #ec4899; box-shadow: 0 0 0 3px #fce7f3;"></div>
                <p class="vault-body text-xs text-pink-400 uppercase tracking-widest mb-0.5">Today</p>
                <p class="vault-display text-gray-800 text-base">{{ formattedDate(new Date().toISOString()) }}</p>
              </div>
            </div>
          </div>

          <!-- ── Vault ID Footer ─────────────────────────────────── -->
          <div class="text-center py-6 border-t border-gray-100">
            <p class="vault-body text-gray-400 text-xs tracking-widest uppercase mb-2">Vault ID</p>
            <p class="font-mono text-xs text-gray-400 select-all">{{ vault.vault_id }}</p>
            <div class="flex items-center justify-center gap-2 mt-5">
              <div class="w-8 h-px bg-purple-200"></div>
              <svg width="14" height="14" viewBox="0 0 48 48" fill="none">
                <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z"
                      fill="#c084fc"/>
              </svg>
              <div class="w-8 h-px bg-purple-200"></div>
            </div>
          </div>

        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
.vault-page {
  background: linear-gradient(160deg, #fdfaff 0%, #ffffff 50%, #fdf4ff 100%);
}

.vault-display {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-weight: 500;
  line-height: 1.2;
}

.vault-body {
  font-family: 'DM Sans', sans-serif;
}

/* Fade in on load */
.fade-in {
  animation: fadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Stat cards staggered entry */
.stat-card {
  animation: fadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.15s; }
.stat-card:nth-child(3) { animation-delay: 0.2s; }
.stat-card:nth-child(4) { animation-delay: 0.25s; }
.stat-card:nth-child(5) { animation-delay: 0.3s; }
.stat-card:nth-child(6) { animation-delay: 0.35s; }

/* Slow spinner */
.animate-spin-slow {
  animation: spin 3s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* Floating petals */
.petal {
  animation: floatPetal 12s ease-in-out infinite;
  will-change: transform;
}

.petal-1 { top: 15%; left: 5%; animation-delay: 0s; animation-duration: 14s; }
.petal-2 { top: 40%; right: 8%; animation-delay: 3s; animation-duration: 11s; }
.petal-3 { bottom: 30%; left: 12%; animation-delay: 6s; animation-duration: 16s; }
.petal-4 { top: 65%; right: 5%; animation-delay: 9s; animation-duration: 13s; }

@keyframes floatPetal {
  0%   { transform: translateY(0px) rotate(0deg); }
  33%  { transform: translateY(-18px) rotate(12deg); }
  66%  { transform: translateY(-8px) rotate(-8deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}

/* Loading spinner container */
.locket-spinner {
  position: relative;
  width: 64px;
  height: 64px;
}
</style>