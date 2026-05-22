<script setup>
import { Award, BadgeCheck, ScrollText } from "lucide-vue-next";
import RevealBlock from "./RevealBlock.vue";
import SectionHeading from "./SectionHeading.vue";

defineProps({
  practiceData: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <section
    id="practice"
    class="mx-auto max-w-7xl px-6 py-20 sm:px-8"
  >
    <RevealBlock>
      <SectionHeading
        eyebrow="Practice / Certification"
        title="算法训练、工程认证与持续进阶"
        description="一边用算法实践打磨对模型的理解，一边系统化补全了大模型应用、提示工程、RAG 这些关键能力的认证。"
      />
    </RevealBlock>

    <div class="mt-12 grid gap-6">
      <!-- Algorithm Practice -->
      <RevealBlock>
        <article class="glass-panel overflow-hidden rounded-[2rem] p-8">
          <div class="flex items-center gap-3 text-emerald-300">
            <ScrollText class="h-5 w-5" />
            <h3 class="text-xl font-semibold text-white">算法实践</h3>
          </div>

          <div class="-mx-2 mt-8 flex snap-x gap-4 overflow-x-auto px-2 pb-3">
            <div
              v-for="item in practiceData.algorithm"
              :key="item"
              class="min-w-[18rem] snap-start rounded-[1.75rem] border border-white/10 bg-gradient-to-br from-emerald-400/10 via-slate-900/80 to-cyan-400/10 p-6 transition duration-300 hover:-translate-y-1 hover:border-emerald-300/40"
            >
              <p class="text-xs uppercase tracking-[0.32em] text-slate-400">
                Algorithm
              </p>
              <p class="mt-4 text-lg leading-relaxed text-white">
                {{ item }}
              </p>
            </div>
          </div>
        </article>
      </RevealBlock>

      <!-- iFlytek Certifications -->
      <RevealBlock>
        <article class="glass-panel overflow-hidden rounded-[2rem] p-8">
          <div class="flex items-center gap-3 text-cyan-300">
            <BadgeCheck class="h-5 w-5" />
            <h3 class="text-xl font-semibold text-white">科大讯飞认证</h3>
          </div>

          <div class="-mx-2 mt-8 flex snap-x gap-4 overflow-x-auto px-2 pb-3">
            <div
              v-for="item in practiceData.certifications"
              :key="item"
              class="min-w-[18rem] snap-start rounded-[1.75rem] border border-white/10 bg-gradient-to-br from-cyan-400/10 via-slate-900/80 to-emerald-400/10 p-6 transition duration-300 hover:-translate-y-1 hover:border-cyan-300/40"
            >
              <p class="text-xs uppercase tracking-[0.32em] text-slate-400">
                iFlytek
              </p>
              <p class="mt-4 text-lg leading-relaxed text-white">
                {{ item }}
              </p>
            </div>
          </div>
        </article>
      </RevealBlock>

      <!-- Other Certifications -->
      <RevealBlock>
        <article class="glass-panel overflow-hidden rounded-[2rem] p-8">
          <div class="flex items-center gap-3 text-violet-300">
            <Award class="h-5 w-5" />
            <h3 class="text-xl font-semibold text-white">其他认证</h3>
          </div>

          <div class="-mx-2 mt-8 flex snap-x gap-4 overflow-x-auto px-2 pb-3">
            <div
              v-for="item in practiceData.other_certifications"
              :key="item"
              class="min-w-[18rem] snap-start rounded-[1.75rem] border border-white/10 bg-gradient-to-br from-violet-400/10 via-slate-900/80 to-pink-400/10 p-6 transition duration-300 hover:-translate-y-1 hover:border-violet-300/40"
            >
              <p class="text-xs uppercase tracking-[0.32em] text-slate-400">
                Other
              </p>
              <p class="mt-4 text-lg leading-relaxed text-white">
                {{ item }}
              </p>
            </div>
          </div>
        </article>
      </RevealBlock>
    </div>
  </section>
</template>
