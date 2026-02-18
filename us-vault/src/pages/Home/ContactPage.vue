<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ── Form state ────────────────────────────────────────────────────────────────
const title   = ref('')
const content = ref('')
const sending = ref(false)
const success = ref(false)
const error   = ref('')

const submitContact = async () => {
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Please fill in both fields.'
    return
  }

  error.value = ''
  sending.value = true

  const payload = {
    title: title.value,
    content: content.value,
    submitted_at: new Date().toISOString()
  }

  console.log('Submitting contact form:', payload)

  await new Promise(r => setTimeout(r, 1200))

  sending.value = false
  success.value = true

  setTimeout(() => {
    title.value = ''
    content.value = ''
    success.value = false
  }, 4000)
}
</script>

<template>
  <div class="contact-page">
    <component :is="'style'">
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
    </component>

    <!-- Background -->
    <div class="contact-bg" aria-hidden="true">
      <div class="contact-orb contact-orb-1"></div>
      <div class="contact-orb contact-orb-2"></div>
      <div class="contact-orb contact-orb-3"></div>
      <!-- Decorative SVG shapes -->
      <svg class="contact-shape contact-shape-1" viewBox="0 0 100 100">
        <rect x="10" y="10" width="80" height="80" fill="none" stroke="rgba(236,72,153,0.08)" stroke-width="1" rx="8"/>
        <rect x="20" y="20" width="60" height="60" fill="none" stroke="rgba(236,72,153,0.06)" stroke-width="1" rx="6"/>
      </svg>
      <svg class="contact-shape contact-shape-2" viewBox="0 0 60 60">
        <circle cx="30" cy="30" r="20" fill="none" stroke="rgba(244,63,94,0.06)" stroke-width="1"/>
        <circle cx="30" cy="30" r="12" fill="none" stroke="rgba(244,63,94,0.04)" stroke-width="1"/>
      </svg>
    </div>

    <!-- Navbar -->
    <nav class="contact-nav">
      <div class="contact-nav-container">
        <button @click="router.push('/')" class="contact-logo">
          <div class="contact-logo-icon">
            <svg width="18" height="18" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="white"/>
            </svg>
          </div>
          <span class="contact-logo-text">Us Vault</span>
        </button>
        <div class="flex items-center gap-3"> 
          <button @click="router.push('/')" class="contact-nav-link">Home</button>
          <button @click="router.push('/about')" class="contact-nav-link">About</button>
          <button @click="router.push('/login')" class="contact-nav-btn">Sign In</button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="contact-hero">
      <div class="contact-hero-container">
        <div class="contact-hero-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Get in Touch
        </div>
        <h1 class="contact-hero-title">Contact Us</h1>
        <p class="contact-hero-desc">We'd love to hear from you.</p>
      </div>
    </section>

    <!-- Form -->
    <section class="contact-form-section">
      <div class="contact-form-container">

        <!-- Info card -->
        <div class="contact-info">
          <div class="contact-info-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </div>
          <h2 class="contact-info-title">We're here to help</h2>
          <p class="contact-info-desc">
            Whether you have a question, feedback, or just want to say hello — we're all ears.
            Fill out the form and we'll get back to you as soon as we can.
          </p>
          <div class="contact-info-details">
            <div class="contact-info-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
              <span>We typically respond within 24 hours</span>
            </div>
            <div class="contact-info-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>Your information is safe with us</span>
            </div>
          </div>
        </div>

        <!-- Form card -->
        <div class="contact-form-card">
          <form @submit.prevent="submitContact">
            <div class="contact-form-group">
              <label for="title" class="contact-label">Subject</label>
              <input 
                id="title"
                v-model="title"
                type="text"
                placeholder="What's this about?"
                class="contact-input"
                :disabled="sending"
              />
            </div>

            <div class="contact-form-group">
              <label for="content" class="contact-label">Message</label>
              <textarea
                id="content"
                v-model="content"
                placeholder="Tell us more…"
                rows="8"
                class="contact-textarea"
                :disabled="sending"
              ></textarea>
            </div>

            <Transition name="error-shake">
              <p v-if="error" class="contact-error">{{ error }}</p>
            </Transition>

            <Transition name="success-pop">
              <div v-if="success" class="contact-success">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Message sent! We'll be in touch soon.
              </div>
            </Transition>

            <button type="submit" :disabled="sending || success" class="contact-submit-btn">
              <svg v-if="sending" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
              {{ sending ? 'Sending…' : success ? 'Sent!' : 'Send Message' }}
            </button>
          </form>
        </div>

      </div>
    </section>

    <!-- Footer -->
    <footer class="contact-footer">
      <div class="contact-footer-container">
        <div class="contact-footer-brand">
          <div class="contact-footer-logo">
            <svg width="16" height="16" viewBox="0 0 48 48" fill="none">
              <path d="M24 40C24 40 6 28 6 16C6 10.477 10.477 6 16 6C19.314 6 22.251 7.616 24 10.101C25.749 7.616 28.686 6 32 6C37.523 6 42 10.477 42 16C42 28 24 40 24 40Z" fill="#ec4899"/>
            </svg>
          </div>
          <span class="contact-footer-text">Us Vault</span>
        </div>
        <div class="contact-footer-links">
          <button @click="router.push('/about')" class="contact-footer-link">About</button>
          <button @click="router.push('/contact')" class="contact-footer-link">Contact</button>
          <button @click="router.push('/')" class="contact-footer-link">Sign In</button>
        </div>
        <p class="contact-footer-copy">© 2026 Us Vault. Built with love.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* ── Base ────────────────────────────────────────────────────────── */
.contact-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #fdf2f8 0%, #ffffff 40%, #fff7ed 100%);
  position: relative;
  overflow-x: hidden;
}

/* ── Background ──────────────────────────────────────────────────── */
.contact-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
.contact-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}
.contact-orb-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(236,72,153,0.15), transparent);
  top: -100px; left: -100px;
  animation: drift 20s ease-in-out infinite alternate;
}
.contact-orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(244,63,94,0.12), transparent);
  bottom: -80px; right: -80px;
  animation: drift 25s ease-in-out infinite alternate-reverse;
}
.contact-orb-3 {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(251,207,232,0.2), transparent);
  top: 50%; right: 10%;
  animation: drift 18s ease-in-out infinite;
}
@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50%      { transform: translate(30px, -30px) scale(1.1); }
}
.contact-shape {
  position: absolute;
  opacity: 0.4;
  animation: rotate 40s linear infinite;
}
.contact-shape-1 {
  width: 180px; height: 180px;
  top: 20%; left: 8%;
}
.contact-shape-2 {
  width: 120px; height: 120px;
  bottom: 15%; right: 12%;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* ── Nav ─────────────────────────────────────────────────────────── */
.contact-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(236,72,153,0.08);
  padding: 16px 0;
}
.contact-nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.contact-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.contact-logo:hover { opacity: 0.8; }
.contact-logo-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #ec4899, #f43f5e);
  display: flex; align-items: center; justify-content: center;
}
.contact-logo-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: -0.01em;
}
.contact-nav-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: color 0.2s;
  cursor: pointer;
}
.contact-nav-link:hover { color: #ec4899; }
.contact-nav-btn {
  padding: 8px 18px;
  border-radius: 10px;
  background: linear-gradient(135deg, #ec4899, #f43f5e);
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(236,72,153,0.25);
}
.contact-nav-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(236,72,153,0.35);
}

/* ── Hero ────────────────────────────────────────────────────────── */
.contact-hero {
  position: relative;
  z-index: 10;
  padding: 100px 24px 60px;
  text-align: center;
}
.contact-hero-container {
  max-width: 700px;
  margin: 0 auto;
}
.contact-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 12px;
  background: rgba(236,72,153,0.08);
  border: 1px solid rgba(236,72,153,0.15);
  color: #ec4899;
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  margin-bottom: 24px;
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1);
}
.contact-hero-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 600;
  color: #1f2937;
  line-height: 1.1;
  margin-bottom: 20px;
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) 0.1s both;
}
.contact-hero-desc {
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

/* ── Form Section ────────────────────────────────────────────────── */
.contact-form-section {
  position: relative;
  z-index: 10;
  padding: 0 24px 100px;
}
.contact-form-container {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}
@media (min-width: 768px) {
  .contact-form-container {
    grid-template-columns: 380px 1fr;
  }
}

/* ── Info Card ───────────────────────────────────────────────────── */
.contact-info {
  background: white;
  border: 1.5px solid rgba(236,72,153,0.12);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(236,72,153,0.06);
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
}
.contact-info-icon {
  width: 56px; height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #fce7f3, #fef3f2);
  display: flex; align-items: center; justify-content: center;
  color: #ec4899;
  margin-bottom: 24px;
}
.contact-info-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
  line-height: 1.3;
}
.contact-info-desc {
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  line-height: 1.7;
  color: #6b7280;
  margin-bottom: 28px;
}
.contact-info-details {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.contact-info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  color: #4b5563;
}
.contact-info-item svg {
  flex-shrink: 0;
  color: #ec4899;
}

/* ── Form Card ───────────────────────────────────────────────────── */
.contact-form-card {
  background: white;
  border: 1.5px solid rgba(236,72,153,0.12);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 4px 24px rgba(236,72,153,0.06);
  animation: fadeUp 0.8s cubic-bezier(0.22,1,0.36,1) 0.1s both;
}
.contact-form-group {
  margin-bottom: 24px;
}
.contact-label {
  display: block;
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.contact-input,
.contact-textarea {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1.5px solid #fbcfe8;
  font-family: 'Inter', sans-serif;
  font-size: 0.9375rem;
  color: #1f2937;
  background: white;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.contact-input:focus,
.contact-textarea:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 3px rgba(236,72,153,0.1);
}
.contact-input::placeholder,
.contact-textarea::placeholder {
  color: #d1d5db;
}
.contact-textarea {
  resize: vertical;
  min-height: 120px;
}
.contact-input:disabled,
.contact-textarea:disabled {
  background: #fef2f8;
  cursor: not-allowed;
  opacity: 0.6;
}

/* ── Error / Success ─────────────────────────────────────────────── */
.contact-error {
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  color: #ef4444;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
}
.contact-success {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: #16a34a;
  font-weight: 500;
  margin-bottom: 16px;
  padding: 12px 16px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 10px;
}

/* ── Submit Button ───────────────────────────────────────────────── */
.contact-submit-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, #ec4899, #f43f5e);
  color: white;
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 8px 24px rgba(236,72,153,0.3);
}
.contact-submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(236,72,153,0.4);
}
.contact-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ── Footer ──────────────────────────────────────────────────────── */
.contact-footer {
  position: relative;
  z-index: 10;
  border-top: 1px solid rgba(236,72,153,0.08);
  padding: 40px 24px;
  background: rgba(255,255,255,0.8);
}
.contact-footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  text-align: center;
}
.contact-footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}
.contact-footer-logo {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #fce7f3, #fef3f2);
  display: flex; align-items: center; justify-content: center;
}
.contact-footer-text {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}
.contact-footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  justify-content: center;
}
.contact-footer-link {
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  color: #6b7280;
  transition: color 0.2s;
  cursor: pointer;
}
.contact-footer-link:hover { color: #ec4899; }
.contact-footer-copy {
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  color: #9ca3af;
}

/* ── Transitions ─────────────────────────────────────────────────── */
.error-shake-enter-active {
  animation: shake 0.5s;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25%      { transform: translateX(-8px); }
  75%      { transform: translateX(8px); }
}

.success-pop-enter-active {
  animation: pop 0.5s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes pop {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}

/* ── Responsive ──────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .contact-info { padding: 28px 24px; }
  .contact-form-card { padding: 28px 24px; }
  .contact-hero { padding: 80px 24px 60px; }
}
</style>