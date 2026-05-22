<script setup>
import { BrainCircuit, GraduationCap, UserCheck, Award, Trophy } from "lucide-vue-next";
import RevealBlock from "./RevealBlock.vue";
import SectionHeading from "./SectionHeading.vue";

defineProps({
  personalInfo: {
    type: Object,
    required: true,
  },
  education: {
    type: Array,
    default: () => [],
  },
});

const highlightIcons = {
  position: UserCheck,
  club: Award,
  award: Trophy,
};
</script>

<template>
  <section
    id="about"
    class="mx-auto max-w-7xl px-6 py-20 sm:px-8"
  >
    <RevealBlock>
      <SectionHeading
        eyebrow="About / Education"
        title="理论根基与系统落地并重的 AI 工程型人才"
        description="我将科班训练出的算法理解力，与真实业务中的系统设计、稳定性治理和产品化意识结合在一起，专注把 AI 能力变成真正可交付、可维护、可扩展的解决方案。"
      />
    </RevealBlock>

    <div class="mt-12 grid gap-8 lg:grid-cols-2">
      <RevealBlock>
        <article class="glass-panel h-full rounded-[2rem] p-8 sm:p-10">
          <div class="flex items-center gap-3 text-cyan-300">
            <BrainCircuit class="h-5 w-5" />
            <p class="text-sm uppercase tracking-[0.35em]">关于我</p>
          </div>
          <p class="mt-6 text-lg leading-relaxed text-slate-300">
            做的项目多了慢慢发现，一个 AI 项目能不能成，模型效果只是一部分。工作流设计、系统约束、接口协同、业务价值验证——这些工程层面的东西往往才是决定因素。所以不管做 Agent 还是做应用，我都习惯先从「能不能落地」的角度去拆问题、定方案、推实现。
          </p>
          <p class="mt-6 text-base leading-relaxed text-slate-400">
            {{ personalInfo.summary }}
          </p>
        </article>
      </RevealBlock>

      <RevealBlock>
        <article
          id="education"
          class="glass-panel h-full rounded-[2rem] p-8 sm:p-10"
        >
          <div class="flex items-center gap-3 text-emerald-300">
            <GraduationCap class="h-5 w-5" />
            <p class="text-sm uppercase tracking-[0.35em]">教育时间轴</p>
          </div>

          <div class="relative mt-8 pl-8">
            <div class="absolute left-3 top-0 h-full w-px bg-gradient-to-b from-cyan-300 via-cyan-400/50 to-transparent" />

            <div
              v-for="item in education"
              :key="`${item.institution}-${item.major}`"
              class="relative pb-2"
            >
              <div
                class="absolute -left-[1.82rem] top-2 h-4 w-4 rounded-full border-4 border-slate-950 bg-cyan-300 shadow-[0_0_0_6px_rgba(34,211,238,0.12)]"
              />
              <p class="text-sm uppercase tracking-[0.32em] text-cyan-300/80">
                Bachelor Track
              </p>
              <h3 class="mt-3 text-2xl font-semibold text-white">
                {{ item.institution }}
              </h3>
              <p class="mt-2 text-base text-slate-200">
                {{ item.degree }} · {{ item.major }}
              </p>
              <p class="mt-2 text-sm text-slate-400">
                {{ item.period }}
              </p>
              <p class="mt-4 text-base leading-relaxed text-slate-400">
                {{ item.description }}
              </p>

              <div
                v-if="item.coreCourses?.length"
                class="mt-5 flex flex-wrap gap-2"
              >
                <span
                  v-for="course in item.coreCourses"
                  :key="course"
                  class="rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-xs text-slate-300"
                >
                  {{ course }}
                </span>
              </div>

              <div
                v-if="item.highlights?.length"
                class="mt-5 grid gap-3"
              >
                <div
                  v-for="(h, hIdx) in item.highlights"
                  :key="hIdx"
                  class="flex items-start gap-3 rounded-xl border border-white/5 bg-white/[0.03] p-3"
                >
                  <component
                    :is="highlightIcons[h.type]"
                    class="mt-0.5 h-4 w-4 shrink-0 text-emerald-300"
                  />
                  <div>
                    <p class="text-sm font-medium text-white/90">{{ h.title }}</p>
                    <p class="mt-0.5 text-xs text-slate-400">{{ h.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </article>
      </RevealBlock>
    </div>
  </section>
</template>
