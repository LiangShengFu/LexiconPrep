<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'

const WORK_MINUTES = 25
const BREAK_MINUTES = 5

const isWork = ref(true)
const minutes = ref(WORK_MINUTES)
const seconds = ref(0)
const running = ref(false)
const minimized = ref(true)
const fullscreen = ref(false)
let timer: ReturnType<typeof setInterval> | null = null

const totalSeconds = computed(() => (isWork.value ? WORK_MINUTES : BREAK_MINUTES) * 60)
const elapsed = computed(() => totalSeconds.value - (minutes.value * 60 + seconds.value))
const progress = computed(() => (elapsed.value / totalSeconds.value) * 100)
const display = computed(() => `${String(minutes.value).padStart(2, '0')}:${String(seconds.value).padStart(2, '0')}`)
const label = computed(() => isWork.value ? '专注' : '休息')

const tick = () => {
  if (seconds.value === 0) {
    if (minutes.value === 0) {
      clearInterval(timer!)
      timer = null
      running.value = false
      switchMode()
      return
    }
    minutes.value--
    seconds.value = 59
  } else {
    seconds.value--
  }
}

const start = () => {
  if (running.value) return
  running.value = true
  minimized.value = false
  timer = setInterval(tick, 1000)
}

const pause = () => {
  running.value = false
  if (timer) { clearInterval(timer); timer = null }
}

const reset = () => {
  pause()
  minutes.value = isWork.value ? WORK_MINUTES : BREAK_MINUTES
  seconds.value = 0
}

const switchMode = () => {
  isWork.value = !isWork.value
  minutes.value = isWork.value ? WORK_MINUTES : BREAK_MINUTES
  seconds.value = 0
  running.value = false
  if (timer) { clearInterval(timer); timer = null }
}

const openFullscreen = () => {
  fullscreen.value = true
  minimized.value = false
}

const closeFullscreen = () => {
  fullscreen.value = false
  minimized.value = true
}

const toggleMinimize = () => {
  minimized.value = !minimized.value
  if (!minimized.value) fullscreen.value = false
}

const radius = 180
const circumference = 2 * Math.PI * radius

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
  <!-- Minimized floating button -->
  <button
    v-if="minimized && !fullscreen"
    class="fixed bottom-6 right-6 z-40 w-12 h-12 rounded-full bg-canvas-card border border-hairline flex items-center justify-center hover:border-ink transition-colors"
    @click="toggleMinimize"
  >
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff7a17" stroke-width="2" stroke-linecap="round">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12,6 12,12 16,14"/>
    </svg>
  </button>

  <!-- Small floating timer -->
  <div
    v-if="!minimized && !fullscreen"
    class="fixed bottom-6 right-6 z-40 card-xai w-[200px] text-center space-y-3"
  >
    <div class="flex items-center justify-between">
      <button class="text-mute text-xs hover:text-ink" @click="switchMode">{{ isWork ? '切换休息' : '切换专注' }}</button>
      <button class="text-mute text-xs hover:text-ink" @click="openFullscreen">放大</button>
      <button class="text-mute text-xs hover:text-ink" @click="toggleMinimize">收起</button>
    </div>

    <div class="relative w-[100px] h-[100px] mx-auto">
      <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="44" fill="none" stroke="#212327" stroke-width="5" />
        <circle cx="50" cy="50" r="44" fill="none"
          :stroke="isWork ? '#ff7a17' : '#50e3c2'" stroke-width="5" stroke-linecap="round"
          :stroke-dasharray="2 * Math.PI * 44"
          :stroke-dashoffset="2 * Math.PI * 44 * (1 - progress / 100)" />
      </svg>
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-xl text-ink font-mono">{{ display }}</span>
        <span class="text-xs text-mute">{{ label }}</span>
      </div>
    </div>

    <div class="flex items-center justify-center gap-2">
      <button v-if="!running" class="btn-pill-filled text-xs px-4 py-1.5" @click="start">开始</button>
      <button v-else class="btn-pill-outline text-xs px-4 py-1.5" @click="pause">暂停</button>
      <button class="btn-pill-outline text-xs px-3 py-1.5" @click="reset">重置</button>
    </div>
  </div>

  <!-- Fullscreen mode -->
  <div
    v-if="fullscreen"
    class="fixed inset-0 z-50 bg-canvas flex flex-col items-center justify-center"
  >
    <button class="absolute top-6 right-6 btn-pill-outline text-sm" @click="closeFullscreen">退出全屏</button>

    <p class="eyebrow-mono mb-6">{{ isWork ? '专注模式' : '休息时间' }}</p>

    <!-- Large ring -->
    <div class="relative" style="width:400px;height:400px">
      <svg class="w-full h-full -rotate-90" viewBox="0 0 400 400">
        <circle cx="200" cy="200" :r="radius" fill="none" stroke="#212327" stroke-width="6" />
        <circle cx="200" cy="200" :r="radius" fill="none"
          :stroke="isWork ? '#ff7a17' : '#50e3c2'" stroke-width="6" stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="circumference * (1 - progress / 100)"
          class="transition-all duration-1000" />
      </svg>
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-[96px] text-ink font-mono tracking-tight leading-none">{{ display }}</span>
        <span class="text-2xl text-mute mt-2">{{ label }}</span>
        <span class="text-sm text-mute mt-1">{{ isWork ? `${WORK_MINUTES} 分钟` : `${BREAK_MINUTES} 分钟` }}</span>
      </div>
    </div>

    <div class="flex items-center gap-4 mt-10">
      <button v-if="!running" class="btn-pill-filled text-lg px-10 py-4" @click="start">开始</button>
      <button v-else class="btn-pill-outline text-lg px-10 py-4" @click="pause">暂停</button>
      <button class="btn-pill-outline text-lg px-8 py-4" @click="reset">重置</button>
    </div>

    <button class="btn-pill-outline text-sm mt-8" @click="switchMode">
      切换到{{ isWork ? '休息' : '专注' }}
    </button>
  </div>
</template>
