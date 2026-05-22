<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const isVisible = ref(false);
const root = ref(null);

let observer;

onMounted(() => {
  observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true;
        observer.disconnect();
      }
    },
    { threshold: 0.18 }
  );

  if (root.value) {
    observer.observe(root.value);
  }
});

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<template>
  <div
    ref="root"
    :class="[
      'transition-all duration-700 ease-out will-change-transform',
      isVisible ? 'translate-y-0 opacity-100' : 'translate-y-5 opacity-0',
    ]"
  >
    <slot />
  </div>
</template>
