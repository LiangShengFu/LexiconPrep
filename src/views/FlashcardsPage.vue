<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

interface Card {
  id: string; user_id: string; front: string; back: string
  subject: string | null; difficulty: number; review_count: number
  next_review_at: string; created_at: string
}

const cards = ref<Card[]>([])
const loading = ref(false)
const currentIndex = ref(0)
const flipped = ref(false)
const filterSubject = ref('all')
const showCreate = ref(false)
const newFront = ref('')
const newBack = ref('')
const newSubject = ref('')
const creating = ref(false)

const loadCards = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = { limit: 100 }
    if (filterSubject.value !== 'all') params.subject = filterSubject.value
    const { data } = await api.get('/flashcards', { params })
    cards.value = data
  } catch { useUiStore().addToast('加载闪卡失败', 'error') }
  finally { loading.value = false }
}

watch(filterSubject, () => { currentIndex.value = 0; flipped.value = false; loadCards() })
onMounted(loadCards)

const subjects = computed(() => [...new Set(cards.value.map(c => c.subject).filter(Boolean))] as string[])
const currentCard = computed(() => cards.value[currentIndex.value])
const hasCards = computed(() => cards.value.length > 0)

const flip = () => { flipped.value = !flipped.value }
const nextCard = () => { flipped.value = false; currentIndex.value = currentIndex.value < cards.value.length - 1 ? currentIndex.value + 1 : 0 }
const prevCard = () => { flipped.value = false; currentIndex.value = currentIndex.value > 0 ? currentIndex.value - 1 : cards.value.length - 1 }

const createCard = async () => {
  if (!newFront.value || !newBack.value) return
  creating.value = true
  try {
    await api.post('/flashcards', { front: newFront.value, back: newBack.value, subject: newSubject.value || null })
    newFront.value = ''; newBack.value = ''; newSubject.value = ''; showCreate.value = false
    await loadCards()
    currentIndex.value = cards.value.length - 1
    useUiStore().addToast('闪卡已创建', 'success')
  } catch { useUiStore().addToast('创建失败', 'error') }
  finally { creating.value = false }
}

const reviewCard = async (remembered: boolean) => {
  if (!currentCard.value) return
  try {
    await api.post(`/flashcards/${currentCard.value.id}/review`, null, { params: { remembered } })
    await loadCards()
  } catch { useUiStore().addToast('操作失败', 'error') }
  nextCard()
}

const deleteCard = async (id: string) => {
  try {
    await api.delete(`/flashcards/${id}`)
    await loadCards()
    useUiStore().addToast('已删除', 'success')
  } catch { useUiStore().addToast('删除失败', 'error') }
}
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">间隔重复</p>
      <h1 class="text-display-sm text-ink">闪卡</h1>
    </div>

    <div class="flex flex-wrap items-center gap-2 justify-between">
      <div class="flex flex-wrap gap-2">
        <button class="btn-pill-outline cursor-target text-xs" :class="{ 'border-ink bg-canvas-soft': filterSubject === 'all' }" @click="filterSubject = 'all'">全部</button>
        <button v-for="s in subjects" :key="s" class="btn-pill-outline cursor-target text-xs" :class="{ 'border-ink bg-canvas-soft': filterSubject === s }" @click="filterSubject = s">{{ s }}</button>
      </div>
      <button class="btn-pill-filled cursor-target text-sm" @click="showCreate = true">创建闪卡</button>
    </div>

    <div v-if="hasCards" class="flex flex-col items-center">
      <div class="w-full max-w-[600px] aspect-[3/2] cursor-pointer" @click="flip">
        <div class="relative w-full h-full transition-transform duration-500" :style="{ transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)', transformStyle: 'preserve-3d' }">
          <div class="absolute inset-0 card-xai flex flex-col justify-center items-center p-10" :style="{ backfaceVisibility: 'hidden' }">
            <span v-if="currentCard.subject" class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute font-mono uppercase mb-4">{{ currentCard.subject }}</span>
            <p class="text-display-xs text-ink text-center font-normal leading-relaxed">{{ currentCard.front }}</p>
            <span class="text-mute text-xs mt-6">点击翻转</span>
          </div>
          <div class="absolute inset-0 card-xai flex flex-col justify-center items-center p-10 bg-canvas-soft" :style="{ transform: 'rotateY(180deg)', backfaceVisibility: 'hidden' }">
            <span class="eyebrow-mono-sm text-mute mb-4">答案</span>
            <p class="text-lg text-ink text-center font-normal leading-relaxed">{{ currentCard.back }}</p>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-4 mt-6">
        <button class="btn-pill-outline cursor-target text-sm" @click="prevCard">上一张</button>
        <span class="text-mute text-sm">{{ currentIndex + 1 }} / {{ filteredCards.length }}</span>
        <button class="btn-pill-outline cursor-target text-sm" @click="nextCard">下一张</button>
      </div>
      <div class="flex items-center gap-3 mt-4">
        <button class="btn-pill-outline cursor-target text-sm border-red-500/30 text-red-400 hover:border-red-500" @click="reviewCard(false)">再复习</button>
        <button class="btn-pill-filled cursor-target text-sm" @click="reviewCard(true)">记住了</button>
      </div>
    </div>

    <div v-else-if="!loading" class="card-xai text-center py-12">
      <p class="text-mute text-sm">暂无闪卡，开始创建吧！</p>
      <button class="btn-pill-filled cursor-target mt-4 text-sm" @click="showCreate = true">创建闪卡</button>
    </div>

    <div v-if="showCreate" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="showCreate = false">
      <div class="card-xai w-full max-w-[440px] mx-4 space-y-4">
        <p class="eyebrow-mono-sm text-mute">新建闪卡</p>
        <div><label class="block text-body text-sm mb-2">正面（问题）</label><input v-model="newFront" type="text" placeholder="输入问题..." class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" /></div>
        <div><label class="block text-body text-sm mb-2">背面（答案）</label><input v-model="newBack" type="text" placeholder="输入答案..." class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" /></div>
        <div><label class="block text-body text-sm mb-2">学科（可选）</label><input v-model="newSubject" type="text" placeholder="如：政治" class="w-full bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink" /></div>
        <div class="flex gap-3 pt-2">
          <button class="btn-pill-outline cursor-target flex-1 text-sm" @click="showCreate = false">取消</button>
          <button class="btn-pill-filled cursor-target flex-1 text-sm" :disabled="creating" @click="createCard">{{ creating ? '创建中...' : '创建' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
