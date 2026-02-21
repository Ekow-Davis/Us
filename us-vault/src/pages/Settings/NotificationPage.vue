<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'
import { Bell, Check, CheckCheck, Trash2, Inbox } from 'lucide-vue-next'

const router = useRouter()

// ── State ──────────────────────────────────────────────────────────────────
const notifications = ref([])
const isLoading = ref(true)
const isProcessing = ref(false)

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)
const totalPages = ref(1)
const totalNotifications = ref(0)

// ── Mock API Calls ─────────────────────────────────────────────────────────
const fetchNotifications = async (page = 1, size = 10) => {
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mock notifications data
  const allNotifications = [
    {
      id: 'notif-001',
      user_id: 'user-001',
      type: 'seed_bloomed',
      title: 'Seed Ready to Bloom',
      message: 'Your seed "The First Time We Laughed Together" is ready to bloom!',
      is_read: false,
      created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
      related_entity_id: 'seed-008',
      related_entity_type: 'seed'
    },
    {
      id: 'notif-002',
      user_id: 'user-001',
      type: 'memory_created',
      title: 'New Memory Created',
      message: 'Your partner added a new memory: "Summer Vacation 2024"',
      is_read: false,
      created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
      related_entity_id: 'mem-010',
      related_entity_type: 'memory'
    },
    {
      id: 'notif-003',
      user_id: 'user-001',
      type: 'seed_planted',
      title: 'Partner Planted a Seed',
      message: 'Your partner planted a new seed that will bloom in 14 days',
      is_read: true,
      created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
      related_entity_id: 'seed-009',
      related_entity_type: 'seed'
    },
    {
      id: 'notif-004',
      user_id: 'user-001',
      type: 'vault_invitation',
      title: 'Vault Invitation',
      message: 'You have been invited to join "Our Forever Vault"',
      is_read: true,
      created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
      related_entity_id: 'vault-002',
      related_entity_type: 'vault'
    },
    {
      id: 'notif-005',
      user_id: 'user-001',
      type: 'seed_bloomed',
      title: 'Seed Bloomed into Memory',
      message: '"What I Noticed First" has bloomed into a beautiful memory',
      is_read: true,
      created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      related_entity_id: 'seed-002',
      related_entity_type: 'seed'
    },
    {
      id: 'notif-006',
      user_id: 'user-001',
      type: 'memory_liked',
      title: 'Memory Liked',
      message: 'Your partner loved your memory "First Date Anniversary"',
      is_read: true,
      created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      related_entity_id: 'mem-005',
      related_entity_type: 'memory'
    }
  ]
  
  const start = (page - 1) * size
  const paginatedNotifs = allNotifications.slice(start, start + size)
  
  return {
    items: paginatedNotifs,
    total: allNotifications.length,
    page,
    page_size: size,
    total_pages: Math.ceil(allNotifications.length / size)
  }
}

const markAsRead = async (notificationId) => {
  await new Promise(resolve => setTimeout(resolve, 200))
  
  // Update local state
  const notif = notifications.value.find(n => n.id === notificationId)
  if (notif) {
    notif.is_read = true
  }
}

const markAllAsRead = async () => {
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Mark all as read in local state
  notifications.value.forEach(n => {
    n.is_read = true
  })
}

const clearNotifications = async () => {
  await new Promise(resolve => setTimeout(resolve, 300))
  
  // Remove all read notifications
  notifications.value = notifications.value.filter(n => !n.is_read)
  totalNotifications.value = notifications.value.length
}

// ── Computed ───────────────────────────────────────────────────────────────
const unreadCount = computed(() => 
  notifications.value.filter(n => !n.is_read).length
)

const hasUnread = computed(() => unreadCount.value > 0)
const hasRead = computed(() => 
  notifications.value.some(n => n.is_read)
)

// ── Methods ────────────────────────────────────────────────────────────────
const handleNotificationClick = async (notification) => {
  // Mark as read if unread
  if (!notification.is_read) {
    await markAsRead(notification.id)
  }
  
  // Navigate to related entity if applicable
  if (notification.related_entity_type === 'seed') {
    router.push('/seeds')
  } else if (notification.related_entity_type === 'memory') {
    router.push('/memories')
  } else if (notification.related_entity_type === 'vault') {
    router.push('/vault')
  }
}

const handleMarkAsRead = async (notification, event) => {
  event.stopPropagation()
  
  if (!notification.is_read) {
    isProcessing.value = true
    try {
      await markAsRead(notification.id)
    } finally {
      isProcessing.value = false
    }
  }
}

const handleMarkAllAsRead = async () => {
  if (!hasUnread.value) return
  
  isProcessing.value = true
  try {
    await markAllAsRead()
  } finally {
    isProcessing.value = false
  }
}

const handleClearNotifications = async () => {
  if (!hasRead.value) return
  
  if (!confirm('This will clear all read notifications. Are you sure?')) {
    return
  }
  
  isProcessing.value = true
  try {
    await clearNotifications()
  } finally {
    isProcessing.value = false
  }
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadNotifications()
  }
}

const loadNotifications = async () => {
  isLoading.value = true
  try {
    const data = await fetchNotifications(currentPage.value, pageSize.value)
    notifications.value = data.items
    totalNotifications.value = data.total
    totalPages.value = data.total_pages
  } catch (error) {
    console.error('Failed to load notifications:', error)
  } finally {
    isLoading.value = false
  }
}

// ── Helpers ────────────────────────────────────────────────────────────────
const formatTimeAgo = (isoDate) => {
  const now = new Date()
  const date = new Date(isoDate)
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays}d ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const getNotificationIcon = (type) => {
  const icons = {
    'seed_bloomed': '🌸',
    'seed_planted': '🌱',
    'memory_created': '💝',
    'memory_liked': '❤️',
    'vault_invitation': '🔐',
    'default': '🔔'
  }
  return icons[type] || icons.default
}

const getNotificationColor = (type) => {
  const colors = {
    'seed_bloomed': 'bg-purple-50 border-purple-200',
    'seed_planted': 'bg-emerald-50 border-emerald-200',
    'memory_created': 'bg-pink-50 border-pink-200',
    'memory_liked': 'bg-rose-50 border-rose-200',
    'vault_invitation': 'bg-indigo-50 border-indigo-200',
    'default': 'bg-slate-50 border-slate-200'
  }
  return colors[type] || colors.default
}

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(() => {
  loadNotifications()
})
</script>

<template>
  <InactivityOverlay>
      <Sidebar>
    <div class="notifications-page min-h-screen relative overflow-x-hidden">
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
      </component>

      <!-- Ambient BG -->
      <div class="pointer-events-none select-none absolute inset-0 overflow-hidden" aria-hidden="true">
        <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full opacity-20" style="background: radial-gradient(circle,#c7d2fe 0%,transparent 70%);"></div>
        <div class="absolute top-1/2 -left-20 w-72 h-72 rounded-full opacity-15" style="background: radial-gradient(circle,#ddd6fe 0%,transparent 70%);"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">

        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center min-h-100">
          <div class="flex flex-col items-center gap-3">
            <div class="flex gap-1">
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.2s"></span>
              <span class="w-2 h-2 rounded-full bg-indigo-400 loading-dot" style="animation-delay:0.4s"></span>
            </div>
            <p class="notif-body text-sm text-indigo-400 tracking-wide">Loading notifications…</p>
          </div>
        </div>

        <template v-else>
          <!-- Header -->
          <div class="mb-8">
            <div class="flex items-start justify-between gap-4 flex-wrap mb-4">
              <div>
                <p class="notif-sub text-xs text-indigo-500 uppercase tracking-widest mb-1">Your Updates</p>
                <h1 class="notif-display text-3xl md:text-4xl text-slate-900">Notifications</h1>
                <p class="notif-body text-sm text-slate-500 mt-2">
                  {{ totalNotifications }} total · {{ unreadCount }} unread
                </p>
              </div>

              <!-- Actions -->
              <div class="flex items-center gap-2">
                <button 
                  @click="handleMarkAllAsRead"
                  :disabled="!hasUnread || isProcessing"
                  class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-50 text-indigo-600 hover:bg-indigo-100 notif-body text-sm font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed">
                  <CheckCheck :size="16" />
                  <span class="hidden sm:inline">Mark all read</span>
                </button>
                <button 
                  @click="handleClearNotifications"
                  :disabled="!hasRead || isProcessing"
                  class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-50 text-rose-600 hover:bg-rose-100 notif-body text-sm font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed">
                  <Trash2 :size="16" />
                  <span class="hidden sm:inline">Clear read</span>
                </button>
              </div>
            </div>

            <!-- Divider -->
            <div class="flex items-center gap-3">
              <div class="h-px flex-1" style="background: linear-gradient(90deg,#6366f1,#818cf8,transparent);"></div>
              <Bell :size="16" class="text-indigo-400" />
              <div class="h-px w-8" style="background:#818cf8;"></div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="notifications.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
            <div class="w-20 h-20 rounded-full bg-indigo-50 flex items-center justify-center mb-4">
              <Inbox :size="32" class="text-indigo-300" />
            </div>
            <h3 class="notif-display text-xl text-slate-700 mb-2">All caught up!</h3>
            <p class="notif-body text-sm text-slate-500 text-center max-w-sm">
              You have no notifications right now. We'll let you know when something important happens.
            </p>
          </div>

          <!-- Notifications List -->
          <div v-else class="space-y-3">
            <div 
              v-for="(notification, idx) in notifications" 
              :key="notification.id"
              @click="handleNotificationClick(notification)"
              :class="[
                'notif-card group relative bg-white rounded-xl p-4 md:p-5 border transition-all duration-200 cursor-pointer',
                notification.is_read 
                  ? 'border-slate-200 hover:border-indigo-200' 
                  : 'border-indigo-200 hover:border-indigo-300 bg-linear-to-br from-white to-indigo-50/30',
                getNotificationColor(notification.type)
              ]"
              :style="`animation-delay:${idx*50}ms`">
              
              <!-- Unread indicator -->
              <div v-if="!notification.is_read" 
                   class="absolute top-4 left-4 w-2 h-2 rounded-full bg-indigo-500 animate-pulse-soft"></div>

              <div :class="['flex items-start gap-4', notification.is_read ? 'pl-0' : 'pl-4']">
                <!-- Icon -->
                <div class="shrink-0 w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-xl">
                  {{ getNotificationIcon(notification.type) }}
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-3 mb-1">
                    <h3 class="notif-display text-base text-slate-900 font-semibold">
                      {{ notification.title }}
                    </h3>
                    <span class="notif-body text-xs text-slate-400 whitespace-nowrap">
                      {{ formatTimeAgo(notification.created_at) }}
                    </span>
                  </div>
                  <p class="notif-body text-sm text-slate-600 leading-relaxed">
                    {{ notification.message }}
                  </p>
                </div>

                <!-- Mark as read button -->
                <button 
                  v-if="!notification.is_read"
                  @click="handleMarkAsRead(notification, $event)"
                  class="shrink-0 w-8 h-8 rounded-lg bg-indigo-50 hover:bg-indigo-100 flex items-center justify-center text-indigo-600 transition opacity-0 group-hover:opacity-100"
                  title="Mark as read">
                  <Check :size="16" />
                </button>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8 pt-6 border-t border-slate-200">
            <button 
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed notif-body text-sm font-semibold transition">
              Previous
            </button>
            <span class="notif-body text-sm text-slate-500 px-3">
              Page {{ currentPage }} of {{ totalPages }}
            </span>
            <button 
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed notif-body text-sm font-semibold transition">
              Next
            </button>
          </div>
        </template>

      </div>
    </div>
  </Sidebar>
  </InactivityOverlay>

</template>

<style scoped>
.notifications-page {
  background: linear-gradient(160deg, #f1f5f9 0%, #ffffff 50%, #f8fafc 100%);
}
.notif-display { font-family: 'Crimson Pro', Georgia, serif; font-weight: 500; }
.notif-body    { font-family: 'Inter', sans-serif; }
.notif-sub     { font-family: 'Inter', sans-serif; }

.notif-card {
  box-shadow: 0 2px 8px rgba(99,102,241,0.04);
  animation: cardReveal 0.4s cubic-bezier(0.22,1,0.36,1) both;
}
.notif-card:hover {
  box-shadow: 0 4px 16px rgba(99,102,241,0.08);
  transform: translateY(-2px);
}

@keyframes cardReveal {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.loading-dot { 
  animation: dotPulse 1.2s ease-in-out infinite; 
}
@keyframes dotPulse { 
  0%,100% { opacity: 0.3; transform: scale(0.8); } 
  50% { opacity: 1; transform: scale(1.2); } 
}

@keyframes pulseSoft {
  0%,100% { opacity: 1; }
  50%     { opacity: 0.5; }
}
.animate-pulse-soft { animation: pulseSoft 2s ease-in-out infinite; }
</style>