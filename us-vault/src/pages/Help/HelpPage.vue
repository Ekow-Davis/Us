<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue' // Assuming same path as your example
import { BookOpen, Image as ImageIcon, Heart, Share2, Shield, Settings } from 'lucide-vue-next'

// ── Data: Help Sections ──────────────────────────────────────────────────────
// This drives the content. The 'image' part currently uses a placeholder div,
// but you can replace the placeholder logic with actual <img> tags later.
const helpSections = [
  {
    id: 1,
    title: "The Memory Vault",
    description: "Your central hub for all shared moments. Here you can see a timeline of your relationship, track stats, and see the 'Locket' status. This page pulses when new memories are added.",
    icon: Shield,
    color: "text-purple-600",
    bgColor: "bg-purple-100",
    petalColor: "#c084fc"
  },
  {
    id: 2,
    title: "Planting Seeds",
    description: "Seeds are conversation starters. Drop a seed here to prompt your partner with a question or a thought. When they answer, the seed grows into a permanent memory.",
    icon: Heart,
    color: "text-pink-600",
    bgColor: "bg-pink-100",
    petalColor: "#f472b6"
  },
  {
    id: 3,
    title: "Gallery & Media",
    description: "A dedicated space for all your photos and videos. You can organize them by date or mood. Hover over images to see the context or the message attached to them.",
    icon: ImageIcon,
    color: "text-blue-600",
    bgColor: "bg-blue-100",
    petalColor: "#60a5fa"
  },
  {
    id: 4,
    title: "Sharing Signals",
    description: "Send subtle non-verbal signals. A 'thinking of you' pulse or a 'miss you' vibration. These appear instantly on your partner's dashboard without needing a full message.",
    icon: Share2,
    color: "text-amber-600",
    bgColor: "bg-amber-100",
    petalColor: "#fbbf24"
  }
]

// ── Scroll Observer Logic ────────────────────────────────────────────────────
// This handles the "Bloom" effect when elements come into view
const sectionRefs = ref([])

const setRef = (el) => {
  if (el && !sectionRefs.value.includes(el)) {
    sectionRefs.value.push(el)
  }
}

let observer = null

onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible')
      }
    })
  }, {
    threshold: 0.2, // Trigger when 20% of the item is visible
    rootMargin: "0px 0px -50px 0px"
  })

  sectionRefs.value.forEach(ref => observer.observe(ref))
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<template>
  <Sidebar>
    <div class="help-page min-h-screen relative overflow-x-hidden">
      
      <!-- ── Global Styles/Fonts ────────────────────────────────────────── -->
      <component :is="'style'">
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');
      </component>

      <!-- ── Background Atmosphere (Matching Vault.vue) ─────────────────── -->
      <div class="fixed inset-0 pointer-events-none select-none" aria-hidden="true">
        <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full opacity-20"
             style="background: radial-gradient(circle, #ddd6fe 0%, transparent 70%);"></div>
        <div class="absolute top-1/3 -right-32 w-80 h-80 rounded-full opacity-15"
             style="background: radial-gradient(circle, #fbcfe8 0%, transparent 70%);"></div>
        <div class="absolute -bottom-16 left-1/3 w-64 h-64 rounded-full opacity-10"
             style="background: radial-gradient(circle, #c4b5fd 0%, transparent 70%);"></div>
      </div>

      <!-- ── Hero Section: Falling Petals ───────────────────────────────── -->
      <div class="relative min-h-[60vh] flex flex-col items-center justify-center text-center px-4 overflow-hidden">
        
        <!-- Falling Petals Animation Layer -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <svg v-for="n in 12" :key="n" 
               class="falling-petal absolute opacity-60" 
               :class="`petal-anim-${n}`"
               viewBox="0 0 40 40" width="30">
             <path d="M20 40C20 40 0 20 0 10C0 4.5 4.5 0 10 0C15 0 20 5 20 10C20 5 25 0 30 0C35.5 0 40 4.5 40 10C40 20 20 40 20 40Z" 
                   fill="url(#petalGradient)" />
          </svg>
          <defs>
            <linearGradient id="petalGradient" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stop-color="#e879f9" />
              <stop offset="100%" stop-color="#c084fc" />
            </linearGradient>
          </defs>
        </div>

        <!-- Hero Content -->
        <div class="relative z-10 animate-fade-in">
          <div class="w-16 h-16 mx-auto bg-white rounded-2xl flex items-center justify-center shadow-xl shadow-purple-200/50 mb-6 rotate-3 transform border border-purple-100">
            <BookOpen class="w-8 h-8 text-purple-500" />
          </div>
          <h1 class="font-display text-5xl md:text-6xl text-gray-900 mb-4">
            How to use your <span class="italic text-purple-600">Vault</span>
          </h1>
          <p class="font-body text-gray-500 max-w-lg mx-auto text-lg leading-relaxed">
            Scroll down to watch the guide unfold.
          </p>
          
          <!-- Scroll Indicator -->
          <div class="mt-12 animate-bounce opacity-50">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7c3aed" stroke-width="2">
              <path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- ── Help Sections ──────────────────────────────────────────────── -->
      <div class="relative z-10 max-w-6xl mx-auto px-6 pb-32">
        <div class="space-y-24 md:space-y-32">
          
          <div v-for="(item, index) in helpSections" 
               :key="item.id" 
               :ref="setRef"
               class="bloom-section grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-16 items-center">
            
            <!-- 
              Logic: 
              If index is EVEN (0, 2): Text on Left, Image on Right.
              If index is ODD (1, 3): Image on Left, Text on Right.
              
              We use 'order-last' on mobile to ensure image is always second, 
              but on desktop we swap using md:order classes.
            -->

            <!-- TEXT BOX SIDE -->
            <div :class="[
              'bloom-text-wrapper relative',
              index % 2 !== 0 ? 'md:order-2' : 'md:order-1'
            ]">
              <!-- The Decorative Petal Behind (Part of the emerge effect) -->
              <svg class="absolute -left-12 -top-12 w-48 h-48 opacity-10 text-petal rotate-12" 
                   viewBox="0 0 100 100" 
                   :style="{ fill: item.petalColor }">
                <path d="M50 100C50 100 0 50 0 25C0 11.2 11.2 0 25 0C37.5 0 50 12.5 50 25C50 12.5 62.5 0 75 0C88.8 0 100 11.2 100 25C100 50 50 100 50 100Z" />
              </svg>

              <!-- The Card -->
              <div class="bloom-card relative bg-white/80 backdrop-blur-sm border border-white p-8 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-lg transition-shadow duration-500">
                <div class="flex items-center gap-4 mb-4">
                  <div :class="`w-10 h-10 rounded-full ${item.bgColor} flex items-center justify-center`">
                    <component :is="item.icon" :class="`w-5 h-5 ${item.color}`" />
                  </div>
                  <h2 class="font-display text-3xl text-gray-800">{{ item.title }}</h2>
                </div>
                <p class="font-body text-gray-600 leading-relaxed text-lg">
                  {{ item.description }}
                </p>
                <div class="mt-6 flex items-center gap-2 text-sm font-semibold tracking-wide uppercase" :class="item.color">
                  <span>Learn more</span>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- IMAGE/SCREENSHOT SIDE -->
            <div :class="[
              'bloom-image-wrapper relative perspective-1000',
              index % 2 !== 0 ? 'md:order-1' : 'md:order-2'
            ]">
               <!-- Fake Browser Window / Screenshot Container -->
               <div class="screenshot-card bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden transform transition-all duration-1000">
                 <!-- Browser Toolbar -->
                 <div class="bg-gray-50 border-b border-gray-100 px-4 py-3 flex items-center gap-2">
                   <div class="w-3 h-3 rounded-full bg-red-300"></div>
                   <div class="w-3 h-3 rounded-full bg-amber-300"></div>
                   <div class="w-3 h-3 rounded-full bg-green-300"></div>
                   <div class="ml-4 w-full h-4 bg-white border border-gray-200 rounded-full opacity-50"></div>
                 </div>
                 <!-- Image Placeholder (Replace bg-color with <img> tag in real app) -->
                 <div class="h-64 w-full bg-gray-100 relative group overflow-hidden flex items-center justify-center">
                    <!-- Placeholder Visuals -->
                    <div class="absolute inset-0 opacity-10" 
                         :style="`background: linear-gradient(135deg, ${item.petalColor}, white);`"></div>
                    
                    <component :is="item.icon" 
                              class="w-16 h-16 opacity-20 transform group-hover:scale-110 transition-transform duration-700" 
                              :style="`color: ${item.petalColor}`"/>
                    
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/5">
                      <span class="bg-white px-4 py-2 rounded-full shadow-sm text-xs uppercase tracking-widest font-bold text-gray-500">
                        View Screenshot
                      </span>
                    </div>
                 </div>
               </div>
               
               <!-- Decorative elements behind image -->
               <div class="absolute -bottom-4 -right-4 w-full h-full border-2 border-dashed border-purple-200 rounded-xl -z-10"></div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </Sidebar>
</template>

<style scoped>
/* ── Theming ─────────────────────────────────────────────────────────────── */
.help-page {
  background: linear-gradient(160deg, #fdfaff 0%, #fffbfc 50%, #fcf4ff 100%);
}

.font-display {
  font-family: 'Cormorant Garamond', Georgia, serif;
}

.font-body {
  font-family: 'DM Sans', sans-serif;
}

/* ── Hero Petals Animation ───────────────────────────────────────────────── */
.falling-petal {
  top: -10%;
}

/* Generates random fall durations and delays for natural effect */
.petal-anim-1 { left: 10%; animation: fall 10s linear infinite, sway 4s ease-in-out infinite alternate; animation-delay: 0s; }
.petal-anim-2 { left: 25%; animation: fall 14s linear infinite, sway 5s ease-in-out infinite alternate; animation-delay: -2s; }
.petal-anim-3 { left: 40%; animation: fall 12s linear infinite, sway 3s ease-in-out infinite alternate; animation-delay: -5s; }
.petal-anim-4 { left: 55%; animation: fall 15s linear infinite, sway 6s ease-in-out infinite alternate; animation-delay: -1s; }
.petal-anim-5 { left: 70%; animation: fall 9s linear infinite, sway 4s ease-in-out infinite alternate; animation-delay: -8s; }
.petal-anim-6 { left: 85%; animation: fall 11s linear infinite, sway 5s ease-in-out infinite alternate; animation-delay: -3s; }
.petal-anim-7 { left: 15%; animation: fall 13s linear infinite, sway 4s ease-in-out infinite alternate; animation-delay: -6s; width: 20px; opacity: 0.4; }
.petal-anim-8 { left: 60%; animation: fall 16s linear infinite, sway 5s ease-in-out infinite alternate; animation-delay: -9s; width: 22px; opacity: 0.3; }

@keyframes fall {
  0% { transform: translateY(-10vh) rotate(0deg); }
  100% { transform: translateY(110vh) rotate(360deg); }
}

@keyframes sway {
  0% { margin-left: -20px; }
  100% { margin-left: 20px; }
}

.animate-fade-in {
  animation: fadeIn 1.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── The "Bloom" Effect (Scroll Reveal) ──────────────────────────────────── */

/* Initial State: Hidden, small, rotated (looking like a folded petal) */
.bloom-section .bloom-text-wrapper,
.bloom-section .bloom-image-wrapper {
  opacity: 0;
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.bloom-section .bloom-text-wrapper {
  transform: translateY(40px) scale(0.8) rotate(5deg);
  transform-origin: center left;
}

.bloom-section .bloom-image-wrapper {
  transform: translateY(40px) scale(0.9);
}

/* When the JS adds .is-visible */
.bloom-section.is-visible .bloom-text-wrapper {
  opacity: 1;
  transform: translateY(0) scale(1) rotate(0deg); /* Blooms into a straight box */
}

.bloom-section.is-visible .bloom-image-wrapper {
  opacity: 1;
  transform: translateY(0) scale(1);
  transition-delay: 0.2s; /* Image comes in slightly after text */
}

/* Decor Petal Spin on Reveal */
.bloom-section .text-petal {
  transform: rotate(0deg) scale(0.5);
  transition: transform 1.5s ease-out;
}
.bloom-section.is-visible .text-petal {
  transform: rotate(45deg) scale(1.2);
}

/* Perspective for Image 3D feel */
.perspective-1000 {
  perspective: 1000px;
}
</style>