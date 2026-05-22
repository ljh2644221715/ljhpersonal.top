<script setup>
import { ref } from "vue";
import { Menu, X } from "lucide-vue-next";

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
});

const mobileMenuOpen = ref(false);

function toggleMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
}

function closeMenu() {
  mobileMenuOpen.value = false;
}
</script>

<template>
  <header class="fixed top-0 z-50 w-full px-4 py-4 sm:px-6">
    <nav
      class="mx-auto flex max-w-7xl items-center justify-between rounded-full border border-white/10 bg-slate-900/60 px-5 py-3 backdrop-blur-md sm:px-7"
    >
      <a
        href="#hero"
        class="text-sm font-semibold uppercase tracking-[0.45em] text-cyan-300 transition duration-300 hover:text-cyan-200"
      >
        JH.AI
      </a>

      <div class="hidden items-center gap-6 md:flex">
        <a
          v-for="item in items"
          :key="item.href"
          :href="item.href"
          class="text-sm text-slate-300 transition duration-300 hover:text-white"
        >
          {{ item.label }}
        </a>
      </div>

      <div class="flex items-center gap-3">
        <a
          href="#projects"
          class="hidden rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-xs font-medium text-cyan-200 transition duration-300 hover:scale-105 hover:border-cyan-300 hover:bg-cyan-400/20 sm:inline-block"
        >
          Explore
        </a>

        <button
          class="inline-flex items-center justify-center rounded-full border border-white/15 bg-white/5 p-2 text-slate-200 transition duration-300 hover:border-cyan-300/60 hover:text-cyan-200 md:hidden"
          @click="toggleMenu"
          aria-label="Toggle menu"
        >
          <Menu v-if="!mobileMenuOpen" class="h-5 w-5" />
          <X v-else class="h-5 w-5" />
        </button>
      </div>
    </nav>

    <!-- Mobile menu overlay -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-2 opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        class="mt-3 overflow-hidden rounded-2xl border border-white/10 bg-slate-900/95 backdrop-blur-xl md:hidden"
      >
        <div class="flex flex-col gap-1 p-3">
          <a
            v-for="item in items"
            :key="item.href"
            :href="item.href"
            class="rounded-xl px-4 py-3 text-sm text-slate-300 transition duration-200 hover:bg-white/5 hover:text-white"
            @click="closeMenu"
          >
            {{ item.label }}
          </a>
        </div>
      </div>
    </Transition>
  </header>
</template>
