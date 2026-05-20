<script setup lang="ts">
import { ref, computed, watch } from 'vue'
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
  id: string; question_id: string; wrong_count: number
  last_review_at: string | null; next_review_at: string
  question_content: string | null; question_subject: string | null
}

const resources = ref<Resource[]>([])
const mistakes = ref<MistakeItem[]>([])
const loading = ref(false)
const error = ref('')

const subjects = ['政治', '英语', '数学', '计算机科学', '法学', '心理学']
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
  await api.delete(`/mistakes/${id}`)
  mistakes.value = mistakes.value.filter(m => m.id !== id)
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
    <div class="flex gap-4 border-b border-hairline pb-0">
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
          class="flex-1 bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm placeholder:text-mute focus:outline-none focus:border-ink transition-colors" />
        <select v-model="selectedSubject" class="bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm">
          <option value="all">全部学科</option>
          <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
        </select>
        <select v-model="selectedType" class="bg-canvas-soft border border-hairline rounded-card px-4 py-2.5 text-ink text-sm">
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
            <span class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute">{{ r.type }}</span>
            <span class="text-mute text-xs">{{ r.year }}</span>
          </div>
          <h3 class="text-ink text-base font-normal leading-snug">{{ r.title }}</h3>
          <p v-if="r.description" class="text-mute text-xs leading-relaxed line-clamp-2">{{ r.description }}</p>
          <div class="flex items-center justify-between mt-auto pt-2 border-t border-hairline">
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
        <div v-for="m in mistakes" :key="m.id" class="card-xai flex items-start justify-between gap-4 group cursor-target">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs px-2 py-0.5 rounded-full border border-hairline text-mute">{{ m.question_subject }}</span>
              <span class="text-xs text-mute">错 {{ m.wrong_count }} 次</span>
              <span class="text-xs text-mute">下次复习: {{ formatDate(m.next_review_at) }}</span>
            </div>
            <p class="text-body text-sm truncate">{{ m.question_content }}</p>
          </div>
          <button class="text-mute text-xs hover:text-red-400 transition-colors shrink-0 mt-1" @click="deleteMistake(m.id)">删除</button>
        </div>
      </div>
    </template>
  </div>
</template>
