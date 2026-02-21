<script setup>
import { ref, computed, onUnmounted } from 'vue'
import Sidebar from '../../components/layout/Sidebar.vue'
import InactivityOverlay from '../../components/layout/InactivityOverlay.vue'

// ── State ─────────────────────────────────────────────────────────────────────
const MAX_SIGNALS = 25
const COOLDOWN_S  = 5

const signalsSent   = ref(0)
const isCoolingDown = ref(false)
const cooldownLeft  = ref(0)
const isAnimating   = ref(false)  // thought bubble active
const isSending     = ref(false)  // API in-flight
const thoughtsToday = ref([])     // timestamps of signals sent today
let   cooldownTimer = null
let   animTimer     = null

// ── Computed ──────────────────────────────────────────────────────────────────
const canSend       = computed(() => !isCoolingDown.value && !isSending.value && signalsSent.value < MAX_SIGNALS)
const remaining     = computed(() => MAX_SIGNALS - signalsSent.value)
const progressAngle = computed(() => (signalsSent.value / MAX_SIGNALS) * 360)

// ── Send signal ───────────────────────────────────────────────────────────────
const sendSignal = async () => {
  if (!canSend.value) return

  isSending.value  = true
  isAnimating.value = true

  // Dummy API call
  console.log('Signal sent at', new Date().toISOString())
  await new Promise(r => setTimeout(r, 600))

  signalsSent.value++
  thoughtsToday.value.push(Date.now())
  isSending.value  = false

  // Start cooldown
  isCoolingDown.value = true
  cooldownLeft.value  = COOLDOWN_S

  cooldownTimer = setInterval(() => {
    cooldownLeft.value--
    if (cooldownLeft.value <= 0) {
      clearInterval(cooldownTimer)
      isCoolingDown.value = false
    }
  }, 1000)

  // Keep thought bubble showing for 3.5s then fade
  clearTimeout(animTimer)
  animTimer = setTimeout(() => {
    isAnimating.value = false
  }, 3500)
}

onUnmounted(() => {
  clearInterval(cooldownTimer)
  clearTimeout(animTimer)
})
</script>

<template>
  <InactivityOverlay>
        <Sidebar>
      <div class="signal-page">
        <component :is="'style'">
          @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        </component>

        <!-- ── Background ─────────────────────────────────────────── -->
        <div class="signal-bg" aria-hidden="true">
          <!-- Slow drifting gradient orbs -->
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="orb orb-3"></div>
          <!-- Subtle grid -->
          <div class="signal-grid"></div>
        </div>

        <!-- ── Content ────────────────────────────────────────────── -->
        <div class="signal-content">

          <!-- Title -->
          <div class="signal-header">
            <h1 class="signal-title">Send a thought</h1>
            <p class="signal-sub">Let them know you're thinking of them.</p>
          </div>

          <!-- ── The Scene ─────────────────────────────────────────── -->
          <div class="scene-wrapper" @click="sendSignal" :class="{ 'scene--active': isAnimating, 'scene--disabled': !canSend }">

            <!-- Ripple rings (emit on click) -->
            <div class="ripple-ring ripple-1" :class="{ 'ripple--go': isAnimating }"></div>
            <div class="ripple-ring ripple-2" :class="{ 'ripple--go': isAnimating }"></div>
            <div class="ripple-ring ripple-3" :class="{ 'ripple--go': isAnimating }"></div>

            <!-- Person SVG scene -->
            <svg class="person-svg" viewBox="0 0 220 260" fill="none" xmlns="http://www.w3.org/2000/svg">

              <!-- Floor line -->
              <line x1="20" y1="230" x2="200" y2="230" stroke="#e2d9f3" stroke-width="1.5" stroke-linecap="round"/>

              <!-- ── Person body ── -->
              <!-- Legs / sitting cross-legged -->
              <path d="M80 200 Q70 218 55 222 Q68 224 90 215 Z" fill="#6d28d9" opacity="0.7"/>
              <path d="M140 200 Q150 218 165 222 Q152 224 130 215 Z" fill="#6d28d9" opacity="0.7"/>
              <!-- Body -->
              <rect x="82" y="155" width="56" height="52" rx="18" fill="#7c3aed"/>
              <!-- Arms resting -->
              <path d="M82 178 Q62 185 58 200 Q68 196 80 192 Z" fill="#6d28d9" opacity="0.8"/>
              <path d="M138 178 Q158 185 162 200 Q152 196 140 192 Z" fill="#6d28d9" opacity="0.8"/>
              <!-- Hands -->
              <ellipse cx="58" cy="202" rx="8" ry="6" fill="#a78bfa"/>
              <ellipse cx="162" cy="202" rx="8" ry="6" fill="#a78bfa"/>

              <!-- Neck -->
              <rect x="102" y="142" width="16" height="16" rx="6" fill="#a78bfa"/>

              <!-- Head -->
              <ellipse cx="110" cy="126" rx="26" ry="24" fill="#a78bfa"/>

              <!-- ── Eyes (asleep → awake) ── -->
              <!-- Sleeping eyes (closed arcs) -->
              <g class="eyes-asleep" :class="{ 'eyes--hide': isAnimating }">
                <path d="M100 124 Q104 120 108 124" stroke="#5b21b6" stroke-width="2" stroke-linecap="round" fill="none"/>
                <path d="M112 124 Q116 120 120 124" stroke="#5b21b6" stroke-width="2" stroke-linecap="round" fill="none"/>
              </g>
              <!-- Awake eyes (open circles) -->
              <g class="eyes-awake" :class="{ 'eyes--show': isAnimating }">
                <circle cx="104" cy="123" r="4" fill="#4c1d95"/>
                <circle cx="116" cy="123" r="4" fill="#4c1d95"/>
                <circle cx="105.5" cy="121.5" r="1.5" fill="white"/>
                <circle cx="117.5" cy="121.5" r="1.5" fill="white"/>
              </g>

              <!-- Eyebrows (surprised when active) -->
              <g class="brows" :class="{ 'brows--up': isAnimating }">
                <path d="M99 116 Q104 114 109 116" stroke="#5b21b6" stroke-width="1.8" stroke-linecap="round" fill="none"/>
                <path d="M111 116 Q116 114 121 116" stroke="#5b21b6" stroke-width="1.8" stroke-linecap="round" fill="none"/>
              </g>

              <!-- Mouth (smile) -->
              <path class="mouth" :class="{ 'mouth--smile': isAnimating }"
                    d="M104 133 Q110 135 116 133" stroke="#5b21b6" stroke-width="1.8" stroke-linecap="round" fill="none"/>

              <!-- Hair little tufts -->
              <path d="M88 112 Q86 104 92 106" stroke="#5b21b6" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M110 102 Q110 94 115 97" stroke="#5b21b6" stroke-width="2.5" stroke-linecap="round" fill="none"/>
              <path d="M130 110 Q134 103 130 106" stroke="#5b21b6" stroke-width="2.5" stroke-linecap="round" fill="none"/>

              <!-- ── Z z z (asleep, disappears on click) ── -->
              <g class="zs" :class="{ 'zs--hide': isAnimating }">
                <text x="138" y="108" font-size="11" fill="#c4b5fd" opacity="0.8" font-family="DM Sans">z</text>
                <text x="148" y="96"  font-size="9"  fill="#c4b5fd" opacity="0.55" font-family="DM Sans">z</text>
                <text x="156" y="86"  font-size="7"  fill="#c4b5fd" opacity="0.35" font-family="DM Sans">z</text>
              </g>

              <!-- ── Thought bubble chain ── -->
              <g class="thought-group" :class="{ 'thought--show': isAnimating }">
                <!-- Small circles leading up -->
                <circle cx="132" cy="108" r="3.5" fill="white" opacity="0.9"/>
                <circle cx="141" cy="96"  r="5"   fill="white" opacity="0.95"/>
                <circle cx="152" cy="82"  r="7"   fill="white"/>

                <!-- Main bubble -->
                <rect x="152" y="40" width="56" height="42" rx="14" fill="white"/>
                <!-- Bubble tail -->
                <polygon points="165,80 172,82 168,86" fill="white"/>

                <!-- Heart inside bubble -->
                <g class="bubble-heart">
                  <path d="M180 57 C180 54 177 51 174 51 C171 51 168 54 168 57 C168 62 174 68 180 72 C186 68 192 62 192 57 C192 54 189 51 186 51 C183 51 180 54 180 57Z" fill="#f43f5e"/>
                </g>

                <!-- "thinking of you" text -->
                <text x="180" y="78" font-size="5.5" fill="#7c3aed" text-anchor="middle" font-family="DM Sans" font-weight="500">thinking of you</text>
              </g>

            </svg>

            <!-- Cursor hint when idle -->
            <div class="click-hint" :class="{ 'hint--hide': isAnimating || isCoolingDown || signalsSent > 0 }">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2v-4M9 21H5a2 2 0 0 1-2-2v-4m0 0h18"/></svg>
              <span>Click to send</span>
            </div>
          </div>

          <!-- ── Count ring ──────────────────────────────────────── -->
          <div class="count-area">
            <svg class="count-ring" viewBox="0 0 80 80" width="80" height="80">
              <!-- Track -->
              <circle cx="40" cy="40" r="32" fill="none" stroke="#ede9fe" stroke-width="4"/>
              <!-- Progress arc -->
              <circle cx="40" cy="40" r="32" fill="none"
                      :stroke="remaining < 5 ? '#f43f5e' : '#7c3aed'"
                      stroke-width="4"
                      stroke-linecap="round"
                      :stroke-dasharray="`${(signalsSent / MAX_SIGNALS) * 201} 201`"
                      stroke-dashoffset="0"
                      transform="rotate(-90 40 40)"
                      style="transition: stroke-dasharray 0.5s ease;"/>
              <text x="40" y="37" text-anchor="middle" font-size="14" font-weight="600" fill="#4c1d95" font-family="DM Sans">{{ remaining }}</text>
              <text x="40" y="50" text-anchor="middle" font-size="6" fill="#a78bfa" font-family="DM Sans">left today</text>
            </svg>
          </div>

          <!-- ── Cooldown timer ─────────────────────────────────── -->
          <Transition name="timer-fade">
            <div v-if="isCoolingDown" class="cooldown-strip">
              <div class="cooldown-bar-track">
                <div class="cooldown-bar-fill" :style="`width: ${(cooldownLeft / COOLDOWN_S) * 100}%`"></div>
              </div>
              <p class="cooldown-label">Wait {{ cooldownLeft }}s before sending another</p>
            </div>
          </Transition>

          <!-- Maxed out state -->
          <Transition name="timer-fade">
            <div v-if="signalsSent >= MAX_SIGNALS" class="maxed-notice">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              You've sent all 25 thoughts for today. See you tomorrow ✦
            </div>
          </Transition>

          <!-- ── Disclaimer ─────────────────────────────────────── -->
          <p class="signal-disclaimer">
            You can only send a max of 25 thoughts a day to your partner —<br/>
            we don't want to overwhelm them with how much you think of them 24/7.
          </p>

        </div>
      </div>
    </Sidebar>
  </InactivityOverlay>
</template>

<style scoped>
/* ── Page ────────────────────────────────────────────────────────── */
.signal-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  background: #fdf8ff;
}

/* ── Background ──────────────────────────────────────────────────── */
.signal-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(72px);
  opacity: 0.35;
}
.orb-1 {
  width: 420px; height: 420px;
  background: radial-gradient(circle, #ddd6fe, transparent);
  top: -100px; left: -80px;
  animation: drift1 18s ease-in-out infinite alternate;
}
.orb-2 {
  width: 320px; height: 320px;
  background: radial-gradient(circle, #fce7f3, transparent);
  bottom: -60px; right: -60px;
  animation: drift2 22s ease-in-out infinite alternate;
}
.orb-3 {
  width: 200px; height: 200px;
  background: radial-gradient(circle, #ede9fe, transparent);
  top: 45%; left: 55%;
  animation: drift1 14s ease-in-out infinite alternate-reverse;
}

@keyframes drift1 {
  from { transform: translate(0,0) scale(1); }
  to   { transform: translate(40px, 30px) scale(1.1); }
}
@keyframes drift2 {
  from { transform: translate(0,0) scale(1.05); }
  to   { transform: translate(-30px,-20px) scale(0.95); }
}

.signal-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* ── Content ─────────────────────────────────────────────────────── */
.signal-content {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 20vh;
  padding: 2rem 1rem;
  gap: 1.5rem;
}

/* ── Header ──────────────────────────────────────────────────────── */
.signal-header { text-align: center; }

.signal-title {
  font-family: 'DM Serif Display', Georgia, serif;
  font-size: clamp(2rem, 5vw, 2.75rem);
  color: #1e1b4b;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;
}

.signal-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: #8b5cf6;
  margin-top: 0.35rem;
  font-weight: 400;
  letter-spacing: 0.02em;
}

/* ── Scene wrapper ───────────────────────────────────────────────── */
.scene-wrapper {
  position: relative;
  width: 240px;
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.scene-wrapper:hover .person-svg {
  transform: scale(1.03);
}

.scene--disabled {
  cursor: not-allowed;
  opacity: 0.5;
  pointer-events: none;
}

/* ── Person SVG ──────────────────────────────────────────────────── */
.person-svg {
  width: 220px;
  height: 260px;
  transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
  overflow: visible;
}

/* ── Eyes ────────────────────────────────────────────────────────── */
.eyes-asleep  { transition: opacity 0.2s ease; opacity: 1; }
.eyes-awake   { transition: opacity 0.25s ease 0.15s; opacity: 0; }
.eyes--hide   { opacity: 0 !important; }
.eyes--show   { opacity: 1 !important; }

/* ── Brows ───────────────────────────────────────────────────────── */
.brows { transition: transform 0.3s ease 0.1s; transform-origin: 110px 115px; }
.brows--up { transform: translateY(-4px); }

/* ── Mouth ───────────────────────────────────────────────────────── */
.mouth { transition: d 0.3s ease; }

/* ── Z letters ───────────────────────────────────────────────────── */
.zs {
  transition: opacity 0.3s ease;
  animation: floatZs 3s ease-in-out infinite;
}
.zs--hide { opacity: 0 !important; animation: none; }

@keyframes floatZs {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-5px); }
}

/* ── Thought bubble ──────────────────────────────────────────────── */
.thought-group {
  opacity: 0;
  transform-origin: 140px 180px;
  transform: scale(0.4) translateY(10px);
  transition: opacity 0.45s cubic-bezier(0.34,1.4,0.64,1), transform 0.45s cubic-bezier(0.34,1.4,0.64,1);
}
.thought--show {
  opacity: 1 !important;
  transform: scale(1) translateY(0) !important;
}

/* Heart inside bubble pulses when visible */
.thought--show .bubble-heart {
  animation: heartBeat 0.8s ease-in-out infinite;
}
@keyframes heartBeat {
  0%,100% { transform: scale(1); }
  30%     { transform: scale(1.18); }
  60%     { transform: scale(0.95); }
}

/* ── Ripple rings ────────────────────────────────────────────────── */
.ripple-ring {
  position: absolute;
  top: 50%; left: 50%;
  width: 120px; height: 120px;
  margin-top: -60px; margin-left: -60px;
  border-radius: 50%;
  border: 1.5px solid rgba(124,58,237,0.35);
  opacity: 0;
  pointer-events: none;
}

.ripple--go {
  animation: rippleOut 1.8s ease-out forwards;
}
.ripple-2.ripple--go { animation-delay: 0.25s; }
.ripple-3.ripple--go { animation-delay: 0.5s; }

@keyframes rippleOut {
  0%   { transform: scale(0.6); opacity: 0.7; }
  100% { transform: scale(2.8); opacity: 0; }
}

/* ── Click hint ──────────────────────────────────────────────────── */
.click-hint {
  position: absolute;
  bottom: -28px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  color: #a78bfa;
  white-space: nowrap;
  animation: blink 2.5s ease-in-out infinite;
  transition: opacity 0.4s ease;
}
.hint--hide { opacity: 0 !important; }

@keyframes blink {
  0%,100% { opacity: 0.5; }
  50%     { opacity: 1; }
}

/* ── Count ring area ─────────────────────────────────────────────── */
.count-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  margin-top: 0.5rem;
}

/* ── Cooldown strip ──────────────────────────────────────────────── */
.cooldown-strip {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 200px;
}

.cooldown-bar-track {
  width: 100%;
  height: 3px;
  background: #ede9fe;
  border-radius: 4px;
  overflow: hidden;
}

.cooldown-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #7c3aed, #c084fc);
  border-radius: 4px;
  transition: width 1s linear;
}

.cooldown-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  color: #a78bfa;
  text-align: center;
}

/* ── Maxed out notice ────────────────────────────────────────────── */
.maxed-notice {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: #7c3aed;
  background: #f5f0ff;
  border: 1px solid #e9d5ff;
  border-radius: 12px;
  padding: 10px 16px;
  text-align: center;
  max-width: 280px;
  line-height: 1.5;
}

/* ── Disclaimer ──────────────────────────────────────────────────── */
.signal-disclaimer {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.72rem;
  color: #c4b5fd;
  text-align: center;
  max-width: 300px;
  line-height: 1.7;
  margin-top: 0.25rem;
}

/* ── Transitions ─────────────────────────────────────────────────── */
.timer-fade-enter-active, .timer-fade-leave-active { transition: all 0.4s ease; }
.timer-fade-enter-from, .timer-fade-leave-to       { opacity: 0; transform: translateY(-6px); }
</style>