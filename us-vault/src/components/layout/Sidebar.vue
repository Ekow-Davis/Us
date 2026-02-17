<template>
  <div class="flex flex-col h-screen" style="font-family: 'DM Sans', sans-serif;">
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
    </component>

    <!-- ── Navbar ──────────────────────────────────────────────────── -->
    <div class="navbar-bar w-full flex items-center z-20 relative px-4" style="height:60px; background: #ffffff; border-bottom: 1px solid #f0ebff;">

      <!-- Hamburger -->
      <button @click="toggleSidebar"
              class="w-9 h-9 flex items-center justify-center rounded-xl transition-all duration-200 hover:bg-purple-50 text-purple-700 flex-shrink-0">
        <Menu :size="20" />
      </button>

      <!-- Logo -->
      <div class="ml-3 flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg,#7c3aed,#a855f7);">
          <svg width="14" height="14" viewBox="0 0 48 48" fill="none">
            <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white"/>
          </svg>
        </div>
        <span class="font-semibold text-gray-900 tracking-tight" style="font-family:'Cormorant Garamond',serif; font-size:1.15rem; letter-spacing:-0.01em;">Us Vault</span>
      </div>

      <div class="flex-1"></div>

      <!-- Profile trigger -->
      <div class="relative" ref="profileMenuRef">
        <button @click="toggleProfileMenu"
                class="flex items-center gap-2.5 pl-3 pr-2 py-1.5 rounded-xl transition-all duration-200 hover:bg-purple-50 group">
          <div class="text-right hidden sm:block">
            <p class="text-xs font-semibold text-gray-800 leading-none" style="font-family:'DM Sans',sans-serif;">{{ user.username }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ user.email }}</p>
          </div>
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0" style="background: linear-gradient(135deg,#ec4899,#a855f7);">
            {{ user.username?.charAt(0)?.toUpperCase() || 'U' }}
          </div>
          <ChevronsUpDown :size="14" class="text-gray-400 group-hover:text-purple-600 transition-colors" />
        </button>

        <!-- Dropdown -->
        <Transition name="dropdown">
          <div v-if="isProfileMenuOpen"
               class="absolute top-full right-0 mt-2 w-52 bg-white rounded-2xl overflow-hidden z-50 border border-purple-50"
               style="box-shadow: 0 16px 48px rgba(124,58,237,0.14), 0 4px 12px rgba(0,0,0,0.06);">
            <!-- User header in dropdown -->
            <div class="px-4 py-3 border-b border-gray-50" style="background: linear-gradient(135deg,#faf5ff,#fff);">
              <p class="text-xs font-semibold text-gray-800" style="font-family:'Cormorant Garamond',serif; font-size:0.95rem;">{{ user.name }}</p>
              <p class="text-xs text-gray-400">{{ user.email }}</p>
            </div>
            <div class="py-1">
              <router-link to="/Account" @click="closeProfileMenu"
                           class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-700 transition-colors">
                <User :size="15" class="text-gray-400" />
                <span style="font-family:'DM Sans',sans-serif; font-size:0.8125rem;">Account</span>
              </router-link>
              <router-link to="/Notifications" @click="closeProfileMenu"
                           class="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-700 transition-colors">
                <Bell :size="15" class="text-gray-400" />
                <span style="font-family:'DM Sans',sans-serif; font-size:0.8125rem;">Notifications</span>
              </router-link>
            </div>
            <div class="border-t border-gray-50 py-1">
              <button @click="handleLogout"
                      class="w-full flex items-center gap-3 px-4 py-2.5 text-sm text-rose-600 hover:bg-rose-50 transition-colors">
                <LogOut :size="15" />
                <span style="font-family:'DM Sans',sans-serif; font-size:0.8125rem;">Log out</span>
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- ── Body ────────────────────────────────────────────────────── -->
    <div class="flex flex-1 overflow-hidden">

      <!-- ── Sidebar ───────────────────────────────────────────────── -->
      <div ref="sidebarRef"
           :class="[
             'sidebar-shell fixed md:relative top-0 md:top-auto left-0 z-30 flex flex-col transition-all duration-300 ease-in-out overflow-hidden',
             'min-h-full md:h-[calc(100vh-60px)]',
             isMobile
               ? (isSidebarOpen ? 'w-64 translate-x-0' : '-translate-x-full w-64')
               : isSidebarOpen ? 'w-64' : 'w-16'
           ]"
           style="background: linear-gradient(180deg, #1a0d2e 0%, #0f0620 60%, #130826 100%);">

        <!-- Decorative top accent line -->
        <div class="h-px w-full flex-shrink-0" style="background: linear-gradient(90deg, transparent, #7c3aed, #c084fc, #ec4899, transparent);"></div>

        <!-- Ambient glow top -->
        <div class="absolute top-0 left-0 right-0 h-48 pointer-events-none"
             style="background: radial-gradient(ellipse at 50% -20%, rgba(124,58,237,0.25) 0%, transparent 70%);"></div>

        <!-- Floating botanical SVG (only when open) -->
        <div v-if="isSidebarOpen" class="absolute bottom-32 right-0 w-24 pointer-events-none opacity-[0.06]" aria-hidden="true">
          <svg viewBox="0 0 80 200" fill="none">
            <path d="M40 200 Q20 150 40 100 Q60 50 40 0" stroke="#c084fc" stroke-width="2"/>
            <ellipse cx="22" cy="80" rx="18" ry="8" fill="#c084fc" transform="rotate(-30 22 80)"/>
            <ellipse cx="58" cy="130" rx="16" ry="7" fill="#a855f7" transform="rotate(25 58 130)"/>
          </svg>
        </div>

        <!-- Nav items -->
        <nav class="relative z-10 flex-1 overflow-y-auto py-4 px-2" style="scrollbar-width: none;">

          <!-- Section: Main -->
          <div v-if="isSidebarOpen" class="px-3 mb-2">
            <span class="text-xs font-semibold uppercase tracking-widest" style="color: rgba(192,132,252,0.4); font-family:'DM Sans',sans-serif; font-size:0.65rem;">Navigate</span>
          </div>

          <router-link to="/Dashboard" :class="navClass('/Dashboard')">
            <div :class="iconWrap('/Dashboard')">
              <Home :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Dashboard</span>
            <div v-if="isSidebarOpen && isActive('/Dashboard')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <!-- Section: Seeds -->
          <div v-if="isSidebarOpen" class="px-3 mt-5 mb-2">
            <span class="text-xs font-semibold uppercase tracking-widest" style="color: rgba(192,132,252,0.4); font-family:'DM Sans',sans-serif; font-size:0.65rem;">Seeds</span>
          </div>
          <div v-else class="my-2 mx-auto w-6 h-px" style="background: rgba(124,58,237,0.3);"></div>

          <router-link to="/add-seed" :class="navClass('/add-seed')">
            <div :class="iconWrap('/add-seed')">
              <Plus :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Plant a Seed</span>
            <div v-if="isSidebarOpen && isActive('/add-seed')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <router-link to="/Seeds" :class="navClass('/Seeds')">
            <div :class="iconWrap('/Seeds')">
              <Sprout :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Seeds</span>
            <div v-if="isSidebarOpen && isActive('/Seeds')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <!-- Section: Memories -->
          <div v-if="isSidebarOpen" class="px-3 mt-5 mb-2">
            <span class="text-xs font-semibold uppercase tracking-widest" style="color: rgba(192,132,252,0.4); font-family:'DM Sans',sans-serif; font-size:0.65rem;">Memories</span>
          </div>
          <div v-else class="my-2 mx-auto w-6 h-px" style="background: rgba(124,58,237,0.3);"></div>

          <router-link to="/add-memory" :class="navClass('/add-memory')">
            <div :class="iconWrap('/add-memory')">
              <FilePlus :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Add Memory</span>
            <div v-if="isSidebarOpen && isActive('/add-memory')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <router-link to="/memories" :class="navClass('/memories')">
            <div :class="iconWrap('/memories')">
              <Heart :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Memories</span>
            <div v-if="isSidebarOpen && isActive('/memories')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <!-- Section: Vault -->
          <div v-if="isSidebarOpen" class="px-3 mt-5 mb-2">
            <span class="text-xs font-semibold uppercase tracking-widest" style="color: rgba(192,132,252,0.4); font-family:'DM Sans',sans-serif; font-size:0.65rem;">Vault</span>
          </div>
          <div v-else class="my-2 mx-auto w-6 h-px" style="background: rgba(124,58,237,0.3);"></div>

          <router-link to="/vault" :class="navClass('/vault')">
            <div :class="iconWrap('/vault')">
              <Shield :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Vault Details</span>
            <div v-if="isSidebarOpen && isActive('/vault')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <router-link to="/Signal" :class="navClass('/Signal')">
            <div :class="iconWrap('/Signal')">
              <Zap :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Signal</span>
            <div v-if="isSidebarOpen && isActive('/Signal')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <!-- Section: System -->
          <div v-if="isSidebarOpen" class="px-3 mt-5 mb-2">
            <span class="text-xs font-semibold uppercase tracking-widest" style="color: rgba(192,132,252,0.4); font-family:'DM Sans',sans-serif; font-size:0.65rem;">System</span>
          </div>
          <div v-else class="my-2 mx-auto w-6 h-px" style="background: rgba(124,58,237,0.3);"></div>

          <router-link to="/Settings" :class="navClass('/Settings')">
            <div :class="iconWrap('/Settings')">
              <Settings :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Settings</span>
            <div v-if="isSidebarOpen && isActive('/Settings')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>

          <router-link to="/Help" :class="navClass('/Help')">
            <div :class="iconWrap('/Help')">
              <HelpCircle :size="16" />
            </div>
            <span v-if="isSidebarOpen" class="nav-label">Help</span>
            <div v-if="isSidebarOpen && isActive('/Help')" class="ml-auto w-1.5 h-1.5 rounded-full bg-fuchsia-400"></div>
          </router-link>
        </nav>

        <!-- ── Sidebar Footer ────────────────────────────────────── -->
        <div class="relative z-10 flex-shrink-0 p-3 border-t" style="border-color: rgba(124,58,237,0.2);">
          <!-- Decorative flower in footer -->
          <div v-if="isSidebarOpen" class="flex items-center gap-3 px-2 py-2">
            <div class="flex-shrink-0">
              <svg width="28" height="28" viewBox="0 0 100 100">
                <g transform="translate(50,50)">
                  <ellipse rx="8" ry="22" fill="#7c3aed" opacity="0.5" transform="rotate(0)"/>
                  <ellipse rx="8" ry="22" fill="#a855f7" opacity="0.5" transform="rotate(60)"/>
                  <ellipse rx="8" ry="22" fill="#7c3aed" opacity="0.5" transform="rotate(120)"/>
                  <circle r="8" fill="#fbbf24" opacity="0.7"/>
                </g>
              </svg>
            </div>
            <div class="min-w-0">
              <p class="text-xs font-semibold text-purple-200 truncate" style="font-family:'Cormorant Garamond',serif; font-size:0.85rem; letter-spacing:0.01em;">{{ user.name }}</p>
              <p class="text-xs truncate" style="color:rgba(167,139,250,0.6); font-size:0.7rem;">{{ user.email }}</p>
            </div>
          </div>
          <div v-else class="flex justify-center py-1">
            <div class="w-6 h-6 rounded-full" style="background:linear-gradient(135deg,#7c3aed,#c084fc);">
              <svg width="24" height="24" viewBox="0 0 48 48">
                <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white" opacity="0.9"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Bottom accent line -->
        <div class="h-px w-full flex-shrink-0" style="background: linear-gradient(90deg, transparent, #7c3aed, transparent);"></div>
      </div>

      <!-- Mobile overlay -->
      <div v-if="isMobile && isSidebarOpen"
           class="fixed inset-0 z-20"
           style="background: rgba(10,5,25,0.6); backdrop-filter: blur(4px);"
           @click="toggleSidebar" />

      <!-- ── Main content ───────────────────────────────────────── -->
      <div class="flex-1 overflow-auto" style="background: #f8f4ff;">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Menu, Home, HelpCircle, Plus, Sprout, FilePlus, Heart,
  Shield, Zap, Settings, ChevronsUpDown, LogOut, Bell, User
} from 'lucide-vue-next'

const route  = useRoute()
const router = useRouter()

const isSidebarOpen    = ref(true)
const isMobile         = ref(window.innerWidth < 768)
const isProfileMenuOpen = ref(false)
const sidebarRef       = ref(null)
const profileMenuRef   = ref(null)

const user = ref({
  name: 'John Doe',
  username: 'johndoe',
  email: 'john@example.com'
})

const toggleSidebar     = () => { isSidebarOpen.value = !isSidebarOpen.value }
const toggleProfileMenu = () => { isProfileMenuOpen.value = !isProfileMenuOpen.value }
const closeProfileMenu  = () => { isProfileMenuOpen.value = false }

const handleLogout = () => {
  console.log('Logging out…')
  localStorage.removeItem('token')
  closeProfileMenu()
  router.push('/')
}

const isActive = (path) => route.path === path || route.path.startsWith(path + '/')

// Nav item class builder
const navClass = (path) => {
  const active = isActive(path)
  return [
    'nav-item group flex items-center gap-3 w-full rounded-xl transition-all duration-200 px-3 py-2.5 mb-0.5 relative',
    active
      ? 'nav-item--active text-white'
      : 'text-purple-300 hover:text-white'
  ]
}

// Icon wrapper
const iconWrap = (path) => {
  const active = isActive(path)
  return [
    'flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center transition-all duration-200',
    active
      ? 'icon-active'
      : 'icon-inactive group-hover:icon-hover'
  ]
}

const handleResize = () => { isMobile.value = window.innerWidth < 768 }
const handleClickOutside = (e) => {
  if (isMobile.value && isSidebarOpen.value && sidebarRef.value && !sidebarRef.value.contains(e.target)) {
    isSidebarOpen.value = false
  }
  if (isProfileMenuOpen.value && profileMenuRef.value && !profileMenuRef.value.contains(e.target)) {
    closeProfileMenu()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  document.addEventListener('mousedown', handleClickOutside)
  if (window.innerWidth < 768) isSidebarOpen.value = false
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
/* ── Sidebar shell ────────────────────────────────────────────── */
.sidebar-shell {
  box-shadow: 4px 0 32px rgba(0,0,0,0.35), 1px 0 0 rgba(124,58,237,0.15);
}

/* ── Nav items ────────────────────────────────────────────────── */
.nav-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8125rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(124,58,237,0.15);
}

.nav-item--active {
  background: linear-gradient(135deg, rgba(124,58,237,0.35) 0%, rgba(168,85,247,0.2) 100%) !important;
  box-shadow: inset 1px 0 0 rgba(192,132,252,0.5), 0 2px 12px rgba(124,58,237,0.2);
}

.nav-item--active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 25%;
  height: 50%;
  width: 2px;
  border-radius: 0 2px 2px 0;
  background: linear-gradient(to bottom, #c084fc, #a855f7);
}

/* ── Icon wrappers ───────────────────────────────────────────── */
.icon-active {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  box-shadow: 0 2px 12px rgba(124,58,237,0.4);
  color: white;
}

.icon-inactive {
  background: rgba(124,58,237,0.08);
  color: rgba(167,139,250,0.7);
}

.nav-item:hover .icon-inactive {
  background: rgba(124,58,237,0.2);
  color: rgba(216,180,254,0.9);
}

/* ── Navbar ──────────────────────────────────────────────────── */
.navbar-bar {
  box-shadow: 0 1px 0 rgba(124,58,237,0.08), 0 2px 12px rgba(0,0,0,0.04);
}

/* ── Dropdown transition ──────────────────────────────────────── */
.dropdown-enter-active, .dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1);
}
.dropdown-enter-from, .dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* ── Scrollbar ───────────────────────────────────────────────── */
nav::-webkit-scrollbar {
  width: 3px;
}
nav::-webkit-scrollbar-track {
  background: transparent;
}
nav::-webkit-scrollbar-thumb {
  background: rgba(124,58,237,0.3);
  border-radius: 2px;
}
</style>