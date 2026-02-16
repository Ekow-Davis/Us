<template>
  <div class="min-h-screen bg-white">
    <!-- Header / Navbar -->
    <header class="border-b border-gray-200">
      <nav class="max-w-7xl mx-auto px-8 py-6 flex items-center justify-between">
        <div class="text-2xl font-bold text-purple-700">datingnow</div>
        <div class="flex items-center gap-8">
          <a href="#" class="text-gray-700 hover:text-purple-700 transition-colors font-medium">Home</a>
          <a href="#" class="text-gray-700 hover:text-purple-700 transition-colors font-medium">Contact</a>
          <a href="#" class="text-gray-700 hover:text-purple-700 transition-colors font-medium">About</a>
          <a href="#" class="text-gray-700 hover:text-purple-700 transition-colors font-medium">Reviews</a>
          <a href="#" class="text-purple-700 font-semibold">Log In</a>
          <a href="#" class="bg-purple-700 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-800 transition">Sign Up</a>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-purple-50">
      <div class="max-w-7xl mx-auto px-8 py-16 lg:py-20 relative grid lg:grid-cols-2 gap-12 items-center">
        
        <!-- LEFT: TEXT -->
        <div class="space-y-6 z-10">
          <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
            Dating For you
          </h1>
          <p class="text-lg text-gray-600 leading-relaxed max-w-xl">
            Dating is a stage of romantic relationships in humans whereby two
            people meet socially with the aim of each assessing the other's
            suitability as a prospective partner in an intimate relationship.
            It is a form of courtship, consisting of social activities done by
            the couple, either alone or with others.
          </p>
          <button
            class="bg-purple-700 hover:bg-purple-800 text-white font-semibold px-8 py-3 rounded-lg transition shadow-md hover:shadow-lg"
          >
            Find Now
          </button>
        </div>

        <!-- RIGHT: CURVED IMAGE SHAPE -->
<div class="relative h-[700px] lg:h-[800px] flex items-center justify-end -ml-40 -mr-40 w-[150%]">

  <svg
    viewBox="0 0 1200 900"
    preserveAspectRatio="none"
    class="absolute right-0 top-0 h-full w-full"
  >
    <defs>
      <clipPath id="waveClip">
        <path
          d="M100,0 
             Q420,180 350,450 
             Q300,700 420,900 
             L1200,900 
             L1200,0 
             Z"
        />
      </clipPath>
    </defs>

    <!-- Purple wave extended MUCH further -->
    <path
      d="M100,0 
         Q420,180 350,450 
         Q300,700 420,900 
         L1200,900 
         L1200,0 
         Z"
      fill="#6D28D9"
    />
  </svg>

  <!-- Bigger image canvas -->
  <img
    src="/images/homepage_image.jpg"
    alt="Dating couple illustration"
    class="absolute right-0 top-0 h-full w-full object-cover object-[8%_bottom]"
    style="clip-path: url(#waveClip);"
  />

</div>



      </div>
    </section>
  </div>
</template>
<script setup>
// Vue 3 Composition API setup
// No additional logic needed for this static page
</script>

<style scoped>
/* Wave container styling */
.wave-container {
  position: relative;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .wave-container {
    margin-top: 2rem;
  }
}

/* Ensure smooth rendering */

</style>