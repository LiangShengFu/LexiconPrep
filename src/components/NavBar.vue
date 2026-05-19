<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (path: string) => {
  router.push(path)
}
</script>

<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-canvas/80 backdrop-blur-sm border-b border-hairline">
    <div class="max-w-[1200px] mx-auto flex items-center justify-between h-14 px-6">
      <!-- Logo -->
      <button
        class="text-ink text-sm font-normal tracking-tight hover:text-body transition-colors"
        @click="goTo('/')"
      >
        LexiconPrep
      </button>

      <!-- Nav Links -->
      <nav class="hidden md:flex items-center gap-8">
        <button
          class="text-body text-sm font-normal hover:text-ink transition-colors"
          @click="goTo('/library')"
        >
          资源库
        </button>
        <button
          class="text-body text-sm font-normal hover:text-ink transition-colors"
          @click="goTo('/exam')"
        >
          做题
        </button>
        <button
          class="text-body text-sm font-normal hover:text-ink transition-colors"
          @click="goTo('/flashcards')"
        >
          闪卡
        </button>
        <button
          class="text-body text-sm font-normal hover:text-ink transition-colors"
          @click="goTo('/community')"
        >
          社区
        </button>
      </nav>

      <!-- CTA -->
      <div class="flex items-center gap-3">
        <button
          class="btn-pill-outline text-sm"
          @click="goTo('/login')"
        >
          登录
        </button>
        <button
          class="btn-pill-filled text-sm"
          @click="goTo('/register')"
        >
          注册
        </button>
      </div>
    </div>
  </header>
</template>
