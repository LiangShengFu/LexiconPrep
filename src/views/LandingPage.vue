<script setup lang="ts">
import { useRouter } from 'vue-router'
import DecryptedText from '@/components/DecryptedText.vue'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()

const subjects = [
  { name: '计算机科学', tag: '计算机科学', span: 'col-span-1 row-span-1' },
  { name: '法学硕士', tag: '法学硕士', span: 'col-span-1 row-span-1' },
  { name: '经济学', tag: '经济学', span: 'col-span-1 row-span-1' },
  { name: '心理学专硕', tag: '心理学专硕', span: 'col-span-2 row-span-1' },
  { name: '医学', tag: '医学', span: 'col-span-1 row-span-1' },
]

const features = [
  { title: '自适应题库', description: '根据掌握程度实时调整难度，精准定位薄弱环节。' },
  { title: '悬浮番茄钟', description: '悬浮番茄钟跨页面保持专注，学习节奏不被打断。' },
  { title: '智能复习算法', description: '基于间隔重复算法，针对考研题型优化复习策略。' },
]
</script>

<template>
  <div class="min-h-screen bg-canvas pt-14 relative">
    <!-- Full-page terminal background -->
    <div class="fixed inset-0 opacity-25 pointer-events-none z-0">
      <FaultyTerminal
        :scale="2"
        :grid-mul="[4, 2]"
        :digit-size="1.5"
        :time-scale="0.2"
        :scanline-intensity="0.2"
        :glitch-amount="0.8"
        :flicker-amount="0.6"
        :noise-amp="0.5"
        :chromatic-aberration="0"
        :dither="0"
        :curvature="0"
        tint="#ffffff"
        :mouse-react="false"
        :page-load-animation="true"
        :brightness="0.6"
      />
    </div>

    <!-- ─── Hero Band ─── -->
    <section class="relative px-6 py-section max-w-[1200px] mx-auto z-10">
      <p class="eyebrow-mono mb-6">考研备考平台</p>
      <h1 class="text-display-xl text-ink max-w-[800px] leading-[96px]">
        <DecryptedText
          text="精准备考"
          :speed="100"
          :max-iterations="10"
          :sequential="true"
          reveal-direction="start"
          :use-original-chars-only="false"
          animate-on="view"
          class-name="text-ink"
          encrypted-class-name="text-mute"
        />
        <br />
        <DecryptedText
          text="攻克最难考试。"
          :speed="100"
          :max-iterations="10"
          :sequential="true"
          reveal-direction="start"
          :use-original-chars-only="false"
          animate-on="view"
          class-name="text-ink"
          encrypted-class-name="text-mute"
        />
      </h1>
      <p class="text-body-lg text-body mt-8 max-w-[520px] leading-7">
        LexiconPrep 整合自适应题库、智能闪卡复习与实时进度分析，为考研学子打造一站式专注备考平台。
      </p>
      <div class="flex items-center gap-4 mt-10">
        <button class="btn-pill-filled cursor-target text-base px-6 py-3" @click="router.push('/login')">
          开始备考
        </button>
        <button class="btn-pill-outline cursor-target text-base px-6 py-3 cursor-target" @click="router.push('/profile')">
          查看个人主页
        </button>
      </div>
    </section>

    <div class="divider-hairline max-w-[1200px] mx-auto relative z-10" />

    <!-- ─── Subject Bento Grid ─── -->
    <section class="relative z-10 px-6 py-section max-w-[1200px] mx-auto">
      <p class="eyebrow-mono mb-4">学科分类</p>
      <h2 class="text-display-md text-ink mb-10">
        <DecryptedText text="找到你的学科方向。" :speed="100" :max-iterations="10" :sequential="true" animate-on="view" class-name="text-ink" encrypted-class-name="text-mute" />
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 auto-rows-[160px]">
        <div
          v-for="subj in subjects"
          :key="subj.name"
          :class="[subj.span, 'card-xai flex flex-col justify-between cursor-pointer hover:border-canvas-mid transition-colors group cursor-target']"
          @click="router.push('/library')"
        >
          <span class="eyebrow-mono-sm text-mute">{{ subj.tag }}</span>
          <div class="flex items-center justify-between">
            <span class="text-xl text-ink font-normal">{{ subj.name }}</span>
            <span class="text-mute group-hover:text-ink transition-colors">&rarr;</span>
          </div>
        </div>
      </div>
    </section>

    <div class="divider-hairline max-w-[1200px] mx-auto relative z-10" />

    <!-- ─── Features ─── -->
    <section class="relative z-10 px-6 py-section max-w-[1200px] mx-auto">
      <p class="eyebrow-mono mb-4">核心能力</p>
      <h2 class="text-display-md text-ink mb-10">
        <DecryptedText text="备考所需，一站俱全。" :speed="100" :max-iterations="10" :sequential="true" animate-on="view" class-name="text-ink" encrypted-class-name="text-mute" />
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="f in features" :key="f.title" class="card-xai cursor-target">
          <div class="w-2 h-2 rounded-full bg-accent-sunset mb-6" />
          <h3 class="text-lg text-ink font-normal mb-2">{{ f.title }}</h3>
          <p class="text-body-mid text-sm leading-5">{{ f.description }}</p>
        </div>
      </div>
    </section>

    <div class="divider-hairline max-w-[1200px] mx-auto relative z-10" />

    <!-- ─── Footer ─── -->
    <footer class="relative z-10 px-6 py-section max-w-[1200px] mx-auto">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <span class="text-body text-sm font-normal tracking-tight">LexiconPrep</span>
        <div class="flex items-center gap-6">
          <span class="text-mute text-sm cursor-pointer hover:text-ink transition-colors">荣誉准则</span>
          <span class="text-mute text-sm cursor-pointer hover:text-ink transition-colors">服务条款</span>
          <span class="text-mute text-sm cursor-pointer hover:text-ink transition-colors">联系我们</span>
        </div>
        <span class="text-mute text-sm">&#169; 2026 LexiconPrep</span>
      </div>
    </footer>
  </div>
</template>
