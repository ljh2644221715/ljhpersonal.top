<script setup>
import { Blocks, Bot, CodeXml, Cpu, Wrench } from "lucide-vue-next";
import RevealBlock from "./RevealBlock.vue";
import SectionHeading from "./SectionHeading.vue";

defineProps({
  skills: {
    type: Object,
    required: true,
  },
});

const iconMap = {
  AI_Intelligence: Bot,
  FullStack_Development: CodeXml,
  System_Architecture: Cpu,
  Tools_Platforms: Wrench,
};

const labels = {
  AI_Intelligence: "AI / 大模型应用",
  FullStack_Development: "全栈编程",
  System_Architecture: "系统工程架构",
  Tools_Platforms: "工具与平台",
};
</script>

<template>
  <section
    id="skills"
    class="mx-auto max-w-7xl px-6 py-20 sm:px-8"
  >
    <RevealBlock>
      <SectionHeading
        eyebrow="Skills Matrix"
        title="从模型到落地的全链路能力"
        description="技能是按做产品落地的真实链路排的——理解模型、写应用、搭系统、用工具，缺哪个环节都跑不通。"
      />
    </RevealBlock>

    <div class="mt-12 grid gap-6 lg:grid-cols-4">
      <RevealBlock
        v-for="(items, key, index) in skills"
        :key="key"
      >
        <article
          class="glass-panel h-full rounded-[2rem] p-8 transition duration-300 hover:-translate-y-1 hover:border-cyan-400/30"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3 text-cyan-300">
              <component
                :is="iconMap[key] || Blocks"
                class="h-5 w-5"
              />
              <h3 class="text-xl font-semibold text-white">
                {{ labels[key] }}
              </h3>
            </div>
            <span class="text-xs uppercase tracking-[0.3em] text-slate-500">
              0{{ index + 1 }}
            </span>
          </div>

          <div class="mt-8 flex flex-wrap gap-3">
            <span
              v-for="item in items"
              :key="item"
              class="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-200 transition duration-300 hover:scale-105 hover:border-cyan-300/60 hover:text-cyan-100"
            >
              {{ item }}
            </span>
          </div>
        </article>
      </RevealBlock>
    </div>
  </section>
</template>
