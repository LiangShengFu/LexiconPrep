<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="h-full flex items-center justify-center p-8">
    <div class="text-center">
      <p class="font-mono text-8xl text-ink mb-4">404</p>
      <p class="eyebrow-mono-sm text-mute mb-2">PAGE NOT FOUND</p>
      <p class="text-body text-sm mb-8">你访问的页面不存在或已被移除。</p>
      <div class="flex items-center justify-center gap-3">
        <button class="btn-pill-outline cursor-target text-sm" @click="router.back()">返回上页</button>
        <button class="btn-pill-filled cursor-target text-sm" @click="router.push('/')">回到首页</button>
      </div>
    </div>
  </div>
</template>
