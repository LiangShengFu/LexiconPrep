<script setup lang="ts">
import { gsap } from 'gsap'
import { onMounted, onBeforeUnmount, ref, useTemplateRef, watch } from 'vue'

interface TargetCursorProps {
  targetSelector?: string
  spinDuration?: number
  hideDefaultCursor?: boolean
}

const props = withDefaults(defineProps<TargetCursorProps>(), {
  targetSelector: '.cursor-target',
  spinDuration: 2,
  hideDefaultCursor: false,
})

const cursorRef = useTemplateRef('cursorRef')
const cornersRef = ref<NodeListOf<HTMLDivElement> | null>(null)
const spinTl = ref<gsap.core.Timeline | null>(null)

const constants = { borderWidth: 3, cornerSize: 12, parallaxStrength: 0.00005 }

const moveCursor = (x: number, y: number) => {
  if (!cursorRef.value) return
  gsap.to(cursorRef.value, { x, y, duration: 0.1, ease: 'power3.out' })
}

let cleanupAnimation: () => void = () => {}

const setupAnimation = () => {
  if (!cursorRef.value) return
  const originalCursor = document.body.style.cursor
  if (props.hideDefaultCursor) document.body.style.cursor = 'none'

  const cursor = cursorRef.value
  cornersRef.value = cursor.querySelectorAll<HTMLDivElement>('.target-cursor-corner')

  let activeTarget: Element | null = null
  let currentTargetMove: ((ev: Event) => void) | null = null
  let currentLeaveHandler: (() => void) | null = null
  let isAnimatingToTarget = false
  let resumeTimeout: ReturnType<typeof setTimeout> | null = null

  const cleanupTarget = (target: Element) => {
    if (currentTargetMove) target.removeEventListener('mousemove', currentTargetMove)
    if (currentLeaveHandler) target.removeEventListener('mouseleave', currentLeaveHandler)
    currentTargetMove = null; currentLeaveHandler = null
  }

  gsap.set(cursor, { xPercent: -50, yPercent: -50, x: window.innerWidth / 2, y: window.innerHeight / 2, opacity: 1, display: 'block' })

  const createSpinTimeline = () => {
    if (spinTl.value) spinTl.value.kill()
    spinTl.value = gsap.timeline({ repeat: -1 }).to(cursor, { rotation: '+=360', duration: props.spinDuration, ease: 'none' })
  }
  createSpinTimeline()

  const handleGlobalMouseMove = (e: MouseEvent) => moveCursor(e.clientX, e.clientY)

  const handleGlobalMouseOver = (e: MouseEvent) => {
    const directTarget = e.target as Element
    const allTargets: Element[] = []
    let current = directTarget
    while (current && current !== document.body) {
      if (current.matches(props.targetSelector)) allTargets.push(current)
      current = current.parentElement!
    }
    const target = allTargets[0] || null
    if (!target || !cursorRef.value || !cornersRef.value) return
    if (activeTarget === target) return
    if (activeTarget) cleanupTarget(activeTarget)
    if (resumeTimeout) { clearTimeout(resumeTimeout); resumeTimeout = null }

    activeTarget = target
    const corners = Array.from(cornersRef.value)
    corners.forEach(c => gsap.killTweensOf(c))
    gsap.killTweensOf(cursorRef.value, 'rotation')
    spinTl.value?.pause()
    gsap.set(cursorRef.value, { rotation: 0 })

    const updateCorners = (mouseX?: number, mouseY?: number) => {
      const rect = target.getBoundingClientRect()
      const cursorRect = cursorRef.value!.getBoundingClientRect()
      const cx = cursorRect.left + cursorRect.width / 2
      const cy = cursorRect.top + cursorRect.height / 2
      const [tlc, trc, brc, blc] = Array.from(cornersRef.value!)
      const { borderWidth, cornerSize, parallaxStrength } = constants
      const offsets = [
        { x: rect.left - cx - borderWidth, y: rect.top - cy - borderWidth },
        { x: rect.right - cx + borderWidth - cornerSize, y: rect.top - cy - borderWidth },
        { x: rect.right - cx + borderWidth - cornerSize, y: rect.bottom - cy + borderWidth - cornerSize },
        { x: rect.left - cx - borderWidth, y: rect.bottom - cy + borderWidth - cornerSize },
      ]
      if (mouseX !== undefined && mouseY !== undefined) {
        const tcx = rect.left + rect.width / 2; const tcy = rect.top + rect.height / 2
        const mx = (mouseX - tcx) * parallaxStrength; const my = (mouseY - tcy) * parallaxStrength
        offsets.forEach(o => { o.x += mx; o.y += my })
      }
      const tl = gsap.timeline();
      [tlc, trc, brc, blc].forEach((c, i) => {
        tl.to(c as HTMLElement, { x: offsets[i].x, y: offsets[i].y, duration: 0.2, ease: 'power2.out' }, 0)
      })
    }

    isAnimatingToTarget = true; updateCorners()
    setTimeout(() => { isAnimatingToTarget = false }, 1)

    let moveThrottle: number | null = null
    currentTargetMove = (ev: Event) => {
      if (moveThrottle || isAnimatingToTarget) return
      moveThrottle = requestAnimationFrame(() => {
        updateCorners((ev as MouseEvent).clientX, (ev as MouseEvent).clientY)
        moveThrottle = null
      })
    }
    currentLeaveHandler = () => {
      activeTarget = null; isAnimatingToTarget = false
      if (cornersRef.value) {
        const corners = Array.from(cornersRef.value); gsap.killTweensOf(corners)
        const pos = [{ x: -18, y: -18 }, { x: 6, y: -18 }, { x: 6, y: 6 }, { x: -18, y: 6 }]
        const tl = gsap.timeline()
        corners.forEach((c, i) => tl.to(c as HTMLElement, { x: pos[i].x, y: pos[i].y, duration: 0.3, ease: 'power3.out' }, 0))
      }
      resumeTimeout = setTimeout(() => {
        if (!activeTarget && cursorRef.value && spinTl.value) {
          const cr = gsap.getProperty(cursorRef.value, 'rotation') as number; const nr = cr % 360
          spinTl.value.kill()
          spinTl.value = gsap.timeline({ repeat: -1 }).to(cursorRef.value, { rotation: '+=360', duration: props.spinDuration, ease: 'none' })
          gsap.to(cursorRef.value, { rotation: nr + 360, duration: props.spinDuration * (1 - nr / 360), ease: 'none', onComplete: () => spinTl.value?.restart() })
        }
        resumeTimeout = null
      }, 50)
      cleanupTarget(target)
    }
    target.addEventListener('mousemove', currentTargetMove)
    target.addEventListener('mouseleave', currentLeaveHandler)
  }

  window.addEventListener('mousemove', handleGlobalMouseMove)
  window.addEventListener('mouseover', handleGlobalMouseOver, { passive: true })

  cleanupAnimation = () => {
    window.removeEventListener('mousemove', handleGlobalMouseMove)
    window.removeEventListener('mouseover', handleGlobalMouseOver)
    if (activeTarget) cleanupTarget(activeTarget)
    if (resumeTimeout) clearTimeout(resumeTimeout)
    spinTl.value?.kill(); spinTl.value = null
    if (cursorRef.value) gsap.killTweensOf(cursorRef.value)
    if (cornersRef.value) gsap.killTweensOf(Array.from(cornersRef.value))
    if (cursorRef.value) gsap.set(cursorRef.value, { x: 0, y: 0, rotation: 0, opacity: 0, display: 'none' })
    document.body.style.cursor = originalCursor
    activeTarget = null
  }
}

onMounted(() => setupAnimation())
onBeforeUnmount(() => cleanupAnimation())
watch(() => [props.targetSelector, props.spinDuration, props.hideDefaultCursor], () => { cleanupAnimation(); setupAnimation() })
</script>

<template>
  <div ref="cursorRef"
    class="top-0 left-0 z-[9999] fixed w-0 h-0 -translate-x-1/2 -translate-y-1/2 pointer-events-none mix-blend-difference opacity-0"
    :style="{ willChange: 'transform' }">
    <div class="top-1/2 left-1/2 absolute bg-white rounded-full w-1 h-1 -translate-x-1/2 -translate-y-1/2" />
    <div class="top-1/2 left-1/2 absolute border-[3px] border-white border-r-0 border-b-0 w-3 h-3 -translate-x-[150%] -translate-y-[150%] target-cursor-corner" />
    <div class="top-1/2 left-1/2 absolute border-[3px] border-white border-b-0 border-l-0 w-3 h-3 -translate-y-[150%] translate-x-1/2 target-cursor-corner" />
    <div class="top-1/2 left-1/2 absolute border-[3px] border-white border-t-0 border-l-0 w-3 h-3 translate-x-1/2 translate-y-1/2 target-cursor-corner" />
    <div class="top-1/2 left-1/2 absolute border-[3px] border-white border-t-0 border-r-0 w-3 h-3 -translate-x-[150%] translate-y-1/2 target-cursor-corner" />
  </div>
</template>
