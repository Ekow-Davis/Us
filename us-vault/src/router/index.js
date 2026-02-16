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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
