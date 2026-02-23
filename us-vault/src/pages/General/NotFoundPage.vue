<script setup>
import { useRouter } from 'vue-router'
import { Home, ArrowLeft, Search } from 'lucide-vue-next'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="not-found-page min-h-screen flex items-center justify-center p-4 relative overflow-hidden"
       style="background: linear-gradient(135deg, #1a0d2e 0%, #0f0620 60%, #130826 100%);">
    
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Ambient glow effects -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full opacity-20 blur-3xl" 
           style="background: radial-gradient(circle, #7c3aed, transparent);"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full opacity-15 blur-3xl" 
           style="background: radial-gradient(circle, #ec4899, transparent);"></div>
    </div>

    <!-- Left Bleeding Heart Vine - PLACEHOLDER -->
    <div class="absolute left-0 top-0 bottom-0 w-32 md:w-48 pointer-events-none opacity-30">
      <!-- 
        PLACEHOLDER: Replace this section with your bleeding heart flower vine PNG
        Recommended image: Vertical vine with bleeding heart flowers
      -->  
        <img 
          src="../../../../images/bleeeding-heart-right.png" 
          alt="Bleeding heart vine decoration"
          class="h-full w-full object-cover object-right"
        />
      
      <!-- Temporary fallback SVG vine -->
      <!-- <svg class="h-full w-full" viewBox="0 0 100 800" preserveAspectRatio="none" fill="none">
        <path d="M60 0 Q30 100 60 200 Q90 300 60 400 Q30 500 60 600 Q90 700 60 800" 
              stroke="#c084fc" 
              stroke-width="3" 
              opacity="0.3"/>
        
        <g opacity="0.4">
          <path d="M45 120 Q35 110 30 120 Q25 130 30 140 L45 155 L60 140 Q65 130 60 120 Q55 110 45 120" fill="#ec4899"/>
          <path d="M70 320 Q60 310 55 320 Q50 330 55 340 L70 355 L85 340 Q90 330 85 320 Q80 310 70 320" fill="#ec4899"/>
          <path d="M45 520 Q35 510 30 520 Q25 530 30 540 L45 555 L60 540 Q65 530 60 520 Q55 510 45 520" fill="#ec4899"/>
          <path d="M70 720 Q60 710 55 720 Q50 730 55 740 L70 755 L85 740 Q90 730 85 720 Q80 710 70 720" fill="#ec4899"/>
        </g>
      </svg> -->
    </div>

    <!-- Right Bleeding Heart Vine - PLACEHOLDER -->
    <div class="absolute right-0 top-0 bottom-0 w-32 md:w-48 pointer-events-none opacity-30">
      <!-- 
        PLACEHOLDER: Replace this section with your bleeding heart flower vine PNG
        Recommended image: Vertical vine with bleeding heart flowers (mirrored)
      -->  
        <img 
          src="../../../../images/bleeeding-heart-right.png" 
          alt="Bleeding heart vine decoration"
          class="h-full w-full object-cover object-left"
        />
      
      <!-- Temporary fallback SVG vine -->
      <!-- <svg class="h-full w-full" viewBox="0 0 100 800" preserveAspectRatio="none" fill="none">
        <path d="M40 0 Q70 100 40 200 Q10 300 40 400 Q70 500 40 600 Q10 700 40 800" 
              stroke="#c084fc" 
              stroke-width="3" 
              opacity="0.3"/>
  
        <g opacity="0.4">
          <path d="M55 120 Q65 110 70 120 Q75 130 70 140 L55 155 L40 140 Q35 130 40 120 Q45 110 55 120" fill="#ec4899"/>
          <path d="M30 320 Q40 310 45 320 Q50 330 45 340 L30 355 L15 340 Q10 330 15 320 Q20 310 30 320" fill="#ec4899"/>
          <path d="M55 520 Q65 510 70 520 Q75 530 70 540 L55 555 L40 540 Q35 530 40 520 Q45 510 55 520" fill="#ec4899"/>
          <path d="M30 720 Q40 710 45 720 Q50 730 45 740 L30 755 L15 740 Q10 730 15 720 Q20 710 30 720" fill="#ec4899"/>
        </g>
      </svg> -->
    </div>

    <!-- Main Content -->
    <div class="relative z-10 text-center max-w-2xl mx-auto">
      
      <!-- 404 Number -->
      <div class="mb-8">
        <h1 class="text-9xl md:text-[12rem] font-bold mb-2 tracking-tight"
            style="font-family: 'Crimson Pro', Georgia, serif; 
                   background: linear-gradient(135deg, #c084fc, #ec4899, #a855f7);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   text-shadow: 0 0 80px rgba(192,132,252,0.3);">
          404
        </h1>
      </div>

      <!-- Top Bleeding Heart Accent - PLACEHOLDER -->
      <div class="flex justify-center mb-6">
        <!-- 
          PLACEHOLDER: Replace with a small bleeding heart flower PNG
          Recommended: Single bleeding heart flower or small cluster
        -->  
          <img 
            src="../../../../images/bleeeding-heart-right.png" 
            alt="Bleeding heart flower"
            class="w-16 h-16 md:w-20 md:h-20 opacity-70"
          />
        
        <!-- Temporary fallback -->
        <svg width="64" height="64" viewBox="0 0 100 100" class="opacity-70">
          <path d="M30 30 Q20 20 15 30 Q10 40 15 50 L30 65 L45 50 Q50 40 45 30 Q40 20 30 30" 
                fill="#ec4899" 
                opacity="0.8"/>
          <path d="M70 30 Q60 20 55 30 Q50 40 55 50 L70 65 L85 50 Q90 40 85 30 Q80 20 70 30" 
                fill="#ec4899" 
                opacity="0.8"/>
          <path d="M50 50 L50 85" stroke="#a855f7" stroke-width="3" stroke-linecap="round"/>
          <circle cx="50" cy="50" r="8" fill="#fbbf24"/>
        </svg>
      </div>

      <!-- Message -->
      <h2 class="text-3xl md:text-4xl font-semibold mb-4 text-purple-100"
          style="font-family: 'Crimson Pro', Georgia, serif;">
        Page Not Found
      </h2>
      
      <p class="text-lg md:text-xl text-purple-200 mb-8 max-w-lg mx-auto leading-relaxed"
         style="font-family: 'Inter', sans-serif;">
        The page you're looking for seems to have wandered off into the garden. 
        It might be resting among the flowers.
      </p>

      <!-- Search suggestion (optional) -->
      <div class="mb-10 max-w-md mx-auto">
        <div class="flex items-center gap-3 px-5 py-3.5 rounded-xl bg-white/5 backdrop-blur-sm border border-purple-400/20">
          <Search :size="20" class="text-purple-300 shrink-0" />
          <p class="text-sm text-purple-200 text-left" style="font-family: 'Inter', sans-serif;">
            Lost? Try checking the URL or return home to find your way.
          </p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <button @click="goBack"
                class="group flex items-center gap-2.5 px-6 py-3.5 rounded-xl border-2 border-purple-400/30 text-purple-200 hover:bg-purple-500/10 hover:border-purple-400/50 transition-all duration-200"
                style="font-family: 'Inter', sans-serif; font-size: 0.9375rem; font-weight: 600;">
          <ArrowLeft :size="18" class="group-hover:-translate-x-1 transition-transform" />
          Go Back
        </button>
        
        <button @click="goHome"
                class="group flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 transition-all duration-200 shadow-lg shadow-purple-500/25"
                style="font-family: 'Inter', sans-serif; font-size: 0.9375rem; font-weight: 600;">
          <Home :size="18" />
          Return Home
        </button>
      </div>

      <!-- Bottom Bleeding Heart Accent - PLACEHOLDER -->
      <div class="flex justify-center mt-12">
        <!-- 
          PLACEHOLDER: Replace with a small bleeding heart flower PNG or vine segment
          Recommended: Horizontal vine segment with 2-3 flowers
        -->  
          <img 
            src="../../../../images/bleeeding-heart-right.png" 
            alt="Bleeding heart flowers"
            class="w-32 h-16 md:w-40 md:h-20 opacity-60"
          />
        
        <!-- Temporary fallback -->
        <!-- <svg width="120" height="60" viewBox="0 0 200 80" class="opacity-60">
          <path d="M10 40 Q50 30 100 40 Q150 50 190 40" 
                stroke="#a855f7" 
                stroke-width="2.5" 
                fill="none" 
                opacity="0.6"/>
          
          <g opacity="0.7">
            <path d="M55 25 Q50 20 47 25 Q44 30 47 35 L55 42 L63 35 Q66 30 63 25 Q60 20 55 25" fill="#ec4899"/>
            <path d="M100 35 Q95 30 92 35 Q89 40 92 45 L100 52 L108 45 Q111 40 108 35 Q105 30 100 35" fill="#ec4899"/>
            <path d="M145 25 Q140 20 137 25 Q134 30 137 35 L145 42 L153 35 Q156 30 153 25 Q150 20 145 25" fill="#ec4899"/>
          </g>
        </svg> -->
      </div>

      <!-- Helpful Links (Optional) -->
      <div class="mt-12 pt-8 border-t border-purple-400/20">
        <p class="text-sm text-purple-300 mb-4" style="font-family: 'Inter', sans-serif;">
          Quick Links
        </p>
        <div class="flex flex-wrap justify-center gap-4 text-sm" style="font-family: 'Inter', sans-serif;">
          <button @click="router.push('/dashboard')" 
                  class="text-purple-300 hover:text-purple-100 transition">
            Dashboard
          </button>
          <span class="text-purple-500">•</span>
          <button @click="router.push('/seeds')" 
                  class="text-purple-300 hover:text-purple-100 transition">
            Seeds
          </button>
          <span class="text-purple-500">•</span>
          <button @click="router.push('/memories')" 
                  class="text-purple-300 hover:text-purple-100 transition">
            Memories
          </button>
          <span class="text-purple-500">•</span>
          <button @click="router.push('/help')" 
                  class="text-purple-300 hover:text-purple-100 transition">
            Help
          </button>
        </div>
      </div>

    </div>

    <!-- Floating particles -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="particle particle-1"></div>
      <div class="particle particle-2"></div>
      <div class="particle particle-3"></div>
      <div class="particle particle-4"></div>
      <div class="particle particle-5"></div>
    </div>

  </div>
</template>

<style scoped>
/* Particles animation */
.particle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(236,72,153,0.3), transparent);
  animation: float 25s infinite ease-in-out;
  opacity: 0.6;
}

.particle-1 { 
  width: 8px; 
  height: 8px; 
  top: 15%; 
  left: 20%; 
  animation-delay: 0s;
  animation-duration: 20s;
}

.particle-2 { 
  width: 6px; 
  height: 6px; 
  top: 45%; 
  left: 75%; 
  animation-delay: 5s;
  animation-duration: 25s;
}

.particle-3 { 
  width: 10px; 
  height: 10px; 
  top: 70%; 
  left: 15%; 
  animation-delay: 10s;
  animation-duration: 22s;
}

.particle-4 { 
  width: 7px; 
  height: 7px; 
  top: 25%; 
  left: 85%; 
  animation-delay: 15s;
  animation-duration: 28s;
}

.particle-5 { 
  width: 9px; 
  height: 9px; 
  top: 85%; 
  left: 60%; 
  animation-delay: 20s;
  animation-duration: 24s;
}

@keyframes float {
  0%, 100% { 
    transform: translate(0, 0) scale(1); 
    opacity: 0.6;
  }
  25% { 
    transform: translate(30px, -40px) scale(1.1); 
    opacity: 0.8;
  }
  50% { 
    transform: translate(-20px, -80px) scale(0.9); 
    opacity: 0.5;
  }
  75% { 
    transform: translate(40px, -50px) scale(1.05); 
    opacity: 0.7;
  }
}
</style>