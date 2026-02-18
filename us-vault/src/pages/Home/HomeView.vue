<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Scroll-based color transition ────────────────────────────────────────────
const scrollProgress = ref(0)

const updateScrollProgress = () => {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  scrollProgress.value = Math.min(scrollTop / docHeight, 1)
}

onMounted(() => {
  window.addEventListener('scroll', updateScrollProgress)
  updateScrollProgress()
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateScrollProgress)
})

// Interpolate between purple and pink based on scroll
const computedBgColor = () => {
  const purple = { r: 124, g: 58, b: 237 }  // #7c3aed
  const pink = { r: 236, g: 72, b: 153 }     // #ec4899
  
  const r = Math.round(purple.r + (pink.r - purple.r) * scrollProgress.value)
  const g = Math.round(purple.g + (pink.g - purple.g) * scrollProgress.value)
  const b = Math.round(purple.b + (pink.b - purple.b) * scrollProgress.value)
  
  return `rgb(${r}, ${g}, ${b})`
}

const features = [
  {
    icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
    title: 'Your Private Vault',
    desc: 'A sacred space for you and your closest person. No public profiles, no followers, no noise.'
  },
  {
    icon: 'M12 2L2 7l10 5 10-5-10-5z M2 17l10 5 10-5 M2 12l10 5 10-5',
    title: 'Seeds & Blooms',
    desc: 'Plant memories for the future. Watch them bloom at just the right moment.'
  },
  {
    icon: 'M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z',
    title: 'Signals',
    desc: 'Send silent "thinking of you" moments without needing a reply. Just presence.'
  },
  {
    icon: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z',
    title: 'Journals',
    desc: 'Write privately or share your thoughts. Express yourself without performance.'
  }
]
</script>

<template>
  <div class="home-page">
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Dynamic gradient background that shifts with scroll -->
    <div class="home-gradient-bg" :style="{ background: `linear-gradient(180deg, ${computedBgColor()} 0%, rgba(255,255,255,0.95) 100%)` }"></div>

    <!-- Ambient decorations -->
    <div class="home-ambient" aria-hidden="true">
      <div class="home-orb home-orb-1"></div>
      <div class="home-orb home-orb-2"></div>
      <div class="home-orb home-orb-3"></div>
    </div>

    <!-- ── Navbar ──────────────────────────────────────────────── -->
    <nav class="home-nav">
      <div class="home-nav-container">
        <button @click="router.push('/')" class="home-logo">
          <div class="home-logo-icon" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">
            <svg width="20" height="20" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white"/>
            </svg>
          </div>
          <span class="home-logo-text">Us Vault</span>
        </button>
        <div class="flex items-center gap-8">
          <button @click="router.push('/')" class="home-nav-link">Home</button>
          <button @click="router.push('/about')" class="home-nav-link">About</button>
          <button @click="router.push('/contact')" class="home-nav-link">Contact</button>
          <button @click="router.push('/')" class="home-nav-btn" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">
            Sign In
          </button>
        </div>
      </div>
    </nav>

    <!-- ── Hero Section ────────────────────────────────────────── -->
    <section class="home-hero">
      <div class="home-hero-container">
        
        <!-- Left: Text content -->
        <div class="home-hero-content">
          <div class="home-hero-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
            </svg>
            A space for two
          </div>
          <h1 class="home-hero-title">
            Your Vault.<br/>
            Your Memories.<br/>
            <span class="home-hero-title-accent">Just You Two.</span>
          </h1>
          <p class="home-hero-desc">
            Not another social network. Not a place to perform for followers. 
            Just an intimate space to share moments, plant seeds for the future, 
            and remind your closest person that they matter — without the noise of the world watching.
          </p>
          <div class="flex items-center gap-4 flex-wrap">
            <button @click="router.push('/')" class="home-hero-cta" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">
              Create Your Vault
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
              </svg>
            </button>
            <button @click="router.push('/about')" class="home-hero-secondary">
              Learn More
            </button>
          </div>
        </div>

        <!-- Right: Curved wave image -->
      <div class="home-hero-image-wrapper">
        <svg viewBox="0 0 1200 900" preserveAspectRatio="xMidYMin slice" class="home-hero-svg">

          <defs>
            <clipPath id="waveClip">
              <path d="M100,0 Q420,180 350,450 Q300,700 420,900 L1200,900 L1200,0 Z"/>
            </clipPath>
          </defs>

          <!-- Background wave color -->
          <path
            d="M100,0 Q420,180 350,450 Q300,700 420,900 L1200,900 L1200,0 Z"
            :fill="computedBgColor()"
          />

          <!-- Image INSIDE the SVG -->
          <image
            href="/images/homepage_image.jpg"
            width="1200"
            height="1050"
            y="-150"
            clip-path="url(#waveClip)"
            preserveAspectRatio="xMidYMid slice"
          />
          
        </svg>
      </div>


      </div>
    </section>

    <!-- ── Features Grid ───────────────────────────────────────── -->
    <section class="home-features">
      <div class="home-features-container">
        <div class="home-features-header">
          <h2 class="home-features-title">Everything you need to feel close</h2>
          <p class="home-features-subtitle">Built for intimacy, not audience.</p>
        </div>

        <div class="home-features-grid">
          <article v-for="(feature, idx) in features" :key="idx" 
                   class="home-feature-card"
                   :style="`animation-delay: ${idx * 100}ms`">
            <div class="home-feature-icon" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}15, ${computedBgColor()}08)`, color: computedBgColor() }">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path :d="feature.icon"/>
              </svg>
            </div>
            <h3 class="home-feature-title">{{ feature.title }}</h3>
            <p class="home-feature-desc">{{ feature.desc }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ── How It Works ────────────────────────────────────────── -->
    <section class="home-how">
      <div class="home-how-container">
        <h2 class="home-how-title">How it works</h2>
        <div class="home-how-steps">
          <div class="home-how-step">
            <div class="home-how-number" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">1</div>
            <h3 class="home-how-step-title">Create Your Vault</h3>
            <p class="home-how-step-desc">Sign up and invite your person. Simple. Private. Just for you two.</p>
          </div>
          <div class="home-how-connector"></div>
          <div class="home-how-step">
            <div class="home-how-number" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">2</div>
            <h3 class="home-how-step-title">Share Your Moments</h3>
            <p class="home-how-step-desc">Add memories, plant seeds, write journals. No likes, no comments, no pressure.</p>
          </div>
          <div class="home-how-connector"></div>
          <div class="home-how-step">
            <div class="home-how-number" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">3</div>
            <h3 class="home-how-step-title">Stay Connected</h3>
            <p class="home-how-step-desc">Send signals, watch seeds bloom, and cherish every moment in your private space.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Testimonial / Quote ─────────────────────────────────── -->
    <section class="home-quote">
      <div class="home-quote-container">
        <svg class="home-quote-mark" width="48" height="48" viewBox="0 0 24 24" fill="none" :stroke="computedBgColor()" stroke-width="1.5">
          <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"/>
          <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>
        </svg>
        <blockquote class="home-quote-text">
          Because some things are too precious to share with the world.
        </blockquote>
        <p class="home-quote-author">— The Us Vault Philosophy</p>
      </div>
    </section>

    <!-- ── Final CTA ───────────────────────────────────────────── -->
    <section class="home-final-cta">
      <div class="home-final-cta-container">
        <h2 class="home-final-cta-title">Ready to build your vault?</h2>
        <p class="home-final-cta-desc">Create a space where your relationship can breathe.</p>
        <button @click="router.push('/')" class="home-final-cta-btn" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}, ${computedBgColor()})` }">
          Get Started — It's Free
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
          </svg>
        </button>
      </div>
    </section>

    <!-- ── Footer ──────────────────────────────────────────────── -->
    <footer class="home-footer">
      <div class="home-footer-container">
        <div class="home-footer-brand">
          <div class="home-footer-logo" :style="{ background: `linear-gradient(135deg, ${computedBgColor()}20, ${computedBgColor()}10)` }">
            <svg width="18" height="18" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" :fill="computedBgColor()"/>
            </svg>
          </div>
          <span class="home-footer-text">Us Vault</span>
        </div>
        <div class="home-footer-links">
          <button @click="router.push('/')" class="home-footer-link">Home</button>
          <button @click="router.push('/about')" class="home-footer-link">About</button>
          <button @click="router.push('/contact')" class="home-footer-link">Contact</button>
          <button @click="router.push('/')" class="home-footer-link">Privacy</button>
        </div>
        <p class="home-footer-copy">© 2026 Us Vault. Built with love for the people who matter most.</p>
      </div>
    </footer>

  </div>
</template>

<style scoped>
/* ── Base ────────────────────────────────────────────────────────── */
.home-page {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* ── Gradient background ─────────────────────────────────────────── */
.home-gradient-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  transition: background 0.3s ease;
}

/* ── Ambient decorations ─────────────────────────────────────────── */
.home-ambient {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}
.home-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.2;
}
.home-orb-1 {
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,255,255,0.3), transparent);
  top: -200px; right: -200px;
  animation: drift 25s ease-in-out infinite alternate;
}
.home-orb-2 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,255,255,0.25), transparent);
  bottom: -150px; left: -150px;
  animation: drift 30s ease-in-out infinite alternate-reverse;
}
.home-orb-3 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(255,255,255,0.2), transparent);
  top: 50%; left: 50%;
  animation: drift 20s ease-in-out infinite;
}
@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%      { transform: translate(50px, -40px) scale(1.1); }
}

/* ── Nav ─────────────────────────────────────────────────────────── */
.home-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  padding: 18px 0;
}
.home-nav-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.home-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.home-logo:hover { opacity: 0.85; }
.home-logo-icon {
  width: 40px; height: 40px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transition: background 0.3s;
}
.home-logo-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: -0.02em;
}
.home-nav-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #4b5563;
  transition: color 0.2s;
  cursor: pointer;
}
.home-nav-link:hover { color: #1f2937; }
.home-nav-btn {
  padding: 10px 24px;
  border-radius: 12px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}
.home-nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}

/* ── Hero ────────────────────────────────────────────────────────── */
.home-hero {
  position: relative;
  z-index: 10;
  padding: 80px 0 120px;
}
.home-hero-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 60px;
  align-items: center;
}
@media (min-width: 1024px) {
  .home-hero-container {
    grid-template-columns: 1fr 1.2fr;
  }
}

/* Hero content */
.home-hero-content {
  max-width: 600px;
  animation: fadeUp 1s cubic-bezier(0.22,1,0.36,1);
}
.home-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 14px;
  background: rgba(255,255,255,0.95);
  border: 1px solid rgba(0,0,0,0.08);
  color: #374151;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.home-hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 600;
  color: white;
  line-height: 1.1;
  margin-bottom: 28px;
  text-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.home-hero-title-accent {
  display: block;
  font-style: italic;
  opacity: 0.95;
}
.home-hero-desc {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  line-height: 1.8;
  color: rgba(255,255,255,0.95);
  margin-bottom: 40px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.home-hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 32px;
  border-radius: 14px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 1.0625rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.home-hero-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 36px rgba(0,0,0,0.25);
}
.home-hero-secondary {
  padding: 16px 32px;
  border-radius: 14px;
  background: rgba(255,255,255,0.95);
  color: #374151;
  font-family: 'Inter', sans-serif;
  font-size: 1.0625rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.home-hero-secondary:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Hero image with wave */
.home-hero-image-wrapper {
  position: relative;
  height: 600px;
  animation: fadeUp 1s cubic-bezier(0.22,1,0.36,1) 0.2s both;
}
@media (max-width: 1023px) {
  .home-hero-image-wrapper {
    margin: 0 -32px;
    height: 400px;
  }
}
.home-hero-svg {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 100%;
  transition: fill 0.3s;
}
.home-hero-image {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 100%;
  object-fit: cover;
  object-position: center;
  clip-path: url(#waveClip);
}

/* ── Features ────────────────────────────────────────────────────── */
.home-features {
  position: relative;
  z-index: 10;
  padding: 100px 0;
  background: white;
}
.home-features-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}
.home-features-header {
  text-align: center;
  margin-bottom: 72px;
}
.home-features-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
  line-height: 1.2;
}
.home-features-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 1.25rem;
  color: #6b7280;
}
.home-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 32px;
}
.home-feature-card {
  background: white;
  border: 1.5px solid #f3f4f6;
  border-radius: 20px;
  padding: 36px;
  transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
  animation: cardSlideUp 0.6s cubic-bezier(0.22,1,0.36,1) both;
}
.home-feature-card:hover {
  border-color: #e5e7eb;
  box-shadow: 0 20px 48px rgba(0,0,0,0.08);
  transform: translateY(-6px);
}
@keyframes cardSlideUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.home-feature-icon {
  width: 60px; height: 60px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 24px;
  transition: all 0.3s;
}
.home-feature-card:hover .home-feature-icon {
  transform: scale(1.1);
}
.home-feature-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.375rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
  line-height: 1.3;
}
.home-feature-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.7;
  color: #6b7280;
}

/* ── How It Works ────────────────────────────────────────────────── */
.home-how {
  position: relative;
  z-index: 10;
  padding: 100px 0;
  background: #fafafa;
}
.home-how-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 32px;
}
.home-how-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  margin-bottom: 72px;
}
.home-how-steps {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: 24px;
  align-items: center;
}
@media (max-width: 768px) {
  .home-how-steps {
    grid-template-columns: 1fr;
  }
  .home-how-connector { display: none; }
}
.home-how-step {
  text-align: center;
}
.home-how-number {
  width: 56px; height: 56px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  transition: background 0.3s;
}
.home-how-step-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}
.home-how-step-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.7;
  color: #6b7280;
}
.home-how-connector {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, #d1d5db, #e5e7eb);
}

/* ── Quote ───────────────────────────────────────────────────────── */
.home-quote {
  position: relative;
  z-index: 10;
  padding: 100px 0;
  background: white;
}
.home-quote-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 32px;
  text-align: center;
}
.home-quote-mark {
  margin: 0 auto 24px;
  opacity: 0.6;
}
.home-quote-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(1.5rem, 4vw, 2.25rem);
  font-weight: 400;
  font-style: italic;
  color: #1f2937;
  line-height: 1.5;
  margin-bottom: 20px;
}
.home-quote-author {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  color: #9ca3af;
}

/* ── Final CTA ───────────────────────────────────────────────────── */
.home-final-cta {
  position: relative;
  z-index: 10;
  padding: 120px 0;
  background: #fafafa;
}
.home-final-cta-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 32px;
  text-align: center;
}
.home-final-cta-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2rem, 5vw, 3.25rem);
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
  line-height: 1.2;
}
.home-final-cta-desc {
  font-family: 'Inter', sans-serif;
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 48px;
}
.home-final-cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 18px 40px;
  border-radius: 14px;
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 12px 36px rgba(0,0,0,0.2);
}
.home-final-cta-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 48px rgba(0,0,0,0.25);
}

/* ── Footer ──────────────────────────────────────────────────────── */
.home-footer {
  position: relative;
  z-index: 10;
  border-top: 1px solid #e5e7eb;
  padding: 60px 0;
  background: white;
}
.home-footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
  text-align: center;
}
.home-footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.home-footer-logo {
  width: 40px; height: 40px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.3s;
}
.home-footer-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}
.home-footer-links {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  justify-content: center;
}
.home-footer-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  font-weight: 500;
  color: #6b7280;
  transition: color 0.2s;
  cursor: pointer;
}
.home-footer-link:hover { color: #1f2937; }
.home-footer-copy {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: #9ca3af;
}

/* ── Responsive ──────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .home-nav-container { padding: 0 20px; }
  .home-nav-container > div { display: none; }
  .home-hero { padding: 60px 0 80px; }
  .home-features { padding: 60px 0; }
  .home-how { padding: 60px 0; }
  .home-quote { padding: 60px 0; }
  .home-final-cta { padding: 80px 0; }
}
</style>