<template>
  <div class="flex flex-col h-screen">
    <!-- NavBar -->
    <div class="w-full bg-white text-purple-700 p-3 flex items-center z-20 relative">
      <Menu 
        :size="24" 
        class="cursor-pointer hover:text-pink-500 transition-colors" 
        @click="toggleSidebar" 
      />
      <span class="ml-4 text-lg font-bold">Us Vault</span>
      <div class="grow"></div>
      <div class="flex items-center space-x-2">
        <div class="text-sm">{{ user.name }}</div>
      </div>

      <!-- Profile Menu Dropdown -->
      <div 
        v-if="isProfileMenuOpen"
        ref="profileMenuRef"
        class="absolute top-full right-4 mt-2 w-48 bg-white rounded overflow-hidden z-50 border border-gray-200"
      >
        <div class="text-purple-700">
          <router-link to="/Account" class="flex items-center p-3 hover:bg-gray-100 transition-colors" @click="closeProfileMenu">
            <User :size="16" class="mr-2" />
            <span>Account</span>
          </router-link>
          <router-link to="/Notifications" class="flex items-center p-3 hover:bg-gray-100 transition-colors" @click="closeProfileMenu">
            <Bell :size="16" class="mr-2" />
            <span>Notifications</span>
          </router-link>
          <div class="border-t border-gray-200"></div>
          <div @click="handleLogout" class="flex items-center p-3 hover:bg-gray-100 cursor-pointer transition-colors">
            <LogOut :size="16" class="mr-2" />
            <span>Log out</span>
          </div>
        </div>
      </div>
      
      <!-- Profile Button -->
      <div 
        class="flex items-center cursor-pointer hover:bg-purple-700 group rounded text-white p-2 ml-4 transition-colors"
        @click="toggleProfileMenu"
      >
        <div class="flex items-center space-x-2 grow">
          <div class="w-8 h-8 rounded-full bg-pink-500 flex items-center justify-center overflow-hidden">
            <User :size="16" class="text-white" />
          </div>
          <div v-if="isSidebarOpen" class="grow">
            <div class="text-sm font-medium text-purple-700 group-hover:text-white">
              {{ user.username }}
            </div>
            <div class="text-xs text-gray-400 group-hover:text-gray-200">
              {{ user.email }}
            </div>
          </div>
        </div>
        <ChevronsUpDown v-if="isSidebarOpen" :size="16" class="text-purple-700 group-hover:text-white" />
      </div>
    </div>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <div
        ref="sidebarRef"
        :class="[
          'sidebar p-2 fixed md:relative top-0 md:top-auto left-0 min-h-full md:h-[calc(100vh-64px)] bg-white transition-all z-30 overflow-y-auto flex-col',
          isMobile 
            ? (isSidebarOpen ? 'w-64 translate-x-0' : '-translate-x-full') 
            : isSidebarOpen ? 'w-60' : 'w-14'
        ]"
      >
        <div class="grow overflow-y-auto">
          <!-- Dashboard -->
          <router-link
            to="/Dashboard"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/Dashboard') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Home :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Dashboard</span>
          </router-link>

          <!-- Add Seed -->
          <router-link
            to="/add-seed"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/add-seed') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Plus :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Add Seed</span>
          </router-link>

          <!-- Seeds -->
          <router-link
            to="/Seeds"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/Seeds') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Sprout :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Seeds</span>
          </router-link>

          <!-- Add Memory -->
          <router-link
            to="/add-memory"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/add-memory') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <FilePlus :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Add Memory</span>
          </router-link>

          <!-- Memories -->
          <router-link
            to="/memories"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/memories') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Heart :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Memories</span>
          </router-link>

          <!-- Vault Details -->
          <router-link
            to="/vault"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/vault') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Shield :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Vault Details</span>
          </router-link>

          <!-- Signal -->
          <router-link
            to="/Signal"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/Signal') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Zap :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Signal</span>
          </router-link>

          <!-- Settings -->
          <router-link
            to="/Settings"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/Settings') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <Settings :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Settings</span>
          </router-link>

          <!-- Help -->
          <router-link
            to="/Help"
            :class="[
              'flex items-center p-2 my-1 rounded cursor-pointer transition-all',
              isActive('/Help') 
                ? 'bg-purple-700 text-white' 
                : 'text-purple-700 hover:bg-purple-700 hover:text-white'
            ]"
          >
            <HelpCircle :size="20" class="mr-2" />
            <span v-if="isSidebarOpen">Help</span>
          </router-link>
        </div>
      </div>

      <!-- Mobile overlay -->
      <div
        v-if="isMobile && isSidebarOpen"
        class="fixed inset-0 bg-black/50 z-20"
        @click="toggleSidebar"
      />

      <!-- Main content -->
      <div class="flex-1 overflow-auto bg-gray-100 rounded-3xl">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  Menu, Home, HelpCircle, Plus, Sprout, FilePlus, Heart,
  Shield, Zap, Settings, ChevronsUpDown, LogOut, Bell,
  CreditCard, User
} from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();

// State
const isSidebarOpen = ref(true);
const isMobile = ref(window.innerWidth < 768);
const isProfileMenuOpen = ref(false);
const sidebarRef = ref(null);
const profileMenuRef = ref(null);

// Sample user data - replace with actual user data from store/context
const user = ref({
  name: 'John Doe',
  username: 'johndoe',
  email: 'john@example.com'
});

// Methods
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const toggleProfileMenu = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value;
};

const closeProfileMenu = () => {
  isProfileMenuOpen.value = false;
};

const handleLogout = () => {
  // Add your logout logic here
  console.log('Logging out...');
  
  // Clear any stored auth tokens
  localStorage.removeItem('token');
  
  closeProfileMenu();
  router.push('/');
};

const isActive = (path) => {
  return route.path === path;
};

const handleResize = () => {
  isMobile.value = window.innerWidth < 768;
};

const handleClickOutside = (e) => {
  // Close sidebar on mobile when clicking outside
  if (isMobile.value && isSidebarOpen.value && sidebarRef.value && !sidebarRef.value.contains(e.target)) {
    isSidebarOpen.value = false;
  }
  
  // Close profile menu when clicking outside
  if (isProfileMenuOpen.value && profileMenuRef.value && !profileMenuRef.value.contains(e.target)) {
    closeProfileMenu();
  }
};

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', handleResize);
  document.addEventListener('mousedown', handleClickOutside);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  document.removeEventListener('mousedown', handleClickOutside);
});
</script>

<style scoped>
/* Additional custom styles if needed */

/* Smooth transitions */
.sidebar {
  transition: width 0.3s ease, transform 0.3s ease;
}

/* Custom scrollbar */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #6d28d9;
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #5b21b6;
}
</style>