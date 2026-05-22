<script setup>
import { ref, computed } from "vue";
import { ArrowUpRight, Layers3, Clock, CheckCircle, ExternalLink } from "lucide-vue-next";
import RevealBlock from "./RevealBlock.vue";
import SectionHeading from "./SectionHeading.vue";

const props = defineProps({
  projects: {
    type: Array,
    default: () => [],
  },
});

const activeFilter = ref("全部");

const filterTabs = ["全部", "AI 应用", "全栈系统", "创业项目"];

const filteredProjects = computed(() => {
  if (activeFilter.value === "全部") return props.projects;
  return props.projects.filter((p) =>
    p.type.includes(activeFilter.value),
  );
});

const featuredIndexes = computed(() => {
  const indexes = new Set();
  let count = 0;
  filteredProjects.value.forEach((p, i) => {
    if (p.featured && count < 3) {
      indexes.add(i);
      count++;
    }
  });
  return indexes;
});
</script>

<template>
  <section
    id="projects"
    class="mx-auto max-w-7xl px-6 py-20 sm:px-8"
  >
    <RevealBlock>
      <SectionHeading
        eyebrow="Projects Gallery"
        title="从 AI Agent 到全栈系统，每个项目解决一个真问题"
        description="项目背景各有不同，但始终围绕「痛点→方案→落地」这条线展开。有折腾技术的，也有折腾产品的，都是实打实干出来的。"
      />
    </RevealBlock>

    <!-- Filter Tabs -->
    <div class="mt-10 flex flex-wrap gap-3">
      <button
        v-for="tab in filterTabs"
        :key="tab"
        @click="activeFilter = tab"
        :class="[
          'rounded-full border px-5 py-2 text-sm font-medium transition-all duration-300',
          activeFilter === tab
            ? 'border-cyan-400/30 bg-cyan-500/15 text-cyan-200 shadow-[0_0_15px_-3px_rgba(34,211,238,0.15)]'
            : 'border-white/10 bg-white/5 text-slate-400 hover:border-white/20 hover:text-slate-200',
        ]"
      >
        {{ tab }}
      </button>
    </div>

    <!-- Project Grid -->
    <div
      class="mt-10 grid auto-rows-[minmax(18rem,_1fr)] gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
    >
      <RevealBlock
        v-for="(project, index) in filteredProjects"
        :key="project.name"
      >
        <article
          :class="[
            'group glass-panel flex h-full flex-col rounded-[2rem] p-8 transition duration-300 hover:-translate-y-2 hover:border-cyan-400/30 hover:shadow-glow',
            featuredIndexes.has(index)
              ? 'lg:col-span-2 lg:row-span-1'
              : '',
          ]"
        >
          <!-- Top section: type badge + period and status -->
          <div class="flex items-start justify-between gap-4">
            <p class="text-sm uppercase tracking-[0.28em] text-cyan-300/80">
              {{ project.type }}
            </p>
            <div class="flex shrink-0 items-center gap-3 text-sm text-slate-400">
              <div class="flex items-center gap-1.5">
                <Clock class="h-3.5 w-3.5 text-emerald-300" />
                <span>{{ project.period }}</span>
              </div>
              <span
                v-if="project.status === 'ongoing'"
                class="relative flex h-2.5 w-2.5"
              >
                <span
                  class="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75"
                ></span>
                <span
                  class="relative inline-flex h-2.5 w-2.5 rounded-full bg-green-500"
                ></span>
              </span>
              <CheckCircle v-else class="h-4 w-4 text-green-400" />
            </div>
          </div>

          <!-- Project name + external link / arrow icon -->
          <div class="mt-4 flex items-center justify-between">
            <h3 class="text-2xl font-semibold tracking-tight text-white">
              {{ project.name }}
            </h3>
            <a
              v-if="project.link"
              :href="project.link"
              target="_blank"
              rel="noopener noreferrer"
              class="shrink-0 rounded-full border border-white/10 bg-white/5 p-2.5 text-slate-300 transition duration-300 hover:border-cyan-400/40 hover:text-cyan-200"
            >
              <ExternalLink class="h-4 w-4" />
            </a>
            <div
              v-else
              class="shrink-0 rounded-full border border-white/10 bg-white/5 p-2.5 text-slate-300"
            >
              <ArrowUpRight class="h-4 w-4" />
            </div>
          </div>

          <!-- Description -->
          <div class="mt-6 flex-1">
            <div class="mb-4 flex items-center gap-2 text-sm text-slate-400">
              <Layers3 class="h-4 w-4 text-emerald-300" />
              <span>核心价值与技术难点</span>
            </div>
            <p class="text-base leading-relaxed text-slate-300">
              {{ project.description }}
            </p>
          </div>

          <!-- Tech stack tags -->
          <div class="mt-8 flex flex-wrap gap-3">
            <span
              v-for="stack in project.techStack"
              :key="stack"
              class="rounded-full border border-white/10 bg-slate-900/80 px-3 py-1.5 text-xs uppercase tracking-[0.18em] text-slate-300 transition duration-300 group-hover:border-cyan-300/30 group-hover:text-cyan-100"
            >
              {{ stack }}
            </span>
          </div>
        </article>
      </RevealBlock>
    </div>
  </section>
</template>
