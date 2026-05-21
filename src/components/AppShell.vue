<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PomodoroTimer from '@/components/PomodoroTimer.vue'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const navItems = [
  { path: '/profile', label: '个人主页', icon: 'User' },
  { path: '/library', label: '资源库', icon: 'Reading' },
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
          class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors cursor-target"
          :class="isActive(item.path) ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
          @click="router.push(item.path)"
        >
          <el-icon :size="16">
            <component :is="item.icon" />
          </el-icon>
          {{ item.label }}
        </button>
        <div v-if="isAdmin()" class="pt-3 mt-3 border-t border-hairline">
          <button
            class="w-full flex items-center gap-3 px-3 py-2 rounded-card text-sm font-normal transition-colors cursor-target"
            :class="route.path.startsWith('/admin') ? 'bg-canvas-soft text-ink' : 'text-body hover:text-ink hover:bg-canvas-soft'"
            @click="router.push('/admin')"
          >
            <el-icon :size="16"><component :is="adminNav.icon" /></el-icon>
            管理后台
          </button>
        </div>
      </nav>

      <div class="p-3 border-t border-hairline">
        <button
          class="btn-pill-outline cursor-target text-sm w-full"
          @click="auth.logout(); router.push('/')"
        >
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto relative z-10">
      <slot />
    </main>
    <PomodoroTimer />
  </div>
</template>
