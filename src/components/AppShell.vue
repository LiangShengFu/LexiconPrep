<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PomodoroTimer from '@/components/PomodoroTimer.vue'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const sidebarOpen = ref(false)

const navItems = [
  { path: '/profile', label: '个人主页', icon: 'User' },
  { path: '/exam', label: '答题', icon: 'EditPen' },
  { path: '/library', label: '资源库', icon: 'Reading' },
  { path: '/progress', label: '学习进度', icon: 'TrendCharts' },
  { path: '/flashcards', label: '闪卡', icon: 'Collection' },
  { path: '/community', label: '社区', icon: 'ChatLineSquare' },
]
const adminNav = { path: '/admin', label: '管理后台', icon: 'Setting' }

const isAdmin = () => {
  const userStr = localStorage.getItem('user')
  if (!userStr) return false
  try { return JSON.parse(userStr).role === 'admin' } catch { return false }
}

const isActive = (path: string) => route.path === path
const navigateTo = (path: string) => { router.push(path); sidebarOpen.value = false }
</script>

<template>
  <div class="flex h-screen bg-canvas relative">
    <!-- Terminal background -->
    <div class="fixed inset-0 opacity-20 pointer-events-none z-0">
      <FaultyTerminal :scale="2" :grid-mul="[4, 2]" :digit-size="1.5" :time-scale="0.2"
        :scanline-intensity="0.2" :glitch-amount="0.8" :flicker-amount="0.6" :noise-amp="0.5"
        :chromatic-aberration="0" :dither="0" :curvature="0" tint="#ffffff"
        :mouse-react="false" :page-load-animation="true" :brightness="0.6" />
    </div>

    <!-- Mobile overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black/50 z-30 md:hidden" @click="sidebarOpen = false" />

    <!-- Sidebar -->
    <aside class="w-56 flex-shrink-0 border-r border-hairline bg-canvas flex-col fixed md:relative inset-y-0 left-0 z-40 transition-transform md:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0 flex' : '-translate-x-full md:flex'">
      <button
        class="h-14 flex items-center px-6 text-ink text-sm font-normal tracking-tight border-b border-hairline focus:outline-none focus:ring-2 focus:ring-ink"
        aria-label="首页"
        @click="navigateTo('/')"
      >
        LexiconPrep
      </button>

      <nav class="flex-1 py-4 space-y-1 px-3">
        <button
          v-for="item in navItems"
          :key="item.path"
          class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors cursor-target focus:outline-none focus:ring-2 focus:ring-ink"
          :class="isActive(item.path) ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
          :aria-label="item.label"
          @click="navigateTo(item.path)"
        >
          <el-icon :size="16">
            <component :is="item.icon" />
          </el-icon>
          {{ item.label }}
        </button>
        <div v-if="isAdmin()" class="pt-3 mt-3 border-t border-hairline">
          <button
            class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors cursor-target focus:outline-none focus:ring-2 focus:ring-ink"
            :class="route.path.startsWith('/admin') ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
            aria-label="管理后台"
            @click="navigateTo('/admin')"
          >
            <el-icon :size="16"><component :is="adminNav.icon" /></el-icon>
            管理后台
          </button>
        </div>
      </nav>

      <div class="p-3 border-t border-hairline">
        <button
          class="btn-pill-outline cursor-target text-sm w-full focus:outline-none focus:ring-2 focus:ring-ink"
          aria-label="退出登录"
          @click="auth.logout(); router.push('/')"
        >
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto relative z-10">
      <!-- Mobile top bar -->
      <div class="md:hidden flex items-center justify-between h-14 px-4 border-b border-hairline bg-canvas/80 backdrop-blur-sm sticky top-0 z-20">
        <button class="text-ink focus:outline-none focus:ring-2 focus:ring-ink" aria-label="打开菜单" @click="sidebarOpen = true">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <span class="text-ink text-sm font-normal tracking-tight">LexiconPrep</span>
        <div class="w-6" />
      </div>
      <slot />
    </main>
    <PomodoroTimer />
  </div>
</template>
