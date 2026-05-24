<script setup lang="ts">
import { ref, computed, onUnmounted, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import FaultyTerminal from '@/components/FaultyTerminal.vue'

const router = useRouter()
const savedWork = parseInt(localStorage.getItem('pomodoro_work') || '25')
const savedBreak = parseInt(localStorage.getItem('pomodoro_break') || '5')

const workMinutes = ref(savedWork)
const breakMinutes = ref(savedBreak)
const isWork = ref(true)
const running = ref(false)
const showSettings = ref(false)
const settingWork = ref(savedWork)
const settingBreak = ref(savedBreak)

const totalMs = computed(() => (isWork.value ? workMinutes.value : breakMinutes.value) * 60 * 1000)
const remainMs = ref(totalMs.value)
let startStamp = 0
let remainAtStart = 0
let timer: ReturnType<typeof setInterval> | null = null

const elapsed = computed(() => totalMs.value - remainMs.value)
const progress = computed(() => (elapsed.value / totalMs.value) * 100)
const display = computed(() => {
  const ms = Math.max(0, remainMs.value)
  const m = Math.floor(ms / 60000)
  const s = Math.floor((ms % 60000) / 1000)
  const cs = Math.floor((ms % 1000) / 10)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(cs).padStart(2, '0')}`
})
const label = computed(() => isWork.value ? '专注' : '休息')

const tick = () => {
  const now = Date.now()
  remainMs.value = Math.max(0, remainAtStart - (now - startStamp))
  if (remainMs.value <= 0) {
    clearInterval(timer!); timer = null; running.value = false; switchMode()
  }
}
const start = () => {
  if (running.value) return
  running.value = true
  startStamp = Date.now()
  remainAtStart = remainMs.value
  timer = setInterval(tick, 16)
}
const pause = () => {
  running.value = false
  if (timer) { clearInterval(timer); timer = null }
}
const reset = () => {
  pause()
  remainMs.value = totalMs.value
}
const switchMode = () => {
  isWork.value = !isWork.value
  remainMs.value = totalMs.value
  running.value = false
  if (timer) { clearInterval(timer); timer = null }
}
const saveSettings = () => {
  workMinutes.value = settingWork.value; breakMinutes.value = settingBreak.value
  localStorage.setItem('pomodoro_work', String(settingWork.value))
  localStorage.setItem('pomodoro_break', String(settingBreak.value))
  if (!running.value) { remainMs.value = totalMs.value }
  showSettings.value = false
}

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animFrame = 0
let orbitTick = 0

function isDark() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

function drawArc(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, startAngle: number, endAngle: number, color: string, lw: number, dash: number[] = []) {
  ctx.save()
  ctx.beginPath()
  ctx.arc(cx, cy, r, startAngle, endAngle)
  ctx.strokeStyle = color
  ctx.lineWidth = lw
  ctx.setLineDash(dash)
  ctx.stroke()
  ctx.restore()
}

function drawTick(ctx: CanvasRenderingContext2D, cx: number, cy: number, r1: number, r2: number, angle: number, color: string, lw: number) {
  ctx.save()
  ctx.beginPath()
  ctx.moveTo(cx + Math.cos(angle) * r1, cy + Math.sin(angle) * r1)
  ctx.lineTo(cx + Math.cos(angle) * r2, cy + Math.sin(angle) * r2)
  ctx.strokeStyle = color
  ctx.lineWidth = lw
  ctx.stroke()
  ctx.restore()
}

function drawCanvas() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const W = 400, H = 400, CX = W / 2, CY = H / 2
  const dark = isDark()

  const accent1 = isWork.value ? (dark ? '#F0997B' : '#993C1D') : (dark ? '#5DCAA5' : '#0F6E56')
  const faint1 = isWork.value
    ? (dark ? 'rgba(240,153,123,0.12)' : 'rgba(153,60,29,0.08)')
    : (dark ? 'rgba(93,202,165,0.12)' : 'rgba(15,110,86,0.08)')
  const accent2 = dark ? '#AFA9EC' : '#534AB7'
  const faint2 = dark ? 'rgba(175,169,236,0.12)' : 'rgba(83,74,183,0.08)'

  ctx.clearRect(0, 0, W, H)

  const RAD = -Math.PI / 2
  const prog = progress.value / 100

  for (let i = 0; i < 60; i++) {
    const a = RAD + (i / 60) * Math.PI * 2
    const isMaj = i % 5 === 0
    const r1 = isMaj ? 175 : 179
    const r2 = 185
    drawTick(ctx, CX, CY, r1, r2, a, isMaj ? accent2 : (dark ? 'rgba(175,169,236,0.35)' : 'rgba(83,74,183,0.25)'), isMaj ? 1.5 : 0.75)
  }

  drawArc(ctx, CX, CY, 165, 0, Math.PI * 2, faint1, 6)
  const progAngle = RAD + prog * Math.PI * 2
  drawArc(ctx, CX, CY, 165, RAD, progAngle, accent1, 6)

  ctx.save()
  ctx.beginPath()
  ctx.arc(CX + Math.cos(progAngle) * 165, CY + Math.sin(progAngle) * 165, 5, 0, Math.PI * 2)
  ctx.fillStyle = accent1
  ctx.fill()
  ctx.restore()

  drawArc(ctx, CX, CY, 148, 0, Math.PI * 2, faint2, 4)
  const secFrac = (remainMs.value / 1000) % 60 / 60
  const secAngle = RAD + secFrac * Math.PI * 2
  drawArc(ctx, CX, CY, 148, RAD, secAngle, accent2, 4)

  ctx.save()
  ctx.beginPath()
  ctx.arc(CX + Math.cos(secAngle) * 148, CY + Math.sin(secAngle) * 148, 3.5, 0, Math.PI * 2)
  ctx.fillStyle = accent2
  ctx.fill()
  ctx.restore()

  drawArc(ctx, CX, CY, 132, 0, Math.PI * 2, dark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)', 0.75, [4, 6])

  ctx.save()
  ctx.font = '500 10px monospace'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillStyle = dark ? '#aaa' : '#666'
  const totalMin = isWork.value ? workMinutes.value : breakMinutes.value
  for (let i = 0; i <= 12; i++) {
    const a = RAD + (i / 12) * Math.PI * 2
    const tx = CX + Math.cos(a) * 118
    const ty = CY + Math.sin(a) * 118
    const label = Math.round((i / 12) * totalMin)
    ctx.fillText(String(label).padStart(2, '0'), tx, ty)
  }
  ctx.restore()

  const crossSize = 10
  ctx.save()
  ctx.strokeStyle = dark ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.12)'
  ctx.lineWidth = 0.75
  ctx.beginPath(); ctx.moveTo(CX - crossSize, CY); ctx.lineTo(CX + crossSize, CY); ctx.stroke()
  ctx.beginPath(); ctx.moveTo(CX, CY - crossSize); ctx.lineTo(CX, CY + crossSize); ctx.stroke()
  ctx.restore()

  ctx.save()
  ctx.beginPath()
  ctx.arc(CX, CY, 3, 0, Math.PI * 2)
  ctx.fillStyle = dark ? '#aaa' : '#666'
  ctx.fill()
  ctx.restore()

  const orbitAngle = (orbitTick * 0.3) % 360
  const oRad = orbitAngle * Math.PI / 180
  ctx.save()
  ctx.beginPath()
  ctx.arc(CX, CY, 192, oRad, oRad + Math.PI * 0.25)
  ctx.strokeStyle = dark ? 'rgba(175,169,236,0.25)' : 'rgba(83,74,183,0.15)'
  ctx.lineWidth = 1
  ctx.stroke()
  ctx.beginPath()
  ctx.arc(CX, CY, 192, oRad + Math.PI, oRad + Math.PI * 1.25)
  ctx.stroke()
  ctx.restore()

  orbitTick++
  animFrame = requestAnimationFrame(drawCanvas)
}

onMounted(() => {
  nextTick(() => { drawCanvas() })
})

watch([progress, isWork], () => {})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (animFrame) cancelAnimationFrame(animFrame)
})
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
        <canvas ref="canvasRef" width="400" height="400" class="w-full h-full" />
        <div class="absolute inset-0 flex flex-col items-center justify-center" role="timer" :aria-label="label + '模式，剩余' + display" aria-live="polite">
          <span class="text-[56px] text-ink font-mono tracking-tight leading-none">{{ display.slice(0, 5) }}<span class="text-[32px] text-mute">.{{ display.slice(6) }}</span></span>
          <span class="text-xl text-mute mt-2">{{ label }}</span>
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
