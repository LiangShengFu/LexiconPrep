<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import api from '@/api/client'

const activeTab = ref<'resources' | 'mistakes'>('resources')
const search = ref('')
const selectedSubject = ref('all')
const selectedType = ref('all')

interface Resource {
  id: string; title: string; description: string | null; type: string
  subject: string; year: number | null; size: number; downloads: number; file_url: string
}
interface MistakeItem {
  id: string; question_id: string; wrong_count: number; review_count: number | null
  last_review_at: string | null; next_review_at: string
  question_content: string | null; question_subject: string | null
  mastered: boolean | null
}

const resources = ref<Resource[]>([])
const mistakes = ref<MistakeItem[]>([])
const loading = ref(false)
const error = ref('')

const subjects = ref<string[]>(['政治', '英语', '数学', '计算机科学', '法学', '心理学'])

const fetchSubjects = async () => {
  try {
    const { data } = await api.get('/questions/subjects')
    if (data.length) subjects.value = data
  } catch { /* keep defaults */ }
}

onMounted(() => { fetchSubjects() })
const types = ['PDF', 'DOC', 'VIDEO']

const loadResources = async () => {
  loading.value = true; error.value = ''
  try {
    const params: Record<string, any> = { limit: 50 }
    if (selectedSubject.value !== 'all') params.subject = selectedSubject.value
    if (selectedType.value !== 'all') params.type = selectedType.value
    if (search.value) params.search = search.value
    const { data } = await api.get('/resources', { params })
    resources.value = data
  } catch { error.value = '加载资源失败' }
  finally { loading.value = false }
}

const loadMistakes = async () => {
  loading.value = true; error.value = ''
  try {
    const { data } = await api.get('/mistakes')
    mistakes.value = data
  } catch { error.value = '加载错题失败' }
  finally { loading.value = false }
}

const deleteMistake = async (id: string) => {
  try {
    await api.delete(`/mistakes/${id}`)
    mistakes.value = mistakes.value.filter(m => m.id !== id)
    useUiStore().addToast('已删除', 'success')
  } catch {
    useUiStore().addToast('删除失败', 'error')
  }
}

const reviewMistake = async (id: string, remembered: boolean) => {
  try {
    await api.post(`/mistakes/${id}/review`, null, { params: { remembered } })
    if (remembered) {
      mistakes.value = mistakes.value.filter(m => m.id !== id)
      useUiStore().addToast('已标记为掌握', 'success')
    } else {
      const m = mistakes.value.find(m => m.id === id)
      if (m) {
        m.wrong_count += 1
        m.review_count = (m.review_count || 0) + 1
      }
      useUiStore().addToast('已重新安排复习', 'success')
    }
  } catch {
    useUiStore().addToast('操作失败', 'error')
  }
}

watch(activeTab, (tab) => {
  if (tab === 'resources') loadResources()
  else loadMistakes()
}, { immediate: true })

let debounceTimer: ReturnType<typeof setTimeout>
watch([search, selectedSubject, selectedType], () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => loadResources(), 300)
})

const formatSize = (mb: number) => mb >= 1000 ? `${(mb / 1000).toFixed(1)} GB` : `${mb} MB`
const formatDate = (d: string) => new Date(d).toLocaleDateString('zh-CN')
</script>

<template>
  <div class="p-8 space-y-6">
    <div>
      <p class="eyebrow-mono-sm mb-2">学习资源</p>
      <h1 class="text-display-sm text-ink">资源库</h1>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 border-b-4 border-dashed border-hairline pb-0">
      <button class="pb-3 text-sm border-b-2 transition-colors -mb-[1px]"
        :class="activeTab === 'resources' ? 'border-ink text-ink' : 'border-transparent text-mute hover:text-body'"
        @click="activeTab = 'resources'">资源库</button>
      <button class="pb-3 text-sm border-b-2 transition-colors -mb-[1px]"
        :class="activeTab === 'mistakes' ? 'border-ink text-ink' : 'border-transparent text-mute hover:text-body'"
        @click="activeTab = 'mistakes'">错题本</button>
    </div>

    <!-- Resources Tab -->
    <template v-if="activeTab === 'resources'">
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="search" type="text" placeholder="搜索资源..."
          class="flex-1 bg-canvas-soft border-4 border-dashed border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors" />
        <select v-model="selectedSubject" class="bg-canvas-soft border-4 border-dashed border-hairline rounded-card px-4 py-2.5 text-ink text-sm">
          <option value="all">全部学科</option>
          <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
        </select>
        <select v-model="selectedType" class="bg-canvas-soft border-4 border-dashed border-hairline rounded-card px-4 py-2.5 text-ink text-sm">
          <option value="all">全部类型</option>
          <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>

      <div v-if="loading" class="text-mute text-sm py-12 text-center">加载中...</div>
      <div v-else-if="error" class="text-red-400 text-sm py-12 text-center">{{ error }}</div>
      <div v-else-if="!resources.length" class="card-xai text-center py-12">
        <p class="text-mute text-sm">未找到匹配的资源。</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="r in resources" :key="r.id" class="card-xai flex flex-col gap-3 group cursor-target hover:border-canvas-mid transition-colors">
          <div class="flex items-start justify-between">
            <span class="text-xs px-2 py-0.5 rounded-full border-4 border-dashed border-hairline text-mute">{{ r.type }}</span>
            <span class="text-mute text-xs">{{ r.year }}</span>
          </div>
          <h3 class="text-ink text-base font-normal leading-snug">{{ r.title }}</h3>
          <p v-if="r.description" class="text-mute text-xs leading-relaxed line-clamp-2">{{ r.description }}</p>
          <div class="flex items-center justify-between mt-auto pt-2 border-t-4 border-dashed border-hairline">
            <span class="text-mute text-xs">{{ formatSize(r.size) }}</span>
            <span class="text-mute text-xs">{{ r.downloads.toLocaleString() }} 次下载</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Mistakes Tab -->
    <template v-if="activeTab === 'mistakes'">
      <div v-if="loading" class="text-mute text-sm py-12 text-center">加载中...</div>
      <div v-else-if="!mistakes.length" class="card-xai text-center py-16">
        <p class="text-mute text-sm mb-2">错题本为空</p>
        <p class="text-mute text-xs">做题时答错的题目会自动加入这里。</p>
      </div>
      <div v-else class="space-y-3">
        <div v-for="m in mistakes" :key="m.id" class="card-xai flex items-start justify-between gap-4 group">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs px-2 py-0.5 rounded-full border-4 border-dashed border-hairline text-mute">{{ m.question_subject }}</span>
              <span class="text-xs text-mute">错 {{ m.wrong_count }} 次</span>
              <span v-if="m.review_count" class="text-xs text-mute">复习 {{ m.review_count }} 次</span>
              <span class="text-xs text-mute">下次复习: {{ formatDate(m.next_review_at) }}</span>
            </div>
            <p class="text-body text-sm truncate">{{ m.question_content }}</p>
          </div>
          <div class="flex items-center gap-2 shrink-0 mt-1">
            <button class="btn-pill-filled cursor-target text-xs px-3 py-1" @click="reviewMistake(m.id, true)">已掌握</button>
            <button class="btn-pill-outline cursor-target text-xs px-3 py-1" @click="reviewMistake(m.id, false)">再复习</button>
            <button class="text-mute text-xs hover:text-red-400 transition-colors" @click="deleteMistake(m.id)">删除</button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
