<script setup>
import { Briefcase } from "lucide-vue-next";
import RevealBlock from "./RevealBlock.vue";
import SectionHeading from "./SectionHeading.vue";

defineProps({
  experience: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <section
    id="experience"
    class="mx-auto max-w-7xl px-6 py-20 sm:px-8"
  >
    <RevealBlock>
      <SectionHeading
        eyebrow="Experience"
        title="从课堂到产线，在真实数据中打磨工程手感"
        description="第一次进到 AI 公司做数据标注和训练工作，对数据质量、标注规范和工程流程有了实打实的认识。"
      />
    </RevealBlock>

    <div class="mt-12 grid gap-8">
      <RevealBlock>
        <article class="glass-panel h-full rounded-[2rem] p-8 sm:p-10">
          <div class="flex items-center gap-3 text-emerald-300">
            <Briefcase class="h-5 w-5" />
            <p class="text-sm uppercase tracking-[0.35em]">工作经历</p>
          </div>

          <div class="relative mt-8 pl-8">
            <div class="absolute left-3 top-0 h-full w-px bg-gradient-to-b from-emerald-300 via-emerald-400/50 to-transparent" />

            <div
              v-for="job in experience"
              :key="`${job.company}-${job.period}`"
              class="relative pb-2"
            >
              <div
                class="absolute -left-[1.82rem] top-2 h-4 w-4 rounded-full border-4 border-slate-950 bg-emerald-300 shadow-[0_0_0_6px_rgba(52,211,153,0.12)]"
              />
              <p class="text-sm uppercase tracking-[0.32em] text-emerald-300/80">
                {{ job.company }}
              </p>
              <h3 class="mt-3 text-2xl font-semibold text-white">
                {{ job.position }}
              </h3>
              <p class="mt-2 text-base text-slate-200">
                {{ job.period }}
              </p>
              <p class="mt-4 text-base leading-relaxed text-slate-400">
                {{ job.description }}
              </p>
              <ul
                v-if="job.highlights?.length"
                class="mt-4 space-y-2"
              >
                <li
                  v-for="(highlight, hIdx) in job.highlights"
                  :key="hIdx"
                  class="flex items-start gap-2 text-sm text-slate-300"
                >
                  <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400/60" />
                  {{ highlight }}
                </li>
              </ul>
            </div>
          </div>
        </article>
      </RevealBlock>
    </div>
  </section>
</template>
