<template>
  <div class="min-h-screen bg-linear-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
    <!-- Loading Heart Animation -->
    <div v-if="isLoading" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="text-center">
        <div class="relative w-32 h-32 mx-auto">
          <!-- Heart SVG -->
          <svg viewBox="0 0 100 100" class="w-full h-full">
            <defs>
              <clipPath id="heartClip">
                <path d="M50,90 C50,90 10,60 10,40 C10,25 20,15 30,15 C40,15 45,20 50,30 C55,20 60,15 70,15 C80,15 90,25 90,40 C90,60 50,90 50,90 Z" />
              </clipPath>
            </defs>
            
            <!-- Heart Outline -->
            <path 
              d="M50,90 C50,90 10,60 10,40 C10,25 20,15 30,15 C40,15 45,20 50,30 C55,20 60,15 70,15 C80,15 90,25 90,40 C90,60 50,90 50,90 Z" 
              fill="none" 
              stroke="#E773A4" 
              stroke-width="2"
            />
            
            <!-- Water Fill -->
            <g clip-path="url(#heartClip)">
              <rect 
                x="0" 
                :y="100 - loadingProgress" 
                width="100" 
                :height="loadingProgress" 
                fill="#E773A4"
              />
            </g>
          </svg>
        </div>
        <div class="mt-4 text-2xl font-bold text-white">{{ Math.round(loadingProgress) }}%</div>
      </div>
    </div>

    <div class="w-full max-w-6xl flex flex-col lg:flex-row gap-8 items-center">
      <!-- Image Carousel - Hidden on mobile -->
      <div class="hidden lg:block flex-1 relative h-[600px] overflow-hidden">
        <TransitionGroup name="carousel">
          <div
            v-for="(image, index) in carouselImages"
            :key="index"
            v-show="currentImageIndex === index"
            class="absolute inset-0 flex items-center justify-center"
          >
            <img 
              :src="image" 
              alt="Illustration" 
              class="max-w-full max-h-full object-contain"
            />
          </div>
        </TransitionGroup>
      </div>

      <!-- Modal Section -->
      <div class="flex-1 w-full max-w-md">
        <div class="bg-white rounded-2xl shadow-2xl p-8 relative">
          <!-- Main Choice Modal -->
          <div v-if="currentStep === 'choice'" class="space-y-6">
            <div class="text-center mb-8">
              <h2 class="text-3xl font-bold text-gray-800 mb-2">Welcome!</h2>
              <p class="text-gray-600">Choose how you'd like to get started</p>
            </div>

            <button
              @click="selectCreateOwn"
              class="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-4 px-6 rounded-lg transition-all transform hover:scale-105 shadow-md"
            >
              Create Your Own Vault
            </button>

            <button
              @click="selectJoinVault"
              class="w-full bg-pink-500 hover:bg-pink-600 text-white font-semibold py-4 px-6 rounded-lg transition-all transform hover:scale-105 shadow-md"
            >
              Join Someone's Vault
            </button>
          </div>

          <!-- Create Own Confirmation -->
          <div v-else-if="currentStep === 'createOwn'" class="space-y-6">
            <button 
              @click="goBack" 
              class="text-gray-600 hover:text-gray-800 flex items-center gap-2 mb-4"
            >
              <ChevronLeft :size="20" />
              <span>Back</span>
            </button>

            <div class="text-center mb-8">
              <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Plus :size="40" class="text-purple-600" />
              </div>
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Create Your Own Vault</h2>
              <p class="text-gray-600">You'll be able to invite others to join your vault after creation</p>
            </div>

            <button
              @click="handleCreateOwn"
              class="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-4 px-6 rounded-lg transition-all shadow-md"
            >
              Continue
            </button>
          </div>

          <!-- Join Vault - Code Input -->
          <div v-else-if="currentStep === 'joinVault'" class="space-y-6">
            <button 
              @click="goBack" 
              class="text-gray-600 hover:text-gray-800 flex items-center gap-2 mb-4"
            >
              <ChevronLeft :size="20" />
              <span>Back</span>
            </button>

            <div class="text-center mb-8">
              <div class="w-20 h-20 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users :size="40" class="text-pink-500" />
              </div>
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Join a Vault</h2>
              <p class="text-gray-600">Enter the 8-character code you received</p>
            </div>

            <!-- Code Input Boxes -->
            <div class="flex justify-center gap-2 mb-6">
              <input
                v-for="(digit, index) in 8"
                :key="index"
                :ref="el => codeInputs[index] = el"
                v-model="vaultCode[index]"
                @input="handleCodeInput(index, $event)"
                @keydown="handleKeyDown(index, $event)"
                @paste="handlePaste($event)"
                type="text"
                maxlength="1"
                class="w-12 h-14 text-center text-2xl font-bold border-2 border-gray-300 rounded-lg focus:border-pink-500 focus:outline-none transition-colors uppercase"
              />
            </div>

            <button
              @click="handleJoinVault"
              :disabled="vaultCode.filter(c => c).length < 8"
              :class="[
                'w-full font-semibold py-4 px-6 rounded-lg transition-all shadow-md',
                vaultCode.filter(c => c).length < 8
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-pink-500 hover:bg-pink-600 text-white'
              ]"
            >
              Join Vault
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { ChevronLeft, Plus, Users } from 'lucide-vue-next';

const router = useRouter();

// State
const currentStep = ref('choice'); // 'choice', 'createOwn', 'joinVault'
const vaultCode = ref(Array(8).fill(''));
const codeInputs = ref([]);
const isLoading = ref(false);
const loadingProgress = ref(0);
const currentImageIndex = ref(0);

// Carousel images
const carouselImages = ref([
  '../../../public/images/undraw_effortless-love_zg5q.svg',
  '../../../public/images/undraw_intense-feeling_4i8u.svg',
  '../../../public/images/undraw_love-messages_9oca.svg',
  '../../../public/images/undraw_pure-love_cvaw.svg',
  '../../../public/images/undraw_spread-love_0ekp.svg',
]);

let carouselInterval = null;

// Start carousel
onMounted(() => {
  carouselInterval = setInterval(() => {
    currentImageIndex.value = (currentImageIndex.value + 1) % carouselImages.value.length;
  }, 4000);
});

onUnmounted(() => {
  if (carouselInterval) {
    clearInterval(carouselInterval);
  }
});

// Navigation functions
const selectCreateOwn = () => {
  currentStep.value = 'createOwn';
};

const selectJoinVault = () => {
  currentStep.value = 'joinVault';
  setTimeout(() => {
    if (codeInputs.value[0]) {
      codeInputs.value[0].focus();
    }
  }, 100);
};

const goBack = () => {
  currentStep.value = 'choice';
  vaultCode.value = Array(8).fill('');
};

// Loading simulation
const simulateLoading = () => {
  return new Promise((resolve) => {
    isLoading.value = true;
    loadingProgress.value = 0;
    
    const interval = setInterval(() => {
      loadingProgress.value += 2;
      
      if (loadingProgress.value >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          isLoading.value = false;
          loadingProgress.value = 0;
          resolve();
        }, 300);
      }
    }, 30);
  });
};

// Handle Create Own Vault
const handleCreateOwn = async () => {
  console.log('Creating own vault...');
  
  await simulateLoading();
  
  // API call placeholder
  // const response = await fetch('/api/create-vault', { method: 'POST' });
  
  router.push('./Dashboard');
};

// Handle Join Vault
const handleJoinVault = async () => {
  const code = vaultCode.value.join('').toUpperCase();
  console.log('Joining vault with code:', code);
  
  await simulateLoading();
  
  // API call placeholder
  // const response = await fetch('/api/join-vault', { 
  //   method: 'POST',
  //   body: JSON.stringify({ code })
  // });
  
  router.push('./Dashboard');
};

// Code input handlers
const handleCodeInput = (index, event) => {
  const value = event.target.value.toUpperCase();
  
  if (value && index < 7) {
    codeInputs.value[index + 1]?.focus();
  }
};

const handleKeyDown = (index, event) => {
  if (event.key === 'Backspace' && !vaultCode.value[index] && index > 0) {
    codeInputs.value[index - 1]?.focus();
  }
};

const handlePaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData.getData('text').toUpperCase().slice(0, 8);
  
  for (let i = 0; i < pastedData.length; i++) {
    vaultCode.value[i] = pastedData[i];
  }
  
  const nextEmptyIndex = pastedData.length < 8 ? pastedData.length : 7;
  codeInputs.value[nextEmptyIndex]?.focus();
};
</script>

<style scoped>
/* Carousel transitions */
.carousel-enter-active {
  transition: all 0.8s ease-out;
}

.carousel-leave-active {
  transition: all 0.8s ease-in;
}

.carousel-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

.carousel-leave-to {
  opacity: 0;
  transform: translateX(-100%) scale(0.8);
}

.carousel-enter-to,
.carousel-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}

/* Input field animations */
input:focus {
  animation: pulse 0.3s ease-in-out;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Prevent number input arrows */
input[type="text"]::-webkit-inner-spin-button,
input[type="text"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>