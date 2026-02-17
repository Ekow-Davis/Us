<template>
  <div v-if="visible" class="overlay">
    <div class="close-btn" @click="closeEarly">✕</div>

    <div class="ground">
      <div
        v-for="n in signalCount"
        :key="n"
        class="flower-container"
        :class="{ 'animate': isAnimating }"
      >
        <div class="flower-top">
          <div v-for="i in 8" :key="`petal-${i}`" :class="`flower-petal flower-petal__${i}`"></div>
          <div class="flower-circle"></div>
          <div v-for="i in 8" :key="`light-${i}`" :class="`flower-light flower-light__${i}`"></div>
        </div>
        <div class="flower-bottom">
          <div class="flower-stem"></div>
          <div v-for="i in 6" :key="`leaf-${i}`" :class="`flower-leaf flower-leaf__${i}`"></div>
          <div v-for="i in 4" :key="`grass-${i}`" :class="`flower-grass flower-grass__${i}`"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const props = defineProps({
  signalCount: {
    type: Number,
    required: true,
    default: 0
  }
})

const visible = ref(true)
const isAnimating = ref(false)

const closeEarly = () => {
  visible.value = false
}

onMounted(async () => {
  // Simulate API delay
  setTimeout(() => {
    console.log(`Signal count received: ${props.signalCount}`)
    console.log(`Rendering ${props.signalCount} flowers`)
  }, 1500)

  // Start animation after a brief delay
  setTimeout(() => {
    isAnimating.value = true
  }, 100)
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: linear-gradient(to bottom, #060825 0%, #000 50%);
  z-index: 9999;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  cursor: pointer;
  z-index: 10000;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.ground {
  width: 100vmin;
  aspect-ratio: 1.5;
  overflow: visible;
  position: relative;
  transform-origin: center center;
  transform: scale(2);
  animation: shrink 1.5s ease-in forwards 4s;
}

.flower-container {
  position: absolute;
  width: 10%;
  aspect-ratio: 16;
  container-type: inline-size;
  filter: drop-shadow(0 0 25cqi #ffd85faa);
  justify-items: center;
  align-content: center;
  transform-origin: bottom center;
}

/* Predefined positions for the first 10 flowers */
.flower-container:nth-child(1) {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10%;
}

.flower-container:nth-child(2) {
  top: 45%;
  left: 30%;
  width: 8%;
}

.flower-container:nth-child(3) {
  top: 45%;
  left: 70%;
  width: 8%;
}

.flower-container:nth-child(4) {
  top: 85%;
  left: 95%;
  width: 20%;
}

.flower-container:nth-child(5) {
  top: 130%;
  left: 30%;
  width: 30%;
}

.flower-container:nth-child(6) {
  top: 60%;
  left: 10%;
  width: 12%;
}

.flower-container:nth-child(7) {
  top: 20%;
  left: 15%;
  width: 6%;
}

.flower-container:nth-child(8) {
  top: 15%;
  left: 35%;
  width: 5%;
}

.flower-container:nth-child(9) {
  top: 26%;
  left: 85%;
  width: 7%;
}

.flower-container:nth-child(10) {
  top: 22%;
  left: 60%;
  width: 6.5%;
}

.flower-top {
  width: 50cqi;
  aspect-ratio: 1.5;
  position: relative;
  z-index: 1;
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translate(-50%, 50%);
}

.flower-circle {
  width: 30cqi;
  aspect-ratio: 1.5;
  border-radius: 50%;
  background-color: #ffe4a0;
  box-shadow: inset 0px -3cqi 3cqi #aa7a0266;
  position: absolute;
  scale: 0;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 100% 100% 100% 100%/90% 90% 90% 90%;
  filter: drop-shadow(0 0 15cqi #ffd85f);
  transform-origin: top left;
}

.flower-petal {
  width: 80%;
  aspect-ratio: 1;
  background-color: #ffe4a0;
  background-image: linear-gradient(135deg, #ff6236 20%, #ffd85f 80%);
  position: absolute;
  opacity: 0;
}

.flower-petal__1 {
  bottom: 42%;
  right: 65%;
  border-radius: 0px 100% 5% 100%/0px 100% 5% 100%;
  transform: rotate(-10deg) scale(0.82);
}

.flower-petal__2 {
  bottom: 42%;
  left: 65%;
  border-radius: 0px 100% 5% 100%/0px 100% 5% 100%;
  transform: rotate(100deg) scale(0.82);
}

.flower-petal__3 {
  bottom: 40%;
  left: 10%;
  border-radius: 0px 100% 50% 100%/0px 100% 50% 100%;
  transform: rotate(45deg) scale(0.8);
}

.flower-petal__4 {
  top: -10%;
  left: 80%;
  border-radius: 0px 100% 0% 100%/0px 100% 0% 100%;
  transform: rotate(135deg) scale(0.9);
}

.flower-petal__5 {
  top: -10%;
  right: 70%;
  border-radius: 0px 100% 0% 100%/0px 100% 0% 100%;
  transform: rotate(315deg) scale(0.9);
}

.flower-petal__6 {
  top: 50%;
  right: 65%;
  border-radius: 0px 100% 10% 100%/0px 100% 5% 100%;
  transform: rotate(270deg) scale(1.1);
}

.flower-petal__7 {
  top: 50%;
  left: 65%;
  border-radius: 0px 100% 10% 100%/0px 100% 5% 100%;
  transform: rotate(180deg) scale(1.1);
}

.flower-petal__8 {
  top: 50%;
  left: 10%;
  border-radius: 0px 100% 50% 100%/0px 100% 30% 100%;
  transform: rotate(225deg) scale(1);
}

.flower-light {
  width: 3cqi;
  aspect-ratio: 1;
  position: absolute;
  border-radius: 50%;
  opacity: 0;
}

.flower-light:nth-child(odd) {
  background-color: #ffe4a0;
  filter: blur(2cqi) drop-shadow(0 0 5cqi #ffd85f);
}

.flower-light:nth-child(even) {
  background-color: #ff6236;
  filter: blur(2cqi) drop-shadow(0 0 5cqi #ff6236);
}

.flower-light__1 {
  top: 10%;
  left: 20%;
  scale: 0.8;
}

.flower-light__2 {
  top: 20%;
  left: 80%;
  scale: 1.2;
}

.flower-light__3 {
  top: 30%;
  left: 50%;
  scale: 1.5;
}

.flower-light__4 {
  top: 40%;
  left: 10%;
}

.flower-light__5 {
  top: 50%;
  left: 90%;
  scale: 2;
}

.flower-light__6 {
  top: 60%;
  left: 30%;
}

.flower-light__7 {
  top: 70%;
  left: 40%;
  scale: 0.5;
}

.flower-light__8 {
  top: 60%;
  left: 60%;
}

.flower-bottom {
  width: 6%;
  aspect-ratio: 0.02;
  left: 47%;
  top: 50%;
}

.flower-stem {
  width: 100%;
  height: 100%;
  transform: scaleY(0);
  background-image: linear-gradient(to left, rgba(0, 0, 0, 0.2), transparent, rgba(87, 42, 25, 0.2)),
    linear-gradient(to top, transparent 10%, #da580099, #da580099);
  border-radius: 50px 50px 0 0;
  transform-origin: bottom center;
}

.flower-leaf {
  width: 40%;
  aspect-ratio: 2.5;
  position: absolute;
  scale: 0;
  opacity: 0;
}

.flower-leaf:nth-child(even) {
  right: 55%;
  background-image: linear-gradient(120deg, #d86100aa 0%, #da580000 90%);
  border-radius: 0% 100% 0% 100%/0% 100% 0% 100%;
  transform-origin: bottom right;
}

.flower-leaf:nth-child(odd) {
  left: 55%;
  background-image: linear-gradient(300deg, #d86100aa 0%, #da580000 90%);
  border-radius: 100% 0% 100% 0%/100% 0% 100% 0%;
  transform-origin: bottom left;
}

.flower-leaf__2 {
  top: 25%;
  transform: rotate(-15deg) scale(1);
}

.flower-leaf__1 {
  top: 31%;
  transform: rotate(15deg) scale(1);
}

.flower-leaf__4 {
  top: 37%;
  transform: rotate(-15deg) scale(1.2);
}

.flower-leaf__3 {
  top: 43%;
  transform: rotate(15deg) scale(1.2);
}

.flower-leaf__6 {
  top: 50%;
  transform: rotate(-15deg) scale(1.5);
}

.flower-leaf__5 {
  top: 56%;
  transform: rotate(15deg) scale(1.5);
}

.flower-grass {
  position: absolute;
  bottom: -20cqi;
  width: 80cqi;
  height: 120cqi;
  opacity: 0;
  scale: 0;
  mask-image: linear-gradient(to top, transparent 15%, #fff 50%);
}

.flower-grass:nth-child(odd) {
  right: 55%;
  border-top-right-radius: 100%;
  border-right: 5cqi solid #d86100aa;
  transform-origin: bottom right;
}

.flower-grass:nth-child(even) {
  left: 55%;
  border-top-left-radius: 100%;
  border-left: 5cqi solid #d86100aa;
  transform-origin: bottom left;
}

.flower-grass__3 {
  left: 70% !important;
  width: 75cqi;
  height: 100cqi;
}

.flower-grass__4 {
  right: 70% !important;
  width: 75cqi;
  height: 90cqi;
}

/* ANIMATIONS */
.animate.flower-container {
  animation: flower-rotate 12s linear infinite;
}

.animate .flower-circle {
  animation: grass-grow 0.25s ease-in forwards 3s;
}

.animate .flower-petal {
  animation: petal-grow 0.5s ease-in forwards, flower-rotate 3s linear infinite;
}

.animate .flower-petal__3 {
  animation-delay: 3.2s;
}

.animate .flower-petal__2 {
  animation-delay: 3.3s;
}

.animate .flower-petal__4 {
  animation-delay: 3.4s;
}

.animate .flower-petal__7 {
  animation-delay: 3.5s;
}

.animate .flower-petal__8 {
  animation-delay: 3.6s;
}

.animate .flower-petal__6 {
  animation-delay: 3.7s;
}

.animate .flower-petal__5 {
  animation-delay: 3.8s;
}

.animate .flower-petal__1 {
  animation-delay: 3.9s;
}

.animate .flower-stem {
  animation: stem-grow 3s ease-in forwards;
}

.animate .flower-grass {
  animation: grass-grow 1s ease-in forwards 1.5s, flower-rotate 6s linear infinite;
}

.animate .flower-leaf {
  animation: grass-grow 0.75s ease-in forwards, flower-rotate 6s linear infinite;
}

.animate .flower-leaf__2 {
  animation-delay: 2s;
}

.animate .flower-leaf__1 {
  animation-delay: 1.9s;
}

.animate .flower-leaf__4 {
  animation-delay: 1.8s;
}

.animate .flower-leaf__3 {
  animation-delay: 1.65s;
}

.animate .flower-leaf__6 {
  animation-delay: 1.5s;
}

.animate .flower-leaf__5 {
  animation-delay: 1.25s;
}

.animate .flower-light {
  animation: light-float 5s ease-in-out infinite;
}

.animate .flower-light__1 {
  animation-delay: 4.7s;
}

.animate .flower-light__2 {
  animation-delay: 5.2s;
}

.animate .flower-light__3 {
  animation-delay: 5.7s;
}

.animate .flower-light__4 {
  animation-delay: 6.2s;
}

.animate .flower-light__5 {
  animation-delay: 6.7s;
}

.animate .flower-light__6 {
  animation-delay: 7.2s;
}

.animate .flower-light__7 {
  animation-delay: 7.7s;
}

.animate .flower-light__8 {
  animation-delay: 8.2s;
}

@keyframes petal-grow {
  0% {
    scale: 0;
    opacity: 0.8;
  }
  50% {
    scale: 1;
    opacity: 0.8;
  }
  75% {
    scale: 1.1;
    opacity: 0.8;
  }
  90% {
    scale: 0.9;
    opacity: 0.8;
  }
  100% {
    scale: 1;
    opacity: 0.8;
  }
}

@keyframes grass-grow {
  100% {
    opacity: 1;
    scale: 1;
  }
}

@keyframes stem-grow {
  0% {
    border-radius: 10%;
  }
  100% {
    transform: scaleY(1);
  }
}

@keyframes flower-rotate {
  0%,
  100% {
    rotate: 0deg;
  }
  25% {
    rotate: 5deg;
  }
  75% {
    rotate: -5deg;
  }
}

@keyframes shrink {
  100% {
    transform: scale(1);
  }
}

@keyframes light-float {
  0% {
    opacity: 0;
    transform: translate(0, 0);
  }
  25% {
    opacity: 1;
    transform: translate(20cqi, -25cqi);
  }
  50% {
    opacity: 1;
    transform: translate(0, -50cqi);
  }
  75% {
    opacity: 1;
    transform: translate(-20cqi, -75cqi);
  }
  100% {
    opacity: 0;
    transform: translate(0, -100cqi);
  }
}
</style>