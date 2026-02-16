import { createRouter, createWebHistory } from 'vue-router'

// Import pages
import HomeView from '../pages/Home/HomeView.vue'
import LoginView from '../pages/Home/LoginPage.vue'
import DashboardView from '../pages/General/DashboardPage.vue'

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
