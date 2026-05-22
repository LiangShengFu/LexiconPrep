<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const loggedIn = ref(false)
const mobileMenuOpen = ref(false)

const checkAuth = () => {
  loggedIn.value = !!localStorage.getItem('access_token')
}

checkAuth()

watch(() => route.path, () => { checkAuth(); mobileMenuOpen.value = false })

const goTo = (path: string) => { router.push(path); mobileMenuOpen.value = false }

const logout = () => {
  localStorage.clear()
  loggedIn.value = false
  mobileMenuOpen.value = false
  router.push('/')
}
</script>

<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-canvas/80 backdrop-blur-sm border-b border-hairline">
    <div class="max-w-[1200px] mx-auto flex items-center justify-between h-14 px-6">
      <button class="text-ink text-sm font-normal tracking-tight hover:text-body transition-colors focus:outline-none focus:ring-2 focus:ring-ink" aria-label="首页" @click="goTo('/')">
        LexiconPrep
      </button>

      <nav class="hidden md:flex items-center gap-8">
        <button class="text-body text-sm font-normal hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/library')">资源库</button>
        <button class="text-body text-sm font-normal hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/flashcards')">闪卡</button>
        <button class="text-body text-sm font-normal hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/community')">社区</button>
      </nav>

      <div class="hidden md:flex items-center gap-3" v-if="loggedIn">
        <button class="btn-pill-outline cursor-target text-sm focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/profile')">个人主页</button>
        <button class="btn-pill-outline cursor-target text-sm focus:outline-none focus:ring-2 focus:ring-ink" aria-label="退出登录" @click="logout">退出</button>
      </div>
      <div class="hidden md:flex items-center gap-3" v-else>
        <button class="btn-pill-outline cursor-target text-sm focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/login')">登录</button>
        <button class="btn-pill-filled cursor-target text-sm focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/register')">注册</button>
      </div>

      <!-- Mobile hamburger -->
      <button class="md:hidden text-ink focus:outline-none focus:ring-2 focus:ring-ink" aria-label="菜单" @click="mobileMenuOpen = !mobileMenuOpen">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-hairline bg-canvas px-6 py-4 space-y-3">
      <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/library')">资源库</button>
      <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/flashcards')">闪卡</button>
      <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/community')">社区</button>
      <div class="pt-3 border-t border-hairline space-y-2" v-if="loggedIn">
        <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/profile')">个人主页</button>
        <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="logout">退出</button>
      </div>
      <div class="pt-3 border-t border-hairline space-y-2" v-else>
        <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/login')">登录</button>
        <button class="block w-full text-left text-body text-sm py-2 hover:text-ink transition-colors focus:outline-none focus:ring-2 focus:ring-ink" @click="goTo('/register')">注册</button>
      </div>
    </div>
  </header>
</template>
