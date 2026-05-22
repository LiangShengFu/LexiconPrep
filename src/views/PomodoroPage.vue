<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()
const savedWork = parseInt(localStorage.getItem('pomodoro_work') || '25')
const savedBreak = parseInt(localStorage.getItem('pomodoro_break') || '5')

const workMinutes = ref(savedWork)
const breakMinutes = ref(savedBreak)
const isWork = ref(true)
const minutes = ref(savedWork)
const seconds = ref(0)
const running = ref(false)
const showSettings = ref(false)
const settingWork = ref(savedWork)
const settingBreak = ref(savedBreak)
let timer: ReturnType<typeof setInterval> | null = null

const totalSeconds = computed(() => (isWork.value ? workMinutes.value : breakMinutes.value) * 60)
const elapsed = computed(() => totalSeconds.value - (minutes.value * 60 + seconds.value))
const progress = computed(() => (elapsed.value / totalSeconds.value) * 100)
const display = computed(() => `${String(minutes.value).padStart(2, '0')}:${String(seconds.value).padStart(2, '0')}`)
const label = computed(() => isWork.value ? '专注' : '休息')
const radius = 180
const circumference = 2 * Math.PI * radius

const tick = () => {
  if (seconds.value === 0) {
    if (minutes.value === 0) { clearInterval(timer!); timer = null; running.value = false; switchMode(); return }
    minutes.value--; seconds.value = 59
  } else { seconds.value-- }
}
const start = () => { if (running.value) return; running.value = true; timer = setInterval(tick, 1000) }
const pause = () => { running.value = false; if (timer) { clearInterval(timer); timer = null } }
const reset = () => { pause(); minutes.value = isWork.value ? workMinutes.value : breakMinutes.value; seconds.value = 0 }
const switchMode = () => { isWork.value = !isWork.value; minutes.value = isWork.value ? workMinutes.value : breakMinutes.value; seconds.value = 0; running.value = false; if (timer) { clearInterval(timer); timer = null } }
const saveSettings = () => {
  workMinutes.value = settingWork.value; breakMinutes.value = settingBreak.value
  localStorage.setItem('pomodoro_work', String(settingWork.value))
  localStorage.setItem('pomodoro_break', String(settingBreak.value))
  if (!running.value) { minutes.value = isWork.value ? workMinutes.value : breakMinutes.value; seconds.value = 0 }
  showSettings.value = false
}

onUnmounted(() => { if (timer) clearInterval(timer) })
</script>

<template>
  <div class="fixed inset-0 z-50 flex flex-col items-center justify-center">
    <div class="absolute inset-0 opacity-25 pointer-events-none">
      <FaultyTerminal :scale="2" :grid-mul="[4, 2]" :digit-size="1.5" :time-scale="0.2"
        :scanline-intensity="0.2" :glitch-amount="0.8" :flicker-amount="0.6" :noise-amp="0.5"
        :chromatic-aberration="0" :dither="0" :curvature="0" tint="#ffffff"
        :mouse-react="false" :page-load-animation="false" :brightness="0.6" />
    </div>
    <div class="relative z-10 flex flex-col items-center">
      <button class="absolute top-6 right-6 btn-pill-outline cursor-target text-sm" @click="router.back()">返回</button>
      <button class="absolute top-6 left-6 btn-pill-outline cursor-target text-sm" @click="showSettings = true">设置</button>

      <p class="eyebrow-mono mb-6">{{ isWork ? '专注模式' : '休息时间' }}</p>
      <div class="relative max-w-[400px] w-full aspect-square">
        <svg class="w-full h-full -rotate-90" viewBox="0 0 400 400">
          <circle cx="200" cy="200" :r="radius" fill="none" stroke="#212327" stroke-width="6" />
          <circle cx="200" cy="200" :r="radius" fill="none" :stroke="isWork ? '#ff7a17' : '#50e3c2'" stroke-width="6" stroke-linecap="round"
            :stroke-dasharray="circumference" :stroke-dashoffset="circumference * (1 - progress / 100)" class="transition-all duration-1000" />
        </svg>
        <div class="absolute inset-0 flex flex-col items-center justify-center" role="timer" :aria-label="label + '模式，剩余' + display" aria-live="polite">
          <span class="text-[96px] text-ink font-mono tracking-tight leading-none">{{ display }}</span>
          <span class="text-2xl text-mute mt-2">{{ label }}</span>
          <span class="text-sm text-mute mt-1">{{ isWork ? workMinutes : breakMinutes }} 分钟</span>
        </div>
      </div>
      <div class="flex items-center gap-4 mt-10">
        <button v-if="!running" class="btn-pill-filled cursor-target text-lg px-10 py-4" @click="start">开始</button>
        <button v-else class="btn-pill-outline cursor-target text-lg px-10 py-4" @click="pause">暂停</button>
        <button class="btn-pill-outline cursor-target text-lg px-8 py-4" @click="reset">重置</button>
      </div>
      <button class="btn-pill-outline cursor-target text-sm mt-8" @click="switchMode">切换到{{ isWork ? '休息' : '专注' }}</button>
    </div>

    <!-- Settings -->
    <div v-if="showSettings" class="fixed inset-0 z-[70] flex items-center justify-center bg-black/60" @click.self="showSettings = false">
      <div class="card-xai w-full max-w-[320px] mx-4 space-y-4 relative z-20">
        <p class="eyebrow-mono-sm text-mute">番茄钟设置</p>
        <div>
          <label class="block text-body text-sm mb-2">专注时长: {{ settingWork }} 分钟</label>
          <input v-model.number="settingWork" type="range" min="5" max="60" step="5" class="w-full accent-white" />
        </div>
        <div>
          <label class="block text-body text-sm mb-2">休息时长: {{ settingBreak }} 分钟</label>
          <input v-model.number="settingBreak" type="range" min="1" max="30" step="1" class="w-full accent-white" />
        </div>
        <div class="flex gap-3 pt-2">
          <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="showSettings = false">取消</button>
          <button class="btn-pill-filled cursor-target flex-1 text-sm" @click="saveSettings">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>
