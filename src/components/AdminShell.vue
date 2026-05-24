<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PomodoroTimer from '@/components/PomodoroTimer.vue'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const navItems = [
  { path: '/admin', label: '概览', icon: 'Odometer' },
  { path: '/admin/questions', label: '题目管理', icon: 'EditPen' },
  { path: '/admin/users', label: '用户管理', icon: 'User' },
]

const isActive = (path: string) => route.path === path
</script>

<template>
  <div class="flex h-screen bg-canvas relative">
    <div class="fixed inset-0 opacity-20 pointer-events-none z-0">
      <FaultyTerminal :scale="2" :grid-mul="[4, 2]" :digit-size="1.5" :time-scale="0.2"
        :scanline-intensity="0.2" :glitch-amount="0.8" :flicker-amount="0.6" :noise-amp="0.5"
        :chromatic-aberration="0" :dither="0" :curvature="0" tint="#ffffff"
        :mouse-react="false" :page-load-animation="true" :brightness="0.6" />
    </div>
    <aside class="w-56 flex-shrink-0 border-r-4 border-dashed border-hairline bg-canvas flex flex-col">
      <button class="h-14 flex items-center px-6 text-ink text-sm font-normal tracking-tight border-b-4 border-dashed border-hairline" @click="router.push('/admin')">
        管理后台
      </button>
      <nav class="flex-1 py-4 space-y-1 px-3">
        <button
          v-for="item in navItems" :key="item.path"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors cursor-target"
          :class="isActive(item.path) ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
          @click="router.push(item.path)"
        >
          <el-icon :size="16"><component :is="item.icon" /></el-icon>
          {{ item.label }}
        </button>
      </nav>
      <div class="p-3 border-t-4 border-dashed border-hairline space-y-2">
        <button class="btn-pill-outline cursor-target text-sm w-full" @click="router.push('/profile')">返回前台</button>
        <button class="btn-pill-outline cursor-target text-sm w-full" @click="auth.logout(); router.push('/')">退出</button>
      </div>
    </aside>
    <main class="flex-1 overflow-auto relative z-10">
      <slot />
    </main>
    <PomodoroTimer />
  </div>
</template>
