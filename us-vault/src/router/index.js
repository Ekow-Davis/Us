import { createRouter, createWebHistory } from 'vue-router'

// Import pages
// Home Section Pages
import HomeView from '../pages/Home/HomeView.vue'
import LoginView from '../pages/Home/LoginPage.vue'
import RegistrationTransferView from '../pages/General/RegistrationTransferPage.vue'

// Main System Pages
// Dashboard
import DashboardView from '../pages/General/DashboardPage.vue'

// Seed
import AddSeedPage from '../pages/Seed/AddSeedPage.vue'
import SeedPage from '../pages/Seed/SeedPage.vue'

// Memory
import AddMemoryPage from '../pages/Memories/AddMemoryPage.vue'
import MemoryDetailPage from '../pages/Memories/MemoryDetailPage.vue'
import MemoryPage from '../pages/Memories/MemoryPage.vue'

// Vault
import VaultPage from '../pages/Vault/VaultPage.vue'

// Signal
import SignalPage from '../pages/Signal/SignalPage.vue'

// Settings
import SettingsPage from '../pages/Settings/SettingsPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
  },
  {
    path: '/registration-transfer',
    name: 'registration-transfer',
    component: RegistrationTransferView,
  },

  {
    path: '/add-seed',
    name: 'add-seed',
    component: AddSeedPage,
  },
  {
    path: '/seeds',
    name: 'seeds',
    component: SeedPage,
  },
  {
    path: '/vault',
    name: 'vault',
    component: VaultPage,
  },
  {
    path: '/memories',
    name: 'memories',
    component: MemoryPage,
  },
  {
    path: '/add-memory',
    name: 'add-memory',
    component: AddMemoryPage,
  },
  { path: '/memories/:id', name: 'memorydetail', component: MemoryDetailPage },
  {
    path: '/signal',
    name: 'signal',
    component: SignalPage,
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsPage,
  },
  { path: '/:pathMatch(.*)*',     redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
