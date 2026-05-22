<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import {
  ArrowDownRight,
  Download,
  Mail,
  MapPin,
  Sparkles,
} from "lucide-vue-next";

const props = defineProps({
  personalInfo: {
    type: Object,
    required: true,
  },
  metrics: {
    type: Array,
    default: () => [],
  },
});

const roleOptions = ["AI 智能体开发者", "智能系统架构师", "算法工程师"];
const typedText = ref("");
const roleIndex = ref(0);
const charIndex = ref(0);
const isDeleting = ref(false);

const currentRole = computed(() => roleOptions[roleIndex.value]);
const emailChars = [
  108, 106, 104, 50, 50, 48, 56, 49, 53, 64, 49, 54, 51, 46, 99, 111, 109,
];
const protectedEmail = computed(() => String.fromCharCode(...emailChars));
const contactHref = computed(
  () =>
    `mailto:${protectedEmail.value}?subject=${encodeURIComponent("联系李建华")}`
);

let timer;

function loopTyping() {
  const target = currentRole.value;
  const speed = isDeleting.value ? 55 : 110;

  if (!isDeleting.value) {
    typedText.value = target.slice(0, charIndex.value + 1);
    charIndex.value += 1;

    if (typedText.value === target) {
      timer = window.setTimeout(() => {
        isDeleting.value = true;
        loopTyping();
      }, 1400);
      return;
    }
  } else {
    typedText.value = target.slice(0, Math.max(charIndex.value - 1, 0));
    charIndex.value -= 1;

    if (charIndex.value === 0) {
      isDeleting.value = false;
      roleIndex.value = (roleIndex.value + 1) % roleOptions.length;
    }
  }

  timer = window.setTimeout(loopTyping, speed);
}

onMounted(() => {
  loopTyping();
});

onBeforeUnmount(() => {
  window.clearTimeout(timer);
});
</script>

<template>
  <section
    id="hero"
    class="mx-auto grid min-h-[calc(100vh-5rem)] max-w-7xl gap-14 px-6 pb-24 pt-14 sm:px-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center"
  >
    <div>
      <div
        class="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 shadow-soft backdrop-blur-md"
      >
        <Sparkles class="h-4 w-4 text-cyan-300" />
        <span>{{ personalInfo.status }}</span>
      </div>

      <h1
        class="mt-8 text-5xl font-semibold tracking-[-0.05em] text-white sm:text-6xl lg:text-7xl"
      >
        {{ personalInfo.name }}
      </h1>

      <div class="mt-5 min-h-[3.5rem] text-2xl font-medium text-slate-200 sm:text-3xl">
        <span class="text-cyan-300">{{ typedText }}</span>
        <span class="ml-1 inline-block h-8 w-px animate-pulse bg-cyan-200 align-middle" />
      </div>

      <p class="mt-8 max-w-3xl text-lg leading-relaxed text-slate-300">
        {{ personalInfo.summary }}
      </p>

      <div class="mt-8 flex flex-wrap items-center gap-3">
        <span
          v-for="item in personalInfo.coreDirection"
          :key="item"
          class="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-100"
        >
          {{ item }}
        </span>
      </div>

      <div class="mt-10 flex flex-wrap gap-4">
        <a
          href="#projects"
          class="inline-flex items-center gap-2 rounded-full bg-cyan-400 px-6 py-3 text-sm font-semibold text-slate-950 transition duration-300 hover:scale-105 hover:bg-cyan-300"
        >
          探索项目集
          <ArrowDownRight class="h-4 w-4" />
        </a>
        <a
          href="/李建华-完整简历.md"
          download
          class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-6 py-3 text-sm font-semibold text-slate-100 transition duration-300 hover:scale-105 hover:border-cyan-300/60 hover:bg-white/10"
        >
          下载完整简历
          <Download class="h-4 w-4" />
        </a>
      </div>
    </div>

    <div class="relative">
      <div
        class="glass-panel relative overflow-hidden rounded-[2rem] p-8 shadow-glow sm:p-10"
      >
        <div
          class="absolute inset-x-8 top-0 h-px animate-pulse-line bg-gradient-to-r from-transparent via-cyan-300/80 to-transparent"
        />
        <div class="flex items-center justify-between">
          <p class="text-sm uppercase tracking-[0.35em] text-slate-400">
            Profile Snapshot
          </p>
          <div class="flex items-center gap-2 text-sm text-slate-300">
            <MapPin class="h-4 w-4 text-emerald-300" />
            <span>{{ personalInfo.location }}</span>
          </div>
        </div>

        <div class="mt-8 grid gap-5">
          <article
            v-for="metric in metrics"
            :key="metric.label"
            class="rounded-3xl border border-white/8 bg-white/[0.03] p-5 transition duration-300 hover:scale-[1.02] hover:border-cyan-400/30"
          >
            <p class="text-3xl font-semibold tracking-tight text-white">
              {{ metric.value }}
            </p>
            <p class="mt-2 text-sm uppercase tracking-[0.3em] text-cyan-300/90">
              {{ metric.label }}
            </p>
            <p class="mt-3 text-sm leading-relaxed text-slate-400">
              {{ metric.detail }}
            </p>
          </article>
        </div>

        <div class="mt-6 rounded-3xl border border-emerald-300/15 bg-emerald-400/[0.05] p-5">
          <div class="flex items-center gap-3 text-emerald-300">
            <Mail class="h-4 w-4" />
            <p class="text-sm uppercase tracking-[0.3em]">联系我</p>
          </div>
          <p class="mt-3 text-sm leading-relaxed text-slate-300">
            想聊 AI 智能体、算法或者项目合作？发个邮件就行，看到就会回。
          </p>
          <div class="mt-4 flex flex-wrap items-center gap-3">
            <a
              :href="contactHref"
              class="inline-flex items-center gap-2 rounded-full border border-emerald-300/20 bg-emerald-400/10 px-4 py-2 text-sm font-medium text-emerald-100 transition duration-300 hover:scale-105 hover:border-emerald-200/50 hover:bg-emerald-400/20"
            >
              发送邮件
              <ArrowDownRight class="h-4 w-4" />
            </a>
            <span class="text-xs uppercase tracking-[0.24em] text-slate-500">
              邮箱地址已做前端动态拼接保护
            </span>
          </div>
        </div>
      </div>

      <div
        class="pointer-events-none absolute -right-4 top-10 hidden h-28 w-28 rounded-full border border-cyan-300/20 bg-cyan-400/10 blur-sm lg:block"
      />
      <div
        class="pointer-events-none absolute -bottom-3 left-3 hidden h-20 w-20 animate-float rounded-full border border-emerald-300/20 bg-emerald-400/10 blur-sm lg:block"
      />
    </div>
  </section>
</template>
