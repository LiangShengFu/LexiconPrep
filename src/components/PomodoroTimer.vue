<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const savedWork = parseInt(localStorage.getItem('pomodoro_work') || '25')
const savedBreak = parseInt(localStorage.getItem('pomodoro_break') || '5')

const workMinutes = ref(savedWork)
const breakMinutes = ref(savedBreak)
const isWork = ref(true)
const minutes = ref(savedWork)
const seconds = ref(0)
const running = ref(false)
const minimized = ref(true)
let timer: ReturnType<typeof setInterval> | null = null

const totalSeconds = computed(() => (isWork.value ? workMinutes.value : breakMinutes.value) * 60)
const elapsed = computed(() => totalSeconds.value - (minutes.value * 60 + seconds.value))
const progress = computed(() => (elapsed.value / totalSeconds.value) * 100)
const display = computed(() => `${String(minutes.value).padStart(2, '0')}:${String(seconds.value).padStart(2, '0')}`)
const label = computed(() => isWork.value ? '专注' : '休息')

const tick = () => {
  if (seconds.value === 0) {
    if (minutes.value === 0) { clearInterval(timer!); timer = null; running.value = false; switchMode(); return }
    minutes.value--; seconds.value = 59
  } else { seconds.value-- }
}

const start = () => { if (running.value) return; running.value = true; minimized.value = false; timer = setInterval(tick, 1000) }
const pause = () => { running.value = false; if (timer) { clearInterval(timer); timer = null } }
const reset = () => { pause(); minutes.value = isWork.value ? workMinutes.value : breakMinutes.value; seconds.value = 0 }
const switchMode = () => { isWork.value = !isWork.value; minutes.value = isWork.value ? workMinutes.value : breakMinutes.value; seconds.value = 0; running.value = false; if (timer) { clearInterval(timer); timer = null } }
const toggleMinimize = () => { minimized.value = !minimized.value }

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
  <button v-if="minimized"
    class="fixed bottom-6 right-6 z-40 w-12 h-12 rounded-full bg-canvas-card border border-hairline flex items-center justify-center hover:border-ink transition-colors cursor-target"
    @click="toggleMinimize">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff7a17" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>
  </button>

  <div v-if="!minimized" class="fixed bottom-6 right-6 z-40 card-xai w-[200px] text-center space-y-3">
    <div class="flex items-center justify-between">
      <button class="text-mute text-xs hover:text-ink cursor-target" @click="switchMode">{{ isWork ? '切换休息' : '切换专注' }}</button>
      <button class="text-mute text-xs hover:text-ink cursor-target" @click="router.push('/pomodoro')">全屏</button>
      <button class="text-mute text-xs hover:text-ink cursor-target" @click="toggleMinimize">收起</button>
    </div>
    <div class="relative w-[100px] h-[100px] mx-auto">
      <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="44" fill="none" stroke="#212327" stroke-width="5" />
        <circle cx="50" cy="50" r="44" fill="none" :stroke="isWork ? '#ff7a17' : '#50e3c2'" stroke-width="5" stroke-linecap="round"
          :stroke-dasharray="2 * Math.PI * 44" :stroke-dashoffset="2 * Math.PI * 44 * (1 - progress / 100)" />
      </svg>
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-xl text-ink font-mono">{{ display }}</span>
        <span class="text-xs text-mute">{{ label }}</span>
      </div>
    </div>
    <div class="flex items-center justify-center gap-2">
      <button v-if="!running" class="btn-pill-filled cursor-target text-xs px-4 py-1.5" @click="start">开始</button>
      <button v-else class="btn-pill-outline cursor-target text-xs px-4 py-1.5" @click="pause">暂停</button>
      <button class="btn-pill-outline cursor-target text-xs px-3 py-1.5" @click="reset">重置</button>
    </div>
  </div>
</template>
