<script setup>
defineProps({
  eyebrow: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    default: "",
  },
  description: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div class="max-w-3xl">
    <p class="mb-4 text-sm uppercase tracking-[0.35em] text-cyan-300/80">
      {{ eyebrow }}
    </p>
    <h2 class="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
      {{ title }}
    </h2>
    <p class="mt-4 text-base leading-relaxed text-slate-300 sm:text-lg">
      {{ description }}
    </p>
  </div>
</template>
