<script setup>
import { computed, onMounted, ref } from "vue";
import { fetchResumeProfile } from "./api/resumeApi";
import AboutAndEducation from "./components/AboutAndEducation.vue";
import HeroSection from "./components/HeroSection.vue";
import NavBar from "./components/NavBar.vue";
import PracticeAndCertificates from "./components/PracticeAndCertificates.vue";
import ProjectsGallery from "./components/ProjectsGallery.vue";
import SkillsMatrix from "./components/SkillsMatrix.vue";
import WorkExperience from "./components/WorkExperience.vue";

const resume = ref(null);

const navItems = [
  { label: "关于我", href: "#about" },
  { label: "教育背景", href: "#education" },
  { label: "技能矩阵", href: "#skills" },
  { label: "工作经历", href: "#experience" },
  { label: "核心项目", href: "#projects" },
  { label: "实践认证", href: "#practice" },
];

const metrics = computed(() => {
  if (!resume.value) {
    return [];
  }

  return [
    {
      value: "LLM",
      label: "工作流能力",
      detail: "Prompt Engineering / RAG / Agent 设计",
    },
    {
      value: "10+",
      label: "实战项目",
      detail: "AI Agent、全栈系统、创业项目多领域覆盖",
    },
    {
      value: "Python + Vue",
      label: "系统落地",
      detail: "从 Flask API 到高并发架构，全链路工程交付",
    },
  ];
});

onMounted(async () => {
  resume.value = await fetchResumeProfile();
});
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <div class="pointer-events-none fixed inset-0 overflow-hidden">
      <div
        class="absolute inset-0 bg-aurora-radial opacity-90"
      />
      <div
        class="absolute left-1/2 top-0 h-[38rem] w-[38rem] -translate-x-1/2 rounded-full bg-cyan-400/10 blur-3xl"
      />
      <div
        class="absolute bottom-[-8rem] right-[-6rem] h-[26rem] w-[26rem] rounded-full bg-emerald-400/10 blur-3xl"
      />
      <div
        class="absolute inset-0 bg-hero-grid bg-[size:72px_72px] opacity-[0.06]"
      />
    </div>

    <NavBar :items="navItems" />

    <main class="relative z-10">
      <template v-if="resume">
        <HeroSection
          :personal-info="resume.personalInfo"
          :metrics="metrics"
        />
        <AboutAndEducation
          :personal-info="resume.personalInfo"
          :education="resume.education"
        />
        <SkillsMatrix :skills="resume.skills" />
        <WorkExperience :experience="resume.workExperience" />
        <ProjectsGallery :projects="resume.projects" />
        <PracticeAndCertificates
          :practice-data="resume.practices_and_certifications"
        />
      </template>

      <section
        v-else
        class="mx-auto flex min-h-screen max-w-7xl items-center justify-center px-6"
      >
        <div
          class="glass-panel flex items-center gap-4 rounded-3xl px-8 py-6 text-slate-200"
        >
          <div class="h-3 w-3 animate-pulse rounded-full bg-cyan-300" />
          <p class="text-sm uppercase tracking-[0.35em] text-slate-300">
            Initializing profile system...
          </p>
        </div>
      </section>
    </main>
  </div>
</template>
