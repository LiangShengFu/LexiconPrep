<script setup lang="ts">
import { ref, computed, onUnmounted, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const savedWork = parseInt(localStorage.getItem('pomodoro_work') || '25')
const savedBreak = parseInt(localStorage.getItem('pomodoro_break') || '5')

const workMinutes = ref(savedWork)
const breakMinutes = ref(savedBreak)
const isWork = ref(true)
const running = ref(false)
const minimized = ref(true)

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
  running.value = true; minimized.value = false
  startStamp = Date.now()
  remainAtStart = remainMs.value
  timer = setInterval(tick, 16)
}
const pause = () => { running.value = false; if (timer) { clearInterval(timer); timer = null } }
const reset = () => { pause(); remainMs.value = totalMs.value }
const switchMode = () => {
  isWork.value = !isWork.value
  remainMs.value = totalMs.value
  running.value = false
  if (timer) { clearInterval(timer); timer = null }
}
const toggleMinimize = () => { minimized.value = !minimized.value }

const miniCanvasRef = ref<HTMLCanvasElement | null>(null)
let miniAnimFrame = 0
let miniOrbitTick = 0

function isDark() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

function drawMiniArc(ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number, startAngle: number, endAngle: number, color: string, lw: number, dash: number[] = []) {
  ctx.save()
  ctx.beginPath()
  ctx.arc(cx, cy, r, startAngle, endAngle)
  ctx.strokeStyle = color
  ctx.lineWidth = lw
  ctx.setLineDash(dash)
  ctx.stroke()
  ctx.restore()
}

function drawMiniTick(ctx: CanvasRenderingContext2D, cx: number, cy: number, r1: number, r2: number, angle: number, color: string, lw: number) {
  ctx.save()
  ctx.beginPath()
  ctx.moveTo(cx + Math.cos(angle) * r1, cy + Math.sin(angle) * r1)
  ctx.lineTo(cx + Math.cos(angle) * r2, cy + Math.sin(angle) * r2)
  ctx.strokeStyle = color
  ctx.lineWidth = lw
  ctx.stroke()
  ctx.restore()
}

function drawMiniCanvas() {
  const canvas = miniCanvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const W = 100, H = 100, CX = W / 2, CY = H / 2
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
    const r1 = isMaj ? 43 : 45
    const r2 = 47
    drawMiniTick(ctx, CX, CY, r1, r2, a, isMaj ? accent2 : (dark ? 'rgba(175,169,236,0.35)' : 'rgba(83,74,183,0.25)'), isMaj ? 1 : 0.5)
  }

  drawMiniArc(ctx, CX, CY, 40, 0, Math.PI * 2, faint1, 4)
  const progAngle = RAD + prog * Math.PI * 2
  drawMiniArc(ctx, CX, CY, 40, RAD, progAngle, accent1, 4)

  ctx.save()
  ctx.beginPath()
  ctx.arc(CX + Math.cos(progAngle) * 40, CY + Math.sin(progAngle) * 40, 3, 0, Math.PI * 2)
  ctx.fillStyle = accent1
  ctx.fill()
  ctx.restore()

  drawMiniArc(ctx, CX, CY, 34, 0, Math.PI * 2, faint2, 2.5)
  const secFrac = (remainMs.value / 1000) % 60 / 60
  const secAngle = RAD + secFrac * Math.PI * 2
  drawMiniArc(ctx, CX, CY, 34, RAD, secAngle, accent2, 2.5)

  ctx.save()
  ctx.beginPath()
  ctx.arc(CX + Math.cos(secAngle) * 34, CY + Math.sin(secAngle) * 34, 2, 0, Math.PI * 2)
  ctx.fillStyle = accent2
  ctx.fill()
  ctx.restore()

  drawMiniArc(ctx, CX, CY, 28, 0, Math.PI * 2, dark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)', 0.5, [2, 3])

  const orbitAngle = (miniOrbitTick * 0.3) % 360
  const oRad = orbitAngle * Math.PI / 180
  ctx.save()
  ctx.beginPath()
  ctx.arc(CX, CY, 48, oRad, oRad + Math.PI * 0.25)
  ctx.strokeStyle = dark ? 'rgba(175,169,236,0.25)' : 'rgba(83,74,183,0.15)'
  ctx.lineWidth = 0.5
  ctx.stroke()
  ctx.beginPath()
  ctx.arc(CX, CY, 48, oRad + Math.PI, oRad + Math.PI * 1.25)
  ctx.stroke()
  ctx.restore()

  miniOrbitTick++
  miniAnimFrame = requestAnimationFrame(drawMiniCanvas)
}

onMounted(() => {
  nextTick(() => { drawMiniCanvas() })
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  if (miniAnimFrame) cancelAnimationFrame(miniAnimFrame)
})
</script>

<template>
  <button v-if="minimized"
    class="fixed bottom-6 right-6 z-40 w-12 h-12 rounded-full bg-canvas-card border-4 border-dashed border-hairline flex items-center justify-center hover:border-ink transition-colors cursor-target"
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
      <canvas ref="miniCanvasRef" width="100" height="100" class="w-full h-full" />
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-lg text-ink font-mono">{{ display.slice(0, 5) }}<span class="text-xs text-mute">.{{ display.slice(6) }}</span></span>
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
