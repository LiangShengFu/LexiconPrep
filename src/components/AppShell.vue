<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { path: '/dashboard', label: '仪表盘', icon: 'Odometer' },
  { path: '/library', label: '资源库', icon: 'Reading' },
  { path: '/exam', label: '做题', icon: 'EditPen' },
  { path: '/flashcards', label: '闪卡', icon: 'Collection' },
  { path: '/progress', label: '学习进度', icon: 'TrendCharts' },
  { path: '/community', label: '社区', icon: 'ChatLineSquare' },
  { path: '/settings', label: '设置', icon: 'Setting' },
]

const isActive = (path: string) => route.path === path
</script>

<template>
  <div class="flex h-screen bg-canvas">
    <!-- Sidebar -->
    <aside class="w-56 flex-shrink-0 border-r border-hairline bg-canvas flex flex-col">
      <button
        class="h-14 flex items-center px-6 text-ink text-sm font-normal tracking-tight border-b border-hairline"
        @click="router.push('/')"
      >
        LexiconPrep
      </button>

      <nav class="flex-1 py-4 space-y-1 px-3">
        <button
          v-for="item in navItems"
          :key="item.path"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors"
          :class="isActive(item.path) ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
          @click="router.push(item.path)"
        >
          <el-icon :size="16">
            <component :is="item.icon" />
          </el-icon>
          {{ item.label }}
        </button>
      </nav>

      <div class="p-3 border-t border-hairline">
        <button
          class="btn-pill-outline text-sm w-full"
          @click="router.push('/')"
        >
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <slot />
    </main>
  </div>
</template>
