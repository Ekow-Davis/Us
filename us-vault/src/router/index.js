import { createRouter, createWebHistory } from 'vue-router'

// Import pages
// Home Section Pages
import HomeView from '../pages/Home/HomeView.vue'
import ContactPage from '../pages/Home/ContactPage.vue'
import AboutPage from '../pages/Home/AboutPage.vue'
import LoginView from '../pages/Home/LoginPage.vue'
import RegistrationTransferView from '../pages/General/RegistrationTransferPage.vue'

// Main System Pages
// Dashboard
import DashboardView from '../pages/General/DashboardPage.vue'

// Seed
import AddSeedPage from '../pages/Seed/AddSeedPage.vue'
import SeedPage from '../pages/Seed/SeedPage.vue'
import MySeedsPage from '../pages/Seed/MySeedsPage.vue'
import SeedDetailPage from '../pages/Seed/SeedDetailPage.vue'

// Memory
import AddMemoryPage from '../pages/Memories/AddMemoryPage.vue'
import MemoryDetailPage from '../pages/Memories/MemoryDetailPage.vue'
import MemoryPage from '../pages/Memories/MemoryPage.vue'

// Vault
import VaultPage from '../pages/Vault/VaultPage.vue'

// Journal
import JournalPage from '../pages/Journal/JournalPage.vue'

// Signal
import SignalPage from '../pages/Signal/SignalPage.vue'

// Settings
import NotificationPage from '../pages/Settings/NotificationPage.vue'
import SettingsPage from '../pages/Settings/SettingsPage.vue'
import HelpPage from '../pages/Help/HelpPage.vue'


const routes = [
  // Routes that don't require authentication
  { path: '/', name: 'home', component: HomeView, },
  { path: '/contact', name: 'contact', component: ContactPage, },
  { path: '/about', name: 'about', component: AboutPage, },

  // Authentication routes
  { path: '/login', name: 'login', component: LoginView, },

  // Protected routes (require authentication)
  { path: '/registration-transfer', name: 'registration-transfer', component: RegistrationTransferView, },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, },

  { path: '/add-seed', name: 'add-seed', component: AddSeedPage, },
  { path: '/seeds', name: 'seeds', component: SeedPage, },
  { path: '/my-seeds', name: 'my-seeds', component: MySeedsPage, },
  { path: '/seeds/edit/:id', name: 'edit-seed', component: SeedDetailPage, props: true },  

  { path: '/vault', name: 'vault', component: VaultPage, },

  { path: '/memories', name: 'memories', component: MemoryPage,},
  { path: '/add-memory', name: 'add-memory', component: AddMemoryPage, },
  { path: '/memories/:id', name: 'memory-detail', component: MemoryDetailPage },

  { path: '/journal', name: 'journal', component: JournalPage, },
  { path: '/signal', name: 'signal', component: SignalPage, },

  { path: '/settings', name: 'settings', component: SettingsPage, },
  { path: '/notifications', name: 'notifications', component: NotificationPage, },
  { path: '/help', name: 'help', component: HelpPage, },

  { path: '/:pathMatch(.*)*',   redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
