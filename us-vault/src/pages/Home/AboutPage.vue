<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="about-page">
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Background -->
    <div class="about-bg" aria-hidden="true">
      <div class="about-orb about-orb-1"></div>
      <div class="about-orb about-orb-2"></div>
      <div class="about-orb about-orb-3"></div>
      <!-- Decorative SVG shapes -->
      <svg class="about-shape about-shape-1" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(124,58,237,0.08)" stroke-width="1"/>
        <circle cx="100" cy="100" r="60" fill="none" stroke="rgba(124,58,237,0.06)" stroke-width="1"/>
      </svg>
      <svg class="about-shape about-shape-2" viewBox="0 0 100 100">
        <path d="M50 10 L90 90 L10 90 Z" fill="none" stroke="rgba(168,85,247,0.06)" stroke-width="1"/>
      </svg>
    </div>

    <!-- Navbar -->
    <nav class="about-nav">
      <div class="about-nav-container">
        <button @click="router.push('/')" class="about-logo">
          <div class="about-logo-icon">
            <svg width="18" height="18" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white"/>
            </svg>
          </div>
          <span class="about-logo-text">Us Vault</span>
        </button>
        <div class="flex items-center gap-3">
          <button @click="router.push('/contact')" class="about-nav-link">Contact</button>
          <button @click="router.push('/')" class="about-nav-link">Home</button>
          <button @click="router.push('/login')" class="about-nav-btn">Sign In</button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="about-hero">
      <div class="about-hero-container">
        <div class="about-hero-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          Our Story
        </div>
        <h1 class="about-hero-title">About Us Vault</h1>
        <p class="about-hero-desc">A space for two, built with love.</p>
      </div>
    </section>

    <!-- Content -->
    <section class="about-content">
      <div class="about-content-container">

        <!-- Story card -->
        <article class="about-card about-card--main">
          <div class="about-card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </div>
          <h2 class="about-card-title">Where It All Started</h2>
          <div class="about-card-content">
            <p>Us Vault began as a passion project — a gift for a close friend who needed something special. Not another social media app. Not another place where you have to perform for an audience.</p>
            <p>Just a quiet, intimate space. A vault. For two.</p>
            <p>We wanted to create somewhere you could share moments without the pressure of likes, comments, or the endless scroll. A place where you could remind your person that you're thinking of them — not because you have to respond to everyone else, but because you genuinely want to.</p>
            <p>Where memories aren't buried under algorithmic noise, but treasured and preserved. Where you can plant seeds of love that bloom at just the right moment.</p>
          </div>
        </article>

        <!-- Features grid -->
        <div class="about-grid">
          <div class="about-feature">
            <div class="about-feature-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <h3 class="about-feature-title">Private by Design</h3>
            <p class="about-feature-desc">No public profiles. No followers. Just you two. Your vault is yours alone — a sacred space for the relationship that matters most.</p>
          </div>

          <div class="about-feature">
            <div class="about-feature-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
              </svg>
            </div>
            <h3 class="about-feature-title">Without the Clutter</h3>
            <p class="about-feature-desc">No ads. No distractions. No pressure to respond to anyone else. This isn't about growing an audience — it's about deepening a connection.</p>
          </div>

          <div class="about-feature">
            <div class="about-feature-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
              </svg>
            </div>
            <h3 class="about-feature-title">Moments That Matter</h3>
            <p class="about-feature-desc">Plant seeds for the future. Archive memories from today. Send silent signals that say "I'm thinking of you" — without needing a reply.</p>
          </div>

          <div class="about-feature">
            <div class="about-feature-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <h3 class="about-feature-title">Feel Special, Not Clingy</h3>
            <p class="about-feature-desc">Express yourself freely without worrying about being "too much." This is a space designed for closeness, not performance.</p>
          </div>
        </div>

        <!-- Philosophy -->
        <article class="about-card about-card--accent">
          <h2 class="about-card-title">The Philosophy</h2>
          <div class="about-card-content">
            <p>We believe relationships deserve their own sanctuary. A place where love isn't competing for attention with everyone else's updates. Where you don't have to curate your vulnerability for public consumption.</p>
            <p>Us Vault is about presence, not performance. It's about holding space for the one person who matters most — without the weight of an audience watching.</p>
            <p class="about-quote">"Because some things are too precious to share with the world."</p>
          </div>
        </article>

        <!-- CTA -->
        <div class="about-cta">
          <h2 class="about-cta-title">Ready to build your vault?</h2>
          <p class="about-cta-desc">Create a space where your relationship can breathe.</p>
          <button @click="router.push('/')" class="about-cta-btn">
            Get Started
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
            </svg>
          </button>
        </div>

      </div>
    </section>

    <!-- Footer -->
    <footer class="about-footer">
      <div class="about-footer-container">
        <div class="about-footer-brand">
          <div class="about-footer-logo">
            <svg width="16" height="16" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="#7c3aed"/>
            </svg>
          </div>
          <span class="about-footer-text">Us Vault</span>
        </div>
        <div class="about-footer-links">
          <button @click="router.push('/about')" class="about-footer-link">About</button>
          <button @click="router.push('/contact')" class="about-footer-link">Contact</button>
          <button @click="router.push('/')" class="about-footer-link">Sign In</button>
        </div>
        <p class="about-footer-copy">© 2026 Us Vault. Built with love.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* ── Base ────────────────────────────────────────────────────────── */
.about-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #faf5ff 0%, #ffffff 40%, #fdf8ff 100%);
  position: relative;
  overflow-x: hidden;
}

/* ── Background ──────────────────────────────────────────────────── */
.about-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.about-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}
.about-orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(124,58,237,0.15), transparent);
  top: -100px; right: -100px;
  animation: drift 20s ease-in-out infinite alternate;
}
.about-orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(168,85,247,0.12), transparent);
  bottom: -80px; left: -80px;
  animation: drift 25s ease-in-out infinite alternate-reverse;
}
.about-orb-3 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(192,132,252,0.1), transparent);
  top: 50%; left: 50%;
  animation: drift 18s ease-in-out infinite;
}
@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%      { transform: translate(30px, -30px) scale(1.1); }
}
.about-shape {
  position: absolute;
  opacity: 0.4;
  animation: rotate 40s linear infinite;
}
.about-shape-1 {
  width: 200px; height: 200px;
  top: 15%; right: 10%;
}
.about-shape-2 {
  width: 120px; height: 120px;
  bottom: 20%; left: 8%;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* ── Nav ─────────────────────────────────────────────────────────── */
.about-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(124,58,237,0.08);
  padding: 16px 0;
}
.about-nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.about-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.about-logo:hover { opacity: 0.8; }
.about-logo-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  display: flex; align-items: center; justify-content: center;
}
.about-logo-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: -0.01em;
}
.about-nav-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: color 0.2s;
  cursor: pointer;
}
.about-nav-link:hover { color: #7c3aed; }
.about-nav-btn {
  padding: 8px 18px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7c3aed, #a855f7);
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(124,58,237,0.25);
}
.about-nav-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(124,58,237,0.35);
}

/* ── Hero ────────────────────────────────────────────────────────── */
.about-hero {
  position: relative;
  z-index: 10;
  padding: 100px 24px 80px;
  text-align: center;
}
.about-hero-container {
  max-width: 700px;
  margin: 0 auto;
}
.about-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 12px;
  background: rgba(124,58,237,0.08);
  border: 1px solid rgba(124,58,237,0.15);
  color: #7c3aed;
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  margin-bottom: 24px;
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1);
}
.about-hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 600;
  color: #1f2937;
  line-height: 1.1;
  margin-bottom: 20px;
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) 0.1s both;
}
.about-hero-desc {
  font-family: 'Inter', sans-serif;
  font-size: 1.25rem;
  color: #6b7280;
  font-weight: 400;
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) 0.2s both;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Content ─────────────────────────────────────────────────────── */
.about-content {
  position: relative;
  z-index: 10;
  padding: 0 24px 100px;
}
.about-content-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

/* ── Cards ───────────────────────────────────────────────────────── */
.about-card {
  background: white;
  border: 1.5px solid rgba(124,58,237,0.12);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(124,58,237,0.06);
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
.about-card--accent {
  background: linear-gradient(145deg, #faf5ff, #ffffff);
  border-color: rgba(124,58,237,0.2);
}
.about-card-icon {
  width: 56px; height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f3e8ff, #fdf4ff);
  display: flex; align-items: center; justify-content: center;
  color: #7c3aed;
  margin-bottom: 24px;
}
.about-card-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 20px;
  line-height: 1.3;
}
.about-card-content {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  line-height: 1.8;
  color: #4b5563;
}
.about-card-content p {
  margin-bottom: 16px;
}
.about-card-content p:last-child {
  margin-bottom: 0;
}
.about-quote {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-style: italic;
  color: #7c3aed;
  margin-top: 28px;
  padding-left: 24px;
  border-left: 3px solid #c084fc;
}

/* ── Features grid ───────────────────────────────────────────────── */
.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}
.about-feature {
  background: white;
  border: 1.5px solid rgba(124,58,237,0.1);
  border-radius: 20px;
  padding: 28px;
  transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
}
.about-feature:hover {
  border-color: rgba(124,58,237,0.25);
  box-shadow: 0 12px 32px rgba(124,58,237,0.12);
  transform: translateY(-4px);
}
.about-feature-icon {
  width: 44px; height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f3e8ff, #fdf4ff);
  display: flex; align-items: center; justify-content: center;
  color: #7c3aed;
  margin-bottom: 16px;
}
.about-feature-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 10px;
  line-height: 1.3;
}
.about-feature-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  line-height: 1.7;
  color: #6b7280;
}

/* ── CTA ─────────────────────────────────────────────────────────── */
.about-cta {
  text-align: center;
  padding: 60px 40px;
  background: linear-gradient(145deg, #7c3aed, #a855f7);
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(124,58,237,0.3);
}
.about-cta-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2rem;
  font-weight: 600;
  color: white;
  margin-bottom: 12px;
  line-height: 1.2;
}
.about-cta-desc {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  color: rgba(255,255,255,0.9);
  margin-bottom: 32px;
}
.about-cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  border-radius: 12px;
  background: white;
  color: #7c3aed;
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.about-cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.18);
}

/* ── Footer ──────────────────────────────────────────────────────── */
.about-footer {
  position: relative;
  z-index: 10;
  border-top: 1px solid rgba(124,58,237,0.08);
  padding: 40px 24px;
  background: rgba(255,255,255,0.8);
}
.about-footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  text-align: center;
}
.about-footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.about-footer-logo {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #f3e8ff, #fdf4ff);
  display: flex; align-items: center; justify-content: center;
}
.about-footer-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}
.about-footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: center;
}
.about-footer-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.2s;
  cursor: pointer;
}
.about-footer-link:hover { color: #7c3aed; }
.about-footer-copy {
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  color: #9ca3af;
}

/* ── Responsive ──────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .about-card { padding: 28px 24px; }
  .about-hero { padding: 80px 24px 60px; }
  .about-cta { padding: 40px 24px; }
  .about-grid { grid-template-columns: 1fr; }
}
</style>